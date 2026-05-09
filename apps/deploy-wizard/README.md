# APEX Deploy Wizard — Control Plane

A full control plane for deploying APEX onto an Azure tenant and managing it
over time. The wizard is the operator-facing UX for everything covered by
`infra/bicep/` and `services/`.

## Scope (full control plane)

The wizard is **not** a one-shot installer. It owns:

| Capability | Description |
|---|---|
| **Service catalog browser** | Browse all 724 scenarios from `services/_registry.json` filtered by industry, domain, service code, featured/catalog. |
| **Wave-by-wave deploy** | Operator picks tenant + wave (W1/W2/W3) + services + featured scenarios; wizard renders Bicep param files and runs `az deployment group create`. |
| **Tenant management** | Multiple Azure tenants under one wizard install. Each tenant gets its own Cosmos partition for state. |
| **Deployment history** | Every deploy writes an audit row (tenant, wave, services, scenarios, Bicep `what-if` diff, operator identity) to Cosmos. |
| **Drift detection** | Daily job runs Bicep `what-if` against the pinned release manifest; reports divergence per book §3792. |
| **Agent registration** | After Bicep deploys agent fleets, wizard registers them with Agent Service via REST per book §10.5. |
| **HITL gate config** | UI for setting per-scenario approval thresholds (markdown %, refund $, etc.) — written to Key Vault, consumed by `decide`/`act` agents. |
| **Schema discovery** | Pulls Silver-canonical schemas (MERML, SCML, CXML, ...) from Purview and shows which scenarios consume which. |
| **Promotion** | Moves a catalog scenario to featured: scaffolds its agent fleet, drops a PR against the repo. |

## Layout

```
apps/deploy-wizard/
  README.md                        # this file
  api/                             # FastAPI control-plane backend
    pyproject.toml
    src/apex_wizard/
      __init__.py
      main.py                      # FastAPI entrypoint
      catalog.py                   # /api/catalog endpoints
      tenants.py                   # /api/tenants CRUD
      deployments.py               # /api/deployments + Bicep runner
      drift.py                     # /api/drift detector
      hitl.py                      # /api/hitl threshold mgmt
      registry.py                  # services/_registry.json loader
      bicep_runner.py              # subprocess wrapper around `az deployment`
      models.py                    # Pydantic models
    tests/
  web/                             # React + TypeScript frontend
    package.json
    src/
      App.tsx                      # router, layout
      pages/
        Catalog.tsx                # browse 724 scenarios
        Tenants.tsx                # tenant list
        Deploy.tsx                 # wave + service + scenario picker → Bicep
        History.tsx                # past deployments
        Drift.tsx                  # drift report
        HitlConfig.tsx             # threshold editor
      components/
        ServicePicker.tsx
        ScenarioCard.tsx
        WaveStepper.tsx
  bicep/                           # the wizard's own Azure resources
    main.bicep                     # references infra/bicep/control-plane/main.bicep
  parameters/                      # generated parameter files per deployment
    .gitignore                     # ignore generated; keep examples
    examples/
      contoso-w2-pilot.json
```

## Flow: deploying Wave 2 to a tenant

1. Operator opens wizard `/deploy` page.
2. Picks tenant `contoso-prod`, wave `W2`.
3. Picks 1+ service codes (e.g., `RC-E2E-03`, `RC-E2E-04`).
4. For each service, ticks the featured scenarios to deploy.
5. Wizard renders a parameter file:
   ```json
   {
     "tenant": "contoso-prod",
     "containerAppsEnvId": "/subscriptions/.../...",
     "agentIdentityId": "/subscriptions/.../...",
     "selections": [
       {"serviceCode": "RC-E2E-03", "featuredScenarios": ["rc-cold-chain-excursion-mid-shift", "rc-dynamic-markdown-optimization"]},
       {"serviceCode": "RC-E2E-04", "featuredScenarios": ["rc-loyalty-churn-prediction-winback"]}
     ]
   }
   ```
6. Wizard runs:
   ```bash
   az deployment group create \
     --resource-group rg-apex-contoso-prod \
     --template-file infra/bicep/blueprints/w2-pilot.bicep \
     --parameters @parameters/contoso-w2-2026-05-09.json
   ```
7. On success, wizard registers each agent with Agent Service and writes an
   audit row to Cosmos.
8. Drift detector runs daily on cron; flags any tag mismatches.

## Stack

- **API**: Python 3.12 + FastAPI + Pydantic (matches existing apex-* monorepo).
- **Web**: React 19 + TypeScript + Tailwind v4 + shadcn/ui (matches the
  `responsive-ui-system` standard for APEX UIs).
- **State**: Azure Cosmos DB (NoSQL) — tenants, deployments, drift reports.
- **IaC**: Bicep (this wizard's own resources at `bicep/main.bicep`; the
  services it deploys at `infra/bicep/blueprints/*.bicep`).
- **Auth**: Entra ID with managed identity for the API → Cosmos / Key Vault.

## Status

**Scaffold only.** All files in `api/src/apex_wizard/*.py` and `web/src/**`
are stubs marked TBD. The contracts are settled; implementation tracked in a
separate plan.
