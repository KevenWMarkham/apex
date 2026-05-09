# APEX Service Catalog

Source-of-truth folder structure for all APEX services and scenarios. Generated
from [`docs/reference/APEX-Scenario-Chains.xlsx`](../docs/reference/APEX-Scenario-Chains.xlsx)
via [`tools/gen_services_tree.py`](../tools/gen_services_tree.py). Re-run that
script after the spreadsheet changes.

## Counts

| | Count |
|---|---:|
| Industries | 7 |
| Service codes | 38 |
| Total scenarios | 724 |
| Featured (fully scaffolded) | 36 |
| Catalog (registry stub only) | 688 |

## Layout

```
services/
  _registry.json                       # full index of every scenario
  rc/   axle/   er/   hls/   ice/   th/   tmt/
    {SERVICE-CODE}/                    # e.g. RC-E2E-03
      service.yaml                     # service contract
      bicep/
        main.bicep                     # deploys the service for a wave
        agents.bicep                   # service-level agent overrides
      scenarios/
        {scenario-id}/                 # featured only
          scenario.yaml                # 24-step chain
          agents/{role}/agent.yaml      # 6-agent fleet (assess→learn)
          agents/{role}/prompts/*.md
          bicep/scenario.bicep         # scenario overlay
```

Featured scenarios are fully scaffolded with a 6-agent fleet
(`assess`, `classify`, `quantify`, `decide`, `act`, `learn`). Catalog scenarios
live only in `_registry.json` until they are promoted to featured (which means
adding their scenario folder + agent fleet here).

## Industries

| Slug | Label | Service codes |
|---|---|---:|
| `axle/` | Automotive · Aftermarket · Mobility | 5 |
| `er/` | Energy & Resources | 6 |
| `hls/` | Health Care & Life Sciences | 4 |
| `ice/` | Industrial Connected Equipment | 5 |
| `rc/` | Retail & Consumer Products | 7 |
| `th/` | Travel & Hospitality | 5 |
| `tmt/` | Technology · Media · Telecom | 6 |

## Adding a service

1. Add the new `Service Code` row to the spreadsheet's *Scenario Library* sheet.
2. Re-run `python tools/gen_services_tree.py`.
3. Fill in the generated `service.yaml` (personas, schemas).
4. If the service should be deployable: edit `bicep/main.bicep` to compose the
   relevant `infra/bicep/modules/*` and add the service to the wizard registry
   at `apps/deploy-wizard/api/services_catalog.py`.

## Promoting a catalog scenario to featured

1. Mark `Featured?` = `⭐ Featured` in the spreadsheet.
2. Re-run the generator — agent fleet and `scenario.yaml` are scaffolded.
3. Replace the `TBD` placeholders in `agents/*/agent.yaml` with real config.

## Bicep ↔ Terraform

This tree generates **Bicep** modules. Existing Terraform modules under
`infra/terraform/` remain canonical for Fabric capacity, Key Vault, Container
App environments, and Purview (per the architecture book §10). The Bicep modules
under `infra/bicep/` and the per-service Bicep here layer on top — they deploy
*services and agent fleets* into resource groups already provisioned by
Terraform. The `apps/deploy-wizard/` control plane orchestrates both.
