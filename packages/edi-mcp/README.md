# edi-mcp

External MCP server — EDI X12 message processing (minimal stubs).

Tools: `parse_850` (purchase order), `parse_856` (shipment notice), `emit_810` (invoice).

Sprint 9 ships segment-level parsers only. Sprint 15 (BL.P.155) ships the full industrial-grade X12 parser for 850/856/810/820 + HIPAA 837/835/270/271.
