"""fda-mcp — FDA recall + adverse-event MCP tools."""

from fda_mcp.tools import (
    CONTRACTS,
    FdaBackend,
    InMemoryFdaBackend,
    get_recall_detail,
    list_recalls_by_date,
    search_adverse_events,
    set_fda_backend,
)

__all__ = [
    "CONTRACTS", "FdaBackend", "InMemoryFdaBackend",
    "get_recall_detail", "list_recalls_by_date", "search_adverse_events",
    "set_fda_backend",
]
