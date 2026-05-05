"""High-level emission pipeline: build + seal a decision audit row.

Walks the Section 11.3 emission path end-to-end:

    1. Pre-invocation  - stamp manifest/policy/prompt/model versions
    2. Tool calls      - content-hash params + results
    3. Reasoning       - DLP-scrub + store by reference
    4. Decision output - caller supplies
    5. HITL status     - caller supplies (NONE if no gate fired)
    6. Downstream ref  - caller supplies (None if advisory)
    7. Seal            - AuditStore signs + appends
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from apex_audit.content_store import ContentAddressedStore
from apex_audit.reasoning import (
    ReasoningCapture,
    StructuredReasoning,
    ToolCallRecord,
    scrub_structured,
)
from apex_audit.row import AuditRow, HitlRecord, HitlStatus
from apex_audit.store import AuditStore
from apex_audit.trace import new_decision_id, require_trace_id
from apex_audit.versions import VersionResolver, stamp_versions


@dataclass
class RestrictedTraceStore:
    """Section 11.4 restricted store for raw chain-of-thought.

    Separate from the main audit ledger with stricter access (incident
    investigation only). The emitter only ever hands raw traces here, never
    into the main ``AuditStore``.
    """

    _traces: dict[str, str] = field(default_factory=dict)

    def put(self, decision_id: str, raw_trace: str) -> str:
        if not raw_trace:
            return ""
        self._traces[decision_id] = raw_trace
        return f"restricted://{decision_id}"

    def get(self, decision_id: str) -> str:
        return self._traces[decision_id]

    def __contains__(self, decision_id: str) -> bool:
        return decision_id in self._traces


@dataclass
class AuditEmitter:
    """End-to-end builder for the 14-field audit row.

    Wires the four stores/resolvers together so callers pass domain data only:

    - ``version_resolver`` - resolves manifest/policy/prompt/model SHAs
    - ``content_store``    - hashes + stores inputs and tool results
    - ``audit_store``      - seals and appends the final row
    - ``restricted_store`` - holds raw chain-of-thought (stricter access)
    """

    version_resolver: VersionResolver
    content_store: ContentAddressedStore
    audit_store: AuditStore
    restricted_store: RestrictedTraceStore = field(
        default_factory=RestrictedTraceStore
    )

    def emit(
        self,
        *,
        trace_id: str,
        agent_id: str,
        invoking_identity: str,
        orchestration_name: str,
        tenant_id: str,
        inputs: Any,
        tool_calls: list[dict[str, Any]] | None = None,
        structured_reasoning: StructuredReasoning | None = None,
        raw_reasoning: str = "",
        decision_output: dict[str, Any],
        hitl: HitlRecord | None = None,
        downstream_effect_ref: str | None = None,
        sensitivity_labels: tuple[str, ...] = (),
        cost_attribution: dict[str, float] | None = None,
        confidence_score: float | None = None,
        decision_id: str | None = None,
        extra_dlp_tokens: frozenset[str] = frozenset(),
    ) -> dict[str, Any]:
        """Build, seal, append. Return the sealed row dict.

        Raises ``TraceMissingError`` if ``trace_id`` is empty - this is the
        runtime enforcement point for Section 11.6.
        """
        require_trace_id(trace_id)

        stamps = stamp_versions(
            self.version_resolver,
            orchestration_name=orchestration_name,
            tenant_id=tenant_id,
        )

        inputs_ref = self.content_store.put(inputs)

        tool_records: tuple[ToolCallRecord, ...] = ()
        if tool_calls:
            tool_records = tuple(
                ToolCallRecord(
                    mcp_tool_id=tc["mcp_tool_id"],
                    tool_version=tc["tool_version"],
                    parameters_hash=self.content_store.put(tc.get("parameters", {})),
                    result_hash=self.content_store.put(tc.get("result", {})),
                )
                for tc in tool_calls
            )

        reasoning = structured_reasoning or StructuredReasoning(
            tool_call_sequence=tool_records,
        )
        # If caller did not fill tool_call_sequence themselves, attach the
        # records we just hashed.
        if not reasoning.tool_call_sequence and tool_records:
            reasoning = reasoning.model_copy(
                update={"tool_call_sequence": tool_records},
            )
        reasoning = scrub_structured(
            reasoning,
            propagated_labels=frozenset(sensitivity_labels),
            extra_tokens=extra_dlp_tokens,
        )
        # Structured reasoning goes into the main ledger by content-hash ref.
        reasoning_trace_ref = self.content_store.put(reasoning.model_dump(mode="json"))

        did = decision_id or new_decision_id()
        if raw_reasoning:
            self.restricted_store.put(did, raw_reasoning)

        row = AuditRow(
            trace_id=trace_id,
            decision_id=did,
            agent_id=agent_id,
            invoking_identity=invoking_identity,
            manifest_version=stamps.manifest_version,
            policy_version=stamps.policy_version,
            model_version=stamps.model_version,
            prompt_version=stamps.prompt_version,
            inputs_ref=inputs_ref,
            tools_called=tool_records,
            reasoning_trace_ref=reasoning_trace_ref,
            decision_output=decision_output,
            hitl_status=hitl or HitlRecord(status=HitlStatus.NONE),
            downstream_effect_ref=downstream_effect_ref,
            cost_attribution=cost_attribution,
            sensitivity_label_propagation=sensitivity_labels,
            confidence_score=confidence_score,
        )
        return self.audit_store.append(row)

    # ------------------------------------------------------------------
    # Auditor tool (Section 11, Task 12.3.2)

    def resolve_decision(
        self, decision_id: str
    ) -> dict[str, Any]:
        """Given a decision_id, resolve the three SHAs + effective rule-set.

        Returns a dict with the three Git SHAs, inputs payload, structured
        reasoning, and sealed row. Enables an auditor to reconstruct the
        decision without walking the Git registry manually.
        """
        sealed = self.audit_store.get(decision_id)
        return {
            "manifest_version": sealed["manifest_version"],
            "policy_version": sealed["policy_version"],
            "prompt_version": sealed["prompt_version"],
            "model_version": sealed["model_version"],
            "inputs": self.content_store.get(sealed["inputs_ref"]),
            "structured_reasoning": self.content_store.get(
                sealed["reasoning_trace_ref"]
            ),
            "row": sealed,
        }


__all__ = [
    "AuditEmitter",
    "ReasoningCapture",
    "RestrictedTraceStore",
]
