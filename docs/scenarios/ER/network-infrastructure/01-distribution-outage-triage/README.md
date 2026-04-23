# Distribution outage triage

**Practice:** ER — Energy & Resources  
**Scenario index:** 01 of 5 featured (global chain 11 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Storm front hits service territory; 340,000 customers offline ; 1,200 field-crew dispatches needed within 2 hours. Traditional dispatch relies on OMS heuristics and senior-dispatcher judgment; restoration is uneven.

## Solution
Outage-triage agent fuses OMS events, AMI ping data, SCADA telemetry, weather model, crew location. Proposes restoration sequence optimized for CMI and critical-load first. HITL per-dispatch approval.

## Use Case
Storm-mode restoration triage. Reads P&amp;U.Outage , P&amp;U.Customer , P&amp;U.Crew , weather feeds.

## Service
ER-PU-04 Distribution Reliability. Wave 2 at two operating companies; Wave 3 enterprise.

## Persona
Primary Terrence Boyle · Grid Operations Supervisor Reviews proposed sequence; approves dispatch in Teams.

## KPI
MTTR −22% · CMI −18% · customer-complaint rate −41% · audit-row attributed.

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-distribution-outage-triage-build-guide.md` — step-by-step build
- `APEX-distribution-outage-triage-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
