"""Tests for apex_schemas_common.standards.catalog — Sprint 20 Task 20.4."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from typer.testing import CliRunner

from apex_core.types import Practice
from apex_schemas_common.standards import (
    STANDARDS,
    StandardSpec,
    StandardType,
)
from apex_schemas_common.standards.catalog import (
    catalog_path,
    check_catalog_drift,
    dict_to_standard,
    emit_catalog,
    load_catalog,
    standard_to_dict,
    write_catalog,
)
from apex_schemas_common._cli import standards_app

runner = CliRunner()


# ---------------------------------------------------------------------------
# Round-trip
# ---------------------------------------------------------------------------


def test_catalog_path_inside_standards_module() -> None:
    p = catalog_path()
    assert p.name == "catalog.yaml"
    assert "standards" in p.parts


def test_emit_catalog_has_kind_and_version() -> None:
    payload = emit_catalog()
    assert payload["kind"] == "apex.standards.catalog"
    assert payload["version"] == 1
    assert payload["count"] == len(STANDARDS)
    assert len(payload["standards"]) == len(STANDARDS)


def test_emit_catalog_keys_sorted() -> None:
    """Stable key ordering for reviewable diffs."""
    payload = emit_catalog()
    ids = [row["id"] for row in payload["standards"]]
    assert ids == sorted(ids)


def test_standard_round_trips_through_dict() -> None:
    """Every shipped StandardSpec round-trips dict <-> StandardSpec cleanly."""
    for sid, spec in STANDARDS.items():
        as_dict = standard_to_dict(spec)
        back = dict_to_standard(as_dict)
        assert back.id == spec.id
        assert back.name == spec.name
        assert back.type == spec.type
        assert back.pattern == spec.pattern
        assert back.apex_pinned_version == spec.apex_pinned_version
        assert back.license == spec.license
        assert back.redistribution_ok == spec.redistribution_ok
        assert set(back.practices) == set(spec.practices)


def test_practices_serialize_as_strings() -> None:
    for spec in STANDARDS.values():
        as_dict = standard_to_dict(spec)
        for p in as_dict["practices"]:
            assert isinstance(p, str)


def test_standard_type_serializes_as_string() -> None:
    spec = STANDARDS["gs1-gtin"]
    as_dict = standard_to_dict(spec)
    assert as_dict["type"] == "identifier"


def test_load_catalog_returns_dict_keyed_by_id() -> None:
    loaded = load_catalog()
    assert loaded
    for sid, spec in loaded.items():
        assert spec.id == sid


def test_load_catalog_round_trip_matches_registry() -> None:
    loaded = load_catalog()
    assert set(loaded) == set(STANDARDS)


def test_write_catalog_creates_or_updates_file(tmp_path: Path) -> None:
    target = tmp_path / "catalog.yaml"
    written = write_catalog(target)
    assert written == target
    assert target.exists()
    with target.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    assert data["count"] == len(STANDARDS)


# ---------------------------------------------------------------------------
# Drift detection
# ---------------------------------------------------------------------------


def test_shipped_catalog_has_no_drift() -> None:
    """The catalog.yaml shipped in the repo matches the in-memory STANDARDS."""
    report = check_catalog_drift()
    if report.errors:
        for issue in report.errors:
            print(f"{issue.standard_id}: [{issue.code}] {issue.message}")
    assert report.ok
    assert report.standards_in_code == report.standards_in_catalog


def test_drift_detects_missing_catalog_row(tmp_path: Path) -> None:
    """If a code-registered standard is absent from catalog.yaml, drift fires."""
    fake_catalog = tmp_path / "catalog.yaml"
    payload = emit_catalog()
    payload["standards"] = payload["standards"][:-1]  # drop one
    payload["count"] = len(payload["standards"])
    with fake_catalog.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(payload, fh)
    report = check_catalog_drift(catalog_file=fake_catalog)
    codes = {i.code for i in report.errors}
    assert "CATALOG_MISSING_ROW" in codes


def test_drift_detects_extra_catalog_row(tmp_path: Path) -> None:
    fake_catalog = tmp_path / "catalog.yaml"
    payload = emit_catalog()
    payload["standards"].append({
        "id": "fake-zombie",
        "name": "Fake Zombie",
        "authority": "x",
        "authority_url": "https://example.com",
        "type": "identifier",
        "current_version": "1",
        "apex_pinned_version": "1",
        "license": "open",
        "redistribution_ok": True,
        "pattern": "A",
        "practices": ["rc"],
    })
    payload["count"] = len(payload["standards"])
    with fake_catalog.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(payload, fh)
    report = check_catalog_drift(catalog_file=fake_catalog)
    codes = {i.code for i in report.errors}
    assert "CODE_MISSING_REGISTRATION" in codes


def test_drift_detects_field_mismatch(tmp_path: Path) -> None:
    fake_catalog = tmp_path / "catalog.yaml"
    payload = emit_catalog()
    # Mutate one field
    for row in payload["standards"]:
        if row["id"] == "gs1-gtin":
            row["apex_pinned_version"] = "BMS-9.99"
            break
    with fake_catalog.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(payload, fh)
    report = check_catalog_drift(catalog_file=fake_catalog)
    codes = {i.code for i in report.errors}
    assert "FIELD_MISMATCH" in codes


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_sync_catalog_check_passes_on_clean_repo() -> None:
    result = runner.invoke(standards_app, ["sync-catalog", "--check"])
    assert result.exit_code == 0
    assert "OK" in result.stdout or "in sync" in result.stdout


def test_cli_validate_catalog_passes_on_clean_repo() -> None:
    result = runner.invoke(standards_app, ["validate-catalog"])
    assert result.exit_code == 0
    assert "OK" in result.stdout or "consistent" in result.stdout


# ---------------------------------------------------------------------------
# Conformance
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_catalog_in_sync() -> None:
    """Sprint 20 BL.P.137 exit criterion — every code registration has a catalog row."""
    report = check_catalog_drift()
    assert report.ok, [
        f"{i.standard_id}: [{i.code}] {i.message}" for i in report.errors
    ]
    assert report.standards_in_code >= 20


@pytest.mark.conformance
def test_conformance_catalog_yaml_exists() -> None:
    assert catalog_path().exists()
    assert catalog_path().stat().st_size > 0
