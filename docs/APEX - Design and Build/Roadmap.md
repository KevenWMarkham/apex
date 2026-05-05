# APEX Roadmap

**Source:** `APEX_Design.md`
**Date:** 2026-04-23 (v1.2 — Scenario Library + Wave Ribbon + design-system artifacts completed)
**Purpose:** Backlog of work derived from the APEX Framework Design. Items are grouped into **Completed** (already delivered in the repository and documentation set) and **Planned** (designed but not yet built).

**Backlog-item ID convention:**
- `BL.C.NN` — Completed backlog item
- `BL.P.NN` — Planned backlog item
- Each item references the design section it implements (e.g., `§3.3`).

---

## 1. Completed Backlog (BL.C.*)

### 1.1 — Core Contract & Tools (L1)

- [x] **BL.C.01** — `apex-core` build spec authored (`apex-core-build-spec.md`) — §3.1
- [x] **BL.C.02** — `apex-core` v1.1 amendment (`apex-core-v1.1-amendment.md`) — §3.3
- [x] **BL.C.03** — `apex-core` v1.2 amendment (`apex-core-v1.2-amendment.md`) — §3.3
- [x] **BL.C.04** — Schema-versioning conventions (`apex-core/conventions/schema-versioning.md`) — §3.3
- [x] **BL.C.05** — Schema manifest contract JSON (`apex-core/data/schema-manifest-contract.json`) — §5.6
- [x] **BL.C.06** — `classify-bump` tool + tests — §3.3
- [x] **BL.C.07** — `validate-manifest` tool + tests — §3
- [x] **BL.C.08** — `validate-practice` tool + tests — §3
- [x] **BL.C.09** — `validate-fleet` tool + tests — §3
- [x] **BL.C.10** — `apex-sync` tool + tests — §3.2
- [x] **BL.C.11** — `apex-validate` tool + tests — §3
- [x] **BL.C.12** — `ddl-driver` tool — §5.6
- [x] **BL.C.13** — `release-bundler` tool + tests — §3.2
- [x] **BL.C.14** — `render-html` + `report` tooling — §5.6
- [x] **BL.C.15** — Fleet release bundler (`apex-fleet/tools/release-bundler.js`) — §3.2

### 1.2 — Per-Practice Build Specs (L3)

- [x] **BL.C.16** — RC build spec v2 (`apex-rc-build-spec-v2.md`) — §15
- [x] **BL.C.17** — HLS build spec — §15
- [x] **BL.C.18** — ER build spec — §15
- [x] **BL.C.19** — AXLE / ICE build spec (`apex-ice-build-spec.md`) — §15
- [x] **BL.C.20** — TMT build spec — §15
- [x] **BL.C.21** — TH build spec — §15

### 1.3 — RC Anchor Assets

- [x] **BL.C.22** — RC schemas manifest bootstrap (`apex-rc/data/schemas.manifest.json`) — §5.2
- [x] **BL.C.23** — RC report (`report.html`, `report.json`) — §5.6

### 1.4 — Published Documentation

- [x] **BL.C.24** — Professional APEX book (Wrox-style HTML) — reference
- [x] **BL.C.25** — Professional APEX Sellers Guide (HTML) — reference
- [x] **BL.C.26** — Developer-guide chapters 01–07 (Fabric layering, Medallion/SOR, MCP servers, Agent lifecycle, Observability/Security, Testing topology, Service catalog) — §4, §6, §7, §8, §11
- [x] **BL.C.27** — APEX Design reference (`APEX_Design.md`) — this document's source
- [x] **BL.C.28** — Store 100 facilitator guide (`APEX-Store-100-facilitator-guide.*`) — §18.1
- [x] **BL.C.29** — Comprehensive solutions reference (`APEX-comprehensive-solutions-reference.*`) — §15
- [x] **BL.C.30** — Solution overview (`APEX-solution-overview.*`) — §1
- [x] **BL.C.30a** — APEX Stacked Architecture Narrated HTML — 11-tab cinematic (Overview, Foundation, Data Plane, Schemas, Standards, Reasoning, Runtime, Context, Services, Chains, Practices) with Web Speech API narration decks — §20
- [x] **BL.C.30b** — Sellers Guide Runtime Addendum (DOCX + PDF) — pocket talking points for Orchestration / HITL / LEDGER / Audit — §21.1
- [x] **BL.C.30c** — APEX acronym cinematic band + 12-scene Overview narration deck — §20.3
- [x] **BL.C.30d** — LEDGER feedback loop visualization — §20.4 (layer 10)
- [x] **BL.C.30e** — Runtime plane deep-dive visualization — §20.2 tab 07

### 1.5 — Plan & Design Docs

- [x] **BL.C.31** — Schema-versioning manifest design + implementation plans — §3.3
- [x] **BL.C.32** — RC agent catalog design — §15
- [x] **BL.C.33** — APEX MCP tools Appendix I design — §7, Appendix F
- [x] **BL.C.34** — APEX schemas Appendix H design — Appendix A
- [x] **BL.C.35** — Purview Appendix K design — §14
- [x] **BL.C.36** — Orchestration deep-dive & catalog design — §10
- [x] **BL.C.37** — Fabric chapter deep-dive design — §12
- [x] **BL.C.38** — AXLE vs APEX AXLEML design — §5.2, §15
- [x] **BL.C.39** — Developer implementation guide design + draft — §8, §11
- [x] **BL.C.40** — Sellers guide design — reference
- [x] **BL.C.41** — Professional APEX book design — reference
- [x] **BL.C.42** — Store 100 repositioning design — §18.1

### 1.5a — Scenario Library, Wave Ribbon & Design System (Sprint 27)

- [x] **BL.C.42a** — APEX Scenario Library v1: 35 featured scenarios across 7 Practices (5 per Practice) with full Scenario → Solution → Use Case → Service → Persona → KPI chains — §19.2
- [x] **BL.C.42b** — Scenario Library browsable catalog: 723 compact scenario rows (100+ per Practice) embedded as `APEX_SCENARIO_LIBRARY` JS constant (~106 KB JSON) — §19.2
- [x] **BL.C.42c** — Scenario Library modal dialog: native `<dialog>` element with alphabetical sort + real-time filter + Esc-to-close + backdrop blur — §19.2
- [x] **BL.C.42d** — Per-practice browse-all CTA buttons with banner-color-aware hover states — §19.2, §22.2
- [x] **BL.C.42e** — Wave Ribbon pattern (W1 Foundation / W2 Pilot / W3 Scale-&-Fuse) for all 35 featured scenarios; three-column layout with sky/gold/amber rails and "you are here" W2 marker — §19.3
- [x] **BL.C.42f** — Wave Ribbon authored content for 35 scenarios (W1 prerequisites + W2 pilot scope + W3 enterprise + fusion-partner references) — §19.4
- [x] **BL.C.42g** — Per-practice color semantics (RC amber · HLS crimson · ER gold · AXLE teal · TMT violet · TH sky · ICE ember) codified in CSS tokens across all artifacts — §22.2
- [x] **BL.C.42h** — Universal color semantics (amber=HITL · teal=agent/autonomous · gold=outcomes · crimson=critical · sky=data · violet=schema · ember=identity) — §22.2
- [x] **BL.C.42i** — Typography system (Fraunces display · IBM Plex Sans body · JetBrains Mono monospace) enforced across visual artifacts — §22.1
- [x] **BL.C.42j** — Dark-first + warm-paper-light theme toggle across cinematic artifacts — §22.3
- [x] **BL.C.42k** — Independence-language linguistic compliance check (no "partner/alliance") integrated into pre-publish pipeline — §22.4
- [x] **BL.C.42l** — Collapsible `<details>`/`<summary>` chain cards with KPI preview chips in collapsed state (70 preview chips across 35 cards) — §19.2
- [x] **BL.C.42m** — Chain-card scenario body with color-coded row labels (r-scenario amber · r-solution teal · r-usecase sky · r-service violet · r-persona crimson · r-kpi gold) — §19.2

### 1.6 — Build Scripts

- [x] **BL.C.43** — `build-docx.cjs`, `build-facilitator-guide.cjs`, `build-reference-docx.cjs` — doc generators
- [x] **BL.C.44** — `build-professional-apex.cjs`, `build-sellers-guide.cjs` — book/guide generators
- [x] **BL.C.45** — `build-agent-catalog.cjs`, `build-dev-guide-docx.cjs` — catalog/guide generators
- [x] **BL.C.46** — `build-solution-stack.py` — solution-stack chart generator

---

## 2. Planned Backlog (BL.P.*)

### 2.1 — L1 Contract — Remaining Manifest Schemas

- [x] **BL.P.01** — Event manifest schema + validator — §10.4 *(Sprint 1 — Pydantic v2 port)*
- [x] **BL.P.02** — Orchestration manifest schema + validator — §10.4 *(Sprint 1)*
- [x] **BL.P.03** — Agent manifest schema + validator — §8, §10.4 *(Sprint 1)*
- [x] **BL.P.04** — Tenant manifest schema + validator — §3.4 *(Sprint 1)*
- [x] **BL.P.05** — Policy manifest schema (HITL / DLP / gate) + validator — §9, §14 *(Sprint 1)*
- [x] **BL.P.06** — Service manifest schema + validator — §15, Appendix B *(Sprint 1)*
- [x] **BL.P.07** — Canonical envelope enforcement (`event_id`, `event_ts`, `entity_id`, `source_system`, `source_system_ts`) — §5.3 *(Sprint 1)*

### 2.2 — Canonical Schemas (L3)

- [x] **BL.P.08** — SCML complete (Supply Chain — SKU, Location, Lot, Shipment, Supplier, Item) — §5.2 *(Sprint 2 — `apex-scml` with GS1 GTIN/SSCC/GLN bindings)*
- [x] **BL.P.09** — MERML complete (Merchandising — Category, Price, Promotion, Markdown) — §5.2 *(Sprint 2 — `apex-merml`)*
- [x] **BL.P.10** — CXML complete (Customer — Customer, Loyalty, Interaction, Order) — §5.2 *(Sprint 2 — `apex-cxml` with tokenizer hooks)*
- [x] **BL.P.11** — HLSCML / PatientML (Patient, Practitioner, Encounter, Observation, DiagnosticReport, MedicationRequest) — §5.2 *(Sprint 3 Phase 2 — `apex-hlscml` with FHIR Pattern-C round-trip translators + PHI tokenisation hooks)*
- [x] **BL.P.12** — ClaimML (ClaimHeader + ClaimLine with CPT/HCPCS) — §5.2 *(Sprint 3 Phase 2)*
- [x] **BL.P.13** — StudyML (Study + StudyEnrollment + AdverseEvent; CDISC-aligned) — §5.2 *(Sprint 3 Phase 2)*
- [x] **BL.P.14** — ERCML (Meter, MeterReading, GridEvent, Asset, WorkOrder, ReliabilityRecord; CIM + ISO 14224) — §5.2 *(Sprint 3 Phase 2 — UOGML/P&UML/MiningML O&G extensions deferred)*
- [x] **BL.P.15** — AXLECML (Equipment, WorkCenter, ProductionEvent, QualityResult, Genealogy, BoM, J1939Signal, ReliabilityRecord; ISA-95 + J1939 + ISO 14224) — §5.2 *(Sprint 3 Phase 2)*
- [x] **BL.P.16** — TELML (TelcoCustomer, ProductOffering, Product, Service, NetworkResource, BillingAccount; TM Forum SID) — §5.2 *(Sprint 3 Phase 2 — ContentSafetyML deferred)*
- [x] **BL.P.17** — THML (Traveler, Reservation, Itinerary, Segment, LoyaltyAccount, Disruption; OpenTravel + IATA NDC) — §5.2 *(Sprint 3 Phase 2 — package named `apex-thml`)*
- [x] **BL.P.18** — ICEML (IceEquipment, TelemetryReading, ServiceEvent, MaintenanceRecord, FleetMember; SAE J1939 + AEMP 2.0 + ISO 14224) — §5.2 *(Sprint 3 Phase 2 — package named `apex-iceml`)*
- [x] **BL.P.19** — Cross-standard translators shipped alongside consuming entities: GS1 ↔ Schema.org (Sprint 2); FHIR ↔ HLSCML + HL7 v2/CDA stubs (Phase 2); CIM ↔ ERCML (Phase 2); ISA-95 → AXLECML + J1939 → AXLECML (Phase 2); SID → TELML (Phase 2); OTA → THML (Phase 2); AEMP → ICEML (Phase 2) — §5.4

### 2.3 — Medallion Architecture

- [x] **BL.P.20** — Bronze landing template: Mirrored Database — §6.2.1 *(Sprint 4 — `notebooks/bronze/mirrored_database.py`)*
- [x] **BL.P.21** — Bronze landing template: Eventstream / Eventhouse — §6.2.2 *(Sprint 4 — `notebooks/bronze/eventstream.py` with structured-streaming pattern)*
- [x] **BL.P.22** — Bronze landing template: Data Pipeline (batch) — §6.2.3 *(Sprint 4 — `notebooks/bronze/data_pipeline.py`)*
- [x] **BL.P.23** — Bronze landing template: Dataflow Gen2 (REST/SaaS) — §6.2.4 *(Sprint 4 — `notebooks/bronze/dataflow_gen2.py` with watermark helpers)*
- [x] **BL.P.24** — Bronze landing template: Custom Endpoint (webhook) — §6.2.5 *(Sprint 4 — `notebooks/bronze/custom_endpoint.py` FastAPI app + HMAC verify + dead-letter)*
- [x] **BL.P.25** — Bronze retention & partitioning policies (Purview-managed) — §6.3 *(Sprint 4 — `apex-medallion.bronze.retention` + `partitioning` + `dead_letter` + `config` + `schema`)*
- [x] **BL.P.26** — Silver transform notebooks per Practice (canonicalize + classify) — §6.4 *(Sprint 5 — `notebooks/silver/transform_template.py` + `apex-medallion.silver.transform` helpers; HLSCML wired end-to-end)*
- [x] **BL.P.27** — Tokenization service at Bronze→Silver boundary — §6.4.1 *(Sprint 5 — `apex-tokenizer` package: `TokenService` + HMAC-SHA256 determinism + `InMemoryVaultBackend` + `DeltaVaultBackend` stub + `vault_ddl()` + `tokenize_classified_fields` walker; HLSCML `_tokenize.py` now delegates to the real service. `tokenizer-mcp` server itself lands in Sprint 7.)*
- [x] **BL.P.28** — SCD Type 2 history framework — §6.4 *(Sprint 5 — `apex-medallion.silver.scd2` with `Scd2Config` + `compute_row_hash` + `next_scd2_fields` + `add_scd2_fields_to_instance`)*
- [x] **BL.P.29** — Gold materialization — Direct Lake semantic models per Practice — §6.5 *(Sprint 6 — `apex-medallion.gold.direct_lake` `SemanticModelSpec` + `render_tmdl()` + `notebooks/gold/direct_lake.py` RC anchor)*
- [x] **BL.P.30** — Gold materialization — Warehouse T-SQL views per Practice — §6.5 *(Sprint 6 — `generate_warehouse_view()` with `view_definition_sha()` + `notebooks/gold/warehouse_views.py`)*
- [x] **BL.P.31** — Gold materialization — real-time KQL functions (Eventhouse) — §6.5 *(Sprint 6 — `generate_kql_function()` + `notebooks/gold/kql_functions.py`)*
- [x] **BL.P.32** — Pre-measure library (PySpark, Silver→Gold) per Practice — §6.6 *(Sprint 6 — `apex-medallion.gold.rc_measures` with effective_margin_pct / stock_days_remaining / time_since_last_event_seconds)*
- [x] **BL.P.33** — Post-measure library (DAX / T-SQL / KQL) per Practice — §6.6 *(Sprint 6 — period_over_period_pct (DAX) / rolling_avg_14_day (T-SQL) / events_last_15_min (KQL) in rc_measures; `MeasureRegistry` governs per-language selection)*
- [x] **BL.P.34** — Drift detector (Fabric schema vs Pydantic model) — §5.6 *(Sprint 5 — `apex-medallion.silver.drift.detect_drift()` + `DriftReport` + `expected_columns()` with Delta-type alias normalisation)*

### 2.4 — MCP Servers

- [x] **BL.P.35** — Domain MCP: `scml-mcp` (get_sku_by_key · list_skus_by_supplier · list_shipments_by_destination; scope `practice:rc`) — §7.2 *(Sprint 8)*
- [x] **BL.P.36** — Domain MCP: `merml-mcp` (get_current_price · list_active_promotions · list_recent_markdowns) — §7.2 *(Sprint 8)*
- [x] **BL.P.37** — Domain MCP: `cxml-mcp` (get_customer · list_orders · list_interactions; PII+PCI propagation) — §7.2 *(Sprint 8)*
- [x] **BL.P.38** — Domain MCP: `hlscml-mcp` (get_patient · list_observations · list_medications; PHI-segregated, scope `practice:hls`) — §7.2 *(Sprint 8)*
- [x] **BL.P.39** — Domain MCP: `ercml-mcp` (get_meter · list_readings · list_grid_events_by_type) — §7.2 *(Sprint 8)*
- [x] **BL.P.40** — Domain MCP: `axlecml-mcp` (get_equipment · list_production_events · list_quality_results) — §7.2 *(Sprint 8)*
- [x] **BL.P.41** — Utility MCP: `fabric-mcp` (OneLake / workspace reads) — §7.2 *(Sprint 7 — 3 tools: get_entity_by_key, query_gold_view, list_classifications; InMemoryFabricBackend)*
- [x] **BL.P.42** — Utility MCP: `policy-mcp` (rule / compliance eval) — §7.2 *(Sprint 7 — 3 tools: evaluate_policy, check_compliance, classify_bump; delegates to apex-core)*
- [x] **BL.P.43** — Utility MCP: `telemetry-mcp` (trace / log / observability) — §7.2 *(Sprint 7 — 3 tools: emit_trace, log_event, query_latency_percentile)*
- [x] **BL.P.44** — Utility MCP: `approvals-mcp` (HITL workflow integration) — §7.2, §9 *(Sprint 7 — 3 tools: request_approval, get_approval_status, record_decision; conflict detection on double-record)*
- [x] **BL.P.45** — Utility MCP: `ledger-mcp` (audit-row persistence) — §7.2, §11 *(Sprint 7 — 3 tools: append_audit_row, fetch_row_by_trace, verify_row_signature; HMAC signing + tamper detection)*
- [x] **BL.P.46** — External MCP: `fda-mcp` (FDA recall / adverse-event feeds) — §7.2 *(Sprint 9 — list_recalls_by_date · get_recall_detail · search_adverse_events; InMemoryFdaBackend stub)*
- [x] **BL.P.47** — External MCP: `ferc-mcp` (FERC grid / compliance) — §7.2 *(Sprint 9 — list_enforcement_actions · get_interconnection_queue_status · list_compliance_filings)*
- [x] **BL.P.48** — External MCP: `edi-mcp` (EDI message processing) — §7.2 *(Sprint 9 — parse_850 · parse_856 · emit_810 stubs; full X12 parser in Sprint 15 BL.P.155)*
- [x] **BL.P.49** — External MCP: `vendor-portal-mcp` — §7.2 *(Sprint 9 — get_vendor_status · list_vendor_orders · get_vendor_compliance_score; compliance carries TRADE_SECRET classification)*
- [x] **BL.P.50** — External MCP: `pharma-recall-mcp` — §7.2 *(Sprint 9 — list_pharma_recalls · search_recalls_by_ndc (NDC-regex validated) · get_recall_detail)*
- [x] **BL.P.51** — MCP tool-contract generator (inputSchema, outputSchema, SLO, version) — §7.3 *(Sprint 7 — `mcp-common.contract.ToolContract` + `SloSpec` frozen Pydantic models; every utility server exports its CONTRACTS list)*
- [x] **BL.P.52** — MCP trace instrumentation (operation_id, classification_applied) — §7.3 *(Sprint 7 — `mcp-common.trace` with `ToolTraceRecord`, `traced_call()` context-manager, module-level sink hook)*

### 2.5 — Identity, Scope, & Visibility Lattice

- [x] **BL.P.53** — Entra managed-identity provisioning per agent — §8.1 *(Sprint 10 — `apex-identity.provisioning` with `EntraProvisioningProvider` protocol + `MockEntraProvisioningProvider`; deterministic OID derivation; register/lookup/revoke)*
- [x] **BL.P.54** — Scope evaluator (tenant × practice × persona × classification × row filter) — §8.2 *(Sprint 10 — `ScopeResolver` composes identity + `AgentRole` → `ScopeContext`; fails closed on unknown agent / missing role / tenant mismatch)*
- [x] **BL.P.55** — Visibility-lattice runtime (RLS + OLS + per-agent scope) — §8.3 *(Sprint 10 — `evaluate_visibility()` walks Pydantic classification annotations + applies row filters; `VisibilityDecision` structured result)*
- [x] **BL.P.56** — Agent-safe view generator (classification-aware masking) — §8.4 *(Sprint 10 — `apply_agent_safe_view()` returns masked `model_copy` with non-visible fields → None, or None if row filters reject the row)*
- [x] **BL.P.57** — Response signing (agent service principal) — §8.4 *(Sprint 10 — `sign_response()` / `verify_response()` HMAC-SHA256 keyed on (agent_id, tenant_id); Sprint 13 upgrades to RSA + Key Vault)*

### 2.6 — Agent Catalogs

- [ ] **BL.P.58** — RC agent catalog (40–50 agents) — §15
- [ ] **BL.P.59** — HLS agent catalog (40–50 agents) — §15
- [ ] **BL.P.60** — ER agent catalog (40–50 agents) — §15
- [ ] **BL.P.61** — AXLE agent catalog (40–50 agents) — §15
- [ ] **BL.P.62** — TMT agent catalog (40–50 agents) — §15
- [ ] **BL.P.63** — TH agent catalog (40–50 agents) — §15
- [ ] **BL.P.64** — ICE agent catalog (40–50 agents) — §15

### 2.7 — Orchestration Framework

- [x] **BL.P.65** — 47 orchestration archetypes library — §10.3 *(Sprint 11 — `apex-orchestrator/archetypes/catalog.py`, 10 impl + 37 manifest-only)*
- [x] **BL.P.66** — Sequential / Parallel / Hierarchical / Feedback-loop primitives — §10.2 *(Sprint 11 — `apex-orchestrator/primitives/`)*
- [x] **BL.P.67** — Orchestration manifest runtime (version stamps, gate placement) — §10.4 *(Sprint 11 — `apex-orchestrator/manifest.py` + `runtime.py`, three-version rule enforced)*
- [ ] **BL.P.68** — Practice-specific orchestrations (15–25 per Practice) — §10.3 *(Sprint 11 — reference Cold Chain Response shipped; per-Practice libraries in Sprint 18)*

### 2.8 — HITL Gate Runtime

- [x] **BL.P.69** — Gate-kind runtime: ZERO_TOUCH — §9.1 *(Sprint 11 — `gates/kinds.py::ZeroTouchGate`)*
- [x] **BL.P.70** — Gate-kind runtime: ACK_ONLY — §9.1 *(Sprint 11 — `gates/kinds.py::AckOnlyGate`)*
- [x] **BL.P.71** — Gate-kind runtime: HITL (present + wait) — §9.1 *(Sprint 11 — `gates/kinds.py::HitlGate` + pausable `Orchestrator.run`/`resume`)*
- [x] **BL.P.72** — Gate-kind runtime: ESCALATION — §9.1 *(Sprint 11 — `gates/kinds.py::EscalationGate`)*
- [x] **BL.P.73** — Gate variants (hard / soft / policy / escalation) — §9.2 *(Sprint 11 — `GateVariant` resolver in `gates/resolver.py`)*
- [x] **BL.P.74** — Teams card integration for HITL presentation — §9.3 *(Sprint 11 — `integrations/teams.py::build_adaptive_card`)*
- [x] **BL.P.75** — Copilot Studio action integration for HITL — §9.3 *(Sprint 11 — `integrations/copilot_studio.py::copilot_studio_skill_stub`)*
- [x] **BL.P.76** — Tenant policy tuning framework (2-week observation window) — §9.4 *(Sprint 11 — `tuning.py::TuningStore`, auto-rollback on reversal/escalation)*

### 2.9 — Decision Audit Row

- [x] **BL.P.77** — 14-field audit-row schema + immutable append-only store — §11.2 *(Sprint 12 — `apex-audit/row.py::AuditRow`, `store.py::AuditStore`, retrofitted into `ledger-mcp`)*
- [x] **BL.P.78** — Trace-ID discipline runtime (reject emissions missing `trace_id`) — §11.6 *(Sprint 12 — `apex-audit/trace.py::require_trace_id` + `TraceMissingError`; enforced at model + store + MCP boundaries)*
- [x] **BL.P.79** — Three-version rule enforcement (`manifest_version` + `policy_version` + `prompt_version`) — §11.7 *(Sprint 12 — `apex-audit/versions.py::VersionStamps` + `stamp_versions`; emitter stamps at pre-invocation; `resolve_decision` auditor tool)*
- [x] **BL.P.80** — Reasoning-trace capture with DLP scrub — §11.4 *(Sprint 12 — `apex-audit/reasoning.py` + `RestrictedTraceStore`; raw CoT routed to restricted store, structured reasoning DLP-scrubbed before content-hashing)*
- [x] **BL.P.81** — Orchestration composite-row emission — §11.5 *(Sprint 12 — `apex-audit/composite.py::OrchestrationCompositeRow` + `AuditStore.append_composite`)*
- [x] **BL.P.82** — Content-addressed input/output hash store — §11.3 *(Sprint 12 — `apex-audit/content_store.py::ContentAddressedStore` + `content_hash` sha256)*
- [x] **BL.P.83** — Downstream-effect cross-reference — §11.3 *(Sprint 12 — `AuditRow.downstream_effect_ref` field; `trace_id` threads the parent + action rows)*
- [x] **BL.P.84** — Row signing + hashing (WORM) — §11.3 *(Sprint 12 — `apex-audit/signing.py::sign_row`/`verify_row` HMAC-SHA256; `AppendOnlyViolationError` blocks overwrites)*

### 2.10 — Purview Trust Architecture

- [ ] **BL.P.85** — Classification registration pipeline (YAML → Purview) — §14.1
- [ ] **BL.P.86** — Lineage capture: SOR → Bronze → Silver → Gold → MCP tool → Agent → Audit row — §14.2
- [ ] **BL.P.87** — DLP policies (label-based redaction across surfaces) — §14.1
- [ ] **BL.P.88** — WORM retention policies (7 y default, 10 y HLS, permanent legal-hold) — §6.3, §14.1
- [ ] **BL.P.89** — Unified Catalog business-glossary registration — §14.1
- [ ] **BL.P.90** — Classification propagation chain (Silver → Gold → semantic model → Copilot → agent output) — §14.3

### 2.11 — Fabric Capacity & Provisioning

- [ ] **BL.P.91** — Terraform module for F-SKU capacity provisioning — §12.1
- [ ] **BL.P.92** — OneLake workspace provisioning via Fabric REST API — §12.1
- [ ] **BL.P.93** — Capacity-pattern templates (single / dev-prod split / per-workload isolation) — §12.3
- [ ] **BL.P.94** — OneLake shortcut provisioning (ADLS / S3 / GCS / Dataverse) — §12.7

### 2.12 — SOR Integration Adapters

- [ ] **BL.P.95** — Epic Clarity adapter — §13.6
- [ ] **BL.P.96** — SAP S/4HANA adapter — §13.6
- [ ] **BL.P.97** — Salesforce adapter — §13.6
- [ ] **BL.P.98** — Manhattan Active WMS adapter — §13.6
- [ ] **BL.P.99** — Workday HCM adapter — §13.6
- [ ] **BL.P.100** — ServiceNow adapter — §13.6
- [ ] **BL.P.101** — OSIsoft / AVEVA PI Historian adapter — §13.6
- [ ] **BL.P.102** — GE Proficy / AVEVA Wonderware adapter — §13.6
- [ ] **BL.P.103** — Legacy AS/400 / DB2 adapter — §13.6
- [ ] **BL.P.104** — Adobe / Google Analytics adapter — §13.6
- [ ] **BL.P.105** — Salesforce Marketing Cloud adapter — §13.6
- [ ] **BL.P.106** — HL7 v2 / FHIR feed adapter — §13.6
- [ ] **BL.P.107** — SAP Ariba / Coupa adapter — §13.6
- [ ] **BL.P.108** — Oracle EBS / Fusion adapter — §13.6
- [ ] **BL.P.109** — Snowflake / Databricks interop adapter — §13.6

### 2.13 — Service Catalogs

- [ ] **BL.P.110** — RC service catalog (45+ productized services with personas, KPIs, SLOs) — §15, Appendix B
- [ ] **BL.P.111** — HLS service catalog — §15
- [ ] **BL.P.112** — ER service catalog — §15
- [ ] **BL.P.113** — AXLE service catalog — §15
- [ ] **BL.P.114** — TMT service catalog — §15
- [ ] **BL.P.115** — TH service catalog — §15
- [ ] **BL.P.116** — ICE service catalog — §15

### 2.14 — Reference Deployments

- [ ] **BL.P.117** — Big Box Store reference deployment (RC) — §18.1
- [ ] **BL.P.118** — Hospital reference deployment (HLS) — §18.1
- [ ] **BL.P.119** — Utility reference deployment (ER) — §18.1
- [ ] **BL.P.120** — Plant reference deployment (AXLE) — §18.1
- [ ] **BL.P.121** — Airline reference deployment (TH) — §18.1

### 2.15 — Registries, Playbooks & Appendices

- [ ] **BL.P.122** — KPI master registry (Appendix C) — §15, Appendix C
- [ ] **BL.P.123** — Persona catalog (Appendix E) — §15, Appendix E
- [ ] **BL.P.124** — MCP tool catalog (Appendix F) — §7, Appendix F
- [ ] **BL.P.125** — Schema reference (Appendix A) — §5, Appendix A
- [ ] **BL.P.126** — Orchestration catalog (Appendix D — 47 archetypes documented) — §10, Appendix D
- [ ] **BL.P.127** — Microsoft product & SKU reference (Appendix G) — §12, Appendix G
- [ ] **BL.P.128** — Partner ecosystem catalog (Appendix H) — Appendix H
- [ ] **BL.P.129** — Independence & competitive posture (Appendix K) — Appendix K
- [ ] **BL.P.130** — Exercise solutions (Appendix J) — Appendix J
- [ ] **BL.P.131** — Wave 1 / 2 / 3 delivery playbook per Practice — §18.2
- [ ] **BL.P.132** — Discovery prompt templates per Practice — §18.2
- [ ] **BL.P.133** — Pre-clearance checklists (technical / legal / compliance) — §18.2

### 2.16 — Industry-Standards Incorporation

Source: `Industry-Standards-Incorporation-Plan.md` §11.

**Registry & infrastructure**

- [x] **BL.P.134** — `apex-schemas-common.standards` module (`StandardSpec`, `StandardRef`, `STANDARDS` registry, `introspect`) *(Sprint 2)*
- [x] **BL.P.135** — `apex standards list|show|audit|bump` CLI subcommands *(Path 3 — in `apex-schemas-common/_cli.py`; auto-attached to `apex` CLI via conditional import)*
- [x] **BL.P.136** — `conformance` lane in `.github/workflows/ci.yml` *(Path 3 — pytest `conformance` marker + `apex standards audit` step + `pytest -m conformance`)*
- [ ] **BL.P.137** — `standards/catalog.yaml` — machine-readable catalog source
- [ ] **BL.P.138** — `LICENSE-ATTRIBUTION.md` template + per-`apex-standards-*` package licence file

**Shared Pattern-B standard packages** (Sprint 3)

- [x] **BL.P.139** — `apex-standards-fhir` (R4 + R5 mirrors, R4→R5 migration) *(Sprint 3 Phase 1 — 7 R4 resources + 9 primitives + R5 skeleton + migration stub + terminology mock)*
- [x] **BL.P.140** — `apex-standards-cim` (IEC 61970 + 61968 subset for ER) *(Sprint 3 Phase 1)*
- [x] **BL.P.141** — `apex-standards-isa95` (hierarchy + personnel + equipment + material; shared ER/AXLE/ICE) *(Sprint 3 Phase 1)*
- [x] **BL.P.142** — `apex-standards-sid` (TM Forum SID — 7 domains for TMT) *(Sprint 3 Phase 1)*
- [x] **BL.P.143** — `apex-standards-opentravel` (OTA Air/Hotel/Car for TH) *(Sprint 3 Phase 1)*
- [x] **BL.P.144** — `apex-standards-cdisc` (ODM + SDTM DM/AE/LB skeletons) *(Sprint 3 Phase 1)*
- [x] **BL.P.145** — `apex-standards-iso14224` (reliability taxonomy + failure modes + record; shared AXLE/ICE) *(Sprint 3 Phase 1)*
- [x] **BL.P.146** — `apex-standards-j1939` (SPN/PGN seed registry + CAN frame; shared AXLE/ICE) *(Sprint 3 Phase 1)*

**Identifier-type bindings (T1 — Pattern A)**

- [x] **BL.P.147** — RC identifiers: GS1 GTIN-8/12/13/14, SSCC, GLN *(Sprint 2 — in `apex-schemas-common.standards.types`)*
- [x] **BL.P.148** — HLS identifiers: ICD-10/11, CPT, HCPCS, NDC, RxNorm, SNOMED-CT, LOINC *(Sprint 3 Phase 1 — in `apex-schemas-common.standards.types`; registered in `STANDARDS`)*
- [x] **BL.P.149** — ICE/AXLE identifiers: J1939 SPN/PGN *(Sprint 3 Phase 1 — `apex-standards-j1939.SEED_SPNS`/`SEED_PGNS` + loader hooks)*; AEMP 2.0 fields ship alongside ICEML entity work in Phase 2
- [x] **BL.P.150** — TMT identifiers: EIDR *(Sprint 2 — in `apex-schemas-common.standards.types`)*

**Terminology bindings (T2 — Pattern A + external hook)**

- [x] **BL.P.151** — SNOMED CT binding + lookup hook interface *(Sprint 3 Phase 1 — regex binding + `TerminologyService` protocol + `MockTerminologyService` in `apex-standards-fhir/terminology`)*
- [x] **BL.P.152** — LOINC binding + lookup hook interface *(Sprint 3 Phase 1)*
- [x] **BL.P.153** — RxNorm binding + lookup hook interface *(Sprint 3 Phase 1)*
- [ ] **BL.P.154** — ISO 8000 master-data-quality binding

**Message-format translators (T4 — Pattern D)**

- [ ] **BL.P.155** — EDI X12 parser/emitter (850/856/810/820 retail; 837/835/270/271 HLS)
- [ ] **BL.P.156** — HL7 v2.x parser/emitter
- [ ] **BL.P.157** — HL7 CDA / C-CDA parser
- [ ] **BL.P.158** — EPCIS event parser/emitter
- [ ] **BL.P.159** — OAGIS message parser/emitter
- [ ] **BL.P.160** — IATA PADIS parser

**Cross-standard translators (T3 — Pattern D)**

- [x] **BL.P.161** — GS1 ↔ Schema.org Product (round-trip tested) *(Sprint 2 — `apex-scml/translators`)*
- [ ] **BL.P.162** — HL7 v2 → FHIR R4 (one-way with conformance suite)
- [ ] **BL.P.163** — HL7 CDA → FHIR R4 (one-way)
- [ ] **BL.P.164** — CIM ↔ ISO 15926
- [ ] **BL.P.165** — SAE J1939 ↔ AEMP 2.0

**Protocol adapters (T5 — wrapped in SOR adapters, Sprint 15)**

- [ ] **BL.P.166** — OPC UA adapter core (shared ER / AXLE / ICE)
- [ ] **BL.P.167** — IEC 61850 adapter core
- [ ] **BL.P.168** — SAE J1939 telematics transport wrapper

### 2.17 — Scenario Library Extensions (Sprint 28+)

Source: `APEX_Design.md` §19 + §21. Completed foundation: BL.C.42a–m.

**Wave ribbon propagation**

- [ ] **BL.P.169** — Extend Wave ribbon (W1/W2/W3) to all 723 browsable-library scenarios (currently on 35 featured only) — §19.3
- [ ] **BL.P.170** — Micro Wave-progress indicator (compact 3-dot) on modal library rows; expands to full ribbon on row click — §19.3

**Wave 1 Foundation catalog**

- [ ] **BL.P.171** — W1 Foundation catalog as new sibling tab in Stacked Architecture HTML: ~40 reusable W1 building blocks (schema projections, LEDGER surfaces, MCP tools, HITL surfaces) with SoW-quotable scope — §19.3, §20
- [ ] **BL.P.172** — W1 Foundation asset classification (schema · LEDGER · MCP · HITL · policy) with per-asset estimated effort (story points / calendar weeks)
- [ ] **BL.P.173** — W1-to-W2 dependency graph showing which W1 assets unblock which W2 scenarios

**Wave 3 Fusion catalog**

- [ ] **BL.P.174** — W3 Fusion catalog: named agent meshes that compose after W2 proves out (e.g., "Perishables Economics Mesh" = cold-chain + markdown + loyalty-churn) — §19.2 tier 3
- [ ] **BL.P.175** — Per-Practice fusion mesh inventory (5–8 named meshes per Practice)
- [ ] **BL.P.176** — Fusion-mesh Wave ribbon variant showing 2–4 W2 scenarios as inputs, with W3 composed outcomes

**Scenario Library tooling**

- [ ] **BL.P.177** — Library CSV export from modal (full scenario set or filtered subset) — §19.1
- [ ] **BL.P.178** — Library PowerPoint export: one slide per filtered scenario with chain + wave ribbon
- [ ] **BL.P.179** — Cross-practice search modal: single "Browse all 723 scenarios" with practice-tag chip filters + free-text filter
- [ ] **BL.P.180** — Keyboard shortcuts: `/` focus filter, `↑/↓` row navigation, `Enter` expand chain, `Esc` close — §22.5

**Scenario Library governance & registry**

- [ ] **BL.P.181** — Appendix L: Scenario Library Master Catalog — normative JSON + human-readable reference per Practice
- [ ] **BL.P.182** — Scenario-to-Service-Catalog traceability validator (every `service_code` must resolve to a BL.P.110–116 Service Catalog entry)
- [ ] **BL.P.183** — Scenario-to-Agent-Catalog traceability validator (every featured scenario's Solution must name agents registered in BL.P.58–64 agent catalogs)
- [ ] **BL.P.184** — Scenario KPI-to-KPI-Registry traceability (Appendix C — BL.P.122)
- [ ] **BL.P.185** — Scenario versioning discipline: PATCH / MINOR / MAJOR rules + CI enforcement

### 2.18 — Published Communication Artifacts (Sprint 29+)

Source: `APEX_Design.md` §21. Completed foundation: BL.C.24, BL.C.25, BL.C.30a.

- [ ] **BL.P.186** — Appendix M: Narration Script Catalog — all 11-tab narration decks from Stacked Architecture HTML in standalone markdown with scene anchors + timing guidance — §20.3
- [ ] **BL.P.187** — Appendix N: Design-System Reference — typography, color tokens, per-practice banners, theme tokens, accessibility baseline, Independence rules — §22
- [ ] **BL.P.188** — Appendix O: Visual Artifacts Index — cross-reference table for every published artifact with Design Reference §§ — §21.2
- [ ] **BL.P.189** — Executive one-pager summarizing 35 featured scenarios in scannable pre-read table — §21.1
- [ ] **BL.P.190** — Companion slide deck: one chain per Practice in SteerCo format (7 slides × 6 chain-rows + Wave ribbon) — §21.1
- [ ] **BL.P.191** — Narrated HTML version of Sellers Guide Runtime Addendum (BL.C.30b) — §21.1
- [ ] **BL.P.192** — Tracked-changes version of Sellers Guide with v1.2 additions called out — §21.1
- [ ] **BL.P.193** — Claude Code build-instruction spec for porting Chains tab into main Professional APEX Sellers Guide HTML — §19, §21
- [ ] **BL.P.194** — Independence-language linter as standalone package (`apex-compliance-lint`) usable across all artifact build pipelines — §22.4
- [ ] **BL.P.195** — Pre-publish compliance-check CI lane: (a) Independence linguistic rules · (b) typography correctness · (c) color-token compliance · (d) responsive-layout smoke test — §22

---

## 3. Progress Snapshot

| Area | Completed | Planned | % Done |
|------|-----------|---------|--------|
| L1 Core contract & tools (Sprint 1 ✅) | 22 | 0 | 100% |
| Canonical schemas (Sprint 2 RC ✅, others pending) | 3 | 9 | 25% |
| Medallion architecture | 0 | 15 | 0% |
| MCP servers | 0 | 18 | 0% |
| Identity & visibility | 0 | 5 | 0% |
| Agent catalogs | 0 | 7 | 0% |
| Orchestration | 0 | 4 | 0% |
| HITL gates | 0 | 8 | 0% |
| Audit row | 0 | 8 | 0% |
| Purview trust | 0 | 6 | 0% |
| Fabric capacity | 0 | 4 | 0% |
| SOR adapters | 0 | 15 | 0% |
| Service catalogs | 0 | 7 | 0% |
| Reference deployments | 0 | 5 | 0% |
| Appendices & playbooks | 6 (plans) | 12 | ~30% |
| Industry-standards incorporation | 3 | 32 | ~9% |
| Published documentation artifacts (Sprint 27 ✅) | 12 | 0 | 100% |
| Scenario Library & Wave Ribbon (Sprint 27 ✅) | 13 | 0 | 100% |
| Scenario Library extensions (Sprint 28+) | 0 | 17 | 0% |
| Communication artifacts & compliance (Sprint 29+) | 0 | 10 | 0% |
| **TOTAL** | **81** | **182** | **~31%** |

Note: "Completed" counts reflect repository artifacts, tooling, design plans, and documentation authored to date. It does **not** imply a running production system — the L1 contract layer, design artefacts, Scenario Library, Stacked Architecture narrated cinematic, and design-system conventions are in hand; the L3 Practice implementations, MCP servers, agent catalogs, and runtime components (most BL.P.* items) remain to be built.
