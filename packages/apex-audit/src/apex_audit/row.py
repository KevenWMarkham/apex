"""The 14-field Decision Audit Row (Section 11.2).

Every decision an agent emits produces one of these rows. The runtime
**rejects** emissions missing any required field.

Required fields (14):
    trace_id, decision_id, agent_id, invoking_identity,
    manifest_version, policy_version, model_version, prompt_version,
    inputs_ref, tools_called, reasoning_trace_ref, decision_output,
    hitl_status, downstream_effect_ref

Optional (carried when available): cost_attribution,
sensitivity_label_propagation, confidence_score.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from apex_audit.reasoning import ToolCallRecord


class HitlStatus(StrEnum):
    """Mirrors the six terminal/transient HITL states from Section 11.2."""

    NONE = "none"
    PENDING = "pending"
    APPROVED = "approved"
    MODIFIED = "modified"
    REJECTED = "rejected"
    OVERRIDDEN = "overridden"


class HitlRecord(BaseModel):
    """Approver identity + timestamp bound to a HITL status."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    status: HitlStatus
    approver_identity: str | None = None
    approved_at: datetime | None = None
    rationale: str | None = None


class AuditRow(BaseModel):
    """The 14-field required row, plus commonly carried optional fields.

    The row is immutable once constructed (``frozen=True``). The store appends
    a ``signature`` afterwards via ``with_signature`` - this returns a new
    instance; the original is never mutated.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    # --- 14 required fields ---
    trace_id: str = Field(min_length=1)
    decision_id: str = Field(min_length=1)
    agent_id: str = Field(min_length=1)
    invoking_identity: str = Field(min_length=1)
    manifest_version: str = Field(min_length=1)
    policy_version: str = Field(min_length=1)
    model_version: str = Field(min_length=1)
    prompt_version: str = Field(min_length=1)
    inputs_ref: str = Field(min_length=1)
    tools_called: tuple[ToolCallRecord, ...] = ()
    reasoning_trace_ref: str = Field(min_length=1)
    decision_output: dict[str, Any]
    hitl_status: HitlRecord
    downstream_effect_ref: str | None = None  # required field; null = advisory

    # --- commonly carried optionals ---
    cost_attribution: dict[str, float] | None = None
    sensitivity_label_propagation: tuple[str, ...] = ()
    confidence_score: float | None = None

    # --- seal metadata (set by the store) ---
    sealed_at: datetime | None = None
    signature: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """JSON-ready dict with enums/datetimes serialised to strings."""
        return self.model_dump(mode="json")


def utc_now() -> datetime:
    return datetime.now(UTC)
