# Cross-Cloud Agentic Study Guide v3.1 — "Win the Deal" section — Design

**Date:** 2026-05-15
**Status:** Design approved · ready for writing-plans handoff
**Modifies:** `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic\Cross-Cloud-Agentic-Study-Guide.html` (~322 KB after v3, 10 tabs)

## Goal

Add one new per-episode section — **⑦ Win the Deal** — combining two things the seller asked for: a "How to say it · How to position it" talk-track for winning the deal, and a "References & follow-up" list of the episode's cited references as curated authoritative links, each saveable into My Notes.

## Decisions (from brainstorming)

- Both parts live **together in one new per-episode section**, not split between the Note Card and a separate block.
- The section is appended as **⑦**, after the existing ⑥ Vocabulary — no renumbering of existing sections.
- The episode scripts' `## Further reading` sections cite references mostly by **name** (analyst reports, product docs, standards), only a few with URLs. The build **curates a real authoritative URL** for each cited reference.

## Key constraints

- One self-contained HTML; offline from `file://`; Google Fonts the only external dependency.
- No changes to audio, episode scripts, or the existing six per-episode sections, the v3 axis view, keyword/modal, multi-client store, or the APEX opt-in `<details>`.
- Reuse existing component families — `.block` / `.block-label`, the `<details class="godeep">` collapse pattern, and the v3 Save-to-My-Notes mechanism.
- Content discipline unchanged — generic, "the Acceleration Framework", no forbidden vocabulary, APEX only inside opt-in `<details>`.

## The new section — ⑦ Win the Deal

A standard visible `.block` in each of the 8 episode panels, placed after the ⑥ Vocabulary block. `<div class="block-num">7</div><h3>Win the Deal</h3>`. Two parts:

### Part 1 — How to say it · How to position it

A talk-track: per episode, **3–4 paired entries**. Each entry has:
- **Say it** — a short, verbatim line the seller can use in the room.
- **Position it** — the strategic move behind the line and why it lands.

Drawn from each episode's pivot, disagreement resolution, and carry-forward. Always visible (not collapsed) — this is the deal-winning core of the section. Rendered as a list of paired cards; the "Say it" line is quoted/emphasized, the "Position it" line is supporting text.

### Part 2 — References & follow-up

A collapsed `<details>` (the `.godeep` pattern), titled "References & follow-up". Inside, the episode's cited references — taken from that episode's `## Further reading` — grouped by category (e.g. Analyst · Standards · Microsoft · AWS · Google Cloud · Independence). Each reference is a row: a curated **authoritative link** (the script's URL where present; otherwise a curated stable hub URL — Microsoft Learn, AWS/GCP doc hubs, nist.gov, the EU AI Act page, analyst-firm pages), a one-line descriptor, and a **"＋ Save to My Notes"** button that adds the reference to the active client's My Notes for post-meeting follow-up.

## Data model

Two new inline build-time JS objects beside `EP_CUES` / `EP_AXES` / `EP_ACTIONS` / `EP_KEYWORDS`:

- `EP_POSITIONING` — per episode, an array of `{say, position}`.
- `EP_REFS` — per episode, an array of `{category, label, url, note}`. `label` is the reference name; `url` the curated authoritative link; `note` a one-line descriptor; `category` the group heading.

Both embedded inline (browsers block `fetch()` of a separate file on `file://`).

## Save-to-My-Notes integration

The reference "Save to My Notes" reuses the v3 notes pipeline. A saved reference becomes a note object `{id, kw:<reference label>, ep, detail:<note + url>, userText:'', ts}` pushed onto `sg3Active().notes` and rendered by the existing `renderNotes()`. The note's detail carries the URL so it is clickable / copyable from the My Notes tab. (My Notes rendering may need a minor tweak so a URL in a note is shown as a link.)

## Architecture / build

- New CSS: `.wtd` wrapper, `.say-it` / `.position-it` paired-card styling, `.ref-group` / `.ref-row` / `.ref-save` for the references list. Reuse `.godeep` for the collapsed references block.
- New markup: one `.block` (⑦ Win the Deal) per episode panel, after ⑥ Vocabulary.
- New JS: a `winDealInit()` that renders `EP_POSITIONING` and `EP_REFS` into each episode's section ⑦ and wires the per-reference Save-to-My-Notes buttons.
- Vanilla JS; one HTML file; the file grows ~30–45 KB.

## Testing / verification

- HTML renders; 10 tabs intact; 8 new `<h3>Win the Deal</h3>` blocks; tag balance preserved; JS brace/paren balance; `node --check` passes.
- `EP_POSITIONING` and `EP_REFS` present for all 8 episodes; every `EP_REFS` entry has a non-empty `url`.
- Each episode's section ⑦ shows the talk-track and a collapsed References block; Save-to-My-Notes adds a note to the active client and it appears in My Notes.
- APEX still opt-in; content discipline clean.

## Out of scope (YAGNI)

Live link-checking · per-reference annotations beyond one line · printing section ⑦ with the Note Card · a global references index · changes to audio or scripts.

---

**Next:** invoke `superpowers:writing-plans` for the implementation plan.
