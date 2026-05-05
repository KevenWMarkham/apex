"""Tests for the HL7 v2 + CDA stub translators."""

from __future__ import annotations

from apex_hlscml.translators import (
    adt_a01_to_fhir_patient_stub,
    cda_bundle_to_fhir_patient_stub,
)


def test_adt_a01_pid_parsed() -> None:
    msg = (
        "MSH|^~\\&|HOSP|FAC|APEX|DST|20260419000000||ADT^A01|MSG001|P|2.5\n"
        "EVN|A01|20260419000000\n"
        "PID|1||12345^^^HOSP^MR||Smith^Jane^A||19800101|F\n"
        "PV1|1|I|ICU^101^1\n"
    )
    patient = adt_a01_to_fhir_patient_stub(msg)
    assert patient.id == "12345"
    assert patient.name[0].family == "Smith"
    assert patient.name[0].given == ["Jane"]


def test_adt_a01_missing_pid_returns_empty_patient() -> None:
    patient = adt_a01_to_fhir_patient_stub("MSH|...|no-pid-here")
    assert patient.id is None
    assert patient.name == []


def test_cda_stub_returns_empty_patient() -> None:
    # Sprint-3 stub — returns a minimal FhirPatient regardless of input
    patient = cda_bundle_to_fhir_patient_stub("<ClinicalDocument>...</ClinicalDocument>")
    assert patient.resource_type == "Patient"
