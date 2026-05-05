# tokenizer-mcp

Utility MCP server — wraps `apex-tokenizer` with scope-gated detokenisation.

Tools: `detokenize_under_scope`.

Scope gating stub (Sprint 7): requires the caller's scope to list at least one
classification whose tokens are being requested. Sprint 10 replaces with the
full visibility-lattice check.
