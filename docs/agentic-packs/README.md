# Agentic Packs

**Cross-cutting design packs** that extend one or more APEX Editions with a coherent agentic business model — not a single scenario, not a single industry pack, but a multi-document narrative that ties **business model → data feeds → schema → medallion build → services catalog → partnerships → value model → go-to-market** into one place.

Use a pack when the proposition spans:

- A **new business model** layered on top of an existing customer base
- **Multiple device or system feeds** that need a unified data foundation
- A **catalog of subscribable services** (orchestrator + sub-agents) rather than a single agent
- A **partnership ecosystem** where the platform's defensibility comes from who else plays on it

Packs are **design artefacts**. They reference (and are operationalized by) the Edition build-specs, scenario folders, and agent YAMLs — they do not replace them.

## Packs

| Pack | Edition(s) extended | Status | Description |
|---|---|---|---|
| [`telco/`](./telco/) | TMT (with TMT-TEL-HOM-* service line) | Draft | Telco Home Agentic — orchestrated in-home services on top of router/ONT, customer-owned vault, subscribable sub-agents (Grocery, Energy, Eldercare, Maintenance, Security, Wellness, Vehicle, Entertainment) |

## Authoring a new pack

1. Copy [`_template/`](./_template/) into `docs/agentic-packs/<your-pack>/`.
2. Fill in the ten standard sections (business model → device feeds → ERD → medallion → services catalog → partnerships → business value → consumer case → portability → ecosystem differentiators).
3. Register any new service codes in the parent Edition build-spec (e.g., for the `telco` pack, see `docs/build-specs/apex-tmt-agentic-home-amendment.md`).
4. Scaffold the corresponding scenario folders under `docs/scenarios/<PRACTICE>/<domain>/`.
5. Scaffold the agent YAMLs under `packages/apex-agents/src/apex_agents/catalogs/<practice>/`.
6. Update the parent Edition's scenario manifest so `apex-validate.js` picks up the new tables/views.

## Relationship to existing APEX artefacts

```
docs/build-specs/          ← Edition specs (Core, TMT, HLS, RC, ER, AXLE, TH, ICE)
docs/scenarios/            ← per-Practice scenario library (operationalizes services)
packages/apex-agents/      ← agent catalog YAMLs (operationalizes agents)
docs/agentic-packs/        ← THIS — cross-cutting business-model design packs
```

A pack is **narrative-first**. The Edition specs, scenarios, and YAMLs are **implementation-first**. Packs make the cross-cutting "why this works as a coherent business" argument that no single scenario folder can carry.
