"""apex-audit — Sprint 12: Decision Audit Row.

Public surface:

- Row model + enums: ``AuditRow``, ``HitlStatus``, ``HitlRecord``
- Trace discipline: ``TraceContext``, ``new_trace_id``, ``new_decision_id``,
  ``require_trace_id``, ``TraceMissingError``
- Three-version rule: ``VersionStamps``, ``VersionResolver``,
  ``StaticVersionResolver``, ``stamp_versions``
- Reasoning capture: ``StructuredReasoning``, ``ToolCallRecord``,
  ``ReasoningCapture``, ``dlp_scrub``, ``scrub_structured``
- Composite orchestration row: ``OrchestrationCompositeRow``,
  ``ParticipatingAgent``, ``HitlEvent``
- Content store: ``ContentAddressedStore``, ``content_hash``
- Signing: ``sign_row``, ``verify_row``
- Store + emitter: ``AuditStore``, ``AppendOnlyViolationError``,
  ``AuditEmitter``, ``RestrictedTraceStore``
"""

from __future__ import annotations

from apex_audit.composite import (
    HitlEvent,
    OrchestrationCompositeRow,
    ParticipatingAgent,
)
from apex_audit.content_store import ContentAddressedStore, content_hash
from apex_audit.emitter import AuditEmitter, RestrictedTraceStore
from apex_audit.reasoning import (
    ReasoningCapture,
    StructuredReasoning,
    ToolCallRecord,
    dlp_scrub,
    scrub_structured,
)
from apex_audit.row import AuditRow, HitlRecord, HitlStatus
from apex_audit.signing import sign_row, verify_row
from apex_audit.store import AppendOnlyViolationError, AuditStore
from apex_audit.trace import (
    TraceContext,
    TraceMissingError,
    new_decision_id,
    new_trace_id,
    require_trace_id,
)
from apex_audit.versions import (
    StaticVersionResolver,
    VersionResolver,
    VersionStamps,
    stamp_versions,
)

__all__ = [
    "AppendOnlyViolationError",
    "AuditEmitter",
    "AuditRow",
    "AuditStore",
    "ContentAddressedStore",
    "HitlEvent",
    "HitlRecord",
    "HitlStatus",
    "OrchestrationCompositeRow",
    "ParticipatingAgent",
    "ReasoningCapture",
    "RestrictedTraceStore",
    "StaticVersionResolver",
    "StructuredReasoning",
    "ToolCallRecord",
    "TraceContext",
    "TraceMissingError",
    "VersionResolver",
    "VersionStamps",
    "content_hash",
    "dlp_scrub",
    "new_decision_id",
    "new_trace_id",
    "require_trace_id",
    "scrub_structured",
    "sign_row",
    "stamp_versions",
    "verify_row",
]
