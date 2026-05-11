# Design — Trilogy-Wide Fabric IQ Adoption

**Date:** 2026-05-11
**Author:** Keven Markham
**Status:** Approved — addenda landing across all three Trilogy volumes
**Scope:** Add Fabric IQ adoption guidance to Services Guide, Deployment Guide, and Sellers Guide as clearly-marked closing addenda. Update Library landing + TRILOGY-MS-PLATFORM-VALIDATION.md.

---

## Goal

Microsoft has shipped **Fabric IQ** as a Fabric workload — Ontology (preview) · Plan (preview) · Graph (preview) · Data Agent (**GA**) · Operations Agent (preview) · Power BI semantic models — that converts what the Trilogy currently describes as hand-rolled APEX primitives (canonical schemas with DDL + ERDs, custom MCP read tools per Gold view, custom orchestration of operational AI alerts) into native Microsoft surfaces. The Trilogy needs an answer to "what changes when the client is on Fabric IQ?" without invalidating the existing chapters (still correct for non-Fabric-IQ clients like Vuori).

## Approach

**Additive · closing addenda.** Each Trilogy volume gains a new closing chapter/section labeled "Fabric IQ Addendum" with status pins, edit notes, and Microsoft Learn anchors. Existing chapters are untouched in this pass — they remain correct for the MCP-led path. A future revision (next quarter, after preview-state items move) will fold the addenda into the relevant in-line chapters.

The addenda are pinned to current Microsoft Learn — Fabric Data Agent is GA today, the other Fabric IQ items are preview. Currency note at the top of each addendum tracks state.

## Per-volume scope

### Services Guide — 14 edits
The full architectural impact. New chapter "Adopting Fabric IQ at the Fabric Layer" with 14 numbered edits (E1–E14) covering: schemas → ontology, MCP catalog bifurcation, governance precedence lattice, Foundry orchestration of Fabric Data Agents, Operations Agent archetype, per-Service ontology authoring, DSPM-for-AI integration, ALM via Fabric deployment pipelines.

### Deployment Guide — 6 deployment-specific notes
- F2+ capacity floor (no trial capacities for Operations Agent)
- Cross-region capacity affinity (Data Agent + sources must share region)
- Cross-geo processing/storage tenant setting
- Workspace outbound access protection (PSG-16 candidate)
- Fabric deployment pipelines + Git integration for Data Agent assets
- Operations Agent Teams app provisioning

### Sellers Guide — 4 positioning notes
- Pitch shift: "Microsoft now ships the semantic + Q&A layer natively"
- Strengthens the "101→401" answer — clients inherit Microsoft governance + Purview lineage
- Fabric-Trilogy bundle for Fabric-resident clients (ECIF leverage)
- Objection handling: "Aren't you obsolete if Microsoft ships this?"

### Library landing
- New "Currency · Fabric IQ" banner pointing at the three addenda
- Reading-path entries updated: Service Architect path adds "for Fabric IQ clients, also read Services Guide Addendum NN"

### TRILOGY-MS-PLATFORM-VALIDATION.md
Add new **Recommended additions** section entries:

- **A7** — Fabric IQ workload as a first-class architectural option
- **A8** — Fabric Data Agent (GA) as MCP-equivalent for read paths
- **A9** — Operations Agent as a new orchestration archetype

## Status pin (canonical, used in every addendum)

| Fabric IQ item | Status (May 2026) |
|---|---|
| Fabric IQ workload | Preview |
| Ontology | Preview |
| Plan | Preview |
| Graph | Preview |
| Data Agent | **GA** |
| Operations Agent | Preview |
| DLP for Fabric Data Warehouse | GA |
| Access restriction policies (KQL/SQL/Warehouse) | Preview |
| DSPM Data Risk Assessments · Insider Risk Management · Risk discovery for agents | Preview |

When preview items move to GA, the pin updates and the relevant edit-note flips from "preview-gated" to "production".

## Source baseline (fetched 2026-05-11)

- [learn.microsoft.com/fabric/iq/overview](https://learn.microsoft.com/fabric/iq/overview)
- [learn.microsoft.com/fabric/data-science/concept-data-agent](https://learn.microsoft.com/fabric/data-science/concept-data-agent)
- [learn.microsoft.com/fabric/real-time-intelligence/operations-agent](https://learn.microsoft.com/fabric/real-time-intelligence/operations-agent)
- [learn.microsoft.com/fabric/iq/ontology/overview](https://learn.microsoft.com/fabric/iq/ontology/overview)
- [learn.microsoft.com/azure/foundry/agents/how-to/tools/fabric](https://learn.microsoft.com/azure/foundry/agents/how-to/tools/fabric)
- [learn.microsoft.com/purview/ai-copilot-fabric](https://learn.microsoft.com/purview/ai-copilot-fabric)

## What stays identical across the Trilogy

- The 38-Service catalog
- Bronze/Silver/Gold medallion
- Two-contract Independence model
- LEDGER hash chain + Purview audit (Fabric writes its own trail; LEDGER references it)
- Foundry-hosted agent fleet (Fabric Data Agents become tools, not replacements)
- 4-tier PII classification with pii-unlock identity
- Wave 1 → Wave 2 → Wave 3 commercial envelope
- PSG-1 through PSG-15 (PSG-16 candidate added in Deployment Guide addendum)

## Decision matrix (engagement-level)

| Engagement profile | Path |
|---|---|
| Fabric-resident client, English-only ops, conversational analytics primary | **Fabric IQ-led** |
| Snowflake-on-Azure client (e.g., Vuori) | **MCP-led** |
| Multi-region client, non-English markets, heavy bulk-extract needs | **Hybrid with bias to MCP** |
| Fabric-resident client building cross-domain reasoning (Order → Shipment → Sensor → Breach) | **Fabric IQ-led, ontology-first** |

## Risks

- **Preview drift** — Fabric IQ items in preview may change. Mitigation: currency banner in every addendum, quarterly review cycle.
- **Reader confusion** — Existing Services Guide chapters describe schemas as DDL. Mitigation: explicit cross-reference from each addendum back to the existing chapter it modifies; explicit "what stays the same" note.
- **Trial capacity gap** — Operations Agent requires paid F-SKU. Mitigation: Deployment Guide addendum flags this for laptop/dev substrates; Foundry stand-in noted.

## Out of scope (deferred)

- Inline rewrites of Services Guide schema chapters
- Bicep templates for Fabric IQ items (preview APIs)
- Ontology authoring tooling
- Migration playbook (DDL → Ontology)

These move to a later revision after Fabric IQ items reach GA.
