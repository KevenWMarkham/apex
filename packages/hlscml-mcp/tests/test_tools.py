"""Tests for hlscml-mcp tools."""

from __future__ import annotations

import pytest

from apex_core.types import Classification
from fabric_mcp import InMemoryFabricBackend, set_fabric_backend
from hlscml_mcp import (
    CONTRACTS,
    get_patient_by_key,
    list_medications_for_patient,
    list_observations_for_patient,
)
from mcp_common import McpError, McpErrorCode


@pytest.fixture(autouse=True)
def _seed() -> None:
    set_fabric_backend(InMemoryFabricBackend(
        entities={
            ("patient", "pt-1"): {"fhir_id": "ex1", "mrn_token": "tok_mrn"},
        },
        views={
            "gold_hlscml.observation": [
                {"fhir_id": "o-1", "patient_key": "pt-1", "loinc_code": "85354-9"},
                {"fhir_id": "o-2", "patient_key": "pt-1", "loinc_code": "1234-5"},
            ],
            "gold_hlscml.medication_request": [
                {"fhir_id": "m-1", "patient_key": "pt-1"},
            ],
        },
    ))


def test_get_patient() -> None:
    row = get_patient_by_key("pt-1")
    assert row["mrn_token"].startswith("tok_")


def test_get_patient_missing() -> None:
    with pytest.raises(McpError) as exc:
        get_patient_by_key("nope")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_list_observations_all() -> None:
    assert len(list_observations_for_patient("pt-1")) == 2


def test_list_observations_filtered_by_loinc() -> None:
    rows = list_observations_for_patient("pt-1", loinc_code="85354-9")
    assert len(rows) == 1


def test_list_medications() -> None:
    rows = list_medications_for_patient("pt-1")
    assert len(rows) == 1


def test_hls_scope_and_phi_propagation() -> None:
    for c in CONTRACTS:
        assert "practice:hls" in c.required_scopes
        assert Classification.PHI in c.classification_propagation
