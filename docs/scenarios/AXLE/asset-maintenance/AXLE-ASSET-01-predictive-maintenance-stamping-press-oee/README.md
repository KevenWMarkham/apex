# Predictive maintenance — stamping press OEE

**Practice:** AXLE — Automotive & Manufacturing  
**Scenario index:** 01 of 5 featured (global chain 16 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Automotive stamping line has 67% OEE . Unplanned downtime = 14% of available time. Die-crack failures are the top single contributor; early indicators in acoustic-emission and motor-current signatures are buried in manual-review-heavy workflow.

## Solution
PdM agent fuses PLC telemetry, vibration, thermal, acoustic-emission signals. Surfaces predicted-failure windows with confidence intervals. Recommends maintenance actions in between-shift windows. HITL on action plan.

## Use Case
Stamping-line PdM across 12 presses. Reads AXLEML.Equipment , AXLEML.Shift , OPC-UA stream.

## Service
AXLE-Connected-Factory-01 PdM &amp; OEE. Wave 2 at pilot plant; Wave 3 enterprise.

## Persona
Primary Peter Oni · Plant Maintenance Lead Reviews predicted-failure dashboard; dispatches maintenance.

## KPI
OEE +6–9pp · unplanned downtime −41% · maintenance cost −22% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-predictive-maintenance-stamping-press-oee-build-guide.md` — step-by-step build
- `APEX-predictive-maintenance-stamping-press-oee-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
