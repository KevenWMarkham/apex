"""Tests for apex_wizard.security_gate (Sprint 46.2)."""

from __future__ import annotations

import pytest

from apex_wizard.security_gate import (
    GateEvaluation,
    GateStatus,
    SecurityGateReport,
    evaluate_all_gates,
    register_checker,
)


def test_evaluate_all_gates_returns_15_gates() -> None:
    """Per Pre-deployment-Security-Gate.md — PSG-1 through PSG-15."""
    report = evaluate_all_gates("bigbox")
    assert len(report.gates) == 15
    gate_ids = {g.gate_id for g in report.gates}
    expected = {f"PSG-{i}" for i in range(1, 16)}
    assert gate_ids == expected


def test_mock_mode_returns_overall_green_for_psg_1_14() -> None:
    """Without context.use_case_data, PSG-15 is UNKNOWN; others mock-green."""
    report = evaluate_all_gates("bigbox")
    # PSG-1 through PSG-14 are all mock-green
    for gate in report.gates:
        if gate.gate_id != "PSG-15":
            assert gate.status == GateStatus.GREEN, (
                f"{gate.gate_id} expected GREEN, got {gate.status}"
            )


def test_psg_15_without_context_returns_unknown() -> None:
    """Without use_case_data PSG-15 can't evaluate — UNKNOWN."""
    report = evaluate_all_gates("bigbox")
    psg_15 = next(g for g in report.gates if g.gate_id == "PSG-15")
    assert psg_15.status == GateStatus.UNKNOWN


def test_psg_15_with_laptop_substrate_passes_with_synthetic_personas() -> None:
    context = {
        "use_case_data": {
            "use_case_id": "rc-e2e-05--default",
            "substrate": "laptop",
            "personas_active": [{"id": "jamie-oconnor-store-manager"}],
        },
    }
    report = evaluate_all_gates("bigbox", context)
    psg_15 = next(g for g in report.gates if g.gate_id == "PSG-15")
    assert psg_15.status == GateStatus.GREEN
    assert psg_15.mode == "real"


def test_psg_15_with_prod_substrate_unbound_personas_fails_red() -> None:
    context = {
        "use_case_data": {
            "use_case_id": "rc-e2e-05--bigbox-prod",
            "substrate": "prod",
            "personas_active": [{"id": "jamie-oconnor-store-manager"}],
        },
    }
    report = evaluate_all_gates("bigbox", context)
    psg_15 = next(g for g in report.gates if g.gate_id == "PSG-15")
    assert psg_15.status == GateStatus.RED
    assert psg_15.mode == "real"
    assert psg_15.metadata.get("substrate") == "prod"


def test_psg_15_with_prod_substrate_and_bindings_passes_green() -> None:
    context = {
        "use_case_data": {
            "use_case_id": "rc-e2e-05--bigbox-prod",
            "substrate": "prod",
            "personas_active": [{"id": "jamie-oconnor-store-manager"}],
            "persona_principal_bindings": {
                "jamie-oconnor-store-manager": {
                    "binding_mode": "entra_group",
                    "entra_group_object_id": "8a3c1234-aaaa-bbbb-cccc-456789abcdef",
                },
            },
        },
    }
    report = evaluate_all_gates("bigbox", context)
    psg_15 = next(g for g in report.gates if g.gate_id == "PSG-15")
    assert psg_15.status == GateStatus.GREEN


def test_overall_status_is_red_when_any_blocking_gate_red() -> None:
    context = {
        "use_case_data": {
            "use_case_id": "x",
            "substrate": "prod",
            "personas_active": [{"id": "jamie-oconnor-store-manager"}],
        },
    }
    report = evaluate_all_gates("bigbox", context)
    # PSG-15 is RED (prod + unbound) → overall RED
    assert report.overall_status == GateStatus.RED
    assert report.deploy_allowed is False
    assert "PSG-15" in report.red_gates


def test_overall_status_is_green_when_all_gates_pass() -> None:
    context = {
        "use_case_data": {
            "use_case_id": "x",
            "substrate": "laptop",
            "personas_active": [{"id": "jamie-oconnor-store-manager"}],
        },
    }
    report = evaluate_all_gates("bigbox", context)
    # All mock-green + PSG-15 green
    assert report.overall_status == GateStatus.GREEN
    assert report.deploy_allowed is True


def test_register_checker_swaps_mock_for_custom() -> None:
    """Sprint 41-45 production wiring uses register_checker to swap mock checkers."""
    from datetime import UTC, datetime

    def my_checker(tenant: str, context: dict) -> GateEvaluation:
        return GateEvaluation(
            gate_id="PSG-1",
            title="Defender for Cloud (production)",
            status=GateStatus.YELLOW,
            evaluated_at=datetime.now(UTC),
            mode="real",
            rationale="custom checker returned yellow for testing",
            blocking=False,
        )

    # Save the original to restore after the test
    from apex_wizard.security_gate import _REGISTRY
    original = _REGISTRY["PSG-1"]
    try:
        register_checker("PSG-1", my_checker)
        report = evaluate_all_gates("bigbox")
        psg_1 = next(g for g in report.gates if g.gate_id == "PSG-1")
        assert psg_1.status == GateStatus.YELLOW
        assert psg_1.mode == "real"
    finally:
        _REGISTRY["PSG-1"] = original


def test_report_as_dict_is_json_serialisable() -> None:
    import json
    report = evaluate_all_gates("bigbox")
    body = json.dumps(report.as_dict())
    assert "PSG-15" in body
    assert "overall_status" in body


def test_deploy_allowed_when_yellow_but_no_red() -> None:
    """Yellow gates surface warnings but don't block deploy."""
    from datetime import UTC, datetime

    def yellow_checker(tenant: str, context: dict) -> GateEvaluation:
        return GateEvaluation(
            gate_id="PSG-1",
            title="Defender warning",
            status=GateStatus.YELLOW,
            evaluated_at=datetime.now(UTC),
            mode="real",
            rationale="some warning",
            blocking=True,
        )

    from apex_wizard.security_gate import _REGISTRY
    original = _REGISTRY["PSG-1"]
    try:
        register_checker("PSG-1", yellow_checker)
        report = evaluate_all_gates("bigbox")
        # YELLOW present but no RED → deploy still allowed
        assert report.overall_status == GateStatus.YELLOW
        assert report.deploy_allowed is True
    finally:
        _REGISTRY["PSG-1"] = original
