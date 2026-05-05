"""FHIR R4 Practitioner resource (APEX subset)."""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field

from apex_standards_fhir.primitives import (
    FhirAddress,
    FhirCodeableConcept,
    FhirContactPoint,
    FhirHumanName,
    FhirIdentifier,
    FhirPeriod,
    FhirReference,
    _FHIR_BASE_CONFIG,
)


class FhirPractitionerQualification(BaseModel):
    """FHIR Practitioner.qualification — certifications / licences."""

    model_config = _FHIR_BASE_CONFIG

    identifier: list[FhirIdentifier] = Field(default_factory=list)
    code: FhirCodeableConcept
    period: FhirPeriod | None = None
    issuer: FhirReference | None = None


class FhirPractitioner(BaseModel):
    """FHIR R4 Practitioner — clinician identity."""

    model_config = _FHIR_BASE_CONFIG

    resource_type: Literal["Practitioner"] = Field("Practitioner", alias="resourceType")
    id: str | None = None
    identifier: list[FhirIdentifier] = Field(default_factory=list)
    active: bool | None = None
    name: list[FhirHumanName] = Field(default_factory=list)
    telecom: list[FhirContactPoint] = Field(default_factory=list)
    address: list[FhirAddress] = Field(default_factory=list)
    gender: Literal["male", "female", "other", "unknown"] | None = None
    birth_date: date | None = Field(None, alias="birthDate")
    qualification: list[FhirPractitionerQualification] = Field(default_factory=list)
