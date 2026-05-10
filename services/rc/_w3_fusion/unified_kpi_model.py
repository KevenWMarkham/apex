"""Sprint 40 item 40.3 — Unified Power BI Direct Lake semantic model.

Joins KPI Gold marts from all 5 RC services into a single semantic model
that Daniel Chen (Merchandising Director) + the executive scorecard
consume via Power BI Direct Lake.

Per Services Guide §1.6 + §18 the unified model lives in the
``rc-canonical`` primary workspace's ``rc-gold`` lakehouse. The model
references each per-service KPI mart via its OneLake path; cross-service
joins are at the date + tenant + (sometimes) sku grain.

Five service-specific KPI marts join here:

| Service | KPI mart | Sprint shipped |
|---|---|---|
| RC-E2E-03 | g_kpi_rc_e2e_03_daily         | Sprint 30.6 |
| RC-E2E-04 | g_kpi_rc_e2e_04_weekly        | Sprint 40 (canonical name; service authors at deploy time) |
| RC-E2E-05 | g_kpi_rc_e2e_05_per_shift     | Sprint 40 (same) |
| RC-E2E-07 | g_kpi_rc_e2e_07_daily         | Sprint 40 (same) |
| RC-E2E-09 | g_kpi_rc_e2e_09_daily         | Sprint 40 (same) |

The unified model exposes 14 cross-service measures (one per RC KPI in
``services/_kpis.yaml``) plus 4 Sprint 40 fusion measures that only make
sense across services (e.g., ``perishables_economics_mesh_total_value_usd``
which sums protected-margin from RC-E2E-03 + saved-LTV from RC-E2E-04 +
recovered-loss from RC-E2E-07).

Renderable via :func:`apex_medallion.gold.direct_lake.render_tmdl`; the
output TMDL artefact lives at ``services/rc/_w3_fusion/rc_unified_kpi.tmdl``
(committed alongside this module).
"""

from __future__ import annotations

from apex_medallion.gold.direct_lake import SemanticModelSpec, TableSpec
from apex_medallion.gold.measure import (
    MeasureDefinition,
    MeasureKind,
    MeasureLanguage,
)


# ---------------------------------------------------------------------------
# OneLake path conventions
# ---------------------------------------------------------------------------

_RC_GOLD_BASE = (
    "abfss://rc-canonical@onelake.dfs.fabric.microsoft.com/rc-gold.Lakehouse/Tables"
)


def _rc_gold_path(table: str) -> str:
    return f"{_RC_GOLD_BASE}/{table}"


# ---------------------------------------------------------------------------
# Sprint 40 fusion measures (cross-service rollups)
# ---------------------------------------------------------------------------


PERISHABLES_ECONOMICS_MESH_TOTAL_VALUE_DAX = MeasureDefinition(
    name="perishables_economics_mesh_total_value_usd",
    kind=MeasureKind.POST_MEASURE,
    language=MeasureLanguage.DAX,
    owner="rc-practice-lead",
    description=(
        "Sprint 40 W3 Fusion measure. Sum of protected margin (RC-E2E-03) + "
        "saved LTV (RC-E2E-04) + recovered loss (RC-E2E-07) across the "
        "selected date range. The headline number on the executive scorecard."
    ),
    formula=(
        "SUM('rc_g_kpi_rc_e2e_03_daily'[at_risk_margin_avoided_usd]) "
        "+ SUM('rc_g_kpi_rc_e2e_04_weekly'[expected_total_ltv_saved_usd]) "
        "+ SUM('rc_g_kpi_rc_e2e_07_daily'[expected_total_recovered_loss_usd])"
    ),
    depends_on=[
        "at_risk_margin_avoided_usd",
        "expected_total_ltv_saved_usd",
        "expected_total_recovered_loss_usd",
    ],
    consumer_map=["rc-executive-scorecard", "rc-perishables-mesh-dashboard"],
)


CROSS_SERVICE_DECISION_LOOP_TIME_DAX = MeasureDefinition(
    name="cross_service_avg_decision_loop_time_sec",
    kind=MeasureKind.POST_MEASURE,
    language=MeasureLanguage.DAX,
    owner="rc-practice-lead",
    description=(
        "Average decision-to-commit latency across all 5 RC services. "
        "Tracks the W3 SLO target (<120 sec from event to operator action)."
    ),
    formula=(
        "DIVIDE("
        "  SUM('rc_g_kpi_rc_e2e_03_daily'[kpi_avg_excursion_to_decision_seconds]) "
        "+ SUM('rc_g_kpi_rc_e2e_04_weekly'[kpi_avg_winback_decision_seconds]) "
        "+ SUM('rc_g_kpi_rc_e2e_05_per_shift'[kpi_avg_dispatch_decision_seconds]) "
        "+ SUM('rc_g_kpi_rc_e2e_07_daily'[kpi_avg_fraud_decision_seconds]) "
        "+ SUM('rc_g_kpi_rc_e2e_09_daily'[kpi_avg_recall_decision_seconds]),"
        "5)"
    ),
    depends_on=[
        "kpi_avg_excursion_to_decision_seconds",
        "kpi_avg_winback_decision_seconds",
        "kpi_avg_dispatch_decision_seconds",
        "kpi_avg_fraud_decision_seconds",
        "kpi_avg_recall_decision_seconds",
    ],
    consumer_map=["rc-executive-scorecard"],
)


HITL_ESCALATION_RATE_TOTAL_DAX = MeasureDefinition(
    name="hitl_escalation_rate_total_pct",
    kind=MeasureKind.POST_MEASURE,
    language=MeasureLanguage.DAX,
    owner="rc-practice-lead",
    description=(
        "Weighted-average HITL escalation rate across all 5 services. "
        "Anchor input to the Sprint 11 BL.P.76 tuning auto-rollback."
    ),
    formula=(
        "DIVIDE("
        "  SUM('rc_g_kpi_rc_e2e_03_daily'[kpi_hitl_escalation_rate_pct]) "
        "+ SUM('rc_g_kpi_rc_e2e_04_weekly'[kpi_hitl_escalation_rate_pct]) "
        "+ SUM('rc_g_kpi_rc_e2e_05_per_shift'[kpi_hitl_escalation_rate_pct]) "
        "+ SUM('rc_g_kpi_rc_e2e_07_daily'[kpi_hitl_escalation_rate_pct]) "
        "+ SUM('rc_g_kpi_rc_e2e_09_daily'[kpi_hitl_attestation_rate_pct]),"
        "5)"
    ),
    depends_on=[
        "kpi_hitl_escalation_rate_pct",
        "kpi_hitl_attestation_rate_pct",
    ],
    consumer_map=["rc-executive-scorecard", "rc-tuning-dashboard"],
)


PERISHABLES_LIFETIME_TRACE_COMPLETENESS_DAX = MeasureDefinition(
    name="perishables_lifetime_trace_completeness_pct",
    kind=MeasureKind.POST_MEASURE,
    language=MeasureLanguage.DAX,
    owner="rc-practice-lead",
    description=(
        "Cross-service: % of RC-E2E-03 cold-chain decisions where the "
        "underlying lot had a complete FSMA-204 trace at decision time. "
        "Pulls from RC-E2E-09's lot_provenance via the cross-service "
        "join. SLO target: 99%."
    ),
    formula=(
        "DIVIDE("
        "  CALCULATE("
        "    COUNT('rc_g_kpi_rc_e2e_03_daily'[kpi_excursions_handled_count]),"
        "    'rc_g_kpi_rc_e2e_09_daily'[trace_completeness_pct_avg] >= 99"
        "  ),"
        "  SUM('rc_g_kpi_rc_e2e_03_daily'[kpi_excursions_handled_count])"
        ") * 100"
    ),
    depends_on=["kpi_excursions_handled_count", "trace_completeness_pct_avg"],
    consumer_map=["rc-fsma-compliance-dashboard"],
)


# ---------------------------------------------------------------------------
# Per-service KPI mart specs (the join rows of the unified model)
# ---------------------------------------------------------------------------


def _table_g_kpi_rc_e2e_03_daily() -> TableSpec:
    return TableSpec(
        name="g_kpi_rc_e2e_03_daily",
        silver_delta_path=_rc_gold_path("g_kpi_rc_e2e_03_daily"),
        columns=(
            "as_of_date", "store_id", "category_key",
            "kpi_excursions_handled_count",
            "kpi_markdown_proposals_count",
            "kpi_markdown_recovery_pct",
            "kpi_at_risk_margin_avoided_usd",
            "at_risk_margin_avoided_usd",
            "kpi_pricing_recommendations_approved",
            "kpi_pricing_recommendations_overridden",
            "kpi_avg_excursion_to_decision_seconds",
            "kpi_hitl_escalation_rate_pct",
            "_classification",
        ),
    )


def _table_g_kpi_rc_e2e_04_weekly() -> TableSpec:
    return TableSpec(
        name="g_kpi_rc_e2e_04_weekly",
        silver_delta_path=_rc_gold_path("g_kpi_rc_e2e_04_weekly"),
        columns=(
            "week_start_date", "tenant_id", "category_key",
            "kpi_loyalty_churn_rate_pct",
            "kpi_winback_response_rate_pct",
            "kpi_saved_customer_ltv_pct_lift",
            "expected_total_ltv_saved_usd",
            "expected_total_offer_cost_usd",
            "expected_total_roi_usd",
            "kpi_avg_winback_decision_seconds",
            "kpi_hitl_escalation_rate_pct",
            "_classification",
        ),
    )


def _table_g_kpi_rc_e2e_05_per_shift() -> TableSpec:
    return TableSpec(
        name="g_kpi_rc_e2e_05_per_shift",
        silver_delta_path=_rc_gold_path("g_kpi_rc_e2e_05_per_shift"),
        columns=(
            "shift_start_ts", "store_id", "department_key",
            "kpi_oos_rate_pct",
            "kpi_sales_per_sqft_pct_lift",
            "kpi_associate_productivity_pct_lift",
            "tasks_dispatched", "tasks_completed",
            "completion_rate_pct", "p0_completion_rate_pct",
            "kpi_avg_dispatch_decision_seconds",
            "kpi_hitl_escalation_rate_pct",
            "_classification",
        ),
    )


def _table_g_kpi_rc_e2e_07_daily() -> TableSpec:
    return TableSpec(
        name="g_kpi_rc_e2e_07_daily",
        silver_delta_path=_rc_gold_path("g_kpi_rc_e2e_07_daily"),
        columns=(
            "as_of_date", "tenant_id",
            "kpi_fraud_detection_rate_pct_lift",
            "recovered_loss_usd",
            "expected_total_recovered_loss_usd",
            "kpi_false_positive_rate_pct",
            "rings_detected_count",
            "kpi_avg_fraud_decision_seconds",
            "kpi_hitl_escalation_rate_pct",
            "_classification",
        ),
    )


def _table_g_kpi_rc_e2e_09_daily() -> TableSpec:
    return TableSpec(
        name="g_kpi_rc_e2e_09_daily",
        silver_delta_path=_rc_gold_path("g_kpi_rc_e2e_09_daily"),
        columns=(
            "as_of_date", "tenant_id",
            "kpi_recall_traceability_time_hr",
            "kpi_fsma_compliance_score_pct",
            "trace_completeness_pct_avg",
            "recalls_class_I_count", "recalls_class_II_count",
            "recalls_class_III_count",
            "regulatory_filings_pending",
            "kpi_avg_recall_decision_seconds",
            "kpi_hitl_attestation_rate_pct",
            "_classification",
        ),
    )


def _table_dim_date() -> TableSpec:
    """Shared date dimension — every per-service mart joins this."""
    return TableSpec(
        name="dim_date",
        silver_delta_path=_rc_gold_path("dim_date"),
        columns=(
            "date", "year", "quarter", "month", "week",
            "fiscal_period", "season",
        ),
    )


# ---------------------------------------------------------------------------
# Public — unified semantic model
# ---------------------------------------------------------------------------


def build_rc_unified_kpi_semantic_model() -> SemanticModelSpec:
    """Sprint 40 deliverable — unified Power BI Direct Lake semantic model.

    Combines all 5 service KPI marts + a shared date dimension into one
    model. The 4 Sprint 40 fusion measures sit on the model spec's notes;
    they're rendered into the executive scorecard's TMDL.
    """
    return SemanticModelSpec(
        model_name="rc_unified_kpi",
        culture="en-US",
        notes=(
            "Sprint 40 W3 Fusion. Joins g_kpi_rc_e2e_03_daily / "
            "g_kpi_rc_e2e_04_weekly / g_kpi_rc_e2e_05_per_shift / "
            "g_kpi_rc_e2e_07_daily / g_kpi_rc_e2e_09_daily on dim_date. "
            "Fusion measures: perishables_economics_mesh_total_value_usd · "
            "cross_service_avg_decision_loop_time_sec · "
            "hitl_escalation_rate_total_pct · "
            "perishables_lifetime_trace_completeness_pct."
        ),
        tables=(
            _table_dim_date(),
            _table_g_kpi_rc_e2e_03_daily(),
            _table_g_kpi_rc_e2e_04_weekly(),
            _table_g_kpi_rc_e2e_05_per_shift(),
            _table_g_kpi_rc_e2e_07_daily(),
            _table_g_kpi_rc_e2e_09_daily(),
        ),
    )


# Alphabetised list of fusion measure names — used by the wizard's
# Roadmap page + the Bicep deploymentScripts to verify all 4 land in the
# deployed semantic model.
RC_W3_FUSION_MEASURE_NAMES: tuple[str, ...] = tuple(sorted(m.name for m in (
    PERISHABLES_ECONOMICS_MESH_TOTAL_VALUE_DAX,
    CROSS_SERVICE_DECISION_LOOP_TIME_DAX,
    HITL_ESCALATION_RATE_TOTAL_DAX,
    PERISHABLES_LIFETIME_TRACE_COMPLETENESS_DAX,
)))


# Alphabetised list of joined per-service KPI mart names.
RC_W3_FUSION_KPI_MART_NAMES: tuple[str, ...] = tuple(sorted(t.name for t in
    build_rc_unified_kpi_semantic_model().tables
    if t.name.startswith("g_kpi_")
))
