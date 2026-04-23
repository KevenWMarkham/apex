# Returns fraud detection

**Practice:** RC — Retail & Consumer  
**Scenario index:** 04 of 5 featured (global chain 4 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Retailer loses $42M/yr to returns fraud (serial returners, wardrobing, credit-card-linked rings, BORIS-abuse of online-purchased goods). Legacy rules engine catches ~$10M.

## Solution
Graph-based fraud-detection agent traces return behaviors across customer, payment, device, shipping, and SKU graphs. HITL on high-value denial decisions.

## Use Case
Real-time returns triage at POS and e-comm refund gateway. Reads CXML.Customer , MERML.Transaction , SCML.Return , plus device/payment fingerprints.

## Service
RC-E2E-07 Returns &amp; Refund Integrity. Wave 2 across NA e-comm + store network.

## Persona
Primary Rebecca Hall · Returns Operations Manager Reviews flagged cases via dashboard; approves / denies with audit-row trace.

## KPI
Fraud detection rate +52% · recovered loss $8.6M in Year 1 · false-positive rate &lt;2% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-returns-fraud-detection-build-guide.md` — step-by-step build
- `APEX-returns-fraud-detection-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
