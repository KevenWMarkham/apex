# Supply chain disruption response

**Practice:** AXLE — Automotive & Manufacturing  
**Scenario index:** 03 of 5 featured (global chain 18 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Tier-1 automotive supplier disruptions (material shortages, logistics delays, geopolitical events) hit the plant 14x/yr on average . Traditional response is reactive, manual, days-long; cost is $11M/yr in expedite freight and line stops.

## Solution
Supply-disruption agent fuses supplier ERP feeds, logistics providers, news/sanctions monitoring, weather, inventory position. Proposes response playbook (expedite, substitute, dual-source, reschedule) with simulated cost/service impact. HITL on dual-source activation.

## Use Case
End-to-end supply-risk monitoring + response orchestration. Reads SupplyML-A.Supplier , SupplyML-A.Shipment , external-event feed.

## Service
AXLE-Supply-04 Supply Resilience. Wave 2 at critical-material portfolio; Wave 3 enterprise.

## Persona
Primary Sohrab Irani · Supply Chain Director Reviews disruption alerts; approves response playbook.

## KPI
On-time disruption response +43pp · expedite cost −$11M/yr · line-stop events −62% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-supply-chain-disruption-response-build-guide.md` — step-by-step build
- `APEX-supply-chain-disruption-response-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
