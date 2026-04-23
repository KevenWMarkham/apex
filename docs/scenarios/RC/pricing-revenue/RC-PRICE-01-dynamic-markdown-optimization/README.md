# Dynamic markdown optimization

**Practice:** RC — Retail & Consumer  
**Scenario index:** 02 of 5 featured (global chain 2 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Seasonal inventory aging faster than markdown cadence supports. Category managers set blanket markdowns that overshoot (margin erosion) or undershoot (stockholding cost). ~$12M/yr value leakage at mid-size chain.

## Solution
Markdown-optimization agent reads elasticity, competitor pricing, store-level velocity, weather, and event calendars. Proposes per-SKU-per-store markdown with simulated P&amp;L impact. HITL gate on markdowns above 30%.

## Use Case
Assortment-wide markdown cadence with weekly refresh. Reads MERML.Markdown , MERML.Elasticity , SCML.Inventory , MERML.Competitor .

## Service
RC-E2E-03 Assortment &amp; Pricing. Commercial envelope tied to category-level P&amp;L attribution.

## Persona
Primary Daniel Chen · Merchandising Director Reviews weekly markdown proposal in Power BI; approves via Copilot chat.

## KPI
Gross margin +3.2pp category-level · aged-stock days on hand −28% · markdown-to-clear ratio +41% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-dynamic-markdown-optimization-build-guide.md` — step-by-step build
- `APEX-dynamic-markdown-optimization-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
