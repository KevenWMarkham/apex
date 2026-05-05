# ledger-mcp

Utility MCP server — Decision Audit Row store.

Tools: `append_audit_row`, `fetch_row_by_trace`, `verify_row_signature`.

Sprint 7 ships in-memory store + HMAC-SHA256 row signing. Sprint 12 wires the
full 14-field audit-row schema, Delta-backed append-only store, and the
three-version rule (manifest + policy + prompt SHAs).
