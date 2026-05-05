"""Approvals client protocol — orchestrator → approvals-mcp seam."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable
from uuid import uuid4


@runtime_checkable
class ApprovalsClient(Protocol):
    """Narrow protocol for the approvals seam.

    Production maps onto ``approvals-mcp`` tools. Tests inject
    :class:`InMemoryApprovalsClient`.
    """

    def request(self, decision_id: str, approver_group: str, proposal: dict) -> str: ...
    def poll(self, pending_id: str) -> dict: ...
    def finalise(self, pending_id: str, decision: str, approver_id: str, rationale: str) -> dict: ...


@dataclass
class InMemoryApprovalsClient:
    """In-memory approvals — identical semantics to `approvals-mcp` for tests."""

    _pending: dict[str, dict[str, Any]] = field(default_factory=dict)

    def request(self, decision_id: str, approver_group: str, proposal: dict) -> str:
        pid = str(uuid4())
        self._pending[pid] = {
            "pending_id": pid,
            "decision_id": decision_id,
            "approver_group": approver_group,
            "proposal": proposal,
            "status": "pending",
            "approver_id": None,
            "rationale": "",
        }
        return pid

    def poll(self, pending_id: str) -> dict:
        if pending_id not in self._pending:
            raise KeyError(f"No pending approval {pending_id!r}")
        return dict(self._pending[pending_id])

    def finalise(
        self,
        pending_id: str,
        decision: str,
        approver_id: str,
        rationale: str = "",
    ) -> dict:
        if pending_id not in self._pending:
            raise KeyError(f"No pending approval {pending_id!r}")
        rec = self._pending[pending_id]
        if rec["status"] != "pending":
            raise ValueError(f"Approval {pending_id} already finalised as {rec['status']}")
        rec["status"] = decision
        rec["approver_id"] = approver_id
        rec["rationale"] = rationale
        return dict(rec)
