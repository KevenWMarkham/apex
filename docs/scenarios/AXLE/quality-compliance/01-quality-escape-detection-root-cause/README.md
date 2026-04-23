# Quality escape detection & root-cause

**Practice:** AXLE — Automotive & Manufacturing  
**Scenario index:** 02 of 5 featured (global chain 17 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Precision-machining operation has 4.2% first-pass-yield defect rate on critical-to-quality (CTQ) features. Root-cause analysis takes 4–8 days per escape; recurrence rate is 31%.

## Solution
Quality-escape agent fuses CMM data, operator logs, SPC control charts, supplier-material lot data. Proposes root-cause hypothesis ranked by confidence; surfaces corrective-action candidates. HITL on CAPA approval.

## Use Case
CTQ-feature quality monitoring + RCA automation. Reads AXLEML.Inspection , AXLEML.Material , QMS-1 data.

## Service
AXLE-QMS-02 Quality Management. Wave 2 at flagship plant; Wave 3 enterprise.

## Persona
Primary Katherine Liu · Quality Director Reviews RCA proposals; approves CAPA actions.

## KPI
FPY defect rate −52% · RCA cycle time −74% · recurrence rate −58% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-quality-escape-detection-root-cause-build-guide.md` — step-by-step build
- `APEX-quality-escape-detection-root-cause-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
