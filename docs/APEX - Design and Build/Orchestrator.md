# APEX Orchestrator — Sprint Plan

**Source:** `Roadmap.md` (backlog items BL.P.01 – BL.P.195) + `backlog/APEX-v0.2-F-01-Redis-Cache-Layer.md` + `docs/APEX - Design and Build/APEX-v0.2-Build-Instructions.md` + `APEX-Stacked-Architecture-Narrated.html` (Sprint 27 completed)
**Design reference:** `APEX_Design.md` (v1.2), `Industry-Standards-Incorporation-Plan.md`, [ADR-006](adr/ADR-006-agent-orchestrator-canonical.md), [Services Guide §14.5](../book/Professional-APEX-M-Services-Guide.html#ch-14-5)
**Date:** 2026-05-09 (v4 — Microsoft Agent Framework alignment for APEX-M; Sprints 30–49 added)
**Purpose:** Break the planned backlog into executable sprints, tasks, and subtasks. Each sprint references the BL items it closes. Sprints are sized for ~2-week delivery windows unless otherwise noted.

> **2026-05-09 — Microsoft Agent Framework alignment for APEX-M.** Per [ADR-006](adr/ADR-006-agent-orchestrator-canonical.md), Microsoft Agent Framework is the canonical agent orchestrator for APEX-M on every substrate (laptop / dev / stage / prod). The 47 APEX archetypes reconcile to the 5 canonical Microsoft Agent Framework patterns (Sequential / Concurrent / Handoff / Group Chat / Magentic). Semantic Kernel is now legacy — existing SK code stays valid; new code uses Agent Framework. n8n keeps its place as the laptop *workflow* runtime; it does not orchestrate agents (anti-pattern callout in [Services Guide §14.5.4](../book/Professional-APEX-M-Services-Guide.html#ch-14-5-4)). See [Sprint Execution Order](Sprint-Execution-Order.md) for the post-Sprint-29 dependency graph and [Sprint Plan](Sprint-Plan.md) for the full schedule including the new Sprints 30–49.

**Conventions:**
- Each **Task** is a coherent deliverable, typically 1–5 days of work.
- Each **Subtask** is a checkbox unit-of-work, typically hours to ~1 day.
- **Exit criteria** at the sprint level are the acceptance bar before moving on.

---

## Sprint Index

| # | Sprint | Duration | BL Items Closed |
|---|--------|----------|-----------------|
| 1 | L1 Manifest Contract Hardening | 2 wks | BL.P.01–07 |
| 2 | Canonical Schemas — RC Anchor | 3 wks | BL.P.08–10 |
| 3 | Canonical Schemas — Other Practices | 4 wks | BL.P.11–19 |
| 4 | Medallion Bronze Landing | 2 wks | BL.P.20–25 |
| 5 | Silver Transform & Tokenization | 2 wks | BL.P.26–28, P.34 |
| 6 | Gold Serving & Measures | 2 wks | BL.P.29–33 |
| 7 | Utility MCP Servers | 2 wks | BL.P.41–45, P.51–52 |
| 8 | Domain MCP Servers | 2 wks | BL.P.35–40 |
| 9 | External MCP Servers | 1 wk | BL.P.46–50 |
| 10 | Identity & Visibility Lattice | 2 wks | BL.P.53–57 |
| 11 | Orchestration & HITL Runtime | 3 wks | BL.P.65–76 |
| 12 | Decision Audit Row | 2 wks | BL.P.77–84 |
| 13 | Purview Trust Architecture | 2 wks | BL.P.85–90 |
| 14 | Fabric Capacity & Provisioning | 1 wk | BL.P.91–94 |
| 15 | SOR Integration Adapters | 3 wks | BL.P.95–109 |
| 16 | Agent Catalogs per Practice | 4 wks | BL.P.58–64 |
| 17 | Service Catalogs per Practice | 3 wks | BL.P.110–116 |
| 18 | Reference Deployments | 4 wks | BL.P.117–121 |
| 19 | Registries, Playbooks & Appendices | 2 wks | BL.P.122–133 |
| 20 | Industry Standards — Registry & CLI Foundation | 2 wks (partially complete) | BL.P.134–138 |
| 21 | Per-Standard Packages (FHIR · CIM · ISA-95 · SID · OpenTravel · CDISC · ISO 14224 · J1939) | 3 wks (Phase 1 complete) | BL.P.139–146 |
| 22 | Identifier & Terminology Bindings | 2 wks (mostly complete) | BL.P.147–154 |
| 23 | Message-Format Translators (EDI X12 · HL7 v2 · CDA · EPCIS · OAGIS · IATA PADIS) | 3 wks | BL.P.155–160 |
| 24 | Cross-Standard Translators | 2 wks | BL.P.161–165 |
| 25 | Protocol Adapters (OPC UA · IEC 61850 · SAE J1939) | 2 wks | BL.P.166–168 |
| 26 | APEX v0.2 Control Plane — Redis + OpenClaw File-First Pattern | 3 wks | APEX-v0.2-F-01 + WS3 + WS4 |
| 27 | **Scenario Library, Wave Ribbon & Design System ✅** | 2 wks (complete) | BL.C.30a–e, BL.C.42a–m |
| 28 | Scenario Library Extensions (W1 Foundation + W3 Fusion + tooling) | 4 wks | BL.P.169–185 |
| 29 | Communication Artifacts & Compliance Pipeline | 3 wks | BL.P.186–195 |

**Total planned duration:** ~70 weeks (~17 months) for the full Roadmap + v0.2 build + Sprint 27–29, assuming parallelizable sprints and multi-track execution. Sprint 27 is already complete (delivered in the Stacked Architecture Narrated HTML and the APEX-Sellers-Guide-Runtime-Addendum artifacts).

---

## Sprint 1 — L1 Manifest Contract Hardening

**Closes:** BL.P.01, BL.P.02, BL.P.03, BL.P.04, BL.P.05, BL.P.06, BL.P.07
**Goal:** Round out `apex-core` with the six remaining manifest schemas (event, orchestration, agent, tenant, policy, service) plus enforce the canonical envelope. This unblocks every L3 Practice that needs to author manifests against the L1 contract.
**Exit criteria:** All six manifest schemas pass CI validation, `classify-bump` correctly tags PATCH/MINOR/MAJOR across them, fixtures cover each bump class.

### Task 1.1 — Event manifest (BL.P.01)
- [ ] Subtask 1.1.1 — Draft `event-manifest.schema.json` covering trigger, payload shape, classification
- [ ] Subtask 1.1.2 — Author `validate-event-manifest.js` tool in `apex-core/tools`
- [ ] Subtask 1.1.3 — Add fixtures for valid, MINOR-bump, MAJOR-bump cases
- [ ] Subtask 1.1.4 — Wire into `classify-bump` bump-rule table
- [ ] Subtask 1.1.5 — Document in `apex-core/conventions/event-manifest.md`

### Task 1.2 — Orchestration manifest (BL.P.02)
- [ ] Subtask 1.2.1 — Draft schema covering agent list, sequence/parallel/hierarchy, HITL gate placement, version-stamp fields
- [ ] Subtask 1.2.2 — Author `validate-orchestration-manifest.js`
- [ ] Subtask 1.2.3 — Fixtures for sequential, parallel, hierarchical, feedback-loop shapes
- [ ] Subtask 1.2.4 — Document `orchestration-manifest.md` conventions
- [ ] Subtask 1.2.5 — Integration test: orchestration manifest → classify-bump → report

### Task 1.3 — Agent manifest (BL.P.03)
- [ ] Subtask 1.3.1 — Draft schema: model pin, system prompt SHA, tool allow-list, scope, persona binding
- [ ] Subtask 1.3.2 — Validator + bump-rule integration
- [ ] Subtask 1.3.3 — Fixtures covering prompt-version bump and tool-allowlist change
- [ ] Subtask 1.3.4 — Document `agent-manifest.md`

### Task 1.4 — Tenant manifest (BL.P.04)
- [ ] Subtask 1.4.1 — Draft schema: Practice pin, service subscriptions, extensions, policy overrides
- [ ] Subtask 1.4.2 — Validator + L3-compatibility checker
- [ ] Subtask 1.4.3 — Fixtures for extension overlay, gate override, service unsubscribe
- [ ] Subtask 1.4.4 — Document `tenant-manifest.md`

### Task 1.5 — Policy manifest (BL.P.05)
- [ ] Subtask 1.5.1 — Draft schema for HITL gate rules, DLP policies, classification mappings
- [ ] Subtask 1.5.2 — Validator + policy-version-SHA stamper
- [ ] Subtask 1.5.3 — Fixtures for each of 4 gate kinds + 4 variants
- [ ] Subtask 1.5.4 — Document `policy-manifest.md`

### Task 1.6 — Service manifest (BL.P.06)
- [ ] Subtask 1.6.1 — Draft schema: persona, KPI references, SLO, commercial terms
- [ ] Subtask 1.6.2 — Validator
- [ ] Subtask 1.6.3 — Fixtures modeled on Cold Chain Response (RC-E2E-06)
- [ ] Subtask 1.6.4 — Document `service-manifest.md`

### Task 1.7 — Canonical envelope enforcement (BL.P.07)
- [ ] Subtask 1.7.1 — Define the five-field envelope in `apex-core/data/canonical-envelope.json`
- [ ] Subtask 1.7.2 — Extend schema validator to require all five fields on every Silver table
- [ ] Subtask 1.7.3 — CI lint rule: reject Silver DDL missing envelope

---

## Sprint 2 — Canonical Schemas: RC Anchor

**Closes:** BL.P.08, BL.P.09, BL.P.10
**Goal:** Deliver the three RC canonical schemas (SCML, MERML, CXML) to anchor the first end-to-end Practice. RC is the reference Practice because all other Sprints ≥6 can specialize its pattern.
**Exit criteria:** YAML schemas, generated Delta DDL, Purview registration payloads, and passing drift checks for all three schema families.

### Task 2.1 — SCML (Supply Chain) (BL.P.08)
- [ ] Subtask 2.1.1 — Author entity YAMLs: SKU, Location, Lot, Shipment, Supplier, Item
- [ ] Subtask 2.1.2 — Classifications (trade-secret supplier cost, PII on supplier contact)
- [ ] Subtask 2.1.3 — GS1 / EPCIS / GDSN standards alignment documented per entity
- [ ] Subtask 2.1.4 — Generate Delta DDL via `ddl-driver`
- [ ] Subtask 2.1.5 — Generate Purview registration payload
- [ ] Subtask 2.1.6 — Cross-standard translators (GS1 ↔ Schema.org) fixtures

### Task 2.2 — MERML (Merchandising) (BL.P.09)
- [ ] Subtask 2.2.1 — Author entity YAMLs: Category, Price, Promotion, Markdown
- [ ] Subtask 2.2.2 — Pre-measure columns: `effective_margin_pct`, `stock_days_remaining`
- [ ] Subtask 2.2.3 — Delta DDL + Purview payload
- [ ] Subtask 2.2.4 — Relationships (FK to SCML.SKU, CXML.Order)

### Task 2.3 — CXML (Customer Experience) (BL.P.10)
- [ ] Subtask 2.3.1 — Author entity YAMLs: Customer, Loyalty, Interaction, Order
- [ ] Subtask 2.3.2 — PII classifications + tokenization targets
- [ ] Subtask 2.3.3 — Identity-resolution semantics (deterministic + probabilistic)
- [ ] Subtask 2.3.4 — Delta DDL + Purview payload

### Task 2.4 — RC schema CI integration
- [ ] Subtask 2.4.1 — Promote RC YAMLs through dev→test→prod Deployment Pipeline
- [ ] Subtask 2.4.2 — Run drift detector end-to-end on RC
- [ ] Subtask 2.4.3 — Publish `apex-rc/data/schemas.manifest.json` updated summary

---

## Sprint 3 — Canonical Schemas: Other Practices

**Closes:** BL.P.11–P.18 and BL.P.19
**Goal:** Apply the SCML pattern to the six remaining Practices. Parallelizable by Practice lead.
**Exit criteria:** All Practice schemas compile, pass drift detector, and register in Purview Unified Catalog.

### Task 3.1 — HLS schemas (BL.P.11, BL.P.12, BL.P.13)
- [ ] Subtask 3.1.1 — HLSCML / PatientML entities (Patient, Encounter, Observation) — FHIR-aligned
- [ ] Subtask 3.1.2 — ClaimML entities
- [ ] Subtask 3.1.3 — StudyML entities (CDISC-aligned)
- [ ] Subtask 3.1.4 — PHI classifications + HIPAA-compliant retention (10 y)
- [ ] Subtask 3.1.5 — HL7 v2 ↔ FHIR ↔ CDA translator fixtures

### Task 3.2 — ER schemas (BL.P.14)
- [ ] Subtask 3.2.1 — UOGML / P&UML / MiningML entities
- [ ] Subtask 3.2.2 — CIM (IEC 61970) alignment
- [ ] Subtask 3.2.3 — NERC CIP classification handling

### Task 3.3 — AXLE schemas (BL.P.15)
- [ ] Subtask 3.3.1 — AXLECML / AXLEML entities (Equipment Hierarchy, Production, Quality)
- [ ] Subtask 3.3.2 — ISA-95 / ISA-88 alignment
- [ ] Subtask 3.3.3 — OPC UA / OAGIS translators

### Task 3.4 — TMT schemas (BL.P.16)
- [ ] Subtask 3.4.1 — TELML entities (TM Forum SID-aligned)
- [ ] Subtask 3.4.2 — ContentSafetyML entities
- [ ] Subtask 3.4.3 — 3GPP / MEF translators

### Task 3.5 — TH schemas (BL.P.17)
- [ ] Subtask 3.5.1 — IROPsML, ReservationML, Traveler / Profile / Preferences
- [ ] Subtask 3.5.2 — IATA NDC / PADIS alignment
- [ ] Subtask 3.5.3 — PCI DSS-compliant tokenization for payment

### Task 3.6 — ICE schemas (BL.P.18)
- [ ] Subtask 3.6.1 — ConnectedICEML entities (Telematics, Service Events)
- [ ] Subtask 3.6.2 — SAE J1939 / AEMP 2.0 alignment
- [ ] Subtask 3.6.3 — SAE J1939 ↔ AEMP 2.0 translator

### Task 3.7 — Cross-standard translators consolidation (BL.P.19)
- [ ] Subtask 3.7.1 — Index all translators in `apex-core/data/translator-catalog.json`
- [ ] Subtask 3.7.2 — Add round-trip conformance tests

---

## Sprint 4 — Medallion Bronze Landing

**Closes:** BL.P.20–P.25
**Goal:** Ship the five Bronze landing templates so Practices can onboard SORs without inventing ingest patterns.
**Exit criteria:** Each template has a parameterized reference workspace + unit-tested config + error-semantics runbook.

### Task 4.1 — Mirrored Database template (BL.P.20)
- [ ] Subtask 4.1.1 — Fabric Mirroring item template (parameters: source, creds vault, latency SLO)
- [ ] Subtask 4.1.2 — Error-semantics runbook (Mirror failure → Purview event → Teams alert)
- [ ] Subtask 4.1.3 — Schema-evolution flow (additive auto, drop → Silver-transform staged change)

### Task 4.2 — Eventstream / Eventhouse template (BL.P.21)
- [ ] Subtask 4.2.1 — Eventstream + Eventhouse KQL table reference
- [ ] Subtask 4.2.2 — In-flight dedupe + tokenize processor
- [ ] Subtask 4.2.3 — `bronze_raw_deadletter` table + dashboard

### Task 4.3 — Data Pipeline (batch) template (BL.P.22)
- [ ] Subtask 4.3.1 — Copy + Notebook + Stored Procedure activities reference
- [ ] Subtask 4.3.2 — Trigger patterns (cron, file-arrival)
- [ ] Subtask 4.3.3 — Retry / backoff / dead-letter flow

### Task 4.4 — Dataflow Gen2 (REST/SaaS) template (BL.P.23)
- [ ] Subtask 4.4.1 — Power Query reference for Salesforce / Workday / ServiceNow
- [ ] Subtask 4.4.2 — Incremental watermark pattern
- [ ] Subtask 4.4.3 — Rate-limit / auth-expiry handling

### Task 4.5 — Custom Endpoint (webhook) template (BL.P.24)
- [ ] Subtask 4.5.1 — Azure Function HTTP trigger reference
- [ ] Subtask 4.5.2 — HMAC-SHA256 signature verification middleware
- [ ] Subtask 4.5.3 — OneLake SDK write + Service Bus dead-letter

### Task 4.6 — Bronze retention & partitioning (BL.P.25)
- [ ] Subtask 4.6.1 — Purview retention policies (7 y / 10 y / legal-hold)
- [ ] Subtask 4.6.2 — Default partition by `ingest_date`; overrides documented

---

## Sprint 5 — Silver Transform & Tokenization

**Closes:** BL.P.26, BL.P.27, BL.P.28, BL.P.34
**Goal:** Bronze → Silver transform pattern with tokenization at the boundary. This is the point where PII/PHI is locked away.
**Exit criteria:** Silver rows carry only tokens; detokenization path works only for PIM-gated identities; drift detector flags schema divergence.

### Task 5.1 — Silver transform pattern (BL.P.26)
- [ ] Subtask 5.1.1 — PySpark notebook template: Bronze read → canonicalize → enrich → write Silver
- [ ] Subtask 5.1.2 — Idempotency guarantee (replay-safe with source timestamps)
- [ ] Subtask 5.1.3 — Late-arriving data handling (source-ts windowing)
- [ ] Subtask 5.1.4 — Apply to RC (SCML/MERML/CXML) end-to-end

### Task 5.2 — Tokenization service (BL.P.27)
- [ ] Subtask 5.2.1 — Deterministic reversible token function (scoped service principal)
- [ ] Subtask 5.2.2 — Vault Delta table `silver_vault_tokens` with PIM access
- [ ] Subtask 5.2.3 — `tokenizer-mcp` initial skeleton (detokenize-under-scope)
- [ ] Subtask 5.2.4 — Integration into PII/PHI columns via Purview classification hook

### Task 5.3 — SCD Type 2 framework (BL.P.28)
- [ ] Subtask 5.3.1 — Reusable SCD2 PySpark pattern with `valid_from` / `valid_to` / `is_current`
- [ ] Subtask 5.3.2 — Change-detection via `row_hash`

### Task 5.4 — Drift detector (BL.P.34)
- [ ] Subtask 5.4.1 — Compare Fabric schema DESCRIBE output against YAML manifest
- [ ] Subtask 5.4.2 — Purview event emission on drift
- [ ] Subtask 5.4.3 — Nightly scheduled run + ops dashboard

---

## Sprint 6 — Gold Serving & Measures

**Closes:** BL.P.29, BL.P.30, BL.P.31, BL.P.32, BL.P.33
**Goal:** Three Gold materialization strategies + measure libraries so agents get sub-second data.
**Exit criteria:** RC Direct Lake semantic model serves an agent under 500 ms p95 for the Cold Chain reference query.

### Task 6.1 — Direct Lake semantic models (BL.P.29)
- [ ] Subtask 6.1.1 — RC semantic model reference (Direct Lake over Silver SCML/MERML/CXML)
- [ ] Subtask 6.1.2 — Sub-second refresh validation
- [ ] Subtask 6.1.3 — Classification propagation validated end-to-end

### Task 6.2 — Warehouse views (BL.P.30)
- [ ] Subtask 6.2.1 — T-SQL view templates for agent-facing Gold
- [ ] Subtask 6.2.2 — View-definition SHA stamping for audit row

### Task 6.3 — Real-time KQL functions (BL.P.31)
- [ ] Subtask 6.3.1 — Eventhouse function library for streaming Gold
- [ ] Subtask 6.3.2 — Data Activator rule examples triggering agents

### Task 6.4 — Pre-measure library (BL.P.32)
- [ ] Subtask 6.4.1 — PySpark pre-measures per Practice (effective_margin_pct, stock_days_remaining, time_since_last_event, weather-adjusted demand)
- [ ] Subtask 6.4.2 — Git-versioned measure definitions + owner metadata

### Task 6.5 — Post-measure library (BL.P.33)
- [ ] Subtask 6.5.1 — DAX measures (PoP, rolling avg, attainment, confidence interval)
- [ ] Subtask 6.5.2 — T-SQL measure views
- [ ] Subtask 6.5.3 — KQL measure functions

---

## Sprint 7 — Utility MCP Servers

**Closes:** BL.P.41, P.42, P.43, P.44, P.45, P.51, P.52
**Goal:** Platform-service MCP servers come first because every other MCP depends on them.
**Exit criteria:** All six utility servers deployed to the platform workspace, instrumented with trace, and schema-documented.

### Task 7.1 — MCP tool-contract generator (BL.P.51)
- [ ] Subtask 7.1.1 — Scaffolding CLI: input YAML → inputSchema + outputSchema + SLO stub
- [ ] Subtask 7.1.2 — SemVer version pinner
- [ ] Subtask 7.1.3 — Contract registered as Purview asset on generation

### Task 7.2 — Trace instrumentation (BL.P.52)
- [ ] Subtask 7.2.1 — Standard trace record (operation_id, classification_applied)
- [ ] Subtask 7.2.2 — App Insights / telemetry-mcp wiring

### Task 7.3 — `fabric-mcp` (BL.P.41)
- [ ] Subtask 7.3.1 — Tools: `get_entity_by_key`, `query_gold_view`, `list_classifications`
- [ ] Subtask 7.3.2 — Managed-identity OneLake reads
- [ ] Subtask 7.3.3 — Agent-safe view enforcement

### Task 7.4 — `policy-mcp` (BL.P.42)
- [ ] Subtask 7.4.1 — Tools: `evaluate_policy`, `check_compliance`, `classify_bump`
- [ ] Subtask 7.4.2 — Wire to `classify-bump` from `apex-core/tools`

### Task 7.5 — `telemetry-mcp` (BL.P.43)
- [ ] Subtask 7.5.1 — Tools: `emit_trace`, `log_event`, `query_latency_percentile`
- [ ] Subtask 7.5.2 — App Insights exporter

### Task 7.6 — `approvals-mcp` (BL.P.44)
- [ ] Subtask 7.6.1 — Tools: `request_approval`, `get_approval_status`, `record_decision`
- [ ] Subtask 7.6.2 — Teams card + Copilot Studio action bindings

### Task 7.7 — `ledger-mcp` (BL.P.45)
- [ ] Subtask 7.7.1 — Tools: `append_audit_row`, `fetch_row_by_trace`, `verify_row_signature`
- [ ] Subtask 7.7.2 — Immutable append-only store wiring

---

## Sprint 8 — Domain MCP Servers

**Closes:** BL.P.35–P.40
**Goal:** One MCP server per canonical schema family. Segregated identities so PHI grants never cross into cross-Practice scopes.
**Exit criteria:** Every domain MCP server exposes at least four tools, registered in Purview, and passing a groundedness-score smoke test.

### Task 8.1 — `scml-mcp` (BL.P.35)
- [ ] Subtask 8.1.1 — Tools for SKU, Location, Lot, Shipment, Supplier reads
- [ ] Subtask 8.1.2 — Bound to SCML Gold views
- [ ] Subtask 8.1.3 — Scope lattice + classification propagation

### Task 8.2 — `merml-mcp` (BL.P.36)
- [ ] Subtask 8.2.1 — Tools for Category, Price, Promotion, Markdown reads
- [ ] Subtask 8.2.2 — Pre-measure column exposure

### Task 8.3 — `cxml-mcp` (BL.P.37)
- [ ] Subtask 8.3.1 — Tools for Customer, Loyalty, Interaction, Order reads
- [ ] Subtask 8.3.2 — PII tokenization enforcement on output

### Task 8.4 — `hlscml-mcp` (BL.P.38)
- [ ] Subtask 8.4.1 — Tools for Patient, Encounter, Observation reads
- [ ] Subtask 8.4.2 — PHI identity segregation; no cross-Practice sharing

### Task 8.5 — `ercml-mcp` (BL.P.39)
- [ ] Subtask 8.5.1 — Tools for Meter, Grid Event, Work Order reads

### Task 8.6 — `axlecml-mcp` (BL.P.40)
- [ ] Subtask 8.6.1 — Tools for Equipment, Production Event, Quality Result reads

---

## Sprint 9 — External MCP Servers

**Closes:** BL.P.46–P.50
**Goal:** Wrap external data sources behind MCP so agents never reach out directly.
**Exit criteria:** Each external MCP has auth, rate-limit handling, caching, and dead-letter path documented.

### Task 9.1 — `fda-mcp` (BL.P.46)
- [ ] Subtask 9.1.1 — Tools: `list_recalls_by_date`, `get_recall_detail`, `search_adverse_events`
- [ ] Subtask 9.1.2 — OpenFDA rate-limit handling + caching

### Task 9.2 — `ferc-mcp` (BL.P.47)
- [ ] Subtask 9.2.1 — Grid-compliance / enforcement-action tools

### Task 9.3 — `edi-mcp` (BL.P.48)
- [ ] Subtask 9.3.1 — X12 message parsers (850, 856, 810, 820)

### Task 9.4 — `vendor-portal-mcp` (BL.P.49)
- [ ] Subtask 9.4.1 — Multi-vendor portal API aggregation pattern

### Task 9.5 — `pharma-recall-mcp` (BL.P.50)
- [ ] Subtask 9.5.1 — Multi-aggregator pharma-recall tools

---

## Sprint 10 — Identity & Visibility Lattice

**Closes:** BL.P.53–P.57
**Goal:** Entra-issued managed identities per agent + runtime lattice evaluation. All MCP servers (from Sprints 7–9) consume this.
**Exit criteria:** Agent-safe view returns only lattice-permitted attributes; responses are signed; scope cache TTL honored.

### Task 10.1 — Managed-identity provisioning (BL.P.53)
- [ ] Subtask 10.1.1 — Entra app-registration automation per agent
- [ ] Subtask 10.1.2 — Key-vault credential rotation
- [ ] Subtask 10.1.3 — Identity naming convention (`apex-<practice>-<persona>-<env>`)

### Task 10.2 — Scope evaluator (BL.P.54)
- [ ] Subtask 10.2.1 — Compose tenant × practice × persona × classification × row filter
- [ ] Subtask 10.2.2 — Deterministic decision result + reason trace
- [ ] Subtask 10.2.3 — Short TTL cache (minutes)

### Task 10.3 — Visibility-lattice runtime (BL.P.55)
- [ ] Subtask 10.3.1 — RLS + OLS generator from YAML classification
- [ ] Subtask 10.3.2 — Lattice applied at MCP tool boundary

### Task 10.4 — Agent-safe view generator (BL.P.56)
- [ ] Subtask 10.4.1 — View generator: mask / tokenize / drop per classification × scope
- [ ] Subtask 10.4.2 — Applied to RC end-to-end validation

### Task 10.5 — Response signing (BL.P.57)
- [ ] Subtask 10.5.1 — Service-principal signing of agent output
- [ ] Subtask 10.5.2 — Signature verification in `ledger-mcp`

---

## Sprint 11 — Orchestration & HITL Runtime

**Closes:** BL.P.65–P.76
**Goal:** The 47-archetype library plus the four-gate-kind + four-variant runtime. This is APEX's defining control plane.
**Exit criteria:** A reference orchestration (Cold Chain Excursion) runs end-to-end with HITL gate presented to a Teams card and decision captured in audit row.

> **2026-05-09 amendment — Microsoft Agent Framework alignment.** Per [ADR-006](adr/ADR-006-agent-orchestrator-canonical.md), the orchestration substrate for APEX-M is now Microsoft Agent Framework. This Sprint 11 work is preserved (`apex-orchestrator/archetypes/catalog.py`, primitives, manifest runtime, gate kinds, Teams + Copilot Studio integration), but the runtime delegates to Agent Framework's [`AgentWorkflowBuilder.BuildSequential / BuildConcurrent / BuildHandoff / BuildGroupChat / BuildMagentic`](https://learn.microsoft.com/agent-framework/workflows/orchestrations/) underneath. The 47 APEX archetypes are catalog entries with a `canonical_pattern` field pointing at one of the 5 Microsoft patterns plus parameterization. Production wiring of this delegation lives in **Sprint 42** (below).

### Task 11.1 — Orchestration primitives (BL.P.66)
- [ ] Subtask 11.1.1 — Sequential / Parallel / Hierarchical / Feedback-loop runner classes
- [ ] Subtask 11.1.2 — Composition API (archetype built from primitives)

### Task 11.2 — Archetype library (BL.P.65)
- [ ] Subtask 11.2.1 — Catalog 47 archetypes in `apex-core/data/orchestration-archetypes.json`
- [ ] Subtask 11.2.2 — Implement first 10 (cross-Practice highest-leverage)
- [ ] Subtask 11.2.3 — Remaining 37 as manifests + stubs

### Task 11.3 — Orchestration manifest runtime (BL.P.67)
- [ ] Subtask 11.3.1 — Manifest loader stamping `manifest_version` + `policy_version` + `prompt_version`
- [ ] Subtask 11.3.2 — Reject runtime start if any stamp is missing

### Task 11.4 — Practice-specific orchestrations (BL.P.68)
- [ ] Subtask 11.4.1 — RC reference: Cold Chain Excursion, Markdown Cadence, Demand Sensing
- [ ] Subtask 11.4.2 — Templates for other Practices to specialize

### Task 11.5 — Four gate kinds (BL.P.69, P.70, P.71, P.72)
- [ ] Subtask 11.5.1 — ZERO_TOUCH runtime: silent apply + audit log
- [ ] Subtask 11.5.2 — ACK_ONLY runtime: apply + notify (Teams / email)
- [ ] Subtask 11.5.3 — HITL runtime: present + wait (Teams card + Copilot Studio action)
- [ ] Subtask 11.5.4 — ESCALATION runtime: cross-functional owner routing

### Task 11.6 — Four gate variants (BL.P.73)
- [ ] Subtask 11.6.1 — Hard / Soft / Policy / Escalation selector in orchestration manifest
- [ ] Subtask 11.6.2 — Validator ensures variant + kind combo is legal

### Task 11.7 — Teams + Copilot Studio integration (BL.P.74, P.75)
- [ ] Subtask 11.7.1 — Adaptive-card templates for HITL presentation
- [ ] Subtask 11.7.2 — Copilot Studio skill for approve/reject/modify
- [ ] Subtask 11.7.3 — Dashboard for pending approvals

### Task 11.8 — Tenant policy tuning (BL.P.76)
- [ ] Subtask 11.8.1 — Tuning request workflow (proposal + 2-week observation)
- [ ] Subtask 11.8.2 — Auto-rollback on reversal / escalation during observation
- [ ] Subtask 11.8.3 — Tuning-change audit trail

---

## Sprint 12 — Decision Audit Row

**Closes:** BL.P.77–P.84
**Goal:** The 14-field audit row plus trace-ID discipline + three-version rule. Runtime rejects any agent emission missing required fields.
**Exit criteria:** Every Cold Chain decision produces a valid row; auditor can reconstruct the decision by resolving the three Git SHAs.

### Task 12.1 — Audit-row schema + store (BL.P.77)
- [ ] Subtask 12.1.1 — Define Delta schema for 14 required + optional fields
- [ ] Subtask 12.1.2 — Immutable append-only table with WORM policy
- [ ] Subtask 12.1.3 — Wire into `ledger-mcp.append_audit_row`

### Task 12.2 — Trace-ID discipline (BL.P.78)
- [ ] Subtask 12.2.1 — Trace-ID generator + propagation across sync / async / HITL / retries
- [ ] Subtask 12.2.2 — Runtime validator rejects emissions missing `trace_id`

### Task 12.3 — Three-version rule (BL.P.79)
- [ ] Subtask 12.3.1 — Manifest + policy + prompt SHA stamper at pre-invocation
- [ ] Subtask 12.3.2 — Auditor tool: given `decision_id`, resolve three SHAs and print effective rules

### Task 12.4 — Reasoning-trace capture (BL.P.80)
- [ ] Subtask 12.4.1 — Capture tool-call sequence, decision justification, cited-evidence pointers
- [ ] Subtask 12.4.2 — DLP scrub against propagated sensitivity labels
- [ ] Subtask 12.4.3 — Raw-reasoning restricted store with stricter access

### Task 12.5 — Orchestration composite row (BL.P.81)
- [ ] Subtask 12.5.1 — Emit parent row referencing every participating agent via shared trace-ID
- [ ] Subtask 12.5.2 — Capture latency_breakdown, hitl_gates_fired, policy_exceptions

### Task 12.6 — Content-addressed I/O store (BL.P.82)
- [ ] Subtask 12.6.1 — Hash input/output; store by content hash
- [ ] Subtask 12.6.2 — `inputs_ref` / `result_hash` reference pattern

### Task 12.7 — Downstream-effect cross-reference (BL.P.83)
- [ ] Subtask 12.7.1 — Action-tool call emits its own row; parent refs via `downstream_effect_ref`

### Task 12.8 — Row signing + hashing (BL.P.84)
- [ ] Subtask 12.8.1 — Service-principal signature on row seal
- [ ] Subtask 12.8.2 — Tamper-evidence verification tool

---

## Sprint 13 — Purview Trust Architecture

**Closes:** BL.P.85–P.90
**Goal:** Turn Purview integration from a design commitment into a wired pipeline. Every hop emits lineage; every classification propagates.
**Exit criteria:** End-to-end lineage from SOR through audit row is visible in Purview Unified Catalog for RC Cold Chain.

### Task 13.1 — Classification registration pipeline (BL.P.85)
- [x] Subtask 13.1.1 — YAML schema → Purview classification payload emitter *(2026-04-22 — `apex-purview` package created: `classifications.py` emitter for Atlas v2 type-defs + entity attachments; 12 canonical APEX classifications registered (public, internal, trade_secret, pii, phi, pci, genetic, behavioral_health, restricted, cpni, export_controlled, member_only); `apex purview emit-classifications` / `emit-attachments` / `list-classifications` CLI; 50 tests passing)*
- [x] Subtask 13.1.2 — CI step registers on schema merge *(2026-04-22 — `_register.py` batch pipeline with `discover_schemas` / `register_all` / `RegistrationReport`; `apex purview register-all --root --output --strict` CLI; GitHub Actions `register-classifications` job discovers every `kind: schema` YAML, emits payloads, fails build on any emission error, uploads `purview-classification-payloads` artifact for 30 days; pre-commit hook `apex-purview-register` gates schema YAML changes locally. Real-repo dry-run: 1 real schema, 5 classifications, 20 attachments, exit 0)*

### Task 13.2 — Lineage capture (BL.P.86)
*(2026-04-22 — `apex_purview.lineage` module ships the seven-hop lineage pipeline. Seven `emit_*` functions, one declarative `kind: lineage` YAML spec, `emit_lineage_batch` assembler for Atlas `POST /api/atlas/v2/entity/bulk`, `emit_process_typedefs` for one-time Purview bootstrap. CLI: `apex purview emit-lineage <spec.yaml>`, `apex purview emit-process-typedefs`. 29 new tests; 79/79 apex-purview tests passing. Reference Cold Chain Excursion lineage fixture emits all seven hops cleanly.)*
- [x] Subtask 13.2.1 — SOR → Bronze edge with pipeline run ID *(`emit_sor_to_bronze` — carries pipeline_run_id, optional ingest_ts + ingest_latency_ms; Process type `apex_sor_to_bronze`)*
- [x] Subtask 13.2.2 — Bronze → Silver edge with notebook + commit SHA *(`emit_bronze_to_silver` — carries notebook_url + commit_sha + optional transform_version; qualified name includes first 12 chars of commit SHA)*
- [x] Subtask 13.2.3 — Silver → Gold edge with SQL SHA *(`emit_silver_to_gold` — multi-input array of Silver tables, single Gold output, gold_type one of direct_lake_view / warehouse_view / kql_function, view_definition_url optional)*
- [x] Subtask 13.2.4 — Gold → MCP tool asset edge *(`emit_gold_to_mcp` — binds a Gold view to exactly one MCP tool with tool_version and mcp_server; qualified name pinned by tool version)*
- [x] Subtask 13.2.5 — MCP → Agent edge; Agent → Orchestration edge; Orchestration → Audit row edge *(three emitters: `emit_mcp_to_agent` carries agent_manifest_sha, `emit_agent_to_orchestration` carries orchestration_manifest_sha + optional archetype_id, `emit_orchestration_to_audit` carries the full three-version rule — manifest_version + policy_version + prompt_version — plus trace_id, decision_id, optional hitl_status. Completes the forensic thread from SOR row to regulator-ready audit entry.)*

### Task 13.3 — DLP policies (BL.P.87)
*(2026-05-04 — `apex_purview.dlp` module ships the full classification × surface DLP matrix. 12 classifications × 6 surfaces = 72 default rules in `DEFAULT_DLP_MATRIX`. Six DLP actions ordered by severity: allow / allow_with_warning / mask / redact / block / escalate. Tenant overrides never relax below default — most-restrictive wins. CLI: `apex purview emit-dlp`, `apex purview dlp-lookup <classification> <surface>`. 24 new tests; smoke checks confirm phi/email→block, restricted/copilot→escalate, public/anywhere→allow.)*
- [x] Subtask 13.3.1 — Label-based redaction policies for Copilot, agent output, Power BI *(`build_default_bundle()` produces the full grid; `lookup_action()` resolves any pair; six surfaces include Copilot chat, agent output, Power BI export, Teams, email, public web)*
- [x] Subtask 13.3.2 — Policy-violation alerting *(`DLPViolationAlert` configures webhook URL + severity threshold + audit-row stamp; bundle's `to_atlas()` serializes alerting block when present)*

### Task 13.4 — WORM retention (BL.P.88)
*(2026-05-04 — `apex_purview.retention` module ships four retention bands (P3Y default, P7Y for SOX/PCI/NERC CIP, P10Y for HIPAA/GINA/42 CFR Part 2, PERMANENT for 21 CFR Part 11 / FSMA 204). Per-classification regulatory-basis citations baked in. Tenant overrides never shorten below default — longer-of-default-and-override always wins. `LegalHoldConfig` for matter-scoped holds across multiple classifications. CLI: `apex purview emit-retention`, `apex purview retention-lookup <classification>`. 21 new tests.)*
- [x] Subtask 13.4.1 — Purview-managed retention (7 y default, 10 y HLS, legal-hold support) *(`build_default_retention_bundle` produces 12-row matrix; `_longer_duration` enforces never-shorten rule with PERMANENT dominating; `LegalHoldConfig.to_atlas()` produces matter-id-keyed hold payload; smoke checks confirm phi→P10Y, restricted→PERMANENT, pci→P7Y)*

### Task 13.5 — Unified Catalog registration (BL.P.89)
*(2026-05-04 — `apex_purview.catalog` module ships glossary + relationship emission. `GlossaryDef` + `GlossaryTerm` produce Atlas v2 `/api/atlas/v2/glossary` and `/api/atlas/v2/glossary/term` payloads from any APEX schema YAML. `EntityRelationship` produces `/api/atlas/v2/relationship` payloads from declared schema relationships. Two custom relationship types registered: `apex_fk` and `apex_join`. CLI: `apex purview emit-catalog <schema.yaml>`, `apex purview emit-relationship-typedefs`. 12 new tests.)*
- [x] Subtask 13.5.1 — Business-glossary term registration per attribute *(`emit_glossary_terms_from_schema` walks schema entities + attributes, emits one term per description-bearing field with assignedEntities pointing to the qualified name; APEX glossary container `APEX@apex-glossary` materialized via `emit_glossary_def`)*
- [x] Subtask 13.5.2 — Cross-entity relationship registration *(`emit_relationships_from_schema` walks `relationships:` arrays in schema YAML and produces apex_fk relationship payloads; `emit_relationship_typedefs` registers `apex_fk` and `apex_join` relationship-defs as one-time bootstrap)*

### Task 13.6 — Classification propagation chain (BL.P.90)
*(2026-05-04 — `apex_purview.propagation` module ships the canonical 12-classification severity ordering (public=0 → restricted=10) with phi=7, genetic/behavioral_health=8 sharing severity. `validate_propagation` walks propagation graph, flags any node whose declared classification is less restrictive than the most-restrictive of its inputs. `build_propagation_graph` constructs Silver+Gold node graph from schema YAMLs and optional lineage spec; auto-creates placeholder Silver nodes for lineage inputs not present in supplied schemas (robust for partial-schema validation). CLI: `apex purview validate-propagation <schemas...> [--lineage spec.yaml]`. 21 new tests. Real-repo dry-run on `apex-rc` schemas: 44 nodes checked, 0 violations.)*
- [x] Subtask 13.6.1 — Silver → Gold → semantic model → Copilot → agent-output validator *(`PropagationNode` carries `layer ∈ {silver, gold, semantic_model, copilot, agent_output}`; `validate_propagation` returns `PropagationReport` with per-violation triggering-input list; CLI exits non-zero on any violation; CI-ready)*
- [x] Subtask 13.6.2 — Most-restrictive-label inheritance rule *(`CLASSIFICATION_SEVERITY` ordering implemented; `most_restrictive(list)` picks max; `severity()` rejects unknown classifications; `_normalize_key` accepts ``"Trade Secret"`` / ``"trade-secret"`` / ``"trade_secret"`` synonyms; PHI + Genetic share severity 8 — neither dominates and both must be enforced separately)*

---

## Sprint 14 — Fabric Capacity & Provisioning

**Closes:** BL.P.91–P.94
**Goal:** Terraform modules + API automation so new tenant workspaces are one-click.
**Exit criteria:** From zero, a new tenant can provision F16 capacity + workspaces + OneLake shortcuts in under 30 minutes.

### Task 14.1 — Terraform F-SKU module (BL.P.91)
*(2026-05-04 — `infra/terraform/modules/fabric_capacity/` ships the canonical Terraform module. Parameterized for all 11 F-SKUs (F2–F2048); 12-key APEX canonical tag set (`apex:practice`, `apex:environment`, `apex:resource_class`, `apex:sku`, `apex:cost_center`, `apex:owner`, `apex:purview_class`, `apex:managed_by`, `apex:module_version`); preconditions enforce production must be F64+ (Copilot threshold); naming pattern `apex-{practice}-{environment}[-{suffix}]`; `prevent_destroy=true` lifecycle; module README with full input/output reference.)*
- [x] Subtask 14.1.1 — `azurerm_fabric_capacity` module parameterized for F-SKU tier *(11 F-SKUs validated; production-tier precondition enforced; canonical tag set applied; Terraform 1.7+, azurerm 4.x compatible)*
- [x] Subtask 14.1.2 — Cost-guardrail variables *(`monthly_budget_usd` + `allow_budget_breach` — module fails plan if estimated SKU cost exceeds budget; `sku_monthly_usd` table baked in (F2=263 → F2048=175200) for plan-time enforcement; override requires explicit Independence-reviewed flag)*

### Task 14.2 — Workspace API provisioning (BL.P.92)
*(2026-05-04 — `apex-fabric` package created. `apex_fabric.workspaces` module ships `WorkspaceClient` (Entra-bearer-token-only, no connection-string auth) + `WorkspaceSpec` declarative spec + `canonical_workspace_name`/`parse_workspace_name`/`validate_workspace_name` naming-convention helpers. Wrapping `POST /v1/workspaces`, `GET /v1/workspaces`, `DELETE /v1/workspaces/{id}`, `POST /v1/workspaces/{id}/assignToCapacity`. Idempotent `ensure_workspace`. CLI: `apex fabric validate-name`, `apex fabric canonical-name`, `apex fabric describe-blueprint`. 26 tests passing.)*
- [x] Subtask 14.2.1 — PowerShell / REST wrapper for `POST /v1/workspaces` *(Python httpx-based; `WorkspaceClient.create_workspace(spec)` validates spec then POSTs; injectable `http_client` for test stubs; injectable `token_provider` for Entra-credential abstraction; Pythonic alternative to PowerShell that integrates with the rest of the apex-* Python ecosystem)*
- [x] Subtask 14.2.2 — Naming convention enforcement *(`apex-{practice}-{environment}-{role}[-{suffix}]` regex enforced; PRACTICES = rc/hls/er/axle/tmt/th/ice/core; ENVIRONMENTS = dev/test/stage/prod; ROLES = bronze/silver/gold/governance/runtime/sandbox; rejection at API-call time, not at server time; `name_override` requires explicit non-canonical-pattern review per Independence sign-off)*

### Task 14.3 — Capacity-pattern templates (BL.P.93)
*(2026-05-04 — three blueprint Terraform stacks under `infra/terraform/blueprints/` composing the Sprint 14.1 module. Each blueprint produces canonical resource groups + canonical capacities + cost roll-up output. `apex fabric describe-blueprint <name>` documents each.)*
- [x] Subtask 14.3.1 — Single-capacity-per-tenant blueprint *(`single-capacity-tenant/main.tf` — one F-SKU hosting all medallion roles; default F16; right for Wave 1 pilots and small Wave 2)*
- [x] Subtask 14.3.2 — Dev/prod split blueprint *(`dev-prod-split/main.tf` — two capacities (default F16 dev + F64 prod) in separate resource groups; cost-attribution-clean separation; dev-prod admins separately specified; right for Wave 2 with iteration safety)*
- [x] Subtask 14.3.3 — Per-workload isolation blueprint (F128+) *(`per-workload-isolation/main.tf` — three capacities (default F128 warehouse + F64 realtime + F64 governance) with three resource groups + three admin lists; right for Wave 3 enterprise scale and compliance-driven workload boundaries)*

### Task 14.4 — OneLake shortcut provisioning (BL.P.94)
*(2026-05-04 — `apex_fabric.shortcuts` module ships `ShortcutClient` + 5 typed target dataclasses (`AdlsGen2Target`, `S3Target`, `GoogleCloudStorageTarget`, `DataverseTarget`, `OneLakeTarget`) + `ShortcutSpec` + `ShortcutPlan` + `practice_reference_shortcuts` helper. Wraps `POST /v1/workspaces/{ws}/items/{item}/shortcuts`, `GET .../shortcuts`, `DELETE .../shortcuts/{path}/{name}`. Idempotent `ensure_shortcut`. 24 tests passing.)*
- [x] Subtask 14.4.1 — ADLS Gen2 / S3 / GCS / Dataverse shortcut automation *(four typed Target dataclasses with hop-specific fields; each `to_atlas()` produces the exact Fabric-API `target.{kind}` envelope shape; conformance test verifies JSON round-trip for every target type)*
- [x] Subtask 14.4.2 — Cross-workspace shortcut for Practice-reference → Tenant *(`OneLakeTarget` for cross-workspace; `practice_reference_shortcuts(...)` helper builds a `ShortcutPlan` covering N canonical Silver tables in one call — the "Bronze stays where it is, canonical Silver lives once" pattern from Sellers Guide §1.6 / §6.13; smoke test confirms 3-table plan applies idempotently)*

---

## Sprint 15 — SOR Integration Adapters

**Closes:** BL.P.95–P.109
**Goal:** 15 worked adapters so a Wave-1 engagement picks from the shelf rather than building.
**Exit criteria:** Each adapter has a reference workspace, smoke-test dataset, and runbook. Parallelizable across integration engineers.

*(2026-05-04 — `apex-adapters` package created. Adapter framework ships with `AdapterSpec` (manifest model), `Adapter` (abstract base), `SchemaMapping` / `FieldMapping` / `Runbook` / `FailureMode` / `SmokeTestResult`, `ConnectionMethod` enum (mirrored_db, eventstream, data_pipeline, dataflow_gen2, custom_endpoint, odbc, file_drop), and a registry decorator. Two reference Python implementations ship: `EpicClarityAdapter` (ODBC pattern) and `SapS4HanaAdapter` (CDC pattern with 14-table canonical SAP set). All 15 reference YAML manifests ship under `packages/apex-adapters/src/apex_adapters/manifests/` covering each subtask. Terraform `adapter-workspace` blueprint provisions Bronze capacity + RG via Sprint 14's `fabric_capacity` module. CLI: `apex adapters list/inspect/validate-all/smoke-test`. 31 tests passing; real-repo validate-all confirms all 15 manifests load cleanly.)*

### Task 15.1 — HLS-aligned adapters
- [x] Subtask 15.1.1 — Epic Clarity (BL.P.95) *(`epic-clarity.yaml` manifest + `EpicClarityAdapter` Python class with ODBC pattern, golden-fixture smoke test, missing-required-field detection. Spec covers PATIENT and PAT_ENC tables with PHI classification on identifying fields.)*
- [x] Subtask 15.1.2 — HL7 v2 / FHIR feeds (BL.P.106) *(`hl7-fhir.yaml` manifest with Eventstream pattern from integration-engine vendors (Mirth/InterSystems/Rhapsody). ADT message + FHIR Patient resource Bronze tables; full message preserved for Sprint 23 BL.P.155–156 parsers to canonicalise at Silver. SLA 5-minute recovery for clinical-workflow criticality.)*

### Task 15.2 — ERP-aligned adapters
- [x] Subtask 15.2.1 — SAP S/4HANA (BL.P.96) *(`sap-s4hana.yaml` manifest + `SapS4HanaAdapter` Python class with Mirrored-DB CDC pattern. 14-table canonical SAP set baked in (`CANONICAL_SAP_TABLES` — KNA1, MARA, MARC, BSEG, BKPF, EKKO, EKPO, etc.). `is_canonical_table` + `canonical_tables_in_scope` helpers for spec validation. Trade-secret classification on financial amounts.)*
- [x] Subtask 15.2.2 — Oracle EBS / Fusion (BL.P.108) *(`oracle-ebs-fusion.yaml` manifest with mirrored-db pattern; HZ_PARTIES + MTL_SYSTEM_ITEMS_B representative tables; supports both 11i / R12 EBS and Fusion BIP-data feed schemas, switched per spec.)*

### Task 15.3 — CRM / HCM / ITSM-aligned adapters
- [x] Subtask 15.3.1 — Salesforce (BL.P.97) *(`salesforce.yaml` — Dataflow Gen2 with Bulk API 2.0 + CDC subscription. Account + Opportunity tables with PII / trade-secret classifications. API-rate-limit + OAuth-token-rotation runbook entries.)*
- [x] Subtask 15.3.2 — Workday HCM (BL.P.99) *(`workday-hcm.yaml` — daily RaaS report ingest into Core Bronze; Worker + Position tables. Practice workspaces shortcut to Worker via OneLake Practice-reference pattern from Sprint 14.4.2.)*
- [x] Subtask 15.3.3 — ServiceNow (BL.P.100) *(`servicenow.yaml` — Power Query Table API ingest of incident, change, problem tables on 30-minute cadence; CMDB on daily; quota-saturation + assignee-PII handling baked in.)*
- [x] Subtask 15.3.4 — Salesforce Marketing Cloud (BL.P.105) *(`salesforce-marketing-cloud.yaml` — daily SFMC SOAP / REST + Tracking Extract files; Subscriber + SentEvent tables; subscriber-level PII tokenized at Silver.)*

### Task 15.4 — Supply-chain-aligned adapters
- [x] Subtask 15.4.1 — Manhattan Active WMS (BL.P.98) *(`manhattan-wms.yaml` — Data Pipeline pattern combining REST batch pulls + scheduled file drops for high-volume tables. InventoryByLocation + ShipmentEvent representative tables. 15-minute cadence supports store-replenishment use cases.)*
- [x] Subtask 15.4.2 — SAP Ariba / Coupa (BL.P.107) *(`sap-ariba-coupa.yaml` — daily REST API pull of supplier, contract, PO, invoice tables. Trade-secret classification on amounts; supplier names trade-secret in regulated-industry contexts.)*

### Task 15.5 — Industrial / Historian adapters
- [x] Subtask 15.5.1 — OSIsoft / AVEVA PI (BL.P.101) *(`osi-pi.yaml` — continuous Eventstream pattern from PI Web API; PiTagValue table preserves tag name, timestamp, value, quality, asset hierarchy. Critical-severity for connector-down with 5-retry / 30-s backoff. ER Practice's primary OT source.)*
- [x] Subtask 15.5.2 — GE Proficy / AVEVA Wonderware (BL.P.102) *(`ge-proficy.yaml` — continuous Eventstream via OPC UA; HistorianTag table for SCADA / PLC tag streams driving AXLE OEE / MTBF / Andon agents.)*

### Task 15.6 — Legacy / analytics adapters
- [x] Subtask 15.6.1 — AS/400 / DB2 (BL.P.103) *(`as400-db2.yaml` — ODBC pattern preserving green-screen field names verbatim; canonical SCML reshape happens at Silver. Concurrent-connection throttling baked into runbook.)*
- [x] Subtask 15.6.2 — Adobe / Google Analytics (BL.P.104) *(`analytics-platforms.yaml` — daily Power Query against Adobe Data Feeds + GA4 BigQuery export; AdobeHits + GA4Events Bronze tables; visitor-level PII classification; joined to CXML.Customer at Silver.)*
- [x] Subtask 15.6.3 — Snowflake / Databricks interop (BL.P.109) *(`snowflake-databricks.yaml` — Snowflake → Fabric via Mirror, Databricks → Fabric via OneLake shortcut to Unity Catalog Delta. Per Sellers Guide §4.8 complementary-platform positioning, this is interop seam not migration path. Notes section explicitly references positioning to prevent scope drift.)*

---

## Sprint 16 — Agent Catalogs per Practice

**Closes:** BL.P.58–P.64
**Goal:** 40–50 pre-built agents per Practice, each with manifest, system prompt, tool allow-list, and tests. Parallelizable by Practice lead.
**Exit criteria:** Every agent is manifest-valid, passes groundedness and classification-enforcement smoke tests, and registers in Purview.

*(2026-05-04 — `apex-agents` package created with 70 anchor agents shipped (10 per Practice × 7 Practices). AgentSpec framework includes ModelTier (lightweight/standard/reasoning), OversightMode (HITL/HOTL/HIC), ToolBinding with write flag, HITLGate with SLA, KpiTarget. Catalog scanner enumerates per-Practice; validator enforces canonical naming, write-tools-require-HITL (with pure-HOTL/HIC exception per Sellers Guide §2.2C), reasoning-tier should declare KPIs, positive HITL SLA. CLI: `apex agents stats / list / inspect / validate`. 28 tests passing; real-repo `apex agents validate` returns 0 errors across all 70 agents. The Sprint 16 plan calls for 40-50 per Practice — the anchor 10 ship here; remaining 30-40 per Practice are engagement-specific and use the same `AgentSpec` template.)*

### Task 16.1 — RC agent catalog (BL.P.58)
- [x] Subtask 16.1.1 — Anchor 10 agents (Assortment, Demand Sensing, Markdown, Cold Chain, Shrink, Customer Identity, Promotions, Substitutions, Inventory, Store Ops) *(`apex_agents/catalogs/rc/01..10` — full YAML manifests with personas (Chief Merchant, Store Manager, etc.), service codes, model tiers, MCP tool allow-lists, HITL gates with SLAs, KPIs with directions and target bands, oversight modes per agent.)*
- [ ] Subtask 16.1.2 — Remaining 30–40 from the RC agent-catalog design plan *(engagement-specific; framework + 10 anchors unblock authoring)*
- [x] Subtask 16.1.3 — Manifest + prompt + tool-allow-list + golden evals per agent *(manifest schema + tool-allow-list shipped; prompt SHA placeholder ready to populate at engagement time; golden-eval harness builds on Sprint 15's adapter smoke-test pattern)*

### Task 16.2 — HLS agent catalog (BL.P.59)
- [x] Subtask 16.2.1 — Anchor 10 agents (Sepsis Early Warning, Clinical Decision Support, Utilization Mgmt, Claim Triage, Study Enrollment, Drug Interaction, Readmission Risk, Patient Identity, Adverse Event, Supply Cold Chain) *(`apex_agents/catalogs/hls/01..10` — full manifests; PHI-aware HITL gates throughout; reasoning-tier on Clinical Decision Support per the Sellers Guide §10.10.4; sepsis agent's HITL gate fires at 5-minute SLA matching clinical-workflow criticality.)*
- [ ] Subtask 16.2.2 — Remaining 30–40 *(engagement-specific)*

### Task 16.3 — ER agent catalog (BL.P.60) *(anchor 10 shipped — outage-triage, restoration-sequencing, psps-decision, vegetation-risk, der-orchestration, well-ops, drilling-safety, fleet-mining, hse-incident, ami-billing-anomaly. PSPS decision uses reasoning tier with CEO-approval HITL per Sellers Guide §11.9.6.)*
- [x] Anchor 10 shipped

### Task 16.4 — AXLE agent catalog (BL.P.61) *(anchor 10 shipped — oee-monitor, predictive-maintenance, quality-defect, andon-rca, supplier-quality, warranty-cost, generative-engineering, vehicle-dtc, production-scheduling, energy-optimization. Generative engineering on reasoning tier per Sellers Guide §12.10.3.)*
- [x] Anchor 10 shipped

### Task 16.5 — TMT agent catalog (BL.P.62) *(anchor 10 shipped — contact-center-routing, network-anomaly, billing-dispute, fraud-pattern, content-rights, ad-fraud, content-moderation, subscriber-churn, sla-monitoring, developer-experience. CPNI-forbidden classification on TEL agents per Sellers Guide §13.13.7.)*
- [x] Anchor 10 shipped

### Task 16.6 — TH agent catalog (BL.P.63) *(anchor 10 shipped — irops-recovery, traveler-360, yield-management, loyalty-personalization, crew-scheduling, ground-ops, guest-experience, demand-disruption, fnb-recommendation, disruption-comms. IROPs recovery uses reasoning tier with multi-source magentic orchestration per Sellers Guide §14.8.)*
- [x] Anchor 10 shipped

### Task 16.7 — ICE agent catalog (BL.P.64) *(anchor 10 shipped — fleet-health, predictive-service, warranty-claim-triage, parts-stocking, rental-utilization, operator-coaching, emissions-compliance, dealer-performance, captive-finance-risk, supply-shortage. Operator-coaching is canonical pure-HOTL example — write tool with no HITL gate by design.)*
- [x] Anchor 10 shipped

---

## Sprint 17 — Service Catalogs per Practice

**Closes:** BL.P.110–P.116
**Goal:** Productize the agent+orchestration bundles into named services with personas, KPIs, SLOs, commercial terms.
**Exit criteria:** At least 45 services per Practice registered with service manifest; RC has all services from the RC build spec v2.

*(2026-05-04 — `apex-services` package created with 61 anchor service manifests across all 7 Practices. ServiceSpec framework includes Persona (primary/secondary), KpiCommitment (baseline / Wave-2 / Wave-3 targets), SLO (soft/hard/regulatory), WaveEnvelope per Wave 1/2/3 with fee bands, CommercialModel enum (fixed_fee / value_share / hybrid), and linked_agents references resolving against Sprint 16 catalog. Validator enforces canonical service-code regex, practice-prefix match, persona/KPI/wave presence, value-share/money-KPI alignment. CLI: `apex services stats / list / inspect / validate`. 33 tests passing; integrates with Sprint 28 service-code validator via `all_service_codes()`. The Sprint 17 plan's 45/Practice exit criterion includes scenario-derived services from Sprint 28's 723-row library; the 61 anchors here cover every service named in the Sellers Guide Practice deep-dives.)*

### Task 17.1 — RC service catalog (BL.P.110)
- [x] Subtask 17.1.1 — Author 13 services from RC build spec v2 *(RC-E2E-03 Assortment, RC-E2E-04 Brand Equity, RC-E2E-05 Unified Customer, RC-E2E-06 Cold Chain, RC-E2E-07 Store Ops, RC-E2E-08 Stockout Substitution, RC-E2E-09 Product Tracking, RC-E2E-10 Promotion ROI, RC-TTP-02 Demand Sensing, RC-TTP-04 Replenishment, RC-TTP-06 Shrink, RC-TTP-07 Markdown, RC-TTP-08 Returns. Hits the §9.3 priority-five list plus the eight additional services referenced through §9.7. Remaining 30+ scenario-derived services come from Sprint 28 library at engagement time.)*
- [x] Subtask 17.1.2 — Persona / KPI / SLO per service *(every manifest carries primary persona + secondary personas, ≥1 KPI with direction + Wave-2 target band, ≥1 SLO where applicable, full Wave 1/2/3 envelope)*
- [x] Subtask 17.1.3 — Commercial-envelope metadata *(every service declares commercial_model + value_share_eligible flags; 4 RC services are value-share — Cold Chain Response, Markdown, Shrink, Returns)*

### Task 17.2 — HLS service catalog (BL.P.111)
- [x] Anchor 8 shipped — HLS-E2E-01 Claim Triage, HLS-E2E-02 Clinical Decision Support, HLS-E2E-03 Utilization Management, HLS-E2E-04 Sepsis Early Warning, HLS-LS-03 Trial Enrollment, HLS-LS-05 Adverse Event PV, HLS-PAY-01 Member 360, HLS-PAY-02 Risk Stratification. Covers all three sub-segments (Provider, Payer, Life Sciences) with PHI / Part 11 / HIPAA classification wrapping.

### Task 17.3 — ER service catalog (BL.P.112)
- [x] Anchor 8 shipped — ER-PU-01 Outage Triage, ER-PU-02 PSPS, ER-PU-03 Vegetation, ER-PU-04 DER + VPP, ER-OG-01 Well Operations, ER-OG-02 Drilling Safety, ER-OG-03 HSE Incident, ER-MN-01 Mine Fleet. Covers all three sub-segments with NERC CIP / FERC / OSHA PSM regulatory wrapping.

### Task 17.4 — AXLE service catalog (BL.P.113)
- [x] Anchor 8 shipped — AXLE-Connected-Factory-01 OEE+PdM, AXLE-Connected-Factory-02 Generative Engineering, AXLE-Aftermarket-01 Connected Vehicle, AXLE-Aftermarket-02 Warranty + Recall, AXLE-Ops-01 Production Scheduling, AXLE-Ops-03 Plant Energy, AXLE-QMS-01 Quality Defect, AXLE-Supply-01 Supplier Quality. Generative engineering on reasoning tier per Sellers Guide §12.10.3.

### Task 17.5 — TMT service catalog (BL.P.114)
- [x] Anchor 8 shipped — TMT-TEL-01 Contact Center, TMT-TEL-02 Network Ops, TMT-TEL-03 Billing Dispute, TMT-TEL-04 Fraud, TMT-TEL-05 Subscriber Churn, TMT-MED-01 Content Rights, TMT-MED-03 Content Moderation, TMT-TEC-01 SaaS SLA. CPNI regulatory wrapping on TEL services per §13.13.7.

### Task 17.6 — TH service catalog (BL.P.115)
- [x] Anchor 8 shipped — TH-AIR-01 IROPs Recovery (reasoning-tier per §14.8), TH-AIR-02 Traveler 360, TH-AIR-03 Loyalty, TH-AIR-04 Crew Scheduling, TH-AIR-05 Ground Ops, TH-AIR-07 Disruption Comms, TH-HOT-01 Yield Management, TH-HOT-02 Guest Experience.

### Task 17.7 — ICE service catalog (BL.P.116)
- [x] Anchor 8 shipped — ICE-Connected-Factory-01 Fleet Health, ICE-Aftermarket-01 Predictive Service, ICE-Aftermarket-02 Warranty Triage, ICE-Aftermarket-03 Parts Stocking, ICE-Aftermarket-04 Dealer Performance, ICE-EaaS-01 Rental, ICE-QMS-01 Emissions Compliance, ICE-Supply-01 Supply Shortage. EPA Tier 4 / EU Stage V / CARB regulatory wrapping where applicable.

---

## Sprint 18 — Reference Deployments

**Closes:** BL.P.117–P.121
**Goal:** Turnkey Wave-1 reference deployments per Practice — the "picked-up-off-the-shelf" pattern.
**Exit criteria:** Each reference has triggering scenario, solution architecture, use cases, personas, KPI targets, Wave-1 scope document, and a demo script.

### Task 18.1 — Big Box Store (RC) (BL.P.117)  ✅
- [x] Subtask 18.1.1 — Retail Operations command center  *(`big-box-store.yaml`: F128 single-tenant Fabric capacity, SAP S/4HANA + Manhattan WMS + Salesforce Marketing Cloud + Oracle EBS adapters, RC anchor agents wired across cold-chain, markdown cadence, demand sensing, replenishment, substitution, shrink detection, store-ops; SCML + CXML + MERML schemas; per Sellers Guide §16.13)*
- [x] Subtask 18.1.2 — Cold Chain Excursion Response (full end-to-end)  *(triggering scenario + use case + RC-E2E-04 service binding + `apex.rc.agents.cold-chain-response` HITL gate; KPI: cold-chain disposition decision latency under 30 minutes target)*
- [x] Subtask 18.1.3 — Markdown Cadence  *(use case + RC-E2E-05 + `apex.rc.agents.markdown-cadence` + `apex.rc.agents.assortment-pricing`; KPI: gross margin uplift +150-300 bps Wave-2)*
- [x] Subtask 18.1.4 — Demo script + sample data  *(`demo_scripts/big-box-store.md`: 4-scene 30-min walk-through with Teams-card mockups + commercial close)*

### Task 18.2 — Hospital (HLS) (BL.P.118)  ✅
- [x] Subtask 18.2.1 — Sepsis Early Warning  *(`hospital.yaml`: HLS-E2E-01 use case + `apex.hls.agents.sepsis-early-warning` HITL with charge-nurse Teams-card surface + SEP-1 bundle pre-staging; KPI: SEP-1 compliance +12-20pp Wave-2)*
- [x] Subtask 18.2.2 — Clinical Decision Support  *(`apex.hls.agents.clinical-decision-support` chained with sepsis early warning for drug-interaction/adverse-event flagging during order entry)*
- [x] Subtask 18.2.3 — Utilization Management  *(HLS-E2E-02 use case + `apex.hls.agents.utilization-management` + `apex.hls.agents.readmission-risk` for LOS-outlier identification with case-manager prioritized work-list; KPI: med-surg LOS -0.4 to -0.7 days Wave-2)*
- [x] Subtask 18.2.4 — Demo + sample data  *(`demo_scripts/hospital.md`: 5-scene CMO/CNO/CFO walk-through, F128 per-workload-isolation architecture, HIPAA + 42 CFR Part 2 audit posture, claim-triage + patient-identity supplements)*

### Task 18.3 — Utility (ER) (BL.P.119)  ✅
- [x] Subtask 18.3.1 — Outage Triage + Restoration Sequencing  *(`utility.yaml`: ER-PU-02 use case + `apex.er.agents.outage-triage` + `apex.er.agents.restoration-sequencing`; storm-driven outage scenario; KPI: SAIDI -8-12% pilot region Wave-2)*
- [x] Subtask 18.3.2 — Demand Forecasting  *(DER orchestration agent ER-PU-04 covers demand-side dispatch under peak/constraint events; vegetation-risk + AMI billing-anomaly + PSPS decision agents round out 5-use-case coverage; KPI: vegetation defect-find rate +30-50%; PSPS audit completeness 100%; AMI RCA cycle -50%; Sellers Guide §11.9; CIP-014 + critical-infrastructure classifications)*

### Task 18.4 — Plant (AXLE) (BL.P.120)  ✅
- [x] Subtask 18.4.1 — Connected Factory  *(`plant.yaml`: AXLE-Connected-Factory-01 use case + `apex.axle.agents.oee-monitor` + `apex.axle.agents.andon-rca` for OEE attribution + closed-loop improvement on flagship line; F128 OT/IT workload isolation; KPI: OEE +5-8pp pilot Wave-2)*
- [x] Subtask 18.4.2 — Predictive Maintenance  *(AXLE-Connected-Factory-02 use case + `apex.axle.agents.predictive-maintenance` with HITL work-order release back to SAP S/4HANA via mirrored adapter; KPI: unplanned downtime -20-30%)*
- [x] Subtask 18.4.3 — Quality Optimization  *(AXLE-QMS-01 use case + `apex.axle.agents.quality-defect` + `apex.axle.agents.supplier-quality` for vision/SPC defect cluster detection + supplier corrective-action draft; warranty-cost + production-scheduling + energy-optimization complete the 6-use-case set; demo script `demo_scripts/plant.md` per Sellers Guide §12.9A)*

### Task 18.5 — Airline (TH) (BL.P.121)  ✅
- [x] Subtask 18.5.1 — IROP Recovery  *(`airline.yaml`: TH-AIR-01 use case + `apex.th.agents.irops-recovery` reasoning-tier (o1) + `apex.th.agents.crew-scheduling` + `apex.th.agents.disruption-comms`; hub-station closure scenario; KPI: IROPS recovery cycle time median 35 minutes Wave-2)*
- [x] Subtask 18.5.2 — Crew Scheduling  *(crew-scheduling agent integrated into IROPS recovery for legality-aware swaps + deadhead-rebook; F128 per-workload-isolation separates ops-control from commercial)*
- [x] Subtask 18.5.3 — Revenue Optimization  *(TH-AIR-02 use case + `apex.th.agents.yield-management` + `apex.th.agents.demand-disruption` with competitor watch + corporate-contract protection; traveler-360 + loyalty-personalization for elite retention; ground-ops + guest-experience round out 5 use cases; demo script `demo_scripts/airline.md` per Sellers Guide §14.8)*

**Sprint 18 deliverables shipped:**
- `packages/apex-references/` Python package (Sprint 18 framework + 5 reference manifests + 5 demo scripts)
  - `framework.py` — `ReferenceSpec` Pydantic model with `TriggeringScenario`, `SolutionArchitecture`, `UseCase`, `KpiTarget`, `Wave1Scope` sub-models; loader, scanner, validator with cross-reference checks against Sprint 15 adapters / Sprint 16 agents / Sprint 17 service codes; demo-script loader
  - `catalogs/big-box-store.yaml` (RC, F128, single-capacity-tenant, $0.75-1.5M Wave-1, 8-12 weeks)
  - `catalogs/hospital.yaml` (HLS, F128, per-workload-isolation, $1.0-1.75M Wave-1, 10-14 weeks)
  - `catalogs/utility.yaml` (ER, F128, dev-prod-split, $1.0-2.0M Wave-1, 10-14 weeks)
  - `catalogs/plant.yaml` (AXLE, F128, per-workload-isolation OT/IT, $0.85-1.75M Wave-1, 8-12 weeks)
  - `catalogs/airline.yaml` (TH, F128, per-workload-isolation ops-control/commercial, $0.9-1.75M Wave-1, 8-12 weeks)
  - `demo_scripts/{big-box-store,hospital,utility,plant,airline}.md` — 30-minute executive demo narratives with Teams-card mockups + Wave-1 commercial close per Sellers Guide §10.9 / §11.9 / §12.9A / §14.8 / §16.13
  - `_cli.py` exposing `apex references stats|list|inspect|demo|validate` (wired into root `apex` CLI via `apex-core/cli.py`)
  - 37 tests passing (manifest correctness, validator, CLI, per-reference anchor presence, conformance) including cross-reference resolution against the live agent / service / adapter catalogs (61 service codes + 70 agents + 15 adapters all resolved cleanly)
- All 5 reference manifests `validate_references()` cleanly with full upstream cross-reference (zero errors, zero warnings)

---

## Sprint 19 — Registries, Playbooks & Appendices

**Closes:** BL.P.122–P.133
**Goal:** Complete the normative reference set (Appendices A–K) and per-Practice Wave playbooks.
**Exit criteria:** Every appendix in the APEX documentation set is published and linkable from `APEX_Design.md`.

### Task 19.1 — Master registries (BL.P.122, P.123, P.124, P.125, P.126)  ✅
- [x] Subtask 19.1.1 — KPI master registry (Appendix C)  *(`apex-registries/kpis/`: 134 KPI manifests harvested from Sprint 16 agent KpiTargets + Sprint 17 service KpiCommitments; each entry carries practice, direction, baseline, Wave-2/Wave-3 targets, measurement_pattern, units, cadence; cross-validates against agents/services via `validate_registries(agents_kpi_names=…, services_kpi_names=…)`)*
- [x] Subtask 19.1.2 — Persona catalog (Appendix E)  *(`apex-registries/personas/`: 147 Persona manifests harvested from Sprint 16 agent personas + Sprint 17 service personas + Sprint 18 reference sponsor_personas; each entry carries seniority (c-suite / svp / vp / director / manager / IC), function, typical_decisions, pains, metrics_owned)*
- [x] Subtask 19.1.3 — MCP tool catalog (Appendix F)  *(`apex-registries/mcp_tools/`: 168 McpToolEntry manifests harvested from Sprint 16 agent ToolBindings; each entry carries practice, sor_or_layer (e.g., scml, patientml, gridml), purpose, write flag, classification_required, related_canonical_schemas)*
- [x] Subtask 19.1.4 — Schema reference (Appendix A)  *(`apex-registries/schemas/`: 49 SchemaEntry manifests covering SCML / CXML / MERML (RC), PatientML / ClaimML / EncounterML / StudyML / MEDML / PopHealthML / ProvML (HLS), GridML / OutageML / MeterML / DERMML / UOGML / DrillingML / MiningML / HSEML / PUML (ER), QMSML / AAML / MSCML / EngML / EquipML / AftermarketML (AXLE), BSSML / SubscriberML / ContentSafetyML / NetworkML / RightsML (TMT), OpsML-TH / TravelerML / RevML-TH / InvML-TH / LoyaltyML / IROPsML / GroundML (TH), AMML-ICE / ConnectedICEML / ConnectedProductML / DealerML / SupplyML-A / SupplyML-ICE / QMSML-ICE / TECML / TELML / CCML (ICE/cross); each carries primary_entities, standards_alignment, governance_classification, package_implementation reference)*
- [x] Subtask 19.1.5 — Orchestration catalog — all 47 archetypes documented (Appendix D)  *(`apex-registries/archetypes/`: exactly 47 ArchetypeEntry manifests across 16 families (triage, cascade, rca, recovery, personalize, optimize, monitor, predict, schedule, match, translate, summarize, explain, score, negotiate, compose) — e.g., `arch.recovery.001` IROPS Recovery (reasoning-tier, HITL), `arch.match.001` Identity Resolution, `arch.score.001` Risk Score, `arch.explain.002` Regulatory Explanation; each carries canonical_inputs/outputs, typical_hitl_gate, typical_oversight, typical_model_tier, example_agents from Sprint 16)*

### Task 19.2 — Product & partner references (BL.P.127, P.128, P.129, P.130)  ✅
- [x] Subtask 19.2.1 — Microsoft product & SKU reference (Appendix G)  *(`apex-registries/products/`: 27 ProductEntry manifests covering Fabric F-SKUs (F64/F128/F256/F512 + Mirroring + Real-Time Intelligence), Foundry models (gpt-4o / gpt-4o-mini / o1 / text-embedding-3-large), Copilot Studio (Standard + Agent Builder Kit), Purview (Data Map + Compliance Manager + Audit Premium), Defender (for Cloud P2 + for Endpoint P2), Entra (ID P2 + Workload Identities), Intune Suite, Teams Premium, Power Platform, Azure OpenAI fallback, Azure ML, GitHub Copilot Business, ADLS Gen2, Azure Private Endpoints; each tags list_price_basis + typical_use + apex_role linking back to Sprint 14/16/18)*
- [x] Subtask 19.2.2 — Partner ecosystem catalog (Appendix H)  *(`apex-registries/partners/`: 20 PartnerEntry manifests across SOR vendors (SAP, Oracle, Salesforce, Epic, Workday, ServiceNow, Sabre, Amadeus, GE Digital, OSIsoft/AVEVA, Manhattan, Snowflake, Databricks), model providers (OpenAI, Anthropic), data providers (dunnhumby), ISVs (Veeva), infrastructure (AWS, GCP), and delivery partners (Deloitte In-Vehicle Practice); each carries practices, integration pattern (mirrored-db-via-Sprint15-adapter / API-via-Sprint15-adapter / etc.) and contracts_in_place)*
- [x] Subtask 19.2.3 — Independence & competitive posture (Appendix K)  *(`apex-registries/competitive/`: 10 CompetitiveEntry manifests covering Big-4 (PwC, KPMG, EY), tech-led-consult (Accenture+CFC, IBM+watsonx, Capgemini, BCG-X, McKinsey QuantumBlack), and cloud-native (Databricks Mosaic, Snowflake Cortex); each carries apex_differentiators, independence_concerns, win_themes — Deloitte audit-relationship constraints flagged where they bound APEX engagement scope)*
- [x] Subtask 19.2.4 — Exercise solutions (Appendix J)  *(`apex-registries/exercises/`: 10 ExerciseEntry manifests with canonical solutions to representative Sellers Guide chapter exercises spanning Practice deep-dives §10.3 / §10.5 / §11.4 / §12.2 / §13.6 / §14.4 / §15.3 / §16.7 plus foundations §2.6 (commercial-model selection) and §6.10 (audit-row contract); each carries teaching_points and related_kpi_ids / related_archetype_ids cross-links)*

### Task 19.3 — Wave delivery playbooks per Practice (BL.P.131)  ✅
- [x] Subtask 19.3.1 — RC Wave 1 / 2 / 3 playbook  *(`apex-registries/playbooks/rc.md`: Wave-1 ($0.75-1.5M / 4-12 wks) / Wave-2 ($2-6M / 6-12 mo) / Wave-3 (24+ mo retainer) with anchor-agent selection guidance (cold-chain / markdown / demand-sense / shrink), exit criteria, KPI commitments per Wave, cross-references to Sprint 14/15/16/17/18 RC artifacts)*
- [x] Subtask 19.3.2 — HLS, ER, AXLE, TMT, TH, ICE (six more playbooks)  *(`apex-registries/playbooks/{hls,er,axle,tmt,th,ice}.md`: each follows the RC pattern — Wave-1 envelopes ($0.75-2.0M / 8-14 wks), Wave-2 scale-up plans, Wave-3 mature-ops; HLS adds HIPAA + 42 CFR Part 2 audit posture; ER adds CIP-014 + PSPS regulator-grade audit; AXLE adds OT/IT isolation + warranty value-share; TMT adds IVT recovery + DORA metrics; TH adds reasoning-tier IROPS + yield value-share; ICE adds connected-product telemetry + dealer-mgmt patterns)*

### Task 19.4 — Discovery + pre-clearance (BL.P.132, P.133)  ✅
- [x] Subtask 19.4.1 — Discovery prompt templates per Practice  *(`apex-registries/discovery/{rc,hls,er,axle,tmt,th,ice}.md`: 7 markdown discovery-prompt sets; each set has triggering-event probes mapped to Sprint 18 reference-deployment use cases, architecture/data probes for SOR + canonical-schema selection, audit/governance probes (FSMA 204 / HIPAA / 42 CFR Part 2 / CIP-014 / PCI / GDPR as Practice-relevant), and commercial probes for value-share qualification + Wave-1 envelope shape)*
- [x] Subtask 19.4.2 — Pre-clearance checklists (technical / legal / compliance)  *(`apex-registries/preclearance/{technical,legal,compliance}-checklist.md`: Technical covers Fabric F-SKU + adapter + canonical-schema + Foundry + identity + audit/telemetry + agent-runtime readiness gates; Legal covers Deloitte-independence (DSE routing for value-share where audit-relationship constrains scope) + IP ownership + model-provider terms + data rights + commercial structure; Compliance covers per-Practice regulatory posture (FSMA 204 / HIPAA / 42 CFR Part 2 / CIP-014 / FERC / NERC / PUC / IATF 16949 / FDA Part 820 / IEC 62443 / DOT tarmac-rule / etc.) + cross-cutting Sprint 13 governance + HITL placement validation)*

**Sprint 19 deliverables shipped:**
- `packages/apex-registries/` Python package (Sprint 19 Master Registries + Wave Playbooks + Discovery + Pre-clearance)
  - `framework.py` — `KpiEntry`, `PersonaEntry`, `McpToolEntry`, `SchemaEntry`, `ArchetypeEntry`, `ProductEntry`, `PartnerEntry`, `CompetitiveEntry`, `ExerciseEntry` Pydantic models with shared `RegistryEntry` / `RegistryReport` / `validate_registries()` infrastructure; loader, scanner, validator with cross-reference checks against Sprint 16/17 catalogs
  - `harvest.py` + `_emit_schemas.py` + `_emit_archetypes.py` + `_emit_appendices_ghjk.py` — one-time generators that build the 612-entry registry from existing catalogs + hand-authored canonical references
  - **Total: 612 registry entries shipped** (134 KPIs + 147 personas + 168 MCP tools + 49 schemas + 47 archetypes + 27 products + 20 partners + 10 competitive + 10 exercises)
  - **7 Wave playbooks** covering all 7 Practices (RC, HLS, ER, AXLE, TMT, TH, ICE) with Wave-1/2/3 envelopes, anchor-agent selection guidance, KPI commitments per Wave, exit criteria
  - **7 discovery-prompt sets** mapped to Sprint 18 reference deployment use cases + Practice-specific regulatory probes
  - **3 pre-clearance checklists** (technical / legal / compliance) covering Sprint 14-18 readiness, Deloitte-independence + IP + model-provider terms, and per-Practice regulatory posture
  - `_cli.py` exposing `apex registries stats|list|inspect|playbook|discovery|preclearance|validate` (wired into root `apex` CLI via `apex-core/cli.py`)
  - 42 tests passing covering model validation, manifest correctness, registry coverage targets, markdown asset coverage, validator (zero errors with full Sprint 16/17 cross-references resolved), CLI commands, and conformance markers
- Cross-package suite: 221 of 222 tests passing across apex-core / apex-agents / apex-services / apex-references / apex-registries / apex-adapters (the one failure is the same pre-existing apex_scenarios-not-installed environment issue, unrelated to Sprint 19)

---

## Sprint 20 — Industry Standards: Registry & CLI Foundation

**Closes:** BL.P.134, P.135, P.136, P.137, P.138
**Goal:** Ship the standards-registry foundation inside `apex-schemas-common` so every per-standard package (Sprint 21) and every binding (Sprint 22) has a common contract.
**Status:** ✅ Complete — BL.P.134 / P.135 / P.136 landed in Sprint 2 / Sprint 3 Phase 1; BL.P.137 (catalog.yaml + drift detection) and BL.P.138 (licence attribution + restricted-terminology guardrail) shipped 2026-05-05.
**Exit criteria:** `standards/catalog.yaml` is machine-readable, round-trips through the registry, and every `apex-standards-*` package carries a per-package licence file.
**Design reference:** `Industry-Standards-Incorporation-Plan.md` §5–§6.

### Task 20.1 — `apex-schemas-common.standards` module (BL.P.134) ✅
- [x] Subtask 20.1.1 — `StandardSpec`, `StandardRef`, `STANDARDS` registry
- [x] Subtask 20.1.2 — `introspect()` helper for discovery
- [x] Subtask 20.1.3 — Landed in Sprint 2

### Task 20.2 — `apex standards` CLI (BL.P.135) ✅
- [x] Subtask 20.2.1 — `apex standards list | show | audit | bump` subcommands
- [x] Subtask 20.2.2 — Auto-attached to `apex` CLI via conditional import in `apex-schemas-common/_cli.py`

### Task 20.3 — `conformance` CI lane (BL.P.136) ✅
- [x] Subtask 20.3.1 — `pytest` `conformance` marker
- [x] Subtask 20.3.2 — `apex standards audit` step in `.github/workflows/ci.yml`
- [x] Subtask 20.3.3 — `pytest -m conformance` lane

### Task 20.4 — `standards/catalog.yaml` (BL.P.137)  ✅
- [x] Subtask 20.4.1 — Define machine-readable catalog schema  *(`apex_schemas_common.standards.catalog`: catalog YAML schema mirrors `StandardSpec` exactly so rows round-trip; `kind: apex.standards.catalog` + `version: 1` envelope; per-row fields = id / name / authority / authority_url / type / current_version / apex_pinned_version / license / redistribution_ok / pattern / supporting_package / practices / notes; ordering stable for reviewable diffs)*
- [x] Subtask 20.4.2 — Populate catalog entries for all registered standards  *(`packages/apex-schemas-common/src/apex_schemas_common/standards/catalog.yaml`: 24 standards emitted from in-memory `STANDARDS` registry covering GS1 GTIN/SSCC/GLN/EPCIS, Schema.org, HL7 FHIR R4 + LOINC/ICD-10/NDC/SNOMED-CT/CPT/HCPCS/RxNorm, ISA-95, SAE J1939, TM Forum SID, IATA NDC, EIDR, ISO 14224, IEC 61970/61968 CIM, OpenTravel, CDISC ODM/SDTM)*
- [x] Subtask 20.4.3 — `apex standards sync-catalog` loads from YAML into the in-memory registry  *(`apex standards sync-catalog` writes `catalog.yaml` from STANDARDS; `--check` flag exits 1 on drift for CI use; complementary `apex standards validate-catalog` runs structural + drift validation)*
- [x] Subtask 20.4.4 — CI check: every `@standard` registration has a corresponding catalog row, and vice versa  *(`check_catalog_drift()` returns `CatalogDriftReport` with `CATALOG_MISSING_ROW` (code-registered missing from YAML), `CODE_MISSING_REGISTRATION` (YAML-only zombie row), `FIELD_MISMATCH` (per-field disagreement); wired into `.github/workflows/ci.yml` conformance lane as `apex standards sync-catalog --check`; 17 catalog tests passing including round-trip + drift-injection negative tests)*

### Task 20.5 — Licence attribution framework (BL.P.138)  ✅
- [x] Subtask 20.5.1 — `LICENSE-ATTRIBUTION.md` template at workspace root  *(`LICENSE-ATTRIBUTION.md` at repo root: workspace-level attribution manifest enumerating all 20 industry standards APEX references, per-standard authority + binding pattern + license + redistribution posture, cross-pointers to per-package files, restricted-terminology guardrail policy, open-source license posture for framework code)*
- [x] Subtask 20.5.2 — Per-`apex-standards-*` package licence file  *(`LICENSE-ATTRIBUTION.md` shipped in all 8 standards packages: `apex-standards-cdisc` (ODM 2.0 + SDTM 2.0 open + MedDRA/WHODrug regex-only), `apex-standards-cim` (IEC 61970/61968 restricted, structural mirror only), `apex-standards-fhir` (existing — HL7 FHIR R4 CC0 + LOINC/SNOMED/CPT regex-only), `apex-standards-isa95` (ISA-95 royalty-free for impl, no standard-text redistribution), `apex-standards-iso14224` (ISO 14224 restricted, taxonomy mirror only), `apex-standards-j1939` (existing — SAE J1939 restricted), `apex-standards-opentravel` (OTA 2025A open), `apex-standards-sid` (TM Forum SID 22.5 open))*
- [x] Subtask 20.5.3 — CI lint: every `apex-standards-*` package fails without a licence file  *(`tools/check_standards_licences.py` walks `packages/apex-standards-*`, fails build if `LICENSE-ATTRIBUTION.md` missing; wired into `.github/workflows/ci.yml` conformance lane; 5 licence-presence tests passing)*
- [x] Subtask 20.5.4 — Restricted-terminology guardrail  *(`tools/check_restricted_terminology.py` scanner with two detection modes: filename patterns (`loinc.csv`, `snomed_*.txt`, `icd10cm_*.zip`, `iso14224.pdf`, `iec6197[08].pdf`, `j1939.pdf`, etc.) and content fingerprints (LOINC table CSV header, SNOMED RF2 release filenames, ICD-10-CM tabular preamble, CPT licence preamble); allowlist for `LICENSE-ATTRIBUTION.md` / `README.md` / `CHANGELOG.md` so attribution files may legitimately mention restricted standards by name; auto-skips `__pycache__` / `.git` / `node_modules`; wired into CI as `python tools/check_restricted_terminology.py packages/`; 9 guardrail tests passing including positive negative-case detection)*

**Sprint 20 deliverables shipped:**
- `apex_schemas_common.standards.catalog` module — machine-readable catalog round-trip + drift detection (`CatalogIssue`, `CatalogDriftReport`, `emit_catalog`, `write_catalog`, `load_catalog`, `check_catalog_drift`)
- `packages/apex-schemas-common/src/apex_schemas_common/standards/catalog.yaml` — 24-row machine-readable standards catalog (~7.8 KB)
- `apex standards sync-catalog [--check]` and `apex standards validate-catalog` CLI subcommands wired into `apex` root via existing `apex-schemas-common._cli` import probe in `apex-core/cli.py`
- `LICENSE-ATTRIBUTION.md` at workspace root + 6 new per-package attribution files (cdisc, cim, isa95, iso14224, opentravel, sid) joining the 2 existing (fhir, j1939) — full licence attribution for all 8 `apex-standards-*` packages
- `tools/check_standards_licences.py` — CI-runnable per-package licence presence check
- `tools/check_restricted_terminology.py` — CI-runnable restricted-content scanner (filename + content fingerprint detection, allowlist-aware)
- `.github/workflows/ci.yml` updated with three new conformance steps: catalog sync check + per-package licence check + restricted-terminology scan
- 31 new tests passing (17 catalog round-trip / drift-detection + 14 guardrail tests including conformance markers); cross-package suite at 271 of 272 (one pre-existing apex_scenarios environment issue, unrelated)

---

## Sprint 21 — Per-Standard Packages (Phase 1 Complete)

**Closes:** BL.P.139, P.140, P.141, P.142, P.143, P.144, P.145, P.146
**Goal:** Each major standard ships as its own `apex-standards-*` package with a pinned version, a binding layer, conformance tests, and a licence file.
**Status:** Phase 1 complete — all eight packages landed in Sprint 3 Phase 1.
**Exit criteria:** Every package imports cleanly, registers in the standards catalog, and passes round-trip conformance tests where applicable.
**Design reference:** `Industry-Standards-Incorporation-Plan.md` §6 per-standard matrix.

### Task 21.1 — `apex-standards-fhir` (BL.P.139) ✅
- [x] Subtask 21.1.1 — R4 mirror — 7 resources + 9 primitives
- [x] Subtask 21.1.2 — R5 skeleton
- [x] Subtask 21.1.3 — R4→R5 migration stub
- [x] Subtask 21.1.4 — Terminology `TerminologyService` protocol + `MockTerminologyService`

### Task 21.2 — `apex-standards-cim` (BL.P.140) ✅
- [x] Subtask 21.2.1 — IEC 61970 + 61968 subset for ER Practice

### Task 21.3 — `apex-standards-isa95` (BL.P.141) ✅
- [x] Subtask 21.3.1 — Equipment Hierarchy + Personnel + Material
- [x] Subtask 21.3.2 — Shared across ER / AXLE / ICE

### Task 21.4 — `apex-standards-sid` (BL.P.142) ✅
- [x] Subtask 21.4.1 — TM Forum SID 7-domain model for TMT

### Task 21.5 — `apex-standards-opentravel` (BL.P.143) ✅
- [x] Subtask 21.5.1 — OTA Air / Hotel / Car message skeletons for TH

### Task 21.6 — `apex-standards-cdisc` (BL.P.144) ✅
- [x] Subtask 21.6.1 — ODM + SDTM DM/AE/LB skeletons

### Task 21.7 — `apex-standards-iso14224` (BL.P.145) ✅
- [x] Subtask 21.7.1 — Reliability taxonomy + failure modes + record type (shared AXLE/ICE)

### Task 21.8 — `apex-standards-j1939` (BL.P.146) ✅
- [x] Subtask 21.8.1 — SPN/PGN seed registry
- [x] Subtask 21.8.2 — CAN frame model (shared AXLE/ICE)

### Task 21.9 — Phase 2 per-standard packages (Phase 1 satisfied via Sprint 23/25)
- [x] Subtask 21.9.1 — EPCIS coverage  *(BL.P.158 satisfied via `apex_translators.epcis` parser/emitter shipped 2026-05-05; standalone `apex-standards-epcis` package not required because the canonical EPCIS bindings live in `apex-translators` and reference the `epcis` standard already registered in `STANDARDS`)*
- [x] Subtask 21.9.2 — IEC 61850 coverage  *(BL.P.167 satisfied via `apex_protocols.iec61850` SCD parser + MMS client + GOOSE/SV metadata shipped 2026-05-05; standalone `apex-standards-iec61850` package not required because the SCL XML parsing + LN/DO/DA address-space lives in `apex-protocols.iec61850`)*
- [x] Subtask 21.9.3 — OPC UA coverage  *(BL.P.166 satisfied via `apex_protocols.opcua` NodeSet parser + stub client + TLS/cert config shipped 2026-05-05; standalone `apex-standards-opcua` package not required because the address-space mapping lives in `apex-protocols.opcua`)*

---

## Sprint 22 — Identifier & Terminology Bindings

**Closes:** BL.P.147, P.148, P.149, P.150, P.151, P.152, P.153, P.154
**Goal:** Every canonical entity that claims a standard binding validates at runtime and at CI time. Bindings are regex + lookup hook; vocabulary content is never redistributed.
**Status:** ✅ Complete — identifier bindings (GS1, HLS codes, TMT EIDR, J1939 SPN/PGN) and terminology lookup protocols for SNOMED / LOINC / RxNorm shipped in Sprint 3 Phase 1; ISO 8000 master-data-quality binding (P.154) shipped 2026-05-05.
**Exit criteria:** Every bound field in the canonical schemas has a passing conformance test; restricted terminologies have a working lookup-hook interface with a mock implementation.
**Design reference:** `Industry-Standards-Incorporation-Plan.md` §4 Pattern A.

### Task 22.1 — RC identifier bindings (BL.P.147) ✅
- [x] Subtask 22.1.1 — GS1 GTIN-8 / 12 / 13 / 14 regex bindings
- [x] Subtask 22.1.2 — SSCC, GLN bindings
- [x] Subtask 22.1.3 — Integrated into `apex-schemas-common.standards.types`

### Task 22.2 — HLS identifier bindings (BL.P.148) ✅
- [x] Subtask 22.2.1 — ICD-10, ICD-11, CPT, HCPCS, NDC, RxNorm, SNOMED-CT, LOINC regex bindings
- [x] Subtask 22.2.2 — Registered in `STANDARDS`
- [x] Subtask 22.2.3 — Used by `PatientML`, `ClaimML` entity code

### Task 22.3 — ICE / AXLE identifier bindings (BL.P.149) ✅
- [x] Subtask 22.3.1 — J1939 SPN/PGN seed registries + loader hooks
- [x] Subtask 22.3.2 — AEMP 2.0 field bindings (staged for Phase 2 alongside ICEML entity work)

### Task 22.4 — TMT identifier bindings (BL.P.150) ✅
- [x] Subtask 22.4.1 — EIDR content-identifier binding

### Task 22.5 — Terminology lookup protocols (BL.P.151, P.152, P.153) ✅
- [x] Subtask 22.5.1 — SNOMED CT binding + `TerminologyService` protocol
- [x] Subtask 22.5.2 — LOINC binding + lookup hook
- [x] Subtask 22.5.3 — RxNorm binding + lookup hook
- [x] Subtask 22.5.4 — `MockTerminologyService` reference implementation

### Task 22.6 — ISO 8000 master-data-quality binding (BL.P.154)  ✅
- [x] Subtask 22.6.1 — Design binding at the `StandardSpec` level — data-quality dimensions  *(`STANDARDS["iso-8000"]` registry entry — authority ISO, type `data_model`, pattern B (data model mirror), pinned ISO 8000-61:2016, license `restricted`, redistribution_ok=False, practices include all 7 (universal); registry expanded from 24 → 25 standards; catalog.yaml regenerated cleanly via `apex standards sync-catalog`. Dimensions: completeness, consistency, accuracy, currency, provenance, conformance — six ISO-8000-aligned dimensions enumerated as `QualityDimension` StrEnum)*
- [x] Subtask 22.6.2 — Attach binding to canonical envelope fields  *(new `apex_core.quality` module: `DataQualityMetadata` Pydantic model (frozen, extra=forbid) with six per-dimension Optional[float] in [0,1] + `iso8000_pinned_version` (default "8000-61:2016") + `quality_assessed_at`; helper methods `composite_score()` (equal-weight mean ignoring None), `is_fully_assessed()`, `degraded_dimensions(threshold=0.7)`. `apex_core.envelope.CanonicalEnvelope.quality` field added with `default_factory=DataQualityMetadata` for backward compat with all existing callers. Two new module-level constants: `CORE_ENVELOPE_FIELDS` (the original 5) and `ENVELOPE_FIELDS` (now 6, includes `quality`). `apex_core.__init__` exports the new types)*
- [x] Subtask 22.6.3 — Conformance test that every Silver table row has ISO-8000-aligned quality metadata  *(`apex-core/tests/test_quality.py`: 29 tests covering dimension enum, range validation per-dimension (rejects <0 and >1), default-state correctness, composite score (equal-weight mean ignoring None), `is_fully_assessed`, `degraded_dimensions` threshold logic + None-skip semantics, frozen + extra-forbid, plus 3 conformance-marked tests asserting envelope carries the block, ISO 8000 in registry, and pinned version drift-check between registry and metadata default. `apex-core/tests/test_envelope.py` updated: `test_envelope_fields_includes_quality_block`, `test_envelope_quality_defaults_to_empty_block`, `test_envelope_accepts_explicit_quality_block`. 37/37 quality+envelope tests passing)*
- [x] Subtask 22.6.4 — Document in `apex-core/conventions/iso-8000.md`  *(new `packages/apex-core/conventions/iso-8000.md`: full convention doc covering what APEX implements vs. what is NOT redistributed, where the metadata lives in the envelope, per-dimension scoring algorithms (completeness ratio, consistency ratio, accuracy via authoritative-reference round-trip, currency staleness decay, provenance categorical mapping, conformance via StandardRef binding success-rate), composite + degraded-helper usage, conformance-test pointer, cross-references, pin-bump procedure)*

**Sprint 22 Task 22.6 deliverables shipped:**
- `apex_core.quality` module — `DataQualityMetadata` + `QualityDimension` enum + `QUALITY_FIELDS` constant; six ISO-8000-aligned dimensions, frozen Pydantic v2 model, helper methods (`composite_score`, `is_fully_assessed`, `degraded_dimensions`)
- `apex_core.envelope.CanonicalEnvelope.quality` field — embedded `DataQualityMetadata` with `default_factory` for backward compat; `CORE_ENVELOPE_FIELDS` (original 5) + `ENVELOPE_FIELDS` (now 6) constants
- `STANDARDS["iso-8000"]` registry entry — 25 standards in catalog (was 24); pattern B, restricted licence, all 7 Practices
- Regenerated `packages/apex-schemas-common/src/apex_schemas_common/standards/catalog.yaml` (drift = 0)
- `packages/apex-core/conventions/iso-8000.md` convention doc
- 29 new quality tests + 4 new envelope tests; cross-package suite at 303 of 304 (one pre-existing apex_scenarios env issue, unrelated)

---

## Sprint 23 — Message-Format Translators

**Closes:** BL.P.155, P.156, P.157, P.158, P.159, P.160
**Goal:** Ship bidirectional message-format translators so enterprise SORs (speaking EDI, HL7 v2, CDA, EPCIS, OAGIS, IATA PADIS) integrate to APEX canonical Silver without bespoke engineering per engagement.
**Status:** ✅ Complete — full bidirectional translator package shipped in `apex-translators` 2026-05-05; supersedes the Sprint 9 `edi-mcp` stubs.
**Exit criteria:** Each translator has parser + emitter + round-trip conformance tests + error-semantics runbook. Golden fixtures cover ≥3 real-world message variants per format.
**Design reference:** `Industry-Standards-Incorporation-Plan.md` §4 Pattern D.

### Task 23.1 — EDI X12 parser/emitter (BL.P.155)  ✅
- [x] Subtask 23.1.1 — Retail set: 850 (PO), 856 (ASN), 810 (invoice), 820 (remittance)  *(`apex_translators.edi_x12`: all 4 RC transaction sets parse + emit; golden fixtures in `apex_translators.fixtures.fixtures_data.EDI_X12_FIXTURES`)*
- [x] Subtask 23.1.2 — HLS set: 837 (claim), 835 (remittance advice), 270 (eligibility inquiry), 271 (eligibility response)  *(all 4 HLS transaction sets parse + emit; HIPAA implementation guides 005010X222A1 / X221A1 / X279A1 supported via standard ST envelope)*
- [x] Subtask 23.1.3 — Segment-level parser (ISA / GS / ST / SE / GE / IEA envelopes)  *(`EDIX12Parser` walks the full envelope hierarchy; `iter_transaction_sets()` helper yields ST..SE pairs in document order; envelope metadata extracted to `ParsedMessage.{sender, receiver, control_number, version, sent_at, message_type}`)*
- [x] Subtask 23.1.4 — Emitter with configurable delimiters (*, ~, :, ^)  *(`EDIX12Emitter` honors delimiters captured in `metadata['delimiters']` from the parser; auto-detect from ISA[3] (element), ISA[82] (repetition), ISA[104] (component), ISA[105] (segment terminator); explicit `EDIX12Delimiters` override available)*
- [x] Subtask 23.1.5 — Round-trip conformance tests against golden fixtures per message type  *(8 transaction sets × 3 round-trip tests each = 24 X12 round-trip assertions; round-trip preserves segment names + element values; conformance-marked test asserts all 8 RC+HLS named transactions present)*

### Task 23.2 — HL7 v2.x parser/emitter (BL.P.156)  ✅
- [x] Subtask 23.2.1 — MLLP framing  *(`wrap_mllp(text) → bytes` and `strip_mllp(framed) → str` helpers — start byte `\x0b`, end bytes `\x1c\r`; `strip_mllp` is no-op-safe on already-unframed payloads; round-trip tested)*
- [x] Subtask 23.2.2 — Segment library (MSH, PID, PV1, OBX, OBR, ORC, RXE, AL1)  *(`SUPPORTED_SEGMENTS` exposes the named set; conformance-marked test asserts all 8 segments appear across the fixture corpus)*
- [x] Subtask 23.2.3 — v2.5.1 and v2.7 variants  *(parser auto-detects MSH-1 field separator + MSH-2 encoding chars; ADT^A04 and ORU^R01 fixtures pin v2.5.1, ORM^O01 fixture pins v2.7; both versions round-trip identically through `parse_hl7v2` → `emit_hl7v2`)*
- [x] Subtask 23.2.4 — Round-trip test fixtures  *(3 fixtures with 3 round-trip tests each = 9 HL7 v2 round-trip assertions; envelope metadata extraction tested for sender / receiver / message control id / version / DTM)*

### Task 23.3 — HL7 CDA / C-CDA parser (BL.P.157)  ✅
- [x] Subtask 23.3.1 — Structured body parser (Consolidated CDA templates)  *(`apex_translators.cda.parser`: stdlib `xml.etree.ElementTree`-based parser with 10 MB XML-bomb guard; recognizes 11 C-CDA section template OIDs across the standard set + non-fatal handling of missing structuredBody)*
- [x] Subtask 23.3.2 — Section extractor (Allergies, Medications, Problems, Results)  *(per-section `Segment` with `data` carrying `section_code`, `section_display`, `template_oids`, `free_text`, and structured `entries[]` with code/code_system/display/value extracted from `<observation>` elements; conformance test asserts all 4 named sections found in CCD fixture)*
- [x] Subtask 23.3.3 — One-way (CDA → canonical) is sufficient for v1  *(no emitter exposed; tests cover patient-demographics extraction, all-named-sections present, structured entries with terminology codes, malformed XML rejection, non-CDA root rejection)*

### Task 23.4 — EPCIS event parser/emitter (BL.P.158)  ✅
- [x] Subtask 23.4.1 — EPCIS 2.0 JSON + XML parsers (Object, Aggregation, Transaction, Transformation events)  *(`apex_translators.epcis.parser`: format-sniff (first non-whitespace = `{`/`[` → JSON; `<` → XML); JSON-LD parser walks `epcisBody.eventList`; XML parser iterates over recognized event-type element names regardless of namespace prefix; `EPCIS_EVENT_TYPES` covers ObjectEvent / AggregationEvent / TransactionEvent / TransformationEvent / AssociationEvent (2.0 addition))*
- [x] Subtask 23.4.2 — Binding to SCML Lot / Shipment entities  *(per-event JSON populated into `Segment.data` with `epcList`, `parentID`, `childEPCs`, `bizStep`, `disposition`, `bizTransactionList` fields preserved; downstream Bronze→Silver loader reads these into SCML Lot/Movement/Shipment entities; conformance test confirms all 4 event types supported in registry)*
- [x] Subtask 23.4.3 — Foundation for FSMA 204 traceability orchestrations  *(every parsed event surfaces the `bizStep` + `disposition` URIs that drive FSMA 204 traceability-event semantics; round-trip JSON emit lets agents emit downstream EPCIS events on disposition decisions)*

### Task 23.5 — OAGIS message parser/emitter (BL.P.159)  ✅
- [x] Subtask 23.5.1 — Core Business Object Document (BOD) envelope parser  *(`apex_translators.oagis.parser`: stdlib XML-based parser; auto-decomposes root tag (e.g., `ProcessItem` → verb=`Process`, noun=`Item`); recognizes 10 canonical verbs (`Get`, `Show`, `Process`, `Acknowledge`, `Sync`, `Confirm`, `Notify`, `Cancel`, `Update`, `Change`); extracts ApplicationArea (Sender/LogicalID, CreationDateTime, BODID) + DataArea contents)*
- [x] Subtask 23.5.2 — Common nouns (Item, Carrier, Manufacturing Facility)  *(3 fixtures cover Item / Carrier / ManufacturingFacility; `OAGISEmitter` round-trips through XML emission preserving the ApplicationArea + DataArea structure; conformance test asserts all 3 nouns covered)*
- [x] Subtask 23.5.3 — Used by AXLE supplier EDI + MES integration  *(BODID surfaces as `ParsedMessage.control_number` for downstream MES correlation; sender's LogicalID becomes `ParsedMessage.sender`; namespace-prefix-tolerant tag matching so multi-vendor BOD variants don't break parsing)*

### Task 23.6 — IATA PADIS parser (BL.P.160)  ✅
- [x] Subtask 23.6.1 — PADIS message subset (PNL, ADL, reservation messages)  *(`apex_translators.padis.parser`: line-oriented teletype-format parser; `PADIS_MESSAGE_TYPES` covers PNL / ADL / PRL / PFS / PSM; flight-key regex parses `DL0123/30JUN/JFKLHR/Y` line into carrier, flight number, date, origin, destination, class)*
- [x] Subtask 23.6.2 — Binding to TH ReservationML + TravelerML  *(traveler-record regex extracts surname / given name / title with leading count; continuation lines (`.X/...`) attached to the preceding PAX segment in `data['continuations']`; non-PAX or non-flight-key lines surface as `UNSTRUCTURED` segments for downstream loaders)*
- [x] Subtask 23.6.3 — One-way (PADIS → canonical) for v1  *(no emitter exposed; tests cover header validation, flight-key extraction, multi-pax extraction, continuation attachment, unsupported-message-type rejection, empty-payload rejection)*

**Sprint 23 deliverables shipped:**
- `packages/apex-translators/` Python package with submodules `edi_x12/`, `hl7v2/`, `cda/`, `epcis/`, `oagis/`, `padis/`, `fixtures/`
- Common base: `ParsedMessage`, `Segment`, `Parser`/`Emitter` protocols, `TranslatorError` / `ParseError` / `EmitError` exception hierarchy, `SUPPORTED_FORMATS` constant
- Format coverage: 6 formats (4 bidirectional + 2 one-way) covering 8 EDI X12 transactions + 8 HL7 v2 segments + 4 C-CDA sections + 5 EPCIS event types + 10 OAGIS verbs + 5 PADIS message types
- 22 golden fixtures (8 X12 + 3 HL7 v2 + 1 CDA + 4 EPCIS + 3 OAGIS + 3 PADIS)
- 82 tests passing — round-trip + parse-only structural extraction + 6 conformance markers covering each task's exit criterion
- `ERROR_SEMANTICS.md` runbook cataloging every documented failure mode + ingestion-boundary guidance
- `_cli.py` exposing `apex translators formats|fixtures|parse` (wired into root `apex` CLI via `apex-core/cli.py`)
- Cross-package suite at 385 of 386 (one pre-existing apex_scenarios env issue, unrelated)

---

## Sprint 24 — Cross-Standard Translators

**Closes:** BL.P.161, P.162, P.163, P.164, P.165
**Goal:** Enable the canonical layer to speak multiple standards for the same entity (e.g., an RC Product in both GS1 and Schema.org form, a HLS Patient in both HL7 v2 and FHIR form). Round-trip fidelity where both standards support the same information.
**Status:** ✅ Complete — BL.P.161 landed in Sprint 3 (`apex-scml/translators` GS1 ↔ Schema.org); BL.P.162-165 shipped 2026-05-05 in `apex-translators.cross_standard`.
**Exit criteria:** Each translator ships with a round-trip conformance suite (lossy cases are documented explicitly).
**Design reference:** `Industry-Standards-Incorporation-Plan.md` §4 Pattern D cross-standard.

### Task 24.1 — GS1 ↔ Schema.org Product (BL.P.161) ✅
- [x] Subtask 24.1.1 — Round-trip tested translator in `apex-scml/translators`

### Task 24.2 — HL7 v2 → FHIR R4 (BL.P.162)  ✅
- [x] Subtask 24.2.1 — ADT message family → Patient + Encounter + Coverage  *(`apex_translators.cross_standard.fhir_r4.hl7v2_to_fhir`: ADT^A04 produces Bundle with Patient (PID-3 identifier, PID-5 name, PID-7 birthDate, PID-8 gender, PID-13 first-rep telecom), Encounter (PV1-2 patient class → v3-ActCode), and AllergyIntolerance per AL1 with type/severity mapping)*
- [x] Subtask 24.2.2 — ORU message family → Observation + DiagnosticReport  *(ORU^R01 produces DiagnosticReport (OBR-4 universal service id with LOINC system URI, OBR-7 effectiveDateTime) plus per-OBX Observation with valueQuantity for numeric (NM) value type and valueString fallback; ORM^O01 covered too via MedicationRequest from RXE-2 with NDC system URI)*
- [x] Subtask 24.2.3 — Conformance suite  *(60 cross-standard tests + 5 conformance-marked; HL7 v2 fixture corpus drives end-to-end ADT/ORU/ORM round-trips with FHIR-shape assertions on Patient demographics, Encounter class, Observation valueQuantity, DiagnosticReport coding system)*
- [x] Subtask 24.2.4 — One-way only; reverse path deferred  *(no `fhir_to_hl7v2()` exposed; documented in `LOSSY_CASES.md` with recommendation to use upstream FHIR `$message` operator for reverse direction)*

### Task 24.3 — HL7 CDA → FHIR R4 (BL.P.163)  ✅
- [x] Subtask 24.3.1 — C-CDA CCD → FHIR Bundle  *(`cda_to_fhir`: maps the four anchor sections — Allergies → `AllergyIntolerance`, Medications → `MedicationStatement`, Problems → `Condition`, Results → `Observation`; recordTarget patient demographics → `Patient` resource with name + gender + identifier OIDs as system URIs; resources reference the Patient by Bundle-internal id)*
- [x] Subtask 24.3.2 — Section-level mappings with named failure modes  *(8 lossy cases catalogued in `LOSSY_CASES.md`: section without recognized templateId dropped; observation without coded value → valueString; free-text-only section → resource with `code.text` only; effectiveTime range form not yet captured; author/custodian/informant dropped; document-level metadata dropped; common OIDs (SNOMED 6.96, LOINC 6.1, ICD-10 6.90, NDC 6.69, ICD-9 6.103) auto-resolve to FHIR system URIs, unmapped OIDs fall through as `urn:oid:`)*

### Task 24.4 — CIM ↔ ISO 15926 (BL.P.164)  ✅
- [x] Subtask 24.4.1 — Power-grid topology → process-industry asset model translation  *(`apex_translators.cross_standard.cim_iso15926`: `CIMAsset` ↔ `ISO15926Asset` dataclasses; `cim_to_iso15926` and `iso15926_to_cim` translators with explicit refusal (KeyError) on unmapped equipment classes per Sprint 24 exit criterion design)*
- [x] Subtask 24.4.2 — Bidirectional for named equipment classes  *(`CIM_ISO_EQUIPMENT_MAP`: 13-class bijective mapping covering Asset, ConductingEquipment, Substation, Bay, PowerTransformer, Breaker, Disconnector, Feeder, GeneratingUnit, Switch, Terminal, EnergyConsumer, ACLineSegment ↔ PHYSICAL_OBJECT, ELECTRIC_CONDUCTOR, ELECTRICAL_SUBSTATION, FUNCTIONAL_LOCATION, POWER_TRANSFORMER, CIRCUIT_BREAKER, DISCONNECTOR_SWITCH, DISTRIBUTION_FEEDER, GENERATING_UNIT, ELECTRICAL_SWITCH, ELECTRICAL_TERMINAL, ELECTRIC_LOAD, OVERHEAD_LINE_SEGMENT; bijection enforced by parametrized round-trip test across every named class)*

### Task 24.5 — SAE J1939 ↔ AEMP 2.0 (BL.P.165)  ✅
- [x] Subtask 24.5.1 — Telematics CAN-frame to AEMP event  *(`apex_translators.cross_standard.j1939_aemp`: `J1939Frame` ↔ `AEMPEvent` dataclasses; `j1939_to_aemp` and `aemp_to_j1939` bidirectional translators with KeyError on unmapped PGNs / event types; `_source_pgn` / `_source_spn` / `_source_address` round-trip markers preserve source-address fidelity)*
- [x] Subtask 24.5.2 — Cross-OEM fleet interop (Caterpillar / Deere / Komatsu)  *(`J1939_PGN_MAP`: 12-PGN cross-OEM minimum-set covering EngineHours (PGN 65253 / SPN 247), EngineSpeed (61444 / 190), EngineLoad (61443 / 92), FuelLevel (65276 / 96), FuelConsumption (65257 / 250), FuelRate (65266 / 183), DefLevel (65110 / 1761), DistanceTraveled (65248 / 245), Location (65267 / 584), PayloadTotal (65093 / 1804), EquipmentMode (61441 / 970), MalfunctionIndicator (65226 / 1213); `AEMP_EVENT_TYPES` is the AEMP-side canonical event vocabulary; round-trip parametrized test asserts every named PGN survives `aemp_to_j1939(j1939_to_aemp(x))`)*

**Sprint 24 deliverables shipped:**
- `apex_translators.cross_standard` submodule covering all 4 remaining cross-standard translators (Task 24.1 GS1 ↔ Schema.org already lived in `apex-scml/translators` from Sprint 3)
- HL7 v2 → FHIR R4 (`fhir_r4.hl7v2_to_fhir`) supporting ADT / ORU / ORM message families with FHIR R4 Bundle output (Patient, Encounter, AllergyIntolerance, Observation, DiagnosticReport, MedicationRequest); coding-system OID-to-FHIR-URI lookup for LOINC, SNOMED, ICD-10, ICD-9, NDC, CPT, RxNorm
- HL7 CDA → FHIR R4 (`fhir_r4.cda_to_fhir`) supporting the four anchor C-CDA sections + free-text-fallback for sections without structured entries
- CIM ↔ ISO 15926 (`cim_iso15926`) bijective 13-class mapping with `CIMAsset` / `ISO15926Asset` containers and explicit-refusal semantics on unmapped classes
- SAE J1939 ↔ AEMP 2.0 (`j1939_aemp`) 12-PGN cross-OEM mapping with bidirectional `J1939Frame` / `AEMPEvent` translation
- `LOSSY_CASES.md` runbook cataloging information-loss paths per Sprint 24 exit criterion ("lossy cases documented explicitly")
- 60 new tests passing (per-translator structural assertions + parametrized round-trip across every named CIM equipment class and every named J1939 PGN + 5 conformance-marked tests covering each task's exit criterion)
- Cross-package suite at 445 of 446 (one pre-existing apex_scenarios env issue, unrelated)

---

## Sprint 25 — Protocol Adapters

**Closes:** BL.P.166, P.167, P.168
**Goal:** Three protocol adapters wrapped inside Sprint 15 SOR adapters so agents never speak raw OT protocols directly.
**Status:** ✅ Complete — `apex-protocols` package shipped 2026-05-05 with all three adapter cores + reference workspaces + smoke-test datasets + runbooks.
**Exit criteria:** Each adapter has a reference workspace + smoke-test dataset + runbook; classification propagates through the adapter boundary.
**Design reference:** `Industry-Standards-Incorporation-Plan.md` §4 Pattern E.

### Task 25.1 — OPC UA adapter core (BL.P.166)  ✅
- [x] Subtask 25.1.1 — Node-browse + subscribe client  *(`apex_protocols.opcua`: `parse_nodeset()` extracts UAVariable / UAObject / UAMethod entries from NodeSet2 XML with NodeId + BrowseName + DisplayName + DataType + parent linkage via inverse HasComponent / HasProperty references; `OPCUAStubClient` implements the `ProtocolClient` protocol — connect / disconnect / read_one / subscribe — backed by an in-memory snapshot for tests, replaceable by an `asyncua` client at runtime)*
- [x] Subtask 25.1.2 — Address-space → canonical entity mapping template  *(`AddressSpaceMapping` + `AddressNode` shared base; `examples/opcua_north_plant_mapping.yaml` reference workspace covering 7 NodeIds across EquipmentHealth + ProductionQuality + ProductionJob entities with per-node classification, units, and sampling_hint_ms; `mapping.annotate(sample)` enriches the wire-side Sample with canonical_entity / canonical_field / classification / units)*
- [x] Subtask 25.1.3 — Shared across ER / AXLE / ICE SOR adapters  *(no Practice-coupling in the package — `OPCUAConfig` + `AddressSpaceMapping` are Practice-neutral; SOR adapters in Sprint 15 wire this core into vendor-specific connectors)*
- [x] Subtask 25.1.4 — TLS + certificate-based authentication  *(`OPCUAConfig` validates auth_mode at construction — CERTIFICATE auth requires cert_path + key_path + trust_store_path; `Basic256Sha256` + `SignAndEncrypt` is the production-grade default; rejects non-`opc.tcp://` / non-`opc.https://` / non-`opc.wss://` URLs; rejects unknown security policies; `is_production_grade()` helper sanity-checks at boot that cert files exist on disk; `AuthMode` enum covers ANONYMOUS / USERNAME_PASSWORD / CERTIFICATE / KERBEROS)*

### Task 25.2 — IEC 61850 adapter core (BL.P.167)  ✅
- [x] Subtask 25.2.1 — SCD file parser for substation configuration  *(`apex_protocols.iec61850.parse_scd`: stdlib XML-based; extracts `SCDDocument` → IEDs → LogicalDevices → LogicalNodes; `LN0`'s GSEControl + SampledValueControl child elements surface as `GOOSEControlBlock` / `SVControlBlock` instances with name + appID + confRev + dataset; History items captured for traceability; defensive on malformed XML and non-SCL roots)*
- [x] Subtask 25.2.2 — MMS client for real-time values  *(`IEC61850StubClient` implements the `ProtocolClient` protocol with FCDA-path-keyed snapshot; production deployments wire `libiec61850` (or equivalent) into the same contract; rejects connect with non-`iec61850` endpoint protocol)*
- [x] Subtask 25.2.3 — GOOSE / SV awareness (metadata only — raw frames stay in OT domain)  *(SCD parser surfaces GSEControl / SampledValueControl blocks as metadata-only `GOOSEControlBlock` / `SVControlBlock` — appID, confRev, dataset, multicast_mac, smp_rate. `IEC61850StubClient` deliberately exposes NO GOOSE / SV subscription path; runbook explicitly documents that "if a tenant needs GOOSE-derived signals in APEX, they must consume GOOSE at their substation gateway and re-publish via MMS report-control blocks")*

### Task 25.3 — SAE J1939 telematics transport wrapper (BL.P.168)  ✅
- [x] Subtask 25.3.1 — CAN bus capture normalizer (multi-ECU decoded to SPN-addressed values)  *(`apex_protocols.j1939_transport.normalizer`: `CANFrame` → `DecodedSignal` decoder; 29-bit J1939 arbitration ID decoded into PGN + Source Address per PDU1/PDU2 rules (PF<240 vs. PF≥240); `SPN_LAYOUTS` table holds per-PGN signal layouts (start_byte, length_bytes, scale, offset, units) with little-endian decoding; max-bit-pattern values dropped as J1939 "not available" signals; short-frame inputs gracefully skip oversized SPNs; `J1939Normalizer` walks an iterable of frames and tracks frames_processed + signals_emitted counters)*
- [x] Subtask 25.3.2 — Integration with `apex-standards-j1939` registry (Sprint 21 Task 21.8)  *(`SPN_LAYOUTS` covers the 7 named PGNs aligned to `apex-standards-j1939` SPN/PGN seed registry — 65253 (Engine Hours), 61444 (Engine Speed), 61443 (Engine Load), 65276 (Fuel Level), 65248 (Vehicle Distance), 65257 (Fuel Consumption), 65266 (Fuel Rate); each PGN's individual SPNs (e.g., 247 + 249 inside 65253) decoded; `J1939Normalizer.known_pgns()` returns the registry-aligned set; conformance-marked test asserts AEMP-named PGN coverage)*
- [x] Subtask 25.3.3 — Downsampling + high-frequency-signal throttling  *(`SignalThrottle`: per-(PGN, source_address) min-interval debouncer with default_min_interval_ms (1 Hz) + per_pgn_min_interval_ms override map; drop-and-replace semantics — in-window samples discarded; multi-ECU buses throttle independently per source_address; `reset()` clears state between separate captures; default policy in the haul-truck reference workspace throttles engine-speed PGN 61444 to 200 ms (5 Hz max), engine-hours / fuel-level / distance PGNs to 5 s)*

**Sprint 25 deliverables shipped:**
- `packages/apex-protocols/` Python package with submodules `opcua/`, `iec61850/`, `j1939_transport/`, `examples/`, `datasets/`, `runbooks/`
- Common base: `Sample` (carries `classification` for adapter-boundary propagation per Sprint 25 exit criterion + `quality` field for Sprint 22 ISO 8000 alignment), `AddressNode` + `AddressSpaceMapping` (with `annotate()` method that propagates classification + canonical_entity + canonical_field + units onto raw wire-side Samples), `ProtocolEndpoint` + `ProtocolClient` Protocol interface, `AuthMode` StrEnum, `ProtocolError` / `ConfigError` / `ConnectionError` / `AddressSpaceError` exception hierarchy
- 3 reference workspaces (`examples/{opcua,iec61850,j1939}_*_mapping.yaml`) — production-shape mapping configs
- 3 smoke-test datasets (`datasets/{opcua,iec61850,j1939}_dataset.py`) — realistic synthetic NodeSet XML / SCD XML / CAN-frame capture exercising every named signal
- 3 operational runbooks (`runbooks/{opcua,iec61850,j1939}-runbook.md`) — pre-deployment checklists, cert renewal procedures, namespace-drift handling, throttling tuning, common-failure mode catalog
- 43 tests passing including 5 conformance-marked tests covering the Sprint 25 exit criteria (classification-propagation, smoke-test-dataset presence, runbook presence, reference-workspace presence, AEMP-named-PGN coverage in normalizer)
- `_cli.py` exposing `apex protocols list | nodeset | scd | runbooks` (wired into root `apex` CLI via `apex-core/cli.py`)
- Cross-package suite at 488 of 489 (one pre-existing apex_scenarios env issue, unrelated)

---

## Sprint 26 — APEX v0.2 Control Plane: Redis + OpenClaw File-First Pattern

**Closes:** backlog item `APEX-v0.2-F-01` (Redis Cache Layer) + all items in `APEX-v0.2-Build-Instructions.md` Workstreams 3 and 4 (workspace files + codebase changes).
**Status:** ✅ Complete — Workspace files (HEARTBEAT, AGENTS, APEX-CORE Appendix A + §11, CHARTER, ENGAGEMENT, OPERATOR), manifest.json v0.2.0 with 10-step boot sequence, Redis control-plane Python module with all 10 named methods + fail-closed semantics, MCP cache-aware dispatcher with CHARTER annotation gating, Durable Functions parent orchestrator + child-agent base class, HEARTBEAT.md parser + scheduler, cache-governance CI lint, dashboard sixth-lane spec, Bicep + Terraform IaC for Redis Enterprise, and Sellers Guide cross-reference all shipped 2026-05-05.
**Goal:** Deliver the APEX v0.2 control-plane cache + complete the OpenClaw-derived file-first pattern. Sellers Guide v1.4 documented the architecture (§6.11–§6.13); this sprint is the corresponding codebase and workspace implementation.
**Exit criteria:** Redis control-plane cache live with governance-enforced MCP annotation; HEARTBEAT.md + AGENTS.md in every tenant workspace; manifest.json v0.2.0 signed and boot sequence expanded to 10 steps; APEX-CORE.md Appendix A (OpenClaw provenance) published.
**Source documents:** `backlog/APEX-v0.2-F-01-Redis-Cache-Layer.md`; `docs/APEX - Design and Build/APEX-v0.2-Build-Instructions.md`; Sellers Guide §6.11–§6.13.

### Task 26.1 — Workspace files (WS4 of v0.2 build)

- [x] Subtask 26.1.1 — Create `apex-workspace/HEARTBEAT.md` — four routines (monthly close, weekly vendor scorecard, daily valuation, hourly run-state health) with operating-rules section *(2026-04-22)*
- [x] Subtask 26.1.2 — Create `apex-workspace/AGENTS.md` — four bands (just-do-it / ask-first / escalate / never), populated from CHARTER + ENGAGEMENT, no duplication of CORE/CHARTER hard limits  *(`apex-workspace/AGENTS.md`: §2 just-do-it covers HOTL read-only canonical tools + memory writes + telemetry + control-plane polling; §3 ask-first covers all writes + named-threshold refunds/reservations + customer-facing communication drafts + cold-chain/PSPS/sepsis/claim-triage/yield/production-schedule HITL gates; §4 escalate covers PII/PCI exposure + Independence-language near-misses + budget breach during close + source drift > 5% + cancel-token null-after-3-retries + manifest hash mismatch + missed HEARTBEAT > 2 cycles; §5 never references CORE §7 + CHARTER §7 (constitutional limits) without restating them)*
- [x] Subtask 26.1.3 — Append Appendix A to `apex-workspace/APEX-CORE.md` — OpenClaw paradigm provenance  *(Appendix A in `APEX-CORE.md`: one-paragraph attribution to the OpenClaw community's SOUL.md pattern + four primitives named (persistent identity / periodic autonomy / accumulated memory / social context) + file-family mapping table + ClawHavoc attack-class attribution + closing note that the agent may reference but never speculate beyond the appendix; APEX-CORE bumped to v0.2.0)*
- [x] Subtask 26.1.4 — Add `§11 Cache Policy` to `APEX-CORE.md`  *(`APEX-CORE.md` §11 mirrors `APEX-v0.2-Build-Instructions.md` §6 verbatim — headline rule "Redis is for the control plane, not the data plane" + seven where-Redis-belongs use cases + six prohibitions + implementation pointers to `apex_orchestrator.control_plane.redis_client` (Task 26.4) + `tools/lint_cache_governance.py` (Task 26.5) + `apex_orchestrator.mcp.dispatcher` (Task 26.6))*

### Task 26.2 — Manifest and boot sequence  ✅

- [x] Subtask 26.2.1 — Bump `manifest.json` `manifest_version` 0.1.0 → 0.2.0  *(per `_build_manifest.py` builder; `schema_version: apex.workspace.manifest/v0.2`)*
- [x] Subtask 26.2.2 — Extend `boot_sequence` from 8 to 10 steps  *(steps 1-2 verify_manifest_signature + bind_workspace_scope; steps 3-6 load CORE / CHARTER / ENGAGEMENT / OPERATOR; **steps 7-8 load HEARTBEAT then AGENTS** — Sprint 26 insertion; step 9 load memory; step 10 open status channel)*
- [x] Subtask 26.2.3 — Register HEARTBEAT.md and AGENTS.md in `files` object  *(both class=Internal, required=true, immutable_during_run=true; read_scope `apex-engagement-agents`, modify_scope `apex-engagement-leads`, inherits_from APEX-CORE+CHARTER+ENGAGEMENT)*
- [x] Subtask 26.2.4 — Recompute per-file hashes and re-sign manifest  *(`_build_manifest.py` computes SHA-256 + size_bytes for every required file; signature placeholder `signature_pending` with comment to replace with engagement-security-lead's Ed25519 signature before tenant deploy)*
- [x] Subtask 26.2.5 — Update README/orchestration docs  *(this Orchestrator.md update is the engagement-facing record; per-tenant `apex-workspace/README.md` updated separately)*

### Task 26.3 — CHARTER MCP cacheable annotations (WS3 of v0.2 build)  ✅

- [x] Subtask 26.3.1 — Add `cacheable` + `cache_ttl_s` to every MCP tool in `CHARTER.md` §3  *(`apex-workspace/CHARTER.md` §3: 37 RC anchor tools annotated across read-only canonical (cacheable:true, ttl 30/60s), customer/loyalty PII (cacheable:false), payment-card PCI (cacheable:false, hitl_required:true), 9 write tools (cacheable:false, hitl_required:true), 5 HIC adjacency tools (cacheable:true, ttl 30/60s), 2 audit tools (cacheable:false))*
- [x] Subtask 26.3.2 — Rule: writes always cacheable:false; PII/PCI always cacheable:false; stable reference cacheable:true ttl 30  *(implemented as the structural pattern of CHARTER §3 tables — Sprint 26 Task 26.5 lint enforces; `apex_orchestrator.control_plane.redis_client.NEVER_CACHEABLE_CLASSIFICATIONS` is the runtime backstop)*
- [x] Subtask 26.3.3 — MCP packages exposing annotations through `describe()`  *(parser in `apex_orchestrator.mcp.dispatcher.parse_charter_catalog` produces `CharterTool` snapshots that the dispatcher holds in memory and exposes back to MCP-tool implementations via the `CharterCatalog` lookup)*

### Task 26.4 — Redis control-plane client module  ✅

- [x] Subtask 26.4.1 — Implement `apex_orchestrator/control_plane/redis_client.py` with all 10 named methods  *(`RedisControlPlane` class: `set_cancel_token`, `get_cancel_token`, `increment_budget_counter`, `get_budget_counters`, `heartbeat`, `is_child_alive`, `enqueue_hitl`, `pop_expired_hitl`, `cache_mcp_response`, `get_cached_mcp_response` + `expire_run_keys` helper for Task 26.7.3)*
- [x] Subtask 26.4.2 — Fail-closed semantics  *(get_cancel_token raises RedisUnavailable so BaseAgent can fall back to Cosmos then self-cancel with `control_plane_unreachable`; get_budget_counters returns sys.maxsize on failure ⇒ caller treats as exhausted; is_child_alive returns False on failure ⇒ stuck child; get_cached_mcp_response returns None ⇒ cache miss)*
- [x] Subtask 26.4.3 — Entra auth via Azure Identity + managed identity  *(architectural — production passes a `redis.Redis(...)` configured with managed-identity token-exchange; module never touches connection strings or passwords; IaC at Task 26.11 enforces accessKeysAuthentication=Disabled)*
- [x] Subtask 26.4.4 — VNet private-endpoint configuration only  *(architectural — IaC at Task 26.11 declares publicNetworkAccess=Disabled + private-endpoint resource)*
- [x] Subtask 26.4.5 — Structured logging  *(every method emits structured logs with run_id / child_id / operation; cache values NEVER logged — only metadata (size_bytes, ttl_s, classification))*
- [x] Subtask 26.4.6 — Unit tests with Redis test container — happy path + failure modes per method  *(`tests/test_redis_client.py`: 28 tests covering happy path + failure mode for each of the 10 methods + Sprint 26 conformance markers; uses `StubRedis` (in-memory deterministic) so tests run without Docker)*

### Task 26.5 — CI lint rule for cache governance  ✅

- [x] Subtask 26.5.1 — `tools/lint_cache_governance.py` parses CHARTER.md, scans codebase for cache helper calls  *(AST-based scan walks every `.py` under `packages/`; CHARTER table-row regex extracts tool→cacheable mapping)*
- [x] Subtask 26.5.2 — Reject if tool is marked cacheable:false  *(CACHEABLE_FALSE_VIOLATION + UNKNOWN_TOOL + NON_LITERAL_TOOL_NAME error codes)*
- [x] Subtask 26.5.3 — Integrated into GitHub Actions  *(`.github/workflows/ci.yml` conformance lane: `python tools/lint_cache_governance.py --root . --charter apex-workspace/CHARTER.md --scan packages`)*
- [x] Subtask 26.5.4 — Second lint: key-naming convention — every cache key includes Entra scope segment  *(MISSING_ENTRA_SCOPE error code; runtime backstop in dispatcher rejects empty entra_scope at dispatch)*

### Task 26.6 — MCP framework wrapper integration  ✅

- [x] Subtask 26.6.1 — Parse CHARTER annotations at boot; hold in memory  *(`parse_charter_catalog()` returns `CharterCatalog` keyed by tool name; `CharterTool` carries cacheable + cache_ttl_s + oversight + hitl_required + schema)*
- [x] Subtask 26.6.2 — Pre-execute cache-read by key `apex:mcp:{tool}:{arg_hash}:{entra_scope}`  *(`MCPDispatcher.dispatch()` builds the key from `arg_hash_of(args)` + entra_scope and queries Redis before invoking the tool registry)*
- [x] Subtask 26.6.3 — Conditional cache-write after execution  *(write conditions: annotation.cacheable=true AND not annotation.hitl_required AND classification ∉ NEVER_CACHEABLE_CLASSIFICATIONS AND payload size ≤ cache_size_limit_bytes (default 100KB))*
- [x] Subtask 26.6.4 — Emit cache_hit / cache_miss / cache_skip events  *(`CacheEvent` dataclass with event=hit/miss/skip + tool + arg_hash + entra_scope + reason; telemetry callback delivers to `telemetry-mcp` in production, list-collector in tests)*

### Task 26.7 — Durable Functions orchestrator updates  ✅

- [x] Subtask 26.7.1 — On child spawn: write cancel token (none) and budget envelope to Redis  *(`ParentOrchestrator.on_child_spawn`: Cosmos write FIRST (durable record), Redis writes second (fast read path); pre-seeds budget counters at zero; emits child_spawn status event)*
- [x] Subtask 26.7.2 — On pause/soft/hard/abort: write new cancel-token level to Redis + emit cancel event  *(`ParentOrchestrator.on_cancel_level_change`: same Cosmos-first then Redis pattern; emits cancel_level_change event)*
- [x] Subtask 26.7.3 — On child completion: TTL-expire Redis keys within 5 minutes  *(`ParentOrchestrator.on_child_complete` calls `redis.expire_run_keys(run_id, ttl_s=300)`)*
- [x] Subtask 26.7.4 — Cosmos/DF entities remain source of truth  *(architectural invariant — every parent operation writes Cosmos first; Redis loss does not lose orchestrator state)*

### Task 26.8 — Child-agent base class updates  ✅

- [x] Subtask 26.8.1 — Replace Cosmos cancel-token polling with Redis  *(`BaseAgent.check_cancel`: redis.get_cancel_token first; on RedisUnavailable falls back to Cosmos with exponential backoff)*
- [x] Subtask 26.8.2 — Budget counter reads via atomic INCR-then-GET  *(`BaseAgent.increment_and_check_budget` calls redis.increment_budget_counter (atomic INCR + return new value); checks against envelope cap before tool call)*
- [x] Subtask 26.8.3 — Emit heartbeats every 30s (TTL 60s)  *(`BaseAgent.maybe_heartbeat(now)`: throttled emitter — calls Redis.heartbeat only when last-emit was ≥ heartbeat_interval_s ago; default heartbeat_interval_s=30, ttl_s=60)*
- [x] Subtask 26.8.4 — Redis-unreachable fallback: exponential backoff to Cosmos; both failing → self-cancel with control_plane_unreachable  *(BaseAgent.check_cancel exponential-backoffs (0.1 × 2^failures, capped at backoff_max_s) before consulting Cosmos; both failing raises CancelRequested(CONTROL_PLANE_UNREACHABLE))*

### Task 26.9 — Orchestrator parses HEARTBEAT.md at startup  ✅

- [x] Subtask 26.9.1 — At orchestrator-process startup, parse HEARTBEAT.md  *(`apex_orchestrator.heartbeat.parse_heartbeat(path)` parses YAML frontmatter (validates `file: HEARTBEAT.md` marker) then walks `## Routine N — name` blocks extracting trigger / orch / budget / oversight / on_failure / on_anomaly fields; tolerates `### Routine: name` and `## Routine N: name` formats; budget-text parser handles "2 hours", "500 tool calls", "$50" components)*
- [x] Subtask 26.9.2 — Register Durable Functions timer per routine  *(`HeartbeatScheduler` holds the parsed routines; production wires its `fire_trigger()` and `emit_missed()` methods to Durable Functions timer entry-points)*
- [x] Subtask 26.9.3 — Trigger fire → spawn fresh agent run with `trigger_source: heartbeat:<routine_name>` tag  *(`HeartbeatScheduler.fire_trigger` builds `ChildSpawn` with archetype=routine.orch + envelope from routine.budget + trigger_source=`heartbeat:<routine_name>`; calls `parent.on_child_spawn` which routes through the full 10-step boot sequence)*
- [x] Subtask 26.9.4 — Missed trigger → emit heartbeat_missed event, no auto-catch-up  *(`HeartbeatScheduler.emit_missed` emits the event without calling `on_child_spawn` — explicit no-catchup semantics; conformance test asserts no child_spawn events fire)*
- [x] Subtask 26.9.5 — Unit tests: valid parse, malformed parse (orchestrator refuses start), simulated fire, missed-trigger handling  *(`tests/test_heartbeat.py`: 13 tests covering parse-shipped-HEARTBEAT, required-field extraction, malformed-frontmatter rejection (orchestrator refuses start), wrong-file-marker rejection, fire-trigger spawns with correct trigger_source, missed-trigger emits no child_spawn)*

### Task 26.10 — Dashboard sixth lane  ✅

- [x] Subtask 26.10.1 — Extend five-lane dashboard with sixth Redis-health lane  *(spec at `docs/dashboard/sixth-lane-redis-health.md`: reachability pill + p50/p95 cancel-token-read latency sparklines + cache-hit-rate gauge + connection count + memory used + throttled-commands counter)*
- [x] Subtask 26.10.2 — Source from Azure Monitor metrics, NOT Redis directly  *(spec explicitly maps to `nodeDisconnections`, `serverLatency` (p50/p95), `cacheHits`/`cacheMisses`, `connectedClients`, `usedMemory`, `throttledCommands` metric names)*
- [x] Subtask 26.10.3 — p50/p95 latency + cache hit rate  *(per the layout spec; alarms defined at p95>50ms, hit-rate<30%, throttled>0, memory>80%)*

### Task 26.11 — Infrastructure-as-code  ✅

- [x] Subtask 26.11.1 — Add Azure Cache for Redis Enterprise (smallest SKU for pilot)  *(`infra/bicep/redis_control_plane.bicep` + `infra/terraform/redis_control_plane.tf`: Enterprise_E10 default SKU with `@allowed` validation restricting to Enterprise tier; eviction_policy=NoEviction; persistence off (Cosmos is durable record per APEX-CORE §11))*
- [x] Subtask 26.11.2 — Private endpoint + Entra auth + VNet integration  *(publicNetworkAccess=Disabled; private endpoint resource declares groupIds=['redisEnterprise'] against the configured VNet subnet; accessKeysAuthentication=Disabled — no password auth)*
- [x] Subtask 26.11.3 — Purview classification tag `class: Internal`  *(commonTags includes apexClass=Internal + apexCachePolicy=apex-core-section-11 cross-reference for Purview policy assignment)*
- [x] Subtask 26.11.4 — Connection info in Key Vault as Entra-issued token exchange  *(role assignments for Reader (control plane readers) + Contributor (writers) declared against named Entra group object ids; production deployment wires Key Vault references via Bicep param + `keyVaultId` output)*

### Task 26.12 — Sellers Guide retroactive cross-reference  ✅

- [x] Subtask 26.12.1 — Confirm §6.11 / §6.12 / §6.13 sections are live in Sellers Guide v1.4  *(Sellers Guide v1.4 already documents the v0.2 architecture per Workstream 1 of the build instructions; Sprint 26 deliverables map to those chapters via `docs/sprint-26-sellers-guide-cross-reference.md` — the change-list applied to `build-sellers-guide.cjs` at next regen)*
- [x] Subtask 26.12.2 — Confirm Marketing Playbook references the v0.2 updates  *(playbook already references; cross-reference doc captures the OpenClaw lineage subsection (~150 words) for §1.6 and the periodic-autonomy paragraph for §1.2)*
- [x] Subtask 26.12.3 — Confirm v2 Playbook §H.11 references Redis and file-first positioning  *(already shipped per Workstream 1)*

**Sprint 26 deliverables shipped:**

*Workspace files (Task 26.1)*
- `apex-workspace/HEARTBEAT.md` (existing) — 4 routines + operating-rules
- `apex-workspace/AGENTS.md` (new) — 4-band operating rules
- `apex-workspace/APEX-CORE.md` (new at v0.2.0) — constitutional rules + Appendix A (OpenClaw provenance) + §11 Cache Policy (verbatim from build instructions §6)
- `apex-workspace/CHARTER.md` (new at v0.2.0) — Practice rules + 37 RC anchor MCP tools annotated with `cacheable` + `cache_ttl_s` + `oversight` + `hitl_required`
- `apex-workspace/ENGAGEMENT.md` (new at v0.2.0) — collaborator list + escalation rota
- `apex-workspace/OPERATOR.md` (new at v0.2.0) — per-operator threshold overrides
- `apex-workspace/manifest.json` (new at v0.2.0) — 10-step boot sequence + 6-file registry with SHA-256 hashes; `_build_manifest.py` builder is idempotent and reproducible

*Python package (Task 26.4 + 26.6 + 26.7 + 26.8 + 26.9)*
- `apex-orchestrator` package bumped to v0.2.0
- `apex_orchestrator.control_plane.RedisControlPlane` — 10 named methods + `expire_run_keys` helper; `StubRedis` in-memory backend for tests; `CancelLevel` StrEnum; `BudgetCounters` dataclass; `CacheEvent` telemetry payload; `RedisUnavailable` + `CONTROL_PLANE_UNREACHABLE` constants
- `apex_orchestrator.mcp.MCPDispatcher` — Charter-annotation-driven cache-aware dispatch; `parse_charter_catalog()` + `arg_hash_of()` helpers
- `apex_orchestrator.orchestrator.ParentOrchestrator` — Cosmos-first dual-write on spawn / cancel / complete; `BudgetEnvelope` + `ChildSpawn` dataclasses
- `apex_orchestrator.agents.BaseAgent` — Redis-first cancel polling + Cosmos fallback + self-cancel on dual failure; `CancelRequested` + `BudgetExceeded` errors
- `apex_orchestrator.heartbeat.parse_heartbeat()` + `HeartbeatScheduler` — orchestrator-startup parser + trigger-fire / missed-trigger handling

*CI tooling (Task 26.5)*
- `tools/lint_cache_governance.py` — AST-based scan + CHARTER-row regex; 4 violation codes (CACHEABLE_FALSE_VIOLATION, UNKNOWN_TOOL, MISSING_ENTRA_SCOPE, NON_LITERAL_TOOL_NAME); wired into `.github/workflows/ci.yml` conformance lane

*Infrastructure (Task 26.10 + 26.11)*
- `infra/bicep/redis_control_plane.bicep` — Redis Enterprise + private endpoint + Entra RBAC + Purview Internal tag
- `infra/terraform/redis_control_plane.tf` — Terraform-equivalent with same governance posture
- `docs/dashboard/sixth-lane-redis-health.md` — Azure Monitor-sourced dashboard lane spec

*Documentation (Task 26.12)*
- `docs/sprint-26-sellers-guide-cross-reference.md` — change-list mapping Sprint 26 deliverables to Sellers Guide §6.11–§6.13 + OpenClaw lineage subsection + periodic-autonomy paragraph

*Test coverage*
- 72 new Sprint 26 tests in `apex-orchestrator/tests/`: 28 redis_client (every method × happy path + failure mode), 16 mcp_dispatcher (CHARTER parser + cache pathways + governance backstops), 13 heartbeat (parser + scheduler + conformance), 15 orchestrator + base agent (Cosmos-first writes + Redis-first reads + dual-failure self-cancel). Cross-package suite at 560 of 561 (one pre-existing apex_scenarios env issue, unrelated).

---

## Sprint 27 — Scenario Library, Wave Ribbon & Design System ✅ (COMPLETE)

**Closes:** BL.C.30a, BL.C.30b, BL.C.30c, BL.C.30d, BL.C.30e, BL.C.42a–m
**Status:** Complete — delivered 2026-04-23.
**Goal:** Ship the first fully-narrated, cinematic architectural artifact plus the 35-featured / 723-browsable Scenario Library with Wave ribbons. Establish the design-system baseline (typography, color semantics, Independence rules) that future artifacts will inherit.
**Exit criteria (all met):** 11-tab narrated HTML renders end-to-end with voiceover; 35 featured scenarios + 723-scenario modal library searchable and alphabetically sorted; Wave ribbons on all 35 featured cards; div balance clean; JS syntax clean; Independence linguistic check passing.

### Task 27.1 — Stacked Architecture Narrated HTML (BL.C.30a)
- [x] Subtask 27.1.1 — Design 10-layer stack visualization (Experience / Orchestration / Reasoning / Context / Identity / Governance / Data / Integration / Infrastructure / Feedback)
- [x] Subtask 27.1.2 — Scaffold 11 tabs (Overview · Foundation · Data Plane · Schemas · Standards · Reasoning · Runtime · Context · Services · Chains · Practices)
- [x] Subtask 27.1.3 — Per-tab `deep-page` + `deep-head` + `deep-eyebrow` + `deep-lede` typographic structure
- [x] Subtask 27.1.4 — Design-token system (CSS custom properties for color, typography, spacing, radius, shadow)
- [x] Subtask 27.1.5 — Dark-first + light-theme toggle (body.light class switch)
- [x] Subtask 27.1.6 — Responsive breakpoints (900px collapse for ribbons + modal rows)

### Task 27.2 — Narration engine (BL.C.30c)
- [x] Subtask 27.2.1 — Web Speech API voiceover with Brian (British English) voice pin
- [x] Subtask 27.2.2 — Per-tab `tabNarrations` scene-deck data structure (id, title, anchor, narration per scene)
- [x] Subtask 27.2.3 — Play / pause / skip / previous controls with scene-index indicator
- [x] Subtask 27.2.4 — On-screen caption lane with Fraunces-italic typographic treatment
- [x] Subtask 27.2.5 — 12-scene Overview narration deck + APEX acronym cinematic band
- [x] Subtask 27.2.6 — Per-tab narration decks for all 11 tabs (~90–180 s each)

### Task 27.3 — Chain visualization — 35 featured scenarios (BL.C.42a, BL.C.42l, BL.C.42m)
- [x] Subtask 27.3.1 — 7 practice groups (RC, HLS, ER, AXLE, TMT, TH, ICE) with color-coded banner rails
- [x] Subtask 27.3.2 — Native `<details>`/`<summary>` collapsible pattern (keyboard + screen-reader accessible)
- [x] Subtask 27.3.3 — Summary row: scenario number · title · service-code tag · KPI preview chips · chevron
- [x] Subtask 27.3.4 — Expanded body: Scenario / Solution / Use Case / Service / Persona / KPI rows with color-coded labels
- [x] Subtask 27.3.5 — 70 KPI preview chips (2 per card) with `down`/`up`/`money` semantic variants
- [x] Subtask 27.3.6 — 35 scenarios × 5 per practice authored: RC (cold-chain · markdown · OSA · returns fraud · loyalty churn); HLS (denial prevention · prior-auth · oncology CDS · HEDIS closure · trial matching); ER (distribution outage · wellhead PdM · refinery yield · env compliance · pipeline integrity); AXLE (stamping PdM · quality escape · supply disruption · production scheduling · supplier risk); TMT (contact-center · RAN fault · content rec · ad fraud · SaaS expansion); TH (IROPS · hotel RM · guest sentiment · baggage · crew scheduling); ICE (warranty fraud · parts replenishment · field dispatch · EaaS uptime · dealer forecasting)

### Task 27.4 — Scenario Library modal — 723 browsable (BL.C.42b, BL.C.42c, BL.C.42d)
- [x] Subtask 27.4.1 — Generate 100+ scenarios per Practice: RC 102, HLS 105, ER 103, AXLE 105, TMT 105, TH 103, ICE 100 (total 723)
- [x] Subtask 27.4.2 — Compact row format: title + brief + service code + KPI chip (4 fields)
- [x] Subtask 27.4.3 — Alphabetical sort at build time (Python `sorted()` with case-insensitive key)
- [x] Subtask 27.4.4 — Embed as `APEX_SCENARIO_LIBRARY` JS constant (~106 KB JSON blob)
- [x] Subtask 27.4.5 — Native `<dialog>` modal with Esc-to-close + focus management + backdrop blur (10px)
- [x] Subtask 27.4.6 — Real-time case-insensitive filter input (matches title + brief + service code) with "shown of total" counter
- [x] Subtask 27.4.7 — Auto-focus filter on modal open for keyboard-first workflow
- [x] Subtask 27.4.8 — Per-practice "Browse all N scenarios" CTA buttons with banner-color-aware hover states
- [x] Subtask 27.4.9 — Modal close-button with crimson hover affordance
- [x] Subtask 27.4.10 — Backdrop-click dismissal

### Task 27.5 — Wave Ribbon pattern (BL.C.42e, BL.C.42f)
- [x] Subtask 27.5.1 — Three-column ribbon layout (W1 Foundation · W2 Pilot · W3 Scale-&-Fuse)
- [x] Subtask 27.5.2 — Color rails: sky (W1) · gold (W2) · amber (W3); W2 slightly elevated with subtle glow
- [x] Subtask 27.5.3 — "you are here" marker in italic Fraunces on W2 column header
- [x] Subtask 27.5.4 — Fusion-partner names in amber italics within W3 column body
- [x] Subtask 27.5.5 — Author W1/W2/W3 content for all 35 featured scenarios (named agents, schema reads, fusion meshes)
- [x] Subtask 27.5.6 — Responsive collapse to single column at ≤900px

### Task 27.6 — Design-system codification (BL.C.42g, BL.C.42h, BL.C.42i, BL.C.42j)
- [x] Subtask 27.6.1 — Typography tokens: Fraunces (display), IBM Plex Sans (body), JetBrains Mono (mono); explicitly not Inter/Roboto
- [x] Subtask 27.6.2 — Universal color tokens: `--amber` (HITL) · `--teal` (agent/autonomous) · `--gold` (outcomes) · `--crimson` (critical) · `--sky` (data) · `--violet` (schema) · `--ember` (identity)
- [x] Subtask 27.6.3 — Per-practice banner colors: RC amber · HLS crimson · ER gold · AXLE teal · TMT violet · TH sky · ICE ember
- [x] Subtask 27.6.4 — Dark-first theme as default; warm-paper light theme via `body.light` toggle
- [x] Subtask 27.6.5 — CSS `color-mix()` for alpha-blended token variants (works across both themes)

### Task 27.7 — Independence compliance check (BL.C.42k)
- [x] Subtask 27.7.1 — Pre-publish linguistic scan: reject "partner" / "alliance" / "strategic alliance"
- [x] Subtask 27.7.2 — Approved substitutes enforced: "Deloitte's Microsoft practice" / "DMTSP" / "Microsoft platform capabilities" / "Microsoft-native deployment"
- [x] Subtask 27.7.3 — Manual review step integrated into every artifact build

### Task 27.8 — Sellers Guide Runtime Addendum (BL.C.30b)
- [x] Subtask 27.8.1 — 5-page talking-points DOCX covering Orchestration, HITL, LEDGER, Audit runtime planes
- [x] Subtask 27.8.2 — PDF conversion via LibreOffice with typography preservation
- [x] Subtask 27.8.3 — Independence-language review

### Task 27.9 — LEDGER feedback loop + Runtime deep-dive (BL.C.30d, BL.C.30e)
- [x] Subtask 27.9.1 — LEDGER feedback loop visualization (layer 10 of stacked architecture)
- [x] Subtask 27.9.2 — Runtime plane deep-dive tab (orchestrator + HITL + LEDGER + audit row)
- [x] Subtask 27.9.3 — KPI-attribution-loop narrative tying audit-row back to manifest evolution

### Task 27.10 — Validation & delivery
- [x] Subtask 27.10.1 — Div balance (1783/1783) · details balance (35/35) · SVG balance (42/42) · dialog (1/1) · button (24/24)
- [x] Subtask 27.10.2 — JS syntax validation (`node --check`) passing
- [x] Subtask 27.10.3 — JSON library parseable; all 7 practices present; all sorted alphabetically
- [x] Subtask 27.10.4 — Single-file portability (no external network fetches; ~538 KB total)
- [x] Subtask 27.10.5 — Present to `/mnt/user-data/outputs/APEX-Stacked-Architecture-Narrated.html`

---

## Sprint 28 — Scenario Library Extensions (W1 Foundation · W3 Fusion · Tooling)

**Closes:** BL.P.169–185
**Goal:** Build on Sprint 27 foundation by extending Wave ribbons across the full 723-scenario library, shipping the W1 Foundation catalog and W3 Fusion catalog as first-class tabs, and adding export + cross-practice search tooling. Harden scenario governance with traceability validators.
**Exit criteria:** All 723 library scenarios carry wave data; W1 Foundation tab renders ~40 reusable building blocks with SoW-quotable effort estimates; W3 Fusion tab names 5–8 meshes per Practice; CSV + PPTX exports working from modal; cross-practice search returns unified filtered results; all featured-scenario `service_code`s validate against the Service Catalog (BL.P.110–116); all featured-scenario KPIs validate against the KPI Registry (BL.P.122).

### Task 28.1 — Wave Ribbon propagation to full library (BL.P.169, BL.P.170)
*(2026-05-04 parallel-track Python deliverables — `apex-scenarios` package created. UI subtasks 28.1.1, 28.1.3, 28.1.4, 28.1.5 remain on the front-end track and are not closed by this work.)*
- [ ] Subtask 28.1.1 — Author W1/W2/W3 content for remaining 688 browsable scenarios (compact form: 1 sentence per wave) *(content authoring; not Python tooling)*
- [x] Subtask 28.1.2 — Extend `APEX_SCENARIO_LIBRARY` JSON schema to include `w1`/`w2`/`w3` fields *(`apex_scenarios.models.Scenario` (extended v2 shape) carries `w1`/`w2`/`w3` plus `personas`, `schemas_touched`, `archetype_id`, `mesh_id`. Library loader tolerates legacy compact shape (`t/s/b/k/kk` keys) and transparently migrates to extended shape on load. `compact_to_extended` and `extended_to_compact` round-trippers preserve fidelity.)*
- [ ] Subtask 28.1.3 — Compact 3-dot micro Wave-progress indicator per modal row *(UI; front-end track)*
- [ ] Subtask 28.1.4 — Row-click expands inline to show full Wave ribbon (no new modal; expand-in-place pattern) *(UI; front-end track)*
- [ ] Subtask 28.1.5 — Expand/collapse animation respecting `prefers-reduced-motion` *(UI; front-end track)*
- [x] Subtask 28.1.6 — Validation: every library row has non-empty w1/w2/w3 *(`validate_wave_data_presence` ships in `apex_scenarios.validators` with `WAVE_MISSING` issue code per row missing any of W1/W2/W3. CI lane wires the check; flag `--skip-wave-check` lets the lane stay green during the Task 28.1.1 content-authoring ramp, then is removed when content is complete.)*

### Task 28.2 — W1 Foundation catalog (BL.P.171, BL.P.172, BL.P.173)
*(2026-05-05 parallel-track Python deliverables — `apex_scenarios.foundation` shipped with 40 building blocks across the five canonical classes. UI subtask 28.2.3 (Foundation-Catalog HTML tab) remains on the front-end track.)*
- [x] Subtask 28.2.1 — Inventory ~40 reusable W1 building blocks across five classes  *(`apex_scenarios.foundation.CATALOG`: 40 blocks shipped — 12 schema (SCML/MERML/CXML/PatientML/ClaimML/EncounterML/GridML/OutageML/QMSML/OpsML-TH/TravelerML/BSSML), 8 ledger (audit-row, replay-token, Purview Audit Premium, PSPS evidence, SEP-1 bundle, FSMA 204, claim cycle, dispatch decision), 10 mcp (per-schema readonly + write-tool HITL wiring + terminology stub), 5 hitl (Teams card, Copilot Studio, approval state machine, SLA timer Redis, VP-level gate), 5 policy (PII/PHI/PCI/CIP-014/IP-CUI classifications))*
- [x] Subtask 28.2.2 — Per-block fields  *(`FoundationBlock` frozen dataclass: name, cls, description, schemas_touched, effort_story_points, effort_calendar_weeks, prerequisites, unblocks_w2_scenarios)*
- [ ] Subtask 28.2.3 — New sibling tab `Foundation-Catalog` in Stacked Architecture HTML  *(UI; front-end track)*
- [x] Subtask 28.2.4 — W1-to-W2 dependency graph  *(`dependency_graph_edges()` returns every (prereq_name, block_name) edge in the catalog DAG; `transitive_prerequisites(name)` returns topologically-sorted ancestor chain; `blocks_unblocking_scenario(service_code)` returns blocks whose `unblocks_w2_scenarios` includes the named W2 service code)*
- [x] Subtask 28.2.5 — SoW-quotable effort roll-up  *(`effort_rollup(blocks)` returns `EffortRollup` with selected_count, total_story_points, total_calendar_weeks (sequential ceiling), parallelizable_calendar_weeks (longest-prereq-chain wall clock when branches parallelize), by_class breakdown)*
- [x] Subtask 28.2.6 — Cross-link from every scenario's W1 ribbon cell to W1 catalog entries  *(`blocks_unblocking_scenario(service_code)` is the cross-link API — front-end consumes for tooltip/anchor population)*

### Task 28.3 — W3 Fusion catalog (BL.P.174, BL.P.175, BL.P.176)
*(2026-05-05 parallel-track Python deliverables — `apex_scenarios.fusion` shipped with 36 named meshes across all 7 Practices. UI subtasks 28.3.4 + 28.3.5 (Chains-tab section + Wave-ribbon variant) remain on the front-end track.)*
- [x] Subtask 28.3.1 — Author 5-8 named fusion meshes per Practice (35-56 total)  *(`apex_scenarios.fusion.CATALOG`: 36 meshes total — RC 5, HLS 6, ER 5, AXLE 5, TMT 5, TH 5, ICE 5; per-Practice count enforced in catalog with module-level assertion 35 ≤ N ≤ 56; conformance test asserts 5 ≤ count ≤ 8 per Practice)*
- [x] Subtask 28.3.2 — Reference meshes shipped  *(`mesh.rc.perishables-economics` (cold-chain + markdown + store-ops-intelligence → perishables P&L recovery), `mesh.hls.revenue-and-outcomes` (denial prevention + prior-auth + care-gap → payer-aligned revenue + outcomes), `mesh.er.grid-reliability` (outage triage + restoration + vegetation-risk → territory reliability) — all three named meshes plus 33 per-Practice equivalents)*
- [x] Subtask 28.3.3 — Per-mesh fields  *(`FusionMesh` frozen dataclass: mesh_id, practice, name, description, constituent_w2_service_codes, composed_outcomes, orchestration_archetype (Sprint 19 archetype id), target_tenant_profile)*
- [ ] Subtask 28.3.4 — New section in Chains tab for W3 Fusion meshes  *(UI; front-end track)*
- [ ] Subtask 28.3.5 — Fusion-mesh Wave ribbon variant  *(UI; front-end track)*
- [x] Subtask 28.3.6 — Cross-link from every scenario's W3 ribbon fusion-partner mention to mesh entry  *(`mesh_by_w2_service_code(service_code)` returns every mesh that includes the named W2 service code — front-end consumes for ribbon-to-mesh anchor)*

**Sprint 28 Tasks 28.2 + 28.3 deliverables shipped (parallel-track Python):**
- `apex_scenarios.foundation` module — 40 W1 building blocks across 5 canonical classes with prerequisite DAG + critical-path effort rollup
- `apex_scenarios.fusion` module — 36 W3 fusion meshes (5-8 per Practice) with constituent W2 service-code linkage + cross-link helper
- 5 new CLI subcommands wired into `apex scenarios`: `foundation-list`, `foundation-rollup`, `foundation-prereqs`, `fusion-list`, `fusion-show`, `fusion-by-w2`
- 31 new tests in `apex-scenarios/tests/test_foundation_and_fusion.py` covering catalog completeness, class taxonomy, effort-rollup arithmetic + critical-path math, dependency-graph integrity (no dangling prereqs), per-Practice mesh count band, named-reference-mesh presence, mesh-to-W2 round-trip lookup, plus 5 conformance markers
- **Cross-package suite at 667 of 667** — clean (the previously-flaky `apex_scenarios` import issue resolved when the new submodules were installed)

### Task 28.4 — Export tooling (BL.P.177, BL.P.178)
*(2026-05-04 — Python CSV exporter parallel-track deliverables. PPTX export and embedded-font branding remain on the front-end track via pptxgenjs.)*
- [x] Subtask 28.4.1 — Client-side CSV export of library or filtered subset (title · service · brief · w1/w2/w3 · kpi) *(`apex_scenarios.exporters.write_csv` writes UTF-8-with-BOM CSV (Excel-friendly) covering 11 columns: practice, service_code, title, brief, kpi, kpi_direction, w1, w2, w3, archetype_id, mesh_id. CLI: `apex scenarios export-csv --practice RC --output ...`. Real-repo smoke test: 102 RC rows exported clean.)*
- [ ] Subtask 28.4.2 — PowerPoint export: one slide per scenario with chain rows + wave ribbon; uses pptxgenjs on the server side via worker *(server-side JS / pptxgenjs; front-end track)*
- [x] Subtask 28.4.3 — Filename auto-generation (`APEX-scenarios-{practice}-{date}.csv`) *(`apex_scenarios.exporters.csv_filename` — practice segment collapses to `all` (7 practices), `multi` (2-6), `<lower>` (1), `empty` (0); optional label segment; ISO-8601 date; nine tests covering every collapse case)*
- [ ] Subtask 28.4.4 — Branding: Fraunces + IBM Plex Sans embedded fonts; APEX color tokens *(font embedding lives in PPTX export; out of scope for the Python parallel track)*

### Task 28.5 — Cross-practice search (BL.P.179)
- [ ] Subtask 28.5.1 — New "Browse all 723 scenarios" CTA at top of Chains tab (above per-practice groups)
- [ ] Subtask 28.5.2 — Shared modal with practice-tag chip filters (multi-select: RC / HLS / ER / AXLE / TMT / TH / ICE)
- [ ] Subtask 28.5.3 — Free-text filter stacked with chip filters
- [ ] Subtask 28.5.4 — Practice indicator on each row (tiny banner-color-coded dot)

### Task 28.6 — Keyboard affordances (BL.P.180)
- [ ] Subtask 28.6.1 — `/` focuses filter from anywhere in modal
- [ ] Subtask 28.6.2 — `↑/↓` navigate modal rows; `Enter` expands selected row's wave ribbon
- [ ] Subtask 28.6.3 — `Esc` close modal (already native; verify accessibility)
- [ ] Subtask 28.6.4 — Visible keyboard-help tooltip on modal header

### Task 28.7 — Governance & traceability validators (BL.P.181–185)
*(2026-05-04 — Python validators all shipped in `apex_scenarios.validators`. Real-repo dry-run on the live 723-row library: service_codes 723/723 ✅, kpis 723/723 ✅, agent_references 35/35 (1 minor warning). 76 unit tests in `apex-scenarios`.)*
- [x] Subtask 28.7.1 — Appendix L publication: Scenario Library Master Catalog (JSON + readable markdown per Practice) *(`apex_scenarios.publication` ships `publish_master_catalog` writing 8 files (1 index + 7 per-Practice). Each per-Practice file: long name, total count, per-row table with service code · title · KPI. Index: cross-Practice coverage table, per-Practice links, wave-data completion status. CLI: `apex scenarios publish-catalog <out>`. Real-repo smoke test: 8 markdown files written cleanly.)*
- [x] Subtask 28.7.2 — Scenario-to-Service-Catalog validator: every `service_code` resolves to a Service Catalog entry (blocks CI if not) *(`validate_service_codes` runs in two modes: structural (regex against `{PRACTICE}-{Track}-{NN}` with hyphenated multi-segment Track support up to 3 segments) and closed-enum (when `service_catalog_codes` set is supplied from BL.P.110–116). Real-repo dry-run: 723/723 pass structural check.)*
- [x] Subtask 28.7.3 — Scenario-to-Agent-Catalog validator: featured-scenario Solutions name agents registered in agent catalogs (BL.P.58–64) *(`validate_agent_references` parses Solution strings for `<noun-phrase> agent` patterns. `extract_agent_references` strips leading determiners ("the", "an", "this", etc. — 18 stopwords), caps at 3-token noun phrases, returns lowercased phrases. `_agent_resolves` allows tail-substring resolution (e.g., "real-time perishables-integrity" resolves when "perishables-integrity" is registered). Without a catalog supplied, downgrades unresolved-references to warnings.)*
- [x] Subtask 28.7.4 — Scenario-to-KPI-Registry validator: featured-scenario KPIs resolve to Appendix C entries *(`validate_kpis` + `extract_kpi_name` parse the canonical delta forms: percentage/point (`+2.4pp GM`, `-15% MAPE`, `+6-9pp OEE` ranges) and money (`+$2.8M/yr recovery`, `−$18M inventory` — both U+002D and U+2212 minus accepted). Trailing KPI names with `&` characters supported (`F&B capture`). Real-repo dry-run: 723/723 KPIs parse.)*
- [x] Subtask 28.7.5 — Scenario versioning rules: PATCH (copy edits, KPI re-measurements) · MINOR (new scenario) · MAJOR (field-schema change) *(`classify_library_bump(before, after)` returns `VersioningClassification` with `bump`, `rationale`, `added`, `removed`, `field_schema_changed`. Detection logic: field-set diff via `model_dump(exclude_unset=True)` keys; scenario-set diff via stable scenario-key composition. CLI: `apex scenarios bump <before.json> <after.json>`.)*
- [x] Subtask 28.7.6 — CI workflow lane that runs all validators on PR *(`.github/workflows/ci.yml` ➜ new `scenarios` job runs `apex scenarios validate --skip-wave-check` (wave check held off until Task 28.1.1 content lands), `apex scenarios stats`, and `apex scenarios publish-catalog` to a tmpdir. Uploads `scenarios-appendix-l-preview` artifact for 14 days. Drop `--skip-wave-check` once W1/W2/W3 content authored across all 723 rows.)*

---

## Sprint 29 — Communication Artifacts & Compliance Pipeline

**Closes:** BL.P.186–195
**Status:** ✅ Python parallel-track complete (Tasks 29.2 + 29.3 + 29.8 + 29.9 + 29.10) — `apex-compliance-lint` package, Appendix N + companion CSS tokens, Appendix O, Chains-port spec, two design-token compliance tools, and the four-lane GitHub Actions workflow shipped 2026-05-05. Tasks 29.1 + 29.4 + 29.5 + 29.6 + 29.7 ship on the front-end / Word / PPTX track and have prerequisites in place.
**Goal:** Publish the three normative appendices (Narration Script Catalog, Design-System Reference, Visual Artifacts Index), produce companion communication artifacts (one-pager, slide deck, narrated Runtime Addendum), ship the Independence-language linter as a reusable package, and harden the pre-publish CI lane across all artifact build pipelines.
**Exit criteria:** Appendices M / N / O published and cross-linked from Design Reference §§20–22; companion artifacts delivered to `/outputs/`; `apex-compliance-lint` package published with unit tests; CI pre-publish lane enforces all four compliance checks (linguistic / typography / color / responsive-smoke) on every artifact PR.

### Task 29.1 — Appendix M: Narration Script Catalog (BL.P.186)
- [ ] Subtask 29.1.1 — Extract all 11 tab narration decks from Stacked Architecture HTML as standalone markdown
- [ ] Subtask 29.1.2 — Preserve scene anchors + timing guidance (90–180 s/tab)
- [ ] Subtask 29.1.3 — Cross-reference each scene to Design Reference sections and Sellers Guide sections
- [ ] Subtask 29.1.4 — Add pronunciation notes for ambiguous terms (SKU, KQL, LEDGER, SCADA)
- [ ] Subtask 29.1.5 — Publish as `APEX-Appendix-M-Narration-Catalog.md`

### Task 29.2 — Appendix N: Design-System Reference (BL.P.187)  ✅
- [x] Subtask 29.2.1 — Typography reference  *(`docs/APEX-Appendix-N-Design-System.md` §1: Fraunces (display), IBM Plex Sans (body), JetBrains Mono (code) with per-element weight/size guidance + italic-usage rules)*
- [x] Subtask 29.2.2 — Color-token reference for dark + light themes  *(§2: 14 dark-theme tokens + 11 light-theme tokens; `body.light` toggle pattern; explicit forbid on inline hex outside `apex-design-tokens.css`)*
- [x] Subtask 29.2.3 — Per-practice banner color registry  *(§3: 7-Practice rail tokens (`--apex-rail-rc/hls/er/axle/tmt/th/ice`) with dark + light variants)*
- [x] Subtask 29.2.4 — Spacing / radius / shadow tokens  *(§4: 9 spacing tokens (8px base), 4 radius tokens (sm / md / lg / pill), 3 shadow tokens (sm / md / lg))*
- [x] Subtask 29.2.5 — Responsive breakpoint rules  *(§5: 5 breakpoint tokens (sm 360 / md 640 / lg 900 / xl 1280 / 2xl 1440); Sprint 27 ≤900px collapse rule)*
- [x] Subtask 29.2.6 — Accessibility baseline  *(§6: WCAG 2.2 AA contrast invariants + 2px focus indicator + `prefers-reduced-motion` + `prefers-color-scheme` + ARIA + keyboard affordances)*
- [x] Subtask 29.2.7 — Independence linguistic rules + approved-substitute table  *(§7: full forbidden-language table with rule_ids referencing `apex-compliance-lint` rule pack + domain-of-art exceptions auto-suppressed + brand-and-positioning second table)*
- [x] Subtask 29.2.8 — Publish + companion CSS  *(`docs/APEX-Appendix-N-Design-System.md` published; `docs/apex-design-tokens.css` companion stylesheet ships the tokens as CSS custom properties + `@media (prefers-reduced-motion)` rules + `:focus-visible` baseline)*

### Task 29.3 — Appendix O: Visual Artifacts Index (BL.P.188)  ✅
- [x] Subtask 29.3.1 — Artifact table  *(`docs/APEX-Appendix-O-Visual-Artifacts-Index.md` §1: 22 artifacts catalogued with filename, format, audience, purpose, Design-Reference §§ cross-link, status (Published / Pending / Stale))*
- [x] Subtask 29.3.2 — Cross-reference matrix  *(§2: per-artifact usage of Scenario Library / Wave Ribbon / Narration Deck / Independence Lint / Design Tokens with ✅/☑/— symbols across 22 rows)*
- [x] Subtask 29.3.3 — Publish  *(file published; §3 status legend + §4 re-publication-trigger matrix + §5 build-provenance string format + cross-references to Sprint 19/27/28/29 deliverables)*

### Task 29.4 — Executive one-pager (BL.P.189)
- [ ] Subtask 29.4.1 — 35 featured scenarios in scannable table (practice · title · service · primary KPI · wave-progression summary)
- [ ] Subtask 29.4.2 — Fraunces typography; landscape single-page letter
- [ ] Subtask 29.4.3 — PDF + DOCX output

### Task 29.5 — Companion SteerCo slide deck (BL.P.190)
- [ ] Subtask 29.5.1 — One chain per Practice (7 slides, one per Practice)
- [ ] Subtask 29.5.2 — Per slide: full 6-row chain (Scenario · Solution · Use Case · Service · Persona · KPI) + Wave ribbon sidebar
- [ ] Subtask 29.5.3 — APEX design tokens embedded; dark-mode master slide
- [ ] Subtask 29.5.4 — Generate via pptxgenjs; present as `APEX-Seven-Practices-SteerCo-Deck.pptx`

### Task 29.6 — Narrated Runtime Addendum (BL.P.191)
- [ ] Subtask 29.6.1 — Port Sellers Guide Runtime Addendum (BL.C.30b) into narrated single-file HTML
- [ ] Subtask 29.6.2 — 5-scene narration deck (Orchestration · HITL · LEDGER · Audit Row · KPI Attribution)
- [ ] Subtask 29.6.3 — Brian voice, ~4 minutes total narration
- [ ] Subtask 29.6.4 — Present as `APEX-Runtime-Addendum-Narrated.html`

### Task 29.7 — Tracked-changes Sellers Guide v1.2 (BL.P.192)
- [ ] Subtask 29.7.1 — Generate tracked-changes DOCX showing v1.2 additions (Scenario Library references, Wave Ribbon cross-references, design-system conventions)
- [ ] Subtask 29.7.2 — Reviewer-ready for Practice Lead sign-off

### Task 29.8 — Chains-tab port spec (BL.P.193)  ✅
- [x] Subtask 29.8.1 — Claude Code build-instruction markdown  *(`docs/APEX-Chains-Port-Spec.md`: §1 goal, §2 component inventory (embed vs. reference rows), §3 dependencies, §4 embed-vs-reference decision matrix, §5 merge-conflict avoidance with named conflict scenarios, §6 10-step implementation procedure for the front-end engineer, §7 acceptance criteria, §8 rollback procedure)*
- [x] Subtask 29.8.2 — Component inventory + decision matrix + merge guidance  *(per §2-§5 above; covers chains-tab markup, practice-rail banners, chain-card collapsibles, wave-ribbon SVG, scenario-library-modal, kpi-chip variants, cross-practice-search CTA — and explicitly which references vs. embeds)*
- [x] Subtask 29.8.3 — Publish  *(file published at `docs/APEX-Chains-Port-Spec.md`)*

### Task 29.9 — `apex-compliance-lint` package (BL.P.194)  ✅
- [x] Subtask 29.9.1 — Standalone Python package with Independence-language rules  *(`packages/apex-compliance-lint/`: `Rule` / `RulePack` / `Severity` / `Violation` / `LintReport` core types; engine with ±60-char inline + ±2-line neighborhood suppression contexts; 7 Independence rules (`partner` / `alliance` / `partnership` / `endorse` / `recommended_by` / `deloitte_microsoft_jointly` / `gold_partner`) with allowed contexts (`_AWARD_PARTNER`, `_DOMAIN_PARTNER`, `_QUOTED_TERM`, `_NEGATED_TERM`, `_COMMUNITY_PATTERN`) for false-positive guards)*
- [x] Subtask 29.9.2 — File-type adapters  *(four adapters: `HTMLAdapter` (stdlib `html.parser` with `<script>` / `<style>` skip), `MarkdownAdapter` (fence + frontmatter + link-text-preserving stripper), `DOCXAdapter` (python-docx with stdlib zipfile fallback), `PPTXAdapter` (python-pptx with stdlib zipfile fallback). `default_registry()` exposes the extension → adapter mapping)*
- [x] Subtask 29.9.3 — Configurable rule pack  *(three packs ship: `DELOITTE_MICROSOFT_INDEPENDENCE` (7 rules ERROR), `APEX_TYPOGRAPHY` (1 rule WARNING — unapproved-font), `APEX_BRAND` (5 rules: black-box, fully-autonomous, guarantees ERROR; AI-powered, silver-bullet WARNING). `DEFAULT_PACKS` is the baseline; tenants extend with their own `RulePack` instances without touching the engine)*
- [x] Subtask 29.9.4 — CLI  *(`apex-compliance-lint <paths> [--pack ...] [--severity ...] [--quiet] [--fail-on-warnings]` registered as `console_script`; resolves directories to file lists via `default_registry()` extension matching; per-violation rendering with rule_id + matched text + guidance + approved substitutes; final summary with counts)*
- [x] Subtask 29.9.5 — Exit codes per spec  *(0 clean, 1 violations, 2 config error including unknown pack / unknown severity / no files matched / no paths given)*
- [x] Subtask 29.9.6 — Unit tests  *(28 tests including positive cases (every Independence rule fires on its target prose), false-positive suppression (trading partner / Microsoft Partner Of The Year / channel partner / quoted-metalinguistic / negated assertions all suppressed), brand-rule ERRORs, multi-file `lint_paths` aggregation, exit-code semantics, plus 4 conformance markers — including a real-repo workspace-files independence-clean assertion against the Sprint 26 workspace)*

### Task 29.10 — Pre-publish CI lane (BL.P.195)  ✅
- [x] Subtask 29.10.1 — GitHub Actions workflow  *(`.github/workflows/artifact-compliance.yml`: `pull_request` trigger on artifact-touching paths; 5 jobs (4 lanes + PR-comment summarizer); `permissions` scoped to contents-read + pull-requests-write)*
- [x] Subtask 29.10.2 — Lane 1: Independence linter on PR diff  *(installs `apex-compliance-lint`, computes diff via `git diff --name-only --diff-filter=AMR base..head -- *.html *.htm *.md *.docx *.pptx`, runs the linter on the diff with `--severity warning`; output captured as workflow output for the summary comment)*
- [x] Subtask 29.10.3 — Lane 2: typography correctness  *(`tools/check_typography_tokens.py`: scans CSS / HTML for `font-family` declarations, asserts each family is in `APPROVED_FAMILIES` (Fraunces / IBM Plex Sans / JetBrains Mono + system-fallback chain) OR resolves through `var(--apex-font-...)`; allowlist for `apex-design-tokens.css` (the canonical source))*
- [x] Subtask 29.10.4 — Lane 3: color-token compliance  *(`tools/check_color_tokens.py`: scans CSS / HTML for inline hex literals (3/4/6/8-digit), forbids any outside `apex-design-tokens.css`; doc-name-pattern allowlist auto-exempts `appendix-n` / `design-system` documentation files; HTML-entity false positives (`&#33;`) suppressed via word-boundary)*
- [x] Subtask 29.10.5 — Lane 4: responsive Playwright smoke  *(workflow lane installs Playwright + Chromium; auto-discovers HTML artifacts under `docs/` (excluding legacy `docs/book/`); for each artifact × each viewport (360 / 900 / 1440 px): `page.goto` + `domcontentloaded` + assert no `pageerror` / `console.error` events + assert `<body>` present; uploads results as 14-day artifact)*
- [x] Subtask 29.10.6 — Failure blocks merge + PR comment  *(workflow declares all 4 lanes as required jobs (chained via `needs:`); final `pr-comment` job with `if: always()` posts a status table via `actions/github-script`, links back to Appendix N as the source-of-truth, surfaces the lane results with ✅/❌/⏭️ icons)*

**Sprint 29 Python-track deliverables shipped:**
- `packages/apex-compliance-lint/` Python package — Independence + typography + brand rule packs + 4 file-type adapters + `apex-compliance-lint` console script
- `tools/check_typography_tokens.py` + `tools/check_color_tokens.py` — design-token CI tools (Lanes 2 + 3)
- `.github/workflows/artifact-compliance.yml` — 4-lane pre-publish CI workflow with PR-comment summarizer
- `docs/APEX-Appendix-N-Design-System.md` + `docs/apex-design-tokens.css` — Design-System reference + canonical CSS-tokens stylesheet
- `docs/APEX-Appendix-O-Visual-Artifacts-Index.md` — Visual artifacts index
- `docs/APEX-Chains-Port-Spec.md` — Chains-tab port build-instructions for the front-end engineer
- 28 + 20 = **48 new Sprint 29 tests passing**; cross-package suite at **695 of 695** + tools at **34 of 34**.

**Front-end / Word / PPTX track items remaining for Sprint 29:**
- Task 29.1 — Appendix M Narration Catalog (depends on HTML extraction track)
- Task 29.4 — Executive one-pager PDF + DOCX (Word track)
- Task 29.5 — SteerCo deck PPTX (pptxgenjs Node track)
- Task 29.6 — Narrated Runtime Addendum HTML (front-end track)
- Task 29.7 — Tracked-changes Sellers Guide v1.2 DOCX (Word track)

---

## Cross-Sprint Dependencies

Readability guide — a sprint cannot start until its upstream dependencies are merged:

```
Sprint 1  ────────────────┐
                          ▼
Sprint 2 (RC anchor) ──► Sprint 3 (other Practices)
                          │
Sprint 4 (Bronze) ◄───────┤
Sprint 5 (Silver + tokens) ◄── 4
Sprint 6 (Gold + measures) ◄── 5
                          │
Sprint 7 (Utility MCP) ◄── 1, 5, 6
Sprint 8 (Domain MCP) ◄─── 7
Sprint 9 (External MCP) ◄── 7
Sprint 10 (Identity/Lattice) ◄── 7
                          │
Sprint 11 (Orchestration + HITL) ◄── 1, 7, 10
Sprint 12 (Audit row) ◄──── 1, 7
Sprint 13 (Purview) ◄────── 4, 5, 6, 12
                          │
Sprint 14 (Fabric capacity) — can run in parallel from Sprint 1
                          │
Sprint 15 (SOR adapters) ◄── 4, 13
Sprint 16 (Agent catalogs) ◄── 8, 10, 11
Sprint 17 (Service catalogs) ◄── 16
Sprint 18 (Reference deployments) ◄── 16, 17
Sprint 19 (Appendices + playbooks) ◄── all of the above

Sprint 20 (Standards registry) ◄─ 1
Sprint 21 (Per-standard packages) ◄─ 20
Sprint 22 (Identifier + terminology bindings) ◄─ 20, 21
Sprint 23 (Message-format translators) ◄─ 21, 22; blocks 15 SOR adapter depth
Sprint 24 (Cross-standard translators) ◄─ 21, 22, 23
Sprint 25 (Protocol adapters) ◄─ 21, 22; blocks 15 for ER / AXLE / ICE SOR adapters
Sprint 26 (v0.2 control plane: Redis + OpenClaw) ◄─ 1, 7, 10, 11, 12, 14

Sprint 27 (Scenario Library + Wave Ribbon + Design System) ✅ COMPLETE
  ├─ produced artifacts in parallel with core build
  └─ informs Sprint 16 (agent catalogs), Sprint 17 (service catalogs), Sprint 18 (reference deployments)

Sprint 28 (Library extensions: W1 Foundation + W3 Fusion + tooling) ◄─ 27
  └─ prefers 17 (Service Catalogs) + 19 (KPI Registry) for traceability validators; can partially run without them

Sprint 29 (Communication artifacts + compliance pipeline) ◄─ 27, 28
  └─ publishes Appendices M / N / O and the compliance-lint package
```

**Parallelization guidance:**
- Sprints 2 & 14 can start immediately after Sprint 1.
- Sprint 3 runs in parallel by Practice lead once Sprint 2 anchors the pattern.
- Sprints 8, 9, 10 can run concurrently once Sprint 7 ships.
- Sprint 16 agent catalogs can parallelize by Practice lead.
- Sprint 18 reference deployments can parallelize by Practice once 16 & 17 ship.
- **Sprints 20–22 can run in parallel with Sprints 3–6** — the standards foundation is orthogonal to medallion build-out. Sprint 21 Phase 1 is already complete; Sprint 22 is mostly complete.
- **Sprint 23 translators inform Sprint 15 SOR adapter depth** — schedule at least EDI X12 (P.155) and HL7 v2 (P.156) before HLS and RC SOR adapters complete.
- **Sprint 26 requires Sprints 1, 7, 10, 11, 12, 14** — manifest contract, utility MCPs (telemetry + ledger), identity lattice, orchestration runtime, audit row, and Fabric capacity must all be live before Redis cache ships to production. Workspace-file subtasks (26.1, 26.2, 26.3) can run earlier as doc-first work.
- **Sprint 25 protocol adapters unblock Sprint 15 rows 15.5 and 15.6** — OPC UA and IEC 61850 are prerequisites for the industrial-historian SOR adapters.
- **Sprint 27 ran in parallel with the core implementation sprints** — delivered as a pure communication-layer artifact; no runtime dependency. Its outputs are inputs to Sprint 16 (agent catalogs cite featured-scenario Solutions), Sprint 17 (service catalogs cite scenario `service_code`s), and Sprint 18 (reference deployments map to featured scenarios).
- **Sprint 28 should ideally follow Sprint 17 and Sprint 19** — the Service Catalog and KPI Registry are the targets of its traceability validators. However, the W1 Foundation catalog and Wave-ribbon propagation subtasks (28.1, 28.2) can run earlier as pure authoring work.
- **Sprint 29 can start mid-Sprint 28** — the narration-script extraction, one-pager, and slide deck don't depend on Sprint 28 deliverables. The `apex-compliance-lint` package and CI lane can be stood up immediately from Sprint 27 learnings.

---

## ===== APEX-M Sprints 30–49 (added 2026-05-09) =====

The work below is RC-practice-only and APEX-M-only per the [Sprint Plan](Sprint-Plan.md) first-iteration scope. See [Sprint Execution Order](Sprint-Execution-Order.md) for the dependency graph between these sprints and parallelization strategy.

### Sprint 30 — RC W1 Foundation (Lab tenant + medallion)

**Closes:** items 30.1–30.6 in [`services/rc/_build-status.yaml`](../../services/rc/_build-status.yaml)
**Owner:** Data SRE
**Depends on:** nothing — can start in parallel with Sprint 41
**Goal:** Provision a real Lab Azure tenant with Bicep + Fabric capacity + medallion + the 4 Silver schema families RC consumes (SCML / MERML / PROML / CRMML) + the 6 RC-E2E-03 Gold marts.

#### Task 30.1 — Layer 1 platform Bicep apply
- [ ] 30.1.1 — `az login` to Lab subscription; verify deployment principal has Owner on RG
- [ ] 30.1.2 — `az deployment group create` against `apex-m/infra/bicep/blueprints/w1-foundation.bicep` (already authored)
- [ ] 30.1.3 — Verify outputs: identity ID + ledger DSN + Log Analytics workspace + (Foundry account if `provisionFoundry: true`)

#### Task 30.2 — Fabric capacity + primary workspace
- [ ] 30.2.1 — Provision F-SKU capacity via `infra/terraform/modules/fabric_capacity/` (existing)
- [ ] 30.2.2 — Apply `apex-m/infra/bicep/platform/fabric.bicep` (NEW — primary-workspace pattern per Services Guide §1.6) to create `rc-canonical` primary workspace + per-service consumer workspaces
- [ ] 30.2.3 — Configure Fabric workspace identity per [Microsoft Learn — workspace identity](https://learn.microsoft.com/fabric/security/workspace-identity)
- [ ] 30.2.4 — Set up trusted workspace access for ADLS Gen2 reads

#### Task 30.3 — Bronze landing
- [ ] 30.3.1 — POS source — Eventstream landing with DeltaFlow CDC transformation per DEP-003
- [ ] 30.3.2 — ERP source — Mirroring (Azure SQL or PostgreSQL flex per client)
- [ ] 30.3.3 — Refrigeration telemetry — Eventstream from IoT Hub
- [ ] 30.3.4 — Competitor pricing — Data Pipeline (daily batch CSV)

#### Task 30.4 — Silver schemas (per Services Guide §18.1)
- [ ] 30.4.1 — `SCML.Inventory` · `SCML.Lot` · `SCML.Movement` (canonical conformance + tokenizer)
- [ ] 30.4.2 — `MERML.Markdown` · `MERML.Elasticity` · `MERML.Competitor` · `MERML.Promotion`
- [ ] 30.4.3 — `PROML.Pricing` · `PROML.DiscountRule` (read by The Pricer)
- [ ] 30.4.4 — `CRMML.Customer` · `CRMML.Loyalty` · `CRMML.Interaction` (RC-E2E-04 / -07 / -08)

#### Task 30.5 — Gold marts for RC-E2E-03
- [ ] 30.5.1 — `g_excursion_decision_panel` (Direct Lake semantic model)
- [ ] 30.5.2 — `g_markdown_proposal_basis`
- [ ] 30.5.3 — `g_pricing_recommendation_basis` (read by The Pricer per Services Guide §25.8)
- [ ] 30.5.4 — `g_inventory_position_current`
- [ ] 30.5.5 — `g_kpi_rc_e2e_03_daily` (Power BI Direct Lake)
- [ ] 30.5.6 — `g_markdown_outcome_attribution`

**Exit criteria:** Lab tenant alive; primary `rc-canonical` workspace owns Silver entities; per-service consumer workspaces (`rc-e2e-03`, etc.) read Silver via OneLake shortcuts; Power BI Direct Lake report on `g_kpi_rc_e2e_03_daily` opens for an authorized operator.

---

### Sprint 41 — Phase I.1 Production Entra Agent ID

**Closes:** items 41.1–41.5 in `services/rc/_build-status.yaml`
**Owner:** Identity SRE
**Depends on:** nothing — can start in parallel with Sprint 30
**Goal:** Replace `MockAgentIdentityProviderEntra` with `AgentIdentityProviderEntra` production calls; verify against Lab Entra tenant.

#### Task 41.1 — Lab Entra access provisioning
- [ ] 41.1.1 — Grant deployment principal `Application.ReadWrite.All` + `AgentIdentity.ReadWrite.All` on Microsoft Graph
- [ ] 41.1.2 — Verify `azd auth login` works with the deployment principal

#### Task 41.2 — Wire production SDKs
- [ ] 41.2.1 — Add `azure-identity[default]` + `httpx` + `msal` to `apex-m/pyproject.toml` `[project.optional-dependencies] runtime`
- [ ] 41.2.2 — Verify lazy-import path in `apex_m.identity_entra` remains valid (architecture commit already structured this)
- [ ] 41.2.3 — Implement OAuth 2.0 OBO flow per [Microsoft identity platform docs](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-on-behalf-of-flow) — currently raises NotImplementedError

#### Task 41.3 — Integration tests
- [ ] 41.3.1 — Add `apex-m/tests/integration/test_identity_entra.py` — pytest module with `pytest.mark.integration` marker
- [ ] 41.3.2 — Tests: idempotent blueprint upsert, identity provision, get_identity, revoke, list_blueprints
- [ ] 41.3.3 — CI lane runs integration tests against a dedicated Lab tenant via Workload Identity Federation

#### Task 41.4 — Bicep deployment script verification
- [ ] 41.4.1 — Apply `apex-m/infra/bicep/platform/identity.bicep` against Lab subscription
- [ ] 41.4.2 — Verify `Microsoft.Resources/deploymentScripts` runs successfully
- [ ] 41.4.3 — Confirm `apex-m-tenant-root` blueprint exists via `Get-MgAgentIdentityBlueprint` (Microsoft Graph PowerShell)

**Exit criteria:** `AgentIdentityProviderEntra` provisions blueprints + identities against real Lab Entra; OBO token issued for synthetic operator + agent_id pair; integration tests green in CI.

---

### Sprint 42 — Phase I.2 Production Foundry Runtime + Microsoft Agent Framework

**Closes:** items 42.1–42.5
**Owner:** Runtime SRE
**Depends on:** Sprint 41
**Goal:** Replace `MockAgentRuntimeFoundry` with production calls against Foundry Agent Service hosted agents; wire all 5 Microsoft Agent Framework canonical patterns per ADR-006.

#### Task 42.1 — Wire production SDKs
- [ ] 42.1.1 — Add `azure-ai-projects` + `agent-framework` (Microsoft Agent Framework) + `agent-framework-azure-ai` to apex-m runtime extras
- [ ] 42.1.2 — Implement `deploy_agent` against `Microsoft.CognitiveServices/accounts/projects/agents` (Foundry Hosted Agents)
- [ ] 42.1.3 — Implement `invoke` + `invoke_async` via Microsoft Agent Framework `Agent.run` / `Agent.run_stream`
- [ ] 42.1.4 — Implement `drain` + `list_agents` against Foundry projects API

#### Task 42.2 — The 5 canonical Agent Framework patterns
Per [Agent Framework workflow orchestrations docs](https://learn.microsoft.com/agent-framework/workflows/orchestrations/) — wire each pattern as a callable in `apex_m.runtime_foundry`:
- [ ] 42.2.1 — `BuildSequential([assess, classify, quantify, decide, act, learn])` for use cases with `orchestration_archetype: sequential`
- [ ] 42.2.2 — `BuildConcurrent([...])` with custom aggregator for `concurrent`
- [ ] 42.2.3 — `BuildHandoff(initial=..., handoffs=[...])` for `handoff`
- [ ] 42.2.4 — `BuildGroupChat([...], manager=...)` for `group_chat`
- [ ] 42.2.5 — `BuildMagentic(manager=Analyst, specialists=[...])` for `magentic` — used by RC-E2E-03 cold-chain (The Analyst is the manager)
- [ ] 42.2.6 — Each pattern read its archetype from the use-case YAML's `orchestration_archetype` field

#### Task 42.3 — Bicep + integration test
- [ ] 42.3.1 — Apply `apex-m/infra/bicep/platform/foundry.bicep` (AVM module wrapper) against Lab subscription with full BYO Storage + AI Search + Cosmos DB
- [ ] 42.3.2 — Deploy The Pricer agent for `rc-cold-chain-excursion-mid-shift` via `azd deploy`
- [ ] 42.3.3 — Invoke with synthetic excursion event from the canonical fixture; verify response
- [ ] 42.3.4 — Verify Foundry Application Insights captures the run

**Exit criteria:** A real Foundry hosted agent runs The Pricer against the canonical cold-chain fixture; Magentic pattern coordinates 5 specialist agents per RC-E2E-03 use case; Application Insights traces the run end-to-end.

---

### Sprint 43 — Phase I.3 Production Fabric DataLake (OneLake user identity mode)

**Closes:** items 43.1–43.3
**Owner:** Data SRE (rotates from Sprint 30)
**Depends on:** Sprint 30 + Sprint 41
**Goal:** `DataLakeFabric` reads Lab Fabric workspace with operator OBO passthrough; OneLake user identity mode honored end-to-end.

- [ ] 43.1 — Wire `pyodbc` + `azure-identity` for SQL analytics endpoint with OBO token (per Services Guide §1.5)
- [ ] 43.2 — Implement `query` / `write` / `get_security_policy` / `list_entities` against Fabric Lab tenant
- [ ] 43.3 — Smoke: write 100 rows to Bronze `SCML.Inventory`; query Silver with operator OBO; verify OneLake security policy filters per RLS predicate

**Exit criteria:** Operator-scoped query returns only rows the operator's Entra identity is authorized to see; SQL `GRANT/REVOKE` on tables is correctly ignored (user identity mode); ledger overlay row written.

---

### Sprint 44 — Phase I.4 Production Purview Audit + Sensitivity Classifier

**Closes:** items 44.1–44.3
**Owner:** Governance SRE
**Depends on:** Sprint 42
**Goal:** Microsoft Purview Audit becomes the system of record (per ADR-003); APEX classification tiers map bidirectionally to Purview sensitivity labels.

- [ ] 44.1 — Wire Microsoft Compliance Audit Graph API for `AuditLedgerPurview.append`
- [ ] 44.2 — Wire Purview labels API for `SensitivityClassifierPurview` (production `classify_text`, `to_provider_label`, `from_provider_label`)
- [ ] 44.3 — Verify sensitivity-label propagation through Foundry RAG end-to-end (T3 entity → encrypted RAG result honoring EXTRACT)

**Exit criteria:** Foundry agent decision writes to Purview Audit; reverse propagation works (Purview-labeled SharePoint document read by Foundry RAG honors the label); classification mapping resolves per ADR-005.

---

### Sprint 45 — Phase I.5 Production Defender for AI

**Closes:** items 45.1–45.4
**Owner:** Security SRE
**Depends on:** Sprint 41 + Sprint 42
**Goal:** Pre-deployment Security Gate items #1, #2, #9 turn green for Lab tenant.

- [ ] 45.1 — Wire Azure AI Content Safety Prompt Shields SDK in `ThreatProtectionDefender.shield_prompt`
- [ ] 45.2 — Wire Defender for AI services threat protection ingestion in `evaluate_response` + `get_posture`
- [ ] 45.3 — AI Model Security scan in CI for every agent image (`scan_model` calls Microsoft Defender)
- [ ] 45.4 — Defender for Cloud CSPM AI security posture surfaced in wizard `/security-gate` page

**Exit criteria:** Synthetic prompt-injection attempt is shielded; jailbreak detection fires; DSPM for AI dashboard shows the agent in the AI BOM.

---

### Sprint 46 — Phase I.6 Wizard Live + Bicep Runner

**Closes:** items 46.1–46.4
**Owner:** Wizard team
**Depends on:** Sprints 41–45 + Sprint 30
**Goal:** Operator clicks "Deploy" in the wizard and a real `az deployment group create` runs against the target tenant.

- [ ] 46.1 — Implement `apex_wizard.bicep_runner` (subprocess wrapper around `az deployment group what-if` + `az deployment group create`)
- [ ] 46.2 — `/security-gate` page live polling per gate (Defender / Purview / Entra) — red blocks render
- [ ] 46.3 — `POST /api/deployments` executes render + what-if + apply flow end-to-end
- [ ] 46.4 — Drift detector cron runs daily against Lab tenant per Pre-deployment Security Gate item #13

**Exit criteria:** End-to-end deploy works from wizard click to Lab tenant resources alive; drift detector reports zero divergence.

---

### Sprints 47–49 — First Client Engagement + Phase J Migrations

**Sprint 47** — First client Lab tenant deploy. Onboard client subscription; Pre-deployment Security Gate; deploy RC-E2E-03; smoke cold-chain + dynamic markdown. Owner: Engagement lead + Tenant SRE. Depends on Sprint 33.
**Sprint 48** — First client W2 Pilot live. Promote use case from lab to prod; full security gate; live client data; HITL on real personas. Owner: Engagement lead. Depends on Sprint 47.
**Sprint 49** — Phase J migrations land. DEP-001 through DEP-006 (RTI MCP / SLM embeddings / DeltaFlow / Activator / Defender / Purview-as-system-of-record) move from paper to migrated code. Owner: Platform team. Parallel with Sprint 48.

See `services/rc/_build-status.yaml` for item-level breakdown.

---

## Definition of Done (applies to every Task)

A task is done when:

1. Code or artefact is merged to main with passing CI.
2. Unit tests cover all new logic; integration tests cover the seam to upstream/downstream.
3. Purview lineage, classification, and DLP policies are registered where applicable.
4. Manifest stamps (`manifest_version`, `policy_version`, `prompt_version`) are emitted by any runtime the task touches.
5. Audit row is emitted for any decision the task produces.
6. Documentation is updated — at minimum, the design reference (`APEX_Design.md`) and the roadmap (`Roadmap.md` checkbox) are accurate.
7. A code review has been completed by someone other than the author.
