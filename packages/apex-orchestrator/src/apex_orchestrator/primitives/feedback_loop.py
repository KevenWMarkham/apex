"""Feedback-loop orchestration — agent produces output; evaluator accepts or refines."""

from __future__ import annotations

from typing import Callable

from apex_orchestrator.types import StepFn, StepResult

Evaluator = Callable[[dict, dict], bool]
"""Given (current_result, context), return True if acceptable."""


class FeedbackLoopRunner:
    """Run ``producer`` then ``evaluator``; loop until accept or max_iterations."""

    def __init__(
        self,
        *,
        producer: StepFn,
        evaluator: Evaluator,
        producer_step_id: str = "produce",
        producer_agent_name: str = "producer",
        producer_agent_version: str = "1.0.0",
        max_iterations: int = 3,
    ) -> None:
        if max_iterations < 1:
            raise ValueError("max_iterations must be >= 1")
        self._producer = producer
        self._evaluator = evaluator
        self._producer_step_id = producer_step_id
        self._producer_agent_name = producer_agent_name
        self._producer_agent_version = producer_agent_version
        self._max_iterations = max_iterations

    def run(self, initial_context: dict) -> tuple[dict, list[StepResult]]:
        """Run the loop. Returns final context + per-iteration step results."""
        context = dict(initial_context)
        results: list[StepResult] = []
        for iteration in range(1, self._max_iterations + 1):
            result = self._producer(context)
            results.append(StepResult(
                step_id=f"{self._producer_step_id}_{iteration}",
                agent_name=self._producer_agent_name,
                agent_version=self._producer_agent_version,
                result=result,
            ))
            if self._evaluator(result, context):
                context["_feedback_iterations"] = iteration
                context.update(result)
                return context, results
            context.update(result)
            context["_feedback_iterations"] = iteration
        return context, results
