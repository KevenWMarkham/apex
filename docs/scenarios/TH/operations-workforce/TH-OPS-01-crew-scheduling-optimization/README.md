# Crew scheduling optimization

**Practice:** TH — Travel & Hospitality  
**Scenario index:** 05 of 5 featured (global chain 30 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Airline has 14,000 flight crew . Pairing and rotation are optimized weekly but FAA fatigue rules, equipment-type qualifications, and crew preferences create 3,200+ manual exceptions/month. Fatigue-related cancels cost $12M/yr .

## Solution
Crew-scheduling agent optimizes rotations for FAA compliance + seniority rules + qualification depth + bid preferences. Surfaces fatigue-risk patterns pre-flight. HITL on any schedule change affecting committed pairings.

## Use Case
Monthly crew-pairing + daily re-flow. Reads TravelerML.CrewMember , TripML.Pairing , FAA rule corpus in LEDGER.

## Service
TH-AIR-06 Crew Resource Planning. Wave 2 at narrowbody fleet; Wave 3 widebody.

## Persona
Primary Rebecca Torres · Crew Resource Planner Reviews proposed rotations; approves schedule changes.

## KPI
Fatigue-related cancels −$12M/yr · crew-bid satisfaction +6pts · schedule-change rate −22% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-crew-scheduling-optimization-build-guide.md` — step-by-step build
- `APEX-crew-scheduling-optimization-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
