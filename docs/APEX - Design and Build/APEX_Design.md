# APEX Framework Design

**Document type:** Verbose design reference
**Status:** Canonical design baseline
**Date:** 2026-04-23 (v1.2 — Stacked Architecture, Scenario Library, Wave Ribbon pattern)
**Source:** Synthesized from `docs/book/Professional-APEX-M.html` (the Wrox-style book), `docs/book/Professional-APEX-M-Sellers-Guide.html` (the sellers guide), and `docs/visualization/APEX-Stacked-Architecture-Narrated.html` (the narrated stacked-architecture cinematic)
**Audience:** Architects, Practice Leads, Delivery Leads, Platform Engineers, Governance Owners, Account Teams

---

## Table of Contents

1. [Executive Summary & Positioning](#1-executive-summary--positioning)
2. [Core Architectural Principles](#2-core-architectural-principles)
3. [The Four-Layer Manifest Model (L1–L4)](#3-the-four-layer-manifest-model-l1l4)
4. [The Five-Plane Platform Architecture](#4-the-five-plane-platform-architecture)
5. [Canonical Schema Framework](#5-canonical-schema-framework)
6. [Medallion Architecture — Bronze / Silver / Gold](#6-medallion-architecture--bronze--silver--gold)
7. [MCP Server Topology & Agent Tool Contracts](#7-mcp-server-topology--agent-tool-contracts)
8. [Agent Identity, Scope, and the Visibility Lattice](#8-agent-identity-scope-and-the-visibility-lattice)
9. [HITL Gates & Decision Governance](#9-hitl-gates--decision-governance)
10. [Orchestration Framework](#10-orchestration-framework)
11. [Decision Audit Row Architecture](#11-decision-audit-row-architecture)
12. [Microsoft Fabric as the Data Plane](#12-microsoft-fabric-as-the-data-plane)
13. [SOR Integration Playbook — Five Patterns](#13-sor-integration-playbook--five-patterns)
14. [Purview Trust Architecture](#14-purview-trust-architecture)
15. [Industry Practices (RC, HLS, ER, AXLE, TMT, TH, ICE)](#15-industry-practices)
16. [Value-Delivery Chain & Commercial Envelopes](#16-value-delivery-chain--commercial-envelopes)
17. [Human Oversight Spectrum — HITL / HOTL / HIC](#17-human-oversight-spectrum--hitl--hotl--hic)
18. [Reference Implementations & Delivery Waves](#18-reference-implementations--delivery-waves)
19. [Scenario Library & Wave Ribbon Pattern](#19-scenario-library--wave-ribbon-pattern)
20. [Stacked Architecture Visualization & Narration](#20-stacked-architecture-visualization--narration)
21. [Published Communication Artifacts](#21-published-communication-artifacts)
22. [Design-System Conventions](#22-design-system-conventions)
23. [Glossary of Terms](#23-glossary-of-terms)
24. [Appendix Catalog](#24-appendix-catalog)

---

## 1. Executive Summary & Positioning

### 1.1 What APEX Is

**APEX (Agent-based Platform for EXecution)** is Deloitte's internal delivery accelerator for agentic AI on the Microsoft technology platform. It is deliberately **not** a product that clients license or purchase; it is the engineering substrate that lets Deloitte deliver Agentic AI Delivery Services to clients in **9–12 months** instead of the **18–24 months** a ground-up build would demand.

APEX is best understood as a **manifest-driven, auditable agentic platform** that turns enterprise events into resolved, auditable decisions. Every APEX deployment answers three questions, by design, for every decision it touches:

1. **What should happen next?** — an agent reasons over canonical data and proposes an action
2. **Who must approve it, and under what rules?** — HITL gates are mapped deterministically from a manifest-declared classification
3. **What audit trail does the decision leave?** — an append-only row captures the inputs, reasoning, outputs, approvers, and rationale

APEX is **not** "a data platform with AI features bolted on." It is a **contract between data and decisions**, enforced in code and auditable end-to-end.

### 1.2 The Five Forces Driving APEX

APEX exists because five forces converged late 2024 / early 2026:

1. **Decision-Velocity Gap** — events outpace human triage; 80% of operational signals become aged work
2. **Agentic AI Inflection** — LLMs plus tool-use crossed the enterprise-viability threshold; operating models have not caught up
3. **Data Sovereignty & PII Complexity** — agent reasoning must respect regulatory boundaries; cleartext PII/PHI must never reach agents — APEX enforces this via tokenization at the Bronze/Silver boundary
4. **Regulatory Acceleration** — SOX, HIPAA, GDPR, FERC, FDA, EU AI Act create deterministic audit obligations; HITL gates plus audit rows satisfy them by construction
5. **Knowledge-Worker Capacity Shortage** — automation of high-touch decisions (approvals, dispute resolution, exception routing) is the compounding answer to retiring domain experts

### 1.3 What Makes APEX Structurally Different

Four dimensions separate APEX from generic "AI platforms":

1. **Manifest-driven, not model-driven.** Manifests (event, orchestration, agent, tenant, schema, service) are the primary governance artifacts; the specific LLM is an implementation detail pinned in a manifest field.
2. **Audit row, not log line.** Every decision writes a structured row containing inputs, reasoning trace, model version, tool version, policy version, HITL status, and downstream effect. Agents that fail to emit the row are quarantined by the runtime.
3. **HITL is first-class, not bolted on.** HITL gates are declared in the manifest and enforced by the orchestrator. APEX is *adaptive human-supervised decisioning*, not autonomous AI.
4. **Fabric + Foundry + Purview + Entra native composition.** APEX is architecturally native to Microsoft's four-plane pattern, not wrapped around it.

---

## 2. Core Architectural Principles

These principles govern every design decision downstream. Deviations require explicit exception approval.

1. **Auditability over autonomy.** Every decision is reconstructible from the audit row using Git-pinned manifest, policy, and prompt SHAs. Reconstruction must not depend on change-log reasoning.
2. **Determinism before intelligence.** Gate mapping, classification propagation, schema compatibility, and orchestration sequencing are deterministic. Intelligence lives inside the agent's bounded reasoning scope, not in the control plane.
3. **Backward compatibility is a contract.** L1 Contract changes propagate top-down through L2 Editions, L3 Practices, and L4 Tenants. Tenants upgrade on their own schedule, within policy.
4. **Classification propagates.** Sensitivity labels follow data from Silver → Gold → semantic model → agent output → Copilot response. DLP enforces at every surface.
5. **Tokenization at the boundary.** PII/PHI never cross the Bronze → Silver boundary in cleartext. Agents hold tokens only. Cleartext detokenization occurs only at user-surface time, for authorized identities.
6. **Typed contracts at every seam.** Schemas are typed. MCP tools are typed. Agent outputs are schema-validated. Manifest fields are validated by CI.
7. **No side channels.** Agents reason only over data returned by typed MCP tool calls. No direct lakehouse reads. No unmediated HTTP.
8. **Idempotency everywhere.** Silver transforms, agent tool calls, HITL resolutions, and downstream writes are idempotent. Replays produce the same state.
9. **Version everything.** Every schema, agent, tool, orchestration, policy, and prompt is SemVer-stamped and Git-pinned in the audit row.
10. **Scope is lattice, not list.** Visibility emerges from the composition of tenant × practice × persona × classification × row-level filters, not from ad-hoc allow-lists.

---

## 3. The Four-Layer Manifest Model (L1–L4)

APEX governs change and configuration through a hierarchical four-layer model. Each layer is a Git repository (or repository slice) with independent SemVer lifecycle.

```
L1  CONTRACT   apex-core         — normative specification, validators, bump rules
                ↓ (propagates to every Edition)
L2  EDITION    apex-core v1.2.0  — a versioned, pinned release of L1
                ↓ (propagates to every Practice that consumes this Edition)
L3  PRACTICE   RC / HLS / ER / AXLE / TMT / TH / ICE
                 — industry bundle: schemas, agents, MCP tools, orchestrations,
                   gates, services, personas, KPIs
                ↓ (tenants pin Practice releases)
L4  TENANT     client-xyz        — instance pinning Practice release,
                                   subscribes to services, defines extensions
```

### 3.1 Layer Definitions

| Layer | Name | Artifact | Lifecycle Owner |
|-------|------|----------|-----------------|
| **L1** | Contract | `apex-core` specification, validators, bump-classification rules, canonical-envelope definition | Central APEX platform team |
| **L2** | Edition | A specific versioned, immutable release of L1 (e.g., Core v1.2.0) | Central APEX platform team |
| **L3** | Practice | Industry bundle: canonical schemas + agent catalog + MCP servers + orchestration archetypes + HITL gate policies + services + personas + KPIs | Practice lead (e.g., RC Practice Lead) |
| **L4** | Tenant | A client instance. Pins a Practice release. Declares service subscriptions, tenant-scoped extensions, policy overrides | Client delivery lead, Account Team |

### 3.2 Change-Flow Contract

Changes always propagate **top-down**:

- An L1 Contract change rolls into a new L2 Edition.
- A new Edition can be consumed by any L3 Practice on its own schedule.
- A Practice release lands at an L4 Tenant only when that tenant explicitly pins the new release.
- Clients are **never forced to upgrade**; they upgrade on their own schedule within tenant policy.

### 3.3 SemVer Bump Classification

Every change (schema, tool, agent, orchestration) is classified:

| Bump Class | Meaning | Default Gate |
|------------|---------|--------------|
| **PATCH** | Backward-compatible bug fix | ZERO_TOUCH — apply silently, log as auto-taken |
| **MINOR** | Backward-compatible feature (additive field, new tool, new orchestration variant) | ACK_ONLY — notify and auto-apply |
| **MAJOR** | Breaking change (field removal, type narrowing, required-field addition) | HITL — present and wait for approve/reject/modify |

Tenants override defaults via policy (a high-risk HIPAA tenant may map MINOR → HITL globally; a low-risk tenant may narrow PATCH → ZERO_TOUCH across the board).

### 3.4 Tenant Extension Pattern

Tenants may extend L3 Practice reference artifacts without modifying them:

- **Schema extension:** add tenant-specific attributes as an L4 overlay, carrying SemVer and classification; the L3 schema remains authoritative.
- **Agent extension:** override tool allow-list, system prompt, or model pin at L4; the L3 agent manifest remains the parent.
- **Gate extension:** override default gate mapping for a specific service at L4; audit record captures the override decision.
- **Service extension:** subscribe or unsubscribe from L3 services at L4; tenant declares its service portfolio.

No L4 extension is permitted to silently break L3 contracts; CI validates every extension against the L3 parent.

---

## 4. The Five-Plane Platform Architecture

APEX is built on Microsoft's four-plane pattern — Data, Reasoning, Experience, Trust — plus an Identity plane that cuts through all four. The same five-plane mapping applies identically across all seven Practices.

### 4.1 Plane Definitions

| Plane | Microsoft Component | APEX Role |
|-------|---------------------|-----------|
| **Data Plane** | Microsoft Fabric | OneLake, Lakehouse, Warehouse, Real-Time Intelligence (Eventhouse, KQL), Data Factory, Direct Lake. Holds Bronze/Silver/Gold. |
| **Reasoning Plane** | Azure AI Foundry + Azure OpenAI | Agent runtime, model deployment, multi-agent orchestration, prompt versioning, tool-calling enforcement |
| **Experience Plane** | Microsoft 365 Copilot + Copilot Studio + Teams + Power BI | Knowledge-worker surfaces, Teams cards for HITL gates, Direct-Lake-grounded Power BI, front-office agentic interfaces |
| **Trust Plane** | Microsoft Purview | Classification (sensitivity labels), lineage end-to-end, DLP enforcement, compliance auditing, Unified Catalog |
| **Identity Plane** | Microsoft Entra | Managed identities for agents, scope enforcement, invoking-identity capture, fine-grained authz per decision class |

### 4.2 End-to-End Flow

```
SORs (SAP, Oracle, Salesforce, Epic, SCADA, …)
      ↓  (one of five integration patterns)
Fabric Bronze (raw, source-fidelity)
      ↓  (Silver transform: canonicalize + classify + tokenize)
Fabric Silver (canonical schemas: SCML, MERML, PatientML, …)
      ↓  (Gold view / Direct Lake / Warehouse)
Fabric Gold (agent-consumable, low-latency, pre-measured)
      ↓  (MCP tool binding, one typed tool per Gold view)
MCP Servers (domain / utility / external)
      ↓  (scope, classification, identity enforcement)
Foundry Agents (reason over data via typed tools)
      ↓  (orchestration manifests; HITL gates)
Teams card / Copilot Studio / Power App / Power BI (human surface)
      ↓
Decision Audit Row (manifest+policy+prompt SHAs, inputs, outputs, approver, outcome)
```

### 4.3 What Fabric Provides vs What APEX Adds

**Fabric ships:** OneLake, Lakehouse, Warehouse, Direct Lake, Shortcuts, Mirrored Databases, Real-Time Intelligence (Eventhouse, KQL), Data Factory, Data Activator, native Purview + Entra integration.

**APEX adds on top:**
- Industry canonical semantic models (SCML, MERML, CXML, PatientML, …)
- Agent library (40–50 pre-built, tested agents per Practice)
- Orchestration patterns (47 archetypal patterns, Practice-specific instantiations)
- MCP tool catalog (150+ tools per Practice)
- HITL gate framework (manifest-declared checkpoints with Teams/Copilot Studio integration)
- Decision audit row schema (14+ required fields)
- Manifest governance (event, orchestration, agent, tenant, schema manifests as Git-versioned contracts)
- Per-Practice productized services (45+ named services with KPIs, SLOs, commercial terms)

---

## 5. Canonical Schema Framework

### 5.1 What a Canonical Schema Is

A canonical schema is a **semantic contract** — an opinionated, typed, classification-aware, relationship-defined specification of the entities that matter in an industry. It is **not** a database schema; it is a *contract* against which database schemas, MCP tools, agent prompts, and BI measures are validated.

Every APEX canonical schema:

- Names entities (SKU, Patient, Well, Unit, Traveler, Meter, Equipment, …)
- Defines relationships (cardinality, temporal validity, identity-resolution semantics)
- Specifies classifications (PII, PHI, PCI, SOX-controlled, trade-secret, member-only, export-controlled)
- Constrains types (nullability, defaults, enumerations, allowed domains)
- References industry standards (GS1, HL7 FHIR, CIM, ISA-95, TM Forum SID, IATA NDC, SAE J1939, …)
- Governs agent behavior (which tools may read which attributes at which scopes)
- Enables cross-Practice federation (consistent surrogate keys across schemas)

### 5.2 Canonical Schema Families

| Practice | Canonical Schemas |
|----------|-------------------|
| **RC** (Retail & Consumer) | **SCML** (Supply Chain), **MERML** (Merchandising), **CXML** (Customer Experience) |
| **HLS** (Healthcare & Life Sciences) | **HLSCML** / **PatientML**, **ClaimML**, **StudyML** |
| **ER** (Energy & Resources) | **ERCML** / **UOGML** (Utility Operations), **P&UML** (Power & Utility), **MiningML** |
| **AXLE** (Automotive / Industrial Manufacturing) | **AXLECML** / **AXLEML** (ISA-95 aligned) |
| **TMT** (Tech, Media, Telecom) | **TELML** (TM Forum SID-aligned), **ContentSafetyML** |
| **TH** (Travel & Hospitality) | **IROPsML**, **ReservationML**, Traveler / Profile / Preferences |
| **ICE** (Industrial & Commercial Equipment) | **ConnectedICEML** (SAE J1939, AEMP 2.0 aligned) |

### 5.3 Canonical Envelope — Five Universal Fields

Every Silver row, regardless of schema family, carries a five-field envelope that makes cross-entity joins and temporal analysis possible:

| Field | Meaning |
|-------|---------|
| `event_id` | Unique event identifier (UUID) |
| `event_ts` | When the event occurred (source system timestamp) |
| `entity_id` | Canonical entity key (surrogate + natural compound) |
| `source_system` | Which SOR emitted this row |
| `source_system_ts` | Source system's timestamp (for audit and change detection) |

### 5.4 Three-Step Schema Design Pattern

Every APEX schema is designed by the same pattern:

1. **Consume** — entity definitions are derived from the dominant industry standard for the Practice
2. **Extend** — APEX adds governance metadata: sensitivity labels, consent pointers, agent-safe flags, audit-row bindings, model-version constraints, HITL declarations, manifest cross-references
3. **Translate** — pre-built bidirectional mappings between competing standards (HL7 v2 ↔ FHIR ↔ CDA; EDI X12 ↔ XML; GS1 ↔ Schema.org; SAE J1939 ↔ AEMP 2.0)

**Practical consequence:** a Retail client with GS1-conformant SAP item master, Schema.org-conformant Salesforce catalog, and EDI X12 inbound integrates to SCML through off-the-shelf APEX adapters, not custom engineering.

### 5.5 Entity Schema Structure

Every APEX entity specifies:

- **Name** — canonical entity name
- **Keys** — natural key (source identifier) plus surrogate key (APEX-assigned UUID)
- **Attributes** — typed columns with nullability, defaults, allowed-value enumerations
- **Pre-measure attributes** — derived columns computed during Silver → Gold transform (`effective_margin_pct`, `stock_days_remaining`, `time_since_last_event`)
- **Post-measure attributes** — computed at query time (period-over-period, rolling averages, attainment vs target, confidence scores)
- **Classifications** — Purview sensitivity tags per attribute
- **Relationships** — foreign keys to other canonical entities with cardinality and temporal validity
- **Business-term bindings** — Purview Unified Catalog glossary term implemented by each attribute

### 5.6 Schema Registration Pipeline

1. Author schema YAML in Git
2. CI lint-validates, generates Delta DDL, generates Purview registration payload
3. Fabric Deployment Pipeline promotes table definitions (dev → test → prod)
4. Purview scan registers tables and applies classifications per YAML
5. Drift detector compares actual Fabric schema against YAML; drift generates alert

### 5.7 Why Canonical Schemas Matter for Agentic AI

1. **Cross-SOR decision aggregation** — agents reason across systems without data movement (mirroring + shortcuts)
2. **Typed interfaces are mandatory for agents** — humans tolerate ambiguity; agents cannot
3. **Classification propagation** — schema carries classifications through every derivation; agent output inherits correct DLP handling automatically
4. **Audit-row attribution** — stable canonical IDs enable "this margin dollar saved by this decision" attribution; ad-hoc IDs cannot
5. **Agent evaluation at scale** — testing agent behavior across 10,000 scenarios requires schema stability
6. **Cross-Practice federation** — diversified clients with RC + HLS agents reasoning across boundaries require canonical schemas that meaningfully join

### 5.8 The Acceleration Math

- **Without canonical schema:** first use case 6–9 months; each subsequent use case 6–9 months again
- **With canonical schema (APEX model):** first use case 6–9 months (or weeks if consuming a shipped schema); second 2–3 months; third in weeks; fifth-and-beyond under a month

This compounds to **10–50× acceleration by Wave 3** because canonical schema exists from Wave 1 Day 1.

---

## 6. Medallion Architecture — Bronze / Silver / Gold

APEX's medallion is a **contract**, not a folder structure. Every table carries layer, classification, retention, and SLO declarations in its manifest.

### 6.1 Layer Contract Summary

| Layer | Purpose | Format | Retention (default) | Classification | SLO |
|-------|---------|--------|---------------------|-----------------|-----|
| **Bronze** | Source-fidelity raw landing | Delta or Parquet, append-only with source timestamps | 7 years default; longer with legal hold | Source-inherited; classified before acceptance | Landing within 60 s (streamed); schedule-bounded (batch) |
| **Silver** | Canonical, cleaned, typed, deduplicated, enriched, tokenized | Delta with SCD Type 2 where history matters; tokenized for PII/PHI | Per-Practice regulatory minimum (7 y HLS, 5 y SOX) | Most-restrictive classification across sources + tokenization guarantees | Ready within 5–15 min streaming; configurable batch |
| **Gold** | Agent-consumable views, pre-measure computations, materialized for low latency | Delta (Warehouse or Lakehouse) + KQL functions (real-time) | Inherits Silver | Classification + Gold-specific DLP policies | Matched to agent SLO (sub-second real-time, hourly batch) |

### 6.2 Bronze — Five Landing Patterns

APEX supports five ingestion patterns. Choice is governed by how the source SOR emits data (not by preference).

#### 6.2.1 Mirrored Database Landing

- **Sources:** Azure SQL DB, Cosmos DB, Snowflake, PostgreSQL, MongoDB, Oracle, BigQuery, Databricks
- **Implementation:** Fabric Mirroring item with CDC-based continuous replication; credentials in Key Vault; managed-identity access
- **Latency:** 60–180 s typical
- **Schema evolution:** additive propagates automatically; drops require Mirror reconfiguration and staged Silver transform change
- **Error semantics:** Mirror failures emit Purview error events; auto-resume on recovery; consumers see `mirror_lag_seconds`
- **APEX uses:** any SOR needing sub-minute freshness (Oracle Retail pricing, Epic Clarity encounters where supported)

#### 6.2.2 Eventstream / Eventhouse Landing

- **Sources:** Event Hubs, Kafka, MQTT (via Azure IoT Operations), Service Bus, custom HTTP/webhook
- **Implementation:** Eventstream receives; processor normalizes + dedupes + tokenizes in flight; routes to Eventhouse KQL table
- **Schema evolution:** Eventhouse tolerates drift via `.ingest inline`; structural changes update table policy
- **Error semantics:** parse failures → `bronze_raw_deadletter` with payload, error, retry count; sustained dead-lettering pages platform ops
- **APEX uses:** IoT telemetry (cold-chain sensors, industrial historians), POS streams, EHR ADT events, network alarms, clickstream

#### 6.2.3 Data Pipeline (Scheduled Batch) Landing

- **Implementation:** Fabric Data Pipeline activities (Copy, Notebook, Stored Procedure); cron or event triggers
- **Schema evolution:** Copy activity tolerates additive; breaking halts pipeline
- **Error semantics:** activity-level success/failure monitoring; retries with exponential backoff; final failure routes to ops
- **APEX uses:** supplier master refresh, overnight inventory snapshots, regulatory extracts, EDI drops (post-format-conversion)

#### 6.2.4 Dataflow Gen2 (REST / SaaS) Landing

- **Implementation:** Power Query (M) connectors for 100+ SaaS sources (Salesforce, Workday, ServiceNow, Jira, HubSpot); incremental via watermark
- **Schema evolution:** tolerates additive drift with column-order safety
- **Error semantics:** connector errors (rate limit, auth, timeout) surface in history; retry with backoff; final failure routes to ops
- **APEX uses:** Salesforce CRM, Workday HCM, ServiceNow change-feed, marketing-platform campaign data

#### 6.2.5 Custom Endpoint (Webhook) Landing

- **Implementation:** Azure Function / Container App with HTTP trigger; Entra managed-identity auth; writes to OneLake via the OneLake SDK; optional parallel Eventhouse write
- **Schema evolution:** endpoint code enforces payload schema; additive passes; breaking returns 400-class and alerts
- **Error semantics:** App Insights logs; failed ingests dead-letter to Service Bus for manual reprocessing
- **APEX uses:** legacy industrial equipment (webhook-only), niche medical devices, third-party notification services

### 6.3 Bronze Discipline

- **Partitioning:** by source-event date (`ingest_date`) by default; override where recall-style trace requires (e.g., `lot_id`)
- **Retention:** 7 years default; 10+ for HLS; permanent with legal hold for recalls; Purview-managed policies enforce
- **Schema-on-read:** Bronze tables keep canonical columns plus a JSON `_raw_payload` preserving exact source payload; Silver reads canonical, escape-hatch debugging reads raw
- **Time-travel:** Delta time-travel preserves reproducibility for audit (`TIMESTAMP AS OF`)

### 6.4 Silver — Canonical Layer

Silver is where Bronze raw becomes canonical. Each APEX Practice ships per-domain semantic models (SCML, MERML, CXML, PatientML, AXLEML, …) as Silver-layer artifacts. Every Silver table:

- Uses stable canonical surrogate keys plus preserved natural keys
- Enforces types, defaults, and enumerations at write time
- Carries SCD Type 2 history where business change-tracking matters (Customer, Employee, Product)
- Is **tokenized at the ingest boundary** for PII/PHI, Purview-classified, DLP-enforced
- Maintains foreign-key relationships via consistent canonical keys
- Registers its attributes to Purview Unified Catalog business-glossary terms

#### 6.4.1 Tokenization at the Bronze / Silver Boundary

The design guarantee: **an agent that holds a row holds only tokens**. Even under prompt-injection, cleartext is not reachable.

1. Bronze lands raw source with cleartext PII per source convention
2. Silver-transform PySpark reads Bronze, identifies classified columns per Purview, tokenizes via a deterministic reversible token function
3. Silver stores tokens in canonical columns; cleartext is held in a vault Delta table (`silver_vault_tokens`) with row-level PIM-gated access
4. Gold queries see tokens; agent outputs carry tokens; Copilot grounds on tokens
5. Detokenization occurs only at user-surface rendering, and only for authorized identities

#### 6.4.2 Silver DDL Excerpt (SCML SKU, representative)

```sql
CREATE TABLE silver_scml.sku (
  sku_key              STRING NOT NULL,    -- surrogate UUID
  sku_natural          STRING NOT NULL,    -- source natural key
  sku_status           STRING NOT NULL,    -- ACTIVE / INACTIVE / DISCONTINUED
  category_key         STRING NOT NULL,
  supplier_key         STRING,
  upc                  STRING,
  description          STRING,
  unit_cost_token      STRING,             -- tokenized supplier-confidential
  unit_retail          DECIMAL(10,2),
  case_pack            INT,
  weight_kg            DECIMAL(8,3),
  lifecycle_start_dt   DATE,
  lifecycle_end_dt     DATE,
  scd2_valid_from      TIMESTAMP NOT NULL,
  scd2_valid_to        TIMESTAMP,
  scd2_is_current      BOOLEAN NOT NULL,
  purview_label        STRING NOT NULL,    -- classification propagated
  row_hash             STRING NOT NULL     -- change detection
)
USING DELTA
PARTITIONED BY (sku_status)
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'delta.logRetentionDuration' = '30 days'
);
```

### 6.5 Gold — Materialization & Serving

Gold has three materialization strategies:

- **Direct Lake semantic model** — Power BI directly over Silver Delta; sub-second refresh; no copy
- **Warehouse SQL views** — T-SQL views over Warehouse tables sourced from Silver; fast but compute-bound
- **Materialized Delta tables** — pre-computed Gold tables in Lakehouse; fastest but require refresh orchestration

Gold refresh patterns:

- **Real-time:** Silver change → Delta trigger → Gold KQL function update (sub-second)
- **Batch hourly:** Data Factory pipeline reads Silver, materializes Gold view, refreshes Power BI semantic model
- **Event-triggered:** Data Activator rule fires on Silver change → triggers Gold refresh

### 6.6 Measures — Pre-Measure and Post-Measure

- **Pre-measure (input-side, Silver → Gold):** embodied as Gold table columns (effective margin, stock-days remaining, weather-adjusted demand signal). Authored in PySpark; Git-versioned.
- **Post-measure (output-side, query-time):** computed in Power BI (DAX), Warehouse (SQL), or Eventhouse (KQL). Period-over-period, rolling averages, attainment vs target, actionability score, confidence intervals.

**Authoring language choice:**

- **DAX** for Power BI / Direct Lake consumption
- **T-SQL** for Warehouse-served measures consumed by agents via MCP
- **KQL** for real-time measures over Eventhouse event streams
- **PySpark** for complex pre-measures (joins, windows, ML-derived attributes)

Every measure has owner, definition, consumer map, change-control history. Deprecation flows `deprecated_v1.2` → consumer warning for 2 quarters → retirement.

---

## 7. MCP Server Topology & Agent Tool Contracts

### 7.1 Model Context Protocol — The Contract Seam

MCP (Model Context Protocol) is the open-standard, typed contract between agents and the outside world. Every APEX tool carries typed I/O, standardized error codes, rate limits, and trace instrumentation. Agents may reason only over what MCP tools return. There are no side channels.

### 7.2 Three MCP Server Classes

**1. Domain servers — one per canonical schema family:**

| Server | Responsibility |
|--------|----------------|
| `scml-mcp` | Supply-chain canonical reads |
| `merml-mcp` | Merchandising reads (prices, inventory, markdowns) |
| `cxml-mcp` | Customer-experience reads (orders, loyalty, incidents) |
| `hlscml-mcp` | Healthcare reads (encounters, observations, claims) |
| `ercml-mcp` | Energy / resources reads |
| `axlecml-mcp` | Manufacturing reads |

**Design principle:** segregate identity so PHI-read grants stay within `hlscml-mcp` and never leak into cross-Practice scopes.

**2. Utility servers — cross-cutting platform services:**

| Server | Responsibility |
|--------|----------------|
| `fabric-mcp` | OneLake / workspace data access |
| `policy-mcp` | Rule evaluation, compliance checks |
| `telemetry-mcp` | Trace, logging, observability |
| `approvals-mcp` | Approval workflows, HITL integration |
| `tokenizer-mcp` | PII/PHI detokenization under scoped access |
| `ledger-mcp` | Decision-audit-row persistence |

**3. External servers — wrapped third-party sources:**

| Server | Responsibility |
|--------|----------------|
| `fda-mcp` | FDA recall / adverse-event feeds |
| `ferc-mcp` | FERC grid / compliance data |
| `edi-mcp` | EDI message processing |
| `vendor-portal-mcp` | Vendor portal API aggregation |
| `pharma-recall-mcp` | Pharmaceutical recall aggregators |

### 7.3 Tool Contract Structure

Every MCP tool declares:

- **inputSchema** — typed parameter definitions with domains, ranges, required fields
- **outputSchema** — bound to a named Gold view or Silver projection
- **SLO** — latency target, freshness target, availability target
- **Classification inheritance** — labels on backing Gold data propagate into tool output
- **Identity scope** — which agent scopes are authorized
- **Version** — SemVer; behavior change = new version; immutable by version

Each tool call emits a trace record containing: `operation_id`, `agent_id`, `tool_name`, `tool_version`, `parameters_hash`, `result_hash`, `latency_ms`, `classification_applied`, `caller_identity`.

### 7.4 Tool-to-Gold-View Binding

- Each tool's `inputSchema` maps to canonical entity keys.
- Tool output is bound to a specific named Gold view structure.
- Parameter validation (value domain, type, range) is enforced at the tool boundary **before** the Gold query executes.

### 7.5 Retrieval Patterns

- **Full-entity retrieval** — get entity by key (simple agents)
- **Vector-embedding retrieval** — semantic search over Azure AI Search indices grounded on OneLake
- **Hybrid** — structured key + embedding (complex agents)
- **Pre-aggregated rollups** — agent-facing rollup tables pre-compute common aggregates for sub-second response

---

## 8. Agent Identity, Scope, and the Visibility Lattice

### 8.1 Agents Authenticate Nothing Directly

Agents do not hold source credentials. MCP servers authenticate under their own managed identity on the agent's behalf. The sequence:

1. Agent invokes an MCP tool
2. MCP server evaluates the caller's (agent's) Entra identity and scope
3. MCP server validates permissions against the visibility lattice
4. MCP server executes the read/write and returns classified output

### 8.2 Scope Dimensions

An agent's scope is the composition of:

- **Tenant** — which L4 client
- **Practice** — which L3 domain
- **Persona** — which human role this agent serves
- **Classification visibility** — which sensitivity labels the agent may see (lattice-evaluated per tool call)
- **Row-level filters** — tenant-specific attribute predicates (region, store, service-line)

### 8.3 Visibility Lattice

Classification-driven row-level security (RLS), object-level security (OLS), and per-agent scope combine into a lattice evaluated at tool-call time. Scopes are cached for minutes, not hours. An agent accessing an entity sees only the attributes the lattice permits.

### 8.4 Agent-Safe Views

Every agent reads Gold through an **agent-safe view** — a derivative view with classification-appropriate masking, scoped to the agent's tenant / practice / persona. Agents never see cleartext PII/PHI unless the lattice and classification permit. Responses are signed by the agent's service principal for audit traceability.

---

## 9. HITL Gates & Decision Governance

### 9.1 Four Gate Kinds

| Gate | Behavior | Default Mapping | Tuning |
|------|----------|-----------------|--------|
| **ZERO_TOUCH** | Apply silently; log as auto-taken | PATCH | Tenant may narrow to MAJOR |
| **ACK_ONLY** | Apply + notify; acknowledgement optional | MINOR | Tenant may override per service |
| **HITL** | Present + wait for approve / reject / modify | MAJOR | Tenant may narrow to ACK_ONLY for low-risk |
| **ESCALATION** | Route to cross-functional owner | Context-dependent | Tenant defines escalation path & owner |

### 9.2 Gate-Type Variants (Orchestration-Scoped)

Within HITL, orchestrations may declare:

- **Hard gate** — pauses, requires explicit approval to proceed
- **Soft gate** — continues after acknowledgement; may be deferred
- **Policy gate** — auto-approved against codified policy; reviewable post-hoc
- **Escalation gate** — approver may escalate to a higher authority

### 9.3 Gate Resolution Contract

1. Agent proposes an action
2. The SemVer bump classification is determined via the `classify-bump` tool
3. Gate Kind is mapped deterministically from bump class
4. Gate is applied per tenant policy
5. If HITL: the human is presented with proposal, inputs, outputs, confidence score → approve / reject / modify
6. The decision is captured in an append-only Decision Audit Row

### 9.4 Tenant Policy Tuning Process

1. New tenants onboard with conservative defaults
2. Tenant requests gate tuning for specific services
3. Tuning enters Decision Audit Review — 2-week observation window
4. If no reversals or escalations surface, tuning is approved; otherwise rolled back
5. All gate-tuning changes are themselves audited

### 9.5 Regulator Alignment

The EU AI Act explicitly defines "appropriate human oversight" to include HITL, HOTL, and HIC modes. APEX's four-gate model plus the three-mode oversight spectrum (§17) is designed for direct mappability to EU AI Act Article 14 and equivalent obligations.

---

## 10. Orchestration Framework

### 10.1 What Orchestration Is — and Isn't

APEX orchestration is distinct from:

- **Data orchestration** (Fabric Data Factory pipelines, Data Activator rules) — moves data between layers
- **BPM / workflow engines** (UiPath, Camunda) — automate deterministic processes
- **Single-agent prompt chains** — prompt engineering, not orchestration

**Defining property:** multi-agent composition with explicit manifest governance. Every step is a distinct agent with its own identity, tools, classification scope, and audit emission.

### 10.2 Four Primitive Orchestration Patterns

1. **Sequential** — A → B → C strict dependency order (e.g., detect → classify → disposition → notify)
2. **Parallel** — dispatch fans to independent agents; outputs merge downstream
3. **Hierarchical** — an orchestrator plans, dispatches to specialists, receives outputs back (the plan itself requires reasoning)
4. **Feedback loop** — an evaluator accepts or refines an agent's output against quality thresholds

Real orchestrations compose these. A recall orchestration is typically parallel-inside-sequential-inside-hierarchical.

### 10.3 47 Orchestration Archetypes

APEX ships a reusable library of **47 orchestration archetypes**. These are not 47 implementations; they are 47 **patterns** from which Practice-specific orchestrations are composed.

**Examples:**

- "Anomaly detection + disposition + HITL approval + action"
- "Multi-source identity resolution with confidence-weighted merge"
- "Pattern-match on event cluster → regulatory-scope compute → multi-stakeholder notification"
- "Predictive trigger + workflow-aware scheduling + resource confirmation"
- "Classification-change propagation across dependent services"
- "Cross-Practice entity federation with trust-boundary enforcement"

**Why 47:** seven Practices × ~seven decision-shape categories per Practice ≈ 47 archetypes covering the vast majority of real operational decisions. Edge-case decisions get one-off treatment.

**Acceleration kernel:** Practice-specific orchestration ships in weeks-to-months because it specializes an existing archetype rather than being invented from scratch.

### 10.4 Orchestration Manifest

Every orchestration is manifest-declared — a Git-versioned artifact defining:

- Agent sequence / parallelism / hierarchy
- Tool bindings per agent
- Classification scopes per step
- HITL gate placement and type (hard / soft / policy / escalation)
- Audit emission requirements
- Failure handling and retry logic
- Version stamps (`manifest_version`, `policy_version`, `prompt_version`)

Without a manifest, a multi-agent workflow cannot be audited, versioned, or safely evolved — and is therefore rejected by the APEX runtime.

### 10.5 HITL Gates as Orchestration Checkpoints

HITL gates are first-class checkpoints. Gate placement balances risk, latency, and autonomy scaling. Parallel orchestrations may fire multiple gates concurrently. Hierarchical orchestrations have gates at both the orchestrator level (strategic) and the specialist level (execution).

---

## 11. Decision Audit Row Architecture

### 11.1 What an Audit Row Is

**Not** a log line. A **structured, tamper-evident, signed record of a decision** — the unit of work an agent performs. Operational test: it is the minimum artifact a regulator, auditor, or forensic reviewer needs to reconstruct and evaluate the decision.

### 11.2 Fourteen Required Fields

| Field | Content |
|-------|---------|
| `trace_id` | UUID binding every orchestration step into one forensic thread |
| `decision_id` | UUID of this specific agent decision |
| `agent_id` | Entra Agent ID of the emitting agent |
| `invoking_identity` | Entra principal (user or upstream agent) that invoked this agent |
| `manifest_version` | Git SHA of the orchestration manifest in effect |
| `policy_version` | Git SHA of the Purview / DLP / HITL policy bundle in effect |
| `model_version` | Specific Foundry-deployed model (e.g., `gpt-4.1-2025-xx-xx`), including fine-tune ref |
| `prompt_version` | Git SHA of the system-prompt / few-shot bundle |
| `inputs_ref` | Content-hash reference to the input payload (actual data in a Gold snapshot) |
| `tools_called` | Ordered list of `(mcp_tool_id, tool_version, parameters_hash, result_hash)` tuples |
| `reasoning_trace_ref` | Reference to the captured reasoning trace (redacted per DLP) |
| `decision_output` | Structured output the agent produced |
| `hitl_status` | `{none, pending, approved, modified, rejected, overridden}` with approver identity + timestamp |
| `downstream_effect_ref` | Reference to the action-tool call or write-back that resulted (null if advisory) |

Optional fields frequently carried: `cost_attribution` (PTU / token cost), `sensitivity_label_propagation`, `confidence_score`.

### 11.3 Emission Path

1. **Pre-invocation** — Foundry resolves manifest, policy, prompt, and model versions; stamps on row-in-progress
2. **Tool calls** — each MCP invocation produces `(tool_id, version, params_hash, result_hash)`; actual params/results are content-addressed to an immutable store
3. **Reasoning capture** — the model's reasoning trace is captured, DLP-scanned against propagated sensitivity labels, and stored by reference; sensitive tokens never land inline
4. **Decision output** — validated against the manifest's output schema
5. **HITL gate** — if a gate fires, row marked `hitl_status=pending`; paused until Teams card / Copilot Studio action / dashboard returns
6. **Downstream effect** — if the decision drives an action, the action's audit row is cross-referenced via `downstream_effect_ref` and `trace_id`
7. **Seal** — row is signed, hashed, and written to the immutable audit store

### 11.4 Reasoning-Trace Capture

**Not** raw chain-of-thought (may contain PHI, PCI, trade secrets, hallucinations). APEX captures:

- Tool-call sequence — verifiable, high-value for forensic review
- Decision justification — constrained, post-reasoning summary in structured form
- Cited-evidence pointers — which Gold-view records / documents referenced, by content hash
- Model confidence / uncertainty signal where produced

Raw internal reasoning is captured separately into a restricted store with stricter access controls (incident investigation only).

### 11.5 Orchestration Composite Row

The orchestration emits a parent row referencing every participating agent's row via shared `trace_id`:

- `orchestration_id`
- `archetype_id`
- `trigger` (event, user action, schedule)
- `participating_agents` — ordered list of `decision_id`s with `trace_id` join
- `orchestration_outcome`
- `latency_breakdown` — per-step wall clock
- `hitl_gates_fired` — ordered list of HITL events
- `policy_exceptions` — any policy deferrals or escalations

Auditors walk: orchestration row → participating agent rows → MCP tool calls → Purview-registered Gold view versions.

### 11.6 Trace-ID Discipline

All agents in an orchestration inherit the same `trace_id`. The forensic thread carries across:

- Synchronous calls (parallel, sequential, hierarchical)
- Asynchronous handoffs (queued work)
- HITL gate pauses and resumes
- Retries and alternate paths
- Action-tool invocations

**Any audit row missing `trace_id` is a bug; the Foundry runtime rejects its emission.**

### 11.7 Three-Version Rule

Every audit row pins three Git SHAs:

- `manifest_version` (orchestration contract)
- `policy_version` (Purview / DLP / HITL rules)
- `prompt_version` (system prompt + few-shot)

A regulator asking "what rules governed this decision on April 15, 2026?" gets a precise answer: resolve the three SHAs, check out each, read exact bytes. No reconstruction from change logs.

---

## 12. Microsoft Fabric as the Data Plane

### 12.1 Fabric as SaaS, not PaaS

Fabric's SaaS delivery model drives several APEX design consequences:

- **Workspace provisioning is API-driven.** Terraform `azurerm` creates Fabric capacity (the F-SKU Azure resource); workspaces are created via `POST https://api.fabric.microsoft.com/v1/workspaces` or the `Az.Fabric` PowerShell module.
- **Compute is capacity-shared.** One F64 is a pool of 64 Capacity Units. Eventhouse, Warehouse, Power BI, and Data Factory compete for the same CU pool unless workspace-to-capacity bindings isolate them.
- **Storage is tenant-wide under OneLake.** Every Fabric item writes to OneLake; there is no per-workspace storage account to manage.

### 12.2 F-SKU Capacity Sizing

| F-SKU | CUs | Monthly list (USD) | Typical APEX use |
|-------|-----|---------------------|-------------------|
| F2 | 2 | ~$263 | Dev sandbox (too small for real work) |
| F4 | 4 | ~$525 | Dev + small Practice reference |
| F8 | 8 | ~$1,050 | Wave 1 pilot, single-tenant, one Practice |
| F16 | 16 | ~$2,100 | Wave 1/2 small multi-tenant, 25–100 units |
| F32 | 32 | ~$4,200 | Wave 2 mid-scale, 100–500 units or two Practice pilot |
| F64 | 64 | ~$8,400 | Wave 2 full-scale, 500+ units or multi-Practice |
| F128 | 128 | ~$16,800 | Wave 3 enterprise, multi-Practice |
| F256 | 256 | ~$33,600 | Large enterprise, multi-Practice, real-time intensive |
| F512 | 512 | ~$67,200 | Very large enterprise, multi-tenant consolidation |
| F1024 | 1024 | ~$134,400 | Top-tier enterprise |
| F2048 | 2048 | ~$268,800 | Hyperscale retail / telecom / media |

### 12.3 Capacity Patterns

1. **Single capacity per tenant** — all workspaces share one capacity. Simple; noisy-neighbor risk.
2. **Split dev/prod capacities** — dev/test and prod separated. Protects prod performance; doubles cost.
3. **Per-workload isolation** — Eventhouse-heavy on one capacity; batch on another; BI on a third. Maximum isolation at F128+ scale.

### 12.4 OneLake

OneLake is Fabric's unified storage substrate, on ADLS Gen2 physically, presented as a tenant-scoped hierarchical filesystem:

```
OneLake (tenant root)
├── Workspace 1/
│   ├── Lakehouse A/
│   │   ├── Tables/   (managed Delta tables)
│   │   └── Files/    (unstructured, semistructured, raw)
│   ├── Warehouse B/  (T-SQL managed tables, Delta on disk)
│   └── Eventhouse C/ (KQL databases, event-time indexed)
├── Workspace 2/
└── …
```

Key properties:

- **Single copy across workloads.** A Delta table written by Spark is queryable by T-SQL, Power BI Direct Lake, and other notebooks — all reading the same Parquet files. No ETL between Fabric workloads.
- **Delta Lake as default format.** ACID, time-travel, schema evolution. All APEX Silver/Gold are Delta.
- **Iceberg interop.** Native Iceberg support for interop with Snowflake, Databricks. APEX uses Iceberg at Bronze where the source writes Iceberg natively.
- **Shortcut-native.** OneLake shortcuts are pointers, not copies. They reach ADLS Gen2, S3, GCS, Dataverse, and other OneLake workspaces.
- **Path-level ACLs via Entra.** Every OneLake path carries fine-grained ACLs enforced against Entra identities.

### 12.5 Workload Engines

| Engine | Compute | Language | APEX Usage |
|--------|---------|----------|------------|
| **Lakehouse** | Apache Spark | PySpark, Scala, Spark SQL | Bronze landing, Silver transforms |
| **Warehouse** | MPP T-SQL | T-SQL | Gold materialization, BI serving |
| **SQL Analytics Endpoint** | Read-only T-SQL over Lakehouse Delta | T-SQL (read-only) | Quick SQL access to Silver |
| **Eventhouse** | Kusto | KQL | Real-time Bronze landing, time-series agent queries |
| **Data Factory** | Serverless pipelines | JSON pipeline DSL | Orchestrating Bronze landing, Silver refresh |
| **Dataflow Gen2** | Managed M (Power Query) | M | Low-code SaaS-API ingest |
| **Eventstream** | Stream processor | No-code / SQL | Real-time event routing |
| **Data Activator** | Event-rule engine | Reflex rules | Trigger agents from data conditions |

### 12.6 The Query-Path Triangle

- **Import** — data loaded into Power BI semantic model; fully materialized; fastest query; most storage
- **DirectQuery** — Power BI queries Warehouse/SQL endpoint live; no import; slower; no storage overhead
- **Direct Lake** — Power BI queries OneLake Delta directly; sub-second refresh; Import-speed query; no data copy. **APEX-preferred for agents.**

### 12.7 Cross-Cloud Federation via Shortcuts

- **OneLake Shortcuts** — pointers to ADLS Gen2, S3, GCS, Dataverse, other OneLake. Used for cross-workspace sharing, intercloud federation, and avoiding duplication.
- **Mirroring** — CDC mirror of source database (Azure SQL, Cosmos, Snowflake, PostgreSQL, MongoDB) into Bronze Delta. Latency 60–180 s.

---

## 13. SOR Integration Playbook — Five Patterns

### 13.1 Decision Matrix

| Decision Factor | Integration Pattern |
|-----------------|---------------------|
| Source has CDC | Mirrored Database |
| High-volume real-time events | Eventstream → Eventhouse |
| Scheduled API pull (SaaS) | Dataflow Gen2 |
| Batch files (daily / weekly) | Data Pipeline + Copy Activity |
| Custom webhook | Custom Endpoint (Azure Function) |
| On-premises database | Self-Hosted Gateway + Mirrored Database or Data Pipeline |
| Sensitive identity (e.g., Epic patient data) | Dataflow with tokenization at source boundary |

### 13.2 REST API Integration Patterns

**Authentication:** API Key (in Key Vault), OAuth2 service-principal flow, managed identity, Basic (discouraged).
**Pagination:** offset, cursor, Link-header.
**Rate limits:** exponential backoff; respect `Retry-After`.
**Incremental pull:** last-success timestamp in metadata table; filter `?updated_since=…`.
**Webhooks:** HTTP trigger function with HMAC-SHA256 signature verification; idempotent processing via dedupe key; async write with durable retry queue.
**Errors:** transient (429, 5xx) → exponential backoff up to 5 retries; permanent (401, 403, 404) → alert + dead-letter.

### 13.3 Database Integration Patterns

- **Mirrored Database** — CDC-based for Azure SQL, Cosmos, Snowflake, PostgreSQL, MongoDB
- **ODBC / JDBC** — Data Pipeline via Self-Hosted Gateway
- **Fabric Synapse connector** — for migrations from legacy Synapse
- **Snowflake connector** — for Snowflake interop

### 13.4 Event-Bus Integration

- **Event Hubs → Eventstream → Eventhouse**
- **Kafka → Event Hubs bridge → Eventstream**
- **Service Bus Queue → Custom Endpoint**

### 13.5 File-Based Integration

- **Blob landing zone** — SOR drops to Blob; Data Pipeline monitors + Copy Activity reads
- **SFTP landing zone** — third-party drops to SFTP; Self-Hosted Gateway proxies read
- **SharePoint document library** — Power Automate triggers pipeline or custom Function

### 13.6 Worked SOR Examples

1. **Epic Clarity** — Mirrored Database where CDC available, else Dataflow Gen2 with FHIR `_lastUpdated`; tokenize MRN at Bronze→Silver
2. **SAP S/4HANA** — ODP / CDS via Mirrored Database or Custom Endpoint webhook; on-prem via Self-Hosted Gateway
3. **Salesforce** — Dataflow Gen2 for standard objects; Eventstream for platform events
4. **Manhattan Active WMS** — Data Pipeline scheduled pull, or Eventstream for webhook events
5. **Workday HCM** — Dataflow Gen2 scheduled nightly, OAuth2 service principal
6. **ServiceNow** — Dataflow Gen2 hourly, or Data Pipeline REST to `/api/now/table/{table}`
7. **OSIsoft / AVEVA PI Historian** — Custom Endpoint via PI SDK / MQTT, or Eventstream from PI Message Bus
8. **GE Proficy / AVEVA Wonderware** — Custom Endpoint for historian queries; Eventstream if the system emits events
9. **Legacy AS/400 / DB2** — Self-Hosted Gateway + Mirrored Database; or Data Pipeline via ODBC
10. **Adobe / Google Analytics** — Data Pipeline scheduled REST pulls; Dataflow Gen2 connectors where available
11. **Salesforce Marketing Cloud** — Dataflow Gen2; Custom Endpoint for journey event hooks
12. **HL7 v2 / FHIR feeds** — Custom Endpoint (e.g., Mirth) for v2 reception; Eventstream for FHIR Bundle events
13. **SAP Ariba / Coupa** — Dataflow Gen2 daily with OAuth2
14. **Oracle EBS / Fusion** — Self-Hosted Gateway + Mirrored Database, or Data Pipeline via ODBC/JDBC
15. **Snowflake / Databricks interop** — Snowflake via Mirrored Database; Databricks via Unity Catalog shortcut + Mirrored Database / Delta Sharing

---

## 14. Purview Trust Architecture

### 14.1 Purview is Mandatory

APEX's compliance posture depends on Purview. It is not optional. Purview provides:

- **Classification** — sensitivity labels on Fabric assets
- **Lineage** — end-to-end SOR → Bronze → Silver → Gold → tool → agent → audit row
- **DLP enforcement** — Copilot + agent output scanning against classifications
- **Audit-ready evidence** — tamper-proof retention (WORM policy)
- **Unified Catalog** — business glossary, data products, access requests

### 14.2 End-to-End Lineage Capture

Purview captures edges at every hop:

1. **SOR → Bronze** — source registered upstream; Bronze registered with pipeline run ID and timestamp
2. **Bronze → Silver** — Silver canonical table registered; edge carries notebook / Dataflow URL + commit SHA
3. **Silver → Gold** — Gold view registered; defining SQL SHA-stamped; edges point to Silver tables
4. **Gold → MCP tool** — tool registered as Purview asset; binding recorded with typed schema
5. **MCP tool → Agent** — agent registered; edges to every authorized tool
6. **Agent → Orchestration** — orchestration registered; references participating agents
7. **Orchestration → Audit row** — decision references orchestration via `trace_id`

### 14.3 Classification Propagation

Labels propagate automatically from Silver downstream: Silver → Gold → Power BI semantic model → Copilot response → agent output. DLP policies enforce label-based redaction at every surface. Agent outputs inherit the most-restrictive label across the data they consumed.

---

## 15. Industry Practices

APEX ships seven Practices. Each contains five reusable asset classes: canonical schemas, agent catalog, orchestration catalog, service catalog, delivery playbook.

| Practice | Industries | Canonical Schemas | Key SORs | Signature Services |
|----------|-----------|-------------------|----------|---------------------|
| **RC** — Retail & Consumer | Grocery, mass, apparel, specialty, pharmacy, CPG, QSR, e-commerce, luxury | SCML, MERML, CXML | SAP, Salesforce, Oracle Retail, WMS, POS | Assortment & Pricing, Unified Customer, Product Tracking, Demand Sensing, Markdown, Shrink |
| **HLS** — Healthcare & Life Sciences | Hospitals, health systems, pharma, medtech, diagnostics, biotech | PatientML, ClaimML, StudyML | Epic, Cerner, claims systems, trial systems | Clinical Decision Support, Sepsis Prediction, Utilization Management, Drug Discovery |
| **ER** — Energy & Resources | Utilities, O&G, mining, renewables | UOGML, P&UML, MiningML | SCADA, AMI, OMS, historians | Outage Triage, Asset Maintenance, Demand Forecasting, Grid Optimization |
| **AXLE** — Automotive / Manufacturing | Auto, heavy equipment, process, contract mfg | AXLEML (ISA-95) | MES, PLM, ERP, OPC UA, historian | Connected Factory, Predictive Maintenance, Quality Optimization, Supply Chain Resilience |
| **TMT** — Tech, Media, Telecom | Telecom, M&E, software, SaaS | TELML, ContentSafetyML | CRM, CMS, network OSS, billing | Contact Center Intelligence, Content Recommendation, Network Optimization, Churn Prevention |
| **TH** — Travel & Hospitality | Airlines, hospitality, cruise, rental car | IROPsML, ReservationML | PSS, CRS, loyalty, ops | Revenue Optimization, Crew Scheduling, Disruption Recovery, Personalized Offers |
| **ICE** — Industrial & Commercial Equipment | Commercial vehicles, agriculture, construction, mining equipment | ConnectedICEML | Telematics (SAE J1939), OPC UA, historian | Fleet Optimization, Predictive Service, Dealer Insights, Customer Engagement |

Each Practice aligns its canonical schemas to industry standards:

| Practice | Primary Standards |
|----------|-------------------|
| RC | GS1 (GTIN, SSCC, GLN), ARTS ODM, EPCIS, GDSN, EDI X12, IFPS, ISO 8000, Schema.org |
| HLS | HL7 FHIR R4/R5, HL7 v2.x, CDA/C-CDA, SNOMED CT, LOINC, ICD-10/11, CPT, HCPCS, RxNorm, NDC, HIPAA X12, NCPDP, CDISC, DICOM, IHE, USCDI, IDMP |
| ER | CIM (IEC 61970/61968/62325), ISO 15926, WITSML/PRODML, IEC 61850, OPC UA, ISA-95, NERC CIP, EPRI |
| AXLE | ISA-95, ISA-88, AutomationML, OPC UA, STEP (AP242/203/214), PLCS, OAGIS, VDA, Odette, X12, MIMOSA CRIS, ISO 14224, IATF 16949, SAE J1939, ISO 11783 ISOBUS |
| TMT | TM Forum SID / ODA / Open APIs, 3GPP, MEF 55/LSO, DVB, EIDR, SMPTE, IAB/AdCOM, ETSI |
| TH | IATA NDC, IATA PADIS, OpenTravel (OTA), HTNG, ONE Record, TSA/APIS/PNR, PCI DSS, IATA PSS, GSF |
| ICE | SAE J1939/J1708, ISO 11783 ISOBUS, OPC UA, AEMP 2.0 / ISO 15143-3, ISO 14224, ESG/CDP |

---

## 16. Value-Delivery Chain & Commercial Envelopes

### 16.1 The Value-Delivery Chain

Every APEX engagement is a concrete instance of:

> **Scenario → Solution → Use Case → Service → Persona → KPI**

Sellers walk top-down in executive conversations; architects walk bottom-up in architect conversations. The chain keeps commercial discussions anchored to operational reality.

A full catalog of 723 productized scenario instances (100+ per Practice × 7 Practices) is published as the APEX Scenario Library, detailed in §19. The 35 featured scenarios (5 per Practice) carry full chain detail plus Wave ribbons (§19.3); the remaining ~688 are captured as compact, filterable catalog rows.

### 16.2 Worked Example — Cold-Chain Excursion

- **Scenario:** refrigeration case holds at 48–52 °F (vs 41 °F threshold) for 4h 12m; 412 units across 28 SKUs at risk; store opens 7:00 AM
- **Solution:** Cold Chain Excursion Response (IoT telemetry + FDA food-safety classification + save-viable-vs-destroy logic + inventory quantification + HITL approval + vendor ticketing + regulatory evidence preservation)
- **Use cases:** product salvage, damage assessment, customer notification, regulator evidence chain
- **Service:** RC-E2E-06 Cold Chain Response
- **Personas:** Store Operations Lead, Pull-Team Lead, Store Manager, Inventory Control, Refrigeration Vendor, Food Safety Compliance Lead
- **KPIs:** write-off avoided ($1,313 per event, 71% of at-risk inventory saved); time-to-brief (8 min); manager touch-time (90 s); audit-trail completeness (100%)

The 6:08 AM audit row attributes $1,313 saved to this specific agent decision at Store 100, looping the KPI back to the decision.

### 16.3 Five Nested Commercial Envelopes

```
Commercial Envelope (money & time)
    ← contains ←
Scope Envelope (functional: which services, agents, tools, KPIs)
    ← contains ←
Data Envelope (footprint: which SORs, Gold views, classifications)
    ← derived from ←
Schema Envelope (canonical entities in scope per service)
    ← governed by ←
Trust Envelope (classification + identity + DLP)
```

**Critical relationship:** the *schema envelope* is the architectural kernel of the commercial envelope. More canonical entities in scope → more Silver models, Gold views, MCP tools, agents → higher Wave 2 cost. This makes scope conversations data-driven, not hand-wavy.

### 16.4 Wave Progression

- **Wave 1** — narrow scope, narrow schema, narrow data, narrow agent fleet. 4–8 weeks; $500K–$2M; envisioning + first concrete service + business case.
- **Wave 2** — schema envelope expands to full Practice catalog. 6–15 months; $5M–$15M; commercial envelope grows; trust envelope tightens.
- **Wave 3** — expands across Practices, sites, and autonomy (selectively loosens HITL). Multi-year; $8M–$30M; trust envelope remains authoritative.

Every featured scenario in the Scenario Library (§19) carries a **Wave ribbon** (§19.3) specializing this generic W1→W2→W3 arc into concrete W1 prerequisites, W2 pilot scope with KPI goals, and W3 enterprise-scale + fusion-partner references.

---

## 17. Human Oversight Spectrum — HITL / HOTL / HIC

Human oversight is a three-mode spectrum, not a binary. Most APEX services combine all three across decision classes; the manifest declares the mode per class.

| Mode | Definition | Latency | Scale Ceiling | When |
|------|------------|---------|---------------|------|
| **HITL** (Human-In-The-Loop) | Agent pauses; human approves / rejects / modifies; action then executes | Seconds to hours | Bounded by human bandwidth | Consequential decisions (write-off approval, personnel action, safety override) |
| **HOTL** (Human-On-The-Loop) | Agent acts autonomously within constraints; human supervises dashboards, reviews exceptions, intervenes on anomalies | Near-zero agent latency; human observability in minutes | Scales to thousands of decisions/hour | Routine pattern matching (alert categorization, demand forecast) |
| **HIC** (Human-In-Charge) | Human uses APEX outputs as decision support; final call is human; audit captures review and override | Strategic (quarterly, annual governance) | Scales to organizational strategy | Policy refresh, model-retraining decisions, risk-appetite adjustment |

**Regulatory alignment.** The EU AI Act (Article 14) defines "appropriate human oversight" to include all three modes. APEX's manifest declares the mode per decision class and emits it into the audit row, giving regulators an explicit mapping from their obligation to the system's operation.

---

## 18. Reference Implementations & Delivery Waves

### 18.1 Canonical Reference Deployments

Each Practice ships a canonical reference deployment — a complete, tested instance that Wave-1 teams specialize rather than build from scratch.

- **Big Box Store (RC)** — Retail Operations command center, cold-chain excursion response, markdown cadence
- **Hospital (HLS)** — sepsis early-warning, clinical decision support, utilization management
- **Utility (ER)** — outage triage + restoration sequencing, demand forecasting
- **Plant (AXLE)** — connected factory, predictive maintenance, quality optimization
- **Airline (TH)** — IROP recovery, crew scheduling, revenue optimization

Each reference specifies: triggering scenario; solution architecture (agents, orchestrations, gates); use cases and personas; KPI targets; typical Wave-1 scope; regulatory / compliance artifacts.

### 18.2 Wave Playbook Structure

Each Practice's delivery playbook contains:

- Discovery-prompt templates per Wave
- Objection handlers tuned to Practice stakeholders
- Pre-clearance checklists for technical, legal, and compliance reviews
- Reference-architecture sketches per Wave
- Commercial envelope ranges calibrated from real engagements
- Governance milestones per Wave

---

## 19. Scenario Library & Wave Ribbon Pattern

### 19.1 Why a Scenario Library

APEX engagements are instances of the value-delivery chain from §16. A seller can cite three scenarios from memory, but an enterprise-grade credibility posture requires a **catalog** — a breadth signal that backs up the five or six scenarios the seller actually walks in any given meeting.

The canonical APEX Scenario Library ships as a reference dataset of **723 productized scenarios** (100+ per Practice × 7 Practices) with **35 featured scenarios** (5 per Practice) detailed as full Scenario→KPI chains. The library is rendered interactively in `APEX-Stacked-Architecture-Narrated.html` Chains tab.

### 19.2 Three-Tier Structure

| Tier | Count | Purpose | Depth |
|------|-------|---------|-------|
| **Featured scenarios** | 35 (5 per Practice) | Deep-walk material — the opening move in an executive conversation | Full Scenario → Solution → Use Case → Service → Persona → KPI chain + Wave ribbon |
| **Browsable library** | ~723 (100+ per Practice) | Breadth signal — "what else do you have?" Filter-and-scan catalog | Compact: title, service code, brief, primary KPI |
| **Wave 3 fusion mesh** | *(planned)* | The scenarios that compose *other* scenarios after W2 proves out | Named combinations (e.g., "Perishables Economics Mesh" = cold-chain + markdown + loyalty-churn) |

Each scenario row carries **five structured fields**:
- `title` — the customer-facing scenario name
- `service_code` — anchor into the Service Catalog (e.g. `RC-E2E-03`, `HLS-E2E-02`)
- `brief` — one-sentence scenario description
- `kpi_display` — the headline outcome (e.g. "+3.2pp GM", "−58% cycle time", "$8.6M recovery")
- `kpi_kind` — semantic class: `down` (teal reductions), `up` (amber increases), `money` (gold dollar), `''` (neutral positive)

### 19.3 Wave Ribbon — Framing the Scenario in its Delivery Progression

Every featured scenario carries a **three-column Wave ribbon** at the top of its expanded view:

| Wave | Role | Content | Color rail |
|------|------|---------|-----------|
| **W1 — Foundation** | Prerequisites | Schema projections, LEDGER instantiation, MCP tools, HITL approval surfaces that must exist before the agent runs | Sky blue (`--sky`) |
| **W2 — Pilot** *(you are here)* | Reference deployment | Pilot scope, goal KPIs, approval authority — the scenario at its proof-point scale | Gold (`--gold`), slightly elevated with subtle glow |
| **W3 — Scale & Fuse** | Enterprise progression | Full-footprint scope + named adjacent-agent fusions that only make sense after W2 proves out | Amber (`--amber`) |

**W3 fusion references** appear in amber italics within the W3 cell (e.g., *"Fuses with the dynamic-markdown and loyalty-churn agents…"*), signaling the mesh of scenarios that compose after W2 proves out. This is not redundant with §16.4 — it is the **per-scenario specialization** of the generic Wave progression, named concretely against the scenario's neighbors.

### 19.4 Worked Example — Cold-Chain Excursion

The Cold-Chain Excursion scenario (Practice RC, Scenario 01, Service RC-E2E-03 + RC-E2E-09) carries this Wave ribbon:

- **W1 — Foundation.** FSMA 204 lot-traceability in `SCML.Lot`; store-level temp telemetry via Real-Time Hub; LEDGER audit-row for markdown/destroy decisions; HITL Adaptive Card surface wired to Teams.
- **W2 — Pilot** *(you are here)*. One 250-store cluster, dairy + deli + produce cases. Excursion detection → markdown/destroy decisioning with manager approval. **Goal:** prove 5.2 hr/shift time-return and 18% shrink reduction on the pilot footprint.
- **W3 — Scale & Fuse.** All stores enterprise-wide, all perishable categories. Agent fuses with *dynamic-markdown* and *loyalty-churn* agents so a single excursion-driven markdown respects customer-tier elasticity and forward shrink trajectory.

### 19.5 Design Goals Served by This Pattern

1. **Executive conversation** — the ribbon collapses the engagement arc into three sentences: "this is our Wave-2 reference deployment, these are the W1 rails we set down, this is what W3 scale-and-fuse looks like."
2. **Architect conversation** — W1 enumerates exact schema reads and LEDGER surfaces so a solution architect can quote W1 SoW scope directly from the card.
3. **CFO conversation** — W2 goals are quantified ("prove X"); W3 is qualified ("all stores, fused with Y"). The buyer sees W2 as a bounded, measurable bet and W3 as the scaling option.

### 19.6 Library Governance

The Scenario Library is a first-class governance artifact. Changes follow the same SemVer discipline as any L1-adjacent contract:

- **PATCH** — copy edits, KPI re-measurements, brief refinements
- **MINOR** — new scenario added, or new fields added to a row
- **MAJOR** — schema change (e.g. adding `wave_ribbon` as a top-level field for all 723 scenarios, which is currently MINOR because only the 35 featured rows carry it)

The library is embedded in `APEX-Stacked-Architecture-Narrated.html` as a single JavaScript constant (`APEX_SCENARIO_LIBRARY`, ~106 KB JSON blob). Versioning metadata is carried in the containing HTML's header.

---

## 20. Stacked Architecture Visualization & Narration

### 20.1 Why Narrated Cinematics Exist

APEX's ten-layer stack from §4 is correct, but dense. A narrative-quality, voiceover-narrated walkthrough of the stack — with each layer foregrounded in turn — is a higher-throughput communication channel for exec-level conversations than the technical reference text alone.

The canonical artifact is `APEX-Stacked-Architecture-Narrated.html`: a self-contained, single-file HTML cinematic that renders the full stack, tabs through each layer, and narrates the architecture via the Web Speech API (Brian voice, British-English documentary register).

### 20.2 Artifact Structure

**11 tabs** (corresponding to architectural domains):

1. **Overview** — the stacked-architecture cinematic (12 scenes + APEX acronym band + LEDGER feedback loop)
2. **Foundation** — Part I platform foundation (medallion, schemas, Microsoft-native deployment)
3. **Data Plane** — Fabric / OneLake / Delta-Iceberg interop
4. **Schemas** — canonical schema families per Practice
5. **Standards** — industry standards binding (GS1, FHIR, CIM, ISA-95, J1939, TM Forum SID, OpenTravel, …)
6. **Reasoning** — Azure AI Foundry runtime, model pins, prompt versioning
7. **Runtime** — orchestrator, HITL gates, LEDGER, audit row
8. **Context** — Chapter 6 deep dive on the three context sources (structured, semantic, documentary)
9. **Services** — productized service catalog per Practice
10. **Chains** — value-delivery chain catalog (35 featured + modal library of 723)
11. **Practices** — seven-practice overview (RC, HLS, ER, AXLE, TMT, TH, ICE)

### 20.3 Narration Deck Model

Each tab carries a **scene deck** that drives both the visual focus-stepping and the voiceover narration:

```
tabNarrations = {
  overview: { label, scenes: [{ id, title, anchor, narration }, ...] },
  foundation: { ... },
  ...
}
```

The narration engine exposes **play / pause / skip / previous** controls, scene-index indicator, and an on-screen caption lane. Captions display the current scene's narration text in a Fraunces-italic typographic treatment.

### 20.4 The Ten-Layer Stack (rendered visually)

The Overview tab renders the full stack with per-layer color-coded emission bars (amber / teal / gold / sky / violet / crimson / ember):

1. **Experience Plane** — Teams, Copilot, Power BI, Power Apps (user-surface)
2. **Orchestration Plane** — Azure AI Agent Service (DAG orchestrator)
3. **Reasoning Plane** — Azure AI Foundry, Azure OpenAI (GPT-4o + model pins)
4. **Context Plane** — three sources: structured (MCP tools), semantic (vector + episodic), documentary (file-first)
5. **Identity Plane** — Entra managed identities per agent + visibility lattice
6. **Governance Plane** — HITL gates, LEDGER audit row, Purview classification
7. **Data Plane** — Microsoft Fabric / OneLake, medallion (Bronze/Silver/Gold)
8. **Integration Plane** — MCP servers (domain / utility / external), Real-Time Hub
9. **Infrastructure Plane** — Azure subscription, landing zone, networking, Key Vault
10. **Feedback Plane** — LEDGER → KPI attribution → manifest evolution (the loop that makes W1→W2→W3 non-linear)

### 20.5 Authoring Pipeline

The established pipeline for these cinematic artifacts:

1. **Markdown specification** — scene list, narration text, layer descriptions in a Claude Code build-instruction file
2. **HTML scaffold** — design tokens applied (see §22), tab structure scaffolded
3. **Scene-by-scene build** — each scene's visual (SVG or CSS-driven) authored alongside its narration text
4. **Web Speech API wiring** — voiceover engine, captions, play/pause controls
5. **Validation** — div balance, JS parse, accessibility (focus management, keyboard nav)
6. **Present** — single-file HTML deliverable to `/mnt/user-data/outputs/`

### 20.6 Narration Style Guide

- **Voice:** Brian (Web Speech API, British-English)
- **Register:** documentary narrator — authoritative, paced, no marketing language
- **Sentence length:** 18–32 words; complete sentences, no bullets spoken aloud
- **Cadence:** each scene is 3–6 sentences; total tab narration 90–180 seconds
- **Prohibited words:** "partner", "alliance", "strategic alliance" (Deloitte Independence constraint; see §22.4)

---

## 21. Published Communication Artifacts

APEX ships a layered set of published artifacts. Each has a distinct audience and purpose; together they form the complete communication surface.

### 21.1 The Artifact Stack

| Artifact | Format | Audience | Purpose |
|----------|--------|----------|---------|
| **Professional APEX (Wrox book)** | HTML + PDF | Architects, engineers, developers | Full technical reference — 20+ chapters, deep dives, code listings |
| **Professional APEX Sellers Guide** | HTML + PDF | Account Teams, GPLs, sellers, solution architects | Commercial framing — value-delivery chain, discovery prompts, objection handlers, scenario ammunition |
| **APEX Stacked Architecture Narrated** | Single-file HTML (cinematic) | Executive audiences in live meetings | Voiceover-narrated architecture walkthrough — SteerCo-grade |
| **APEX Design Reference** | Markdown *(this document)* | Architects, Practice Leads, Delivery Leads | Canonical design baseline — the "source of truth" for all other artifacts |
| **APEX Sellers Guide Runtime Addendum** | DOCX + PDF | Sellers in the field | Pocket-sized talking points for the Runtime plane (Orchestration, HITL, LEDGER, Audit) |
| **Store 100 Facilitator Guide** | DOCX + PDF | Workshop facilitators | Step-by-step walk of the canonical Big Box Store (RC) reference deployment |
| **Comprehensive Solutions Reference** | DOCX + PDF | Pre-sales, discovery leads | Catalog view of all services across Practices |
| **Per-Practice Build Specs** | Markdown | Practice Leads, Platform Engineers | Implementation-level specification per Practice (RC, HLS, ER, AXLE, ICE, TMT, TH) |

### 21.2 Artifact Cross-References

- The Sellers Guide cites Design Reference §16 for the value-delivery chain.
- The Stacked Architecture Narrated HTML cites Design Reference §4 for the ten-layer stack, §16 for the chain pattern, and §19 for the Scenario Library.
- The Wrox book cites Design Reference §§3–11 for canonical architecture.
- The Design Reference (this document) is the **single source of truth**; when artifacts diverge, the Design Reference wins and the artifact is updated.

### 21.3 Authoring & Publishing Pipeline

Markdown specs first (as Claude Code build instructions) → interactive HTML as SteerCo-grade presentation artifacts → Word/PDF documents for client-facing talking points. Artifact creation tooling includes `pptxgenjs` (PowerPoint), `openpyxl` (Excel), LibreOffice (PDF conversion / QA), Web Speech API (narrated HTML).

All deliverables are saved to `/mnt/user-data/outputs/` and presented for download. Compliance check (Independence-language review per §22.4) is built into the pipeline.

---

## 22. Design-System Conventions

The APEX communication surface is unified by a shared design system. These conventions are enforced across all published artifacts (§21) to give clients a consistent visual and linguistic experience.

### 22.1 Typography

| Use | Typeface | Fallback |
|-----|----------|----------|
| **Display** (titles, headings, eyebrows) | **Fraunces** (serif) | Georgia, serif |
| **Body** (prose, tables) | **IBM Plex Sans** (sans-serif) | Inter, system-ui |
| **Monospace** (code, service codes, metadata) | **JetBrains Mono** | SFMono-Regular, Consolas |

Inter and Roboto are explicitly **not** used as primary typefaces — Fraunces is the APEX visual signature.

### 22.2 Color Semantics

**Universal semantics** (apply across all artifacts and Practices):

| Token | Role | Visual |
|-------|------|--------|
| `--amber` | HITL, human-approval surfaces, decision-moment UI | Warm amber |
| `--teal` | Agent / autonomous action, reductions ("−34%") | Cool teal |
| `--gold` | Outcomes, KPI highlights, dollar figures, W2 *(you are here)* | Rich gold |
| `--crimson` | Critical severity, errors, destructive actions | Deep crimson |
| `--sky` | Data, schema reads, W1 Foundation | Soft sky |
| `--violet` | Schema / service anchors, TMT Practice | Muted violet |
| `--ember` | Identity, ICE Practice | Amber-red hybrid |

**Per-practice banner colors** (used in Chains tab and Scenario Library):

| Practice | Banner Color | Token |
|----------|--------------|-------|
| RC — Retail & Consumer | Amber | `--amber` |
| HLS — Healthcare & Life Sciences | Crimson | `--crimson` |
| ER — Energy & Resources | Gold | `--gold` |
| AXLE — Industrial & Manufacturing | Teal | `--teal` |
| TMT — Technology, Media & Telecom | Violet | `--violet` |
| TH — Travel & Hospitality | Sky | `--sky` |
| ICE — Industrial & Commercial Equipment | Ember | `--ember` |

### 22.3 Theme

- **Default mode:** dark-first (charcoal background, warm-ink text)
- **Light mode:** warm-paper (cream background, dark-ink text)
- **Toggle:** expected on every visual artifact; persists via CSS class `body.light`

### 22.4 Independence-Compliance Linguistic Rules

These rules apply to **every word** emitted in any APEX artifact or narration, without exception:

- **NEVER** use "partner", "alliance", or "strategic alliance" to describe the Deloitte–Microsoft relationship
- **Approved substitutes:** "Deloitte's Microsoft practice", "DMTSP", "Microsoft platform capabilities", "Microsoft-native deployment", "Deloitte Microsoft Technology Solutions & Practices"
- Compliance check runs as a pre-publish step for every artifact

### 22.5 Responsive & Accessibility Baseline

- All cinematic artifacts render at `viewport ≥ 900px` at full fidelity; narrower viewports collapse to stacked layouts
- `prefers-reduced-motion: reduce` disables scene-transition animation
- `prefers-color-scheme` respected at initial load if no user override set
- All interactive elements (`<button>`, `<dialog>`, `<details>`) use native HTML primitives with full keyboard and ARIA support
- Modal dialogs use the native `<dialog>` element for built-in Esc-to-close and focus management

---

## 23. Glossary of Terms

| Term | Definition |
|------|------------|
| **ACK_ONLY** | HITL gate kind meaning "notify + auto-apply" (default for MINOR) |
| **Agent** | Reasoning component in Azure AI Foundry / Agent Service with system prompt, tool allow-list, model pin, manifest |
| **Agent-safe view** | Derivative of a Gold view with classification-appropriate masking, scoped to agent tenant / practice / persona |
| **APEX** | Agent-based Platform for EXecution — Deloitte's internal delivery accelerator for agentic AI on Microsoft platform |
| **APEX Scenario Library** | Reference catalog of 723 productized scenarios (100+ per Practice × 7 Practices) embedded in the Stacked Architecture Narrated HTML; 35 are featured with full chain detail |
| **Audit row** | Structured, tamper-evident, signed record of a decision; the unit of work an agent performs |
| **Bronze** | Medallion layer where SOR data lands in source-native shape; read-only for Silver transforms |
| **Browsable library** | Tier 2 of the Scenario Library: ~100 compact scenario rows per Practice, filterable and alphabetically sorted in a `<dialog>` modal |
| **Canonical envelope** | Five universal fields on every Silver row: `event_id`, `event_ts`, `entity_id`, `source_system`, `source_system_ts` |
| **Canonical schema** | Semantic contract naming entities, relationships, classifications, types, standards |
| **Chain (value-delivery)** | The pattern Scenario → Solution → Use Case → Service → Persona → KPI — every APEX engagement is an instance |
| **Contract (L1)** | Normative `apex-core` specification |
| **Decision audit row** | Append-only record capturing inputs, outputs, approver, rationale, rollback pointer |
| **Direct Lake** | Power BI query path reading OneLake Delta directly; sub-second refresh; Import-speed query |
| **DMTSP** | Deloitte Microsoft Technology Solutions & Practices — the practice under which APEX is developed and delivered |
| **Edition (L2)** | Versioned, pinned release of L1 Core |
| **Entra** | Microsoft identity service; issues managed identities for agents and services |
| **ESCALATION** | HITL gate kind routing to a cross-functional owner |
| **Eventhouse** | Fabric's real-time item; KQL-queried; sink for Bronze streaming |
| **Fabric** | Microsoft's unified SaaS data platform; APEX's data plane |
| **Featured scenario** | Tier 1 of the Scenario Library: 5 per Practice × 7 Practices = 35; full Scenario → KPI chain with Wave ribbon |
| **Foundry** | Azure AI Foundry; APEX's reasoning plane runtime |
| **Fusion (W3)** | Composition of two or more agents after their individual W2 pilots prove out — the emergent mesh of scenarios that only makes sense at enterprise scope |
| **Gate kind** | One of ZERO_TOUCH, ACK_ONLY, HITL, ESCALATION |
| **Gold** | Medallion layer; agent-consumable views and pre-measures; materialized for low latency |
| **HIC** | Human-In-Charge; human uses APEX outputs as decision support |
| **HITL** | Human-In-The-Loop; agent pauses for approval |
| **HOTL** | Human-On-The-Loop; human supervises autonomous operation |
| **Independence** | Deloitte audit-independence constraint; governs how the Deloitte-Microsoft relationship is described in all artifacts (no "partner/alliance") |
| **L1 / L2 / L3 / L4** | Contract / Edition / Practice / Tenant |
| **LEDGER** | APEX's decision-provenance store; holds policy corpora, HITL approval surfaces, and audit rows |
| **Managed identity** | Entra service principal with credential-free auth to Azure resources |
| **Manifest** | Git-versioned definition of a schema, agent, event, orchestration, policy, or service |
| **MCP** | Model Context Protocol — open-standard typed contract for agent tools |
| **Medallion** | Bronze / Silver / Gold layering — a contract, not a folder convention |
| **Narration deck** | Scene-indexed voiceover script driving a cinematic artifact (Web Speech API + on-screen captions) |
| **OneLake** | Fabric's unified tenant-scoped storage substrate |
| **Orchestration** | Multi-agent composition with manifest governance; ships as one of 47 archetypes |
| **Persona** | User role with permissions, KPIs, typical workflows |
| **Practice (L3)** | Industry bundle (RC / HLS / ER / AXLE / TMT / TH / ICE) containing schemas, agents, MCP, orchestrations, gates, services, personas, KPIs |
| **Purview** | Microsoft governance service for classification, lineage, DLP, Unified Catalog |
| **SCD2** | Slowly Changing Dimension Type 2 — history via `valid_from` / `valid_to` |
| **Scenario Library** | See **APEX Scenario Library** |
| **Service** | Named, productized APEX capability with persona, KPI, SLO, commercial terms |
| **Silver** | Medallion layer; canonical, cleaned, typed, deduplicated, enriched, tokenized |
| **SLO** | Service Level Objective — latency, freshness, availability targets |
| **SOR** | System of Record — source system of truth (ERP, CRM, EHR, WMS, …) |
| **Stacked Architecture** | APEX's ten-layer plane stack (Experience / Orchestration / Reasoning / Context / Identity / Governance / Data / Integration / Infrastructure / Feedback) — canonical visual representation in the Narrated HTML |
| **Tenant (L4)** | Client instance; pins a Practice release; subscribes to services |
| **Tokenization** | Deterministic reversible encoding of PII/PHI so agents never see cleartext |
| **Trace** | End-to-end instrumentation linking agent reasoning, tool calls, and approvals via shared `trace_id` |
| **Trace-id** | UUID binding all steps of an orchestration into one forensic thread |
| **Visibility lattice** | Composition of tenant × practice × persona × classification × row filters determining an agent's effective view |
| **W1 / W2 / W3** | Delivery Waves — Foundation (prerequisites) / Pilot (reference deployment) / Scale & Fuse (enterprise + mesh); see §16.4 and §19.3 |
| **Wave ribbon** | Three-column visual at top of every featured scenario card showing W1 Foundation / W2 Pilot / W3 Scale-&-Fuse cells with colored rails |
| **Workspace** | Fabric logical container holding Lakehouses, Warehouses, Eventhouses, pipelines, notebooks |
| **ZERO_TOUCH** | HITL gate kind meaning "apply silently, log as auto-taken" (default for PATCH) |

---

## 24. Appendix Catalog

The published APEX documentation set includes the following appendices, each of which acts as a normative reference:

| Appendix | Contents |
|----------|----------|
| **A. Schema Reference** | Master list of all canonical schema families (SCML, MERML, CXML, HLSCML, ERCML, AXLECML, TELML, IROPsML, ConnectedICEML) with DDL, entity definitions, attribute mappings |
| **B. Service Catalog Master Registry** | Every APEX-shipped service (tokenizer, approvals, ledger, policy, fabric-mcp, etc.) with interfaces, SLOs, commercial terms |
| **C. KPI Master Registry** | Canonical KPIs across Practices with definitions, owners, consumers |
| **D. Orchestration Catalog** | 47 orchestration archetypes with triggers, decision trees, approval flows, gate placement |
| **E. Persona Catalog** | Personas (Store Manager, Pharmacist, Grid Operator, QA Engineer, Procurement Manager, …) with permissions, workflows, required KPIs |
| **F. MCP Tool Catalog** | Complete tool catalog by server class (domain / utility / external) with schemas, SLOs, classification propagation rules |
| **G. Microsoft Product & SKU Reference** | Azure AI products, Fabric workloads, licensing models, capacity-sizing guidance |
| **H. Partner Ecosystem** | Deloitte practices, Azure architecture patterns, Microsoft partner solutions |
| **I. Glossary** | 65+ canonical terms (see §23) |
| **J. Exercise Solutions** | Solutions to Wrox-style exercises in each chapter |
| **K. Independence, Tech-Stack Posture & Competitive Differentiation** | How APEX's manifest-driven, auditable design positions Deloitte vs. competing consulting practices |
| **L. Scenario Library Master Catalog** | All 723 scenarios across 7 Practices; featured-scenario chain details + Wave ribbons for the 35 anchor scenarios; JSON dump of `APEX_SCENARIO_LIBRARY` constant |
| **M. Narration Script Catalog** | All 11-tab narration decks from Stacked Architecture Narrated HTML; per-scene text, scene anchors, voiceover timing guidance |
| **N. Design-System Reference** | Typography, color tokens, per-practice banner colors, theme tokens, Independence linguistic rules; CSS variable reference |
| **O. Visual Artifacts Index** | Stacked Architecture Narrated HTML, Sellers Guide HTML, Wrox book HTML, Sellers Guide Runtime Addendum (DOCX/PDF), Store 100 Facilitator Guide, Comprehensive Solutions Reference — with cross-references to Design Reference sections |

---

## Design Summary

APEX is a **manifest-driven, auditable agentic platform** that:

1. **Separates concerns** across four layers (Contract → Edition → Practice → Tenant) enabling backward-compatible evolution.
2. **Canonicalizes** enterprise data via a medallion architecture (Bronze → Silver → Gold) governed deterministically.
3. **Contracts tools** via MCP with typed I/O, rate limits, and trace instrumentation — decoupling agents from infrastructure.
4. **Gates decisions** deterministically from SemVer bump class → gate kind (ZERO_TOUCH / ACK_ONLY / HITL / ESCALATION), with tenant override.
5. **Protects sensitive data** via tokenization at the Bronze / Silver boundary — agents never hold cleartext PII/PHI.
6. **Audits everything** via structured decision rows capturing every reasoning step, approval, and rollback, with `trace_id` forensic threading and a three-version (manifest + policy + prompt) rule.
7. **Runs natively on Microsoft Fabric** (data plane) + Azure AI Foundry (reasoning) + Copilot/Teams/Power BI (experience) + Purview (trust) + Entra (identity), bound by Git-versioned contracts.
8. **Ships seven Practices** (RC, HLS, ER, AXLE, TMT, TH, ICE) each with canonical schemas, 40–50 agents, 15–25 orchestrations specializing 47 archetypes, and a named service catalog — collapsing 18–24-month ground-up builds to 9–12 months.

The design's priorities — **auditability**, **determinism**, **backward compatibility**, **data protection**, **operational visibility** — make APEX suitable for regulated enterprises (healthcare, energy, financial services, public sector) where decision governance, compliance posture, and regulator-grade evidence are non-negotiable.
