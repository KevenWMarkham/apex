"""Child-agent base class — Sprint 26 Task 26.8.

Replaces Cosmos-backed cancel-token polling and budget-counter reads
with the Redis control plane. Cosmos remains the durable record;
Redis is the fast read path. On Redis-unreachable, the base class
falls back to Cosmos with exponential backoff; if both fail, the
agent self-cancels with reason ``control_plane_unreachable``.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from apex_orchestrator.control_plane.redis_client import (
    CONTROL_PLANE_UNREACHABLE,
    BudgetCounters,
    CancelLevel,
    RedisControlPlane,
    RedisUnavailable,
)


log = logging.getLogger("apex.orchestrator.agents.base_agent")


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class CancelRequested(RuntimeError):
    """Raised when the cancel token has crossed into pause/soft/hard/abort."""


class BudgetExceeded(RuntimeError):
    """Raised when a budget counter has crossed its envelope."""


# ---------------------------------------------------------------------------
# Base agent
# ---------------------------------------------------------------------------


@dataclass
class BaseAgent:
    """Deployment-neutral child-agent logic.

    Production deployments wrap this in the Azure AI Agent Service SDK
    (or equivalent). The orchestration logic — heartbeat cadence,
    cancel-token polling, budget enforcement — lives here.
    """

    run_id: str
    child_id: str
    redis: RedisControlPlane
    envelope: dict[str, int] = field(default_factory=dict)
    """Budget envelope from spawn config — keys: tool_calls, tokens,
    cost_cents, wall_s."""

    cosmos_fallback: Optional[Callable[[str, str], dict]] = None
    """Cosmos fallback reader for cancel/budget when Redis is down.
    Production injects a Cosmos client; tests inject a stub."""

    heartbeat_interval_s: int = 30
    heartbeat_ttl_s: int = 60
    backoff_max_s: float = 30.0

    _last_heartbeat_s: float = 0.0
    _last_cancel_check_s: float = 0.0
    _redis_failure_count: int = 0

    # -- cancel-token check -------------------------------------------

    def check_cancel(self) -> None:
        """Sprint 26 Task 26.8.1 — Redis-first cancel polling.

        Raises :class:`CancelRequested` if the token has crossed into a
        cancel level. Falls back to Cosmos with exponential backoff if
        Redis is down. Self-cancels with ``control_plane_unreachable``
        if both are down.
        """
        try:
            level_raw = self.redis.get_cancel_token(self.run_id)
            self._redis_failure_count = 0
            level = CancelLevel(level_raw) if level_raw in CancelLevel._value2member_map_ else CancelLevel.NONE
            if level != CancelLevel.NONE:
                raise CancelRequested(
                    f"cancel level {level.value} on run {self.run_id}"
                )
            return
        except RedisUnavailable:
            pass  # Fall through to Cosmos
        except CancelRequested:
            raise
        except Exception as exc:
            log.warning(
                "agent.check_cancel.redis_path_failed",
                extra={"run_id": self.run_id, "error": str(exc)},
            )

        # Cosmos fallback
        self._redis_failure_count += 1
        backoff = min(
            self.backoff_max_s,
            0.1 * (2 ** self._redis_failure_count),
        )
        time.sleep(backoff)
        if self.cosmos_fallback is not None:
            try:
                doc = self.cosmos_fallback(self.run_id, "cancel_level")
                level_str = doc.get("level", "none") if isinstance(doc, dict) else "none"
                if level_str != "none":
                    raise CancelRequested(
                        f"cancel level {level_str} on run {self.run_id} (cosmos fallback)"
                    )
                return
            except CancelRequested:
                raise
            except Exception as exc:
                log.error(
                    "agent.check_cancel.cosmos_path_failed",
                    extra={"run_id": self.run_id, "error": str(exc)},
                )
        # Both Redis and Cosmos failed — self-cancel
        raise CancelRequested(CONTROL_PLANE_UNREACHABLE)

    # -- budget check + increment ------------------------------------

    def increment_and_check_budget(self, metric: str, amount: int = 1) -> None:
        """Sprint 26 Task 26.8.2 — atomic INCR-then-check.

        Raises :class:`BudgetExceeded` if the post-INCR value crosses
        the envelope cap for ``metric``. On Redis failure, fall back to
        Cosmos for the read; if both fail, self-cancel.
        """
        cap = self.envelope.get(metric)
        if cap is None:
            return  # No cap configured for this metric
        try:
            new_value = self.redis.increment_budget_counter(
                self.run_id, self.child_id, metric, amount,
            )
            if new_value > cap:
                raise BudgetExceeded(
                    f"{metric}={new_value} exceeds envelope cap {cap}"
                )
            return
        except RedisUnavailable:
            pass

        # Cosmos fallback for the read; can't atomic-INCR through Cosmos
        if self.cosmos_fallback is not None:
            try:
                doc = self.cosmos_fallback(self.run_id, f"budget/{self.child_id}")
                cur = (doc.get(metric, 0) if isinstance(doc, dict) else 0) + amount
                if cur > cap:
                    raise BudgetExceeded(
                        f"{metric}={cur} exceeds envelope cap {cap} (cosmos fallback)"
                    )
                return
            except BudgetExceeded:
                raise
            except Exception:
                pass
        # Both failed — fail-closed treats as exceeded
        raise BudgetExceeded(f"control plane unreachable; treating {metric} as exceeded")

    # -- heartbeat ---------------------------------------------------

    def maybe_heartbeat(self, now_s: Optional[float] = None) -> bool:
        """Sprint 26 Task 26.8.3 — emit a heartbeat every 30s.

        Returns True iff this call actually emitted (i.e., interval
        elapsed since last emission). Idempotent — safe to call from a
        tight inner loop.
        """
        now = now_s if now_s is not None else time.time()
        if (now - self._last_heartbeat_s) < self.heartbeat_interval_s:
            return False
        self.redis.heartbeat(self.run_id, self.child_id, ttl_s=self.heartbeat_ttl_s)
        self._last_heartbeat_s = now
        return True
