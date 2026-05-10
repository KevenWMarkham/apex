"""Tests for rc-e2e-05-mcp tools (Sprint 35)."""

from __future__ import annotations

import pytest

from apex_core.types import Classification
from fabric_mcp import InMemoryFabricBackend, set_fabric_backend
from mcp_common import McpError, McpErrorCode
from rc_e2e_05_mcp import (
    CONTRACTS,
    commit_task_dispatch,
    get_oos_event,
    get_shelf_gap_assignment_basis,
)
from rc_e2e_05_mcp.tools import _reset_committed_dispatch_for_test


@pytest.fixture(autouse=True)
def _seed_fabric() -> InMemoryFabricBackend:
    _reset_committed_dispatch_for_test()
    b = InMemoryFabricBackend(
        views={
            "rc_gold.g_oos_event_panel": [
                {
                    "event_id": "OSA-001",
                    "store_id": "store-100",
                    "bay_id": "bay-A4",
                    "event_ts": "2026-05-10T06:02:00Z",
                    "signal_kind": "pos_zero",
                    "sku_key": "SKU-MILK-2PCT-1G",
                    "on_hand_qty": 0,
                    "last_sold_at": "2026-05-10T05:18:00Z",
                    "last_received_at": "2026-05-09T14:00:00Z",
                    "key_value_flag": True,
                    "unit_retail": 3.99,
                    "baseline_velocity_hourly": 4.5,
                    "pos_velocity_24h": [4, 5, 6, 4, 0, 0, 0],
                    "replenishment_eta_minutes": 45,
                    "matched_sku_confidence": 0.95,
                    "observed_qty": 0,
                },
                {
                    "event_id": "OSA-001",
                    "store_id": "store-100",
                    "bay_id": "bay-A6",
                    "event_ts": "2026-05-10T06:02:00Z",
                    "signal_kind": "pos_zero",
                    "sku_key": "SKU-YOGURT-32OZ-PLAIN",
                    "on_hand_qty": 2,
                    "last_sold_at": "2026-05-10T04:30:00Z",
                    "last_received_at": "2026-05-09T14:00:00Z",
                    "key_value_flag": False,
                    "unit_retail": 5.49,
                    "baseline_velocity_hourly": 1.2,
                    "pos_velocity_24h": [1, 2, 1, 1, 0, 0, 0],
                    "replenishment_eta_minutes": 45,
                    "matched_sku_confidence": 0.92,
                    "observed_qty": 2,
                },
            ],
            "rc_gold.g_shelf_gap_assignment_basis": [
                {
                    "store_id": "store-100",
                    "shift_capacity_minutes_remaining": 240,
                    "associates": [
                        {"associate_id": "tok-emp-A", "skill_tier": "level_3",
                         "authorised_zones": ["dairy", "bakery"], "last_known_bay": "bay-A1"},
                        {"associate_id": "tok-emp-B", "skill_tier": "level_1",
                         "authorised_zones": ["dairy"], "last_known_bay": "bay-D1"},
                    ],
                    "bay_layout": {
                        "bay-A1-bay-A4": 1,  "bay-A4-bay-A6": 1,  "bay-A6-bay-D1": 4,
                    },
                    "task_duration_norms": {
                        "restock_from_backroom": 3,
                        "raise_replenishment_request": 2,
                        "fix_planogram": 6,
                        "verify_perpetual": 5,
                    },
                },
            ],
        },
    )
    set_fabric_backend(b)
    return b


# --- get_oos_event ---------------------------------------------------------


def test_get_oos_event_aggregates_skus() -> None:
    panel = get_oos_event("OSA-001")
    assert panel["event_id"] == "OSA-001"
    assert panel["store_id"] == "store-100"
    assert len(panel["affected_skus"]) == 2
    assert {s["sku_key"] for s in panel["affected_skus"]} == {
        "SKU-MILK-2PCT-1G", "SKU-YOGURT-32OZ-PLAIN",
    }
    # Key-value flag preserved
    milk = next(s for s in panel["affected_skus"] if s["sku_key"] == "SKU-MILK-2PCT-1G")
    assert milk["key_value_flag"] is True


def test_get_oos_event_missing_raises_not_found() -> None:
    with pytest.raises(McpError) as exc:
        get_oos_event("OSA-NO-SUCH")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_get_oos_event_invalid_input_rejected() -> None:
    with pytest.raises(McpError) as exc:
        get_oos_event("")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


# --- get_shelf_gap_assignment_basis ----------------------------------------


def test_get_shelf_gap_assignment_basis_returns_roster() -> None:
    basis = get_shelf_gap_assignment_basis(
        store_id="store-100", as_of="2026-05-10T06:00:00Z",
    )
    assert basis["store_id"] == "store-100"
    assert basis["shift_capacity_minutes_remaining"] == 240
    associates = basis["associates"]
    assert len(associates) == 2
    # Tokenised IDs
    for a in associates:
        assert a["associate_id"].startswith("tok-emp-")
    # Task duration norms present
    assert basis["task_duration_norms"]["restock_from_backroom"] == 3


def test_get_shelf_gap_assignment_basis_missing_raises_not_found() -> None:
    with pytest.raises(McpError) as exc:
        get_shelf_gap_assignment_basis(
            store_id="store-no-such", as_of="2026-05-10T06:00:00Z",
        )
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_get_shelf_gap_assignment_basis_malformed_as_of_rejected() -> None:
    with pytest.raises(McpError) as exc:
        get_shelf_gap_assignment_basis(store_id="store-100", as_of="not-a-date")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_get_shelf_gap_assignment_basis_requires_store() -> None:
    with pytest.raises(McpError) as exc:
        get_shelf_gap_assignment_basis(store_id="", as_of="2026-05-10T06:00:00Z")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


# --- commit_task_dispatch --------------------------------------------------


def test_commit_task_dispatch_fanout_phase() -> None:
    out = commit_task_dispatch(
        dispatch_id="DSP-001",
        associate_id="tok-emp-A",
        task_order=1,
        operator_principal="jamie.oconnor@labtenant.onmicrosoft.com",
        sku_key="SKU-MILK-2PCT-1G",
        bay_id="bay-A4",
        task_kind="restock_from_backroom",
        trace_id="trace-osa-001",
    )
    assert out["dispatch_id"] == "DSP-001"
    assert out["phase"] == "fanout"
    assert out["completion_kind"] is None
    assert out["service_code"] == "RC-E2E-05"
    assert out["outcome"] == "ok"


def test_commit_task_dispatch_completion_phase() -> None:
    # Fan-out first
    commit_task_dispatch(
        dispatch_id="DSP-COMP-001",
        associate_id="tok-emp-A",
        task_order=1,
        operator_principal="jamie.oconnor@labtenant.onmicrosoft.com",
        sku_key="SKU-MILK-2PCT-1G",
        bay_id="bay-A4",
        task_kind="restock_from_backroom",
    )
    # Completion (different task_order = different idempotency key)
    out = commit_task_dispatch(
        dispatch_id="DSP-COMP-001",
        associate_id="tok-emp-A",
        task_order=2,
        operator_principal="jamie.oconnor@labtenant.onmicrosoft.com",
        completion_kind="complete",
    )
    assert out["phase"] == "completion"
    assert out["completion_kind"] == "complete"


def test_commit_task_dispatch_idempotent_on_triple_key() -> None:
    args = dict(
        dispatch_id="DSP-IDEM-001",
        associate_id="tok-emp-A",
        task_order=1,
        operator_principal="jamie.oconnor@labtenant.onmicrosoft.com",
        sku_key="SKU-X",
        bay_id="bay-X1",
        task_kind="restock_from_backroom",
    )
    first = commit_task_dispatch(**args)  # type: ignore[arg-type]
    second = commit_task_dispatch(**args)  # type: ignore[arg-type]
    assert first["cxml_associate_task_id"] == second["cxml_associate_task_id"]
    assert first["applied_at"] == second["applied_at"]


def test_commit_task_dispatch_conflict_on_param_mismatch() -> None:
    base = dict(
        dispatch_id="DSP-CFL-001",
        associate_id="tok-emp-A",
        task_order=1,
        operator_principal="jamie.oconnor@labtenant.onmicrosoft.com",
    )
    commit_task_dispatch(  # type: ignore[arg-type]
        sku_key="SKU-MILK", bay_id="bay-A4",
        task_kind="restock_from_backroom", **base,
    )
    with pytest.raises(McpError) as exc:
        commit_task_dispatch(  # type: ignore[arg-type]
            sku_key="SKU-YOGURT", bay_id="bay-A4",
            task_kind="restock_from_backroom", **base,
        )
    assert exc.value.code is McpErrorCode.CONFLICT


def test_commit_task_dispatch_fanout_requires_sku_bay_task_kind() -> None:
    with pytest.raises(McpError) as exc:
        commit_task_dispatch(
            dispatch_id="DSP-NOPE",
            associate_id="tok-emp-A",
            task_order=1,
            operator_principal="jamie.oconnor@labtenant.onmicrosoft.com",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_commit_task_dispatch_unknown_completion_kind_rejected() -> None:
    with pytest.raises(McpError) as exc:
        commit_task_dispatch(
            dispatch_id="DSP-CK",
            associate_id="tok-emp-A",
            task_order=1,
            operator_principal="jamie.oconnor@labtenant.onmicrosoft.com",
            completion_kind="dance",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_commit_task_dispatch_rejects_invalid_task_order() -> None:
    with pytest.raises(McpError) as exc:
        commit_task_dispatch(
            dispatch_id="DSP-OOB",
            associate_id="tok-emp-A",
            task_order=0,   # < 1 invalid
            operator_principal="jamie.oconnor@labtenant.onmicrosoft.com",
            sku_key="x", bay_id="x", task_kind="restock_from_backroom",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_commit_task_dispatch_rejects_missing_operator() -> None:
    with pytest.raises(McpError) as exc:
        commit_task_dispatch(
            dispatch_id="DSP-NO-OP",
            associate_id="tok-emp-A",
            task_order=1,
            operator_principal="",
            sku_key="x", bay_id="x", task_kind="restock_from_backroom",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


# --- Contracts -------------------------------------------------------------


def test_contracts_declare_required_scopes() -> None:
    for c in CONTRACTS:
        assert "practice:rc" in c.required_scopes
        assert "service:rc-e2e-05" in c.required_scopes


def test_no_contract_propagates_trade_secret_or_pii() -> None:
    """RC-E2E-05 domain is INTERNAL only — no margin / customer data."""
    for c in CONTRACTS:
        assert Classification.TRADE_SECRET not in c.classification_propagation
        assert Classification.PII not in c.classification_propagation
