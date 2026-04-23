# Field service dispatch optimization

**Practice:** ICE — Industrial, Construction, Equipment  
**Scenario index:** 03 of 5 featured (global chain 33 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
OEM operates 1,400 field service technicians across NA. First-time-fix rate is 68% — technicians routinely arrive without the right parts or miss diagnosis. Mean cost per truck roll = $420; repeat-visit rate adds $8.4M/yr .

## Solution
Dispatch agent reads service request + equipment telemetry + technician skill profile + parts availability. Proposes optimal dispatch with pre-loaded parts + remote-guided diagnosis. HITL on dispatch assignments.

## Use Case
Field-service dispatch and readiness. Reads AftermarketML.ServiceRequest , ConnectedICEML.Telemetry , AftermarketML.Technician .

## Service
ICE-Aftermarket-01 Field Service Ops. Wave 2 at one division; Wave 3 enterprise.

## Persona
Primary Beatriz Carvalho · Field Service Manager Reviews dispatch queue; approves escalations.

## KPI
First-time-fix +22pp · repeat-visit cost −$8.4M/yr · dispatch cost −17% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-field-service-dispatch-optimization-build-guide.md` — step-by-step build
- `APEX-field-service-dispatch-optimization-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
