"""Trace-ID discipline + three-version rule (BL.P.78, BL.P.79)."""

from __future__ import annotations

import pytest

from apex_audit import (
    StaticVersionResolver,
    TraceContext,
    TraceMissingError,
    VersionStamps,
    new_decision_id,
    new_trace_id,
    require_trace_id,
    stamp_versions,
)


class TestTrace:
    def test_new_trace_id_is_uuid_string(self) -> None:
        tid = new_trace_id()
        assert isinstance(tid, str)
        # UUID-4 canonical form has 4 hyphens
        assert tid.count("-") == 4

    def test_require_trace_id_rejects_empty(self) -> None:
        with pytest.raises(TraceMissingError):
            require_trace_id("")
        with pytest.raises(TraceMissingError):
            require_trace_id(None)

    def test_child_decision_inherits_trace_id(self) -> None:
        ctx = TraceContext.start()
        tid1, did1 = ctx.child_decision()
        tid2, did2 = ctx.child_decision()
        assert tid1 == tid2 == ctx.trace_id
        assert did1 != did2

    def test_new_decision_id_unique(self) -> None:
        ids = {new_decision_id() for _ in range(100)}
        assert len(ids) == 100


class TestVersions:
    def _stamps(self) -> VersionStamps:
        return VersionStamps(
            manifest_version="m-sha",
            policy_version="p-sha",
            prompt_version="pr-sha",
            model_version="gpt-4.1-2025-01",
        )

    def test_version_stamps_are_frozen(self) -> None:
        s = self._stamps()
        with pytest.raises(Exception):  # pydantic ValidationError / FrozenInstanceError
            s.manifest_version = "x"  # type: ignore[misc]

    def test_stamp_versions_returns_resolver_output(self) -> None:
        resolver = StaticVersionResolver(self._stamps())
        out = stamp_versions(
            resolver, orchestration_name="cold-chain", tenant_id="t1"
        )
        assert out.manifest_version == "m-sha"
        assert out.model_version == "gpt-4.1-2025-01"

    def test_empty_sha_rejected(self) -> None:
        with pytest.raises(Exception):
            VersionStamps(
                manifest_version="", policy_version="p",
                prompt_version="pr", model_version="m",
            )
