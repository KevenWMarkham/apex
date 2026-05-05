"""Rule-evaluation engine — Sprint 29 Task 29.9.

Walks every (line_number, line_text) pair from a :class:`FileAdapter`
and applies each rule in the chosen :class:`RulePack`. Emits a
:class:`Violation` for every match, suppressing matches whose
surrounding context falls inside the rule's ``allowed_contexts``.
"""

from __future__ import annotations

from pathlib import Path

from apex_compliance_lint.types import (
    FileAdapter,
    LintReport,
    Rule,
    RulePack,
    Severity,
    Violation,
)


CONTEXT_RADIUS = 60
"""±60-char window inside a single line — used for the *reported* context."""

NEIGHBOR_LINES = 2
"""±N adjacent lines included in the *suppression* context (not in the
reported context). Lets allowed-context patterns catch cross-line
negations like 'does not claim partnership / with OpenClaw — not a /
commercial alliance' without making per-line reporting noisy."""


def evaluate_rule(
    rule: Rule, lines: list[tuple[int, str]], path: Path,
) -> list[Violation]:
    """Apply one rule to a list of extracted lines."""
    out: list[Violation] = []
    line_index = {ln: i for i, (ln, _t) in enumerate(lines)}
    for line_no, line_text in lines:
        for m in rule.pattern.finditer(line_text):
            start, end = m.span()
            ctx_start = max(0, start - CONTEXT_RADIUS)
            ctx_end = min(len(line_text), end + CONTEXT_RADIUS)
            inline_context = line_text[ctx_start:ctx_end]

            # Wider neighborhood for suppression checks: ±NEIGHBOR_LINES
            # adjacent lines so cross-line negations like
            # "does not claim partnership ... not a / commercial alliance"
            # can suppress.
            i = line_index[line_no]
            neighbor_start = max(0, i - NEIGHBOR_LINES)
            neighbor_end = min(len(lines), i + NEIGHBOR_LINES + 1)
            neighborhood = " ".join(t for _, t in lines[neighbor_start:neighbor_end])

            suppressed = any(
                ac.search(inline_context) or ac.search(neighborhood)
                for ac in rule.allowed_contexts
            )
            if suppressed:
                continue

            out.append(
                Violation(
                    rule_id=rule.rule_id,
                    severity=rule.severity,
                    file=path,
                    line=line_no,
                    column=start + 1,  # 1-indexed
                    matched_text=m.group(0),
                    context=inline_context,
                    guidance=rule.guidance,
                    approved_substitutes=rule.approved_substitutes,
                )
            )
    return out


def lint_file(
    path: Path, adapter: FileAdapter, packs: list[RulePack],
) -> LintReport:
    """Lint one file using one adapter and a list of rule packs.

    Returns a fresh :class:`LintReport` carrying the violations + counts.
    """
    report = LintReport()
    report.files_scanned = 1
    lines = adapter.extract(path)
    for pack in packs:
        for rule in pack.rules:
            report.rules_evaluated += 1
            report.violations.extend(evaluate_rule(rule, lines, path))
    return report


def lint_paths(
    paths: list[Path],
    *,
    adapter_registry: dict[str, FileAdapter],
    packs: list[RulePack],
) -> LintReport:
    """Lint multiple files. Adapter selected by file extension."""
    aggregate = LintReport()
    for path in paths:
        ext = path.suffix.lower()
        adapter = adapter_registry.get(ext)
        if adapter is None:
            continue
        sub = lint_file(path, adapter, packs)
        aggregate.files_scanned += sub.files_scanned
        aggregate.rules_evaluated += sub.rules_evaluated
        aggregate.violations.extend(sub.violations)
    return aggregate
