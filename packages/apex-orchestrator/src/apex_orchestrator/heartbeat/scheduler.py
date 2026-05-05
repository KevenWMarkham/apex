"""HEARTBEAT scheduler — Sprint 26 Task 26.9.2-4.

Production deployments wire this on top of Azure Durable Functions
timers. The class here holds the **deployment-neutral logic**:

- Register one timer per routine (Task 26.9.2)
- On trigger fire, spawn a fresh agent run through the full 10-step
  boot sequence with ``trigger_source: heartbeat:<routine_name>``
  (Task 26.9.3)
- Missed triggers (Redis unreachable, orchestrator down) emit
  ``heartbeat_missed`` event; no auto-catch-up (Task 26.9.4)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable

from apex_orchestrator.heartbeat.parser import HeartbeatRoutine
from apex_orchestrator.orchestrator.parent import (
    BudgetEnvelope,
    ChildSpawn,
    ParentOrchestrator,
)


log = logging.getLogger("apex.orchestrator.heartbeat.scheduler")


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TriggerFire:
    """One trigger-fire event for an audit / status stream."""

    routine_name: str
    fired_at: datetime
    trigger_source: str
    """Always ``heartbeat:<routine_name>`` per §26.9.3."""

    spawned_run_id: str | None = None


@dataclass(frozen=True)
class HeartbeatMissedEvent:
    """One missed-trigger event."""

    routine_name: str
    missed_at: datetime
    reason: str


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------


@dataclass
class HeartbeatScheduler:
    """Deployment-neutral HEARTBEAT scheduler logic."""

    routines: list[HeartbeatRoutine]
    parent: ParentOrchestrator
    spawn_run_id_factory: Callable[[str], str] = field(
        default=lambda routine_name: f"hb-{routine_name}-{int(datetime.now(timezone.utc).timestamp())}"
    )
    """Factory for run ids — production injects a UUID-based factory."""

    emit_event: Callable[[str, dict], None] = field(default=lambda _t, _p: None)
    """Status-channel emitter — typically ``telemetry-mcp.emit``."""

    def fire_trigger(self, routine_name: str) -> TriggerFire:
        """Fire one routine — spawn a fresh agent run (Task 26.9.3)."""
        routine = self._lookup(routine_name)
        run_id = self.spawn_run_id_factory(routine_name)
        envelope = self._envelope_from_budget(routine.budget)
        spawn = ChildSpawn(
            run_id=run_id,
            child_id="root",
            archetype=routine.orch,
            envelope=envelope,
            trigger_source=f"heartbeat:{routine_name}",
        )
        self.parent.on_child_spawn(spawn)
        evt = TriggerFire(
            routine_name=routine_name,
            fired_at=datetime.now(timezone.utc),
            trigger_source=spawn.trigger_source,
            spawned_run_id=run_id,
        )
        self.emit_event("heartbeat_fired", {
            "routine": routine_name,
            "run_id": run_id,
            "fired_at_utc": evt.fired_at.isoformat(),
            "trigger_source": spawn.trigger_source,
        })
        log.info(
            "heartbeat.fired",
            extra={
                "routine": routine_name,
                "run_id": run_id,
                "trigger_source": spawn.trigger_source,
            },
        )
        return evt

    def emit_missed(
        self, routine_name: str, reason: str
    ) -> HeartbeatMissedEvent:
        """Emit a missed-trigger event (Task 26.9.4) — no auto-catch-up."""
        # Confirm routine is real — emit-missed for an unknown routine is
        # a programming error
        self._lookup(routine_name)
        evt = HeartbeatMissedEvent(
            routine_name=routine_name,
            missed_at=datetime.now(timezone.utc),
            reason=reason,
        )
        self.emit_event("heartbeat_missed", {
            "routine": routine_name,
            "missed_at_utc": evt.missed_at.isoformat(),
            "reason": reason,
        })
        log.warning(
            "heartbeat.missed",
            extra={"routine": routine_name, "reason": reason},
        )
        return evt

    # -- helpers -----------------------------------------------------

    def _lookup(self, routine_name: str) -> HeartbeatRoutine:
        for r in self.routines:
            if r.name == routine_name:
                return r
        raise KeyError(
            f"Routine {routine_name!r} not in scheduler. Known: "
            f"{sorted(r.name for r in self.routines)}"
        )

    @staticmethod
    def _envelope_from_budget(budget: dict) -> BudgetEnvelope:
        return BudgetEnvelope(
            tool_calls=int(budget.get("tool_calls", 100)),
            tokens=int(budget.get("tokens", 50_000)),
            cost_cents=int(budget.get("cost_cents", 500)),
            wall_s=int(budget.get("wall_s", 1800)),
        )
