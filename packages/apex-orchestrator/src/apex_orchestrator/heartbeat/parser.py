"""HEARTBEAT.md parser — Sprint 26 Task 26.9.1.

Walks the HEARTBEAT.md frontmatter + body and extracts the declared
routines. Each routine becomes a :class:`HeartbeatRoutine` with
trigger / ORCH / budget / oversight / on-failure / on-anomaly fields
ready for the scheduler.

The parser is deliberately strict — malformed frontmatter or a routine
section missing required fields raises :class:`HeartbeatParseError`,
which the orchestrator surfaces as a "refuse to start" signal per
Sprint 26 §26.9.5.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class HeartbeatParseError(ValueError):
    """Raised when HEARTBEAT.md frontmatter or body cannot be parsed."""


# ---------------------------------------------------------------------------
# Routine model
# ---------------------------------------------------------------------------


@dataclass
class HeartbeatRoutine:
    """One periodic routine declared in HEARTBEAT.md."""

    name: str
    trigger: str
    """Cron-like or named-window expression, e.g., ``"0 6 1-8 * *"``,
    ``"every Monday 08:00 local"``, ``"every hour"``."""

    orch: str
    """Sprint 19 archetype id or Practice ORCH code, e.g., ``"ORCH-RC-04"``."""

    budget: dict[str, Any] = field(default_factory=dict)
    """Wall-clock + tool-call + cost envelope shape — same shape as agent
    spawn budgets."""

    oversight: str = "HITL"
    """``HITL`` / ``HOTL`` / ``HIC``."""

    on_failure: str = ""
    """Named escalation target from ENGAGEMENT.md."""

    on_anomaly: str = ""
    """Optional anomaly rule, e.g., ``">5% variance → escalate to Scott Rodgers"``."""


# ---------------------------------------------------------------------------
# Frontmatter splitter
# ---------------------------------------------------------------------------


_FRONTMATTER_RE = re.compile(
    r"^---\s*\n(.*?)\n---\s*\n(.*)$",
    re.DOTALL,
)


def _split_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    m = _FRONTMATTER_RE.match(raw)
    if m is None:
        raise HeartbeatParseError(
            "HEARTBEAT.md must start with a YAML frontmatter block (---)"
        )
    try:
        front = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as exc:
        raise HeartbeatParseError(f"Frontmatter YAML error: {exc}") from exc
    if not isinstance(front, dict):
        raise HeartbeatParseError(
            f"Frontmatter must be a mapping, got {type(front).__name__}"
        )
    if front.get("file") != "HEARTBEAT.md":
        raise HeartbeatParseError(
            f"Frontmatter file must be 'HEARTBEAT.md', got {front.get('file')!r}"
        )
    return front, m.group(2)


# ---------------------------------------------------------------------------
# Routine extractor
# ---------------------------------------------------------------------------


# Match a routine block starting with either:
#   `### Routine: name`
#   `## Routine N — name`
#   `## Routine N: name`
# and capture all key/value lines until the next same-level header.
_ROUTINE_BLOCK_RE = re.compile(
    r"^(?:###?)\s+Routine[\s\d]*?[\s—:\-]+([^\n]+?)\s*\n"
    r"((?:(?!^##\s).)*?)"
    r"(?=^##\s+|\Z)",
    re.DOTALL | re.MULTILINE,
)

# Match `- **key:** value` or `- **key** — value` rows inside a routine block.
# Tolerates ``orchestration`` (alias for ``orch``).
_ROUTINE_KV_RE = re.compile(
    r"^\s*-\s*\*\*([\w\-/ ]+?)[:*]+\s*[—:-]?\s*(.+?)$",
    re.MULTILINE,
)


# Acceptable aliases — normalize Practice / engagement vocabulary onto
# the parser's required-field names.
_FIELD_ALIASES: dict[str, str] = {
    "orchestration": "orch",
    "on_anomaly": "on_anomaly",
    "on_failure": "on_failure",
}


REQUIRED_FIELDS = {"trigger", "orch", "budget", "oversight"}


def _parse_routine_block(name: str, body: str) -> HeartbeatRoutine:
    fields: dict[str, str] = {}
    for m in _ROUTINE_KV_RE.finditer(body):
        key = m.group(1).strip().lower().replace(" ", "_")
        key = _FIELD_ALIASES.get(key, key)
        value = m.group(2).strip()
        fields[key] = value

    missing = REQUIRED_FIELDS - set(fields.keys())
    if missing:
        raise HeartbeatParseError(
            f"Routine {name!r} missing required fields: {sorted(missing)}; "
            f"got {sorted(fields.keys())}"
        )

    return HeartbeatRoutine(
        name=name.strip(),
        trigger=fields["trigger"],
        orch=fields["orch"],
        budget=_parse_budget_text(fields["budget"]),
        oversight=fields["oversight"].upper().split()[0] if fields["oversight"] else "HITL",
        on_failure=fields.get("on_failure", "").strip(),
        on_anomaly=fields.get("on_anomaly", "").strip(),
    )


def _parse_budget_text(text: str) -> dict[str, Any]:
    """Pull "2 hours, 500 tool calls, $50" → structured budget."""
    out: dict[str, Any] = {}
    for piece in text.split(","):
        piece = piece.strip().lower()
        if not piece:
            continue
        # Wall clock
        m = re.match(r"(\d+)\s*(hour|hr|h|min|minute)s?", piece)
        if m:
            n = int(m.group(1))
            unit = m.group(2)[:1]
            out["wall_s"] = n * 3600 if unit == "h" else n * 60
            continue
        # Tool calls
        m = re.match(r"(\d+)\s*tool\s*call", piece)
        if m:
            out["tool_calls"] = int(m.group(1))
            continue
        # Cost
        m = re.match(r"\$?(\d+(?:\.\d+)?)", piece)
        if m and "$" in piece:
            out["cost_cents"] = int(float(m.group(1)) * 100)
            continue
    return out


def parse_heartbeat(path: str | Path) -> list[HeartbeatRoutine]:
    """Parse a HEARTBEAT.md file into a list of routines.

    Sprint 26 Task 26.9.1 — runs at orchestrator-process startup (not
    per-agent boot). Failure raises :class:`HeartbeatParseError` so the
    orchestrator can refuse to start per §26.9.5.
    """
    p = Path(path)
    if not p.exists():
        raise HeartbeatParseError(f"HEARTBEAT.md not found at {p}")
    raw = p.read_text(encoding="utf-8")
    _front, body = _split_frontmatter(raw)

    routines: list[HeartbeatRoutine] = []
    for m in _ROUTINE_BLOCK_RE.finditer(body):
        name = m.group(1).strip()
        block = m.group(2)
        try:
            routines.append(_parse_routine_block(name, block))
        except HeartbeatParseError:
            raise

    return routines
