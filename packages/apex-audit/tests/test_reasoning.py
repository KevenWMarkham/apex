"""Reasoning-trace capture + DLP scrub (BL.P.80)."""

from __future__ import annotations

from apex_audit import (
    StructuredReasoning,
    ToolCallRecord,
    dlp_scrub,
    scrub_structured,
)


class TestDlpScrub:
    def test_redacts_ssn(self) -> None:
        out = dlp_scrub("patient SSN 123-45-6789 on file")
        assert "[SSN]" in out
        assert "123-45-6789" not in out

    def test_redacts_email(self) -> None:
        out = dlp_scrub("contact qa@example.com")
        assert "[EMAIL]" in out
        assert "qa@example.com" not in out

    def test_redacts_credit_card(self) -> None:
        out = dlp_scrub("card 4111 1111 1111 1111 used")
        assert "[CC]" in out

    def test_extra_tokens_redacted(self) -> None:
        out = dlp_scrub(
            "patient Jane Doe was treated",
            extra_tokens=frozenset({"Jane Doe"}),
        )
        assert "Jane Doe" not in out
        assert "[REDACTED]" in out

    def test_safe_text_preserved(self) -> None:
        text = "salvage 71% within safety window"
        assert dlp_scrub(text) == text


class TestScrubStructured:
    def test_scrub_preserves_tool_call_sequence(self) -> None:
        r = StructuredReasoning(
            tool_call_sequence=(
                ToolCallRecord(
                    mcp_tool_id="fabric-mcp.query",
                    tool_version="1.0.0",
                    parameters_hash="sha256:aaa",
                    result_hash="sha256:bbb",
                ),
            ),
            decision_justification="email alice@co.com approved",
            cited_evidence_refs=("ref-1",),
        )
        scrubbed = scrub_structured(r)
        assert scrubbed.tool_call_sequence == r.tool_call_sequence
        assert scrubbed.cited_evidence_refs == r.cited_evidence_refs
        assert "alice@co.com" not in scrubbed.decision_justification
        assert "[EMAIL]" in scrubbed.decision_justification

    def test_original_not_mutated(self) -> None:
        r = StructuredReasoning(decision_justification="SSN 111-22-3333")
        scrub_structured(r)
        assert "111-22-3333" in r.decision_justification  # original intact
