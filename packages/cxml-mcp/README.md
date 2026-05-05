# cxml-mcp

Domain MCP server — Customer Experience reads. Heavy PII — outputs carry tokens only.

Tools: `get_customer_by_key`, `list_orders_by_customer`, `list_interactions_by_customer`.

Required scope: `practice:rc`. PII / PCI detokenisation happens via `tokenizer-mcp`, gated separately.
