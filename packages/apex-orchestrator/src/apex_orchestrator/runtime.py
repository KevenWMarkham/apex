"""Pausable orchestration runtime.

Executes steps with gates; pauses on HITL/ESCALATION; `resume()` continues
once an approver decides.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from apex_core.types import BumpClass, GateKind

from apex_orchestrator.gates.approvals import ApprovalsClient
from apex_orchestrator.gates.kinds import GateOutcome
from apex_orchestrator.gates.resolver import (
    GateResolution,
    resolve_gate_kind,
    resolve_gate_runner,
)
from apex_orchestrator.manifest import StampedManifest
from apex_orchestrator.types import StepFn, StepResult


class OrchestrationStatus(StrEnum):
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    REJECTED = "rejected"
    FAILED = "failed"


@dataclass
class OrchestrationResult:
    status: OrchestrationStatus
    context: dict[str, Any] = field(default_factory=dict)
    steps: list[StepResult] = field(default_factory=list)
    gate_outcomes: list[GateOutcome] = field(default_factory=list)
    pending_approvals: list[str] = field(default_factory=list)
    rejection_reason: str | None = None


@dataclass
class _OrchestrationStep:
    step_id: str
    agent_name: str
    agent_version: str
    fn: StepFn
    bump_class: BumpClass | None = None
    approver_group: str | None = None


class Orchestrator:
    """Pausable sequential orchestrator with per-step gates.

    Parallel / Hierarchical / Feedback composition is expressed by wrapping
    the primitive runners inside a step's ``fn``.
    """

    def __init__(
        self,
        manifest: StampedManifest,
        *,
        approvals: ApprovalsClient | None = None,
        tenant_gate_override: dict[BumpClass, GateKind] | None = None,
    ) -> None:
        self.manifest = manifest
        self.approvals = approvals
        self.tenant_gate_override = tenant_gate_override or {}
        self._steps: list[_OrchestrationStep] = []
        self._pending_pid_to_step_idx: dict[str, int] = {}
        self._state: dict[str, Any] = {"context": {}, "step_idx": 0, "results": [], "gate_outcomes": []}

    def add_step(
        self,
        *,
        step_id: str,
        agent_name: str,
        agent_version: str,
        fn: StepFn,
        bump_class: BumpClass | None = None,
        approver_group: str | None = None,
    ) -> "Orchestrator":
        self._steps.append(_OrchestrationStep(
            step_id=step_id, agent_name=agent_name, agent_version=agent_version,
            fn=fn, bump_class=bump_class, approver_group=approver_group,
        ))
        return self

    def run(self, initial_context: dict[str, Any]) -> OrchestrationResult:
        """Execute until completion or until a HITL/ESCALATION gate pauses us."""
        self._state = {
            "context": dict(initial_context),
            "step_idx": 0,
            "results": [],
            "gate_outcomes": [],
        }
        return self._advance()

    def resume(self, pending_id: str, decision: str, approver_id: str, rationale: str = "") -> OrchestrationResult:
        """Continue after an approver decides on a pending HITL/ESCALATION gate."""
        if self.approvals is None:
            raise RuntimeError("resume() requires an approvals client.")
        if pending_id not in self._pending_pid_to_step_idx:
            raise KeyError(f"Unknown pending_id {pending_id!r}")
        self.approvals.finalise(
            pending_id=pending_id,
            decision=decision,
            approver_id=approver_id,
            rationale=rationale,
        )
        if decision == "rejected":
            return OrchestrationResult(
                status=OrchestrationStatus.REJECTED,
                context=dict(self._state["context"]),
                steps=list(self._state["results"]),
                gate_outcomes=list(self._state["gate_outcomes"]),
                rejection_reason=rationale or "rejected by approver",
            )
        # 'approved' / 'modified' — advance past the pending step.
        del self._pending_pid_to_step_idx[pending_id]
        self._state["step_idx"] += 1
        return self._advance()

    # --- internals ----------------------------------------------------------

    def _advance(self) -> OrchestrationResult:
        while self._state["step_idx"] < len(self._steps):
            idx = self._state["step_idx"]
            step = self._steps[idx]
            try:
                step_result = step.fn(self._state["context"])
            except Exception as exc:  # noqa: BLE001
                return OrchestrationResult(
                    status=OrchestrationStatus.FAILED,
                    context=dict(self._state["context"]),
                    steps=list(self._state["results"]),
                    gate_outcomes=list(self._state["gate_outcomes"]),
                    rejection_reason=f"step {step.step_id!r} failed: {type(exc).__name__}: {exc}",
                )
            self._state["results"].append(StepResult(
                step_id=step.step_id,
                agent_name=step.agent_name,
                agent_version=step.agent_version,
                result=step_result,
            ))
            self._state["context"].update(step_result)

            if step.bump_class is not None:
                outcome = self._run_gate(step, step_result)
                self._state["gate_outcomes"].append(outcome)
                if outcome.status in {"pending", "escalated"}:
                    self._pending_pid_to_step_idx[outcome.pending_id] = idx
                    return OrchestrationResult(
                        status=OrchestrationStatus.PAUSED,
                        context=dict(self._state["context"]),
                        steps=list(self._state["results"]),
                        gate_outcomes=list(self._state["gate_outcomes"]),
                        pending_approvals=[outcome.pending_id],
                    )

            self._state["step_idx"] += 1

        return OrchestrationResult(
            status=OrchestrationStatus.COMPLETED,
            context=dict(self._state["context"]),
            steps=list(self._state["results"]),
            gate_outcomes=list(self._state["gate_outcomes"]),
        )

    def _run_gate(self, step: _OrchestrationStep, proposal: dict[str, Any]) -> GateOutcome:
        resolution: GateResolution = resolve_gate_kind(
            bump_class=step.bump_class,  # type: ignore[arg-type]
            tenant_override=self.tenant_gate_override.get(step.bump_class),
        )
        runner = resolve_gate_runner(
            resolution,
            approvals=self.approvals,
            approver_group=step.approver_group or "default-approver",
            escalation_group=step.approver_group or "default-escalation",
        )
        decision_id = f"{self.manifest.name}:{step.step_id}"
        return runner.apply(decision_id=decision_id, proposal=proposal)
