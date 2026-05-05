"""Tests for ledger-mcp tools (Sprint 12: full 14-field contract)."""

from __future__ import annotations

import pytest

from ledger_mcp import (
    CONTRACTS,
    append_audit_row,
    fetch_row_by_trace,
    reset_ledger,
    verify_row_signature,
)
from ledger_mcp.tools import _get_store
from mcp_common import McpError, McpErrorCode


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_ledger()


def _valid_row(trace_id: str = "trace-1", decision_id: str = "dec-1") -> dict:
    """Produce a full 14-field audit row."""
    return {
        "trace_id": trace_id,
        "decision_id": decision_id,
        "agent_id": "agent:rc.dispose",
        "invoking_identity": "user:qa@ex.com",
        "manifest_version": "sha-m",
        "policy_version": "sha-p",
        "model_version": "gpt-4.1-2025-01",
        "prompt_version": "sha-pr",
        "inputs_ref": "sha256:aaa",
        "tools_called": (),
        "reasoning_trace_ref": "sha256:rz",
        "decision_output": {"action": "salvage"},
        "hitl_status": {"status": "approved",
                        "approver_identity": "qa@ex.com"},
        "downstream_effect_ref": None,
    }


def test_append_then_fetch_by_trace() -> None:
    r = append_audit_row(_valid_row())
    rows = fetch_row_by_trace("trace-1")
    assert len(rows) == 1
    assert rows[0]["decision_id"] == r["row_id"]


def test_multiple_rows_same_trace_ordered() -> None:
    r1 = append_audit_row(_valid_row(decision_id="dec-1"))
    r2 = append_audit_row(_valid_row(decision_id="dec-2"))
    rows = fetch_row_by_trace("trace-1")
    assert [row["decision_id"] for row in rows] == [r1["row_id"], r2["row_id"]]


def test_missing_required_field_rejected() -> None:
    bad = _valid_row()
    del bad["manifest_version"]
    with pytest.raises(McpError) as exc:
        append_audit_row(bad)
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_empty_trace_id_rejected() -> None:
    bad = _valid_row(trace_id="")
    with pytest.raises(McpError) as exc:
        append_audit_row(bad)
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_duplicate_decision_id_rejected() -> None:
    append_audit_row(_valid_row())
    with pytest.raises(McpError) as exc:
        append_audit_row(_valid_row())  # same decision_id
    assert exc.value.code is McpErrorCode.CONFLICT


def test_signature_valid_after_append() -> None:
    r = append_audit_row(_valid_row())
    result = verify_row_signature(r["row_id"])
    assert result["signature_valid"] is True


def test_signature_mismatch_on_tamper() -> None:
    r = append_audit_row(_valid_row())
    # Tamper with the stored row directly.
    _get_store()._rows[r["row_id"]]["decision_output"] = {"action": "tampered"}
    result = verify_row_signature(r["row_id"])
    assert result["signature_valid"] is False


def test_verify_unknown() -> None:
    with pytest.raises(McpError) as exc:
        verify_row_signature("nonexistent")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_fetch_empty_trace_returns_empty_list() -> None:
    rows = fetch_row_by_trace("unknown-trace")
    assert rows == []


def test_contracts_count() -> None:
    assert len(CONTRACTS) == 3
