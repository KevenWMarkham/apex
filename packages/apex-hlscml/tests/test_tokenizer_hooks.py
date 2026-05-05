"""Tests for HLSCML tokenisation hooks."""

from __future__ import annotations

from apex_core.types import Classification
from apex_hlscml import (
    AdverseEvent,
    Patient,
    Practitioner,
    Study,
    StudyEnrollment,
    tokenized_fields,
)


def test_patient_phi_fields_discovered() -> None:
    fields = tokenized_fields(Patient)
    names = {(f.entity, f.field) for f in fields}
    assert ("Patient", "mrn_token") in names
    assert ("Patient", "name_family_token") in names
    assert ("Patient", "name_given_token") in names
    assert ("Patient", "address_token") in names
    assert ("Patient", "phone_token") in names
    assert ("Patient", "email_token") in names


def test_patient_classifications_are_phi() -> None:
    fields = tokenized_fields(Patient)
    for f in fields:
        assert f.classification is Classification.PHI


def test_practitioner_classifications_are_pii() -> None:
    fields = tokenized_fields(Practitioner)
    assert {f.classification for f in fields} == {Classification.PII}


def test_non_tokenised_fields_excluded() -> None:
    fields = tokenized_fields(Patient)
    names = {f.field for f in fields}
    assert "birth_date" not in names
    assert "gender" not in names
    assert "source_fhir_version" not in names


def test_enrollment_subject_key_tokenised() -> None:
    fields = tokenized_fields(StudyEnrollment)
    assert any(f.field == "subject_key_token" for f in fields)


def test_ae_subject_key_tokenised() -> None:
    fields = tokenized_fields(AdverseEvent)
    assert any(f.field == "subject_key_token" for f in fields)


def test_study_has_no_tokenised_fields() -> None:
    # Study-level metadata is not PHI by itself.
    assert tokenized_fields(Study) == []


def test_aggregation_across_entities_sorted() -> None:
    fields = tokenized_fields(Patient, Practitioner, AdverseEvent)
    key = [(f.entity, f.field) for f in fields]
    assert key == sorted(key)
