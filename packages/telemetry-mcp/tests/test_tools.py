"""Tests for telemetry-mcp tools."""

from __future__ import annotations

import pytest

from mcp_common import McpError, McpErrorCode
from telemetry_mcp import (
    CONTRACTS,
    EVENTS,
    TRACES,
    emit_trace,
    log_event,
    query_latency_percentile,
    record_latency,
    reset_telemetry,
)


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_telemetry()


def test_emit_trace_persists() -> None:
    r = emit_trace({"operation_id": "op-1", "tool_name": "foo"})
    assert "trace_record_id" in r
    assert len(TRACES) == 1


def test_log_event_persists() -> None:
    r = log_event("info", "hello", {"k": 1})
    assert "event_id" in r
    assert EVENTS[-1]["level"] == "info"


def test_log_event_bad_level() -> None:
    with pytest.raises(McpError) as exc:
        log_event("spam", "hello")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_latency_percentile() -> None:
    for ms in range(1, 101):
        record_latency("op-a", ms)
    r = query_latency_percentile("op-a", 95)
    assert r["sample_count"] == 100
    assert 90 <= r["value_ms"] <= 100


def test_latency_percentile_empty() -> None:
    with pytest.raises(McpError) as exc:
        query_latency_percentile("nope", 50)
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_latency_bad_percentile() -> None:
    record_latency("x", 10)
    with pytest.raises(McpError) as exc:
        query_latency_percentile("x", 100)
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_contracts_count() -> None:
    assert len(CONTRACTS) == 3
