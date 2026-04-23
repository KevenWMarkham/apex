# APEX Scenario Library

The canonical on-disk representation of the APEX scenario catalog. One folder per Practice, with featured-scenario sub-folders and a compact browse catalog for the long tail.

## At a glance

- **7 Practices** — RC, HLS, ER, AXLE, TMT, TH, ICE
- **35 featured scenarios** (5 per Practice) with full Scenario → Solution → Use Case → Service → Persona → KPI chains
- **723 compact scenarios** (100–105 per Practice) in browse catalogs

## Practice folders

- **[RC](./RC/)** — Retail & Consumer · 5 featured + 102 catalogued
- **[HLS](./HLS/)** — Health, Life Sciences · 5 featured + 105 catalogued
- **[ER](./ER/)** — Energy & Resources · 5 featured + 103 catalogued
- **[AXLE](./AXLE/)** — Automotive & Manufacturing · 5 featured + 105 catalogued
- **[TMT](./TMT/)** — Technology, Media, Telecom · 5 featured + 105 catalogued
- **[TH](./TH/)** — Travel & Hospitality · 5 featured + 103 catalogued
- **[ICE](./ICE/)** — Industrial, Construction, Equipment · 5 featured + 100 catalogued

## Layout

```
docs/scenarios/
  README.md                            <-- this file
  _catalog/
    scenario-library.json              <-- full 723-row catalog as JSON
    featured-chains.json               <-- 35 featured scenarios with full chains
    by-practice.md                     <-- count summary
  <PRACTICE>/                          <-- RC / HLS / ER / AXLE / TMT / TH / ICE
    README.md                          <-- Practice overview + featured list
    _browse-catalog.md                 <-- 100+ compact scenarios, alphabetical
    NN-<slug>/                        <-- one folder per scenario (01-05 featured; 06+ compact)
      README.md                        <-- chain content (full for featured; lightweight for compact)
      tests/                           <-- pytest fixtures (when apex-test-harness targets this Practice)
      artifacts/                       <-- diagrams, screenshots, sample payloads
      manifests/                       <-- agent / orchestration / policy manifest YAMLs
```

## Featured vs compact

Both folder shapes are structurally identical (README + `tests/` + `artifacts/` + `manifests/`). The difference is content:

- **Featured (01-05 per Practice)** — hand-authored full chains: Scenario / Solution / Use Case / Service / Persona / KPI plus a Wave Ribbon.
- **Compact (06-NNN per Practice)** — catalog entries from `APEX_SCENARIO_LIBRARY`. Lightweight README with title, service code, description, headline KPI. Promote to featured by authoring the full chain.

## Provenance

- **Compact catalog** (`_catalog/scenario-library.json`) extracted from the `APEX_SCENARIO_LIBRARY` JS constant in [`docs/reference/APEX-Stacked-Architecture-Narrated.html`](../reference/APEX-Stacked-Architecture-Narrated.html).
- **Featured chains** (`_catalog/featured-chains.json`) extracted from the 35 collapsible chain cards in the same narrated HTML.
- Roadmap entries: **BL.C.42a** (35 featured) · **BL.C.42b** (723 compact) · **BL.C.42e–f** (Wave Ribbon).

## Where the original Cold-Chain Excursion materials live now

The original hand-authored `Cold-Chain Excursion/` folder (containing `APEX-Cold-Chain-Excursion-Build-Guide.md` and the walkthrough DOCX) has been relocated into [`RC/01-cold-chain-excursion-store-cooler/`](./RC/01-cold-chain-excursion-store-cooler/) for consistency with the Practice-organized tree. No content was lost.

## Regenerate

```bash
python scripts/build_scenarios_tree.py
```

This rebuilds the `_browse-catalog.md` files (deterministic from the library) and the `_catalog/*.json` files. Per-scenario `README.md` files are only written if absent — hand-edits are preserved.
