# APEX · Store 100 Facilitator Guide — Design

**Date:** 2026-04-17
**Status:** Approved; implementation in progress
**Outputs:**
- `docs/APEX-Store-100-facilitator-guide.md` — markdown source
- `docs/APEX-Store-100-facilitator-guide.docx` — Word-format deliverable
- `build-facilitator-guide.cjs` — generator script

---

## Purpose

A facilitation layer for DMTSP Account Teams walking a client through the Store 100 HTML walkthrough (`C:\Stage\Clients\Industries\Consumer\Retail\Walmart\02_projects\apex-rc-store-100-shift-walkthrough.html`). The HTML is the narrative; this document is how to use it in a client conversation. It maps every scenario to the APEX framework (ORCH, agents, schemas, HITL gates, wave availability), gives facilitators talking points and objection handlers, and closes with a wave-commitment worksheet.

---

## Structure (14 parts)

1. Part 0 — Compliance (inherited) + scenario-vs-engagement boundary
2. Part 1 — How to use this guide (3 meeting settings)
3. Part 2 — Store 100 at a glance (demo shape)
4. Part 3 — Reader's kit (which APEX artifacts to pair)
5. Parts 4–11 — Eight event sheets (one per HTML scenario)
6. Part 12 — Aggregate ROI pitch
7. Part 13 — Common objections & prepared responses
8. Part 14 — Next-meeting checklist

## Event sheet template (7 fields)

| Field | Content |
|---|---|
| Event summary | Time, severity, one-sentence headline from HTML |
| The hook | One-sentence attention-grabber the facilitator opens with |
| APEX cross-walk | Table: ORCH · agents · primary schema · key entities · HITL gate · wave |
| Talking points | 3–5 bullets — what to emphasize |
| Common client questions | 2–3 Q&As the facilitator must be ready for |
| The ROI point | Specific economic argument backed by outcome metrics |
| Next step | How this scenario hooks to a wave commitment |

## Framework mapping (pre-worked)

| # | Time | HTML headline | ORCH | Primary agents (catalog IDs) | Schema · Entities |
|---|---|---|---|---|---|
| 01 | 5:58 AM | Reefer 14 cold chain | ORCH-03 | SCM-A04, SCM-A05, SCM-A06 | SCML · COLD_CHAIN_TELEMETRY, TEMPERATURE_EXCURSION, STORE_INVENTORY_POSITION |
| 02 | 7:20 AM | DSD short-ship | ORCH-01 | SCM-A01, SCM-A02, SCM-A03 | SCML · ASN, STORE_RECEIVING_EVENT, RECEIVING_DISCREPANCY, DSD_INVOICE |
| 03 | 8:36 AM | 127 stale tags | ORCH-02 | MER-A04, MER-A05 | MERML · PRICE_RECORD, PRICE_TAG_STATUS, PROMOTION_ACTIVATION |
| 04 | 10:15 AM | 18 empty shelves w/ backroom stock | ORCH-04 | MER-A06, MER-A07, MER-A08 | MERML · STORE_INVENTORY_POSITION, OSA_EVENT |
| 05 | 11:43 AM | Infant formula recall | ORCH-05 | SCM-A07, SCM-A08 | SCML · RECALL_NOTICE, LOT_TRACE · plus CXML · LOYALTY_STATE |
| 06 | 12:32 PM | BOPIS spinach substitution | ORCH-06 | CXM-A01, CXM-A02, CXM-A03 | CXML · FULFILLMENT_ORDER, PICK_EXCEPTION, SUBSTITUTION_EVENT |
| 07 | 1:47 PM | 4.2× void rate on spirits | ORCH-07 | MER-A09, MER-A10, MER-A11 | MERML · POS_VOID, SHRINK_EVENT, CYCLE_COUNT_VARIANCE |
| 08 | 2:32 PM | Plastic in muffin | ORCH-08 | CXM-A04, CXM-A05, CXM-A06 | CXML · CUSTOMER_INCIDENT |

Together: 8 events → 8 distinct ORCHs (of 12) → 17 distinct agents (of 34) → all 3 RC schemas (MERML, SCML, CXML). One shift demonstrates 2/3 of the RC orchestration grid.

## Visual style

Inherits from overview + catalog generators. Each event sheet rendered as a bordered card block with title row (time + severity + ORCH) and labeled field rows. Running header: "APEX · Store 100 Facilitator Guide · Core v1.2". Standard page size, margins, fonts, colors.

## Compliance

Store 100 / Marisol Reyes / DFW Metroplex / Apr 14 2026 are treated as synthetic reference-implementation identifiers consistent with the HTML walkthrough. Part 0 explicitly states that actual client-engagement specifics (real store numbers, real manager names, client-identifiable ROI figures) belong in engagement-specific deliverables, not this reusable guide.

## Generator

`build-facilitator-guide.cjs` follows the established pattern:

- Reuses docx helpers (h1, h2, p, bullet, makeTable, etc.) — factored identically to build-agent-catalog.cjs.
- Event data declared as a structured array of 8 objects.
- New helper `eventSheet(e)` renders each event as a two-column bordered table.
- Writes to `docs/APEX-Store-100-facilitator-guide.docx`.

Re-runnable whenever the HTML walkthrough or the APEX catalog changes.

---

**End of design — 2026-04-17**
