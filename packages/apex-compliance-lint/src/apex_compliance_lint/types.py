"""Core types for the compliance linter — Sprint 29 Task 29.9.

Three layers:

- :class:`Rule` — one named compliance rule with a pattern + severity +
  guidance. Rules are independent of the file format; they operate on
  extracted plain text.
- :class:`RulePack` — a named bundle of rules (e.g.,
  ``deloitte_microsoft_independence``, ``apex_typography``,
  ``custom_engagement_overrides``).
- :class:`FileAdapter` — extracts plain text from one file format
  (HTML / DOCX / Markdown / PPTX) so the rule engine can scan
  uniformly.

The configurability boundary is the ``RulePack``. Tenants extending the
framework beyond Deloitte-Microsoft override or add packs without
touching the core engine.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Pattern


class Severity(StrEnum):
    """Compliance violation severity."""

    ERROR = "error"
    """Blocks merge / publish."""

    WARNING = "warning"
    """Surfaces on the PR but does not block."""

    INFO = "info"
    """Informational; suggests an improvement."""


@dataclass(frozen=True)
class Rule:
    """One named compliance rule.

    The ``pattern`` is a compiled regex. Matches in the extracted
    plain text emit a :class:`Violation`. ``allowed_contexts`` is a
    list of regex patterns; if a match falls inside any of those
    contexts (a surrounding window of ±N characters), the rule
    suppresses the violation. This handles cases like "the rule
    explicitly allows 'partner' in the title 'Microsoft Partner Of
    The Year'" — the linter shouldn't flag legitimate award names.
    """

    rule_id: str
    """Stable id, e.g., ``deloitte_microsoft_independence.partner``."""

    description: str
    pattern: Pattern[str]
    severity: Severity = Severity.ERROR
    guidance: str = ""
    """Plain-language explanation + suggested replacement."""

    approved_substitutes: tuple[str, ...] = ()
    """Suggested replacement terms — surfaced in the linter output."""

    allowed_contexts: tuple[Pattern[str], ...] = ()
    """Regex patterns; if the matched text appears within ±50 characters
    of any of these, the violation is suppressed."""


@dataclass
class RulePack:
    """A named bundle of rules."""

    pack_id: str
    name: str
    description: str
    rules: tuple[Rule, ...]
    """Ordered tuple — order does not affect detection but does affect
    consistent output ordering."""

    version: str = "0.1.0"


@dataclass(frozen=True)
class Violation:
    """One compliance-rule violation."""

    rule_id: str
    severity: Severity
    file: Path
    """Path being scanned."""

    line: int
    """1-indexed line number where the match starts."""

    column: int
    """1-indexed column."""

    matched_text: str
    """The exact substring the rule matched."""

    context: str
    """Surrounding context (±60 chars for human readability)."""

    guidance: str = ""
    approved_substitutes: tuple[str, ...] = ()


@dataclass
class LintReport:
    """Result of one or more lint runs."""

    violations: list[Violation] = field(default_factory=list)
    files_scanned: int = 0
    rules_evaluated: int = 0

    @property
    def errors(self) -> list[Violation]:
        return [v for v in self.violations if v.severity == Severity.ERROR]

    @property
    def warnings(self) -> list[Violation]:
        return [v for v in self.violations if v.severity == Severity.WARNING]

    @property
    def infos(self) -> list[Violation]:
        return [v for v in self.violations if v.severity == Severity.INFO]

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    @property
    def exit_code(self) -> int:
        """0 = clean (no errors); 1 = at least one error.
        Config errors get exit code 2 — those don't flow through here."""
        return 0 if self.ok else 1


# ---------------------------------------------------------------------------
# File-adapter Protocol
# ---------------------------------------------------------------------------


class FileAdapter:
    """Per-format plain-text extractor.

    Concrete adapters are in ``apex_compliance_lint.adapters``. Each
    adapter's :meth:`extract` returns a tuple of (line_number, text)
    pairs preserving line numbers for accurate violation reporting.
    """

    file_extensions: tuple[str, ...] = ()
    """Lowercase extensions including the dot, e.g., (`.html`, `.htm`)."""

    def extract(self, path: Path) -> list[tuple[int, str]]:
        """Return [(line_number, line_text), ...] for the rule engine."""
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Rule helpers
# ---------------------------------------------------------------------------


def make_pattern(literal_or_regex: str, *, word_boundary: bool = True) -> Pattern[str]:
    """Build a case-insensitive regex from a literal phrase or pre-formed pattern.

    If ``word_boundary`` is True (default), wraps with ``\\b`` so we don't
    flag ``"partnership"`` as a match for ``"partner"`` unless the rule
    explicitly intends to. Pass an existing escape-aware pattern if more
    control is needed.
    """
    if word_boundary:
        return re.compile(rf"\b{re.escape(literal_or_regex)}\b", re.IGNORECASE)
    return re.compile(literal_or_regex, re.IGNORECASE)
