"""APEX HL7 FHIR Pattern-B mirror — R4 resources + shared primitives."""

from apex_standards_fhir.primitives import (
    FhirAddress,
    FhirCodeableConcept,
    FhirCoding,
    FhirContactPoint,
    FhirHumanName,
    FhirIdentifier,
    FhirPeriod,
    FhirQuantity,
    FhirReference,
)
from apex_standards_fhir.r4 import (
    FhirClaim,
    FhirDiagnosticReport,
    FhirEncounter,
    FhirMedicationRequest,
    FhirObservation,
    FhirPatient,
    FhirPractitioner,
)

__all__ = [
    "FhirAddress",
    "FhirClaim",
    "FhirCodeableConcept",
    "FhirCoding",
    "FhirContactPoint",
    "FhirDiagnosticReport",
    "FhirEncounter",
    "FhirHumanName",
    "FhirIdentifier",
    "FhirMedicationRequest",
    "FhirObservation",
    "FhirPatient",
    "FhirPeriod",
    "FhirPractitioner",
    "FhirQuantity",
    "FhirReference",
]
