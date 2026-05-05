"""Tests for the SID 7-domain subset."""

from __future__ import annotations

from apex_standards_sid import (
    SidBillingAccount,
    SidCustomer,
    SidLifecycleStatus,
    SidParty,
    SidProduct,
    SidProductOffering,
    SidRelatedParty,
    SidResource,
    SidService,
)


def test_party_roundtrip() -> None:
    p = SidParty(id="party-1", name="Jane Doe", party_type="individual")
    assert p.status is SidLifecycleStatus.ACTIVE


def test_customer_references_party() -> None:
    party = SidParty(id="p1", name="Acme Inc.", party_type="organization")
    cust = SidCustomer(id="c1", party_id=party.id, customer_segment="enterprise")
    assert cust.party_id == "p1"


def test_product_offering_to_product() -> None:
    offering = SidProductOffering(id="po1", name="Business Fiber 1 Gbps")
    party = SidParty(id="p1", name="Acme", party_type="organization")
    cust = SidCustomer(id="c1", party_id=party.id)
    product = SidProduct(
        id="prod1", product_offering_id=offering.id, customer_id=cust.id,
        service_ids=["svc1"],
    )
    assert product.product_offering_id == "po1"


def test_service_with_related_party() -> None:
    svc = SidService(
        id="svc1", name="Fiber Access", service_type="network_access",
        related_parties=[SidRelatedParty(party_id="p-owner", role="owner")],
    )
    assert svc.related_parties[0].role == "owner"


def test_resource_types() -> None:
    r = SidResource(id="r1", name="ONT-serial-XYZ", resource_type="physical")
    assert r.resource_type == "physical"


def test_billing_account_defaults_usd() -> None:
    ba = SidBillingAccount(id="ba1", customer_id="c1")
    assert ba.currency == "USD"


def test_lifecycle_statuses_cover_core() -> None:
    values = {s.value for s in SidLifecycleStatus}
    assert {"active", "withdrawn", "obsolete"}.issubset(values)
