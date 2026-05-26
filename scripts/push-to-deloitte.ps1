<#
.SYNOPSIS
  Commit pending changes and push APEX to Deloitte-US-Consulting/APEX (EMU org).

.DESCRIPTION
  Idempotent helper that:
    1. Verifies the EMU GitHub account is authenticated and the target repo exists.
    2. Adds or replaces the Deloitte remote.
    3. Stages and commits pending changes per the chosen scope.
    4. Pushes the current branch (defaults to main) with all history.

  Run AFTER you have:
    - Authenticated `gh` as `kmarkham_deloitte` (`gh auth login`, then `gh auth switch`).
    - Created the empty `APEX` repo inside the `Deloitte-US-Consulting` org.

.PARAMETER CommitScope
  all      : Stage every pending change (HTML + final MP3s + _tmp/ + _originals/ deletions).
  minimal  : Stage only the HTML and the 13 final episode MP3s under docs/podcast/pc-cfmp/audio/.
  none     : Skip the commit step entirely (push existing history only).

.PARAMETER RemoteMode
  add      : Add Deloitte as remote `deloitte`, keep existing `origin` untouched (default, recommended).
  replace  : Point `origin` at the Deloitte repo (drops the personal URL from local config).

.PARAMETER RemoteName
  Name to use for the Deloitte remote when RemoteMode = add. Default: deloitte.

.PARAMETER CommitMessage
  Commit message to use when CommitScope is `all` or `minimal`. Default is a generic CFMP podcast message.

.PARAMETER Branch
  Branch to push. Default: main.

.PARAMETER DryRun
  Print every action without executing it.

.EXAMPLE
  ./scripts/push-to-deloitte.ps1
  # Adds `deloitte` remote, commits everything, pushes main.

.EXAMPLE
  ./scripts/push-to-deloitte.ps1 -CommitScope minimal -DryRun
  # Show what a minimal commit + push would do, without making changes.
#>

[CmdletBinding()]
param(
    [ValidateSet('all', 'minimal', 'none')]
    [string]$CommitScope = 'all',

    [ValidateSet('add', 'replace')]
    [string]$RemoteMode = 'add',

    [string]$RemoteName = 'deloitte',

    [string]$CommitMessage = 'chore: sync APEX working tree to Deloitte-US-Consulting/APEX',

    [string]$Branch = 'main',

    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$DeloitteOrg  = 'Deloitte-US-Consulting'
$DeloitteRepo = 'APEX'
$ExpectedUser = 'kmarkham_deloitte'
$DeloitteUrl  = "https://github.com/$DeloitteOrg/$DeloitteRepo.git"

function Write-Step([string]$msg) {
    Write-Host ""
    Write-Host "==> $msg" -ForegroundColor Cyan
}

function Invoke-Step([string]$label, [scriptblock]$action) {
    Write-Host "  - $label" -ForegroundColor DarkGray
    if ($DryRun) {
        Write-Host "    (dry-run, skipped)" -ForegroundColor Yellow
        return
    }
    & $action
    if ($LASTEXITCODE -and $LASTEXITCODE -ne 0) {
        throw "Step failed (exit $LASTEXITCODE): $label"
    }
}

# --- 1. Preflight: repo, auth, target ---------------------------------------

Write-Step "Preflight checks"

if (-not (Test-Path .git)) {
    throw "Not a git repository: run this from the APEX repo root."
}

$currentBranch = (git rev-parse --abbrev-ref HEAD).Trim()
Write-Host "  current branch: $currentBranch" -ForegroundColor DarkGray
if ($currentBranch -ne $Branch) {
    Write-Warning "Current branch is '$currentBranch' but -Branch is '$Branch'. Will push '$Branch'."
}

$ghStatus = gh auth status 2>&1 | Out-String
if ($ghStatus -notmatch [regex]::Escape($ExpectedUser)) {
    Write-Warning "gh CLI does not show '$ExpectedUser' as an authenticated account."
    Write-Host $ghStatus
    throw "Run: gh auth login   (sign in as $ExpectedUser), then: gh auth switch --user $ExpectedUser"
}

if ($ghStatus -match 'Active account: true' -and $ghStatus -notmatch "(?ms)account $ExpectedUser.*?Active account: true") {
    Write-Host "  switching active gh account to $ExpectedUser" -ForegroundColor DarkGray
    if (-not $DryRun) {
        gh auth switch --user $ExpectedUser | Out-Null
    }
}

# Verify the target repo exists.
$repoCheck = gh repo view "$DeloitteOrg/$DeloitteRepo" --json name,visibility 2>&1
if ($LASTEXITCODE -ne 0) {
    throw "Target repo $DeloitteOrg/$DeloitteRepo not visible to $ExpectedUser. Create it in the GitHub UI (empty, no README), then re-run.`n$repoCheck"
}
Write-Host "  repo OK: $DeloitteOrg/$DeloitteRepo" -ForegroundColor DarkGray

# --- 2. Configure remote ----------------------------------------------------

Write-Step "Configure remote ($RemoteMode -> $DeloitteUrl)"

$existingRemotes = (git remote) -split "`n" | Where-Object { $_ }

switch ($RemoteMode) {
    'add' {
        if ($existingRemotes -contains $RemoteName) {
            Invoke-Step "update existing '$RemoteName' URL" {
                git remote set-url $RemoteName $DeloitteUrl
            }
        } else {
            Invoke-Step "add remote '$RemoteName'" {
                git remote add $RemoteName $DeloitteUrl
            }
        }
        $pushRemote = $RemoteName
    }
    'replace' {
        if ($existingRemotes -contains 'origin') {
            Invoke-Step "update origin URL to Deloitte repo" {
                git remote set-url origin $DeloitteUrl
            }
        } else {
            Invoke-Step "add origin -> Deloitte repo" {
                git remote add origin $DeloitteUrl
            }
        }
        $pushRemote = 'origin'
    }
}

# --- 3. Stage + commit ------------------------------------------------------

Write-Step "Commit pending changes (scope: $CommitScope)"

switch ($CommitScope) {
    'none' {
        Write-Host "  skipping commit step." -ForegroundColor DarkGray
    }
    'minimal' {
        $minimalPaths = @(
            'docs/podcast/pc-cfmp/CFMP-Capabilities-Map.html'
        )
        $finalEpisodes = Get-ChildItem -Path 'docs/podcast/pc-cfmp/audio' -Filter '*.mp3' -File -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -match '^\d{2}-' } |
            Select-Object -ExpandProperty FullName
        $minimalPaths += $finalEpisodes

        foreach ($p in $minimalPaths) {
            if (Test-Path $p) {
                Invoke-Step "git add $p" { git add -- "$p" }
            }
        }

        $staged = git diff --cached --name-only
        if (-not $staged) {
            Write-Host "  no minimal-scope changes staged; skipping commit." -ForegroundColor Yellow
        } else {
            Invoke-Step "git commit" { git commit -m $CommitMessage }
        }
    }
    'all' {
        Invoke-Step "git add -A" { git add -A }

        $staged = git diff --cached --name-only
        if (-not $staged) {
            Write-Host "  nothing to commit." -ForegroundColor Yellow
        } else {
            Invoke-Step "git commit (all)" { git commit -m $CommitMessage }
        }
    }
}

# --- 4. Push ----------------------------------------------------------------

Write-Step "Push '$Branch' to '$pushRemote' ($DeloitteUrl)"

Invoke-Step "git push -u $pushRemote $Branch" {
    git push -u $pushRemote $Branch
}

Write-Step "Done"
Write-Host "  Pushed $Branch to $DeloitteOrg/$DeloitteRepo." -ForegroundColor Green
Write-Host "  https://github.com/$DeloitteOrg/$DeloitteRepo/tree/$Branch" -ForegroundColor Green
