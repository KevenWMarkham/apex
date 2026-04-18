# APEX · RC Agent Catalog — Design

**Document class:** Deliverable design
**Date:** 2026-04-17
**Status:** Approved; implementation in progress
**Output:** `docs/APEX-RC-agent-catalog.docx`
**Generator:** `build-agent-catalog.cjs`

---

## Part 1 — Purpose

The APEX Solution Overview (`docs/APEX-solution-overview.docx`) Part 7 currently lists RC's 34 agents as a grouped bullet list. This is sufficient for the solution-overview's pitch role but is too thin for engagement engineers, Account Teams, or a client CTO trying to understand what each agent actually does.

This document specifies a standalone **APEX · RC Agent Catalog** that deep-dives on each of the 34 RC agents using a consistent 8-field card format, then cross-references them by ORCH and by decision cadence. The catalog is a reference artifact — the overview points to it; the catalog carries the detail.

---

## Part 2 — Structure

- **Title page** — wordmark + subtitle + metadata. Same visual language as the overview.
- **Part 0** — Compliance & language constraints (inherited from Core).
- **Part 1 — How to read this catalog** — explains the 8-field card, domain-intro pattern, and cross-references.
- **Part 2 — Merchandising Domain (12 agents)** — MER-A01..A12.
- **Part 3 — Supply Chain Domain (8 agents)** — SCM-A01..A08.
- **Part 4 — Customer Experience Domain (8 agents)** — CXM-A01..A08.
- **Part 5 — Marketing Domain (6 agents)** — MKT-A01..A06.
- **Part 6 — Agent × ORCH cross-reference matrix** — 34 rows × 12 columns, dot grid.
- **Part 7 — Decision cadence summary** — five cadence bands (second / minute / hour / day / weekly), which agents live in each.

Each domain part opens with a one-paragraph intro naming primary schema, consumed schemas, and decision cadence band (lifted verbatim from the RC build spec Part 5 so the catalog stays in sync with the authoritative spec).

---

## Part 3 — Agent Card Schema

Eight fields per agent, rendered as a bordered two-column layout (labels left in small caps, content right):

| Field | Content |
|---|---|
| Purpose | One-sentence problem statement. |
| Primary ORCH | ORCH-NN binding, or `(platform)`. |
| Primary schema + key entities | e.g., MERML · STORE_INVENTORY_POSITION, OSA_EVENT |
| Inputs | Gold view(s) or schema entities it reads. |
| Outputs | Artifacts, events, or state changes it produces. |
| Decomposition notes | Sub-agent contracts, verbatim from RC build spec Part 5. |
| HITL gate | Gate type + decision surface. |
| Wave availability | W1 / W2 / W3 / W4 — when this agent becomes available. |

---

## Part 4 — Content sourcing rules

- **`agent_id`, `name`, `decomposition_note`, `primary_orch`** — lifted verbatim from `apex-rc-build-spec-v2.md` Part 5.
- **Primary schema** — inferred from domain (Merchandising → MERML, Supply Chain → SCML, Customer Experience → CXML, Marketing → MKTL).
- **Key entities** — selected by matching the agent's purpose to the entities declared in `apex-rc/data/schemas.manifest.json`.
- **Purpose, Inputs, Outputs, HITL gate, Wave availability** — authored based on the decomposition note and the agent's domain context. Where the build spec is explicit (primary_orch, decomposition), use it verbatim. Where the spec is silent, compose a reasonable inference that is consistent with the APEX conventions and flag it implicitly by staying within the framework's established vocabulary.

No invented data. No client-identifiable names. Synthetic examples only.

---

## Part 5 — Visual style

Inherits from the overview's generator:

- US Letter, 0.75" margins.
- Arial body 11pt; heading navy `#1A2339` H1 bold 18pt, slate `#2F3F5F` H2 bold 14pt.
- Agent cards rendered as 2-column tables with light border (`#B8B8B8`), narrow field-label column (2000 DXA) with pale-paper shading (`#F4EFE3`), content column takes remainder.
- Cross-reference matrix (Part 6): table with agent IDs down, ORCH numbers across, teal dot (`●`) where binding exists, dash otherwise.
- Running header: "APEX · RC Agent Catalog · Core v1.2" right-aligned.
- Footer: "Page X of Y" centered.

---

## Part 6 — Generator

Extends `build-docx.cjs` pattern. New file `build-agent-catalog.cjs`:

1. Imports the same docx helpers as the overview generator.
2. Defines agent data as structured arrays (4 domains × N agents each, each agent an object with 8 fields).
3. Reuses the overview's `h1`/`h2`/`p`/`bullet`/`makeTable` helpers.
4. Adds `agentCard(agent)` helper — returns a 2-column table styled per Part 5.
5. Writes to `docs/APEX-RC-agent-catalog.docx`.

Re-runnable any time the RC spec or manifest changes.

---

## Part 7 — Overview integration

Part 7 of `docs/APEX-solution-overview.docx` and the markdown source `docs/APEX-solution-overview.md` get a one-line pointer:

> Each agent is documented in the companion catalog. See `docs/APEX-RC-agent-catalog.docx` (or the markdown equivalent).

The bullet list stays for quick reference; the catalog is the authoritative deep-dive.

---

## Part 8 — Acceptance

- Generator runs clean, writes valid .docx.
- 34 agent cards total: 12 MER + 8 SCM + 8 CXM + 6 MKT.
- Every card has all 8 fields populated.
- Cross-reference matrix in Part 6 shows every agent-to-ORCH binding matching the RC build spec.
- Cadence summary in Part 7 groups all 34 agents into exactly one band each.
- Catalog visual style matches the overview (fonts, color tokens, margins).
- Committed to git with the generator script.

---

**End of design — 2026-04-17**
