# Baggage proactive resolution

**Practice:** TH — Travel & Hospitality  
**Scenario index:** 04 of 5 featured (global chain 29 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Airline mishandles 5.3 bags per 1,000 passengers . Traditional workflow is reactive — passenger reports at baggage service, files claim, waits. Claims hit $7.2M/yr in direct compensation plus NPS damage.

## Solution
Baggage agent tracks bag via RFID + flight data + destination handoffs. Detects mishandling within 30 minutes of occurrence; generates proactive outreach + compensation offer BEFORE passenger reports. HITL on comp above threshold.

## Use Case
Proactive mishandled-bag recovery. Reads TravelerML.Passenger , TripML.Baggage , IATA RFID feeds.

## Service
TH-AIR-04 Baggage Operations. Wave 2 at three hubs; Wave 3 network.

## Persona
Primary Amelia Park · Ground Operations Supervisor Reviews mishandled-bag alerts; approves recovery playbook.

## KPI
Claim-escalation rate −44% · compensation cost −$7.2M/yr · baggage-related NPS hit −31% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-baggage-proactive-resolution-build-guide.md` — step-by-step build
- `APEX-baggage-proactive-resolution-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
