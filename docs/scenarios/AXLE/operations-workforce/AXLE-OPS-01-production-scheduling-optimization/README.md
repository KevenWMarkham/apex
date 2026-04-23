# Production scheduling optimization

**Practice:** AXLE — Automotive & Manufacturing  
**Scenario index:** 04 of 5 featured (global chain 19 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Mixed-model assembly line schedules are built weekly by a master planner; changeovers and sequence decisions are rule-of-thumb. Throughput is 89% of theoretical ; on-time delivery runs 82%.

## Solution
Production-scheduling agent optimizes sequence across changeover constraints, material availability, order priority, due dates. Proposes weekly schedule + real-time reschedule on disruption. HITL on any reschedule affecting committed orders.

## Use Case
Mixed-model line scheduling. Reads OpsML-A.WorkOrder , OpsML-A.Equipment , SupplyML-A.Inventory .

## Service
AXLE-Ops-03 Production Ops. Wave 2 at one plant; Wave 3 network.

## Persona
Primary Danila Volkov · Operations Manager Reviews daily schedule; approves reschedules.

## KPI
Throughput +11% · OTD +7pp · changeover time −24% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-production-scheduling-optimization-build-guide.md` — step-by-step build
- `APEX-production-scheduling-optimization-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
