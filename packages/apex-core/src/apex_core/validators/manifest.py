"""Single-manifest validator.

Loads a YAML file, dispatches to the correct Pydantic model by ``kind``, and
returns a structured :class:`ValidationReport`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from apex_core.manifests import (
    AgentManifest,
    BaseManifest,
    EventManifest,
    OrchestrationManifest,
    PolicyManifest,
    SchemaManifest,
    ServiceManifest,
    TenantManifest,
)

_DISPATCH: dict[str, type[BaseManifest]] = {
    "schema": SchemaManifest,
    "event": EventManifest,
    "orchestration": OrchestrationManifest,
    "agent": AgentManifest,
    "tenant": TenantManifest,
    "policy": PolicyManifest,
    "service": ServiceManifest,
}


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """Structured result of a single-manifest validation."""

    path: Path
    kind: str | None
    valid: bool
    errors: list[str] = field(default_factory=list)
    manifest: BaseManifest | None = None

    def summary(self) -> str:
        """Human-readable one-line summary."""
        status = "OK" if self.valid else "FAIL"
        kind = self.kind or "?"
        return f"[{status}] {self.path} ({kind})"


def validate_manifest(path: Path) -> ValidationReport:
    """Validate a single manifest YAML file.

    Dispatches to the correct Pydantic model based on the ``kind`` field.

    Args:
        path: Filesystem path to a YAML manifest.

    Returns:
        A :class:`ValidationReport`. When valid, ``manifest`` holds the
        parsed Pydantic instance and ``errors`` is empty.
    """
    try:
        raw: Any = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return ValidationReport(path, None, False, [f"File not found: {path}"])
    except yaml.YAMLError as exc:
        return ValidationReport(path, None, False, [f"YAML parse error: {exc}"])

    if not isinstance(raw, dict):
        return ValidationReport(
            path, None, False, ["Manifest root must be a YAML mapping."]
        )

    kind = raw.get("kind")
    if not isinstance(kind, str) or kind not in _DISPATCH:
        known = sorted(_DISPATCH)
        return ValidationReport(
            path,
            kind if isinstance(kind, str) else None,
            False,
            [f"Unknown or missing 'kind'. Must be one of: {known}"],
        )

    model_cls = _DISPATCH[kind]
    try:
        manifest = model_cls.model_validate(raw)
    except ValidationError as exc:
        errors = [
            f"{'.'.join(str(p) for p in err['loc'])}: {err['msg']}"
            for err in exc.errors()
        ]
        return ValidationReport(path, kind, False, errors)

    return ValidationReport(path, kind, True, [], manifest)
