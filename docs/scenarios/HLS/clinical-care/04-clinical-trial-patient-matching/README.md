# Clinical trial patient matching

**Practice:** HLS — Health, Life Sciences  
**Scenario index:** 05 of 5 featured (global chain 10 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Academic medical center runs 340 active trials . Only 4% of eligible patients are enrolled due to matching complexity — manually screening I/E criteria against the EMR takes weeks per cohort. Pharma sponsors escalate enrollment concerns.

## Solution
Trial-matching agent parses the EMR at scale, evaluates I/E criteria per active protocol, ranks match confidence, produces ranked patient list for investigator review. HITL is always the PI.

## Use Case
Trial-feasibility assessment + enrollment outreach. Reads PatientML.Patient , StudyML.Protocol , genomics in LEDGER.

## Service
HLS-LS-03 Clinical Trial Operations. Wave 2 at oncology portfolio; Wave 3 enterprise trial pipeline.

## Persona
Primary Dr. Marcus Webb · Principal Investigator Reviews ranked match list; coordinators execute outreach.

## KPI
Enrollment rate +47% · screen-failure rate −33% · median time-to-enrollment −12 weeks .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-clinical-trial-patient-matching-build-guide.md` — step-by-step build
- `APEX-clinical-trial-patient-matching-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
