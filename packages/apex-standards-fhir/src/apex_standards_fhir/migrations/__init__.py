"""FHIR cross-version migrations."""

from apex_standards_fhir.migrations.r4_to_r5 import migrate_patient_r4_to_r5

__all__ = ["migrate_patient_r4_to_r5"]
