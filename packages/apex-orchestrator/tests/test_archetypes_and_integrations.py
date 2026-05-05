"""Tests for the archetype catalog + Teams/Copilot-Studio stubs."""

from __future__ import annotations

from apex_orchestrator import (
    ARCHETYPES,
    build_adaptive_card,
    copilot_studio_skill_stub,
)


class TestArchetypes:
    def test_exactly_47_entries(self) -> None:
        assert len(ARCHETYPES) == 47

    def test_first_ten_are_impl(self) -> None:
        impl_count = sum(1 for a in ARCHETYPES if a.status == "impl")
        assert impl_count == 10

    def test_ids_unique(self) -> None:
        ids = [a.archetype_id for a in ARCHETYPES]
        assert len(set(ids)) == len(ids)


class TestTeamsCard:
    def test_card_shape(self) -> None:
        card = build_adaptive_card(
            title="Approve markdown",
            subtitle="Low-margin SKUs",
            decision_id="dec-1",
            proposal={"sku": "sku-1", "delta_pct": -30},
            approver_group="rc-store-ops",
        )
        assert card["type"] == "AdaptiveCard"
        assert card["version"] == "1.5"
        titles = [a["title"] for a in card["actions"]]
        assert {"Approve", "Reject", "Modify"}.issubset(set(titles))

    def test_facts_populated(self) -> None:
        card = build_adaptive_card(
            title="t", subtitle="s",
            decision_id="d", proposal={"a": 1, "b": "two"},
            approver_group="g",
        )
        facts = next(b for b in card["body"] if b["type"] == "FactSet")["facts"]
        assert {f["title"] for f in facts} == {"a", "b"}


class TestCopilotStudio:
    def test_payload_shape(self) -> None:
        payload = copilot_studio_skill_stub(
            skill_name="apex-approvals",
            decision_id="dec-1",
            proposal={"x": 1},
        )
        assert payload["skill"] == "apex-approvals"
        assert payload["action"] == "decide"
        assert "action" in payload["output_schema"]
