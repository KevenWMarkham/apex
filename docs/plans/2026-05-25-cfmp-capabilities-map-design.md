# CFMP Capabilities Map + Eps 10–11 — Design

**Date:** 2026-05-25
**Status:** Design approved · ready for writing-plans handoff
**Owner:** kmarkham@deloitte.com · Deloitte MS Technology & Services Practice

**Output artifacts:**
1. `pc-cfmp/CFMP-Capabilities-Map.html` — single self-contained HTML capability map.
2. `pc-cfmp/10-flux-household-composition.md` — new podcast episode: Flux.
3. `pc-cfmp/11-recipes-meal-plan-front-door.md` — new podcast episode: Recipes capture & cultural breadth.
4. Audio for the two new episodes (appended to the in-flight 9-episode batch).
5. `pc-cfmp/_build_capabilities_map.py` — code-scanner that walks `C:\code\iot_device\` and emits the file-inventory the HTML embeds.

**Source code mapped:** `C:\code\iot_device\` — orchestrator/ · mobile/app/ · portal/app/ · device_app/ · db/ · scripts/.
**Source design docs scanned:** the 24 docs in `C:\code\iot_device\docs\packs\`.

## Goal

A single interactive HTML page that maps the CFMP solution's **business capabilities** (not technical components) to their podcast episodes, design-doc sections, and supporting code — so a seller, engineer, or stakeholder can answer in one screen: *what does CFMP do, where is it covered, where is the code, and what's still proposed or gapped?* Plus two new podcast episodes that fill the most material design+code gaps the map surfaces.

## Privacy as the headline differentiator (cross-cutting)

The architecture has the privacy DNA today (Vision Kit local inference, Sonos household-local, phone-mic STT not cloud-streamed, MCP boundary, customer-owned audit chain) but the podcast frames it as "trust" without naming the **Alexa contrast**: public-cloud-always-listening → vendor lock-in. The map elevates this to the headline through:

1. **A sticky top banner** above the seller's-opener row: "🛡️ Privacy is the moat — runs on your home network + telco edge; not the Alexa/Google-Home public-cloud surveillance pattern; the customer owns the audit chain."
2. **Lane 11 — 🛡️ Privacy-First Architecture · Home & Telco Edge** — added as the synthesizing closing lane. Capabilities: voice-on-device · Vision Kit local inference · Sonos household-local · MCP boundary as privacy boundary · customer-owned identity · selective uplink · telco-edge orchestrator (v2 ❓) · on-device LedgerRow witness (v2 ❓) · local-first fallback · anti-vendor-lock-in posture.
3. **Episode 12 · Privacy as the moat** — dedicated episode framing the differentiator vs. Alexa/Google-Home. Series becomes 12.
4. **Surgical edits to Ep 09 Seller's Playbook** — promote privacy to a headline (a) 7th discovery opener: *"Does your assistant listen to everything in your home — or only what you ask?"* (b) 6th honest claim: *"Privacy is architectural, not a setting."* (c) 4th 'recommend NOT Microsoft' scenario: the customer who wants always-listening public-cloud AI.

## The podcast — extended from 9 to 12 episodes

Eps 01–09 stay as-is. The Ep 09 finale + "See you in the field" sign-off remains the headline arc close. Eps 10 and 11 are **documentary deep-dives** appended after the finale — for the seller who wants the meal-plan front door or the household-composition substrate, queued when the client conversation goes there.

- **Ep 10 · Flux — Household composition & presence events.** The 7 kinds (vacation · partial absence · arrival · permanent arrival · permanent departure · event · move) across 5 families. The detected→proposed→approved→active HITL lifecycle. Why composition is a first-class sibling of lots, not a property of one. Sources: `CFMP-Mobile-Flux-Design.md`, `db/04_flux_events.sql`, `orchestrator/flux.py`.
- **Ep 11 · Recipes — the meal-plan front door.** Capture from YouTube · friend-shared · family heirloom (mom's dishes, generational) · restaurant-meal repeat · holiday favorites · cuisine breadth (Japanese · Chinese · Mexican · South American · Korean · Italian · English · German · Spanish · Indian · Thai · Vietnamese · Mediterranean · Seafood) · specialty-ingredient sourcing · allergen-aware import gate. Sources: `orchestrator/meal_planner.py` head + the existing recipe-library hints in Mobile §6; most capability boxes here are ❓ Proposed.

Audio for Ep 10 + Ep 11 uses the same two-Andrew voice pair (continuity), gets stings, joins the `pc-cfmp/audio/` set.

## Capabilities Map — layout

**Header — Seller's-playbook discovery openers.** A chip row across the top — the six openers from Ep 09, each clickable. Clicking an opener highlights the lane(s) it pivots on. Makes the page *immediately useful* on a client call: open the URL, click an opener, the relevant capabilities light up.

**Persona ribbon.** Below the header — five persona icons (Sarah · Robert · Diana · Marcus · Priya). Clicking a persona dims capabilities they don't touch. Multi-select supported.

**10 swimlanes (horizontal rows).** Each lane has a colored header band, a one-line description, the primary episode reference, and a row of capability boxes flowing left-to-right by maturity (Completed → In Progress → Not Started → Proposed):

| # | Lane | Primary episode | Notes |
|---|---|---|---|
| 1 | 🛒 Discovery & Lot Composition | Ep 03 + 01 | SCAN, LOT noun, 4 archetypes, recipe→lot (existing), Care-Lot |
| 2 | 🛍️ Lot Lifecycle, Replenish & Home | Ep 04 | trip lifecycle, auto-replenish, home channel, preferences, UI, senior on Mobile |
| 3 | 🏪 In-Store Experience | Ep 03 + 04 + 06 | aisle checklist · walk-aisle nav · real-time coupons · store map · geofence · self-checkout QR · receipt→pantry |
| 4 | 🚚 Fulfillment & Pickup | Ep 07 | plug-in tier, BOPIS+pharmacy gate, substitution, status webhooks |
| 5 | 🔊 Voice Channel · Sonos | Ep 06 | Cue Bus, zones, cadence, AirPlay-bridge, voice-in |
| 6 | 🤖 Agent Orchestration & MCP | Ep 02 | gpt-5-mini parent + specialists, MCP boundary |
| 7 | 🔒 Trust, Identity, Consent & HIPAA | Ep 08 + 02 | four-identity, Entra, consent gradient, HIPAA presence-gating, audit chain, trace_id |
| 8 | ⚙️ Operations, Portal & Multi-Tenant | Ep 05 + 02 | `/architecture` hero, operator console, chat panel, vision-kit, retailer multi-tenant |
| 9 | 🍳 Recipe Capture & Cultural Breadth | Ep 11 NEW | mostly ❓ Proposed — the v2 roadmap argument |
| 10 | 🍷 Pairings & Mixers | (no episode) | mostly ❓ Proposed — wine · beer · cocktails · holiday · age-gate via the pharmacy-pattern reuse |
| 11 | 🛡️ Privacy-First Architecture · Home & Telco Edge | Ep 12 NEW | voice on device · Vision Kit local · MCP boundary · customer-owned identity · selective uplink · telco-edge orchestrator (v2) · on-device witness (v2) · anti-vendor-lock-in |

Cross-lane "see also" tags will link related capabilities (e.g., *walk-the-aisle navigation* in Lane 3 references the route cue in Lane 5).

## Per-capability box

Each box renders:

```
┌─────────────────────────────────────────┐
│  ⬤  <capability name>                    │
│  Status: <color-icon> <state> · <%>      │
│  Episode: Ep NN · <Episode title>        │
│  Design:  <doc> §<section>               │
│  Personas: <icons>                       │
│  Code:    <file>:<lines>                 │
│           <file>:<lines>                 │
│  Gaps:    <one-line named gap, if any>   │
└─────────────────────────────────────────┘
```

The episode reference is a clickable link → opens that episode's `.md` in a side panel.
The design-doc reference is a link → opens the referenced doc + section anchor.
Clicking the capability name expands the box into a full-detail panel showing **all** supporting code files (path · lines · last-modified · one-line role).

## Status taxonomy (six)

| Color | Symbol | State | Meaning |
|---|---|---|---|
| green | 🟢 | Completed | Design ↔ code match; capability ships end-to-end |
| amber | 🟡 | In Progress | Partial code present; show estimated % from a curated table |
| white | ⚪ | Not Started | Designed in podcast / design-doc; no code yet |
| violet | 🟣 | Implemented but not podcasted | Code + design exist; podcast doesn't cover it (Flux is the canonical example before Ep 10) |
| red | 🔴 | Gap with named risk | Design-described, partial code, with a *named* gap (missing test, missing schema field, missing webhook idempotency) |
| grey-dashed | ❓ | Proposed (new) | Not in code, design, or podcast; the v2 roadmap argument |

The map's bottom section ("Gap Analysis") aggregates:
- All 🔴 boxes (the must-fix list).
- All 🟣 boxes (the podcast-extension argument).
- All ❓ boxes (the v2 backlog argument).

## Code scanner — `_build_capabilities_map.py`

Mirrors the `_build_cues.py` pattern from the Cross-Cloud series. The scanner:
1. Walks `C:\code\iot_device\` (orchestrator/ · mobile/app/ · portal/app/ · device_app/ · db/).
2. For each `.py`, `.ts`, `.tsx`, `.sql` file: counts lines, reads the docstring/header comment for a one-line role, captures the file's last-modified timestamp.
3. Maps files to capability boxes via a hand-authored mapping table (`CAPABILITIES` dict keyed by box-id → list of file paths or glob patterns).
4. Emits a single JSON: `{ capabilities: [{id, lane, name, status, episode, design_ref, personas, files:[{path,lines,last_mod,role}], gaps:[]}], lanes: [...], openers: [...] }`.
5. The HTML embeds this JSON inline (browsers block `fetch()` on `file://`).

A separate file-inventory pass produces a deterministic ranking of "unmapped" files — code that hasn't been assigned to a capability — so the map's 🟣 surface stays honest.

## Persona filter & opener filter

Persona ribbon (multi-select): Sarah · Robert · Diana · Marcus · Priya. Capabilities are tagged per-persona. Filter dims non-matching boxes.

Opener chips (Ep 09's 6 openers): each opener tagged with one or more lanes. Filter highlights matching lane headers.

## Build sequence

1. **Write Ep 10 (Flux)** — dispatch subagent with the Flux Design doc + flux.py header.
2. **Write Ep 11 (Recipes)** — dispatch subagent with the meal_planner.py header + cuisine-breadth brief.
3. **Audio-batch the two new episodes** — same `_build_audio.py` (extend the EPISODES list to 11). Apply stings.
4. **Curate the capability inventory** — hand-author the ~80-100 capability boxes across the 10 lanes; tag each with status + episode + design + personas + a list of code-file paths/patterns.
5. **Implement the code scanner** — `_build_capabilities_map.py` reads the inventory + walks the iot_device repo + emits the embedded JSON.
6. **Build the HTML** — CSS swimlanes (reuse the study-guide design language: warm-midnight palette, Fraunces/Instrument Sans/JetBrains Mono fonts, `.paq-details` collapse pattern); JS for persona filter / opener filter / status filter / box-expand side panel.
7. **Verification** — counts, link audit, all 11 episode refs resolve, all design refs resolve, status histogram, persona-tag completeness, unmapped-file count surfaced.

## Verification

- 10 swimlane headers + 5 persona icons + 6 opener chips render.
- 80–100 capability boxes total (rough estimate); every box carries episode + design + status + personas + ≥0 files.
- Status histogram: counts by status (🟢/🟡/⚪/🟣/🔴/❓) shown at the top.
- Click an opener → matching lanes highlight; click a persona → matching capabilities dim/un-dim; click a capability → side panel opens with file list.
- All 11 episode refs are clickable + open the right `.md`.
- All design-doc refs link to a file that exists in `C:\code\iot_device\docs\packs\`.
- HTML tag balance + JS `node --check` pass.
- The map matches the podcast: capabilities the podcast covers are visible; capabilities the podcast doesn't cover are flagged 🟣 or ❓.

## Out of scope (YAGNI)

- Real-time code analysis (the scanner runs once; the JSON is embedded; updates are a rebuild, not a live link).
- AST-level mapping (file-level role is sufficient).
- Dependency graphs between capabilities (cross-lane "see also" tags are enough).
- Per-line code annotation.
- Audio production for Ep 10/11 beyond the same edge-tts + stings pipeline.
- A separate JSON export for the map data (it's embedded).

---

**Next:** invoke `superpowers:writing-plans` for the bite-sized implementation plan.
