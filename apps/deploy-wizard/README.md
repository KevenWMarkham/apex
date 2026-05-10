# APEX Deploy Wizard — Control Plane

A full control plane for deploying APEX onto a client tenant and managing
it over time. The wizard is the operator-facing UX for everything covered
by `apex-m/infra/bicep/` and `services/`.

The wizard itself is provider-neutral but ships first against APEX-M
(the Microsoft variant). When APEX-G and APEX-A variants ship, the
wizard's render endpoint adds Terraform / CloudFormation paths alongside
Bicep — same wizard, different IaC dialect.

---

## Quick start — launch the wizard (mock mode, no Azure needed)

```bash
# One command brings up backend + frontend:
python apps/deploy-wizard/launch.py

# Or for backend only:
python apps/deploy-wizard/launch.py --no-frontend

# Or with real az calls (requires az CLI + Lab Azure subscription):
python apps/deploy-wizard/launch.py --real
```

Once running, open:

- **Wizard**:        http://localhost:5173/wizard
- **Security Gate**: http://localhost:5173/security-gate
- **Roadmap**:       http://localhost:5173/roadmap
- **API docs**:      http://localhost:8000/docs
- **Health**:        http://localhost:8000/health

### First-run setup

| Component | Setup |
|---|---|
| Python backend | `pip install fastapi uvicorn[standard] pydantic httpx pyyaml`<br>`pip install -e apps/deploy-wizard/api` |
| Node frontend | Install Node 20+. The launcher runs `npm install` automatically on first run. |
| Real-mode `az` | Install Azure CLI: https://learn.microsoft.com/cli/azure/install-azure-cli. `az login` against the Lab tenant. |

### Mock mode vs real mode

| Mode | When to use | What happens |
|---|---|---|
| **mock** (default) | Demos, laptop dev, CI, user-acceptance review | `apex_wizard.bicep_runner` returns synthetic what-if diffs + correlation IDs. 14 of 15 security gates report mock-green; PSG-15 evaluates real persona bindings against use-case data. |
| **real** (`--real`) | Lab deploy, prod deploy | Shells out to `az deployment group what-if` / `create`. Requires `az login` on the tenant. |

The same code paths fire in both modes; the runner is dual-mode by design.
You can develop the wizard against mocks then flip a flag to deploy live.

---

## The 6-step wizard flow

The wizard's `/wizard` page walks an operator through six steps:

1. **Pick services + scenarios + agents** in the treeview (Practice → Service → Scenario → Agent).
2. **Pick substrate** (laptop · dev · stage · prod) and **variant** (APEX-M).
3. **Pick a use case** from the dropdown (e.g., `rc-e2e-03--default` or a cloned client variant).
4. **Click "Render"** → wizard calls `POST /api/deployments/render`. Output is `docker-compose.yml` for laptop or Bicep parameter JSON for cloud.
   - Wizard also polls `GET /api/security-gate?tenant=X` and shows all 15 gates in-line.
5. **Tick "I have reviewed the diff"** when the rendered diff is acceptable. Required when what-if reports destructive changes (Delete).
6. **Click "Deploy"** → wizard calls `POST /api/deployments`. Server orchestrates:
   - Re-evaluate all 15 security gates → 409 if any blocking gate is red
   - Run `bicep_runner.what_if` → attach diff summary
   - Run `bicep_runner.deploy` → return record with status + correlation id

The deployment record shows up immediately with status + audit-row id. Drift
detection runs daily and surfaces on the `/drift` page.

---

## Pages

| Route | Purpose |
|---|---|
| `/wizard` | Default landing — full deploy flow with treeview + render + deploy |
| `/security-gate` | Pre-deployment Security Gate dashboard (PSG-1 through PSG-15) — poll by tenant, optionally with use-case context for PSG-15 |
| `/roadmap` | Sprint progress per `services/<practice>/_build-status.yaml` |
| `/catalog` | Browse all 724 scenarios from `services/_registry.json` |
| `/adapters` | Adapter inventory (per-engagement bindings to Salesforce / Snowflake / Splunk / Okta / etc.) |
| `/tenants` | Multi-tenant management |
| `/history` | Past deployments (`GET /api/deployments`) |
| `/drift` | Drift reports per tenant (`GET /api/drift/{tenant}`) |
| `/hitl` | Per-scenario HITL threshold editor → Key Vault |

---

## API endpoints

| Method · Path | Description |
|---|---|
| `GET /health` | Service health |
| `GET /api/catalog/tree?featured_only=true` | Practice → Service → Scenario → Agent tree |
| `GET /api/catalog/practices` | 7 practices |
| `GET /api/catalog/services?industry=rc` | Services filtered by practice |
| `GET /api/catalog/scenarios?service_code=RC-E2E-03` | Scenarios (filterable) |
| `GET /api/catalog/use-cases` | Use cases per service |
| `POST /api/deployments/render` | Selection → `docker-compose.yml` (laptop) or Bicep params (cloud) |
| `POST /api/deployments` | **Full deploy: PSG check → what-if → confirm-destructive → apply → audit row** (Sprint 46.3) |
| `GET /api/deployments?tenant=X` | List past deployments |
| `GET /api/deployments/{id}` | Get one deployment record |
| `GET /api/security-gate?tenant=X` | Poll all 15 gates (PSG-15 returns UNKNOWN without context) |
| `POST /api/security-gate/with-context` | Poll with use-case data so PSG-15 evaluates fully |
| `GET /api/drift/{tenant}` | On-demand drift check |
| `GET /api/drift/{tenant}/history` | Recent drift reports |
| `GET /api/hitl/{tenant}/{service}/{scenario}` | HITL threshold get/set |

Full OpenAPI docs at http://localhost:8000/docs once the backend is running.

---

## Layout

```
apps/deploy-wizard/
  README.md                        # this file
  launch.py                        # one-command launcher (backend + frontend)
  api/                             # FastAPI control-plane backend
    pyproject.toml
    src/apex_wizard/
      main.py                      # FastAPI entrypoint
      catalog.py                   # /api/catalog endpoints
      tenants.py                   # /api/tenants CRUD
      deployments.py               # /api/deployments + Bicep runner
      security_gate.py             # /api/security-gate aggregator (Sprint 46.2)
      drift.py                     # /api/drift detector (Sprint 46.4)
      hitl.py                      # /api/hitl threshold mgmt
      registry.py                  # services/_registry.json loader
      bicep_runner.py              # Sprint 46.1 — Mock + RealBicepRunner
      models.py                    # Pydantic models
    tests/                         # 43 unit + integration tests
  web/                             # React + TypeScript frontend
    package.json
    src/
      App.tsx                      # router, layout
      pages/
        Wizard.tsx                 # 6-step deploy flow with deploy button
        SecurityGate.tsx           # PSG-1 through PSG-15 dashboard
        Catalog.tsx                # browse 724 scenarios
        Tenants.tsx                # tenant list
        History.tsx                # past deployments
        Drift.tsx                  # drift report
        HitlConfig.tsx             # threshold editor
        Adapters.tsx               # adapter inventory
        Roadmap.tsx                # sprint progress
        Deploy.tsx                 # legacy stepper (kept for back-compat)
      components/
        TreeView.tsx               # recursive tri-state-checkbox treeview
  bicep/                           # the wizard's own Azure resources
    main.bicep
  parameters/                      # generated parameter files per deployment
```

---

## Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12 · FastAPI · Pydantic v2 · uvicorn |
| Frontend | React 19 · TypeScript · Vite · Tailwind v4 |
| State (production) | Azure Cosmos DB (NoSQL) for tenants/deployments/drift |
| State (mock mode) | In-memory dicts; reset on backend restart |
| IaC | Bicep — wizard's own resources at `bicep/main.bicep`; service blueprints at `apex-m/infra/bicep/blueprints/*.bicep` |
| Auth (real mode) | Entra ID + Entra Agent ID for the API → Cosmos / Key Vault / Microsoft Graph |

---

## Status — Sprint 46 complete

| Component | Status |
|---|---|
| Treeview + Wizard page (full 6-step flow) | ✅ **Complete** (Sprint 46.3) — render + security-gate poll + deploy + record persistence |
| Security Gate page (all 15 PSG gates) | ✅ **Complete** (Sprint 46.2) — auto-refresh + use-case context for PSG-15 |
| `bicep_runner.py` (real + mock) | ✅ **Complete** (Sprint 46.1) |
| `POST /api/deployments` end-to-end | ✅ **Complete** (Sprint 46.3) — PSG → what-if → confirm → apply |
| Drift detector + cron entrypoint | ✅ **Complete** (Sprint 46.4) |
| Test coverage (api package) | ✅ **43 tests pass** |
| Real-mode `az` validation | ⏳ **Awaits Lab subscription** (no code changes — flip APEX_FORCE_MOCK=false) |

---

## Note on agent labels

The deployment guide §7.2 names the canonical 5-persona agent set
("The Analyst · The Demand Checker · The Finance Lead · The Operations
Lead · The Briefer"). The featured-scenario folders use the generic 6-stage
names (`assess` / `classify` / `quantify` / `decide` / `act` / `learn`)
with persona labels in the agent.yaml. The tree endpoint surfaces whatever's
on disk; for catalog scenarios it falls back to the canonical persona set.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: apex_wizard` | `pip install -e apps/deploy-wizard/api` from repo root |
| `npm: command not found` (frontend won't start) | Install Node 20+ from nodejs.org; launcher will then run `npm install` automatically |
| Backend starts but frontend can't reach it | Check `VITE_API_URL` (set by launcher to `http://127.0.0.1:8000`). For different hosts, set it manually before `npm run dev`. |
| Deploy returns 409 with `red_gates: ["PSG-15"]` | On prod substrate, the use-case is missing `persona_principal_bindings`. Clone `services/<svc>/use-cases/_default/` to `<client>/` and populate the bindings block. |
| Deploy returns 412 with `destructive_changes_pending_confirm` | What-if shows Delete changes. Re-submit with `note="confirm_destructive=true"` (or tick the checkbox in the Wizard UI). |
| Drift report severity stuck at "high" | One or more deletes were detected; review the report and either re-apply the manifest or update the manifest to accept the change. |
