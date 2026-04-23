# Dynamic pricing & revenue management — hotel

**Practice:** TH — Travel & Hospitality  
**Scenario index:** 02 of 5 featured (global chain 27 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Hotel group (340 properties, 78K rooms ) uses legacy RM system with rule-based pricing. Pace reporting is daily; competitor-rate monitoring is manual. RevPAR lags peer set by 3–4%.

## Solution
RM agent fuses internal pace, competitor rates, event demand, weather, and channel mix. Proposes rate moves with simulated P&amp;L; applies within guardrails, escalates outside. HITL on rate moves &gt;8%.

## Use Case
Daily rate-optimization across portfolio. Reads HotelML.Property , HotelML.Booking , competitor-rate feed.

## Service
TH-HOT-03 Revenue Management. Wave 2 at top-50 properties; Wave 3 full portfolio.

## Persona
Primary Inez Castillo · Revenue Management Director Reviews daily moves; approves out-of-guardrail decisions.

## KPI
RevPAR +4.1% · year-over-year revenue +$28M · peer-set-index gap closed from −3.2% to +0.6% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-dynamic-pricing-revenue-management-hotel-build-guide.md` — step-by-step build
- `APEX-dynamic-pricing-revenue-management-hotel-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
