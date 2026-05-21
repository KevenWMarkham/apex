# APEX-M GSSC Lab — Bicep IaC

Day-0 Bicep modules for the APEX-M GSSC Lab subscription, per
*APEX-M GSSC Lab Infrastructure Deployment v2.0* (Chapter 12 lists the full
11-module deployment sequence).

## Scope

This folder owns the numbered top-level templates that run during the Day-0
provisioning sequence (§12.1). Modules under `modules/` are shared helpers.

| Template | Purpose | Feature / Story |
|---|---|---|
| `00-subscription-policies.bicep` | Place `sub-apex-m-gssc-lab` under `mg-apex-m-lab`, apply §3.3 tag policy, route Activity Log to `log-apex-m-gssc-eus2` | F1.1 / S1.1.1 |

Modules `01-` through `10-` (network, identity, Fabric, Foundry, Key Vault,
Purview, AKS, observability, per-tenant template) are out of scope of this
work item.

## Conventions

- **Naming** — per *Appendix A — Naming Convention & SKU Reference*: pattern
  `<type-prefix>-apex-m-gssc-<purpose>-<region-short>`. Subscription is
  `sub-apex-m-gssc-lab`; management group is `mg-apex-m-lab` under
  `mg-deloitte-dmtsp`; Log Analytics is `log-apex-m-gssc-eus2`.
- **Tag policy** — six required tags per §3.3:
  `apex-m`, `env`, `owner`, `pack-tenant`, `auto-stop`, `cost-center`.
  Pack-tenant allowed values per §22.2: `shared`, `merch`, `finance`, `risk`,
  `manufacturing`, `cxp`, `esg`.
- **Subscription origin** — subscriptions are allocated by Azure central
  provisioning (§3.1). These templates configure pre-existing subscriptions;
  no `Microsoft.Subscription/aliases` resource is required.
- **Region** — `eastus2` primary, `eastus` paired (§3.1).
- **Verification** — `az bicep build` + `az bicep lint` must exit 0. The
  only acceptable warning is `BCP081` on preview API versions for which no
  GA equivalent exists.

## Authoritative references

| Topic | Source |
|---|---|
| Folder structure | *APEX-M GSSC Lab Infrastructure Deployment* §4.3 |
| Naming | *APEX-M GSSC Lab Infrastructure Deployment* Appendix A.1 |
| Tag policy | *APEX-M GSSC Lab Infrastructure Deployment* §3.3 |
| Pack-tenant allowed values | *APEX-M GSSC Lab Infrastructure Deployment* §22.2 |
| Cost-center value | *APEX-M GSSC Lab Infrastructure Deployment* §14.1 |
| `Microsoft.Management/managementGroups/subscriptions` | <https://learn.microsoft.com/en-us/azure/templates/microsoft.management/managementgroups/subscriptions> |
| `Microsoft.Resources/tags` | <https://learn.microsoft.com/en-us/azure/templates/microsoft.resources/tags> |
| `Microsoft.Insights/diagnosticSettings` | <https://learn.microsoft.com/en-us/azure/templates/microsoft.insights/diagnosticsettings> |
| Bicep subscription vending pattern | <https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/subscription-vending> |
| ALZ Bicep landing-zone vending (Azure Verified Modules) | <https://github.com/Azure/bicep-lz-vending> |

## Deploy

See [`../runbooks/wi-12713-subscription-mg-placement.md`](../runbooks/wi-12713-subscription-mg-placement.md).
