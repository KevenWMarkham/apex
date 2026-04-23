# Claims denial prevention

**Practice:** HLS — Health, Life Sciences  
**Scenario index:** 01 of 5 featured (global chain 6 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Commercial-payer denial rate up 11% YoY. UM staff buried in appeals; most denials are preventable (missing auth, wrong code, thin clinical documentation). $28M AR exposure.

## Solution
Denial-prevention agent reviews claim pre-submission against payer-policy-of-record, clinical documentation, prior-auth status, coding accuracy. Flags issues with specific remediation.

## Use Case
Pre-submission claim scrubbing + denial-appeal triage. Reads ClaimML.Claim , PatientML.Encounter , payer-policy corpus in LEDGER.

## Service
HLS-E2E-02 Clinical Decision Support + HLS-E2E-06 Revenue Cycle. Wave 2 across commercial-payer mix.

## Persona
Primary Sasha Mehra · Revenue Cycle Director Reviews flagged-claim dashboard; UM coders resolve per remediation. HITL on clinical-judgment appeals.

## KPI
First-pass denial rate −34% · appeal cycle time −58% · AR &gt;90 days −$11M in Year 1.

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-claims-denial-prevention-build-guide.md` — step-by-step build
- `APEX-claims-denial-prevention-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
