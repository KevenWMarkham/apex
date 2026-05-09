# RC Design Docs + Foundry-Aligned Runtime — Design

**Date:** 2026-05-09
**Status:** Approved
**Authors:** Keven Markham · DMTSP, with Claude

---

## 1. Problem statement

Two needs converged in one decision:

1. **Design surface for RC services and agents.** Every RC service and every agent in our scaffold ships with a `service.yaml` / `scenario.yaml` / `agent.yaml` (machine-readable) but **no human-readable design narrative**. Architects can't see persona × KPI × use case binding. Deployment is opaque to anyone who isn't reading YAML.

2. **Runtime architecture must align to Microsoft's roadmap.** Today the Deployment Guide makes Layer 3 = `Microsoft.App/containerApps`. Microsoft's current canonical pattern for enterprise agents (May 2026) is **Foundry Hosted Agents on Foundry Agent Service**. Container Apps stays for MCP servers and orchestration code; agents move to Foundry.

This design covers both as a single coordinated change so the new design docs reflect the new runtime.

## 2. Goals and non-goals

**Goals**

- Add three levels of `DESIGN.md` (service / scenario / agent), one default `use-case.yaml` + `DESIGN.md` per service, and a centralized service narrative under `docs/APEX - Design and Build/services/`.
- Introduce a framework-level **persona registry** and **KPI registry** so the same Marisol Reyes persona is referenced from cold-chain and markdown scenarios — not redefined per scenario.
- Adopt **Path C — Microsoft hybrid**: Foundry Hosted Agents for Layer 3, Container Apps for MCP servers and the wizard control plane, Bicep everywhere.
- Update both books (Services Guide + Deployment Guide) to reflect Foundry.
- Cross-link design docs ↔ books ↔ Microsoft Learn so any reader can trace a decision back to its source.
- Keep all 250+ existing scaffolded files unchanged (their schemas are runtime-agnostic).

**Non-goals**

- Rewriting Container Apps Bicep modules other than `agent-fleet.bicep`. `service.bicep`, `mcp-server.bicep`, `hitl-gate.bicep`, the wizard control-plane Bicep, and the Terraform modules all stay.
- Hand-authoring rich design narrative for every one of the ~250 generated `DESIGN.md` files. The RC-E2E-03 trio (service + cold-chain scenario + The Pricer agent + default use case) is the worked example; the rest get rich auto-populated templates and are hand-filled iteratively.
- Touching the framework-wide `Roadmap.md`. Only `RC-Build-Plan.md` gets new items.
- Migrating the orchestrator package to Microsoft Agent Framework. That's a follow-on; design docs reference it but don't depend on it.

## 3. Architecture — Path C (Microsoft hybrid)

### 3.1 The chain, end-to-end

```
KPI ← Persona ← Use Case ← Scenario ← Service ← Agent (Foundry hosted) ← Foundry Agent Service ← Bicep ← Tenant
                                                                  ↑
                                                              MCP Tools
                                                                  ↑
                                                       Container Apps + Managed Identity
```

| Layer | Runtime | IaC |
|---|---|---|
| **Layer 1 — Platform** | Foundry Hub + Project, Container Apps Env, Cosmos DB, AI Search, Storage, Key Vault, Log Analytics | Bicep — Azure Verified Module [`br/public:avm/ptn/ai-ml/ai-foundry`](https://github.com/Azure/bicep-registry-modules/tree/main/avm/ptn/ai-ml/ai-foundry) + our existing `infra/bicep/platform/*` |
| **Layer 2 — Service** | Foundry Project per APEX service (or shared with sub-project per use case) | Bicep — `infra/bicep/modules/service.bicep` composes Foundry project + per-service Cosmos/Storage |
| **Layer 3 — Agents** | **Foundry Hosted Agents** (containerized; Foundry manages threading, tools, observability, content safety) | Bicep references the Foundry project; `azd deploy` pushes agent images |
| **MCP servers** | Azure Container Apps + managed identity | Bicep — `infra/bicep/modules/mcp-server.bicep` (unchanged) |
| **Wizard control plane** | Azure Container Apps | Bicep — `infra/bicep/control-plane/main.bicep` (unchanged) |
| **Orchestration shape** | Defined per-service; runtime in Foundry Agent Service workflows + Microsoft Agent Framework code | YAML + Foundry workflow definition |
| **Use Case** | Configuration above Foundry — picks personas, KPIs, HITL thresholds, tools, model | YAML per client; rendered into Foundry agent params at deploy |

### 3.2 Why Foundry Hosted Agents (not prompt agents, not raw Container Apps)

Microsoft's [baseline Foundry chat reference architecture](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-chat) lists these as the reasons to choose **hosted** agents over prompt agents — every one of them applies to APEX:

- Fine-grained, deterministic control over the agent execution path
- Explicit orchestration patterns
- Multi-agent connection
- **Human-in-the-loop intervention** (book §9 of Deployment Guide)
- Reuse of existing codebases (the apex-orchestrator + apex-agents Python packages)
- Agent code auditing for security, compliance, regulatory purposes (the LEDGER + audit-row chain in Deployment Guide §11)
- Fine-tuned runtime configuration (CPU/memory/autoscale)
- Extended memory (the Pricer's Redis-backed episodic memory in Services Guide §25.8)

Versus raw Container Apps (Path A), Foundry Hosted Agents give us **for free**: managed conversation/threading state, native MCP tool registration with managed-identity auth, content safety, Application Insights tracing per agent decision, M365 Copilot publishing path. We trade: agent runtime VM control (we don't need it) and bring-your-own-Kubernetes (we don't want it).

### 3.3 What stays Container Apps

From [host MCP servers on Azure Container Apps](https://learn.microsoft.com/azure/container-apps/mcp-overview) and the official [`azmcp-foundry-aca-mi`](https://github.com/Azure-Samples/azmcp-foundry-aca-mi) sample: MCP servers are explicitly the right fit for Container Apps. The wizard control plane is not an agent; it stays Container Apps. This is the documented hybrid.

## 4. Design surface — `DESIGN.md` files

Three levels co-located with code, plus one centralized narrative per service.

### 4.1 Co-located (engineering view)

```
services/{ind}/{code}/
  DESIGN.md                                    # service-level: chain, schemas, marts, MCP, agents, Foundry config
  use-cases/
    _default/
      use-case.yaml                            # client-agnostic baseline
      DESIGN.md                                # default use-case narrative
    {client-slug}/                             # added per client
      use-case.yaml
      DESIGN.md
  scenarios/{id}/
    DESIGN.md                                  # scenario narrative + 24-step chain explained
    agents/{role}/
      DESIGN.md                                # agent role, prompt strategy, tools, schemas R/W, HITL, persona served
```

### 4.2 Centralized (architecture view)

```
docs/APEX - Design and Build/services/
  RC-E2E-03/
    index.md                                   # full narrative — links into all the co-located DESIGN.md files
  RC-E2E-04/
    index.md
  ...
```

The two levels cross-link: every co-located `DESIGN.md` has a *"See also"* footer linking to `docs/APEX - Design and Build/services/{code}/index.md` and the books. Every centralized `index.md` links into its co-located peers.

### 4.3 Cross-references included by the generator

Every generated `DESIGN.md` cross-references:

- The Services Guide HTML chapter (`docs/book/Professional-APEX-Services-Guide.html#ch-18` for RC, `#ch-19` for HLS, etc.)
- The Deployment Guide HTML chapter (`docs/book/Professional-APEX-Deployment-Guide.html#ch-7` for service module shape, `#ch-1` for the three-layer cake)
- The Sellers Guide HTML where applicable (`docs/book/Professional-APEX-Sellers-Guide.html`)
- The Microsoft Learn URLs cited in §3 above
- The framework `Roadmap.md` BL.* IDs the design depends on

## 5. Use Cases — the variability layer

A Use Case is the **client-and-data-environment-specific** configuration of a Service. Same Service + same Agents → different personas, different KPI envelope, different HITL thresholds, different substrate, different data sources mapped.

### 5.1 `use-case.yaml` schema

```yaml
use_case_id: contoso-rc-e2e-03-na-pilot
service_code: RC-E2E-03
client: contoso
client_segment: Big-Box Grocery · 250 stores · NA pilot
substrate: lab    # lab | dev | stage | prod
data_environment:
  bronze_sources_present:
    - pos: NCR Aloha
    - erp: SAP S/4HANA Retail
    - refrigeration_telemetry: Monnit + IoT Hub
    - competitor_pricing: Numerator daily CSV
  silver_schemas_owned:
    - SCML.Inventory
    - MERML.Markdown
    - MERML.Elasticity
    - PROML.Pricing
  cross_service_dependencies:
    - service: RC-E2E-09
      tool: rc_e2e_09.get_lot_provenance
personas_active:
  - id: marisol-reyes-store-ops          # ref → services/_personas.yaml
  - id: daniel-chen-merch-director
kpis_targeted:
  - id: gm-pp-lift                       # ref → services/_kpis.yaml
    target: 3.2
  - id: doh-reduction-pct
    target: -28
  - id: markdown-to-clear-pct
    target: 41
hitl_thresholds:
  markdown_pct_above: 30
  destroy_decision: any
  refund_usd_above: 500
agent_overrides:
  pricing:
    model: gpt-4o-2024-11-20
    redis_episodic_memory: true
    learning_loop_window_days: 90
  decide:
    teams_webhook_secret: kv://apex-hitl-contoso-rc-e2e-03-decide
foundry:
  project_ref: foundry-rc-e2e-03-contoso
  hosted_agent_image_tag: rc-e2e-03/v1.2.0
  workflow_def: workflows/excursion-triage.yaml
deployment:
  wave: w2
  blueprint: infra/bicep/blueprints/w2-pilot.bicep
  parameters_path: apps/deploy-wizard/parameters/contoso-rc-e2e-03-w2.json
```

### 5.2 The `_default` use case

Every service ships with `use-cases/_default/use-case.yaml`. Personas are the canonical ones from Services Guide §18 (Marisol Reyes, Daniel Chen for RC-E2E-03). KPIs are the as-published envelope. Substrate is `lab`. Tenant-specific values are placeholders (`REPLACE_*`). Operators who pick "default" in the wizard get a working sample to clone.

## 6. Persona and KPI registries

### 6.1 `services/_personas.yaml` (framework-level)

```yaml
marisol-reyes-store-ops:
  label: Marisol Reyes
  role: Store Operations Lead
  level: store
  org: store-operations
  hitl_authority:
    - markdown_decisions
    - destroy_decisions
    - refund_above_threshold
  default_kpis:
    - shrink-cost-reduction-pct
    - decision-loop-time-sec
  used_by_services:
    - RC-E2E-03
  notes: >-
    Approves cold-chain excursion sell-through / markdown / destroy decisions
    via Teams Adaptive Card. Decision writes to audit row. See Services Guide
    §18.1.
daniel-chen-merch-director:
  label: Daniel Chen
  role: Merchandising Director
  level: regional
  org: merchandising
  ...
```

### 6.2 `services/_kpis.yaml` (framework-level)

```yaml
gm-pp-lift:
  label: Gross Margin lift (percentage points)
  unit: pp
  formula_ref: g_kpi_rc_e2e_03_daily.gm_pp_delta_vs_baseline
  attribution_path: MERML.Markdown.decision_ledger_id → g_markdown_outcome_attribution → g_kpi_rc_e2e_03_daily
  default_persona: daniel-chen-merch-director
  used_by_services:
    - RC-E2E-03
doh-reduction-pct: ...
markdown-to-clear-pct: ...
shrink-cost-reduction-pct: ...
decision-loop-time-sec: ...
```

Both registries are referenced **by id** from use cases, scenarios, and agents. Adding a persona or KPI happens once; every reference resolves automatically.

## 7. Generator and runtime changes

### 7.1 Generator extensions ([`tools/gen_services_tree.py`](../../tools/gen_services_tree.py))

- Read `_personas.yaml`, `_kpis.yaml`, `_extras.yaml` (already exists)
- Scaffold service-level `DESIGN.md` from xlsx + Services Guide §18 cross-refs (rich auto-populated template; `write_if_missing`)
- Scaffold scenario-level `DESIGN.md` from xlsx 24-step chain; resolve persona refs + KPI refs (`write_if_missing`)
- Scaffold agent-level `DESIGN.md` per role; pull prompt-strategy hints from agent role + persona (`write_if_missing`)
- Scaffold `use-cases/_default/use-case.yaml` + `DESIGN.md` per service from canonical Services Guide §18 envelope (`write_if_missing`)
- Scaffold centralized `docs/APEX - Design and Build/services/{code}/index.md` (`write_if_missing`)
- Validate: every use-case persona ref resolves in `_personas.yaml`; every KPI ref resolves in `_kpis.yaml`. Fail loud on dangling refs.

### 7.2 Bicep changes (the only Bicep that gets rewritten)

| File | Change |
|---|---|
| [`infra/bicep/platform/main.bicep`](../../infra/bicep/platform/main.bicep) | **Extended** — adds `module foundry 'br/public:avm/ptn/ai-ml/ai-foundry:<version>'` providing Foundry account + project + Standard Agent Services. Existing identity / ledger / monitoring kept. |
| [`infra/bicep/modules/agent-fleet.bicep`](../../infra/bicep/modules/agent-fleet.bicep) | **Rewritten** — replaces `Microsoft.App/containerApps` per agent with `Microsoft.CognitiveServices/accounts/projects/agents` (Foundry hosted agent definitions). Same params (`tenant`, `serviceCode`, `scenarioId`, `wave`, `agentIdentityId`); different resource type. |
| [`infra/bicep/modules/service.bicep`](../../infra/bicep/modules/service.bicep) | **Minor edit** — drops `containerAppsEnvId` param; adds `foundryProjectId` param. |
| [`infra/bicep/modules/mcp-server.bicep`](../../infra/bicep/modules/mcp-server.bicep) | **Unchanged** — Container Apps + MI is the documented Microsoft pattern for MCP servers. |
| [`infra/bicep/modules/hitl-gate.bicep`](../../infra/bicep/modules/hitl-gate.bicep) | **Unchanged** — Teams webhook + audit row binding is independent of agent runtime. |
| [`infra/bicep/control-plane/main.bicep`](../../infra/bicep/control-plane/main.bicep) | **Unchanged** — wizard is not an agent. |
| [`infra/bicep/blueprints/w1-foundation.bicep`](../../infra/bicep/blueprints/w1-foundation.bicep) | **Minor edit** — calls extended `platform/main.bicep`, exposes Foundry outputs. |
| [`infra/bicep/blueprints/w2-pilot.bicep`](../../infra/bicep/blueprints/w2-pilot.bicep), [`w3-scale-fuse.bicep`](../../infra/bicep/blueprints/w3-scale-fuse.bicep) | **Minor edit** — pass `foundryProjectId` to service modules. |

### 7.3 Wizard changes

- New endpoint `GET /api/catalog/use-cases?service=RC-E2E-03` — lists use cases under the service
- Tree endpoint `GET /api/catalog/tree` adds an optional **use case** node between Service and Scenario when one or more use cases exist
- Render endpoint accepts `use_case_id` and merges its overrides into the Bicep parameters
- TreeView component already supports arbitrary kinds; adds `kind: 'use-case'` with a yellow/orange badge

## 8. Book updates

### 8.1 Deployment Guide ([`docs/book/Professional-APEX-Deployment-Guide.html`](../book/Professional-APEX-Deployment-Guide.html))

- **Chapter 1 (The Three-Layer Cake)** — replace Layer 3 description: "Container image deployed as Container App" → "Foundry Hosted Agent on Microsoft Foundry Agent Service. Same image runs on Docker Desktop locally and Foundry on Azure." Cite [Foundry Hosted Agents](https://learn.microsoft.com/agent-framework/hosting/foundry-hosted-agent).
- **Chapter 7 (Service module shape)** — update `agents.bicep` skeleton to show Foundry resource type; keep service module composition shape. Cite [AVM ai-foundry module](https://github.com/Azure/bicep-registry-modules/tree/main/avm/ptn/ai-ml/ai-foundry).
- **New Chapter 11.5 (Foundry surfacing for M365)** — short chapter on registering hosted agents with Agent Service for Copilot Studio and M365 Copilot consumption. Cite [Foundry Agent Service overview](https://learn.microsoft.com/azure/foundry/agents/overview).
- **Chapter 9 (HITL gates)** — note that HITL is an explicit Microsoft-listed reason for hosted-agent over prompt-agent. Cite [Foundry baseline chat](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-chat).
- **Chapter 10 (MCP servers)** — explicitly cross-reference [host MCP servers on Container Apps](https://learn.microsoft.com/azure/container-apps/mcp-overview) and the [`azmcp-foundry-aca-mi`](https://github.com/Azure-Samples/azmcp-foundry-aca-mi) sample as the canonical pattern.

### 8.2 Services Guide ([`docs/book/Professional-APEX-Services-Guide.html`](../book/Professional-APEX-Services-Guide.html))

- **Chapter 18 (RC services)** — append a §18.x sub-section to each service: *"Use Cases — How clients qualify this Service against their data."* Each lists 1–3 representative use cases with the persona × KPI × substrate variability called out. Link to the centralized `docs/APEX - Design and Build/services/{code}/index.md`.
- **New Chapter 27 (Use Cases as the Variability Layer)** — explains the persona/KPI/substrate model and the `use-case.yaml` schema. Pattern repeats for HLS / ER / AXLE / TH / TMT / ICE.
- **Chapter 14 (Workflow shapes)** — note that orchestration *shape* lives in the Service; orchestration *tuning* (HITL thresholds, model choice, episodic memory) lives in the Use Case.

### 8.3 Cross-link policy

- Every `DESIGN.md` footers a *"References"* section with at least one Services Guide HTML anchor, one Deployment Guide HTML anchor, and one Microsoft Learn URL.
- Every chapter we update in the books gets back-pointers: *"For per-service implementation see [services/rc/RC-E2E-03/DESIGN.md](../../services/rc/RC-E2E-03/DESIGN.md)."*
- Centralized `index.md` files include the full link table and act as the navigation hub.

## 9. RC-E2E-03 worked example

Hand-authored rich content for the canonical trio so the rest of the catalog has a worked template:

1. **`services/rc/RC-E2E-03/DESIGN.md`** — full service narrative: persona × KPI binding (Marisol + Daniel × the published GM/DoH/MtC envelope), Foundry project layout, agent fleet, MCP tool surface, cross-Service consumption (RC-E2E-09), pricing-agent learning loop (Services Guide §25.8), audit-row chain (Deployment Guide §11), Bicep deploy walk-through.

2. **`services/rc/RC-E2E-03/scenarios/rc-cold-chain-excursion-mid-shift/DESIGN.md`** — scenario narrative: the moment, the 24-step chain explained step-by-step, the personas active in this scenario, the KPIs realized, the HITL gate behavior at the destroy/markdown decision, references to Services Guide §14.3 worked example.

3. **`services/rc/RC-E2E-03/scenarios/rc-cold-chain-excursion-mid-shift/agents/pricing/DESIGN.md`** — The Pricer's full design: role, prompt strategy, MCP tools (`get_pricing_recommendation_basis`, `get_similar_pricing_decisions`), schemas read (`PROML.Pricing`, `PROML.DiscountRule`, `MERML.Elasticity`), HITL behavior (markdown > 30%), Year-1 → Year-3 evolution per Services Guide §25.8, Foundry hosted agent config, episodic memory via Redis.

4. **`services/rc/RC-E2E-03/use-cases/_default/use-case.yaml`** + **`DESIGN.md`** — the canonical Services-Guide-§18.1 envelope rendered as a deployable use case. Every other RC service generator-scaffolds a similar default.

5. **`docs/APEX - Design and Build/services/RC-E2E-03/index.md`** — the architectural-view narrative, linking everything together.

The other 6 RC services + their scenarios + their agents get **rich auto-populated templates** from the xlsx + Services Guide §18; engineers fill in over time.

## 10. RC build plan updates ([`RC-Build-Plan.md`](../APEX%20-%20Design%20and%20Build/RC-Build-Plan.md))

Add to existing sprint plan:

- **Sprint 30.7** — Provision Foundry Hub + Project per AVM module
- **Sprint 30.8** — Adopt MCP server pattern from `azmcp-foundry-aca-mi`
- **New Sprint 31a** — Use Case capture: 1–3 use cases per featured RC service captured as `use-case.yaml` with persona/KPI binding; client interviews drive these
- **Sprint 32 amendments** — agent prompts authored as Microsoft Agent Framework or LangGraph code (the Foundry hosted agent unit)
- **New Sprint 33a** — Foundry hosted agent registration smoke tests; M365 Copilot publishing dry-run
- **Sprint 40 amendments** — fusion edges become Foundry workflow definitions

## 11. Risk and rollback

| Risk | Mitigation |
|---|---|
| Foundry resource types churn between AVM module versions | Pin AVM module version; smoke tests run on every wizard render |
| Foundry hosted-agent quota / region availability differs from Container Apps | Document supported regions per Services Guide §18 use cases; fall back to Container Apps Path A if a region blocks |
| Existing `agent-fleet.bicep` rewrites break the wizard render endpoint | The render endpoint emits parameter JSON that's valid for either runtime; smoke test the JSON shape, not the resource type |
| Books drift from `DESIGN.md` content | Generator scaffolds cross-reference footers; pre-publish CI lane (BL.P.195 in Roadmap.md §2.18) flags missing back-links |

Rollback path: revert the Bicep agent-fleet rewrite; everything else (DESIGN.md scaffolds, persona/KPI registries, use cases, book updates, wizard surface) is additive and stays.

## 12. Acceptance criteria

- [ ] All 7 RC services have a co-located `DESIGN.md`
- [ ] All 5 featured RC scenarios have a co-located scenario `DESIGN.md`
- [ ] Every featured-scenario agent (~36 agents × 7 roles incl. The Pricer where applicable) has an agent `DESIGN.md`
- [ ] Each of the 7 RC services has a `use-cases/_default/use-case.yaml` + `DESIGN.md`
- [ ] `services/_personas.yaml` lists every persona referenced from the Services Guide §18 RC profiles
- [ ] `services/_kpis.yaml` lists every KPI referenced from the Services Guide §18 RC envelopes
- [ ] Generator validates persona/KPI refs resolve; fails loud on dangling refs
- [ ] `infra/bicep/platform/main.bicep` deploys Foundry account + project alongside existing platform resources
- [ ] `infra/bicep/modules/agent-fleet.bicep` deploys Foundry hosted agents
- [ ] `mcp-server.bicep`, `hitl-gate.bicep`, control-plane Bicep, all unchanged
- [ ] Deployment Guide ch 1 + 7 + 11.5 updated; Services Guide ch 18 + new ch 27 updated
- [ ] Wizard tree shows use-case node between service and scenario; render emits use-case-scoped Bicep params
- [ ] `docs/APEX - Design and Build/services/RC-E2E-03/index.md` exists and links into all the co-located `DESIGN.md` files
- [ ] RC-Build-Plan updated with use-case + Foundry sprint items
- [ ] Wizard `/health`, `/api/catalog/tree`, `/api/catalog/build-status`, `/api/catalog/use-cases`, `/api/deployments/render` all return 200 with valid shapes
- [ ] All changes committed on `main`; no worktrees

## 13. References

**APEX books** (existing):
- [Professional APEX Deployment Guide](../book/Professional-APEX-Deployment-Guide.html) — chapters 1, 7, 9, 10, 11
- [Professional APEX Services Guide](../book/Professional-APEX-Services-Guide.html) — chapter 14, 18, 25
- [Professional APEX Sellers Guide](../book/Professional-APEX-Sellers-Guide.html)
- [Professional APEX (canonical)](../book/Professional-APEX.html) — §3.10, §3.11

**APEX repository** (existing):
- [Roadmap.md](../APEX%20-%20Design%20and%20Build/Roadmap.md) — BL.P.91 / BL.P.92 (Fabric capacity), BL.P.110 (RC service catalog), BL.P.117 (Big Box reference deployment)
- [RC-Build-Plan.md](../APEX%20-%20Design%20and%20Build/RC-Build-Plan.md)
- [services/_extras.yaml](../../services/_extras.yaml) — pricing agent extension
- [services/rc/_build-status.yaml](../../services/rc/_build-status.yaml)

**Microsoft Learn**:
- [Build a multiple-agent workflow automation (reference architecture)](https://learn.microsoft.com/azure/architecture/ai-ml/idea/multiple-agent-workflow-automation) — the canonical hybrid this design follows
- [Baseline Microsoft Foundry chat reference architecture](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-chat) — when to use hosted agents
- [Baseline Foundry chat in Azure landing zone](https://learn.microsoft.com/azure/architecture/ai-ml/architecture/baseline-microsoft-foundry-landing-zone)
- [Technology plan for AI agents](https://learn.microsoft.com/azure/cloud-adoption-framework/ai-agents/technology-solutions-plan-strategy) — three build paths
- [Foundry Hosted Agents (Agent Framework)](https://learn.microsoft.com/agent-framework/hosting/foundry-hosted-agent) — `azd deploy` flow
- [What is Microsoft Foundry Agent Service?](https://learn.microsoft.com/azure/foundry/agents/overview)
- [Azure Verified Module — `ai-foundry`](https://github.com/Azure/bicep-registry-modules/tree/main/avm/ptn/ai-ml/ai-foundry) — the Bicep module we adopt
- [Host MCP servers on Azure Container Apps](https://learn.microsoft.com/azure/container-apps/mcp-overview)
- [Self-hosted Azure MCP Server connected to Foundry](https://learn.microsoft.com/azure/developer/azure-mcp-server/how-to/deploy-remote-mcp-server-microsoft-foundry)
- [`azmcp-foundry-aca-mi` sample](https://github.com/Azure-Samples/azmcp-foundry-aca-mi)
