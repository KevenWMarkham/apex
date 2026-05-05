"""Tests for the tenant policy-tuning workflow."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from apex_core.types import GateKind
from apex_orchestrator import TuningStatus, TuningStore


def _store_with_proposal() -> tuple[TuningStore, str]:
    store = TuningStore()
    req = store.propose(
        service="rc-markdown",
        from_gate=GateKind.HITL, to_gate=GateKind.ACK_ONLY,
        requested_by="ops-lead@example.com",
        rationale="historically low-risk for this tenant",
    )
    return store, req.request_id


def test_propose_then_observe() -> None:
    store, rid = _store_with_proposal()
    req = store.start_observation(rid)
    assert req.status is TuningStatus.OBSERVING
    assert req.observation_ends_at is not None


def test_auto_approves_after_window() -> None:
    store, rid = _store_with_proposal()
    store.start_observation(rid)
    future = datetime.now(UTC) + timedelta(days=15)
    final = store.evaluate(rid, now=future)
    assert final.status is TuningStatus.APPROVED


def test_rolls_back_on_reversal() -> None:
    store, rid = _store_with_proposal()
    store.start_observation(rid)
    store.record_reversal(rid)
    final = store.evaluate(rid)
    assert final.status is TuningStatus.ROLLED_BACK


def test_rolls_back_on_escalation() -> None:
    store, rid = _store_with_proposal()
    store.start_observation(rid)
    store.get(rid).record_escalation()
    final = store.evaluate(rid)
    assert final.status is TuningStatus.ROLLED_BACK


def test_history_records_lifecycle() -> None:
    store, rid = _store_with_proposal()
    store.start_observation(rid)
    events = [h["event"] for h in store.history]
    assert "proposed" in events
    assert "observation_started" in events
