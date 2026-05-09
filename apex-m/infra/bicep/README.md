# APEX Bicep — Platform & Service IaC

Bicep is the deployment target driven by the [`apps/deploy-wizard/`](../../apps/deploy-wizard/)
control plane. It runs **parallel to** the existing Terraform stack under
[`infra/terraform/`](../terraform/) — Terraform stays canonical for Fabric
capacity, Key Vault, Container App environments, and Purview (per
*Professional-APEX* §10). Bicep here deploys **services and agent fleets** into
resource groups Terraform has already provisioned.

## Layout

```
infra/bicep/
  platform/                          # tenant-level infra the wizard calls first
    main.bicep                       # tenant + identity + ledger + monitoring
    identity.bicep                   # managed identity, RBAC, Entra app
    ledger.bicep                     # SQL ledger / append-only audit row store
    monitoring.bicep                 # Log Analytics, App Insights, alerts
  modules/                           # reusable building blocks
    agent-fleet.bicep                # 6-agent fleet on Container Apps
    mcp-server.bicep                 # MCP server Container App
    service.bicep                    # one APEX service (composes the above)
    hitl-gate.bicep                  # Teams Adaptive Card webhook + audit row
  blueprints/                        # 3-wave deployment shapes
    w1-foundation.bicep              # SOR connect + medallion + canonical
    w2-pilot.bicep                   # 1 service, n featured scenarios
    w3-scale-fuse.bicep              # multi-service + fusion + feedback loop
  control-plane/                     # the wizard's own infra (Container App)
    main.bicep
  redis_control_plane.bicep          # existing — kept as-is
```

## How the wizard uses Bicep

1. Operator picks tenant + wave + services in the wizard UI.
2. Wizard API renders a parameter file from `services/_registry.json` plus
   operator inputs.
3. `az deployment group create` against the right blueprint:
   - Wave 1 → `blueprints/w1-foundation.bicep`
   - Wave 2 → `blueprints/w2-pilot.bicep` with selected service codes
   - Wave 3 → `blueprints/w3-scale-fuse.bicep` with selected scenarios
4. Each blueprint references service modules at
   `services/{industry}/{SERVICE-CODE}/bicep/main.bicep`.
5. Service modules instantiate `modules/agent-fleet.bicep` per featured
   scenario, materializing the 6-agent fleet on Container Apps.

## Calling convention

Every module:
- `targetScope = 'resourceGroup'`
- Takes `tenant` (slug), `wave` (`w1|w2|w3`), and a managed-identity resource ID
- Emits resources tagged with `apex-tenant`, `apex-wave`, `apex-service`,
  `apex-scenario` (when applicable) for drift detection per
  *Professional-APEX* §3792.

## Drift detection

The control plane runs a daily diff between the deployed state and the pinned
release manifest (per book §22). Bicep `what-if` is the diff source.
