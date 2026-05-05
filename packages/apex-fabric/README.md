# apex-fabric

APEX Microsoft Fabric integration package. Sprint 14 deliverables
(BL.P.91–94).

## Scope

| Subtask | Module / artifact | Purpose |
|---|---|---|
| 14.1 | `infra/terraform/modules/fabric_capacity/` | Terraform F-SKU module with cost guardrails |
| 14.2 | `apex_fabric.workspaces` | Fabric workspace REST wrapper + naming-convention enforcement |
| 14.3 | `infra/terraform/blueprints/{single-capacity-tenant,dev-prod-split,per-workload-isolation}/` | Three capacity-pattern blueprints |
| 14.4 | `apex_fabric.shortcuts` | OneLake shortcut provisioning for ADLS Gen2 / S3 / GCS / Dataverse / cross-workspace |

## Quick Start

```bash
# Inside the monorepo:
pip install -e packages/apex-core
pip install -e packages/apex-fabric

# Validate a workspace name against the canonical pattern:
apex fabric validate-name apex-rc-prod-silver

# Generate a canonical name:
apex fabric canonical-name rc prod silver --suffix eu

# Describe a Terraform blueprint:
apex fabric describe-blueprint dev-prod-split
```

## Naming convention

Every APEX workspace follows:

```
apex-{practice}-{environment}-{role}[-{suffix}]
```

| Slot | Allowed values |
|---|---|
| practice | rc / hls / er / axle / tmt / th / ice / core |
| environment | dev / test / stage / prod |
| role | bronze / silver / gold / governance / runtime / sandbox |
| suffix | optional, `[a-z0-9]+` |

The wrapper rejects any non-conforming name. Engagement-specific overrides
must use `WorkspaceSpec(name_override=...)` and require Independence
sign-off captured in the PR.

## Cost guardrail (Task 14.1)

The Terraform module fails plan-time if the chosen F-SKU's estimated
monthly cost exceeds `monthly_budget_usd`. Override only with
`allow_budget_breach = true` and a PR review.

| SKU | Monthly USD (est.) | Notes |
|---|---|---|
| F2 / F4 / F8 / F16 / F32 | 263 / 525 / 1,050 / 2,100 / 4,200 | dev/test only |
| **F64** | 5,475 | **Copilot threshold; minimum for production** |
| F128 / F256 / F512 / F1024 / F2048 | 10,950 / 21,900 / 43,800 / 87,600 / 175,200 | scale tiers |

## Practice-reference shortcut pattern (Task 14.4)

```python
from apex_fabric import practice_reference_shortcuts, ShortcutClient

plan = practice_reference_shortcuts(
    tenant_workspace_id="<tenant-ws>",
    tenant_lakehouse_id="<tenant-lh>",
    practice_reference_workspace_id="<rc-silver-ws>",
    practice_reference_lakehouse_id="<rc-silver-lh>",
    silver_table_names=["scml_sku", "scml_lot", "merml_price"],
)

client = ShortcutClient(token_provider=my_token_provider)
plan.apply(client)
```

This is the "Bronze stays where it is, canonical Silver lives once"
materialization that powers APEX scaling — Sellers Guide §1.6 canonical
schema kernel.

## Cross-reference

- Sellers Guide §1.6 — canonical schema kernel
- Sellers Guide §5.4 — Fabric workspace pattern
- Sellers Guide §6.13.7.4 — F-SKU sizing inflection points
- Sellers Guide Appendix V — cost calculation
- APEX Orchestrator Sprint 14 (BL.P.91–P.94)
