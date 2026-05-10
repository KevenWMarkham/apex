# User-Acceptance Criteria — Status Report

**Audience:** Keven Markham · DMTSP · APEX engagement owner
**Purpose:** Map the original user-acceptance ask to shipped code, validated against an end-to-end run via `tools/validate_acceptance.py`.
**Validation last run:** 2026-05-10 · mock mode · 4 of 4 criteria passed.

---

## The original ask

> *"User acceptance is to have a deployable framework to laptop, dev / test, stage and production (platform). I need a deploy ux (with wizard) to deploy. I need to understand how I will incorporate the usecases when deployed."*

Three concrete deliverables:

1. **Deployable framework** across four substrates: laptop · dev/test · stage · production
2. **Deploy UX (wizard)** that an operator drives
3. **Use-case incorporation at deploy time** — the engagement's specific configuration flows in during the deploy

---

## Status — all four criteria validated (mock mode)

| ID | Criterion | Status | Evidence |
|---|---|---|---|
| **A1** | Laptop substrate produces a runnable docker-compose stack | ✅ | `tools/_acceptance_evidence/A1_laptop_docker_compose.yml` |
| **A2** | Cloud substrates (dev / stage / prod) produce valid Bicep parameter files | ✅ | `tools/_acceptance_evidence/A2_{dev,stage,prod}_bicep_params.json` |
| **A3** | Operator clones `_default/` → `<client>/`, populates persona bindings, PSG-15 unlocks deploy | ✅ | `tools/_acceptance_evidence/A3_{default,bigbox_prod}_use_case.json` |
| **A4** | Wizard end-to-end: PSG check → what-if → deploy → audit row → drift | ✅ | `tools/_acceptance_evidence/A4_wizard_{deployment_record,security_gate}.json` |

Run `python tools/validate_acceptance.py` from the repo root to regenerate.

---

## A1 · Laptop substrate ✅

**What the criterion means:** A developer with this repo on their laptop can produce a `docker-compose.yml` for any RC service + scenario combination, then `docker-compose up` to run the chain end-to-end against mock backends.

**How it's met:**

- `POST /api/deployments/render` with `substrate=laptop` calls `_render_compose_yaml()` in `apps/deploy-wizard/api/src/apex_wizard/deployments.py`.
- The output declares one container per (service × scenario × agent_role) plus 4 mock backends (`apex-mock-foundry` / `apex-mock-fabric` / `apex-mock-purview` / `apex-mock-redis`).
- Every agent container gets `APEX_FORCE_MOCK=true` plus `APEX_USE_CASE_ID` so the use-case overrides flow in.
- All 6 canonical agent roles (`assess` / `classify` / `quantify` / `decide` / `act` / `learn`) materialise.

**Evidence sample (head of A1_laptop_docker_compose.yml):**

```yaml
# rendered docker-compose.yml — substrate: laptop
# tenant: laptop-dev-001  variant: APEX-M  use_case: rc-e2e-03--default
version: '3.9'
services:
  apex-mock-foundry:
    image: ghcr.io/apex/mock-foundry:0.1.0
  apex-mock-fabric: ...
  apex-m-rc-e2e-03-rc-cold-chain-excursion-mid-shift-assess:
    image: ghcr.io/apex/rc-e2e-03/assess:0.1.0
    environment:
      APEX_SUBSTRATE: laptop
      APEX_USE_CASE_ID: rc-e2e-03--default
      APEX_FORCE_MOCK: 'true'
```

**What's still environmental** (not blocking laptop UX):

- Mock container images (`ghcr.io/apex/mock-foundry:0.1.0` etc.) need to be published to a registry the developer can pull from. Today the framework ships the *agent code* that runs inside; the image-build pipeline + GHCR registration is a follow-up engagement-readiness task. Until then, a developer can `pip install` the apex-m runtime and run agents directly with `APEX_FORCE_MOCK=true`.

---

## A2 · Cloud substrates (dev / stage / prod) ✅

**What the criterion means:** The same wizard renders Bicep parameter files for the three cloud substrates that an operator runs via `az deployment group create`.

**How it's met:**

- `POST /api/deployments/render` with `substrate ∈ {dev, stage, prod}` emits an Azure `deploymentParameters.json` body.
- The blueprint is selected per `wave` (w1 / w2 / w3 → `apex-m/infra/bicep/blueprints/{w1-foundation,w2-pilot,w3-scale-fuse}.bicep`).
- The `selections` array carries per-service + per-scenario picks forward to the Bicep modules.

**Evidence sample (A2_prod_bicep_params.json):**

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "tenant": { "value": "bigbox-prod" },
    "containerAppsEnvId": { "value": "REPLACE_WITH_LAYER1_OUTPUT" },
    "agentIdentityId":    { "value": "REPLACE_WITH_LAYER1_OUTPUT" },
    "selections": { "value": [{ "serviceCode": "RC-E2E-03", "featuredScenarios": [...] }] }
  }
}
```

**What's still environmental** (not blocking framework readiness):

- `REPLACE_WITH_LAYER1_OUTPUT` placeholders fill from the Sprint 30 W1 Foundation deploy outputs. That deploy is `blocked_on_environment` until the Lab Azure subscription is provisioned. The wizard's `bicep_runner` is already wired to fill these from the Layer-1 outputs when they exist (mock mode synthesises them).

---

## A3 · Use-case incorporation ✅

**What the criterion means:** Each engagement has its own use-case overlay (client-specific adapter selections, persona bindings, HITL thresholds, KPI targets). When deploying for that client, the wizard incorporates those overrides without the operator hand-editing framework files.

**How it's met:**

- Framework ships `services/<practice>/<service>/use-cases/_default/use-case.yaml` as the worked-example template (synthetic personas, REPLACE_WITH placeholders).
- Per-engagement workflow: operator clones `_default/` → `<client>/`, populates the client-specific block:
  - `client_approved_architecture` — adapter selections per CAB
  - `persona_principal_bindings` — maps framework role → live principals (Sprint 47.6 schema)
  - `hitl_thresholds` — per-tenant overrides
  - `kpis_targeted` — per-tenant SLO targets
- Pre-deployment Security Gate **PSG-15** (Sprint 47.6) validates the bindings before deploy. Fails closed when prod substrate has synthetic personas unbound.
- The wizard's `POST /api/deployments` payload carries the use-case id; the rendered Bicep parameters embed it; agent containers receive it as `APEX_USE_CASE_ID`.

**Evidence (live PSG-15 transitions captured by the validator):**

```
PASS  _default use-case on lab substrate: PSG-15 allows deploy (worked-example mode)
PASS  Cloned _default -> bigbox-prod WITHOUT bindings: PSG-15 fails closed (correct)
PASS  Cloned _default -> bigbox-prod WITH bindings: PSG-15 green, deploy allowed
PASS    Bound personas: 2 of 2 active
```

**What's still environmental** (engagement-driven, not framework-blocked):

- The actual Entra group object IDs come from the client's tenant. The framework schema models the binding; the operator pastes the GUID at deploy time. PSG-15 then verifies the group resolves at HITL fire time (requires `apex-m[runtime]` extras + Microsoft Graph access — Sprint 41 production wiring lights this up).

---

## A4 · Wizard end-to-end ✅

**What the criterion means:** A real operator drives the wizard UI; the wizard walks them through select → render → security-gate check → what-if → confirm → deploy → audit row, with drift detection running daily afterward.

**How it's met (Sprint 46 ships the full chain):**

| Step | Endpoint | Behaviour |
|---|---|---|
| 1. Select | `GET /api/catalog/tree` | Practice → Service → Scenario → Agent treeview |
| 2. Render | `POST /api/deployments/render` | Substrate-aware: docker-compose (laptop) OR Bicep params (cloud) |
| 3. Gate | `GET /api/security-gate?tenant=X` + `POST /with-context` | 15 gates polled; PSG-15 fails closed on missing bindings |
| 4. Deploy | `POST /api/deployments` | Orchestrates PSG check → what-if → destructive 2nd-confirm → apply |
| 5. Track | `GET /api/deployments/{id}` | Returns status + correlation_id + audit_row reference |
| 6. Drift | `GET /api/drift/{tenant}` + daily cron | Severity-bucketed drift report (low/medium/high) |

**Evidence sample (A4_wizard_deployment_record.json):**

```json
{
  "id": "apex-bigbox-prod-11cf3c33-...",
  "tenant": "bigbox-prod",
  "wave": "w2",
  "blueprint_path": "apex-m/infra/bicep/blueprints/w2-pilot.bicep",
  "bicep_what_if_summary": {
    "counts": { "Create": 2, "NoChange": 1 },
    "has_destructive": false,
    "mode": "mock",
    "duration_ms": 42
  },
  "status": "succeeded",
  "audit_row_id": "mock-f59b55a7-c238-475d-986a-81ba9a24df1a"
}
```

**What's still environmental:**

- Real-mode `az` invocation: requires `APEX_FORCE_MOCK=false` AND `az` on PATH AND a Lab Azure subscription. The dual-mode wiring is in `apex_wizard.bicep_runner.get_default_runner()` — set the env, install `az`, and the same code paths fire against real Azure.
- Audit row persistence to Purview: today the wizard records to an in-memory `_DEPLOYMENT_STORE`. Sprint 42's production wiring swaps the AuditLedger protocol for `apex_m.audit_purview.AuditLedgerPurview`; the call signature stays stable.

---

## What this means for the engagement

**Framework readiness:** The four user-acceptance criteria are validated end-to-end in mock mode against the shipped code. A developer can run `tools/validate_acceptance.py` to reproduce the validation. The wizard, the use-case incorporation flow, and all four substrates work today against mocks.

**Lab readiness:** Three things still need a Lab Azure subscription to validate fully:

1. **A1 mock images on GHCR** — image build + publish pipeline (small engagement-readiness task)
2. **A2 Layer-1 placeholder fills** — Sprint 30 W1 Foundation `az deployment group create` against Lab
3. **A4 real-mode wizard** — `APEX_FORCE_MOCK=false` + `az` calls against Lab subscription

None of these change the framework code. They are operational onboarding tasks.

**Phase J + DEP-NNN deprecations:** Independent from user-acceptance. Sprint 49 migrations (RTI MCP, `ai_embeddings`, DeltaFlow, Activator, Defender-only path, Purview Audit primary) are *quality* upgrades to surfaces that already work via the framework's current paths — they don't gate user acceptance.

---

## How to re-validate

```bash
# From repo root, with apex-m + apex-core + apex_wizard editable-installed:
python tools/validate_acceptance.py

# Expect:
#   4 of 4 acceptance criteria validated.
#   Evidence artefacts: tools/_acceptance_evidence/
```

CI gates on this exit code. Any future PR that breaks the criteria fails this script.

---

## Sign-off checklist for the engagement owner

- [ ] Run `tools/validate_acceptance.py` and inspect the 4 evidence artefacts in `tools/_acceptance_evidence/`
- [ ] Confirm A1 docker-compose has the expected per-scenario containers
- [ ] Confirm A2 Bicep params have your tenant slug + correct selections
- [ ] Confirm A3 PSG-15 transitions (lab=warn → prod-unbound=red → prod-bound=green)
- [ ] Confirm A4 deployment record carries an audit-row correlation id
- [ ] Schedule Lab subscription provisioning to validate real-mode A1.images + A2.Layer-1 + A4.az-runner

Once the Lab subscription is in hand, Sprints 41–45 production-wire each of the 10 protocols; the wizard's `register_checker()` swaps in the real PSG-1 through PSG-14 checkers; and the same `validate_acceptance.py` run with `APEX_FORCE_MOCK=false` becomes the production smoke test.
