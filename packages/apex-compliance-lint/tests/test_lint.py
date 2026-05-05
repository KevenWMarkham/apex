"""Tests for apex-compliance-lint — Sprint 29 Task 29.9.6."""

from __future__ import annotations

from pathlib import Path

import pytest

from apex_compliance_lint import (
    APEX_BRAND,
    APEX_TYPOGRAPHY,
    DEFAULT_PACKS,
    DELOITTE_MICROSOFT_INDEPENDENCE,
    HTMLAdapter,
    MarkdownAdapter,
    Rule,
    RulePack,
    Severity,
    Violation,
    default_registry,
    evaluate_rule,
    lint_file,
    lint_paths,
    make_pattern,
)


# ---------------------------------------------------------------------------
# Adapters
# ---------------------------------------------------------------------------


def test_html_adapter_extracts_visible_text(tmp_path: Path) -> None:
    p = tmp_path / "x.html"
    p.write_text(
        "<html><body><p>Hello world</p>"
        "<script>console.log('skip me')</script>"
        "<p>Second paragraph</p></body></html>",
        encoding="utf-8",
    )
    lines = HTMLAdapter().extract(p)
    text = " ".join(t for _, t in lines)
    assert "Hello world" in text
    assert "Second paragraph" in text
    assert "skip me" not in text  # script content stripped


def test_html_adapter_handles_malformed(tmp_path: Path) -> None:
    p = tmp_path / "broken.html"
    p.write_text("<html><body><p>partial", encoding="utf-8")
    lines = HTMLAdapter().extract(p)
    assert any("partial" in t for _, t in lines)


def test_markdown_adapter_strips_code_fences(tmp_path: Path) -> None:
    p = tmp_path / "doc.md"
    p.write_text(
        "# Heading\n\n"
        "Some prose with **partner** in it.\n\n"
        "```python\n"
        "x = 'partner inside code is fine'\n"
        "```\n\n"
        "After fence.\n",
        encoding="utf-8",
    )
    lines = MarkdownAdapter().extract(p)
    text = " ".join(t for _, t in lines)
    assert "partner" in text  # prose preserved
    assert "x =" not in text  # code fence stripped
    assert "After fence" in text


def test_markdown_adapter_strips_yaml_frontmatter(tmp_path: Path) -> None:
    p = tmp_path / "doc.md"
    p.write_text(
        "---\n"
        "title: This is a partner doc\n"
        "---\n\n"
        "Body content here.\n",
        encoding="utf-8",
    )
    lines = MarkdownAdapter().extract(p)
    text = " ".join(t for _, t in lines)
    assert "Body content" in text
    assert "title:" not in text   # frontmatter stripped


def test_markdown_adapter_preserves_link_text(tmp_path: Path) -> None:
    p = tmp_path / "doc.md"
    p.write_text(
        "See [the docs](https://example.com/page) for partner details.",
        encoding="utf-8",
    )
    lines = MarkdownAdapter().extract(p)
    text = " ".join(t for _, t in lines)
    assert "the docs" in text
    assert "partner details" in text
    assert "https://" not in text  # URL stripped


# ---------------------------------------------------------------------------
# Rule engine
# ---------------------------------------------------------------------------


def test_evaluate_rule_finds_match(tmp_path: Path) -> None:
    rule = Rule(
        rule_id="test.partner",
        description="match partner",
        pattern=make_pattern("partner"),
        severity=Severity.ERROR,
    )
    lines = [(1, "We are partner with Microsoft.")]
    p = tmp_path / "x.md"
    p.touch()
    violations = evaluate_rule(rule, lines, p)
    assert len(violations) == 1
    assert violations[0].matched_text.lower() == "partner"
    assert violations[0].line == 1


def test_evaluate_rule_word_boundary_default(tmp_path: Path) -> None:
    """`partnership` should NOT match the rule for `partner`."""
    rule = Rule(
        rule_id="test.partner",
        description="match partner",
        pattern=make_pattern("partner"),
        severity=Severity.ERROR,
    )
    lines = [(1, "Our partnership is great.")]
    p = tmp_path / "x.md"
    p.touch()
    violations = evaluate_rule(rule, lines, p)
    assert violations == []


def test_evaluate_rule_allowed_context_suppression(tmp_path: Path) -> None:
    import re

    rule = Rule(
        rule_id="test.partner",
        description="match partner",
        pattern=make_pattern("partner"),
        severity=Severity.ERROR,
        allowed_contexts=(re.compile(r"trading partner", re.IGNORECASE),),
    )
    lines = [(1, "Each trading partner submits an EDI 850.")]
    p = tmp_path / "x.md"
    p.touch()
    violations = evaluate_rule(rule, lines, p)
    assert violations == []


def test_evaluate_rule_case_insensitive(tmp_path: Path) -> None:
    rule = Rule(
        rule_id="test.partner",
        description="match partner",
        pattern=make_pattern("partner"),
        severity=Severity.ERROR,
    )
    lines = [(1, "PARTNER ecosystem expanded.")]
    p = tmp_path / "x.md"
    p.touch()
    violations = evaluate_rule(rule, lines, p)
    assert len(violations) == 1


# ---------------------------------------------------------------------------
# Independence rule pack — positive cases
# ---------------------------------------------------------------------------


@pytest.fixture
def independence_violations(tmp_path: Path) -> list[Violation]:
    p = tmp_path / "violations.md"
    p.write_text(
        "Deloitte and Microsoft jointly delivered this.\n"
        "Our partnership with Microsoft is a Gold Partner relationship.\n"
        "We have an alliance with Salesforce.\n"
        "This solution is recommended by Microsoft.\n"
        "Our team endorses this approach.\n",
        encoding="utf-8",
    )
    report = lint_file(p, MarkdownAdapter(), [DELOITTE_MICROSOFT_INDEPENDENCE])
    return report.violations


def test_independence_flags_partnership(independence_violations) -> None:
    rule_ids = {v.rule_id for v in independence_violations}
    assert "deloitte_microsoft_independence.partnership" in rule_ids


def test_independence_flags_alliance(independence_violations) -> None:
    rule_ids = {v.rule_id for v in independence_violations}
    assert "deloitte_microsoft_independence.alliance" in rule_ids


def test_independence_flags_gold_partner(independence_violations) -> None:
    rule_ids = {v.rule_id for v in independence_violations}
    assert "deloitte_microsoft_independence.gold_partner" in rule_ids


def test_independence_flags_recommended_by(independence_violations) -> None:
    rule_ids = {v.rule_id for v in independence_violations}
    assert "deloitte_microsoft_independence.recommended_by" in rule_ids


def test_independence_flags_jointly(independence_violations) -> None:
    rule_ids = {v.rule_id for v in independence_violations}
    assert "deloitte_microsoft_independence.deloitte_microsoft_jointly" in rule_ids


def test_independence_flags_endorse(independence_violations) -> None:
    rule_ids = {v.rule_id for v in independence_violations}
    assert "deloitte_microsoft_independence.endorse" in rule_ids


# ---------------------------------------------------------------------------
# Independence rule pack — false-positive guards (allowed contexts)
# ---------------------------------------------------------------------------


def test_independence_does_not_flag_trading_partner(tmp_path: Path) -> None:
    p = tmp_path / "ok.md"
    p.write_text(
        "Each trading partner submits an EDI 850 PO. The trading partner "
        "is responsible for ASN compliance.\n",
        encoding="utf-8",
    )
    report = lint_file(p, MarkdownAdapter(), [DELOITTE_MICROSOFT_INDEPENDENCE])
    partner_violations = [
        v for v in report.violations
        if v.rule_id == "deloitte_microsoft_independence.partner"
    ]
    assert partner_violations == [], (
        f"Expected zero 'partner' flags inside 'trading partner' context; "
        f"got {[v.matched_text for v in partner_violations]}"
    )


def test_independence_does_not_flag_microsoft_partner_of_the_year(tmp_path: Path) -> None:
    p = tmp_path / "ok.md"
    p.write_text(
        "We received Microsoft Partner Of The Year in 2024.\n",
        encoding="utf-8",
    )
    report = lint_file(p, MarkdownAdapter(), [DELOITTE_MICROSOFT_INDEPENDENCE])
    partner_violations = [
        v for v in report.violations
        if v.rule_id == "deloitte_microsoft_independence.partner"
    ]
    assert partner_violations == []


def test_independence_does_not_flag_channel_partner(tmp_path: Path) -> None:
    p = tmp_path / "ok.md"
    p.write_text(
        "The dealer is a channel partner for ICE Practice deployments.\n",
        encoding="utf-8",
    )
    report = lint_file(p, MarkdownAdapter(), [DELOITTE_MICROSOFT_INDEPENDENCE])
    partner_violations = [
        v for v in report.violations
        if v.rule_id == "deloitte_microsoft_independence.partner"
    ]
    assert partner_violations == []


# ---------------------------------------------------------------------------
# Brand rule pack
# ---------------------------------------------------------------------------


def test_brand_flags_black_box(tmp_path: Path) -> None:
    p = tmp_path / "brand.md"
    p.write_text("APEX is not a black box — it is auditable.\n", encoding="utf-8")
    report = lint_file(p, MarkdownAdapter(), [APEX_BRAND])
    rule_ids = {v.rule_id for v in report.violations}
    assert "apex_brand.black_box" in rule_ids


def test_brand_flags_fully_autonomous(tmp_path: Path) -> None:
    p = tmp_path / "brand.md"
    p.write_text("APEX is fully autonomous in production.\n", encoding="utf-8")
    report = lint_file(p, MarkdownAdapter(), [APEX_BRAND])
    rule_ids = {v.rule_id for v in report.violations}
    assert "apex_brand.fully_autonomous" in rule_ids


def test_brand_flags_guarantees(tmp_path: Path) -> None:
    p = tmp_path / "brand.md"
    p.write_text(
        "APEX guarantees ROI in Wave-1 delivery.\n",
        encoding="utf-8",
    )
    report = lint_file(p, MarkdownAdapter(), [APEX_BRAND])
    rule_ids = {v.rule_id for v in report.violations}
    assert "apex_brand.guarantees" in rule_ids


# ---------------------------------------------------------------------------
# Multi-file lint_paths
# ---------------------------------------------------------------------------


def test_lint_paths_multiple_files(tmp_path: Path) -> None:
    a = tmp_path / "a.md"
    a.write_text("We have a partnership with Microsoft.\n", encoding="utf-8")
    b = tmp_path / "b.html"
    b.write_text(
        "<html><body><p>Our alliance with SAP.</p></body></html>",
        encoding="utf-8",
    )
    c = tmp_path / "c.md"
    c.write_text("APEX is auditable by design.\n", encoding="utf-8")
    report = lint_paths(
        [a, b, c],
        adapter_registry=default_registry(),
        packs=list(DEFAULT_PACKS),
    )
    assert report.files_scanned == 3
    # a and b each have one Independence violation; c is clean
    assert len(report.errors) >= 2
    files_with_errors = {v.file for v in report.errors}
    assert a in files_with_errors
    assert b in files_with_errors
    assert c not in files_with_errors


def test_lint_paths_skips_unknown_extensions(tmp_path: Path) -> None:
    txt = tmp_path / "notes.txt"
    txt.write_text("partnership with Microsoft", encoding="utf-8")
    report = lint_paths(
        [txt], adapter_registry=default_registry(), packs=list(DEFAULT_PACKS),
    )
    # .txt has no adapter; no violations emitted
    assert report.files_scanned == 0


def test_lint_report_exit_codes(tmp_path: Path) -> None:
    clean = tmp_path / "clean.md"
    clean.write_text("APEX is auditable.\n", encoding="utf-8")
    dirty = tmp_path / "dirty.md"
    dirty.write_text("Our partnership with Microsoft.\n", encoding="utf-8")

    clean_report = lint_paths(
        [clean], adapter_registry=default_registry(), packs=list(DEFAULT_PACKS),
    )
    dirty_report = lint_paths(
        [dirty], adapter_registry=default_registry(), packs=list(DEFAULT_PACKS),
    )
    assert clean_report.exit_code == 0
    assert clean_report.ok is True
    assert dirty_report.exit_code == 1
    assert dirty_report.ok is False


# ---------------------------------------------------------------------------
# Conformance — Sprint 29 §29.9 acceptance
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_three_default_packs() -> None:
    """Sprint 29 §29.9.1 — three default packs ship: independence, typography, brand."""
    pack_ids = {p.pack_id for p in DEFAULT_PACKS}
    assert pack_ids == {
        "deloitte_microsoft_independence",
        "apex_typography",
        "apex_brand",
    }


@pytest.mark.conformance
def test_conformance_independence_pack_minimum_rules() -> None:
    """Independence pack covers the 7 most-flagged Independence-language patterns."""
    rule_ids = {r.rule_id for r in DELOITTE_MICROSOFT_INDEPENDENCE.rules}
    expected = {
        "deloitte_microsoft_independence.partner",
        "deloitte_microsoft_independence.alliance",
        "deloitte_microsoft_independence.partnership",
        "deloitte_microsoft_independence.endorse",
        "deloitte_microsoft_independence.recommended_by",
        "deloitte_microsoft_independence.deloitte_microsoft_jointly",
        "deloitte_microsoft_independence.gold_partner",
    }
    assert expected.issubset(rule_ids)


@pytest.mark.conformance
def test_conformance_default_registry_supports_all_four_formats() -> None:
    """Sprint 29 §29.9.2 — HTML / DOCX / MD / PPTX adapters."""
    reg = default_registry()
    assert ".html" in reg
    assert ".htm" in reg
    assert ".md" in reg
    assert ".markdown" in reg
    assert ".docx" in reg
    assert ".pptx" in reg


@pytest.mark.conformance
def test_conformance_apex_workspace_is_independence_clean() -> None:
    """Sprint 29 acceptance — the apex-workspace files must pass the linter."""
    workspace = Path(__file__).resolve().parents[3] / "apex-workspace"
    files = sorted(p for p in workspace.glob("*.md"))
    assert files, "apex-workspace markdown files must exist"
    report = lint_paths(
        files,
        adapter_registry=default_registry(),
        packs=[DELOITTE_MICROSOFT_INDEPENDENCE],
    )
    if report.errors:
        msgs = [
            f"{v.file.name}:{v.line}:{v.column} [{v.rule_id}] {v.matched_text!r}"
            for v in report.errors
        ]
        pytest.fail(
            f"apex-workspace markdown has Independence violations:\n  "
            + "\n  ".join(msgs)
        )
