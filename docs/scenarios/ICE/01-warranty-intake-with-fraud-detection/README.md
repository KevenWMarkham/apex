# Warranty intake with fraud detection

**Practice:** ICE — Industrial, Construction, Equipment  
**Scenario index:** 01 of 5 featured (global chain 31 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Heavy-equipment OEM processes 28,000 warranty claims/yr from dealer network. Legacy rule-set catches $2.1M in fraud; actual fraud estimated at $7M+ (duplicate claims, part-substitution, work-not-performed, collusive dealers).

## Solution
Warranty agent analyzes claim patterns, dealer-graph behavior, part-serial-number history, service-hour anomalies. Flags high-risk claims pre-payment; proposes supplier-recovery actions. HITL on dealer-relationship decisions.

## Use Case
Global-warranty-portfolio claim triage. Reads AftermarketML.Claim , AftermarketML.Dealer , AftermarketML.Part .

## Service
ICE-Aftermarket-03 Warranty Integrity. Wave 2 on NA dealer network; Wave 3 global.

## Persona
Primary Christopher Reyna · Warranty Operations Manager Reviews flagged claims; approves denial / recovery.

## KPI
Fraud detection +52% · recovery $6.8M Year 1 · supplier-recovery rate +22pp .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-warranty-intake-with-fraud-detection-build-guide.md` — step-by-step build
- `APEX-warranty-intake-with-fraud-detection-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
