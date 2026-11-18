"""Four gate-kind runners: ZERO_TOUCH · ACK_ONLY · HITL · ESCALATION."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Protocol

from apex_core.types import GateKind

from apex_orchestrator.gates.approvals import ApprovalsClient


@dataclass(frozen=True, slots=True)
class GateOutcome:
    """The result of applying a gate to a proposal."""

    kind: GateKind
    status: str
    """'approved' · 'rejected' · 'pending' · 'auto_applied' · 'acknowledged' · 'escalated'."""
    pending_id: str | None = None
    approver_id: str | None = None
    rationale: str = ""
    occurred_at: datetime | None = None

    @staticmethod
    def now() -> datetime:
        """Return the current UTC time."""
        return datetime.now(UTC)


class GateRunner(Protocol):
    """Protocol every gate-kind runner implements."""

    kind: GateKind

    def apply(self, *, decision_id: str, proposal: dict[str, Any]) -> GateOutcome:
        """Apply this gate to ``proposal`` and return the outcome."""
        ...


# --- ZERO_TOUCH --------------------------------------------------------------


class ZeroTouchGate:
    """Apply silently; log as auto-taken."""

    kind = GateKind.ZERO_TOUCH

    def apply(self, *, decision_id: str, proposal: dict[str, Any]) -> GateOutcome:
        """Return an ``auto_applied`` outcome without any side effects."""
        _ = decision_id, proposal
        return GateOutcome(
            kind=GateKind.ZERO_TOUCH,
            status="auto_applied",
            occurred_at=GateOutcome.now(),
        )


# --- ACK_ONLY ----------------------------------------------------------------


class AckOnlyGate:
    """Notify + auto-apply; acknowledgement is optional."""

    kind = GateKind.ACK_ONLY

    def __init__(self, *, notifier: Notifier | None = None) -> None:
        """Store the optional notifier used to announce applied proposals."""
        self.notifier = notifier

    def apply(self, *, decision_id: str, proposal: dict[str, Any]) -> GateOutcome:
        """Notify (if a notifier is set) and return an ``acknowledged`` outcome."""
        if self.notifier is not None:
            self.notifier.notify(decision_id=decision_id, proposal=proposal)
        return GateOutcome(
            kind=GateKind.ACK_ONLY,
            status="acknowledged",
            occurred_at=GateOutcome.now(),
        )


class Notifier(Protocol):
    """Sink that announces an auto-applied proposal to its stakeholders."""

    def notify(self, *, decision_id: str, proposal: dict[str, Any]) -> None:
        """Send a notification about ``proposal`` for ``decision_id``."""
        ...


# --- HITL --------------------------------------------------------------------


class HitlGate:
    """Pause; open an approval request and return pending_id for async resume."""

    kind = GateKind.HITL

    def __init__(self, *, approvals: ApprovalsClient, approver_group: str) -> None:
        """Store the approvals client and the group that must approve."""
        self.approvals = approvals
        self.approver_group = approver_group

    def apply(self, *, decision_id: str, proposal: dict[str, Any]) -> GateOutcome:
        """Open an approval request and return a ``pending`` outcome with its id."""
        pid = self.approvals.request(
            decision_id=decision_id,
            approver_group=self.approver_group,
            proposal=proposal,
        )
        return GateOutcome(
            kind=GateKind.HITL,
            status="pending",
            pending_id=pid,
            occurred_at=GateOutcome.now(),
        )


# --- ESCALATION --------------------------------------------------------------


class EscalationGate:
    """Route to a cross-functional owner. In Sprint 11: delegate to approvals."""

    kind = GateKind.ESCALATION

    def __init__(self, *, approvals: ApprovalsClient, escalation_group: str) -> None:
        """Store the approvals client and the escalation owner group."""
        self.approvals = approvals
        self.escalation_group = escalation_group

    def apply(self, *, decision_id: str, proposal: dict[str, Any]) -> GateOutcome:
        """Open an approval flagged ``_escalation`` and return an ``escalated`` outcome."""
        pid = self.approvals.request(
            decision_id=decision_id,
            approver_group=self.escalation_group,
            proposal={**proposal, "_escalation": True},
        )
        return GateOutcome(
            kind=GateKind.ESCALATION,
            status="escalated",
            pending_id=pid,
            occurred_at=GateOutcome.now(),
        )
