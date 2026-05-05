"""Tests for the manifest loader + pausable runtime."""

from __future__ import annotations

import pytest

from apex_core.types import BumpClass
from apex_orchestrator import (
    InMemoryApprovalsClient,
    OrchestrationStatus,
    Orchestrator,
    load_manifest_with_stamps,
)
from apex_orchestrator.manifest import MissingVersionStampsError


def _valid_manifest() -> dict:
    return {
        "name": "test-orch",
        "stamps": {
            "manifest_version": "sha1",
            "policy_version": "sha2",
            "prompt_version": "sha3",
        },
    }


class TestManifestLoader:
    def test_valid(self) -> None:
        m = load_manifest_with_stamps(_valid_manifest())
        assert m.manifest_version == "sha1"
        assert m.prompt_version == "sha3"

    def test_missing_name(self) -> None:
        with pytest.raises(MissingVersionStampsError):
            load_manifest_with_stamps({"stamps": _valid_manifest()["stamps"]})

    def test_missing_stamps(self) -> None:
        with pytest.raises(MissingVersionStampsError):
            load_manifest_with_stamps({"name": "x"})

    def test_missing_one_stamp(self) -> None:
        payload = _valid_manifest()
        del payload["stamps"]["policy_version"]
        with pytest.raises(MissingVersionStampsError):
            load_manifest_with_stamps(payload)

    def test_empty_stamp_rejected(self) -> None:
        payload = _valid_manifest()
        payload["stamps"]["policy_version"] = ""
        with pytest.raises(MissingVersionStampsError):
            load_manifest_with_stamps(payload)


class TestRuntime:
    def _orch(self, approvals: InMemoryApprovalsClient | None = None) -> Orchestrator:
        manifest = load_manifest_with_stamps(_valid_manifest())
        return Orchestrator(manifest, approvals=approvals)

    def test_completes_all_zero_touch(self) -> None:
        orch = self._orch()
        orch.add_step(
            step_id="a", agent_name="A", agent_version="1",
            fn=lambda c: {"v": 1}, bump_class=BumpClass.PATCH,
        )
        orch.add_step(
            step_id="b", agent_name="B", agent_version="1",
            fn=lambda c: {"w": 2}, bump_class=BumpClass.PATCH,
        )
        result = orch.run({})
        assert result.status is OrchestrationStatus.COMPLETED
        assert result.context["v"] == 1 and result.context["w"] == 2
        assert all(g.status == "auto_applied" for g in result.gate_outcomes)

    def test_pauses_on_hitl(self) -> None:
        approvals = InMemoryApprovalsClient()
        orch = self._orch(approvals)
        orch.add_step(
            step_id="a", agent_name="A", agent_version="1",
            fn=lambda c: {"pre": True}, bump_class=BumpClass.PATCH,
        )
        orch.add_step(
            step_id="hitl", agent_name="H", agent_version="1",
            fn=lambda c: {"proposal": "dispose"}, bump_class=BumpClass.MAJOR,
            approver_group="qa",
        )
        orch.add_step(
            step_id="post", agent_name="P", agent_version="1",
            fn=lambda c: {"post": True}, bump_class=BumpClass.PATCH,
        )
        result = orch.run({})
        assert result.status is OrchestrationStatus.PAUSED
        assert len(result.pending_approvals) == 1
        assert "post" not in result.context

    def test_resume_approves_continues(self) -> None:
        approvals = InMemoryApprovalsClient()
        orch = self._orch(approvals)
        orch.add_step(
            step_id="hitl", agent_name="H", agent_version="1",
            fn=lambda c: {"proposal": "x"}, bump_class=BumpClass.MAJOR,
            approver_group="qa",
        )
        orch.add_step(
            step_id="after", agent_name="A", agent_version="1",
            fn=lambda c: {"after": True}, bump_class=BumpClass.PATCH,
        )
        paused = orch.run({})
        pid = paused.pending_approvals[0]
        final = orch.resume(pid, decision="approved", approver_id="alice", rationale="ok")
        assert final.status is OrchestrationStatus.COMPLETED
        assert final.context["after"] is True

    def test_resume_rejected(self) -> None:
        approvals = InMemoryApprovalsClient()
        orch = self._orch(approvals)
        orch.add_step(
            step_id="hitl", agent_name="H", agent_version="1",
            fn=lambda c: {"proposal": "x"}, bump_class=BumpClass.MAJOR,
            approver_group="qa",
        )
        paused = orch.run({})
        pid = paused.pending_approvals[0]
        final = orch.resume(pid, decision="rejected", approver_id="bob", rationale="unsafe")
        assert final.status is OrchestrationStatus.REJECTED
        assert final.rejection_reason == "unsafe"

    def test_step_exception_returns_failed(self) -> None:
        orch = self._orch()
        def boom(_ctx: dict) -> dict:
            raise RuntimeError("boom")
        orch.add_step(
            step_id="x", agent_name="X", agent_version="1",
            fn=boom, bump_class=BumpClass.PATCH,
        )
        result = orch.run({})
        assert result.status is OrchestrationStatus.FAILED
        assert "RuntimeError" in (result.rejection_reason or "")
