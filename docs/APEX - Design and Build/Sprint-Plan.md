# APEX Master Sprint Plan

**Audience:** Engagement leads, tenant SREs, finance/ops, anyone who needs to know what ships when
**Purpose:** Single master schedule that ties together [`Roadmap.md`](Roadmap.md) (framework-wide), [`RC-Build-Plan.md`](RC-Build-Plan.md) (RC practice), and the Phase 0 / I / J plans under [`docs/plans/`](../plans/) into one calendar view.

**First-iteration scope:** **Retail & Consumer (RC) practice only.** The 5 featured RC scenarios are the canonical worked examples; HLS / ER / AXLE / TH / TMT / ICE practices come online per Sprint 58+. APEX-G and APEX-A variants stay stub-only until commissioned.

**Sprint cadence:** continues from Sprint 1. Each sprint = 2 weeks. Numbering is non-skipping; gap = sprint not yet committed.

---

## TL;DR — where we are, where we're going

| Phase | Sprints | What lands | Status |
|---|---|---|---|
| **Framework foundation** | 1–29 | L1 contract, schemas, MCP servers, identity, orchestration, HITL, audit | ✅ done (per `Roadmap.md`) |
| **RC scaffolding + Phase 0** | 30–31 | RC service tree, agents, use cases; APEX-M/G/A variant split; APEX-Core protocols | ✅ done (this session) |
| **Phase I architecture (paper)** | (compressed into this session) | Microsoft platform alignment design, mocks, ADRs, deprecation notes | ✅ done (this session) |
| **Phase I production wiring** | **41–46** | Real SDK calls behind every APEX-M protocol impl; wizard live; first end-to-end deploy | ⏳ next |
| **First client engagement** | **47–49** | Lab + Wave 2 Pilot for RC-E2E-03; Phase J migrations land | ⏳ next |
| **RC service expansion** | **50–55** | RC-E2E-04 / -05 / -07 / -09 production impls | planned |
| **RC W3 fusion** | **56** | Cross-service composition (Perishables Economics Mesh) | planned |
| **Second client + HLS kickoff** | **57+** | Second client engagement; HLS practice begins | planned |
| **APEX-G or APEX-A port** | **TBD** | When client commissions a non-Microsoft variant | on-demand |

---

## Reading this plan against the existing artifacts

| Artifact | Covers |
|---|---|
| [`Roadmap.md`](Roadmap.md) | Sprints 1–29 (framework) + ongoing backlog items BL.C.* / BL.P.* |
| [`Sprint-Backlog-Retirement-Map.md`](Sprint-Backlog-Retirement-Map.md) | Priority-ordered orchestration of Sprints 30–49 with explicit BL.P.* / DEP-NNN retirement claims |
| [`Sprint-Execution-Order.md`](Sprint-Execution-Order.md) | Dependency graph + Wave A/B/C/D/E parallelization strategy |
| [`RC-Build-Plan.md`](RC-Build-Plan.md) + [`services/rc/_build-status.yaml`](../../services/rc/_build-status.yaml) | Sprints 30–40 (RC W1 Foundation through RC W3 Fusion) |
| [`docs/plans/2026-05-09-rc-design-docs-foundry-design.md`](../plans/2026-05-09-rc-design-docs-foundry-design.md) | Approved Path C runtime architecture |
| [`docs/plans/2026-05-09-rc-design-docs-foundry-implementation.md`](../plans/2026-05-09-rc-design-docs-foundry-implementation.md) | Phase A–J task breakdown |
| [`docs/plans/2026-05-09-microsoft-platform-alignment-delta.md`](../plans/2026-05-09-microsoft-platform-alignment-delta.md) | Microsoft GA gap analysis |
| [`docs/plans/2026-05-09-apex-m-g-a-with-adapters-design.md`](../plans/2026-05-09-apex-m-g-a-with-adapters-design.md) | Variant + adapter design |
| [`docs/APEX - Design and Build/adr/`](adr/) | 5 ADRs — H.1–H.5 resolutions |
| [`docs/APEX - Design and Build/deprecations/`](deprecations/) | Phase J 6 deprecations |
| [`docs/APEX - Design and Build/agent-identity-blueprints.md`](agent-identity-blueprints.md) | Phase I.1 design |
| [`docs/APEX - Design and Build/Pre-deployment-Security-Gate.md`](Pre-deployment-Security-Gate.md) | Phase I.7 operator checklist |

This master plan **does not duplicate** their content; it sequences them.

---

## Sprint detail — Phase I production wiring (41–46)

Phase I in this session landed **architecture + mocks + ADRs + book content**. Production wiring against real Microsoft SDKs is the next 6 sprints. Each sprint targets one APEX-Core protocol's APEX-M concrete impl, lands integration tests against a real Lab tenant, and updates the wizard surface.

### Sprint 41 — Production Entra Agent ID (2 weeks)
**Owner:** Identity SRE
**Exit:** `apex_m.identity_entra.AgentIdentityProviderEntra` makes real Microsoft Graph calls in Lab
- Wire `azure-identity` + `httpx` SDKs (currently lazy-imported)
- Implement OBO flow per [Microsoft Learn — OAuth 2.0 OBO](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-on-behalf-of-flow)
- Integration tests against real Entra Lab tenant (idempotent blueprint upsert, identity provision, revoke, list)
- `apex-m/infra/bicep/platform/identity.bicep` deployment script verified against Lab subscription
- **Depends on:** Lab tenant Entra access + `Application.ReadWrite.All` + `AgentIdentity.ReadWrite.All` granted to deployment principal

### Sprint 42 — Production Foundry runtime (2 weeks)
**Owner:** Runtime SRE
**Exit:** `apex_m.runtime_foundry.AgentRuntimeFoundry` deploys + invokes a real hosted agent in Lab
- Wire `azure-ai-projects` SDK + Microsoft Agent Framework hosting integration
- Implement deploy_agent / invoke / drain / list against Foundry Agent Service hosted agents
- Integration tests: deploy The Pricer agent for `rc-cold-chain-excursion-mid-shift`, invoke with synthetic excursion event, verify response
- Bicep `apex-m/infra/bicep/platform/foundry.bicep` AVM module deployed against Lab subscription with full BYO Storage + AI Search + Cosmos
- **Depends on:** Sprint 41 (agent identity); Lab Foundry project + ACR + Container image

### Sprint 43 — Production Fabric DataLake (2 weeks)
**Owner:** Data SRE
**Exit:** `apex_m.data_lake_fabric.DataLakeFabric` reads from Lab Fabric workspace with OBO
- Wire SQL analytics endpoint passthrough auth using operator OBO token
- Implement query / write / get_security_policy / list_entities
- Provision Lab `rc-canonical` primary workspace + `rc-e2e-03` consumer workspace via Bicep (Phase I.4 follow-up)
- Smoke: write to Bronze Inventory, query Silver SCML.Inventory with operator-scoped OBO, verify OneLake security policy enforced
- **Depends on:** Sprint 41 (OBO token); Lab Fabric capacity provisioned

### Sprint 44 — Production Purview Audit + sensitivity classifier (2 weeks)
**Owner:** Governance SRE
**Exit:** Real Purview Audit emits + reverse propagation works
- Wire Microsoft Compliance Audit Graph API for `AuditLedgerPurview`
- Wire Purview labels API for `SensitivityClassifierPurview` (production classify_text, get_label_inventory)
- Verify sensitivity-label propagation through Foundry RAG end-to-end (T3 entity → encrypted RAG result honoring EXTRACT)
- **Depends on:** Sprint 42 (Foundry runtime); Purview Information Protection enabled per Pre-deployment Security Gate item #4

### Sprint 45 — Production Defender threat protection (2 weeks)
**Owner:** Security SRE
**Exit:** Pre-prod gate's #1, #2, #9 are green for Lab tenant
- Wire Azure AI Content Safety Prompt Shields SDK
- Wire Defender for AI services threat protection ingestion
- Wire AI Model Security scan in CI pipeline (every agent image scanned at build)
- Defender for Cloud CSPM AI security posture surfaced in Pre-deployment Security Gate page
- **Depends on:** Defender plans enabled (Pre-deployment Security Gate items #1, #2)

### Sprint 46 — Wizard live + Bicep runner (2 weeks)
**Owner:** Wizard team
**Exit:** Wizard `/security-gate` page polls live; deploy button shells out to `az`
- Implement `apps/deploy-wizard/api/src/apex_wizard/bicep_runner.py` (subprocess wrapper around `az deployment group what-if` + `az deployment group create`)
- `/security-gate` page: live polling per gate (Defender, Purview, Entra Agent ID); red gates block render
- `/api/deployments` POST executes the render + what-if + apply flow end-to-end
- Drift detector cron runs daily against Lab tenant
- **Depends on:** Sprints 41–45 (every protocol impl wired)

---

## Sprint detail — First client engagement (47–49)

### Sprint 47 — Lab tenant for first client (2 weeks)
**Owner:** Engagement lead + Tenant SRE
**Exit:** RC-E2E-03 deployed to client's Lab tenant, both featured scenarios run end-to-end
- Onboard the client's Azure subscription: assign roles to Deloitte deployment principal
- Operator runs Pre-deployment Security Gate; remediates per checklist
- Wizard deploys APEX-M platform Bicep + RC-E2E-03 service Bicep + agent fleet
- Smoke tests: synthetic cold-chain excursion event, synthetic markdown batch
- Marisol Reyes + Daniel Chen personas exercise HITL on Lab data
- **Use case:** clone `services/rc/RC-E2E-03/use-cases/_default/` to `<client>/`; populate `client_approved_architecture` per their CAB

### Sprint 48 — Wave 2 Pilot for first client (2 weeks)
**Owner:** Engagement lead
**Exit:** Production substrate live with HITL on real client data, decisions write to Purview Audit
- Promote use case from `lab` to `prod` substrate
- Pre-deployment Security Gate run on prod tenant (every gate must be green)
- 3-month margin-attribution shadow window starts
- KPI Power BI dashboard goes live for Daniel Chen
- **Depends on:** Sprint 47 + client's W2 commercial envelope signed

### Sprint 49 — Phase J migrations land (2 weeks)
**Owner:** Platform team
**Exit:** Six deprecation notes (DEP-001 through DEP-006) move from paper to migrated code
- DEP-001: switch RC-E2E-03 Eventhouse access from custom MCP to RTI remote MCP
- DEP-002: migrate The Pricer's similarity search to in-data-tier `ai_embeddings`
- DEP-003: replace custom Debezium parser in Bronze ingest with Eventstream DeltaFlow
- DEP-004: HITL alert trigger moves from agent runtime to Eventstream Activator destination
- DEP-005: bespoke prompt-injection regex retired; Defender for AI is the only path
- DEP-006: APEX audit-row demoted to overlay; Purview Audit is system of record (already done in code via `is_primary` flag; this sprint validates production tenant emits to Purview correctly)
- Roadmap.md amendments per ADR-003 + DEP-006

---

## Sprint detail — RC service expansion (50–56)

Each sprint takes one RC service through the same flow: agent prompts authored → MCP tools wired → HITL config → Lab deploy → smoke test → Wave 2 promotion. Effort scales with agent count and PII tier.

### Sprint 50 — RC-E2E-04 Loyalty Churn (3 weeks — Tier-3 PII complications)
- 5-agent fleet: Analyst, Demand Checker, Finance Lead, Operations Lead, Briefer
- Tier-3 PII unlock at HITL (re-identification of customer)
- Just-in-time PII unlock pattern per Deployment Guide §5.2.2
- Smoke: top-tier loyalty churn cohort scoring + winback offer above threshold

### Sprint 51 — RC-E2E-05 On-Shelf Availability (2 weeks)
- 4-agent fleet: Analyst, Demand Checker, Operations Lead, Briefer
- Triage-and-decide workflow (shelf-gap event → priority → task dispatch)
- Smoke: synthetic OOS event → associate task list

### Sprint 52 — RC-E2E-07 Returns-Fraud Detection (3 weeks — Tier-3 PII + adaptive HITL)
- 4-agent fleet: Analyst, Fraud Specialist, Operations Lead, Briefer
- Adaptive HITL threshold (auto-clear < 0.4 score · escalate > 0.7)
- Tier-3 PII unlock at hold-decision moment
- Smoke: synthetic fraud-ring pattern match

### Sprint 53 — RC-E2E-09 Product Tracking (FSMA 204) (2 weeks — cross-Service consumer for RC-E2E-03)
- 3-agent fleet: Analyst, Compliance Specialist, Briefer
- Cross-Service MCP — `rc_e2e_09.get_lot_provenance` consumed by RC-E2E-03 cold-chain
- SCML.Lot ownership: RC-E2E-09 writes; RC-E2E-03 reads via MCP only
- Smoke: recall traceability panel + cold-chain excursion now reads real lot provenance

### Sprint 54 — RC-E2E-06 Workforce Operations (2 weeks — catalog-only; built only if a client prioritizes)
- Decision: promote a workforce-ops scenario to featured in the xlsx (if applicable to engagement)
- 4-agent fleet authoring + MCP tools

### Sprint 55 — RC-E2E-08 Marketing & Growth (2 weeks — catalog-only; built only if a client prioritizes)
- Decision: promote a marketing scenario to featured (uplift modeling / campaign mix)
- 3-agent fleet authoring

### Sprint 56 — RC W3 Fusion (3 weeks)
- Wire fusion edges in `apex-m/infra/bicep/blueprints/w3-scale-fuse.bicep`
- LEDGER feedback loop: Pricing Agent reads approved-decision episodic memory (Services Guide §25.8)
- Power BI Direct Lake unified KPI dashboard across the 5 deployed RC services
- Perishables Economics Mesh = cold-chain × loyalty-churn × lot provenance fusion

---

## Sprint detail — Second client + HLS kickoff (57+)

### Sprint 57 — Second client engagement Lab tenant (2 weeks)
- Repeats the Sprint 47 pattern; second client's adapter selections may differ from first
- Validates the use-case-driven model handles real architectural variance

### Sprint 58 — HLS practice kickoff (4 weeks)
**Major effort** — clone the RC pattern for HLS practice
- Author `services/hls/_build-status.yaml` per RC's pattern
- Author `docs/APEX - Design and Build/HLS-Build-Plan.md`
- HLS-E2E-02 (Clinical Care · Claims Denial Prevention + CDS Oncology) — Tier-4 PHI throughout
- Tier-4 PHI handling: dual-control unlock at HITL per Deployment Guide §7.3
- Cross-walk APEX classification with FHIR sensitivity labels per ADR-005

### Sprint 59 — HLS-E2E-04 Prior Authorization (3 weeks)
- 5-agent fleet: Analyst, Clinical Reviewer, Finance Lead, Operations Lead, Briefer
- Triage-and-decide workflow

### Sprint 60+ — Continue HLS, then start ER / AXLE / TH / TMT / ICE
- Each practice gets its own build plan + sprint sequence
- Multi-practice deployment learnings feed back into framework Roadmap.md

---

## APEX-G / APEX-A port — on-demand

Per [Multi-Cloud Port Plan](../apex-core/Multi-Cloud-Port-Plan.md), neither variant is on a fixed sprint schedule. The trigger is a Deloitte client commissioning a non-Microsoft variant deployment as their primary substrate.

When commissioned, the port follows a discrete project plan (estimated 8–10 sprints from kickoff to first client deploy):

- **Port-G/A.1** — Concrete protocol implementations (10 protocols against the variant's services)
- **Port-G/A.2** — IaC modules (Terraform for GCP / CloudFormation for AWS)
- **Port-G/A.3** — Variant book set (6 books cloned + adapted)
- **Port-G/A.4** — Wizard render adapter
- **Port-G/A.5** — Pre-deployment Security Gate equivalent
- **Port-G/A.6** — Per-service catalog port

Existing Sprint cadence pauses RC build for the engagement team conducting the port. Independence checkpoints apply to every port commit.

---

## Cross-cutting streams (always running)

These run *in parallel* with sprints and don't block any individual sprint:

| Stream | Cadence | What |
|---|---|---|
| **Microsoft platform watch** | Weekly | Watch Microsoft Learn for new GA capability; raise ADRs when something supersedes APEX scope |
| **Adapter implementations** | Per engagement | When a client's CAB approves an adapter, build the concrete impl off the Phase 0 stub |
| **Independence reviews** | Per engagement | Per-adapter Independence consultation before any prod deploy |
| **Drift detection** | Daily cron | Wizard's drift detector runs against every deployed tenant; alerts on divergence |
| **Documentation** | Continuous | Books, READMEs, ADRs update as decisions change |

---

## Commercial wave alignment

Each sprint maps to the engagement's commercial wave per Sellers Guide:

| Sprint number | Engagement wave | Commercial posture |
|---|---|---|
| 30–46 | Pre-engagement (framework + platform) | Internal Deloitte investment |
| 47 | W1 Foundation + W2 Pilot kickoff | Fixed-price W2 contract begins |
| 48 | W2 Pilot live | Fixed-price W2 burns down |
| 49–55 | W2 Pilot + W2 expansion (additional services) | W2 fixed-price; possibly outcome-based add-ons |
| 56 | W3 Scale & Fuse | Outcome-based W3 with margin-share trigger |
| 57+ | Second client / additional practices | Repeats per engagement commercial envelope |

---

## How to update this plan

1. Sprint completes → mark exit criteria green in commit message; update [`services/rc/_build-status.yaml`](../../services/rc/_build-status.yaml) for items in scope
2. New sprint commits → append to this doc with sprint number, owner, exit criteria, depends-on
3. Sprint slips → annotate with new target; **do not** renumber subsequent sprints (reuse numbers post-completion only)
4. New ADR or deprecation surfaces → add to its respective folder + reference here

The wizard's Roadmap page reflects this plan via `services/rc/_build-status.yaml`. Future sprints (41+) get added to the YAML when they're committed; until then the wizard shows them as "future / planned".

---

## Open scoping questions (track per engagement)

Per ADR-004 (region coverage) and the Pre-deployment Security Gate, these vary per client and are decided at engagement kickoff (Sprint 47 / 57 / etc.):

- Tenant region (Foundry-supported tier vs feature-constrained tier vs no-Foundry-support tier)
- ACR public-egress posture (per ADR-001 — Foundry hosted vs Container Apps fallback)
- Adapter set in scope (per CAB approval — driven from `client_approved_architecture` in the use case)
- Substrate tier per wave (lab/dev/stage/prod/pilot/ga)
- Commercial envelope (W2 fixed-price scope, W3 outcome-based threshold)

These are engagement decisions, not framework decisions. The framework is sprint-agnostic to them.
