"""telemetry-mcp tool implementations."""

from __future__ import annotations

import bisect
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from mcp_common import McpError, McpErrorCode, ToolContract, traced_call

SERVER_NAME = "telemetry-mcp"
TOOL_VERSION = "1.0.0"

# Module-level in-memory sinks — swapped in production.
TRACES: list[dict[str, Any]] = []
EVENTS: list[dict[str, Any]] = []
LATENCIES: dict[str, list[int]] = {}


def reset_telemetry() -> None:
    """Test helper — clear in-memory sinks."""
    TRACES.clear()
    EVENTS.clear()
    LATENCIES.clear()


def emit_trace(
    record: dict[str, Any],
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, str]:
    """Accept and store one trace record."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.emit_trace",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"record_keys": sorted(record.keys())},
    ) as ctx:
        rid = str(uuid4())
        TRACES.append({**record, "_id": rid, "_received_at": datetime.now(UTC).isoformat()})
        ctx["result"] = {"trace_record_id": rid}
        return {"trace_record_id": rid}


def log_event(
    level: str,
    message: str,
    metadata: dict[str, Any] | None = None,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, str]:
    """Log one event at the given level."""
    if level.lower() not in {"debug", "info", "warning", "error", "critical"}:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=f"Unknown level {level!r}",
        )
    with traced_call(
        tool_name=f"{SERVER_NAME}.log_event",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"level": level},
    ) as ctx:
        eid = str(uuid4())
        EVENTS.append({
            "_id": eid,
            "level": level.lower(),
            "message": message,
            "metadata": metadata or {},
            "timestamp": datetime.now(UTC).isoformat(),
        })
        ctx["result"] = {"event_id": eid}
        return {"event_id": eid}


def record_latency(operation: str, latency_ms: int) -> None:
    """Test / internal helper — feed latency samples for later percentile queries."""
    LATENCIES.setdefault(operation, []).append(int(latency_ms))


def query_latency_percentile(
    operation: str,
    percentile: int = 95,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Return the observed latency percentile for ``operation``."""
    if not 1 <= percentile <= 99:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="percentile must be in [1, 99]",
        )
    with traced_call(
        tool_name=f"{SERVER_NAME}.query_latency_percentile",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"operation": operation, "percentile": percentile},
    ) as ctx:
        samples = sorted(LATENCIES.get(operation, []))
        if not samples:
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message=f"No samples for operation {operation!r}",
            )
        idx = min(len(samples) - 1, (percentile * len(samples)) // 100)
        value = samples[idx]
        result = {
            "operation": operation,
            "percentile": percentile,
            "value_ms": value,
            "sample_count": len(samples),
        }
        ctx["result"] = result
        return result


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.emit_trace", version=TOOL_VERSION,
        description="Accept and store a tool-call trace record.",
    ),
    ToolContract(
        name=f"{SERVER_NAME}.log_event", version=TOOL_VERSION,
        description="Log an event at a named level (debug/info/warning/error/critical).",
    ),
    ToolContract(
        name=f"{SERVER_NAME}.query_latency_percentile", version=TOOL_VERSION,
        description="Return observed latency percentile for an operation.",
    ),
]
