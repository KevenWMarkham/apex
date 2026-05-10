"""Tests for rc-e2e-04-mcp tools (Sprint 34)."""

from __future__ import annotations

import pytest

from apex_core.types import Classification
from fabric_mcp import InMemoryFabricBackend, set_fabric_backend
from mcp_common import McpError, McpErrorCode
from rc_e2e_04_mcp import (
    CONTRACTS,
    commit_winback_offer,
    get_loyalty_churn_cohort,
    get_winback_offer_basis,
)
from rc_e2e_04_mcp.tools import _reset_committed_campaigns_for_test


@pytest.fixture(autouse=True)
def _seed_fabric() -> InMemoryFabricBackend:
    _reset_committed_campaigns_for_test()
    b = InMemoryFabricBackend(
        views={
            "rc_gold.g_loyalty_churn_cohort": [
                {
                    "customer_token": "tok-cust-A",
                    "loyalty_tier": "platinum",
                    "lifetime_value_bucket": "high",
                    "trailing_90d_visit_count": 4,
                    "trailing_90d_visit_count_prior_period": 12,
                    "visit_velocity_change_pct": -67.0,
                    "trailing_90d_revenue_token": "tok-rev-A",
                    "service_interactions_negative_count": 3,
                    "tier_filter": "top_tier",
                },
                {
                    "customer_token": "tok-cust-B",
                    "loyalty_tier": "gold",
                    "lifetime_value_bucket": "mid",
                    "trailing_90d_visit_count": 8,
                    "trailing_90d_visit_count_prior_period": 10,
                    "visit_velocity_change_pct": -20.0,
                    "trailing_90d_revenue_token": "tok-rev-B",
                    "service_interactions_negative_count": 1,
                    "tier_filter": "top_tier",
                },
            ],
            "rc_gold.g_winback_offer_basis": [
                {
                    "customer_token": "tok-cust-A",
                    "predicted_ltv_decline_24m_usd": 1820.00,
                    "response_elasticity_curve": {
                        "5": 4.2, "10": 7.5, "15": 11.0, "20": 14.5,
                        "25": 18.5, "30": 22.0, "40": 27.0, "50": 30.5,
                    },
                    "matched_offer_rules": [
                        {
                            "rule_natural": "WB-2026-PLAT-CAP",
                            "max_offer_pct": 35.0,
                            "margin_floor_pct": 18.0,
                        }
                    ],
                    "consent_personalization": True,
                    "consent_marketing": True,
                    "elasticity_model_version": "wb-elast-v3.4",
                    "_classification": "trade_secret",
                },
            ],
        },
    )
    set_fabric_backend(b)
    return b


# --- get_loyalty_churn_cohort ----------------------------------------------


def test_get_loyalty_churn_cohort_returns_tokenised_members() -> None:
    cohort = get_loyalty_churn_cohort(
        window_start="2026-05-04T00:00:00Z",
        window_end="2026-05-11T00:00:00Z",
        tier_filter="top_tier",
    )
    assert cohort["cohort_size"] == 2
    assert cohort["tier_filter"] == "top_tier"
    # PII fields are tokenised
    for m in cohort["members"]:
        assert m["customer_token"].startswith("tok-cust-")
        assert m["trailing_90d_revenue_token"].startswith("tok-rev-")


def test_get_loyalty_churn_cohort_unknown_tier_rejected() -> None:
    with pytest.raises(McpError) as exc:
        get_loyalty_churn_cohort(
            window_start="2026-05-04T00:00:00Z",
            window_end="2026-05-11T00:00:00Z",
            tier_filter="diamond",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_get_loyalty_churn_cohort_inverted_window_rejected() -> None:
    with pytest.raises(McpError) as exc:
        get_loyalty_churn_cohort(
            window_start="2026-05-11T00:00:00Z",
            window_end="2026-05-04T00:00:00Z",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_get_loyalty_churn_cohort_malformed_timestamp_rejected() -> None:
    with pytest.raises(McpError) as exc:
        get_loyalty_churn_cohort(
            window_start="not-a-date",
            window_end="2026-05-11T00:00:00Z",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


# --- get_winback_offer_basis -----------------------------------------------


def test_get_winback_offer_basis_returns_trade_secret() -> None:
    basis = get_winback_offer_basis(
        customer_token="tok-cust-A",
        cohort_window_start="2026-05-04T00:00:00Z",
        cohort_window_end="2026-05-11T00:00:00Z",
    )
    assert basis["customer_token"] == "tok-cust-A"
    assert basis["predicted_ltv_decline_24m_usd"] == 1820.00
    assert basis["matched_offer_rules"][0]["max_offer_pct"] == 35.0
    assert basis["_classification"] == "trade_secret"


def test_get_winback_offer_basis_missing_customer_raises_not_found() -> None:
    with pytest.raises(McpError) as exc:
        get_winback_offer_basis(
            customer_token="tok-no-such-customer",
            cohort_window_start="2026-05-04T00:00:00Z",
            cohort_window_end="2026-05-11T00:00:00Z",
        )
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_get_winback_offer_basis_requires_token() -> None:
    with pytest.raises(McpError) as exc:
        get_winback_offer_basis(
            customer_token="",
            cohort_window_start="2026-05-04T00:00:00Z",
            cohort_window_end="2026-05-11T00:00:00Z",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


# --- commit_winback_offer --------------------------------------------------


def _make_offers() -> list[dict]:
    return [
        {"customer_token": "tok-cust-A", "offer_kind": "percent_off",
         "offer_depth_pct": 25.0, "offer_amount_usd": None},
        {"customer_token": "tok-cust-B", "offer_kind": "bonus_points",
         "offer_depth_pct": None, "offer_amount_usd": 5.0},
    ]


def test_commit_winback_offer_returns_canonical_envelope() -> None:
    out = commit_winback_offer(
        campaign_natural="WB-2026W19-TOPTIER",
        cohort_window_start="2026-05-04T00:00:00Z",
        cohort_window_end="2026-05-11T00:00:00Z",
        approved_member_offers=_make_offers(),
        operator_principal="maya.patel@labtenant.onmicrosoft.com",
        tier3_pii_unlock_request_id="unlock-req-aaa-001",
        trace_id="trace-rc-e2e-04-001",
    )
    assert out["campaign_natural"] == "WB-2026W19-TOPTIER"
    assert out["cxml_campaign_id"] == "cxml-campaign-WB-2026W19-TOPTIER"
    assert out["approved_count"] == 2
    assert out["service_code"] == "RC-E2E-04"
    assert out["tier3_pii_unlock_request_id"] == "unlock-req-aaa-001"
    assert out["outcome"] == "ok"


def test_commit_winback_offer_idempotent_on_campaign_natural() -> None:
    args = dict(
        campaign_natural="WB-IDEM-001",
        cohort_window_start="2026-05-04T00:00:00Z",
        cohort_window_end="2026-05-11T00:00:00Z",
        approved_member_offers=_make_offers(),
        operator_principal="maya.patel@labtenant.onmicrosoft.com",
        tier3_pii_unlock_request_id="unlock-req-idem-001",
    )
    first = commit_winback_offer(**args)  # type: ignore[arg-type]
    second = commit_winback_offer(**args)  # type: ignore[arg-type]
    assert first["cxml_campaign_id"] == second["cxml_campaign_id"]
    assert first["applied_at"] == second["applied_at"]


def test_commit_winback_offer_conflict_on_cohort_mismatch() -> None:
    base = dict(
        campaign_natural="WB-CFL-001",
        approved_member_offers=_make_offers(),
        operator_principal="maya.patel@labtenant.onmicrosoft.com",
        tier3_pii_unlock_request_id="unlock-req-cfl-001",
    )
    commit_winback_offer(  # type: ignore[arg-type]
        cohort_window_start="2026-05-04T00:00:00Z",
        cohort_window_end="2026-05-11T00:00:00Z",
        **base,
    )
    with pytest.raises(McpError) as exc:
        commit_winback_offer(  # type: ignore[arg-type]
            cohort_window_start="2026-05-11T00:00:00Z",
            cohort_window_end="2026-05-18T00:00:00Z",
            **base,
        )
    assert exc.value.code is McpErrorCode.CONFLICT


def test_commit_winback_offer_rejects_empty_offers() -> None:
    with pytest.raises(McpError) as exc:
        commit_winback_offer(
            campaign_natural="WB-EMPTY",
            cohort_window_start="2026-05-04T00:00:00Z",
            cohort_window_end="2026-05-11T00:00:00Z",
            approved_member_offers=[],
            operator_principal="maya.patel@labtenant.onmicrosoft.com",
            tier3_pii_unlock_request_id="unlock-req-x",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_commit_winback_offer_rejects_missing_tier3_unlock() -> None:
    with pytest.raises(McpError) as exc:
        commit_winback_offer(
            campaign_natural="WB-NOUNLOCK",
            cohort_window_start="2026-05-04T00:00:00Z",
            cohort_window_end="2026-05-11T00:00:00Z",
            approved_member_offers=_make_offers(),
            operator_principal="maya.patel@labtenant.onmicrosoft.com",
            tier3_pii_unlock_request_id="",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_commit_winback_offer_rejects_offer_without_customer_token() -> None:
    bad = [{"offer_kind": "percent_off", "offer_depth_pct": 25.0}]
    with pytest.raises(McpError) as exc:
        commit_winback_offer(
            campaign_natural="WB-NOTOK",
            cohort_window_start="2026-05-04T00:00:00Z",
            cohort_window_end="2026-05-11T00:00:00Z",
            approved_member_offers=bad,
            operator_principal="maya.patel@labtenant.onmicrosoft.com",
            tier3_pii_unlock_request_id="unlock-req-y",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_commit_winback_offer_rejects_out_of_bounds_depth() -> None:
    bad = [{"customer_token": "tok-x", "offer_depth_pct": 150.0}]
    with pytest.raises(McpError) as exc:
        commit_winback_offer(
            campaign_natural="WB-OOB",
            cohort_window_start="2026-05-04T00:00:00Z",
            cohort_window_end="2026-05-11T00:00:00Z",
            approved_member_offers=bad,
            operator_principal="maya.patel@labtenant.onmicrosoft.com",
            tier3_pii_unlock_request_id="unlock-req-z",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


# --- Contracts -------------------------------------------------------------


def test_contracts_declare_required_scopes() -> None:
    for c in CONTRACTS:
        assert "practice:rc" in c.required_scopes
        assert "service:rc-e2e-04" in c.required_scopes


def test_pricing_basis_contract_propagates_trade_secret_and_pii() -> None:
    basis_contract = next(
        c for c in CONTRACTS if c.name.endswith("get_winback_offer_basis")
    )
    assert Classification.TRADE_SECRET in basis_contract.classification_propagation
    assert Classification.PII in basis_contract.classification_propagation


def test_cohort_contract_propagates_pii_only() -> None:
    cohort_contract = next(
        c for c in CONTRACTS if c.name.endswith("get_loyalty_churn_cohort")
    )
    assert Classification.PII in cohort_contract.classification_propagation
    assert Classification.TRADE_SECRET not in cohort_contract.classification_propagation
