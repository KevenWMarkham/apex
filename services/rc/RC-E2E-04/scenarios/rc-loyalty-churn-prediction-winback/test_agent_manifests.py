"""Sprint 34 — RC-E2E-04 loyalty-churn agent manifest smoke tests.

Verifies every agent.yaml under
``services/rc/RC-E2E-04/scenarios/rc-loyalty-churn-prediction-winback/agents/``
declares the production fields Sprint 34 requires:

- model is set (not "TBD")
- prompt_ref exists and the file is non-stub
- hitl_gate fields are wired when hitl_gate=true
- Decide agent declares the Tier-3 PII unlock pattern fields per Sprint 34.3
- TRADE_SECRET-touching agents declare classification_propagation
- canonical_pattern matches the use-case orchestration_archetype (sequential)
- PII-touching agents propagate Classification.PII (tokenised)
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

SCENARIO_DIR = Path(__file__).resolve().parent
AGENTS_DIR = SCENARIO_DIR / "agents"
FIXTURE = SCENARIO_DIR / "fixtures" / "winback-cohort.json"

EXPECTED_ROLES = {"assess", "classify", "quantify", "decide", "act", "learn"}
TRADE_SECRET_ROLES = {"quantify", "decide", "act", "learn"}
PII_ROLES = {"assess", "classify", "quantify", "decide", "act", "learn"}
HITL_GATE_ROLES = {"decide"}


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
    assert agent["model"].startswith("gpt-"), f"{role} model {agent['model']!r} unexpected"


@pytest.mark.parametrize("role", sorted(EXPECTED_ROLES))
def test_each_prompt_is_authored(role: str) -> None:
    body = _load_prompt(role)
    assert "TBD" not in body, f"{role} prompt is still stub (contains TBD)"
    assert len(body) > 500, f"{role} prompt suspiciously short ({len(body)} chars)"


@pytest.mark.parametrize("role", sorted(EXPECTED_ROLES))
def test_each_agent_has_prompt_version_and_manifest_version(role: str) -> None:
    agent = _load_agent(role)
    assert agent.get("prompt_version") == "1.0.0"
    assert agent.get("manifest_version") == "1.0.0"


@pytest.mark.parametrize("role", sorted(EXPECTED_ROLES))
def test_canonical_pattern_is_sequential(role: str) -> None:
    """Per RC-E2E-04 use-case orchestration_archetype: sequential (Sprint 34)."""
    agent = _load_agent(role)
    assert agent["canonical_pattern"] == "sequential"


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


@pytest.mark.parametrize("role", sorted(HITL_GATE_ROLES))
def test_hitl_gate_roles_wire_threshold_secrets(role: str) -> None:
    agent = _load_agent(role)
    assert agent.get("hitl_gate") is True
    assert agent.get("hitl_gate_secret_prefix", "").startswith("apex-hitl-")
    consumed = agent.get("hitl_thresholds_consumed", [])
    assert "winback-offer-above-pct" in consumed
    assert "tier-3-pii-unlock-required" in consumed


def test_decide_agent_routes_to_maya() -> None:
    decide = _load_agent("decide")
    assert decide["hitl_persona"] == "maya-patel-loyalty-crm-director"
    assert decide["hitl_channel"] == "teams-adaptive-card"


def test_decide_agent_declares_tier3_pii_unlock_pattern() -> None:
    """Sprint 34.3 — Tier-3 PII JIT unlock fields."""
    decide = _load_agent("decide")
    assert decide.get("tier3_pii_unlock_webhook_secret", "").startswith("apex-hitl-")
    assert decide.get("tier3_pii_unlock_ttl_seconds") == 60
    purposes = decide.get("tier3_pii_unlock_authorised_purposes", [])
    assert "winback_offer_distribution" in purposes
    assert decide.get("audit_row_emit_separate_for_pii_unlock") is True


def test_decide_redacts_pii_in_adaptive_card() -> None:
    decide = _load_agent("decide")
    redact = decide.get("adaptive_card_redact_classifications", [])
    assert "trade_secret" in redact
    assert "pii" in redact   # tokenised PII still hidden in card body


def test_act_agent_writes_to_cxml_campaign_with_idempotency() -> None:
    act = _load_agent("act")
    assert "CXML.Campaign" in act["schemas_write"]
    assert act["idempotency_keyed_on"] == "campaign_natural"
    assert act.get("ttl_check_seconds") == 60


def test_quantify_uses_winback_basis_tool() -> None:
    quantify = _load_agent("quantify")
    assert any(t.endswith("get_winback_offer_basis") for t in quantify["tools"])
    assert quantify.get("operator_obo_required") is True


def test_learn_agent_emits_ledger_and_campaign_digest() -> None:
    learn = _load_agent("learn")
    assert learn["redis_episodic_memory"] is True
    assert learn["campaign_digest_enabled"] is True
    assert learn["campaign_digest_persona"] == "maya-patel-loyalty-crm-director"
    assert learn["campaign_digest_cadence_days"] == 7
    assert learn["attribution_window_days"] == 30


def test_assess_classify_do_not_require_operator_obo() -> None:
    """Cohort + consent reads operate on tokenised PII; no OBO needed."""
    for role in ("assess", "classify"):
        agent = _load_agent(role)
        assert agent.get("operator_obo_required") is False, (
            f"{role}: cohort reads should not require operator OBO"
        )


# --- Fixture validation ----------------------------------------------------


def test_fixture_exists_and_parses() -> None:
    assert FIXTURE.exists()
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["fixture_id"].startswith("rc-loyalty-churn-prediction-winback")


def test_fixture_cohort_covers_eligibility_classes() -> None:
    """Fixture must exercise all eligibility paths the chain produces."""
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    cohort = data["cohort"]
    expected_eligibilities = {
        m.get("expected_winback_eligibility", "eligible") for m in cohort
    }
    # Must hit at least: eligible + ineligible_consent + ineligible_recent_winback
    assert "eligible" in expected_eligibilities
    assert "ineligible_consent" in expected_eligibilities
    assert "ineligible_recent_winback" in expected_eligibilities


def test_fixture_expected_chain_behavior_threads_pii_unlock() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    behavior = data["expected_chain_behavior"]
    assert behavior["step_16_decide"]["decision_class"] == "hitl_required"
    post_approval = behavior["step_16_decide_post_approval"]
    assert post_approval["should_invoke"] == "tokenizer-mcp.bulk_detokenize"
    assert post_approval["ttl_seconds"] == 60
    assert post_approval["purpose"] == "winback_offer_distribution"
