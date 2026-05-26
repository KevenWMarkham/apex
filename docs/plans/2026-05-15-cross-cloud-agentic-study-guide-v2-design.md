# Cross-Cloud Agentic Study Guide v2 — Design

**Date:** 2026-05-15
**Status:** Design approved · ready for writing-plans handoff
**Modifies:** `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic\Cross-Cloud-Agentic-Study-Guide.html` (currently 177 KB, 9 tabs)

## Goal

Extend the existing Cross-Cloud Agentic Podcast study guide into a single comprehensive artifact that adds: a synced audio player + timeline + screen-pop per episode; an opt-in APEX architecture-linkage per episode; an opt-in APEX stack overview; and curated Microsoft self-learning links per episode. One file, no separate companion.

## Key constraints

- **APEX is opt-in.** The APEX name and the architecture linkage appear ONLY inside collapsed `<details>` sections (collapsed by default). The guide's default/visible view stays generic — "the Acceleration Framework", no APEX — preserving its client-safe-by-default property. A student reveals APEX content only by choosing to.
- **No changes** to the podcast audio, the episode scripts, or the existing five per-episode sections.
- **No re-skin** of the guide's base typography. APEX-specific sections adopt APEX-Stacked design *cues* (semantic palette, stacked-layer visual) so they read as APEX-family content, within the guide.
- Single self-contained HTML; works offline from `file://`; only external dependency is Google Fonts.

## Reference

- `C:\Stage\Clients\Industries\APEX\docs\reference\APEX-Stacked-Architecture-Narrated.html` — source of the APEX name breakdown, the 7-layer stacked architecture, and the design language (warm-midnight theme, semantic palette: ember identity/trust · sky data · violet schema · teal agent · gold outcomes · amber HITL).
- The 8 episode MP3s in `pc-cross-cloud-agentic/audio/` (durations 34:08 / 39:14 / 37:20 / 45:36 / 42:17 / 38:02 / 41:37 / 37:02).
- The 8 episode scripts `01-*.md` … `08-*.md` — source of section structure for cue generation.

## Four additions

### 1. Audio player + synced timeline + screen-pop (per episode, always visible)

A **player strip** at the top of each of the 8 episode tabs, below the episode header, above ① Content Breakdown:
- HTML5 `<audio controls>` element, `src` = relative `audio/<episode>.mp3`
- A **synced timeline** — a horizontal track with ~9 section markers positioned by timestamp; playhead tracks `timeupdate`; markers clickable to seek
- A **screen-pop "Now Playing" card** — updates at each section boundary with a brief highlight animation; shows the current section title + a key discussion point
- As audio plays, the matching item in ① Content Breakdown also receives an `active` highlight — timeline and breakdown stay in sync

### 2. APEX architecture-linkage + Microsoft learning (per episode, opt-in)

A new collapsed section per episode tab — **⑤ Go Deeper** — a `<details>` collapsed by default, two parts:
- **APEX architecture linkage** — the APEX stack layer(s) this episode realizes, a mini stacked-layer diagram highlighting them, and the framing sentence (podcast teaches the vendor-neutral principle; the APEX layer is Microsoft's productized realization).
- **Microsoft self-learning** — 3-5 curated Microsoft Learn links per episode.

Existing **Vocabulary** section renumbers from ⑤ to ⑥.

### 3. APEX stack overview (Overview tab, opt-in)

A collapsed `<details>` section added to the Overview tab — "The APEX architecture stack — optional linkage": the A·P·E·X name breakdown (Agent-based · Platform · Enterprise · eXecution), the 7-layer stacked diagram, and the note that APEX is Microsoft's productized realization of the generic Acceleration Framework.

### 4. Episode → APEX stack mapping (content)

| Ep | APEX layer(s) |
|---|---|
| 1 | The whole stack (overview) |
| 2 | OneLake · Medallion (Bronze→Silver→Gold) · Fabric Connectors |
| 3 | Orchestration / Foundry · MCP Tool · parent-child agents |
| 4 | Identity & Trust planes (Entra + Purview) · Safety plane |
| 5 | Context / LEDGER · Audit Row · Observability plane |
| 6 | Model Gateway · Observability plane — cost |
| 7 | Model Gateway · Connectors — portability |
| 8 | Service Catalog · Experience Plane · the six envelopes |

The 7 APEX stack layers (from the referenced file): Identity & Trust (Entra + Purview, cross-cutting) · OneLake medallion · Canonical Schema kernel · Orchestration/Foundry · Model-serving planes (Gateway/Safety/Evaluation/Observability) · Context/LEDGER · Service Catalog/Experience Plane.

## Architecture / data flow

- **Cue data:** a `_build_cues.py` script parses each episode `.md`, splits by `## Cold Open` + `### ` section headings + the disagreement + carry-forward, counts words per section, distributes each episode's known final-MP3 duration proportionally (offset ~5s for the opening sting, ~6s reserved for the closing sting), and emits a JS object literal. The cue data is embedded inline in the HTML — browsers block `fetch()` of a separate JSON on `file://`.
- **Player JS:** vanilla. On episode-tab activation, the `<audio>` `src` is already set. `timeupdate` → find current cue → update Now-Playing card + active timeline marker + active breakdown item. Marker/topic click → set `audio.currentTime`.
- **localStorage:** unchanged — the existing checklist persistence stays. Playback state is not persisted.

## Microsoft learning links (per episode — finalized at build)

Ep1 AI agents / Azure AI Foundry intro / Agent Framework · Ep2 Microsoft Fabric path / OneLake / Mirroring · Ep3 Foundry Agent Service / Agent Framework SDK / Model Context Protocol · Ep4 Microsoft Purview / DSPM for AI / Microsoft Entra / Responsible AI · Ep5 Purview audit / Foundry observability & tracing / AI governance · Ep6 Microsoft Cost Management / FinOps on Azure / Copilot adoption · Ep7 Azure AI model catalog / Azure Arc / multicloud · Ep8 Cloud Adoption Framework / Azure Well-Architected / Foundry. Real Microsoft Learn URLs (prefer stable product/training hub URLs).

## Testing / verification

- HTML renders; all 9 tabs still wired; tag balance (div/section/details/script) preserved
- 8 player strips; 8 `<audio>` elements with correct relative `src`; cue arrays present for all 8 episodes
- 8 Go Deeper `<details>` collapsed by default; APEX stack overview `<details>` collapsed by default
- APEX name appears ONLY inside `<details>` (collapsed) — never in the always-visible default view
- Content discipline on the non-APEX surface unchanged — no forbidden vocabulary, generic
- JS brace/paren balance; existing checklist persistence still works
- `_build_cues.py` runs and produces cue data for all 8 episodes

## Out of scope (YAGNI)

Transcript scrolling · waveform · playback-speed UI beyond the native player · quiz mode · re-skinning the guide's base typography · precise (build-instrumented) timestamps · changes to audio or scripts · a separate companion file.

---

**Next:** invoke `superpowers:writing-plans` for the bite-sized implementation plan.
