"""APEX TM Forum SID Pattern-B mirror — thin slice for TMT."""

from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field

_SID_CONFIG = ConfigDict(extra="forbid")


class SidLifecycleStatus(StrEnum):
    IN_STUDY = "in_study"
    IN_DESIGN = "in_design"
    IN_TEST = "in_test"
    ACTIVE = "active"
    OBSOLETE = "obsolete"
    WITHDRAWN = "withdrawn"


class SidRelatedParty(BaseModel):
    """A party associated with another SID entity in a specific role."""

    model_config = _SID_CONFIG
    party_id: str
    role: str = Field(..., description="e.g. 'customer', 'owner', 'supplier'.")


class SidParty(BaseModel):
    """SID Party — an individual or organisation."""

    model_config = _SID_CONFIG
    id: str
    name: str
    party_type: str = Field(..., description="'individual' or 'organization'.")
    status: SidLifecycleStatus = SidLifecycleStatus.ACTIVE


class SidCustomer(BaseModel):
    """SID Customer — a party in the role of customer."""

    model_config = _SID_CONFIG
    id: str
    party_id: str = Field(..., description="FK → SidParty.id.")
    customer_segment: str | None = None
    status: SidLifecycleStatus = SidLifecycleStatus.ACTIVE
    billing_account_ids: list[str] = Field(default_factory=list)


class SidProductOffering(BaseModel):
    """SID ProductOffering — a sellable package."""

    model_config = _SID_CONFIG
    id: str
    name: str
    description: str = ""
    status: SidLifecycleStatus = SidLifecycleStatus.ACTIVE
    valid_from: str | None = None
    valid_to: str | None = None


class SidProduct(BaseModel):
    """SID Product — an instance of a ProductOffering for a Customer."""

    model_config = _SID_CONFIG
    id: str
    product_offering_id: str
    customer_id: str
    status: SidLifecycleStatus = SidLifecycleStatus.ACTIVE
    service_ids: list[str] = Field(default_factory=list)


class SidService(BaseModel):
    """SID Service — a provisioned service instance."""

    model_config = _SID_CONFIG
    id: str
    name: str
    service_type: str
    status: SidLifecycleStatus = SidLifecycleStatus.ACTIVE
    related_parties: list[SidRelatedParty] = Field(default_factory=list)


class SidResource(BaseModel):
    """SID Resource — a physical or logical network element."""

    model_config = _SID_CONFIG
    id: str
    name: str
    resource_type: str = Field(..., description="e.g. 'physical', 'logical', 'virtual'.")
    status: SidLifecycleStatus = SidLifecycleStatus.ACTIVE


class SidBillingAccount(BaseModel):
    """SID BillingAccount — billing binding for a Customer."""

    model_config = _SID_CONFIG
    id: str
    customer_id: str
    currency: str = Field("USD", min_length=3, max_length=3)
    status: SidLifecycleStatus = SidLifecycleStatus.ACTIVE


__all__ = [
    "SidBillingAccount",
    "SidCustomer",
    "SidLifecycleStatus",
    "SidParty",
    "SidProduct",
    "SidProductOffering",
    "SidRelatedParty",
    "SidResource",
    "SidService",
]
