"""Base manifest — fields every APEX manifest kind carries.

See ``docs/APEX - Design and Build/APEX_Design.md`` §3.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from apex_core.semver import SemVer
from apex_core.types import ManifestName, Practice

ManifestKind = Literal[
    "schema",
    "event",
    "orchestration",
    "agent",
    "tenant",
    "policy",
    "service",
]
"""The seven recognised manifest kinds (L1 contract)."""


class BaseManifest(BaseModel):
    """Fields common to every APEX manifest.

    Subclasses override ``kind`` with a ``Literal`` discriminator and add
    kind-specific fields.
    """

    model_config = ConfigDict(extra="forbid")

    kind: ManifestKind = Field(..., description="Manifest discriminator.")
    name: ManifestName = Field(..., description="Stable lowercase identifier.")
    version: str = Field(..., description="SemVer string (major.minor.patch).")
    owner: str = Field(..., min_length=1, description="Responsible team or individual.")
    practice: Practice | None = Field(
        None,
        description="L3 Practice binding; None for L1/L2 artefacts.",
    )
    description: str = Field("", description="Short human description.")
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Extensible free-form metadata.",
    )

    @field_validator("version")
    @classmethod
    def _validate_version(cls, value: str) -> str:
        """Reject manifests whose ``version`` field isn't valid SemVer."""
        SemVer.parse(value)  # raises ValueError on bad input
        return value

    def semver(self) -> SemVer:
        """Return the parsed ``version`` as a :class:`SemVer` instance."""
        return SemVer.parse(self.version)
