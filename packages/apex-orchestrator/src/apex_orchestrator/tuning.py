"""Tenant policy-tuning workflow with 2-week observation + auto-rollback."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from uuid import uuid4

from apex_core.types import GateKind


class TuningStatus(StrEnum):
    """Lifecycle state of a tuning request."""

    PROPOSED = "proposed"
    OBSERVING = "observing"
    APPROVED = "approved"
    ROLLED_BACK = "rolled_back"


OBSERVATION_WINDOW = timedelta(days=14)


@dataclass
class TuningRequest:
    """A tenant-initiated change to a service's default gate mapping."""

    request_id: str
    service: str
    from_gate: GateKind
    to_gate: GateKind
    requested_by: str
    rationale: str
    requested_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    status: TuningStatus = TuningStatus.PROPOSED
    observation_ends_at: datetime | None = None
    reversal_count: int = 0
    escalation_count: int = 0
    final_at: datetime | None = None

    def start_observation(self, *, now: datetime | None = None) -> None:
        """Enter OBSERVING and set the window end to ``now`` (default: current UTC) + 14 days."""
        base = now or datetime.now(UTC)
        self.status = TuningStatus.OBSERVING
        self.observation_ends_at = base + OBSERVATION_WINDOW

    def record_reversal(self) -> None:
        """Count one approver reversal observed during the window."""
        self.reversal_count += 1

    def record_escalation(self) -> None:
        """Count one escalation observed during the window."""
        self.escalation_count += 1

    def evaluate(self, *, now: datetime | None = None) -> TuningStatus:
        """Auto-rollback on any reversal/escalation during observation; approve at window end."""
        current = now or datetime.now(UTC)
        if self.status is TuningStatus.OBSERVING:
            if self.reversal_count > 0 or self.escalation_count > 0:
                self.status = TuningStatus.ROLLED_BACK
                self.final_at = current
            elif self.observation_ends_at is not None and current >= self.observation_ends_at:
                self.status = TuningStatus.APPROVED
                self.final_at = current
        return self.status


class TuningStore:
    """In-memory tuning-request store — auditable via append-only `history`."""

    def __init__(self) -> None:
        """Start with no requests and an empty event history."""
        self._requests: dict[str, TuningRequest] = {}
        self.history: list[dict[str, str]] = []

    def propose(
        self,
        *,
        service: str,
        from_gate: GateKind,
        to_gate: GateKind,
        requested_by: str,
        rationale: str,
    ) -> TuningRequest:
        """Create a PROPOSED request with a fresh id, store it and log ``proposed``."""
        req = TuningRequest(
            request_id=str(uuid4()),
            service=service,
            from_gate=from_gate,
            to_gate=to_gate,
            requested_by=requested_by,
            rationale=rationale,
        )
        self._requests[req.request_id] = req
        self.history.append({"event": "proposed", "request_id": req.request_id})
        return req

    def start_observation(self, request_id: str) -> TuningRequest:
        """Begin the observation window for a stored request and log it."""
        req = self._requests[request_id]
        req.start_observation()
        self.history.append({"event": "observation_started", "request_id": request_id})
        return req

    def record_reversal(self, request_id: str) -> TuningRequest:
        """Record a reversal against a stored request and log it."""
        req = self._requests[request_id]
        req.record_reversal()
        self.history.append({"event": "reversal_recorded", "request_id": request_id})
        return req

    def evaluate(self, request_id: str, *, now: datetime | None = None) -> TuningRequest:
        """Re-evaluate a stored request, logging a ``status_change`` event if it moved."""
        req = self._requests[request_id]
        old_status = req.status
        new_status = req.evaluate(now=now)
        if new_status != old_status:
            self.history.append(
                {
                    "event": f"status_change:{old_status.value}_to_{new_status.value}",
                    "request_id": request_id,
                }
            )
        return req

    def get(self, request_id: str) -> TuningRequest:
        """Return the stored request; raises KeyError if unknown."""
        return self._requests[request_id]
