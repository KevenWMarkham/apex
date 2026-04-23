# Refinery yield optimization

**Practice:** ER — Energy & Resources  
**Scenario index:** 03 of 5 featured (global chain 13 of 35)  
**Source:** APEX-Stacked-Architecture-Narrated.html

## Scenario
Complex refinery (350 kbpd) has 0.9%–1.4% yield gap vs optimal in the gasoline fractionator. APC tuning is infrequent and reactive; real-time spread between theoretical and actual yield is ~$14M/yr.

## Solution
Yield-optimization agent ingests DCS data, crude assays, market crack spreads, unit constraints. Recommends APC setpoint adjustments in 4-hour cycles; proposes operating envelope to panel operators. HITL always for control changes.

## Use Case
Gasoline-complex fractionator yield optimization. Reads UOGML.Unit , UOGML.Assay , market-price feed.

## Service
ER-OG-05 Refining Optimization. Wave 2 at flagship refinery; Wave 3 multi-site.

## Persona
Primary Elena Rodriguez · Plant Manager Reviews daily performance; panel operators execute agent recommendations.

## KPI
Yield +1.8% · margin capture +$14M/yr · operating-envelope violations −34% .

## Wave Ribbon (W1 Foundation / W2 Pilot / W3 Scale & Fuse)

_The authored W1 prerequisites, W2 pilot scope, W3 enterprise rollout, and fusion-partner references for this scenario live in the narrated HTML._

## Artifacts to land in this folder

- `APEX-refinery-yield-optimization-build-guide.md` — step-by-step build
- `APEX-refinery-yield-optimization-walkthrough.docx` — narrative walkthrough for sellers
- `tests/` — pytest fixtures + harness scenarios (once apex-test-harness targets this Practice)
- `artifacts/` — diagrams, screenshots, sample payloads
- `manifests/` — agent / orchestration / policy manifest YAMLs

## Cross-references

- Practice overview: [../README.md](../README.md)
- Compact catalog: [../_browse-catalog.md](../_browse-catalog.md)
- Narrated architecture: [../../reference/APEX-Stacked-Architecture-Narrated.html](../../reference/APEX-Stacked-Architecture-Narrated.html)
- APEX Design: [../../APEX - Design and Build/APEX_Design.md](../../APEX%20-%20Design%20and%20Build/APEX_Design.md)
