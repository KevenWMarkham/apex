"""Gate resolver — bump class + tenant policy → gate kind + runner."""

from __future__ import annotations

from dataclasses import dataclass

from apex_core.types import BumpClass, GateKind, GateVariant

from apex_orchestrator.gates.approvals import ApprovalsClient
from apex_orchestrator.gates.kinds import (
    AckOnlyGate,
    EscalationGate,
    GateRunner,
    HitlGate,
    ZeroTouchGate,
)

_DEFAULT_MAPPING: dict[BumpClass, GateKind] = {
    BumpClass.PATCH: GateKind.ZERO_TOUCH,
    BumpClass.MINOR: GateKind.ACK_ONLY,
    BumpClass.MAJOR: GateKind.HITL,
}


@dataclass(frozen=True, slots=True)
class GateResolution:
    bump_class: BumpClass
    gate_kind: GateKind
    variant: GateVariant
    override_source: str | None = None


def resolve_gate_kind(
    *,
    bump_class: BumpClass,
    tenant_override: GateKind | None = None,
    variant: GateVariant = GateVariant.HARD,
) -> GateResolution:
    """Return the effective gate kind + variant for a bump class.

    Tenant overrides are allowed to **narrow** (e.g. MINOR→HITL) or **widen**
    (MAJOR→ACK_ONLY) per APEX_Design §9.4. Variant is passed through; the
    runner is selected from the kind, not the variant.
    """
    if tenant_override is not None:
        return GateResolution(
            bump_class=bump_class,
            gate_kind=tenant_override,
            variant=variant,
            override_source="tenant",
        )
    return GateResolution(
        bump_class=bump_class,
        gate_kind=_DEFAULT_MAPPING[bump_class],
        variant=variant,
    )


def resolve_gate_runner(
    resolution: GateResolution,
    *,
    approvals: ApprovalsClient | None = None,
    approver_group: str = "default-approver",
    escalation_group: str = "default-escalation",
) -> GateRunner:
    """Materialise the appropriate :class:`GateRunner` for a resolution."""
    if resolution.gate_kind is GateKind.ZERO_TOUCH:
        return ZeroTouchGate()
    if resolution.gate_kind is GateKind.ACK_ONLY:
        return AckOnlyGate()
    if resolution.gate_kind is GateKind.HITL:
        if approvals is None:
            raise ValueError("HITL gate requires an ApprovalsClient.")
        return HitlGate(approvals=approvals, approver_group=approver_group)
    if resolution.gate_kind is GateKind.ESCALATION:
        if approvals is None:
            raise ValueError("ESCALATION gate requires an ApprovalsClient.")
        return EscalationGate(approvals=approvals, escalation_group=escalation_group)
    raise ValueError(f"Unknown gate kind: {resolution.gate_kind}")
