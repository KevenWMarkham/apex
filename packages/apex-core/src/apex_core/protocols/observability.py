"""Observability protocol — traces, metrics, alerts.

APEX-M satisfies via Azure Monitor + Application Insights + Log Analytics.
APEX-G satisfies via Cloud Logging + Cloud Monitoring.
APEX-A satisfies via CloudWatch + X-Ray.

Adapters for client SIEM (Splunk, Sumo Logic, Datadog) implement this for
parallel-write observability — primary trace stays with the variant, but
metrics and alerts also fire into the client's existing tooling.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable


@dataclass(frozen=True)
class TraceContext:
    trace_id: str
    span_id: str
    parent_span_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Metric:
    name: str           # e.g., "apex.agent.invocation.duration_ms"
    value: float
    tags: dict[str, str] = field(default_factory=dict)


@runtime_checkable
class Observability(Protocol):
    """Emit traces, metrics, and alerts."""

    variant: str

    def start_span(self, *, name: str, parent: TraceContext | None = None) -> TraceContext:
        """Open a new span. Caller is responsible for end_span."""
        ...

    def end_span(self, ctx: TraceContext, *, status: str = "ok") -> None:
        """Close a span and emit it."""
        ...

    def emit_metric(self, metric: Metric) -> None:
        """Emit a single metric data point."""
        ...

    def emit_alert(
        self,
        *,
        severity: str,             # "info" | "warning" | "error" | "critical"
        title: str,
        description: str,
        target: str | None = None,  # e.g., "teams-channel:apex-sre"
    ) -> str:
        """Fire an alert. Returns provider-specific alert id."""
        ...
