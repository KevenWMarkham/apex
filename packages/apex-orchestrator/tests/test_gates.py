"""Tests for gate kinds, variants, and the resolver."""

from __future__ import annotations

import pytest

from apex_core.types import BumpClass, GateKind, GateVariant
from apex_orchestrator import (
    GateOutcome,
    InMemoryApprovalsClient,
    resolve_gate_kind,
    resolve_gate_runner,
)
from apex_orchestrator.gates.kinds import (
    AckOnlyGate,
    EscalationGate,
    HitlGate,
    ZeroTouchGate,
)


class TestResolver:
    def test_patch_defaults_zero_touch(self) -> None:
        r = resolve_gate_kind(bump_class=BumpClass.PATCH)
        assert r.gate_kind is GateKind.ZERO_TOUCH
        assert r.override_source is None

    def test_minor_defaults_ack_only(self) -> None:
        assert resolve_gate_kind(bump_class=BumpClass.MINOR).gate_kind is GateKind.ACK_ONLY

    def test_major_defaults_hitl(self) -> None:
        assert resolve_gate_kind(bump_class=BumpClass.MAJOR).gate_kind is GateKind.HITL

    def test_tenant_override_applies(self) -> None:
        r = resolve_gate_kind(
            bump_class=BumpClass.MINOR,
            tenant_override=GateKind.HITL,
        )
        assert r.gate_kind is GateKind.HITL
        assert r.override_source == "tenant"


class TestRunners:
    def test_zero_touch_auto_applies(self) -> None:
        out = ZeroTouchGate().apply(decision_id="d1", proposal={"x": 1})
        assert out.status == "auto_applied"

    def test_ack_only_status(self) -> None:
        out = AckOnlyGate().apply(decision_id="d1", proposal={})
        assert out.status == "acknowledged"

    def test_hitl_opens_pending(self) -> None:
        approvals = InMemoryApprovalsClient()
        gate = HitlGate(approvals=approvals, approver_group="qa")
        out = gate.apply(decision_id="d1", proposal={"action": "dispose"})
        assert out.status == "pending"
        assert out.pending_id is not None

    def test_escalation_routes(self) -> None:
        approvals = InMemoryApprovalsClient()
        gate = EscalationGate(approvals=approvals, escalation_group="director")
        out = gate.apply(decision_id="d1", proposal={})
        assert out.status == "escalated"
        assert out.pending_id is not None

    def test_resolver_returns_concrete_runner(self) -> None:
        approvals = InMemoryApprovalsClient()
        r = resolve_gate_kind(bump_class=BumpClass.MAJOR)
        runner = resolve_gate_runner(
            r, approvals=approvals, approver_group="qa",
        )
        assert isinstance(runner, HitlGate)

    def test_resolver_rejects_hitl_without_approvals(self) -> None:
        r = resolve_gate_kind(bump_class=BumpClass.MAJOR)
        with pytest.raises(ValueError):
            resolve_gate_runner(r)


class TestVariants:
    def test_default_variant_is_hard(self) -> None:
        r = resolve_gate_kind(bump_class=BumpClass.MAJOR)
        assert r.variant is GateVariant.HARD

    def test_explicit_variant_preserved(self) -> None:
        r = resolve_gate_kind(bump_class=BumpClass.MAJOR, variant=GateVariant.SOFT)
        assert r.variant is GateVariant.SOFT
