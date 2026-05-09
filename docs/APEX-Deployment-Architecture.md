# APEX Deployment Architecture

How the new folder structure fits together with the existing codebase, and the
end-to-end flow from operator click → running agent fleet on Azure.

## Three new top-level folders

```
APEX/
├─ services/                    NEW — service catalog (7 industries / 38 codes / 724 scenarios)
├─ infra/bicep/                 EXTENDED — platform + modules + blueprints + control-plane
├─ apps/deploy-wizard/          NEW — control-plane API + web + own Bicep
│
├─ packages/                    EXISTING — apex-* runtime libs (unchanged)
├─ infra/terraform/             EXISTING — Fabric, KV, CA env, Purview (unchanged)
├─ docs/                        EXISTING — book, reference, scenarios
```

The wizard reads the catalog from `services/_registry.json`, renders parameter
files for `infra/bicep/blueprints/*.bicep`, and tracks state in Cosmos.

## End-to-end flow

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. Spreadsheet — APEX-Scenario-Chains.xlsx                             │
│    Source of truth for the 724 scenarios.                              │
└────────────────────────────────────────────────────────────────────────┘
            │ python tools/gen_services_tree.py
            ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 2. services/ folder tree                                               │
│    services/_registry.json   — flat index for the wizard               │
│    services/{industry}/{code}/service.yaml + bicep/                    │
│    services/{industry}/{code}/scenarios/{id}/scenario.yaml + agents/   │
└────────────────────────────────────────────────────────────────────────┘
            │ operator opens apps/deploy-wizard/
            ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 3. Wizard UI                                                           │
│    Tenant + Wave + Service codes + Featured scenarios → Bicep params   │
└────────────────────────────────────────────────────────────────────────┘
            │ az deployment group create
            ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 4. Bicep blueprints                                                    │
│    w1-foundation.bicep    → platform/main.bicep (identity/ledger/mon)  │
│    w2-pilot.bicep         → modules/service.bicep × N (agent fleets)   │
│    w3-scale-fuse.bicep    → service.bicep × N + fusion edges           │
└────────────────────────────────────────────────────────────────────────┘
            │ Container Apps + managed identity + Key Vault
            ▼
┌────────────────────────────────────────────────────────────────────────┐
│ 5. Running APEX                                                        │
│    6 agents per featured scenario × N scenarios on Container Apps      │
│    Each agent registered with Agent Service via wizard                 │
│    HITL gates routed via Teams Adaptive Cards                          │
│    Audit rows written to apex_ledger SQL                               │
│    Drift detector cron runs daily on Bicep what-if                     │
└────────────────────────────────────────────────────────────────────────┘
```

## Why Bicep parallel to Terraform

| Concern | IaC |
|---|---|
| Fabric capacity, Key Vault, Container Apps env, Purview | Terraform (existing, per book §10) |
| Tenant identity, ledger, monitoring | Bicep (`platform/`) |
| Per-service agent fleets | Bicep (`modules/agent-fleet.bicep`) |
| Wave blueprints | Bicep (`blueprints/*.bicep`) |
| Wizard control plane itself | Bicep (`control-plane/main.bicep`) |

Terraform is great at long-lived foundational resources. Bicep is what the
wizard renders dynamically per deployment — choosing scenarios at runtime is
much cleaner with Bicep's `for ... in selections` pattern than with Terraform's
`for_each` over JSON-decoded operator input.

## Promotion path: catalog → featured

A scenario starts as a one-line entry in `services/_registry.json` (688 of
them). To make it deployable:

1. Edit `docs/reference/APEX-Scenario-Chains.xlsx`, set `Featured?` = `⭐ Featured`.
2. Run `python tools/gen_services_tree.py` → scaffolds the scenario folder
   and 6-agent fleet.
3. Fill in the agent stubs (model, tools, schemas, prompts).
4. PR + merge.
5. The wizard picks it up automatically on next refresh.

## Drift detection

Per book §3792: a daily job compares deployed state of each tenant against the
pinned release manifest. The wizard's `drift.py` route runs `az deployment
group what-if` for the tenant's last-deployed parameter file and structures
the diff. Any divergence:

- Writes a row to `apex_drift_log` (Silver canonical).
- Posts a Teams alert to the practice SRE.

## Status

| Layer | Status |
|---|---|
| `services/` tree (7/38/724) | **Generated** — re-run script after xlsx changes |
| `infra/bicep/platform/` | **Skeleton** — identity, ledger, monitoring real |
| `infra/bicep/modules/agent-fleet.bicep` | **Working draft** — Container App + identity + env vars |
| `infra/bicep/modules/service.bicep` | **Working draft** — composes fleet × N |
| `infra/bicep/blueprints/w1-w3` | **Skeleton** — call patterns settled |
| `apps/deploy-wizard/api` | **Scaffold** — routes wired, all 501 |
| `apps/deploy-wizard/web` | **Scaffold** — routes + page stubs |
| `apps/deploy-wizard/bicep/main.bicep` | **Working draft** — wraps control-plane |
