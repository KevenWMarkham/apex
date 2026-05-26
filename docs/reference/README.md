# `docs/reference/` — Map of the seller and engineering kit

Reorganized 2026-05-23 into root + one-level-deep folders for easier navigation. Existing industry folders (Automotive, Retail and Consumer, Transportation) are unchanged.

| Folder | What lives here | When to reach for it |
|---|---|---|
| **`Sellers-Guide/`** | Field-use artifacts for client conversations: sellers guide, quick-reference card, BVA workshop deck, ROI calculator, CFMP Pack Lite wedge | Daily seller use; the kit you carry into client meetings |
| **`SOW-Templates/`** | Three redlinable SOW templates (Pack Lite / Standard / Enterprise) | Within 48 hours of a successful BVA workshop |
| **`Walkthrough-Decks/`** | Current v5 walkthrough deck + image-asset notes + assets folder | 45-minute exec briefing |
| **`Architecture-and-Reference/`** | APEX canonical engineering reference docs (comprehensive solutions, services-to-solutions architecture, stacked-architecture-narrated) | When the architect or DPO needs depth |
| **`Scenario-Catalog/`** | APEX scenario chains workbook + hardware extensions | Engineering reference; cited in every SOW Appendix C |
| **`_Archive/`** | Old deck versions (v1-v4), scenario-catalog backups, old deck-asset folder | Reference only; not for active use |
| **`_build-scripts/`** | Python scripts that build / extend scenario catalogs (`_add_*_scenarios.py`) | Maintenance; rerun when extending the scenario chains |
| **`Automotive/`** | Industry-specific Automotive (AXLE) artifacts | Existing — left unchanged |
| **`Retail and Consumer/`** | Industry-specific RC artifacts | Existing — left unchanged |
| **`Transportation/`** | Industry-specific Transportation & Hospitality (TH) artifacts | Existing — left unchanged |

## Quick lookup — "where is X?"

| If you're looking for... | Open this |
|---|---|
| The 60-second pitch + 15-min demo script + objection handlers | `Sellers-Guide/APEX-CFMP-CHC-Sellers-Guide-for-DMTSP.md` |
| A printable 1-page card for your notebook | `Sellers-Guide/Sellers-Quick-Reference-Card.pptx` |
| The 4-hour BVA workshop content | `Sellers-Guide/BVA-Workshop-Facilitator-Deck.pptx` |
| A populated ROI model for the client CFO | `Sellers-Guide/BVA-ROI-Calculator.xlsx` |
| A Pack Lite SOW to redline | `SOW-Templates/SOW-APEX-CFMP-Pack-Lite.docx` |
| The exec-briefing visual deck (15 slides, 45 min) | `Walkthrough-Decks/APEX-Walkthrough-Deck-for-DMTSP-Sellers-v5.pptx` |
| Canonical APEX engineering reference | `Architecture-and-Reference/APEX-comprehensive-solutions-reference.md` |
| All scenarios across all packs (200+) | `Scenario-Catalog/APEX-Scenario-Chains.xlsx` |
| An older v3 deck you used last quarter | `_Archive/APEX-Walkthrough-Deck-for-DMTSP-Sellers-v3.pptx` |

## Companion engineering reference (in `docs/packs/`)

These remain in `docs/packs/` because they are design / engineering documents, not seller artifacts:

- `CFMP-v0.2.md` — Customer Focused Merchandise Pack design
- `Connected-Home-Commerce-v0.1.md` (v0.2) — Connected Home Commerce engagement design (B2B2C + B2C + Alexa-replacement thesis)
- `PARS-Private-Auto-Replenishment-v0.1.md` — Private Auto-Replenishment Service portfolio (sharpened consumption-auto-buy framing)
- `CFMP-Scenario-Chains-v0.1.xlsx` — CFMP scenario detail

## Build scripts (in `docs/packs/`)

The scripts that *build* the artifacts in this directory live in `docs/packs/`:

- `_build_quickref_card.py` → `Sellers-Guide/Sellers-Quick-Reference-Card.pptx`
- `_build_bva_workshop_deck.py` → `Sellers-Guide/BVA-Workshop-Facilitator-Deck.pptx`
- `_build_bva_roi_calculator.py` → `Sellers-Guide/BVA-ROI-Calculator.xlsx`
- `_build_sow_skeletons.py` → `SOW-Templates/SOW-APEX-CFMP-Pack-Lite.docx` (+ Standard + Enterprise)
- `_build_dmtsp_deck_v5.py` → `Walkthrough-Decks/APEX-Walkthrough-Deck-for-DMTSP-Sellers-v5.pptx`

Re-run any build script to regenerate the corresponding artifact. Update the output path in each script if you reorganize this directory further.

## Path-change note (2026-05-23 reorg)

Several documents (the v5 deck, the SOW skeletons, the BVA workshop deck, the sellers guide, the HTML book volume) reference paths in this directory. After this reorg, the referenced paths are:

| Old path | New path |
|---|---|
| `docs/reference/APEX-CFMP-CHC-Sellers-Guide-for-DMTSP.md` | `docs/reference/Sellers-Guide/APEX-CFMP-CHC-Sellers-Guide-for-DMTSP.md` |
| `docs/reference/CFMP-Pack-Lite-Wedge-for-DMTSP-Sellers.md` | `docs/reference/Sellers-Guide/CFMP-Pack-Lite-Wedge-for-DMTSP-Sellers.md` |
| `docs/reference/Sellers-Quick-Reference-Card.pptx` | `docs/reference/Sellers-Guide/Sellers-Quick-Reference-Card.pptx` |
| `docs/reference/BVA-Workshop-Facilitator-Deck.pptx` | `docs/reference/Sellers-Guide/BVA-Workshop-Facilitator-Deck.pptx` |
| `docs/reference/BVA-ROI-Calculator.xlsx` | `docs/reference/Sellers-Guide/BVA-ROI-Calculator.xlsx` |
| `docs/reference/SOW-APEX-CFMP-Pack-Lite.docx` | `docs/reference/SOW-Templates/SOW-APEX-CFMP-Pack-Lite.docx` |
| `docs/reference/SOW-APEX-CFMP-Pack-Standard.docx` | `docs/reference/SOW-Templates/SOW-APEX-CFMP-Pack-Standard.docx` |
| `docs/reference/SOW-APEX-CFMP-Pack-Enterprise.docx` | `docs/reference/SOW-Templates/SOW-APEX-CFMP-Pack-Enterprise.docx` |
| `docs/reference/APEX-Walkthrough-Deck-for-DMTSP-Sellers-v5.pptx` | `docs/reference/Walkthrough-Decks/APEX-Walkthrough-Deck-for-DMTSP-Sellers-v5.pptx` |
| `docs/reference/APEX-Scenario-Chains.xlsx` | `docs/reference/Scenario-Catalog/APEX-Scenario-Chains.xlsx` |
| `docs/reference/APEX-comprehensive-solutions-reference.md` (or `.docx`) | `docs/reference/Architecture-and-Reference/APEX-comprehensive-solutions-reference.md` |

The companion section in `docs/book/Professional-APEX-M-Sellers-Guide.html` and the §14 Related Artifacts section in `Sellers-Guide/APEX-CFMP-CHC-Sellers-Guide-for-DMTSP.md` have been updated to reflect the new paths.

---

*Maintained by Deloitte's Microsoft Technology & Services Practice · Last reorganized 2026-05-23*
