"""Sequential orchestration — A → B → C with strict dependency order."""

from __future__ import annotations

from dataclasses import dataclass

from apex_orchestrator.types import StepFn, StepResult


@dataclass(frozen=True, slots=True)
class _Step:
    step_id: str
    agent_name: str
    agent_version: str
    fn: StepFn


class SequentialRunner:
    """Run steps in declaration order; each sees the previous step's result merged in."""

    def __init__(self) -> None:
        self._steps: list[_Step] = []

    def add(self, *, step_id: str, agent_name: str, agent_version: str, fn: StepFn) -> "SequentialRunner":
        self._steps.append(_Step(step_id, agent_name, agent_version, fn))
        return self

    def run(self, initial_context: dict) -> tuple[dict, list[StepResult]]:
        """Execute steps in order. Returns (final_context, step_results)."""
        context = dict(initial_context)
        results: list[StepResult] = []
        for step in self._steps:
            result = step.fn(context)
            results.append(StepResult(
                step_id=step.step_id,
                agent_name=step.agent_name,
                agent_version=step.agent_version,
                result=result,
            ))
            context.setdefault("_history", []).append({"step_id": step.step_id, "result": result})
            context.update(result)
        return context, results

    def __len__(self) -> int:
        return len(self._steps)
