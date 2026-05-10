"""Sprint 32 — RC-E2E-03 cold-chain agent manifest smoke tests.

Verifies every agent.yaml under
``services/rc/RC-E2E-03/scenarios/rc-cold-chain-excursion-mid-shift/agents/``
declares the production fields Sprint 32 requires:

- model is set (not "TBD")
- prompt_ref exists and the file is non-stub
- hitl_gate fields are wired when hitl_gate=true
- TRADE_SECRET-touching agents declare classification_propagation
- canonical_pattern matches the use-case orchestration_archetype (magentic)
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

SCENARIO_DIR = Path(__file__).resolve().parent
AGENTS_DIR = SCENARIO_DIR / "agents"

EXPECTED_ROLES = {"assess", "classify", "quantify", "decide", "act", "learn", "pricing"}
TRADE_SECRET_ROLES = {"quantify", "pricing", "decide", "act", "learn"}
HITL_GATE_ROLES = {"decide", "pricing"}


def _load_agent(role: str) -> dict:
    path = AGENTS_DIR / role / "agent.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_prompt(role: str) -> str:
    agent = _load_agent(role)
    prompt_path = AGENTS_DIR / role / agent["prompt_ref"]
    return prompt_path.read_text(encoding="utf-8")


def test_all_seven_roles_present() -> None:
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
def test_canonical_pattern_is_magentic(role: str) -> None:
    """Per use-case.yaml orchestration_archetype: magentic."""
    agent = _load_agent(role)
    assert agent["canonical_pattern"] == "magentic"


@pytest.mark.parametrize("role", sorted(TRADE_SECRET_ROLES))
def test_trade_secret_roles_declare_classification_propagation(role: str) -> None:
    agent = _load_agent(role)
    cps = agent.get("classification_propagation", [])
    assert "trade_secret" in cps, (
        f"{role} touches TRADE_SECRET data but agent.yaml does not "
        "declare classification_propagation: [trade_secret]"
    )


@pytest.mark.parametrize("role", sorted(HITL_GATE_ROLES))
def test_hitl_gate_roles_wire_threshold_secrets(role: str) -> None:
    agent = _load_agent(role)
    assert agent.get("hitl_gate") is True
    assert agent.get("hitl_gate_secret_prefix", "").startswith("apex-hitl-")
    consumed = agent.get("hitl_thresholds_consumed", [])
    assert "markdown-pct-above" in consumed


def test_decide_agent_routes_to_marisol() -> None:
    decide = _load_agent("decide")
    assert decide["hitl_persona"] == "marisol-reyes-store-ops"
    assert decide["hitl_channel"] == "teams-adaptive-card"
    assert "trade_secret" in decide["adaptive_card_redact_classifications"]


def test_act_agent_writes_to_merml_markdown_with_idempotency() -> None:
    act = _load_agent("act")
    assert "MERML.Markdown" in act["schemas_write"]
    assert act["idempotency_keyed_on"] == "decision_id"


def test_pricer_uses_redis_episodic_memory() -> None:
    pricing = _load_agent("pricing")
    assert pricing["redis_episodic_memory"] is True
    assert pricing["learning_loop_window_days"] >= 30


def test_learn_agent_emits_ledger_and_shift_digest() -> None:
    learn = _load_agent("learn")
    assert learn["redis_episodic_memory"] is True
    assert learn["shift_digest_enabled"] is True
    assert learn["shift_digest_persona"] == "marisol-reyes-store-ops"


def test_operator_obo_required_on_trade_secret_writes_and_reads() -> None:
    """quantify / pricing / act read or write TRADE_SECRET data — operator OBO required."""
    for role in ("quantify", "pricing", "act"):
        agent = _load_agent(role)
        assert agent.get("operator_obo_required") is True, (
            f"{role} agent reads/writes TRADE_SECRET data but "
            "operator_obo_required is not set"
        )
