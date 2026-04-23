# Care gap closure — population health

**Practice:** HLS — Health, Life Sciences  
**Scenario index:** 04 of 5 featured (global chain 9 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Value-based contracts require HEDIS measure closure (mammography, colonoscopy, diabetic retinopathy, BP control). Care-gap lists are batch, outreach is manual, closure runs 41% .

## Solution
Care-gap agent identifies open measures per patient, generates outreach in preferred channel (portal, SMS, phone queue), tracks closure, escalates non-responders. HITL gate for clinical-team escalation.

## Use Case
Population-wide HEDIS closure across Medicare Advantage and commercial VBC contracts. Reads PatientML.Patient , ClaimML.Claim , CXML.Communication .

## Service
HLS-E2E-06 Population Health. Wave 2 at 120K-life cohort; Wave 3 enterprise.

## Persona
Primary Dr. Priya Shah · Population Health Director Reviews cohort progress in Power BI; approves outreach-escalation playbooks.

## KPI
HEDIS closure rate +24pp · value-based contract bonus $3.8M · clinical-team outreach time −62% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-care-gap-closure-population-health-build-guide.md` — step-by-step build
- `APEX-care-gap-closure-population-health-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
