"""Bronze landing template — Dataflow Gen2 (REST / SaaS) (APEX_Design §6.2.4).

Dataflow Gen2 uses Power Query (M) connectors for 100+ SaaS sources
(Salesforce, Workday, ServiceNow, Jira, HubSpot, ...). Incremental refresh
is watermark-driven. This Python template pairs with the Power Query M
definition — it post-processes the materialised Dataflow output into the
APEX Bronze shape.

Error semantics (§6.2.4): connector errors (rate limit, auth, timeout)
surface in Dataflow run-history. Auto-retry with exponential backoff; final
failure routes to ops.

Watermark strategy: each run tracks ``last_success_ts`` in a metadata table;
the next Dataflow refresh filters ``updated_at > last_success_ts``.
"""

from __future__ import annotations

import os
from datetime import datetime
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
    """CUSTOMIZE per SaaS source."""
    return BronzeLandingConfig(
        source_system=os.environ["APEX_SOURCE_SYSTEM"],
        source_pattern=SourcePattern.DATAFLOW_GEN2,
        source_connection_name=os.environ["APEX_DATAFLOW_ID"],
        workspace_id=os.environ["FABRIC_WORKSPACE_ID"],
        lakehouse_id=os.environ["FABRIC_LAKEHOUSE_ID"],
        target_table=os.environ["APEX_BRONZE_TARGET"],
        practice=Practice(os.environ["APEX_PRACTICE"]),
        classification=Classification(os.environ.get("APEX_CLASSIFICATION", "internal")),
        retention=RetentionPolicy(),
        pattern_detail={
            "dataflow_id": os.environ["APEX_DATAFLOW_ID"],
            "dataflow_output_table": os.environ["APEX_DATAFLOW_OUTPUT"],
            "watermark_column": os.environ.get("APEX_WATERMARK_COLUMN", "updated_at"),
            "watermark_table": os.environ.get("APEX_WATERMARK_TABLE", "apex_bronze_watermarks"),
        },
    )


def bronze_ddl(
    config: BronzeLandingConfig,
    user_columns: dict[str, str] | None = None,
) -> str:
    return generate_bronze_ddl(config, user_columns=user_columns)


def read_watermark(config: BronzeLandingConfig, spark: "SparkSession") -> datetime | None:
    """Look up the last-success timestamp for this (source, target) pair."""
    wm_table = config.pattern_detail["watermark_table"]
    try:
        row = (
            spark.read.table(wm_table)
            .where(
                f"source_system = '{config.source_system}' "
                f"AND target_table = '{config.target_table}'"
            )
            .orderBy("run_ts", ascending=False)
            .limit(1)
            .collect()
        )
        if row:
            return row[0]["last_success_ts"]
    except Exception:  # noqa: BLE001 — watermark table may not yet exist
        return None
    return None


def write_watermark(
    config: BronzeLandingConfig,
    spark: "SparkSession",
    *,
    last_success_ts: datetime,
) -> None:
    """Advance the watermark after a successful run."""
    from pyspark.sql import Row

    wm_table = config.pattern_detail["watermark_table"]
    rows = [
        Row(
            source_system=config.source_system,
            target_table=config.target_table,
            last_success_ts=last_success_ts,
            run_ts=datetime.utcnow(),
        )
    ]
    df = spark.createDataFrame(rows)
    df.write.format("delta").mode("append").saveAsTable(wm_table)


def run(config: BronzeLandingConfig, spark: "SparkSession") -> None:
    """Read Dataflow Gen2 output, filter by watermark, land to Bronze."""
    from pyspark.sql import functions as F

    df = spark.read.table(config.pattern_detail["dataflow_output_table"])
    watermark_col = config.pattern_detail["watermark_column"]
    last_success = read_watermark(config, spark)
    if last_success is not None and watermark_col in df.columns:
        df = df.filter(F.col(watermark_col) > F.lit(last_success))

    annotated = (
        df.withColumn("event_id", F.expr("uuid()"))
          .withColumn("event_ts", F.col(watermark_col) if watermark_col in df.columns else F.current_timestamp())
          .withColumn("entity_id", F.col("id") if "id" in df.columns else F.expr("uuid()"))
          .withColumn("source_system", F.lit(config.source_system))
          .withColumn("source_system_ts", F.col(watermark_col) if watermark_col in df.columns else F.current_timestamp())
          .withColumn("ingest_ts", F.current_timestamp())
          .withColumn("ingest_date", F.to_date(F.current_timestamp()))
          .withColumn("run_id", F.expr("uuid()"))
          .withColumn("_raw_payload", F.to_json(F.struct([F.col(c) for c in df.columns])))
          .withColumn("_classification", F.lit(config.classification.value))
    )
    (
        annotated.write.format("delta")
        .mode("append")
        .partitionBy(*config.partition_columns)
        .option("mergeSchema", "true")
        .saveAsTable(config.target_table)
    )
    write_watermark(config, spark, last_success_ts=datetime.utcnow())
