"""Service manifest — named, productised APEX capability.

See ``docs/APEX - Design and Build/APEX_Design.md`` §15, §16.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from apex_core.manifests.base import BaseManifest
from apex_core.types import HitlMode, ManifestName


class KpiRef(BaseModel):
    """Reference to a KPI in the KPI master registry (Appendix C)."""

    model_config = ConfigDict(extra="forbid")

    kpi_id: ManifestName
    target: str = Field(..., description="Target value or threshold (free-form).")


class SloSpec(BaseModel):
    """Service-level objective for the service."""

    model_config = ConfigDict(extra="forbid")

    latency_ms_p95: int | None = Field(None, gt=0)
    freshness_seconds: int | None = Field(None, gt=0)
    availability_pct: float | None = Field(None, ge=0.0, le=100.0)


class CommercialSpec(BaseModel):
    """Commercial envelope metadata (APEX_Design §16.3)."""

    model_config = ConfigDict(extra="forbid")

    wave: Literal[1, 2, 3]
    envelope_usd_low: int | None = Field(None, ge=0)
    envelope_usd_high: int | None = Field(None, ge=0)
    delivery_weeks_low: int | None = Field(None, gt=0)
    delivery_weeks_high: int | None = Field(None, gt=0)


class ServiceManifest(BaseManifest):
    """Service manifest — the productised unit of APEX value delivery."""

    kind: Literal["service"] = "service"
    persona: ManifestName = Field(
        ..., description="Primary persona that consumes this service."
    )
    hitl_mode: HitlMode = HitlMode.HITL
    kpis: list[KpiRef] = Field(default_factory=list)
    slo: SloSpec | None = None
    commercial: CommercialSpec | None = None
    orchestrations: list[ManifestName] = Field(
        default_factory=list,
        description="Orchestration manifests that implement this service.",
    )
    agents: list[ManifestName] = Field(
        default_factory=list,
        description="Agent manifests invoked by this service.",
    )
    schema_refs: list[ManifestName] = Field(
        default_factory=list,
        description="Canonical schema families consumed.",
    )
