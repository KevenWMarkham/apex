"""Tests for the shipped catalog + the two reference implementations."""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from apex_adapters import (
    EpicClarityAdapter,
    SapS4HanaAdapter,
    list_shipped_manifests,
    load_all_shipped_manifests,
    load_shipped_manifest,
)
from apex_adapters._cli import adapters_app
from apex_adapters.catalog import ADAPTER_REGISTRY
from apex_adapters.implementations.sap_s4hana import CANONICAL_SAP_TABLES

FIXTURES = Path(__file__).parent / "fixtures"
runner = CliRunner()


# ---------------------------------------------------------------------------
# Catalog
# ---------------------------------------------------------------------------


def test_catalog_lists_15_shipped_manifests() -> None:
    manifests = list_shipped_manifests()
    assert len(manifests) == 15


def test_every_shipped_manifest_loads_cleanly() -> None:
    manifests = load_all_shipped_manifests()
    assert len(manifests) == 15
    for name, spec in manifests.items():
        # Every loaded spec exposes the canonical attributes
        assert spec.name == name
        assert spec.runbook.primary_contact
        assert spec.connection_method


def test_adapter_registry_covers_every_subtask() -> None:
    """ADAPTER_REGISTRY enumerates Sprint 15 subtasks for each shipped adapter."""
    assert set(ADAPTER_REGISTRY.keys()) == set(list_shipped_manifests())
    expected_subtasks = {
        "15.1.1", "15.1.2",
        "15.2.1", "15.2.2",
        "15.3.1", "15.3.2", "15.3.3", "15.3.4",
        "15.4.1", "15.4.2",
        "15.5.1", "15.5.2",
        "15.6.1", "15.6.2", "15.6.3",
    }
    seen = {meta["subtask"] for meta in ADAPTER_REGISTRY.values()}
    assert seen == expected_subtasks


def test_load_shipped_manifest_unknown_raises() -> None:
    with pytest.raises(FileNotFoundError):
        load_shipped_manifest("nope")


# ---------------------------------------------------------------------------
# Epic Clarity reference implementation
# ---------------------------------------------------------------------------


def test_epic_clarity_rejects_wrong_connection_method() -> None:
    spec = load_shipped_manifest("salesforce")  # connection_method=dataflow_gen2
    with pytest.raises(ValueError, match="connection_method='odbc'"):
        EpicClarityAdapter(spec)


def test_epic_clarity_smoke_test_with_golden_dataset() -> None:
    spec = load_shipped_manifest("epic-clarity")
    adapter = EpicClarityAdapter(spec)
    result = adapter.smoke_test(golden_dataset=FIXTURES / "golden_epic_clarity.json")
    assert result.ok, result.errors
    assert result.rows_read == 3   # 2 PATIENT + 1 PAT_ENC
    assert result.rows_written == 3
    assert result.fields_mapped == 8  # 4 patient + 4 encounter


def test_epic_clarity_discover_uses_golden_keys() -> None:
    spec = load_shipped_manifest("epic-clarity")
    adapter = EpicClarityAdapter(spec)
    adapter.use_golden_dataset(FIXTURES / "golden_epic_clarity.json")
    tables = adapter.discover()
    assert tables == ["PATIENT", "PAT_ENC"]


def test_epic_clarity_detects_missing_required_field(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text(
        '{"PATIENT":[{"PAT_ID":"X"}]}', encoding="utf-8"
    )  # missing PAT_MRN_ID and others
    spec = load_shipped_manifest("epic-clarity")
    adapter = EpicClarityAdapter(spec)
    result = adapter.smoke_test(golden_dataset=bad)
    assert not result.ok
    assert any("missing" in e.lower() for e in result.errors)


# ---------------------------------------------------------------------------
# SAP S/4HANA reference implementation
# ---------------------------------------------------------------------------


def test_sap_rejects_wrong_connection_method() -> None:
    spec = load_shipped_manifest("salesforce")
    with pytest.raises(ValueError, match="connection_method='mirrored_db'"):
        SapS4HanaAdapter(spec)


def test_sap_smoke_test_with_golden_dataset() -> None:
    spec = load_shipped_manifest("sap-s4hana")
    adapter = SapS4HanaAdapter(spec)
    result = adapter.smoke_test(golden_dataset=FIXTURES / "golden_sap.json")
    assert result.ok, result.errors
    assert result.rows_read == 4    # 1 KNA1 + 2 MARA + 1 BSEG
    assert result.fields_mapped == 12  # 3 KNA1 + 3 MARA + 6 BSEG


def test_sap_canonical_tables_in_scope() -> None:
    spec = load_shipped_manifest("sap-s4hana")
    adapter = SapS4HanaAdapter(spec)
    in_scope = adapter.canonical_tables_in_scope()
    # Manifest declares KNA1, MARA, BSEG — all three are canonical
    assert "KNA1" in in_scope
    assert "MARA" in in_scope
    assert "BSEG" in in_scope


def test_canonical_sap_tables_count() -> None:
    """The canonical SAP table set covers the high-frequency engagement subset."""
    assert len(CANONICAL_SAP_TABLES) >= 12
    assert "KNA1" in CANONICAL_SAP_TABLES
    assert "MARA" in CANONICAL_SAP_TABLES
    assert "BSEG" in CANONICAL_SAP_TABLES


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_list() -> None:
    result = runner.invoke(adapters_app, ["list"])
    assert result.exit_code == 0
    assert "epic-clarity" in result.stdout
    assert "sap-s4hana" in result.stdout
    assert "Shipped reference manifests: 15" in result.stdout


def test_cli_inspect() -> None:
    result = runner.invoke(adapters_app, ["inspect", "epic-clarity"])
    assert result.exit_code == 0
    assert "Epic" in result.stdout
    assert "odbc" in result.stdout
    assert "hls" in result.stdout


def test_cli_inspect_unknown_fails() -> None:
    result = runner.invoke(adapters_app, ["inspect", "nope"])
    assert result.exit_code != 0


def test_cli_validate_all() -> None:
    result = runner.invoke(adapters_app, ["validate-all"])
    assert result.exit_code == 0
    assert "15 manifests loaded cleanly" in result.stdout


def test_cli_smoke_test_with_golden() -> None:
    result = runner.invoke(
        adapters_app,
        [
            "smoke-test", "epic-clarity",
            "--golden", str(FIXTURES / "golden_epic_clarity.json"),
        ],
    )
    assert result.exit_code == 0, result.stdout
    assert "rows_read=3" in result.stdout


def test_cli_smoke_test_unregistered_adapter_inspects_only() -> None:
    """Adapters without a registered Python class show an inspect-only message."""
    result = runner.invoke(adapters_app, ["smoke-test", "salesforce"])
    assert result.exit_code == 0
    assert "No adapter implementation registered" in result.stdout
