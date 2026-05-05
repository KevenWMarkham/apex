"""Eventhouse KQL function materialisation for real-time Gold (APEX_Design §6.5).

For each streaming Silver Eventhouse table, we emit a ``.create-or-alter
function`` that projects canonical columns + KQL post-measures. Agents query
via MCP, which in turn queries Eventhouse.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from apex_medallion.gold import (
    MeasureLanguage,
    generate_kql_function,
)
from apex_medallion.gold.rc_measures import rc_measure_registry

if TYPE_CHECKING:  # pragma: no cover
    from pyspark.sql import SparkSession


# --- CUSTOMIZE per Practice / entity ----------------------------------------

from apex_scml import SKU  # type: ignore[import-not-found]

KQL_FUNCTIONS = [
    {
        "function_name": "fn_sku_stream",
        "silver_table": "silver_scml_sku_kql",
        "entity": SKU,
    },
]

# --- end customize ----------------------------------------------------------


def generate_all_kql() -> list[tuple[str, str]]:
    """Generate KQL function bodies for every configured function."""
    registry = rc_measure_registry()
    kql_measures = registry.list_by_language(MeasureLanguage.KQL)
    results: list[tuple[str, str]] = []
    for f in KQL_FUNCTIONS:
        kql = generate_kql_function(
            f["entity"],
            function_name=f["function_name"],
            silver_table=f["silver_table"],
            measures=kql_measures,
        )
        results.append((f["function_name"], kql))
    return results


def run(spark: "SparkSession") -> None:
    """Emit KQL function bodies (notebook must be run against an Eventhouse)."""
    for function_name, kql in generate_all_kql():
        print(f"// function {function_name}")  # noqa: T201
        print(kql)  # noqa: T201
        print()  # noqa: T201
        # spark.sql(...) won't submit KQL; use Eventhouse SDK in production.
