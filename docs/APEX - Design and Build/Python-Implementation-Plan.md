# APEX Python Implementation Plan

**Source:** `Orchestrator.md` (Sprints 0–19) + `Roadmap.md` (BL.P.*)
**Design reference:** `APEX_Design.md`
**Date:** 2026-04-19
**Purpose:** Concrete Python implementation path for every Orchestrator sprint — stack choices, package layout, per-sprint deliverables (files, modules, tests), and execution order.

---

## 1. Scoping Assumptions (please confirm)

These are my proposed defaults. Push back on any you'd change and I'll revise the plan.

| Decision | Default | Rationale |
|----------|---------|-----------|
| **Python version** | 3.12 | Pydantic v2 + PySpark + Azure SDK compatibility; long support window |
| **Package/venv manager** | `uv` (workspaces) | 10–100× faster than pip/poetry; native workspace support for monorepo |
| **Manifest validation** | Pydantic v2 | Typed models generate JSON Schema for free; replaces hand-written `.js` validators |
| **MCP server framework** | FastAPI + `mcp` Python SDK | Async, OpenAPI-native, matches Anthropic's reference MCP servers |
| **Medallion transforms** | PySpark on Fabric runtime | Native Fabric Lakehouse compute; Delta reads/writes |
| **Audit / trace** | OpenTelemetry + structlog | Fabric Application Insights integration; structured JSON logs |
| **Test framework** | `pytest` + `pytest-asyncio` + `pytest-cov` | Standard; async support for FastAPI |
| **Lint/format** | `ruff` (check + format) | Replaces black + isort + flake8 in one tool |
| **Type checking** | `mypy --strict` on all packages | Enforces typed contracts at CI |
| **Cloud SDK** | `azure-identity`, `azure-storage-file-datalake`, `azure-ai-projects`, `azure-monitor-opentelemetry` | Python-first Azure/Fabric/Foundry access |
| **IaC** | Terraform (kept) + Python Pulumi for edge cases | Stay with Terraform for F-SKU provisioning (Sprint 14) |
| **Scope of port** | **New work only.** `apex-core/tools/*.js` ports to Python in Sprint 1; existing `.js` code stays until sprint-1 Python tools reach parity | Keeps old pipelines running while we build |
| **Repo layout** | Single monorepo with `uv` workspace | One lockfile, one CI, cross-package refactors atomic |

**Open questions to confirm:**

1. Is `uv` acceptable, or do you want `poetry` / `pip-tools` / `hatch`?
2. Any Deloitte-house Python conventions I should inherit (internal package index, vendored wheels, proxy config)?
3. Does Deloitte's Azure AI / Fabric environment impose a specific Python runtime (e.g., Fabric Data Science notebooks pin Python 3.11)? If so, we align to that.
4. CI target: GitHub Actions, Azure Pipelines, or both?

---

## 2. Target Monorepo Layout

```
APEX/                                          (repo root)
├── pyproject.toml                             (uv workspace root)
├── uv.lock
├── .python-version                            ("3.12")
├── ruff.toml
├── mypy.ini
├── .pre-commit-config.yaml
├── .github/workflows/                         (CI)
│   ├── ci.yml                                 (lint + type + test per package)
│   └── release.yml                            (semver-bump + tag)
├── packages/
│   ├── apex-core/                             (L1 contract)
│   │   ├── pyproject.toml
│   │   ├── src/apex_core/
│   │   │   ├── __init__.py
│   │   │   ├── manifests/                     (Pydantic models: event, orch, agent, tenant, policy, service, schema)
│   │   │   ├── envelope.py                    (canonical 5-field envelope)
│   │   │   ├── semver.py                      (classify-bump logic)
│   │   │   ├── validators/                    (validate_manifest, validate_practice, validate_fleet)
│   │   │   └── cli.py                         (apex CLI entry point)
│   │   └── tests/
│   ├── apex-practices/                        (L3 Practices)
│   │   ├── apex-rc/
│   │   ├── apex-hls/
│   │   ├── apex-er/
│   │   ├── apex-axle/
│   │   ├── apex-tmt/
│   │   ├── apex-th/
│   │   └── apex-ice/
│   ├── apex-schemas/                          (canonical schemas per Practice)
│   │   ├── scml/
│   │   ├── merml/
│   │   ├── cxml/
│   │   ├── hlscml/
│   │   ├── ercml/
│   │   ├── axleml/
│   │   ├── telml/
│   │   ├── iropsml/
│   │   └── connected-ice-ml/
│   ├── apex-medallion/                        (Bronze/Silver/Gold templates + PySpark helpers)
│   ├── apex-tokenizer/                        (tokenization service)
│   ├── mcp-servers/
│   │   ├── domain/
│   │   │   ├── scml-mcp/
│   │   │   ├── merml-mcp/
│   │   │   ├── cxml-mcp/
│   │   │   ├── hlscml-mcp/
│   │   │   ├── ercml-mcp/
│   │   │   └── axlecml-mcp/
│   │   ├── utility/
│   │   │   ├── fabric-mcp/
│   │   │   ├── policy-mcp/
│   │   │   ├── telemetry-mcp/
│   │   │   ├── approvals-mcp/
│   │   │   ├── ledger-mcp/
│   │   │   └── tokenizer-mcp/
│   │   └── external/
│   │       ├── fda-mcp/
│   │       ├── ferc-mcp/
│   │       ├── edi-mcp/
│   │       ├── vendor-portal-mcp/
│   │       └── pharma-recall-mcp/
│   ├── apex-identity/                         (Entra managed-identity + visibility lattice)
│   ├── apex-orchestrator/                     (47-archetype runtime + HITL gates)
│   ├── apex-audit/                            (14-field audit row + WORM store)
│   ├── apex-purview/                          (Purview registration pipeline)
│   ├── apex-adapters/                         (15 SOR adapters)
│   │   ├── epic-clarity/
│   │   ├── sap-s4hana/
│   │   ├── salesforce/
│   │   └── ...
│   └── apex-cli/                              (unified `apex` CLI)
├── notebooks/                                 (Fabric PySpark notebooks)
│   ├── bronze/
│   │   ├── mirrored_database.py               (template)
│   │   ├── eventstream.py
│   │   ├── data_pipeline.py
│   │   ├── dataflow_gen2.py
│   │   └── custom_endpoint.py
│   ├── silver/
│   │   └── transform_template.py
│   └── gold/
│       ├── direct_lake.py
│       └── warehouse_views.sql
├── infra/                                     (Terraform + Pulumi)
│   ├── terraform/
│   │   ├── fabric-capacity/
│   │   ├── onelake-workspaces/
│   │   └── entra/
│   └── pulumi/
├── docs/                                      (existing — preserved)
└── archive/                                   (existing — preserved)
```

---

## 3. Sprint 0 — Python Scaffolding (NEW)

**Duration:** 3–5 days
**Not in Orchestrator.md yet.** This precedes Sprint 1; it's the substrate every subsequent sprint runs on.

### Deliverables

- [ ] **S0.1** — `pyproject.toml` (uv workspace root) with all member packages declared
- [ ] **S0.2** — `.python-version` pinning 3.12
- [ ] **S0.3** — `ruff.toml` with strict rules (E, F, W, I, N, UP, B, A, C4, PIE, SIM, PTH, RUF)
- [ ] **S0.4** — `mypy.ini` with `--strict` globally
- [ ] **S0.5** — `.pre-commit-config.yaml` (ruff + mypy + trailing-whitespace + end-of-file-fixer)
- [ ] **S0.6** — `.github/workflows/ci.yml` — matrix build across all workspace packages (lint + type + test)
- [ ] **S0.7** — `packages/apex-core/` skeleton: `pyproject.toml`, `src/apex_core/__init__.py`, `tests/test_smoke.py`
- [ ] **S0.8** — Shared `conftest.py` with fixtures for Fabric mocking (`moto`-style `azure-mock`), temp paths, canonical envelope test data
- [ ] **S0.9** — CHANGELOG.md conventions + `bump-my-version` config for SemVer per package
- [ ] **S0.10** — Developer onboarding doc (`docs/guides/APEX-python-developer-onboarding.md`)

### Exit Criteria

- `uv sync` from a fresh clone produces a working venv.
- `uv run pytest` passes smoke test.
- `uv run ruff check .` and `uv run mypy` pass.
- `git commit` triggers pre-commit hooks.

---

## 4. Sprint 1 — L1 Manifest Contract (Pydantic port)

**Closes:** BL.P.01–P.07
**Python deliverables:** Pydantic v2 models + CLI validators replacing `apex-core/tools/*.js`.

### Task 1.1 — Event manifest (BL.P.01)
- [ ] `packages/apex-core/src/apex_core/manifests/event.py`
  ```python
  class EventManifest(BaseModel):
      name: str
      version: SemVer
      trigger: TriggerSpec
      payload_schema: JsonSchema
      classification: Classification
      bump_class: Literal["PATCH", "MINOR", "MAJOR"]
  ```
- [ ] Fixtures: `tests/fixtures/event/{valid,minor_bump,major_bump}.yaml`
- [ ] Test: `tests/manifests/test_event.py`

### Task 1.2 — Orchestration manifest (BL.P.02)
- [ ] `manifests/orchestration.py` with `OrchestrationManifest` (agents, HITL gate placement, three-version stamps)

### Task 1.3 — Agent manifest (BL.P.03)
- [ ] `manifests/agent.py` with `AgentManifest` (model pin, prompt SHA, tool allow-list, scope)

### Task 1.4 — Tenant manifest (BL.P.04)
- [ ] `manifests/tenant.py` with `TenantManifest` (Practice pin, subscriptions, overrides) + L3-parent compatibility checker

### Task 1.5 — Policy manifest (BL.P.05)
- [ ] `manifests/policy.py` with `PolicyManifest` (HITL rules, DLP, classification mappings)

### Task 1.6 — Service manifest (BL.P.06)
- [ ] `manifests/service.py` with `ServiceManifest` (persona, KPI refs, SLO, commercial terms)

### Task 1.7 — Canonical envelope + classify-bump + validators (BL.P.07)
- [ ] `envelope.py` — `CanonicalEnvelope` Pydantic mixin enforcing 5 fields
- [ ] `semver.py` — `classify_bump(old, new) -> Literal["PATCH", "MINOR", "MAJOR"]` (ports `apex-core/tools/classify-bump.js`)
- [ ] `validators/manifest.py` — `validate_manifest(path) -> ValidationReport` (ports `validate-manifest.js`)
- [ ] `validators/practice.py` + `validators/fleet.py` (port remaining `.js` tools)
- [ ] `cli.py` — Typer-based CLI: `apex validate <path>`, `apex classify-bump <old> <new>`, `apex report --html`

### Sprint 1 Exit
- All six manifest schemas validate with matching fixtures.
- `apex` CLI runs on the command line.
- Python-side parity with `.js` tools verified by running the same fixtures through both.

---

## 5. Sprint 2 — Canonical Schemas: RC Anchor

**Closes:** BL.P.08–P.10
**Python deliverables:** Entity Pydantic models + Delta DDL generator + Purview payload emitter, per schema family.

### Package: `packages/apex-schemas/scml/`
- [ ] `src/apex_scml/entities/sku.py`, `location.py`, `lot.py`, `shipment.py`, `supplier.py`, `item.py` — Pydantic models inheriting `CanonicalEnvelope`
- [ ] `src/apex_scml/classifications.py` — Purview sensitivity tags
- [ ] `src/apex_scml/ddl.py` — `generate_delta_ddl(entity: type[BaseModel]) -> str` using Pydantic schema + SCD2 mixin
- [ ] `src/apex_scml/purview.py` — `build_purview_payload(entity) -> dict` for Purview REST registration
- [ ] `src/apex_scml/translators/gs1_to_schema_org.py`
- [ ] Tests for round-trip GS1 ↔ Schema.org

### Package: `packages/apex-schemas/merml/` — same pattern
### Package: `packages/apex-schemas/cxml/` — same pattern + `tokenizer_hooks.py`

### Anchor: `packages/apex-practices/apex-rc/`
- [ ] `src/apex_rc/practice.py` — Pydantic `PracticeBundle` listing schemas, agents, services
- [ ] `src/apex_rc/data/schemas.manifest.yaml` — declarative bundle
- [ ] CI step: `uv run apex validate packages/apex-practices/apex-rc`

---

## 6. Sprint 3 — Canonical Schemas: Other Practices

**Closes:** BL.P.11–P.19
**Python deliverables:** Replicate Sprint 2 pattern across HLS, ER, AXLE, TMT, TH, ICE.

Each Practice package follows the same `entities/ + ddl.py + purview.py + translators/` shape.

- [ ] `apex-schemas/hlscml/` (PatientML, ClaimML, StudyML) — FHIR ↔ HL7 v2 ↔ CDA translators; PHI classifications
- [ ] `apex-schemas/ercml/` (UOGML, P&UML, MiningML) — CIM alignment
- [ ] `apex-schemas/axleml/` — ISA-95 / ISA-88 / OPC UA
- [ ] `apex-schemas/telml/` — TM Forum SID alignment
- [ ] `apex-schemas/iropsml/` — IATA NDC / PADIS; PCI-DSS tokenization for payment
- [ ] `apex-schemas/connected-ice-ml/` — SAE J1939 / AEMP 2.0 round-trip translator
- [ ] `apex-core/src/apex_core/translator_catalog.py` — indexes all translators

### Parallelization
Each Practice package is independent — Sprint 3 parallelizes by Practice lead.

---

## 7. Sprints 4–6 — Medallion (Bronze / Silver / Gold)

### Sprint 4 — Bronze landing (BL.P.20–P.25)

**Python deliverables:** Parameterized PySpark notebooks + Fabric artifact templates.

- [ ] `notebooks/bronze/mirrored_database.py` — Mirrored Database template; config via env vars
- [ ] `notebooks/bronze/eventstream.py` — Eventstream → Eventhouse KQL table
- [ ] `notebooks/bronze/data_pipeline.py` — Fabric Data Factory batch (JSON export from Python CLI)
- [ ] `notebooks/bronze/dataflow_gen2.py` — Power Query M wrapper + incremental-watermark helper
- [ ] `notebooks/bronze/custom_endpoint.py` — Azure Function HTTP trigger reference (separate FastAPI app)
- [ ] `packages/apex-medallion/src/apex_medallion/bronze/retention.py` — Purview retention policy emitter

### Sprint 5 — Silver + Tokenization (BL.P.26, P.27, P.28, P.34)

- [ ] `notebooks/silver/transform_template.py` — PySpark: Bronze read → canonicalize → enrich → tokenize → Silver write
- [ ] `packages/apex-tokenizer/src/apex_tokenizer/`
  - `service.py` — deterministic reversible token function
  - `vault.py` — vault Delta table `silver_vault_tokens` I/O
  - `classifier_hook.py` — Purview classification trigger → tokenize column
- [ ] `packages/apex-medallion/src/apex_medallion/silver/scd2.py` — reusable SCD2 pattern
- [ ] `packages/apex-medallion/src/apex_medallion/drift.py` — Fabric-schema vs Pydantic-model drift detector (CLI + nightly job)

### Sprint 6 — Gold + Measures (BL.P.29–P.33)

- [ ] `packages/apex-medallion/src/apex_medallion/gold/direct_lake.py` — semantic-model definition helpers
- [ ] `notebooks/gold/warehouse_views.sql` — T-SQL view templates (SHA-stamped)
- [ ] `packages/apex-medallion/src/apex_medallion/gold/kql_functions.py` — real-time Eventhouse KQL generators
- [ ] `packages/apex-medallion/src/apex_medallion/measures/`
  - `pre_measures.py` — PySpark pre-measure library (effective_margin_pct, stock_days_remaining, …)
  - `post_measures_dax.py`, `post_measures_tsql.py`, `post_measures_kql.py`

---

## 8. Sprints 7–9 — MCP Servers

**Framework:** FastAPI + `mcp` Python SDK (Anthropic).
**Common pattern:** each MCP server is its own `packages/mcp-servers/<class>/<name>-mcp/` package.

### Shared scaffolding — `packages/mcp-servers/mcp-common/`
- [ ] `auth.py` — Entra managed-identity middleware
- [ ] `trace.py` — OpenTelemetry instrumentation emitting the required trace record
- [ ] `scope.py` — visibility-lattice evaluator middleware
- [ ] `contract.py` — Pydantic-to-MCP tool-contract generator (BL.P.51)
- [ ] `testing.py` — pytest fixtures for MCP client/server round-trips

### Sprint 7 — Utility MCP Servers (BL.P.41–P.45, P.51–P.52)
- [ ] `fabric-mcp/` — tools: `get_entity_by_key`, `query_gold_view`, `list_classifications`
- [ ] `policy-mcp/` — tools: `evaluate_policy`, `check_compliance`, `classify_bump`
- [ ] `telemetry-mcp/` — tools: `emit_trace`, `log_event`, `query_latency_percentile`
- [ ] `approvals-mcp/` — tools: `request_approval`, `get_approval_status`, `record_decision` (Teams + Copilot Studio bindings in Sprint 11)
- [ ] `ledger-mcp/` — tools: `append_audit_row`, `fetch_row_by_trace`, `verify_row_signature`
- [ ] `tokenizer-mcp/` — tools: `detokenize_under_scope` (wraps `apex-tokenizer`)

### Sprint 8 — Domain MCP Servers (BL.P.35–P.40)
- [ ] `scml-mcp/`, `merml-mcp/`, `cxml-mcp/`, `hlscml-mcp/`, `ercml-mcp/`, `axlecml-mcp/`
- [ ] Each binds to its Gold views via `fabric-mcp`, applies scope + classification, registers tools

### Sprint 9 — External MCP Servers (BL.P.46–P.50)
- [ ] `fda-mcp/` — OpenFDA client + rate-limit handling
- [ ] `ferc-mcp/`, `edi-mcp/`, `vendor-portal-mcp/`, `pharma-recall-mcp/`

---

## 9. Sprint 10 — Identity & Visibility Lattice

**Closes:** BL.P.53–P.57
**Package:** `packages/apex-identity/`

- [ ] `src/apex_identity/provisioning.py` — Entra app-registration automation (Microsoft Graph SDK for Python)
- [ ] `src/apex_identity/scope.py` — composition of tenant × practice × persona × classification × row filter
- [ ] `src/apex_identity/lattice.py` — RLS + OLS generator from YAML classification
- [ ] `src/apex_identity/agent_safe_view.py` — view generator: mask / tokenize / drop per classification × scope
- [ ] `src/apex_identity/signing.py` — service-principal signing of agent output
- [ ] Integration test: end-to-end RC agent calls `scml-mcp` → lattice evaluated → masked response signed

---

## 10. Sprint 11 — Orchestration & HITL Runtime

**Closes:** BL.P.65–P.76
**Package:** `packages/apex-orchestrator/`

- [ ] `src/apex_orchestrator/primitives/`
  - `sequential.py`, `parallel.py`, `hierarchical.py`, `feedback_loop.py`
- [ ] `src/apex_orchestrator/archetypes/` — 47 archetype modules (first 10 implemented in-sprint; remaining 37 as manifests + stubs)
- [ ] `src/apex_orchestrator/manifest_runtime.py` — manifest loader + three-version stamping
- [ ] `src/apex_orchestrator/gates/`
  - `zero_touch.py`, `ack_only.py`, `hitl.py`, `escalation.py`
  - `variants.py` — hard / soft / policy / escalation selectors
- [ ] `src/apex_orchestrator/integrations/`
  - `teams_card.py` — Adaptive Card builder
  - `copilot_studio.py` — Copilot Studio skill action
- [ ] `src/apex_orchestrator/tenant_tuning.py` — 2-week observation workflow
- [ ] Reference orchestration: Cold Chain Excursion Response (RC) — demonstrable end-to-end

---

## 11. Sprint 12 — Decision Audit Row

**Closes:** BL.P.77–P.84
**Package:** `packages/apex-audit/`

- [ ] `src/apex_audit/row.py` — `AuditRow` Pydantic model, 14 required fields
- [ ] `src/apex_audit/store.py` — append-only Delta writer with WORM policy
- [ ] `src/apex_audit/trace.py` — trace-ID generator + propagation (OpenTelemetry context)
- [ ] `src/apex_audit/version_stamps.py` — three-SHA stamper at pre-invocation
- [ ] `src/apex_audit/reasoning.py` — capture with DLP scrub (Presidio integration for PII detection)
- [ ] `src/apex_audit/composite.py` — orchestration composite-row emitter
- [ ] `src/apex_audit/content_hash.py` — input/output content-addressed hash store
- [ ] `src/apex_audit/signing.py` — row signing + hashing
- [ ] CLI: `apex audit reconstruct <decision_id>` — resolves three SHAs and prints effective rules

---

## 12. Sprint 13 — Purview Trust Architecture

**Closes:** BL.P.85–P.90
**Package:** `packages/apex-purview/`

- [ ] `src/apex_purview/registration.py` — YAML schema → Purview classification payload → REST client
- [ ] `src/apex_purview/lineage.py` — emit edges at every hop (via Purview SDK)
- [ ] `src/apex_purview/dlp.py` — label-based redaction policy emitter
- [ ] `src/apex_purview/worm.py` — retention policy emitter (7 y / 10 y / legal hold)
- [ ] `src/apex_purview/catalog.py` — Unified Catalog business-glossary registration
- [ ] `src/apex_purview/propagation.py` — Silver → Gold → semantic → Copilot → agent output validator (most-restrictive label)

---

## 13. Sprint 14 — Fabric Capacity & Provisioning

**Closes:** BL.P.91–P.94
**Track:** Terraform + thin Python wrappers.

- [ ] `infra/terraform/fabric-capacity/` — F-SKU module parameterized F2 → F2048
- [ ] `infra/terraform/onelake-workspaces/` — workspace creation via Fabric REST provider
- [ ] `packages/apex-cli/src/apex_cli/fabric.py` — `apex fabric create-workspace`, `apex fabric shortcut` wrappers
- [ ] `infra/terraform/shortcuts/` — ADLS / S3 / GCS / Dataverse shortcut provisioning

**Parallelizable from Sprint 1** — does not block other work.

---

## 14. Sprint 15 — SOR Integration Adapters

**Closes:** BL.P.95–P.109
**Package:** `packages/apex-adapters/`

Each adapter is its own sub-package with:
- `src/apex_adapters/<sor_name>/client.py` — API client
- `config.py` — connection schema
- `reference_workspace/` — Fabric artifact (Mirrored DB / Dataflow / Pipeline)
- `tests/` — recorded-response integration tests (`pytest-vcr`)

15 adapters, parallelizable. Priority order:

1. `epic-clarity/` — HLS anchor
2. `sap-s4hana/` — cross-Practice anchor
3. `salesforce/` — cross-Practice
4. `manhattan-active-wms/` — RC
5. Others in any order

---

## 15. Sprint 16 — Agent Catalogs per Practice

**Closes:** BL.P.58–P.64

- [ ] Per-Practice agent directory: `packages/apex-practices/apex-<practice>/src/apex_<practice>/agents/`
- [ ] Each agent: `agent.yaml` (manifest) + `prompts/system.md` + `tools.py` (allow-list binding) + `tests/golden.py`
- [ ] Parallelizable by Practice lead
- [ ] RC anchor 10 agents: Assortment, Demand Sensing, Markdown, Cold Chain, Shrink, Customer Identity, Promotions, Substitutions, Inventory, Store Ops

---

## 16. Sprint 17 — Service Catalogs per Practice

**Closes:** BL.P.110–P.116

- [ ] Per-Practice service directory: `packages/apex-practices/apex-<practice>/src/apex_<practice>/services/`
- [ ] Each service: `service.yaml` (manifest: persona, KPI refs, SLO, commercial terms) + `bundle.py` (composes agents + orchestrations + gates)

---

## 17. Sprint 18 — Reference Deployments

**Closes:** BL.P.117–P.121

- [ ] `packages/apex-practices/apex-rc/src/apex_rc/reference_deployments/big_box_store/`
  - `cold_chain_excursion.py`
  - `markdown_cadence.py`
  - `demo_data/` — seeded Delta tables for self-contained demo
  - `demo_script.md`
- [ ] Similarly: `hospital/`, `utility/`, `plant/`, `airline/` under their Practice packages

---

## 18. Sprint 19 — Registries, Playbooks & Appendices

**Closes:** BL.P.122–P.133

- [ ] `packages/apex-core/src/apex_core/registries/`
  - `kpi.py`, `persona.py`, `mcp_tool.py`, `schema.py`, `orchestration.py` — generate Appendices A/C/D/E/F from code
- [ ] `docs/appendices/` — markdown generated from registries
- [ ] `docs/playbooks/wave-1-<practice>.md`, `wave-2-<practice>.md`, `wave-3-<practice>.md` per Practice

---

## 19. Critical-Path & Parallelization

```
Sprint 0 ──────────────────┐
                           ▼
Sprint 1 (L1 Pydantic) ───┬─► Sprint 2 (RC anchor)
                          │        │
                          │        ▼
                          │   Sprint 3 (other Practices, parallel by lead)
                          │        │
                          ▼        ▼
                     Sprint 4 (Bronze templates)
                          │
                          ▼
                     Sprint 5 (Silver + tokenizer)
                          │
                          ▼
                     Sprint 6 (Gold + measures)
                          │
Sprint 7 (Utility MCP) ◄──┤
Sprint 10 (Identity) ◄────┤
                          │
Sprint 8 (Domain MCP) ◄── 7
Sprint 9 (External MCP) ◄─ 7
                          │
Sprint 11 (Orchestration + HITL) ◄── 1, 7, 10
Sprint 12 (Audit row) ◄────────────── 1, 7
Sprint 13 (Purview) ◄──────────────── 4, 5, 6, 12
                          │
Sprint 14 (Fabric infra) — parallel from Sprint 1
                          │
Sprint 15 (SOR adapters) ◄─ 4, 13
Sprint 16 (Agent catalogs) ◄ 8, 10, 11
Sprint 17 (Services) ◄────── 16
Sprint 18 (Reference deployments) ◄ 16, 17
Sprint 19 (Appendices) ◄──── all
```

**Recommended team sequencing (single-stream):**
1. Platform engineer: Sprints 0 → 1 → 4 → 5 → 6
2. Same engineer + schema leads: Sprints 2 → 3 (parallel by Practice from Sprint 3 onwards)
3. MCP team picks up Sprint 7 → 8 → 9 after Sprint 6 ships
4. Runtime team: Sprint 10, 11, 12, 13 in that order after Sprints 7 & 8
5. Infra engineer: Sprint 14 in parallel from Sprint 1
6. Adapter leads: Sprint 15 in parallel by adapter after Sprint 4
7. Practice leads: Sprint 16 & 17 in parallel by Practice
8. Anchor team: Sprint 18 & 19 last

**Conservative single-stream calendar:** ~48 weeks (Sprints 0–19).
**Parallelized (3–4 streams):** ~26–30 weeks.

---

## 20. Definition of Done (Python-specific, applied to every task)

A task is Python-DoD-complete when:

1. Code passes `ruff check .` and `ruff format --check .`
2. Code passes `mypy --strict` (package-scoped)
3. Tests pass: `uv run pytest` (minimum 85% coverage on new code)
4. Pydantic models generate valid JSON Schema (round-trip test)
5. Public API documented (Google-style docstrings; `sphinx` opt-in later)
6. CHANGELOG entry under the correct SemVer bump
7. Pre-commit hooks pass
8. CI green on merge
9. Purview lineage / classification / DLP registered where applicable
10. Audit row emitted by any runtime path the task touches
11. Code review completed by someone other than the author

---

## 21. Open Questions (blocker-level)

1. **`uv` vs `poetry`?** — I default to `uv`; confirm.
2. **Python version — 3.11 or 3.12?** — Fabric Data Science notebooks may pin 3.11. Confirm target runtime.
3. **MCP SDK choice** — Anthropic's `mcp` Python package, or FastAPI-only with custom contract? I default to `mcp` + FastAPI together.
4. **CI target** — GitHub Actions, Azure Pipelines, both?
5. **Cloud-auth pattern** — DefaultAzureCredential chain (local dev → CLI → managed identity in prod), or fixed service-principal pattern?
6. **Fabric runtime** — will PySpark notebooks run in Fabric's managed runtime, or a self-hosted Spark cluster? Affects packaging (`.whl` on OneLake vs workspace libraries).
7. **Do you want Sprint 0 to also scaffold the `archive/` → `notebooks/` / `infra/` directories**, or keep them out until later?

Once these are answered, I can start Sprint 0 scaffolding in the next session.
