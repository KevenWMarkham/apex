"""Orchestration manifest — multi-agent composition with governance.

See ``docs/APEX - Design and Build/APEX_Design.md`` §10.4.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from apex_core.manifests.base import BaseManifest
from apex_core.types import GateKind, GateVariant, GitSha, ManifestName, OrchestrationPattern


class VersionStamps(BaseModel):
    """The three Git SHAs that every audit row must pin (APEX_Design §11.7)."""

    model_config = ConfigDict(extra="forbid")

    manifest_version: GitSha
    policy_version: GitSha
    prompt_version: GitSha


class AgentRef(BaseModel):
    """Reference to an agent within an orchestration."""

    model_config = ConfigDict(extra="forbid")

    agent: ManifestName = Field(..., description="Name of a registered AgentManifest.")
    agent_version: str = Field(..., description="SemVer pin.")
    step_id: ManifestName = Field(..., description="Step identifier unique within orchestration.")
    depends_on: list[ManifestName] = Field(
        default_factory=list,
        description="Step IDs that must complete first (for parallel/hierarchical flows).",
    )


class GatePlacement(BaseModel):
    """HITL gate placement within an orchestration."""

    model_config = ConfigDict(extra="forbid")

    at_step: ManifestName = Field(..., description="Step ID this gate fires on.")
    kind: GateKind
    variant: GateVariant = GateVariant.HARD
    approver_group: str | None = Field(
        None,
        description="Entra group that approves; required for HITL/ESCALATION kinds.",
    )


class OrchestrationManifest(BaseManifest):
    """Orchestration manifest — composes agents into a governed workflow."""

    kind: Literal["orchestration"] = "orchestration"
    archetype_id: str | None = Field(
        None,
        description="One of the 47 APEX archetype IDs this orchestration specialises.",
    )
    pattern: OrchestrationPattern
    triggers: list[ManifestName] = Field(
        default_factory=list,
        description="Event manifest names that fire this orchestration.",
    )
    agents: list[AgentRef] = Field(..., min_length=1)
    gates: list[GatePlacement] = Field(default_factory=list)
    stamps: VersionStamps
