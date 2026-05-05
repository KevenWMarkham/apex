"""Tenant manifest — L4 client instance pinning an L3 Practice release.

See ``docs/APEX - Design and Build/APEX_Design.md`` §3.4.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from apex_core.manifests.base import BaseManifest
from apex_core.types import GateKind, ManifestName, Practice


class PracticePin(BaseModel):
    """Pin to a specific L3 Practice release."""

    model_config = ConfigDict(extra="forbid")

    practice: Practice
    release: str = Field(..., description="SemVer release of the Practice.")


class ExtensionRef(BaseModel):
    """Tenant-scoped extension to an L3 artefact."""

    model_config = ConfigDict(extra="forbid")

    target_kind: Literal["schema", "agent", "service", "orchestration"]
    target_name: ManifestName
    overlay: dict[str, Any] = Field(
        default_factory=dict,
        description="Additive fields / overrides; CI rejects breaking overlays.",
    )


class PolicyOverride(BaseModel):
    """Tenant-scoped override of a default gate mapping."""

    model_config = ConfigDict(extra="forbid")

    service: ManifestName
    gate_kind: GateKind
    rationale: str = Field(..., min_length=1, description="Why the override is justified.")


class TenantManifest(BaseManifest):
    """Tenant manifest — an L4 client instance."""

    kind: Literal["tenant"] = "tenant"
    practice_pin: PracticePin
    service_subscriptions: list[ManifestName] = Field(default_factory=list)
    extensions: list[ExtensionRef] = Field(default_factory=list)
    policy_overrides: list[PolicyOverride] = Field(default_factory=list)
    region: str | None = Field(None, description="Azure region (e.g. eastus2).")
