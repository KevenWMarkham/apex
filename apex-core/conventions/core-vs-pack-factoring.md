# APEX Core vs. Domain Pack — Factoring Convention

**Status:** Normative. Applies to APEX Core v1.3 and later.
**Scope:** The split between platform capabilities (Core) and domain knowledge (Pack), and the manifest seam a Pack declares to Core. Complements — does not replace — the Schema Versioning Convention (`conventions/schema-versioning.md`), which governs data/schema manifests only.

---

## Purpose

An agentic workspace (the Merchandising view that triggered this convention, a Finance-close view, a Supply-chain control tower) is mostly domain-agnostic frame with a minority of domain knowledge. This convention draws the line so the **second** Pack is *a manifest + tools + Gold views, not another application*. Every Pack then inherits HITL, the hash-chained ledger, provenance, and escalation for free — which is the governance / Independence story APEX sells (Deloitte's own accelerator on Microsoft technology).

Full design and rationale: `docs/plans/2026-07-01-apex-core-vs-domain-pack-design.md`.

---

## The Principle (Normative)

**The frame goes to Core; the knowledge stays in the Pack.** Anything that would look and behave **identically** in a Finance-close or Supply-chain-control-tower workspace is Core. Anything that knows what a *markdown* (or a *close*, or a *reorder point*) is stays in the domain Pack.

**Litmus test for any piece:** *"Would the Finance-close workspace need this, unchanged?"*
→ **Yes → Core.** **No → Pack.**

Two hard rules follow:

1. **Core never imports domain code.** Core renders and enforces whatever a manifest declares; it never names a domain concept.
2. **A Pack ships as a manifest + implementations against Core contracts.** Adding a Pack requires **no Core change**.

---

## Core (platform capabilities)

| Capability | What it is (domain-agnostic) |
|---|---|
| **Recommendation envelope + HITL queue** | The card contract → the gate-16 queue → the decision written to the ledger. The workspace spine. |
| **Escalation-policy machinery** | Threshold/floor breach → block the auto-path → escalate to a named human role → sign-off. The *mechanism* is Core; the floor **values** are Pack config. |
| **Agent-roster component** | Rail of agents grouped by capability area, status dot, pending-work count — driven by the Pack manifest. |
| **KPI-strip framework** | Metric card with value / trend / target-band styling. Core renders; the Pack declares KPIs + targets. |
| **Chain-progress widget** | Sense → Reason → Propose → **Gate 16** → Execute → Ledger. The standard visual of the canonical 24-step chain. |
| **Provenance chips** | `gold_<domain>_v<N>` source badges + confidence on every recommendation — the Purview-lineage surface. |
| **Impact-estimate contract** | Typed synthetic-impact field (`value, unit, direction, illustrative:true`) so cards quantify consistently and stay guardrail-compliant. |
| **Priority taxonomy** | Differentiate / Optimize / Grow tagging — platform-level. |
| **`build_workspace(pack)` shell** | Rail + KPI strip + gate queue + agent-detail panel composed from a Pack manifest — the enterprise sibling of the agentic-home `build_app(domains=[…])` seam. |

These are declared by the L1 Pack manifest contract (`data/pack-manifest-contract.json`) under `core_provides`. A Pack conforms to them; it never redefines them.

---

## Pack (domain knowledge)

Stays entirely in the domain Pack — Core never sees these except as manifest declarations:

- **The agents** — the scenario-catalog manifest *is* the Pack.
- **Domain Gold views** — `gold_<domain>_v<N>` schemas + pipelines.
- **KPIs + targets** — the metrics and target bands that view surfaces.
- **Policy content** — floors, thresholds, ladders, zones (values, not the escalation mechanism).
- **Write-side MCP tools** — one-tool-one-purpose, registered into Core's tool registry.
- **Reasoning content** — models, per-agent prompts, rec-card copy.
- **Domain visualizations** and **rail grouping** — domain taxonomy, not platform structure.

---

## The Seam (what a Pack declares to Core)

A Pack manifest conforms to `data/pack-manifest-contract.json` and declares only:

- **Agent descriptors** — `{name, group, scenario_ids, tools[], prompt_ref, priority}`.
- **Gold-view registrations** — the `gold_<domain>_v<N>` views agents may read.
- **KPI descriptors** — `{label, source_view, target, band}`.
- **Policy descriptors** — `{name, metric, threshold, escalate_to_role}`.
- **Tool registrations** — write-side MCP tools, into Core's registry.

Core provides everything else: `build_workspace(pack)`, the recommendation envelope + gate-16 HITL queue, the escalation engine, the chain-progress / provenance / KPI components, the ledger, and the Differentiate/Optimize/Grow taxonomy.

---

## Versioning

- The Pack manifest is a **distinct concern** from the schema manifest. A Pack pins `core_version_required`; its own `manifest_version` follows SemVer for the Pack surface (agents/KPIs/policies/tools/gold-view registrations).
- Core-owned contracts (`core_provides`) version with Core. A MAJOR bump to the recommendation envelope or impact-estimate contract obliges Packs to re-verify their cards on their next release, mirroring the event-envelope rule in the Schema Versioning Convention.
- **Guardrail (hard):** `impact_estimate.illustrative` MUST be `true`. All currency / ROI / impact figures are synthetic reference figures, never client claims.

---

## Out of Scope / Follow-on

- This convention + the L1 contract define the **seam**. Building the `build_workspace(pack)` shell and the recommendation/escalation runtime is a follow-on implementation (per the design doc).
- A `validate-pack.js` validator (sibling to `tools/validate-manifest.js`) that enforces this L1 contract is a follow-on; until it lands, the contract is the normative reference.

---

## References

- Factoring design + rationale: `docs/plans/2026-07-01-apex-core-vs-domain-pack-design.md`
- L1 Pack contract artifact: `apex-core/data/pack-manifest-contract.json`
- Sibling convention (data/schema): `apex-core/conventions/schema-versioning.md`
- Precedent (consumer): agentic-home `apex_core` / `build_app(domains=[…])`

---

**End of APEX Core vs. Domain Pack Factoring Convention**
