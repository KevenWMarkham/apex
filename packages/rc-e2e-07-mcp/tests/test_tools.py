"""Tests for rc-e2e-07-mcp tools (Sprint 37)."""

from __future__ import annotations

import pytest

from apex_core.types import Classification
from fabric_mcp import InMemoryFabricBackend, set_fabric_backend
from mcp_common import McpError, McpErrorCode
from rc_e2e_07_mcp import (
    CONTRACTS,
    commit_hold_decision,
    get_fraud_score_basis,
    get_return_event,
)
from rc_e2e_07_mcp.tools import _reset_committed_decisions_for_test


@pytest.fixture(autouse=True)
def _seed_fabric() -> InMemoryFabricBackend:
    _reset_committed_decisions_for_test()
    b = InMemoryFabricBackend(
        views={
            "rc_gold.g_return_event_panel": [
                {
                    "event_id": "RET-001",
                    "tenant_id": "labtenant",
                    "return_kind": "ecomm",
                    "ts": "2026-05-10T11:30:00Z",
                    "customer_token": "tok-cust-Z",
                    "device_fingerprint_token": "tok-dev-Q",
                    "payment_fingerprint_token": "tok-pay-R",
                    "original_order_natural": "ORD-2026-7711",
                    "original_purchase_at": "2026-04-25T09:11:00Z",
                    "skus_returned": [
                        {"sku_key": "SKU-LAPTOP-15", "qty": 1, "unit_refund_usd": 1299.00}
                    ],
                    "refund_value_usd": 1299.00,
                    "channel": "online",
                    "return_reason_code": "DAMAGED",
                    "receipt_present": True,
                    "receipt_match_quality": "exact",
                },
            ],
            "rc_gold.g_fraud_score_basis": [
                {
                    "event_id": "RET-001",
                    "graphs": {
                        "customer": {
                            "trailing_90d_return_count": 7,
                            "lifetime_return_ratio_pct": 22.5,
                        },
                        "payment": {
                            "payment_token_linked_customers_count": 4,
                        },
                        "device": {
                            "device_token_linked_accounts_30d": 6,
                        },
                        "shipping": {
                            "address_linked_customers_count": 3,
                        },
                        "sku": {
                            "tenant_return_rate_decile": 9,
                        },
                    },
                    "tenant_thresholds": {
                        "weights_override": {
                            "customer.trailing_90d_return_count_excessive": 0.20,
                            "customer.lifetime_return_ratio_high": 0.15,
                            "payment.payment_token_linked_to_>=_3_customers": 0.25,
                            "device.device_token_linked_to_>=_5_accounts_30d": 0.20,
                            "shipping.shipping_address_linked_to_>=_4_customers": 0.15,
                            "sku.sku_return_rate_top_decile": 0.05,
                        },
                    },
                    "loss_economics": {
                        "_classification": "trade_secret",
                        "hold_recovery_efficiency_pct": 70,
                        "hold_admin_flat_usd": 35.00,
                        "return_label_cost_usd": 12.00,
                    },
                    "chargeback_priors": {
                        "_classification": "trade_secret",
                        "deny_to_chargeback_rate_pct": 30,
                    },
                    "regional_constraints": {
                        "jurisdiction": "US-NY",
                        "max_hold_days_allowed": None,
                        "must_provide_written_reason": True,
                    },
                },
            ],
        },
    )
    set_fabric_backend(b)
    return b


# --- get_return_event ------------------------------------------------------


def test_get_return_event_returns_tokenised_panel() -> None:
    panel = get_return_event("RET-001")
    assert panel["event_id"] == "RET-001"
    assert panel["customer_token"].startswith("tok-cust-")
    assert panel["device_fingerprint_token"].startswith("tok-dev-")
    assert panel["payment_fingerprint_token"].startswith("tok-pay-")
    # Refund value present
    assert panel["refund_value_usd"] == 1299.00


def test_get_return_event_missing_raises_not_found() -> None:
    with pytest.raises(McpError) as exc:
        get_return_event("RET-NO-SUCH")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_get_return_event_invalid_input_rejected() -> None:
    with pytest.raises(McpError) as exc:
        get_return_event("")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


# --- get_fraud_score_basis -------------------------------------------------


def test_get_fraud_score_basis_default_strips_loss_economics() -> None:
    """Without include_loss_economics, TRADE_SECRET blocks must NOT be returned."""
    basis = get_fraud_score_basis(event_id="RET-001", depth=2)
    assert basis["event_id"] == "RET-001"
    assert "graphs" in basis
    # TRADE_SECRET stripped at the read boundary
    assert "loss_economics" not in basis
    assert "chargeback_priors" not in basis


def test_get_fraud_score_basis_with_loss_economics_returns_trade_secret() -> None:
    """include_loss_economics=True returns the TRADE_SECRET blocks."""
    basis = get_fraud_score_basis(
        event_id="RET-001", depth=2, include_loss_economics=True,
    )
    assert "loss_economics" in basis
    assert basis["loss_economics"]["_classification"] == "trade_secret"
    assert basis["chargeback_priors"]["deny_to_chargeback_rate_pct"] == 30


def test_get_fraud_score_basis_invalid_depth_rejected() -> None:
    with pytest.raises(McpError) as exc:
        get_fraud_score_basis(event_id="RET-001", depth=0)
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_get_fraud_score_basis_depth_too_deep_rejected() -> None:
    with pytest.raises(McpError) as exc:
        get_fraud_score_basis(event_id="RET-001", depth=4)
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_get_fraud_score_basis_missing_event_raises_not_found() -> None:
    with pytest.raises(McpError) as exc:
        get_fraud_score_basis(event_id="RET-NO-SUCH")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_get_fraud_score_basis_requires_event_id() -> None:
    with pytest.raises(McpError) as exc:
        get_fraud_score_basis(event_id="")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


# --- commit_hold_decision --------------------------------------------------


def test_commit_hold_decision_auto_clear_path() -> None:
    out = commit_hold_decision(
        decision_id="DEC-AC-001",
        return_event_id="RET-001",
        decision_class="auto_clear",
        operator_principal="agent-system",
        fraud_score=0.18,
        refund_value_usd=49.99,
        trace_id="trace-rf-001",
    )
    assert out["decision_class"] == "auto_clear"
    assert out["service_code"] == "RC-E2E-07"
    assert out["fraud_score"] == 0.18
    assert out["outcome"] == "ok"


def test_commit_hold_decision_hold_with_pii_unlock_requires_unlock_id() -> None:
    """Sprint 37.3 — escalate path REQUIRES tier3_pii_unlock_request_id."""
    with pytest.raises(McpError) as exc:
        commit_hold_decision(
            decision_id="DEC-NOID",
            return_event_id="RET-001",
            decision_class="hold_with_pii_unlock",
            operator_principal="rebecca.hall@labtenant.onmicrosoft.com",
            fraud_score=0.85,
            # tier3_pii_unlock_request_id missing
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT
    assert "tier3_pii_unlock_request_id" in str(exc.value)


def test_commit_hold_decision_hold_with_pii_unlock_accepts_unlock_id() -> None:
    out = commit_hold_decision(
        decision_id="DEC-HLD-001",
        return_event_id="RET-001",
        decision_class="hold_with_pii_unlock",
        operator_principal="rebecca.hall@labtenant.onmicrosoft.com",
        tier3_pii_unlock_request_id="unlock-req-rf-001",
        fraud_score=0.85,
    )
    assert out["decision_class"] == "hold_with_pii_unlock"
    assert out["tier3_pii_unlock_request_id"] == "unlock-req-rf-001"


def test_commit_hold_decision_deny_requires_rationale() -> None:
    """Regional consumer-law audit field — deny without rationale rejected."""
    with pytest.raises(McpError) as exc:
        commit_hold_decision(
            decision_id="DEC-DENY-NORS",
            return_event_id="RET-001",
            decision_class="deny_at_hitl",
            operator_principal="rebecca.hall@labtenant.onmicrosoft.com",
            fraud_score=0.55,
            # deny_rationale missing
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT
    assert "deny_rationale" in str(exc.value)


def test_commit_hold_decision_deny_with_rationale_accepted() -> None:
    out = commit_hold_decision(
        decision_id="DEC-DENY-001",
        return_event_id="RET-001",
        decision_class="deny_at_hitl",
        operator_principal="rebecca.hall@labtenant.onmicrosoft.com",
        fraud_score=0.55,
        deny_rationale="Receipt missing; 60-day return window exceeded.",
    )
    assert out["decision_class"] == "deny_at_hitl"
    assert out["deny_rationale"].startswith("Receipt missing")


def test_commit_hold_decision_unknown_class_rejected() -> None:
    with pytest.raises(McpError) as exc:
        commit_hold_decision(
            decision_id="DEC-X",
            return_event_id="RET-001",
            decision_class="banhammer",
            operator_principal="rebecca.hall@labtenant.onmicrosoft.com",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_commit_hold_decision_idempotent_on_decision_id() -> None:
    args = dict(
        decision_id="DEC-IDEM-001",
        return_event_id="RET-001",
        decision_class="auto_clear",
        operator_principal="agent-system",
        fraud_score=0.18,
        refund_value_usd=49.99,
    )
    first = commit_hold_decision(**args)  # type: ignore[arg-type]
    second = commit_hold_decision(**args)  # type: ignore[arg-type]
    assert first["applied_at"] == second["applied_at"]


def test_commit_hold_decision_conflict_on_param_mismatch() -> None:
    base = dict(
        decision_id="DEC-CFL-001",
        return_event_id="RET-001",
        operator_principal="rebecca.hall@labtenant.onmicrosoft.com",
        fraud_score=0.18,
    )
    commit_hold_decision(decision_class="auto_clear", **base)  # type: ignore[arg-type]
    with pytest.raises(McpError) as exc:
        commit_hold_decision(  # type: ignore[arg-type]
            decision_class="approve_at_hitl", **base,
        )
    assert exc.value.code is McpErrorCode.CONFLICT


def test_commit_hold_decision_rejects_out_of_bound_fraud_score() -> None:
    with pytest.raises(McpError) as exc:
        commit_hold_decision(
            decision_id="DEC-OOB",
            return_event_id="RET-001",
            decision_class="auto_clear",
            operator_principal="agent-system",
            fraud_score=1.5,    # > 1.0 invalid
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_commit_hold_decision_requires_operator_principal() -> None:
    with pytest.raises(McpError) as exc:
        commit_hold_decision(
            decision_id="DEC-NOOP",
            return_event_id="RET-001",
            decision_class="auto_clear",
            operator_principal="",
            fraud_score=0.18,
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


# --- Contracts -------------------------------------------------------------


def test_contracts_declare_required_scopes() -> None:
    for c in CONTRACTS:
        assert "practice:rc" in c.required_scopes
        assert "service:rc-e2e-07" in c.required_scopes


def test_fraud_basis_contract_propagates_pii_and_trade_secret() -> None:
    basis_contract = next(
        c for c in CONTRACTS if c.name.endswith("get_fraud_score_basis")
    )
    assert Classification.PII in basis_contract.classification_propagation
    assert Classification.TRADE_SECRET in basis_contract.classification_propagation


def test_return_event_contract_propagates_pii_only() -> None:
    return_contract = next(
        c for c in CONTRACTS if c.name.endswith("get_return_event")
    )
    assert Classification.PII in return_contract.classification_propagation
    # TRADE_SECRET fields require the include_loss_economics path on basis tool only
    assert Classification.TRADE_SECRET not in return_contract.classification_propagation
