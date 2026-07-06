# APEX-M on Azure — Implementation Guide for Claude

**Audience:** A Claude session starting fresh on an APEX-M on Azure build. Read this in full before generating infrastructure or code. Every section here is **earned knowledge** — patterns that worked, anti-patterns that wasted hours, and copy-paste templates that ship.

**Reference implementation:** https://github.com/Deloitte-US-Consulting/sap-agentic — every pattern in this doc is live and verifiable there.

**Last updated:** 2026-06-02 (after Sonepar S1.0 → S3.1 shipped).

---

## 1. What APEX-M is (one paragraph)

**APEX-M** = Agentic Platform for Enterprise eXecution, **Microsoft variant**. Deloitte's accelerator for shipping agentic solutions on the Microsoft stack (Azure Container Apps + Azure OpenAI + Microsoft Agent Framework + M365 Copilot). Component model: **Personas** (agent prompts + roles), **Adapters** (source/system bindings), **Featurizers** (transform raw → agent-shaped features), **Virtual Views** (business-ready PG views for MCP consumption), **Constitution** (HITL gates + safety rules in YAML), **Scenarios** (end-to-end stories tying it all together), **Substrates** (laptop / dev / stage / prod environments with 15 standard pack-service-groups). Sibling variants: **APEX-A** (Anthropic), **APEX-G** (Google), **APEX-RC** (Reference Core).

---

## 2. The reference architecture (5 tiers)

```
┌───────────────────────────────────────────────────────────────┐
│ UX           React Portal (HITL desktop) + M365 Copilot       │
├───────────────────────────────────────────────────────────────┤
│ ORCHESTRATION  Microsoft Agent Framework (MAF)                │
│                Azure OpenAI · Constitution YAML · audit chain │
├───────────────────────────────────────────────────────────────┤
│ MCP SERVERS    One per domain (FastMCP 2.x streamable-http)   │
├───────────────────────────────────────────────────────────────┤
│ MEDALLION      Gold Virtual Views ← Silver typed ← Bronze raw │
│                (PG, no Fabric)                                │
├───────────────────────────────────────────────────────────────┤
│ SOURCE         Real API / SAP / DB / simulated source service │
└───────────────────────────────────────────────────────────────┘

Cross-cutting:
- Identity:  Entra External ID + 4-identity audit chain
                (actor/on_behalf_of/agent/system/chain_id)
- Secrets:   Key Vault (no .env files)
- Hosting:   Container Apps (single multi-role image, see §4)
- Bronze:    Container Apps Job (batch, run-to-completion)
```

---

## 3. Azure infrastructure pattern

Default to **maximum reuse** of existing infra. Don't provision a new resource group unless explicitly required.

| Resource | Pattern | Notes |
|---|---|---|
| Subscription | Reuse client's existing | Confirm with `az account show` |
| Resource group | Reuse | One per practice, not per project |
| ACR | Reuse, admin-enabled | Until Owner / UAA can grant MI AcrPull (see §10) |
| Container Apps env | Reuse | All apps + jobs in same CAE for internal DNS |
| Postgres flex | Reuse, **new schemas per project** | E.g. `myproject_bronze`, `myproject_silver`, `myproject_gold`, `myproject` |
| Key Vault | **One per project** | Don't share — KVs are cheap and access boundaries matter |
| Blob storage | Per project | Bronze archive, file uploads, etc. |

**Naming convention** (matches sap-agentic reference):
- Container App: `ca-<project>-<role>` (e.g. `ca-sonepar-sap-sim`, `ca-sonepar-mcp-ocom`)
- Container Apps Job: `ca-<project>-<job>` (e.g. `ca-sonepar-bronze-loader`)
- Key Vault: `kv-<project>` (e.g. `kv-sap-agentic`)
- Image: `ca-<project>-<base-role>:vN.M` (e.g. `ca-sonepar-sap-sim:v0.5`) — the BASE role names the image even though it hosts multiple roles

---

## 4. The multi-role image pattern (CRITICAL)

**The problem:** Azure CLI's `az containerapp create --args` won't accept tokens starting with `-` as values (treats them as flags). So `--command "python" --args "-m" "myapp.loaders.bronze"` fails to parse — `-m` gets dropped.

**The solution:** Embed the dispatcher in the image. One Dockerfile, one ACR repo, one build pipeline, infinite roles selectable via `RUN_MODE` env var.

### Template: `src/<package>/entrypoint.sh`

```sh
#!/bin/sh
# Multi-role dispatcher. Add a case per long-running role.
set -e

case "${RUN_MODE:-server}" in
    server)
        # ca-<project>-<base> Container App runs this
        exec python -m mypackage.app
        ;;
    bronze_loader)
        # ca-<project>-bronze-loader Container Apps Job runs this
        exec python -m mypackage.loaders.bronze_loader
        ;;
    mcp_domainX)
        # ca-<project>-mcp-domainX Container App runs this
        exec python -m mypackage.mcp_servers.domainX
        ;;
    *)
        echo "FATAL: unknown RUN_MODE='$RUN_MODE'" >&2
        exit 64
        ;;
esac
```

### Template: `src/<package>/<base>/Dockerfile`

```dockerfile
FROM python:3.11-slim AS base
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir -e .

# CRITICAL: entrypoint dispatcher lives here, not at build time
COPY src/mypackage/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV PYTHONUNBUFFERED=1
ENV PORT=8000
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD curl -fsS http://localhost:8000/health || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]
# No CMD -- entrypoint dispatches based on RUN_MODE
```

**Adding a new role** = (1) new case in `entrypoint.sh`, (2) new Container App / Job with `RUN_MODE=<new>` env var. Same image. Zero CLI workarounds.

---

## 5. PowerShell deploy script conventions

The user runs scripts in **Windows PowerShell 5.1** (not 7+). Several gotchas:

### Numbering & naming

```
infra/scripts/
├── 01-create-pg-schemas.ps1          # Phase 1 setup
├── 02-create-keyvault.ps1
├── 03-build-and-push-<image>.ps1     # ACR cloud build (no local Docker)
├── 04-create-<role>-container-app.ps1
├── 05-create-bronze-tables.ps1
├── 06-create-bronze-loader-job.ps1
├── 07-trigger-bronze-loader.ps1
├── 08-create-silver-gold-views.ps1
├── 09-create-mcp-<domain>-container-app.ps1
├── _verify-s1-2.ps1                  # Verify phase outputs
├── _verify-s2.ps1
├── _verify-s2-3.ps1
├── _verify-s3-1.ps1
└── _fix-encoding.ps1                 # Em-dash sweep (see §6)
```

### Existence-check pattern (anti-pattern + fix)

```powershell
# DO NOT do this -- 'show' errors loudly on miss + trips $ErrorActionPreference=Stop
$exists = az containerapp show -n $name -g $rg 2>$null
# script dies before falling through to create branch

# DO this -- 'list' returns empty without erroring
$exists = az containerapp list -g $rg --query "[?name=='$name'].name | [0]" -o tsv
if ($exists) { ... } else { ... }
```

Apply same pattern to `az keyvault show` / `az acr show` / `az containerapp env show` / `az role assignment list` etc.

### Git commit messages — use `-F file`, never here-strings

```powershell
# DO NOT -- PowerShell here-string + native command arg splitting mangles flags inside the body
git commit -m @'
fix: blah blah
- replace `az containerapp show` with `--query` ...
'@
# git parses --query from inside the body as a flag and errors

# DO -- write to a temp file, use -F, delete after
$msg | Set-Content .commit-msg.tmp
git commit -F .commit-msg.tmp
Remove-Item .commit-msg.tmp
```

Add `.commit-msg.tmp` to `.gitignore` — it's a recurring scratch file.

### Pulling DB creds without typing the password

```powershell
$pgUrl = az keyvault secret show --vault-name <kv> --name <secret> --query value -o tsv
Add-Type -AssemblyName System.Web
$uri = [System.Uri]$pgUrl
$ui  = $uri.UserInfo -split ':'
$env:PG_HOST     = $uri.Host
$env:PG_DB       = $uri.AbsolutePath.TrimStart('/')
$env:PG_USER     = [System.Web.HttpUtility]::UrlDecode($ui[0])
$env:PG_PASSWORD = [System.Web.HttpUtility]::UrlDecode($ui[1])
# UrlDecode is REQUIRED -- KV-stored URLs typically URL-encode special chars like ! -> %21
```

### Read-only verify scripts

```powershell
# Verify scripts are checks, not enforcement -- DO NOT fail-fast on missing items
$ErrorActionPreference = 'Continue'   # NOT 'Stop'
$failures = 0
# ... checks set $failures++
if ($failures -gt 0) { exit 1 } else { Write-Host "[done] verified" }
```

---

## 6. The em-dash trap (PowerShell 5.1 + UTF-8 without BOM)

**The bug:** PS 5.1 reads `.ps1` files as Windows-1252 by default. UTF-8 em-dashes (U+2014, 3 bytes `E2 80 94`) get decoded as 3 separate Windows-1252 chars — the third of which is a stray `"` that corrupts string parsing **even inside comments**.

**Symptom:** `Missing closing '}' in statement block` or `Unexpected token 'X'` errors pointing at innocent-looking comment lines.

**The fix:** Always save `.ps1` files with **UTF-8 + BOM**. Claude's `Write` tool typically saves without BOM, so:

1. **Avoid em-dashes** in any `.ps1` file you author. Use `--` (double-hyphen) instead. ASCII-only is the safest default for scripts.

2. **Sweep + re-save** with this helper any time errors look encoding-related:

```powershell
# infra/scripts/_fix-encoding.ps1
Get-ChildItem "$PSScriptRoot\*.ps1" | ForEach-Object {
    $path = $_.FullName
    $content = [System.IO.File]::ReadAllText($path)
    $fixed = $content -replace [char]0x2014, '--'
    if ($content -ne $fixed) {
        $utf8Bom = New-Object System.Text.UTF8Encoding($true)
        [System.IO.File]::WriteAllText($path, $fixed, $utf8Bom)
        Write-Host "[fixed] $($_.Name)" -ForegroundColor Green
    }
}
```

---

## 7. The Medallion pattern (without Microsoft Fabric)

Three PG schemas per project. Cheap, fast, no Fabric dependency.

### Bronze — append-only raw

```sql
CREATE TABLE myproject_bronze.<entity> (
  _row_id        bigserial PRIMARY KEY,
  _ingest_run_id uuid        NOT NULL,
  _ingested_at   timestamptz NOT NULL DEFAULT now(),
  _source_url    text        NOT NULL,
  business_key   text        NOT NULL,   -- natural key extracted for fast lookup
  payload        jsonb       NOT NULL    -- raw response, no transformation
);
CREATE INDEX ix_bronze_<entity>_ingest_run   ON myproject_bronze.<entity> (_ingest_run_id);
CREATE INDEX ix_bronze_<entity>_business_key ON myproject_bronze.<entity> (business_key);
CREATE INDEX ix_bronze_<entity>_ingested_at  ON myproject_bronze.<entity> (_ingested_at DESC);
```

Plus an `ingest_runs` metadata table:

```sql
CREATE TABLE myproject_bronze.ingest_runs (
  ingest_run_id  uuid PRIMARY KEY,
  loader_name    text NOT NULL,
  source_url     text NOT NULL,
  started_at     timestamptz NOT NULL DEFAULT now(),
  finished_at    timestamptz,
  status         text NOT NULL DEFAULT 'running',  -- running | success | failed
  row_counts     jsonb,
  error_message  text
);
```

Re-running the loader inserts another full set tagged with a new `_ingest_run_id`. Silver dedups.

### Silver — typed latest-state per entity

```sql
CREATE OR REPLACE VIEW myproject_silver.<entity> AS
SELECT DISTINCT ON (business_key)
    business_key                          AS <entity>_id,
    payload->>'<JsonField>'               AS typed_field,
    (payload->>'<NumericField>')::numeric AS amount,
    (payload->>'<DateField>')::timestamptz AS event_date,
    _ingest_run_id                        AS _source_run,
    _ingested_at                          AS _source_ingested_at
FROM myproject_bronze.<entity>
ORDER BY business_key, _ingested_at DESC;
```

`DISTINCT ON + ORDER BY business_key, _ingested_at DESC` is the **idiomatic** way to grab the latest row per natural key from append-only Bronze.

For nested arrays (e.g. `payload->'to_Item'`):

```sql
CREATE OR REPLACE VIEW myproject_silver.<entity>_items AS
WITH latest AS (
    SELECT DISTINCT ON (business_key) business_key, payload
    FROM myproject_bronze.<entity>
    ORDER BY business_key, _ingested_at DESC
)
SELECT
    latest.business_key                   AS <entity>_id,
    item->>'<ChildKey>'                   AS line_item,
    -- ... typed fields from `item`
FROM latest, jsonb_array_elements(latest.payload->'<arrayKey>') AS item;
```

### Gold — business-ready Virtual Views

One VV per scenario / agent-callable surface. Keep them **denormalized** (joins, computed fields, status labels) so the MCP server's tool is a trivial `SELECT * FROM vv WHERE ... LIMIT $1`.

```sql
CREATE OR REPLACE VIEW myproject_gold.vv_<business_concept> AS
SELECT
    s.<entity>_id,
    s.business_field,
    j.joined_field,
    CASE s.status WHEN 'A' THEN 'Open' WHEN 'C' THEN 'Closed' END AS status_label,
    EXTRACT(DAY FROM (now() - s.event_date))::int AS days_open,
    (computed_amount_a - computed_amount_b) AS variance,
    -- ... all the fields the agent / MCP tool will surface
FROM myproject_silver.<entity> s
LEFT JOIN myproject_silver.<related> j ON j.fk = s.<entity>_id
WHERE s.status = '<filter>'
ORDER BY s.event_date DESC;
```

**Tiny datasets** (< 100K rows): plain VIEWs are fine, query time is sub-millisecond.
**Big datasets**: promote to MATERIALIZED VIEW with `REFRESH MATERIALIZED VIEW CONCURRENTLY` on a schedule.

### Bronze loader (async Python, asyncpg COPY fast path)

```python
import asyncio, json, os
from uuid import uuid4
import aiohttp, asyncpg

async def run(source_base, dsn):
    ingest_run_id = uuid4()
    pg = await asyncpg.connect(dsn=dsn)
    try:
        await pg.execute("INSERT INTO myproject_bronze.ingest_runs (ingest_run_id, ...) ...",
                         ingest_run_id, ...)

        async with aiohttp.ClientSession() as session:
            for entity_map in CATALOG:
                rows = await fetch_with_pagination(session, source_base, entity_map)
                records = [(ingest_run_id, source_url, str(r[key_field]), json.dumps(r)) for r in rows]
                # COPY is 10-100x faster than INSERT...VALUES at scale
                await pg.copy_records_to_table(
                    entity_map.bronze_table,
                    records=records,
                    columns=["_ingest_run_id", "_source_url", "business_key", "payload"],
                    schema_name="myproject_bronze",
                )

        await pg.execute("UPDATE myproject_bronze.ingest_runs SET status='success', ... WHERE ingest_run_id=$1",
                         ingest_run_id)
    finally:
        await pg.close()

if __name__ == "__main__":
    asyncio.run(run(os.environ["SOURCE_URL"], os.environ["POSTGRES_URL"]))
```

Deploy as a **Container Apps Job** (not a long-running App). Manual trigger via `az containerapp job start -n <job> -g <rg>`.

---

## 8. The MCP server pattern (FastMCP 2.x + Starlette)

**Required:** `fastmcp>=2.0` (pre-2.0 doesn't have `http_app()` ASGI accessor).

### Pyproject deps

```toml
"fastmcp>=2.0",
"mcp>=1.0",
"uvicorn>=0.30",
"starlette>=0.37",
"asyncpg>=0.29",
```

### Tool implementation pattern

```python
from fastmcp import FastMCP
from mypackage.mcp_servers.db import get_pool, rows_to_list

mcp = FastMCP(
    name="myproject-domainX",
    instructions="One paragraph describing what this server does and when to call it.",
)

@mcp.tool()
async def list_things(top: int = 10, filter_id: str | None = None) -> list[dict]:
    """One-line summary the LLM reads.

    Args:
        top: max rows (default 10, cap at 200)
        filter_id: optional filter

    Returns rows from myproject_gold.vv_things with all denormalized fields.
    """
    top = max(1, min(top, 200))
    pool = await get_pool()
    async with pool.acquire() as conn:
        if filter_id:
            rows = await conn.fetch("SELECT * FROM myproject_gold.vv_things WHERE id=$1 LIMIT $2", filter_id, top)
        else:
            rows = await conn.fetch("SELECT * FROM myproject_gold.vv_things ORDER BY date DESC LIMIT $1", top)
    return rows_to_list(rows)
```

### Shared DB module (`mcp_servers/db.py`)

```python
import os
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID
import asyncpg

_pool = None

async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(dsn=os.environ["POSTGRES_URL"], min_size=1, max_size=5)
    return _pool

def serialize(v):
    """Convert PG-native types -- Decimal->str (preserve $$$ precision), datetime->ISO, UUID->str."""
    if isinstance(v, Decimal):           return str(v)
    if isinstance(v, (datetime, date)):  return v.isoformat()
    if isinstance(v, UUID):              return str(v)
    if isinstance(v, dict):              return {k: serialize(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):     return [serialize(x) for x in v]
    return v

def row_to_dict(row):  return {k: serialize(v) for k, v in dict(row).items()}
def rows_to_list(rs):  return [row_to_dict(r) for r in rs]
```

### Server wrapper (CRITICAL — lifespan forwarding)

```python
def build_app():
    """Starlette wrapper: mounts fastmcp's ASGI app + adds /health route."""
    import fastmcp as _fm
    LOGGER.info("fastmcp version: %s", getattr(_fm, "__version__", "unknown"))

    from starlette.routing import Route, Mount
    from starlette.applications import Starlette

    # Defensive ASGI accessor: API name varies by fastmcp version
    mcp_app = None
    for method in ("streamable_http_app", "http_app", "sse_app"):
        if hasattr(mcp, method):
            mcp_app = getattr(mcp, method)()
            LOGGER.info("Using FastMCP.%s() for ASGI app", method)
            break
    if mcp_app is None:
        raise RuntimeError("FastMCP has no recognized ASGI app accessor")

    # *** THIS LINE IS CRITICAL ***
    # Without lifespan=mcp_app.lifespan, FastMCP's StreamableHTTPSessionManager
    # task group never initializes, and every /mcp POST returns 500
    # "Task group is not initialized". This is THE fastmcp-2.x gotcha.
    return Starlette(
        routes=[
            Route("/health", health, methods=["GET"]),
            Mount("/", app=mcp_app),
        ],
        lifespan=mcp_app.lifespan,
    )

def main():
    import uvicorn
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(build_app(), host="0.0.0.0", port=port, log_level="info")
```

### MCP client smoke test (PowerShell, paste-ready)

```powershell
$base = 'https://<fqdn>'

# 1. initialize -- captures Mcp-Session-Id header for subsequent calls
$init = @{ jsonrpc="2.0"; id=1; method="initialize"; params=@{
    protocolVersion="2024-11-05"; capabilities=@{};
    clientInfo=@{name="smoke"; version="1.0"}
}} | ConvertTo-Json -Depth 5
$resp = Invoke-WebRequest -Uri "$base/mcp" -Method POST -ContentType 'application/json' `
    -Headers @{ Accept='application/json, text/event-stream' } -Body $init -UseBasicParsing
$sessionId = $resp.Headers['Mcp-Session-Id']

# 2. tools/list -- enumerate registered tools with their JSON schemas
$list = @{ jsonrpc="2.0"; id=2; method="tools/list"; params=@{} } | ConvertTo-Json
Invoke-WebRequest -Uri "$base/mcp" -Method POST -ContentType 'application/json' `
    -Headers @{ Accept='application/json, text/event-stream'; 'Mcp-Session-Id'=$sessionId } `
    -Body $list -UseBasicParsing | Select-Object -ExpandProperty Content

# 3. tools/call -- invoke a tool
$call = @{ jsonrpc="2.0"; id=3; method="tools/call"; params=@{
    name="list_things"; arguments=@{ top=3 }
}} | ConvertTo-Json -Depth 6
Invoke-WebRequest -Uri "$base/mcp" -Method POST -ContentType 'application/json' `
    -Headers @{ Accept='application/json, text/event-stream'; 'Mcp-Session-Id'=$sessionId } `
    -Body $call -UseBasicParsing | Select-Object -ExpandProperty Content
```

---

## 9. Deploy script template (PowerShell)

The shape every deploy script in this repo follows. Copy-paste, swap names.

```powershell
# ========================================================
# NN-create-<role>-container-app.ps1 -- Phase X
# ========================================================
$ErrorActionPreference = 'Stop'

Write-Host "=== Phase X -- NN-create-<role>-container-app ===" -ForegroundColor Cyan

# Constants (env vars override defaults)
$SubId       = if ($env:SUB_ID) { $env:SUB_ID } else { '<sub-guid>' }
$ResourceGrp = if ($env:RG)     { $env:RG }     else { 'rg-iot-visionkit' }
$AcrName     = if ($env:ACR)    { $env:ACR }    else { 'acrvisionkit4459' }
$EnvName     = if ($env:CAE)    { $env:CAE }    else { 'cae-visionkit' }
$VaultName   = if ($env:KV)     { $env:KV }     else { 'kv-<project>' }
$Tag         = if ($env:TAG)    { $env:TAG }    else { 'v0.1' }
$AppName     = if ($env:APP)    { $env:APP }    else { 'ca-<project>-<role>' }
$AcrServer   = "$AcrName.azurecr.io"
$FullImage   = "$AcrServer/<base-image>:$Tag"

az account set --subscription $SubId
if ($LASTEXITCODE -ne 0) { Write-Error "az account set failed"; exit 1 }

# Existence check using 'list' (not 'show' -- see §5)
$envExists = az containerapp env list -g $ResourceGrp --query "[?name=='$EnvName'].name | [0]" -o tsv
if (-not $envExists) { Write-Error "CAE $EnvName not found"; exit 1 }

# Pull secrets from KV (NOT hardcoded)
$pgUrl = az keyvault secret show --vault-name $VaultName --name postgres-url --query value -o tsv

# ACR admin creds (until MI+AcrPull can be granted -- see §10)
$acrCreds = az acr credential show -n $AcrName -o json | ConvertFrom-Json
$AcrUser  = $acrCreds.username
$AcrPass  = $acrCreds.passwords[0].value

# Create OR update
$appExists = az containerapp list -g $ResourceGrp --query "[?name=='$AppName'].name | [0]" -o tsv
if ($appExists) {
    # Update path -- registry creds + secrets + image
    az containerapp registry set -n $AppName -g $ResourceGrp --server $AcrServer --username $AcrUser --password $AcrPass --output none
    az containerapp secret set -n $AppName -g $ResourceGrp --secrets "postgres-url=$pgUrl" --output none
    $revSuffix = "r" + [int][double]::Parse((Get-Date -UFormat %s))
    az containerapp update -n $AppName -g $ResourceGrp `
        --image $FullImage --revision-suffix $revSuffix `
        --cpu 0.5 --memory 1.0Gi --min-replicas 0 --max-replicas 1 `
        --set-env-vars "RUN_MODE=<role>" "PORT=8000" "POSTGRES_URL=secretref:postgres-url" `
        --output none
} else {
    az containerapp create -n $AppName -g $ResourceGrp --environment $EnvName `
        --image $FullImage `
        --target-port 8000 --ingress external `
        --min-replicas 0 --max-replicas 1 --cpu 0.5 --memory 1.0Gi `
        --system-assigned `
        --registry-server $AcrServer --registry-username $AcrUser --registry-password $AcrPass `
        --secrets "postgres-url=$pgUrl" `
        --env-vars "RUN_MODE=<role>" "PORT=8000" "POSTGRES_URL=secretref:postgres-url" `
        --output none
}

$fqdn = az containerapp show -n $AppName -g $ResourceGrp --query "properties.configuration.ingress.fqdn" -o tsv
Write-Host "[done] $AppName at https://$fqdn" -ForegroundColor Green
```

---

## 10. The MI vs admin-creds tradeoff (RBAC reality)

**Best practice:** Container App pulls from ACR via system-assigned MI + AcrPull role.

**Reality:** Granting `AcrPull` requires `Microsoft.Authorization/roleAssignments/write` on the ACR scope, which means **Owner** or **User Access Administrator**. **Contributor is NOT enough.**

**Pragmatic default:** Use **ACR admin user + password** (matches the existing CFMP pattern). Document that swapping to MI is a followup once someone with proper RBAC can grant the role.

```powershell
# Enable admin user on the ACR (one-time)
az acr update -n $AcrName --admin-enabled true

# Each container app + job uses:
--registry-server $AcrServer --registry-username $AcrUser --registry-password $AcrPass
```

System-assigned MI is **still worth enabling** even when not used for ACR — it's free, and you'll use it for Key Vault data-plane access in later phases.

---

## 11. Common gotchas (the hours-of-debugging list)

| Gotcha | Symptom | Fix |
|---|---|---|
| PS 5.1 reads UTF-8 without BOM as Win-1252 | mangled multibyte chars in errors; "Missing closing brace" in innocent comments | `_fix-encoding.ps1` sweep + ASCII-only in new files |
| `az ... show` errors on miss | Script dies before fall-through | Use `az ... list --query "[?name=='X']"` |
| `az containerapp --args` rejects `-m` | `unrecognized arguments: -m mymod` | Use `entrypoint.sh` dispatcher (see §4) |
| `az containerapp job logs show` is preview | WARNING on stderr trips ErrorActionPreference=Stop | Wrap in try/catch with local `$ErrorActionPreference = 'Continue'` |
| PG password URL-encoded in KV | Auth fails because `%21` is sent literally | `[System.Web.HttpUtility]::UrlDecode($pwd)` |
| Container Apps scale-to-zero cold start | First `/health` request times out 20-40s | Wait + retry; verify scripts should tolerate one cold-miss |
| FastMCP < 2.0 has no `http_app()` | `AttributeError: ... has no attribute 'streamable_http_app'` | `fastmcp>=2.0` in pyproject |
| FastMCP lifespan not forwarded | `500 Task group is not initialized` on every /mcp POST | `lifespan=mcp_app.lifespan` in `Starlette(...)` constructor |
| Empty package dir shadows `.py` file | `ImportError: cannot import name X from package` | Delete empty `mod/__init__.py` directories that scaffold from stubs |
| Git here-string + native command arg splitting | `unknown option 'query'` from words inside commit body | Use `-F file` instead: `git commit -F .commit-msg.tmp` |
| Empty execution name causes poll-loop spam | `--job-execution-name` errors firing 12/sec | Guard with pre-flight existence check + JSON parse try/catch before polling |

---

## 12. Recommended build order

For any new APEX-M on Azure project, follow this dependency chain:

1. **Scaffold** — repo layout, `pyproject.toml`, `Dockerfile`, `entrypoint.sh` with `server` case
2. **PG schemas + Key Vault** — 4 schemas (`<proj>_bronze`, `<proj>_silver`, `<proj>_gold`, `<proj>`) + foundational tables (audit_chain, budget_ledger, schema_migrations) + KV with 5 placeholder secrets
3. **Source service** — Container App with public ingress, returns OData-shaped (or your-API-shaped) JSON over some seed data
4. **Bronze loader** — Container Apps Job that pulls from source, writes raw jsonb to `<proj>_bronze.*`
5. **Silver views + Gold VVs** — PG migration creating typed views + business-ready VVs
6. **MCP server (per scenario)** — FastMCP 2.x with `@tool()` decorators querying Gold VVs
7. **MAF orchestrator** — aiohttp app, MAF skills per scenario, MCP client connections to (6), AOAI for the LLM
8. **Azure OpenAI wiring** — populate the AOAI placeholders in KV, Constitution YAML for HITL gates
9. **React portal** — Next.js 15 + theming + HITL approval surfaces
10. **Copilot connector** — Declarative Agent / Teams + M365 mobile
11. **Demo polish** — scripted walkthroughs, screenshot capture

Each phase committed independently with `feat(<tier>): SX.Y <what shipped>` messages. Each phase has its own `_verify-sX-Y.ps1`.

---

## 13. Quick-start for a new APEX-M project on Azure

1. **Clone sap-agentic as the starting template**:
   ```powershell
   git clone https://github.com/Deloitte-US-Consulting/sap-agentic.git C:\code\<new-project>
   cd C:\code\<new-project>
   git remote set-url origin <new-repo-url>
   ```

2. **Find-and-replace** the brand-specific tokens:
   - `sap-agentic` -> `<new-project>` (in pyproject.toml, README, scripts)
   - `sonepar` -> `<new-domain>` (in PG schema names, image names, container app names)
   - `kv-sap-agentic` -> `kv-<new-project>`

3. **Drop unused stubs** in `services/`, `src/<pkg>/mcp_servers/`, etc.

4. **Update `seed_data.py`** with domain-specific Faker generation (or replace with a real data fetcher).

5. **Rewrite MCP server tools** for your domain's Gold VVs.

6. **Run the phase scripts in order** (`01` -> `09` etc.), verifying after each.

---

## 14. What to NEVER do

- Don't commit `.env*` files. `.gitignore` already excludes them but be paranoid.
- Don't put secrets in script comments or task descriptions. KV pulls only.
- Don't `--no-verify` git hooks unless the user explicitly asks.
- Don't skip the `lifespan=mcp_app.lifespan` line. Save 30 min of debugging.
- Don't use em-dashes in `.ps1` files. ASCII-only.
- Don't use here-strings for git commit messages on PowerShell. `-F file` only.
- Don't assume Owner / UAA on ACR. Plan for Contributor; document MI followup.
- Don't share a Key Vault across projects. Cheap to provision, expensive to entangle.
- Don't promote Bronze VIEWs to MATERIALIZED without measuring. Tiny datasets don't need it.

---

## 15. Where to look when stuck (sap-agentic reference repo)

| Question | Where |
|---|---|
| What's the canonical Container App deploy script? | `infra/scripts/04-create-sap-sim-container-app.ps1` |
| What's the canonical MCP server pattern? | `src/sap_agentic/mcp_servers/ocom_mcp_server.py` |
| What's the canonical bronze loader pattern? | `src/sap_agentic/loaders/bronze_loader.py` |
| What's the canonical entrypoint dispatcher? | `src/sap_agentic/entrypoint.sh` |
| What's the canonical PG migration pattern? | `infra/scripts/08-create-silver-gold-views.ps1` |
| Why did X fail before? | This doc, §11 "Common gotchas" |

All accessible at https://github.com/Deloitte-US-Consulting/sap-agentic.

---

## 16. Independence (Deloitte-specific)

Microsoft platform engagement under Deloitte's **Microsoft Technology & Services Practice (DMTSP)**. **NO** alliance, **NO** preferred-partner agreement. Productized delivery pattern: **Agentic Deployment Services with Accelerator** on **APEX-M**. Language matters — never write "Deloitte's partnership with Microsoft" or similar.

---

## 17. Loading this into a new Claude session

A new session can be brought up to speed in 3 ways:

1. **GitHub URL** (preferred for any session that can fetch web):
   ```
   https://github.com/Deloitte-US-Consulting/APEX/blob/main/docs/guides/APEX-M-on-Azure-Implementation-Guide.md
   ```
   Tell the session: *"Read the APEX-M on Azure Implementation Guide at the URL above before generating anything."*

2. **Local path** (if working on the same machine):
   ```
   C:\Stage\Clients\Industries\APEX\docs\guides\APEX-M-on-Azure-Implementation-Guide.md
   ```

3. **Direct paste**: copy this entire file into a new session's first message.

Then say what you want to build (e.g. *"I want to build an agentic solution for Brand X using the APEX-M on Azure pattern"*) and the session will have all the templates + gotchas + naming conventions to ship without re-discovering them.
