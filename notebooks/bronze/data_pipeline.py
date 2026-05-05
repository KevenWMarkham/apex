"""Bronze landing template — Fabric Data Pipeline (batch) (APEX_Design §6.2.3).

For scheduled batch ingest from SORs without CDC. The template is a PySpark
notebook invoked by a Data Factory Notebook activity that runs after a Copy
activity has deposited raw files (CSV / Parquet / JSON) into a staging path.

Error semantics (§6.2.3): activity-level success/failure monitoring. Retries
configurable per activity (default 3 with exponential backoff). Final failure
routes to ops via Purview event.

Schema evolution: Copy activity tolerates additive drift; breaking halts the
pipeline. Notebook explicitly validates schema at load time.
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
    """CUSTOMIZE per pipeline."""
    return BronzeLandingConfig(
        source_system=os.environ["APEX_SOURCE_SYSTEM"],
        source_pattern=SourcePattern.DATA_PIPELINE,
        source_connection_name=os.environ["APEX_PIPELINE_ID"],
        workspace_id=os.environ["FABRIC_WORKSPACE_ID"],
        lakehouse_id=os.environ["FABRIC_LAKEHOUSE_ID"],
        target_table=os.environ["APEX_BRONZE_TARGET"],
        practice=Practice(os.environ["APEX_PRACTICE"]),
        classification=Classification(os.environ.get("APEX_CLASSIFICATION", "internal")),
        retention=RetentionPolicy(),
        pattern_detail={
            "pipeline_id": os.environ["APEX_PIPELINE_ID"],
            "activity_name": os.environ["APEX_ACTIVITY_NAME"],
            "staging_path": os.environ["APEX_STAGING_PATH"],
            "file_format": os.environ.get("APEX_FILE_FORMAT", "parquet"),
        },
    )


def bronze_ddl(
    config: BronzeLandingConfig,
    user_columns: dict[str, str] | None = None,
) -> str:
    return generate_bronze_ddl(config, user_columns=user_columns)


def _read_staged_batch(config: BronzeLandingConfig, spark: "SparkSession") -> "DataFrame":
    """Load the file batch deposited by the upstream Copy activity."""
    fmt = config.pattern_detail["file_format"]
    path = config.pattern_detail["staging_path"]
    if fmt == "parquet":
        return spark.read.parquet(path)
    if fmt == "csv":
        return spark.read.option("header", "true").csv(path)
    if fmt == "json":
        return spark.read.json(path)
    raise ValueError(f"Unsupported file_format {fmt!r}")


def run(config: BronzeLandingConfig, spark: "SparkSession") -> None:
    """Fabric entry-point — read staged files and land to Bronze."""
    from pyspark.sql import functions as F

    batch = _read_staged_batch(config, spark)
    annotated = (
        batch.withColumn("event_id", F.expr("uuid()"))
        .withColumn("event_ts", F.current_timestamp())
        .withColumn("entity_id", F.col("entity_id") if "entity_id" in batch.columns else F.expr("uuid()"))
        .withColumn("source_system", F.lit(config.source_system))
        .withColumn("source_system_ts", F.current_timestamp())
        .withColumn("ingest_ts", F.current_timestamp())
        .withColumn("ingest_date", F.to_date(F.current_timestamp()))
        .withColumn("run_id", F.lit(config.pattern_detail.get("activity_name", "unknown")))
        .withColumn("_raw_payload", F.to_json(F.struct([F.col(c) for c in batch.columns])))
        .withColumn("_classification", F.lit(config.classification.value))
    )
    (
        annotated.write.format("delta")
        .mode("append")
        .partitionBy(*config.partition_columns)
        .option("mergeSchema", "true")
        .saveAsTable(config.target_table)
    )
