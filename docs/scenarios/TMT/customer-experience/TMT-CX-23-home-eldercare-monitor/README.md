# Home eldercare monitor

**Practice:** TMT — Technology, Media, Telecom
**Catalog index:** 23
**Service code:** `TMT-TEL-HOM-03`
**Headline KPI:** ↓ false-positive alert rate; ↓ time-to-caregiver-notification

## Description

Detects deviations from activity-of-daily-living (ADL) baselines using wearable signals + presence (motion, door/bed sensors) + appliance usage patterns. Escalates to designated family contacts and (with consent) clinicians when `elder_adl_deviation_score` exceeds a household-configured threshold. PHI-scoped, HITL-gated. The highest-LTV service in the pack, typically sponsored by a Medicare Advantage plan.

## Status

Featured scenario for the Telco Home Agentic pack.

## Cross-references

- Agentic pack: [`docs/agentic-packs/telco/`](../../../../agentic-packs/telco/)
- Agent YAML: [`packages/apex-agents/src/apex_agents/catalogs/tmt/14-home-eldercare-monitor.yaml`](../../../../../packages/apex-agents/src/apex_agents/catalogs/tmt/14-home-eldercare-monitor.yaml)
- Bronze/Silver/Gold lineage: [`docs/agentic-packs/telco/04-medallion-bronze-silver-gold.md`](../../../../agentic-packs/telco/04-medallion-bronze-silver-gold.md)
- Build-spec amendment: [`docs/build-specs/apex-tmt-agentic-home-amendment.md`](../../../../build-specs/apex-tmt-agentic-home-amendment.md)
