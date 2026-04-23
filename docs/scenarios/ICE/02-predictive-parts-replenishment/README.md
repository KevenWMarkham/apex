# Predictive parts replenishment

**Practice:** ICE — Industrial, Construction, Equipment  
**Scenario index:** 02 of 5 featured (global chain 32 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Dealer network holds $240M in parts inventory across 420 locations. Stockout rate on fast-movers is 14%; excess on slow-movers is 31%. Lost sales from stockouts estimated at $6.8M/yr .

## Solution
Parts-replenishment agent forecasts demand per SKU per dealer using install-base + failure-mode + service-event data. Proposes replenishment orders + inter-dealer-transfer opportunities. HITL on inventory-level overrides.

## Use Case
Dealer-network parts planning. Reads AftermarketML.InstallBase , AftermarketML.Part , SupplyML-A.Inventory .

## Service
ICE-Aftermarket-05 Parts Intelligence. Wave 2 at top-50 dealers; Wave 3 network.

## Persona
Primary Omar Al-Rashid · Parts Distribution Manager Reviews weekly replenishment proposals; approves transfers.

## KPI
Stockouts −28% · lost-sale capture $6.8M/yr · total working-capital −$18M .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-predictive-parts-replenishment-build-guide.md` — step-by-step build
- `APEX-predictive-parts-replenishment-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
