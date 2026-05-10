"""Smoke tests for the RC-E2E-03 Gold mart spec.

Sprint 30 item 30.6. Validates the spec is constructable + renderable; deeper
data-correctness lives in the Sprint 33 smoke test against Lab data.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow the test file to import its sibling marts module without packaging it.
sys.path.insert(0, str(Path(__file__).parent))

from apex_medallion.gold.direct_lake import render_tmdl

from marts import (  # type: ignore[import-not-found]  # noqa: E402
    RC_E2E_03_GOLD_MART_NAMES,
    build_rc_e2e_03_semantic_model,
)


def test_six_marts() -> None:
    spec = build_rc_e2e_03_semantic_model()
    assert len(spec.tables) == 6


def test_mart_names_match_sprint_30_6() -> None:
    """Per services/rc/_build-status.yaml item 30.6 + Roadmap.md."""
    expected = {
        "g_excursion_decision_panel",
        "g_markdown_proposal_basis",
        "g_pricing_recommendation_basis",
        "g_inventory_position_current",
        "g_kpi_rc_e2e_03_daily",
        "g_markdown_outcome_attribution",
    }
    assert set(RC_E2E_03_GOLD_MART_NAMES) == expected


def test_every_mart_has_silver_delta_path() -> None:
    spec = build_rc_e2e_03_semantic_model()
    for table in spec.tables:
        assert table.silver_delta_path.startswith("abfss://rc-canonical@")
        assert "rc-gold.Lakehouse/Tables/" in table.silver_delta_path
        assert table.silver_delta_path.endswith(table.name)


def test_pricing_recommendation_basis_has_trade_secret_columns() -> None:
    spec = build_rc_e2e_03_semantic_model()
    pricing_mart = next(t for t in spec.tables if t.name == "g_pricing_recommendation_basis")
    # Floor / MAP / target margin / elasticity coefficients are TRADE_SECRET in
    # PROML / MERML; the mart projects them.
    cols = set(pricing_mart.columns)
    assert {"floor_price", "map_price", "target_margin_pct", "elasticity_coefficient"} <= cols


def test_render_tmdl_round_trip() -> None:
    spec = build_rc_e2e_03_semantic_model()
    body = render_tmdl(spec)
    assert "model rc_e2e_03_pricing_revenue" in body
    # Every mart appears in the rendered TMDL.
    for name in RC_E2E_03_GOLD_MART_NAMES:
        assert f"table {name}" in body
