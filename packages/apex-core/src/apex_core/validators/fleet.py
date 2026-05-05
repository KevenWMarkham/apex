"""Fleet validator — cross-tenant consistency checks.

Given a set of L4 TenantManifests plus their pinned L3 Practices, verifies:

- Every tenant pins a known Practice release.
- Every tenant extension's overlay passes L3-compat CI (presence-only check
  here; full overlay semantics land in a later sprint).
- No two tenants collide on reserved identifiers.

The full semantics of Fleet validation (cross-tenant SLO aggregation, capacity
planning, migration windows) are out of scope for Sprint 1.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from apex_core.manifests import TenantManifest
from apex_core.validators.manifest import ValidationReport, validate_manifest


@dataclass(frozen=True, slots=True)
class FleetReport:
    """Structured result of fleet validation."""

    tenant_reports: list[ValidationReport] = field(default_factory=list)
    cross_tenant_errors: list[str] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return (
            all(r.valid for r in self.tenant_reports)
            and not self.cross_tenant_errors
        )

    def summary(self) -> str:
        n = len(self.tenant_reports)
        bad = sum(1 for r in self.tenant_reports if not r.valid)
        extra = len(self.cross_tenant_errors)
        status = "OK" if self.valid else "FAIL"
        return (
            f"[{status}] fleet — {n - bad}/{n} tenants valid, "
            f"{extra} cross-tenant errors"
        )


def validate_fleet(tenant_paths: list[Path]) -> FleetReport:
    """Validate a fleet of L4 TenantManifests.

    Args:
        tenant_paths: Paths to individual tenant YAML files.

    Returns:
        A :class:`FleetReport` with per-tenant reports plus any cross-tenant
        errors (duplicate names, collisions, ...).
    """
    reports: list[ValidationReport] = [validate_manifest(p) for p in tenant_paths]
    cross_errors: list[str] = []

    names: list[str] = [
        r.manifest.name
        for r in reports
        if r.valid and isinstance(r.manifest, TenantManifest)
    ]
    dupes = [name for name, count in Counter(names).items() if count > 1]
    cross_errors.extend(f"Duplicate tenant name: {name!r}" for name in sorted(dupes))

    return FleetReport(tenant_reports=reports, cross_tenant_errors=cross_errors)
