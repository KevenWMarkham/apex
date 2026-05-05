"""Parent orchestrator — Sprint 26 Task 26.7.

Production deployments wire this on top of Azure Durable Functions; the
class here is the **deployment-neutral logic** that Durable Functions
hosts via a thin entry-point. Cosmos / DF entities remain the durable
source of truth for orchestrator state — this class just lights up
the fast Redis read path on top.

Lifecycle hooks (Task 26.7.1-3):

- :meth:`on_child_spawn` — write cancel token (null) + budget envelope to Redis
- :meth:`on_cancel_level_change` — write new level (pause/soft/hard/abort)
  to Redis + emit cancel event to Event Hubs
- :meth:`on_child_complete` — schedule TTL-expire of run keys within 5 min
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable

from apex_orchestrator.control_plane.redis_client import (
    CancelLevel,
    RedisControlPlane,
    RedisUnavailable,
)


log = logging.getLogger("apex.orchestrator.orchestrator.parent")


@dataclass
class BudgetEnvelope:
    """Per-child budget — passed to the child at spawn time."""

    tool_calls: int = 100
    tokens: int = 50_000
    cost_cents: int = 500
    wall_s: int = 1800


@dataclass
class ChildSpawn:
    """One child spawn intent."""

    run_id: str
    child_id: str
    archetype: str
    """Sprint 19 archetype id, e.g., ``arch.recovery.001``."""

    envelope: BudgetEnvelope = field(default_factory=BudgetEnvelope)
    trigger_source: str = "operator"
    """``operator:<upn>`` / ``heartbeat:<routine>`` / ``api:<scope>``."""


class ParentOrchestrator:
    """Deployment-neutral parent-orchestrator logic."""

    def __init__(
        self,
        redis: RedisControlPlane,
        *,
        emit_event: Callable[[str, dict[str, Any]], None] = lambda _t, _p: None,
        cosmos_writer: Callable[[str, dict[str, Any]], None] = lambda _k, _p: None,
    ) -> None:
        self._r = redis
        self._emit = emit_event
        self._cosmos = cosmos_writer

    # -- spawn --------------------------------------------------------

    def on_child_spawn(self, spawn: ChildSpawn) -> None:
        """Sprint 26 Task 26.7.1 — write cancel-null + budget envelope."""
        # Cosmos is the durable record — write first
        self._cosmos(
            f"runs/{spawn.run_id}/children/{spawn.child_id}",
            {
                "child_id": spawn.child_id,
                "archetype": spawn.archetype,
                "envelope": vars(spawn.envelope),
                "trigger_source": spawn.trigger_source,
                "cancel_level": "none",
            },
        )
        # Light up the Redis fast read path
        try:
            self._r.set_cancel_token(spawn.run_id, CancelLevel.NONE)
        except RedisUnavailable as exc:
            log.warning(
                "orchestrator.spawn.redis_unavailable_cosmos_only",
                extra={"run_id": spawn.run_id, "error": str(exc)},
            )
        # Pre-seed budget counters at zero
        for metric in ("tool_calls", "tokens", "cost_cents", "wall_s"):
            try:
                # incrby 0 is a no-op write that creates the key at zero
                self._r.increment_budget_counter(spawn.run_id, spawn.child_id, metric, 0)
            except RedisUnavailable:
                pass
        self._emit("child_spawn", {
            "run_id": spawn.run_id, "child_id": spawn.child_id,
            "archetype": spawn.archetype,
            "trigger_source": spawn.trigger_source,
        })

    # -- cancel-level change -----------------------------------------

    def on_cancel_level_change(self, run_id: str, level: CancelLevel) -> None:
        """Sprint 26 Task 26.7.2 — write new cancel level + emit event."""
        # Cosmos durable record first
        self._cosmos(f"runs/{run_id}/cancel_level", {"level": level.value})
        try:
            self._r.set_cancel_token(run_id, level)
        except RedisUnavailable as exc:
            log.error(
                "orchestrator.cancel.redis_unavailable",
                extra={"run_id": run_id, "level": level.value, "error": str(exc)},
            )
        self._emit("cancel_level_change", {
            "run_id": run_id, "level": level.value,
        })

    # -- complete -----------------------------------------------------

    def on_child_complete(self, run_id: str, child_id: str, ttl_s: int = 300) -> None:
        """Sprint 26 Task 26.7.3 — TTL-expire run keys within 5 min."""
        self._cosmos(
            f"runs/{run_id}/children/{child_id}/status",
            {"status": "complete"},
        )
        self._r.expire_run_keys(run_id, ttl_s)
        self._emit("child_complete", {
            "run_id": run_id, "child_id": child_id,
        })
