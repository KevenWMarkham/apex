# pharma-recall-mcp

External MCP server — pharmaceutical recall aggregation across multiple sources (FDA, vendor alerts, DSCSA).

Tools: `list_pharma_recalls`, `search_recalls_by_ndc`, `get_recall_detail`.

Validates NDC codes against `apex-schemas-common.standards.NdcCode`.

Sprint 9 ships in-memory seed. Sprint 15 wires real aggregator clients.
