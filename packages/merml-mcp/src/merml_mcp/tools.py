"""merml-mcp tool implementations."""

from __future__ import annotations

from apex_core.types import Classification
from fabric_mcp import query_gold_view as _fabric_query_view
from mcp_common import McpError, McpErrorCode, ToolContract, traced_call

SERVER_NAME = "merml-mcp"
TOOL_VERSION = "1.0.0"
_REQUIRED_SCOPES = ["practice:rc"]


def get_current_price(
    sku_key: str,
    location_key: str | None = None,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict:
    """Return the most-recent active Price row for (sku, location)."""
    filters: dict[str, object] = {"sku_key": sku_key, "kind": "REGULAR"}
    if location_key is not None:
        filters["location_key"] = location_key
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_current_price",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"sku_key": sku_key, "location_key": location_key},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        rows = _fabric_query_view(
            "gold_merml.price", filters, 1,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        if not rows:
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message=f"No active price for sku {sku_key!r}",
            )
        ctx["result"] = rows[0]
        return rows[0]


def list_active_promotions(
    limit: int = 100,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """List currently-active promotions."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_active_promotions",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"limit": limit},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        rows = _fabric_query_view(
            "gold_merml.promotion", {"is_active": True}, limit,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = rows
        return rows


def list_recent_markdowns(
    sku_key: str,
    limit: int = 50,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """List recent markdown events on a specific SKU."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_recent_markdowns",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"sku_key": sku_key, "limit": limit},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        rows = _fabric_query_view(
            "gold_merml.markdown", {"sku_key": sku_key}, limit,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = rows
        return rows


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.get_current_price", version=TOOL_VERSION,
        description="Return the most-recent active Price row for a SKU (optionally by location).",
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.list_active_promotions", version=TOOL_VERSION,
        description="List currently-active promotions.",
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.list_recent_markdowns", version=TOOL_VERSION,
        description="List recent markdown events on a specific SKU.",
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES,
    ),
]
