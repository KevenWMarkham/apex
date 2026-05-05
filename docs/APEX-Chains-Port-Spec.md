# Chains Port Specification

**Sprint 29 Task 29.8 (BL.P.193).** Build-instruction markdown for porting
the **Chains tab** from `APEX-Stacked-Architecture-Narrated.html` (Sprint
27) into the main `Professional-APEX-Sellers-Guide.html` build pipeline.

This document is the engineering brief — it lists every component to
move, every dependency to embed-vs-reference, and every merge-conflict
to avoid when the front-end engineer executes the port.

---

## §1 Goal

Embed the Sprint 27 Chains tab — 35 featured scenarios + 723-row modal
library + Wave Ribbon visualization + per-Practice cinematic banners —
inside the v1.4 Sellers Guide HTML so a single deliverable carries:

1. The narrative sales / governance content (existing Sellers Guide v1.4 chapters)
2. The complete Scenario Library + Wave Ribbons (current Stacked Arch Narrated)
3. The Sprint 28 Wave-data extensions (W1 Foundation catalog cross-links + W3 Fusion mesh cross-links)

End state: one HTML to ship, one HTML to lint, one HTML to publish.

---

## §2 Component inventory

### Components to **embed** (copied / inlined into Sellers Guide HTML)

| Component | Source location (Stacked Arch HTML) | Target placement (Sellers Guide HTML) | Notes |
|-----------|-------------------------------------|----------------------------------------|-------|
| `chains-tab` markup | Tab #9 of 11 | New chapter `§28 — Scenario Chains` after §27 | Single `<section id="chains-tab">` root; preserve all `aria-*` attributes |
| `practice-rail` per-Practice banners (×7) | Inside `chains-tab` | Same — inside the new §28 section | Color tokens already defined in `apex-design-tokens.css` |
| `chain-card` `<details>`/`<summary>` collapsibles | Inside `practice-rail`s | Same | Native HTML5 — no JS dependency |
| `wave-ribbon` per-card | Inside expanded `chain-card` body | Same | Sprint 27 SVG variant + Sprint 28 W1/W2/W3 ribbon cells |
| `scenario-library-modal` (723 rows) | Below `chains-tab` markup | Same — co-located with §28 | Modal trigger button moves into §28 header |
| `kpi-chip` semantic variants | Inline within chain rows | Same | Up/down/money color tokens already in `apex-design-tokens.css` |
| `cross-practice-search` CTA | At top of `chains-tab` | Same | Sprint 28 §28.5 deliverable; opens scenario-library-modal pre-filtered |

### Components to **reference** (link to existing Sellers Guide artifacts)

| Component | Why reference vs. embed |
|-----------|--------------------------|
| Narration deck (Sprint 27 11-tab voiceover) | Tab-specific decks are tied to the Stacked-Arch single-file context; embedding the full speech-synthesis controls would bloat the Sellers Guide HTML |
| Per-Practice anchor agents (Sprint 16) | Cross-link to Appendix D (archetypes) + Appendix F (MCP tools) — those appendices are the source of truth |
| Per-Practice service-codes (Sprint 17) | Cross-link to Appendix L (Scenario Library master catalog) |

---

## §3 Dependencies

### Required (must be present in target HTML before port)

- `apex-design-tokens.css` imported in `<head>` (Sprint 29 Task 29.2 deliverable)
- IBM Plex Sans + Fraunces + JetBrains Mono fonts loaded
- Light/dark theme toggle wiring (`body.light` class switch)
- WCAG 2.2 focus indicator + `prefers-reduced-motion` rules

### Optional (graceful degrade if missing)

- Web Speech API narration controls — Stacked Arch ships with them; Sellers Guide may opt out (the Chains tab content is fully readable without voiceover)
- Browser support for `<details>` native collapsible — every modern browser ships this; IE11 users get a flat fallback layout

---

## §4 Embed-vs-reference decision matrix

For each piece of source-of-truth content, decide whether to embed or
reference:

| Source-of-truth | Decision | Rationale |
|------------------|----------|-----------|
| 35 featured chains content | **Embed** | Sellers Guide is offline-first; chains are the heart of the §28 chapter |
| 723-row modal scenario data | **Embed** (as inline JSON in `<script type="application/json" id="apex-scenario-library">`) | Same reason; total size ~80 KB which is acceptable |
| Wave-ribbon W1/W2/W3 data | **Embed** | Sprint 28 §28.1.2 extended-shape Scenario JSON inlined |
| W1 Foundation catalog (40 blocks) | **Reference** (anchor to Appendix N or the new Foundation-Catalog tab) | Catalog is reusable across artifacts; embedding duplicates content |
| W3 Fusion mesh catalog (36 meshes) | **Reference** (anchor to dedicated Fusion section per Sprint 28 §28.3.4) | Same reason |
| Narration scripts | **Reference** (anchor to `APEX-Appendix-M-Narration-Catalog.md`) | Decks are reused across artifacts; text-only mention in Sellers Guide §28 |
| Per-Practice playbooks | **Reference** (anchor to `apex-registries/playbooks/{practice}.md`) | Sprint 19 Task 19.3 deliverable; already published |
| Independence-language ruleset | **Reference** (anchor to Appendix N §7) | Sprint 29 Task 29.2 deliverable |

---

## §5 Merge-conflict avoidance

The Sellers Guide HTML is built by `build-sellers-guide.cjs`; the
Stacked-Arch HTML is hand-authored / regenerated separately. Both
share design tokens (`apex-design-tokens.css`) and font imports — but
diverge on:

| Concern | Sellers Guide | Stacked Arch | Resolution |
|---------|---------------|--------------|------------|
| Section anchoring | Numbered chapters (§1, §2, …) | Tab IDs (`tab-overview`, `tab-chains`) | Port adds `<section id="chains-tab">` inside the `§28` chapter — keeps both anchor styles working |
| Top-level navigation | Sticky sidebar Table-of-Contents | Tab strip across top | Port adds the §28 chapter to the existing TOC; Stacked-Arch tab strip is **not** ported |
| Cinematic narration | Optional / opt-out | Default-on | Sellers Guide port disables auto-narration; manual play button only |
| Modal z-indexing | `--apex-z-modal: 100` (existing) | Same | No conflict |
| `<details>`/`<summary>` styling | New | Existing | Port adds the styles inside `#chains-tab` scope so it doesn't bleed into other Sellers Guide sections |

### Specific conflicts to watch

1. **Heading-hash anchor IDs.** Stacked Arch uses `id="chain-rc-cold-chain-response"`; Sellers Guide may already have similar IDs. **Fix:** prefix all chain anchors with `chain-` and namespace under the `§28` chapter id (`#s28-chain-rc-cold-chain-response`).

2. **CSS specificity.** Stacked Arch uses some unscoped selectors (`.chain-card`, `.wave-ribbon`). **Fix:** port wraps the entire `<section id="chains-tab">` in a CSS scope; all chain-tab selectors prefixed with `#chains-tab .chain-card` etc.

3. **JavaScript globals.** Stacked Arch defines `window.apexNarrationDecks`. **Fix:** drop this global from the Sellers Guide port; narration is opt-out by default.

4. **Inline `<style>` blocks.** Sellers Guide build script injects styles per-section. **Fix:** add a new `injectChainsTabStyles()` step to `build-sellers-guide.cjs` that emits the chain-tab-specific CSS during chapter §28 assembly.

---

## §6 Implementation steps for the front-end engineer

1. **Snapshot the Stacked-Arch HTML.** Save current
   `APEX-Stacked-Architecture-Narrated.html` to a versioned filename so
   the post-port comparison is reproducible.

2. **Extract the Chains-tab markup.** Open in DOM inspector; copy
   `<section id="chains-tab">` plus its sibling `<div id="scenario-library-modal">`. Save to `build-sources/chains-tab.html`.

3. **Extract the inline scenario-library JSON.** Find
   `<script type="application/json" id="apex-scenario-library">`; save
   to `build-sources/scenario-library.json`. Validate against
   `apex_scenarios.models.Scenario` shape (Sprint 28 Task 28.1.2).

4. **Extract the chain-tab styles.** Pull the `#chains-tab`-prefixed
   CSS rules from the Stacked-Arch `<style>` block; save to
   `build-sources/chains-tab.css`.

5. **Update `build-sellers-guide.cjs`.** Add a new chapter assembly
   step `assembleChapter28Chains()` that:
   - Loads `chains-tab.html` as the `§28` body
   - Loads `chains-tab.css` and emits as a scoped `<style>` block
   - Loads `scenario-library.json` and inlines as
     `<script type="application/json" id="apex-scenario-library">`
   - Adds `§28 — Scenario Chains` to the TOC after `§27 — Scenario Library`
   - Adds anchor namespacing per §5 above

6. **Run `apex-compliance-lint`** on the resulting HTML — Sprint 29
   Task 29.10 lane catches any Independence regressions introduced
   by the port.

7. **Run typography lane** (Task 29.10.3) — verify font-family CSS
   declarations match the design-token registry; fail if a port-introduced
   declaration uses a non-registered family.

8. **Run color-token lane** (Task 29.10.4) — verify no inline hex
   was introduced; every color reference is via `var(--apex-...)`.

9. **Run responsive smoke** (Task 29.10.5) — Playwright @ 360 / 900 /
   1440 px. The chain-card collapse rule at ≤900px must engage.

10. **Re-publish.** Bump Sellers Guide version metadata to v1.5; update
    Appendix O (this index) with the new build provenance.

---

## §7 Acceptance criteria

- `Professional-APEX-Sellers-Guide.html` renders the §28 chapter with
  all 7 Practice rails, all 35 featured chain cards, the 723-row
  modal, and the Wave Ribbon visualization on every chain.
- All anchor IDs in §28 are namespaced (`#s28-...`) so they don't
  collide with existing Sellers Guide anchors.
- `apex-compliance-lint` exits 0 on the merged file.
- Typography / color-token / responsive lanes all green.
- File size after port: ≤ 4 MB (current Sellers Guide is ~1.8 MB,
  Stacked-Arch chain-tab content is ~1.5 MB; budget is 4 MB to
  preserve email-deliverability for the executive distribution list).
- No JavaScript errors in the browser console under the four target
  viewports.

---

## §8 Rollback procedure

If the merged HTML fails any of the §7 criteria post-merge, the
front-end engineer:

1. Reverts the `build-sellers-guide.cjs` change
2. Restores the previous `Professional-APEX-Sellers-Guide.html` from
   the published `outputs/` directory
3. Files an issue in the engagement-tracker with the failing criterion
   and the diff of the failing build
4. Sprint 29 retro covers the lessons learned; the merge is rescheduled

The Stacked-Arch HTML and its narration decks remain available as
**separate artifacts** during the rollback window — clients still get
the cinematic walk-through; only the in-Sellers-Guide embed is
deferred.

---

## Cross-references

- Sprint 27 — Stacked Architecture Narrated HTML (source of the Chains tab)
- Sprint 28 §28.1.2 — Extended Scenario JSON shape (W1/W2/W3 fields)
- Sprint 28 §28.4 — CSV export (alternate distribution path)
- Sprint 28 §28.5 — Cross-practice search (Sprint 28 front-end work)
- Sprint 29 Task 29.2 — Appendix N (design-token source)
- Sprint 29 Task 29.9 — `apex-compliance-lint`
- Sprint 29 Task 29.10 — Pre-publish CI lane (the four gates this port must pass)
