"""Tests for apex_orchestrator.control_plane.redis_client — Sprint 26 Task 26.4.

Covers all 10 named methods + happy-path + failure-mode per build
instructions §3.1. Uses :class:`StubRedis` rather than a Redis test
container so the suite runs without Docker.
"""

from __future__ import annotations

import json
import sys
import time

import pytest

from apex_orchestrator.control_plane.redis_client import (
    CONTROL_PLANE_UNREACHABLE,
    BudgetCounters,
    CancelLevel,
    RedisControlPlane,
    RedisUnavailable,
    StubRedis,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def stub() -> StubRedis:
    return StubRedis()


@pytest.fixture
def cp(stub: StubRedis) -> RedisControlPlane:
    return RedisControlPlane(stub)


# ---------------------------------------------------------------------------
# 1 + 2: cancel token
# ---------------------------------------------------------------------------


def test_cancel_token_default_is_none(cp: RedisControlPlane) -> None:
    assert cp.get_cancel_token("run-1") == "none"


def test_cancel_token_round_trip(cp: RedisControlPlane) -> None:
    cp.set_cancel_token("run-1", CancelLevel.SOFT)
    assert cp.get_cancel_token("run-1") == "soft"
    cp.set_cancel_token("run-1", CancelLevel.ABORT)
    assert cp.get_cancel_token("run-1") == "abort"


def test_set_cancel_token_accepts_string(cp: RedisControlPlane) -> None:
    cp.set_cancel_token("run-1", "hard")
    assert cp.get_cancel_token("run-1") == "hard"


def test_get_cancel_token_raises_on_redis_failure(cp: RedisControlPlane, stub: StubRedis) -> None:
    """Sprint 26 — RedisControlPlane surfaces failure; BaseAgent does the
    fail-closed-to-abort decision after consulting Cosmos per build §3.5."""
    stub.fail_all = True
    with pytest.raises(RedisUnavailable):
        cp.get_cancel_token("run-x")


def test_set_cancel_token_raises_on_redis_failure(cp: RedisControlPlane, stub: StubRedis) -> None:
    stub.fail_all = True
    with pytest.raises(RedisUnavailable):
        cp.set_cancel_token("run-1", CancelLevel.PAUSE)


# ---------------------------------------------------------------------------
# 3 + 4: budget counters
# ---------------------------------------------------------------------------


def test_budget_counter_increments(cp: RedisControlPlane) -> None:
    assert cp.increment_budget_counter("r", "c", "tool_calls", 1) == 1
    assert cp.increment_budget_counter("r", "c", "tool_calls", 4) == 5
    counters = cp.get_budget_counters("r", "c")
    assert counters.tool_calls == 5


def test_budget_counters_default_to_zero(cp: RedisControlPlane) -> None:
    counters = cp.get_budget_counters("r-fresh", "c-fresh")
    assert counters.tool_calls == 0
    assert counters.tokens == 0


def test_budget_counters_failclosed_to_exhausted(cp: RedisControlPlane, stub: StubRedis) -> None:
    """Failclosed read returns sys.maxsize on every metric."""
    stub.fail_all = True
    counters = cp.get_budget_counters("r", "c")
    assert counters.tool_calls == sys.maxsize
    assert counters.tokens == sys.maxsize
    assert counters.cost_cents == sys.maxsize
    assert counters.wall_s == sys.maxsize


def test_increment_budget_counter_raises_on_redis_failure(
    cp: RedisControlPlane, stub: StubRedis,
) -> None:
    stub.fail_all = True
    with pytest.raises(RedisUnavailable):
        cp.increment_budget_counter("r", "c", "tool_calls")


# ---------------------------------------------------------------------------
# 5 + 6: heartbeat + liveness
# ---------------------------------------------------------------------------


def test_heartbeat_sets_alive(cp: RedisControlPlane) -> None:
    cp.heartbeat("run-1", "child-1", ttl_s=60)
    assert cp.is_child_alive("run-1", "child-1") is True


def test_no_heartbeat_means_dead(cp: RedisControlPlane) -> None:
    assert cp.is_child_alive("run-x", "child-x") is False


def test_is_child_alive_failclosed_to_dead(cp: RedisControlPlane, stub: StubRedis) -> None:
    cp.heartbeat("run-1", "child-1", ttl_s=60)
    stub.fail_all = True
    assert cp.is_child_alive("run-1", "child-1") is False


def test_heartbeat_failure_is_non_fatal(cp: RedisControlPlane, stub: StubRedis) -> None:
    """Heartbeat write failures do NOT raise — caller carries on."""
    stub.fail_next = True
    cp.heartbeat("run-1", "child-1")  # Should not raise


# ---------------------------------------------------------------------------
# 7 + 8: HITL deadline queue
# ---------------------------------------------------------------------------


def test_enqueue_hitl_round_trips(cp: RedisControlPlane) -> None:
    cp.enqueue_hitl("hitl-1", deadline_unix=100, payload={"gate": "g1"})
    cp.enqueue_hitl("hitl-2", deadline_unix=200, payload={"gate": "g2"})
    expired = cp.pop_expired_hitl(now_unix=150)
    assert expired == ["hitl-1"]
    # hitl-2 still pending
    expired_again = cp.pop_expired_hitl(now_unix=150)
    assert expired_again == []


def test_pop_expired_hitl_returns_in_deadline_order(cp: RedisControlPlane) -> None:
    cp.enqueue_hitl("h-c", deadline_unix=300, payload={})
    cp.enqueue_hitl("h-a", deadline_unix=100, payload={})
    cp.enqueue_hitl("h-b", deadline_unix=200, payload={})
    expired = cp.pop_expired_hitl(now_unix=350)
    assert expired == ["h-a", "h-b", "h-c"]


def test_enqueue_hitl_raises_on_redis_failure(cp: RedisControlPlane, stub: StubRedis) -> None:
    stub.fail_all = True
    with pytest.raises(RedisUnavailable):
        cp.enqueue_hitl("h", deadline_unix=1, payload={})


def test_pop_expired_hitl_failclosed_to_empty(cp: RedisControlPlane, stub: StubRedis) -> None:
    cp.enqueue_hitl("h", deadline_unix=1, payload={})
    stub.fail_all = True
    assert cp.pop_expired_hitl(now_unix=10) == []


# ---------------------------------------------------------------------------
# 9 + 10: MCP response cache
# ---------------------------------------------------------------------------


def test_cache_round_trip(cp: RedisControlPlane) -> None:
    cached = cp.cache_mcp_response(
        "rc.item.get", "abc123", "scope-1", {"id": 1, "sku": "X"}, ttl_s=30,
        classification="Internal",
    )
    assert cached is True
    hit = cp.get_cached_mcp_response("rc.item.get", "abc123", "scope-1")
    assert hit == {"id": 1, "sku": "X"}


def test_cache_miss_returns_none(cp: RedisControlPlane) -> None:
    assert cp.get_cached_mcp_response("rc.item.get", "abc123", "scope-1") is None


def test_cache_skips_restricted_classifications(cp: RedisControlPlane) -> None:
    """Sprint 26 governance — PII/PCI/Confidential/etc. NEVER cache."""
    for cls in ("Restricted-PII", "Restricted-PCI", "Confidential", "phi", "pii", "payment-card"):
        ok = cp.cache_mcp_response(
            "rc.payment.method.get", "x", "scope-1", {"card": "x"}, ttl_s=30,
            classification=cls,
        )
        assert ok is False, f"classification {cls!r} must not cache"


def test_cache_skips_oversize_payloads() -> None:
    cp = RedisControlPlane(StubRedis(), cache_size_limit_bytes=100)
    big = {"data": "x" * 1000}
    ok = cp.cache_mcp_response(
        "rc.item.get", "x", "scope-1", big, ttl_s=30, classification="Internal",
    )
    assert ok is False


def test_cache_get_failclosed_to_miss(cp: RedisControlPlane, stub: StubRedis) -> None:
    cp.cache_mcp_response("rc.item.get", "k", "scope-1", {"v": 1}, ttl_s=30)
    stub.fail_all = True
    assert cp.get_cached_mcp_response("rc.item.get", "k", "scope-1") is None


def test_cache_write_failure_returns_false(cp: RedisControlPlane, stub: StubRedis) -> None:
    stub.fail_next = True
    ok = cp.cache_mcp_response("rc.item.get", "k", "scope-1", {"v": 1}, ttl_s=30)
    assert ok is False


# ---------------------------------------------------------------------------
# Key naming convention (Sprint 26 Task 26.5.4)
# ---------------------------------------------------------------------------


def test_cache_key_includes_entra_scope() -> None:
    """Two calls with same tool+args but different Entra scopes don't collide."""
    cp = RedisControlPlane(StubRedis())
    cp.cache_mcp_response("rc.item.get", "k1", "scope-A", {"v": 1}, ttl_s=30)
    cp.cache_mcp_response("rc.item.get", "k1", "scope-B", {"v": 2}, ttl_s=30)
    assert cp.get_cached_mcp_response("rc.item.get", "k1", "scope-A") == {"v": 1}
    assert cp.get_cached_mcp_response("rc.item.get", "k1", "scope-B") == {"v": 2}


def test_run_keys_expire_on_completion(cp: RedisControlPlane) -> None:
    cp.set_cancel_token("run-1", CancelLevel.NONE)
    cp.expire_run_keys("run-1", ttl_s=300)
    # Sanity — the call doesn't raise on absence either
    cp.expire_run_keys("does-not-exist", ttl_s=300)


# ---------------------------------------------------------------------------
# Conformance markers — Sprint 26 acceptance
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_all_ten_methods_present() -> None:
    """Sprint 26 Task 26.4.1 — the 10 named methods all exist."""
    expected = {
        "set_cancel_token",
        "get_cancel_token",
        "increment_budget_counter",
        "get_budget_counters",
        "heartbeat",
        "is_child_alive",
        "enqueue_hitl",
        "pop_expired_hitl",
        "cache_mcp_response",
        "get_cached_mcp_response",
    }
    actual = {name for name in dir(RedisControlPlane) if not name.startswith("_")}
    assert expected.issubset(actual), f"Missing: {expected - actual}"


@pytest.mark.conformance
def test_conformance_failclosed_constant_named() -> None:
    """The CONTROL_PLANE_UNREACHABLE reason string is exported for child agents."""
    assert CONTROL_PLANE_UNREACHABLE == "control_plane_unreachable"


@pytest.mark.conformance
def test_conformance_never_cache_classifications_complete() -> None:
    """The runtime backstop covers all classifications APEX-CORE §11 forbids."""
    cp = RedisControlPlane(StubRedis())
    for cls in ("Restricted-PII", "Restricted-PCI", "Confidential",
                "phi", "pii", "payment-card"):
        assert not cp.cache_mcp_response(
            "rc.x", "h", "s", {"v": 1}, ttl_s=30, classification=cls,
        )
