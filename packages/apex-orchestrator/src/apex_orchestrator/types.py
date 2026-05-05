"""Shared types for the orchestrator runtime."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Callable

StepFn = Callable[[dict[str, Any]], dict[str, Any]]
"""The per-step callable: takes a context dict, returns a result dict."""


@dataclass(frozen=True, slots=True)
class StepResult:
    """One step's completion record."""

    step_id: str
    agent_name: str
    agent_version: str
    result: dict[str, Any] = field(default_factory=dict)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    error_class: str | None = None
