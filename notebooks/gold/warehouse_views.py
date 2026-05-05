"""Fabric Warehouse Gold T-SQL view materialisation (APEX_Design §6.5).

Generates + executes ``CREATE OR ALTER VIEW`` statements for each Practice's
Gold projection. Every view definition is SHA-stampable for audit-row
``view_definition_sha`` — MCP tool calls backed by these views record the
SHA in the audit row's ``tools_called.result_hash``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from apex_medallion.gold import (
    MeasureLanguage,
    generate_warehouse_view,
)
from apex_medallion.gold.rc_measures import rc_measure_registry
from apex_medallion.gold.warehouse import view_definition_sha

if TYPE_CHECKING:  # pragma: no cover
    from pyspark.sql import SparkSession


# --- CUSTOMIZE per Practice / entity ----------------------------------------

# Import the canonical entity classes we're generating views for.
from apex_scml import SKU  # type: ignore[import-not-found]
from apex_merml import Price  # type: ignore[import-not-found]

VIEW_DEFINITIONS = [
    {
        "view_name": "v_sku",
        "silver_table": "silver_scml.sku",
        "entity": SKU,
    },
    {
        "view_name": "v_price",
        "silver_table": "silver_merml.price",
        "entity": Price,
    },
]

# --- end customize ----------------------------------------------------------


def generate_all() -> list[tuple[str, str, str]]:
    """Generate DDLs for every configured view.

    Returns:
        List of ``(view_name, ddl, sha)`` tuples — emitted to the notebook
        output for review + captured in the audit row.
    """
    registry = rc_measure_registry()
    tsql_measures = registry.list_by_language(MeasureLanguage.TSQL)
    results: list[tuple[str, str, str]] = []
    for v in VIEW_DEFINITIONS:
        ddl = generate_warehouse_view(
            v["entity"],
            view_name=v["view_name"],
            silver_table=v["silver_table"],
            measures=tsql_measures,
        )
        results.append((v["view_name"], ddl, view_definition_sha(ddl)))
    return results


def run(spark: "SparkSession") -> None:
    """Generate view DDLs and apply them via the Warehouse T-SQL endpoint."""
    for view_name, ddl, sha in generate_all():
        print(f"-- {view_name} (sha: {sha[:12]}...)")  # noqa: T201
        print(ddl)  # noqa: T201
        print()  # noqa: T201
        # spark.sql(ddl)  # uncomment in production — requires Warehouse T-SQL endpoint
