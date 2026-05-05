"""Policy manifest — HITL / DLP / classification-mapping rules.

See ``docs/APEX - Design and Build/APEX_Design.md`` §9, §14.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from apex_core.manifests.base import BaseManifest
from apex_core.types import BumpClass, Classification, GateKind, GateVariant, ManifestName


class HitlRule(BaseModel):
    """Default gate mapping for a bump classification."""

    model_config = ConfigDict(extra="forbid")

    bump_class: BumpClass
    gate_kind: GateKind
    variant: GateVariant = GateVariant.HARD


class DlpRule(BaseModel):
    """Label-based redaction rule applied across surfaces."""

    model_config = ConfigDict(extra="forbid")

    classification: Classification
    action: Literal["mask", "tokenise", "drop", "allow"]
    surfaces: list[Literal["agent_output", "copilot", "power_bi", "teams_card"]] = Field(
        default_factory=list
    )


class ClassificationMapping(BaseModel):
    """Binding from an attribute path to a Purview sensitivity label."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(
        ..., description="Dotted attribute path, e.g. 'cxml.customer.email'."
    )
    classification: Classification


class PolicyManifest(BaseManifest):
    """Policy manifest — governs HITL gates, DLP rules, and classification labels."""

    kind: Literal["policy"] = "policy"
    hitl_rules: list[HitlRule] = Field(default_factory=list)
    dlp_rules: list[DlpRule] = Field(default_factory=list)
    classification_mappings: list[ClassificationMapping] = Field(default_factory=list)
    scope: list[ManifestName] = Field(
        default_factory=list,
        description="Service names this policy applies to; empty = all.",
    )
