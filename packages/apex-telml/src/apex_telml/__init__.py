"""APEX TELML — TMT canonical entities."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Annotated
from uuid import uuid4

from pydantic import Field

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity, ScdType2Fields
from apex_standards_sid import SidCustomer, SidLifecycleStatus


# --- Entities ---------------------------------------------------------------


class CustomerSegment(StrEnum):
    RESIDENTIAL = "residential"
    SMB = "small_business"
    ENTERPRISE = "enterprise"
    WHOLESALE = "wholesale"
    GOVERNMENT = "government"


class TelcoCustomer(CanonicalEntity, ScdType2Fields):
    """TMT canonical customer — extends the APEX CXML concept with telco flavouring."""

    sid_id: str = Field(..., description="TM Forum SID Customer id.")
    party_id: str = Field(..., description="SID Party id that anchors identity.")
    customer_segment: CustomerSegment = CustomerSegment.RESIDENTIAL
    status: SidLifecycleStatus = SidLifecycleStatus.ACTIVE
    account_number_token: Annotated[str, Classification.PII] | None = None
    billing_account_keys: list[str] = Field(default_factory=list)


class ProductOffering(CanonicalEntity, ScdType2Fields):
    """A sellable bundle (e.g. 'Business Fibre 1 Gbps + Static IP')."""

    sid_id: str
    name: str
    description: str = ""
    status: SidLifecycleStatus = SidLifecycleStatus.ACTIVE
    monthly_recurring_charge_usd: float | None = Field(None, ge=0.0)


class Product(CanonicalEntity):
    """An instance of a ProductOffering purchased by a TelcoCustomer."""

    sid_id: str
    product_offering_key: str = Field(..., description="FK → ProductOffering.entity_id.")
    customer_key: str = Field(..., description="FK → TelcoCustomer.entity_id.")
    status: SidLifecycleStatus = SidLifecycleStatus.ACTIVE
    service_keys: list[str] = Field(default_factory=list)


class ServiceKind(StrEnum):
    MOBILE_VOICE = "mobile_voice"
    MOBILE_DATA = "mobile_data"
    FIXED_BROADBAND = "fixed_broadband"
    FIXED_VOICE = "fixed_voice"
    IPTV = "iptv"
    HOSTING = "hosting"
    MESSAGING = "messaging"
    OTHER = "other"


class Service(CanonicalEntity):
    """A provisioned service instance — ties customer to network resources."""

    sid_id: str
    name: str
    service_kind: ServiceKind = ServiceKind.OTHER
    status: SidLifecycleStatus = SidLifecycleStatus.ACTIVE
    provisioned_at: datetime | None = None
    resource_keys: list[str] = Field(default_factory=list)


class ResourceKind(StrEnum):
    PHYSICAL = "physical"
    LOGICAL = "logical"
    VIRTUAL = "virtual"


class NetworkResource(CanonicalEntity):
    """A physical or logical network element."""

    sid_id: str
    name: str
    resource_kind: ResourceKind = ResourceKind.LOGICAL
    status: SidLifecycleStatus = SidLifecycleStatus.ACTIVE
    resource_type: str | None = Field(
        None, description="e.g. 'ONT', 'OLT', 'BaseStation', 'VLAN', 'vCPU'."
    )


class BillingAccount(CanonicalEntity, ScdType2Fields):
    """Billing binding for a TelcoCustomer."""

    sid_id: str
    customer_key: str = Field(..., description="FK → TelcoCustomer.entity_id.")
    currency: str = Field("USD", min_length=3, max_length=3)
    status: SidLifecycleStatus = SidLifecycleStatus.ACTIVE
    credit_limit_usd: float | None = Field(None, ge=0.0)


# --- Translators ------------------------------------------------------------


def _envelope(*, entity_id: str, source_system: str = "sid") -> dict[str, object]:
    now = datetime.now(UTC)
    return {
        "event_id": uuid4(),
        "event_ts": now,
        "entity_id": entity_id,
        "source_system": source_system,
        "source_system_ts": now,
    }


def _scd2() -> dict[str, object]:
    return {
        "scd2_valid_from": datetime.now(UTC),
        "scd2_is_current": True,
        "row_hash": "sid-import",
    }


def telco_customer_from_sid(sid: SidCustomer) -> TelcoCustomer:
    """Translate a SID Customer into an APEX TELML TelcoCustomer."""
    segment = CustomerSegment.RESIDENTIAL
    if sid.customer_segment:
        try:
            segment = CustomerSegment(sid.customer_segment.lower())
        except ValueError:
            segment = CustomerSegment.RESIDENTIAL
    return TelcoCustomer(
        **_envelope(entity_id=f"telco_customer:{sid.id}"),
        **_scd2(),
        sid_id=sid.id,
        party_id=sid.party_id,
        customer_segment=segment,
        status=sid.status,
        billing_account_keys=list(sid.billing_account_ids),
    )  # type: ignore[arg-type]


__all__ = [
    "BillingAccount",
    "CustomerSegment",
    "NetworkResource",
    "Product",
    "ProductOffering",
    "ResourceKind",
    "Service",
    "ServiceKind",
    "TelcoCustomer",
    "telco_customer_from_sid",
]
