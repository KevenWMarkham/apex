"""Copilot Studio skill-action stub.

Sprint 11 ships the payload shape. Sprint 17 wires it into a published
Copilot Studio skill that invokes the same decision flow via MCP.
"""

from __future__ import annotations

from typing import Any


def copilot_studio_skill_stub(
    *,
    skill_name: str,
    decision_id: str,
    proposal: dict[str, Any],
) -> dict[str, Any]:
    """Return the Copilot-Studio-friendly payload for a decision proposal."""
    return {
        "skill": skill_name,
        "action": "decide",
        "input": {
            "decision_id": decision_id,
            "proposal": proposal,
        },
        "output_schema": {
            "action": "enum:approve|reject|modify",
            "rationale": "string",
            "approver_id": "string",
        },
    }
