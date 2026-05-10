"""Tests for rc-e2e-09-mcp tools (Sprint 39)."""

from __future__ import annotations

import pytest

from apex_core.types import Classification
from fabric_mcp import InMemoryFabricBackend, set_fabric_backend
from mcp_common import McpError, McpErrorCode
from rc_e2e_09_mcp import (
    CONTRACTS,
    commit_lot_event,
    get_lot_provenance,
    get_recall_panel,
)
from rc_e2e_09_mcp.tools import _reset_committed_lot_events_for_test


@pytest.fixture(autouse=True)
def _seed_fabric() -> InMemoryFabricBackend:
    _reset_committed_lot_events_for_test()
    b = InMemoryFabricBackend(
        views={
            "rc_gold.g_recall_panel": [
                {
                    "trigger_event_id": "REC-001",
                    "trigger_kind": "recall_issued",
                    "jurisdiction": "US-Federal",
                    "fda_ftl_version": "2026.05",
                    "state_recall_filing_required": False,
                    "lot_key": "L-2026W18-DAIRY-A12",
                    "sku_key": "SKU-MILK-2PCT-1G",
                    "is_covered_food": True,
                    "received_with_temp_log": True,
                    "cold_chain_compliant_pre_event": True,
                    "has_critical_tracking_event_log": True,
                    "cte_count": 4,
                    "kde_count": 14,
                    "earliest_cte_ts": "2026-05-04T08:00:00Z",
                    "latest_cte_ts": "2026-05-09T13:00:00Z",
                    "supplier_key": "SUP-DAIRY-7",
                    "downstream_distribution_locations_count": 3,
                    "trace_gaps": [],
                },
                {
                    "trigger_event_id": "REC-001",
                    "trigger_kind": "recall_issued",
                    "jurisdiction": "US-Federal",
                    "fda_ftl_version": "2026.05",
                    "state_recall_filing_required": False,
                    "lot_key": "L-2026W18-DAIRY-B07",
                    "sku_key": "SKU-YOGURT-32OZ-PLAIN",
                    "is_covered_food": True,
                    "received_with_temp_log": False,    # gap
                    "cold_chain_compliant_pre_event": True,
                    "has_critical_tracking_event_log": True,
                    "cte_count": 3,
                    "kde_count": 9,
                    "earliest_cte_ts": "2026-05-04T08:00:00Z",
                    "latest_cte_ts": "2026-05-09T13:00:00Z",
                    "supplier_key": "SUP-DAIRY-7",
                    "downstream_distribution_locations_count": 3,
                    "trace_gaps": [{"cte_kind": "RECEIVING", "missing_kde": "temp_log",
                                    "severity": "high"}],
                },
            ],
            "rc_gold.g_lot_provenance": [
                {
                    "lot_key": "L-2026W18-DAIRY-A12",
                    "sku_key": "SKU-MILK-2PCT-1G",
                    "supplier_key": "SUP-DAIRY-7",
                    "is_covered_food": True,
                    "received_with_temp_log": True,
                    "cold_chain_compliant_pre_event": True,
                    "has_critical_tracking_event_log": True,
                    "event_kind": "trace_audit_pass",
                    "event_ts": "2026-05-09T14:00:00Z",
                    "decision_id": "DEC-AUDIT-001",
                    "trace_id": "trace-rc-09-001",
                },
                {
                    "lot_key": "L-2026W18-DAIRY-A12",
                    "sku_key": "SKU-MILK-2PCT-1G",
                    "supplier_key": "SUP-DAIRY-7",
                    "is_covered_food": True,
                    "received_with_temp_log": True,
                    "cold_chain_compliant_pre_event": True,
                    "has_critical_tracking_event_log": True,
                    "event_kind": "lot_status_held_in_dc",
                    "event_ts": "2026-05-09T16:00:00Z",
                    "decision_id": "DEC-HOLD-001",
                    "trace_id": "trace-rc-09-002",
                },
            ],
        },
    )
    set_fabric_backend(b)
    return b


# --- get_recall_panel ------------------------------------------------------


def test_get_recall_panel_aggregates_lots() -> None:
    panel = get_recall_panel("REC-001")
    assert panel["trigger_event_id"] == "REC-001"
    assert panel["regulatory"]["jurisdiction"] == "US-Federal"
    assert len(panel["affected_lots"]) == 2
    # Trace gaps preserved per FSMA-204 audit requirements
    yogurt = next(
        l for l in panel["affected_lots"]
        if l["lot_key"] == "L-2026W18-DAIRY-B07"
    )
    assert yogurt["received_with_temp_log"] is False
    assert len(yogurt["trace_gaps"]) == 1


def test_get_recall_panel_missing_raises_not_found() -> None:
    with pytest.raises(McpError) as exc:
        get_recall_panel("REC-NO-SUCH")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_get_recall_panel_invalid_input_rejected() -> None:
    with pytest.raises(McpError) as exc:
        get_recall_panel("")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


# --- get_lot_provenance (CROSS-SERVICE) ------------------------------------


def test_get_lot_provenance_returns_current_status_and_history() -> None:
    """Cross-service consumer view — RC-E2E-03 + RC-E2E-07 read this."""
    prov = get_lot_provenance("L-2026W18-DAIRY-A12")
    assert prov["lot_key"] == "L-2026W18-DAIRY-A12"
    assert prov["is_covered_food"] is True
    assert prov["received_with_temp_log"] is True
    # Current status is the most-recent event (held_in_dc), not the earlier audit
    assert prov["current_status"] == "lot_status_held_in_dc"
    # Both events present in history
    assert len(prov["events"]) == 2


def test_get_lot_provenance_missing_lot_raises_not_found() -> None:
    with pytest.raises(McpError) as exc:
        get_lot_provenance("L-NO-SUCH")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_get_lot_provenance_requires_lot_key() -> None:
    with pytest.raises(McpError) as exc:
        get_lot_provenance("")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


# --- commit_lot_event ------------------------------------------------------


def test_commit_lot_event_trace_audit_pass() -> None:
    out = commit_lot_event(
        decision_id="DEC-AUD-001",
        lot_key="L-2026W18-DAIRY-A12",
        event_kind="trace_audit_pass",
        operator_principal="agent-system",
        sku_key="SKU-MILK-2PCT-1G",
        trace_id="trace-rc-09-aud-001",
    )
    assert out["service_code"] == "RC-E2E-09"
    assert out["event_kind"] == "trace_audit_pass"
    assert out["lot_event_id"].startswith("scml-lot-DEC-AUD-001-")
    assert out["outcome"] == "ok"
    # Downstream invalidation keys for RC-E2E-03 + RC-E2E-07 emitted
    invalidation_services = {
        k.split("/")[0] for k in out["downstream_invalidation_keys"]
    }
    assert "rc-e2e-03" in invalidation_services
    assert "rc-e2e-07" in invalidation_services


def test_commit_lot_event_class_I_requires_attestation_id() -> None:
    """FSMA-204 / 21 CFR 7.3 chain-of-custody — Class I requires attestation."""
    with pytest.raises(McpError) as exc:
        commit_lot_event(
            decision_id="DEC-CLASS1-NOATT",
            lot_key="L-2026W18-DAIRY-A12",
            event_kind="recall_class_I",
            operator_principal="rebecca.hall@labtenant.onmicrosoft.com",
            # compliance_attestation_id missing
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT
    assert "compliance_attestation_id" in str(exc.value)


def test_commit_lot_event_class_I_with_attestation_accepted() -> None:
    out = commit_lot_event(
        decision_id="DEC-CLASS1-001",
        lot_key="L-2026W18-DAIRY-A12",
        event_kind="recall_class_I",
        operator_principal="rebecca.hall@labtenant.onmicrosoft.com",
        compliance_attestation_id="attest-fsma-001",
    )
    assert out["event_kind"] == "recall_class_I"
    assert out["compliance_attestation_id"] == "attest-fsma-001"


def test_commit_lot_event_class_II_does_not_require_attestation() -> None:
    """Class II auto-clears with audit row only — no attestation required."""
    out = commit_lot_event(
        decision_id="DEC-CLASS2-001",
        lot_key="L-2026W18-DAIRY-A12",
        event_kind="recall_class_II",
        operator_principal="agent-system",
    )
    assert out["event_kind"] == "recall_class_II"
    assert out["compliance_attestation_id"] is None


def test_commit_lot_event_unknown_kind_rejected() -> None:
    with pytest.raises(McpError) as exc:
        commit_lot_event(
            decision_id="DEC-X",
            lot_key="L-X",
            event_kind="recall_class_omega",   # not a valid kind
            operator_principal="agent-system",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_commit_lot_event_idempotent_on_triple_key() -> None:
    args = dict(
        decision_id="DEC-IDEM-001",
        lot_key="L-IDEM-A",
        event_kind="trace_audit_pass",
        operator_principal="agent-system",
        sku_key="SKU-X",
    )
    first = commit_lot_event(**args)  # type: ignore[arg-type]
    second = commit_lot_event(**args)  # type: ignore[arg-type]
    assert first["lot_event_id"] == second["lot_event_id"]
    assert first["scd2_valid_from"] == second["scd2_valid_from"]


def test_commit_lot_event_conflict_on_param_mismatch() -> None:
    base = dict(
        decision_id="DEC-CFL-001",
        lot_key="L-CFL-A",
        event_kind="trace_audit_pass",
    )
    commit_lot_event(  # type: ignore[arg-type]
        operator_principal="agent-A", sku_key="SKU-X", **base,
    )
    with pytest.raises(McpError) as exc:
        commit_lot_event(  # type: ignore[arg-type]
            operator_principal="agent-A", sku_key="SKU-Y", **base,
        )
    assert exc.value.code is McpErrorCode.CONFLICT


def test_commit_lot_event_requires_operator_principal() -> None:
    with pytest.raises(McpError) as exc:
        commit_lot_event(
            decision_id="DEC-NOOP",
            lot_key="L-X",
            event_kind="trace_audit_pass",
            operator_principal="",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_commit_lot_event_requires_decision_id_and_lot_key() -> None:
    with pytest.raises(McpError) as exc:
        commit_lot_event(
            decision_id="",
            lot_key="L-X",
            event_kind="trace_audit_pass",
            operator_principal="agent-system",
        )
    assert exc.value.code is McpErrorCode.INVALID_INPUT


# --- Contracts -------------------------------------------------------------


def test_write_contract_requires_rc_e2e_09_scope() -> None:
    """SCML.Lot ownership boundary — only RC-E2E-09 can write."""
    write_contract = next(
        c for c in CONTRACTS if c.name.endswith("commit_lot_event")
    )
    assert "service:rc-e2e-09" in write_contract.required_scopes


def test_lot_provenance_contract_accepts_cross_service_scope() -> None:
    """Cross-service read — service:rc-e2e-09 NOT required."""
    lot_prov_contract = next(
        c for c in CONTRACTS if c.name.endswith("get_lot_provenance")
    )
    # Must have practice:rc but NOT require service:rc-e2e-09 specifically
    assert "practice:rc" in lot_prov_contract.required_scopes
    assert "service:rc-e2e-09" not in lot_prov_contract.required_scopes


def test_recall_panel_contract_requires_rc_e2e_09_scope() -> None:
    """get_recall_panel is internal-RC-E2E-09 only — Analyst + Compliance."""
    recall_contract = next(
        c for c in CONTRACTS if c.name.endswith("get_recall_panel")
    )
    assert "service:rc-e2e-09" in recall_contract.required_scopes


def test_no_contract_propagates_trade_secret_or_pii() -> None:
    """RC-E2E-09 domain is INTERNAL only — compliance is not a TRADE_SECRET surface."""
    for c in CONTRACTS:
        assert Classification.TRADE_SECRET not in c.classification_propagation
        assert Classification.PII not in c.classification_propagation
