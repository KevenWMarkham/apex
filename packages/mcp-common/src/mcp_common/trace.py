"""Per-tool-call trace record (APEX_Design §7.3)."""

from __future__ import annotations

import hashlib
import json
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Callable, Iterator
from uuid import UUID, uuid4

from apex_core.types import Classification

_TRACE_SINK: Callable[["ToolTraceRecord"], None] | None = None


@dataclass(frozen=True, slots=True)
class ToolTraceRecord:
    """One trace emitted per MCP tool call.

    Every field here propagates into the Decision Audit Row `tools_called`
    list (APEX_Design §11.2).
    """

    operation_id: UUID
    agent_id: str
    tool_name: str
    tool_version: str
    parameters_hash: str
    result_hash: str
    latency_ms: int
    classification_applied: list[Classification]
    caller_identity: str
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    error_class: str | None = None


def compute_hash(payload: Any) -> str:
    """Content-hash any JSON-serialisable payload (deterministic SHA-256).

    Used for ``parameters_hash`` and ``result_hash`` in the trace record.
    """
    try:
        blob = json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    except TypeError:
        blob = str(payload).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def set_trace_sink(sink: Callable[[ToolTraceRecord], None]) -> None:
    """Replace the module-level trace sink (tests / OpenTelemetry exporter)."""
    global _TRACE_SINK
    _TRACE_SINK = sink


def get_trace_sink() -> Callable[[ToolTraceRecord], None]:
    """Return the current trace sink; a no-op by default."""
    return _TRACE_SINK or (lambda _r: None)


def emit_trace(record: ToolTraceRecord) -> None:
    """Emit a trace record through the module-level sink."""
    get_trace_sink()(record)


@contextmanager
def traced_call(
    *,
    tool_name: str,
    tool_version: str = "1.0.0",
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
    parameters: Any = None,
    classification_applied: list[Classification] | None = None,
) -> Iterator[dict[str, Any]]:
    """Context manager that emits a ``ToolTraceRecord`` when the block exits.

    Usage::

        with traced_call(tool_name="fabric-mcp.get_entity_by_key",
                         parameters={"key": "sku:1"}) as ctx:
            result = do_work()
            ctx["result"] = result

    The context dict is used for the caller to store the result so the
    wrapper can compute ``result_hash``. ``error_class`` is populated if an
    exception escapes the block; the exception re-raises after emission.
    """
    start = time.perf_counter_ns()
    ctx: dict[str, Any] = {}
    params_hash = compute_hash(parameters)
    op_id = uuid4()
    error_class: str | None = None
    try:
        yield ctx
    except Exception as exc:
        error_class = type(exc).__name__
        raise
    finally:
        elapsed_ms = max(1, (time.perf_counter_ns() - start) // 1_000_000)
        emit_trace(
            ToolTraceRecord(
                operation_id=op_id,
                agent_id=agent_id,
                tool_name=tool_name,
                tool_version=tool_version,
                parameters_hash=params_hash,
                result_hash=compute_hash(ctx.get("result")),
                latency_ms=int(elapsed_ms),
                classification_applied=classification_applied or [],
                caller_identity=caller_identity,
                error_class=error_class,
            )
        )
