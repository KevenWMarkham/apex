"""Parallel orchestration — dispatch fans to independent steps; outputs merge."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from typing import Any

from apex_orchestrator.types import StepFn, StepResult


@dataclass(frozen=True, slots=True)
class _Step:
    step_id: str
    agent_name: str
    agent_version: str
    fn: StepFn


class ParallelRunner:
    """Run steps concurrently; merge their results into a single output context."""

    def __init__(self, *, max_workers: int | None = None) -> None:
        """Start with no steps; ``max_workers`` caps the pool (default: one per step)."""
        self._steps: list[_Step] = []
        self._max_workers = max_workers

    def add(
        self, *, step_id: str, agent_name: str, agent_version: str, fn: StepFn
    ) -> ParallelRunner:
        """Append a step to run concurrently; returns self for chaining."""
        self._steps.append(_Step(step_id, agent_name, agent_version, fn))
        return self

    def run(self, initial_context: dict[str, Any]) -> tuple[dict[str, Any], list[StepResult]]:
        """Execute all steps in a thread pool; merge results by key (last-writer-wins)."""
        context = dict(initial_context)
        results: list[StepResult] = []
        if not self._steps:
            return context, results

        with ThreadPoolExecutor(max_workers=self._max_workers or len(self._steps)) as pool:
            futures = {pool.submit(s.fn, context): s for s in self._steps}
            for fut, step in futures.items():
                result = fut.result()
                results.append(
                    StepResult(
                        step_id=step.step_id,
                        agent_name=step.agent_name,
                        agent_version=step.agent_version,
                        result=result,
                    )
                )
                context.update(result)

        # Keep results in declaration order for determinism
        results.sort(key=lambda r: [s.step_id for s in self._steps].index(r.step_id))
        return context, results

    def __len__(self) -> int:
        """Return the number of registered steps."""
        return len(self._steps)
