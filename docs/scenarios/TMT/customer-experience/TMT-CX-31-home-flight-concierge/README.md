# Home flight concierge

**Practice:** TMT — Technology, Media, Telecom
**Catalog index:** 31
**Service code:** `TMT-TEL-HOM-11`
**Headline KPI:** ↓ IROPS recovery time (target < 15 min median); ↑ rebook acceptance rate

## Description

Flight booking, status, IROPS rebooking, seat upgrade, baggage tracking across American Airlines (AAdvantage), Delta (SkyMiles), United (MileagePlus), Southwest, JetBlue, Alaska. IROPS recovery is the wedge — detects disruption, cross-references household calendar + traveler preferences, proposes alternate routing (across carriers via Expedia fallback), submits rebook with attached loyalty number.

**Anchor partner:** American Airlines.

## Status

Featured scenario for the Travel & Hospitality agentic pack.

## Cross-references

- Agentic pack: [`docs/agentic-packs/travel-hospitality/`](../../../../agentic-packs/travel-hospitality/)
- Partnership map for this service: [`docs/agentic-packs/travel-hospitality/06-partnership-map.md`](../../../../agentic-packs/travel-hospitality/06-partnership-map.md)
- End-to-end IROPS flow: [`docs/agentic-packs/travel-hospitality/diagrams/flow-irops-end-to-end.md`](../../../../agentic-packs/travel-hospitality/diagrams/flow-irops-end-to-end.md)
- Agent YAML: [`packages/apex-agents/src/apex_agents/catalogs/tmt/21-home-flight-concierge.yaml`](../../../../../packages/apex-agents/src/apex_agents/catalogs/tmt/21-home-flight-concierge.yaml)
- Build-spec amendment: [`docs/build-specs/apex-tmt-agentic-travel-amendment.md`](../../../../build-specs/apex-tmt-agentic-travel-amendment.md)
