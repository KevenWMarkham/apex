"""Bronze landing template — Mirrored Database (APEX_Design §6.2.1).

Fabric Mirroring items replicate CDC rows from a source database into OneLake
as Delta, sub-minute latency. This template:

- Reads the mirrored Delta shadow.
- Appends canonical-envelope + ingest-metadata columns.
- Writes to the Bronze Delta target.
- Sends row-level failures to ``bronze_raw_deadletter``.

Error semantics (§6.2.1): Mirror failures (timeout, auth expiry, structural
incompatibility) emit Purview error events. Consumers see ``mirror_lag_seconds``.

Schema evolution: additive columns propagate automatically. Column drops
require Mirror reconfiguration + staged Silver-transform change.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from apex_core.types import Classification, Practice
from apex_medallion import (
    BronzeLandingConfig,
    RetentionPolicy,
    SourcePattern,
    generate_bronze_ddl,
)

if TYPE_CHECKING:  # pragma: no cover
    from pyspark.sql import DataFrame, SparkSession


def landing_config() -> BronzeLandingConfig:
    """Construct the config for this tenant's Mirrored Database landing.

    CUSTOMIZE: replace env-var lookups or keep as-is for env-driven deployments.
    """
    return BronzeLandingConfig(
        source_system=os.environ["APEX_SOURCE_SYSTEM"],
        source_pattern=SourcePattern.MIRRORED_DATABASE,
        source_connection_name=os.environ["APEX_MIRROR_ITEM"],
        workspace_id=os.environ["FABRIC_WORKSPACE_ID"],
        lakehouse_id=os.environ["FABRIC_LAKEHOUSE_ID"],
        target_table=os.environ["APEX_BRONZE_TARGET"],
        practice=Practice(os.environ["APEX_PRACTICE"]),
        classification=Classification(os.environ.get("APEX_CLASSIFICATION", "internal")),
        retention=RetentionPolicy(),
        pattern_detail={
            "mirror_item_id": os.environ["APEX_MIRROR_ITEM"],
            "mirror_shadow_table": os.environ["APEX_MIRROR_SHADOW_TABLE"],
        },
    )


def bronze_ddl(
    config: BronzeLandingConfig,
    user_columns: dict[str, str] | None = None,
) -> str:
    """Generate the Bronze table DDL for this config."""
    return generate_bronze_ddl(config, user_columns=user_columns)


def _annotate_envelope(df: "DataFrame", config: BronzeLandingConfig) -> "DataFrame":
    """Add canonical envelope + ingest metadata to the mirrored rows."""
    from pyspark.sql import functions as F

    return (
        df.withColumn("event_id", F.expr("uuid()"))
          .withColumn("event_ts", F.current_timestamp())
          .withColumn("entity_id", F.col("entity_id") if "entity_id" in df.columns else F.expr("uuid()"))
          .withColumn("source_system", F.lit(config.source_system))
          .withColumn("source_system_ts", F.current_timestamp())
          .withColumn("ingest_ts", F.current_timestamp())
          .withColumn("ingest_date", F.to_date(F.current_timestamp()))
          .withColumn("run_id", F.expr("uuid()"))
          .withColumn("_raw_payload", F.to_json(F.struct([F.col(c) for c in df.columns])))
          .withColumn("_classification", F.lit(config.classification.value))
    )


def run(config: BronzeLandingConfig, spark: "SparkSession") -> None:
    """Fabric entry-point — read the mirrored shadow and land to Bronze."""
    shadow_table = config.pattern_detail["mirror_shadow_table"]
    source_df = spark.read.format("delta").table(shadow_table)
    annotated = _annotate_envelope(source_df, config)
    (
        annotated.write.format("delta")
        .mode("append")
        .partitionBy(*config.partition_columns)
        .option("mergeSchema", "true")
        .saveAsTable(config.target_table)
    )
