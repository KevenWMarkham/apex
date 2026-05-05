"""Trace-ID discipline.

A single UUID binds every orchestration step - synchronous calls, async
handoffs, HITL pauses/resumes, retries, downstream action-tool calls - into
one forensic thread. Any audit row missing ``trace_id`` is a bug; the
emitter refuses to seal such a row.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4


class TraceMissingError(Exception):
    """Raised when an emission lacks a ``trace_id``."""


def new_trace_id() -> str:
    return str(uuid4())


def new_decision_id() -> str:
    return str(uuid4())


@dataclass(frozen=True)
class TraceContext:
    """Immutable handle carried across an orchestration.

    Every spawned agent/tool invocation inherits the same ``trace_id``; each
    individual decision mints its own ``decision_id`` via ``child_decision``.
    """

    trace_id: str
    parent_decision_id: str | None = None

    @classmethod
    def start(cls) -> TraceContext:
        return cls(trace_id=new_trace_id())

    def child_decision(self) -> tuple[str, str]:
        """Return ``(trace_id, decision_id)`` for the next emission."""
        return self.trace_id, new_decision_id()


def require_trace_id(trace_id: str | None) -> str:
    if not trace_id:
        raise TraceMissingError(
            "trace_id is required for audit-row emission (Section 11.6)"
        )
    return trace_id
