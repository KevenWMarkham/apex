# Home orchestrator (meta-agent)

**Practice:** TMT — Technology, Media, Telecom
**Catalog index:** 29
**Service code:** `TMT-TEL-HOM-99`
**Headline KPI:** ↑ successful intent rate; ↑ customer NPS for Home Agentic

## Description

Meta-orchestrator for the Telco Home Agentic suite. Routes household intents ("order groceries", "lower the bill", "make sure Mom's OK") to the appropriate sub-agent (`TMT-TEL-HOM-01..08`) and aggregates results. Reads Gold views only — never raw Bronze/Silver — and writes only via sub-agent tools. PHI and CPNI are forbidden classifications at the orchestrator level; only sub-agents may handle them. Included free at every subscription tier; it has no value without at least one sub-agent.

## Status

Featured scenario for the Telco Home Agentic pack. This is the meta-agent — the entry point for natural-language interaction with the platform.

## Cross-references

- Agentic pack: [`docs/agentic-packs/telco/`](../../../../agentic-packs/telco/)
- Agent YAML: [`packages/apex-agents/src/apex_agents/catalogs/tmt/11-home-orchestrator.yaml`](../../../../../packages/apex-agents/src/apex_agents/catalogs/tmt/11-home-orchestrator.yaml)
- Sub-agents (HOM-01..08): scenarios `TMT-CX-21` through `TMT-CX-28` in this folder
- Build-spec amendment: [`docs/build-specs/apex-tmt-agentic-home-amendment.md`](../../../../build-specs/apex-tmt-agentic-home-amendment.md)
