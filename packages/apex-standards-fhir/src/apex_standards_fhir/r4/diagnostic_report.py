"""FHIR R4 DiagnosticReport resource (APEX subset)."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from apex_standards_fhir.primitives import (
    FhirCodeableConcept,
    FhirIdentifier,
    FhirReference,
    _FHIR_BASE_CONFIG,
)


class FhirDiagnosticReport(BaseModel):
    """FHIR R4 DiagnosticReport — clinical findings report with result links."""

    model_config = _FHIR_BASE_CONFIG

    resource_type: Literal["DiagnosticReport"] = Field(
        "DiagnosticReport", alias="resourceType"
    )
    id: str | None = None
    identifier: list[FhirIdentifier] = Field(default_factory=list)
    status: Literal[
        "registered", "partial", "preliminary", "final", "amended",
        "corrected", "appended", "cancelled", "entered-in-error", "unknown",
    ]
    category: list[FhirCodeableConcept] = Field(default_factory=list)
    code: FhirCodeableConcept = Field(..., description="Name/code for this report.")
    subject: FhirReference | None = None
    encounter: FhirReference | None = None
    effective_date_time: datetime | None = Field(None, alias="effectiveDateTime")
    issued: datetime | None = None
    performer: list[FhirReference] = Field(default_factory=list)
    result: list[FhirReference] = Field(
        default_factory=list, description="References to Observations."
    )
    conclusion: str | None = None
