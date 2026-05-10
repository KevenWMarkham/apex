"""Sprint 46.2 — /api/security-gate aggregator endpoint.

Polls all 15 Pre-deployment Security Gates and returns a structured
status per gate. The wizard's /security-gate page renders this; red
gates block the deploy button.

Gate inventory
==============

Per ``docs/APEX - Design and Build/Pre-deployment-Security-Gate.md``:

  Structural gates (one-time per tenant):
    PSG-1  Defender for Cloud CSPM with AI security posture
    PSG-2  Defender for AI services on Foundry project
    PSG-3  Microsoft Entra Agent ID tenant root blueprint
    PSG-4  Purview sensitivity labels enabled for SharePoint + OneDrive
    PSG-5  Purview Audit retention configured
    PSG-6  Customer Managed Keys (CMK) for Storage + Cognitive Services
    PSG-7  Customer Lockbox enabled
    PSG-8  Workspace-level IP firewall on Fabric workspaces

  Per-deployment gates (per wave):
    PSG-9  AI Model Security scan green
    PSG-10 Conditional Access on the service blueprint
    PSG-11 HITL threshold config in Key Vault
    PSG-12 Use case `client_approved_architecture` resolves
    PSG-13 Foundry Standard Setup with Private Networking
    PSG-14 Independence consultation per adapter
    PSG-15 Persona-binding resolvability (Sprint 47.6 — apex_core.validators)

Dual-mode polling
=================

Each gate has a checker function. Mock-mode checkers return canned green
statuses (laptop substrate); real-mode checkers call into the
corresponding Microsoft surface (Graph + Defender API + Purview API
etc.). Sprint 41-45 production wiring lights up the real-mode checkers.

PSG-15 (the persona-bindings lint) IS implemented today — it uses
apex_core.validators.use_case_personas.quick_check_psg_15. This is the
first gate that is real-mode-ready before the Lab tenant lands.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Callable

from fastapi import APIRouter, Query


# ---------------------------------------------------------------------------
# Gate model
# ---------------------------------------------------------------------------


class GateStatus(StrEnum):
    """Per-gate evaluation result."""

    GREEN = "green"           # Gate passes; deploy may proceed
    YELLOW = "yellow"         # Gate has warnings; operator override possible
    RED = "red"               # Gate fails; deploy must NOT proceed
    UNKNOWN = "unknown"       # Gate could not be evaluated (mode/env mismatch)


@dataclass(frozen=True)
class GateEvaluation:
    """One gate's result + the evidence the wizard surfaces."""

    gate_id: str
    title: str
    status: GateStatus
    evaluated_at: datetime
    mode: str   # "mock" | "real"
    rationale: str
    remediate: str | None = None
    blocking: bool = True   # True = RED blocks deploy; False = warn-only
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SecurityGateReport:
    """Aggregated result of polling all 15 gates."""

    tenant: str
    evaluated_at: datetime
    gates: tuple[GateEvaluation, ...]

    @property
    def overall_status(self) -> GateStatus:
        """Worst of any blocking gate.

        If any blocking gate is RED → overall RED.
        Else if any blocking gate is YELLOW → overall YELLOW.
        Else GREEN.
        """
        has_red = any(g.status == GateStatus.RED and g.blocking for g in self.gates)
        if has_red:
            return GateStatus.RED
        has_yellow = any(g.status == GateStatus.YELLOW and g.blocking for g in self.gates)
        if has_yellow:
            return GateStatus.YELLOW
        if any(g.status == GateStatus.UNKNOWN and g.blocking for g in self.gates):
            return GateStatus.YELLOW
        return GateStatus.GREEN

    @property
    def deploy_allowed(self) -> bool:
        """Whether the wizard's deploy button should be enabled."""
        return self.overall_status != GateStatus.RED

    @property
    def red_gates(self) -> list[str]:
        return [g.gate_id for g in self.gates if g.status == GateStatus.RED]

    def as_dict(self) -> dict:
        """JSON-serialisable shape the wizard frontend consumes."""
        return {
            "tenant": self.tenant,
            "evaluated_at": self.evaluated_at.isoformat(),
            "overall_status": self.overall_status.value,
            "deploy_allowed": self.deploy_allowed,
            "red_gates": self.red_gates,
            "gates": [
                {
                    "gate_id": g.gate_id,
                    "title": g.title,
                    "status": g.status.value,
                    "evaluated_at": g.evaluated_at.isoformat(),
                    "mode": g.mode,
                    "rationale": g.rationale,
                    "remediate": g.remediate,
                    "blocking": g.blocking,
                    "metadata": g.metadata,
                }
                for g in self.gates
            ],
        }


# ---------------------------------------------------------------------------
# Gate registry — one checker per gate id
# ---------------------------------------------------------------------------


CheckerFn = Callable[[str, dict[str, Any]], GateEvaluation]
# Signature: checker(tenant, context) -> GateEvaluation
# context carries optional use-case data + substrate for gates that need it.


_GATE_TITLES: dict[str, str] = {
    "PSG-1": "Defender for Cloud CSPM with AI security posture",
    "PSG-2": "Defender for AI services on Foundry project",
    "PSG-3": "Microsoft Entra Agent ID tenant root blueprint",
    "PSG-4": "Purview sensitivity labels enabled for SharePoint + OneDrive",
    "PSG-5": "Purview Audit retention configured",
    "PSG-6": "Customer Managed Keys (CMK) for Storage + Cognitive Services",
    "PSG-7": "Customer Lockbox enabled",
    "PSG-8": "Workspace-level IP firewall on Fabric workspaces",
    "PSG-9": "AI Model Security scan green",
    "PSG-10": "Conditional Access on the service blueprint",
    "PSG-11": "HITL threshold config in Key Vault",
    "PSG-12": "Use case `client_approved_architecture` resolves",
    "PSG-13": "Foundry Standard Setup with Private Networking",
    "PSG-14": "Independence consultation per adapter",
    "PSG-15": "Persona-binding resolvability (Sprint 47.6)",
}


def _is_force_mock() -> bool:
    return os.environ.get("APEX_FORCE_MOCK", "").strip().lower() == "true"


# --- Mock-mode checker (Sprints 41-45 real-mode lights up later) -----------


def _mock_green(gate_id: str, tenant: str, *, blocking: bool = True) -> GateEvaluation:
    return GateEvaluation(
        gate_id=gate_id,
        title=_GATE_TITLES[gate_id],
        status=GateStatus.GREEN,
        evaluated_at=datetime.now(UTC),
        mode="mock",
        rationale=f"[mock] {gate_id} returned synthetic green for tenant={tenant!r}",
        blocking=blocking,
    )


def _make_mock_checker(gate_id: str) -> CheckerFn:
    def checker(tenant: str, context: dict[str, Any]) -> GateEvaluation:
        return _mock_green(gate_id, tenant)
    return checker


# --- PSG-15 (Sprint 47.6) — real-mode-ready today --------------------------


def _check_psg_15(tenant: str, context: dict[str, Any]) -> GateEvaluation:
    """Persona-binding resolvability — uses Sprint 47.6's validator.

    Requires ``context['use_case_data']`` populated (the parsed use-case
    YAML). When absent, returns UNKNOWN (cannot evaluate without the
    use-case in hand) — the wizard surfaces this as "select a use case
    first."
    """
    use_case_data = context.get("use_case_data")
    if not use_case_data:
        return GateEvaluation(
            gate_id="PSG-15",
            title=_GATE_TITLES["PSG-15"],
            status=GateStatus.UNKNOWN,
            evaluated_at=datetime.now(UTC),
            mode="real",  # the checker itself is real even when input absent
            rationale=(
                "Cannot evaluate without context.use_case_data. Wizard: "
                "render the use-case YAML first, then re-poll."
            ),
            remediate="POST /api/security-gate with use_case_data populated.",
            blocking=True,
        )

    try:
        from apex_core.validators import validate_use_case_personas
    except ImportError:
        return GateEvaluation(
            gate_id="PSG-15",
            title=_GATE_TITLES["PSG-15"],
            status=GateStatus.UNKNOWN,
            evaluated_at=datetime.now(UTC),
            mode="mock",
            rationale="apex_core.validators not importable in this environment",
            blocking=True,
        )

    report = validate_use_case_personas(use_case_data)

    if report.fails_psg_15:
        return GateEvaluation(
            gate_id="PSG-15",
            title=_GATE_TITLES["PSG-15"],
            status=GateStatus.RED,
            evaluated_at=datetime.now(UTC),
            mode="real",
            rationale=(
                f"PSG-15 failed: {len(report.errors)} error(s). "
                f"Unresolved personas: {report.unresolved_personas}"
            ),
            remediate=(
                "Clone services/<practice>/<service>/use-cases/_default/ to "
                "<client>/ and populate the persona_principal_bindings block "
                "for each persona in personas_active. See PSG-15 in "
                "Pre-deployment-Security-Gate.md."
            ),
            blocking=True,
            metadata={
                "substrate": report.substrate.value,
                "personas_active": report.personas_active,
                "unresolved_personas": report.unresolved_personas,
                "errors": report.errors,
                "warnings": report.warnings,
                "synthetic_personas_present_on_non_laptop":
                    report.synthetic_personas_present_on_non_laptop,
            },
        )

    if report.warnings:
        return GateEvaluation(
            gate_id="PSG-15",
            title=_GATE_TITLES["PSG-15"],
            status=GateStatus.YELLOW,
            evaluated_at=datetime.now(UTC),
            mode="real",
            rationale=(
                f"PSG-15 warnings only (substrate={report.substrate.value}). "
                f"{len(report.warnings)} warning(s)."
            ),
            remediate="Review warnings; binding completion advised before prod.",
            blocking=False,
            metadata={
                "substrate": report.substrate.value,
                "warnings": report.warnings,
                "unresolved_personas": report.unresolved_personas,
            },
        )

    return GateEvaluation(
        gate_id="PSG-15",
        title=_GATE_TITLES["PSG-15"],
        status=GateStatus.GREEN,
        evaluated_at=datetime.now(UTC),
        mode="real",
        rationale=(
            f"PSG-15 green for substrate={report.substrate.value}. "
            f"All {len(report.personas_active)} active personas bound."
        ),
        blocking=True,
        metadata={
            "substrate": report.substrate.value,
            "personas_active_count": len(report.personas_active),
            "bindings_count": report.bindings_count,
        },
    )


# --- Registry construction -------------------------------------------------


_REGISTRY: dict[str, CheckerFn] = {
    "PSG-1":  _make_mock_checker("PSG-1"),
    "PSG-2":  _make_mock_checker("PSG-2"),
    "PSG-3":  _make_mock_checker("PSG-3"),
    "PSG-4":  _make_mock_checker("PSG-4"),
    "PSG-5":  _make_mock_checker("PSG-5"),
    "PSG-6":  _make_mock_checker("PSG-6"),
    "PSG-7":  _make_mock_checker("PSG-7"),
    "PSG-8":  _make_mock_checker("PSG-8"),
    "PSG-9":  _make_mock_checker("PSG-9"),
    "PSG-10": _make_mock_checker("PSG-10"),
    "PSG-11": _make_mock_checker("PSG-11"),
    "PSG-12": _make_mock_checker("PSG-12"),
    "PSG-13": _make_mock_checker("PSG-13"),
    "PSG-14": _make_mock_checker("PSG-14"),
    "PSG-15": _check_psg_15,
}


def register_checker(gate_id: str, checker: CheckerFn) -> None:
    """Sprint 41-45 production-wiring entry point — swap the mock for real."""
    _REGISTRY[gate_id] = checker


# ---------------------------------------------------------------------------
# Public aggregator
# ---------------------------------------------------------------------------


def evaluate_all_gates(
    tenant: str,
    context: dict[str, Any] | None = None,
) -> SecurityGateReport:
    """Poll every registered gate and return a structured report.

    Args:
        tenant: Tenant slug (e.g. "bigbox-prod").
        context: Optional dict carrying use-case data, substrate, etc.
            PSG-12 + PSG-15 need ``context['use_case_data']`` populated.
    """
    context = context or {}
    gates = tuple(
        _REGISTRY[gate_id](tenant, context)
        for gate_id in _GATE_TITLES.keys()
    )
    return SecurityGateReport(
        tenant=tenant,
        evaluated_at=datetime.now(UTC),
        gates=gates,
    )


# ---------------------------------------------------------------------------
# FastAPI router
# ---------------------------------------------------------------------------


router = APIRouter()


@router.get("")
def security_gate_status(
    tenant: str = Query(..., description="Tenant slug"),
) -> dict:
    """GET /api/security-gate — quick read for the wizard's poll loop.

    Returns the aggregate gate report. PSG-12 + PSG-15 return UNKNOWN
    because they require use-case context — use POST for those.
    """
    report = evaluate_all_gates(tenant)
    return report.as_dict()


@router.post("/with-context")
def security_gate_with_context(payload: dict) -> dict:
    """POST /api/security-gate/with-context — full evaluation including PSG-12/15.

    Body:
        {
          "tenant": "bigbox-prod",
          "use_case_data": { ...parsed use-case YAML... }
        }

    Returns the aggregate gate report with PSG-15 evaluated against the
    provided use-case (succeeds when persona bindings resolve; fails closed
    when substrate >= dev with unbound personas).
    """
    tenant = payload.get("tenant", "")
    context = {
        "use_case_data": payload.get("use_case_data"),
        "substrate": payload.get("substrate"),
    }
    report = evaluate_all_gates(tenant, context)
    return report.as_dict()
