"""Machine-readable standards catalog — Sprint 20 Task 20.4 (BL.P.137).

The in-memory :data:`STANDARDS` registry is the source of truth at *runtime*.
The catalog YAML at :func:`catalog_path()` is the source of truth at
*release-time* — a versioned, reviewable artifact that:

1. Auditors read without importing Python.
2. CI checks for drift against the registry (every code registration has a YAML
   row, and every YAML row has a code registration).
3. Tooling (Sprint 28 scenario validators, Sellers Guide generators, etc.) can
   parse for cross-reference without a Python runtime.

The schema mirrors :class:`StandardSpec` exactly so a YAML row round-trips into
a :class:`StandardSpec` instance via ``StandardSpec.model_validate()``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from apex_schemas_common.standards.registry import STANDARDS, StandardSpec


# ---------------------------------------------------------------------------
# Catalog file location
# ---------------------------------------------------------------------------


def catalog_path() -> Path:
    """Path to the shipped ``standards/catalog.yaml`` artifact."""
    return Path(__file__).parent / "catalog.yaml"


# ---------------------------------------------------------------------------
# Serialize / deserialize
# ---------------------------------------------------------------------------


def standard_to_dict(spec: StandardSpec) -> dict[str, Any]:
    """Serialize a :class:`StandardSpec` to a YAML-friendly mapping.

    ``Practice`` enums are emitted as their ``value`` strings; ``StandardType``
    is emitted as its lowercase string value.
    """
    data = spec.model_dump(mode="python")
    # Practice enum -> string value
    data["practices"] = sorted(
        p.value if hasattr(p, "value") else str(p)
        for p in data.get("practices", [])
    )
    # StandardType enum -> string
    if hasattr(data.get("type"), "value"):
        data["type"] = data["type"].value
    # Drop empty notes for tidier YAML
    if not data.get("notes"):
        data.pop("notes", None)
    if data.get("supporting_package") is None:
        data.pop("supporting_package", None)
    return data


def dict_to_standard(data: dict[str, Any]) -> StandardSpec:
    """Deserialize a YAML mapping back into a :class:`StandardSpec`.

    Re-applies field defaults the catalog omits (``notes=""``,
    ``supporting_package=None``).
    """
    payload = dict(data)
    payload.setdefault("notes", "")
    payload.setdefault("supporting_package", None)
    return StandardSpec.model_validate(payload)


def emit_catalog(standards: dict[str, StandardSpec] | None = None) -> dict[str, Any]:
    """Build the catalog mapping from a registry dict (defaults to STANDARDS).

    The returned mapping has stable key ordering so YAML diffs stay reviewable.
    """
    src = standards if standards is not None else STANDARDS
    rows = [standard_to_dict(src[k]) for k in sorted(src)]
    return {
        "kind": "apex.standards.catalog",
        "version": 1,
        "count": len(rows),
        "standards": rows,
    }


def write_catalog(path: Path | None = None) -> Path:
    """Write the catalog YAML from the in-memory STANDARDS registry.

    Returns the path written. Idempotent — run on every release-bump.
    """
    target = path if path is not None else catalog_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = emit_catalog()
    with target.open("w", encoding="utf-8") as fh:
        fh.write("# auto-generated — apex_schemas_common.standards.catalog.write_catalog()\n")
        fh.write("# Source of truth at runtime: STANDARDS dict in registry.py\n")
        fh.write("# This file is reviewable diff-bait; CI fails on drift.\n")
        yaml.safe_dump(
            payload, fh, sort_keys=False, default_flow_style=False, allow_unicode=True
        )
    return target


def load_catalog(path: Path | None = None) -> dict[str, StandardSpec]:
    """Load catalog YAML and return ``{id: StandardSpec}``."""
    target = path if path is not None else catalog_path()
    if not target.exists():
        return {}
    with target.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict) or "standards" not in data:
        raise ValueError(
            f"Catalog {target}: expected mapping with 'standards' key, got {type(data).__name__}"
        )
    out: dict[str, StandardSpec] = {}
    for row in data["standards"]:
        spec = dict_to_standard(row)
        out[spec.id] = spec
    return out


# ---------------------------------------------------------------------------
# Drift detection
# ---------------------------------------------------------------------------


@dataclass
class CatalogIssue:
    standard_id: str
    code: str
    severity: str = "error"
    message: str = ""


@dataclass
class CatalogDriftReport:
    issues: list[CatalogIssue] = field(default_factory=list)
    standards_in_code: int = 0
    standards_in_catalog: int = 0

    @property
    def errors(self) -> list[CatalogIssue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    @property
    def exit_code(self) -> int:
        return 0 if self.ok else 1


def check_catalog_drift(
    code_registry: dict[str, StandardSpec] | None = None,
    catalog_file: Path | None = None,
) -> CatalogDriftReport:
    """Compare the YAML catalog against the in-memory STANDARDS registry.

    Detects:

    - ``CATALOG_MISSING_ROW`` — registered in code, missing from catalog.yaml
    - ``CODE_MISSING_REGISTRATION`` — present in catalog, no code registration.
    - ``FIELD_MISMATCH`` — present in both but a field disagrees.
    """
    code = code_registry if code_registry is not None else STANDARDS
    yaml_catalog = load_catalog(catalog_file)

    report = CatalogDriftReport(
        standards_in_code=len(code),
        standards_in_catalog=len(yaml_catalog),
    )

    code_ids = set(code)
    yaml_ids = set(yaml_catalog)

    for missing in sorted(code_ids - yaml_ids):
        report.issues.append(
            CatalogIssue(
                standard_id=missing,
                code="CATALOG_MISSING_ROW",
                message=f"{missing!r} is registered in STANDARDS but not in catalog.yaml",
            )
        )
    for extra in sorted(yaml_ids - code_ids):
        report.issues.append(
            CatalogIssue(
                standard_id=extra,
                code="CODE_MISSING_REGISTRATION",
                message=f"{extra!r} is in catalog.yaml but not in the STANDARDS registry",
            )
        )
    for sid in sorted(code_ids & yaml_ids):
        code_dict = standard_to_dict(code[sid])
        yaml_dict = standard_to_dict(yaml_catalog[sid])
        # Ignore optional defaults that round-trip cleanly
        for key in sorted(set(code_dict) | set(yaml_dict)):
            if code_dict.get(key) != yaml_dict.get(key):
                report.issues.append(
                    CatalogIssue(
                        standard_id=sid,
                        code="FIELD_MISMATCH",
                        message=(
                            f"{sid}.{key}: code={code_dict.get(key)!r} "
                            f"vs. catalog={yaml_dict.get(key)!r}"
                        ),
                    )
                )

    return report
