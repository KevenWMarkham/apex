"""Tests for rc-e2e-03-mcp tools (Sprint 32.7-32.9)."""

from __future__ import annotations

import pytest

from fabric_mcp import InMemoryFabricBackend, set_fabric_backend
from mcp_common import McpError, McpErrorCode
from rc_e2e_03_mcp import (
    CONTRACTS,
    commit_markdown_decision,
    get_excursion_decision_panel,
    get_pricing_recommendation_basis,
)
from rc_e2e_03_mcp.tools import _reset_committed_decisions_for_test


@pytest.fixture(autouse=True)
def _seed_fabric() -> InMemoryFabricBackend:
    """Seed the in-memory fabric backend with canonical RC-E2E-03 Gold mart rows."""
    _reset_committed_decisions_for_test()
    b = InMemoryFabricBackend(
        views={
            "rc_gold.g_excursion_decision_panel": [
                # Three SKUs in one excursion — matches the canonical fixture.
                {
                    "excursion_event_id": "EXC-001",
                    "store_id": "store-100",
                    "asset_id": "dairy-case-3",
                    "excursion_started_at": "2026-05-09T13:36:00Z",
                    "excursion_severity_factor": 0.55,
                    "time_since_last_event_seconds": 30,
                    "sku_key": "SKU-MILK-2PCT-1G",
                    "lot_key": "L-2026W18-DAIRY-A12",
                    "on_hand_qty": 84,
                    "unit_retail": 3.99,
                    "stock_days_remaining": 12.0,
                },
                {
                    "excursion_event_id": "EXC-001",
                    "store_id": "store-100",
                    "asset_id": "dairy-case-3",
                    "excursion_started_at": "2026-05-09T13:36:00Z",
                    "excursion_severity_factor": 0.55,
                    "time_since_last_event_seconds": 30,
                    "sku_key": "SKU-YOGURT-32OZ-PLAIN",
                    "lot_key": "L-2026W18-DAIRY-B07",
                    "on_hand_qty": 36,
                    "unit_retail": 5.49,
                    "stock_days_remaining": 7.5,
                },
            ],
            "rc_gold.g_pricing_recommendation_basis": [
                {
                    "sku_key": "SKU-MILK-2PCT-1G",
                    "location_key": "store-100",
                    "channel": "STORE",
                    "list_price": 3.99,
                    "floor_price": 2.50,
                    "map_price": None,
                    "target_margin_pct": 35.0,
                    "elasticity_coefficient": -1.4,
                    "elasticity_confidence_lower": -1.7,
                    "elasticity_confidence_upper": -1.1,
                    "competitor_observed_min_price": 3.79,
                    "matched_discount_rules": [
                        {"rule_natural": "DR-2026-Q2-DAIRY", "cap_pct": 40.0}
                    ],
                    "rule_min_cap_pct": 40.0,
                    "rule_min_margin_floor_pct": None,
                    "_classification": "trade_secret",
                },
            ],
        },
    )
    set_fabric_backend(b)
    return b


# --- get_excursion_decision_panel (32.7) -----------------------------------


def test_get_excursion_decision_panel_aggregates_lots() -> None:
    panel = get_excursion_decision_panel("EXC-001")
    assert panel["excursion_event_id"] == "EXC-001"
    assert panel["store_id"] == "store-100"
    assert panel["asset_id"] == "dairy-case-3"
    assert len(panel["affected_lots"]) == 2
    assert {lot["sku_key"] for lot in panel["affected_lots"]} == {
        "SKU-MILK-2PCT-1G", "SKU-YOGURT-32OZ-PLAIN",
    }


def test_get_excursion_decision_panel_missing_raises_not_found() -> None:
    with pytest.raises(McpError) as exc:
        get_excursion_decision_panel("NO-SUCH-EXCURSION")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_get_excursion_decision_panel_invalid_input_rejected() -> None:
    with pytest.raises(McpError) as exc:
        get_excursion_decision_panel("")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


# --- get_pricing_recommendation_basis (32.8) -------------------------------


def test_get_pricing_recommendation_basis_returns_trade_secret_payload() -> None:
    basis = get_pricing_recommendation_basis(
        "SKU-MILK-2PCT-1G", location_key="store-100", channel="STORE",
    )
    assert basis["floor_price"] == 2.50
    assert basis["elasticity_coefficient"] == -1.4
    assert basis["_classification"] == "trade_secret"


def test_get_pricing_recommendation_basis_unknown_channel_rejected() -> None:
    with pytest.raises(McpError) as exc:
        get_pricing_recommendation_basis("SKU-MILK-2PCT-1G", channel="GIFT_CARD")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_get_pricing_recommendation_basis_missing_sku_raises_not_found() -> None:
    with pytest.raises(McpError) as exc:
        get_pricing_recommendation_basis("SKU-DOES-NOT-EXIST")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_get_pricing_recommendation_basis_requires_sku() -> None:
    with pytest.raises(McpError) as exc:
        get_pricing_recommendation_basis("")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


# --- commit_markdown_decision (32.9) ---------------------------------------


def test_commit_markdown_decision_returns_canonical_envelope() -> None:
    out = commit_markdown_decision(
        decision_id="DEC-001",
        sku_natural="SKU-MILK-2PCT-1G",
        location_key="store-100",
        proposed_markdown_pct=30.0,
        proposed_price=2.79,
        operator_principal="marisol.reyes@labtenant.onmicrosoft.com",
        trace_id="trace-xyz-001",
    )
    assert out["decision_id"] == "DEC-001"
    assert out["merml_markdown_id"] == "merml-markdown-DEC-001"
    assert out["operator_principal"].startswith("marisol.reyes@")
    assert out["service_code"] == "RC-E2E-03"
    assert out["outcome"] == "ok"


def test_commit_markdown_decision_idempotent_on_decision_id() -> None:
    args = dict(
        decision_id="DEC-IDEM-001",
        sku_natural="SKU-MILK-2PCT-1G",
        location_key="store-100",
        proposed_markdown_pct=30.0,
        proposed_price=2.79,
        operator_principal="marisol.reyes@labtenant.onmicrosoft.com",
    )
    first = commit_markdown_decision(**args)  # type: ignore[arg-type]
    second = commit_markdown_decision(**args)  # type: ignore[arg-type]
    # Same merml_markdown_id, same applied_at — proves no second write.
    assert first["merml_markdown_id"] == second["merml_markdown_id"]
    assert first["applied_at"] == second["applied_at"]


def test_commit_markdown_decision_conflict_on_parameter_mismatch() -> None:
    base = dict(
        decision_id="DEC-CFL-001",
        sku_natural="SKU-MILK-2PCT-1G",
        location_key="store-100",
        operator_principal="marisol.reyes@labtenant.onmicrosoft.com",
    )
    commit_markdown_decision(  # type: ignore[arg-type]
        proposed_markdown_pct=30.0, proposed_price=2.79, **base,
    )
    with pytest.raises(McpError) as exc:
        commit_markdown_decision(  # type: ignore[arg-type]
            proposed_markdown_pct=35.0, proposed_price=2.59, **base,
        )
    assert exc.value.code is McpErrorCode.CONFLICT


def test_commit_markdown_decision_rejects_out_of_bound_markdown() -> None:
    with pytest.raises(McpError) as exc:
        commit_markdown_decision(
            decision_id="DEC-OOB",
            sku_natural="SKU-X",
            location_key="store-100",
            proposed_markdown_pct=150.0,  # > 100 invalid
            proposed_price=1.99,
            operator_principal="marisol.reyes@labtenant.onmicrosoft.com",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_commit_markdown_decision_rejects_negative_price() -> None:
    with pytest.raises(McpError) as exc:
        commit_markdown_decision(
            decision_id="DEC-NEG",
            sku_natural="SKU-X",
            location_key="store-100",
            proposed_markdown_pct=30.0,
            proposed_price=-0.01,
            operator_principal="marisol.reyes@labtenant.onmicrosoft.com",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_commit_markdown_decision_rejects_missing_operator_principal() -> None:
    with pytest.raises(McpError) as exc:
        commit_markdown_decision(
            decision_id="DEC-NOOP",
            sku_natural="SKU-X",
            location_key="store-100",
            proposed_markdown_pct=30.0,
            proposed_price=2.79,
            operator_principal="",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


# --- Contracts -------------------------------------------------------------


def test_contracts_declare_required_scopes() -> None:
    for c in CONTRACTS:
        assert "practice:rc" in c.required_scopes
        assert "service:rc-e2e-03" in c.required_scopes


def test_pricing_basis_contract_propagates_trade_secret() -> None:
    pricing_contract = next(
        c for c in CONTRACTS
        if c.name.endswith("get_pricing_recommendation_basis")
    )
    from apex_core.types import Classification
    assert Classification.TRADE_SECRET in pricing_contract.classification_propagation
