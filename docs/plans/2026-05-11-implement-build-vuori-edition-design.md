# Design — Professional APEX-M · Implement & Build (Vuori Edition)

**Date:** 2026-05-11
**Author:** Keven Markham
**Status:** Approved — proceeding to draft
**Target file:** `docs/book/Professional-APEX-M.html` (overwrite the master volume)

---

## Goal

Replace the 30-chapter survey body of `Professional-APEX-M.html` with a focused
8-chapter engineering manual: an implement/build guide built around the Vuori
engagement, with the MVP reference implementation
(`C:\Stage\Clients\Industries\Consumer\Merch\MVP`) providing every concrete
code example.

The book is the deliverable artefact the engagement uses to:
- onboard new engineers in days, not weeks
- prove acceptance criteria pass against the synthetic Vuori schema
- show clients (Matt King, Himanshu) the engineering depth behind the demo

## Approach

**Vuori-threaded.** Every chapter ties an APEX pattern to a concrete piece of
the Vuori engagement (the 8 confirmed gaps, the WBR Friday-to-Monday journey,
the merml-mcp + cxml-mcp split, the Snowflake medallion on Azure). Code blocks
mirror or extend what's already shipped in MVP/.

**MVP-derived.** UCs come from `MVP/TestHarness/catalog_seed/uc_catalog.json`
(21 items, 6 groups + 1 journey). Test harness chapters walk the actual
`mvp_test_harness` package. Personas use the canonical 5-name set (The Analyst,
The Demand Checker, The Finance Lead, The Operations Lead, The Briefer).

## Structure — 4 parts, 8 chapters

| Part | Chapters | Theme |
|------|----------|-------|
| I — Engagement & APEX integration | Ch 1–2 | The Vuori brief, framed as an APEX use-case bundle |
| II — Building the solution | Ch 3–5 | Five-persona architecture, ingestion, medallion |
| III — MCP & Microsoft Agent Framework | Ch 6–7 | Writing the two MCPs, wiring the agent framework |
| IV — Test harness | Ch 8 | The mvp_test_harness deep dive — the engagement's acceptance artefact |

### Chapter detail

1. **The Vuori engagement, framed as an APEX use-case bundle.**
   The 8 confirmed gaps map onto the 21-UC catalog. Q1 scope: 5 agents, 9
   personas, WBR Friday-to-Monday journey. Demo scenario: Apparel · Week 16 ·
   Midwest · −12% miss · supply-disruption root cause.
2. **Registering the engagement as an APEX service.**
   Scaffold `services/rc/rc-wbr/`. Clone `use-cases/_default/` → `vuori/`.
   Populate `persona_principal_bindings`, run PSG-15.
3. **The five-persona, two-MCP architecture.**
   ADR-006 patterns (Sequential / Concurrent / Handoff / Group Chat / Magentic).
   `agentic_merch/base.py` shape. Persona → Agent-ID mapping.
4. **Ingesting Vuori data.**
   Fivetran Shopify → Snowflake RAW. ADF for Anaplan. SFTP for iSEYON.
   ConCON synthetic feed. `generate_vuori_synthetic.py` for the 8 tables.
5. **Building the medallion tier.**
   Snowflake DDL for RAW → CLEANSED → CURATED. dbt models per layer.
   Dual-calendar (NRF + Gregorian) reconciliation. Aging proxy.
6. **Writing merml-mcp and cxml-mcp.**
   Python MCP server pattern. Tool schemas. Tier-3 PII unlock.
7. **Microsoft Agent Framework wiring.**
   APEX-M `agent_framework_loader`. Friday-to-Monday journey orchestration.
   HITL gates at every Tier-2+ decision. LEDGER write.
8. **Building with the MVP test harness.**
   21-UC catalog. `steps.yaml` anatomy. 7 executor kinds. Assertion kinds.
   Manifest swap. Stub-then-graduate. Stepper UI on :8765. 277-test pyramid.
   Catalog-wide report. LEDGER hash chain. Vuori acceptance run.

## Confidentiality

Top-of-file ribbon:
> *CONFIDENTIAL — Vuori engagement. Code examples derived from the MVP
> reference implementation. Synthetic data only — no production Vuori data
> is reproduced.*

The existing 30-chapter master content survives in
`Professional-APEX-M-Library.html` (unchanged).

## Visual system

Reuse the Wrox-style chrome from the current Professional-APEX-M.html:
- Sticky topbar with navy background + apex-teal accent + dark-mode toggle
- 280px fixed sidebar with grouped TOC
- Source Serif 4 body / Aptos headings / Cascadia Mono code
- Callout boxes: note, warning, bestpractice, tryitout
- Chapter objectives panel, chapter summary, chapter exercises

Add Vuori-overlay accents per `vuori-style-overlay.md`:
- Rust (#B85450) accent bar in cover gradient
- Sage (#7C8968) for "positive" callouts / completed states
- Gold (#C4A55A) for component labels

## What ships

- `docs/book/Professional-APEX-M.html` — replaced with the Vuori build edition
- `docs/plans/2026-05-11-implement-build-vuori-edition-design.md` — this doc
- Commit message: `docs(book): Implement & Build · Vuori Edition`

## What does not ship

- New code in `apps/` or `apex-m/` — this is documentation, not implementation
- Changes to MVP/ — that's a separate repo and the source of truth
- Real Vuori production data — synthetic only

## Risks

- **Confidentiality drift.** Vuori-specific framing leaks into the wider APEX
  brand. Mitigation: top-of-file ribbon, synthetic-data-only stance, the
  generic synthetic schema (`dim_product`, `fact_sales`, etc.) is reusable
  across $2B vertically integrated retailers per the technical context.
- **MVP drift.** Book diverges from the actual MVP code over time. Mitigation:
  every code block carries a path comment pointing back to the MVP file it
  derives from, so a future reader can diff.
- **Scope creep.** Eight chapters is the discipline. Resist adding a Part V
  on operations / change management — that lives in the Deployment Guide.
