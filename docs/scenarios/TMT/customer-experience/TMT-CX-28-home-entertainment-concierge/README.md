# Home entertainment concierge

**Practice:** TMT — Technology, Media, Telecom
**Catalog index:** 28
**Service code:** `TMT-TEL-HOM-08`
**Headline KPI:** ↑ engagement minutes; ↑ bundled-streamer attach rate

## Description

Cross-device watch/listen orchestration across smart TVs, streaming sticks, game consoles, smart speakers (Echo, Google Nest, HomePod), and connected audio (Sonos). Reads `MediaSessionEvent` to inform personalized content suggestions; respects household profile boundaries (kids vs. adult content); coordinates bundled-streamer offers (Netflix, Disney+, Max, Paramount+, Peacock) to surface as part of the customer's Telco bill. Read-only by default; write only for explicit content adds.

## Status

Featured scenario for the Telco Home Agentic pack.

## Cross-references

- Agentic pack: [`docs/agentic-packs/telco/`](../../../../agentic-packs/telco/)
- Agent YAML: [`packages/apex-agents/src/apex_agents/catalogs/tmt/19-home-entertainment-concierge.yaml`](../../../../../packages/apex-agents/src/apex_agents/catalogs/tmt/19-home-entertainment-concierge.yaml)
- Bronze/Silver/Gold lineage: [`docs/agentic-packs/telco/04-medallion-bronze-silver-gold.md`](../../../../agentic-packs/telco/04-medallion-bronze-silver-gold.md)
- Build-spec amendment: [`docs/build-specs/apex-tmt-agentic-home-amendment.md`](../../../../build-specs/apex-tmt-agentic-home-amendment.md)
