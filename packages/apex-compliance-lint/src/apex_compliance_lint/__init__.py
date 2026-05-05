"""APEX compliance linter — Sprint 29 Task 29.9.

Public API:

- :class:`Rule`, :class:`RulePack`, :class:`Severity`, :class:`Violation`,
  :class:`LintReport` — core types
- :func:`lint_file`, :func:`lint_paths` — engine entry points
- :data:`DEFAULT_PACKS` — Independence + typography + brand baseline
- File adapters: :class:`HTMLAdapter`, :class:`MarkdownAdapter`,
  :class:`DOCXAdapter`, :class:`PPTXAdapter`
- :func:`default_registry` — the extension → adapter mapping
"""

from __future__ import annotations

from apex_compliance_lint.adapters import (
    DOCXAdapter,
    HTMLAdapter,
    MarkdownAdapter,
    PPTXAdapter,
    default_registry,
)
from apex_compliance_lint.engine import (
    CONTEXT_RADIUS,
    evaluate_rule,
    lint_file,
    lint_paths,
)
from apex_compliance_lint.rules import (
    APEX_BRAND,
    APEX_TYPOGRAPHY,
    DEFAULT_PACKS,
    DELOITTE_MICROSOFT_INDEPENDENCE,
)
from apex_compliance_lint.types import (
    FileAdapter,
    LintReport,
    Rule,
    RulePack,
    Severity,
    Violation,
    make_pattern,
)

__all__ = [
    "APEX_BRAND",
    "APEX_TYPOGRAPHY",
    "CONTEXT_RADIUS",
    "DEFAULT_PACKS",
    "DELOITTE_MICROSOFT_INDEPENDENCE",
    "DOCXAdapter",
    "FileAdapter",
    "HTMLAdapter",
    "LintReport",
    "MarkdownAdapter",
    "PPTXAdapter",
    "Rule",
    "RulePack",
    "Severity",
    "Violation",
    "default_registry",
    "evaluate_rule",
    "lint_file",
    "lint_paths",
    "make_pattern",
]

__version__ = "0.1.0"
