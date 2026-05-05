"""FHIR shared primitive datatypes.

Every primitive uses:

- ``populate_by_name=True`` — models construct with snake_case *or* FHIR camelCase.
- ``extra="ignore"`` — unknown FHIR fields are silently dropped so real payloads
  don't fail to parse (scope-discipline: we handle only what HLS agents consume).

Round-trip: construct from FHIR JSON, emit via ``model_dump(by_alias=True)``.
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

_FHIR_BASE_CONFIG = ConfigDict(
    populate_by_name=True,
    extra="ignore",
    use_enum_values=False,
)


class FhirCoding(BaseModel):
    """A coded value drawn from a code system (FHIR Coding)."""

    model_config = _FHIR_BASE_CONFIG

    system: str | None = Field(None, description="URI identifying the code system.")
    version: str | None = None
    code: str | None = None
    display: str | None = None
    user_selected: bool | None = Field(None, alias="userSelected")


class FhirCodeableConcept(BaseModel):
    """A concept represented by one or more codings plus optional free text."""

    model_config = _FHIR_BASE_CONFIG

    coding: list[FhirCoding] = Field(default_factory=list)
    text: str | None = None


class FhirPeriod(BaseModel):
    """A time period with a start and (optionally) an end."""

    model_config = _FHIR_BASE_CONFIG

    start: datetime | None = None
    end: datetime | None = None


class FhirReference(BaseModel):
    """A reference to another FHIR resource (string reference or inline display)."""

    model_config = _FHIR_BASE_CONFIG

    reference: str | None = Field(None, description='e.g. "Patient/example".')
    type: str | None = None
    display: str | None = None


class FhirIdentifier(BaseModel):
    """A business identifier (e.g. MRN, NPI, SSN)."""

    model_config = _FHIR_BASE_CONFIG

    use: Literal["usual", "official", "temp", "secondary", "old"] | None = None
    type: FhirCodeableConcept | None = None
    system: str | None = None
    value: str | None = None
    period: FhirPeriod | None = None
    assigner: FhirReference | None = None


class FhirHumanName(BaseModel):
    """A human name (family + given + use)."""

    model_config = _FHIR_BASE_CONFIG

    use: Literal[
        "usual", "official", "temp", "nickname", "anonymous", "old", "maiden"
    ] | None = None
    text: str | None = None
    family: str | None = None
    given: list[str] = Field(default_factory=list)
    prefix: list[str] = Field(default_factory=list)
    suffix: list[str] = Field(default_factory=list)
    period: FhirPeriod | None = None


class FhirContactPoint(BaseModel):
    """A contact detail (phone, email, fax, url, sms, other)."""

    model_config = _FHIR_BASE_CONFIG

    system: Literal["phone", "fax", "email", "pager", "url", "sms", "other"] | None = None
    value: str | None = None
    use: Literal["home", "work", "temp", "old", "mobile"] | None = None
    rank: int | None = None
    period: FhirPeriod | None = None


class FhirAddress(BaseModel):
    """A postal address."""

    model_config = _FHIR_BASE_CONFIG

    use: Literal["home", "work", "temp", "old", "billing"] | None = None
    type: Literal["postal", "physical", "both"] | None = None
    text: str | None = None
    line: list[str] = Field(default_factory=list)
    city: str | None = None
    district: str | None = None
    state: str | None = None
    postal_code: str | None = Field(None, alias="postalCode")
    country: str | None = None
    period: FhirPeriod | None = None


class FhirQuantity(BaseModel):
    """A measured amount (value + unit + code system)."""

    model_config = _FHIR_BASE_CONFIG

    value: float | None = None
    comparator: Literal["<", "<=", ">=", ">"] | None = None
    unit: str | None = None
    system: str | None = None
    code: str | None = None


# Optional re-exports commonly needed by resource files
__all__ = [
    "FhirAddress",
    "FhirCodeableConcept",
    "FhirCoding",
    "FhirContactPoint",
    "FhirHumanName",
    "FhirIdentifier",
    "FhirPeriod",
    "FhirQuantity",
    "FhirReference",
    "_FHIR_BASE_CONFIG",
    "date",
    "datetime",
]
