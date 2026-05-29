#!/usr/bin/env bash
# =====================================================================
# APEX-M · Local mock quickstart (bash)
# =====================================================================
# Boots one APEX-M agent against in-process mock Microsoft SDKs.
# No Docker required. No Azure subscription required.
# Independence-clean by construction.
# =====================================================================
set -euo pipefail

# --- Resolve repo root (script lives in docs/guides/APEX-M-Local-Setup) ---
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$( cd "${SCRIPT_DIR}/../../.." && pwd )"
cd "${REPO_ROOT}"

echo "==> APEX repo root: ${REPO_ROOT}"

# --- Python version gate ---
if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)"; then
    echo "ERROR: Python >= 3.12 required (apex-m/pyproject.toml gate)" >&2
    python3 --version >&2
    exit 1
fi

# --- Install via uv if available, else pip fallback ---
if command -v uv >/dev/null 2>&1; then
    echo "==> Installing with uv (canonical)"
    uv sync --extra runtime --extra dev
    PYTHON="uv run python"
else
    echo "==> uv not found; falling back to pip"
    if [[ ! -d ".venv" ]]; then
        python3 -m venv .venv
    fi
    # shellcheck disable=SC1091
    source .venv/bin/activate
    pip install --quiet -e packages/apex-core
    pip install --quiet -e "apex-m[runtime,dev]"
    PYTHON="python"
fi

# --- Stage .env if missing ---
if [[ ! -f "apex-m/.env" ]]; then
    echo "==> Staging apex-m/.env from package template"
    cp "${SCRIPT_DIR}/.env.example" "apex-m/.env"
fi

# --- Export the substrate envelope ---
export APEX_SUBSTRATE=laptop
export APEX_VARIANT=APEX-M
export APEX_FORCE_MOCK=true
export APEX_LOG_LEVEL=DEBUG
export APEX_TRACE_TO_STDOUT=true

# --- Run the mock agent ---
SERVICE_CODE="${1:-RC-E2E-03}"
SCENARIO="${2:-cold-chain-pricing}"

echo "==> Running agent: service=${SERVICE_CODE} scenario=${SCENARIO}"
cd apex-m
${PYTHON} -m apex_m.cli run-agent \
    --service-code "${SERVICE_CODE}" \
    --scenario "${SCENARIO}"
