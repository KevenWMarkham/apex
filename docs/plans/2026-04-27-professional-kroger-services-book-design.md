# Professional Kroger Services — Book Design

**Date:** 2026-04-27
**Author:** Keven Markham (with Claude)
**Status:** Approved (brainstorming complete; ready for plan)

## Purpose

Build a single-file HTML book that wraps the 17 Kroger pursuit artifacts under
`Consumer/Retail/Kroger/02_projects/FY27_Pipeline/assortment-pricing-agentic/deliverables/`
into a coherent engagement narrative. The book is the read-front-to-back
companion to the artifact set: a seller can read it cold to get smart on the
Kroger pursuit, then click through to underlying deliverables for depth.

The reference look-and-feel is `docs/book/Professional-APEX-Sellers-Guide.html`
(the Wrox-style 5-part book). This new book uses the same visual system,
sidebar navigation, callouts, mermaid diagrams, search, and dark-mode toggle.

## Scope decisions (from brainstorming)

| Decision | Choice |
|---|---|
| Book scope | **Services-focused** — anchored on the Kroger service portfolio (RC-E2E-03 + RC-E2E-09 + shared) |
| Structure | **Engagement arc** — 5 parts following Why → Services → Architecture → Pursuit → At Scale |
| Voice | **Hybrid** — internal Deloitte sellers as primary voice, with embedded client-presentable narrative blocks (Store-100-style "Kroger Store 412") |
| Artifact handling | **Hybrid** — narrative is rewritten inline; each chapter ends with a *Companion Artifacts* callout linking the underlying files |
| Output location | `Consumer/Retail/Kroger/02_projects/FY27_Pipeline/assortment-pricing-agentic/deliverables/Professional-Kroger-Services.html` (sits next to the artifacts so relative links work without rewriting) |

## Architecture

Mirror the Sellers Guide build pattern (proven, in production):

- `kroger-services-content.cjs` — chapter content keyed by part/chapter id; markdown-ish strings with embedded mermaid blocks and callout markers
- `build-kroger-services.cjs` — the renderer; copy of `build-sellers-guide.cjs` with new content import and new output path

Both files live in the APEX repo root (alongside `build-sellers-guide.cjs` /
`sellers-guide-content.cjs`). Build command:

```bash
node build-kroger-services.cjs
```

Output is the single self-contained HTML file (CSS + JS embedded; mermaid
pre-rendered to PNG and inlined as base64, same as the Sellers Guide). The
book references the 17 artifacts using **relative paths** from the deliverables
folder.

## Outline (5 parts, 22 chapters)

### Part I — Why Kroger, Why APEX
1. **Foreword** — how to use this book; sellers vs. client-narrative split
2. **Kroger Strategic Context** — public signals (84.51°, Boost, Ocado, Restock, FreshFlex, post-Albertsons posture)
3. **Where Margin Moves at Kroger** — the agentic-AI thesis for grocery
4. **APEX Wedge into the Kroger Estate** — Microsoft pillars at Kroger; coexistence with 84.51° / Ocado / GCP

### Part II — The Service Portfolio
5. **The Two Anchors at a Glance** — RC-E2E-03 + RC-E2E-09 in one frame
6. **RC-E2E-03 Assortment & Pricing Intelligence** — absorbs Walkthrough, OnePager, Personas, Six-Agents Deep Dive, Use-Case Catalog
7. **RC-E2E-09 Product Tracking & FSMA 204 Traceability** — absorbs FSMA-204 Checklist
8. **The High-Attach Catalog** — the other 6 RC services tier-ranked for Grocery Merchandising (from `APEX-RC-Grocery-Merchandising-Service-Portfolio.docx`)
9. **Cross-Grocer Differentiation** — Kroger vs. Albertsons / Publix / HEB / Ahold (from `APEX-RC-E2E-03-Cross-Grocer-Comparison.xlsx`)

### Part III — The Architecture
10. **System of Record** — Bronze→Silver, ERD
11. **The Fabric Plane** — Runbook, semantic model
12. **The Foundry Plane** — six agents, sequence diagram
13. **The MCP Layer** — server deep-dive
14. **Purview & Governance** — Privacy/Data-Governance Spec, AI/ML Model Spec

### Part IV — The Pursuit
15. **Executive Engagement** — One-pager, ROI Case, Persona journeys
16. **The Pitch** — pitch-deck walkthrough
17. **Risk & Stakeholders** — Risk Register, Stakeholder Map
18. **The Demo** — Demo Script & Walkthrough Guide
19. **Kroger Store 412 — A Day in the Shift** — client-presentable narrative, Store-100 pattern: 8 events across one shift at a Cincinnati Marketplace store

### Part V — At Scale
20. **Operations & Test Strategy** — Service Operations Playbook, Test Strategy
21. **The Service Roadmap** — multi-wave envelope
22. **Cross-Grocer Expansion Pattern** — extending the Kroger pattern to other grocers
23. **The Kroger Compact** — closing chapter, seller actions

(Total chapters reads as 22 because the Foreword is unnumbered in the Sellers
Guide convention; the body chapters are 1–22.)

## Per-chapter pattern

Each chapter follows the Sellers Guide template:

- Chapter header (number + title)
- **What This Chapter Does for You** objectives box (4 bullets)
- Body sections (`##` and `###` per topic)
- **Companion Artifacts** callout listing underlying deliverables with relative links
- **Key Takeaways** summary block (3–5 bullets)
- **Seller Actions** exercises block (3 imperative-voice items)

The client-presentable Ch 19 ("Kroger Store 412") additionally carries an
**Independence Reminder** callout at top and bottom positioning the narrative
as "Deloitte-delivered agents on Kroger's Microsoft platform" (APEX stays
unmentioned in the narrative itself).

## Visual system (inherited from Sellers Guide)

- Topbar with Kroger book brand, search, theme toggle, font-size controls
- Left sidebar: 5 collapsible parts → chapter list, current chapter highlighted via IntersectionObserver
- Cover page: navy/gold gradient, "Professional Kroger Services" title, "The Anchor-Account Companion to APEX RC-E2E-03 + RC-E2E-09" subtitle
- Callout types: Note, Warning, Best Practice, Independence, Key Play, Companion Artifacts (new — gold-bordered)
- Mermaid diagrams pre-rendered to PNG via `@mermaid-js/mermaid-cli` and inlined as base64 (same caching scheme: `.cache/mermaid/<hash>.png`)
- Print stylesheet for PDF export

## Build dependencies

Same as Sellers Guide:
- Node.js (already used by other `.cjs` builders)
- `@mermaid-js/mermaid-cli` (already in `node_modules`)
- No new packages required

## Risks & considerations

1. **Length** — Sellers Guide content file is ~17K lines; this book has fewer
   chapters but each chapter is artifact-rich. Estimate ~10–12K lines of
   content. Manageable.
2. **Artifact link integrity** — relative links assume the book sits at the
   deliverables folder root. If the folder is reorganized, links break.
   Document the placement clearly in the build script header.
3. **Public-source discipline** — Ch 1 ("Strategic Context") must source only
   public Kroger signals; carry an Independence Reminder consistent with the
   Sellers Guide chapter 16 pattern.
4. **Store 412 narrative** — invented illustrative content; must be flagged as
   "illustrative reference deployment" the way Store 100 is. Include explicit
   disclaimer.

## Out of scope

- DOCX export (HTML only for now; can add later via existing `build-docx.cjs` pattern)
- Per-service standalone books (this is one book covering the full portfolio)
- Updates to the underlying 17 artifacts (book wraps them as-is)
- Adding services beyond what's in the deliverables folder

## Definition of done

- `build-kroger-services.cjs` and `kroger-services-content.cjs` exist in the APEX repo root
- Running `node build-kroger-services.cjs` from the APEX repo root produces `Professional-Kroger-Services.html` at the deliverables folder path with no errors
- Output HTML opens in a browser, sidebar navigates, all 22 chapters render, all Companion Artifacts links resolve to existing files
- Mermaid diagrams render
- Search, dark mode, font-size controls work
- File size in the same order of magnitude as the Sellers Guide (~3–4 MB)
