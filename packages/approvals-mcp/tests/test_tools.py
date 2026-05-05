"""Tests for approvals-mcp tools."""

from __future__ import annotations

import pytest

from approvals_mcp import (
    ApprovalStatus,
    CONTRACTS,
    get_approval_status,
    record_decision,
    request_approval,
    reset_approvals,
)
from mcp_common import McpError, McpErrorCode


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_approvals()


def _open() -> str:
    r = request_approval(
        decision_id="dec-1",
        approver_group="rc-store-ops",
        proposal={"action": "mark_down", "sku": "sku-1"},
    )
    return r["pending_id"]


def test_request_returns_pending() -> None:
    r = request_approval("dec-1", "rc-store-ops", {"x": 1})
    assert r["status"] == ApprovalStatus.PENDING.value


def test_get_status_of_pending() -> None:
    pid = _open()
    got = get_approval_status(pid)
    assert got["status"] == ApprovalStatus.PENDING.value
    assert got["decision_id"] == "dec-1"


def test_record_approval() -> None:
    pid = _open()
    rec = record_decision(pid, "approved", "alice@example.com", "looks fine")
    assert rec["status"] == ApprovalStatus.APPROVED.value
    assert rec["approver_id"] == "alice@example.com"
    assert rec["rationale"] == "looks fine"


def test_record_rejection() -> None:
    pid = _open()
    rec = record_decision(pid, "rejected", "bob@example.com", "over threshold")
    assert rec["status"] == ApprovalStatus.REJECTED.value


def test_record_twice_conflicts() -> None:
    pid = _open()
    record_decision(pid, "approved", "alice@example.com")
    with pytest.raises(McpError) as exc:
        record_decision(pid, "rejected", "bob@example.com")
    assert exc.value.code is McpErrorCode.CONFLICT


def test_record_pending_rejected_explicitly() -> None:
    pid = _open()
    with pytest.raises(McpError) as exc:
        record_decision(pid, "pending", "alice@example.com")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_get_unknown() -> None:
    with pytest.raises(McpError) as exc:
        get_approval_status("nonexistent")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_contracts_count() -> None:
    assert len(CONTRACTS) == 3
