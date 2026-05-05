"""Tests for the apex-scenarios Typer CLI."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from apex_scenarios._cli import scenarios_app

FIXTURES = Path(__file__).parent / "fixtures"
runner = CliRunner()


def _setup_root(tmp_path: Path) -> Path:
    """Create a fake repo root with docs/scenarios/_catalog/* fixtures."""
    catalog = tmp_path / "docs" / "scenarios" / "_catalog"
    catalog.mkdir(parents=True)
    (catalog / "scenario-library.json").write_text(
        (FIXTURES / "scenario-library-mini.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (catalog / "featured-chains.json").write_text(
        (FIXTURES / "featured-chains-mini.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return tmp_path


def test_cli_stats(tmp_path: Path) -> None:
    root = _setup_root(tmp_path)
    result = runner.invoke(scenarios_app, ["stats", "--root", str(root)])
    assert result.exit_code == 0
    assert "Total scenarios: 3" in result.stdout
    assert "RC" in result.stdout
    assert "HLS" in result.stdout


def test_cli_validate_fails_on_missing_wave_data(tmp_path: Path) -> None:
    root = _setup_root(tmp_path)
    result = runner.invoke(scenarios_app, ["validate", "--root", str(root)])
    # Mini fixture has no wave fields; wave-data validator must error.
    assert result.exit_code == 1
    assert "wave_data_presence" in result.stdout


def test_cli_validate_skip_wave_check_passes(tmp_path: Path) -> None:
    root = _setup_root(tmp_path)
    result = runner.invoke(
        scenarios_app, ["validate", "--root", str(root), "--skip-wave-check"]
    )
    assert result.exit_code == 0


def test_cli_export_csv_default_filename(tmp_path: Path, monkeypatch) -> None:
    root = _setup_root(tmp_path)
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(scenarios_app, ["export-csv", "--root", str(root)])
    assert result.exit_code == 0
    # Auto-generated canonical filename in CWD
    csvs = list(tmp_path.glob("APEX-scenarios-*.csv"))
    assert len(csvs) == 1
    assert "Wrote 3 rows" in result.stdout


def test_cli_export_csv_practice_filter(tmp_path: Path, monkeypatch) -> None:
    root = _setup_root(tmp_path)
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(
        scenarios_app, ["export-csv", "--root", str(root), "-p", "RC"]
    )
    assert result.exit_code == 0
    assert "Wrote 2 rows" in result.stdout
    csvs = list(tmp_path.glob("APEX-scenarios-rc-*.csv"))
    assert len(csvs) == 1


def test_cli_publish_catalog(tmp_path: Path) -> None:
    root = _setup_root(tmp_path)
    out = tmp_path / "appendix-l"
    result = runner.invoke(
        scenarios_app, ["publish-catalog", "--root", str(root), str(out)]
    )
    assert result.exit_code == 0
    assert (out / "index.md").exists()
    assert (out / "rc.md").exists()


def test_cli_bump_classifies_minor(tmp_path: Path) -> None:
    # Build before/after where AFTER has one new scenario in HLS
    before = json.loads((FIXTURES / "scenario-library-mini.json").read_text(encoding="utf-8"))
    after = json.loads((FIXTURES / "scenario-library-mini.json").read_text(encoding="utf-8"))
    after["HLS"].append({
        "t": "Care-gap closure",
        "s": "HLS-E2E-07",
        "b": "Population-health gap closure with payer-aligned outreach.",
        "k": "+8% closure rate",
        "kk": "up",
    })
    before_path = tmp_path / "before.json"
    after_path = tmp_path / "after.json"
    before_path.write_text(json.dumps(before), encoding="utf-8")
    after_path.write_text(json.dumps(after), encoding="utf-8")

    result = runner.invoke(scenarios_app, ["bump", str(before_path), str(after_path)])
    assert result.exit_code == 0
    assert "MINOR" in result.stdout


def test_cli_bump_classifies_patch(tmp_path: Path) -> None:
    src = (FIXTURES / "scenario-library-mini.json").read_text(encoding="utf-8")
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    a.write_text(src, encoding="utf-8")
    b.write_text(src, encoding="utf-8")

    result = runner.invoke(scenarios_app, ["bump", str(a), str(b)])
    assert result.exit_code == 0
    assert "PATCH" in result.stdout
