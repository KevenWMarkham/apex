"""Adaptive-card builder for Teams HITL presentation.

Emits a minimal v1.5 Adaptive Card payload. Sprint 11 ships the JSON
builder; Sprint 17 wires the Graph `sendActivity` call that delivers the
card to an approver's Teams channel.
"""

from __future__ import annotations

from typing import Any


def build_adaptive_card(
    *,
    title: str,
    subtitle: str,
    decision_id: str,
    proposal: dict[str, Any],
    approver_group: str,
) -> dict[str, Any]:
    """Return an Adaptive Card 1.5 payload for an HITL approval prompt."""
    facts = [
        {"title": str(k), "value": str(v)[:200]}
        for k, v in proposal.items()
    ]
    return {
        "type": "AdaptiveCard",
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.5",
        "body": [
            {"type": "TextBlock", "text": title, "weight": "Bolder", "size": "Medium", "wrap": True},
            {"type": "TextBlock", "text": subtitle, "isSubtle": True, "wrap": True},
            {"type": "FactSet", "facts": facts},
            {
                "type": "TextBlock",
                "text": f"Approver group: {approver_group}",
                "isSubtle": True, "size": "Small",
            },
        ],
        "actions": [
            {
                "type": "Action.Submit",
                "title": "Approve",
                "data": {"action": "approve", "decision_id": decision_id},
            },
            {
                "type": "Action.Submit",
                "title": "Reject",
                "data": {"action": "reject", "decision_id": decision_id},
            },
            {
                "type": "Action.Submit",
                "title": "Modify",
                "data": {"action": "modify", "decision_id": decision_id},
            },
        ],
    }
