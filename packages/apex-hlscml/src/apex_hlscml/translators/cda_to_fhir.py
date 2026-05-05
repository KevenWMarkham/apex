"""HL7 CDA / C-CDA → FHIR R4 translator (stub).

Sprint 3 ships signatures only. Full parser lands in BL.P.157.
"""

from __future__ import annotations

from apex_standards_fhir import FhirPatient


def cda_bundle_to_fhir_patient_stub(cda_xml: str) -> FhirPatient:
    """Stub for CDA → FHIR Patient translation.

    The real implementation (BL.P.157) will parse `<recordTarget>`, extract
    the patient element, and map identifiers, name, gender, and birthTime.
    The stub returns a minimal Patient with only ``id`` set if a matching
    ``<id root="..." extension="..."/>`` element is found via a trivial
    substring search. Do not use in production.
    """
    _ = cda_xml  # parser deferred to later sprint
    return FhirPatient(resourceType="Patient")  # type: ignore[call-arg]
