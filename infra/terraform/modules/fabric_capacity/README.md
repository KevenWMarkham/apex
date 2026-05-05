# Fabric Capacity Terraform Module

**Sprint 14 Task 14.1 (BL.P.91)** — provisions one `azurerm_fabric_capacity`
with APEX-canonical naming, tagging, and cost guardrails.

## Inputs

| Variable | Required | Default | Notes |
|---|---|---|---|
| `resource_group_name` | yes | — | Existing RG. |
| `location` | yes | — | Azure region. |
| `sku` | yes | — | F2 / F4 / F8 / F16 / F32 / F64 / F128 / F256 / F512 / F1024 / F2048. |
| `environment` | yes | — | dev / test / stage / prod. |
| `practice` | yes | — | rc / hls / er / axle / tmt / th / ice / core. |
| `capacity_admins` | yes | — | At least one UPN or Entra group ID. |
| `name_override` | no | `null` | Bypass canonical naming. |
| `suffix` | no | `null` | Appended to canonical name. |
| `monthly_budget_usd` | no | `999999` | Cost guardrail. Fails plan if exceeded. |
| `allow_budget_breach` | no | `false` | Override the budget guardrail (PR review required). |
| `cost_center` | no | `TBD` | Stamped to tag. |
| `owner` | no | `deloitte-apex-team` | Stamped to tag. |
| `tags` | no | `{}` | Merged with canonical APEX tag set. |

## Cost guardrail

Approximate F-SKU list-price-per-month (USD, PAYGO, illustrative — final
costs come from Microsoft):

| SKU | USD/mo |
|---|---|
| F2 | 263 |
| F4 | 525 |
| F8 | 1,050 |
| F16 | 2,100 |
| F32 | 4,200 |
| **F64** | 5,475 *(Copilot threshold)* |
| F128 | 10,950 |
| F256 | 21,900 |
| F512 | 43,800 |
| F1024 | 87,600 |
| F2048 | 175,200 |

If `sku_monthly_usd[var.sku] > var.monthly_budget_usd` the module **fails
at plan time** unless `var.allow_budget_breach = true` is explicitly set
(which should require a separate PR with sign-off).

## Production rule

Production environments must use **F64 or larger** — F2-F32 are
dev/test-only tiers (no Copilot, insufficient capacity for Practice
workloads). The module's `precondition` enforces this.

## Outputs

- `id` — Azure resource ID
- `name` — canonical name
- `sku` — provisioned tier
- `estimated_monthly_cost_usd` — used by parent stacks for chargeback dashboards
- `tags` — canonical tag set (used by Purview classification policies)
- `canonical_naming_pattern` — the pattern used

## Cross-reference

- Sellers Guide §1.6 (canonical schema kernel)
- Sellers Guide §6.13.7.4 (F-SKU sizing inflection points)
- Sellers Guide Appendix V (cost calculation)
- APEX Orchestrator Sprint 14 Task 14.1
