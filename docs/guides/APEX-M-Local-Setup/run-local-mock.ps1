# =====================================================================
# APEX-M . Local mock quickstart (PowerShell)
# =====================================================================
# Boots one APEX-M agent against in-process mock Microsoft SDKs.
# No Docker required. No Azure subscription required.
# Independence-clean by construction.
# =====================================================================

$ErrorActionPreference = 'Stop'

# --- Resolve repo root (script lives in docs/guides/APEX-M-Local-Setup) ---
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RepoRoot  = Resolve-Path (Join-Path $ScriptDir '..\..\..')
Set-Location $RepoRoot

Write-Host "==> APEX repo root: $RepoRoot"

# --- Python version gate ---
$pyOk = $false
try {
    $pyVersion = (python -c "import sys; print('{}.{}'.format(sys.version_info[0], sys.version_info[1]))") 2>$null
    $major, $minor = $pyVersion.Split('.')
    if ([int]$major -gt 3 -or ([int]$major -eq 3 -and [int]$minor -ge 12)) { $pyOk = $true }
} catch { }
if (-not $pyOk) {
    Write-Error "Python >= 3.12 required (apex-m/pyproject.toml gate). Found: $pyVersion"
    exit 1
}

# --- Install via uv if available, else pip fallback ---
$uvAvailable = $null -ne (Get-Command uv -ErrorAction SilentlyContinue)
if ($uvAvailable) {
    Write-Host "==> Installing with uv (canonical)"
    uv sync --extra runtime --extra dev
    $Python = 'uv run python'
} else {
    Write-Host "==> uv not found; falling back to pip"
    if (-not (Test-Path '.venv')) {
        python -m venv .venv
    }
    & '.venv\Scripts\Activate.ps1'
    pip install --quiet -e packages/apex-core
    pip install --quiet -e "apex-m[runtime,dev]"
    $Python = 'python'
}

# --- Stage .env if missing ---
if (-not (Test-Path 'apex-m\.env')) {
    Write-Host "==> Staging apex-m\.env from package template"
    Copy-Item -Path (Join-Path $ScriptDir '.env.example') -Destination 'apex-m\.env'
}

# --- Export the substrate envelope ---
$env:APEX_SUBSTRATE      = 'laptop'
$env:APEX_VARIANT        = 'APEX-M'
$env:APEX_FORCE_MOCK     = 'true'
$env:APEX_LOG_LEVEL      = 'DEBUG'
$env:APEX_TRACE_TO_STDOUT= 'true'

# --- Run the mock agent ---
$ServiceCode = if ($args.Count -ge 1) { $args[0] } else { 'RC-E2E-03' }
$Scenario    = if ($args.Count -ge 2) { $args[1] } else { 'cold-chain-pricing' }

Write-Host "==> Running agent: service=$ServiceCode scenario=$Scenario"
Set-Location 'apex-m'
Invoke-Expression "$Python -m apex_m.cli run-agent --service-code $ServiceCode --scenario $Scenario"
