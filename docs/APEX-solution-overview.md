# APEX — Solution Overview

**Document class:** Solution reference
**Audience:** DMTSP SteerCo · Account Teams · engagement engineers · client CTOs evaluating APEX
**Status:** Current as of APEX Core v1.2 (2026-04-17)
**Maintainer:** APEX SteerCo
**Related documents:**
- `apex-core-build-spec.md` — the authoritative Core specification
- `apex-core-v1.1-amendment.md` — formal edition registry
- `apex-core-v1.2-amendment.md` — schema versioning manifest
- `docs/plans/2026-04-17-schema-versioning-manifest-design.md` — design rationale for v1.2
- `docs/plans/2026-04-17-schema-versioning-manifest-implementation.md` — implementation plan

---

## Part 0 — Compliance & Language Constraints (Inherited)

This document inherits Part 0 of APEX Core. All Deloitte–Microsoft terminology rules apply (see Core Part 0). All examples use synthetic, clearly fictional client names. No client-identifiable data appears anywhere in this document.

---

## Part 1 — What APEX Is

APEX (Agentic Platform for Enterprise eXecution) is a domain-canonical reference framework for deploying agentic AI systems on Microsoft-native infrastructure. It is produced by Deloitte's Microsoft practice (DMTSP) as the opinionated answer to a recurring question from enterprise clients entering the Agentic Era: *how do we deploy a disciplined, compliant, and economically-sound agent fleet on Azure / Microsoft Fabric, and how do we avoid reinventing the wheel every time we onboard a new industry?*

APEX answers this by giving every industry a shared grammar (the Core framework) and an industry-specific dialect (the edition). The grammar defines *how* things are named, shaped, and composed — Forces of Change, AI Journey Eras, a Commercial Maturity Model, a seven-layer reference architecture, canonical schemas, agent fleets, twelve numbered orchestrations, a gate taxonomy, a design system, and a set of reusable widgets. The dialect — an edition — populates that grammar with the nouns, verbs, and cadences of a specific industry: Retail & Consumer (RC), Travel & Hospitality (TH), Health Care & Life Sciences (HLS), Technology Media & Telecom (TMT), Energy & Resources (ER), Industrial & Commercial Equipment (ICE), and the two reserved editions Financial Services (FS) and Public Sector (PS).

### 1.1 What APEX is not

APEX is not a product. It is not a SaaS offering. It is not middleware that Deloitte hosts. It is not a platform with a dashboard that clients log into. APEX is a **framework of frameworks** — a set of specs, conventions, shared data, and reusable tools — that clients instantiate on their own Microsoft-native infrastructure. Deloitte's Microsoft practice engagements *use* APEX to produce client-specific solutions; clients do not "buy APEX."

This posture is deliberate. It preserves Independence, it matches how Microsoft Fabric / Azure AI Agent Service / Logic Apps are actually procured and deployed, and it lets Deloitte ship improvements to the framework at the pace of software rather than the pace of commercial contracts.

### 1.2 Core vs. Editions

Everything APEX defines lives in one of two places:

- **Core (`apex-core/`)** — industry-agnostic conventions, shared content (AI Journey Eras, CMM stages, event envelope, HITL gate taxonomy, design tokens, reusable widgets). Core changes rarely. Every edition inherits it.
- **Editions (`apex-rc/`, `apex-th/`, etc.)** — industry-specific content. Forces of Change specific to that industry. Three-to-five canonical schemas shaped to industry grain. A fleet of agents (typically 30–34 per edition). Twelve orchestrations that solve that industry's highest-blast-radius decisions. Industry-specific ISV bindings. Industry-specific reference implementations ("Day in the Shift" for retail, "Day in the GM Seat" for lodging, "Day in the OIM Seat" for offshore platforms).

Clients see editions. They never see Core directly. Core is the DMTSP-facing IP.

---

## Part 2 — The Problem APEX Solves

### 2.1 The five pains APEX addresses

Enterprise clients entering the agentic era typically run into five compounding pains:

1. **Bespoke everything.** Every agent, every schema, every orchestration is designed from scratch. A retailer's "inventory agent" and a hotel chain's "inventory agent" look nothing alike even when the underlying decision shape is identical. No cross-engagement reuse, no knowledge compounding.
2. **Schema drift and silent breakage.** Data schemas evolve. Downstream agents and ORCH contracts break quietly because there is no version pin, no diff, and no migration discipline.
3. **Weak HITL discipline.** "Human in the loop" gets handwaved. Nobody writes down which decisions require human approval, which are acknowledge-only, and which are fully autonomous. Audit trails suffer.
4. **ROI invisibility per wave.** The enterprise invests in a 12-month agentic program and cannot answer "what did Wave 1 actually return?" in concrete dollars-and-cents. Waves 2+ starve.
5. **Compliance and Independence uncertainty.** Who owns what data plane? Where does client PII live? What happens when Deloitte's Independence posture changes? Most programs hand-wave this and deal with it after the fact.

APEX addresses each of these directly:

| Pain | APEX answer |
|---|---|
| Bespoke everything | Shared grammar in Core; industry dialects in editions. Reuse at the *convention* layer even when content diverges. |
| Schema drift | Four-layer manifest model with SemVer + bump-classification + auto-apply rules (Core v1.2). |
| Weak HITL | Core Part 8.3 taxonomy: HITL / ACK_ONLY / ZERO_TOUCH / ESCALATION. Every agent and ORCH declares its gate explicitly. |
| ROI invisibility | Wave model: four waves, each self-funding, with `expected_economics` and exit criteria baked into Part 12 of every edition. |
| Compliance & Independence | Part 0 terminology rules (inherited by every edition, enforced by `lint-compliance.js`). Independence posture explicit: client-tenant data planes; no Deloitte-side retention. |

### 2.2 Why framework-of-frameworks (and not a product)

A product would require Deloitte to host, update, and operate something the client's IT team depends on — and to share responsibility for outages. A framework-of-frameworks lets Deloitte ship opinions without taking on operational liability. Clients deploy APEX-shaped solutions on their own Microsoft infrastructure. Deloitte's value is the framework, the implementation expertise, and the ongoing engagement — not a runtime.

This also matches Microsoft's own go-to-market. Fabric, Azure AI Agent Service, and Logic Apps are sold and consumed by the client, with Microsoft's billing, SLAs, and telemetry. APEX sits on top, not in front of.

---

## Part 3 — The Edition Registry

APEX Core v1.1 introduced a machine-readable edition registry at `apex-core/data/edition-registry.json`. Each entry declares the edition's code, full name, accent color tokens, status, sub-variants, schema count, agent count, and reference implementations. Today the registry carries nine entries:

| Code | Name | Status | Sub-variants | Schemas | Agents |
|---|---|---|---|---|---|
| **RC** | Retail & Consumer | Active | — | 4 | 34 |
| **TH** | Travel & Hospitality | Active | airline, cruise, lodging (informal) | 4 | 30 |
| **HLS** | Health Care & Life Sciences | Planned | PRV, LS (formal) | 5 | 34 |
| **TMT** | Technology, Media & Telecom | Planned | TEL, MED, TEC (formal) | 5 | 30 |
| **ER** | Energy & Resources | Planned | OG, PU, MN (formal) | 5 | 32 |
| **ICE** | Industrial & Commercial Equipment | Planned | HVY, AD, AUT (candidates) | 5 | 32 |
| **FS** | Financial Services | Reserved | BNK, INS, IM (candidates) | — | — |
| **PS** | Public Sector | Reserved | FED, SLG (candidates) | — | — |

**Formal vs. informal sub-variants.** Formal sub-variants (e.g., HLS-PRV vs HLS-LS) are tagged on every agent, orchestration, and schema entity; they show up as filters in the edition site. Informal sub-variants (e.g., TH airline vs cruise) are descriptive only — handled via specialized dimensional anchors and tool prefixes without explicit tagging. Promotion from informal to formal is a Core amendment, never a silent refactor.

**Edition-split policy (v1.1).** Two industries justify separate editions only when **all four** of these tests are true: operational vocabulary diverges materially; regulatory floor diverges materially; schema grain diverges materially; primary user personas diverge materially. Fewer than four → sub-variant. This is the policy that kept TH from splitting into three editions (the operational overlap between airline, cruise, and lodging is still too high) and that *will* eventually split ICE-AD into APEX-AD once export-control posture diverges further.

---

## Part 4 — The Seven-Layer Reference Architecture

Every edition inherits the same seven-layer architecture (Core Part 6). The layer model is Microsoft-native by default; editions define which source systems feed L1 and which experiences expose L7.

| Layer | Name | Primary Microsoft services | Function |
|---|---|---|---|
| **L1** | Edge & Source | *Edition-defined* (POS, PMS, CRS, core banking, SCADA, EMR, ...) | Origin systems emit events and state. |
| **L2** | Ingest & Integration | Fabric Data Factory, Event Hubs, IoT Hub, Synapse Link | CDC + streaming ingestion; API mediation. |
| **L3** | Storage | OneLake (Fabric), Azure Data Lake, ADX for telemetry | Bronze–Silver–Gold medallion. |
| **L4** | Semantic | Fabric Lakehouse + SQL endpoints; Power BI semantic models | Canonical schema registries (the MERML / HOSML / REVML / ... of the world). |
| **L5** | Intelligence | Azure AI Foundry, Azure OpenAI, Azure AI Search, embedding stores | Models, retrieval, evaluation harnesses. |
| **L6** | Orchestration | Azure AI Agent Service (DAG), Logic Apps, Durable Functions | ORCH-01 through ORCH-12 execution. |
| **L7** | Experience | D365 Customer Insights, Copilot, Power Platform, Teams, custom frontends | Where humans and agents collaborate. |

### 4.1 Cross-cutting concerns

The layers are cross-cut by four disciplines that every edition inherits:

- **Identity & access** — Entra ID, Purview for data governance, customer-managed keys.
- **Observability** — Application Insights, Fabric monitoring, custom agent telemetry.
- **Evals & safety** — Azure AI Foundry evals, red-team harness, PII detection.
- **Independence posture** — client-tenant data planes; no Deloitte-side retention of client-identifiable data. This is not negotiable; editions may not soften it.

### 4.2 Medallion architecture (Bronze / Silver / Gold)

Every schema entity is assigned to Bronze, Silver, or Gold with explicit exit criteria for promotion between layers:

| Layer | Purpose | Exit criteria |
|---|---|---|
| **Bronze** | Raw ingested, immutable, source-system schemas preserved | Schema conformance + quality thresholds + lineage complete |
| **Silver** | Cleansed, conformed, canonical schema applied, PII tokenized | Foreign keys resolve + canonical envelope validates + retention classified |
| **Gold** | Business-ready, denormalized, agent-consumable | Agent contract tests pass + BI semantic layer coverage + latency SLO met |

Gold is where agents read. Silver is where the canonical schemas live. Bronze is ungoverned and exists only as a lineage safety net.

---

## Part 5 — Canonical Schemas and the Event Envelope

### 5.1 How schemas are shaped

Each edition defines 3–5 canonical schemas named with a 4–5 character uppercase code ending in `L` or `ML`. `<DOMAIN>ML` means "<Domain> Machine Learning schema" — the suffix is an APEX convention signalling that the schema is designed to feed agent contracts, not only BI.

Examples across editions:

- **RC:** MERML (Merchandising), SCML (Supply Chain), CXML (Customer Experience), MKTL (Marketing)
- **TH:** HOSML (Hospitality / Rooms), REVML (Revenue Management), DISML (Disruption), LOYML (Loyalty)
- **HLS (PRV):** CLNML (Clinical), CRVML (Care-Revenue), ADMML (Admissions), PHRML (Pharmacy), RADML (Radiology)
- **ER (OG):** PRODML (Production), MAINTML (Maintenance), SAFML (Safety), LOGML (Logistics), EMISML (Emissions)

Each schema contains 25–40 entities. Each entity declares its grain, primary key, columns, foreign keys, retention class, PII class, and the MCP tool IDs that read/write it.

### 5.2 The canonical event envelope

Every Silver-layer event entity — in every edition — uses the same canonical envelope. This is the single most important cross-edition concept APEX defines. A client that runs APEX-RC for its retail estate and APEX-TH for its hotel subsidiary can correlate events across both because the envelope is identical.

```
event_id          UUID              -- primary key
event_ts          TIMESTAMPTZ (UTC)
event_type        VARCHAR(64)       -- controlled vocabulary, per-schema enum
entity_id         VARCHAR(32)       -- store_id, property_id, account_id, etc.
product_id        VARCHAR(32)       -- nullable
lot_id            VARCHAR(32)       -- nullable, SGTIN-compatible
customer_id       VARCHAR(32)       -- tokenized, nullable
business_step     VARCHAR(32)       -- EPCIS-compatible controlled vocabulary
disposition       VARCHAR(32)       -- EPCIS-compatible controlled vocabulary
source_system     VARCHAR(32)
source_system_ts  TIMESTAMPTZ
payload           JSONB
pii_tokenized     BOOLEAN
```

Editions extend the controlled vocabularies for `business_step` and `disposition`. RC uses `receiving`, `putaway`, `picking`, `stocking`, `selling`, `returning`, `disposing`, `transferring`. TH uses analogous verbs for its own domain. But the envelope shape does not change.

### 5.3 Dimensional anchors

Each edition defines its dimensional anchors (snowflake tables) to which every Silver entity can resolve. RC: `DIM_STORE`, `DIM_PRODUCT`, `DIM_LOT`, `DIM_EMPLOYEE`, `DIM_CUSTOMER`, `DIM_SUPPLIER`, `DIM_CATEGORY`, `DIM_LOCATION`, `DIM_DATE`, `DIM_TIME`. TH: `DIM_PROPERTY`, `DIM_ROOM_CLASS`, `DIM_RATE_PLAN`, `DIM_GUEST`, etc. These anchors are shared across schemas within an edition.

### 5.4 Gold views as contracts

Gold-layer views follow the naming convention `GV_<SCOPE>_<PURPOSE>` (e.g., `GV_STORE_INVENTORY_TODAY`, `GV_PROPERTY_OCCUPANCY_7DAY`). Editions document their Gold views as **contracts, not materialized entities**. That means: the agents and ORCH contracts bind to the Gold view's shape and SLO; the underlying materialization can change without breaking consumers as long as the contract holds.

---

## Part 6 — Schema Versioning (The v1.2 Manifest System)

Core v1.2 introduced a disciplined answer to schema drift. Prior to v1.2, schemas evolved by pull request and tribal memory; agents that pinned to a particular entity shape broke silently when the shape changed. v1.2 makes schema evolution explicit, machine-enforceable, and auditable across the client fleet.

### 6.1 Four layers

| Layer | File | Owner | Purpose |
|---|---|---|---|
| **L1 — Contract** | `apex-core/data/schema-manifest-contract.json` | APEX SteerCo | Defines the shape every L2 manifest must obey. Versioned with Core. |
| **L2 — Edition catalog** | `apex-<code>/data/schemas.manifest.json` | Edition maintainers | Declares the schemas this edition offers and the SemVer of each. Carries the entity-level changelog. |
| **L3 — Fleet registry** | `apex-fleet/data/fleet-registry.json` | DMTSP Account Teams | Source of truth for which client accounts are pinned to which schema versions, plus each account's upgrade policy. |
| **L4 — Tenant deployed** | `<client-onelake>/apex-sync/deployed-manifest.json` | Client tenant (pull) | Read-only record of what is actually running in that tenant. Never leaves the tenant. |

### 6.2 SemVer rules

Every schema change is classified as MAJOR, MINOR, or PATCH, and every classification maps to one of the HITL gate types Core Part 8.3 already defines:

| Bump | Triggers | Gate | Auto-apply? |
|---|---|---|---|
| **PATCH** | Docs, metadata, PII classification refinement | `ZERO_TOUCH` | Yes, silent |
| **MINOR** | New entity, new *nullable* column, new Gold view, new dimensional anchor, deprecated_in marker | `ACK_ONLY` | Yes, Teams notification |
| **MAJOR** | Remove, rename, change type, change PK, change grain, non-nullable column, envelope toggle | `HITL` | No — requires approval |

Two anti-cheating rules keep authors honest:

1. **Adding a non-nullable column is MAJOR** (see decision table). The safer pattern is two-phase: MINOR to add the column as nullable with a default-populator, then MAJOR in a later release to tighten the NOT NULL constraint.
2. **Renaming is MAJOR.** Never rename in place. The required safer pattern is three phases: MINOR add new, MINOR mark old `deprecated_in`, MAJOR remove old.

The validator checks that the declared `bump` on every changelog entry matches what the bump classifier would compute from the `changes[]` array. Silent under-classification is a critical finding.

### 6.3 Distribution model (GitOps, not Kubernetes)

The Git repository holding L1, L2, and L3 is the source of truth. On merge:

1. The release bundler assembles a per-account bundle from L3, filtering to that one account's pinned versions plus the inlined changelog entries.
2. Each bundle is signed and published to an Azure DevOps artifact feed (or equivalent signed release channel).
3. Each client tenant runs a scheduled Fabric Data Factory pipeline or Logic App that pulls **only its own bundle**, classifies the drift per its local `auto_upgrade_policy`, and applies DDL inside a Fabric transaction.
4. On success, the tenant rewrites its L4 `deployed-manifest.json` and posts a heartbeat back to the release feed. The heartbeat carries only `{ account_id, heartbeat_utc, manifest_hash }` — no row-level data, no client credentials.

This is GitOps (declarative artifacts in Git, reconciled by a pull agent) applied to declarative *data-schema* artifacts. Kubernetes is not in the APEX reference stack and is not introduced here.

### 6.4 Independence posture (Part 6)

This entire distribution model is designed to preserve Core's Independence posture: **client-tenant data planes; no Deloitte-side retention of client-identifiable data**. Deloitte does not push to tenants. Deloitte does not hold tenant credentials. The only things that ever cross the boundary are opaque account IDs, pinned version numbers, manifest hashes, and heartbeat timestamps. Each of those four categories is explicitly scoped; everything else stays in the client's tenant.

---

## Part 7 — Agent Fleets and Decomposition

Each edition defines 30–34 agents grouped into 4 domain buckets. RC's 34 agents, as an example:

- **Merchandising (12 agents)** — dynamic pricing, assortment, planogram compliance, ESL gateway monitoring, POS mismatch detection, phantom OOS detection, pick list optimization, associate routing, void pattern detection, variance correlation, evidence package building, markdown cadence.
- **Supply Chain (8 agents)** — DSD reconciliation, vendor pattern detection, claim assembly, cold-chain telemetry, disposition classification, write-off pre-approval, FDA feed listening, lot trace resolution.
- **Customer Experience (8 agents)** — pick exception handling, substitution ranking, customer confirm gateway, OCR lot extraction, incident pattern detection, stakeholder routing, returns disposition, lifecycle signals.
- **Marketing (6 agents)** — audience building, creative variant generation, campaign orchestration, attribution, LTV forecasting, journey state.

### 7.1 Decomposition philosophy

Every agent has typed sub-agent contracts backtested in isolation before the orchestrator connects them. The `decomposition_note` field in each agent declaration records this: e.g., MER-A01 Dynamic Pricing = "elasticity learner, competitive signal, margin guardrail." The decomposition matters because agents are expensive to debug end-to-end; sub-agent contracts let each piece be tested against a fixed distribution before integration.

### 7.2 Binding to ORCHs

Each agent declares a `primary_orch` — the orchestration that is its main consumer — or `(platform)` if the agent is a cross-cutting capability used by many ORCHs. An agent can participate in multiple ORCHs, but a single primary is named for governance purposes.

---

## Part 8 — Orchestrations (ORCH-01 through ORCH-12)

Every edition defines exactly twelve orchestrations numbered ORCH-01 through ORCH-12. The numbering is a **positional slot**, not a semantic guarantee. ORCH-05 in APEX-RC is Recall Impact; ORCH-05 in APEX-TH is Disruption Recovery. They share a slot position, not a meaning. The numbering exists so DMTSP engagement teams can compare implementation maturity across clients using a consistent grid.

### 8.1 Orchestration contract template

Every ORCH in every edition declares:

```
orch_id
domain
agents                 [list]
trigger                event spec
inputs                 [gold_view | schema_entity]
tool_bindings          [mcp_tool_id]
hitl_gates             [gate_type + decision_surface + decision_attrib]
outputs                [artifact | event | state_change]
success_slo            time + quality thresholds
observability          telemetry + eval harness references
```

This contract is enforced at edition-build time by `validate-edition.js`.

### 8.2 HITL gate taxonomy (Core Part 8.3)

Four gate types. Every edition uses these; no edition may add new types without amending Core.

| Gate | Description | Typical latency |
|---|---|---|
| **HITL** | Decision required, human-in-the-loop. Agent surfaces a decision-ready brief; human approves, modifies, or rejects. | Seconds to minutes |
| **ACK_ONLY** | No decision required, visibility only. Human acknowledges autonomous action after the fact. | Asynchronous |
| **ZERO_TOUCH** | Fully autonomous. Surfaces to a human only on exception or SLO breach. | No human latency |
| **ESCALATION** | Deferred to higher authority (legal, compliance, comms, exec). The local human initiates handoff rather than deciding. | Hours to days |

The v1.2 manifest system reuses this taxonomy unchanged. SemVer bumps map directly: PATCH → ZERO_TOUCH, MINOR → ACK_ONLY, MAJOR → HITL. This is deliberate — it keeps the number of gate categories small and keeps schema change governance consistent with agent/ORCH governance.

### 8.3 MCP tool convention

Every tool an agent can call follows the naming convention `mcp.<domain>.<capability>.<action>`. Domain codes are edition-specific (`mcp.store.*`, `mcp.property.*`, `mcp.well.*`). Action verbs are declarative: `resolve`, `detect`, `assemble`, `stage`. Tool contracts declare request/response JSON Schema, identity scope, idempotency, side effects, and observability (latency SLO + error taxonomy).

---

## Part 9 — Deployment Model (Wave-Based)

Core Part 12 defines the wave convention; editions populate the content. Every edition deploys in exactly four waves:

| Wave | Name | Entry posture | Typical economics |
|---|---|---|---|
| **W1** | Foundation | CMM-1 → CMM-2 | Targeted ROI from 2–3 high-blast-radius ORCHs |
| **W2** | Expansion | CMM-2 → CMM-3 | Broader agent fleet; W1 ROI funds W2 |
| **W3** | Platform | CMM-3 → CMM-4 | 20+ agents in production with HITL gates |
| **W4** | Adaptive | CMM-4 → CMM-5 | Self-optimizing fleet; cross-domain ORCHs |

Every wave is **self-funding**: the ROI of completing Wave N pays for starting Wave N+1. Edition-specific durations and economics go into the Part 12 wave tables for that edition. Exit criteria for each wave are measurable (e.g., "95th percentile time-to-decision under 30 seconds for ORCH-04," not "agents are running smoothly").

### 9.1 Commercial Maturity Model (CMM)

Five stages, industry-agnostic, referenced unchanged by every edition (Core Part 5):

| Stage | Data posture | Agent posture | Operations posture |
|---|---|---|---|
| **CMM-1** Foundations | ERP + core systems integrated; basic BI | No production agents | Reactive, manual exception handling |
| **CMM-2** Connected | Real-time unified fabric; API-first | Isolated ML models in production | Alerting on exceptions; dashboards primary |
| **CMM-3** Intelligent | Full canonical schemas in Gold; MLOps mature | Generative copilots; 1–3 agents | Detection automated; resolution mostly human |
| **CMM-4** Agentic | Schemas + ORCHs + MCP tool catalog; agent fleet | 20+ agents; HITL gates defined | Resolution mostly autonomous; human for judgment |
| **CMM-5** Adaptive | Continuous-learning schemas; drift monitoring native | Fleet self-optimizes; cross-domain ORCHs | Adaptive operations |

APEX's operating zone is CMM-4. Clients typically arrive at CMM-1 or CMM-2. W1 gets them to CMM-3; W2–W3 to CMM-4.

### 9.2 AI Journey Eras (contextual, not commercial)

Five eras, industry-agnostic (Core Part 4). Referenced unchanged by every edition. Provides the temporal context for where a client's existing AI investments fit:

| Era | Name | Window | Signature |
|---|---|---|---|
| ERA-01 | Automate | 2015–2020 | RPA, rules engines, BI dashboards |
| ERA-02 | Augment | 2020–2023 | ML in production; embedded analytics |
| ERA-03 | Generative | 2023–2025 | LLM copilots; generative content |
| ERA-04 | Agentic | 2025–2027 | Orchestrated agent fleets; HITL gates |
| ERA-05 | Adaptive | 2027+ | Self-learning fleets; cross-domain planning |

---

## Part 10 — Solution Stack

Every edition produces a ~50-row "Solution Stack" table — the flat, denormalized grid that binds every layer of the framework into one addressable structure. Each row declares: layer, domain, component name, component type (service / entity / agent / orch / tool / isv / experience), Microsoft service binding, ISV binding (optional), wave availability, CMM stage required, agent/tool/Gold-view references, and a one-paragraph description.

Row composition for a typical edition:

- ~7 infrastructure rows (L1–L4 services)
- ~4 schema-registry rows (MERML, SCML, CXML, MKTL for RC)
- ~4 Gold-view-category rows
- ~30+ agent rows (edition-defined count)
- ~12 ORCH rows (ORCH-01 through ORCH-12)
- Plus experience and ISV-binding rows

The Solution Stack is the document Account Teams hand to CTOs evaluating APEX. It is the single artifact that says "here is everything the edition does, bound to Microsoft services, by wave and by CMM stage." It is also the input to the render widgets described in Part 11.

---

## Part 11 — Design System and Reusable Widgets

Every edition site uses the same design system (Core Part 9). Editions may extend tokens (add one industry-accent color) but may not break theme behavior, typography, or component patterns.

- **Typography** — Fraunces (display), Instrument Sans (body), JetBrains Mono (code). Inter / Roboto / Arial are forbidden as primary.
- **Dark theme** is the default. Every site includes an inline theme-init script that reads `localStorage['apex-theme']`, falls back to `prefers-color-scheme`, and persists the toggle choice.
- **Semantic colors** are consistent across themes: teal = agent / autonomous / schema, amber = HITL / decision surface, crimson = critical severity, slate = low severity, gold = commercial outcome, indigo = platform foundation.
- **Layout** — max-width 1280px, 48px padding, sticky top nav, large Fraunces section numbers.

### 11.1 Shipped reusable widgets

Core ships a set of framework-agnostic widgets that every edition site consumes by feeding them edition-specific JSON. The widgets are pure functions of their input JSON — no industry logic is hard-coded:

| Widget | File | Consumes |
|---|---|---|
| Theme toggle | `/js/theme.js` | `localStorage['apex-theme']` |
| Navigation | `/js/navigation.js` | HTML structure |
| Solution Stack Chart | `/js/solution-stack.js` | `solution-stack.json` |
| ORCH Expander | `/js/orch-expander.js` | `orchestrations.json` |
| Wave Timeline | `/js/wave-timeline.js` | `waves.json` |
| CMM Filter | `/js/cmm-filter.js` | `cmm-stages.json` + edition content |
| Domain Tabs | `/js/domain-tabs.js` | `agents.json` grouped by domain |
| Architecture Diagram | `/js/arch-diagram.js` | `solution-stack.json` filtered |

Adding a new edition means shaping its JSON to these contracts. All rendering is inherited for free.

### 11.2 apex-validate HTML reports (v1.2)

The v1.2 validator reports render in the same design vocabulary: Fraunces / Instrument Sans, dark-default with toggle, teal PASS chip / amber WARN / crimson CRITICAL, JetBrains Mono for rule IDs and JSONPath locators. Reports are single-file static HTML — portable to PR comments, email attachments, and the edition site.

---

## Part 12 — The Tooling Surface (What Shipped in v1.2)

As of APEX Core v1.2 (2026-04-17), the following Core-owned tools are live:

### 12.1 `apex-validate` — dual-mode manifest validator

- **Author mode:** `apex-validate <edition-folder>` runs the L2 validator against the edition's `schemas.manifest.json`, produces `report.html` + `report.json`. Used in edition CI on every PR.
- **Fleet mode:** `apex-validate --fleet` reads the L3 fleet registry, resolves every pin against the discovered L2 manifests, produces a `fleet-report.html` with a drift matrix (rows = accounts, columns = schemas, colors by required gate).
- **Account-scoped:** `apex-validate --fleet --account <id>` drills into a single account.
- **CI mode:** `--ci` emits JSON to stdout and exits non-zero on any critical.

Rules enforced (14 today):
- `REQ-01..04` — required top-level fields.
- `REQ-01-PATTERN`, `REQ-03-SEMVER`, `REQ-04-COUNT` — pattern and count checks.
- `SCHEMA-CODE`, `SCHEMA-VERSION` — schema code regex and SemVer.
- `PK-EMPTY`, `GRAIN-MISSING`, `ENUM-LAYER` — entity shape.
- `VERSION-CHANGELOG-MISMATCH`, `BUMP-MISMATCH`, `DETAIL-MISSING`, `ENUM-BUMP`, `ENUM-GATE` — changelog integrity.
- `SHAPE-ROOT`, `SHAPE-SCHEMAS`, `SHAPE-ENTITIES`, `SHAPE-CHANGELOG` — defensive shape guards against malformed input.

### 12.2 `apex-sync` — tenant-side pull CLI

Four commands:

- `apex-sync status` — read-only 3-column table (Deployed / Pinned / Status).
- `apex-sync check` — silent CI gate; exits 1 on any drift.
- `apex-sync plan [--schema CODE]` — dry-run, prints the DDL operations that would execute.
- `apex-sync apply [--approve ticket://CHG-<n>]` — applies PATCH/MINOR automatically; refuses MAJOR without the approval token.

Environment-driven configuration: `APEX_DEPLOYED` and `APEX_PINNED` point to the tenant's L4 and the pulled bundle. The DDL driver is pluggable; the default is a no-op logger. A production driver wires Fabric Lakehouse DDL execution with tenant-local credentials (out of scope for Core; each engagement provides its own).

### 12.3 Release bundler — per-account signed bundles

`apex-fleet/tools/release-bundler.js` reads L3, filters to each account's entry, inlines the changelog entries from each edition's L2, and writes a signed bundle to `apex-fleet/bundles/<account_id>.json`. Signing is currently a stub (`signature: "SHA256:STUB"`); production signing is a follow-up hardening task.

### 12.4 `validate-edition` and `lint-compliance`

From earlier phases (Core v1.0 / v1.1):

- `validate-edition <edition-folder>` checks an edition against the Part 11 acceptance criteria.
- `lint-compliance <edition-folder>` scans every markdown, JSON, HTML, and JS file for forbidden Part 0 terminology. This is the compliance backstop Part 0 depends on.

---

## Part 13 — Reference Implementations

Every active edition ships at least one reference implementation — a "day-in-the-seat" narrative walkthrough that shows the agent fleet in action for a synthetic client. Reference implementations live at `apex-<code>/ref-impl/`. They are explicitly demo-ware: synthetic data, clearly fictional client names, meant to be shown in sales conversations and architecture reviews.

Registered reference implementations:

| Edition | Reference implementation | Status |
|---|---|---|
| RC | Store 100 Day-in-the-Shift | Built |
| TH | Property 201 Day-in-the-GM-Seat | Planned |
| HLS (PRV) | Memorial 4-West Day-in-the-Unit | Planned |
| HLS (LS) | Trial ATLAS-3 Day-in-Operations | Planned |
| TMT (TEL) | Carrier NOC Day-in-the-Console | Planned |
| TMT (MED) | Streaming Platform Operations Day | Planned |
| TMT (TEC) | SaaS Tenant Success Day | Planned |
| ER (OG) | Offshore Platform Charlie Day-in-OIM-Seat | Planned |
| ER (PU) | Control Center Gamma Day-in-Ops | Planned |
| ER (MN) | Mine Site Delta Day-in-Ops | Planned |
| ICE | Dealer Site Bravo Day-in-the-Service-Manager-Seat | Planned |

---

## Part 14 — Acceptance Criteria for New Editions

A new APEX edition is Core-conformant when:

1. Folder exists as `apex-<code>/` parallel to `apex-core/`.
2. Edition README declares its code, full name, and Core spec version referenced.
3. Edition defines 6–10 Forces of Change conforming to Core Part 3.
4. Edition references Core Parts 4 (Eras) and 5 (CMM) unchanged.
5. Edition defines 3–5 canonical schemas using Core Part 7 naming and entity template.
6. Every Silver-layer event entity uses the Core Part 7.4 canonical envelope unchanged.
7. Edition defines 12 orchestrations (ORCH-01 through ORCH-12) with Core Part 8.2 contracts.
8. Edition defines its MCP tool catalog using Core Part 8.4 naming.
9. Edition site uses Core design system (Part 9) with at most one accent-token addition.
10. Edition site consumes Core reusable widgets (Part 10); does not reimplement them.
11. Edition passes Part 0 compliance check (no forbidden terminology anywhere).
12. Edition Solution Stack has ≥50 rows conforming to the Core Part 13 shape.
13. Edition defines at least one reference implementation under `apex-<code>/ref-impl/`.
14. **(v1.2)** Edition includes `schemas.manifest.json` conforming to the Core v1.2 manifest contract.
15. **(v1.2)** Every schema declares `version`, `changelog`, and `envelope_required`.
16. **(v1.2)** `apex-validate` exits 0 or 1 (no criticals) against the edition.

---

## Part 15 — What APEX Is Not Doing (Yet)

Explicit non-goals, flagged so Account Teams do not over-promise:

- **No runtime that Deloitte hosts.** Clients deploy on their own Azure tenant. DMTSP has engagement visibility, not operational control.
- **No agent versioning.** The v1.2 manifest system versions schemas only. Agents, ORCHs, and Solution Stack rows follow the same pattern when they adopt it — but they have not adopted it yet. This is deliberate: schemas are the hardest-to-reverse dependency, so versioning them first gives the most leverage.
- **No cross-client benchmark dashboard.** The fleet registry records intent and heartbeats only. Building a "which client is performing best at ORCH-04" dashboard would require client-identifiable telemetry, which violates Core Part 6 Independence posture. Any benchmark that ships must be anonymous-by-construction.
- **No automated ROI attribution.** The wave model declares expected economics per wave, but capturing realized economics requires client financial integration on a case-by-case basis. That belongs in each engagement's scope, not the framework.
- **No signed release bundles yet.** Release bundler currently uses a stub signature. Real signing via Azure Key Vault or sigstore is a hardening follow-up.
- **No Fabric DDL driver.** `apex-sync apply` uses a no-op driver by default. Each client engagement wires a Fabric driver with tenant-local credentials. The driver interface is stable; the implementation is engagement-specific.

---

## Part 16 — How Engagements Use APEX

The typical DMTSP engagement lifecycle with APEX:

1. **Select the edition.** Client is retail → APEX-RC. Client is a multi-industry conglomerate → combination (APEX-RC + APEX-TH). The edition choice is part of scoping.
2. **Assess against CMM.** Where is the client today (CMM-1? CMM-2?)? This determines the starting wave.
3. **Walk the Solution Stack.** Hand the client's CTO the ~50-row Solution Stack for their edition. This is the single artifact that names everything APEX will deploy, bound to Microsoft services.
4. **Scope Wave 1.** Pick 2–3 high-blast-radius ORCHs. Define exit criteria and expected economics for W1.
5. **Populate L1 + L2 manifests.** Edition's `schemas.manifest.json` is already populated (Core maintainers handle this). Client's L3 entry is added via a PR to the fleet registry — edition, Core version, pinned schemas (initial GA), wave stage, quiet window, auto-upgrade policy.
6. **Build.** Engagement teams implement the W1 ORCHs on the client's Azure tenant using the edition's agent catalog and the Core reusable widgets for any client-facing surfaces.
7. **Validate continuously.** `apex-validate apex-<code>` runs in CI on every PR. `apex-validate --fleet` runs on every fleet-registry merge. The Account Team dashboard is rebuilt on each merge.
8. **Deploy through `apex-sync`.** The tenant's nightly pipeline pulls its signed bundle and applies PATCH/MINOR automatically, surfaces MAJOR to the client's change-approval process.
9. **Measure wave exit.** When W1 exit criteria are met and the economics are proven, proceed to W2. If not, stay in W1 until the exit criteria are satisfied — do not advance waves on schedule alone.
10. **Repeat for W2 → W3 → W4.**

---

## Part 17 — Governance

### 17.1 Core changes

Core changes are rare. Every Core change is a formal amendment document (see `apex-core-v1.1-amendment.md`, `apex-core-v1.2-amendment.md`). Amendments follow a two-week SteerCo review cycle. MAJOR contract bumps trigger a migration window; editions have until the window deadline to conform. MINOR contract bumps are adopted at each edition's own pace.

### 17.2 Edition changes

Edition changes happen on edition cadence — typically every 2–6 weeks. Each edition has its own maintainers and its own CHANGELOG. Edition changes do not require SteerCo approval unless they change something Core-owned (in which case they are a Core amendment, not an edition change).

### 17.3 Fleet changes

Fleet-registry changes (pinning an account to a new schema version, onboarding a new account, changing an account's upgrade policy) are handled by Account Teams via pull request against the `apex-fleet/` repo. Each PR requires at least one reviewer from the Account Team plus one from the edition maintainers (to confirm the pin is valid).

### 17.4 When things conflict

When editions disagree with Core, **Core wins**. An edition that wants a new gate type, a new ORCH numbering, a new event-envelope field, or a new HITL taxonomy must propose a Core amendment, not a silent edition override. The `lint-compliance` and `validate-edition` tools catch silent overrides.

---

## Part 18 — Glossary

- **APEX** — Agentic Platform for Enterprise eXecution. The framework.
- **Core** — APEX Core. The industry-agnostic parent spec.
- **Edition** — An industry-specific child spec (RC, TH, HLS, TMT, ER, ICE, FS, PS).
- **Sub-variant** — A further-specialized dialect within an edition (e.g., HLS-PRV = provider, HLS-LS = life sciences). Formal or informal.
- **Fleet** — The set of client accounts that have adopted an APEX edition. Managed via L3 fleet registry.
- **L1 / L2 / L3 / L4** — The four layers of the v1.2 manifest model (contract / edition catalog / fleet registry / tenant deployed).
- **MERML / SCML / CXML / MKTL / HOSML / REVML ...** — Schema codes. 4–5 uppercase letters, suffix `L` or `ML`.
- **ORCH-NN** — Canonical orchestration, numbered ORCH-01 through ORCH-12. Positional slot only.
- **HITL / ACK_ONLY / ZERO_TOUCH / ESCALATION** — The four gate types. See Core Part 8.3.
- **CMM-1..5** — Commercial Maturity Model stages. APEX's operating zone is CMM-4.
- **ERA-01..05** — AI Journey Eras. APEX's operating zone is ERA-04 (Agentic).
- **W1..W4** — The four deployment waves. Each self-funding.
- **DMTSP** — Deloitte's Microsoft practice. Builds APEX, delivers engagements, maintains editions.
- **Independence posture** — The non-negotiable rule that client-tenant data stays on the client's tenant; no Deloitte-side retention of client-identifiable data.
- **Event envelope** — The immutable Silver-layer event shape shared across all editions (Core Part 7.4).
- **Gold view** — Business-ready denormalized view that agents and ORCHs contract against.
- **GitOps pull** — Distribution pattern used by the v1.2 manifest system. Client tenants pull signed bundles from a release feed; Deloitte never pushes to tenants.

---

**End of APEX Solution Overview — 2026-04-17**

*For the full Core specification, read `apex-core-build-spec.md`. For the v1.2 manifest system design, read `docs/plans/2026-04-17-schema-versioning-manifest-design.md`.*
