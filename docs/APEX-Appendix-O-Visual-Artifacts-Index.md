# Appendix O — Visual Artifacts Index

**Sprint 29 Task 29.3 (BL.P.188).** Comprehensive index of every published
APEX visual artifact: filename, format, audience, purpose, Design-Reference
section cross-links, and Scenario Library / Wave Ribbon / Narration Deck
usage matrix.

This appendix is the **release-time inventory** that lets a sales lead
or engagement counsel verify which artifacts are current, which are
stale, and which compose into a given client deliverable.

---

## §1 Artifact catalog

| Filename | Format | Audience | Purpose | Design-Reference §§ | Status |
|----------|--------|----------|---------|---------------------|--------|
| `Professional-APEX-M-Sellers-Guide.html` | HTML (single-file) | Sales lead, engagement counsel, practice steward | Comprehensive sales narrative + governance reference (v1.4) | §1, §2, §6.10, §6.11–§6.13, §10–§16 | Published |
| `APEX-Stacked-Architecture-Narrated.html` | HTML (single-file) | Executive briefing, client-facing demo | 11-tab cinematic narrated walk-through of the layered architecture | §1, §2, §6 | Published (Sprint 27) |
| `APEX-Runtime-Addendum-Narrated.html` | HTML (single-file) | Engagement-team onboarding, technical pre-clearance | 5-scene narrated runtime walk-through (Orchestration · HITL · LEDGER · Audit Row · KPI Attribution) | §6.10, §6.11–§6.13 | **Pending Sprint 29 §29.6** (front-end track) |
| `APEX-Seven-Practices-SteerCo-Deck.pptx` | PPTX | SteerCo / executive sponsor | One slide per Practice with full 6-row chain + Wave ribbon sidebar | §1, §6 | **Pending Sprint 29 §29.5** (front-end track via pptxgenjs) |
| `APEX-Executive-One-Pager.pdf` | PDF (landscape letter) | C-suite, prospect lead | 35 featured scenarios scannable table | §1, §27 | **Pending Sprint 29 §29.4** (front-end track) |
| `APEX-Executive-One-Pager.docx` | DOCX | Same; editable form | Same as PDF; editable for engagement-specific overlays | §1, §27 | **Pending Sprint 29 §29.4** |
| `APEX-Sellers-Guide-v1.2-tracked-changes.docx` | DOCX | Practice-Lead reviewer | v1.2 → v1.4 tracked-changes for Practice-Lead sign-off | §27, §29 | **Pending Sprint 29 §29.7** (Word track) |
| `APEX-Appendix-A-Schema-Reference.md` | Markdown | Engineering, technical pre-clearance | 49 canonical schema families with primary entities + standards alignment | §22 (Schema bindings) | Published (Sprint 19) |
| `APEX-Appendix-C-KPI-Registry.md` | Markdown | Practice steward, SoW author | 134 KPI master entries with Wave-2/3 targets + measurement patterns | §17 (Service catalog), §28 | Published (Sprint 19) |
| `APEX-Appendix-D-Archetype-Library.md` | Markdown | Solutioning lead, agent-author | 47 orchestration archetypes across 16 families | §16 (Agent catalog), §6 | Published (Sprint 19) |
| `APEX-Appendix-E-Persona-Catalog.md` | Markdown | Practice steward, solutioning | 147 personas with seniority + function + decisions owned | §17, §16, §18 | Published (Sprint 19) |
| `APEX-Appendix-F-MCP-Tool-Catalog.md` | Markdown | Engineering, MCP-tool author | 168 MCP tools with classification + canonical schema linkage | §16 | Published (Sprint 19) |
| `APEX-Appendix-G-Microsoft-Products.md` | Markdown | Sales, technical pre-clearance | 27 Microsoft products with SKU + APEX role mapping | §1, §6 | Published (Sprint 19) |
| `APEX-Appendix-H-Partner-Ecosystem.md` | Markdown | Solutioning, integration architect | 20 SOR vendor / model provider / data provider entries | §15 (Adapters) | Published (Sprint 19) |
| `APEX-Appendix-J-Exercise-Solutions.md` | Markdown | Practice-Lead training | 10 canonical solutions to representative Sellers Guide exercises | §10–§16 | Published (Sprint 19) |
| `APEX-Appendix-K-Independence-Competitive.md` | Markdown | Sales, engagement counsel | 10 competitive-posture entries with Independence-clean win themes | §1, §29.9 | Published (Sprint 19) |
| `APEX-Appendix-L-Scenario-Library.md` | Markdown index + 7 per-Practice files | Sales, solutioning | Master catalog of 723-row Scenario Library with 35 featured chains | §27, §28 | Published (Sprint 28 §28.7.1) |
| `APEX-Appendix-M-Narration-Catalog.md` | Markdown | Narration writer, engagement-team onboarding | All 11 tab narration decks extracted with scene anchors + pronunciation notes | §27, §29.1 | **Pending Sprint 29 §29.1** (HTML extraction track) |
| `APEX-Appendix-N-Design-System.md` | Markdown + companion CSS | Engineering, brand reviewer | Typography, color tokens, breakpoints, accessibility, Independence linguistic rules | §27, §29.2 | Published (Sprint 29 Task 29.2) |
| `apex-design-tokens.css` | CSS | Engineering | Companion tokens stylesheet, sole source of inline hex | §29.2 | Published (Sprint 29 Task 29.2) |
| `APEX-Appendix-O-Visual-Artifacts-Index.md` | Markdown (this file) | Release manager, engagement counsel | Inventory of every artifact + status + cross-references | §29.3 | Published (Sprint 29 Task 29.3) |
| `APEX-Chains-Port-Spec.md` | Markdown | Front-end engineer | Build-instructions for porting Chains tab into the main Sellers Guide HTML | §27, §29.8 | Published (Sprint 29 Task 29.8) |

---

## §2 Cross-reference matrix

Per Sprint 29 §29.3.2, this matrix shows which artifacts use the
Scenario Library, Wave Ribbon visualization, and narration decks.

Symbols: ✅ direct use · ☑ referenced · — not applicable.

| Artifact | Scenario Library | Wave Ribbon | Narration Deck | Independence Lint | Design Tokens |
|----------|------------------|-------------|----------------|-------------------|---------------|
| Sellers Guide HTML | ☑ | ☑ | — | ✅ | ✅ |
| Stacked Architecture Narrated HTML | ✅ (35 featured + 723 modal) | ✅ | ✅ (11 tab decks) | ✅ | ✅ |
| Runtime Addendum Narrated HTML | ☑ | — | ✅ (5 scenes) | ✅ | ✅ |
| SteerCo Deck PPTX | ✅ (7 chains) | ✅ | — | ✅ | ✅ |
| Executive One-Pager (PDF + DOCX) | ✅ (35 featured table) | ☑ | — | ✅ | ✅ |
| Sellers Guide v1.2 Tracked-Changes DOCX | ☑ | ☑ | — | ✅ | — |
| Appendix A — Schema Reference | — | — | — | ✅ | — |
| Appendix C — KPI Registry | ☑ | — | — | ✅ | — |
| Appendix D — Archetype Library | — | — | — | ✅ | — |
| Appendix E — Persona Catalog | — | — | — | ✅ | — |
| Appendix F — MCP Tool Catalog | — | — | — | ✅ | — |
| Appendix G — Microsoft Products | — | — | — | ✅ | — |
| Appendix H — Partner Ecosystem | — | — | — | ✅ | — |
| Appendix J — Exercise Solutions | ☑ | ☑ | — | ✅ | — |
| Appendix K — Independence/Competitive | — | — | — | ✅ | — |
| Appendix L — Scenario Library Master | ✅ (entire library) | ☑ | — | ✅ | — |
| Appendix M — Narration Catalog | — | — | ✅ (source-of-truth for all 11 decks) | ✅ | — |
| Appendix N — Design System | — | — | — | ✅ (defines the rules) | ✅ (defines the tokens) |
| Appendix O — this file | ✅ | ✅ | ✅ | ✅ | ✅ |
| Chains Port Spec | ✅ (target component) | ✅ | — | ✅ | ✅ |

---

## §3 Status legend

- **Published** — Artifact ships in its final form; CI gates green;
  cross-references active.
- **Pending Sprint 29 §X** — Artifact is committed in the Sprint 29
  scope and tracked under the named subtask. Front-end / Word / PPTX
  tracks ship outside the Python parallel-track work; Python parallel
  track has shipped its prerequisites.
- **Stale** *(none currently)* — Artifact requires a re-publish to
  reflect downstream catalog changes (Sprint 27 introduces this status
  but no entries currently apply).

---

## §4 Re-publication triggers

An artifact moves from `Published` → `Stale` when any of the following
occur and the artifact's content depends on the changed material:

| Trigger | Affected artifacts |
|---------|--------------------|
| New service code added to `apex-services` catalog (Sprint 17) | Sellers Guide HTML, Stacked Architecture Narrated, Appendix L, SteerCo Deck, Executive One-Pager |
| New agent added to `apex-agents` catalog (Sprint 16) | Stacked Architecture Narrated, Appendix F |
| New Practice on-boarded | All Practice-coded artifacts |
| Independence-language rules updated in `apex-compliance-lint` | All artifacts (re-lint required) |
| Design tokens updated in `apex-design-tokens.css` | All HTML/PPTX artifacts |
| Sellers Guide version bumped | Tracked-Changes DOCX, Stacked Architecture Narrated cross-references |

The re-publication runbook lives in `docs/release-runbook.md` (front-end
track ships separately).

---

## §5 Build provenance

Every artifact carries embedded build-provenance metadata so an auditor
can verify the artifact matches the catalog state it claims to. For
HTML: `<meta name="apex-build-provenance" content="...">`; for DOCX:
custom doc properties; for PPTX: slide-master metadata; for Markdown:
YAML frontmatter when applicable.

The provenance string is structured as:

```
sprint:<N>;catalog-revisions:<scenario-lib:0.X.Y,services:0.X.Y,agents:0.X.Y>;tokens:<sha>;built:<iso8601>
```

The `apex-compliance-lint` package's pre-publish CI lane (Sprint 29
Task 29.10) verifies the provenance string is present and not stale
relative to the catalog SHA at PR time.

---

## Cross-references

- Sprint 19 — Appendices A, C, D, E, F, G, H, J, K (registry-derived)
- Sprint 28 — Appendix L (Scenario Library master catalog)
- Sprint 29 Task 29.1 — Appendix M (Narration catalog, pending)
- Sprint 29 Task 29.2 — Appendix N (Design System)
- Sprint 29 Task 29.3 — Appendix O (this file)
- Sprint 29 Task 29.8 — Chains Port Spec
- Sprint 29 Task 29.9 — `apex-compliance-lint` package
- Sprint 29 Task 29.10 — Pre-publish CI workflow
