"""Tests for the batch registration pipeline (CI-facing)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
from typer.testing import CliRunner

from apex_purview._cli import purview_app
from apex_purview._register import (
    RegistrationReport,
    RegistrationResult,
    discover_schemas,
    main,
    register_all,
)

FIXTURES = Path(__file__).parent / "fixtures"
runner = CliRunner()


# ---------------------------------------------------------------------------
# discover_schemas
# ---------------------------------------------------------------------------


def test_discover_schemas_finds_scml_fixture(tmp_path: Path) -> None:
    shutil.copy(FIXTURES / "schema_scml.yaml", tmp_path / "scml.yaml")
    assert discover_schemas(tmp_path) == [tmp_path / "scml.yaml"]


def test_discover_schemas_skips_non_schema_yaml(tmp_path: Path) -> None:
    (tmp_path / "not-a-schema.yaml").write_text("kind: event\nname: foo\n", encoding="utf-8")
    shutil.copy(FIXTURES / "schema_scml.yaml", tmp_path / "scml.yaml")
    results = discover_schemas(tmp_path)
    assert results == [tmp_path / "scml.yaml"]


def test_discover_schemas_skips_noise_dirs(tmp_path: Path) -> None:
    (tmp_path / ".venv").mkdir()
    (tmp_path / ".venv" / "nested.yaml").write_text(
        "kind: schema\nname: ignored\npractice: rc\nfamily: scml\n",
        encoding="utf-8",
    )
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "pkg.yaml").write_text(
        "kind: schema\nname: ignored2\npractice: rc\nfamily: scml\n",
        encoding="utf-8",
    )
    shutil.copy(FIXTURES / "schema_scml.yaml", tmp_path / "valid.yaml")
    results = discover_schemas(tmp_path)
    assert results == [tmp_path / "valid.yaml"]


def test_discover_schemas_handles_malformed_yaml(tmp_path: Path) -> None:
    (tmp_path / "broken.yaml").write_text("this: : invalid:\n::not yaml::\n", encoding="utf-8")
    shutil.copy(FIXTURES / "schema_scml.yaml", tmp_path / "valid.yaml")
    # Malformed YAML is silently skipped, valid schemas still discovered
    results = discover_schemas(tmp_path)
    assert results == [tmp_path / "valid.yaml"]


def test_discover_schemas_finds_yml_extension(tmp_path: Path) -> None:
    shutil.copy(FIXTURES / "schema_scml.yaml", tmp_path / "alt.yml")
    results = discover_schemas(tmp_path)
    assert tmp_path / "alt.yml" in results


def test_discover_schemas_skips_fixtures_dir(tmp_path: Path) -> None:
    """Schemas under a `fixtures/` directory are test-only and never registered."""
    (tmp_path / "fixtures").mkdir()
    shutil.copy(FIXTURES / "schema_scml.yaml", tmp_path / "fixtures" / "test.yaml")
    shutil.copy(FIXTURES / "schema_scml.yaml", tmp_path / "real.yaml")
    results = discover_schemas(tmp_path)
    assert results == [tmp_path / "real.yaml"]


# ---------------------------------------------------------------------------
# register_all (happy + failure + output)
# ---------------------------------------------------------------------------


def test_register_all_empty_repo_returns_empty_report(tmp_path: Path) -> None:
    report = register_all(tmp_path)
    assert report.results == []
    assert report.ok_count == 0
    assert report.fail_count == 0
    assert report.exit_code == 0


def test_register_all_happy_path(tmp_path: Path) -> None:
    shutil.copy(FIXTURES / "schema_scml.yaml", tmp_path / "scml.yaml")
    shutil.copy(FIXTURES / "schema_hls_patient.yaml", tmp_path / "hls.yaml")
    report = register_all(tmp_path)
    assert report.ok_count == 2
    assert report.fail_count == 0
    assert report.exit_code == 0


def test_register_all_failure_path(tmp_path: Path) -> None:
    shutil.copy(FIXTURES / "schema_scml.yaml", tmp_path / "scml.yaml")
    shutil.copy(
        FIXTURES / "schema_unknown_classification.yaml",
        tmp_path / "bad.yaml",
    )
    report = register_all(tmp_path)
    assert report.ok_count == 1
    assert report.fail_count == 1
    assert report.exit_code == 1
    failed = report.failed[0]
    assert "Unknown APEX classification" in (failed.error or "")


def test_register_all_writes_output_artifacts(tmp_path: Path) -> None:
    shutil.copy(FIXTURES / "schema_scml.yaml", tmp_path / "scml.yaml")
    out = tmp_path / "purview-output"
    report = register_all(tmp_path, output_dir=out)
    assert report.exit_code == 0
    # scml schema writes to rc.scml/classifications.json + attachments.json
    classifications = out / "rc.scml" / "classifications.json"
    attachments = out / "rc.scml" / "attachments.json"
    assert classifications.exists()
    assert attachments.exists()
    # Content round-trips through json
    payload = json.loads(classifications.read_text(encoding="utf-8"))
    assert payload["classificationDefs"]
    attach_payload = json.loads(attachments.read_text(encoding="utf-8"))
    assert attach_payload


def test_register_all_explicit_schemas_override_discovery(tmp_path: Path) -> None:
    """When `schemas` is passed explicitly, ``root`` is NOT walked."""
    # tmp_path has no YAMLs at all
    explicit = [FIXTURES / "schema_scml.yaml"]
    report = register_all(tmp_path, schemas=explicit)
    assert report.ok_count == 1


# ---------------------------------------------------------------------------
# RegistrationReport
# ---------------------------------------------------------------------------


def test_registration_report_summary() -> None:
    report = RegistrationReport(
        results=[
            RegistrationResult(path=Path("a.yaml"), ok=True),
            RegistrationResult(path=Path("b.yaml"), ok=False, error="boom"),
        ]
    )
    assert report.ok_count == 1
    assert report.fail_count == 1
    assert report.exit_code == 1
    assert len(report.failed) == 1
    assert "1/2" in report.summary()


# ---------------------------------------------------------------------------
# CLI integration
# ---------------------------------------------------------------------------


def test_cli_register_all_happy_path(tmp_path: Path) -> None:
    shutil.copy(FIXTURES / "schema_scml.yaml", tmp_path / "scml.yaml")
    result = runner.invoke(purview_app, ["register-all", "--root", str(tmp_path)])
    assert result.exit_code == 0
    assert "1/1 schemas emitted" in result.stdout


def test_cli_register_all_failure_fails_build(tmp_path: Path) -> None:
    shutil.copy(
        FIXTURES / "schema_unknown_classification.yaml",
        tmp_path / "bad.yaml",
    )
    result = runner.invoke(purview_app, ["register-all", "--root", str(tmp_path)])
    assert result.exit_code == 1
    assert "FAIL" in result.stdout


def test_cli_register_all_strict_empty(tmp_path: Path) -> None:
    """--strict exits 2 when no schemas are discovered."""
    result = runner.invoke(purview_app, ["register-all", "--root", str(tmp_path), "--strict"])
    assert result.exit_code == 2


def test_cli_register_all_with_output(tmp_path: Path) -> None:
    shutil.copy(FIXTURES / "schema_scml.yaml", tmp_path / "scml.yaml")
    out = tmp_path / "out"
    result = runner.invoke(
        purview_app,
        ["register-all", "--root", str(tmp_path), "--output", str(out)],
    )
    assert result.exit_code == 0
    assert (out / "rc.scml" / "classifications.json").exists()


# ---------------------------------------------------------------------------
# __main__ / argparse entry point
# ---------------------------------------------------------------------------


def test_main_returns_zero_on_empty(tmp_path: Path) -> None:
    # No --strict, empty dir, should exit 0
    assert main([str(tmp_path)]) == 0


def test_main_returns_two_on_empty_with_strict(tmp_path: Path) -> None:
    assert main([str(tmp_path), "--strict"]) == 2


def test_main_returns_one_on_any_failure(tmp_path: Path) -> None:
    shutil.copy(FIXTURES / "schema_unknown_classification.yaml", tmp_path / "bad.yaml")
    assert main([str(tmp_path)]) == 1
