"""Hierarchical orchestration — an orchestrator plans, dispatches to specialists."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from apex_orchestrator.types import StepFn, StepResult

Planner = Callable[[dict], list[str]]
"""Planner inspects context and returns the specialist step_ids to dispatch."""


@dataclass(frozen=True, slots=True)
class _Specialist:
    step_id: str
    agent_name: str
    agent_version: str
    fn: StepFn


class HierarchicalRunner:
    """An orchestrator callable decides which specialists to invoke per-context."""

    def __init__(
        self,
        *,
        planner: Planner,
        planner_step_id: str = "plan",
        planner_agent_name: str = "orchestrator",
        planner_agent_version: str = "1.0.0",
    ) -> None:
        self._planner = planner
        self._planner_step_id = planner_step_id
        self._planner_agent_name = planner_agent_name
        self._planner_agent_version = planner_agent_version
        self._specialists: dict[str, _Specialist] = {}

    def register_specialist(
        self,
        *,
        step_id: str,
        agent_name: str,
        agent_version: str,
        fn: StepFn,
    ) -> "HierarchicalRunner":
        self._specialists[step_id] = _Specialist(step_id, agent_name, agent_version, fn)
        return self

    def run(self, initial_context: dict) -> tuple[dict, list[StepResult]]:
        """Plan → dispatch selected specialists sequentially → merge."""
        context = dict(initial_context)
        selected = self._planner(context)

        plan_result = {"planned_specialists": list(selected)}
        results: list[StepResult] = [
            StepResult(
                step_id=self._planner_step_id,
                agent_name=self._planner_agent_name,
                agent_version=self._planner_agent_version,
                result=plan_result,
            )
        ]
        context.update(plan_result)

        for sid in selected:
            if sid not in self._specialists:
                raise KeyError(f"Planner selected unknown specialist {sid!r}")
            spec = self._specialists[sid]
            spec_result = spec.fn(context)
            results.append(StepResult(
                step_id=spec.step_id,
                agent_name=spec.agent_name,
                agent_version=spec.agent_version,
                result=spec_result,
            ))
            context.update(spec_result)
        return context, results
