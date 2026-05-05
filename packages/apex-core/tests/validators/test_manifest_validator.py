"""Tests for ``apex_core.validators.manifest.validate_manifest``."""

from __future__ import annotations

from pathlib import Path

from apex_core.manifests import AgentManifest, ServiceManifest
from apex_core.validators import validate_manifest

FIXTURES = Path(__file__).parent.parent / "fixtures"


def test_valid_agent_fixture() -> None:
    report = validate_manifest(FIXTURES / "agent_cold_chain_disposition.yaml")
    assert report.valid
    assert report.kind == "agent"
    assert isinstance(report.manifest, AgentManifest)
    assert report.errors == []


def test_valid_service_fixture() -> None:
    report = validate_manifest(FIXTURES / "service_cold_chain.yaml")
    assert report.valid
    assert isinstance(report.manifest, ServiceManifest)


def test_missing_kind_fails() -> None:
    report = validate_manifest(FIXTURES / "invalid_missing_kind.yaml")
    assert not report.valid
    assert report.manifest is None
    assert any("kind" in e for e in report.errors)


def test_bad_semver_fails() -> None:
    report = validate_manifest(FIXTURES / "invalid_bad_version.yaml")
    assert not report.valid
    assert report.manifest is None
    assert any("version" in e.lower() or "semver" in e.lower() for e in report.errors)


def test_missing_file() -> None:
    report = validate_manifest(Path("/nonexistent/path/to/manifest.yaml"))
    assert not report.valid
    assert any("not found" in e.lower() for e in report.errors)


def test_summary_format() -> None:
    good = validate_manifest(FIXTURES / "agent_cold_chain_disposition.yaml")
    assert "[OK]" in good.summary()
    bad = validate_manifest(FIXTURES / "invalid_missing_kind.yaml")
    assert "[FAIL]" in bad.summary()
