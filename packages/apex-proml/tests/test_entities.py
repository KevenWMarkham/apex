"""Tests for PROML entities (Sprint 30.4)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from apex_proml import (
    DiscountRule,
    DiscountRuleKind,
    PriceChannel,
    Pricing,
)
from apex_schemas_common import generate_delta_ddl


def _envelope() -> dict[str, object]:
    return {
        "event_id": uuid4(),
        "event_ts": datetime.now(UTC),
        "entity_id": "test_entity",
        "source_system": "rc-pricing-engine",
        "source_system_ts": datetime.now(UTC),
    }


def _scd2() -> dict[str, object]:
    return {
        "scd2_valid_from": datetime.now(UTC),
        "scd2_is_current": True,
        "row_hash": "deadbeef",
    }


# --- Pricing ----------------------------------------------------------------


def test_pricing_minimal_construction() -> None:
    p = Pricing(
        sku_key="sku_0001",
        location_key="store-100",
        channel=PriceChannel.STORE,
        effective_from=datetime.now(UTC),
        list_price=Decimal("9.99"),
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert p.list_price == Decimal("9.99")
    assert p.channel is PriceChannel.STORE
    assert p.floor_price is None


def test_pricing_with_floor_and_map() -> None:
    p = Pricing(
        sku_key="sku_0001",
        channel=PriceChannel.ECOM,
        effective_from=datetime.now(UTC),
        list_price=Decimal("19.99"),
        floor_price=Decimal("12.00"),
        map_price=Decimal("14.99"),
        target_margin_pct=Decimal("35"),
        cost_token="tok-cost-abc123",
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert p.floor_price == Decimal("12.00")
    assert p.map_price == Decimal("14.99")
    assert p.cost_token == "tok-cost-abc123"


def test_pricing_negative_list_rejected() -> None:
    with pytest.raises(ValidationError):
        Pricing(
            sku_key="sku_0001",
            channel=PriceChannel.STORE,
            effective_from=datetime.now(UTC),
            list_price=Decimal("-1"),
            **_envelope(),
            **_scd2(),
        )  # type: ignore[arg-type]


# --- DiscountRule -----------------------------------------------------------


def test_discount_rule_with_cap_pct() -> None:
    r = DiscountRule(
        rule_natural="DR-2026-Q2-001",
        rule_kind=DiscountRuleKind.BUYER_LADDER,
        rule_name="Q2 dairy buyer ladder",
        sku_key=None,
        category_key="cat_dairy",
        effective_from=datetime.now(UTC),
        cap_pct=Decimal("40"),
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert r.rule_kind is DiscountRuleKind.BUYER_LADDER
    assert r.cap_pct == Decimal("40")


def test_discount_rule_with_margin_floor() -> None:
    r = DiscountRule(
        rule_natural="DR-2026-MF-DAIRY",
        rule_kind=DiscountRuleKind.MARGIN_FLOOR,
        rule_name="Dairy margin floor",
        category_key="cat_dairy",
        effective_from=datetime.now(UTC),
        margin_floor_pct=Decimal("18"),
        requires_hitl_above_pct=Decimal("25"),
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert r.margin_floor_pct == Decimal("18")
    assert r.requires_hitl_above_pct == Decimal("25")


def test_discount_rule_requires_at_least_one_cap() -> None:
    """Either cap_pct or margin_floor_pct must be set."""
    with pytest.raises(ValidationError, match="cap_pct or margin_floor_pct"):
        DiscountRule(
            rule_natural="DR-EMPTY",
            rule_kind=DiscountRuleKind.SEASONAL,
            rule_name="Empty rule",
            effective_from=datetime.now(UTC),
            **_envelope(),
            **_scd2(),
        )  # type: ignore[arg-type]


def test_discount_rule_cap_pct_bounded() -> None:
    with pytest.raises(ValidationError):
        DiscountRule(
            rule_natural="DR-OOB",
            rule_kind=DiscountRuleKind.SEASONAL,
            rule_name="Out of bounds",
            effective_from=datetime.now(UTC),
            cap_pct=Decimal("150"),  # > 100 invalid
            **_envelope(),
            **_scd2(),
        )  # type: ignore[arg-type]


def test_discount_rule_with_window() -> None:
    now = datetime.now(UTC)
    r = DiscountRule(
        rule_natural="DR-WIN",
        rule_kind=DiscountRuleKind.CLEARANCE,
        rule_name="EOL clearance",
        sku_key="sku_0001",
        effective_from=now,
        effective_to=now + timedelta(days=30),
        cap_pct=Decimal("70"),
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert r.effective_to is not None


def test_pricing_ddl_generation() -> None:
    ddl = generate_delta_ddl(Pricing, database="silver_proml")
    assert "CREATE TABLE silver_proml.pricing" in ddl
    assert "list_price" in ddl


def test_discount_rule_ddl_generation() -> None:
    # DDL generator derives the table name from the class name lowercased
    # (no snake_case conversion). DiscountRule -> discountrule.
    ddl = generate_delta_ddl(DiscountRule, database="silver_proml")
    assert "CREATE TABLE silver_proml.discountrule" in ddl
    assert "USING DELTA" in ddl
