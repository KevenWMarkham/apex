# fabric-mcp

Utility MCP server — **Gold / OneLake reads** for agents.

Tools:
- `get_entity_by_key(entity_type, key)` — canonical entity by key
- `query_gold_view(view_name, filters, limit)` — Gold view with filters
- `list_classifications(entity_type)` — classification map for an entity

Sprint 7 ships in-memory backends for tests + development. Sprint 8 domain
MCP servers (`scml-mcp`, `hlscml-mcp`, etc.) delegate to `fabric-mcp` for the
raw OneLake read path, adding per-schema-family scoping on top.
