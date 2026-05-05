# hlscml-mcp

Domain MCP server — HLS clinical reads. **PHI segregated** — this server's identity never grants tokens outside HLS.

Tools: `get_patient_by_key`, `list_observations_for_patient`, `list_medications_for_patient`.

Required scope: `practice:hls`. Cleartext PHI is retrieved only via `tokenizer-mcp` with matching classification scope.
