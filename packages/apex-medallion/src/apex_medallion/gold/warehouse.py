"""Warehouse T-SQL view generator.

Emits a ``CREATE OR ALTER VIEW`` for a Pydantic canonical entity plus any
post-measures defined in T-SQL. The output is Fabric Warehouse-compatible
T-SQL. View definitions are SHA-stampable for audit-row traceability
(APEX_Design §11 tools_called.result_hash for Warehouse-backed tool reads).
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable

from pydantic import BaseModel

from apex_medallion.gold.measure import MeasureDefinition, MeasureLanguage


def generate_warehouse_view(
    entity_cls: type[BaseModel],
    *,
    view_name: str,
    silver_table: str,
    schema: str = "gold",
    measures: Iterable[MeasureDefinition] | None = None,
    classification_column: bool = True,
) -> str:
    """Generate a ``CREATE OR ALTER VIEW`` T-SQL statement.

    Args:
        entity_cls: Pydantic entity whose fields form the base projection.
        view_name: Target view name (without schema).
        silver_table: Fully qualified Silver source table.
        schema: Target database / schema for the view.
        measures: Post-measures to append. Only ``MeasureLanguage.TSQL`` are
            included; the rest are filtered out silently.
        classification_column: If True, include ``_classification`` in the
            projection (propagates the Silver column into Gold).

    Returns:
        A ``CREATE OR ALTER VIEW ... AS SELECT ... FROM ...;`` statement.
    """
    column_lines: list[str] = []
    for name in entity_cls.model_fields:
        column_lines.append(f"  {name}")
    if classification_column:
        column_lines.append("  _classification")

    if measures:
        for m in measures:
            if m.language is not MeasureLanguage.TSQL:
                continue
            column_lines.append(f"  ({m.formula}) AS {m.name}")

    body = ",\n".join(column_lines)
    return (
        f"CREATE OR ALTER VIEW {schema}.{view_name} AS\n"
        f"SELECT\n{body}\n"
        f"FROM {silver_table};"
    )


def view_definition_sha(ddl: str) -> str:
    """Return a hex SHA-256 of the view DDL for audit-row stamping."""
    return hashlib.sha256(ddl.encode("utf-8")).hexdigest()
