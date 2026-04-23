# SaaS expansion & consumption — tech

**Practice:** TMT — Technology, Media, Telecom  
**Scenario index:** 05 of 5 featured (global chain 25 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
B2B SaaS operator has $340M ARR across 4,200 enterprise accounts. Expansion ARR is 11% (target 18%); customer-success motions are generic, triggered on renewal window rather than consumption signals.

## Solution
Customer-success agent monitors product-consumption telemetry, support-ticket patterns, renewal signals. Proposes per-account expansion plays + early-churn interventions. HITL is always the CSM.

## Use Case
Strategic-account portfolio CS. Reads TECML.Account , TECML.Consumption , TECML.Support .

## Service
TMT-TEC-04 Customer Success Intelligence. Wave 2 at top-200 accounts; Wave 3 full portfolio.

## Persona
Primary Tara Bergstrom · Customer Success Director CSMs review agent-surfaced plays; execute outreach.

## KPI
Expansion ARR +31% · churn −24% · renewal NRR 98% → 119% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-saas-expansion-consumption-tech-build-guide.md` — step-by-step build
- `APEX-saas-expansion-consumption-tech-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
