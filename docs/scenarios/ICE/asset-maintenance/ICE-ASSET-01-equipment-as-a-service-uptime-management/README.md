# Equipment-as-a-service uptime management

**Practice:** ICE — Industrial, Construction, Equipment  
**Scenario index:** 04 of 5 featured (global chain 34 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
EaaS contracts across 340 enterprise customers have 97.5% uptime SLA. Current adherence is 91.2%; SLA-penalty exposure $4.2M/yr . Root cause: reactive maintenance + long parts lead-times + uncoordinated dispatch.

## Solution
Uptime agent fuses equipment telemetry + SLA-consumption tracker + parts-availability + technician-scheduling. Proposes preventive-maintenance windows + parts pre-staging + dispatch priority. HITL on customer communications.

## Use Case
EaaS-contract portfolio uptime. Reads ConnectedICEML.Unit , ConnectedICEML.Contract , AftermarketML.Technician .

## Service
ICE-EaaS-04 Connected Service. Wave 2 at top contracts; Wave 3 portfolio.

## Persona
Primary Wei Zhang · EaaS Service Director Reviews SLA dashboard; approves customer-communication escalations.

## KPI
SLA adherence 91.2% → 97.6% · penalty cost −$4.2M/yr · EaaS renewal rate +14pp .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-equipment-as-a-service-uptime-management-build-guide.md` — step-by-step build
- `APEX-equipment-as-a-service-uptime-management-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
