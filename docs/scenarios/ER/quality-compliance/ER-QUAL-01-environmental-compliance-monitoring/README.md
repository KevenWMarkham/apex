# Environmental compliance monitoring

**Practice:** ER — Energy & Resources  
**Scenario index:** 04 of 5 featured (global chain 14 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Mining operation has 240 permit conditions across air, water, tailings, noise, biodiversity. Monitoring is largely manual; agency audits find 18–24 violations/year; $2M+/yr in fines and remediation .

## Solution
Compliance-monitoring agent continuously reads sensor network (air-quality stations, water-quality probes, tailings-pond instruments), cross-references against permit conditions, flags drift before violation. HITL for agency notification.

## Use Case
Real-time permit-condition monitoring. Reads MiningML.Site , MiningML.Sensor , permit corpus in LEDGER.

## Service
ER-MN-02 Environmental &amp; Compliance. Wave 2 at one mine site; Wave 3 enterprise.

## Persona
Primary Ahmed Farouk · EHS Director Reviews real-time dashboard; approves agency-communication decisions.

## KPI
Permit violation rate −67% · fines and remediation −$1.4M/yr · full FSMA-equivalent audit trail via LEDGER.

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-environmental-compliance-monitoring-build-guide.md` — step-by-step build
- `APEX-environmental-compliance-monitoring-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
