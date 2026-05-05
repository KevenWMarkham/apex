"""RC anchor measure library — pre- and post-measures for the RC Practice.

Registered into a :class:`MeasureRegistry` so notebooks + Gold view generators
pull from a single governed source. Other Practices follow the same pattern
in later sprints.
"""

from __future__ import annotations

from apex_core.types import Classification
from apex_medallion.gold.measure import (
    MeasureDefinition,
    MeasureKind,
    MeasureLanguage,
    MeasureRegistry,
)

# --- Pre-measures (Silver → Gold, PySpark) ----------------------------------

EFFECTIVE_MARGIN_PCT = MeasureDefinition(
    name="effective_margin_pct",
    kind=MeasureKind.PRE_MEASURE,
    language=MeasureLanguage.PYSPARK,
    owner="rc-practice-lead",
    description=(
        "Effective gross margin as a percentage of retail. "
        "((unit_retail - unit_cost) / unit_retail) * 100"
    ),
    classification=Classification.TRADE_SECRET,
    formula="((F.col('unit_retail') - F.col('unit_cost')) / F.col('unit_retail')) * F.lit(100)",
    depends_on=["unit_retail", "unit_cost"],
    consumer_map=["rc-markdown-agent", "rc-assortment-agent"],
)

STOCK_DAYS_REMAINING = MeasureDefinition(
    name="stock_days_remaining",
    kind=MeasureKind.PRE_MEASURE,
    language=MeasureLanguage.PYSPARK,
    owner="rc-practice-lead",
    description=(
        "Expected days until current on-hand inventory is exhausted at the "
        "trailing 14-day average daily demand. NULL when avg_daily_demand = 0."
    ),
    formula=(
        "F.when(F.col('avg_daily_demand') > 0, "
        "F.col('on_hand_qty') / F.col('avg_daily_demand')).otherwise(F.lit(None))"
    ),
    depends_on=["on_hand_qty", "avg_daily_demand"],
    consumer_map=["rc-replenishment-agent", "rc-cold-chain-agent"],
)

TIME_SINCE_LAST_EVENT_SECONDS = MeasureDefinition(
    name="time_since_last_event_seconds",
    kind=MeasureKind.PRE_MEASURE,
    language=MeasureLanguage.PYSPARK,
    owner="rc-practice-lead",
    description=(
        "Seconds between the current snapshot and the most-recent event_ts "
        "for this entity. Enables 'stale data' gating in agent prompts."
    ),
    formula=(
        "F.unix_timestamp(F.current_timestamp()) "
        "- F.unix_timestamp(F.col('last_event_ts'))"
    ),
    depends_on=["last_event_ts"],
    consumer_map=["rc-cold-chain-agent"],
)


# --- Post-measures (Gold query-time) ----------------------------------------

PERIOD_OVER_PERIOD_PCT_DAX = MeasureDefinition(
    name="period_over_period_pct",
    kind=MeasureKind.POST_MEASURE,
    language=MeasureLanguage.DAX,
    owner="rc-practice-lead",
    description="(current - prior_month) / prior_month * 100",
    formula=(
        "VAR _cur = [base_metric] "
        "VAR _prior = CALCULATE([base_metric], DATEADD('Date'[Date], -1, MONTH)) "
        "RETURN DIVIDE(_cur - _prior, _prior) * 100"
    ),
    depends_on=["base_metric"],
    consumer_map=["rc-store-dashboard"],
)

ROLLING_AVG_14_DAY_TSQL = MeasureDefinition(
    name="rolling_avg_14_day",
    kind=MeasureKind.POST_MEASURE,
    language=MeasureLanguage.TSQL,
    owner="rc-practice-lead",
    description="14-day rolling average of base_metric.",
    formula=(
        "AVG(base_metric) OVER ("
        "ORDER BY event_date "
        "ROWS BETWEEN 13 PRECEDING AND CURRENT ROW)"
    ),
    depends_on=["base_metric", "event_date"],
    consumer_map=["rc-demand-agent"],
)

RECENT_EVENTS_KQL = MeasureDefinition(
    name="events_last_15_min",
    kind=MeasureKind.POST_MEASURE,
    language=MeasureLanguage.KQL,
    owner="rc-practice-lead",
    description="Count of matching events in the trailing 15 minutes.",
    formula="count() by bin(event_ts, 15m)",
    depends_on=["event_ts"],
    consumer_map=["rc-cold-chain-agent"],
)


# --- Registry ---------------------------------------------------------------


def rc_measure_registry() -> MeasureRegistry:
    """Return a fresh registry populated with RC anchor measures."""
    reg = MeasureRegistry()
    reg.register_many([
        EFFECTIVE_MARGIN_PCT,
        STOCK_DAYS_REMAINING,
        TIME_SINCE_LAST_EVENT_SECONDS,
        PERIOD_OVER_PERIOD_PCT_DAX,
        ROLLING_AVG_14_DAY_TSQL,
        RECENT_EVENTS_KQL,
    ])
    return reg
