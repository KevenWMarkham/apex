"""Tests for the ``apex`` CLI."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from apex_core.cli import app

runner = CliRunner()
FIXTURES = Path(__file__).parent / "fixtures"


def test_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "apex-core 0.1.0" in result.stdout


def test_validate_valid_manifest() -> None:
    result = runner.invoke(
        app, ["validate", str(FIXTURES / "agent_cold_chain_disposition.yaml")]
    )
    assert result.exit_code == 0
    assert "[OK]" in result.stdout


def test_validate_invalid_manifest() -> None:
    result = runner.invoke(
        app, ["validate", str(FIXTURES / "invalid_missing_kind.yaml")]
    )
    assert result.exit_code == 1
    assert "[FAIL]" in result.stdout


def test_classify_bump_patch() -> None:
    result = runner.invoke(app, ["classify-bump", "1.2.3", "1.2.4"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "PATCH"


def test_classify_bump_minor() -> None:
    result = runner.invoke(app, ["classify-bump", "1.2.3", "1.3.0"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "MINOR"


def test_classify_bump_major() -> None:
    result = runner.invoke(app, ["classify-bump", "1.2.3", "2.0.0"])
    assert result.exit_code == 0
    assert result.stdout.strip() == "MAJOR"


def test_classify_bump_regression_exits_nonzero() -> None:
    result = runner.invoke(app, ["classify-bump", "2.0.0", "1.9.9"])
    assert result.exit_code == 1
