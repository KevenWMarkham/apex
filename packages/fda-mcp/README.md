# fda-mcp

External MCP server — FDA recall and adverse-event feeds (openFDA).

Tools: `list_recalls_by_date`, `get_recall_detail`, `search_adverse_events`.

Sprint 9 ships an in-memory `InMemoryFdaBackend` for test + dev. Sprint 15 wires the real openFDA REST client with rate-limit handling.
