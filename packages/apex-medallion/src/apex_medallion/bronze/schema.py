"""Bronze DDL generator — canonical envelope + ``_raw_payload`` + user columns.

The Bronze contract (APEX_Design §6.2) requires every row to carry:

- the canonical envelope (``event_id``, ``event_ts``, ``entity_id``,
  ``source_system``, ``source_system_ts``)
- an ``ingest_ts`` (when the row landed) + ``ingest_date`` (partition default)
- ``_raw_payload`` — the source message as JSON text
- ``run_id`` — Fabric pipeline / notebook run correlation id

Plus any user columns the template projected from the source.
"""

from __future__ import annotations

from apex_medallion.bronze.config import BronzeLandingConfig

_ENVELOPE_COLUMNS = """  event_id                 STRING NOT NULL,
  event_ts                 TIMESTAMP NOT NULL,
  entity_id                STRING NOT NULL,
  source_system            STRING NOT NULL,
  source_system_ts         TIMESTAMP NOT NULL,"""

_INGEST_COLUMNS = """  ingest_ts                TIMESTAMP NOT NULL,
  ingest_date              DATE NOT NULL,
  run_id                   STRING NOT NULL,"""

_RAW_PAYLOAD_COLUMN = """  _raw_payload             STRING,"""


def generate_bronze_ddl(
    config: BronzeLandingConfig,
    *,
    user_columns: dict[str, str] | None = None,
    database: str | None = None,
) -> str:
    """Return a ``CREATE TABLE`` DDL for the Bronze landing target.

    Args:
        config: Bronze landing config.
        user_columns: Optional additional columns the template projects from
            the source (mapping column name → Delta type). If omitted, Bronze
            is envelope + raw-payload only.
        database: Override database / schema prefix.

    Returns:
        Semicolon-terminated ``CREATE TABLE ... USING DELTA`` statement.
    """
    qualified = f"{database}.{config.target_table}" if database else config.target_table

    user_column_lines = ""
    if user_columns:
        user_column_lines = "\n".join(
            f"  {name:<24} {dtype}," for name, dtype in user_columns.items()
        ) + "\n"

    partition_clause = ""
    if config.partition_columns:
        partition_clause = (
            f"\nPARTITIONED BY ({', '.join(config.partition_columns)})"
        )

    return f"""CREATE TABLE {qualified} (
{_ENVELOPE_COLUMNS}
{_INGEST_COLUMNS}
{user_column_lines}{_RAW_PAYLOAD_COLUMN}
  _classification          STRING NOT NULL
)
USING DELTA{partition_clause}
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'apex.medallion.layer' = 'bronze',
  'apex.source_system' = '{config.source_system}',
  'apex.source_pattern' = '{config.source_pattern.value}',
  'apex.practice' = '{config.practice.value}',
  'apex.classification' = '{config.classification.value}'
);"""
