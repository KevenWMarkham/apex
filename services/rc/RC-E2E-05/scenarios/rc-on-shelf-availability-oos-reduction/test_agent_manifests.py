"""Sprint 35 — RC-E2E-05 OSA agent manifest smoke tests.

Verifies every agent.yaml under
``services/rc/RC-E2E-05/scenarios/rc-on-shelf-availability-oos-reduction/agents/``
declares the production fields Sprint 35 requires:

- model is set (not "TBD")
- prompt_ref exists and the file is non-stub
- hitl_gate fields wired when hitl_gate=true
- canonical_pattern matches the use-case orchestration_archetype (sequential)
- RC-E2E-05 is INTERNAL only — no TRADE_SECRET / PII propagation
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

SCENARIO_DIR = Path(__file__).resolve().parent
AGENTS_DIR = SCENARIO_DIR / "agents"
FIXTURE = SCENARIO_DIR / "fixtures" / "shelf-gap-event.json"

EXPECTED_ROLES = {"assess", "classify", "quantify", "decide", "act", "learn"}
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
def test_canonical_pattern_is_sequential(role: str) -> None:
    """Per RC-E2E-05 use-case orchestration_archetype: sequential (Sprint 35)."""
    agent = _load_agent(role)
    assert agent["canonical_pattern"] == "sequential"


@pytest.mark.parametrize("role", sorted(EXPECTED_ROLES))
def test_no_role_propagates_trade_secret_or_pii(role: str) -> None:
    """RC-E2E-05 domain is INTERNAL only — no margin / customer data."""
    agent = _load_agent(role)
    cps = agent.get("classification_propagation", [])
    assert "trade_secret" not in cps, (
        f"{role}: RC-E2E-05 should not propagate trade_secret"
    )
    assert "pii" not in cps, (
        f"{role}: RC-E2E-05 should not propagate pii"
    )
    assert "internal" in cps


@pytest.mark.parametrize("role", sorted(HITL_GATE_ROLES))
def test_hitl_gate_roles_wire_threshold_secrets(role: str) -> None:
    agent = _load_agent(role)
    assert agent.get("hitl_gate") is True
    assert agent.get("hitl_gate_secret_prefix", "").startswith("apex-hitl-")
    consumed = agent.get("hitl_thresholds_consumed", [])
    assert "auto-clear-max-total-tasks" in consumed
    assert "auto-clear-max-p0-tasks" in consumed


def test_decide_agent_routes_to_jamie() -> None:
    decide = _load_agent("decide")
    assert decide["hitl_persona"] == "jamie-oconnor-store-manager"
    assert decide["hitl_channel"] == "teams-adaptive-card"


def test_decide_agent_emits_per_associate_cards() -> None:
    """OSA's distinctive feature — Decide fans out walkable per-associate cards."""
    decide = _load_agent("decide")
    kinds = decide.get("adaptive_card_kinds", [])
    assert "review_card" in kinds
    assert "per_associate_card" in kinds


def test_decide_redact_classifications_empty() -> None:
    """RC-E2E-05 is INTERNAL only — no redaction needed."""
    decide = _load_agent("decide")
    assert decide.get("adaptive_card_redact_classifications") == []


def test_act_agent_writes_to_scml_inventory_with_idempotency() -> None:
    act = _load_agent("act")
    assert "SCML.Inventory" in act["schemas_write"]
    assert act["idempotency_keyed_on"] == "dispatch_id_associate_id_task_order"


def test_quantify_uses_assignment_basis_tool() -> None:
    quantify = _load_agent("quantify")
    assert any(
        t.endswith("get_shelf_gap_assignment_basis") for t in quantify["tools"]
    )


def test_learn_agent_emits_shift_digest_per_shift() -> None:
    learn = _load_agent("learn")
    assert learn["redis_episodic_memory"] is True
    assert learn["shift_digest_enabled"] is True
    assert learn["shift_digest_persona"] == "jamie-oconnor-store-manager"
    assert learn["shift_digest_cadence"] == "end_of_shift"


def test_no_role_requires_operator_obo() -> None:
    """RC-E2E-05 reads + writes are agent-identity-scoped, not operator-OBO."""
    for role in EXPECTED_ROLES:
        agent = _load_agent(role)
        # Default false when key absent; explicit false when set.
        assert not agent.get("operator_obo_required", False), (
            f"{role}: OSA reads/writes are INTERNAL — no operator OBO required"
        )


# --- Fixture validation ----------------------------------------------------


def test_fixture_exists_and_parses() -> None:
    assert FIXTURE.exists()
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["fixture_id"].startswith("rc-on-shelf-availability-oos-reduction")


def test_fixture_covers_p0_critical_and_lower_priorities() -> None:
    """Fixture must exercise both KVI stockout (P0) and silent low-stock (P2)."""
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    classes = {e["expected_priority_class"] for e in data["shelf_gap_events"]}
    assert "P0_critical" in classes
    # Need at least one non-P0 to prove the priority rubric does what it should.
    assert classes - {"P0_critical"}


def test_fixture_chain_behavior_specifies_hitl_due_to_p0() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    decide = data["expected_chain_behavior"]["step_16_decide"]
    assert decide["decision_class"] == "hitl_required"
    assert decide["expected_hitl_persona"] == "jamie-oconnor-store-manager"
    assert "P0_critical" in decide["reason"]


def test_fixture_audit_assertion_no_trade_secret_or_pii() -> None:
    """The smoke fixture asserts RC-E2E-05 doesn't bleed TS/PII classification."""
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assertions = data["audit_assertions"]
    assert assertions["no_trade_secret_classification_present"] is True
    assert assertions["no_pii_classification_present"] is True
