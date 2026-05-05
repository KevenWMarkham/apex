"""ferc-mcp tool implementations."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Protocol, runtime_checkable

from apex_core.types import Classification
from mcp_common import McpError, McpErrorCode, ToolContract, traced_call

SERVER_NAME = "ferc-mcp"
TOOL_VERSION = "1.0.0"


@runtime_checkable
class FercBackend(Protocol):
    def list_enforcement(self, since: date, limit: int) -> list[dict]: ...
    def get_interconnection(self, queue_id: str) -> dict | None: ...
    def list_filings(self, filer: str, since: date, limit: int) -> list[dict]: ...


@dataclass
class InMemoryFercBackend:
    enforcement: list[dict] = field(default_factory=list)
    interconnection: dict[str, dict] = field(default_factory=dict)
    filings: list[dict] = field(default_factory=list)

    def list_enforcement(self, since: date, limit: int) -> list[dict]:
        return [r for r in self.enforcement if date.fromisoformat(r["date"]) >= since][:limit]

    def get_interconnection(self, queue_id: str) -> dict | None:
        return self.interconnection.get(queue_id)

    def list_filings(self, filer: str, since: date, limit: int) -> list[dict]:
        return [
            f for f in self.filings
            if f["filer"] == filer and date.fromisoformat(f["filed_date"]) >= since
        ][:limit]


FERC_BACKEND: FercBackend = InMemoryFercBackend()


def set_ferc_backend(backend: FercBackend) -> None:
    global FERC_BACKEND
    FERC_BACKEND = backend


def _parse_date(iso: str, field_name: str) -> date:
    try:
        return date.fromisoformat(iso)
    except ValueError as exc:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=f"{field_name} must be YYYY-MM-DD (got {iso!r})",
        ) from exc


def list_enforcement_actions(
    since_iso: str,
    limit: int = 50,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """List FERC enforcement actions since a date."""
    since = _parse_date(since_iso, "since_iso")
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_enforcement_actions",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"since_iso": since_iso, "limit": limit},
        classification_applied=[Classification.PUBLIC],
    ) as ctx:
        rows = FERC_BACKEND.list_enforcement(since, limit)
        ctx["result"] = rows
        return rows


def get_interconnection_queue_status(
    queue_id: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict:
    """Return the current queue status for an interconnection request."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_interconnection_queue_status",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"queue_id": queue_id},
        classification_applied=[Classification.PUBLIC],
    ) as ctx:
        row = FERC_BACKEND.get_interconnection(queue_id)
        if row is None:
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message=f"No interconnection queue entry {queue_id!r}",
            )
        ctx["result"] = row
        return row


def list_compliance_filings(
    filer: str,
    since_iso: str,
    limit: int = 50,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """List compliance filings by a specific filer since a date."""
    since = _parse_date(since_iso, "since_iso")
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_compliance_filings",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"filer": filer, "since_iso": since_iso, "limit": limit},
        classification_applied=[Classification.PUBLIC],
    ) as ctx:
        rows = FERC_BACKEND.list_filings(filer, since, limit)
        ctx["result"] = rows
        return rows


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.list_enforcement_actions", version=TOOL_VERSION,
        description="List FERC enforcement actions since a date.",
        classification_propagation=[Classification.PUBLIC],
    ),
    ToolContract(
        name=f"{SERVER_NAME}.get_interconnection_queue_status", version=TOOL_VERSION,
        description="Return an interconnection queue's current status.",
        classification_propagation=[Classification.PUBLIC],
    ),
    ToolContract(
        name=f"{SERVER_NAME}.list_compliance_filings", version=TOOL_VERSION,
        description="List compliance filings by a filer since a date.",
        classification_propagation=[Classification.PUBLIC],
    ),
]
