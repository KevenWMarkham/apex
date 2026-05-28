# Home grocery replenishment

**Practice:** TMT — Technology, Media, Telecom
**Catalog index:** 21
**Service code:** `TMT-TEL-HOM-01`
**Headline KPI:** ↑ +30–60 min/wk grocery time saved per household

## Description

Pantry/fridge-driven grocery orchestration. Smart-fridge camera, pantry weight sensors, trash barcode scanner, and purchase history together produce a continuous inventory state. When projected days-of-supply for any product crosses a threshold, the agent drafts a cart, cross-checks calendar (e.g., dinner party Saturday) and budget, surfaces for HITL approval if the cart exceeds the household's threshold, and submits to the customer's connected grocer via vendor OAuth.

## Status

Featured scenario for the Telco Home Agentic pack. Full chain (Scenario → Solution → Use Case → Service → Persona → KPI) is authored across the pack documents — see [`docs/agentic-packs/telco/`](../../../../agentic-packs/telco/).

## Cross-references

- Agentic pack: [`docs/agentic-packs/telco/`](../../../../agentic-packs/telco/)
- Agent YAML: [`packages/apex-agents/src/apex_agents/catalogs/tmt/12-home-grocery-replenishment.yaml`](../../../../../packages/apex-agents/src/apex_agents/catalogs/tmt/12-home-grocery-replenishment.yaml)
- Bronze/Silver/Gold lineage: [`docs/agentic-packs/telco/04-medallion-bronze-silver-gold.md`](../../../../agentic-packs/telco/04-medallion-bronze-silver-gold.md)
- End-to-end diagram: [`docs/agentic-packs/telco/diagrams/flow-grocery-end-to-end.md`](../../../../agentic-packs/telco/diagrams/flow-grocery-end-to-end.md)
- Build-spec amendment: [`docs/build-specs/apex-tmt-agentic-home-amendment.md`](../../../../build-specs/apex-tmt-agentic-home-amendment.md)
