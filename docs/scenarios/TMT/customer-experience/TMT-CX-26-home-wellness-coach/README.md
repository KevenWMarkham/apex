# Home wellness coach

**Practice:** TMT — Technology, Media, Telecom
**Catalog index:** 26
**Service code:** `TMT-TEL-HOM-06`
**Headline KPI:** ↑ chronic-condition adherence rate; ↑ telehealth-escalation conversion

## Description

Wearable + sleep + glucose coaching for household members who opt in. Reads `gold.v_tmt_hom_wellness_person_daily` (PHI-scoped, behind RLS). Coordinates with CGM (Dexcom / Abbott), sleep (Eight Sleep / Sleep Number), wearables (Apple Health / Fitbit / Oura), and pharmacy adherence (Hero / MedMinder). Escalates to telehealth (Teladoc / Amwell) when daily metrics cross clinically defined thresholds. Often sponsored by a payer or employer wellness program.

## Status

Featured scenario for the Telco Home Agentic pack.

## Cross-references

- Agentic pack: [`docs/agentic-packs/telco/`](../../../../agentic-packs/telco/)
- Agent YAML: [`packages/apex-agents/src/apex_agents/catalogs/tmt/17-home-wellness-coach.yaml`](../../../../../packages/apex-agents/src/apex_agents/catalogs/tmt/17-home-wellness-coach.yaml)
- Bronze/Silver/Gold lineage: [`docs/agentic-packs/telco/04-medallion-bronze-silver-gold.md`](../../../../agentic-packs/telco/04-medallion-bronze-silver-gold.md)
- Build-spec amendment: [`docs/build-specs/apex-tmt-agentic-home-amendment.md`](../../../../build-specs/apex-tmt-agentic-home-amendment.md)
