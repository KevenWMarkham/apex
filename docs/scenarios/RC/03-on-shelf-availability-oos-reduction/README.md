# On-shelf availability / OOS reduction

**Practice:** RC — Retail & Consumer  
**Scenario index:** 03 of 5 featured (global chain 3 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Store network shows 11.4% out-of-stock rate on key-value items. Shelf audits are manual, monthly, reactive. Estimated $6.2M/yr lost sales per store .

## Solution
OSA-monitoring agent fuses POS velocity, inventory position, planogram compliance, and (where available) shelf-cam computer vision. Generates prioritized associate task list with specific SKU/bay locations.

## Use Case
Real-time shelf-availability decisioning. Reads SCML.Inventory , MERML.Planogram , POS stream, optional CV signal.

## Service
RC-E2E-05 Store Operations. Wave 2 at 500-store pilot; Wave 3 enterprise.

## Persona
Primary Jamie O'Connor · Store Manager Receives prioritized task list at shift-open via Teams; each completion logs to audit row.

## KPI
Out-of-stock rate −34% on key-value items · sales per square foot +12% · associate productivity +18% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-on-shelf-availability-oos-reduction-build-guide.md` — step-by-step build
- `APEX-on-shelf-availability-oos-reduction-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
