"""RC-E2E-03 Gold mart specifications — Sprint 30 item 30.6.

Six Gold marts that the RC-E2E-03 Pricing & Revenue Decision Service consumes:

1. ``g_excursion_decision_panel``      — primary cold-chain MCP read (Direct Lake)
2. ``g_markdown_proposal_basis``       — Markdown Agent input (Direct Lake)
3. ``g_pricing_recommendation_basis``  — The Pricer input (Direct Lake)
4. ``g_inventory_position_current``    — Demand Checker input (Direct Lake)
5. ``g_kpi_rc_e2e_03_daily``           — KPI Power BI dashboard (Direct Lake)
6. ``g_markdown_outcome_attribution``  — outcome attribution (Direct Lake + KQL)

Per Services Guide §1.6 + §18.1, all six land inside the
``rc-canonical`` primary workspace's ``rc-gold`` lakehouse. Direct Lake
connections from the consumer workspaces (rc-e2e-03-pricing) read these
through the OneLake security model (user identity mode).

The semantic-model spec returned by :func:`build_rc_e2e_03_semantic_model`
is renderable via :func:`apex_medallion.gold.direct_lake.render_tmdl`.
"""

from __future__ import annotations

from apex_medallion.gold.direct_lake import SemanticModelSpec, TableSpec
from apex_medallion.gold.measure import (
    MeasureDefinition,
    MeasureKind,
    MeasureLanguage,
)
from apex_medallion.gold.rc_measures import (
    EFFECTIVE_MARGIN_PCT,
    PERIOD_OVER_PERIOD_PCT_DAX,
    RECENT_EVENTS_KQL,
    ROLLING_AVG_14_DAY_TSQL,
    STOCK_DAYS_REMAINING,
    TIME_SINCE_LAST_EVENT_SECONDS,
)


# --- RC-E2E-03 mart-specific measures (extend the framework rc_measures) ----

EXCURSION_AT_RISK_MARGIN_USD = MeasureDefinition(
    name="excursion_at_risk_margin_usd",
    kind=MeasureKind.PRE_MEASURE,
    language=MeasureLanguage.PYSPARK,
    owner="rc-e2e-03-pricing-lead",
    description=(
        "Margin-at-risk USD if the cold-chain excursion spoils on-hand inventory. "
        "Computed Silver->Gold for the excursion-decision panel."
    ),
    formula=(
        "F.col('on_hand_qty') * (F.col('unit_retail') - F.col('unit_cost')) "
        "* F.col('excursion_severity_factor')"
    ),
    depends_on=["on_hand_qty", "unit_retail", "unit_cost", "excursion_severity_factor"],
    consumer_map=["rc-e2e-03-cold-chain-agent", "rc-e2e-03-pricing-agent"],
)

MARKDOWN_RECOVERY_PCT_DAX = MeasureDefinition(
    name="markdown_recovery_pct",
    kind=MeasureKind.POST_MEASURE,
    language=MeasureLanguage.DAX,
    owner="rc-e2e-03-pricing-lead",
    description="Percent of original-margin recovered after a markdown was applied.",
    formula=(
        "DIVIDE("
        "SUM('rc_g_markdown_outcome_attribution'[recovered_margin_usd]),"
        "SUM('rc_g_markdown_outcome_attribution'[original_margin_usd])"
        ") * 100"
    ),
    depends_on=["recovered_margin_usd", "original_margin_usd"],
    consumer_map=["rc-e2e-03-power-bi-dashboard"],
)


# --- The six marts ----------------------------------------------------------


def _table_g_excursion_decision_panel() -> TableSpec:
    """Mart 1 — primary cold-chain MCP read."""
    return TableSpec(
        name="g_excursion_decision_panel",
        silver_delta_path="abfss://rc-canonical@onelake.dfs.fabric.microsoft.com/rc-gold.Lakehouse/Tables/g_excursion_decision_panel",
        columns=(
            "excursion_event_id",
            "store_id",
            "asset_id",
            "sku_key",
            "lot_key",
            "excursion_started_at",
            "excursion_severity_factor",
            "on_hand_qty",
            "unit_retail",
            "unit_cost_token",
            "excursion_at_risk_margin_usd",
            "stock_days_remaining",
            "time_since_last_event_seconds",
            "_classification",
        ),
        measures=(
            EXCURSION_AT_RISK_MARGIN_USD,
            STOCK_DAYS_REMAINING,
            TIME_SINCE_LAST_EVENT_SECONDS,
        ),
    )


def _table_g_markdown_proposal_basis() -> TableSpec:
    """Mart 2 — Markdown Agent input."""
    return TableSpec(
        name="g_markdown_proposal_basis",
        silver_delta_path="abfss://rc-canonical@onelake.dfs.fabric.microsoft.com/rc-gold.Lakehouse/Tables/g_markdown_proposal_basis",
        columns=(
            "sku_key",
            "location_key",
            "current_list_price",
            "current_floor_price",
            "current_map_price",
            "elasticity_coefficient",
            "competitor_min_observed_price",
            "competitor_match_confidence",
            "stock_days_remaining",
            "expected_recovery_pct",
            "effective_margin_pct",
            "_classification",
        ),
        measures=(EFFECTIVE_MARGIN_PCT, STOCK_DAYS_REMAINING),
    )


def _table_g_pricing_recommendation_basis() -> TableSpec:
    """Mart 3 — The Pricer input (TRADE_SECRET-heavy)."""
    return TableSpec(
        name="g_pricing_recommendation_basis",
        silver_delta_path="abfss://rc-canonical@onelake.dfs.fabric.microsoft.com/rc-gold.Lakehouse/Tables/g_pricing_recommendation_basis",
        columns=(
            "sku_key",
            "location_key",
            "channel",
            "list_price",
            "floor_price",
            "map_price",
            "target_margin_pct",
            "elasticity_coefficient",
            "elasticity_confidence_lower",
            "elasticity_confidence_upper",
            "competitor_observed_min_price",
            "competitor_observed_at",
            "matched_discount_rules",
            "rule_min_cap_pct",
            "rule_min_margin_floor_pct",
            "_classification",
        ),
        measures=(EFFECTIVE_MARGIN_PCT,),
    )


def _table_g_inventory_position_current() -> TableSpec:
    """Mart 4 — Demand Checker / Operations Lead input."""
    return TableSpec(
        name="g_inventory_position_current",
        silver_delta_path="abfss://rc-canonical@onelake.dfs.fabric.microsoft.com/rc-gold.Lakehouse/Tables/g_inventory_position_current",
        columns=(
            "sku_key",
            "location_key",
            "lot_key",
            "snapshot_at",
            "on_hand_qty",
            "reserved_qty",
            "in_transit_qty",
            "avg_daily_demand",
            "stock_days_remaining",
            "_classification",
        ),
        measures=(STOCK_DAYS_REMAINING,),
    )


def _table_g_kpi_rc_e2e_03_daily() -> TableSpec:
    """Mart 5 — daily KPI rollup for the Power BI dashboard."""
    return TableSpec(
        name="g_kpi_rc_e2e_03_daily",
        silver_delta_path="abfss://rc-canonical@onelake.dfs.fabric.microsoft.com/rc-gold.Lakehouse/Tables/g_kpi_rc_e2e_03_daily",
        columns=(
            "as_of_date",
            "store_id",
            "category_key",
            "kpi_excursions_handled_count",
            "kpi_markdown_proposals_count",
            "kpi_markdown_recovery_pct",
            "kpi_at_risk_margin_avoided_usd",
            "kpi_pricing_recommendations_approved",
            "kpi_pricing_recommendations_overridden",
            "kpi_avg_excursion_to_decision_seconds",
            "kpi_hitl_escalation_rate_pct",
            "_classification",
        ),
        measures=(
            PERIOD_OVER_PERIOD_PCT_DAX,
            ROLLING_AVG_14_DAY_TSQL,
            MARKDOWN_RECOVERY_PCT_DAX,
        ),
    )


def _table_g_markdown_outcome_attribution() -> TableSpec:
    """Mart 6 — markdown outcome attribution for LEDGER feedback (Sprint 40)."""
    return TableSpec(
        name="g_markdown_outcome_attribution",
        silver_delta_path="abfss://rc-canonical@onelake.dfs.fabric.microsoft.com/rc-gold.Lakehouse/Tables/g_markdown_outcome_attribution",
        columns=(
            "decision_id",
            "trace_id",
            "sku_key",
            "location_key",
            "applied_at",
            "applied_markdown_pct",
            "expected_recovery_pct",
            "actual_recovery_pct",
            "original_margin_usd",
            "recovered_margin_usd",
            "outcome_window_days",
            "decision_agent_id",
            "_classification",
        ),
        # KQL recent-events post-measure also valid here for live-dashboard
        # filtering on recently-attributed decisions.
        measures=(RECENT_EVENTS_KQL,),
    )


# --- Public ----------------------------------------------------------------


def build_rc_e2e_03_semantic_model() -> SemanticModelSpec:
    """Return the canonical Direct Lake semantic-model spec for RC-E2E-03.

    Six tables × measures from ``rc_measures`` + the two RC-E2E-03 specifics.
    Render with ``apex_medallion.gold.direct_lake.render_tmdl(spec)``.
    """
    return SemanticModelSpec(
        model_name="rc_e2e_03_pricing_revenue",
        culture="en-US",
        notes=(
            "RC-E2E-03 Pricing & Revenue Decision Service. Six Gold marts feeding "
            "The Pricer + Markdown Agent + Operations Lead HITL Adaptive Cards + "
            "Daniel Chen's KPI dashboard. Sprint 30.6."
        ),
        tables=(
            _table_g_excursion_decision_panel(),
            _table_g_markdown_proposal_basis(),
            _table_g_pricing_recommendation_basis(),
            _table_g_inventory_position_current(),
            _table_g_kpi_rc_e2e_03_daily(),
            _table_g_markdown_outcome_attribution(),
        ),
    )


# Alphabetised list of mart names — used by the wizard's TreeView + the
# Bicep `agents.bicep` Foundry-RAG attachments.
RC_E2E_03_GOLD_MART_NAMES: tuple[str, ...] = tuple(
    sorted(t.name for t in build_rc_e2e_03_semantic_model().tables)
)
