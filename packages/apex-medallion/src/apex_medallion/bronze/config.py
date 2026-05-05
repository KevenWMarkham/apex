"""``BronzeLandingConfig`` — the parameter bag for every Bronze notebook template."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

from apex_core.types import Classification, Practice

from apex_medallion.bronze.retention import RetentionPolicy


class SourcePattern(StrEnum):
    """Which of the five Bronze landing patterns a template implements."""

    MIRRORED_DATABASE = "mirrored_database"
    EVENTSTREAM = "eventstream"
    DATA_PIPELINE = "data_pipeline"
    DATAFLOW_GEN2 = "dataflow_gen2"
    CUSTOM_ENDPOINT = "custom_endpoint"


class BronzeLandingConfig(BaseModel):
    """Parameterises a Bronze landing notebook / pipeline.

    Every Bronze template accepts one of these and drives all configuration
    from it — no hard-coded constants inside the notebook bodies.
    """

    model_config = ConfigDict(extra="forbid")

    # --- Source identity ----------------------------------------------------
    source_system: str = Field(..., description="Stable identifier of the SOR.")
    source_pattern: SourcePattern
    source_connection_name: str = Field(
        ..., description="Fabric / Azure connection reference used by the template.",
    )

    # --- Target identity ----------------------------------------------------
    workspace_id: str = Field(..., description="Fabric workspace id.")
    lakehouse_id: str = Field(..., description="Fabric lakehouse id.")
    target_table: str = Field(
        ...,
        description="Qualified Bronze table, e.g. 'bronze_scml.sku'.",
    )
    partition_columns: list[str] = Field(
        default_factory=lambda: ["ingest_date"],
        description="Columns to partition the Delta table by.",
    )

    # --- Governance ---------------------------------------------------------
    practice: Practice
    classification: Classification = Field(
        Classification.INTERNAL,
        description=(
            "Most-restrictive classification across source columns. Applied "
            "to the Bronze table as a default; per-column overrides happen "
            "in Silver."
        ),
    )
    retention: RetentionPolicy = Field(default_factory=RetentionPolicy)

    # --- Error handling -----------------------------------------------------
    deadletter_table: str = Field(
        "bronze_raw_deadletter",
        description="Target for failed payloads. Defaults to the canonical name.",
    )
    max_retries: int = Field(3, ge=0, le=10)
    retry_backoff_seconds: int = Field(60, ge=0)

    # --- Pattern-specific detail (free-form; pattern-specific key names) ----
    pattern_detail: dict[str, str] = Field(
        default_factory=dict,
        description=(
            "Pattern-specific config. Examples: "
            "mirrored_database → {'mirror_item_id': '...'}; "
            "eventstream → {'topic': 'rc/cold-chain'}; "
            "data_pipeline → {'pipeline_id': 'pl-42', 'activity_name': 'copy-sku'}; "
            "dataflow_gen2 → {'dataflow_id': '...', 'watermark_column': 'updated_at'}; "
            "custom_endpoint → {'function_url': 'https://...', 'signature_header': 'X-Signature'}."
        ),
    )
