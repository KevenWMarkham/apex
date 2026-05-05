"""Tests for the four orchestration primitives."""

from __future__ import annotations

import pytest

from apex_orchestrator import (
    FeedbackLoopRunner,
    HierarchicalRunner,
    ParallelRunner,
    SequentialRunner,
)


class TestSequential:
    def test_order_preserved(self) -> None:
        runner = SequentialRunner()
        runner.add(step_id="a", agent_name="A", agent_version="1", fn=lambda c: {"x": 1})
        runner.add(step_id="b", agent_name="B", agent_version="1", fn=lambda c: {"y": c["x"] + 1})
        ctx, results = runner.run({})
        assert ctx["x"] == 1
        assert ctx["y"] == 2
        assert [r.step_id for r in results] == ["a", "b"]


class TestParallel:
    def test_merges_results(self) -> None:
        runner = ParallelRunner()
        runner.add(step_id="a", agent_name="A", agent_version="1", fn=lambda c: {"a": 1})
        runner.add(step_id="b", agent_name="B", agent_version="1", fn=lambda c: {"b": 2})
        runner.add(step_id="c", agent_name="C", agent_version="1", fn=lambda c: {"c": 3})
        ctx, results = runner.run({})
        assert ctx["a"] == 1 and ctx["b"] == 2 and ctx["c"] == 3
        assert [r.step_id for r in results] == ["a", "b", "c"]  # declaration order


class TestHierarchical:
    def test_planner_drives_specialists(self) -> None:
        runner = HierarchicalRunner(
            planner=lambda c: ["spec_a"] if c.get("mode") == "a" else ["spec_b"],
        )
        runner.register_specialist(
            step_id="spec_a", agent_name="SA", agent_version="1",
            fn=lambda c: {"picked": "a"},
        )
        runner.register_specialist(
            step_id="spec_b", agent_name="SB", agent_version="1",
            fn=lambda c: {"picked": "b"},
        )
        ctx, results = runner.run({"mode": "a"})
        assert ctx["picked"] == "a"
        step_ids = [r.step_id for r in results]
        assert step_ids[0] == "plan"
        assert step_ids[1] == "spec_a"

    def test_unknown_specialist_raises(self) -> None:
        runner = HierarchicalRunner(planner=lambda c: ["missing"])
        with pytest.raises(KeyError):
            runner.run({})


class TestFeedbackLoop:
    def test_accepts_first_iteration(self) -> None:
        runner = FeedbackLoopRunner(
            producer=lambda c: {"score": 0.95},
            evaluator=lambda r, c: r["score"] >= 0.9,
        )
        ctx, results = runner.run({})
        assert len(results) == 1
        assert ctx["_feedback_iterations"] == 1

    def test_loops_until_accept(self) -> None:
        attempts = iter([{"score": 0.3}, {"score": 0.6}, {"score": 0.95}])
        runner = FeedbackLoopRunner(
            producer=lambda c: next(attempts),
            evaluator=lambda r, c: r["score"] >= 0.9,
        )
        ctx, results = runner.run({})
        assert len(results) == 3
        assert ctx["_feedback_iterations"] == 3

    def test_respects_max_iterations(self) -> None:
        runner = FeedbackLoopRunner(
            producer=lambda c: {"score": 0.0},
            evaluator=lambda r, c: False,
            max_iterations=2,
        )
        ctx, results = runner.run({})
        assert len(results) == 2
        assert ctx["_feedback_iterations"] == 2

    def test_rejects_zero_iterations(self) -> None:
        with pytest.raises(ValueError):
            FeedbackLoopRunner(
                producer=lambda c: {}, evaluator=lambda r, c: True, max_iterations=0,
            )
