"""Sprint 39 — RC-E2E-09 FSMA-204 Handoff agent manifest smoke tests.

Verifies:

- Only 3 active agent dirs exist (assess, classify, learn) — RC-E2E-09's
  Handoff flow doesn't use quantify/decide/act
- Each agent.yaml declares canonical_pattern: handoff
- Handoff source/target wiring is correct: assess → classify → learn
- Compliance Specialist (classify) declares conditional attestation HITL
- The Briefer (learn) declares scml_lot_ownership: sole_writer
- Cross-service consumers (RC-E2E-03 + RC-E2E-07) listed on the Briefer
- Cross-service tools resolve through Agent Framework loader

Plus fixture validation for the FSMA-204 recall event.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

SCENARIO_DIR = Path(__file__).resolve().parent
AGENTS_DIR = SCENARIO_DIR / "agents"
FIXTURE = SCENARIO_DIR / "fixtures" / "fsma-recall-event.json"

# RC-E2E-09 Handoff flow — only 3 active roles (Sprint Plan §"3-agent fleet").
ACTIVE_ROLES = {"assess", "classify", "learn"}


def _load_agent(role: str) -> dict:
    path = AGENTS_DIR / role / "agent.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_prompt(role: str) -> str:
    agent = _load_agent(role)
    prompt_path = AGENTS_DIR / role / agent["prompt_ref"]
    return prompt_path.read_text(encoding="utf-8")


# --- Active-role layout (3-agent flow) -------------------------------------


def test_active_roles_are_three() -> None:
    """RC-E2E-09 Handoff is a 3-agent flow — only assess + classify + learn."""
    on_disk = {p.name for p in AGENTS_DIR.iterdir() if p.is_dir()}
    assert on_disk == ACTIVE_ROLES, (
        f"RC-E2E-09 must have exactly 3 active agent dirs (assess/classify/"
        f"learn) for the Handoff flow; found {sorted(on_disk)}"
    )


@pytest.mark.parametrize("role", sorted(ACTIVE_ROLES))
def test_each_agent_has_real_model(role: str) -> None:
    agent = _load_agent(role)
    assert agent["model"] != "TBD"
    assert agent["model"].startswith("gpt-")


@pytest.mark.parametrize("role", sorted(ACTIVE_ROLES))
def test_each_prompt_is_authored(role: str) -> None:
    body = _load_prompt(role)
    assert "TBD" not in body, f"{role} prompt is still stub"
    assert len(body) > 500


@pytest.mark.parametrize("role", sorted(ACTIVE_ROLES))
def test_each_agent_has_versions(role: str) -> None:
    agent = _load_agent(role)
    assert agent.get("prompt_version") == "1.0.0"
    assert agent.get("manifest_version") == "1.0.0"


@pytest.mark.parametrize("role", sorted(ACTIVE_ROLES))
def test_canonical_pattern_is_handoff(role: str) -> None:
    """Per RC-E2E-09 use-case orchestration_archetype: handoff (Sprint 39)."""
    agent = _load_agent(role)
    assert agent["canonical_pattern"] == "handoff"


# --- Handoff sequence wiring -----------------------------------------------


def test_assess_declares_handoff_target_classify() -> None:
    """Step 1 of Handoff chain — Analyst hands off to Compliance Specialist."""
    assess = _load_agent("assess")
    assert assess["handoff_target_role"] == "classify"


def test_classify_declares_full_handoff_chain() -> None:
    """Step 2 of Handoff chain — middle agent declares both source + target."""
    classify = _load_agent("classify")
    assert classify["handoff_source_role"] == "assess"
    assert classify["handoff_target_role"] == "learn"


def test_learn_is_terminal_handoff_step() -> None:
    """Step 3 (terminal) — Briefer has no further handoff."""
    learn = _load_agent("learn")
    assert learn["handoff_source_role"] == "classify"
    assert learn["handoff_target_role"] is None


# --- Persona + HITL wiring -------------------------------------------------


def test_classify_routes_to_compliance_officer_role() -> None:
    classify = _load_agent("classify")
    assert classify["hitl_persona"] == "compliance-officer-fsma-204"
    assert classify["hitl_channel"] == "teams-adaptive-card"


def test_classify_uses_conditional_attestation_gate() -> None:
    """Sprint 39 distinctive — only Class I + large-scope require attestation."""
    classify = _load_agent("classify")
    assert classify["hitl_gate"] is True
    assert classify["hitl_gate_kind"] == "conditional_attestation"
    consumed = classify["hitl_thresholds_consumed"]
    assert "scope-size-attestation-threshold" in consumed
    assert "require-attestation-for-class-I" in consumed


def test_classify_emits_attestation_only_card() -> None:
    """RC-E2E-09's distinctive feature — single-action attestation card."""
    classify = _load_agent("classify")
    kinds = classify.get("adaptive_card_kinds", [])
    assert kinds == ["compliance_attestation_card"]


def test_assess_and_learn_have_no_hitl_gate() -> None:
    """Only the Compliance Specialist gates; Analyst and Briefer don't."""
    assert _load_agent("assess")["hitl_gate"] is False
    assert _load_agent("learn")["hitl_gate"] is False


# --- SCML.Lot ownership boundary (Sprint 39.4) -----------------------------


def test_learn_is_sole_writer_of_scml_lot() -> None:
    """Sprint 39.4 — RC-E2E-09's Briefer is the sole SCML.Lot writer."""
    learn = _load_agent("learn")
    assert "SCML.Lot" in learn["schemas_write"]
    assert learn["scml_lot_ownership"] == "sole_writer"


def test_learn_declares_cross_service_read_consumers() -> None:
    """Sprint 39.4 — RC-E2E-03 + RC-E2E-07 read provenance via MCP."""
    learn = _load_agent("learn")
    consumers = learn["cross_service_read_consumers"]
    consumer_services = {c["service_code"] for c in consumers}
    assert consumer_services == {"RC-E2E-03", "RC-E2E-07"}
    for c in consumers:
        assert c["via_mcp_tool"] == "rc_e2e_09.get_lot_provenance"


def test_assess_and_classify_do_not_write_scml_lot() -> None:
    """Sprint 39.4 — only the Briefer writes; assess + classify are read-only."""
    for role in ("assess", "classify"):
        agent = _load_agent(role)
        assert "SCML.Lot" not in agent["schemas_write"], (
            f"{role} agent.yaml declares SCML.Lot write — violates ownership "
            "boundary (Sprint 39.4)"
        )


# --- Cross-service read tool wiring ----------------------------------------


def test_assess_can_read_excursion_panel_cross_service() -> None:
    """Sprint 39 cross-service: when recall is excursion-linked, Analyst reads RC-E2E-03's panel."""
    assess = _load_agent("assess")
    assert "rc_e2e_03.get_excursion_decision_panel" in assess["tools"]


def test_no_role_propagates_trade_secret_or_pii() -> None:
    """RC-E2E-09 domain is INTERNAL only — compliance is not TRADE_SECRET / PII."""
    for role in ACTIVE_ROLES:
        agent = _load_agent(role)
        cps = agent.get("classification_propagation", [])
        assert "trade_secret" not in cps
        assert "pii" not in cps
        assert "internal" in cps


def test_learn_emits_recall_digest_daily_to_compliance_officer() -> None:
    learn = _load_agent("learn")
    assert learn["redis_episodic_memory"] is True
    assert learn["recall_digest_enabled"] is True
    assert learn["recall_digest_persona"] == "compliance-officer-fsma-204"
    assert learn["recall_digest_cadence"] == "daily"
    assert learn["attribution_window_days"] == 90


# --- Fixture validation ----------------------------------------------------


def test_fixture_exists_and_parses() -> None:
    assert FIXTURE.exists()
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["fixture_id"].startswith("rc-perishable-waste-reduction")


def test_fixture_covers_all_three_recall_classes() -> None:
    """Fixture exercises Class I (attestation) + Class II (auto) + no_recall."""
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    classes = {l["expected_recall_class"] for l in data["affected_lots"]}
    assert "I" in classes
    assert "II" in classes
    assert "no_recall" in classes


def test_fixture_threads_handoff_sequence() -> None:
    """Chain behavior must declare the Handoff sequence assess → classify → learn."""
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    behavior = data["expected_chain_behavior"]
    assert behavior["step_13_assess"]["handoff_target"] == "classify"
    assert behavior["step_14_classify"]["handoff_source"] == "assess"
    assert behavior["step_14_classify"]["handoff_target"] == "learn"
    assert behavior["step_18_learn"]["handoff_source"] == "classify"


def test_fixture_specifies_attestation_required_for_class_I_only() -> None:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    class_I = next(l for l in data["affected_lots"] if l["expected_recall_class"] == "I")
    class_II = next(l for l in data["affected_lots"] if l["expected_recall_class"] == "II")
    assert class_I["expected_compliance_attestation_required"] is True
    assert class_II["expected_compliance_attestation_required"] is False


def test_fixture_validates_cross_service_assertions() -> None:
    """Sprint 39.4 boundary — fixture asserts no other service writes SCML.Lot."""
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    cross = data["cross_service_assertions"]
    assert cross["rc_e2e_03_classify_can_call_get_lot_provenance"] is True
    assert cross["rc_e2e_07_assess_can_call_get_lot_provenance"] is True
    assert cross["no_service_other_than_rc_e2e_09_can_call_commit_lot_event"] is True


def test_fixture_lists_invalidation_paths_for_each_lot() -> None:
    """Each lot's commit_lot_event emits invalidation keys to RC-E2E-03 + RC-E2E-07."""
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    paths = data["cross_service_assertions"]["expected_invalidation_paths"]
    # 2 services × 2 lots written (lot C is no_recall but still trace_audit_pass) = 4 paths min
    services_seen = {p.split("/")[0] for p in paths}
    assert "rc-e2e-03" in services_seen
    assert "rc-e2e-07" in services_seen
