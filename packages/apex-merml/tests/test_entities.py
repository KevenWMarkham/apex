"""Tests for MERML entities."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest
from pydantic import ValidationError

from apex_schemas_common import generate_delta_ddl
from apex_merml import (
    Category,
    Competitor,
    Elasticity,
    Markdown,
    Price,
    Promotion,
)
from apex_merml.entities import (
    CompetitorChannel,
    CompetitorMatchKind,
    ElasticityModelKind,
    MarkdownReason,
    PriceKind,
    PromotionType,
)


def _envelope() -> dict[str, object]:
    return {
        "event_id": uuid4(),
        "event_ts": datetime.now(UTC),
        "entity_id": "test_entity",
        "source_system": "oracle-retail",
        "source_system_ts": datetime.now(UTC),
    }


def _scd2() -> dict[str, object]:
    return {
        "scd2_valid_from": datetime.now(UTC),
        "scd2_is_current": True,
        "row_hash": "cafebabe",
    }


def test_category_hierarchy() -> None:
    root = Category(
        category_natural="grocery",
        category_name="Grocery",
        level=0,
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    child = Category(
        category_natural="dairy",
        category_name="Dairy",
        parent_category_key=root.entity_id,
        level=1,
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert child.level == 1
    assert child.parent_category_key == root.entity_id


def test_price_requires_non_negative_amount() -> None:
    Price(
        sku_key="sku_0001",
        kind=PriceKind.LIST,
        amount=Decimal("0"),
        effective_from=datetime.now(UTC),
        **_envelope(),
    )  # type: ignore[arg-type]
    with pytest.raises(ValidationError):
        Price(
            sku_key="sku_0001",
            kind=PriceKind.LIST,
            amount=Decimal("-1"),
            effective_from=datetime.now(UTC),
            **_envelope(),
        )  # type: ignore[arg-type]


def test_promotion_window_and_skus() -> None:
    now = datetime.now(UTC)
    promo = Promotion(
        promotion_natural="PROMO-2026-Q2",
        promotion_type=PromotionType.PERCENT_OFF,
        sku_keys=["sku_0001", "sku_0002"],
        discount_value=Decimal("10"),
        starts_at=now,
        ends_at=now + timedelta(days=14),
        **_envelope(),
    )  # type: ignore[arg-type]
    assert promo.promotion_type is PromotionType.PERCENT_OFF
    assert len(promo.sku_keys) == 2


def test_markdown_with_reason() -> None:
    md = Markdown(
        sku_key="sku_0001",
        reason=MarkdownReason.EXPIRATION,
        original_price=Decimal("10.00"),
        marked_down_price=Decimal("4.99"),
        applied_at=datetime.now(UTC),
        applied_by="cold-chain-disposition-agent@v1.0.0",
        expected_recovery_pct=49.9,
        **_envelope(),
    )  # type: ignore[arg-type]
    assert md.reason is MarkdownReason.EXPIRATION


def test_elasticity_minimal_construction() -> None:
    el = Elasticity(
        sku_key="sku_0001",
        model_kind=ElasticityModelKind.LOG_LOG,
        fit_at=datetime.now(UTC),
        coefficient=Decimal("-1.4"),
        confidence_lower=Decimal("-1.7"),
        confidence_upper=Decimal("-1.1"),
        sample_size=842,
        holdout_r_squared=0.78,
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert el.coefficient == Decimal("-1.4")
    assert el.model_kind is ElasticityModelKind.LOG_LOG


def test_elasticity_holdout_r_squared_bounded() -> None:
    with pytest.raises(ValidationError):
        Elasticity(
            sku_key="sku_0001",
            model_kind=ElasticityModelKind.SEMI_LOG,
            fit_at=datetime.now(UTC),
            coefficient=Decimal("-1.0"),
            holdout_r_squared=1.5,  # > 1.0 invalid
            **_envelope(),
            **_scd2(),
        )  # type: ignore[arg-type]


def test_competitor_match_confidence_bounded() -> None:
    Competitor(
        sku_key="sku_0001",
        competitor_name="Target",
        match_kind=CompetitorMatchKind.GTIN,
        match_confidence=1.0,
        channel=CompetitorChannel.ECOM,
        observed_at=datetime.now(UTC),
        list_price=Decimal("4.99"),
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    with pytest.raises(ValidationError):
        Competitor(
            sku_key="sku_0001",
            competitor_name="Target",
            match_kind=CompetitorMatchKind.HEURISTIC,
            match_confidence=1.5,  # > 1.0 invalid
            channel=CompetitorChannel.ECOM,
            observed_at=datetime.now(UTC),
            list_price=Decimal("4.99"),
            **_envelope(),
            **_scd2(),
        )  # type: ignore[arg-type]


def test_competitor_with_promo_price() -> None:
    comp = Competitor(
        sku_key="sku_0001",
        competitor_name="BigBox",
        competitor_sku_natural="comp-99",
        match_kind=CompetitorMatchKind.GTIN,
        match_confidence=0.97,
        channel=CompetitorChannel.BRICK,
        observed_at=datetime.now(UTC),
        list_price=Decimal("5.99"),
        promo_price=Decimal("4.49"),
        in_stock=True,
        **_envelope(),
        **_scd2(),
    )  # type: ignore[arg-type]
    assert comp.promo_price == Decimal("4.49")
    assert comp.in_stock is True


def test_ddl_generation_for_all_entities() -> None:
    for entity_cls in (Category, Price, Promotion, Markdown, Elasticity, Competitor):
        ddl = generate_delta_ddl(entity_cls, database="silver_merml")
        assert "CREATE TABLE silver_merml." in ddl
        assert "USING DELTA" in ddl
