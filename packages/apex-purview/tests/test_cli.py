"""Tests for the apex-purview Typer CLI."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from apex_purview._cli import purview_app

FIXTURES = Path(__file__).parent / "fixtures"
runner = CliRunner()


def test_emit_classifications_stdout() -> None:
    result = runner.invoke(
        purview_app,
        ["emit-classifications", str(FIXTURES / "schema_scml.yaml")],
    )
    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    names = {d["name"] for d in payload["classificationDefs"]}
    assert "APEX.Internal" in names
    assert "APEX.TradeSecret" in names


def test_emit_classifications_include_all() -> None:
    result = runner.invoke(
        purview_app,
        [
            "emit-classifications",
            str(FIXTURES / "schema_no_classifications.yaml"),
            "--include-all",
        ],
    )
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    # Every canonical APEX classification present
    assert len(payload["classificationDefs"]) >= 10


def test_emit_classifications_to_file(tmp_path: Path) -> None:
    out = tmp_path / "classifications.json"
    result = runner.invoke(
        purview_app,
        [
            "emit-classifications",
            str(FIXTURES / "schema_scml.yaml"),
            "--output",
            str(out),
        ],
    )
    assert result.exit_code == 0
    assert out.exists()
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["classificationDefs"]


def test_emit_attachments_stdout() -> None:
    result = runner.invoke(
        purview_app,
        ["emit-attachments", str(FIXTURES / "schema_hls_patient.yaml")],
    )
    assert result.exit_code == 0, result.stdout
    attachments = json.loads(result.stdout)
    types = {a["typeName"] for a in attachments}
    assert "APEX.PHI" in types
    assert "APEX.PII" in types
    assert "APEX.Genetic" in types


def test_emit_classifications_rejects_unknown() -> None:
    result = runner.invoke(
        purview_app,
        [
            "emit-classifications",
            str(FIXTURES / "schema_unknown_classification.yaml"),
        ],
    )
    assert result.exit_code != 0


def test_list_classifications_all() -> None:
    result = runner.invoke(purview_app, ["list-classifications"])
    assert result.exit_code == 0
    # Every canonical key appears
    for key in ("public", "internal", "trade_secret", "pii", "phi", "pci", "restricted"):
        assert key in result.stdout


def test_list_classifications_for_schema() -> None:
    result = runner.invoke(
        purview_app,
        ["list-classifications", str(FIXTURES / "schema_hls_patient.yaml")],
    )
    assert result.exit_code == 0
    assert "phi" in result.stdout
    assert "pii" in result.stdout
    assert "genetic" in result.stdout
    # trade_secret is NOT referenced by the HLS fixture
    assert "trade_secret" not in result.stdout
