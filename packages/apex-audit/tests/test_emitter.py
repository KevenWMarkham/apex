"""End-to-end emission pipeline (BL.P.77 + P.78 + P.79 + P.80 + P.82 + P.84)."""

from __future__ import annotations

import pytest

from apex_audit import (
    AuditEmitter,
    AuditStore,
    ContentAddressedStore,
    HitlRecord,
    HitlStatus,
    StaticVersionResolver,
    StructuredReasoning,
    TraceMissingError,
    VersionStamps,
    new_trace_id,
)


def _make_emitter() -> AuditEmitter:
    return AuditEmitter(
        version_resolver=StaticVersionResolver(
            VersionStamps(
                manifest_version="m-sha", policy_version="p-sha",
                prompt_version="pr-sha", model_version="gpt-4.1-2025-01",
            ),
        ),
        content_store=ContentAddressedStore(),
        audit_store=AuditStore(signing_key=b"apex-test-key"),
    )


class TestEmitter:
    def test_full_pipeline_produces_14_field_row(self) -> None:
        emitter = _make_emitter()
        trace_id = new_trace_id()

        sealed = emitter.emit(
            trace_id=trace_id,
            agent_id="agent:rc.dispose",
            invoking_identity="user:qa@ex.com",
            orchestration_name="rc.cold_chain_response",
            tenant_id="tenant-a",
            inputs={"temp_f": 52.0, "duration_min": 240},
            tool_calls=[
                {
                    "mcp_tool_id": "fabric-mcp.query",
                    "tool_version": "1.0.0",
                    "parameters": {"table": "bronze.iot"},
                    "result": {"row_count": 1},
                },
            ],
            structured_reasoning=StructuredReasoning(
                decision_justification="within salvage window",
                cited_evidence_refs=("ref-1",),
                confidence_score=0.88,
            ),
            raw_reasoning="free-form CoT with SSN 111-22-3333",
            decision_output={"action": "salvage", "units": 412},
            hitl=HitlRecord(status=HitlStatus.APPROVED,
                            approver_identity="qa@ex.com"),
            downstream_effect_ref="action:markdown-run-7",
            sensitivity_labels=("Confidential",),
            confidence_score=0.88,
        )
        assert sealed["trace_id"] == trace_id
        assert sealed["manifest_version"] == "m-sha"
        assert sealed["policy_version"] == "p-sha"
        assert sealed["prompt_version"] == "pr-sha"
        assert sealed["model_version"] == "gpt-4.1-2025-01"
        assert sealed["inputs_ref"].startswith("sha256:")
        assert sealed["reasoning_trace_ref"].startswith("sha256:")
        assert sealed["signature"]

    def test_trace_missing_rejected(self) -> None:
        emitter = _make_emitter()
        with pytest.raises(TraceMissingError):
            emitter.emit(
                trace_id="", agent_id="a", invoking_identity="u",
                orchestration_name="x", tenant_id="t",
                inputs={}, decision_output={"ok": True},
            )

    def test_raw_trace_lands_in_restricted_store_not_main_row(self) -> None:
        emitter = _make_emitter()
        trace_id = new_trace_id()
        sealed = emitter.emit(
            trace_id=trace_id,
            agent_id="a", invoking_identity="u",
            orchestration_name="x", tenant_id="t",
            inputs={"v": 1},
            raw_reasoning="raw CoT with SSN 123-45-6789",
            decision_output={"ok": True},
        )
        did = sealed["decision_id"]
        # Raw trace is NOT retrievable via the content_store (main ledger path)
        structured = emitter.content_store.get(sealed["reasoning_trace_ref"])
        assert "123-45-6789" not in repr(structured)
        # But IS in the restricted store
        assert did in emitter.restricted_store
        assert emitter.restricted_store.get(did).startswith("raw CoT")

    def test_resolve_decision_returns_three_shas_and_inputs(self) -> None:
        emitter = _make_emitter()
        trace_id = new_trace_id()
        sealed = emitter.emit(
            trace_id=trace_id, agent_id="a", invoking_identity="u",
            orchestration_name="x", tenant_id="t",
            inputs={"k": "v"}, decision_output={"ok": True},
        )
        resolved = emitter.resolve_decision(sealed["decision_id"])
        assert resolved["manifest_version"] == "m-sha"
        assert resolved["policy_version"] == "p-sha"
        assert resolved["prompt_version"] == "pr-sha"
        assert resolved["inputs"] == {"k": "v"}

    def test_dlp_scrubs_justification_before_hashing(self) -> None:
        emitter = _make_emitter()
        trace_id = new_trace_id()
        sealed = emitter.emit(
            trace_id=trace_id, agent_id="a", invoking_identity="u",
            orchestration_name="x", tenant_id="t",
            inputs={"k": "v"},
            structured_reasoning=StructuredReasoning(
                decision_justification="contact alice@co.com",
            ),
            decision_output={"ok": True},
            sensitivity_labels=("PII",),
        )
        stored_reasoning = emitter.content_store.get(sealed["reasoning_trace_ref"])
        assert "alice@co.com" not in stored_reasoning["decision_justification"]
        assert "[EMAIL]" in stored_reasoning["decision_justification"]

    def test_tool_calls_content_addressed(self) -> None:
        emitter = _make_emitter()
        trace_id = new_trace_id()
        sealed = emitter.emit(
            trace_id=trace_id, agent_id="a", invoking_identity="u",
            orchestration_name="x", tenant_id="t",
            inputs={},
            tool_calls=[
                {
                    "mcp_tool_id": "fabric-mcp.q",
                    "tool_version": "1",
                    "parameters": {"x": 1},
                    "result": {"row_count": 5},
                },
            ],
            decision_output={"ok": True},
        )
        tools = sealed["tools_called"]
        assert len(tools) == 1
        assert tools[0]["parameters_hash"].startswith("sha256:")
        # Round-trip: the content store holds the params + result.
        assert emitter.content_store.get(tools[0]["parameters_hash"]) == {"x": 1}
