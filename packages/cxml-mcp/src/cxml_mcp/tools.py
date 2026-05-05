"""cxml-mcp tool implementations — PII/PCI classification propagation."""

from __future__ import annotations

from apex_core.types import Classification
from fabric_mcp import get_entity_by_key as _fabric_get_entity
from fabric_mcp import query_gold_view as _fabric_query_view
from mcp_common import ToolContract, traced_call

SERVER_NAME = "cxml-mcp"
TOOL_VERSION = "1.0.0"
_REQUIRED_SCOPES = ["practice:rc"]


def get_customer_by_key(
    customer_natural: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict:
    """Return the tokenised Customer canonical row."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_customer_by_key",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"customer_natural": customer_natural},
        classification_applied=[Classification.PII],
    ) as ctx:
        row = _fabric_get_entity(
            "customer", customer_natural,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = row
        return row


def list_orders_by_customer(
    customer_key: str,
    limit: int = 50,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """List orders for a customer (totals only; payment method remains PCI-tokenised)."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_orders_by_customer",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"customer_key": customer_key, "limit": limit},
        classification_applied=[Classification.PCI],
    ) as ctx:
        rows = _fabric_query_view(
            "gold_cxml.order", {"customer_key": customer_key}, limit,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = rows
        return rows


def list_interactions_by_customer(
    customer_key: str,
    limit: int = 100,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """List customer interactions across channels."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_interactions_by_customer",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"customer_key": customer_key, "limit": limit},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        rows = _fabric_query_view(
            "gold_cxml.interaction", {"customer_key": customer_key}, limit,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = rows
        return rows


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.get_customer_by_key", version=TOOL_VERSION,
        description="Return the tokenised Customer canonical row.",
        classification_propagation=[Classification.PII],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.list_orders_by_customer", version=TOOL_VERSION,
        description="List orders for a customer.",
        classification_propagation=[Classification.PII, Classification.PCI],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.list_interactions_by_customer", version=TOOL_VERSION,
        description="List customer interactions across channels.",
        classification_propagation=[Classification.INTERNAL],
        required_scopes=_REQUIRED_SCOPES,
    ),
]
