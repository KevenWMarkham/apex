# Home trip orchestrator

**Practice:** TMT — Technology, Media, Telecom
**Catalog index:** 30
**Service code:** `TMT-TEL-HOM-10`
**Headline KPI:** ↑ successful trip intent rate; ↓ state-transition latency

## Description

Trip-mode meta-orchestrator for the Travel & Hospitality pack. Detects upcoming travel via calendar / booking signals, drives household-state transitions (At-Home → Departing → In-Transit → On-Location → Returning → Reunified), routes trip intents to HOM-11..17 sub-agents, and coordinates with the Home Orchestrator (HOM-99) on home-side posture.

## Status

Featured scenario for the Travel & Hospitality agentic pack.

## Cross-references

- Agentic pack: [`docs/agentic-packs/travel-hospitality/`](../../../../agentic-packs/travel-hospitality/)
- Agent YAML: [`packages/apex-agents/src/apex_agents/catalogs/tmt/20-home-trip-orchestrator.yaml`](../../../../../packages/apex-agents/src/apex_agents/catalogs/tmt/20-home-trip-orchestrator.yaml)
- Sister Home Orchestrator: `TMT-CX-29-home-orchestrator` (`TMT-TEL-HOM-99`)
- Build-spec amendment: [`docs/build-specs/apex-tmt-agentic-travel-amendment.md`](../../../../build-specs/apex-tmt-agentic-travel-amendment.md)
