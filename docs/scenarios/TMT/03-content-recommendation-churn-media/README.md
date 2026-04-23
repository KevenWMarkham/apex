# Content recommendation & churn — media

**Practice:** TMT — Technology, Media, Telecom  
**Scenario index:** 03 of 5 featured (global chain 23 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Streaming service has 24M subscribers . Monthly churn is 4.1%. Recommendation engine is 3 years old; engagement per session is 31 min; cold-start for new content is poor.

## Solution
Recommendation agent learns viewing patterns, content embeddings, session context; proposes personalized rails + surfaces cold-start content via content-similarity reasoning. HITL on editorial overrides.

## Use Case
Homepage + end-of-episode recommendation across the subscriber base. Reads MEDML.Viewer , MEDML.Content , MEDML.Session .

## Service
TMT-MED-01 Subscriber Lifecycle. Wave 2 at mobile app; Wave 3 all surfaces.

## Persona
Primary Li Jun · Subscriber Lifecycle Manager Reviews engagement dashboards; approves editorial-override policies.

## KPI
Churn rate −19% · engagement per session +23% · cold-start engagement +41% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-content-recommendation-churn-media-build-guide.md` — step-by-step build
- `APEX-content-recommendation-churn-media-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
