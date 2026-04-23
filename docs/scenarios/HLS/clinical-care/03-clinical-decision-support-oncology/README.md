# Clinical decision support — oncology

**Practice:** HLS — Health, Life Sciences  
**Scenario index:** 03 of 5 featured (global chain 8 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Oncology treatment plans for complex cases require synthesizing NCCN guidelines, genomics, comorbidities, trial eligibility, and payer coverage. Physicians spend 2.8 hours per complex plan ; variance in guideline adherence across attending physicians is 18%.

## Solution
CDS agent reads patient record, retrieves applicable NCCN guidelines, checks trial eligibility, flags coverage issues, proposes evidence-graded plan. HITL is the physician — the agent proposes; the MD decides.

## Use Case
Tumor-board prep + plan drafting. Reads PatientML.Patient , PatientML.Encounter , genomics in LEDGER, NCCN reference in LEDGER.

## Service
HLS-E2E-02 Clinical Decision Support. Wave 2 at academic cancer center; Wave 3 community affiliates.

## Persona
Primary Dr. Andrew Kim · Attending Oncologist Reviews draft plan in EMR-embedded Copilot; modifies, approves, signs.

## KPI
Guideline adherence +14pp · 30-day readmission −21% · time-to-plan −41% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-clinical-decision-support-oncology-build-guide.md` — step-by-step build
- `APEX-clinical-decision-support-oncology-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
