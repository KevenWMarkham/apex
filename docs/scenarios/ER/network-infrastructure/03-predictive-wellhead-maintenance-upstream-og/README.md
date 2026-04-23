# Predictive wellhead maintenance — upstream O&G

**Practice:** ER — Energy & Resources  
**Scenario index:** 02 of 5 featured (global chain 12 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Rod-pump wells across a field have 14% unplanned downtime . Failures are typically 72 hours from early indicator to catastrophic stoppage, but early indicators are buried in SCADA noise. Lost production $4.2M/yr per 200-well district.

## Solution
Predictive-maintenance agent ingests SCADA telemetry, dyno cards, motor-current signatures, tubing pressures. Surfaces predicted-failure windows with confidence intervals. HITL on workover dispatch.

## Use Case
Field-wide pump-health monitoring. Reads UOGML.Well , UOGML.Equipment , OPC-UA SCADA feed via Real-Time Hub.

## Service
ER-OG-03 Upstream Reliability. Wave 2 at one district; Wave 3 basin-wide.

## Persona
Primary Sam Reeves · Field Operations Lead Reviews predicted-failure dashboard daily; dispatches workover crews.

## KPI
Well uptime +18% · unplanned-workover cost −$4.2M/yr · production capture +9,300 bbl/yr per district.

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-predictive-wellhead-maintenance-upstream-og-build-guide.md` — step-by-step build
- `APEX-predictive-wellhead-maintenance-upstream-og-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
