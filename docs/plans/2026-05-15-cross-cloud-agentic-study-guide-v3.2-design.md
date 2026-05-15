# Cross-Cloud Agentic Study Guide v3.2 — Client Intake + Import + Player UX — Design

**Date:** 2026-05-15
**Status:** Design approved · ready for writing-plans handoff
**Modifies:** `Cross-Cloud-Agentic-Study-Guide.html` (~375 KB after v3.1)
**Adds:** `pc-cross-cloud-agentic/clients/_client-intake-template.md` (new) + `clients/` folder

## Goal

Three things: (1) a runnable Markdown intake template that produces a comprehensive per-client `.md`; (2) an Import pipeline so that client `.md` prepopulates the guide's profile, axis positions, likelihood, and actions in one step; (3) fix and enrich the keyword treeview — auto-expand and highlight the section being played, and stop a keyword/section click from reseeking the audio.

## Part 1 — Client intake MD template

A new file `pc-cross-cloud-agentic/clients/_client-intake-template.md`. It is a **prompt template** — the seller (or an operator) runs it in Claude.

When run, Claude:
1. Lists the existing `clients/*.md` files (excluding the template) and asks the seller to **pick one from the list to refresh, or name a new client**.
2. Researches the named client from **public sources** — recent news, earnings commentary, cloud/AI announcements, job postings, leadership changes.
3. Drafts, for that client:
   - The **Client Profile** fields — industry, current clouds, AI maturity, key signals.
   - A position on **each of the 24 axis questions** (8 episodes × 3) — an integer `0–4` on the pole scale, a one-line rationale, and a **confidence flag** (`high` / `medium` / `low`, `low` where research was thin).
4. Writes `clients/<client-slug>.md` — a comprehensive, human-readable document:
   - Client overview and the researched profile.
   - Per-episode axis rationale: each axis, the chosen position, the rationale, the confidence, and a source.
   - A research-sources list.
   - A final section **"## Import data"** containing **one fenced `json` code block** — the guide-importable client record.

The template embeds the 24 axis questions (id, the two poles, the Microsoft-favorable pole) so it is self-contained.

The generated `clients/<client>.md` files are the seller's working files (not committed to the repo); the template itself is committed.

### The import-data JSON block

The `json` block holds a single client record matching the guide's store schema:
```json
{
  "schema": 3,
  "client": {
    "id": "<slug>",
    "name": "<Client Name>",
    "profile": { "industry": "", "clouds": "", "aiMaturity": "", "signals": "" },
    "axes": { "e1": { "e1-ax1": 3, "e1-ax2": 2, "e1-ax3": 4 }, "...": {} },
    "paq": {}, "actions": {}, "notes": []
  }
}
```
`axes` carries every answerable axis (0–4). `notes` may carry the research sources as starter notes.

## Part 2 — Import pipeline

The Overview "Import" control currently reads a JSON file and merges `data.clients`. v3.2 extends it:

- The file input accepts **`.md`** as well as `.json`.
- On read: locate the **first fenced ` ```json … ``` ` block** in the text; if found, parse that; otherwise parse the whole text as JSON (existing `.json` path).
- Accept three shapes: `{clients:{…}}` (existing multi-client export), `{client:{…}}` (a single record — the template output), or a bare client record `{id,name,profile,axes,…}`.
- Add/replace the client in `SG3.clients`, **set `SG3.activeClientId` to that client's id**, `sg3Save()`, then `hydrateClient()`.

Because `hydrateClient()` already re-applies profile fields, axis selectors, likelihood bars, seller-action emphasis, and notes for the active client, a single import **prepopulates the whole guide and the Client Profile dialog at once**. The imported client is then in the nav selector **list** for the seller to pick.

A missing/garbled json block shows a friendly message; nothing is partially applied.

## Part 3 — Player keyword UX

Three changes to the keyword treeview built in v3.

### 3a. Fix the reseek bug

Today each timeline section row carries two click handlers — the v2 one (`audio.currentTime = cue.t`, a seek) and the v3 one (toggle the keyword tree). Revealing keywords therefore yanks the audio. Fix:
- Remove the toggle-on-row-click handler.
- Make the disclosure triangle a **real element** (`<span class="kw-toggle">`, replacing the CSS `::after`); clicking it toggles the tree and calls `stopPropagation()` — no seek.
- Row-body click keeps the v2 seek (intentional timeline navigation).
- A keyword node click opens the modal, `stopPropagation()`, and never touches the audio.

### 3b. Auto-expand the section being played

In the player's `timeupdate` section-change logic: when playback enters section *i*, add `.open` to that section's row + `.kw-children`, and remove `.open` from the other sections in that episode's list. A manual toggle between section changes still works; the next section change re-syncs.

### 3c. Highlight keywords being discussed

While section *i* is the current section, its keyword nodes carry a `.kw-now` highlight class (a distinct accent — e.g. an amber glow). Per-section granularity (no per-word audio timing exists). Cleared when playback leaves the section.

## Architecture / build

- New file: `clients/_client-intake-template.md`; new `clients/` folder.
- HTML changes: extend the import handler; extend `keywordTreeInit()` and the player's section-change code; one new CSS rule (`.kw-toggle`, `.kw-node.kw-now`).
- Vanilla JS; one HTML file; small size delta.

## Testing / verification

- The template file exists, lists all 24 axes, is internally consistent.
- Import of a `.md` with a json block: client added, set active, profile + axes + likelihood + actions + notes all prepopulate; import of legacy `.json` still works; a bad file shows a message and changes nothing.
- Keyword treeview: clicking the disclosure toggles without seeking; clicking a keyword opens the modal without seeking; clicking the row body still seeks; the playing section auto-expands and its keywords highlight; HTML/JS balance preserved; `node --check` passes.
- APEX still opt-in; content discipline clean.

## Out of scope (YAGNI)

Per-word keyword timing · the guide reading the `clients/` folder directly (a static file cannot) · auto-running the template from the guide · committing generated client files · changes to audio or scripts.

---

**Next:** invoke `superpowers:writing-plans`.
