# IROPS re-accommodation

**Practice:** TH — Travel & Hospitality  
**Scenario index:** 01 of 5 featured (global chain 26 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Major hub disruption (weather, mechanical, ATC) cancels 140 flights. 18,000 passengers to re-accommodate. Current approach is semi-manual via gate agents; top-tier passenger recovery is 34%; NPS drops 22 points post-event.

## Solution
IROPS agent fuses rebooking options, fare rules, loyalty tier, hotel/meal vouchers. Generates personalized re-accommodation proposal per passenger. HITL for gate-agent-approved policy overrides.

## Use Case
Hub-disruption recovery. Reads TravelerML.Passenger , TripML.Itinerary , TripML.Inventory .

## Service
TH-AIR-02 Irregular Ops. Wave 2 at one hub; Wave 3 network-wide.

## Persona
Primary Rajiv Pillai · Airline Operations Center Lead Reviews disruption metrics; gate agents execute.

## KPI
Top-tier passenger recovery +38pp · NPS improvement +17pts post-event · voucher cost −19% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-irops-re-accommodation-build-guide.md` — step-by-step build
- `APEX-irops-re-accommodation-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
