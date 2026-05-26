---
name: vv-author
description: Use when authoring APEX Virtual View YAML manifests. Triggers include "add a VV", "new view for the pack", "create a manifest for X metric".
---

# Authoring APEX Virtual Views

Use the `apex-vv-manifest-author` agent. Provide:
- Natural-language requirement
- Source schema reference
- Pack namespace
- Target sub-domain

The agent writes the manifest to `packs/<industry>/views/<view>.yaml`, generates acceptance tests via the Test Pack Generator, and updates lineage.

## Conventions
- View ID format: `<namespace>.<view_name>` (snake_case)
- Always include `mcp_tool.schema_from_projection: true`
- Always include `ledger.record_per_query: true` unless explicitly suppressed
- Default cache mode: `time_bounded` with TTL appropriate to the metric cadence
- Threshold sustain_window default: `2_cycles` (2 measurement intervals)

## Validation
Run `/apex-acceptance` after authoring to confirm manifest validity tests pass.
