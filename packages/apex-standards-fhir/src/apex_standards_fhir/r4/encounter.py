"""FHIR R4 Encounter resource (APEX subset)."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from apex_standards_fhir.primitives import (
    FhirCodeableConcept,
    FhirCoding,
    FhirIdentifier,
    FhirPeriod,
    FhirReference,
    _FHIR_BASE_CONFIG,
)


class FhirEncounter(BaseModel):
    """FHIR R4 Encounter — interaction between a patient and provider(s)."""

    model_config = _FHIR_BASE_CONFIG

    resource_type: Literal["Encounter"] = Field("Encounter", alias="resourceType")
    id: str | None = None
    identifier: list[FhirIdentifier] = Field(default_factory=list)
    status: Literal[
        "planned", "arrived", "triaged", "in-progress", "onleave",
        "finished", "cancelled", "entered-in-error", "unknown",
    ]
    encounter_class: FhirCoding | None = Field(None, alias="class")
    subject: FhirReference | None = None
    participant: list[FhirReference] = Field(default_factory=list)
    period: FhirPeriod | None = None
    reason_code: list[FhirCodeableConcept] = Field(default_factory=list, alias="reasonCode")
    service_provider: FhirReference | None = Field(None, alias="serviceProvider")
