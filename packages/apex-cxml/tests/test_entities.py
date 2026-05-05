"""Tests for CXML entities."""

from __future__ import annotations

from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import uuid4

from apex_cxml import Customer, Interaction, Loyalty, Order
from apex_cxml.entities import (
    CustomerStatus,
    InteractionChannel,
    LoyaltyTier,
    OrderStatus,
)


def _envelope() -> dict[str, object]:
    return {
        "event_id": uuid4(),
        "event_ts": datetime.now(UTC),
        "entity_id": "test_entity",
        "source_system": "salesforce-cdp",
        "source_system_ts": datetime.now(UTC),
    }


def _scd2() -> dict[str, object]:
    return {
        "scd2_valid_from": datetime.now(UTC),
        "scd2_is_current": True,
        "row_hash": "feedface",
    }


def test_customer_minimal() -> None:
    c = Customer(
        customer_natural="cust_000001",
        status=CustomerStatus.ACTIVE,
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert c.status is CustomerStatus.ACTIVE
    assert c.consent_marketing is False  # default


def test_customer_with_tokenised_fields() -> None:
    c = Customer(
        customer_natural="cust_000001",
        full_name_token="tok_abc123",
        email_token="tok_def456",
        phone_token="tok_789xyz",
        birth_year=1985,
        consent_marketing=True,
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert c.email_token == "tok_def456"


def test_loyalty_defaults() -> None:
    loy = Loyalty(
        customer_key="cust_000001",
        program_code="RC-REWARDS",
        member_number_token="tok_member_999",
        enrolled_date=date(2026, 1, 15),
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert loy.tier is LoyaltyTier.BRONZE
    assert loy.points_balance == 0


def test_interaction_sentiment_range() -> None:
    inter = Interaction(
        channel=InteractionChannel.CHAT,
        occurred_at=datetime.now(UTC),
        sentiment_score=0.8,
        topic="delivery status",
        resolved=True,
        **_envelope(),
    )  # type: ignore[arg-type]
    assert inter.sentiment_score == 0.8


def test_order_with_pci_token() -> None:
    order = Order(
        order_natural="ORD-2026-00001",
        customer_key="cust_000001",
        placed_at=datetime.now(UTC),
        status=OrderStatus.PLACED,
        total_amount=Decimal("123.45"),
        payment_method_token="tok_pm_123",
        **_envelope(),
    )  # type: ignore[arg-type]
    assert order.payment_method_token == "tok_pm_123"
    assert order.status is OrderStatus.PLACED
