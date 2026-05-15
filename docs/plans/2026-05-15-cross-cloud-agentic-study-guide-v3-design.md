# Cross-Cloud Agentic Study Guide v3 — Design

**Date:** 2026-05-15
**Status:** Design approved · ready for writing-plans handoff
**Modifies:** `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic\Cross-Cloud-Agentic-Study-Guide.html` (currently ~236 KB, 9 tabs, after v2)

## Goal

Turn the study guide from a reference artifact into a **working seller tool**: a per-episode interactive "Client Axis View" that scores Microsoft-attachment likelihood and prescribes next-step actions; a keyword deep-dive treeview with detail modals and saved notes; and a multi-client manager so a seller can keep engagement data for several clients in one guide.

## Key constraints

- **One self-contained HTML.** No companion files. Works offline from `file://`. Only external dependency is Google Fonts. The file will grow past ~320 KB — acceptable.
- **No changes** to the podcast audio, the episode scripts, the v2 audio player / cue data, or the APEX opt-in `<details>` (APEX stays opt-in, collapsed).
- **No re-skin.** v3 reuses the existing house style and component families (`.cc-bar`, `.paq-details`, `.godeep`, `.np-list`).
- **No runtime web access.** A static offline file cannot research the web. Client research is a seller-entered, saved activity — the guide provides the structure and persistence, not live data fetching.
- **Client-safe by default.** The guide ships with no client data; the built-in "General" profile is the default. Client records exist only in the local browser (localStorage) and in JSON the seller chooses to export.

## Reference

- The v2 design `2026-05-15-cross-cloud-agentic-study-guide-v2-design.md` and plan — the audio player, `EP_CUES`, the Go Deeper / APEX sections this builds beside.
- Screenshots from the user: the Cloud Comparison bars (the visual family for the likelihood bar), the Pivot & Axis section ③, and the player topic list `.np-list` (the treeview target).

## Four parts

### Part A — Pivot & Axis → "Client Axis View" (per episode, section ③)

The existing section ③ is a collapsed `.paq-details` checklist of `.paq` questions, each with an AXIS (two poles) and BASELINES. v3 makes it interactive and outcome-scoring.

1. **Interactive axis selectors.** Each `.paq` question gains a 5-point segmented control — `Strongly A · Leans A · Neutral · Leans B · Strongly B` — and the seller marks where the client sits. Each axis is annotated (build time) with its **Microsoft-favorable pole** (`A` or `B`) and a **weight**. The selector replaces nothing — the question, AXIS poles, and BASELINES stay; the control sits beneath them. The existing "tick as you ask" checkbox is kept.

2. **Microsoft Attachment Likelihood bar.** Below the checklist, a new bar reusing the Cloud Comparison `.cc-bar` / `.cc-fill` visual family. It fills from the **weighted share of axes leaning Microsoft-favorable** — each answered axis contributes its weight × a 0–1 position score (Strongly-favorable = 1, Neutral = 0.5, Strongly-against = 0). Unanswered axes are excluded and shown as "n of m axes answered". A label band reads `LIKELY` / `CONTESTED` / `OPEN` / `UNLIKELY` by threshold. A **generated reason line** names the supporting and opposing axes — e.g. *"3 of 4 axes favor a composed-with-Microsoft path; the cross-cloud-data axis works against it."* Recomputes live on every selector change.

3. **Seller Actions dropdown.** A `<details class="godeep">`-style block, **collapsed by default** — *"Actions to shift the tide toward Microsoft."* Inside, a localStorage-persisted checklist of concrete next-step actions. Each action is curated (build time) and tagged to the axis it addresses and the triggering position; when the client's current answer on that axis is non-favorable, the action is **emphasized** (the others remain visible as context). Each action carries enough framing — the why, the axis, the proof to bring — to act on.

### Part B — Keyword Deep-Dive (in the player topic list `.np-list`)

The v2 player topic list shows one row per timeline section. v3 makes it a treeview.

1. **Treeview.** Each section row gains a disclosure triangle; expanding it reveals that section's **curated keywords** as indented child nodes (`Section → keywords`). The keyword set is hand-curated per section at build time, folding in the episode's Vocabulary (section ⑥) terms where they fit. Expansion state is transient (not persisted).

2. **Keyword modal.** Clicking a keyword opens a centered popup modal (overlay + dialog, focus-trapped, `Esc` / backdrop to close): the keyword, a crisp definition, a "why it matters for the deal" line, and 1–3 curated links (Microsoft Learn or authoritative sources). A **"Save to Notes"** button writes it to the active client's notes (Part C).

### Part C — Notes panel

A new tab — **"⑩ My Notes"** (added after the 9 existing tabs; tab bar already has horizontal scroll). Saved keyword notes collect here as cards: keyword · source episode · the detail text · an editable free-text box for the seller's own words · timestamp. Per-note delete; panel-level copy-all (to clipboard) and clear-all. All notes belong to the **active client** and persist in that client's record.

### Part D — Multi-client manager

The guide holds any number of **client records**, each a JSON object, all in one localStorage entry.

- **Client selector.** A compact control in the sticky top nav — a `<select>` of saved clients plus an "＋ Add client" affordance. Selecting a client makes it active and re-hydrates all interactive state.
- **Client Profile section** (Overview tab). Editable fields for the active client: name, industry, current clouds, AI maturity, key signals (free text). Add / rename / delete clients. **Export all** (download the whole multi-client JSON) and **Import** (load a JSON file, merging clients). Per-the-screenshot recommendation, this is where a seller records research gathered from public newsfeeds / authoritative sources.
- **"General" default.** A built-in, undeletable client named "General (no client)" — the active client on first load and the client-safe default. The guide ships with only "General".
- **Scoping.** Every piece of client-engagement state — Part A axis positions, Pivot & Axis question checkboxes, Part A seller-action checkboxes, Part C notes, the profile fields — is stored under the active client. Switching clients swaps all of it. Global state (theme) is not scoped.

## Multi-client data model

One localStorage key, `ccap-study-guide-v3`, holding:

```json
{
  "schema": 3,
  "activeClientId": "general",
  "clients": {
    "general": {
      "id": "general",
      "name": "General (no client)",
      "profile": { "industry": "", "clouds": "", "aiMaturity": "", "signals": "" },
      "axes":     { "e2": { "e2-ax1": 3, "e2-ax2": 1 } },
      "paq":      { "e2-q1": true },
      "actions":  { "e2-act1": true },
      "notes":    [ { "id": "...", "kw": "OneLake", "ep": "e2",
                      "detail": "...", "userText": "", "ts": 1747300000000 } ]
    }
  }
}
```

- IDs: `general` is fixed; new clients get a short generated id. Axis ids `e<N>-ax<k>`, action ids `e<N>-act<k>`, paq ids reuse the existing `<panelId>-q<index>` scheme.
- **Migration:** the v2 checklist key `ccap-study-guide-checklist-v1`, if present, is read once and folded into `clients.general.paq`, then left untouched (no destructive delete).
- Reads/writes are funnelled through a small accessor layer so a missing/corrupt entry falls back to a fresh `{schema:3, activeClientId:"general", clients:{general:{…}}}`.

## Architecture / data flow

- **Build-time data** — three new inline JS objects beside `EP_CUES`:
  - `EP_AXES` — per episode, an array of axis descriptors: `{id, label, poleA, poleB, msPole:"A"|"B", weight, baseline}`. Mirrors the existing `.paq` questions; the `.paq` markup is annotated with matching `data-axis` / `data-ms-pole` so JS can bind selectors to the rendered questions.
  - `EP_ACTIONS` — per episode, an array of seller actions: `{id, axis, triggerPole, label, detail}`.
  - `EP_KEYWORDS` — per episode, keyed by section (cue index), an array of `{term, def, why, links:[{label,url}]}`.
- **Runtime JS (vanilla, no libraries):**
  - `store` accessor — load/save the v3 JSON, get/set active client, get/set scoped values.
  - `axisInit()` — renders the 5-point selectors onto each `.paq`, wires change → save + `recalcLikelihood(ep)`.
  - `recalcLikelihood(ep)` — weighted score → `.cc-fill` width + label band + reason line; emphasizes matching actions.
  - `keywordTreeInit()` — extends the v2 `.np-list` rows with disclosure + keyword child nodes; keyword click → `openKeywordModal()`.
  - `notesInit()` / `renderNotes()` — the My Notes tab.
  - `clientInit()` — the nav selector + Overview Client Profile section; switching active client re-runs the hydrate pass.
  - A single `hydrateClient()` re-applies the active client's state to every control; called on load and on client switch.
- The v2 `playerInit()` and `paqInit()` are extended, not replaced; the v2 cue/player behavior is unchanged.

## Testing / verification

- HTML renders; all tabs wired (now 10); tag balance preserved; JS brace/paren balance; `node --check` passes.
- 8 episodes × axis selectors present; each `.paq` annotated with `data-axis` + `data-ms-pole`; `EP_AXES`/`EP_ACTIONS`/`EP_KEYWORDS` present for all 8 episodes.
- Likelihood bar recomputes on selector change; reason line names supporting/opposing axes; unanswered axes excluded.
- Keyword treeview expands; modal opens, traps focus, closes on `Esc`/backdrop; "Save to Notes" lands a card in My Notes.
- Multi-client: add / rename / delete / switch clients; switching re-hydrates axes, checkboxes, notes, profile; "General" undeletable; export downloads valid JSON; import merges; v1 checklist migrates into `general.paq`.
- APEX still opt-in (collapsed `<details>` only); content discipline on the generic surface unchanged.

## Out of scope (YAGNI)

Live web research / API calls · server sync · multi-user / accounts · rich-text notes · PDF export of notes · undo history · keyword search box · re-skinning · changes to audio, scripts, or the v2 player/cue behavior · auto-deriving axis positions from the profile (the seller sets them).

---

**Next:** invoke `superpowers:writing-plans` for the bite-sized implementation plan.
