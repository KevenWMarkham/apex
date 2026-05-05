# Design: MCP Server Tools Deep-Dive — Sellers Guide Appendix I

**Date:** 2026-04-18
**Status:** Approved — proceeding to implementation
**Target:** Sellers Guide new Appendix I

## Purpose

Provide sellers with a comprehensive reference for APEX's MCP server tools — the
interface through which agents consume Gold-tier data and invoke actions. Covers
MCP architecture, tool catalogues per Practice, and the Silver→Gold data-creation
path behind each tool.

## Placement

New Appendix I: "MCP Server Tools — How Agents Call Gold-Tier Data" (after Appendix H).

## Structure

- **I.1** How to read this appendix
- **I.2** MCP architecture in APEX (server, tool, agent, Gold view)
- **I.3** The five Silver→Gold transform patterns (once; then referenced)
- **I.4** The standard MCP tool patterns (entity-read, entity-search, cross-entity-join, temporal-window, action-execute)
- **I.5** RC MCP tools (SCML, MERML, CXML)
- **I.6** HLS MCP tools (Payer, Provider, Life Sciences)
- **I.7** ER MCP tools (UOG, P&U, Mining)
- **I.8** AXLE MCP tools (AXLEML sub-models)
- **I.9** TMT MCP tools (TEC, MED, TEL)
- **I.10** TH MCP tools (TravelerML, OpsML, Loyalty/Revenue)
- **I.11** ICE MCP tools (Equipment, Dealer, Aftermarket, Rental)
- **I.12** Cross-Practice MCP tools
- **I.13** MCP governance — auth, rate limits, audit
- **I.14** Building custom MCP tools — client-specific extensions

## Per-Tool Template

Each tool documented with:
1. Tool name and signature
2. Purpose (1-2 sentences)
3. Input schema (parameters, types, required/optional)
4. Output shape (response structure)
5. Gold view backing (the Fabric artifact the tool reads)
6. Silver→Gold transform (which of the 5 patterns creates the Gold view)
7. Example agent invocation (realistic scenario)
8. Example response (abbreviated JSON)
9. Classification carry-through (which Purview labels apply)
10. Typical consumer agents (which APEX agents use this tool)

~250 words per tool × ~100 tools = ~25,000 words.

## Success Criteria

- Senior sellers and solution architects can answer "how does an agent get data X"
  without guessing
- Client data/architect teams can trace any tool back to its Gold view and Silver transform
- MCP governance (auth, rate limits, audit) understood at seller level

## Batches

1. I.1-I.4 foundation sections
2. I.5 RC MCP tools
3. I.6 HLS MCP tools
4. I.7 ER MCP tools
5. I.8 AXLE MCP tools
6. I.9 TMT MCP tools
7. I.10 TH MCP tools
8. I.11 ICE MCP tools
9. I.12-I.14 closing sections
10. Rebuild
