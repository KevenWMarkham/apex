"""Sprint 37 — RC-E2E-07 returns-fraud agent manifest smoke tests.

Verifies every agent.yaml under
``services/rc/RC-E2E-07/scenarios/rc-returns-fraud-detection/agents/``
declares the production fields Sprint 37 requires:

- model is set (not "TBD")
- prompt_ref exists and the file is non-stub
- canonical_pattern == "concurrent" (Sprint 37's distinctive feature)
- Adaptive HITL fields wired on Decide (3-band gate)
- Tier-3 PII JIT unlock fields per Sprint 37.3
- TRADE_SECRET-touching agents declare classification_propagation
- assess + classify declare each other as concurrent_sibling_roles
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

SCENARIO_DIR = Path(__file__).resolve().parent
AGENTS_DIR = SCENARIO_DIR / "agents"
FIXTURE = SCENARIO_DIR / "fixtures" / "returns-fraud-event.json"

EXPECTED_ROLES = {"assess", "classify", "quantify", "decide", "act", "learn"}
TRADE_SECRET_ROLES = {"quantify", "decide", "act", "learn"}
PII_ROLES = {"assess", "classify", "quantify", "decide", "act", "learn"}
HITL_GATE_ROLES = {"decide"}
CONCURRENT_SIBLING_ROLES = {"assess", "classify"}   # the parallel pair


def _load_agent(role: str) -> dict:
    path = AGENTS_DIR / role / "agent.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_prompt(role: str) -> str:
    agent = _load_agent(role)
    prompt_path = AGENTS_DIR / role / agent["prompt_ref"]
    return prompt_path.read_text(encoding="utf-8")


def test_all_six_roles_present() -> None:
    on_disk = {p.name for p in AGENTS_DIR.iterdir() if p.is_dir()}
    assert on_disk == EXPECTED_ROLES


@pytest.mark.parametrize("role", sorted(EXPECTED_ROLES))
def test_each_agent_has_real_model(role: str) -> None:
    agent = _load_agent(role)
    assert agent["model"] != "TBD", f"{role} agent.yaml still has model=TBD"
    assert agent["model"].startswith("gpt-")


@pytest.mark.parametrize("role", sorted(EXPECTED_ROLES))
def test_each_prompt_is_authored(role: str) -> None:
    body = _load_prompt(role)
    assert "TBD" not in body, f"{role} prompt is still stub (contains TBD)"
    assert len(body) > 500


@pytest.mark.parametrize("role", sorted(EXPECTED_ROLES))
def test_each_agent_has_versions(role: str) -> None:
    agent = _load_agent(role)
    assert agent.get("prompt_version") == "1.0.0"
    assert agent.get("manifest_version") == "1.0.0"


@pytest.mark.parametrize("role", sorted(EXPECTED_ROLES))
def test_canonical_pattern_is_concurrent(role: str) -> None:
    """Per RC-E2E-07 use-case orchestration_archetype: concurrent (Sprint 37)."""
    agent = _load_agent(role)
    assert agent["canonical_pattern"] == "concurrent"


@pytest.mark.parametrize("role", sorted(TRADE_SECRET_ROLES))
def test_trade_secret_roles_declare_classification_propagation(role: str) -> None:
    agent = _load_agent(role)
    cps = agent.get("classification_propagation", [])
    assert "trade_secret" in cps, (
        f"{role} touches TRADE_SECRET data but agent.yaml does not "
        "declare classification_propagation: [trade_secret]"
    )


@pytest.mark.parametrize("role", sorted(PII_ROLES))
def test_pii_roles_declare_pii_classification(role: str) -> None:
    agent = _load_agent(role)
    cps = agent.get("classification_propagation", [])
    assert "pii" in cps, (
        f"{role} reads tokenised PII but classification_propagation does "
        "not include pii"
    )


@pytest.mark.parametrize("role", sorted(CONCURRENT_SIBLING_ROLES))
def test_concurrent_sibling_pair_declared(role: str) -> None:
    """Sprint 37's distinctive feature — assess + classify run in parallel."""
    agent = _load_agent(role)
    siblings = agent.get("concurrent_sibling_roles", [])
    assert siblings, (
        f"{role} runs in the Concurrent canonical pattern but "
        "concurrent_sibling_roles is empty"
    )
    # The sibling must be the other concurrent role
    other = (CONCURRENT_SIBLING_ROLES - {role}).pop()
    assert other in siblings, (
        f"{role} must declare {other} as a concurrent sibling"
    )


def test_decide_agent_declares_adaptive_hitl_gate() -> None:
    """Sprint 37.3 — Decide agent uses adaptive 3-band HITL gate."""
    decide = _load_agent("decide")
    assert decide.get("hitl_gate") is True
    assert decide.get("hitl_gate_kind") == "adaptive"
    consumed = decide.get("hitl_thresholds_consumed", [])
    assert "auto-clear-max-fraud-score" in consumed
    assert "escalate-min-fraud-score" in consumed
    assert "ring-indicator-force-escalate" in consumed


def test_decide_agent_routes_to_returns_ops_manager_role() -> None:
    """Per persona-binding model: hitl_persona is the role identifier."""
    decide = _load_agent("decide")
    assert decide["hitl_persona"] == "rebecca-hall-returns-ops-mgr"
    assert decide["hitl_channel"] == "teams-adaptive-card"


def test_decide_agent_declares_tier3_pii_unlock() -> None:
    """Sprint 37.3 — Tier-3 PII JIT unlock for fraud-hold re-identification."""
    decide = _load_agent("decide")
    assert decide.get("tier3_pii_unlock_webhook_secret", "").startswith("apex-hitl-")
    assert decide.get("tier3_pii_unlock_ttl_seconds") == 60
    purposes = decide.get("tier3_pii_unlock_authorised_purposes", [])
    assert "fraud_hold_re_identification" in purposes
    assert decide.get("audit_row_emit_separate_for_pii_unlock") is True


def test_decide_redacts_pii_and_trade_secret_in_card() -> None:
    decide = _load_agent("decide")
    redact = decide.get("adaptive_card_redact_classifications", [])
    assert "trade_secret" in redact
    assert "pii" in redact


def test_decide_emits_two_card_kinds() -> None:
    """Adaptive 3-band gate: review_card (medium) + hold_pii_unlock_card (high)."""
    decide = _load_agent("decide")
    kinds = decide.get("adaptive_card_kinds", [])
    assert "review_card" in kinds
    assert "hold_pii_unlock_card" in kinds


def test_act_agent_writes_to_fraud_case_with_idempotency() -> None:
    act = _load_agent("act")
    assert "CXML.FraudCase" in act["schemas_write"]
    assert "MERML.Refund" in act["schemas_write"]
    assert act["idempotency_keyed_on"] == "decision_id"
    assert act.get("ttl_check_seconds") == 60


def test_quantify_uses_loss_economics_path() -> None:
    """Loss Quantifier reads TRADE_SECRET via include_loss_economics=True."""
    quantify = _load_agent("quantify")
    assert any(
        t.endswith("get_fraud_score_basis") for t in quantify["tools"]
    )
    assert quantify.get("operator_obo_required") is True


def test_classify_does_not_require_operator_obo() -> None:
    """Fraud Specialist scores on tokenised graph — no OBO needed."""
    classify = _load_agent("classify")
    assert classify.get("operator_obo_required") is False


def test_learn_agent_emits_fraud_digest_daily() -> None:
    learn = _load_agent("learn")
    assert learn["redis_episodic_memory"] is True
    assert learn["fraud_digest_enabled"] is True
    assert learn["fraud_digest_persona"] == "rebecca-hall-returns-ops-mgr"
    assert learn["fraud_digest_cadence"] == "daily"
    assert learn["attribution_window_days"] == 90


# --- Fixture validation ----------------------------------------------------


def test_fixture_exists_and_parses() -> None:
    assert FIXTURE.exists()
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["fixture_id"].startswith("rc-returns-fraud-detection")


def test_fixture_exercises_all_three_adaptive_bands() -> None:
    """Fixture must cover all three adaptive-HITL bands."""
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    bands = {e["expected_fraud_score_band"] for e in data["events"]}
    assert bands == {"low", "medium", "high"}


def test_fixture_exercises_ring_detection() -> None:
    """At least one fixture event must trigger ring_indicator==true."""
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    rings = [e for e in data["events"] if e.get("expected_ring_indicator")]
    assert len(rings) >= 1
    assert all(e["expected_decision_class"] == "hold_with_pii_unlock" for e in rings)


def test_fixture_chain_behavior_threads_concurrent_pattern() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    behavior = data["expected_chain_behavior"]
    assert behavior["step_13_assess"]["concurrent_with_classify"] is True
    assert behavior["step_14_classify"]["concurrent_with_assess"] is True


def test_fixture_chain_behavior_threads_pii_unlock_for_high_score() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    decide = data["expected_chain_behavior"]["step_16_decide"]
    assert decide["hold_with_pii_unlock_count"] == 1
    assert decide["expected_pii_unlock_request_id_present_for_RET-HIGH-001"] is True


def test_fixture_audit_assertion_persona_binding_resolves() -> None:
    """Per persona-binding model: persona_id alongside principal."""
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assertions = data["audit_assertions"]
    assert assertions["operator_principal_resolves_via_persona_principal_bindings"] is True
    assert assertions["persona_id_recorded_alongside_principal"] is True
