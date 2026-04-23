# Supplier risk & dual-sourcing decisioning

**Practice:** AXLE — Automotive & Manufacturing  
**Scenario index:** 05 of 5 featured (global chain 20 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Category managers maintain 4,200 active suppliers . Risk scoring is annual, spreadsheet-based, backward-looking. Top-10 supplier-driven delays cost $22M in FY24. Dual-source decisions are ad hoc.

## Solution
Supplier-risk agent continuously fuses supplier financial-health, delivery performance, news/ESG/compliance signals, geopolitical risk. Maintains live tiered risk score; proposes dual-source decisions with sourcing-cost impact.

## Use Case
Strategic-supplier portfolio risk monitoring. Reads SupplyML-A.Supplier , external risk feeds (D&amp;B, OFAC, news), historical OTD.

## Service
AXLE-Supply-07 Supplier Intelligence. Wave 2 at top-100 suppliers; Wave 3 full supplier base.

## Persona
Primary Akira Tanaka · Procurement Director Reviews risk dashboard; approves dual-source decisions.

## KPI
Supplier-driven delays −38% · risk-adjusted sourcing savings $8M/yr · audit-row-attributed sourcing decisions.

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-supplier-risk-dual-sourcing-decisioning-build-guide.md` — step-by-step build
- `APEX-supplier-risk-dual-sourcing-decisioning-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
