"""fabric-mcp tool implementations (Gold / OneLake reads)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from apex_core.types import Classification
from mcp_common import McpError, McpErrorCode, ToolContract, traced_call

TOOL_VERSION = "1.0.0"
SERVER_NAME = "fabric-mcp"


@runtime_checkable
class FabricBackend(Protocol):
    """Minimal protocol for OneLake / Warehouse read paths."""

    def get_entity(self, entity_type: str, key: str) -> dict[str, Any] | None:
        """Return the entity row for ``(entity_type, key)``, or None when absent."""

    def query_view(
        self, view_name: str, filters: dict[str, Any], limit: int
    ) -> list[dict[str, Any]]:
        """Return up to ``limit`` rows of ``view_name`` whose columns equal every filter value."""

    def classifications(self, entity_type: str) -> dict[str, Classification]:
        """Return the attribute-name to classification map for ``entity_type``."""


@dataclass
class InMemoryFabricBackend:
    """Dev / test backend. Production swaps for Fabric SDK-backed impl."""

    entities: dict[tuple[str, str], dict[str, Any]] = field(default_factory=dict)
    views: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    field_classifications: dict[str, dict[str, Classification]] = field(default_factory=dict)

    def get_entity(self, entity_type: str, key: str) -> dict[str, Any] | None:
        """Return the stored entity row for ``(entity_type, key)``, or None."""
        return self.entities.get((entity_type, key))

    def query_view(
        self, view_name: str, filters: dict[str, Any], limit: int
    ) -> list[dict[str, Any]]:
        """Return the first ``limit`` rows of ``view_name`` matching all ``filters`` exactly.

        An unknown view yields an empty list.
        """
        rows = self.views.get(view_name, [])
        out: list[dict[str, Any]] = []
        for row in rows:
            if all(row.get(k) == v for k, v in filters.items()):
                out.append(row)
                if len(out) >= limit:
                    break
        return out

    def classifications(self, entity_type: str) -> dict[str, Classification]:
        """Return the configured classifications for ``entity_type`` (empty if none)."""
        return self.field_classifications.get(entity_type, {})


FABRIC_BACKEND: FabricBackend = InMemoryFabricBackend()


def set_fabric_backend(backend: FabricBackend) -> None:
    """Replace the module-level backend (production swap, test fixture)."""
    global FABRIC_BACKEND
    FABRIC_BACKEND = backend


# --- Tool functions --------------------------------------------------------


def get_entity_by_key(
    entity_type: str,
    key: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, Any]:
    """Look up a canonical entity by its surrogate or natural key."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_entity_by_key",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"entity_type": entity_type, "key": key},
    ) as ctx:
        row = FABRIC_BACKEND.get_entity(entity_type, key)
        if row is None:
            raise McpError(
                code=McpErrorCode.NOT_FOUND,
                message=f"No {entity_type} with key {key!r}",
            )
        ctx["result"] = row
        return row


def query_gold_view(
    view_name: str,
    filters: dict[str, Any] | None = None,
    limit: int = 100,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict[str, Any]]:
    """Query a Gold view with optional filters."""
    if limit <= 0 or limit > 10_000:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="limit must be in [1, 10000]",
        )
    with traced_call(
        tool_name=f"{SERVER_NAME}.query_gold_view",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"view_name": view_name, "filters": filters or {}, "limit": limit},
    ) as ctx:
        rows = FABRIC_BACKEND.query_view(view_name, filters or {}, limit)
        ctx["result"] = rows
        return rows


def list_classifications(
    entity_type: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict[str, str]:
    """Return a mapping of attribute-name → classification value."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_classifications",
        tool_version=TOOL_VERSION,
        agent_id=agent_id,
        caller_identity=caller_identity,
        parameters={"entity_type": entity_type},
    ) as ctx:
        m = FABRIC_BACKEND.classifications(entity_type)
        out = {k: v.value for k, v in m.items()}
        ctx["result"] = out
        return out


# --- Tool contracts --------------------------------------------------------


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.get_entity_by_key",
        version=TOOL_VERSION,
        description="Look up a canonical entity by its key.",
        classification_propagation=[Classification.INTERNAL],
    ),
    ToolContract(
        name=f"{SERVER_NAME}.query_gold_view",
        version=TOOL_VERSION,
        description="Query a Gold view with optional filters.",
        classification_propagation=[Classification.INTERNAL],
    ),
    ToolContract(
        name=f"{SERVER_NAME}.list_classifications",
        version=TOOL_VERSION,
        description="Return the attribute → classification map for an entity type.",
    ),
]
