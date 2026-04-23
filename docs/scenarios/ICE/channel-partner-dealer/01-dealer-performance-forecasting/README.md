# Dealer performance & forecasting

**Practice:** ICE — Industrial, Construction, Equipment  
**Scenario index:** 05 of 5 featured (global chain 35 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
OEM has 1,800 dealers globally submitting monthly sales forecasts. Forecast accuracy is ±24% at 6 months; production planning is over-built to compensate, driving $22M/yr in inventory carry .

## Solution
Dealer-forecast agent fuses dealer-submitted forecasts + market indicators + install-base + macro factors (interest rates, construction spend, commodity prices). Produces risk-adjusted consensus forecast; surfaces anomalies. HITL on dealer-specific overrides.

## Use Case
S&amp;OP demand-consensus across dealer network. Reads ConnectedICEML.Dealer , ConnectedICEML.InstallBase , market-data feed.

## Service
ICE-Connected-06 Dealer Intelligence. Wave 2 at NA dealer network; Wave 3 global.

## Persona
Primary Vincent D'Ambrosio · Dealer Network VP Reviews consensus forecast; approves override policies.

## KPI
Forecast accuracy +18pp · inventory carry −$22M/yr · stockout-driven lost sales −41% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-dealer-performance-forecasting-build-guide.md` — step-by-step build
- `APEX-dealer-performance-forecasting-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
