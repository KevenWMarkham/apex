# Deprecations — APEX modules superseded by Microsoft GA capability

Phase J of the implementation plan identified six places where APEX was over-building infrastructure that Microsoft shipped GA. Each deprecation note records:

- What APEX was building
- The Microsoft GA capability that supersedes it
- The migration path
- The Roadmap.md backlog item being superseded

The original code stays in place for now; the deprecation notes are paper-only until each item moves through the migration in a future sprint.

## Index

| Deprecation | What APEX was building | Microsoft GA replacement | Status |
|---|---|---|---|
| [DEP-001](DEP-001-eventhouse-mcp.md) | Custom MCP server for Eventhouse queries | RTI remote MCP (Eventhouse + Activator) | Adopt MS-hosted MCP |
| [DEP-002](DEP-002-embedding-endpoint.md) | Custom embedding endpoint for The Pricer | Eventhouse SLM `ai_embeddings` plugin | In-data-tier embeddings |
| [DEP-003](DEP-003-debezium-cdc-parser.md) | Custom Debezium CDC parser for Bronze | Eventstream DeltaFlow transformation | Use DeltaFlow |
| [DEP-004](DEP-004-hitl-alert-trigger.md) | Custom HITL alert trigger | Eventstream Activator destination | Use Activator |
| [DEP-005](DEP-005-bespoke-threat-detection.md) | Bespoke agent threat detection | Defender for AI services | Enable Defender plan |
| [DEP-006](DEP-006-audit-row-hmac-as-system-of-record.md) | Audit-row HMAC as system of record | Microsoft Purview Audit + DSPM for AI | Demote to KPI overlay |

See [ADR-003](../adr/ADR-003-audit-row-vs-purview-audit.md) for the audit-row demotion (DEP-006) decision.

## Format

Each deprecation note follows:

1. What was being built and why
2. Microsoft GA capability that supersedes it
3. Migration path (what code/config changes, what rolls out when)
4. Roadmap.md backlog item being superseded
5. Independence implications (none expected for any of these)
