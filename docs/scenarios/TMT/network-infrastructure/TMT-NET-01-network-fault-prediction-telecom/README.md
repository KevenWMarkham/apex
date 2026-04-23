# Network fault prediction — telecom

**Practice:** TMT — Technology, Media, Telecom  
**Scenario index:** 02 of 5 featured (global chain 22 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Mobile RAN operations generate 28,000 tickets/month . 60% are reactive; many have early-warning signals in performance counters (RSRP, PRB, SINR) that go unnoticed. Unplanned outages average 11/month.

## Solution
Network-fault agent monitors RAN and transport counters, surfaces anomalies with predicted-failure window, proposes preventive-maintenance action. HITL on proactive truck rolls.

## Use Case
RAN fault prediction across urban metro. Reads TELML.Cell , TELML.Counter , TELML.Alarm .

## Service
TMT-TEL-NET-02 Network Operations. Wave 2 at one metro; Wave 3 enterprise.

## Persona
Primary Marcus Jeon · Network Operations Lead Reviews predictions; dispatches proactive maintenance.

## KPI
Ticket volume −41% · MTTR −28% · proactive-maintenance rate 18% → 67% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-network-fault-prediction-telecom-build-guide.md` — step-by-step build
- `APEX-network-fault-prediction-telecom-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
