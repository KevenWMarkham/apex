"""Direct Lake semantic-model binder (APEX_Design §6.5).

Sprint 6 scope: emit a readable TMDL-flavoured descriptor for each Practice's
anchor semantic model. Tenant Power BI engineers import the descriptor into
a real ``.tmdl`` file; the descriptor is reviewed + versioned in Git.

Full programmatic TMDL generation is deferred until a tenant requests
notebook-driven semantic-model publishing.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from apex_medallion.gold import (
    SemanticModelSpec,
    TableSpec,
    render_tmdl,
)
from apex_medallion.gold.rc_measures import (
    PERIOD_OVER_PERIOD_PCT_DAX,
    rc_measure_registry,
)

if TYPE_CHECKING:  # pragma: no cover
    from pyspark.sql import SparkSession


def rc_semantic_model() -> SemanticModelSpec:
    """RC Practice anchor — SCML / MERML / CXML over Direct Lake."""
    _ = rc_measure_registry()  # keeps import used; extend per table as needed
    return SemanticModelSpec(
        model_name="ApexRc",
        tables=(
            TableSpec(
                name="SKU",
                silver_delta_path="onelake://<workspace>/silver_scml.sku",
                columns=(
                    "sku_key", "sku_natural", "gtin", "sku_status",
                    "category_key", "supplier_key", "unit_retail",
                    "effective_margin_pct",
                ),
                measures=(PERIOD_OVER_PERIOD_PCT_DAX,),
            ),
            TableSpec(
                name="Price",
                silver_delta_path="onelake://<workspace>/silver_merml.price",
                columns=("sku_key", "amount", "currency", "effective_from", "effective_to"),
            ),
            TableSpec(
                name="Customer",
                silver_delta_path="onelake://<workspace>/silver_cxml.customer",
                columns=(
                    "customer_natural", "status", "full_name_token",
                    "email_token", "consent_marketing",
                ),
            ),
        ),
        notes="APEX RC anchor semantic model. PII/PHI fields are tokenised.",
    )


def write_tmdl_to_file(spec: SemanticModelSpec, output_path: Path) -> None:
    """Render ``spec`` and write it to disk for Power BI engineer import."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_tmdl(spec), encoding="utf-8")


def run(spark: "SparkSession") -> None:
    """Fabric entry-point — refresh the Direct Lake semantic model.

    Sprint 6 ships only the descriptor. Actual refresh is triggered by
    Power BI / Fabric tooling; the notebook can call the refresh API when
    the model is already published.
    """
    _ = spark  # future: spark.sql("REFRESH TABLE silver_scml.sku") etc
    spec = rc_semantic_model()
    print(f"Anchor semantic model: {spec.model_name}")  # noqa: T201
    print(f"Tables: {[t.name for t in spec.tables]}")  # noqa: T201
    print(f"Total DAX measures: {spec.total_measures()}")  # noqa: T201
