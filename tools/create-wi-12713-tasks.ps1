# tools/create-wi-12713-tasks.ps1
#
# Create 10 child Tasks under Azure DevOps work item AB#12713
# (Feature F1.1 / Story S1.1.1 — APEX-M GSSC Lab subscription placement).
#
# Source plan: docs/plans/2026-05-21-wi-12713-subscription-mg-placement-plan.md
#
# Prerequisites (one-time):
#   az extension add --name azure-devops
#   az devops login                     # PAT with Work Items: Read & Write
#
# Idempotency: running this script twice creates duplicate Tasks. Run once.
# If duplicates appear, remove them via `az boards work-item delete --id <id>`.

$org      = 'https://dev.azure.com/AI-Assist-Demo-Org/'
$project  = 'Agentic Merch'
$parent   = 12713
$plan     = 'docs/plans/2026-05-21-wi-12713-subscription-mg-placement-plan.md'
$tags     = 'apex-m;gssc-lab;infra;governance'

# Optional — set to your actual iteration and area path strings if you want
# the Tasks organized; leave $null to use project defaults.
$iteration = $null   # e.g., 'Agentic Merch\Sprint 1'
$area      = $null   # e.g., 'Agentic Merch\GSSC Lab'

# Title, original-estimate hours, description.
$tasks = @(
  @{ T='WI 12713 / T1 — Verify Bicep on main builds + lints clean';            E=0.08; D="Run az bicep build + lint on all 5 .bicep files; confirm zero diagnostics. See $plan — Task 1." }
  @{ T='WI 12713 / T2 — Resolve param file values from pre-flight';            E=0.08; D="Substitute subscriptionId, ownerEmail, logAnalyticsWorkspaceId in 00-subscription-policies.bicepparam. See $plan — Task 2." }
  @{ T='WI 12713 / T3 — Pre-deploy what-if against mg-apex-m-lab';             E=0.03; D="Run az deployment mg create --what-if; capture to tools/_acceptance_evidence/wi-12713-whatif-pre.txt. See $plan — Task 3." }
  @{ T='WI 12713 / T4 — Deploy 00-subscription-policies.bicep';                E=0.03; D="Run az deployment mg create against mg-apex-m-lab; capture deployment record. See $plan — Task 4." }
  @{ T='WI 12713 / T5 — Acceptance verification (sub, MG, tags, diagnostics)'; E=0.17; D="Run 4 az verification commands; save JSON evidence. Satisfies DoD #1, #4, #9. See $plan — Task 5." }
  @{ T='WI 12713 / T6 — Idempotency verification (post-deploy what-if)';       E=0.03; D="Re-run what-if; expect every resource = Unchanged. Satisfies DoD #8. See $plan — Task 6." }
  @{ T='WI 12713 / T7 — Author runbook (as-built record)';                     E=0.25; D="Create apex-m-gssc-lab/runbooks/wi-12713-subscription-mg-placement.md with actual values. Satisfies DoD #6. See $plan — Task 7." }
  @{ T='WI 12713 / T8 — Stage and commit on main';                             E=0.08; D="Three logical commits: param resolution, evidence + runbook, plan. All include AB#12713. See $plan — Task 8." }
  @{ T='WI 12713 / T9 — Push to origin and open PR (if branch-protected)';     E=0.08; D="git push origin main, or fall back to feature branch + PR if protection blocks. See $plan — Task 9." }
  @{ T='WI 12713 / T10 — GSSC Lab Platform Eng lead review + Closed';          E=0.25; D="Add reviewer, move WI to In Review, await approval, merge, move to Closed. Satisfies DoD #11. See $plan — Task 10." }
)

az devops configure --defaults organization=$org project="$project"

foreach ($t in $tasks) {
  $fields = @(
    "Microsoft.VSTS.Scheduling.OriginalEstimate=$($t.E)",
    "Microsoft.VSTS.Scheduling.RemainingWork=$($t.E)",
    "System.Tags=$tags"
  )

  $createArgs = @(
    'boards', 'work-item', 'create',
    '--type', 'Task',
    '--title', $t.T,
    '--description', $t.D,
    '--fields'
  ) + $fields + @('--query', 'id', '-o', 'tsv')

  if ($iteration) { $createArgs += @('--iteration', $iteration) }
  if ($area)      { $createArgs += @('--area', $area) }

  $id = & az @createArgs

  az boards work-item relation add `
    --id $id `
    --relation-type Parent `
    --target-id $parent `
    --output none

  Write-Host "Created Task $id  ->  parent $parent  ·  $($t.T)"
}

Write-Host ""
Write-Host "Done. View the parent: $org$project/_workitems/edit/$parent"
