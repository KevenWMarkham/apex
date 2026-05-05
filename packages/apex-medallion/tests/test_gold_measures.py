"""Tests for the measure model + registry + RC anchor library."""

from __future__ import annotations

import pytest

from apex_core.types import Classification
from apex_medallion.gold import (
    MeasureDefinition,
    MeasureKind,
    MeasureLanguage,
    MeasureRegistry,
)
from apex_medallion.gold.rc_measures import (
    EFFECTIVE_MARGIN_PCT,
    STOCK_DAYS_REMAINING,
    rc_measure_registry,
)


def test_measure_definition_is_frozen() -> None:
    from pydantic import ValidationError
    m = EFFECTIVE_MARGIN_PCT
    with pytest.raises(ValidationError):
        m.name = "other"  # type: ignore[misc]


def test_measure_requires_name_and_formula() -> None:
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        MeasureDefinition(
            name="", kind=MeasureKind.PRE_MEASURE,
            language=MeasureLanguage.PYSPARK,
            owner="x", formula="x",
        )


class TestRegistry:
    def test_register_and_get(self) -> None:
        reg = MeasureRegistry()
        reg.register(EFFECTIVE_MARGIN_PCT)
        assert reg.get("effective_margin_pct") is EFFECTIVE_MARGIN_PCT
        assert "effective_margin_pct" in reg

    def test_duplicate_rejected(self) -> None:
        reg = MeasureRegistry()
        reg.register(EFFECTIVE_MARGIN_PCT)
        with pytest.raises(ValueError):
            reg.register(EFFECTIVE_MARGIN_PCT)

    def test_unknown_raises(self) -> None:
        reg = MeasureRegistry()
        with pytest.raises(KeyError):
            reg.get("missing")

    def test_list_by_kind(self) -> None:
        reg = rc_measure_registry()
        pre = reg.list_by_kind(MeasureKind.PRE_MEASURE)
        post = reg.list_by_kind(MeasureKind.POST_MEASURE)
        assert EFFECTIVE_MARGIN_PCT in pre
        assert STOCK_DAYS_REMAINING in pre
        assert not any(m.kind is MeasureKind.POST_MEASURE for m in pre)
        assert not any(m.kind is MeasureKind.PRE_MEASURE for m in post)

    def test_list_by_language(self) -> None:
        reg = rc_measure_registry()
        dax = reg.list_by_language(MeasureLanguage.DAX)
        tsql = reg.list_by_language(MeasureLanguage.TSQL)
        kql = reg.list_by_language(MeasureLanguage.KQL)
        assert all(m.language is MeasureLanguage.DAX for m in dax)
        assert all(m.language is MeasureLanguage.TSQL for m in tsql)
        assert all(m.language is MeasureLanguage.KQL for m in kql)


class TestRcAnchor:
    def test_registry_populated(self) -> None:
        reg = rc_measure_registry()
        assert len(reg) == 6
        for name in (
            "effective_margin_pct", "stock_days_remaining",
            "time_since_last_event_seconds", "period_over_period_pct",
            "rolling_avg_14_day", "events_last_15_min",
        ):
            assert name in reg

    def test_margin_classification_is_trade_secret(self) -> None:
        assert EFFECTIVE_MARGIN_PCT.classification is Classification.TRADE_SECRET

    def test_consumer_map_non_empty(self) -> None:
        reg = rc_measure_registry()
        for name in reg.names():
            assert reg.get(name).consumer_map, f"{name} has no consumers"
