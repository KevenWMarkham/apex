# DEP-001 · Custom Eventhouse MCP server → RTI remote MCP servers

**Status:** Deprecated
**Date:** 2026-05-09
**Supersedes:** Roadmap.md BL.P.41 (utility MCP `fabric-mcp`) when its scope was Eventhouse query

## What APEX was building

Custom MCP server wrapping Eventhouse + Activator APIs so APEX agents could issue KQL queries and create Activator rules through the MCP host. Planned name was `eventhouse-mcp` (not yet built; was on the Phase 2 backlog).

## What Microsoft shipped

In **March 2026**, Microsoft Real-Time Intelligence shipped **hosted MCP remote servers** for both Eventhouse and Activator (preview):

- [Get started with the Eventhouse remote MCP server](https://learn.microsoft.com/fabric/real-time-intelligence/mcp-remote-eventhouse)
- [Get started with the Activator remote MCP server](https://learn.microsoft.com/fabric/real-time-intelligence/mcp-remote-activator)

Capabilities:
- **Eventhouse remote MCP**: schema discovery, KQL query generation, data sampling, natural language → KQL.
- **Activator remote MCP**: create monitoring rules, manage alerts, trigger actions.

Both are Microsoft-hosted HTTP endpoints — no infrastructure to maintain on the APEX side.

## Migration path

1. Stop building `eventhouse-mcp` as a custom MCP server. Mark BL.P.41 in Roadmap.md as "scope reduced — Eventhouse path covered by RTI remote MCP."
2. APEX agents that need Eventhouse access **register the RTI remote MCP server URL** in their use-case YAML's `client_approved_architecture` block (TBD field — track as future enhancement).
3. The wizard's render endpoint emits agent configurations that include the RTI MCP endpoint URL alongside any custom MCP servers.

## Independence implications

None. The RTI remote MCP server is a Microsoft-hosted service the client's tenant already has access to via their Fabric subscription. APEX is integrating with the client's existing Fabric investment.

## What stays

`fabric-mcp` (BL.P.41) keeps its non-Eventhouse capabilities — OneLake / workspace reads. Only the Eventhouse-query subset is superseded.
