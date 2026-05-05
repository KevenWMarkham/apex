"""Dead-letter schema + DDL for Bronze ingestion failures.

Every Bronze pattern emits failed payloads to ``bronze_raw_deadletter`` so
ops can replay / diagnose without polluting the source-fidelity table.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field

DEAD_LETTER_TABLE = "bronze_raw_deadletter"


class DeadLetterRecord(BaseModel):
    """One row in ``bronze_raw_deadletter``."""

    model_config = ConfigDict(extra="forbid")

    dead_letter_id: UUID = Field(default_factory=uuid4)
    source_system: str = Field(..., description="Which SOR produced the failed payload.")
    source_pattern: str = Field(
        ..., description="Landing pattern (mirrored_database, eventstream, ...).",
    )
    target_table: str = Field(
        ..., description="Intended Bronze target table, for audit.",
    )
    occurred_at: datetime
    error_class: str = Field(
        ..., description="Exception class name (e.g. 'ParseError', 'AuthExpired').",
    )
    error_message: str
    retry_count: int = Field(0, ge=0)
    payload_raw: str = Field(
        "",
        description=(
            "Raw payload as UTF-8 (truncated to 1 MB upstream). Binary payloads "
            "are base64-encoded before writing."
        ),
    )
    run_id: str | None = Field(
        None,
        description="Fabric pipeline / notebook run-id for cross-reference.",
    )


def dead_letter_ddl(database: str | None = None) -> str:
    """Return the ``CREATE TABLE`` DDL for the dead-letter table."""
    name = DEAD_LETTER_TABLE
    qualified = f"{database}.{name}" if database else name
    return f"""CREATE TABLE {qualified} (
  dead_letter_id           STRING NOT NULL,
  source_system            STRING NOT NULL,
  source_pattern           STRING NOT NULL,
  target_table             STRING NOT NULL,
  occurred_at              TIMESTAMP NOT NULL,
  error_class              STRING NOT NULL,
  error_message            STRING NOT NULL,
  retry_count              INT NOT NULL,
  payload_raw              STRING,
  run_id                   STRING
)
USING DELTA
PARTITIONED BY (source_system)
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'apex.medallion.layer' = 'bronze_deadletter'
);"""
