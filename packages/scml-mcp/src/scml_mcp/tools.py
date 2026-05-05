"""scml-mcp tool implementations — delegate to fabric-mcp with SCML scoping."""

from __future__ import annotations

from apex_core.types import Classification
from fabric_mcp import get_entity_by_key as _fabric_get_entity
from fabric_mcp import query_gold_view as _fabric_query_view
from mcp_common import ToolContract, traced_call

SERVER_NAME = "scml-mcp"
TOOL_VERSION = "1.0.0"
_REQUIRED_SCOPES = ["practice:rc"]


def get_sku_by_key(
    sku_natural: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict:
    """Look up an SCML SKU by its natural key."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_sku_by_key",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"sku_natural": sku_natural},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        row = _fabric_get_entity(
            "sku", sku_natural,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = row
        return row


def list_skus_by_supplier(
    supplier_key: str,
    limit: int = 100,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """List SKUs sourced from a given supplier."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_skus_by_supplier",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"supplier_key": supplier_key, "limit": limit},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        rows = _fabric_query_view(
            "gold_scml.sku", {"supplier_key": supplier_key}, limit,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = rows
        return rows


def list_shipments_by_destination(
    destination_key: str,
    limit: int = 100,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """List shipments headed to a given destination location."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_shipments_by_destination",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"destination_key": destination_key, "limit": limit},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        rows = _fabric_query_view(
            "gold_scml.shipment", {"destination_key": destination_key}, limit,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = rows
        return rows


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.get_sku_by_key", version=TOOL_VERSION,
        description="Look up an SCML SKU by its natural key.",
        classification_propagation=[Classification.INTERNAL, Classification.TRADE_SECRET],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.list_skus_by_supplier", version=TOOL_VERSION,
        description="List SKUs sourced from a given supplier.",
        classification_propagation=[Classification.INTERNAL, Classification.TRADE_SECRET],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.list_shipments_by_destination", version=TOOL_VERSION,
        description="List shipments headed to a given destination location.",
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES,
    ),
]
