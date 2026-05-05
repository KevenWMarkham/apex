"""Reasoning-trace capture with DLP scrub (Section 11.4, BL.P.80).

Design stance (from APEX_Design.md Section 11.4):

- Structured reasoning (tool-call sequence, decision justification,
  cited-evidence pointers, confidence) goes into the main audit row's
  ``reasoning_trace_ref``.
- Raw chain-of-thought may contain PHI / PCI / trade secrets / hallucinations;
  it lands in a **restricted** store with stricter access (incident
  investigation only). APEX never inlines it into the main ledger.
- DLP scrub removes any sensitive tokens that slipped into justifications,
  driven by the sensitivity labels propagated onto the decision's inputs.
"""

from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ToolCallRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    mcp_tool_id: str
    tool_version: str
    parameters_hash: str
    result_hash: str


class StructuredReasoning(BaseModel):
    """What lands in the main audit row (redacted, structured)."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    tool_call_sequence: tuple[ToolCallRecord, ...] = ()
    decision_justification: str = ""
    cited_evidence_refs: tuple[str, ...] = ()
    confidence_score: float | None = None


class ReasoningCapture(BaseModel):
    """Bundle produced at reasoning-capture time.

    ``structured`` is safe for the main ledger; ``raw_trace`` goes to the
    restricted store (separate access scope). The caller is responsible for
    routing each to the right store.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    structured: StructuredReasoning
    raw_trace: str = Field(default="")


_DLP_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    # Common PII / PCI / PHI shapes. Deliberately conservative.
    ("[SSN]", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("[CC]", re.compile(r"\b(?:\d[ -]*?){13,19}\b")),
    ("[EMAIL]", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")),
    ("[PHONE]", re.compile(r"\b\+?\d{1,2}?[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{4}\b")),
)


def dlp_scrub(
    text: str,
    *,
    propagated_labels: frozenset[str] = frozenset(),
    extra_tokens: frozenset[str] = frozenset(),
) -> str:
    """Remove sensitive fragments from free-text reasoning.

    Applies pattern-based redaction (SSN/CC/email/phone) unconditionally, then
    also redacts any ``extra_tokens`` the caller provides (e.g. literal values
    pulled from fields labelled PHI/PII/PCI that the caller already knows).

    ``propagated_labels`` is accepted for API shape but not currently consulted
    by the pattern set - it flows through so label-aware scrubbers can plug in
    later without changing the emitter signature.
    """
    del propagated_labels  # reserved for label-driven scrubbers
    out = text
    for replacement, pattern in _DLP_PATTERNS:
        out = pattern.sub(replacement, out)
    for tok in extra_tokens:
        if tok:
            out = out.replace(tok, "[REDACTED]")
    return out


def scrub_structured(
    reasoning: StructuredReasoning,
    *,
    propagated_labels: frozenset[str] = frozenset(),
    extra_tokens: frozenset[str] = frozenset(),
) -> StructuredReasoning:
    """Return a copy of ``reasoning`` with justification DLP-scrubbed."""
    scrubbed = dlp_scrub(
        reasoning.decision_justification,
        propagated_labels=propagated_labels,
        extra_tokens=extra_tokens,
    )
    return reasoning.model_copy(update={"decision_justification": scrubbed})


def _to_tool_calls(raw: Any) -> tuple[ToolCallRecord, ...]:
    """Coerce a list of dicts / ToolCallRecords into a record tuple."""
    records: list[ToolCallRecord] = []
    for item in raw or ():
        if isinstance(item, ToolCallRecord):
            records.append(item)
        elif isinstance(item, dict):
            records.append(ToolCallRecord(**item))
        else:  # pragma: no cover — defensive
            raise TypeError(f"Cannot coerce {type(item).__name__} to ToolCallRecord")
    return tuple(records)
