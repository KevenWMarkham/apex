"""Tests for the Sprint 40 unified KPI semantic model + Perishables Mesh use case."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

# Allow the test to import the sibling unified_kpi_model module without
# packaging it (pattern matches services/rc/RC-E2E-03/_gold/test_marts.py).
sys.path.insert(0, str(Path(__file__).parent))

from apex_medallion.gold.direct_lake import render_tmdl

from unified_kpi_model import (  # type: ignore[import-not-found]  # noqa: E402
    CROSS_SERVICE_DECISION_LOOP_TIME_DAX,
    HITL_ESCALATION_RATE_TOTAL_DAX,
    PERISHABLES_ECONOMICS_MESH_TOTAL_VALUE_DAX,
    PERISHABLES_LIFETIME_TRACE_COMPLETENESS_DAX,
    RC_W3_FUSION_KPI_MART_NAMES,
    RC_W3_FUSION_MEASURE_NAMES,
    build_rc_unified_kpi_semantic_model,
)


# ---------------------------------------------------------------------------
# Unified KPI semantic model — joins all 5 RC services
# ---------------------------------------------------------------------------


def test_six_tables_dim_date_plus_5_kpi_marts() -> None:
    spec = build_rc_unified_kpi_semantic_model()
    # 1 dim_date + 5 service KPI marts
    assert len(spec.tables) == 6


def test_kpi_mart_names_cover_all_5_rc_services() -> None:
    """Sprint 40 — unified model must join all 5 featured RC services."""
    expected = {
        "g_kpi_rc_e2e_03_daily",
        "g_kpi_rc_e2e_04_weekly",
        "g_kpi_rc_e2e_05_per_shift",
        "g_kpi_rc_e2e_07_daily",
        "g_kpi_rc_e2e_09_daily",
    }
    assert set(RC_W3_FUSION_KPI_MART_NAMES) == expected


def test_dim_date_present_for_cross_service_join() -> None:
    spec = build_rc_unified_kpi_semantic_model()
    table_names = {t.name for t in spec.tables}
    assert "dim_date" in table_names


def test_each_kpi_mart_lives_in_rc_canonical_workspace() -> None:
    spec = build_rc_unified_kpi_semantic_model()
    for table in spec.tables:
        if table.name.startswith("g_kpi_"):
            assert "rc-canonical" in table.silver_delta_path
            assert "rc-gold.Lakehouse/Tables/" in table.silver_delta_path


# ---------------------------------------------------------------------------
# Sprint 40 fusion measures
# ---------------------------------------------------------------------------


def test_four_fusion_measures_authored() -> None:
    """Sprint 40.3 — 4 cross-service rollup measures."""
    expected = {
        "perishables_economics_mesh_total_value_usd",
        "cross_service_avg_decision_loop_time_sec",
        "hitl_escalation_rate_total_pct",
        "perishables_lifetime_trace_completeness_pct",
    }
    assert set(RC_W3_FUSION_MEASURE_NAMES) == expected


def test_perishables_mesh_total_sums_three_services() -> None:
    """The headline executive metric — RC-E2E-03 + 04 + 07 contributions."""
    f = PERISHABLES_ECONOMICS_MESH_TOTAL_VALUE_DAX.formula
    assert "rc_g_kpi_rc_e2e_03_daily" in f
    assert "rc_g_kpi_rc_e2e_04_weekly" in f
    assert "rc_g_kpi_rc_e2e_07_daily" in f


def test_decision_loop_time_avg_covers_all_5_services() -> None:
    """Cross-service KPI — must include all 5 marts."""
    f = CROSS_SERVICE_DECISION_LOOP_TIME_DAX.formula
    for service in ("03_daily", "04_weekly", "05_per_shift", "07_daily", "09_daily"):
        assert service in f


def test_trace_completeness_joins_RC_E2E_09() -> None:
    """The fusion KPI that proves cross-service joins work end-to-end."""
    f = PERISHABLES_LIFETIME_TRACE_COMPLETENESS_DAX.formula
    assert "rc_g_kpi_rc_e2e_03_daily" in f
    assert "rc_g_kpi_rc_e2e_09_daily" in f


def test_render_tmdl_includes_all_5_services() -> None:
    """The TMDL artefact must reference every service KPI mart."""
    spec = build_rc_unified_kpi_semantic_model()
    body = render_tmdl(spec)
    assert "model rc_unified_kpi" in body
    for mart in RC_W3_FUSION_KPI_MART_NAMES:
        assert f"table {mart}" in body


# ---------------------------------------------------------------------------
# Perishables Economics Mesh use-case YAML — concrete W3 fusion example
# ---------------------------------------------------------------------------

PERISHABLES_MESH_YAML = (
    Path(__file__).parent / "perishables-economics-mesh.yaml"
)


def test_perishables_mesh_use_case_yaml_loads() -> None:
    data = yaml.safe_load(PERISHABLES_MESH_YAML.read_text(encoding="utf-8"))
    assert data["use_case_id"] == "rc-w3-fusion--perishables-economics-mesh"
    assert data["fusion_use_case"] is True


def test_perishables_mesh_composes_three_services() -> None:
    """The headline fusion: RC-E2E-03 × RC-E2E-04 × RC-E2E-09."""
    data = yaml.safe_load(PERISHABLES_MESH_YAML.read_text(encoding="utf-8"))
    components = {c["service_code"] for c in data["component_services"]}
    assert components == {"RC-E2E-03", "RC-E2E-04", "RC-E2E-09"}


def test_perishables_mesh_declares_4_fusion_edges() -> None:
    """Sprint 40 fusion edges: 1 signal_fanout + 2 cache_invalidation + 1 ledger_aggregation."""
    data = yaml.safe_load(PERISHABLES_MESH_YAML.read_text(encoding="utf-8"))
    edges = data["fusion_edges"]
    kinds = {e["kind"] for e in edges}
    assert "signal_fanout" in kinds
    assert "cache_invalidation" in kinds
    assert "ledger_aggregation" in kinds
    # Must cover at least 4 distinct fusion-edge ids
    assert len({e["id"] for e in edges}) >= 4


def test_perishables_mesh_uses_w3_blueprint() -> None:
    """Deploys via apex-m/infra/bicep/blueprints/w3-scale-fuse.bicep."""
    data = yaml.safe_load(PERISHABLES_MESH_YAML.read_text(encoding="utf-8"))
    assert data["deployment"]["wave"] == "w3"
    assert "w3-scale-fuse.bicep" in data["deployment"]["blueprint"]


def test_perishables_mesh_kpis_align_with_fusion_measures() -> None:
    """Use-case kpis_targeted reference the unified semantic model fusion measures."""
    data = yaml.safe_load(PERISHABLES_MESH_YAML.read_text(encoding="utf-8"))
    kpi_ids = {k["id"] for k in data["kpis_targeted"]}
    # Each fusion measure has a corresponding kpi_id in kebab-case
    assert "perishables-economics-mesh-total-value-usd" in kpi_ids
    assert "cross-service-avg-decision-loop-time-sec" in kpi_ids
    assert "perishables-lifetime-trace-completeness-pct" in kpi_ids


def test_perishables_mesh_smoke_tests_cover_3_fusion_edge_kinds() -> None:
    """Each smoke test exercises one fusion edge kind end-to-end."""
    data = yaml.safe_load(PERISHABLES_MESH_YAML.read_text(encoding="utf-8"))
    smoke_ids = [s["id"] for s in data["smoke_tests"]]
    assert "smoke-cold-chain-to-loyalty-signal" in smoke_ids
    assert "smoke-lot-recall-cascades-to-cold-chain" in smoke_ids
    assert "smoke-pricer-reads-fusion-ledger" in smoke_ids


def test_perishables_mesh_audit_chain_emits_fusion_edge_audit_row() -> None:
    """Per BL.P.86 lineage — fusion-edge fires emit their own audit row."""
    data = yaml.safe_load(PERISHABLES_MESH_YAML.read_text(encoding="utf-8"))
    audit = data["audit_chain"]
    assert audit["emit_fusion_edge_audit_row"] is True
    assert audit["ledger_unified_table"] == "rc_ledger_unified"


def test_perishables_mesh_commercial_alignment_90_day_window() -> None:
    """Sprint 48 — 3-month margin-attribution shadow window declared."""
    data = yaml.safe_load(PERISHABLES_MESH_YAML.read_text(encoding="utf-8"))
    commercial = data["commercial_alignment"]
    assert commercial["outcome_attribution_window_days"] == 90
    assert commercial["primary_review_persona"] == "daniel-chen-merch-director"
