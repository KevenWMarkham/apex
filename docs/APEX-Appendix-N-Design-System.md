# Appendix N — APEX Design-System Reference

**Sprint 29 Task 29.2 (BL.P.187).** Single source of truth for APEX
visual identity: typography, color tokens, per-Practice banner colors,
spacing/radius/shadow, responsive breakpoints, accessibility baseline,
and Independence linguistic rules with the approved-substitute table.

Cross-references: `apex-compliance-lint` rule packs enforce these
rules in CI; companion CSS tokens file at `docs/apex-design-tokens.css`.

---

## §1 Typography

APEX uses three type families from the Open Font License catalog. Web
deployments embed via the design-tokens stylesheet; PowerPoint uses the
matching brand-fonts pack.

| Family | Role | Weights used | Source |
|--------|------|--------------|--------|
| **Fraunces** | Display + headings + cinematic narration captions | 300, 400, 600, 800 | Google Fonts (OFL) |
| **IBM Plex Sans** | Body, navigation, labels, dense table cells | 300, 400, 500, 600, 700 | Google Fonts (OFL) |
| **JetBrains Mono** | Code, command prompts, structured data tables | 400, 500, 700 | JetBrains (OFL) |

### Weight + size guidance

| Element | Family | Size | Weight | Notes |
|---------|--------|------|--------|-------|
| Cinematic eyebrow | Fraunces italic | 14–16px | 400 | Used for `deep-eyebrow` per-tab labels |
| Cinematic head | Fraunces | 56–80px | 800 | Tab-level top-of-deck headlines |
| Section heading | Fraunces | 32–48px | 600 | In-tab section breaks |
| Sub-heading | IBM Plex Sans | 20–24px | 700 | Card titles + ribbon labels |
| Body | IBM Plex Sans | 15–17px | 400 | Default reading text |
| UI labels | IBM Plex Sans | 13–14px | 500 | Buttons, chips, ribbon segment labels |
| Code | JetBrains Mono | 13–14px | 400 | Inline code + command examples |
| Data table | JetBrains Mono | 13px | 500 | Numeric columns; ensures alignment |

### Italic guidance

Fraunces italic is for **on-screen narration captions** and editorial
asides; IBM Plex Sans italic is for **emphasis** within prose; JetBrains
Mono italic is **never used** (eye fatigue at small sizes).

---

## §2 Color tokens

APEX ships **dark theme primary** (Sprint 27 design). Light theme is
opt-in via `body.light`.

### Dark theme tokens

| Token | Hex | Use |
|-------|-----|-----|
| `--apex-bg` | `#0A0E1A` | Page background |
| `--apex-bg-elevated` | `#121828` | Card / modal background |
| `--apex-bg-rail` | `#1A2238` | Side rails / banner rails |
| `--apex-text` | `#E8ECF4` | Primary body text |
| `--apex-text-muted` | `#9AA3B8` | Secondary / metadata |
| `--apex-text-faint` | `#6B7287` | Tertiary / disabled |
| `--apex-accent` | `#7CC4FF` | Default accent / hyperlinks |
| `--apex-accent-warm` | `#FFAA66` | Warmth / hover / cta |
| `--apex-success` | `#5DD39E` | KPI up / OK semantics |
| `--apex-warning` | `#F2C063` | KPI watch / warn |
| `--apex-error` | `#F47B7B` | KPI breach / fail / blocking validation |
| `--apex-money` | `#A37CFF` | KPI money-direction (revenue, cost, margin) |
| `--apex-divider` | `#222A40` | Hairline separators |
| `--apex-shadow-color` | `rgba(0,0,0,0.45)` | Elevation shadows |

### Light theme tokens (auto-swapped via `body.light`)

| Token | Hex |
|-------|-----|
| `--apex-bg` | `#FAF8F4` |
| `--apex-bg-elevated` | `#FFFFFF` |
| `--apex-bg-rail` | `#F1ECE3` |
| `--apex-text` | `#1A1F2E` |
| `--apex-text-muted` | `#5A6378` |
| `--apex-text-faint` | `#8A93A7` |
| `--apex-accent` | `#1565C0` |
| `--apex-accent-warm` | `#C7551A` |
| `--apex-success` | `#1F7A3D` |
| `--apex-warning` | `#A87100` |
| `--apex-error` | `#A8302C` |
| `--apex-money` | `#5A2BA8` |

**Forbidden in artifact CSS:** inline hex literals (e.g.,
`color: #FF5500`). Sprint 29 Task 29.10.4 lane fails the build on any
inline hex outside `docs/apex-design-tokens.css`. Use CSS variables.

---

## §3 Per-Practice banner colors

Practice-coded banner rails. Cinematic-band rules: 3px-thick rail,
24px paragraph indent for the cited Practice's content blocks.

| Practice | Token | Hex (dark) | Hex (light) |
|----------|-------|-----------|-------------|
| RC — Retail & Consumer | `--apex-rail-rc` | `#7CC4FF` | `#1565C0` |
| HLS — Healthcare & Life Sciences | `--apex-rail-hls` | `#5DD39E` | `#1F7A3D` |
| ER — Energy & Resources | `--apex-rail-er` | `#FFAA66` | `#C7551A` |
| AXLE — Industrial / Manufacturing | `--apex-rail-axle` | `#F2C063` | `#A87100` |
| TMT — Telecom / Media / Tech | `--apex-rail-tmt` | `#A37CFF` | `#5A2BA8` |
| TH — Travel & Hospitality | `--apex-rail-th` | `#F47B7B` | `#A8302C` |
| ICE — Industrial Connected Electronics | `--apex-rail-ice` | `#9CC8E0` | `#2C5973` |

---

## §4 Spacing, radius, shadow tokens

### Spacing scale (8px base)

| Token | px | Use |
|-------|----|-----|
| `--apex-space-0` | 0 | reset |
| `--apex-space-1` | 4 | tight inline gap |
| `--apex-space-2` | 8 | default inline gap |
| `--apex-space-3` | 12 | label/value gap |
| `--apex-space-4` | 16 | card padding |
| `--apex-space-5` | 24 | section padding |
| `--apex-space-6` | 32 | block separation |
| `--apex-space-8` | 48 | major section break |
| `--apex-space-10` | 64 | hero padding |

### Radius

| Token | px | Use |
|-------|----|-----|
| `--apex-radius-sm` | 4 | Chips / pills |
| `--apex-radius-md` | 8 | Cards / inputs |
| `--apex-radius-lg` | 16 | Modals / hero panels |
| `--apex-radius-pill` | 9999 | Ribbon segments |

### Shadow

| Token | Value | Use |
|-------|-------|-----|
| `--apex-shadow-sm` | `0 1px 2px var(--apex-shadow-color)` | Subtle lift |
| `--apex-shadow-md` | `0 4px 12px var(--apex-shadow-color)` | Cards |
| `--apex-shadow-lg` | `0 12px 32px var(--apex-shadow-color)` | Modals / overlays |

---

## §5 Responsive breakpoints

| Token | px | Behavior |
|-------|----|----------|
| `--bp-sm` | 360 | Phone portrait — single-column, ribbons collapse to 3-dot indicator |
| `--bp-md` | 640 | Phone landscape / small tablet — two-column where appropriate |
| `--bp-lg` | 900 | Tablet / small laptop — full ribbons render; modal rows wrap to two lines |
| `--bp-xl` | 1280 | Standard laptop — full layout |
| `--bp-2xl` | 1440 | Large display — comfortable typography spacing |

Sprint 27 collapse rule: at `<= 900px`, ribbons collapse to compact
3-dot indicators per modal row; expand-in-place pattern (no new modal).

---

## §6 Accessibility baseline

- **WCAG 2.2 AA** for color contrast: every token pair (text on bg)
  meets 4.5:1 for body, 3:1 for large display.
- **Focus indicator:** 2px outline in `--apex-accent` with 2px offset on
  every interactive element.
- **`prefers-reduced-motion`:** all narration auto-play / scene-skip
  animations respect this; voiceover does not autostart.
- **`prefers-color-scheme`:** matches default theme, but explicit
  `body.light` toggle overrides.
- **ARIA:** every `<details>`/`<summary>` collapsible has explicit
  `aria-expanded`; every chip filter has `role="button"` +
  `aria-pressed`.
- **Keyboard:** `/` focuses filter; `↑/↓` row navigation; `Enter`
  expands; `Esc` closes modal (Sprint 28 Task 28.6).

---

## §7 Independence linguistic rules + approved substitutes

The `apex-compliance-lint` package enforces these at CI. The full
machine-readable rule set lives in
`packages/apex-compliance-lint/src/apex_compliance_lint/rules/deloitte_microsoft_independence.py`.

### Forbidden language and approved substitutes

| Forbidden | Approved substitute(s) | Rule id |
|-----------|------------------------|---------|
| "partner" / "partner with" | "the platform" / "the underlying technology" / "the vendor" | `deloitte_microsoft_independence.partner` |
| "alliance" / "alliance partner" | "platform" / "technology stack" | `deloitte_microsoft_independence.alliance` |
| "partnership" | "integration" / "deployment" / "community pattern" / "adoption" | `deloitte_microsoft_independence.partnership` |
| "endorses" / "endorsement" | "aligned with" / "consistent with" / "built on" | `deloitte_microsoft_independence.endorse` |
| "recommended by Microsoft / SAP / etc." | "aligned with the vendor's reference architecture" | `deloitte_microsoft_independence.recommended_by` |
| "Deloitte and Microsoft jointly" / "co-developed" | "APEX is built on Microsoft Fabric and Foundry" | `deloitte_microsoft_independence.deloitte_microsoft_jointly` |
| "Gold Partner" / "Platinum Partner" / "Premier Partner" | "certified on the platform" / "deployed on the platform" | `deloitte_microsoft_independence.gold_partner` |

### Domain-of-art exceptions (auto-suppressed)

The linter automatically allows these legitimate uses without flagging:

- **"trading partner"** (EDI / supply-chain term of art)
- **"channel partner"** (dealer / distribution context)
- **"payment partner"** / **"business partner"** / **"community partner"** / **"supply partner"** / **"EDI partner"** / **"fusion partner"**
- **"Microsoft Partner Of The Year"** / **"Microsoft Partner Network"** (formal award + program names)
- **Quoted metalinguistic uses** — `"partner"` / `"alliance"` in quotes when explaining the rule itself
- **Negated assertions** — "not partnered with X", "no commercial alliance", "does not claim partnership"

### Brand & positioning rules

The `apex_brand` rule pack enforces additional positioning:

| Forbidden | Severity | Approved substitute |
|-----------|----------|---------------------|
| "black box" | ERROR | "auditable" / "transparent" / "fully traceable" |
| "fully autonomous" | ERROR | "HOTL (Human-on-the-Loop)" / "agent-orchestrated with HITL gates" |
| "guarantees outcomes" / "guaranteed ROI" | ERROR | "targets" / "Wave-2 commitments per Sellers Guide §2.2" |
| "AI-powered" / "AI-driven" | WARNING | "agentic" / "agent-orchestrated" |
| "silver bullet" / "panacea" | WARNING | "integrated solution" / "engagement framework" |

---

## §8 Sample CSS tokens

A companion file `docs/apex-design-tokens.css` ships the tokens above
as CSS custom properties. Copy/paste into any artifact's `<style>` block
or `@import` if hosting on the same origin.

```css
@import url("https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..800;1,9..144,300..800&family=IBM+Plex+Sans:wght@300..700&family=JetBrains+Mono:wght@400..700&display=swap");

:root {
  --apex-bg: #0A0E1A;
  --apex-bg-elevated: #121828;
  --apex-text: #E8ECF4;
  --apex-text-muted: #9AA3B8;
  --apex-accent: #7CC4FF;
  --apex-success: #5DD39E;
  --apex-warning: #F2C063;
  --apex-error: #F47B7B;
  --apex-money: #A37CFF;
  /* ... full tokens table above ... */
}

body.light {
  --apex-bg: #FAF8F4;
  --apex-bg-elevated: #FFFFFF;
  --apex-text: #1A1F2E;
  /* ... full light table above ... */
}
```

---

## Cross-references

- `apex-workspace/CHARTER.md` §6 — Independence language operationalized in agent prose
- `apex-workspace/APEX-CORE.md` §7 hard limit #8 — Independence is constitutional
- `packages/apex-compliance-lint/` — runtime enforcement
- `.github/workflows/artifact-compliance.yml` — pre-publish CI lane (Sprint 29 Task 29.10)
- Appendix M (Sprint 29 Task 29.1) — narration script catalog (uses §1 typography)
- Appendix O (Sprint 29 Task 29.3) — visual artifacts index (every artifact's design-token usage)
