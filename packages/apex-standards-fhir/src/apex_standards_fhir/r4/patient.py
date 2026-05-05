"""FHIR R4 Patient resource (APEX subset)."""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field

from apex_standards_fhir.primitives import (
    FhirAddress,
    FhirContactPoint,
    FhirHumanName,
    FhirIdentifier,
    _FHIR_BASE_CONFIG,
)


class FhirPatient(BaseModel):
    """FHIR R4 Patient — demographic and administrative data."""

    model_config = _FHIR_BASE_CONFIG

    resource_type: Literal["Patient"] = Field("Patient", alias="resourceType")
    id: str | None = None
    identifier: list[FhirIdentifier] = Field(default_factory=list)
    active: bool | None = None
    name: list[FhirHumanName] = Field(default_factory=list)
    telecom: list[FhirContactPoint] = Field(default_factory=list)
    gender: Literal["male", "female", "other", "unknown"] | None = None
    birth_date: date | None = Field(None, alias="birthDate")
    deceased_boolean: bool | None = Field(None, alias="deceasedBoolean")
    address: list[FhirAddress] = Field(default_factory=list)
