# WI 12713 — Subscription + Management-Group Placement Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Configure the pre-existing `sub-apex-m-gssc-lab` Azure subscription per *APEX-M GSSC Lab Infrastructure Deployment v2.0* Chapter 3 + Chapter 4 + Appendix A — assert placement under `mg-apex-m-lab`, apply the §3.3 tag policy, and route the Activity Log to `log-apex-m-gssc-eus2` — all governed by an idempotent Bicep template, with a runbook and a PR linked to AB#12713.

**Architecture:** A single management-group-scoped Bicep template `00-subscription-policies.bicep` composes three leaf modules (placement, tags, diagnostics). The subscription itself is allocated by Azure central provisioning out of band (§3.1); this template only **configures** the pre-existing subscription. One-pass deploy via `az deployment mg create`. All work lands on `main` (no worktrees).

**Tech Stack:** Bicep CLI **v0.43.8** (latest as of 2026-05-07 — `az bicep install` from Azure CLI ≥ 2.65), Azure CLI for deployment + verification, PowerShell 5.1 / pwsh 7 for orchestration, Markdown for the runbook.

**Folder layout** (per *Deployment doc §4.3*):

```
apex-m-gssc-lab/
├── bicep/
│   ├── 00-subscription-policies.bicep          # top-level (this work item)
│   ├── 00-subscription-policies.bicepparam     # resolved param file
│   ├── README.md                               # folder readme + Microsoft Learn refs
│   └── modules/
│       ├── mg-placement.bicep                  # tenant-scoped MG placement
│       ├── tags.bicep                          # §3.3 tag-shape provider
│       ├── tags-apply.bicep                    # apply tags at sub scope (API 2025-04-01)
│       └── activity-log-diagnostics.bicep      # Activity Log → log-apex-m-gssc-eus2
└── runbooks/
    └── wi-12713-subscription-mg-placement.md   # as-built record (created in Task 6)
```

**Source-of-truth references (read before Task 1):**

| Topic | Source |
|---|---|
| Subscription naming + ownership | *APEX-M GSSC Lab Infrastructure Deployment v2.0* §3.1 — subscription `sub-apex-m-gssc-lab`, MG `mg-apex-m-lab` under `mg-deloitte-dmtsp`, region `eastus2` primary / `eastus` paired, allocated by Azure central provisioning |
| Tag policy | Same doc §3.3 — six tags: `apex-m`, `env`, `owner`, `pack-tenant`, `auto-stop`, `cost-center` |
| Pack-tenant allowed values | Same doc §22.2 — `shared`, `merch`, `finance`, `risk`, `manufacturing`, `cxp`, `esg` |
| Cost-center value | Same doc §14.1 — `DMTSP-APEX-M-LAB` |
| Naming convention | Same doc Appendix A.1 — `<type-prefix>-apex-m-gssc-<purpose>-<region-short>` |
| Folder structure | Same doc §4.3 |
| `Microsoft.Management/managementGroups/subscriptions` (API 2023-04-01 — latest stable) | <https://learn.microsoft.com/en-us/azure/templates/microsoft.management/managementgroups/subscriptions> |
| `Microsoft.Resources/tags` (API 2025-04-01 — latest stable) | <https://learn.microsoft.com/en-us/azure/templates/microsoft.resources/tags> |
| `Microsoft.Insights/diagnosticSettings` (API 2021-05-01-preview — latest available; no GA) | <https://learn.microsoft.com/en-us/azure/templates/microsoft.insights/diagnosticsettings> |
| Bicep subscription-vending pattern | <https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/subscription-vending> |
| ALZ Bicep landing-zone vending (Azure Verified Modules) | <https://github.com/Azure/bicep-lz-vending> |
| Bicep CLI v0.43.8 release | <https://github.com/Azure/bicep/releases> |
| Azure DevOps work item | [AB#12713](https://dev.azure.com/AI-Assist-Demo-Org/Agentic%20Merch/_workitems/edit/12713) |

**Latest API versions chosen (verified against Microsoft Learn on 2026-05-21):**

| Resource | Version used | Why |
|---|---|---|
| `Microsoft.Management/managementGroups/subscriptions` | `2023-04-01` | Latest **stable / GA** (preview `2024-02-01-preview` adds no relevant properties for placement) |
| `Microsoft.Management/managementGroups` (referenced as `existing`) | `2023-04-01` | Pairs with placement above |
| `Microsoft.Resources/tags` | `2025-04-01` | Latest **stable** version on Microsoft Learn |
| `Microsoft.Insights/diagnosticSettings` | `2021-05-01-preview` | Latest available; no GA release exists |

**Tooling validation:**
- Local Bicep: `v0.43.8` — confirmed equal to latest GitHub release (2026-05-07). No upgrade needed.
- Azure CLI: ≥ 2.65 expected. Verify with `az --version`.

---

## Pre-flight checklist — engineer resolves before Task 1

The deployment doc fixes most values. Three operator-provided items remain:

- [ ] **Subscription GUID** for `sub-apex-m-gssc-lab` — supplied by Azure central provisioning (§3.1). Capture from:
   ```powershell
   az account subscription list --query "[?displayName=='sub-apex-m-gssc-lab'].subscriptionId" -o tsv
   ```
   → **resolved value:** `__________________`
- [ ] **Owner email** for the `owner` tag (engineer responsible). Internal Deloitte address per §14.1 Independence. → **resolved value:** `__________________`
- [ ] **Log Analytics workspace ARM ID** for `log-apex-m-gssc-eus2`. Resolve once Feature F6.3 (observability platform) is deployed:
   ```powershell
   az monitor log-analytics workspace show -g rg-apex-m-gssc-observability -n log-apex-m-gssc-eus2 --query id -o tsv
   ```
   → **resolved value:** `__________________`

**Fixed from the doc — do NOT change:**

| Item | Value | Source |
|---|---|---|
| Subscription display name | `sub-apex-m-gssc-lab` | §3.1 |
| Target management group | `mg-apex-m-lab` | §3.1 |
| Region | `eastus2` | §3.1 (Appendix A) |
| Cost center | `DMTSP-APEX-M-LAB` | §14.1 |
| Pack-tenant (sub-scope) | `shared` | §3.3 — sub itself is multi-tenant |
| Auto-stop (sub-scope) | `false` | Sub itself doesn't auto-stop |

**Permissions check:**
- [ ] `Management Group Contributor` on `mg-apex-m-lab` (for placement)
- [ ] `Owner` (or equivalent) on `sub-apex-m-gssc-lab` (for tags + diagnostic settings)
- [ ] Reader on `log-apex-m-gssc-eus2` resource ID (to read its `.id`)

**Working tree preconditions:**
- [ ] On `main` branch, `git pull --ff-only origin main` succeeds
- [ ] `az --version` shows CLI ≥ 2.65 and `bicep` ≥ 0.43.8
- [ ] `az login` then `az account set --subscription sub-apex-m-gssc-lab` (so the deployment context is correct)

**No branch creation** — per the user's main-only workflow. Commits land directly on `main` with the `AB#12713` token.

---

## Notes for the executor

- Every commit message **must** include `AB#12713` exactly once (Azure Boards picks it up on push).
- All Bicep code in `apex-m-gssc-lab/bicep/` is **already authored** in this commit batch — Tasks 1–5 of an earlier worktree pass are now superseded by this single integrated structure on `main`. Files exist and have already been verified `az bicep build` + `az bicep lint` clean.
- The subscription is **pre-created** by Azure central provisioning (§3.1). This work item asserts placement + applies tags + diagnostics on the existing subscription. There is no `Microsoft.Subscription/aliases` resource.
- One-pass deploy. No two-pass orchestration needed (BCP120 doesn't fire because the `subscriptionId` is a literal param, not a runtime expression).
- Independence guardrails (§14.1): no client data, no client identity, no Microsoft-direct ECIF flow. All names, owners, and tags are Deloitte-internal.

---

## Task 1: Verify the authored Bicep is on `main` and builds clean

**Files (already authored — verify, do not rewrite):**
- `apex-m-gssc-lab/bicep/README.md`
- `apex-m-gssc-lab/bicep/00-subscription-policies.bicep`
- `apex-m-gssc-lab/bicep/00-subscription-policies.bicepparam`
- `apex-m-gssc-lab/bicep/modules/mg-placement.bicep`
- `apex-m-gssc-lab/bicep/modules/tags.bicep`
- `apex-m-gssc-lab/bicep/modules/tags-apply.bicep`
- `apex-m-gssc-lab/bicep/modules/activity-log-diagnostics.bicep`
- `.gitignore` — modified to exclude `apex-m-gssc-lab/bicep/**/*.json`

**Step 1: Run build + lint on every file. Expected: all exit 0 with no output.**

```powershell
$az = "C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd"
$root = "apex-m-gssc-lab\bicep"
foreach ($f in @(
    "$root\modules\mg-placement.bicep",
    "$root\modules\tags.bicep",
    "$root\modules\tags-apply.bicep",
    "$root\modules\activity-log-diagnostics.bicep",
    "$root\00-subscription-policies.bicep"
)) {
    & $az bicep build --file $f
    & $az bicep lint --file $f
    if ($LASTEXITCODE -ne 0) { throw "Build/lint failed for $f" }
}
```

**Step 2: Verify `git status` shows the expected untracked files only.**

```powershell
git status --short
```

Expected lines (filtered):
- ` M .gitignore`
- `?? apex-m-gssc-lab/`

The sibling `.json` Bicep build artifacts (`apex-m-gssc-lab/bicep/**/*.json`) must NOT appear — they're auto-ignored.

---

## Task 2: Resolve param values and commit param file

**Step 1: Open `apex-m-gssc-lab/bicep/00-subscription-policies.bicepparam` and substitute the three pre-flight placeholders.**

The committed file ships with these three placeholders that the operator MUST resolve:

```bicep
param subscriptionId = '<sub-apex-m-gssc-lab GUID>'
param ownerEmail = '<engineer-email>'
param logAnalyticsWorkspaceId = '<full-ARM-id-of-log-apex-m-gssc-eus2>'
```

Substitute with the resolved values from the pre-flight checklist.

**Step 2: Verify no remaining placeholders.**

```powershell
Select-String -Path apex-m-gssc-lab/bicep/00-subscription-policies.bicepparam -Pattern '<.*>'
```

Expected: no matches. If any line still matches, resolve before continuing.

---

## Task 3: Pre-deploy `what-if`

**Step 1: Dry-run against `mg-apex-m-lab`.**

```powershell
az deployment mg create `
  --management-group-id mg-apex-m-lab `
  --location eastus2 `
  --template-file apex-m-gssc-lab/bicep/00-subscription-policies.bicep `
  --parameters apex-m-gssc-lab/bicep/00-subscription-policies.bicepparam `
  --what-if
```

Expected (first run, sub not yet under `mg-apex-m-lab` or not yet tagged):
- `+ Microsoft.Management/managementGroups/subscriptions/...` (Create — placement assertion)
- `+ Microsoft.Resources/tags/default` (Create — six tags applied)
- `+ Microsoft.Insights/diagnosticSettings/send-activity-log-to-loganalytics` (Create — Activity Log routing)

If any `Delete` row appears on a first run, **STOP** — the assertion would remove something else. Resolve before deploying.

**Step 2: Save what-if output as evidence.**

```powershell
$evidence = "tools\_acceptance_evidence"
New-Item -ItemType Directory -Path $evidence -Force | Out-Null
az deployment mg create `
  --management-group-id mg-apex-m-lab `
  --location eastus2 `
  --template-file apex-m-gssc-lab/bicep/00-subscription-policies.bicep `
  --parameters apex-m-gssc-lab/bicep/00-subscription-policies.bicepparam `
  --what-if > "$evidence\wi-12713-whatif-pre.txt"
```

---

## Task 4: Deploy

**Step 1: Run the deployment.**

```powershell
$deployName = "wi-12713-$(Get-Date -Format yyyyMMdd-HHmmss)"
az deployment mg create `
  --management-group-id mg-apex-m-lab `
  --location eastus2 `
  --name $deployName `
  --template-file apex-m-gssc-lab/bicep/00-subscription-policies.bicep `
  --parameters apex-m-gssc-lab/bicep/00-subscription-policies.bicepparam
```

Expected duration: ~1–2 minutes (no slow alias-creation step; pure configuration).

Expected outcome: `provisioningState: Succeeded` with `outputs.subscriptionId.value` echoed and `outputs.managementGroupName.value = mg-apex-m-lab`.

**Step 2: Capture deployment record.**

```powershell
az deployment mg show `
  --management-group-id mg-apex-m-lab `
  --name $deployName `
  -o json > "tools\_acceptance_evidence\wi-12713-deployment.json"
```

---

## Task 5: Acceptance verification (Primary acceptance condition)

The DoD's primary acceptance: *"Subscription visible in Azure portal; placed under correct management group."* Verify with four `az` commands, save each as JSON evidence.

**Step 1: Subscription visible + state.**

```powershell
$subId = (Get-Content apex-m-gssc-lab/bicep/00-subscription-policies.bicepparam | Select-String "subscriptionId\s*=\s*'([^']+)'").Matches.Groups[1].Value
az account subscription show --id $subId --query '{name:displayName, state:state}' -o table
```

Expected: `name = sub-apex-m-gssc-lab`, `state = Enabled`.

**Step 2: MG placement.**

```powershell
az account management-group entities list --query "[?name=='$subId'].{name:name, parent:parent.name}" -o table
```

Expected: `parent = mg-apex-m-lab`.

**Step 3: Tags (DoD #4).**

```powershell
az tag list --resource-id "/subscriptions/$subId" --query "properties.tags" -o json
```

Expected keys (per §3.3): `apex-m: lab`, `env: gssc-lab`, `owner: <resolved>`, `cost-center: DMTSP-APEX-M-LAB`, `pack-tenant: shared`, `auto-stop: false`.

**Step 4: Diagnostic settings (DoD #9).**

```powershell
az monitor diagnostic-settings subscription list --subscription $subId --query "value[?name=='send-activity-log-to-loganalytics'].{name:name, ws:properties.workspaceId}" -o table
```

Expected: one row, `ws` matches the resolved `logAnalyticsWorkspaceId`.

**Step 5: Save verification evidence.**

```powershell
$evidence = "tools\_acceptance_evidence"
az account subscription show --id $subId -o json > "$evidence\wi-12713-subscription-show.json"
az account management-group entities list -o json | ConvertFrom-Json | Where-Object name -eq $subId | ConvertTo-Json -Depth 8 > "$evidence\wi-12713-mg-placement.json"
az tag list --resource-id "/subscriptions/$subId" -o json > "$evidence\wi-12713-tags.json"
az monitor diagnostic-settings subscription list --subscription $subId -o json > "$evidence\wi-12713-diagnostic-settings.json"
```

---

## Task 6: Idempotency verification (DoD #8)

**Step 1: Re-run what-if.** Expected: every resource shown as `= Unchanged`. **Zero** `Create | Modify | Delete` rows.

```powershell
az deployment mg create `
  --management-group-id mg-apex-m-lab `
  --location eastus2 `
  --template-file apex-m-gssc-lab/bicep/00-subscription-policies.bicep `
  --parameters apex-m-gssc-lab/bicep/00-subscription-policies.bicepparam `
  --what-if > "tools\_acceptance_evidence\wi-12713-whatif-post.txt"
```

**Step 2: If any drift appears, read the line carefully.** Common false positives:
- `Microsoft.Resources/tags/default` showing `Modify` because Azure normalised tag casing — verify the actual tag values, not the diff shape.
- `Microsoft.Insights/diagnosticSettings/...` showing `Modify` because the `logs[]` order differs from the deployed state — re-sort by `category` if needed.

---

## Task 7: Runbook entry

**Files:**
- Create: `apex-m-gssc-lab/runbooks/wi-12713-subscription-mg-placement.md`

The runbook is the **as-built** record — capture actual values, not placeholders.

```markdown
# Runbook — WI 12713: APEX-M GSSC Lab Subscription Placement & Policies

**Work item:** [AB#12713](https://dev.azure.com/AI-Assist-Demo-Org/Agentic%20Merch/_workitems/edit/12713)
**Deployed:** YYYY-MM-DD by <engineer-email>
**Reference doc:** APEX-M GSSC Lab Infrastructure Deployment v2.0, Chapter 3 + Chapter 4 + Appendix A
**Maps to:** Feature F1.1 / Story S1.1.1 — "Provision sub-apex-m-gssc-lab subscription under mg-apex-m-lab"

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

## Tags applied (§3.3)

```
apex-m       = lab
env          = gssc-lab
owner        = <engineer-email>
cost-center  = DMTSP-APEX-M-LAB
pack-tenant  = shared
auto-stop    = false
```

## Deviations from spec

- _None._

## Re-deploy

The template is idempotent at MG scope; re-running produces zero changes.

\`\`\`powershell
az deployment mg create `
  --management-group-id mg-apex-m-lab `
  --location eastus2 `
  --template-file apex-m-gssc-lab/bicep/00-subscription-policies.bicep `
  --parameters apex-m-gssc-lab/bicep/00-subscription-policies.bicepparam
\`\`\`

Evidence of zero-change re-run: `tools/_acceptance_evidence/wi-12713-whatif-post.txt`.

## Rollback

The subscription itself is owned by Azure central provisioning — Bicep does
not own its lifecycle. To roll back this work item's changes:

1. Remove tags: `az tag delete --resource-id "/subscriptions/<sub-id>" --name <tag-name>` (per tag) or move the sub to a sandbox MG that doesn't enforce these tags.
2. Remove diagnostic settings: `az monitor diagnostic-settings subscription delete --subscription <sub-id> --name send-activity-log-to-loganalytics`.
3. Move the sub under a different MG: portal, or `az account management-group subscription add --name <other-mg> --subscription <sub-id>`.

Reverting the merge commit alone does **not** roll back the cloud state.

## Observability

- Activity Log → `log-apex-m-gssc-eus2`, categories: Administrative, Security, ServiceHealth, Alert, Recommendation, Policy, Autoscale, ResourceHealth.
- Query: `AzureActivity | where SubscriptionId == "<sub-id>" | take 50`.

## Independence (§14.1)

- No client data, no client identity, no Microsoft-direct ECIF flow.
- Subscription, owner email, and all tag values are Deloitte-internal.
- Cost center `DMTSP-APEX-M-LAB` routes to Deloitte DMTSP internal cost center per §14.1.

## API versions and tooling (as deployed)

| Resource | API version | Source |
|---|---|---|
| `Microsoft.Management/managementGroups/subscriptions` | `2023-04-01` (latest stable) | [Microsoft Learn](https://learn.microsoft.com/en-us/azure/templates/microsoft.management/managementgroups/subscriptions) |
| `Microsoft.Resources/tags` | `2025-04-01` (latest stable) | [Microsoft Learn](https://learn.microsoft.com/en-us/azure/templates/microsoft.resources/tags) |
| `Microsoft.Insights/diagnosticSettings` | `2021-05-01-preview` (latest available; no GA) | [Microsoft Learn](https://learn.microsoft.com/en-us/azure/templates/microsoft.insights/diagnosticsettings) |
| Bicep CLI | `0.43.8` (latest, 2026-05-07) | [GitHub releases](https://github.com/Azure/bicep/releases) |
```

Fill every `<actual>` placeholder, run `Select-String -Path apex-m-gssc-lab/runbooks/wi-12713-subscription-mg-placement.md -Pattern '<actual'` — expect no matches.

---

## Task 8: Stage and commit on `main`

Stage and commit in **three logical commits** (cleaner history; each AB#12713 token gets picked up by Azure Boards):

```powershell
# Commit 1 — IaC code + .gitignore rule
git add apex-m-gssc-lab/bicep/ .gitignore
git commit -m "AB#12713 feat(gssc-lab): subscription placement, §3.3 tag policy, Activity Log routing"

# Commit 2 — resolved param file (after Task 2 substitutions)
git add apex-m-gssc-lab/bicep/00-subscription-policies.bicepparam
git commit -m "AB#12713 chore(gssc-lab): resolved subscription param values"

# Commit 3 — acceptance evidence + runbook (after Tasks 3-7)
git add tools/_acceptance_evidence/wi-12713-*.txt tools/_acceptance_evidence/wi-12713-*.json apex-m-gssc-lab/runbooks/wi-12713-subscription-mg-placement.md
git commit -m "AB#12713 docs(gssc-lab): runbook + acceptance evidence for subscription placement"

# Plan update (also AB#12713 — links the design doc into the work item history)
git add docs/plans/2026-05-21-wi-12713-subscription-mg-placement-plan.md
git commit -m "AB#12713 docs: implementation plan for subscription placement"
```

Verify the AB#12713 link picked up:

```powershell
git log --grep "AB#12713" --oneline
```

Expected: at least four matching commits.

---

## Task 9: Push and open PR

**Step 1: Push to remote.**

```powershell
git push origin main
```

Note: pushing directly to `main` requires either branch-protection bypass (Owner privilege) or — if branch protection is enforced — switch to a feature branch first. The deployment doc §12.3 implies a feature-branch + PR flow; the user's "main only" workflow assumes the engineer has direct push or branch-protection-bypass authority. If protection blocks the push, fall back to:

```powershell
git checkout -b feature/wi-12713-subscription-mg-placement
git push -u origin feature/wi-12713-subscription-mg-placement
```

**Step 2: Open the PR (skip if pushed directly to `main`).**

If using Azure Repos:

```powershell
az repos pr create `
  --title "WI 12713 — APEX-M GSSC Lab subscription placement & policies" `
  --description "Places sub-apex-m-gssc-lab under mg-apex-m-lab, applies §3.3 tags, and routes Activity Log to log-apex-m-gssc-eus2. AB#12713" `
  --source-branch feature/wi-12713-subscription-mg-placement `
  --target-branch main `
  --work-items 12713
```

If using GitHub:

```powershell
gh pr create `
  --title "WI 12713 — APEX-M GSSC Lab subscription placement & policies" `
  --body "Places sub-apex-m-gssc-lab under mg-apex-m-lab, applies §3.3 tags, and routes Activity Log to log-apex-m-gssc-eus2.`n`nWork item: AB#12713"
```

---

## Task 10: GSSC Lab Platform Engineering lead review (DoD #11)

**Step 1: Add the reviewer.**

```powershell
# Azure Repos:
az repos pr reviewer add --id <PR-id> --reviewers <team-lead-alias>

# GitHub:
gh pr edit <PR-#> --add-reviewer <team-lead-alias>
```

**Step 2: Move WI 12713 to "In Review" in Azure DevOps. Do not move to Closed until the lead approves.**

**Step 3: After approval — merge to `main`, verify CI green, move WI 12713 to Closed with comment:**

> Merged via <PR-link>. As-built captured in `apex-m-gssc-lab/runbooks/wi-12713-subscription-mg-placement.md`.

---

## Variant — if the subscription has NOT been provisioned yet

If pre-flight reveals Azure central provisioning has not yet allocated `sub-apex-m-gssc-lab`, this work item is **blocked**. Open a ticket with the central provisioning team referencing this work item, and do not proceed with Tasks 3+. The deployment doc §3.1 explicitly delegates subscription creation to central provisioning; per *bicep-lz-vending* and the [Azure subscription-vending design guidance](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/landing-zone/design-area/subscription-vending), this is the correct separation of concerns for a regulated enterprise.

A future evolution (not in this work item) could integrate the [Azure/bicep-lz-vending](https://github.com/Azure/bicep-lz-vending) Azure Verified Modules pattern for self-service subscription creation, but that requires a billing-scope grant the lab does not currently have.

---

## DoD coverage map

| DoD item | Covered by |
|---|---|
| 1. Primary acceptance + evidence | Task 5 (4 `az` verification commands + JSON evidence) |
| 2. Bicep module on feature branch, merged via reviewed PR | Tasks 1–8 + Tasks 9–10 |
| 3. PR linked via AB#12713 | All commit messages + Task 9 work-item link |
| 4. Required tags | `modules/tags.bicep` (6 keys, 7 pack-tenant values) + `modules/tags-apply.bicep` + Task 5 Step 3 |
| 5. Naming per Appendix A | Fixed values in plan + Appendix A.1 |
| 6. Runbook entry | Task 7 |
| 7. Independence guardrails | Pre-flight constraint + runbook §Independence |
| 8. Idempotency | Task 6 (`what-if` post-deploy shows zero changes) |
| 9. Logging to `log-apex-m-gssc-eus2` | `modules/activity-log-diagnostics.bicep` + Task 5 Step 4 |
| 10. Cost guardrails (tag for rollup, auto-shutdown participation) | `cost-center` + `auto-stop` tags in §3.3 schema |
| 11. GSSC Lab Platform Engineering lead approval | Task 10 |

---

## Estimated effort

- Task 1 (verify IaC clean): ~5 minutes
- Task 2 (resolve param file): ~5 minutes
- Task 3 (`what-if`): ~2 minutes
- Task 4 (deploy): ~1–2 minutes
- Task 5 (verification): ~10 minutes
- Task 6 (idempotency re-run): ~2 minutes
- Task 7 (runbook): ~15 minutes
- Tasks 8–9 (commits + PR): ~10 minutes
- Task 10 (review cycle): reviewer SLA dependent

**Total engineer time: ~50 minutes active. Wall clock to Closed: 1 business day (review SLA dependent).**
