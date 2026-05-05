"""pharma-recall-mcp tool implementations."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Protocol, runtime_checkable

from apex_core.types import Classification
from mcp_common import McpError, McpErrorCode, ToolContract, traced_call

SERVER_NAME = "pharma-recall-mcp"
TOOL_VERSION = "1.0.0"

# Matches NDC pattern from apex-schemas-common.standards.types.NdcCode
_NDC_PATTERN = re.compile(r"^\d{4,5}-\d{3,4}-\d{1,2}$")


@runtime_checkable
class PharmaRecallBackend(Protocol):
    def list_recalls(self, since: date, limit: int) -> list[dict]: ...
    def search_by_ndc(self, ndc: str, limit: int) -> list[dict]: ...
    def get_recall(self, recall_id: str) -> dict | None: ...


@dataclass
class InMemoryPharmaRecallBackend:
    recalls: list[dict] = field(default_factory=list)

    def list_recalls(self, since: date, limit: int) -> list[dict]:
        out = [r for r in self.recalls if date.fromisoformat(r["recall_date"]) >= since]
        return out[:limit]

    def search_by_ndc(self, ndc: str, limit: int) -> list[dict]:
        out = [r for r in self.recalls if ndc in r.get("ndc_codes", [])]
        return out[:limit]

    def get_recall(self, recall_id: str) -> dict | None:
        return next((r for r in self.recalls if r["recall_id"] == recall_id), None)


PHARMA_BACKEND: PharmaRecallBackend = InMemoryPharmaRecallBackend()


def set_pharma_backend(backend: PharmaRecallBackend) -> None:
    global PHARMA_BACKEND
    PHARMA_BACKEND = backend


def list_pharma_recalls(
    since_iso: str,
    limit: int = 50,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """List pharmaceutical recalls since a date (YYYY-MM-DD)."""
    try:
        since = date.fromisoformat(since_iso)
    except ValueError as exc:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=f"since_iso must be YYYY-MM-DD (got {since_iso!r})",
        ) from exc
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_pharma_recalls",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"since_iso": since_iso, "limit": limit},
        classification_applied=[Classification.PUBLIC],
    ) as ctx:
        rows = PHARMA_BACKEND.list_recalls(since, limit)
        ctx["result"] = rows
        return rows


def search_recalls_by_ndc(
    ndc: str,
    limit: int = 50,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """Find recalls affecting an NDC code."""
    if not _NDC_PATTERN.match(ndc):
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=f"Invalid NDC format {ndc!r} (expect NNNNN-NNN-NN)",
        )
    with traced_call(
        tool_name=f"{SERVER_NAME}.search_recalls_by_ndc",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"ndc": ndc, "limit": limit},
        classification_applied=[Classification.PUBLIC],
    ) as ctx:
        rows = PHARMA_BACKEND.search_by_ndc(ndc, limit)
        ctx["result"] = rows
        return rows


def get_recall_detail(
    recall_id: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict:
    """Return the full pharmaceutical-recall record."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_recall_detail",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"recall_id": recall_id},
        classification_applied=[Classification.PUBLIC],
    ) as ctx:
        row = PHARMA_BACKEND.get_recall(recall_id)
        if row is None:
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message=f"No pharma recall {recall_id!r}",
            )
        ctx["result"] = row
        return row


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.list_pharma_recalls", version=TOOL_VERSION,
        description="List pharmaceutical recalls since a date.",
        classification_propagation=[Classification.PUBLIC],
    ),
    ToolContract(
        name=f"{SERVER_NAME}.search_recalls_by_ndc", version=TOOL_VERSION,
        description="Find recalls that reference a specific NDC.",
        classification_propagation=[Classification.PUBLIC],
    ),
    ToolContract(
        name=f"{SERVER_NAME}.get_recall_detail", version=TOOL_VERSION,
        description="Return the full pharmaceutical-recall record by id.",
        classification_propagation=[Classification.PUBLIC],
    ),
]
