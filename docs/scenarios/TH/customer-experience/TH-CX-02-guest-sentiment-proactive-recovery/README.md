# Guest sentiment & proactive recovery

**Practice:** TH — Travel & Hospitality  
**Scenario index:** 03 of 5 featured (global chain 28 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Hotel group has 17% of guests experience a service issue during stay but only 4% flag it at the property. Post-stay reviews skew negative; recovery-opportunity window closed by the time it's visible.

## Solution
Sentiment agent fuses in-stay signals (service requests, duration in room, phone-call patterns, app chat, POS activity), detects at-risk guests, proposes proactive outreach (manager visit, amenity recovery). HITL on comps above threshold.

## Use Case
Guest-experience in-stay intervention. Reads HotelML.Guest , HotelML.ServiceRequest , CXML.Sentiment .

## Service
TH-HOT-05 Guest Experience. Wave 2 at luxury tier; Wave 3 full portfolio.

## Persona
Primary Sebastian Fox · General Manager Reviews at-risk-guest dashboard; GMs approve intervention spend.

## KPI
NPS +21pts · post-stay complaints −44% · repeat-booking rate +14% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-guest-sentiment-proactive-recovery-build-guide.md` — step-by-step build
- `APEX-guest-sentiment-proactive-recovery-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
