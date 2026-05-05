"""Tests for apex_adapters.framework — Sprint 15 framework primitives."""

from __future__ import annotations

from pathlib import Path

import pytest

from apex_adapters.framework import (
    Adapter,
    AdapterSpec,
    ConnectionMethod,
    FailureMode,
    FieldMapping,
    Runbook,
    SchemaMapping,
    SmokeTestResult,
    get_adapter,
    list_adapters,
    load_adapter_spec,
    register_adapter,
)


# ---------------------------------------------------------------------------
# FieldMapping + SchemaMapping
# ---------------------------------------------------------------------------


def test_field_mapping_required_fields() -> None:
    f = FieldMapping(source_field="A", bronze_column="a", bronze_type="string")
    assert f.nullable is True
    assert f.classification is None


def test_field_mapping_rejects_unknown_type() -> None:
    with pytest.raises(Exception):  # pydantic ValidationError
        FieldMapping(source_field="A", bronze_column="a", bronze_type="quantum")


def test_schema_mapping_field_count() -> None:
    sm = SchemaMapping(
        source_table="X", bronze_table="bronze_x",
        fields=[
            FieldMapping(source_field="A", bronze_column="a", bronze_type="string"),
            FieldMapping(source_field="B", bronze_column="b", bronze_type="int"),
        ],
    )
    assert sm.field_count() == 2


def test_schema_mapping_classified_fields() -> None:
    sm = SchemaMapping(
        source_table="X", bronze_table="bronze_x",
        fields=[
            FieldMapping(source_field="A", bronze_column="a", bronze_type="string", classification="phi"),
            FieldMapping(source_field="B", bronze_column="b", bronze_type="string", classification="internal"),
            FieldMapping(source_field="C", bronze_column="c", bronze_type="string", classification="phi"),
        ],
    )
    phi = sm.classified_fields("phi")
    assert len(phi) == 2


# ---------------------------------------------------------------------------
# Runbook + FailureMode
# ---------------------------------------------------------------------------


def test_runbook_with_failure_modes() -> None:
    r = Runbook(
        primary_contact="ops@deloitte.com",
        failure_modes=[
            FailureMode(code="A", description="A failure"),
            FailureMode(code="B", description="B failure", severity="critical", retry=True),
        ],
    )
    assert len(r.failure_modes) == 2
    assert r.failure_modes[1].retry is True


# ---------------------------------------------------------------------------
# AdapterSpec
# ---------------------------------------------------------------------------


def test_adapter_spec_total_fields() -> None:
    spec = AdapterSpec(
        name="t", sor_name="T", sor_vendor="TVendor", practice="rc",
        connection_method="odbc", schedule="daily", bronze_workspace="apex-rc-prod-bronze",
        runbook=Runbook(primary_contact="x"),
        schema_mappings=[
            SchemaMapping(
                source_table="X", bronze_table="bronze_x",
                fields=[
                    FieldMapping(source_field="A", bronze_column="a", bronze_type="string"),
                    FieldMapping(source_field="B", bronze_column="b", bronze_type="int"),
                ],
            ),
            SchemaMapping(
                source_table="Y", bronze_table="bronze_y",
                fields=[
                    FieldMapping(source_field="A", bronze_column="a", bronze_type="string"),
                ],
            ),
        ],
    )
    assert spec.total_fields() == 3


def test_adapter_spec_minimal_loads() -> None:
    spec = AdapterSpec(
        name="t", sor_name="T", sor_vendor="V", practice="rc",
        connection_method=ConnectionMethod.ODBC,
        schedule="daily", bronze_workspace="apex-rc-prod-bronze",
        runbook=Runbook(primary_contact="x@deloitte.com"),
        schema_mappings=[],
    )
    assert spec.kind == "adapter"


# ---------------------------------------------------------------------------
# load_adapter_spec
# ---------------------------------------------------------------------------


def test_load_adapter_spec_rejects_non_mapping(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("- list\n- not mapping\n", encoding="utf-8")
    with pytest.raises(ValueError, match="must parse to a mapping"):
        load_adapter_spec(bad)


# ---------------------------------------------------------------------------
# Adapter registry
# ---------------------------------------------------------------------------


def test_register_and_get_adapter() -> None:
    # Confirm both shipped adapters are registered (importing
    # apex_adapters triggers registration through implementations/__init__.py)
    assert "epic-clarity" in list_adapters()
    assert "sap-s4hana" in list_adapters()


def test_get_adapter_unknown() -> None:
    with pytest.raises(KeyError, match="Unknown adapter"):
        get_adapter("nope")


def test_register_duplicate_raises() -> None:
    @register_adapter("test-only-unique")
    class _A(Adapter):
        def probe(self) -> bool:
            return True

        def discover(self) -> list[str]:
            return []

        def ingest(self, mapping, *, limit=None) -> int:
            return 0

    with pytest.raises(ValueError, match="already registered"):
        @register_adapter("test-only-unique")
        class _B(Adapter):
            def probe(self) -> bool:
                return True

            def discover(self) -> list[str]:
                return []

            def ingest(self, mapping, *, limit=None) -> int:
                return 0


# ---------------------------------------------------------------------------
# SmokeTestResult
# ---------------------------------------------------------------------------


def test_smoke_test_result_ok_default() -> None:
    r = SmokeTestResult(adapter_name="x")
    assert r.ok
    assert r.exit_code == 0


def test_smoke_test_result_with_errors() -> None:
    r = SmokeTestResult(adapter_name="x", errors=["boom"])
    assert not r.ok
    assert r.exit_code == 1
