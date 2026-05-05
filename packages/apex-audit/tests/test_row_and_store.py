"""14-field audit row + append-only store (BL.P.77, BL.P.78)."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from apex_audit import (
    AppendOnlyViolationError,
    AuditRow,
    AuditStore,
    HitlEvent,
    HitlRecord,
    HitlStatus,
    OrchestrationCompositeRow,
    ParticipatingAgent,
    ToolCallRecord,
    TraceMissingError,
)


def _row(**overrides) -> AuditRow:
    defaults = dict(
        trace_id="t-1", decision_id="d-1", agent_id="a1",
        invoking_identity="user:qa", manifest_version="m",
        policy_version="p", model_version="gpt-4.1", prompt_version="pr",
        inputs_ref="sha256:aaa",
        tools_called=(
            ToolCallRecord(
                mcp_tool_id="fabric-mcp.query", tool_version="1.0.0",
                parameters_hash="sha256:pp", result_hash="sha256:rr",
            ),
        ),
        reasoning_trace_ref="sha256:rz",
        decision_output={"action": "markdown", "pct": -30},
        hitl_status=HitlRecord(status=HitlStatus.APPROVED,
                               approver_identity="qa@ex.com"),
        downstream_effect_ref=None,
    )
    defaults.update(overrides)
    return AuditRow(**defaults)


class TestAuditRow:
    def test_14_required_fields_present(self) -> None:
        row = _row()
        required = {
            "trace_id", "decision_id", "agent_id", "invoking_identity",
            "manifest_version", "policy_version", "model_version",
            "prompt_version", "inputs_ref", "tools_called",
            "reasoning_trace_ref", "decision_output", "hitl_status",
            "downstream_effect_ref",
        }
        dumped = row.to_dict()
        assert required.issubset(dumped.keys())

    def test_row_is_frozen(self) -> None:
        row = _row()
        with pytest.raises(Exception):
            row.trace_id = "x"  # type: ignore[misc]

    def test_missing_required_field_rejected(self) -> None:
        with pytest.raises(Exception):
            _row(trace_id="")  # min_length=1


class TestAuditStore:
    def test_append_seals_and_signs(self) -> None:
        store = AuditStore(signing_key=b"key")
        sealed = store.append(_row())
        assert sealed["signature"]
        assert sealed["sealed_at"]
        assert store.verify("d-1") is True

    def test_by_trace_walks_in_append_order(self) -> None:
        store = AuditStore(signing_key=b"key")
        store.append(_row(decision_id="d-1"))
        store.append(_row(decision_id="d-2"))
        rows = store.by_trace("t-1")
        assert [r["decision_id"] for r in rows] == ["d-1", "d-2"]

    def test_duplicate_decision_id_rejected(self) -> None:
        store = AuditStore(signing_key=b"key")
        store.append(_row())
        with pytest.raises(AppendOnlyViolationError):
            store.append(_row())

    def test_trace_id_discipline_enforced(self) -> None:
        """An AuditRow with '' trace_id fails at model construction (min_length=1);
        confirm that also the emission path rejects an empty trace if it ever
        slipped past (defence in depth)."""
        # Build a model-valid row then zero trace_id via model_copy to exercise
        # the store-side TraceMissingError path.
        row = _row()
        sneaked = row.model_copy(update={"trace_id": ""})
        store = AuditStore(signing_key=b"key")
        with pytest.raises(TraceMissingError):
            store.append(sneaked)

    def test_verify_detects_tamper(self) -> None:
        store = AuditStore(signing_key=b"key")
        store.append(_row())
        store._rows["d-1"]["decision_output"] = {"action": "tampered"}
        assert store.verify("d-1") is False


class TestCompositeRow:
    def test_append_composite(self) -> None:
        store = AuditStore(signing_key=b"key")
        comp = OrchestrationCompositeRow(
            trace_id="t-1", orchestration_id="orc-1",
            archetype_id="rc.cold_chain", trigger="event",
            tenant_id="tenant-a",
            participating_agents=(
                ParticipatingAgent(
                    decision_id="d-1", agent_id="a1", step_order=0,
                ),
            ),
            orchestration_outcome="completed",
            hitl_gates_fired=(
                HitlEvent(decision_id="d-1", gate_kind="HITL",
                          status="approved"),
            ),
            started_at=datetime.now(UTC),
        )
        sealed = store.append_composite(comp)
        assert sealed["signature"]
        assert sealed["orchestration_id"] == "orc-1"
        assert store.verify("orc-1") is True
