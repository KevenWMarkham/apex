"""FHIR R4 Claim resource (APEX subset)."""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, Field

from apex_standards_fhir.primitives import (
    FhirCodeableConcept,
    FhirIdentifier,
    FhirQuantity,
    FhirReference,
    _FHIR_BASE_CONFIG,
)


class FhirClaimItem(BaseModel):
    """One line item on a FHIR R4 Claim."""

    model_config = _FHIR_BASE_CONFIG

    sequence: int
    product_or_service: FhirCodeableConcept = Field(..., alias="productOrService")
    serviced_date: date | None = Field(None, alias="servicedDate")
    quantity: FhirQuantity | None = None
    unit_price: FhirQuantity | None = Field(None, alias="unitPrice")
    net: FhirQuantity | None = None
    encounter: list[FhirReference] = Field(default_factory=list)


class FhirClaim(BaseModel):
    """FHIR R4 Claim — header-level billing / reimbursement request."""

    model_config = _FHIR_BASE_CONFIG

    resource_type: Literal["Claim"] = Field("Claim", alias="resourceType")
    id: str | None = None
    identifier: list[FhirIdentifier] = Field(default_factory=list)
    status: Literal["active", "cancelled", "draft", "entered-in-error"]
    type: FhirCodeableConcept = Field(..., description="Institutional / professional / oral / vision / pharmacy.")
    use: Literal["claim", "preauthorization", "predetermination"]
    patient: FhirReference
    billable_period: FhirReference | None = Field(None, alias="billablePeriod")
    created: datetime
    provider: FhirReference
    priority: FhirCodeableConcept | None = None
    item: list[FhirClaimItem] = Field(default_factory=list)
    total: FhirQuantity | None = None
