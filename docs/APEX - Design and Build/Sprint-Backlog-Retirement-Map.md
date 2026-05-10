# Sprint Backlog Retirement Map

**Audience:** Engagement leads, sprint planners, the wizard's Roadmap page, anyone tracking "is the backlog actually being retired?"
**Purpose:** Priority-ordered orchestration of Sprints 30–49 with explicit `BL.C.*` / `BL.P.*` retirement claims per sprint. Closes the loop between [`Roadmap.md`](Roadmap.md), [`Sprint-Plan.md`](Sprint-Plan.md), [`Sprint-Execution-Order.md`](Sprint-Execution-Order.md), and [`services/rc/_build-status.yaml`](../../services/rc/_build-status.yaml).

**Reading order:** if you've never seen this file before, start with [§1](#1-tldr--retirement-snapshot). If you're sprint-planning, jump to [§3](#3-priority-ordered-sprint-sequence). If you're reconciling an item back to its sprint, use [§5](#5-reverse-index--every-open-blp-mapped-to-the-sprint-that-retires-it).

---

## 1. TL;DR — retirement snapshot

The roadmap has **259 backlog items** (64 `BL.C.*` + 195 `BL.P.*`). **159 are already done** (95 `BL.P.*` complete from Sprints 1–11 framework work + 64 `BL.C.*`); **100 BL.P.\* are open**.

Sprints 30–49 will retire **14 BL.P.\* items** end-to-end (the ones that depend on the RC platform stack actually running). After Sprint 49, the residual is **86 BL.P.\* items**, all deferred for clear engagement-driven or out-of-RC-scope reasons:

| Residual category | Count | Why deferred |
|---|---|---|
| Other-practice agent catalogs (BL.P.59–64) | 6 | Sprint 58+ HLS / ER / AXLE / TMT / TH / ICE practice kickoff |
| Other-practice service catalogs (BL.P.111–116) | 6 | Same — clones the RC pattern post-Sprint 49 |
| Other-practice reference deployments (BL.P.118–121) | 4 | Same |
| SOR / SaaS adapters (BL.P.95–109) | 15 | Per-engagement; retired only when a client's CAB approves the adapter |
| Standards catalog & licence (BL.P.137–138) | 2 | Continuous standards-track work, not sprint-bound |
| ISO 8000 master-data quality (BL.P.154) | 1 | Per-engagement |
| Message-format translators (BL.P.155–160) | 6 | Per-engagement; some replaced by Microsoft Industry Cloud connectors |
| Cross-standard translators (BL.P.162–165) | 4 | Per-engagement |
| Protocol adapters OPC UA / IEC 61850 / J1939 (BL.P.166–168) | 3 | Per-engagement; AXLE / ICE / ER specific |
| Registries / playbooks / appendices (BL.P.122–133) | 12 | Continuous publishing track, not sprint-bound |
| Scenario Library extensions (BL.P.169–185) | 17 | Sprint 28+ separate parallel track (Sellers Guide / cinematic) |
| Communication artifacts (BL.P.186–195) | 10 | Sprint 29+ separate parallel track |
| **Total residual after Sprint 49** | **86** | None of these block first-client RC deploy |

So **Sprints 30–49 retire every BL.P.\* item that depends on the RC platform stack actually running.** The 86 residual are (a) other-practice clones, (b) per-engagement adapters, or (c) parallel publishing/standards tracks.

After Sprint 49 closes: **173 of 259 = 66.8%** of total backlog retired.

---

## 2. The four-wave critical path

```
WAVE A (~6 weeks parallel)  →  WAVE B (~4 weeks)  →  WAVE C (~4 weeks)  →  WAVE D (~14 weeks)
Foundation + SDK wiring        Wizard + agent prep    First client deploy    RC service expansion
                                                                              + Phase J migrations

Sprints 30 · 41 · 42 · 43      Sprints 32 · 46        Sprints 33 · 47        Sprints 34 · 35 · 37
        44 · 45                                                               39 · 40 · 48 · 49
```

Wave A retires the **platform-trust** backlog (Fabric capacity, Purview, identity).
Wave B retires the **wizard + RC agent** backlog (RC agent catalog drafts).
Wave C retires the **first-deploy** backlog (Big Box reference deployment).
Wave D retires the **RC service-catalog** backlog and the **Phase J deprecations**.

See [`Sprint-Execution-Order.md`](Sprint-Execution-Order.md) for the full dependency graph and parallelization matrix.

---

## 3. Priority-ordered sprint sequence

Each row below answers four questions:

1. **What ships?** — sprint exit criterion
2. **What's the dependency?** — which sprint(s) must land first
3. **What backlog does it retire?** — explicit `BL.C.*` / `BL.P.*` IDs (or DEP-NNN deprecation IDs)
4. **What still doesn't move?** — residual not retired by this sprint

Status is sourced from [`services/rc/_build-status.yaml`](../../services/rc/_build-status.yaml) and surfaces in the wizard's Roadmap page.

### Wave A — Foundation + SDK wiring (parallel-streamable, ~6 weeks)

#### Priority 1 · Sprint 30 — RC W1 Foundation
- **Owner:** Data SRE
- **Depends on:** nothing — kickoff today
- **Status:** in_progress (Bicep authored; Lab apply pending)
- **Exit:** Lab tenant + Fabric capacity + medallion (Bronze · Silver · 6 RC-E2E-03 Gold marts) provisioned. Smoke read of `g_excursion_decision_panel` succeeds with operator OBO.
- **Retires:**
  - `BL.P.91` — F-SKU capacity provisioning IaC module *(Roadmap text says "Terraform" — Sprint 30 retires this with the Bicep `apex-m/infra/bicep/platform/fabric.bicep` module, which is the APEX-M canonical IaC per ADR-006 platform direction.)*
  - `BL.P.92` — OneLake workspace provisioning via Fabric REST API *(deploymentScripts in `fabric.bicep` issue Fabric REST `POST /workspaces` for primary `rc-canonical` + per-service consumer workspaces.)*
  - `BL.P.93` — Capacity-pattern templates *(single + dev-prod split codified in `apex-m/infra/bicep/platform/main.bicep` `provisionFabric` flag; per-workload isolation lands fully in Sprint 43.)*
  - `BL.P.94` — OneLake shortcut provisioning *(ADLS shortcuts to RC Bronze sources; S3 / GCS / Dataverse shortcuts ship in Sprint 43 when DataLakeFabric goes prod.)*
- **Doesn't retire:** the **read path** through the medallion — that's Sprint 43.
- **Validation:** `az deployment group what-if` returns 0 changes after a clean apply; Fabric REST `GET /workspaces?$filter=startswith(displayName,'rc-')` returns the expected 8 workspaces; `notebooks/silver/transform_template.py` against `SCML.Inventory` lands in Bronze.

#### Priority 1 · Sprint 41 — Entra Agent ID production wiring
- **Owner:** Identity SRE
- **Depends on:** nothing — parallel with Sprint 30
- **Status:** in_progress (MSAL OBO wired; integration tests authored; Lab tenant pending)
- **Exit:** `apex_m.identity_entra.AgentIdentityProviderEntra` makes real Microsoft Graph calls in Lab. The 6 integration tests at `apex-m/tests/integration/test_identity_entra.py` pass against a real Lab Entra tenant.
- **Retires:** *(Production posture for Sprint 10 items)*
  - **`BL.P.53` — production posture** — `EntraProvisioningProvider` mock landed Sprint 10; this sprint validates the production `AgentIdentityProviderEntra` against a real tenant.
  - **`BL.P.57` — production posture** — response signing upgraded from HMAC-SHA256 mock to RSA + Key Vault key-id binding via the real OBO-issued token's `kid`.
- **Doesn't retire:** runtime hosting of the agent — that's Sprint 42.
- **Validation:** integration test `test_create_blueprint_idempotent` succeeds; `identity.bicep` deploymentScripts creates `apex-m-tenant-root` blueprint via Microsoft Graph.

#### Priority 2 · Sprint 42 — Foundry runtime production wiring
- **Owner:** Runtime SRE
- **Depends on:** Sprint 41
- **Exit:** `apex_m.runtime_foundry.AgentRuntimeFoundry` deploys + invokes a real hosted agent; the 5 Microsoft Agent Framework canonical patterns wired per ADR-006.
- **Retires:** *(Production posture for Sprint 11 items)*
  - **`BL.P.65` — production posture** — 47 archetypes catalog now resolves to live Agent Framework workflow execution (was mock).
  - **`BL.P.66` — production posture** — Sequential / Concurrent / Handoff / Group Chat / Magentic primitives are façades over `AgentWorkflowBuilder.Build*` (was mock).
  - **`BL.P.67` — production posture** — orchestration manifest runtime delegates to Agent Framework workflow execution (was mock).
- **Doesn't retire:** practice-specific orchestrations (RC's 5) — those are Sprint 32 + 34 + 35 + 37 + 39.
- **Validation:** integration test deploys The Pricer for `rc-cold-chain-excursion-mid-shift`, invokes with a synthetic excursion event, gets a structured response.

#### Priority 3 · Sprint 43 — Fabric DataLake production wiring
- **Owner:** Data SRE
- **Depends on:** Sprint 30 + Sprint 41
- **Exit:** OBO passthrough to SQL analytics endpoint works; OneLake user-identity-mode honored end-to-end.
- **Retires:**
  - **`BL.P.93` — completion** — per-workload-isolation pattern (per-service consumer workspace + cross-workspace shortcut) proven on Lab.
  - **`BL.P.94` — completion** — non-ADLS shortcut provisioning (S3 / GCS / Dataverse) for adapter-driven Bronze sources.
- **Validation:** smoke writes to Bronze `SCML.Inventory`; query Silver via operator-scoped OBO; verify OneLake security policy denies non-operator reads.

#### Priority 3 · Sprint 44 — Purview Audit + Sensitivity Classifier production
- **Owner:** Governance SRE
- **Depends on:** Sprint 42
- **Exit:** Real Purview Audit emits + sensitivity-label propagation through Foundry RAG end-to-end.
- **Retires:** *(the entire §2.10 Purview Trust Architecture block)*
  - **`BL.P.85`** — Classification registration pipeline (YAML → Purview)
  - **`BL.P.86`** — Lineage capture: SOR → Bronze → Silver → Gold → MCP tool → Agent → Audit row
  - **`BL.P.87`** — DLP policies (label-based redaction across surfaces)
  - **`BL.P.88`** — WORM retention policies (7y / 10y HLS / permanent legal-hold)
  - **`BL.P.89`** — Unified Catalog business-glossary registration
  - **`BL.P.90`** — Classification propagation chain (Silver → Gold → semantic model → Copilot → agent output)
- **Six items in one sprint** because they all share the same production wiring point — `apex_m.audit_purview.AuditLedgerPurview` + `apex_m.classifier_purview.SensitivityClassifierPurview` against the Compliance Audit Graph + Information Protection labels APIs.
- **Validation:** push a T3 entity to Bronze; query through the medallion → Foundry RAG → agent output; verify EXTRACT label propagated to the agent's response and to the audit row.

#### Priority 3 · Sprint 45 — Defender threat protection production
- **Owner:** Security SRE
- **Depends on:** Sprint 41 + Sprint 42
- **Exit:** Pre-deployment Security Gate items #1, #2, #9 turn green for Lab.
- **Retires:** *(Pre-deployment Security Gate items — see [`Pre-deployment-Security-Gate.md`](Pre-deployment-Security-Gate.md))*
  - **PSG-#1** — Defender for Cloud CSPM AI security posture
  - **PSG-#2** — Defender for AI services threat protection
  - **PSG-#9** — AI Model Security CI scan on every agent image
- **Doesn't retire:** any `BL.P.*` directly — these gates are operational not architectural; PSG green is the unblocker for Sprint 47 first-client deploy.
- **Validation:** simulated jailbreak prompt blocked by Prompt Shields; Defender for Cloud surface shows green for AI security posture.

### Wave B — Wizard live + agent prep (~4 weeks)

#### Priority 4 · Sprint 32 — RC-E2E-03 agent implementation
- **Owner:** Agent designers
- **Depends on:** Sprint 41 + Sprint 42
- **Exit:** All 6 agent prompts authored (Analyst / Demand Checker / Pricer / Finance Lead / Operations Lead / Briefer); 3 MCP tools wired; HITL thresholds in Key Vault.
- **Retires:** *(partial — RC-E2E-03 is one of seven RC services)*
  - **`BL.P.58` — partial** — RC agent catalog gains 6 production-ready agents (target ~50; this sprint contributes 6).
  - **`BL.P.68` — partial** — Practice-specific orchestrations: `RC-E2E-03=Magentic` binding produces a runnable Agent Framework workflow (was mock binding).
  - **`BL.P.110` — partial** — RC service catalog gains 1 production-ready service (target 7 RC services).
- **Doesn't retire:** the deploy + smoke — that's Sprint 33.
- **Validation:** unit tests on each prompt; MCP tool contract tests; HITL threshold smoke against an in-memory queue.

#### Priority 4 · Sprint 46 — Wizard live + Bicep runner
- **Owner:** Wizard team
- **Depends on:** Sprints 30 + 41 + 42 + 43 + 44 + 45 (every protocol impl wired)
- **Exit:** `bicep_runner.py` shells out to `az`; `/security-gate` polls live; deploy button works end-to-end against Lab; drift detector cron runs daily.
- **Retires:** *(no `BL.P.*` directly — wizard is platform infrastructure)*
  - The wizard itself was scaffolded in Sprint 46a (already shipped this session — `apps/deploy-wizard/`). This sprint wires it to live Microsoft APIs, which **enables** Sprint 33 + Sprint 47 to retire `BL.P.117`.
- **Validation:** `POST /api/deployments` triggers `az deployment group what-if`, returns the diff in the wizard UI, then `az deployment group create` executes on operator confirm.

### Wave C — First deploy + first client (~4 weeks)

#### Priority 5 · Sprint 33 — RC-E2E-03 deploy + smoke (Lab)
- **Owner:** Engagement lead + Tenant SRE
- **Depends on:** Sprint 30 + Sprint 32 + Sprint 46
- **Exit:** RC-E2E-03 deployed to Lab tenant via wizard; cold-chain excursion + dynamic markdown smoke tests pass with audit row in Purview.
- **Retires:**
  - **`BL.P.117` — partial (Lab phase)** — Big Box Store reference deployment is live on Lab with 1 of 5 featured RC services (RC-E2E-03). Full Big Box deployment lands in Sprint 40 when all 5 services are deployed.
- **Validation:** synthetic excursion event → HITL approval → audit row signed + landed in Purview Audit Graph; Daniel Chen approves a markdown batch in Power BI; LEDGER row captured.

#### Priority 5 · Sprint 47 — First client engagement Lab tenant
- **Owner:** Engagement lead + Tenant SRE
- **Depends on:** Sprint 33 + per-engagement Independence sign-off
- **Exit:** First client's Lab tenant has RC-E2E-03 running; cloned use case from `_default/`; `client_approved_architecture` populated per their CAB.
- **Retires:** *(no `BL.P.*` directly — first-client run is operational)*
  - This sprint **proves** that `BL.P.117` extends from Lab to a real client tenant.
- **Validation:** Pre-deployment Security Gate green on client tenant; Marisol Reyes + Daniel Chen exercise HITL on Lab data; both smoke tests pass.

### Wave D — RC service expansion + first client live (~14 weeks)

#### Priority 6 · Sprint 34 — RC-E2E-04 Loyalty Churn (Tier-3 PII)
- **Depends on:** Sprint 33 (per-service Bicep template proven)
- **Retires:** *(partial)*
  - **`BL.P.58` — partial** — +5 agents (Analyst / Demand Checker / Finance Lead / Operations Lead / Briefer)
  - **`BL.P.68` — partial** — `RC-E2E-04=Sequential` binding production-ready
  - **`BL.P.110` — partial** — +1 RC service (now 2 of 7)

#### Priority 6 · Sprint 35 — RC-E2E-05 On-Shelf Availability
- **Depends on:** Sprint 33
- **Retires:** *(partial)*
  - **`BL.P.58` — partial** — +4 agents
  - **`BL.P.68` — partial** — `RC-E2E-05=Sequential` binding production-ready
  - **`BL.P.110` — partial** — +1 RC service (3 of 7)

#### Priority 6 · Sprint 37 — RC-E2E-07 Returns-Fraud (Tier-3 PII + adaptive HITL)
- **Depends on:** Sprint 33
- **Retires:** *(partial)*
  - **`BL.P.58` — partial** — +4 agents
  - **`BL.P.68` — partial** — `RC-E2E-07=Concurrent` binding production-ready
  - **`BL.P.110` — partial** — +1 RC service (4 of 7)

#### Priority 6 · Sprint 39 — RC-E2E-09 Product Tracking (FSMA 204)
- **Depends on:** Sprint 33
- **Retires:** *(partial)*
  - **`BL.P.58` — partial** — +3 agents
  - **`BL.P.68` — partial** — `RC-E2E-09=Handoff` binding production-ready
  - **`BL.P.110` — partial** — +1 RC service (5 of 7; RC-E2E-06 + RC-E2E-08 stay catalog-only)

#### Priority 7 · Sprint 40 — RC W3 Fusion (cross-service composition)
- **Depends on:** Sprints 33 + 34 + 35 + 37 + 39
- **Retires:** *(completion)*
  - **`BL.P.58` — completion (drafts: 22+ agents authored across RC fleet)** — full RC agent catalog at production-ready status; remaining catalog rows for RC-E2E-06 + RC-E2E-08 stay catalog-only per engagement priority gate.
  - **`BL.P.68` — completion** — full RC orchestration library proven, fusion edges wired into `w3-scale-fuse.bicep`.
  - **`BL.P.110` — completion** — full RC service catalog at production-ready status.
  - **`BL.P.117` — completion** — full Big Box reference deployment live (5 RC services × first client).
- **Validation:** Perishables Economics Mesh (RC-E2E-03 × RC-E2E-04 × RC-E2E-09) runs end-to-end with LEDGER feedback loop visible in Power BI.

#### Priority 7 · Sprint 48 — First client Wave 2 Pilot live
- **Depends on:** Sprint 47
- **Retires:** *(operational; `BL.P.117` confirmed on prod substrate)*
  - **PSG-all** — every Pre-deployment Security Gate green on prod tenant (operational confirmation, not architectural retirement).
- **Validation:** 3-month margin-attribution shadow window starts; Daniel Chen's Power BI dashboard goes live.

#### Priority 7 · Sprint 49 — Phase J migrations land
- **Depends on:** Sprint 46 (parallel with Sprint 48)
- **Retires:** *(deprecation IDs, not BL.P.*)*
  - **DEP-001** — RC-E2E-03 Eventhouse access switches to RTI remote MCP
  - **DEP-002** — The Pricer similarity search uses Eventhouse `ai_embeddings`
  - **DEP-003** — Bronze CDC migrates to Eventstream DeltaFlow
  - **DEP-004** — HITL alert trigger via Eventstream Activator
  - **DEP-005** — Defender for AI is sole prompt-injection path
  - **DEP-006** — Purview Audit primary verified in prod
- **Validation:** each DEP-NNN's "definition of done" green; Roadmap.md amended per ADR-003 + DEP-006 (already done in code via `is_primary` flag this session).

---

## 4. Cumulative retirement validation

`BL.P.*` items advanced or completed by each sprint, in commit order. "Cumulative completed" = unique IDs whose status is `completion` (i.e., the box flips `[ ]` → `[x]` in `Roadmap.md`).

| After sprint | Items advanced this sprint | Cumulative completed | Notes |
|---|---|---|---|
| Sprint 30 | BL.P.91 ✅ · BL.P.92 ✅ · BL.P.93 (partial) · BL.P.94 (partial) | **2** | 91, 92 close on Sprint 30; 93, 94 wait for Sprint 43 |
| Sprint 41 | BL.P.53 (production posture) · BL.P.57 (production posture) | 2 | Items already `[x]` in v1.2; this sprint validates production wiring |
| Sprint 42 | BL.P.65 (production) · BL.P.66 (production) · BL.P.67 (production) | 2 | Items already `[x]` in v1.2; this sprint validates production wiring |
| Sprint 43 | BL.P.93 ✅ · BL.P.94 ✅ | **4** | |
| Sprint 44 | BL.P.85 ✅ · BL.P.86 ✅ · BL.P.87 ✅ · BL.P.88 ✅ · BL.P.89 ✅ · BL.P.90 ✅ | **10** | Entire §2.10 Purview Trust block lands in one sprint |
| Sprint 45 | (PSG-1, PSG-2, PSG-9 green — no BL.P.\* retirement) | 10 | Operational gate, not architectural retirement |
| Sprint 46 | (wizard infrastructure — enables BL.P.117 retirement in 33 + 47) | 10 | |
| Sprint 32 | BL.P.58 (partial) · BL.P.68 (partial) · BL.P.110 (partial) | 10 | Partials accumulate toward Sprint 40 completion |
| Sprint 33 | BL.P.117 (partial — Lab phase) | 10 | Partial advances toward Sprint 40 completion |
| Sprint 47 | BL.P.117 (partial — first client tenant) | 10 | |
| Sprint 34 | BL.P.58 / 68 / 110 — all advance further | 10 | |
| Sprint 35 | BL.P.58 / 68 / 110 — all advance further | 10 | |
| Sprint 37 | BL.P.58 / 68 / 110 — all advance further | 10 | |
| Sprint 39 | BL.P.58 / 68 / 110 — all advance further | 10 | |
| Sprint 40 | BL.P.58 ✅ · BL.P.68 ✅ · BL.P.110 ✅ · BL.P.117 ✅ | **14** | All four prior partials close together |
| Sprint 48 | (PSG-all green on prod) | 14 | Operational, not architectural retirement |
| Sprint 49 | DEP-001 ✅ · DEP-002 ✅ · DEP-003 ✅ · DEP-004 ✅ · DEP-005 ✅ · DEP-006 ✅ | 14 BL.P.\* + 6 DEP | Separate ID space — Phase J deprecations |

**Net retirement after Sprint 49:** 14 BL.P.* items move `[ ]` → `[x]`, plus 6 DEP-NNN deprecations migrate from paper to code, plus 5 BL.P.* items get production-posture validation (53, 57, 65, 66, 67 — already counted as `[x]` since Sprint 10/11 mock work).

Total backlog progress (BL.C.* + BL.P.*):
- Pre-Sprint 30: **159 / 259 = 61.4%** done
- Post-Sprint 49: **173 / 259 = 66.8%** done

The 5.4-point bump represents the **last meaningful BL.P.\* retirement before HLS practice kickoff** — every remaining open item is either an other-practice clone (covered by Sprint 58+) or a per-engagement adapter (retired only when a client's CAB approves it).

---

## 5. Reverse index — every open BL.P.* mapped to the sprint that retires it

For the 14 items that flip `[ ]` → `[x]` within this 20-sprint window:

| BL.P.* | Title | Retired by sprint | Status post-Sprint 49 |
|---|---|---|---|
| BL.P.58 | RC agent catalog | Sprints 32 · 34 · 35 · 37 · 39 (completion: 40) | ✅ retired (production-ready agents for the 5 featured services) |
| BL.P.68 | Practice-specific orchestrations (RC) | Sprints 32 · 34 · 35 · 37 · 39 (completion: 40) | ✅ retired |
| BL.P.85 | Classification registration pipeline | Sprint 44 | ✅ retired |
| BL.P.86 | Lineage capture (SOR → audit) | Sprint 44 | ✅ retired |
| BL.P.87 | DLP policies | Sprint 44 | ✅ retired |
| BL.P.88 | WORM retention | Sprint 44 | ✅ retired |
| BL.P.89 | Unified Catalog glossary | Sprint 44 | ✅ retired |
| BL.P.90 | Classification propagation chain | Sprint 44 | ✅ retired |
| BL.P.91 | F-SKU capacity IaC module | Sprint 30 (Bicep, not Terraform) | ✅ retired |
| BL.P.92 | OneLake workspace provisioning | Sprint 30 | ✅ retired |
| BL.P.93 | Capacity-pattern templates | Sprints 30 + 43 | ✅ retired |
| BL.P.94 | OneLake shortcut provisioning | Sprints 30 + 43 | ✅ retired |
| BL.P.110 | RC service catalog | Sprints 32 · 34 · 35 · 37 · 39 · 40 | ✅ retired (5 of 7 production-ready; 2 catalog-only by design) |
| BL.P.117 | Big Box reference deployment | Sprints 33 · 47 · 40 | ✅ retired |

For everything else still `[ ]` in `Roadmap.md`, see [§1 residual table](#1-tldr--retirement-snapshot) for the deferral category.

---

## 6. What this means for the Roadmap

After Sprint 49 commits, the following Roadmap.md updates land:

1. The 14 items in §5 above flip from `[ ]` → `[x]` with `*(Sprint NN — production)*` annotations matching the cadence used for completed items.
2. `§3 Progress Snapshot` table updates from 159/259 (61.4%) to 173/259 (66.8%).
3. Residual `[ ]` items keep their deferral annotation (HLS / per-engagement / parallel-track) so the wizard's Roadmap page surfaces "deferred for X" rather than "not started."

The actual flip-the-checkbox work is part of each sprint's exit criterion in [`_build-status.yaml`](../../services/rc/_build-status.yaml) — when `done: true` lands per item, the corresponding Roadmap row updates in the same commit per [Sprint-Plan.md §"How to update this plan"](Sprint-Plan.md).

---

## 7. Open scoping decisions for this orchestration

These don't block the priority order, but they shape sprint scope at kickoff:

- **Two-team vs single-team Wave D** — running 34/35 and 37/39 as parallel pairs cuts Wave D from 14 weeks to ~8. Decision pending engagement staffing.
- **RC-E2E-06 + RC-E2E-08 promotion** — both are catalog-only today. If a client commissions either, promote it from `planned` to `scaffolded` (via `tools/gen_services_tree.py`) and add a featured scenario; otherwise they stay catalog-only and never enter sprint scope. Does NOT change the BL.P.110 retirement claim — completion is "5 of 7 production-ready; 2 catalog-only by design."
- **Wizard self-deployment task** — the wizard itself ships at `apex-m/infra/bicep/control-plane/main.bicep` (authored, not yet deployed). Could go in Sprint 30.7 (alongside foundation) or Sprint 46.5 (when wizard is wired live). Decision pending — neither retires a `BL.P.*`, both unblock first-client UX.
- **Phase J split** — Sprint 49 currently bundles all six DEP-NNN. If a single one slips on its underlying Microsoft GA dependency (e.g., RTI remote MCP not yet GA in client region), split it into Sprint 49.a + 49.b rather than holding the whole sprint.
