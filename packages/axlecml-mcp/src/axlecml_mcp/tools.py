"""axlecml-mcp tool implementations."""

from __future__ import annotations

from apex_core.types import Classification
from fabric_mcp import get_entity_by_key as _fabric_get_entity
from fabric_mcp import query_gold_view as _fabric_query_view
from mcp_common import ToolContract, traced_call

SERVER_NAME = "axlecml-mcp"
TOOL_VERSION = "1.0.0"
_REQUIRED_SCOPES = ["practice:axle"]


def get_equipment_by_key(
    equipment_key: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict:
    """Return the canonical Equipment row."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_equipment_by_key",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"equipment_key": equipment_key},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        row = _fabric_get_entity(
            "equipment", equipment_key,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = row
        return row


def list_production_events(
    equipment_key: str,
    limit: int = 100,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """List production events for a specific equipment."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_production_events",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"equipment_key": equipment_key, "limit": limit},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        rows = _fabric_query_view(
            "gold_axlecml.production_event", {"equipment_key": equipment_key}, limit,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = rows
        return rows


def list_recent_quality_results(
    equipment_key: str,
    limit: int = 50,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """List recent quality results on a specific equipment."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_recent_quality_results",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"equipment_key": equipment_key, "limit": limit},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        rows = _fabric_query_view(
            "gold_axlecml.quality_result", {"equipment_key": equipment_key}, limit,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = rows
        return rows


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.get_equipment_by_key", version=TOOL_VERSION,
        description="Return an AXLECML Equipment row by key.",
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.list_production_events", version=TOOL_VERSION,
        description="List production events for a specific equipment.",
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.list_recent_quality_results", version=TOOL_VERSION,
        description="List recent quality results on a specific equipment.",
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES,
    ),
]
