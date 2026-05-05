"""Tests for the R4 → R5 migration stub."""

from __future__ import annotations

from apex_standards_fhir import FhirPatient
from apex_standards_fhir.migrations import migrate_patient_r4_to_r5


def test_migration_stub_returns_equivalent_model() -> None:
    patient = FhirPatient.model_validate(
        {"resourceType": "Patient", "id": "ex1", "gender": "female"}
    )
    migrated = migrate_patient_r4_to_r5(patient)
    # Stub: identity transform.
    assert migrated.id == patient.id
    assert migrated.gender == patient.gender
