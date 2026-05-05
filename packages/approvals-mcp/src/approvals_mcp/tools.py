"""approvals-mcp tool implementations."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from mcp_common import McpError, McpErrorCode, ToolContract, traced_call

SERVER_NAME = "approvals-mcp"
TOOL_VERSION = "1.0.0"


class ApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"
    OVERRIDDEN = "overridden"
    EXPIRED = "expired"


# In-memory store: pending_id → record dict
_APPROVALS: dict[str, dict[str, Any]] = {}


def reset_approvals() -> None:
    """Test helper — clear the in-memory store."""
    _APPROVALS.clear()


def request_approval(
    decision_id: str,
    approver_group: str,
    proposal: dict[str, Any],
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, str]:
    """Open a pending approval. Returns the ``pending_id``."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.request_approval",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"decision_id": decision_id, "approver_group": approver_group},
    ) as ctx:
        pid = str(uuid4())
        _APPROVALS[pid] = {
            "pending_id": pid,
            "decision_id": decision_id,
            "approver_group": approver_group,
            "proposal": proposal,
            "status": ApprovalStatus.PENDING.value,
            "requested_at": datetime.now(UTC).isoformat(),
            "approver_id": None,
            "decided_at": None,
            "rationale": "",
        }
        ctx["result"] = {"pending_id": pid, "status": ApprovalStatus.PENDING.value}
        return {"pending_id": pid, "status": ApprovalStatus.PENDING.value}


def get_approval_status(
    pending_id: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Fetch an approval's current state."""
    rec = _APPROVALS.get(pending_id)
    if rec is None:
        raise McpError(
            code=McpErrorCode.NOT_FOUND,
            message=f"No approval with id {pending_id!r}",
        )
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_approval_status",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"pending_id": pending_id},
    ) as ctx:
        ctx["result"] = rec
        return rec


def record_decision(
    pending_id: str,
    decision: str,
    approver_id: str,
    rationale: str = "",
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Finalise an approval with approve / reject / modify."""
    rec = _APPROVALS.get(pending_id)
    if rec is None:
        raise McpError(
            code=McpErrorCode.NOT_FOUND,
            message=f"No approval with id {pending_id!r}",
        )
    if rec["status"] != ApprovalStatus.PENDING.value:
        raise McpError(
            code=McpErrorCode.CONFLICT,
            message=f"Approval {pending_id} already finalised as {rec['status']}",
        )
    try:
        status = ApprovalStatus(decision)
    except ValueError as exc:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=f"Unknown decision {decision!r}",
        ) from exc
    if status is ApprovalStatus.PENDING:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="Cannot record a 'pending' decision — only finalise states are allowed.",
        )
    with traced_call(
        tool_name=f"{SERVER_NAME}.record_decision",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"pending_id": pending_id, "decision": decision, "approver_id": approver_id},
    ) as ctx:
        rec["status"] = status.value
        rec["approver_id"] = approver_id
        rec["decided_at"] = datetime.now(UTC).isoformat()
        rec["rationale"] = rationale
        ctx["result"] = rec
        return rec


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.request_approval", version=TOOL_VERSION,
        description="Open a pending HITL approval; returns pending_id.",
    ),
    ToolContract(
        name=f"{SERVER_NAME}.get_approval_status", version=TOOL_VERSION,
        description="Fetch the current state of a pending approval.",
    ),
    ToolContract(
        name=f"{SERVER_NAME}.record_decision", version=TOOL_VERSION,
        description="Finalise an approval with approve / reject / modify / overridden / expired.",
    ),
]
