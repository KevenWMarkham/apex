"""Sprint 46.4 — drift detector.

Compares the **deployed state** of a tenant's Bicep stack against the
**declared state** (the pinned release manifest) and reports divergence.
A daily cron job calls this and writes any drift to the
``apex_drift_log`` audit table + fires a Teams alert per
``Professional-APEX-M-Services-Guide.html §3792``.

Implementation
==============

Drift detection runs ``az deployment group what-if`` against the pinned
release manifest. Any non-NoChange result indicates drift — someone /
something modified the deployed stack out-of-band (manual portal edit,
SDK call from another tool, regulatory remediation patch, etc.).

The detector is **read-only** — it never applies changes. The cron job
records the drift; the on-call operator decides whether to
auto-remediate (re-apply the manifest) or accept the change (update
the manifest).

Dual-mode (same as bicep_runner):
- mock: returns canned no-drift result; useful for unit tests
- real: shells out to ``az`` and parses the JSON

Cron entrypoint
===============

The :func:`run_drift_cron` callable is what the daily scheduled task
invokes. The FastAPI endpoint exists for on-demand checks from the
wizard UI.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Callable

from fastapi import APIRouter, HTTPException

router = APIRouter()


# ---------------------------------------------------------------------------
# Drift report
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DriftFinding:
    """One detected divergence."""

    resource_id: str
    resource_type: str
    drift_kind: str   # "modified" | "deleted" | "extra_created"
    before: dict | None = None
    after: dict | None = None


@dataclass(frozen=True)
class DriftReport:
    """Aggregated drift result for one tenant."""

    tenant: str
    blueprint_path: str
    pinned_release: str
    detected_at: datetime
    findings: tuple[DriftFinding, ...]
    duration_ms: int
    mode: str   # "mock" | "real"

    @property
    def has_drift(self) -> bool:
        return len(self.findings) > 0

    @property
    def drift_count(self) -> int:
        return len(self.findings)

    @property
    def severity(self) -> str:
        """Severity bucket for Teams alert routing.

        ``low``    = ≤ 2 modified resources (likely manual portal edit)
        ``medium`` = 3-10 modified resources (potential broader change)
        ``high``   = > 10 OR any deletion (likely incident)
        """
        if any(f.drift_kind == "deleted" for f in self.findings):
            return "high"
        n = len(self.findings)
        if n > 10:
            return "high"
        if n > 2:
            return "medium"
        if n > 0:
            return "low"
        return "none"

    def as_dict(self) -> dict:
        return {
            "tenant": self.tenant,
            "blueprint_path": self.blueprint_path,
            "pinned_release": self.pinned_release,
            "detected_at": self.detected_at.isoformat(),
            "has_drift": self.has_drift,
            "drift_count": self.drift_count,
            "severity": self.severity,
            "mode": self.mode,
            "duration_ms": self.duration_ms,
            "findings": [
                {
                    "resource_id": f.resource_id,
                    "resource_type": f.resource_type,
                    "drift_kind": f.drift_kind,
                }
                for f in self.findings
            ],
        }


# ---------------------------------------------------------------------------
# Detector
# ---------------------------------------------------------------------------


@dataclass
class DriftDetector:
    """Compares deployed state vs pinned release manifest.

    Wraps the BicepRunner what-if to find drift; in mock mode returns
    a configurable canned result.
    """

    runner: object | None = None    # BicepRunner; None = use default
    preset_findings: tuple[DriftFinding, ...] = field(default_factory=tuple)
    force_mock: bool = False
    log: Callable[[str], None] | None = None

    def detect(
        self,
        *,
        tenant: str,
        blueprint_path: str,
        parameters_path: str,
        pinned_release: str,
    ) -> DriftReport:
        import time
        from .bicep_runner import MockBicepRunner, get_default_runner

        runner = self.runner or (
            MockBicepRunner() if self.force_mock else get_default_runner(log=self.log)
        )

        started = datetime.now(UTC)
        t0 = time.monotonic()
        what_if = runner.what_if(    # type: ignore[attr-defined]
            tenant=tenant,
            resource_group=f"rg-{tenant}",
            blueprint_path=blueprint_path,
            parameters_path=parameters_path,
        )
        duration_ms = int((time.monotonic() - t0) * 1000)

        # If preset_findings provided (test mode), use them verbatim.
        # Otherwise interpret what-if's non-NoChange results as drift.
        if self.preset_findings:
            findings = self.preset_findings
        else:
            findings = tuple(
                DriftFinding(
                    resource_id=c.resource_id,
                    resource_type=c.resource_type,
                    drift_kind={
                        "Modify": "modified",
                        "Deploy": "modified",
                        "Delete": "deleted",
                        "Create": "extra_created",
                    }.get(c.change_kind, "modified"),
                    before=c.before,
                    after=c.after,
                )
                for c in what_if.changes
                if c.change_kind != "NoChange"
            )

        return DriftReport(
            tenant=tenant,
            blueprint_path=blueprint_path,
            pinned_release=pinned_release,
            detected_at=started,
            findings=findings,
            duration_ms=duration_ms,
            mode=what_if.mode,
        )


# ---------------------------------------------------------------------------
# Audit-row store (in-memory; Sprint 42+ swaps for Cosmos AuditLedger)
# ---------------------------------------------------------------------------


_DRIFT_LOG: list[DriftReport] = []


def _reset_drift_log_for_test() -> None:
    _DRIFT_LOG.clear()


def _record_drift_report(report: DriftReport) -> None:
    """Persist a drift report to the audit log.

    Sprint 42+ swaps this for AuditLedger.append(); the call signature
    stays stable so the cron job + endpoint don't change.
    """
    _DRIFT_LOG.append(report)


def get_drift_history(tenant: str, *, limit: int = 50) -> list[DriftReport]:
    """Test/UI helper — return drift history for a tenant."""
    matching = [r for r in _DRIFT_LOG if r.tenant == tenant]
    return matching[-limit:]


# ---------------------------------------------------------------------------
# Cron entrypoint — invoked daily by a separate scheduled task
# ---------------------------------------------------------------------------


def run_drift_cron(
    *,
    tenants: list[str],
    blueprint_path: str = "apex-m/infra/bicep/blueprints/w3-scale-fuse.bicep",
    pinned_release: str = "v1.0.0",
    detector: DriftDetector | None = None,
) -> list[DriftReport]:
    """Sprint 46.4 cron entrypoint.

    Iterates every tenant, runs drift detection, records the report
    to the audit log, and returns the aggregate list (the cron wrapper
    posts a Teams alert when any report has severity != none).
    """
    detector = detector or DriftDetector()
    reports: list[DriftReport] = []
    for tenant in tenants:
        report = detector.detect(
            tenant=tenant,
            blueprint_path=blueprint_path,
            parameters_path=f"/var/apex/release/{tenant}-{pinned_release}.parameters.json",
            pinned_release=pinned_release,
        )
        _record_drift_report(report)
        reports.append(report)
    return reports


# ---------------------------------------------------------------------------
# FastAPI router
# ---------------------------------------------------------------------------


@router.get("/{tenant}")
def drift_report(tenant: str, pinned_release: str = "v1.0.0") -> dict:
    """On-demand drift check for a tenant.

    Per Services Guide §3792: returns divergence as a structured diff.
    The daily cron job calls this implicitly via :func:`run_drift_cron`.
    """
    if not tenant or len(tenant) > 64:
        raise HTTPException(status_code=400, detail="tenant must be 1..64 chars")

    detector = DriftDetector()
    blueprint_path = "apex-m/infra/bicep/blueprints/w3-scale-fuse.bicep"
    parameters_path = f"/var/apex/release/{tenant}-{pinned_release}.parameters.json"
    try:
        report = detector.detect(
            tenant=tenant,
            blueprint_path=blueprint_path,
            parameters_path=parameters_path,
            pinned_release=pinned_release,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"pinned release artefacts missing: {exc}")

    _record_drift_report(report)
    return report.as_dict()


@router.get("/{tenant}/history")
def drift_history(tenant: str, limit: int = 50) -> dict:
    """Recent drift reports for a tenant (for the wizard's history view)."""
    history = get_drift_history(tenant, limit=limit)
    return {
        "tenant": tenant,
        "count": len(history),
        "reports": [r.as_dict() for r in history],
    }
