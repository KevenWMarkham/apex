# Pipeline integrity & leak detection

**Practice:** ER — Energy & Resources  
**Scenario index:** 05 of 5 featured (global chain 15 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
2,800-mile pipeline network. Legacy SCADA-based leak detection requires 2–8% volumetric change to trigger — most leaks caught late or by third-party reports. Unplanned shutdowns average 11/yr at $280K median cost.

## Solution
Pipeline-integrity agent fuses SCADA pressure/flow, fiber-optic DAS (distributed acoustic sensing), weather, third-party call-in reports. Detects anomalies at 0.3–0.5% threshold; proposes shut-in, dispatches inspection. HITL on shut-in.

## Use Case
Mainline + lateral leak detection. Reads UOGML.Pipeline , UOGML.Sensor , weather feed.

## Service
ER-OG-07 Midstream Integrity. Wave 2 on one mainline; Wave 3 network-wide.

## Persona
Primary Carla Delgado · Pipeline Integrity Manager Reviews anomaly alerts; approves shut-in decisions.

## KPI
Unplanned shutdowns −41% · mean-time-to-detection 4.2 min (vs prior 47 min) · false-positive rate &lt;1 per mile-month.

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-pipeline-integrity-leak-detection-build-guide.md` — step-by-step build
- `APEX-pipeline-integrity-leak-detection-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
