"""Tests for the workspace-root guardrails — Sprint 20 Task 20.5."""

from __future__ import annotations

from pathlib import Path

import pytest

from check_restricted_terminology import (
    Finding,
    scan_path,
    main as restricted_main,
)
from check_standards_licences import (
    check_package,
    find_standards_packages,
    main as licences_main,
)


REPO_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Per-package licence-file presence
# ---------------------------------------------------------------------------


def test_find_standards_packages_returns_all_eight() -> None:
    pkgs = find_standards_packages(REPO_ROOT)
    names = {p.name for p in pkgs}
    expected = {
        "apex-standards-cdisc", "apex-standards-cim", "apex-standards-fhir",
        "apex-standards-isa95", "apex-standards-iso14224", "apex-standards-j1939",
        "apex-standards-opentravel", "apex-standards-sid",
    }
    assert expected.issubset(names)


def test_every_standards_package_has_licence_attribution() -> None:
    pkgs = find_standards_packages(REPO_ROOT)
    for pkg in pkgs:
        issues = check_package(pkg)
        assert not issues, f"{pkg.name}: {issues}"


def test_workspace_root_licence_attribution_exists() -> None:
    assert (REPO_ROOT / "LICENSE-ATTRIBUTION.md").exists()


def test_check_package_detects_missing_file(tmp_path: Path) -> None:
    fake = tmp_path / "apex-standards-fake"
    fake.mkdir()
    issues = check_package(fake)
    assert issues
    assert "missing" in issues[0]


def test_licences_main_passes_on_real_repo() -> None:
    rc = licences_main([str(REPO_ROOT)])
    assert rc == 0


# ---------------------------------------------------------------------------
# Restricted-terminology content scanner
# ---------------------------------------------------------------------------


def test_scan_clean_packages_finds_nothing() -> None:
    findings = scan_path(REPO_ROOT / "packages")
    # Expect exactly zero findings on a clean tree
    assert findings == [], [f"{f.path}: {f.code}" for f in findings]


def test_scan_detects_restricted_filename(tmp_path: Path) -> None:
    bad = tmp_path / "loinc.csv"
    bad.write_text("LOINC_NUM,COMPONENT,PROPERTY\n1234-5,foo,bar\n", encoding="utf-8")
    findings = scan_path(tmp_path)
    codes = {f.code for f in findings}
    assert "RESTRICTED_FILENAME" in codes


def test_scan_detects_loinc_table_dump_in_text_file(tmp_path: Path) -> None:
    bad = tmp_path / "harmless_name.txt"
    bad.write_text(
        "LOINC_NUM, COMPONENT, PROPERTY, TIME_ASPCT, SYSTEM\n"
        "718-7, Hemoglobin, MCnc, Pt, Bld\n",
        encoding="utf-8",
    )
    findings = scan_path(tmp_path)
    codes = {f.code for f in findings}
    assert "RESTRICTED_CONTENT_FINGERPRINT" in codes


def test_scan_allowlists_attribution_md(tmp_path: Path) -> None:
    """LICENSE-ATTRIBUTION.md is allowed to mention LOINC by name."""
    ok = tmp_path / "LICENSE-ATTRIBUTION.md"
    ok.write_text(
        "LOINC_NUM, COMPONENT, PROPERTY (these names appear here for attribution).",
        encoding="utf-8",
    )
    findings = scan_path(tmp_path)
    codes = {f.code for f in findings}
    assert "RESTRICTED_CONTENT_FINGERPRINT" not in codes


def test_scan_skips_dotted_directories(tmp_path: Path) -> None:
    """The scanner ignores .git / __pycache__ / node_modules etc."""
    skipped = tmp_path / ".git" / "loinc.csv"
    skipped.parent.mkdir(parents=True)
    skipped.write_text("noise", encoding="utf-8")
    findings = scan_path(tmp_path)
    assert findings == []


def test_restricted_main_passes_on_real_packages_dir() -> None:
    rc = restricted_main([str(REPO_ROOT / "packages")])
    assert rc == 0


# ---------------------------------------------------------------------------
# Conformance
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_all_standards_packages_have_licences() -> None:
    pkgs = find_standards_packages(REPO_ROOT)
    for pkg in pkgs:
        assert not check_package(pkg)


@pytest.mark.conformance
def test_conformance_workspace_root_attribution_present() -> None:
    assert (REPO_ROOT / "LICENSE-ATTRIBUTION.md").exists()


@pytest.mark.conformance
def test_conformance_no_restricted_content_in_packages() -> None:
    findings = scan_path(REPO_ROOT / "packages")
    assert findings == [], [f"{f.path}: {f.code}" for f in findings]
