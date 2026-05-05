"""ercml-mcp tool implementations."""

from __future__ import annotations

from apex_core.types import Classification
from fabric_mcp import get_entity_by_key as _fabric_get_entity
from fabric_mcp import query_gold_view as _fabric_query_view
from mcp_common import ToolContract, traced_call

SERVER_NAME = "ercml-mcp"
TOOL_VERSION = "1.0.0"
_REQUIRED_SCOPES = ["practice:er"]


def get_meter_by_key(
    meter_key: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict:
    """Return the canonical Meter row."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_meter_by_key",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"meter_key": meter_key},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        row = _fabric_get_entity(
            "meter", meter_key,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = row
        return row


def list_recent_readings(
    meter_key: str,
    limit: int = 100,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """List recent MeterReadings for a meter."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_recent_readings",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"meter_key": meter_key, "limit": limit},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        rows = _fabric_query_view(
            "gold_ercml.meter_reading", {"meter_key": meter_key}, limit,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = rows
        return rows


def list_grid_events_by_type(
    event_type: str,
    limit: int = 100,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """List grid events of a specific type."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_grid_events_by_type",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"event_type": event_type, "limit": limit},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        rows = _fabric_query_view(
            "gold_ercml.grid_event", {"event_type": event_type}, limit,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = rows
        return rows


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.get_meter_by_key", version=TOOL_VERSION,
        description="Return an ERCML Meter row by key.",
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.list_recent_readings", version=TOOL_VERSION,
        description="List recent MeterReadings for a meter.",
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.list_grid_events_by_type", version=TOOL_VERSION,
        description="List grid events of a specific type.",
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES,
    ),
]
