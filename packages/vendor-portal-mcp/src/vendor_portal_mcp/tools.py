"""vendor-portal-mcp tool implementations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from apex_core.types import Classification
from mcp_common import McpError, McpErrorCode, ToolContract, traced_call

SERVER_NAME = "vendor-portal-mcp"
TOOL_VERSION = "1.0.0"


@runtime_checkable
class VendorBackend(Protocol):
    def status(self, vendor_id: str) -> dict | None: ...
    def orders(self, vendor_id: str, limit: int) -> list[dict]: ...
    def compliance_score(self, vendor_id: str) -> dict | None: ...


@dataclass
class InMemoryVendorBackend:
    statuses: dict[str, dict] = field(default_factory=dict)
    orders_by_vendor: dict[str, list[dict]] = field(default_factory=dict)
    compliance: dict[str, dict] = field(default_factory=dict)

    def status(self, vendor_id: str) -> dict | None:
        return self.statuses.get(vendor_id)

    def orders(self, vendor_id: str, limit: int) -> list[dict]:
        return self.orders_by_vendor.get(vendor_id, [])[:limit]

    def compliance_score(self, vendor_id: str) -> dict | None:
        return self.compliance.get(vendor_id)


VENDOR_BACKEND: VendorBackend = InMemoryVendorBackend()


def set_vendor_backend(backend: VendorBackend) -> None:
    global VENDOR_BACKEND
    VENDOR_BACKEND = backend


def get_vendor_status(
    vendor_id: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict:
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_vendor_status",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"vendor_id": vendor_id},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        row = VENDOR_BACKEND.status(vendor_id)
        if row is None:
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message=f"No vendor {vendor_id!r}",
            )
        ctx["result"] = row
        return row


def list_vendor_orders(
    vendor_id: str,
    limit: int = 50,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_vendor_orders",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"vendor_id": vendor_id, "limit": limit},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        rows = VENDOR_BACKEND.orders(vendor_id, limit)
        ctx["result"] = rows
        return rows


def get_vendor_compliance_score(
    vendor_id: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict:
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_vendor_compliance_score",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"vendor_id": vendor_id},
        classification_applied=[Classification.INTERNAL, Classification.TRADE_SECRET],
    ) as ctx:
        row = VENDOR_BACKEND.compliance_score(vendor_id)
        if row is None:
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message=f"No compliance score for vendor {vendor_id!r}",
            )
        ctx["result"] = row
        return row


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.get_vendor_status", version=TOOL_VERSION,
        description="Return the current portal status for a vendor.",
        classification_propagation=[Classification.INTERNAL],
    ),
    ToolContract(
        name=f"{SERVER_NAME}.list_vendor_orders", version=TOOL_VERSION,
        description="List recent orders for a vendor.",
        classification_propagation=[Classification.INTERNAL],
    ),
    ToolContract(
        name=f"{SERVER_NAME}.get_vendor_compliance_score", version=TOOL_VERSION,
        description="Return the compliance scorecard for a vendor.",
        classification_propagation=[Classification.INTERNAL, Classification.TRADE_SECRET],
    ),
]
