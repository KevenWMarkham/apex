# Contact center intelligence

**Practice:** TMT — Technology, Media, Telecom  
**Scenario index:** 01 of 5 featured (global chain 21 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Telecom operator handles 4.2M calls/month across 14 contact centers. AHT is 8.4 min; FCR is 68%; agent churn is 34%/yr driven by complexity and tool-switching overhead.

## Solution
Contact-center-intelligence agent co-pilots the human agent in real time: retrieves customer context, suggests next-best-action, drafts case notes, surfaces policy constraints. HITL is the agent — the tool assists; the human decides.

## Use Case
Consumer-mobility contact center. Reads TELML.Subscriber , TELML.Incident , TELML.Policy .

## Service
TMT-TEL-CC-03 Contact Center Intelligence. Wave 2 at flagship center; Wave 3 all centers.

## Persona
Primary Yolanda Price · Contact Center Director Reviews metrics; operators use tool real-time.

## KPI
AHT −27% · FCR +14pp · agent CSAT +22pts · agent churn −18pp .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-contact-center-intelligence-build-guide.md` — step-by-step build
- `APEX-contact-center-intelligence-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
