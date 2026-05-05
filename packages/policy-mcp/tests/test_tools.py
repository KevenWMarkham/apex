"""Tests for policy-mcp tools."""

from __future__ import annotations

import pytest

from mcp_common import McpError, McpErrorCode
from policy_mcp import CONTRACTS, check_compliance, classify_bump, evaluate_policy


def test_evaluate_policy_default_allow() -> None:
    result = evaluate_policy("rc.default", {"action": "read"})
    assert result["allowed"] is True


def test_check_compliance_patch_zero_touch() -> None:
    result = check_compliance("PATCH")
    assert result["gate_kind"] == "ZERO_TOUCH"


def test_check_compliance_minor_ack_only() -> None:
    result = check_compliance("MINOR")
    assert result["gate_kind"] == "ACK_ONLY"


def test_check_compliance_major_hitl() -> None:
    result = check_compliance("MAJOR")
    assert result["gate_kind"] == "HITL"


def test_check_compliance_unknown_class() -> None:
    with pytest.raises(McpError) as exc:
        check_compliance("NOPE")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_classify_bump_minor() -> None:
    result = classify_bump("1.2.3", "1.3.0")
    assert result["bump_class"] == "MINOR"


def test_classify_bump_bad_input() -> None:
    with pytest.raises(McpError):
        classify_bump("not-semver", "1.0.0")


def test_contracts_complete() -> None:
    names = {c.name for c in CONTRACTS}
    assert len(names) == 3
