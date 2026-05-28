# Home maintenance orchestrator

**Practice:** TMT — Technology, Media, Telecom
**Catalog index:** 24
**Service code:** `TMT-TEL-HOM-04`
**Headline KPI:** ↑ repair-avoidance $ per household; ↑ on-time consumable replacement rate

## Description

Filter, fluid, firmware, and recall triage across the household's appliance fleet. Reads diagnostic codes + firmware status from connected appliances (Whirlpool, GE, Samsung, LG, Bosch), cross-references against CPSC / NHTSA recall feeds, and orchestrates consumable reorders + service-network dispatch. Auto-orders consumables under a household-set threshold; HITL for service-call dispatch and warranty co-sell.

## Status

Featured scenario for the Telco Home Agentic pack.

## Cross-references

- Agentic pack: [`docs/agentic-packs/telco/`](../../../../agentic-packs/telco/)
- Agent YAML: [`packages/apex-agents/src/apex_agents/catalogs/tmt/15-home-maintenance-orchestrator.yaml`](../../../../../packages/apex-agents/src/apex_agents/catalogs/tmt/15-home-maintenance-orchestrator.yaml)
- Bronze/Silver/Gold lineage: [`docs/agentic-packs/telco/04-medallion-bronze-silver-gold.md`](../../../../agentic-packs/telco/04-medallion-bronze-silver-gold.md)
- Build-spec amendment: [`docs/build-specs/apex-tmt-agentic-home-amendment.md`](../../../../build-specs/apex-tmt-agentic-home-amendment.md)
