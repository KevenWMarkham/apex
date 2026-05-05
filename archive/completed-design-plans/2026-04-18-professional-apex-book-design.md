# Professional APEX Book — Design

**Date:** 2026-04-18
**Status:** Approved — implementation proceeding directly (user skipped writing-plans)
**Sources:** `docs/APEX-developer-implementation-guide.docx` (+ underlying markdown), `docs/APEX-comprehensive-solutions-reference.docx`

## 1. Purpose

Produce a single Wrox-style technical book — *Professional APEX: Agentic Platforms on Microsoft Fabric* — that combines the Developer Implementation Guide and the Comprehensive Solutions Reference into one 500+ page programmer-grade title. Delivered as a single self-contained HTML file so a reader can open one artefact and navigate the entire corpus.

## 2. Audience

Technical-forward but mixed: architects, senior developers, delivery leads. The "Professional X" title pattern signals depth. Strategic material is retained but the reader is assumed to be a hands-on practitioner.

## 3. Architecture

### 3.1 Output

- **One self-contained HTML file:** `docs/book/Professional-APEX.html`
- Inline CSS, inline fonts (or webfont links), inline rendered Mermaid PNGs (base64 or referenced)
- Size target: 2.5–4 MB
- Opens in any modern browser; prints cleanly via CSS `@media print`

### 3.2 Build pipeline

`build-professional-apex.cjs` — Node script that:
1. Reads the existing markdown sources (`docs/APEX-developer-guide.md`, `docs/dev-guide/*.md`, `docs/APEX-comprehensive-solutions-reference.md`)
2. Parses with the same hand-rolled parser used by sibling scripts
3. Adds Wrox wrapper elements programmatically:
   - Part openers with numbered title pages
   - Chapter openers with "What You'll Learn in This Chapter" bulleted objectives
   - Code language tab switcher for Python/C# blocks
   - Inserts NOTE / WARNING / BEST-PRACTICE / TRY-IT-OUT callouts where source markdown uses `>` blockquotes with specific conventions
   - End-of-chapter Summary section
   - End-of-chapter Exercises (2–4 per chapter)
4. Renders Mermaid through the existing `.cache/mermaid/` cache
5. Emits one HTML file with sticky sidebar TOC, keyboard nav, and search

### 3.3 Content reuse strategy

**No rewrites.** The entire book body is drawn from existing markdown. Approximately 10–15 % is net-new authoring confined to:
- Part openers (6 short intros)
- Chapter "What You'll Learn" openers (30 bulleted lists)
- Chapter Summary sections (30 short synopses)
- Exercises (~90 numbered exercises across 30 chapters)
- Appendix J (Exercise Solutions) — NEW appendix
- Index — programmatically generated from headings + key-term scan

## 4. Structure

### 4.1 Narrative Parts (30 chapters)

| Part | Chapters | Source |
|---|---|---|
| **I — Introducing APEX** | 1–3 | Reference Exec Summary, Forces of Change, IT Simplification |
| **II — The APEX Framework** | 4–7 | Reference Framework + Dev Guide companions 02/03/04 intro material |
| **III — Building on APEX** | 8–14 | Dev Guide companions 01–06 (full) + Reference Security chapter |
| **IV — APEX in the Enterprise** | 15–21 | Reference Practice chapters (RC/HLS/ER/AXLE/TMT/TH/ICE) + E2E and TTP deep-dives |
| **V — Delivery & Operations** | 22–26 | Reference Part IV (waves, runbooks, governance, change, commercial) |
| **VI — The Future of APEX** | 27–30 | Reference Part V (tiers, flagships, dependency chain, roadmap) |

### 4.2 Appendices

| Appendix | Content | Source |
|---|---|---|
| A | Schema Reference | Ref App A |
| B | Service Catalog (45 services) | Ref App B |
| C | KPI Master Registry (80+ KPIs) | Ref App B2 |
| D | Orchestration Catalog (47 ORCHs) | Ref App C |
| E | Persona Catalog (39 personas) | Ref App D |
| F | MCP Tool Catalog (165+ tools) | Ref App E (exhaustive) |
| G | Microsoft Product & SKU Reference | Ref App F |
| H | Partner Ecosystem | Ref App G |
| I | Glossary | Ref App H |
| J | Exercise Solutions | NEW |

Plus an alphabetised Index generated from chapter headings and glossary terms.

## 5. Wrox conventions

- **Palette:** Wrox red `#B8232F` (accent), APEX teal `#2DD4BF` (secondary), Aptos Display headings, Source Serif 4 body, Cascadia Mono code
- **Part openers:** full-page dramatic spread with Part number, title, chapter list, one-paragraph intro
- **Chapter openers:** "What You'll Learn in This Chapter" bullets + context paragraph
- **"Try It Out" boxes:** red left-rule, numbered per chapter, step-by-step, captioned "How It Works" explanation, expected result
- **Callouts:** coloured left-rule for Notes (blue), Warnings (amber), Best Practices (green)
- **Code:** Python / C# tabs, language label, line numbers, Cascadia Mono
- **End-of-chapter:** Summary + Exercises
- **Index:** alphabetised, anchor-linked

## 6. UX

- Sticky left sidebar TOC with Part/Chapter collapsibles
- Top bar: book title + chapter title + progress indicator + dark-mode toggle
- Keyboard: `J/K` next/prev chapter, `G` jump-to-TOC, `/` focus search
- In-page search box (client-side text filter)
- Print stylesheet hides nav

## 7. Length target

- 6 Parts × avg 5 chapters × avg 13 pages = ~390 pages narrative
- 10 appendices × avg 13 pages = ~130 pages reference
- Front matter + index = ~30 pages
- **Total: ~550 pages** (HTML equivalent at Wrox page density)

## 8. Build script

Single file `build-professional-apex.cjs`, ~1000 lines of Node. Reuses Mermaid rendering logic, markdown parser style, and callout conventions from the existing `build-dev-guide-docx.cjs` and `build-reference-docx.cjs` scripts.

## 9. Risks & mitigations

| Risk | Mitigation |
|---|---|
| HTML file gets too large (> 10 MB) | PNG embed via base64 only for key diagrams; link out for long code samples |
| Wrox brand concerns | Book is labelled "Wrox-style" internally; no actual Wrox logo or trade dress used |
| Content staleness (source docs evolve) | Build script is idempotent; re-run produces fresh book from current sources |
| Single-file HTML performance | Lazy-render chapters via IntersectionObserver; sidebar TOC is always light |

## 10. Deliverables

1. `docs/book/Professional-APEX.html` — final book
2. `build-professional-apex.cjs` — build script
3. This design doc at `docs/plans/2026-04-18-professional-apex-book-design.md`
4. CHANGELOG entry

## 11. Out of scope

- A proper print-ready PDF (reader can use browser Print → Save as PDF)
- DOCX version (user explicitly chose HTML)
- Separate author attribution / ISBN / publisher data
- Commentary on existing Wrox titles or any third-party IP

## 12. Approval

Design approved by user on 2026-04-18 with instruction to proceed directly to implementation (skip formal implementation plan).
