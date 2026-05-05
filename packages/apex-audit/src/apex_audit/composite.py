"""Orchestration composite row (Section 11.5, BL.P.81).

The orchestration emits a *parent* row that references every participating
agent's decision row via the shared ``trace_id``. Auditors walk:

    orchestration row -> participating agent rows ->
    MCP tool calls -> Purview-registered Gold view versions.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ParticipatingAgent(BaseModel):
    """One step in the composite row's ordered agent list."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    decision_id: str = Field(min_length=1)
    agent_id: str = Field(min_length=1)
    step_order: int = Field(ge=0)
    latency_ms: float | None = None


class HitlEvent(BaseModel):
    """One HITL gate fired during the orchestration."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    decision_id: str = Field(min_length=1)
    gate_kind: str = Field(min_length=1)
    status: str = Field(min_length=1)  # pending|approved|rejected|...
    approver_identity: str | None = None


class OrchestrationCompositeRow(BaseModel):
    """Parent row for a whole orchestration run."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    trace_id: str = Field(min_length=1)
    orchestration_id: str = Field(min_length=1)
    archetype_id: str = Field(min_length=1)
    trigger: str = Field(min_length=1)  # event | user_action | schedule
    tenant_id: str = Field(min_length=1)

    participating_agents: tuple[ParticipatingAgent, ...] = ()
    orchestration_outcome: str = Field(min_length=1)
    latency_breakdown: dict[str, float] = Field(default_factory=dict)
    hitl_gates_fired: tuple[HitlEvent, ...] = ()
    policy_exceptions: tuple[str, ...] = ()

    started_at: datetime
    ended_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
