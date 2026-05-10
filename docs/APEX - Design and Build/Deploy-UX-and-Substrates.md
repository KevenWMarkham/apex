# Deploy UX and the Four Substrates

**Audience:** Engagement leads, tenant SREs, anyone deploying APEX
**Purpose:** Define how the wizard deploys APEX across the four substrates (laptop / dev / stage / prod) and how use cases incorporate at deploy time.

**Reference:**
- [APEX-M Deployment Guide ch 2 — Substrate-Aware Architecture](../book/Professional-APEX-M-Deployment-Guide.html#ch-2)
- [Pre-deployment Security Gate](Pre-deployment-Security-Gate.md)
- [Sprint Plan §47](Sprint-Plan.md#sprint-47--lab-tenant-for-first-client-2-weeks)
- [Use case schema](../../services/_use-case.schema.md)

---

## TL;DR

- **Four substrates:** `laptop` · `dev` · `stage` · `prod`. Same agent image runs unchanged on all four. Substrate-awareness lives at the **edges** (env vars, parameter files), never inside agent code.
- **Wizard is substrate-aware:** operator picks substrate first, then variant, then use case, then services + scenarios + agents. Render output differs per substrate (Docker Compose for laptop; Bicep for dev/stage/prod).
- **Use case is the per-tenant binding layer.** Selecting a use case in the wizard folds its `client_approved_architecture` block + `agent_overrides` + `foundry` block into the rendered parameters automatically. No hand-editing of Bicep params.
- **Pre-deployment Security Gate enforces per-substrate.** Lab/dev waivable on items 7, 8, 13; stage/prod must satisfy all 14.

---

## 1. The four substrates

| Substrate | Where it runs | IaC | Identity | Cost | Use |
|---|---|---|---|---|---|
| **laptop** | Docker Desktop (local) | `docker-compose.yml` | Workload Identity Federation (WIF) or full mock | $0 | Engineering iteration; demos; Independence-clean dev (no client cloud touched) |
| **dev** (Lab) | Shared Azure subscription | Bicep `w1-foundation.bicep` | Real Microsoft Entra Agent ID, no private networking | shared dev capacity | Team integration testing; harness runs |
| **stage** | Pre-prod Azure subscription | Bicep `w2-pilot.bicep` with private networking | Real Entra Agent ID + CA + WIF | sized smaller than prod | Pre-prod posture verification; mirrors prod |
| **prod** | Per-tenant Azure subscription | Bicep `w2-pilot.bicep` or `w3-scale-fuse.bicep` (full private networking) | Real Entra Agent ID + CA + Customer Lockbox | sized for SLA | Client-facing deployments |

Each substrate is **identity-aware**: the same APEX-Core protocol contract applies to all four; concrete implementations swap based on substrate (mocks on laptop, real SDK calls on Azure).

```
┌────────────────────────────────────────────────────────────────────┐
│  Same agent container image                                        │
│  Same APEX-Core protocol calls                                     │
│  Same scenario.yaml + agent.yaml + use-case.yaml                   │
└────────────────────────────────────────────────────────────────────┘
                               │
              ┌────────────────┼────────────────┬───────────────┐
              ▼                ▼                ▼               ▼
        ┌──────────┐    ┌──────────┐     ┌──────────┐    ┌──────────┐
        │ laptop   │    │  dev     │     │  stage   │    │  prod    │
        │          │    │          │     │          │    │          │
        │ docker-  │    │ Bicep    │     │ Bicep    │    │ Bicep    │
        │ compose  │    │ w1-      │     │ w2-pilot │    │ w2 or w3 │
        │          │    │ founda-  │     │ private  │    │ + CMK +  │
        │ All Mock │    │ tion     │     │ network  │    │ Customer │
        │ impls    │    │          │     │          │    │ Lockbox  │
        └──────────┘    └──────────┘     └──────────┘    └──────────┘
```

## 2. The deploy wizard flow (operator UX)

```
┌─────────────────────────────────────────────────────────────┐
│  Step 1 — Pick the cloud variant                            │
│   ◉ APEX-M (Microsoft)         [first-shipped]              │
│   ○ APEX-G (Google Cloud)      [Future · Independence Stub] │
│   ○ APEX-A (AWS)               [Future · Independence Stub] │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2 — Pick the substrate                                │
│   ○ laptop  — Docker Compose, mocks for Microsoft SDKs      │
│   ◉ dev     — Lab tenant, real SDKs, no private networking  │
│   ○ stage   — Pre-prod tenant, full private networking      │
│   ○ prod    — Production tenant, full security gate         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 3 — Pick the use case                                 │
│   ◉ rc-e2e-03--default       (canonical Services Guide §18.1)│
│   ○ contoso-rc-e2e-03-na-pilot   (client-specific clone)    │
│   + Add new use case for client                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 4 — Pick services + scenarios + agents (treeview)     │
│   ☑ Practice: Retail & Consumer (RC)                        │
│     ☑ Service: RC-E2E-03 [scaffolded]                       │
│       ☑ Scenario: rc-cold-chain-excursion-mid-shift         │
│         ☑ assess  ☑ classify  ☑ quantify                    │
│         ☑ decide (HITL)  ☑ act (HITL)  ☑ learn              │
│         ☑ The Pricer (HITL)                                 │
│       ☑ Scenario: rc-dynamic-markdown-optimization          │
│         (defaults selected from use case)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 5 — Pre-deployment Security Gate                      │
│   ✓ Gate 1: Defender for Cloud CSPM with AI posture (green) │
│   ✓ Gate 3: Entra Agent ID tenant root blueprint (green)    │
│   ⚠ Gate 13: Foundry private networking (yellow — required  │
│              for stage/prod; waivable for dev)              │
│   …                                                         │
│   [ Approve gate ]                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 6 — Render and review                                 │
│   Output: docker-compose.yml (laptop) OR                    │
│           parameters JSON for Bicep (dev/stage/prod)        │
│   [ Run what-if ]   [ Deploy ]                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                      Deployed APEX
```

Each step's selection is captured in the wizard's `RenderRequest` and posted to `/api/deployments/render`. The render endpoint resolves the substrate-appropriate output.

## 3. How use cases incorporate at deploy time

The use case is **the** binding layer between the catalog (services, scenarios, agents — provider-neutral) and the deployment (variant, substrate, tenant — variant-specific). Selecting a use case in step 3 of the wizard makes everything downstream concrete.

### 3.1 Data flow

```
services/rc/RC-E2E-03/use-cases/<slug>/use-case.yaml
                     │
                     │ (loaded by wizard at step 3)
                     ▼
┌─────────────────────────────────────────────────────┐
│  Use case fields                                    │
│   - primary_variant: APEX-M                         │
│   - substrate: lab | dev | stage | prod             │
│   - client_approved_architecture (adapter slots)    │
│   - personas_active                                 │
│   - kpis_targeted                                   │
│   - hitl_thresholds                                 │
│   - agent_overrides (per-role model/memory/prompt)  │
│   - foundry (project ref, image tag, workflow)      │
│   - deployment (wave + blueprint + parameters file) │
└─────────────────────────────────────────────────────┘
                     │
                     │ (validated against _personas.yaml,
                     │  _kpis.yaml, packages/apex-adapters)
                     │
                     ▼
        substrate == 'laptop' ?
                ┌────┴─────┐
              yes          no
                │           │
                ▼           ▼
    docker-compose.yml    Bicep parameters JSON
    .env file              (w1 / w2 / w3 blueprint
                            picks based on wave)
```

### 3.2 What the use case gives you, mapped per output

| Use case field | Laptop output | Cloud output (dev/stage/prod) |
|---|---|---|
| `primary_variant: APEX-M` | Pulls Mock* impls from `apex_m.*` | Pulls real impls; resource type `Microsoft.CognitiveServices/accounts/projects/agents` |
| `substrate: lab` | sets `APEX_SUBSTRATE=laptop` env in compose | sets Bicep param `substrate: 'lab'` |
| `client_approved_architecture.data_lake.bronze_sources[*].adapter` | container env vars: `APEX_BRONZE_<SOURCE>_ADAPTER=<adapter>` | Bicep `selections[*].mcpServers[]` per adapter; per-adapter Bicep modules from `apex-adapters/.../iac/` get composed |
| `client_approved_architecture.identity.federation` | mock IdP container in compose | Federation credential resource on the service blueprint |
| `client_approved_architecture.siem_audit.secondary` | mock SIEM container (logs to stdout) | Splunk HEC token in Key Vault + Activator destination |
| `client_approved_architecture.hitl_channel.primary` | mock Teams stub (terminal output) | Teams webhook URL in Key Vault |
| `personas_active` | env: `APEX_PERSONAS=marisol-reyes-store-ops,daniel-chen-merch-director` | Same env, plus persona-aware Conditional Access policy attached to service blueprint |
| `kpis_targeted` | env: target values for KPI evaluator | Bicep param wired into `g_kpi_<service>_daily` mart |
| `hitl_thresholds` | env: per-decision thresholds | Key Vault secret per threshold; agent reads at decision time |
| `agent_overrides.<role>.model` | env: `APEX_AGENT_MODEL_<ROLE>=<model>` | Foundry agent definition's model field; substituted at deploy |
| `agent_overrides.pricing.redis_episodic_memory` | mock Redis container in compose | Real Redis Cache resource + connection in Key Vault |
| `foundry.project_ref` | (not used; mock) | Bicep param `foundryProjectId` |
| `foundry.hosted_agent_image_tag` | docker-compose `image:` field | Bicep param `agentImageTag` for `Microsoft.App/containerApps` or hosted agent deployment |
| `deployment.wave` | (informational only) | Picks blueprint: w1 / w2 / w3 |

### 3.3 Worked example — `contoso-rc-e2e-03-na-pilot`

Operator picks: variant=`APEX-M`, substrate=`lab`, use_case=`contoso-rc-e2e-03-na-pilot`, scenarios=both featured.

The wizard's render endpoint produces:

**For substrate=`lab`** — Bicep parameters JSON:

```json
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "tenant": { "value": "contoso-prod" },
    "wave": { "value": "w2" },
    "substrate": { "value": "lab" },
    "containerAppsEnvId": { "value": "/subscriptions/.../cae-apex-contoso" },
    "agentIdentityId": { "value": "/subscriptions/.../id-apex-contoso-agent" },
    "foundryProjectId": { "value": "/subscriptions/.../foundry-rc-e2e-03-contoso" },
    "selections": {
      "value": [{
        "serviceCode": "RC-E2E-03",
        "featuredScenarios": [
          "rc-cold-chain-excursion-mid-shift",
          "rc-dynamic-markdown-optimization"
        ],
        "agentOverrides": {
          "rc-cold-chain-excursion-mid-shift": {
            "pricing": {
              "model": "gpt-4o-2024-11-20",
              "redisEpisodicMemory": true,
              "learningLoopWindowDays": 90
            }
          }
        },
        "mcpServers": [
          { "name": "merml", "image": "ghcr.io/apex/merml-mcp:1.0.0" },
          { "name": "scml",  "image": "ghcr.io/apex/scml-mcp:1.0.0" },
          { "name": "cloud-aws-rds", "image": "ghcr.io/apex/adapter-aws-rds:0.1.0",
            "config": { "dataset": "contoso-pos-prod" } }
        ]
      }]
    },
    "hitlThresholds": {
      "value": {
        "rc-cold-chain-excursion-mid-shift": {
          "markdownPctAbove": 30,
          "destroyDecision": "any",
          "refundUsdAbove": 500
        }
      }
    },
    "personasActive": {
      "value": ["marisol-reyes-store-ops", "daniel-chen-merch-director"]
    }
  }
}
```

The Bicep blueprint reads the parameters and composes:
- `apex-m/infra/bicep/platform/main.bicep` — provisioned at first run
- `apex-m/infra/bicep/modules/agent-fleet.bicep` — instantiated per scenario, with per-role agent overrides
- Adapter-side resources (e.g., AWS RDS read role) — emitted as Bicep snippets from `apex-adapters/.../iac/`
- HITL threshold secrets in Key Vault — provisioned with values from the use case
- Service blueprint Conditional Access policies — bound per personas

**For substrate=`laptop`** — Docker Compose:

```yaml
# rendered docker-compose.yml — substrate: laptop
version: '3.9'
services:
  apex-m-rc-e2e-03-cold-chain-pricing:
    image: ghcr.io/apex/rc-e2e-03/pricing:0.1.0
    environment:
      APEX_SUBSTRATE: laptop
      APEX_VARIANT: APEX-M
      APEX_SERVICE_CODE: RC-E2E-03
      APEX_SCENARIO_ID: rc-cold-chain-excursion-mid-shift
      APEX_AGENT_ROLE: pricing
      APEX_USE_CASE_ID: rc-e2e-03--default
      APEX_AGENT_MODEL_PRICING: gpt-4o-2024-11-20
      APEX_REDIS_EPISODIC: 'true'
      APEX_HITL_MARKDOWN_PCT: '30'
      APEX_PERSONAS: marisol-reyes-store-ops,daniel-chen-merch-director
      # Mock-mode: every Microsoft SDK call routes to apex_m.*Mock impls
      APEX_FORCE_MOCK: 'true'
    depends_on:
      - apex-mock-redis
      - apex-mock-fabric
      - apex-mock-purview
      - apex-mock-foundry

  apex-mock-foundry:    # mocks the Foundry runtime
    image: ghcr.io/apex/mock-foundry:0.1.0
  apex-mock-fabric:     # mocks Fabric SQL analytics endpoint
    image: ghcr.io/apex/mock-fabric:0.1.0
  apex-mock-purview:    # mocks Purview Audit
    image: ghcr.io/apex/mock-purview:0.1.0
  apex-mock-redis:
    image: redis:7-alpine

  # ... one container per agent role per scenario ...
```

The compose file references the same agent images that run in Azure prod — substrate-awareness is purely env-var-driven.

## 4. Per-substrate deploy commands

The wizard wraps these; an operator who prefers CLI can run them directly.

### Laptop

```bash
cd ~/apex-deployments/<engagement>
docker-compose up                     # Brings up the rendered compose file
# (Wizard generated docker-compose.yml + .env in the engagement folder)
```

Mocks log to stdout. Synthetic data fixtures live in `apex-m/test-fixtures/`. The agent runtime is identical to Azure prod; only the SDK calls go to Mocks.

### Dev (Lab)

```bash
az login --tenant <lab-tenant-id>
cd ~/apex-deployments/<engagement>

# Layer 1 platform (one-time per Lab subscription)
az deployment group create \
  -g rg-apex-lab \
  -f ../apex-m/infra/bicep/blueprints/w1-foundation.bicep \
  -p @lab-platform-params.json

# Layer 2 service (per service deployed)
az deployment group create \
  -g rg-apex-lab \
  -f ../apex-m/infra/bicep/blueprints/w2-pilot.bicep \
  -p @lab-rc-e2e-03-params.json
```

The wizard's "Deploy" button runs these via `apex_wizard.bicep_runner` (Sprint 46). Pre-deployment Security Gate items 7, 8, 13 may be waived for Lab with documented sign-off.

### Stage

Identical to Lab but against the Stage subscription, with private networking required:

```bash
az login --tenant <stage-tenant-id>
az deployment group create \
  -g rg-apex-stage \
  -f ../apex-m/infra/bicep/blueprints/w2-pilot.bicep \
  -p @stage-rc-e2e-03-params.json
```

Pre-deployment Security Gate must satisfy all 14 items. Wizard refuses to render parameters until every gate is green.

### Prod

Identical to Stage, but per-tenant subscription, with Customer Lockbox + CMK:

```bash
az login --tenant <client-prod-tenant-id>
az deployment group create \
  -g rg-apex-<client>-prod \
  -f ../apex-m/infra/bicep/blueprints/w2-pilot.bicep \
  -p @<client>-rc-e2e-03-prod-params.json
```

Drift detector cron starts; daily `what-if` against the pinned manifest.

## 5. The wizard's substrate-aware render endpoint

Implementation lands in Sprint 46 alongside the live security gate. The render endpoint receives:

```json
{
  "selected_ids": ["service:RC-E2E-03", "scenario:rc-cold-chain-excursion-mid-shift"],
  "tenant": "contoso-prod",
  "wave": "w2",
  "substrate": "lab",
  "use_case_id": "contoso-rc-e2e-03-na-pilot",
  "primary_variant": "APEX-M"
}
```

And dispatches:

```python
def render(request):
    substrate = request.substrate
    use_case = load_use_case(request.use_case_id)
    validated = validate_adapters(use_case)
    if substrate == "laptop":
        return render_docker_compose(use_case, request)
    return render_bicep_parameters(use_case, request)
```

`render_docker_compose` walks the use case + selections to emit `docker-compose.yml` + `.env`. `render_bicep_parameters` walks the same data to emit a parameter JSON for the substrate-appropriate Bicep blueprint.

Both code paths share the same validation: every adapter ref resolves, every persona id is in `_personas.yaml`, every KPI id is in `_kpis.yaml`, every agent role is in `_extras.yaml` or DEFAULT_AGENT_ROLES.

## 6. What ships when (sprint mapping)

| Capability | Sprint | Status |
|---|---|---|
| Wizard substrate selector UI | **46a** | Shipping in this commit |
| Render endpoint substrate dispatcher | 46a | Shipping in this commit |
| Laptop docker-compose templates | 46a | Stub shipping; full set in 47 |
| Production Bicep render with use-case overrides | 46 | Existing render extended |
| Bicep runner (`az deployment group create`) | 46 | Sprint 46 |
| `/security-gate` page live polling | 46 | Sprint 46 |
| First end-to-end Lab deploy via wizard | 47 | First client engagement |
| Compose images for mock services | 47 | When real agent images stabilize |

The current commit lands the architectural shape (this doc + minimal wizard surface). Sprints 46 and 47 fill in the live-execution paths.

## 7. Independence + substrate

A note for engagement leads: the **laptop** substrate is genuinely Independence-clean — no client cloud touched, no Microsoft / Google / AWS subscription billed. Engineers can iterate on agent code, prompts, and orchestrations on their Deloitte-issued laptop without any cross-organization API call.

The **dev / stage / prod** substrates are client-tenant work; per-engagement Independence consultation applies (per Pre-deployment Security Gate item #14).

## 8. Decommissioning

The wizard's Deploy page also exposes a Decommission action per tenant. Per substrate:

- **laptop**: `docker-compose down -v` clears the engagement folder
- **dev/stage/prod**: Bicep `delete` + Entra Agent ID blueprint revoke + Customer Lockbox-protected resource cleanup; runs the substrate's standard tear-down sequence

Decommission writes a final audit row to Microsoft Purview Audit with the engagement's tenant slug + substrate + reason.

## 9. References

- [Sprint Plan §41–46](Sprint-Plan.md#sprint-detail--phase-i-production-wiring-4146) — production wiring sprints that fill in the SDK calls behind this UX
- [APEX-M Deployment Guide ch 2](../book/Professional-APEX-M-Deployment-Guide.html#ch-2) — substrate-aware architecture
- [APEX-M Deployment Guide ch 13.5](../book/Professional-APEX-M-Deployment-Guide.html#ch-13-5) — Pre-deployment Security Gate
- [Use case schema](../../services/_use-case.schema.md) — every field this UX consumes
- [Adapter Catalog](../apex-core/Adapter-Catalog.md) — what client_approved_architecture refs resolve to
- [Independence Posture](../apex-core/Independence-Posture.md) — variant + adapter Independence framing
