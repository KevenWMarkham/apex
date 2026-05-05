"""FHIR R4 Observation resource (APEX subset)."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from apex_standards_fhir.primitives import (
    FhirCodeableConcept,
    FhirIdentifier,
    FhirQuantity,
    FhirReference,
    _FHIR_BASE_CONFIG,
)


class FhirObservation(BaseModel):
    """FHIR R4 Observation — measurement / lab result / vital sign."""

    model_config = _FHIR_BASE_CONFIG

    resource_type: Literal["Observation"] = Field("Observation", alias="resourceType")
    id: str | None = None
    identifier: list[FhirIdentifier] = Field(default_factory=list)
    status: Literal[
        "registered", "preliminary", "final", "amended",
        "corrected", "cancelled", "entered-in-error", "unknown",
    ]
    category: list[FhirCodeableConcept] = Field(default_factory=list)
    code: FhirCodeableConcept = Field(..., description="What is observed (typically LOINC).")
    subject: FhirReference | None = None
    encounter: FhirReference | None = None
    effective_date_time: datetime | None = Field(None, alias="effectiveDateTime")
    value_quantity: FhirQuantity | None = Field(None, alias="valueQuantity")
    value_codeable_concept: FhirCodeableConcept | None = Field(
        None, alias="valueCodeableConcept"
    )
    value_string: str | None = Field(None, alias="valueString")
    value_boolean: bool | None = Field(None, alias="valueBoolean")
    interpretation: list[FhirCodeableConcept] = Field(default_factory=list)
    performer: list[FhirReference] = Field(default_factory=list)
