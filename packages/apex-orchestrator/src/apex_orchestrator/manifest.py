"""Orchestration manifest runtime — three-version-stamp enforcement."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class MissingVersionStampsError(ValueError):
    """Raised when an orchestration manifest is loaded without the three required SHAs."""


@dataclass(frozen=True, slots=True)
class StampedManifest:
    """A manifest whose three Git SHAs have been validated."""

    name: str
    manifest_version: str
    policy_version: str
    prompt_version: str
    raw: dict[str, Any]


def load_manifest_with_stamps(payload: dict[str, Any]) -> StampedManifest:
    """Load an orchestration manifest dict and enforce the three-version rule.

    Any missing or empty stamp raises :class:`MissingVersionStampsError` —
    runtime rejects the manifest (APEX_Design §11.7). Callers should
    propagate this to CI so broken manifests never reach production.
    """
    name = payload.get("name")
    if not isinstance(name, str) or not name:
        raise MissingVersionStampsError("Manifest missing 'name'.")
    stamps = payload.get("stamps")
    if not isinstance(stamps, dict):
        raise MissingVersionStampsError(f"Manifest {name!r} missing 'stamps' object.")

    missing = [
        field
        for field in ("manifest_version", "policy_version", "prompt_version")
        if not isinstance(stamps.get(field), str) or not stamps.get(field)
    ]
    if missing:
        raise MissingVersionStampsError(
            f"Manifest {name!r} missing required stamps: {missing}"
        )

    return StampedManifest(
        name=name,
        manifest_version=stamps["manifest_version"],
        policy_version=stamps["policy_version"],
        prompt_version=stamps["prompt_version"],
        raw=payload,
    )
