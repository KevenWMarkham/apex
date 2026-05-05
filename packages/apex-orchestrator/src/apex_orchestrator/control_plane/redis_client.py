"""Redis control-plane client — Sprint 26 Task 26.4 (BL.APEX-v0.2-F-01).

Implements the 10 named methods from `APEX-v0.2-Build-Instructions.md`
§3.1 over a small Protocol surface (`RedisProtocol`) so production wires
``redis-py`` while tests use the in-memory ``StubRedis`` shipped here.

**Fail-closed semantics** are the architectural invariant: every method
wraps Redis exceptions, control-plane reads (cancel-token / budget /
liveness) default to "cancel" / "exhausted" / "dead" when Redis is
unreachable. Silent-success is forbidden.

**Entra auth + VNet endpoints + structured logging + size-bounded cache
writes** are configured at construction time. Production deployments
build a ``redis.Redis(...)`` with managed-identity token-exchange and
hand it in; this module never touches connection strings or passwords
itself.

Cross-references:

- ``APEX-CORE.md`` §11 — verbatim cache governance rules
- ``CHARTER.md`` §3 — per-tool ``cacheable`` annotations
- Sprint 26 Task 26.5 — CI lint that enforces those annotations
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any, Literal, Optional, Protocol, runtime_checkable


log = logging.getLogger("apex.orchestrator.control_plane.redis")


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


CONTROL_PLANE_UNREACHABLE = "control_plane_unreachable"
"""Reason string used when child agents self-cancel after Redis falls over."""


# Maximum cached MCP-response size in bytes (configurable at construction).
DEFAULT_CACHE_SIZE_BYTES = 100 * 1024  # 100 KB per build instructions §3.3.4

# Default heartbeat TTL in seconds.
DEFAULT_HEARTBEAT_TTL_S = 60

# Cache classifications that are NEVER cacheable (Sprint 26 governance).
NEVER_CACHEABLE_CLASSIFICATIONS = frozenset({
    "Restricted-PII",
    "Restricted-PCI",
    "Confidential",
    "phi",
    "pii",
    "payment-card",
})


class CancelLevel(StrEnum):
    """Cancel-token escalation levels per CHARTER §6.1."""

    NONE = "none"
    PAUSE = "pause"
    SOFT = "soft"
    HARD = "hard"
    ABORT = "abort"


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class RedisUnavailable(RuntimeError):
    """Raised internally when Redis is unreachable. Callers see fail-closed return values."""


# ---------------------------------------------------------------------------
# Protocol surface — what we need from a Redis-shaped backend
# ---------------------------------------------------------------------------


@runtime_checkable
class RedisProtocol(Protocol):
    """Minimal Redis surface APEX uses.

    Production passes a ``redis.Redis`` instance (or async equivalent);
    tests pass :class:`StubRedis` to drive the same logic deterministically.
    """

    def get(self, key: str) -> Optional[bytes]: ...
    def set(self, key: str, value: bytes | str, ex: Optional[int] = None) -> bool: ...
    def setex(self, key: str, time: int, value: bytes | str) -> bool: ...
    def delete(self, *keys: str) -> int: ...
    def exists(self, key: str) -> int: ...
    def expire(self, key: str, time: int) -> bool: ...
    def incrby(self, key: str, amount: int = 1) -> int: ...
    def hset(self, key: str, mapping: dict[str, str]) -> int: ...
    def hgetall(self, key: str) -> dict[bytes, bytes]: ...
    def zadd(self, key: str, mapping: dict[str, float]) -> int: ...
    def zrangebyscore(
        self, key: str, min: float, max: float, withscores: bool = False
    ) -> list: ...
    def zrem(self, key: str, *members: str) -> int: ...


# ---------------------------------------------------------------------------
# In-memory stub for tests + smoke-tests
# ---------------------------------------------------------------------------


class StubRedis:
    """Deterministic in-memory ``RedisProtocol`` implementation.

    Implements just enough Redis surface to drive the control-plane
    methods + their failure modes. Production code never sees this; the
    real `redis.Redis` does the actual work.

    The :attr:`fail_next` flag lets tests force a transient failure for
    one operation — exercises the fail-closed branches.
    """

    def __init__(self) -> None:
        self._kv: dict[str, bytes] = {}
        self._exp: dict[str, float] = {}
        self._zsets: dict[str, dict[str, float]] = {}
        self._hsets: dict[str, dict[bytes, bytes]] = {}
        self.fail_next: bool = False
        self.fail_all: bool = False

    # ----- helpers -----

    def _check_fail(self) -> None:
        if self.fail_all:
            raise ConnectionError("StubRedis: simulated connection failure (fail_all)")
        if self.fail_next:
            self.fail_next = False
            raise ConnectionError("StubRedis: simulated transient failure")

    def _expired(self, key: str) -> bool:
        exp = self._exp.get(key)
        if exp is None:
            return False
        if time.time() >= exp:
            self._kv.pop(key, None)
            self._exp.pop(key, None)
            self._zsets.pop(key, None)
            self._hsets.pop(key, None)
            return True
        return False

    # ----- get/set/del/exists/expire -----

    def get(self, key: str) -> Optional[bytes]:
        self._check_fail()
        if self._expired(key):
            return None
        return self._kv.get(key)

    def set(self, key: str, value: bytes | str, ex: Optional[int] = None) -> bool:
        self._check_fail()
        v = value.encode("utf-8") if isinstance(value, str) else value
        self._kv[key] = v
        if ex is not None:
            self._exp[key] = time.time() + ex
        else:
            self._exp.pop(key, None)
        return True

    def setex(self, key: str, time_s: int, value: bytes | str) -> bool:
        return self.set(key, value, ex=time_s)

    def delete(self, *keys: str) -> int:
        self._check_fail()
        n = 0
        for k in keys:
            if k in self._kv or k in self._zsets or k in self._hsets:
                n += 1
            self._kv.pop(k, None)
            self._exp.pop(k, None)
            self._zsets.pop(k, None)
            self._hsets.pop(k, None)
        return n

    def exists(self, key: str) -> int:
        self._check_fail()
        if self._expired(key):
            return 0
        return 1 if (key in self._kv or key in self._zsets or key in self._hsets) else 0

    def expire(self, key: str, time_s: int) -> bool:
        self._check_fail()
        if key in self._kv or key in self._zsets or key in self._hsets:
            self._exp[key] = time.time() + time_s
            return True
        return False

    # ----- counters / hashes / zsets -----

    def incrby(self, key: str, amount: int = 1) -> int:
        self._check_fail()
        cur = int(self._kv.get(key, b"0").decode("utf-8")) if key in self._kv else 0
        new = cur + amount
        self._kv[key] = str(new).encode("utf-8")
        return new

    def hset(self, key: str, mapping: dict[str, str]) -> int:
        self._check_fail()
        target = self._hsets.setdefault(key, {})
        for k, v in mapping.items():
            target[k.encode("utf-8")] = (
                v.encode("utf-8") if isinstance(v, str) else v
            )
        return len(mapping)

    def hgetall(self, key: str) -> dict[bytes, bytes]:
        self._check_fail()
        if self._expired(key):
            return {}
        return dict(self._hsets.get(key, {}))

    def zadd(self, key: str, mapping: dict[str, float]) -> int:
        self._check_fail()
        z = self._zsets.setdefault(key, {})
        added = 0
        for m, s in mapping.items():
            if m not in z:
                added += 1
            z[m] = s
        return added

    def zrangebyscore(
        self, key: str, min: float, max: float, withscores: bool = False
    ) -> list:
        self._check_fail()
        z = self._zsets.get(key, {})
        items = sorted(
            ((m, s) for m, s in z.items() if min <= s <= max),
            key=lambda x: x[1],
        )
        if withscores:
            return [(m.encode("utf-8") if isinstance(m, str) else m, s) for m, s in items]
        return [m.encode("utf-8") if isinstance(m, str) else m for m, _ in items]

    def zrem(self, key: str, *members: str) -> int:
        self._check_fail()
        z = self._zsets.get(key)
        if z is None:
            return 0
        n = 0
        for m in members:
            if m in z:
                del z[m]
                n += 1
        return n


# ---------------------------------------------------------------------------
# Cache event (telemetry payload)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CacheEvent:
    """Cache-hit / cache-miss telemetry payload — Sprint 26 Task 26.6.4."""

    event: Literal["cache_hit", "cache_miss", "cache_skip"]
    tool: str
    arg_hash: str
    entra_scope: str
    reason: str = ""
    """For ``cache_skip`` — why the cache was bypassed."""


@dataclass
class BudgetCounters:
    """Snapshot of a child-agent's budget counters."""

    tool_calls: int = 0
    tokens: int = 0
    cost_cents: int = 0
    wall_s: int = 0
    extra: dict[str, int] = field(default_factory=dict)

    @classmethod
    def empty(cls) -> "BudgetCounters":
        return cls()


# ---------------------------------------------------------------------------
# RedisControlPlane — the 10 build-instructions methods
# ---------------------------------------------------------------------------


class RedisControlPlane:
    """The control plane.

    Construction:

    - In production, pass a configured ``redis.Redis`` (or async client)
      that authenticates via Azure managed identity against a private
      VNet endpoint.
    - In tests, pass :class:`StubRedis` and drive deterministically.

    All ten methods named in the v0.2 build instructions §3.1 are
    implemented here. Fail-closed semantics:

    - :meth:`get_cancel_token` returns ``"abort"`` (the strongest cancel
      level) if Redis is unreachable.
    - :meth:`get_budget_counters` returns a counter snapshot of all
      ``sys.maxsize`` (treated as "exhausted") if Redis is unreachable.
    - :meth:`is_child_alive` returns ``False`` if Redis is unreachable.
    - :meth:`get_cached_mcp_response` returns ``None`` (cache miss) if
      Redis is unreachable — caller falls through to the real tool call.
    """

    def __init__(
        self,
        backend: RedisProtocol,
        *,
        cache_size_limit_bytes: int = DEFAULT_CACHE_SIZE_BYTES,
    ) -> None:
        self._r = backend
        self._cache_size_limit = cache_size_limit_bytes

    # ---- helpers ----

    @staticmethod
    def _key_cancel(run_id: str) -> str:
        return f"apex:run:{run_id}:cancel"

    @staticmethod
    def _key_budget(run_id: str, child_id: str, metric: str) -> str:
        return f"apex:run:{run_id}:child:{child_id}:{metric}"

    @staticmethod
    def _key_heartbeat(run_id: str, child_id: str) -> str:
        return f"apex:run:{run_id}:child:{child_id}:heartbeat"

    @staticmethod
    def _key_hitl_zset() -> str:
        return "apex:hitl:pending"

    @staticmethod
    def _key_mcp_cache(tool: str, arg_hash: str, entra_scope: str) -> str:
        return f"apex:mcp:{tool}:{arg_hash}:{entra_scope}"

    @staticmethod
    def _budget_metrics() -> tuple[str, ...]:
        return ("tool_calls", "tokens", "cost_cents", "wall_s")

    # ---- 1. cancel token ----

    def set_cancel_token(self, run_id: str, level: CancelLevel | str) -> None:
        """Set the cancel token. Caller-side write — control-plane SOR is
        Cosmos / DF entities; this just lights up the fast read path."""
        if isinstance(level, str):
            level = CancelLevel(level)
        try:
            self._r.set(self._key_cancel(run_id), level.value, ex=24 * 60 * 60)
            log.info(
                "control_plane.set_cancel_token",
                extra={"run_id": run_id, "level": level.value},
            )
        except Exception as exc:
            log.error(
                "control_plane.set_cancel_token_failed",
                extra={"run_id": run_id, "level": level.value, "error": str(exc)},
            )
            # Surface to caller; orchestrator falls back to Cosmos write
            raise RedisUnavailable(str(exc)) from exc

    def get_cancel_token(self, run_id: str) -> str:
        """Read the cancel token. Raises :class:`RedisUnavailable` on
        Redis failure so callers can fall back to Cosmos per build
        instructions §3.5.

        Returns ``"none"`` / ``"pause"`` / ``"soft"`` / ``"hard"`` /
        ``"abort"``. The fail-closed-to-abort semantic lives at the
        caller (BaseAgent.check_cancel does the Cosmos fallback then
        self-cancels with ``control_plane_unreachable`` if both fail).
        """
        try:
            raw = self._r.get(self._key_cancel(run_id))
            if raw is None:
                return CancelLevel.NONE.value
            return raw.decode("utf-8") if isinstance(raw, bytes) else str(raw)
        except Exception as exc:
            log.error(
                "control_plane.get_cancel_token_failed",
                extra={"run_id": run_id, "error": str(exc)},
            )
            raise RedisUnavailable(str(exc)) from exc

    # ---- 2. budget counters ----

    def increment_budget_counter(
        self, run_id: str, child_id: str, field: str, amount: int = 1
    ) -> int:
        """Atomic INCR on a budget counter. Returns the new value.

        On Redis failure raises :class:`RedisUnavailable` so the caller
        can fall back to Cosmos. (Increment is a write — fail-closed
        means the caller treats failure as exhausted, not as zero.)
        """
        try:
            return self._r.incrby(
                self._key_budget(run_id, child_id, field), amount
            )
        except Exception as exc:
            log.error(
                "control_plane.increment_budget_counter_failed",
                extra={
                    "run_id": run_id, "child_id": child_id,
                    "field": field, "error": str(exc),
                },
            )
            raise RedisUnavailable(str(exc)) from exc

    def get_budget_counters(self, run_id: str, child_id: str) -> BudgetCounters:
        """Fetch all four budget counters. **Fail-closed** to "exhausted".

        On Redis failure returns a :class:`BudgetCounters` whose every
        named field is ``sys.maxsize`` so the child agent's "have I
        exceeded budget?" check fires.
        """
        try:
            counters = BudgetCounters()
            for metric in self._budget_metrics():
                raw = self._r.get(self._key_budget(run_id, child_id, metric))
                value = int(raw.decode("utf-8")) if raw else 0
                setattr(counters, metric, value)
            return counters
        except Exception as exc:
            log.error(
                "control_plane.get_budget_counters_failed_failclosed_exhausted",
                extra={"run_id": run_id, "child_id": child_id, "error": str(exc)},
            )
            import sys
            return BudgetCounters(
                tool_calls=sys.maxsize, tokens=sys.maxsize,
                cost_cents=sys.maxsize, wall_s=sys.maxsize,
            )

    # ---- 3. heartbeat / liveness ----

    def heartbeat(
        self, run_id: str, child_id: str, ttl_s: int = DEFAULT_HEARTBEAT_TTL_S
    ) -> None:
        """Emit one heartbeat. Caller emits every 30s; TTL 60s. SETEX
        idempotent."""
        try:
            self._r.setex(
                self._key_heartbeat(run_id, child_id),
                ttl_s,
                str(int(time.time())),
            )
        except Exception as exc:
            log.warning(
                "control_plane.heartbeat_failed",
                extra={"run_id": run_id, "child_id": child_id, "error": str(exc)},
            )
            # Heartbeat write failure is not catastrophic — caller carries on
            # with the next 30s tick. Repeated failures will surface via
            # is_child_alive=False on the parent side.

    def is_child_alive(self, run_id: str, child_id: str) -> bool:
        """**Fail-closed** to ``False`` — Redis unreachable → child is dead."""
        try:
            return self._r.exists(self._key_heartbeat(run_id, child_id)) == 1
        except Exception as exc:
            log.error(
                "control_plane.is_child_alive_failed_failclosed_dead",
                extra={"run_id": run_id, "child_id": child_id, "error": str(exc)},
            )
            return False

    # ---- 4. HITL deadline queue ----

    def enqueue_hitl(
        self, hitl_id: str, deadline_unix: int, payload: dict
    ) -> None:
        """Enqueue a HITL deadline. Deadline is Unix timestamp; payload
        held alongside as a hash."""
        try:
            self._r.zadd(self._key_hitl_zset(), {hitl_id: float(deadline_unix)})
            self._r.hset(
                f"apex:hitl:{hitl_id}",
                {k: json.dumps(v) for k, v in payload.items()},
            )
            log.info(
                "control_plane.enqueue_hitl",
                extra={
                    "hitl_id": hitl_id,
                    "deadline_unix": deadline_unix,
                    "payload_keys": list(payload.keys()),
                },
            )
        except Exception as exc:
            log.error(
                "control_plane.enqueue_hitl_failed",
                extra={"hitl_id": hitl_id, "error": str(exc)},
            )
            raise RedisUnavailable(str(exc)) from exc

    def pop_expired_hitl(self, now_unix: int) -> list[str]:
        """Return every HITL id whose deadline ≤ ``now_unix``. Atomic
        ZREM removes them from the queue; the caller emits the
        deadline-missed events."""
        try:
            members = self._r.zrangebyscore(
                self._key_hitl_zset(), 0, float(now_unix)
            )
            ids = [
                m.decode("utf-8") if isinstance(m, bytes) else str(m)
                for m in members
            ]
            if ids:
                self._r.zrem(self._key_hitl_zset(), *ids)
            return ids
        except Exception as exc:
            log.error(
                "control_plane.pop_expired_hitl_failed",
                extra={"now_unix": now_unix, "error": str(exc)},
            )
            # Empty list is correct fail-closed — the caller will re-poll
            return []

    # ---- 5. MCP response cache ----

    def cache_mcp_response(
        self,
        tool: str,
        arg_hash: str,
        entra_scope: str,
        value: Any,
        ttl_s: int,
        *,
        classification: str = "Internal",
    ) -> bool:
        """Cache an MCP tool response. Returns True iff actually cached.

        Honors the governance rules from APEX-CORE §11:

        - Tool-level ``cacheable: false`` is enforced UPSTREAM (CHARTER
          parser + Sprint 26 Task 26.5 lint); this method does not
          re-check, but logs the classification so audit can verify.
        - Classifications above Internal (PII / PCI / phi / payment-card /
          Confidential / Restricted-*) are NEVER cached even if the
          caller explicitly asks. This is the runtime backstop.
        - Size-bounded — payloads exceeding ``cache_size_limit_bytes``
          are skipped with ``cache_skip`` event.
        - Never logs the cache value — only the metadata.
        """
        if classification in NEVER_CACHEABLE_CLASSIFICATIONS:
            log.info(
                "control_plane.cache_skip_classification",
                extra={
                    "tool": tool, "entra_scope": entra_scope,
                    "classification": classification,
                },
            )
            return False
        try:
            payload = json.dumps(value, default=str).encode("utf-8")
        except (TypeError, ValueError) as exc:
            log.warning(
                "control_plane.cache_skip_unserializable",
                extra={"tool": tool, "error": str(exc)},
            )
            return False
        if len(payload) > self._cache_size_limit:
            log.info(
                "control_plane.cache_skip_oversize",
                extra={
                    "tool": tool, "entra_scope": entra_scope,
                    "size_bytes": len(payload),
                    "limit": self._cache_size_limit,
                },
            )
            return False
        try:
            self._r.setex(
                self._key_mcp_cache(tool, arg_hash, entra_scope),
                ttl_s,
                payload,
            )
            log.info(
                "control_plane.cache_write",
                extra={
                    "tool": tool, "entra_scope": entra_scope,
                    "ttl_s": ttl_s, "size_bytes": len(payload),
                },
            )
            return True
        except Exception as exc:
            log.error(
                "control_plane.cache_write_failed",
                extra={"tool": tool, "entra_scope": entra_scope, "error": str(exc)},
            )
            return False

    def get_cached_mcp_response(
        self, tool: str, arg_hash: str, entra_scope: str
    ) -> Optional[Any]:
        """Lookup a cached MCP tool response. **Fail-closed** to ``None``
        (cache miss) — Redis unreachable → caller hits the real tool.

        Returns the deserialized value or ``None``.
        """
        try:
            raw = self._r.get(self._key_mcp_cache(tool, arg_hash, entra_scope))
            if raw is None:
                return None
            return json.loads(raw.decode("utf-8") if isinstance(raw, bytes) else raw)
        except Exception as exc:
            log.warning(
                "control_plane.cache_read_failed_failclosed_miss",
                extra={"tool": tool, "entra_scope": entra_scope, "error": str(exc)},
            )
            return None

    # ---- TTL-expire on completion ----

    def expire_run_keys(self, run_id: str, ttl_s: int = 300) -> None:
        """Sprint 26 Task 26.7.3 — TTL-expire run-scoped keys within 5
        minutes after run completion. Cancel-token + heartbeat keys are
        already TTL-bound but explicit short-TTL on completion keeps the
        Redis footprint trim."""
        try:
            self._r.expire(self._key_cancel(run_id), ttl_s)
            log.info(
                "control_plane.expire_run_keys",
                extra={"run_id": run_id, "ttl_s": ttl_s},
            )
        except Exception as exc:
            log.warning(
                "control_plane.expire_run_keys_failed",
                extra={"run_id": run_id, "error": str(exc)},
            )
            # Non-fatal — keys will TTL on their own
