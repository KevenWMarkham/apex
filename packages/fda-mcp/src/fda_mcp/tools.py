"""fda-mcp tool implementations."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Protocol, runtime_checkable

from apex_core.types import Classification
from mcp_common import McpError, McpErrorCode, ToolContract, traced_call

SERVER_NAME = "fda-mcp"
TOOL_VERSION = "1.0.0"


@runtime_checkable
class FdaBackend(Protocol):
    def list_recalls(self, since: date, limit: int) -> list[dict]: ...
    def get_recall(self, recall_id: str) -> dict | None: ...
    def search_adverse_events(self, product: str, limit: int) -> list[dict]: ...


@dataclass
class InMemoryFdaBackend:
    """Dev / test backend. Production swaps for openFDA REST client."""

    recalls: list[dict] = field(default_factory=list)
    adverse_events: list[dict] = field(default_factory=list)

    def list_recalls(self, since: date, limit: int) -> list[dict]:
        out = [r for r in self.recalls if date.fromisoformat(r["event_date"]) >= since]
        return out[:limit]

    def get_recall(self, recall_id: str) -> dict | None:
        return next((r for r in self.recalls if r["recall_id"] == recall_id), None)

    def search_adverse_events(self, product: str, limit: int) -> list[dict]:
        out = [e for e in self.adverse_events if product.lower() in e.get("product", "").lower()]
        return out[:limit]


FDA_BACKEND: FdaBackend = InMemoryFdaBackend()


def set_fda_backend(backend: FdaBackend) -> None:
    global FDA_BACKEND
    FDA_BACKEND = backend


def list_recalls_by_date(
    since_iso: str,
    limit: int = 50,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """List FDA recall events on or after ``since_iso`` (YYYY-MM-DD)."""
    try:
        since = date.fromisoformat(since_iso)
    except ValueError as exc:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=f"since_iso must be YYYY-MM-DD (got {since_iso!r})",
        ) from exc
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_recalls_by_date",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"since_iso": since_iso, "limit": limit},
        classification_applied=[Classification.PUBLIC],
    ) as ctx:
        rows = FDA_BACKEND.list_recalls(since, limit)
        ctx["result"] = rows
        return rows


def get_recall_detail(
    recall_id: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict:
    """Return the full recall record for ``recall_id``."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_recall_detail",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"recall_id": recall_id},
        classification_applied=[Classification.PUBLIC],
    ) as ctx:
        row = FDA_BACKEND.get_recall(recall_id)
        if row is None:
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message=f"No recall with id {recall_id!r}",
            )
        ctx["result"] = row
        return row


def search_adverse_events(
    product: str,
    limit: int = 50,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """Search adverse-event reports by product name (case-insensitive substring)."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.search_adverse_events",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"product": product, "limit": limit},
        classification_applied=[Classification.PUBLIC],
    ) as ctx:
        rows = FDA_BACKEND.search_adverse_events(product, limit)
        ctx["result"] = rows
        return rows


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.list_recalls_by_date", version=TOOL_VERSION,
        description="List FDA recall events since a date.",
        classification_propagation=[Classification.PUBLIC],
    ),
    ToolContract(
        name=f"{SERVER_NAME}.get_recall_detail", version=TOOL_VERSION,
        description="Fetch a recall record by id.",
        classification_propagation=[Classification.PUBLIC],
    ),
    ToolContract(
        name=f"{SERVER_NAME}.search_adverse_events", version=TOOL_VERSION,
        description="Search FDA adverse-event reports by product.",
        classification_propagation=[Classification.PUBLIC],
    ),
]
