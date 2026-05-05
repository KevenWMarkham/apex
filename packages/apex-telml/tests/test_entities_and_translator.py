"""Tests for TELML entities + SID translator."""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

import pytest

from apex_standards_sid import SidCustomer, SidLifecycleStatus
from apex_telml import (
    BillingAccount,
    CustomerSegment,
    NetworkResource,
    Product,
    ProductOffering,
    ResourceKind,
    Service,
    ServiceKind,
    TelcoCustomer,
    telco_customer_from_sid,
)


def _envelope() -> dict[str, object]:
    return {
        "event_id": uuid4(),
        "event_ts": datetime.now(UTC),
        "entity_id": "test",
        "source_system": "sid",
        "source_system_ts": datetime.now(UTC),
    }


def _scd2() -> dict[str, object]:
    return {
        "scd2_valid_from": datetime.now(UTC),
        "scd2_is_current": True,
        "row_hash": "abc",
    }


def test_telco_customer_default_segment() -> None:
    c = TelcoCustomer(sid_id="c1", party_id="p1", **_envelope(), **_scd2())  # type: ignore[arg-type]
    assert c.customer_segment is CustomerSegment.RESIDENTIAL


def test_product_offering() -> None:
    po = ProductOffering(
        sid_id="po1", name="Business Fibre 1 Gbps",
        monthly_recurring_charge_usd=299.0,
        **_envelope(), **_scd2(),
    )  # type: ignore[arg-type]
    assert po.monthly_recurring_charge_usd == 299.0


def test_product_links_offering_and_customer() -> None:
    p = Product(
        sid_id="prod1", product_offering_key="po:1", customer_key="c:1",
        service_keys=["svc1", "svc2"],
        **_envelope(),
    )  # type: ignore[arg-type]
    assert len(p.service_keys) == 2


def test_service_kind() -> None:
    s = Service(
        sid_id="svc1", name="Fibre Access",
        service_kind=ServiceKind.FIXED_BROADBAND,
        **_envelope(),
    )  # type: ignore[arg-type]
    assert s.service_kind is ServiceKind.FIXED_BROADBAND


def test_network_resource_kinds_enumerated() -> None:
    values = {k.value for k in ResourceKind}
    assert values == {"physical", "logical", "virtual"}


def test_network_resource() -> None:
    nr = NetworkResource(
        sid_id="nr1", name="ONT-SN-987",
        resource_kind=ResourceKind.PHYSICAL,
        resource_type="ONT",
        **_envelope(),
    )  # type: ignore[arg-type]
    assert nr.resource_kind is ResourceKind.PHYSICAL


def test_billing_account_defaults_usd() -> None:
    ba = BillingAccount(sid_id="ba1", customer_key="c:1",
                        **_envelope(), **_scd2())  # type: ignore[arg-type]
    assert ba.currency == "USD"


@pytest.mark.conformance
def test_telco_customer_from_sid() -> None:
    sid = SidCustomer(id="sid-c-1", party_id="sid-p-1",
                      customer_segment="enterprise",
                      billing_account_ids=["ba1", "ba2"])
    tc = telco_customer_from_sid(sid)
    assert tc.sid_id == "sid-c-1"
    assert tc.customer_segment is CustomerSegment.ENTERPRISE
    assert tc.status is SidLifecycleStatus.ACTIVE
    assert len(tc.billing_account_keys) == 2


@pytest.mark.conformance
def test_telco_customer_from_sid_unknown_segment_falls_back() -> None:
    sid = SidCustomer(id="c2", party_id="p2", customer_segment="unknown-type")
    tc = telco_customer_from_sid(sid)
    assert tc.customer_segment is CustomerSegment.RESIDENTIAL
