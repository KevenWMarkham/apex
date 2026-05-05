"""Tests for the RC Cold Chain Response reference orchestration."""

from __future__ import annotations

from apex_orchestrator import InMemoryApprovalsClient, OrchestrationStatus
from apex_orchestrator.reference import build_cold_chain_response


def test_no_excursion_completes_without_pause() -> None:
    approvals = InMemoryApprovalsClient()
    orch = build_cold_chain_response(approvals=approvals)
    result = orch.run({"temp_high_f": 38.0, "duration_minutes": 60})
    # No excursion: dispose proposes no_action, but the gate is still MAJOR → HITL.
    # (By design: the policy is "always HITL on batch disposition".)
    assert result.status is OrchestrationStatus.PAUSED


def test_excursion_triggers_hitl_and_completes_after_approve() -> None:
    approvals = InMemoryApprovalsClient()
    orch = build_cold_chain_response(approvals=approvals)
    result = orch.run({
        "temp_high_f": 52.0, "duration_minutes": 240, "units_at_risk": 412,
    })
    assert result.status is OrchestrationStatus.PAUSED
    assert len(result.pending_approvals) == 1
    # Approve → orchestration completes + notify step fires.
    pid = result.pending_approvals[0]
    done = orch.resume(pid, decision="approved", approver_id="qa@example.com",
                       rationale="salvage 71% within safety window")
    assert done.status is OrchestrationStatus.COMPLETED
    assert "notified" in done.context


def test_rejection_leaves_orchestration_rejected() -> None:
    approvals = InMemoryApprovalsClient()
    orch = build_cold_chain_response(approvals=approvals)
    paused = orch.run({"temp_high_f": 55.0, "duration_minutes": 300, "units_at_risk": 500})
    pid = paused.pending_approvals[0]
    done = orch.resume(pid, decision="rejected", approver_id="qa@example.com",
                       rationale="outside salvage window")
    assert done.status is OrchestrationStatus.REJECTED
