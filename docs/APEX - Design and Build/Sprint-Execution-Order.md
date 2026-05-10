# Sprint Execution Order — Dependencies, Waves, and Parallelization

**Audience:** Engagement leads, sprint planners, anyone deciding what to start when
**Purpose:** Makes the dependency graph between sprints explicit and identifies which sprints can run in parallel. Resolves the question *"can we start Sprint 41 if Sprint 30 isn't done?"*

**Reference:**
- [Sprint Plan](Sprint-Plan.md) — the master schedule
- [`services/rc/_build-status.yaml`](../../services/rc/_build-status.yaml) — machine-readable plan, surfaced in the wizard Roadmap page

---

## TL;DR — current state

What's actually done as of this session:

| Status | Scope |
|---|---|
| ✅ **Architecture settled** | Phase 0 (APEX-M/G/A + adapters + protocols), Phase I architecture (mocks + ADRs + book chapters), Phase J deprecation notes (paper) |
| ✅ **Sprint 31 done** | RC service scaffolding — 38 service folders + 36 featured scenarios + 250+ files via `tools/gen_services_tree.py` |
| ⏳ **Sprint 30 NOT started** | RC W1 Foundation — Bicep + Fabric + medallion provisioning of a real Lab tenant (the foundation everything else stands on) |
| ⏳ **Sprints 32–40 NOT started** | RC-E2E-03 agent implementation, per-service expansion, W3 fusion |
| ⏳ **Sprints 41–46 NOT in YAML** | Phase I production wiring — wires real Microsoft SDK calls behind the apex-m mocks |
| ⏳ **Sprint 47 NOT started** | First client engagement |

The mistake was suggesting "Sprint 41 next" without showing that Sprint 30 is also unstarted and is a prerequisite for the production wiring sprints to be testable end-to-end. This doc fixes that.

---

## Dependency graph

```
                        ┌─────────────────────────────────┐
                        │  Phase 0 + Phase I architecture │
                        │  Phase J deprecation notes      │
                        │  (DONE — this session)          │
                        └──────────────┬──────────────────┘
                                       │
                                       ▼
        ┌──────────────────────────────────────────────────────────┐
        │                                                          │
        │  WAVE A — Foundation + SDK wiring (parallel-streamable)  │
        │                                                          │
        │   ┌─────────────────────────┐  ┌─────────────────────┐   │
        │   │ Sprint 30               │  │ Sprint 41           │   │
        │   │ RC W1 Foundation        │  │ Entra Agent ID prod │   │
        │   │ (Data SRE)              │  │ (Identity SRE)      │   │
        │   │ • Lab tenant            │  │ • Microsoft Graph   │   │
        │   │ • Fabric capacity       │  │ • OBO flow          │   │
        │   │ • Bronze/Silver/Gold    │  │ • Blueprints        │   │
        │   │ • Schema landing        │  │ Depends on: nothing │   │
        │   │ Depends on: nothing     │  └──────────┬──────────┘   │
        │   └─────────────┬───────────┘             │              │
        │                 │                         ▼              │
        │                 │              ┌─────────────────────┐   │
        │                 │              │ Sprint 42           │   │
        │                 │              │ Foundry runtime     │   │
        │                 │              │ (Runtime SRE)       │   │
        │                 │              │ Depends on: 41      │   │
        │                 │              └──────────┬──────────┘   │
        │                 │                         │              │
        │                 ▼                         ▼              │
        │   ┌─────────────────────────┐  ┌─────────────────────┐   │
        │   │ Sprint 43               │  │ Sprint 44           │   │
        │   │ Fabric DataLake prod    │  │ Purview Audit prod  │   │
        │   │ (Data SRE)              │  │ (Governance SRE)    │   │
        │   │ Depends on: 30 + 41     │  │ Depends on: 42      │   │
        │   └─────────────┬───────────┘  └──────────┬──────────┘   │
        │                 │                         │              │
        │                 │              ┌──────────▼──────────┐   │
        │                 │              │ Sprint 45           │   │
        │                 │              │ Defender Threat     │   │
        │                 │              │ (Security SRE)      │   │
        │                 │              │ Depends on: 41 + 42 │   │
        │                 │              └──────────┬──────────┘   │
        │                 │                         │              │
        └─────────────────┼─────────────────────────┼──────────────┘
                          │                         │
                          ▼                         ▼
                  ┌─────────────────────────────────────┐
                  │ WAVE B — Wizard live + Service prep │
                  │                                     │
                  │  Sprint 46 — Wizard live + Bicep    │
                  │  runner + security gate polling     │
                  │  Depends on: all of 41–45 + 30      │
                  │                                     │
                  │  Sprint 32 — RC-E2E-03 prompts +    │
                  │  MCP tools (parallel with 46)       │
                  │  Depends on: 41 + 42                │
                  └─────────────────┬───────────────────┘
                                    │
                                    ▼
                  ┌─────────────────────────────────────┐
                  │ WAVE C — First deploy + smoke test  │
                  │                                     │
                  │  Sprint 33 — RC-E2E-03 deploy to    │
                  │  Lab + smoke test cold-chain        │
                  │  Depends on: 30 + 32 + 46           │
                  │                                     │
                  │  Sprint 47 — First client Lab tenant│
                  │  Depends on: 33 + Independence sign-off
                  └─────────────────┬───────────────────┘
                                    │
                                    ▼
                  ┌─────────────────────────────────────┐
                  │ WAVE D — RC service expansion       │
                  │                                     │
                  │  Sprints 34–39 — Per-service impl   │
                  │  (can parallelize across services)  │
                  │  Depends on: 33 (per-service Bicep  │
                  │  template proven)                   │
                  │                                     │
                  │  Sprint 40 — RC W3 Fusion           │
                  │  Depends on: 33–39 done             │
                  └─────────────────┬───────────────────┘
                                    │
                                    ▼
                  ┌─────────────────────────────────────┐
                  │ WAVE E+ — Second client + HLS       │
                  │  Sprint 48 — second client          │
                  │  Sprint 49 — Phase J migrations     │
                  │  Sprint 50+ — HLS practice kickoff  │
                  └─────────────────────────────────────┘
```

---

## Wave-by-wave detail

### WAVE A — Foundation + SDK wiring (~6 weeks, parallel-streamable)

**Six sprints, five different specialist roles, can run in parallel.**

| Sprint | Owner role | Depends on | Touches | Outcome |
|---|---|---|---|---|
| **30** RC W1 Foundation | Data SRE | nothing | `apex-m/infra/bicep/` + Fabric REST + Purview | Lab tenant + medallion + Bronze sources landed |
| **41** Entra Agent ID prod | Identity SRE | nothing | `apex_m.identity_entra` + Microsoft Graph | Real blueprint provisioning + OBO works |
| **42** Foundry runtime prod | Runtime SRE | 41 | `apex_m.runtime_foundry` + `azure-ai-projects` SDK | Real hosted-agent deploy + invoke works |
| **43** Fabric DataLake prod | Data SRE | 30 + 41 | `apex_m.data_lake_fabric` + Fabric SQL endpoint | Real OneLake user-identity-mode reads work |
| **44** Purview Audit + Classifier prod | Governance SRE | 42 | `apex_m.audit_purview` + Purview Audit Graph | Real audit rows emit, sensitivity labels propagate |
| **45** Defender Threat prod | Security SRE | 41 + 42 | `apex_m.threat_defender` + Content Safety SDK | Prompt shields + DSPM for AI live |

Each sprint hits the *same* APEX-Core protocol's apex-m concrete impl that the architecture session already settled. Mocks already pass `isinstance(impl, Protocol)` — the production wiring just swaps in the real SDK.

**Critical path:** 41 → 42 → 44 → 45. Sprint 30 runs in parallel; Sprint 43 joins when both 30 and 41 land.

**Wave A duration:** 6 weeks if Wave A staffs the 5 SRE roles in parallel; 12 weeks if staffed serially.

### WAVE B — Wizard live + RC-E2E-03 prep (~4 weeks)

| Sprint | Owner | Depends on | Outcome |
|---|---|---|---|
| **46** Wizard live | Wizard team | All of 41–45 + 30 | `bicep_runner.py` shells out to `az`; `/security-gate` polls live; deploy button works end-to-end |
| **32** RC-E2E-03 agent implementation | Agent designers | 41 + 42 | The Pricer + 5 other agent prompts authored; MCP tools wired |

These two sprints can run in parallel; both feed Wave C.

**Wave B duration:** 4 weeks.

### WAVE C — First deploy + first client (~4 weeks)

| Sprint | Owner | Depends on | Outcome |
|---|---|---|---|
| **33** RC-E2E-03 deploy + smoke | Engagement lead + tenant SRE | 30 + 32 + 46 | RC-E2E-03 deployed to Lab tenant via wizard; cold-chain smoke test passes end-to-end |
| **47** First client Lab tenant | Engagement lead | 33 + per-engagement Independence sign-off | First client engagement begins; cloned use case from `_default` |

**Wave C duration:** 4 weeks.

### WAVE D — RC service expansion (~14 weeks)

Sprints 34–39 (per-service implementation) can parallelize across services since each operates on its own service code. Sprint 40 (W3 Fusion) gates on all RC services being deployed.

| Sprint | Service | Effort |
|---|---|---|
| **34** | RC-E2E-04 Loyalty Churn (Tier-3 PII) | 3 weeks |
| **35** | RC-E2E-05 OSA | 2 weeks |
| **37** | RC-E2E-07 Returns Fraud (Tier-3 PII + adaptive HITL) | 3 weeks |
| **39** | RC-E2E-09 Product Tracking (FSMA 204) | 2 weeks |
| **36** | RC-E2E-06 Workforce Ops *(catalog only)* | gated on engagement priority |
| **38** | RC-E2E-08 Marketing & Growth *(catalog only)* | gated on engagement priority |
| **40** | RC W3 Fusion (cross-service composition) | 3 weeks |

Two parallel teams could run Sprints 34/35 and 37/39 concurrently, then converge for Sprint 40.

**Wave D duration:** 14 weeks serially; 7–8 weeks with two parallel agent-design teams.

### WAVE E — Second client + Phase J migrations (~6 weeks)

| Sprint | Scope |
|---|---|
| **48** Second client engagement Lab tenant | Validates use-case-driven model handles real architectural variance |
| **49** Phase J migrations | DEP-001 through DEP-006 move from paper to migrated code (RTI MCP, in-data-tier embeddings, DeltaFlow, Activator, Defender, Purview-as-system-of-record) |

### WAVE F+ — HLS practice kickoff and beyond

Per existing [Sprint Plan §57+](Sprint-Plan.md#sprints-57-second-client--hls-kickoff). HLS / ER / AXLE / TH / TMT / ICE practices clone the RC pattern.

---

## Recommended kick-off order

### Option 1 — Maximum parallelism (recommended for staffed engagement)

**Day 1, parallel:**
- Sprint 30 (Data SRE) — `az login` to Lab subscription, run `apex-m/infra/bicep/blueprints/w1-foundation.bicep`, validate Fabric capacity
- Sprint 41 (Identity SRE) — wire `azure-identity` + httpx in `apex_m.identity_entra`, integration test against real Lab Entra tenant

**Day 1 + 2 weeks:**
- Sprint 42 starts (Runtime SRE) when Sprint 41 lands
- Sprint 43 starts (Data SRE — same person rotates from Sprint 30) when 30 + 41 both landed

**Day 1 + 4 weeks:**
- Sprint 44 (Governance SRE) when Sprint 42 lands
- Sprint 45 (Security SRE) in parallel
- Sprint 32 (Agent designers) starts in parallel — author prompts against the now-functional Sprints 41 + 42

**Day 1 + 8 weeks:**
- Sprint 46 (Wizard team) — wires bicep_runner + security gate live polling
- Sprint 33 (Engagement lead + tenant SRE) — first deploy + smoke

**Total to first deploy:** ~10–12 weeks with full parallelism.

### Option 2 — Sequential (if staffing is constrained)

Run sprints serially in critical-path order:

```
30 → 41 → 42 → 43 → 44 → 45 → 46 → 32 → 33 → 47
```

That's 10 sprints × 2 weeks = ~20 weeks to first client deploy.

### Option 3 — Hybrid (the realistic case)

**Phase 1 (4 weeks)** — Sprints 30 + 41 in parallel (two SREs)
**Phase 2 (6 weeks)** — Sprints 42 + 43 + 44 + 45 with overlap (rotating SRE assignments)
**Phase 3 (4 weeks)** — Sprints 46 + 32 in parallel
**Phase 4 (2 weeks)** — Sprint 33
**Phase 5 (2 weeks)** — Sprint 47 first client deploy

**Total:** ~18 weeks with 3 SREs rotating through the specialist roles.

---

## What "starting Sprint 41" actually entails

Concretely, kicking off Sprint 41 (production Entra Agent ID wiring) means:

1. **Provision Entra access in Lab tenant** — Application.ReadWrite.All + AgentIdentity.ReadWrite.All on the deployment principal
2. **Wire the SDK calls** — replace `MockAgentIdentityProviderEntra` consumers with `AgentIdentityProviderEntra` (production). Lazy-imports of `azure-identity` + `httpx` already in the apex-m module from the architecture commit.
3. **Implement OBO flow** — currently raises NotImplementedError; production sprint adds the real OAuth 2.0 OBO exchange per [Microsoft identity platform docs](https://learn.microsoft.com/entra/identity-platform/v2-oauth2-on-behalf-of-flow)
4. **Integration tests** against real Entra Lab tenant — idempotent blueprint upsert, identity provision, revoke, list — exercising every method on the protocol
5. **Verify Bicep deployment script** in `apex-m/infra/bicep/platform/identity.bicep` runs against the Lab subscription and creates the `apex-m-tenant-root` blueprint via Microsoft Graph

It does NOT need:
- Sprint 30 done (Sprint 41 doesn't read Fabric data — it provisions identities)
- Sprint 42 done (Sprint 41 doesn't run agents — it provisions their identities)

It DOES need:
- A Lab Azure subscription
- Lab Entra tenant with the deployment principal granted required Graph permissions

So Sprint 41 can start immediately, in parallel with Sprint 30, with different SREs.

---

## What "starting Sprint 30" actually entails

1. **Provision a Lab Azure subscription** (Deloitte's internal Lab pool)
2. **Run `az deployment group create`** against `apex-m/infra/bicep/blueprints/w1-foundation.bicep` (already authored in Phase I.4)
3. **Provision Fabric capacity** — F-SKU (per Roadmap.md BL.P.91) via Terraform `infra/terraform/modules/fabric_capacity/`
4. **Stand up the primary workspace** `rc-canonical` per Services Guide §1.6 — owns canonical Silver entities (SCML / MERML / PROML / CRMML)
5. **Land Bronze sources** — POS / ERP / refrigeration telemetry / competitor pricing — per Services Guide §18.1 data sources
6. **Stand up Silver entities** — `SCML.Inventory`, `SCML.Lot`, `MERML.Markdown`, `MERML.Elasticity`, `MERML.Competitor`, `PROML.Pricing`, `PROML.DiscountRule` (per Sprint 30 items 30.3 + 30.4 in `_build-status.yaml`)
7. **Materialize the 6 RC-E2E-03 Gold marts** — `g_excursion_decision_panel`, `g_markdown_proposal_basis`, `g_pricing_recommendation_basis`, `g_inventory_position_current`, `g_kpi_rc_e2e_03_daily`, `g_markdown_outcome_attribution`

This is the foundation Sprint 33 (deploy + smoke) needs in place before it can run an actual cold-chain excursion smoke test. Without Sprint 30, Sprint 33 has no data to read.

It does NOT need:
- Phase I production wiring (Sprint 30 is Bicep + Fabric REST API + notebook code, not Microsoft Agent Framework)

It DOES need:
- A Lab Azure subscription
- Sufficient Fabric capacity allocation

So Sprint 30 and Sprint 41 are mutually independent — they can start the same day with different SREs.

---

## Updates to `_build-status.yaml`

The current file has Sprints 30–40. Adding Sprints 41–49 makes them visible in the wizard's Roadmap page so progress is trackable end-to-end. See companion commit.

---

## Three concrete next-step options

Tell me which to start:

**Option A** — Start Sprint 30 (RC W1 Foundation) — Bicep apply + Fabric provisioning + medallion landing. Foundation work; Data SRE owns. ~4-6 weeks.

**Option B** — Start Sprint 41 (production Entra Agent ID) — wire `azure-identity` + httpx + Microsoft Graph calls in `apex_m.identity_entra`. Identity SRE owns. ~2 weeks.

**Option C** — Start both 30 + 41 in parallel — different SREs, no cross-dependency. Recommended if staffing is available.

**Option D** — Update `_build-status.yaml` first to reflect Sprints 41–49, then pick A/B/C — gives you wizard Roadmap visibility on the full execution path before kicking off.
