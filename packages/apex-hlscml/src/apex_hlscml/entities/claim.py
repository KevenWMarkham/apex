"""HLSCML Claim entities — Pattern C over FHIR R4 Claim."""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity
from apex_schemas_common.standards import CptCode, HcpcsCode


class ClaimStatus(StrEnum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    DRAFT = "draft"
    ENTERED_IN_ERROR = "entered-in-error"


class ClaimType(StrEnum):
    INSTITUTIONAL = "institutional"
    PROFESSIONAL = "professional"
    ORAL = "oral"
    VISION = "vision"
    PHARMACY = "pharmacy"


class ClaimHeader(CanonicalEntity):
    """Claim header — one per claim; line items in :class:`ClaimLine`."""

    fhir_id: str = Field(..., description="FHIR Claim.id.")
    status: ClaimStatus
    claim_type: ClaimType
    patient_key: str = Field(..., description="FK → HLSCML Patient.entity_id.")
    provider_key: str = Field(..., description="FK → HLSCML Practitioner.entity_id.")
    created_ts: datetime
    total_amount: Decimal | None = Field(None, description="Claim total (currency per tenant).")
    currency: str = Field("USD", min_length=3, max_length=3)


class ClaimLine(CanonicalEntity):
    """One line item on a claim — procedure / service / product rendered."""

    fhir_id: str = Field(..., description="FHIR Claim.item.sequence as string id.")
    claim_header_key: str = Field(..., description="FK → HLSCML ClaimHeader.entity_id.")
    sequence: int = Field(..., ge=1)
    cpt_code: CptCode | None = Field(None, description="CPT procedure code.")
    hcpcs_code: HcpcsCode | None = Field(None, description="HCPCS Level-II code.")
    service_date: date | None = None
    quantity: Decimal | None = None
    unit_price: Decimal | None = None
    net_amount: Decimal | None = None
