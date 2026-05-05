"""Tests for apex_orchestrator.heartbeat — Sprint 26 Task 26.9."""

from __future__ import annotations

from pathlib import Path

import pytest

from apex_orchestrator.control_plane.redis_client import (
    RedisControlPlane,
    StubRedis,
)
from apex_orchestrator.heartbeat.parser import (
    HeartbeatParseError,
    HeartbeatRoutine,
    parse_heartbeat,
)
from apex_orchestrator.heartbeat.scheduler import (
    HeartbeatMissedEvent,
    HeartbeatScheduler,
    TriggerFire,
)
from apex_orchestrator.orchestrator.parent import (
    BudgetEnvelope,
    ChildSpawn,
    ParentOrchestrator,
)


HEARTBEAT_PATH = Path(__file__).resolve().parents[3] / "apex-workspace" / "HEARTBEAT.md"


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


def test_parse_existing_heartbeat_yields_four_routines() -> None:
    """Sprint 26 Task 26.1.1 ships exactly four routines."""
    routines = parse_heartbeat(HEARTBEAT_PATH)
    assert len(routines) == 4
    names = {r.name for r in routines}
    assert any("close" in n.lower() for n in names)
    assert any("vendor" in n.lower() for n in names)
    assert any("valuation" in n.lower() or "inventory" in n.lower() for n in names)
    assert any("hourly" in n.lower() or "run-state" in n.lower() for n in names)


def test_parsed_routines_carry_required_fields() -> None:
    routines = parse_heartbeat(HEARTBEAT_PATH)
    for r in routines:
        assert r.trigger
        assert r.orch
        assert r.oversight in {"HITL", "HOTL", "HIC"}


def test_parser_rejects_missing_file(tmp_path: Path) -> None:
    bad = tmp_path / "nope.md"
    with pytest.raises(HeartbeatParseError, match="not found"):
        parse_heartbeat(bad)


def test_parser_rejects_no_frontmatter(tmp_path: Path) -> None:
    bad = tmp_path / "HEARTBEAT.md"
    bad.write_text("# No frontmatter here", encoding="utf-8")
    with pytest.raises(HeartbeatParseError, match="frontmatter"):
        parse_heartbeat(bad)


def test_parser_rejects_wrong_file_marker(tmp_path: Path) -> None:
    bad = tmp_path / "HEARTBEAT.md"
    bad.write_text(
        "---\nfile: NOT_HEARTBEAT.md\n---\n# Body",
        encoding="utf-8",
    )
    with pytest.raises(HeartbeatParseError, match="file must be"):
        parse_heartbeat(bad)


def test_parser_rejects_routine_missing_required_fields(tmp_path: Path) -> None:
    bad = tmp_path / "HEARTBEAT.md"
    bad.write_text(
        "---\nfile: HEARTBEAT.md\n---\n"
        "## Routine 1 — Incomplete\n"
        "- **Trigger:** every hour\n"
        # Missing orch, budget, oversight
        ,
        encoding="utf-8",
    )
    with pytest.raises(HeartbeatParseError, match="missing required"):
        parse_heartbeat(bad)


def test_parser_extracts_budget_components() -> None:
    routines = parse_heartbeat(HEARTBEAT_PATH)
    monthly = next(r for r in routines if "close" in r.name.lower())
    assert monthly.budget.get("wall_s", 0) >= 3600  # at least 1 hour
    assert monthly.budget.get("tool_calls", 0) >= 100


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------


def _make_scheduler():
    routines = [
        HeartbeatRoutine(
            name="test-routine",
            trigger="every hour",
            orch="ORCH-RC-04",
            budget={"tool_calls": 50, "wall_s": 1800, "cost_cents": 500},
            oversight="HITL",
            on_failure="engagement-lead",
        ),
    ]
    redis = RedisControlPlane(StubRedis())
    cosmos_writes: list[tuple[str, dict]] = []
    events: list[tuple[str, dict]] = []
    parent = ParentOrchestrator(
        redis,
        emit_event=lambda t, p: events.append((t, p)),
        cosmos_writer=lambda k, v: cosmos_writes.append((k, v)),
    )
    sched = HeartbeatScheduler(
        routines=routines, parent=parent,
        emit_event=lambda t, p: events.append((t, p)),
    )
    return sched, parent, redis, events, cosmos_writes


def test_fire_trigger_spawns_with_heartbeat_trigger_source() -> None:
    sched, _parent, _redis, events, cosmos = _make_scheduler()
    fire = sched.fire_trigger("test-routine")
    assert isinstance(fire, TriggerFire)
    assert fire.trigger_source == "heartbeat:test-routine"
    assert fire.spawned_run_id
    # Cosmos got the durable record
    assert any("runs/" in k for k, _ in cosmos)
    # Status channel saw the trigger
    event_types = {t for t, _ in events}
    assert "child_spawn" in event_types
    assert "heartbeat_fired" in event_types


def test_fire_trigger_unknown_routine_raises() -> None:
    sched, _, _, _, _ = _make_scheduler()
    with pytest.raises(KeyError, match="not in scheduler"):
        sched.fire_trigger("does-not-exist")


def test_emit_missed_records_event_no_catchup() -> None:
    sched, _, _, events, cosmos = _make_scheduler()
    evt = sched.emit_missed("test-routine", reason="redis_unavailable")
    assert isinstance(evt, HeartbeatMissedEvent)
    assert evt.reason == "redis_unavailable"
    # Crucially — NO new run spawned (cosmos write list empty)
    assert all("child_spawn" not in t for t, _ in events)
    assert not any("runs/" in k for k, _ in cosmos)
    # The missed event is on the channel
    missed = [p for t, p in events if t == "heartbeat_missed"]
    assert len(missed) == 1


# ---------------------------------------------------------------------------
# Conformance
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_heartbeat_parses_at_orchestrator_startup() -> None:
    """Sprint 26 Task 26.9.1 — parser succeeds on the shipped HEARTBEAT.md."""
    routines = parse_heartbeat(HEARTBEAT_PATH)
    assert routines, "HEARTBEAT.md must contain at least one routine"


@pytest.mark.conformance
def test_conformance_heartbeat_trigger_source_format() -> None:
    """Sprint 26 Task 26.9.3 — trigger source format is `heartbeat:<name>`."""
    sched, _, _, _, _ = _make_scheduler()
    fire = sched.fire_trigger("test-routine")
    assert fire.trigger_source.startswith("heartbeat:")


@pytest.mark.conformance
def test_conformance_missed_trigger_does_not_auto_catchup() -> None:
    """Sprint 26 Task 26.9.4 — missed-trigger handling is announce-only."""
    sched, _, _, events, cosmos = _make_scheduler()
    sched.emit_missed("test-routine", reason="test")
    # No child_spawn events
    assert not any(t == "child_spawn" for t, _ in events)
