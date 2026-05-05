"""Three-version rule (Section 11.7).

Every audit row pins three Git SHAs: ``manifest_version``, ``policy_version``,
``prompt_version``. Plus the Foundry-deployed ``model_version`` (a model
identifier string, not a Git SHA, but emitted on the same row).

The stamper resolves these at *pre-invocation* and freezes them onto the
row-in-progress so post-hoc manifest edits cannot retroactively alter the
recorded rule-set.
"""

from __future__ import annotations

from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field


class VersionStamps(BaseModel):
    """The four version stamps on every audit row."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    manifest_version: str = Field(min_length=1)
    policy_version: str = Field(min_length=1)
    prompt_version: str = Field(min_length=1)
    model_version: str = Field(min_length=1)


class VersionResolver(Protocol):
    """Looks up the effective SHAs for an orchestration at invocation time."""

    def resolve(
        self, *, orchestration_name: str, tenant_id: str
    ) -> VersionStamps: ...


class StaticVersionResolver:
    """Dev/test resolver that returns a fixed set of stamps.

    Production wires this to the Fabric/Git registry that holds the
    manifest, policy, and prompt bundles.
    """

    def __init__(self, stamps: VersionStamps) -> None:
        self._stamps = stamps

    def resolve(
        self, *, orchestration_name: str, tenant_id: str
    ) -> VersionStamps:
        del orchestration_name, tenant_id
        return self._stamps


def stamp_versions(
    resolver: VersionResolver,
    *,
    orchestration_name: str,
    tenant_id: str,
) -> VersionStamps:
    """Freeze the three-version rule onto the row before the agent runs."""
    return resolver.resolve(
        orchestration_name=orchestration_name,
        tenant_id=tenant_id,
    )
