"""Agent manifest — single agent definition.

See ``docs/APEX - Design and Build/APEX_Design.md`` §8.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from apex_core.manifests.base import BaseManifest
from apex_core.types import Classification, GitSha, ManifestName, ModelPin, Practice


class ScopeSpec(BaseModel):
    """Composition defining an agent's effective view (APEX_Design §8.2).

    The visibility lattice evaluates ``tenant × practice × persona ×
    classification × row_filter`` at tool-call time.
    """

    model_config = ConfigDict(extra="forbid")

    tenant: str | None = Field(None, description="L4 tenant constraint (None = any).")
    practice: Practice | None = Field(None, description="L3 Practice constraint.")
    persona: ManifestName | None = Field(None, description="Persona binding.")
    classification_visibility: list[Classification] = Field(
        default_factory=list,
        description="Classifications this agent is permitted to see.",
    )
    row_filters: dict[str, str] = Field(
        default_factory=dict,
        description="Tenant-specific attribute predicates (e.g. region='US-WEST').",
    )


class AgentManifest(BaseManifest):
    """Agent manifest — pins model, prompt, tool allow-list, and scope."""

    kind: Literal["agent"] = "agent"
    persona: ManifestName | None = None
    model_pin: ModelPin = Field(..., description="Foundry-deployed model id.")
    system_prompt_sha: GitSha = Field(
        ...,
        description="Git SHA of the system-prompt / few-shot bundle.",
    )
    tool_allow_list: list[str] = Field(
        default_factory=list,
        description="Fully-qualified MCP tool identifiers this agent may invoke.",
    )
    scope: ScopeSpec = Field(default_factory=ScopeSpec)
    temperature: float | None = Field(None, ge=0.0, le=2.0)
    max_tokens: int | None = Field(None, gt=0)
