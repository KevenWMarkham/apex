"""Round-trip tests for FHIR R4 resources against reference JSON fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from apex_standards_fhir import (
    FhirClaim,
    FhirDiagnosticReport,
    FhirEncounter,
    FhirMedicationRequest,
    FhirObservation,
    FhirPatient,
    FhirPractitioner,
)

pytestmark = pytest.mark.conformance

FIXTURES = Path(__file__).parent / "fixtures"


def _load(name: str) -> dict[str, object]:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


class TestPatient:
    def test_parses_reference_fixture(self) -> None:
        raw = _load("patient_example.json")
        patient = FhirPatient.model_validate(raw)
        assert patient.resource_type == "Patient"
        assert patient.id == "example"
        assert patient.gender == "male"
        assert patient.name[0].family == "Chalmers"
        assert "Peter" in patient.name[0].given

    def test_round_trip_preserves_fhir_json(self) -> None:
        raw = _load("patient_example.json")
        patient = FhirPatient.model_validate(raw)
        emitted = patient.model_dump(by_alias=True, exclude_none=True, mode="json")
        # Key invariants that must survive the round-trip:
        assert emitted["resourceType"] == "Patient"
        assert emitted["birthDate"] == "1974-12-25"
        assert emitted["address"][0]["postalCode"] == "3999"


class TestObservation:
    def test_parses_blood_pressure_fixture(self) -> None:
        raw = _load("observation_example.json")
        obs = FhirObservation.model_validate(raw)
        assert obs.status == "final"
        loinc = obs.code.coding[0]
        assert loinc.system == "http://loinc.org"
        assert loinc.code == "85354-9"
        assert obs.value_quantity is not None
        assert obs.value_quantity.value == 120.0
        assert obs.value_quantity.unit == "mmHg"

    def test_round_trip(self) -> None:
        raw = _load("observation_example.json")
        obs = FhirObservation.model_validate(raw)
        emitted = obs.model_dump(by_alias=True, exclude_none=True, mode="json")
        assert emitted["resourceType"] == "Observation"
        assert emitted["valueQuantity"]["value"] == 120.0
        assert emitted["effectiveDateTime"].startswith("2026-04-19")


class TestMedicationRequest:
    def test_parses_rxnorm_fixture(self) -> None:
        raw = _load("medication_request_example.json")
        mr = FhirMedicationRequest.model_validate(raw)
        assert mr.status == "active"
        assert mr.intent == "order"
        assert mr.medication_codeable_concept is not None
        rxnorm = mr.medication_codeable_concept.coding[0]
        assert "rxnorm" in rxnorm.system.lower()
        assert rxnorm.code == "1049630"
        assert mr.dosage_instruction[0].as_needed_boolean is True

    def test_round_trip_preserves_authored_on(self) -> None:
        raw = _load("medication_request_example.json")
        mr = FhirMedicationRequest.model_validate(raw)
        emitted = mr.model_dump(by_alias=True, exclude_none=True, mode="json")
        assert emitted["resourceType"] == "MedicationRequest"
        assert "authoredOn" in emitted
        assert emitted["dosageInstruction"][0]["asNeededBoolean"] is True


class TestMinimalResources:
    """Minimal-construction smoke tests for resources without dedicated fixtures."""

    def test_encounter_construction(self) -> None:
        enc = FhirEncounter.model_validate({"status": "finished"})
        assert enc.resource_type == "Encounter"
        assert enc.status == "finished"

    def test_diagnostic_report_construction(self) -> None:
        dr = FhirDiagnosticReport.model_validate(
            {
                "status": "final",
                "code": {"coding": [{"system": "http://loinc.org", "code": "24323-8"}]},
            }
        )
        assert dr.status == "final"
        assert dr.code.coding[0].code == "24323-8"

    def test_practitioner_with_qualification(self) -> None:
        raw = {
            "resourceType": "Practitioner",
            "id": "dr-smith",
            "name": [{"family": "Smith", "given": ["Alice"]}],
            "qualification": [
                {
                    "code": {
                        "coding": [
                            {
                                "system": "http://terminology.hl7.org/CodeSystem/v2-0360|2.7",
                                "code": "MD",
                            }
                        ]
                    }
                }
            ],
        }
        p = FhirPractitioner.model_validate(raw)
        assert p.name[0].family == "Smith"
        assert p.qualification[0].code.coding[0].code == "MD"

    def test_claim_with_single_item(self) -> None:
        raw = {
            "resourceType": "Claim",
            "status": "active",
            "type": {"coding": [{"code": "institutional"}]},
            "use": "claim",
            "patient": {"reference": "Patient/example"},
            "created": "2026-04-19T00:00:00Z",
            "provider": {"reference": "Practitioner/dr-smith"},
            "item": [
                {
                    "sequence": 1,
                    "productOrService": {
                        "coding": [{"system": "http://www.ama-assn.org/go/cpt", "code": "99213"}]
                    },
                }
            ],
        }
        claim = FhirClaim.model_validate(raw)
        assert claim.use == "claim"
        assert claim.item[0].product_or_service.coding[0].code == "99213"
