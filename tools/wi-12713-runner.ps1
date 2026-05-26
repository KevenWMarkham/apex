# tools/wi-12713-runner.ps1
#
# One-shot orchestrator for Azure DevOps work item AB#12713
# (APEX-M GSSC Lab subscription placement & policies).
#
# Target org/project: AI-Assist-Demo-Org / Agentic Merch
# Target work item:   12713 (Feature F1.1 / Story S1.1.1)
#
# What this runs:
#   1. Environment check (Azure CLI, Bicep CLI, azure-devops extension)
#   2. Auth check (az account show, az boards work-item show 12713)
#   3. Bicep build + lint across all 5 .bicep files (zero-diagnostic gate)
#   4. ADO child-Task creation under WI 12713 (idempotent — skips existing)
#
# What this DOES NOT do (deliberately — too risky to automate):
#   - az login / az devops login (prompts user instead)
#   - Pre-flight value resolution (subscriptionId, ownerEmail, workspace ID)
#   - The Bicep deployment (Tasks 3-6 of the plan)
#   - git push / PR creation
#
# Run with:
#   pwsh C:\Stage\Clients\Industries\APEX\tools\wi-12713-runner.ps1
#   pwsh C:\Stage\Clients\Industries\APEX\tools\wi-12713-runner.ps1 -SkipTasks
#   pwsh C:\Stage\Clients\Industries\APEX\tools\wi-12713-runner.ps1 -OnlyTasks
#
# Exit codes:
#   0  — all checks passed and all requested actions succeeded
#   1  — environment missing a prerequisite (install required)
#   2  — auth missing (run az login + az devops login)
#   3  — Bicep build or lint failed (read diagnostic and fix)
#   4  — ADO task creation failed (read diagnostic)

[CmdletBinding()]
param(
    # Skip the ADO child-Task creation step (useful when only verifying Bicep).
    [switch]$SkipTasks,

    # Run ONLY the ADO child-Task creation (skip env + auth + build/lint).
    [switch]$OnlyTasks,

    # Override the parent work item ID (default 12713).
    [int]$ParentId = 12713
)

$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------------------
# Constants — locked to the AI-Assist-Demo-Org / Agentic Merch project
# ---------------------------------------------------------------------------

$Org      = 'https://dev.azure.com/AI-Assist-Demo-Org/'
$Project  = 'Agentic Merch'
$RepoRoot = (Get-Item (Join-Path $PSScriptRoot '..')).FullName
$Az       = 'C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.cmd'
$Plan     = 'docs/plans/2026-05-21-wi-12713-subscription-mg-placement-plan.md'
$Tags     = 'apex-m;gssc-lab;infra;governance'

$BicepFiles = @(
    'apex-m-gssc-lab\bicep\modules\mg-placement.bicep',
    'apex-m-gssc-lab\bicep\modules\tags.bicep',
    'apex-m-gssc-lab\bicep\modules\tags-apply.bicep',
    'apex-m-gssc-lab\bicep\modules\activity-log-diagnostics.bicep',
    'apex-m-gssc-lab\bicep\00-subscription-policies.bicep'
)

$Tasks = @(
    @{ T='WI 12713 / T1 — Verify Bicep on main builds + lints clean';            E=0.08; D="Run az bicep build + lint on all 5 .bicep files; confirm zero diagnostics. See $Plan — Task 1." }
    @{ T='WI 12713 / T2 — Resolve param file values from pre-flight';            E=0.08; D="Substitute subscriptionId, ownerEmail, logAnalyticsWorkspaceId in 00-subscription-policies.bicepparam. See $Plan — Task 2." }
    @{ T='WI 12713 / T3 — Pre-deploy what-if against mg-apex-m-lab';             E=0.03; D="Run az deployment mg create --what-if; capture to tools/_acceptance_evidence/wi-12713-whatif-pre.txt. See $Plan — Task 3." }
    @{ T='WI 12713 / T4 — Deploy 00-subscription-policies.bicep';                E=0.03; D="Run az deployment mg create against mg-apex-m-lab; capture deployment record. See $Plan — Task 4." }
    @{ T='WI 12713 / T5 — Acceptance verification (sub, MG, tags, diagnostics)'; E=0.17; D="Run 4 az verification commands; save JSON evidence. Satisfies DoD #1, #4, #9. See $Plan — Task 5." }
    @{ T='WI 12713 / T6 — Idempotency verification (post-deploy what-if)';       E=0.03; D="Re-run what-if; expect every resource = Unchanged. Satisfies DoD #8. See $Plan — Task 6." }
    @{ T='WI 12713 / T7 — Author runbook (as-built record)';                     E=0.25; D="Fill apex-m-gssc-lab/runbooks/wi-12713-subscription-mg-placement.md with actual values. Satisfies DoD #6. See $Plan — Task 7." }
    @{ T='WI 12713 / T8 — Stage and commit on main';                             E=0.08; D="Three logical commits: param resolution, evidence + runbook, plan. All include AB#12713. See $Plan — Task 8." }
    @{ T='WI 12713 / T9 — Push to origin and open PR (if branch-protected)';     E=0.08; D="git push origin main, or fall back to feature branch + PR if protection blocks. See $Plan — Task 9." }
    @{ T='WI 12713 / T10 — GSSC Lab Platform Eng lead review + Closed';          E=0.25; D="Add reviewer, move WI to In Review, await approval, merge, move to Closed. Satisfies DoD #11. See $Plan — Task 10." }
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

function Write-Section {
    param([string]$Label)
    Write-Host ""
    Write-Host "==> $Label" -ForegroundColor Cyan
}

function Write-Ok    { param([string]$Msg) Write-Host "    [OK]  $Msg" -ForegroundColor Green }
function Write-Fail  { param([string]$Msg) Write-Host "    [!!]  $Msg" -ForegroundColor Red }
function Write-Info  { param([string]$Msg) Write-Host "    $Msg" }

function Exit-WithCode {
    param([int]$Code, [string]$Reason)
    Write-Host ""
    Write-Fail $Reason
    exit $Code
}

# ---------------------------------------------------------------------------
# 1. Environment check
# ---------------------------------------------------------------------------

if (-not $OnlyTasks) {
    Write-Section 'Environment check'

    if (-not (Test-Path $Az)) {
        Exit-WithCode 1 "Azure CLI not found at $Az. Install from https://learn.microsoft.com/en-us/cli/azure/install-azure-cli"
    }
    $azVer = (& $Az version --query '\"azure-cli\"' -o tsv) 2>$null
    Write-Ok "Azure CLI $azVer"

    $bicepVer = (& $Az bicep version 2>$null)
    if (-not $bicepVer) {
        Exit-WithCode 1 "Bicep CLI not installed. Run: $Az bicep install"
    }
    Write-Ok "$bicepVer"
    if ($bicepVer -notmatch '0\.43\.|0\.4[4-9]\.|0\.[5-9]\d\.|[1-9]\.\d') {
        Write-Info "Note: latest Bicep release at time of plan was 0.43.8 (2026-05-07)."
    }

    $extInstalled = (& $Az extension list --query "[?name=='azure-devops'].version" -o tsv) 2>$null
    if (-not $extInstalled) {
        Exit-WithCode 1 "azure-devops extension not installed. Run: $Az extension add --name azure-devops"
    }
    Write-Ok "azure-devops extension $extInstalled"

    # ---------------------------------------------------------------------------
    # 2. Auth check
    # ---------------------------------------------------------------------------
    Write-Section 'Auth check'

    $acct = (& $Az account show --query 'user.name' -o tsv) 2>$null
    if (-not $acct) {
        Write-Fail "az not logged in. Run:"
        Write-Info "  $Az login"
        Exit-WithCode 2 "Azure CLI not authenticated."
    }
    Write-Ok "az logged in as $acct"

    # Set the ADO defaults so subsequent boards commands don't need --org/--project
    & $Az devops configure --defaults organization=$Org project="$Project" | Out-Null

    $wi = (& $Az boards work-item show --id $ParentId --query 'fields.\"System.Title\"' -o tsv) 2>&1
    if ($LASTEXITCODE -ne 0 -or $wi -match 'ERROR') {
        Write-Fail "az devops not authenticated. Generate a PAT with Work Items: Read & Write, then run:"
        Write-Info "  $Az devops login --organization $Org"
        Exit-WithCode 2 "Azure DevOps not authenticated."
    }
    Write-Ok "WI ${ParentId}: $wi"
}

# ---------------------------------------------------------------------------
# 3. Bicep build + lint
# ---------------------------------------------------------------------------

if (-not $OnlyTasks) {
    Write-Section 'Bicep build + lint'

    foreach ($f in $BicepFiles) {
        $abs = Join-Path $RepoRoot $f
        if (-not (Test-Path $abs)) {
            Exit-WithCode 3 "Missing Bicep file: $abs"
        }

        & $Az bicep build --file $abs 2>&1 | ForEach-Object {
            if ($_ -match 'Error|ERROR') { Exit-WithCode 3 "Build error in $f`: $_" }
        }
        if ($LASTEXITCODE -ne 0) { Exit-WithCode 3 "az bicep build exit $LASTEXITCODE on $f" }

        & $Az bicep lint --file $abs 2>&1 | ForEach-Object {
            if ($_ -match 'Error|ERROR') { Exit-WithCode 3 "Lint error in $f`: $_" }
        }
        if ($LASTEXITCODE -ne 0) { Exit-WithCode 3 "az bicep lint exit $LASTEXITCODE on $f" }

        Write-Ok "$f (build + lint clean)"
    }
}

# ---------------------------------------------------------------------------
# 4. ADO child-Task creation (idempotent)
# ---------------------------------------------------------------------------

if (-not $SkipTasks) {
    Write-Section "ADO child Tasks under WI $ParentId (idempotent)"

    # Pull existing child titles to avoid duplicates on re-run.
    $relations = (& $Az boards work-item show --id $ParentId --query 'relations[?attributes.name==`Child`].url' -o tsv) 2>&1
    if ($LASTEXITCODE -ne 0) {
        Exit-WithCode 4 "Could not read child relations of WI $ParentId."
    }

    $existingTitles = @()
    foreach ($url in ($relations -split "`r?`n" | Where-Object { $_ })) {
        $childId = [int]($url -split '/')[-1]
        $title = (& $Az boards work-item show --id $childId --query 'fields.\"System.Title\"' -o tsv) 2>$null
        if ($title) { $existingTitles += $title }
    }

    if ($existingTitles.Count -gt 0) {
        Write-Info "Existing children: $($existingTitles.Count) — will skip create for matches."
    }

    $created = 0; $skipped = 0
    foreach ($t in $Tasks) {
        if ($existingTitles -contains $t.T) {
            Write-Ok "skip (exists): $($t.T)"
            $skipped++
            continue
        }

        $fields = @(
            "Microsoft.VSTS.Scheduling.OriginalEstimate=$($t.E)",
            "Microsoft.VSTS.Scheduling.RemainingWork=$($t.E)",
            "System.Tags=$Tags"
        )

        $createArgs = @(
            'boards', 'work-item', 'create',
            '--type', 'Task',
            '--title', $t.T,
            '--description', $t.D,
            '--fields'
        ) + $fields + @('--query', 'id', '-o', 'tsv')

        $newId = (& $Az @createArgs) 2>&1
        if ($LASTEXITCODE -ne 0 -or $newId -match 'ERROR') {
            Exit-WithCode 4 "Failed to create Task '$($t.T)': $newId"
        }

        & $Az boards work-item relation add `
            --id $newId `
            --relation-type Parent `
            --target-id $ParentId `
            --output none 2>&1 | Out-Null
        if ($LASTEXITCODE -ne 0) {
            Exit-WithCode 4 "Failed to link Task $newId to parent $ParentId"
        }

        Write-Ok "created Task $newId  ->  parent $ParentId  ·  $($t.T)"
        $created++
    }

    Write-Host ""
    Write-Info "Tasks created: $created  ·  skipped (already existed): $skipped"
    Write-Info "View parent: $Org$Project/_workitems/edit/$ParentId"
}

Write-Section 'Done'
Write-Ok "All requested actions completed successfully."
exit 0
