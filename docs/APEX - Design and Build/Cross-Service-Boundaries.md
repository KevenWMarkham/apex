# Cross-Service Schema Ownership Boundaries

**Audience:** Service designers, MCP authors, code reviewers
**Purpose:** Document which RC service is the **sole writer** of each canonical schema, and the **read-only** MCP tools that other services use to consume it. Closes Sprint 39.4 build-status item.

**Why this matters:** RC services share canonical SCML / MERML / CXML / PROML entities. Without an explicit ownership boundary, two services might both write the same Silver row — leading to lost-update conflicts, classification-propagation gaps, and audit-row chains that don't resolve cleanly. This doc declares the boundary; the MCP `required_scopes` enforce it.

---

## TL;DR — ownership table

| Schema | Sole writer | Cross-service read tool | Cross-service consumers |
|---|---|---|---|
| `SCML.SKU` | RC-E2E-03 (master) + supplier portal sync | `scml-mcp.get_sku_by_key` | All RC services |
| `SCML.Inventory` | RC-E2E-03 (cold-chain destroy) + RC-E2E-05 (cycle-count) | `scml-mcp.get_sku_by_key` (via Gold marts) | RC-E2E-04 / -07 (read for context only) |
| **`SCML.Lot`** | **RC-E2E-09** (sole writer per Sprint 39.4) | **`rc_e2e_09.get_lot_provenance`** | **RC-E2E-03 + RC-E2E-07** |
| `SCML.Shipment` | RC-E2E-09 + DC adapter | `scml-mcp.list_shipments_by_destination` | RC-E2E-03 / -07 (read for traceability) |
| `MERML.Markdown` | RC-E2E-03 (sole writer) | `merml-mcp.list_recent_markdowns` | RC-E2E-04 (winback timing) / RC-E2E-07 (returns-fraud price baseline) |
| `MERML.Elasticity` | RC-E2E-03 (Pricer fits the model) | `merml-mcp.get_elasticity_for_sku` | RC-E2E-04 (winback offer-depth response curve) |
| `MERML.Competitor` | RC-E2E-03 (Pricer ingests scrape) | `merml-mcp.get_competitor_observed_prices` | RC-E2E-04 (offer-cap context) |
| `PROML.Pricing` | RC-E2E-03 (Pricer + merchandising team) | `rc_e2e_03.get_pricing_recommendation_basis` | None (TRADE_SECRET; in-service only) |
| `PROML.DiscountRule` | RC-E2E-03 (merchandising team via SAP sync) | `rc_e2e_03.get_pricing_recommendation_basis` | None (TRADE_SECRET; in-service only) |
| `CXML.Customer` | RC-E2E-04 (loyalty enrollment + CRM sync) | `cxml-mcp.get_customer_consent` | RC-E2E-07 (returns-fraud customer graph traversal) |
| `CXML.Loyalty` | RC-E2E-04 (sole writer; winback history) | `cxml-mcp.get_customer_consent` (alongside customer) | None |
| `CXML.Interaction` | RC-E2E-04 (CRM event ingest) | (no cross-service read yet) | RC-E2E-08 marketing — when promoted |
| `CXML.Order` | POS / e-comm SOR (platform-managed; no service writes) | `cxml-mcp` reads | All services (read-only) |
| `CXML.Campaign` | RC-E2E-04 (sole writer) | (no cross-service read yet) | None |
| `CXML.FraudCase` | RC-E2E-07 (sole writer; under PII-unlock handle only) | (no cross-service read yet) | None — internal investigation queue only |
| `CXML.AssociateTask` | RC-E2E-05 (sole writer; per-associate dispatch) | (no cross-service read yet) | None |

---

## Why SCML.Lot is RC-E2E-09's exclusive write surface

FSMA-204 §1.1305 requires Critical Tracking Events (CTEs) and Key Data Elements (KDEs) maintained throughout the supply chain. The lot-event chain is the regulatory artifact a regulator walks during a recall. Splitting writes across services creates three failure modes:

1. **Classification-propagation gaps** — If RC-E2E-03's destroy-disposition wrote `SCML.Lot` directly with `event_kind: lot_status_destruction_only`, the FDA-Reportable-Food-Registry filing trigger that lives in RC-E2E-09's Briefer would never fire (different agent, different audit row, different `trace_id`).
2. **Lost-update conflicts** — If RC-E2E-07 wrote `SCML.Lot` to mark a lot as held-for-fraud-investigation while RC-E2E-09 simultaneously wrote it as recall-class-II, the SCD2 history lands inconsistent. Whichever agent committed second wins; the other agent's audit row references state that no longer exists.
3. **Audit chain divergence** — A regulator subpoenas all events for `lot_key=L-2026W18-DAIRY-A12`. With multiple writers, the chain has multiple `trace_id`s with no canonical sequence.

The fix: **single-writer pattern.** RC-E2E-09's Briefer (`learn` agent) is the only path that calls `commit_lot_event`. Other services express their need via *events*:

- RC-E2E-03 destroy decision → `MERML.Markdown` write (their domain) + emit `lot-destroy-requested` event → RC-E2E-09's Activator-triggered DAG writes the `SCML.Lot.event_kind: lot_status_destruction_only` row.
- RC-E2E-07 fraud-hold-on-recalled-lot → `CXML.FraudCase` write (their domain) + read `rc_e2e_09.get_lot_provenance` to surface the recall context to Rebecca; never writes to `SCML.Lot`.

This is the same pattern Microsoft uses for Purview Audit Graph (single-writer / many-readers via Microsoft Graph) and Microsoft Fabric OneLake (workspace-owner-writes / shortcut-reads).

---

## How the boundary is enforced

### Layer 1 — MCP `required_scopes`

`commit_lot_event` declares `required_scopes: ['practice:rc', 'service:rc-e2e-09']`. The Decide agent of RC-E2E-03 / RC-E2E-07 holds `service:rc-e2e-03` / `service:rc-e2e-07` scope in its OBO token; the contract check fails closed if either tries to call the write tool.

`get_lot_provenance` declares `required_scopes: ['practice:rc']` only — any RC service can read.

### Layer 2 — Pre-deployment Security Gate (PSG-12 NEW)

The wizard's pre-deployment check verifies, for each deployed service, that:
- Its `agent.yaml` `schemas_write` field never lists a schema owned by another service (e.g., RC-E2E-03's act-agent.yaml MUST NOT list `SCML.Lot`).
- Its `agent.yaml` `tools` field references cross-service write tools only with `via_mcp_tool` notation, never raw module imports.

Sprint 46's wizard implementation will add this lint as PSG-12. Until then, the manifest-test patterns Sprint 32+ ship enforce it within each service.

### Layer 3 — Eventstream Activator (production runtime)

When `commit_lot_event` succeeds, RC-E2E-09's Briefer returns `downstream_invalidation_keys` from the MCP tool response. The Foundry runtime publishes those to Eventstream; RC-E2E-03's and RC-E2E-07's Gold-mart join caches refresh on next read. This is the **eventually-consistent** read-side propagation that makes the single-writer pattern viable at production latency.

---

## The five canonical Agent Framework patterns × cross-service reads

The Agent Framework loader's `resolve_tool_for_role` (apex-m/src/apex_m/agent_framework_loader.py) maps `rc_e2e_09.*` tool names to the `rc_e2e_09_mcp` Python package. This means:

- RC-E2E-03's classify (Magentic worker) can call `rc_e2e_09.get_lot_provenance` for FSMA-204 conformance — same loader code path as in-service tools.
- RC-E2E-07's assess (Concurrent sibling) can call `rc_e2e_09.get_lot_provenance` for refund-fraud-by-recall investigation.
- The cross-service call appears in Decide's audit row chain via `tools_called` field per Roadmap.md BL.P.86 (lineage capture: SOR → Bronze → Silver → Gold → MCP → **CROSS-SERVICE MCP** → Agent → Audit row).

---

## Pattern for adding a new shared schema

When a new RC service ships and proposes to write a previously single-writer schema:

1. **Default position: don't.** Two writers is almost always wrong.
2. **If a strong case exists** (e.g., RC-E2E-12 ships and legitimately writes `SCML.Inventory` as part of a DC-receiving-event flow), update this doc with the new owner row + cross-service read tool name.
3. **The MCP contract gets updated** — write tool's `required_scopes` lists every authorised service.
4. **Manifest tests get updated** — each consuming service's manifest test verifies its agent.yaml `schemas_write` references the schema *only* if it's authorised here.
5. **Pre-deployment Security Gate (PSG-12) catches the rest** at deploy time.

---

## Sprint mapping

| Sprint | Boundary work |
|---|---|
| Sprint 32 | RC-E2E-03 declared sole writer of `MERML.Markdown` + `MERML.Elasticity` + `MERML.Competitor` + `PROML.Pricing` + `PROML.DiscountRule` |
| Sprint 34 | RC-E2E-04 declared sole writer of `CXML.Loyalty` + `CXML.Campaign` |
| Sprint 35 | RC-E2E-05 declared sole writer of `CXML.AssociateTask` |
| Sprint 37 | RC-E2E-07 declared sole writer of `CXML.FraudCase` |
| **Sprint 39** | **RC-E2E-09 declared sole writer of `SCML.Lot` (the canonical FSMA-204 surface)** |
| Sprint 40 | W3 Fusion verifies cross-service reads work end-to-end across the Perishables Economics Mesh (cold-chain × loyalty-churn × lot provenance) |
| Sprint 46 | Wizard adds PSG-12 lint (manifest-cross-write detection) at deploy time |

This document is the canonical reference for that lattice.
