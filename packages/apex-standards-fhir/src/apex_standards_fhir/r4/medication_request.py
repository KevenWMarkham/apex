"""FHIR R4 MedicationRequest resource (APEX subset)."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from apex_standards_fhir.primitives import (
    FhirCodeableConcept,
    FhirIdentifier,
    FhirQuantity,
    FhirReference,
    _FHIR_BASE_CONFIG,
)


class FhirDosage(BaseModel):
    """FHIR Dosage (BackboneElement) — instructions for administration."""

    model_config = _FHIR_BASE_CONFIG

    sequence: int | None = None
    text: str | None = None
    patient_instruction: str | None = Field(None, alias="patientInstruction")
    as_needed_boolean: bool | None = Field(None, alias="asNeededBoolean")
    route: FhirCodeableConcept | None = None
    dose_quantity: FhirQuantity | None = Field(None, alias="doseQuantity")


class FhirMedicationRequest(BaseModel):
    """FHIR R4 MedicationRequest — prescription / medication order."""

    model_config = _FHIR_BASE_CONFIG

    resource_type: Literal["MedicationRequest"] = Field(
        "MedicationRequest", alias="resourceType"
    )
    id: str | None = None
    identifier: list[FhirIdentifier] = Field(default_factory=list)
    status: Literal[
        "active", "on-hold", "cancelled", "completed",
        "entered-in-error", "stopped", "draft", "unknown",
    ]
    intent: Literal[
        "proposal", "plan", "order", "original-order",
        "reflex-order", "filler-order", "instance-order", "option",
    ]
    medication_codeable_concept: FhirCodeableConcept | None = Field(
        None, alias="medicationCodeableConcept"
    )
    medication_reference: FhirReference | None = Field(
        None, alias="medicationReference"
    )
    subject: FhirReference
    encounter: FhirReference | None = None
    authored_on: datetime | None = Field(None, alias="authoredOn")
    requester: FhirReference | None = None
    dosage_instruction: list[FhirDosage] = Field(
        default_factory=list, alias="dosageInstruction"
    )
