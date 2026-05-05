"""Event manifest — trigger + payload shape + classification.

See ``docs/APEX - Design and Build/APEX_Design.md`` §4.2, §10.1, §13.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from apex_core.manifests.base import BaseManifest
from apex_core.types import Classification, ManifestName


class TriggerSpec(BaseModel):
    """How an event is raised."""

    model_config = ConfigDict(extra="forbid")

    source: Literal[
        "mirrored_database",
        "eventstream",
        "data_pipeline",
        "dataflow_gen2",
        "custom_endpoint",
        "data_activator",
        "schedule",
        "manual",
    ]
    source_system: str | None = Field(
        None, description="SOR name if the trigger originates outside APEX."
    )
    detail: dict[str, Any] = Field(
        default_factory=dict,
        description="Trigger-specific config (cron expression, topic name, activator rule, ...).",
    )


class EventManifest(BaseManifest):
    """Event manifest — describes an event that drives an orchestration."""

    kind: Literal["event"] = "event"
    trigger: TriggerSpec
    payload_schema: dict[str, Any] | str = Field(
        ...,
        description="Inline JSON schema or reference path to a schema manifest.",
    )
    classification: Classification = Classification.INTERNAL
    entity_refs: list[ManifestName] = Field(
        default_factory=list,
        description="Canonical entities this event concerns (for lineage).",
    )
