"""Round-trip tests for FHIR ↔ HLSCML translators."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from apex_standards_fhir import FhirObservation, FhirPatient

from apex_hlscml.translators import (
    observation_from_fhir,
    observation_to_fhir,
    patient_from_fhir,
    patient_to_fhir,
)

pytestmark = pytest.mark.conformance

FHIR_FIXTURES = Path(__file__).parent.parent.parent / "apex-standards-fhir" / "tests" / "fixtures"


class TestPatientTranslator:
    def test_fhir_to_hlscml_tokenises(self) -> None:
        raw = json.loads((FHIR_FIXTURES / "patient_example.json").read_text())
        fhir = FhirPatient.model_validate(raw)
        patient = patient_from_fhir(fhir)
        # Tokenised — not equal to original cleartext
        assert patient.name_family_token is not None
        assert patient.name_family_token != "Chalmers"
        assert patient.name_family_token.startswith("tok_")
        # But birth_date / gender are not PHI — pass through
        assert str(patient.birth_date) == "1974-12-25"
        assert patient.gender == "male"

    def test_round_trip_preserves_identity(self) -> None:
        raw = json.loads((FHIR_FIXTURES / "patient_example.json").read_text())
        fhir = FhirPatient.model_validate(raw)
        patient = patient_from_fhir(fhir)
        back = patient_to_fhir(patient, detokenise=True)
        # After detokenisation the family name is recovered
        assert back.name[0].family == "Chalmers"
        assert back.name[0].given == ["Peter"]
        assert back.gender == "male"
        assert str(back.birth_date) == "1974-12-25"

    def test_to_fhir_without_detokenise_keeps_tokens(self) -> None:
        raw = json.loads((FHIR_FIXTURES / "patient_example.json").read_text())
        fhir = FhirPatient.model_validate(raw)
        patient = patient_from_fhir(fhir)
        token_view = patient_to_fhir(patient, detokenise=False)
        assert token_view.name[0].family.startswith("tok_")


class TestObservationTranslator:
    def test_fhir_to_hlscml(self) -> None:
        raw = json.loads((FHIR_FIXTURES / "observation_example.json").read_text())
        fhir = FhirObservation.model_validate(raw)
        obs = observation_from_fhir(fhir, patient_key="patient:example")
        assert obs.loinc_code == "85354-9"
        assert obs.value_numeric == 120
        assert obs.value_unit == "mmHg"

    def test_round_trip_preserves_values(self) -> None:
        raw = json.loads((FHIR_FIXTURES / "observation_example.json").read_text())
        fhir = FhirObservation.model_validate(raw)
        obs = observation_from_fhir(fhir, patient_key="patient:example")
        back = observation_to_fhir(obs)
        coding = back.code.coding[0]
        assert coding.system == "http://loinc.org"
        assert coding.code == "85354-9"
        assert back.value_quantity is not None
        assert back.value_quantity.value == 120.0
