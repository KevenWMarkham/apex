# Ad fraud detection

**Practice:** TMT — Technology, Media, Telecom  
**Scenario index:** 04 of 5 featured (global chain 24 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Digital-media ad platform serves 2.4B ad impressions/day . 7.1% is invalid traffic (bots, click farms, domain-spoofing). Lost advertiser trust = $18M/yr in make-goods and churned advertiser budgets.

## Solution
Ad-fraud agent analyzes click/impression patterns, user-agent fingerprints, traffic graphs, transaction timing. Scores in real time; blocks or reroutes flagged traffic. HITL on policy overrides.

## Use Case
Programmatic ad-serving fraud defense. Reads MEDML.Ad , MEDML.Impression , traffic-graph data.

## Service
TMT-MED-03 Ad Operations Integrity. Wave 2 at mobile-web inventory; Wave 3 all channels.

## Persona
Primary Rena Mikhailova · Ad Operations Director Reviews flagged-traffic trends; approves policy thresholds.

## KPI
Invalid traffic −52% · advertiser make-good payouts −$18M/yr · advertiser retention +11pp .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-ad-fraud-detection-build-guide.md` — step-by-step build
- `APEX-ad-fraud-detection-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
