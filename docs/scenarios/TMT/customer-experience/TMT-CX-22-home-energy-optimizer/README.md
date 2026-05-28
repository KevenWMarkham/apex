# Home energy optimizer

**Practice:** TMT — Technology, Media, Telecom
**Catalog index:** 22
**Service code:** `TMT-TEL-HOM-02`
**Headline KPI:** ↑ +$8 to +$18/mo per household in utility-bill reduction

## Description

Tariff-aware HVAC, EV-charge, and discretionary-load shifting against utility time-of-use windows and the customer's posted tariff. Reads `gold.v_tmt_hom_energy_household_hourly` plus thermostat / charger state; writes to Nest / ecobee / ChargePoint via partner tools. Demand-response participation flows capacity-payment share back to the household.

## Status

Featured scenario for the Telco Home Agentic pack.

## Cross-references

- Agentic pack: [`docs/agentic-packs/telco/`](../../../../agentic-packs/telco/)
- Agent YAML: [`packages/apex-agents/src/apex_agents/catalogs/tmt/13-home-energy-optimizer.yaml`](../../../../../packages/apex-agents/src/apex_agents/catalogs/tmt/13-home-energy-optimizer.yaml)
- Bronze/Silver/Gold lineage: [`docs/agentic-packs/telco/04-medallion-bronze-silver-gold.md`](../../../../agentic-packs/telco/04-medallion-bronze-silver-gold.md)
- Build-spec amendment: [`docs/build-specs/apex-tmt-agentic-home-amendment.md`](../../../../build-specs/apex-tmt-agentic-home-amendment.md)
