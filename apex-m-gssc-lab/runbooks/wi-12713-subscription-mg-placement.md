# Runbook — WI 12713: APEX-M GSSC Lab Subscription Placement & Policies

**Work item:** [AB#12713](https://dev.azure.com/AI-Assist-Demo-Org/Agentic%20Merch/_workitems/edit/12713)
**Deployed:** <YYYY-MM-DD> by <engineer-email>
**Reference doc:** *APEX-M GSSC Lab Infrastructure Deployment v2.0*, Chapter 3 + Chapter 4 + Appendix A
**Maps to:** Feature F1.1 / Story S1.1.1 — "Provision sub-apex-m-gssc-lab subscription under mg-apex-m-lab"

> **Status:** TEMPLATE — fill the `<placeholder>` values with actuals after the deployment in Task 4. Verify with: `Select-String -Path apex-m-gssc-lab/runbooks/wi-12713-subscription-mg-placement.md -Pattern '<.*>'` (expect no matches when complete).

## As-built

| Property | Value |
|---|---|
| Subscription display name | `sub-apex-m-gssc-lab` |
| Subscription ID | `<actual GUID>` |
| Parent management group | `mg-apex-m-lab` (under `mg-deloitte-dmtsp`) |
| Region (primary / paired) | `eastus2` / `eastus` |
| Owner | `<engineer-email>` |
| Pack-tenant (sub-scope) | `shared` |
| Auto-stop (sub-scope) | `false` |
| Log Analytics workspace | `log-apex-m-gssc-eus2` (`<resource-id>`) |
| Bicep CLI version at deploy | `0.43.8` |
| Deployment name | `<wi-12713-YYYYMMDD-HHMMSS>` |
| Deployment provisioningState | `<Succeeded>` |

## Tags applied (§3.3)

```
apex-m       = lab
env          = gssc-lab
owner        = <engineer-email>
cost-center  = DMTSP-APEX-M-LAB
pack-tenant  = shared
auto-stop    = false
```

Evidence: `tools/_acceptance_evidence/wi-12713-tags.json`.

## Deviations from spec

- _None._

(Replace this section if the actual deploy diverges from the plan — e.g., a different `packTenant` value, an additional diagnostic-settings category, a different Log Analytics workspace. Cite the §-reference that justifies each deviation.)

## Re-deploy

The template is idempotent at MG scope; re-running produces zero changes.

```powershell
az deployment mg create `
  --management-group-id mg-apex-m-lab `
  --location eastus2 `
  --template-file apex-m-gssc-lab/bicep/00-subscription-policies.bicep `
  --parameters apex-m-gssc-lab/bicep/00-subscription-policies.bicepparam
```

Evidence of zero-change re-run: `tools/_acceptance_evidence/wi-12713-whatif-post.txt`.

## Rollback

The subscription itself is owned by Azure central provisioning (§3.1) — Bicep does **not** own its lifecycle. To roll back this work item's changes:

1. **Remove the §3.3 tags** at subscription scope:
   ```powershell
   az tag delete --resource-id "/subscriptions/<actual GUID>" --name apex-m --yes
   az tag delete --resource-id "/subscriptions/<actual GUID>" --name env --yes
   az tag delete --resource-id "/subscriptions/<actual GUID>" --name owner --yes
   az tag delete --resource-id "/subscriptions/<actual GUID>" --name "cost-center" --yes
   az tag delete --resource-id "/subscriptions/<actual GUID>" --name "pack-tenant" --yes
   az tag delete --resource-id "/subscriptions/<actual GUID>" --name "auto-stop" --yes
   ```
2. **Remove diagnostic settings:**
   ```powershell
   az monitor diagnostic-settings subscription delete --subscription <actual GUID> --name send-activity-log-to-loganalytics
   ```
3. **Move subscription under a different MG** (e.g., Tenant Root if decommissioning):
   ```powershell
   az account management-group subscription add --name <other-mg> --subscription <actual GUID>
   ```

Reverting the merge commit alone does **not** roll back the cloud state.

## Observability

- **Destination:** `log-apex-m-gssc-eus2` Log Analytics workspace (resource ID `<resource-id>`).
- **Categories:** Administrative, Security, ServiceHealth, Alert, Recommendation, Policy, Autoscale, ResourceHealth.
- **Sample query:**
  ```kusto
  AzureActivity
  | where SubscriptionId == "<actual GUID>"
  | take 50
  ```
- **Workspace retention:** 30 days (PerGB SKU per Appendix A.2). Long-term retention follows §3 observability policy.

## Independence (§14.1)

- No client data, no client identity, no Microsoft-direct ECIF flow.
- Subscription name, owner email, and all tag values are Deloitte-internal.
- Cost center `DMTSP-APEX-M-LAB` routes to Deloitte DMTSP internal cost center per §14.1.
- This work item touched no client tenant or client identity in its execution.

## API versions and tooling (as deployed)

| Resource | API version | Source |
|---|---|---|
| `Microsoft.Management/managementGroups/subscriptions` | `2023-04-01` (latest stable) | <https://learn.microsoft.com/en-us/azure/templates/microsoft.management/managementgroups/subscriptions> |
| `Microsoft.Management/managementGroups` (existing ref) | `2023-04-01` | Same |
| `Microsoft.Resources/tags` | `2025-04-01` (latest stable) | <https://learn.microsoft.com/en-us/azure/templates/microsoft.resources/tags> |
| `Microsoft.Insights/diagnosticSettings` | `2021-05-01-preview` (latest available; no GA) | <https://learn.microsoft.com/en-us/azure/templates/microsoft.insights/diagnosticsettings> |
| Bicep CLI | `0.43.8` (latest, 2026-05-07) | <https://github.com/Azure/bicep/releases> |
| Azure CLI | `<actual version>` | <https://learn.microsoft.com/en-us/cli/azure/install-azure-cli> |

## Evidence index

All evidence files live in `tools/_acceptance_evidence/` (committed alongside this runbook):

| File | Source command | DoD line |
|---|---|---|
| `wi-12713-whatif-pre.txt` | Task 3 — pre-deploy what-if | #1 (acceptance proof) |
| `wi-12713-deployment.json` | Task 4 — `az deployment mg show` | #1 |
| `wi-12713-subscription-show.json` | Task 5 Step 5 — `az account subscription show` | #1 |
| `wi-12713-mg-placement.json` | Task 5 Step 5 — `az account management-group entities list` | #1 |
| `wi-12713-tags.json` | Task 5 Step 5 — `az tag list` | #4 |
| `wi-12713-diagnostic-settings.json` | Task 5 Step 5 — `az monitor diagnostic-settings subscription list` | #9 |
| `wi-12713-whatif-post.txt` | Task 6 — post-deploy what-if (zero changes) | #8 |

## DoD coverage at hand-off

| DoD line | Evidence |
|---|---|
| 1. Primary acceptance + evidence | `wi-12713-subscription-show.json` + `wi-12713-mg-placement.json` show sub `Enabled` under `mg-apex-m-lab` |
| 2. Bicep on branch, merged via reviewed PR | `git log --grep "AB#12713"` shows ≥ 4 commits; PR link `<PR-URL>` |
| 3. PR linked via AB#12713 | All commit subjects include literal `AB#12713` token |
| 4. Required tags | `wi-12713-tags.json` shows the six §3.3 keys |
| 5. Naming per Appendix A | `sub-apex-m-gssc-lab`, `mg-apex-m-lab`, `log-apex-m-gssc-eus2` |
| 6. Runbook entry | This file |
| 7. Independence guardrails | Section above |
| 8. Idempotency | `wi-12713-whatif-post.txt` — zero `Create | Modify | Delete` rows |
| 9. Logging to `log-apex-m-gssc-eus2` | `wi-12713-diagnostic-settings.json` |
| 10. Cost guardrails (tag + auto-shutdown) | `wi-12713-tags.json` shows `cost-center: DMTSP-APEX-M-LAB` and `auto-stop: false` |
| 11. GSSC Lab Platform Engineering lead approval | PR review record on `<PR-URL>`; reviewer `<lead-alias>`; approved `<YYYY-MM-DD>` |
