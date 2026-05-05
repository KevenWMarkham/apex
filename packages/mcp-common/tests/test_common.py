"""Tests for mcp-common."""

from __future__ import annotations

from apex_core.types import Classification, Practice
from mcp_common import (
    AgentIdentity,
    McpError,
    McpErrorCode,
    ScopeContext,
    SloSpec,
    ToolContract,
    compute_hash,
    emit_trace,
    require_agent_identity,
    scope_allows,
    traced_call,
)
from mcp_common.trace import set_trace_sink


class TestContract:
    def test_contract_is_frozen(self) -> None:
        from pydantic import ValidationError
        c = ToolContract(name="x.y", description="d")
        with __import__("pytest").raises(ValidationError):
            c.name = "other"  # type: ignore[misc]

    def test_slo_bounds(self) -> None:
        slo = SloSpec(latency_ms_p95=500, availability_pct=99.9)
        assert slo.availability_pct == 99.9


class TestScope:
    def _ctx(self, **overrides: object) -> ScopeContext:
        base: dict[str, object] = {
            "tenant_id": "t1",
            "practice": Practice.RC,
            "persona": "store-ops-lead",
            "classification_visibility": frozenset({Classification.INTERNAL}),
        }
        base.update(overrides)
        return ScopeContext(**base)  # type: ignore[arg-type]

    def test_scope_match(self) -> None:
        assert scope_allows(self._ctx(), required_scopes=["practice:rc"])

    def test_scope_mismatch(self) -> None:
        assert not scope_allows(self._ctx(), required_scopes=["practice:hls"])

    def test_classification_denied(self) -> None:
        assert not scope_allows(
            self._ctx(),
            required_scopes=[],
            data_classifications=[Classification.PHI],
        )

    def test_classification_allowed(self) -> None:
        ctx = self._ctx(
            classification_visibility=frozenset(
                {Classification.INTERNAL, Classification.PHI},
            )
        )
        assert scope_allows(
            ctx, required_scopes=[], data_classifications=[Classification.PHI],
        )

    def test_unknown_dimension_fails_closed(self) -> None:
        assert not scope_allows(self._ctx(), required_scopes=["mystery:something"])


class TestAuth:
    def test_require_rejects_none(self) -> None:
        import pytest
        with pytest.raises(McpError) as exc:
            require_agent_identity(None)
        assert exc.value.code is McpErrorCode.UNAUTHENTICATED

    def test_require_passes_identity(self) -> None:
        ident = AgentIdentity(agent_id="a", tenant_id="t")
        assert require_agent_identity(ident) is ident


class TestTrace:
    def test_hash_stable(self) -> None:
        a = compute_hash({"a": 1, "b": 2})
        b = compute_hash({"b": 2, "a": 1})  # different order
        assert a == b  # sort_keys normalises

    def test_traced_call_emits(self) -> None:
        captured: list = []
        set_trace_sink(captured.append)
        with traced_call(tool_name="x.y", parameters={"k": 1}) as ctx:
            ctx["result"] = {"ok": True}
        assert len(captured) == 1
        rec = captured[0]
        assert rec.tool_name == "x.y"
        assert rec.error_class is None
        assert rec.latency_ms >= 1

    def test_traced_call_captures_exception_class(self) -> None:
        import pytest
        captured: list = []
        set_trace_sink(captured.append)
        with pytest.raises(ValueError):
            with traced_call(tool_name="x.fail"):
                raise ValueError("boom")
        assert captured[0].error_class == "ValueError"


class TestErrors:
    def test_error_has_code(self) -> None:
        err = McpError(code=McpErrorCode.NOT_FOUND, message="missing")
        assert err.code is McpErrorCode.NOT_FOUND
        assert "not_found" in str(err)
