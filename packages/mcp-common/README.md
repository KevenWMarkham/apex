# mcp-common

Shared scaffolding consumed by every APEX MCP server (utility, domain, external).

## What it provides

- **`contract`** — `ToolContract` Pydantic model (tool name, inputSchema, outputSchema, SLO, classification propagation, version).
- **`trace`** — `ToolTraceRecord` (operation_id, agent_id, tool_name, tool_version, parameters_hash, result_hash, latency_ms, classification_applied, caller_identity) + `emit_trace()` helper.
- **`scope`** — `ScopeContext` stub (Sprint 10 wires the real visibility-lattice evaluator via `apex-identity`).
- **`auth`** — Entra managed-identity middleware stub (Sprint 10 wires the real thing).
- **`errors`** — Standard MCP error-code enum + error mapper.

## What it does NOT provide

- A running MCP server. Each server package (`fabric-mcp`, etc.) owns its own `server.py` entry-point using Anthropic's `mcp` SDK. Keeping this package framework-free lets servers be tested without the SDK installed.

Design anchor: `APEX_Design.md` §7, §8.
