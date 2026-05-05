"""Tests for apex_orchestrator.orchestrator.parent + agents.base_agent — Sprint 26 Tasks 26.7 + 26.8."""

from __future__ import annotations

import sys
import time

import pytest

from apex_orchestrator.agents.base_agent import (
    BaseAgent,
    BudgetExceeded,
    CancelRequested,
)
from apex_orchestrator.control_plane.redis_client import (
    CONTROL_PLANE_UNREACHABLE,
    CancelLevel,
    RedisControlPlane,
    StubRedis,
)
from apex_orchestrator.orchestrator.parent import (
    BudgetEnvelope,
    ChildSpawn,
    ParentOrchestrator,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def context():
    stub = StubRedis()
    redis = RedisControlPlane(stub)
    cosmos: list[tuple[str, dict]] = []
    events: list[tuple[str, dict]] = []
    parent = ParentOrchestrator(
        redis,
        emit_event=lambda t, p: events.append((t, p)),
        cosmos_writer=lambda k, v: cosmos.append((k, v)),
    )
    return stub, redis, parent, cosmos, events


# ---------------------------------------------------------------------------
# ParentOrchestrator
# ---------------------------------------------------------------------------


def test_on_child_spawn_writes_cosmos_first_then_redis(context) -> None:
    stub, redis, parent, cosmos, events = context
    spawn = ChildSpawn(
        run_id="r1", child_id="c1", archetype="arch.recovery.001",
        envelope=BudgetEnvelope(tool_calls=50, tokens=10000, cost_cents=200, wall_s=900),
    )
    parent.on_child_spawn(spawn)
    # Cosmos got the durable record
    assert any("runs/r1/children/c1" in k for k, _ in cosmos)
    # Redis got the cancel-token-none + budget zeros
    assert redis.get_cancel_token("r1") == "none"
    counters = redis.get_budget_counters("r1", "c1")
    assert counters.tool_calls == 0
    # Status event emitted
    assert any(t == "child_spawn" for t, _ in events)


def test_on_cancel_level_change_writes_both_paths(context) -> None:
    _, redis, parent, cosmos, events = context
    parent.on_child_spawn(ChildSpawn(run_id="r1", child_id="c1", archetype="x"))
    parent.on_cancel_level_change("r1", CancelLevel.SOFT)
    assert redis.get_cancel_token("r1") == "soft"
    assert any(k.endswith("cancel_level") for k, _ in cosmos)
    assert any(t == "cancel_level_change" for t, _ in events)


def test_on_child_complete_expires_run_keys(context) -> None:
    _, redis, parent, cosmos, events = context
    parent.on_child_spawn(ChildSpawn(run_id="r1", child_id="c1", archetype="x"))
    parent.on_child_complete("r1", "c1", ttl_s=300)
    assert any("status" in k for k, _ in cosmos)
    assert any(t == "child_complete" for t, _ in events)


def test_on_child_spawn_redis_unavailable_still_writes_cosmos(context) -> None:
    """Sprint 26 — Cosmos is the durable record; Redis is the fast read path.
    Redis loss must NOT prevent the spawn from being recorded."""
    stub, _, parent, cosmos, _ = context
    stub.fail_all = True
    parent.on_child_spawn(ChildSpawn(run_id="r1", child_id="c1", archetype="x"))
    assert any("runs/r1/children/c1" in k for k, _ in cosmos)


# ---------------------------------------------------------------------------
# BaseAgent — cancel polling
# ---------------------------------------------------------------------------


def test_base_agent_check_cancel_passes_when_none(context) -> None:
    _, redis, _, _, _ = context
    agent = BaseAgent(run_id="r1", child_id="c1", redis=redis, envelope={})
    agent.check_cancel()  # No raise — cancel level is "none"


def test_base_agent_check_cancel_raises_on_soft(context) -> None:
    _, redis, _, _, _ = context
    redis.set_cancel_token("r1", CancelLevel.SOFT)
    agent = BaseAgent(run_id="r1", child_id="c1", redis=redis, envelope={})
    with pytest.raises(CancelRequested, match="soft"):
        agent.check_cancel()


def test_base_agent_check_cancel_failclosed_when_redis_dead_and_no_cosmos(context) -> None:
    """Sprint 26 — Redis dead + no Cosmos fallback ⇒ self-cancel with control_plane_unreachable."""
    stub, redis, _, _, _ = context
    stub.fail_all = True
    agent = BaseAgent(
        run_id="r1", child_id="c1", redis=redis, envelope={},
        backoff_max_s=0.01,
    )
    with pytest.raises(CancelRequested):
        agent.check_cancel()


def test_base_agent_falls_back_to_cosmos_when_redis_dead(context) -> None:
    stub, redis, _, _, _ = context
    stub.fail_all = True

    def cosmos_read(run_id: str, key: str) -> dict:
        return {"level": "hard"}

    agent = BaseAgent(
        run_id="r1", child_id="c1", redis=redis, envelope={},
        cosmos_fallback=cosmos_read, backoff_max_s=0.01,
    )
    with pytest.raises(CancelRequested, match="hard"):
        agent.check_cancel()


# ---------------------------------------------------------------------------
# BaseAgent — budget enforcement
# ---------------------------------------------------------------------------


def test_base_agent_increment_budget_within_envelope(context) -> None:
    _, redis, _, _, _ = context
    agent = BaseAgent(
        run_id="r1", child_id="c1", redis=redis,
        envelope={"tool_calls": 100},
    )
    agent.increment_and_check_budget("tool_calls", 1)
    agent.increment_and_check_budget("tool_calls", 50)
    counters = redis.get_budget_counters("r1", "c1")
    assert counters.tool_calls == 51


def test_base_agent_budget_exceeded_raises(context) -> None:
    _, redis, _, _, _ = context
    agent = BaseAgent(
        run_id="r1", child_id="c1", redis=redis,
        envelope={"tool_calls": 5},
    )
    agent.increment_and_check_budget("tool_calls", 5)  # at cap, ok
    with pytest.raises(BudgetExceeded, match="tool_calls"):
        agent.increment_and_check_budget("tool_calls", 1)


def test_base_agent_no_envelope_means_no_check(context) -> None:
    _, redis, _, _, _ = context
    agent = BaseAgent(run_id="r1", child_id="c1", redis=redis, envelope={})
    # No envelope cap for "tool_calls" — increment unbounded
    for _ in range(100):
        agent.increment_and_check_budget("tool_calls", 1)


# ---------------------------------------------------------------------------
# BaseAgent — heartbeat
# ---------------------------------------------------------------------------


def test_base_agent_heartbeat_emits_on_first_call(context) -> None:
    _, redis, _, _, _ = context
    agent = BaseAgent(
        run_id="r1", child_id="c1", redis=redis,
        heartbeat_interval_s=30,
    )
    assert agent.maybe_heartbeat() is True
    assert redis.is_child_alive("r1", "c1") is True


def test_base_agent_heartbeat_throttles_within_interval(context) -> None:
    _, redis, _, _, _ = context
    agent = BaseAgent(
        run_id="r1", child_id="c1", redis=redis,
        heartbeat_interval_s=30,
    )
    now = time.time()
    assert agent.maybe_heartbeat(now_s=now) is True
    assert agent.maybe_heartbeat(now_s=now + 5) is False
    assert agent.maybe_heartbeat(now_s=now + 31) is True


# ---------------------------------------------------------------------------
# Conformance
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_spawn_writes_cancel_and_budget_to_redis(context) -> None:
    """Sprint 26 Task 26.7.1."""
    _, redis, parent, _, _ = context
    parent.on_child_spawn(ChildSpawn(run_id="r1", child_id="c1", archetype="x"))
    assert redis.get_cancel_token("r1") == "none"
    counters = redis.get_budget_counters("r1", "c1")
    assert counters.tool_calls == 0


@pytest.mark.conformance
def test_conformance_base_agent_self_cancels_on_dual_failure(context) -> None:
    """Sprint 26 Task 26.8.4 — Redis + Cosmos both down ⇒ self-cancel."""
    stub, redis, _, _, _ = context
    stub.fail_all = True
    agent = BaseAgent(
        run_id="r1", child_id="c1", redis=redis, envelope={},
        backoff_max_s=0.01,
    )
    with pytest.raises(CancelRequested):
        agent.check_cancel()
