# APEX Developer Implementation Guide — Design

**Date:** 2026-04-18
**Status:** Approved — ready for implementation plan
**Author:** APEX Core team
**Supersedes:** N/A (new artifact)
**Related:** `2026-04-17-rc-agent-catalog-design.md`, `2026-04-17-schema-versioning-manifest-design.md`

---

## 1. Purpose

Produce a **Developer Implementation Guide** for APEX that lets a mixed audience (execs, architects, developers) understand how to build and operate APEX on Microsoft Fabric SaaS. The guide must:

1. Explain how the APEX framework layers on top of Fabric SaaS.
2. Show how to build the Medallion (Bronze / Silver / Gold) layers that integrate Systems of Record (SORs) into APEX canonical schemas.
3. Provide a deep dive into MCP servers and the tooling that supports agentic agents in APEX.
4. Fill in supporting gaps for developer understanding: agent & orchestration lifecycle, HITL/decision-gate wiring, observability & security, testing strategy, and environment/tenancy topology.
5. Define a **Service Catalog** layer — scenarios + targeted solutions + target personas + KPIs, delivered as subscribable services.
6. **Rename the L3 layer** from "Fleet" to **"Practice"** across APEX Core to better represent what L3 actually bundles (agents, schemas, MCP tools, orchestrations, gates, services, personas, KPIs).

## 2. Audience

**Mixed** — the doc set is layered so each audience finds its level:

- **Executives** — spine TL;DR and service-first view give the commercial shape.
- **Architects** — spine architecture sections and companion TL;DRs.
- **Senior / mid-level developers** — companion deep-dives with worked code examples.
- **Commercial / client account teams** — Service Catalog companion for subscription conversations.

## 3. Non-goals

- Not a replacement for `apex-core-build-spec.md` — that remains the normative core specification.
- Not a tutorial walking a first-time-APEX developer through a linear hands-on build — this is a reference + architecture guide.
- Not a sales deck — commercial model placeholders are included but pricing is out of scope.

## 4. Doc set architecture

The guide is delivered as a **spine + six companion deep-dives + one service catalog companion**. Each Markdown source file is rendered to Word via the existing `build-docx.cjs` pipeline.

### 4.1 File layout

```
docs/
├── APEX-developer-guide.md                       ← SPINE (source)
├── APEX-developer-guide.docx                     ← rendered
├── dev-guide/
│   ├── 01-fabric-layering.md        → .docx
│   ├── 02-medallion-sor.md          → .docx
│   ├── 03-mcp-servers.md            → .docx
│   ├── 04-agent-lifecycle.md        → .docx
│   ├── 05-observability-security.md → .docx
│   ├── 06-testing-topology.md       → .docx
│   └── 07-service-catalog.md        → .docx
└── plans/
    └── 2026-04-18-developer-implementation-guide-design.md    ← THIS DOC
```

### 4.2 Consistent companion structure

Every companion opens with a one-page TL;DR (for drop-in architects) and then proceeds through: concepts → worked code (Python + C# side-by-side) → worked example → ops / runbook. Cross-references point back to the spine glossary so every term is defined exactly once.

### 4.3 Versioning & CHANGELOG

All files carry a header: `APEX Core v1.2 · Developer Guide v1.0 · 2026-04-18`. A single CHANGELOG entry covers the whole doc set plus the L3 rename.

### 4.4 Diagrams

- **Mermaid** for architecture and flow diagrams (renders natively on GitHub; converts to Word via mermaid-cli pre-pass in `build-docx.cjs`).
- **Tables** for config matrices, SOR-to-service mappings, KPI libraries, persona catalogs.

## 5. Spine content outline (`APEX-developer-guide.md`)

Target: **18–22 pages**. The spine is what execs and architects read end-to-end.

```
1. Executive TL;DR                                      1–2 pp
   — What APEX is; what this guide delivers
   — Single 60-second architecture diagram
   — Who reads which companion

2. How APEX layers on Fabric SaaS                       3–4 pp
   — Fabric as the data plane; APEX as the intelligence layer
   — Component map: OneLake · Lakehouse · Warehouse · Eventstream ·
     Data Pipelines · Notebooks · Azure AI Foundry ·
     Azure AI Agent Service · Logic Apps · Durable Functions ·
     Copilot Studio · Teams
   — Where each APEX concept lives (manifests, schemas, agents,
     orchestrations, gates, services)
   — Tenant topology: L3 Practice workspace → L4 tenant workspace binding
   — Mermaid: annotated end-to-end architecture

3. Developer mental model                               2–3 pp
   — The four lifecycle layers (L1 Contract → L2 Edition →
     L3 Practice → L4 Tenant)
   — The five lanes (schema · agent · orchestration · gate · service)
   — The "what-changed?" question — heart of APEX dev work
   — SemVer bump → HITL gate mapping

4. Repository & workspace layout                        2–3 pp
   — apex-core vs apex-<practice> vs client-tenant repos
   — Fabric workspace naming convention
   — Manifest file conventions (schema-manifest.json,
     practice-manifest.json, service-manifest.json, tenant-manifest.json)
   — Where custom code lives (agents, MCP tools, notebooks, pipelines)

5. The 7-step developer workflow                        2 pp
   — Read contract → author/modify schema → implement Medallion transforms
     → wire agent + MCP tool → declare orchestration → bind HITL gate
     → classify bump → ship
   — Each step: one-line pointer to which companion contains the detail

6. Service-first view                                   1–2 pp
   — Mapping the 7-step workflow to "which service am I building / modifying?"
   — Impact analysis: a schema change ripples to N services
   — When to create a new service vs extend an existing one

7. Guide to the companions                              1–2 pp
   — Table: which companion to open when; skill level required;
     typical dev tasks it answers

8. Glossary                                             2–3 pp
   — APEX terms, Fabric terms, MCP terms, MS-native orchestration terms,
     all defined once so companions hyperlink back
```

## 6. Companion content outlines

### 6.1 Companion 01 — Fabric Layering (`dev-guide/01-fabric-layering.md`)

```
1. TL;DR — APEX's relationship to Fabric in one page
2. The Fabric surface area APEX uses
   — OneLake · Lakehouse · Warehouse · Eventstream · Pipelines ·
     Notebooks · SQL endpoint
3. Workspace topology
   — Dev/Test/Prod workspaces
   — L3 Practice workspace (shared reference data, canonical schemas)
   — L4 Tenant workspaces (client-specific instances)
   — Naming conventions, lineage, Fabric Git integration
4. APEX on top of Fabric
   — Where manifests live (workspace item → lakehouse table)
   — Where agents run (Azure AI Agent Service — not Fabric itself)
   — Where orchestrations run (Logic Apps / Durable Functions)
   — Where gates resolve (Teams / Power Platform Approvals)
   — The data pathway: Eventstream → Bronze → Silver → Gold → agents
5. Identity & access
   — Fabric workspace roles; service principals for APEX runtime
   — OneLake path-level ACLs for PII segregation
6. Fabric-specific gotchas
   — Shortcut vs copy; mirrored databases; capacity sizing for agent workloads
7. Worked example: stand up a new L4 tenant workspace
   — Scripted Fabric workspace creation
   — Shortcut to L3 Practice canonical schema tables
   — Binding the tenant manifest
```

### 6.2 Companion 02 — Medallion + SOR Integration (`dev-guide/02-medallion-sor.md`)

```
1. TL;DR — Why APEX mandates canonical Silver schemas
2. The three-layer pattern in APEX terms
   — Bronze: landed SOR data, SOR-shape, no transforms
   — Silver: canonical schema (SCML / MERML / CXML / HLS / ER / AXLE
     equivalents), PII tokenised
   — Gold: feature views agents read; materialised for agent-latency SLOs
3. Ingestion patterns
   — Event stream (Monnit IoT, POS, Epic ADT): Eventstream → Bronze delta
   — Batch (Manhattan WMS nightly, SAP ISU, Plex MES): Pipeline → Bronze
   — REST pull (Coupa, ServiceNow): Dataflow Gen2 → Bronze
   — Change-data-capture (Epic EHR): Mirrored Database → Bronze
4. Silver canonicalisation — the contract
   — Schema-driven (the manifest is law)
   — PII tokenisation at the Silver boundary (Purview + Fabric native masking)
   — SCD2 for slowly-changing dimensions
   — The five universals: event_id · event_ts · entity_id · source_system ·
     source_system_ts
5. Gold feature views
   — Materialised views for agent reads
   — Latency budgets: p95 agent-read must be < contract SLO (default 500ms)
   — Cache warmth and refresh cadence
6. Worked examples — multi-industry composite
   — RC Practice: Manhattan WMS → MERML.STORE_INVENTORY_POSITION
     (batch → Bronze → Silver SCD2 → Gold feature view)
   — HLS Practice: Epic EHR → HLSCML.PATIENT_ENCOUNTER
     (CDC via mirrored DB → Bronze → Silver with PHI tokenisation)
   — ER Practice: SAP ISU → ERCML.METER_READING (batch → Bronze → Silver)
   — AXLE Practice: Plex MES → AXLECML.PRODUCTION_EVENT (eventstream)
   — Each shows Bronze DDL, Silver transform notebook (PySpark), and
     Gold view (T-SQL) side-by-side
7. Schema evolution & bump classification
   — How to know your schema change is MAJOR / MINOR / PATCH
   — Running `apex-validate` + `classify-bump` in CI
   — Migration patterns (additive, backfill, breaking)
8. SOR-to-Service matrix
   — Table: which services depend on which SOR connections
   — Blast-radius rules when a SOR connector changes
```

### 6.3 Companion 03 — MCP Servers & Tooling (`dev-guide/03-mcp-servers.md`)

```
1. TL;DR — MCP as the agent's tool contract; why APEX uses it
2. MCP in one picture
   — Client (agent) ↔ Server (tool provider) protocol
   — stdio vs SSE vs streamable-HTTP transports
   — Tools, resources, prompts — the three MCP primitives
3. APEX's MCP server taxonomy
   — Domain servers (one per APEX schema family:
     SCML-MCP, MERML-MCP, CXML-MCP, HLSCML-MCP, ERCML-MCP, AXLECML-MCP)
   — Utility servers (policy-MCP for HITL, telemetry-MCP for trace events,
     approvals-MCP for Teams integration)
   — Fabric-MCP (reads Silver/Gold via OneLake SQL endpoint)
   — External-MCP examples (FDA recall feed, vendor portal, EDI gateway)
4. Writing an MCP server
   — Project skeleton in Python (FastMCP) and C# (.NET MCP SDK), side-by-side
   — Declaring tools (schema-typed input/output)
   — Declaring resources (streamable content)
   — Error model and client retry semantics
   — Code example: `fetch_cold_chain_telemetry(since, store_id)` end-to-end
5. Auth & security for MCP servers
   — Managed identity for Fabric data access
   — Entra ID app registration; token audience
   — Per-tenant scoping (tenant manifest determines what data is visible)
6. Hosting & deployment
   — Azure Container Apps vs Azure Functions vs App Service for MCP servers
   — Scaling, cold start, SLO considerations
   — Local dev: MCP Inspector, stdio wrappers, VS Code debug
7. Integration with Azure AI Agent Service
   — How an agent discovers & calls MCP tools
   — Tool catalogs, allow-lists, rate limits
   — Observability: every tool call emits a trace span
8. Worked example — build a new MCP tool end-to-end
   — Author the tool in Python + C#
   — Wire to a canonical Silver table
   — Register with Agent Service
   — Test with MCP Inspector
   — Invoke from a live agent session
```

### 6.4 Companion 04 — Agent & Orchestration Lifecycle + HITL (`dev-guide/04-agent-lifecycle.md`)

```
1. TL;DR — From local agent dev to a production canary release
2. Anatomy of an APEX agent
   — Agent manifest (id, name, schemas, MCP tools, orchestration role, HITL gate)
   — System-prompt conventions; the "contract preamble"
   — Tool allow-list; model selection (gpt-4 vs o-series reasoning)
3. Local authoring loop
   — Azure AI Foundry playground vs code-first authoring
   — Seed fixtures (replay real events against a candidate agent)
   — Prompt-engineering discipline: every change carries a diff test
4. Versioning an agent
   — Agent manifest SemVer; cascade from schema bumps
   — When an agent change is MAJOR (rewrote reasoning) vs
     MINOR (new tool) vs PATCH (prompt tweak)
5. Orchestration authoring
   — The DAG: sub-agents, sequence, fan-out, error handling
   — Logic Apps for declarative DAGs
   — Durable Functions for stateful long-runners
   — Code example: ORCH-03 (Cold Chain) — Logic Apps definition
     and Durable Function side-by-side
6. HITL gate wiring
   — SemVer-bump → gate kind (HITL / ACK_ONLY / ZERO_TOUCH / ESCALATION)
   — Teams approval card template
   — Power Platform approval flow
   — Timeout → escalation path
   — Decision audit log (dedicated Silver table)
7. Deployment
   — Dev → Test → Prod via Fabric Git + Azure DevOps
   — Canary: new agent version takes 5% of traffic for 72 h
   — Rollback: manifest-level rollback; L4 tenant pins prior versions
8. CI/CD patterns
   — Pre-commit: apex-validate + classify-bump
   — PR gate: schema contract tests
   — Release: bundler packages the Practice release
9. Service impact
   — When you modify an agent, which services ship it
   — Cross-reference to Service Catalog
```

### 6.5 Companion 05 — Observability & Security (`dev-guide/05-observability-security.md`)

```
1. TL;DR — How you know an APEX deployment is healthy & safe
2. Telemetry model
   — Every agent invocation = one trace (App Insights operation_Id)
   — DAG step timings, MCP tool call spans, HITL-gate wait time
   — Decision audit log (who approved, when, with what context)
   — Gold-layer query log (what data did the agent read)
3. Dashboards
   — Azure Monitor workbook template for an APEX deployment
   — KPIs: orchestration success rate, mean-time-to-decision,
     HITL queue depth, schema drift incidents, MCP tool failure rate
4. Alerting
   — Contract-violation alerts (manifest drift)
   — SLO burn-rate alerts (Gold read latency, agent response time)
   — Decision-backlog alerts (HITL queue > threshold)
5. Identity model
   — Entra ID for user identity
   — Managed identity for service-to-service (Agent Service → Fabric)
   — Service principals for CI/CD
   — Per-tenant identity segregation (L4 tenant has its own SP)
6. PII & data protection
   — Tokenisation at Silver boundary (Fabric native masking + Purview labels)
   — The "consent-gated" field convention
   — Purview DLP for outbound agent responses
   — Right-to-erasure pattern: re-tokenise + replay
7. Compliance posture
   — HIPAA for HLS Practice; SOX for ER Practice; PCI for RC Practice
   — Audit log retention, immutability, customer-managed keys
   — Independence (Deloitte) compliance notes
```

### 6.6 Companion 06 — Testing & Environment Topology (`dev-guide/06-testing-topology.md`)

```
1. TL;DR — The APEX test pyramid and the workspace topology that enables it
2. Test pyramid for APEX artifacts
   — Unit: schema validators, MCP tool pure functions, orch step logic
   — Contract: manifest round-trip; schema bump classification;
     inter-Practice compatibility
   — Integration: Medallion transforms against fixture SORs;
     agent + MCP in a local harness
   — End-to-end: full orchestration in a dev workspace with seed events
   — Synthetic-load: shift-replay (Store 100's 9-hour day in 5 minutes)
3. Fixtures & mocks
   — The apex-core/fixtures/ convention
   — Recording real SOR payloads; anonymisation pipeline
   — MCP-server mocks for agent tests
4. Environment topology
   — Dev: personal branch workspaces, scratch lakehouse, local MCP stdio
   — Test: shared integration workspace, Practice manifest pinned,
     synthetic data
   — Prod: per-tenant L4 workspace, real SORs, all gates enforced
5. L3 Practice → L4 Tenant binding
   — How a tenant pins a specific Practice release
   — How a tenant can diverge (tenant-scoped overrides) without forking
   — Drift detection and reconciliation
6. Cost allocation & capacity
   — Fabric capacity SKUs sized for agent workloads
   — Per-tenant cost tags; chargeback model
   — Agent-invocation cost envelope (token spend × HITL analyst time)
7. Runbook samples
   — "Deploy a new agent version to one tenant"
   — "Re-bake Gold views after schema MINOR bump"
   — "Rollback a failed orchestration change"
```

### 6.7 Companion 07 — Service Catalog (`dev-guide/07-service-catalog.md`) — NEW

```
1. TL;DR — APEX as subscribable services, not just a framework
2. Service taxonomy & naming
   — ID convention: APEX-<practice>-<domain>-<nn>
   — Tiers: Essentials / Pro / Enterprise
   — Lifecycle states: Preview / GA / Deprecated
3. How services map to the technical framework
   — One service = one bundle of manifests + schemas + agents +
     MCP tools + orchestrations + gates
   — Version-pinning: subscribing pins a specific Practice release
   — Service-manifest schema (new first-class APEX artifact)
4. Personas & KPI model
   — Master persona catalog (Store MOD, Regional Director,
     Clinical Nurse, Revenue Analyst, Plant Supervisor, etc.)
   — KPI library — outcome metrics APEX services measure against
   — SLO model (detection / decision / accuracy / availability)
5. The service catalog (the meat) — full 24-service catalog
   — RC Practice (~8 services):
     · APEX-RC-CXP-01  Cold Chain Excursion Response
     · APEX-RC-RVD-02  Receiving Variance Dispute
     · APEX-RC-ESL-03  ESL Pricing Integrity
     · APEX-RC-OSA-04  Phantom-OOS Detection
     · APEX-RC-RCL-05  Recall Response
     · APEX-RC-BPX-06  BOPIS Exception Handling
     · APEX-RC-SHK-07  Shrink & Void Anomaly
     · APEX-RC-CXI-08  Customer Incident Triage
   — HLS Practice (~6 services):
     · APEX-HLS-DSR-01 Discharge Ready Surveillance
     · APEX-HLS-SEP-02 Sepsis Early Warning
     · APEX-HLS-RVC-03 Revenue-Cycle Denial Recovery
     · APEX-HLS-SUP-04 Supply Expiry Management
     · APEX-HLS-CTM-05 Clinical Trial Matching
     · APEX-HLS-PSI-06 Patient Safety Incident
   — ER Practice (~5 services):
     · APEX-ER-MTR-01  Meter Outage Detection
     · APEX-ER-GRD-02  Grid Anomaly Response
     · APEX-ER-BIL-03  Billing Exception Handling
     · APEX-ER-FWO-04  Field Work-Order Optimisation
     · APEX-ER-REG-05  Regulatory Event Response
   — AXLE Practice (~5 services):
     · APEX-AXLE-LDT-01 Line-Down Triage
     · APEX-AXLE-QEX-02 Quality Excursion Response
     · APEX-AXLE-SCD-03 Supply-Chain Disruption
     · APEX-AXLE-RCL-04 Recall Traceability
     · APEX-AXLE-KPI-05 Plant KPI Drift
   — Each entry populated using the standard service template
6. Composition & bundles
   — Pre-built bundles: "Store Operations Essentials", "Cold Chain + Compliance",
     "Plant-Floor Pro"
   — Custom compositions (client mixes & matches)
7. Subscription lifecycle
   — How a client subscribes: pick services → pin Practice release →
     provision L4 tenant workspace → connect SORs → go live
   — Version upgrades: behaviour of active decisions during a MAJOR bump
   — Decommissioning: data retention, audit-log export
8. Commercial model placeholders
   — Per-entity-year base + per-invocation usage (pattern only)
   — Support tiers (Essentials / Pro / Enterprise)
   — SLA credit model
9. Worked example: subscribing to "Cold Chain + Receiving Variance"
   — Target persona: Store MOD + Regional Director
   — What gets provisioned in the L4 tenant
   — How KPIs surface in the customer dashboard
   — First 30 days playbook
```

## 7. Service template (each catalog entry)

```
Service ID:        APEX-<practice>-<domain>-<nn>
Service Name:      <name>
Tier:              [Essentials | Pro | Enterprise]
Practice:          <RC | HLS | ER | AXLE>
Status:            [Preview | GA | Deprecated] vX.Y

SCENARIO
  Trigger:         <business event>
  Business pain:   <pain narrative>
  Cadence:         <continuous | episodic | nightly>

PERSONAS
  Primary:         <persona id(s)>
  Secondary:       <persona id(s)>
  Consumer:        <persona id(s) or "none">

KPIs & SLOs
  Outcome KPIs:    <kpi id> (target, direction) — repeated
  Service SLOs:    detection_p95 · decision_p95 · accuracy · availability
  False-positive target: ≤ X%

INCLUDED ARTIFACTS
  Schemas:         <schema id(s)>
  Agents:          <agent id(s)>
  MCP Tools:       <tool id(s)>
  Orchestration:   <ORCH id>
  HITL Gate:       <HITL | ACK_ONLY | ZERO_TOUCH | ESCALATION>

PREREQUISITES
  Practice min ver: <x.y.z>
  SOR connections:  <sor id(s)>
  Fabric capacity:  <SKU>
  Identity group:   <AAD group>

COMMERCIAL
  Subscription:     <model>
  Onboarding days:  <n>
  Support tier:     <tier list>
```

## 8. L3 terminology rename: Fleet → Practice

The L3 layer is renamed from **"Fleet"** to **"Practice"** because L3 bundles more than agents (schemas, MCP tools, orchestrations, gates, services, personas, KPIs). "Practice" is Deloitte-native language, captures the full scope, and reads commercially as a subscribable capability.

### 8.1 Rename cascade

| Before | After |
|---|---|
| RC / HLS / ER / AXLE Fleet | RC / HLS / ER / AXLE Practice |
| `apex-fleet/` directory | `apex-practice/` |
| `fleet-manifest.json` | `practice-manifest.json` |
| `fleet-manifest-contract.json` | `practice-manifest-contract.json` |
| `validate-fleet.js` + `.test.js` | `validate-practice.js` + `.test.js` |
| L3 Fleet layer | L3 Practice layer |
| "Fleet release" / "Fleet version" | "Practice release" / "Practice version" |

Service IDs remain unchanged (`APEX-RC-CXP-01`) — the practice abbreviation is the `RC` segment.

### 8.2 Scope of the rename

Touched files (~20 files):

- `apex-core-*.md` build specs and amendments (4 files)
- `apex-<practice>-build-spec*.md` for RC, HLS, ER, AXLE, TMT, TH, ICE (7 files)
- `apex-fleet/` directory (rename)
- `apex-core/conventions/schema-versioning.md`
- Existing docs: Solution Overview, Agent Catalog, Facilitator Guide, Stack Chart
- `README.md`
- `CHANGELOG.md` (new entry)

## 9. New APEX Core code artifacts

```
apex-core/
├── data/
│   ├── schema-manifest-contract.json              (existing)
│   ├── practice-manifest-contract.json            NEW — renamed from fleet-manifest-contract
│   ├── service-manifest-contract.json             NEW — formal service SKU contract
│   └── persona-catalog.json                       NEW — master persona list
├── fixtures/
│   └── services/                                  NEW
│       ├── apex-rc-cxp-01.json                    ~24 service manifest fixtures
│       ├── apex-rc-rvd-02.json
│       ├── … (22 more)
│       ├── apex-hls-dsr-01.json
│       └── apex-axle-ldt-01.json
└── tools/
    ├── validate-practice.js                       RENAMED from validate-fleet.js
    ├── validate-practice.test.js                  RENAMED + updated tests
    ├── validate-service-manifest.js               NEW
    ├── validate-service-manifest.test.js          NEW
    └── apex-validate.js                           UPDATED — invokes new validators
```

### 9.1 `service-manifest-contract.json` — key fields

```json
{
  "service_id":       "string (pattern: APEX-<practice>-<domain>-<nn>)",
  "service_name":     "string",
  "practice":         "RC | HLS | ER | AXLE | TMT | TH | ICE",
  "version":          "semver",
  "lifecycle":        "Preview | GA | Deprecated",
  "tier":             ["Essentials", "Pro", "Enterprise"],
  "scenario": {
    "trigger":        "string",
    "business_pain":  "string",
    "cadence":        "continuous | episodic | nightly | on-demand"
  },
  "personas": {
    "primary":        ["persona_id"],
    "secondary":      ["persona_id"],
    "consumer":       ["persona_id"]
  },
  "kpis": [
    { "id": "string", "target": "number", "direction": "maximize|minimize" }
  ],
  "slos": {
    "detection_p95_sec":    "number",
    "decision_p95_min":     "number",
    "false_positive_rate":  "number 0..1",
    "availability_pct":     "number 0..100"
  },
  "artifacts": {
    "schemas":        ["schema_id"],
    "agents":         ["agent_id"],
    "mcp_tools":      ["tool_id"],
    "orchestration":  "ORCH-id",
    "hitl_gate":      "HITL | ACK_ONLY | ZERO_TOUCH | ESCALATION"
  },
  "prerequisites": {
    "practice_min_version": "semver",
    "sor_connections":      ["sor_id"],
    "fabric_capacity":      "F-SKU",
    "identity_group":       "AAD group id"
  },
  "commercial": {
    "subscription_model": "string (pattern)",
    "support_tiers":      ["Essentials","Pro","Enterprise"],
    "onboarding_days":    "number"
  }
}
```

### 9.2 Validation rules (what `validate-service-manifest.js` checks)

- `service_id` matches `APEX-<practice>-<domain>-<nn>` and is unique across catalog.
- All referenced `schemas`, `agents`, `mcp_tools`, `orchestration`, `hitl_gate` exist in the practice at the pinned `practice_min_version`.
- All `personas` exist in `persona-catalog.json`.
- `kpis[].id` exists in the KPI library.
- `slos` are numeric and ordered sanely (detection_p95 < decision_p95).
- Tier combinations are valid.
- Cross-manifest compatibility: schemas and agents satisfy each other's version constraints.

## 10. Build tooling additions

- **`build-service-catalog.cjs`** — renders `07-service-catalog.md` by iterating `apex-core/fixtures/services/*.json` through the service-entry template so the catalog doc stays in sync with manifests automatically.
- Existing **`build-docx.cjs`** extended to render all eight guide files (spine + 7 companions) in one run.
- Mermaid pre-processor added to `build-docx.cjs` so embedded Mermaid diagrams convert to PNG for Word output.

## 11. Deliverable summary

| Artifact | Count |
|---|---|
| Markdown guide files (spine + 7 companions) | 8 |
| Rendered Word docs (one per .md) | 8 |
| New JSON contracts (practice-manifest, service-manifest) | 2 |
| New catalog data files (persona-catalog, KPI library) | 2 |
| Service manifest fixtures | 24 |
| New validator modules (+ tests) | 2 |
| Renamed validator module | 1 |
| New build script | 1 |
| Rebrand commit touching existing files | ~20 files |
| CHANGELOG entries | 1 (covers rename + Dev Guide v1.0) |

## 12. Risks & mitigations

| Risk | Mitigation |
|---|---|
| Rename of "fleet" breaks scripts or scripts held by clients | Single-commit rename with CHANGELOG warning; keep a deprecation shim for one Core edition (Core v1.2.x exports both `validate-fleet` and `validate-practice` so downstream CI doesn't break immediately) |
| Service catalog drifts from reality | Catalog is generated from fixtures by `build-service-catalog.cjs`; fixtures are validated by `apex-validate` in CI |
| 24 services is a lot to author | Author in priority order: RC 8 first (matches Store 100 demo), then HLS, ER, AXLE. Design plan sequences this |
| Multi-language code tabs double doc size | Use concise examples (20–40 lines each); focus on *contract* not *implementation* where possible |
| Fabric changes feature surface during authoring | Pin to Fabric GA feature set as of 2026-04; note Preview features in a dedicated callout style |

## 13. Out of scope (tracked for future work)

- Service pricing and discounting logic.
- Billing-metering pipeline (the hook points are referenced in commercial model; implementation is separate).
- A machine-readable KPI library schema (this design uses a simple JSON dictionary).
- Customer-facing service-catalog portal (consumption of `service-manifest.json` by a portal is future work).

## 14. Approval

Design approved 2026-04-18. Ready to transition to `writing-plans` skill to produce the detailed implementation plan at `docs/plans/2026-04-18-developer-implementation-guide-implementation.md`.
