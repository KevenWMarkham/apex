"""R4 → R5 migration (stub).

Sprint 3 ships only the entry-point signatures. Actual migration logic lands
when the first APEX tenant pins FHIR R5 and has migration requirements that
can't be met by field-level tolerance.
"""

from __future__ import annotations

from apex_standards_fhir.r4 import FhirPatient


def migrate_patient_r4_to_r5(patient_r4: FhirPatient) -> FhirPatient:
    """Return the R5 equivalent of an R4 Patient resource.

    Sprint 3 stub: returns the input unchanged. R4 Patient and R5 Patient are
    structurally compatible on the fields APEX currently models; a real
    implementation lands when an R5 tenant surfaces a divergence.
    """
    return patient_r4
