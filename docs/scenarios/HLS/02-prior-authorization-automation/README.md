# Prior authorization automation

**Practice:** HLS — Health, Life Sciences  
**Scenario index:** 02 of 5 featured (global chain 7 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
High-volume specialty procedures (imaging, infusions, surgeries) generate 2,400 prior-auth requests/week . Median cycle 6.2 days; 23% of clinical hours spent on auth administration.

## Solution
Prior-auth agent assembles clinical evidence from the EMR, maps to payer medical-necessity criteria, drafts the submission with supporting documentation. HITL gate before submission.

## Use Case
Specialty-procedure prior auth across 14 highest-volume CPT codes. Reads PatientML.Encounter , ClaimML.PriorAuth , payer-criteria corpus in LEDGER.

## Service
HLS-E2E-04 Care Management &amp; UM. Wave 2 at pilot service line; Wave 3 system-wide.

## Persona
Primary Nicole Tran · Care Management Lead Reviews submissions pre-send; approves or edits.

## KPI
Cycle time 6.2d → 2.6d · first-pass approval rate +28pp · clinical time on auth admin −71% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-prior-authorization-automation-build-guide.md` — step-by-step build
- `APEX-prior-authorization-automation-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
