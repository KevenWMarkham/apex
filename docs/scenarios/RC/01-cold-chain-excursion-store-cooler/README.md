# Cold-chain excursion — store cooler

**Practice:** RC — Retail & Consumer  
**Scenario index:** 01 of 5 featured (global chain 1 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Dairy case at Big Box Store 100 exceeds temperature threshold for 47 minutes mid-shift. Operator must decide: sell-through, mark down, destroy. Currently 65% of shift goes to gathering info, 35% to deciding.

## Solution
Real-time perishables-integrity agent fuses SKU-level elasticity with FSMA 204 lot provenance. HITL gate on destroy / markdown actions above threshold.

## Use Case
Excursion triage + markdown decisioning, Wave 2 across NA footprint. Reads SCML.Lot , SCML.Inventory , MERML.Price , MERML.Markdown . Parent orchestration composes 5 agents.

## Service
RC-E2E-03 Assortment &amp; Pricing + RC-E2E-09 Product Tracking. Commercial envelope per store tier. Wave 2 at 250-store pilot; Wave 3 enterprise.

## Persona
Primary Marisol Reyes · Store Operations Lead Approves markdown / destroy above threshold via Teams Adaptive Card; decision writes to audit row.

## KPI
Manager time +5.2 hrs/shift · time-to-decision 12 min → 90 sec · shrink cost −18% · audit-row attributed · §16.13 reference deployment.

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-cold-chain-excursion-store-cooler-build-guide.md` — step-by-step build
- `APEX-cold-chain-excursion-store-cooler-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
