# APEX Deploy Wizard — Control Plane

A full control plane for deploying APEX onto a client tenant and managing
it over time. The wizard is the operator-facing UX for everything covered
by `apex-m/infra/bicep/` and `services/`.

The wizard itself is provider-neutral but ships first against APEX-M
(the Microsoft variant). When APEX-G and APEX-A variants ship, the
wizard's render endpoint adds Terraform / CloudFormation paths alongside
Bicep — same wizard, different IaC dialect.

## Scope (full control plane)

The wizard is **not** a one-shot installer. It owns:

| Capability | Description |
|---|---|
| **Treeview wizard** | Practice → Service → Scenario → Agent treeview with tri-state checkboxes. Selections roll up — tick a practice and every featured scenario beneath it is included. Implementation: `web/src/pages/Wizard.tsx` + `web/src/components/TreeView.tsx`. Powered by `GET /api/catalog/tree`. |
| **Service catalog browser** | Browse all 724 scenarios from `services/_registry.json` filtered by industry, domain, service code, featured/catalog. |
| **Wave-by-wave deploy** | Operator picks tenant + wave (W1/W2/W3) + services + featured scenarios; wizard renders Bicep param files (`POST /api/deployments/render`) and runs `az deployment group create`. |
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
        Wizard.tsx                 # default — Practice→Service→Scenario→Agent treeview deploy
        Catalog.tsx                # browse 724 scenarios
        Tenants.tsx                # tenant list
        Deploy.tsx                 # legacy stepper view
        History.tsx                # past deployments
        Drift.tsx                  # drift report
        HitlConfig.tsx             # threshold editor
      components/
        TreeView.tsx               # recursive tri-state-checkbox treeview
  bicep/                           # the wizard's own Azure resources
    main.bicep                     # references apex-m/infra/bicep/control-plane/main.bicep
  parameters/                      # generated parameter files per deployment
    .gitignore                     # ignore generated; keep examples
    examples/
      contoso-w2-pilot.json
```

## Wizard flow — Practice → Service → Scenario → Agent

This is the canonical layered model from
[`docs/book/Professional-APEX-M-Deployment-Guide.html`](../../docs/book/Professional-APEX-M-Deployment-Guide.html)
chapters 1 and 7. The wizard's treeview enforces it:

1. Operator opens `/wizard` (the default route).
2. **Practice level** — picks one or more of the 7 industry practices
   (RC, HLS, ER, AXLE, TH, TMT, ICE). Selecting a practice rolls up to
   include every deployable service beneath it.
3. **Service level** — drills into a practice and picks specific service
   codes (e.g., `RC-E2E-03`). Each service has a 1:1:1 binding to a
   deployment Bicep module, a commercial envelope, and an audit attribution
   key (book §7.1).
4. **Scenario level** — within a service, picks the featured scenarios to
   include. Featured scenarios are the 36 with full agent-fleet scaffolds;
   catalog-only scenarios are not deployable from the wizard until promoted.
5. **Agent level** — within a scenario, optionally narrows to specific
   agents (e.g., deploy only "The Analyst" + "The Briefer" in W1).
6. Picks **tenant** + **wave** (W1 / W2 / W3) in the right-hand panel.
7. Clicks **Render Bicep parameters** → calls
   `POST /api/deployments/render` which returns the parameter file for
   the matching blueprint.
8. Reviews summary + parameters in-place. (Confirm-and-deploy flow which
   shells out to `az deployment group create` — wired but not yet
   implemented; see `bicep_runner.py`.)

### Tri-state selection rules

- Tick a node → the node + every descendant are added to the selection.
- Untick a node → the node + every descendant are removed.
- Selecting a parent then unticking one child → parent shows partial
  (indeterminate) state.
- Empty selection disables Render.

### Roll-up rule (server side)

When the API receives a selection, it walks the registry:
- Practice tick → all featured scenarios in that practice.
- Service tick → all featured scenarios in that service.
- Scenario tick (explicit) → that scenario, even if not featured.
- Agent tick → that role only, within its parent scenario.

Featured-only is enforced for inherited selections (parent ticks);
explicit scenario picks bypass it. This keeps the operator from
accidentally deploying a catalog stub that has no agent fleet.

## Endpoints

| Method · Path | Description |
|---|---|
| `GET /api/catalog/tree?featured_only=true` | The 4-level tree the wizard renders. |
| `GET /api/catalog/practices` | 7 practices with slug + label. |
| `GET /api/catalog/services?industry=rc` | Service codes filtered by practice. |
| `GET /api/catalog/scenarios?service_code=RC-E2E-03&featured_only=true` | Scenarios (filterable). |
| `POST /api/deployments/render` | Selection → Bicep parameter file (preview). |
| `POST /api/deployments` | Render + execute (TBD). |
| `GET /api/deployments` | Past deployments (TBD). |
| `GET /api/drift/{tenant}` | Drift report (TBD). |
| `GET / PUT /api/hitl` | Per-scenario HITL thresholds (TBD). |

## Stack

- **API**: Python 3.12 + FastAPI + Pydantic + PyYAML.
- **Web**: React 19 + TypeScript + Tailwind v4. Treeview is custom (zero
  external dep) — see [`web/src/components/TreeView.tsx`](web/src/components/TreeView.tsx).
- **State**: Azure Cosmos DB (NoSQL) for tenants, deployments, drift.
- **IaC**: Bicep — wizard's own resources at [`bicep/main.bicep`](bicep/main.bicep);
  APEX-M services deploy via [`apex-m/infra/bicep/blueprints/*.bicep`](../../apex-m/infra/bicep/blueprints/).
  When APEX-G / APEX-A ship, render endpoint also emits Terraform /
  CloudFormation paths.
- **Auth**: Microsoft Entra ID + Entra Agent ID for the API → Cosmos / Key Vault.

## Status

| Component | Status |
|---|---|
| Treeview + Wizard page | **Working draft** — fetches tree, posts render |
| `GET /api/catalog/tree` | **Working** — pulls from `services/_registry.json` |
| `POST /api/deployments/render` | **Working** — emits Bicep param JSON |
| `POST /api/deployments` (execute) | **TBD** — `bicep_runner.py` stub |
| Tenants / History / Drift / HITL pages | **Scaffold** — page stubs only |

## Note on agent labels

The deployment guide §7.2 names the canonical 5-persona agent set
("The Analyst · The Demand Checker · The Finance Lead · The Operations
Lead · The Briefer"). The featured-scenario folders generated from the
xlsx today use the generic 6-stage names (`assess` / `classify` /
`quantify` / `decide` / `act` / `learn`). The tree endpoint surfaces
whatever's on disk; for catalog scenarios (no on-disk dirs) it falls
back to the canonical persona set. To unify, regenerate the agent
folders with persona names — tracked separately.
