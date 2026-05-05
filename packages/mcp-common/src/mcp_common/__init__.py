"""APEX MCP shared scaffolding."""

from mcp_common.auth import AgentIdentity, require_agent_identity
from mcp_common.contract import SloSpec, ToolContract
from mcp_common.errors import McpError, McpErrorCode
from mcp_common.scope import ScopeContext, scope_allows
from mcp_common.trace import ToolTraceRecord, compute_hash, emit_trace, traced_call

__all__ = [
    "AgentIdentity",
    "McpError",
    "McpErrorCode",
    "ScopeContext",
    "SloSpec",
    "ToolContract",
    "ToolTraceRecord",
    "compute_hash",
    "emit_trace",
    "require_agent_identity",
    "scope_allows",
    "traced_call",
]
