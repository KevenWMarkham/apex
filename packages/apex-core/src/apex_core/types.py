"""Shared types and enums used across apex-core.

Every manifest module imports from here to avoid circular dependencies and to
centralise the vocabulary used in APEX's L1 contract.

See ``docs/APEX - Design and Build/APEX_Design.md`` §2–§3, §9.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated

from pydantic import StringConstraints


class Classification(StrEnum):
    """Purview sensitivity taxonomy (APEX_Design §5.7)."""

    PUBLIC = "public"
    INTERNAL = "internal"
    PII = "pii"
    PHI = "phi"
    PCI = "pci"
    SOX = "sox"
    EXPORT_CONTROLLED = "export_controlled"
    TRADE_SECRET = "trade_secret"
    MEMBER_ONLY = "member_only"


class BumpClass(StrEnum):
    """SemVer bump classification (APEX_Design §3.3)."""

    PATCH = "PATCH"
    MINOR = "MINOR"
    MAJOR = "MAJOR"


class GateKind(StrEnum):
    """HITL gate kind (APEX_Design §9.1)."""

    ZERO_TOUCH = "ZERO_TOUCH"
    ACK_ONLY = "ACK_ONLY"
    HITL = "HITL"
    ESCALATION = "ESCALATION"


class GateVariant(StrEnum):
    """Orchestration-scoped gate variant (APEX_Design §9.2)."""

    HARD = "hard"
    SOFT = "soft"
    POLICY = "policy"
    ESCALATION = "escalation"


class Practice(StrEnum):
    """APEX L3 Practices (APEX_Design §15)."""

    RC = "rc"
    HLS = "hls"
    ER = "er"
    AXLE = "axle"
    TMT = "tmt"
    TH = "th"
    ICE = "ice"


class OrchestrationPattern(StrEnum):
    """Four primitive orchestration patterns (APEX_Design §10.2)."""

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"
    FEEDBACK_LOOP = "feedback_loop"


class HitlMode(StrEnum):
    """Three-mode human oversight spectrum (APEX_Design §17)."""

    HITL = "HITL"
    HOTL = "HOTL"
    HIC = "HIC"


# --- Constrained string aliases ----------------------------------------------

ManifestName = Annotated[
    str,
    StringConstraints(
        pattern=r"^[a-z][a-z0-9_-]*$",
        min_length=2,
        max_length=80,
    ),
]
"""Stable lowercase identifier (kebab or snake case)."""

GitSha = Annotated[
    str,
    StringConstraints(pattern=r"^[0-9a-f]{7,40}$"),
]
"""Git commit SHA (short or full)."""

ModelPin = Annotated[
    str,
    StringConstraints(min_length=3, max_length=120),
]
"""Foundry-deployed model identifier, e.g. ``gpt-4.1-2025-06-15``."""
