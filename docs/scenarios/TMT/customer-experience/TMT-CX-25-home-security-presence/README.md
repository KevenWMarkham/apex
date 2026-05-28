# Home security & presence

**Practice:** TMT — Technology, Media, Telecom
**Catalog index:** 25
**Service code:** `TMT-TEL-HOM-05`
**Headline KPI:** ↓ false-alarm rate; ↑ P&C insurance-premium discount captured

## Description

Presence-aware arming, visitor verification, and packaged-theft response across the household's cameras, locks, motion sensors, and alarm panels. Reads `home_presence_state` to choose arming mode; coordinates with August / Schlage / Yale locks for visitor grant/revoke; routes verified events to RapidSOS / Noonlight for first-responder dispatch. P&C insurance carriers fund a premium discount the Telco passes through and shares.

## Status

Featured scenario for the Telco Home Agentic pack.

## Cross-references

- Agentic pack: [`docs/agentic-packs/telco/`](../../../../agentic-packs/telco/)
- Agent YAML: [`packages/apex-agents/src/apex_agents/catalogs/tmt/16-home-security-presence.yaml`](../../../../../packages/apex-agents/src/apex_agents/catalogs/tmt/16-home-security-presence.yaml)
- Bronze/Silver/Gold lineage: [`docs/agentic-packs/telco/04-medallion-bronze-silver-gold.md`](../../../../agentic-packs/telco/04-medallion-bronze-silver-gold.md)
- Build-spec amendment: [`docs/build-specs/apex-tmt-agentic-home-amendment.md`](../../../../build-specs/apex-tmt-agentic-home-amendment.md)
