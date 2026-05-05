"""Tests for typography + color-token compliance tools — Sprint 29 Task 29.10."""

from __future__ import annotations

from pathlib import Path

import pytest

from check_typography_tokens import (
    APPROVED_FAMILIES,
    is_var_reference,
    main as typography_main,
    scan_file as typography_scan_file,
)
from check_color_tokens import (
    main as color_main,
    scan_file as color_scan_file,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Typography tool
# ---------------------------------------------------------------------------


def test_typography_var_reference_is_allowed() -> None:
    assert is_var_reference("var(--apex-font-body)")
    assert is_var_reference("var(--apex-font-display)")
    assert not is_var_reference("Helvetica, sans-serif")
    assert not is_var_reference("\"IBM Plex Sans\"")


def test_typography_approved_families_list_complete() -> None:
    """The three APEX core families plus the system fallback chain."""
    for family in ("fraunces", "ibm plex sans", "jetbrains mono",
                   "system-ui", "sans-serif", "serif", "monospace"):
        assert family in APPROVED_FAMILIES


def test_typography_flags_unapproved_family(tmp_path: Path) -> None:
    p = tmp_path / "bad.css"
    p.write_text(
        ".bad { font-family: Helvetica, Arial, sans-serif; }",
        encoding="utf-8",
    )
    findings = typography_scan_file(p)
    assert len(findings) == 1
    unapproved_lower = [u.lower() for u in findings[0].unapproved]
    assert "helvetica" in unapproved_lower
    assert "arial" in unapproved_lower


def test_typography_accepts_approved_family(tmp_path: Path) -> None:
    p = tmp_path / "ok.css"
    p.write_text(
        '.h1 { font-family: "Fraunces", serif; }',
        encoding="utf-8",
    )
    assert typography_scan_file(p) == []


def test_typography_accepts_var_reference(tmp_path: Path) -> None:
    p = tmp_path / "ok.css"
    p.write_text(
        ".body { font-family: var(--apex-font-body); }",
        encoding="utf-8",
    )
    assert typography_scan_file(p) == []


def test_typography_allowlists_tokens_file(tmp_path: Path) -> None:
    """The tokens file is the only place where literal family declarations
    are expected — they're the source-of-truth definitions."""
    p = tmp_path / "apex-design-tokens.css"
    p.write_text(
        ":root { --apex-font-body: 'IBM Plex Sans', system-ui, sans-serif; }",
        encoding="utf-8",
    )
    assert typography_scan_file(p) == []


def test_typography_html_inline_style(tmp_path: Path) -> None:
    p = tmp_path / "x.html"
    p.write_text(
        '<p style="font-family: Comic Sans MS, sans-serif">hi</p>',
        encoding="utf-8",
    )
    findings = typography_scan_file(p)
    assert len(findings) == 1


def test_typography_main_sprint29_deliverables_pass(tmp_path: Path) -> None:
    """Sprint 29 deliverables (Appendix N + the design-tokens CSS) pass.

    Legacy docs/book/ Word-export HTML predates the design-token
    standardization and is tracked separately for remediation.
    """
    sprint29 = tmp_path / "sprint29"
    sprint29.mkdir()
    src = REPO_ROOT / "docs"
    for name in (
        "apex-design-tokens.css",
        "APEX-Appendix-N-Design-System.md",
        "APEX-Appendix-O-Visual-Artifacts-Index.md",
        "APEX-Chains-Port-Spec.md",
    ):
        target = src / name
        if target.exists():
            (sprint29 / name).write_text(
                target.read_text(encoding="utf-8"), encoding="utf-8",
            )
    rc = typography_main([str(sprint29)])
    assert rc == 0


# ---------------------------------------------------------------------------
# Color-token tool
# ---------------------------------------------------------------------------


def test_color_flags_inline_6digit_hex(tmp_path: Path) -> None:
    p = tmp_path / "bad.css"
    p.write_text(".thing { color: #FF5500; }", encoding="utf-8")
    findings = color_scan_file(p)
    assert len(findings) == 1
    assert findings[0].hex_value == "#FF5500"


def test_color_flags_inline_3digit_hex(tmp_path: Path) -> None:
    p = tmp_path / "bad.css"
    p.write_text(".thing { color: #abc; }", encoding="utf-8")
    findings = color_scan_file(p)
    assert len(findings) == 1


def test_color_flags_8digit_hex_with_alpha(tmp_path: Path) -> None:
    p = tmp_path / "bad.css"
    p.write_text(".thing { color: #80FFAACC; }", encoding="utf-8")
    findings = color_scan_file(p)
    assert len(findings) == 1
    assert findings[0].hex_value.upper() == "#80FFAACC"


def test_color_accepts_var_reference(tmp_path: Path) -> None:
    p = tmp_path / "ok.css"
    p.write_text(".thing { color: var(--apex-text); }", encoding="utf-8")
    assert color_scan_file(p) == []


def test_color_allowlists_tokens_file(tmp_path: Path) -> None:
    p = tmp_path / "apex-design-tokens.css"
    p.write_text(
        ":root { --apex-text: #E8ECF4; --apex-bg: #0A0E1A; }",
        encoding="utf-8",
    )
    assert color_scan_file(p) == []


def test_color_allowlists_appendix_n_documentation(tmp_path: Path) -> None:
    """Appendix N prose discusses hex tokens in its registry tables —
    that prose is documentation, not artifact CSS."""
    p = tmp_path / "APEX-Appendix-N-Design-System.md"
    p.write_text(
        "The token --apex-text is #E8ECF4 in dark theme.",
        encoding="utf-8",
    )
    # md isn't even in the SCAN_EXTENSIONS so this should be empty
    assert color_scan_file(p) == []


def test_color_does_not_match_html_entities(tmp_path: Path) -> None:
    """`&#33;` in HTML is an entity, not a hex literal."""
    p = tmp_path / "ok.html"
    p.write_text("<p>Hello&#33; World</p>", encoding="utf-8")
    assert color_scan_file(p) == []


def test_color_main_sprint29_deliverables_pass(tmp_path: Path) -> None:
    """Sprint 29 deliverables pass the color-token check.

    Legacy docs/APEX - Design and Build/*.html and docs/book/*.html
    predate the design-token standardization (Sprint 29 Task 29.2)
    and remain on the remediation backlog.
    """
    sprint29 = tmp_path / "sprint29"
    sprint29.mkdir()
    src = REPO_ROOT / "docs"
    for name in (
        "apex-design-tokens.css",
        "APEX-Appendix-N-Design-System.md",
        "APEX-Appendix-O-Visual-Artifacts-Index.md",
        "APEX-Chains-Port-Spec.md",
    ):
        target = src / name
        if target.exists():
            (sprint29 / name).write_text(
                target.read_text(encoding="utf-8"), encoding="utf-8",
            )
    rc = color_main([str(sprint29)])
    assert rc == 0


# ---------------------------------------------------------------------------
# Conformance — Sprint 29 acceptance markers
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_design_tokens_css_present() -> None:
    """Sprint 29 Task 29.2 §8 — `apex-design-tokens.css` exists."""
    assert (REPO_ROOT / "docs" / "apex-design-tokens.css").exists()


@pytest.mark.conformance
def test_conformance_appendix_n_present() -> None:
    """Sprint 29 Task 29.2 — Appendix N is published."""
    assert (REPO_ROOT / "docs" / "APEX-Appendix-N-Design-System.md").exists()


@pytest.mark.conformance
def test_conformance_appendix_o_present() -> None:
    """Sprint 29 Task 29.3 — Appendix O is published."""
    assert (REPO_ROOT / "docs" / "APEX-Appendix-O-Visual-Artifacts-Index.md").exists()


@pytest.mark.conformance
def test_conformance_chains_port_spec_present() -> None:
    """Sprint 29 Task 29.8 — Chains port spec is published."""
    assert (REPO_ROOT / "docs" / "APEX-Chains-Port-Spec.md").exists()
