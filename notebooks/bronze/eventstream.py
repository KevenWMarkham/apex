"""Bronze landing template — Eventstream → Eventhouse (APEX_Design §6.2.2).

For high-volume real-time events (Event Hubs / Kafka / MQTT / webhook). The
template illustrates the Eventhouse KQL table pattern AND the Delta
checkpoint pattern many APEX tenants use in parallel for Silver consumers.

Error semantics (§6.2.2): parse failures route to ``bronze_raw_deadletter``
with original payload, error class, and retry count. Sustained dead-lettering
pages platform-ops via the KQL dashboard.

Schema evolution: Eventhouse tolerates drift via ``.ingest inline``; structural
changes update the table policy. Hard-type changes require operator approval.
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
    from pyspark.sql.streaming import StreamingQuery


def landing_config() -> BronzeLandingConfig:
    """CUSTOMIZE per stream source."""
    return BronzeLandingConfig(
        source_system=os.environ["APEX_SOURCE_SYSTEM"],
        source_pattern=SourcePattern.EVENTSTREAM,
        source_connection_name=os.environ["APEX_EVENTSTREAM_ID"],
        workspace_id=os.environ["FABRIC_WORKSPACE_ID"],
        lakehouse_id=os.environ["FABRIC_LAKEHOUSE_ID"],
        target_table=os.environ["APEX_BRONZE_TARGET"],
        practice=Practice(os.environ["APEX_PRACTICE"]),
        classification=Classification(os.environ.get("APEX_CLASSIFICATION", "internal")),
        retention=RetentionPolicy(),
        pattern_detail={
            "eventstream_id": os.environ["APEX_EVENTSTREAM_ID"],
            "eventhouse_kql_table": os.environ["APEX_EVENTHOUSE_KQL_TABLE"],
            "checkpoint_path": os.environ["APEX_CHECKPOINT_PATH"],
            "trigger_interval": os.environ.get("APEX_TRIGGER_INTERVAL", "30 seconds"),
        },
    )


def bronze_ddl(config: BronzeLandingConfig) -> str:
    """Delta shadow DDL for Silver consumers that prefer Delta over KQL."""
    return generate_bronze_ddl(
        config,
        user_columns={
            "event_type": "STRING",
            "partition_key": "STRING",
        },
    )


def run(config: BronzeLandingConfig, spark: "SparkSession") -> "StreamingQuery":
    """Structured Streaming read of the Eventstream → Delta checkpoint."""
    from pyspark.sql import functions as F

    stream_df = (
        spark.readStream.format("eventhubs")
        .option("eventhubs.connectionString", config.pattern_detail["eventstream_id"])
        .load()
    )
    annotated = (
        stream_df.withColumn("event_id", F.expr("uuid()"))
        .withColumn("event_ts", F.col("enqueuedTime"))
        .withColumn("entity_id", F.col("partitionKey"))
        .withColumn("source_system", F.lit(config.source_system))
        .withColumn("source_system_ts", F.col("enqueuedTime"))
        .withColumn("ingest_ts", F.current_timestamp())
        .withColumn("ingest_date", F.to_date(F.current_timestamp()))
        .withColumn("run_id", F.expr("uuid()"))
        .withColumn("_raw_payload", F.col("body").cast("string"))
        .withColumn("_classification", F.lit(config.classification.value))
    )
    return (
        annotated.writeStream.format("delta")
        .option("checkpointLocation", config.pattern_detail["checkpoint_path"])
        .outputMode("append")
        .trigger(processingTime=config.pattern_detail["trigger_interval"])
        .toTable(config.target_table)
    )
