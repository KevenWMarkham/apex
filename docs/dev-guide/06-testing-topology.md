# Companion 06 — Testing & Environment Topology

**APEX Core v1.2 · Developer Guide v1.0 · 2026-04-18**

> **Parent:** [`APEX-developer-guide.md`](../APEX-developer-guide.md) · **Previous:** [05 Observability & Security](./05-observability-security.md) · **Next:** [07 Service Catalog](./07-service-catalog.md)

---

## TL;DR

APEX has a **five-layer test pyramid** (unit → contract → integration → end-to-end → synthetic-load shift-replay) and a matching **three-environment workspace topology** (Dev / Test / Prod) multiplied across Practice + Tenant workspaces. The "shift-replay" synthetic-load pattern is unique to APEX — it replays a real 9-hour shift of anonymised events in 5 minutes to stress-test orchestrations and agent throughput. This companion gives you the pyramid, the fixtures, the workspace-topology rules, the L3 Practice → L4 Tenant binding mechanism, and three production runbooks.

**What you'll leave with:**
- A concrete test-pyramid scaffold in Python (pytest) and C# (xUnit)
- Fixture-recording, anonymisation, and mock-server patterns
- The dev/test/prod workspace topology and how Fabric Git bridges them
- The L3→L4 binding rules (pin, override, drift detection)
- Fabric capacity sizing and per-tenant cost allocation
- Three runbooks for the operations you'll do most often

---

## 1. The APEX test pyramid

```
           ┌─────────────────────┐
           │   shift-replay      │   ← p95 load + long-tail discovery
           │   synthetic-load    │
           ├─────────────────────┤
           │   end-to-end        │   ← full orchestration in dev workspace
           │                     │
           ├─────────────────────┤
           │    integration      │   ← Medallion transforms; agent+MCP harness
           │                     │
           ├─────────────────────┤
           │      contract       │   ← manifest roundtrip; bump classification
           │                     │
           ├─────────────────────┤
           │        unit         │   ← validators; MCP pure fns; orch step logic
           │                     │
           └─────────────────────┘
```

**Rule of thumb on proportions:** 70 % unit, 15 % contract, 10 % integration, 4 % e2e, 1 % shift-replay. Every layer catches a different failure mode. Skipping any tier guarantees you'll pay for it in prod.

### 1.1 Unit — pure functions

**Python (pytest):**
```python
# apex-core/tools/test_classify_bump.py
import pytest
from classify_bump import classify_bump

def test_add_nullable_column_is_minor():
    before = {"entities": [{"name": "X", "columns": [{"name": "a"}]}]}
    after  = {"entities": [{"name": "X",
                            "columns": [{"name": "a"}, {"name": "b", "nullable": True}]}]}
    assert classify_bump(before, after) == "MINOR"
```

**C# (xUnit):**
```csharp
// ApexCore.Tests/ClassifyBumpTests.cs
[Fact]
public void AddNullableColumn_IsMinor() {
    var before = new { entities = new[] { new { name = "X", columns = new[] { new { name = "a" } } } } };
    var after  = new { entities = new[] {
        new { name = "X", columns = new[] { new { name = "a" }, new { name = "b", nullable = true } } }
    }};
    Assert.Equal("MINOR", ClassifyBump.Classify(before, after));
}
```

**Coverage expectations:** every validator rule has one positive and one negative test. Every MCP tool has tests for happy-path, invalid-arg, tenant-scope-violation, and data-not-found. Use `node --test` (Node) and pytest/xUnit for Python/C# components.

### 1.2 Contract — manifest roundtrip + bump classification

- Every practice manifest must round-trip through `validate-practice` with zero critical findings.
- Every schema bump must classify deterministically (same input → same bump).
- Every cross-practice reference (e.g., a service referring to an agent and a schema) must resolve.

```javascript
// apex-core/tools/contract.test.js (Node)
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { validateServiceManifest } from './validate-service-manifest.js';

test('every service fixture validates against its practice manifest', () => {
  const fixtures = readdirSync('apex-rc/data/services');
  for (const f of fixtures) {
    const svc = JSON.parse(readFileSync(`apex-rc/data/services/${f}`, 'utf8'));
    const { findings } = validateServiceManifest(svc);
    assert.equal(findings.filter(x => x.severity === 'critical').length, 0, f);
  }
});
```

### 1.3 Integration — Medallion transforms against fixtures

**Python (pytest + PySpark `SparkSession.builder.master("local")`):**
```python
# apex-rc/notebooks/silver/test_merml_store_inventory.py
import pytest
from pyspark.sql import SparkSession
from transforms.merml_store_inventory_position import transform

@pytest.fixture(scope="session")
def spark():
    return SparkSession.builder.master("local[2]").getOrCreate()

def test_inventory_transform_produces_canonical_envelope(spark):
    bronze = spark.read.json("fixtures/bronze/manhattan_inventory_snapshot.json")
    silver = transform(bronze)
    assert set(silver.columns) >= {
        "event_id", "event_ts", "entity_id", "source_system",
        "source_system_ts", "pii_tokenized", "on_hand", "on_shelf", "in_backroom"
    }
```

**C# equivalent uses Microsoft.Spark or calls the PySpark transform as a black box; mix is OK.**

### 1.4 End-to-end — full orchestration in Dev workspace

Tests that a trigger event → orchestration → HITL card → audit row, measured inside a dev Fabric workspace:

```python
# tests/e2e/test_cold_chain_excursion.py
import pytest
from apex_harness.e2e import seed_event, wait_for_card, approve_card, assert_audit_row

@pytest.mark.e2e
async def test_cold_chain_e2e_happy_path():
    trace_id = await seed_event(
        workspace="apex-rc-practice-dev",
        service="APEX-RC-CXP-01",
        fixture="fixtures/excursions/reefer14_single.json")
    card = await wait_for_card(trace_id, timeout_sec=60)
    await approve_card(card, decision="approve")
    audit = await assert_audit_row(trace_id, decision="approve", gate_kind="HITL")
    assert audit["rollback_pointer"] is not None
```

### 1.5 Shift-replay — the APEX signature test

Replays **9 hours of a real anonymised shift** at **100× speed** through the dev workspace. Intended to surface:

- Orchestration contention (multiple excursions at the same minute)
- Agent concurrency bugs (identity collisions, cache poisoning)
- Long-tail HITL queue behaviour
- Cost-envelope drift (token spend per shift)

```python
# tests/shift_replay/test_store_100_shift.py
from apex_harness.replay import ShiftReplay

def test_store_100_shift_9h_at_100x():
    replay = ShiftReplay(
        workspace="apex-rc-practice-dev",
        fixture_dir="fixtures/shifts/store_100_2026_04_14",
        speedup=100,
        expected_events=8)
    result = replay.run()
    assert result.orchestrations_succeeded >= 7    # allow 1 canary failure
    assert result.p95_decision_sec <= 480           # SLO guard
    assert result.token_spend_usd <= 4.50           # cost envelope
```

The shift-replay harness writes its report to `dist/shift-replay-<date>.json` for trend tracking.

---

## 2. Fixtures & mocks

### 2.1 Recording real SOR payloads

```python
# tools/record-fixture.py
# Capture a live SOR payload, anonymise, save as fixture.
from apex_anonymise import Anonymiser
import httpx, json, pathlib

async def record(sor, endpoint, outpath):
    data = await httpx.get(endpoint).json()
    anonymised = Anonymiser(
        pii_fields=["customer_email", "customer_phone", "mrn", "ssn"],
        id_fields=["store_id", "patient_id"],
        preserve_timing=True).apply(data)
    pathlib.Path(outpath).write_text(json.dumps(anonymised, indent=2))
```

**Anonymisation rules:**
- PII fields → replaced with realistic but synthetic values (names from a faker library, phone numbers from a reserved block)
- ID fields → hashed with a seeded HMAC so fixture-to-fixture joins still work
- Timestamps → preserved exactly (so replay timing matches reality)

### 2.2 MCP-server mocks

For agent tests, run a lightweight MCP mock server:

**Python:**
```python
from apex_harness.mocks import MockMcpServer

mcp = MockMcpServer("fabric-mcp")
mcp.when("read_cold_chain_telemetry").with_args(store_id="acct-a7f2c-001").returns([
    {"sensor_id":"S1","lot_id":"L1","temp_f":52.3,"threshold_f":41,
     "event_ts":"2026-04-14T06:00:00Z","is_breaching":True}
])

# Agent harness picks up MCP_MOCK_ENDPOINT env var
```

**C#:**
```csharp
var mcp = new MockMcpServer("fabric-mcp");
mcp.When("read_cold_chain_telemetry").WithArgs(new { storeId = "acct-a7f2c-001" })
   .Returns(new[] {
       new TelemetryReading("S1","L1",52.3m,41m,
                            DateTimeOffset.Parse("2026-04-14T06:00:00Z"), true)
   });
```

---

## 3. Environment topology

### 3.1 The three environments

| Env | Workspaces | Data | Identity scope | Gates enforced |
|---|---|---|---|---|
| **Dev** | `apex-*-practice-dev`, personal branch workspaces | Synthetic + anonymised fixtures | Dev SP only | Gates in dry-run mode |
| **Test** | `apex-*-practice-test`, `apex-*-tenant-test` | Synthetic + periodic anonymised prod replay | Test SP + test user group | Gates full-run against test identity group |
| **Prod** | `apex-*-practice-prod`, `apex-*-tenant-prod` | Real tenant data | Real tenant identity groups | All gates enforced; real HITL |

### 3.2 Promotion rules

1. **Dev → Test:** Fabric Git merge + pipeline re-run. Data replays an anonymised 7-day prod window.
2. **Test → Prod:** manual release-bundler invocation + tenant pin update. No code change is needed on the tenant side — manifests pin a Practice release.
3. **Never:** copy data from Prod to Dev. Use anonymised replays.

### 3.3 Dev branch workspaces (per-developer)

Each developer gets an ephemeral branch workspace:

```
apex-rc-practice-dev-<git-branch>-<dev-initial>
e.g., apex-rc-practice-dev-feat-cxp-cold-chain-threshold-km
```

Fabric Git creates these on push, tears them down when the branch is deleted. Don't point them at shared capacity — use a separate small Fabric capacity for dev.

---

## 4. L3 Practice → L4 Tenant binding

### 4.1 Pin model

A tenant-manifest *pins* a specific Practice release:

```json
{
  "tenant_id": "acct-a7f2c-001",
  "practice": "RC",
  "practice_pinned_version": "1.2.0",
  "subscribed_services": ["APEX-RC-CXP-01", "APEX-RC-ESL-03"]
}
```

The pin is the contract. Upgrading happens by the tenant flipping the pin (with policy control):

```bash
node apex-core/tools/apex-sync.js \
    --tenant acct-a7f2c-001 \
    --practice rc \
    --pin 1.3.0
```

### 4.2 Tenant overrides (sparingly)

Tenants can override narrow settings without forking the Practice:

```json
{
  "practice_pinned_version": "1.2.0",
  "overrides": {
    "agents.SCM-A04.model": "gpt-4.1-reasoning",
    "slos.APEX-RC-CXP-01.decision_p95_min": 5
  }
}
```

Overrides are validated by `apex-validate`. Only specific fields are overridable (model family, SLO targets, gate-kind upgrades — never the output schema or tool allow-list).

### 4.3 Drift detection

Daily job compares deployed state of each tenant against the pinned release manifest. Any divergence → a Silver row in `apex_drift_log` + a Teams alert to the practice SRE.

---

## 5. Capacity & cost allocation

### 5.1 Right-sizing Fabric capacity

Rule of thumb, per practice:

| Tenants active | Base capacity | Typical burst |
|---|---|---|
| 1–5 | F8 | 2× base during shift peaks |
| 5–25 | F16 | 2×–3× during shift peaks |
| 25+ | F32 + per-tenant F4 add-ons | Smoothing debt accrues |

For HLS and ER practices, **double these** (higher compute per decision due to reasoning-model use).

### 5.2 Per-tenant cost tagging

```yaml
# Azure resource tags (applied at deploy time)
apex-practice: rc
apex-tenant:   acct-a7f2c-001
apex-env:      prod
apex-service:  APEX-RC-CXP-01   # when resource is service-specific
```

Cost Management + Power BI generates per-tenant monthly bills from these tags.

### 5.3 Agent invocation cost envelope

| Cost element | Typical per invocation |
|---|---|
| LLM tokens (gpt-4.1) | $0.02 – $0.10 |
| LLM tokens (reasoning tier) | $0.15 – $0.80 |
| Fabric SQL reads | $0.001 – $0.005 |
| HITL analyst time | 90 sec → $1.50 fully-loaded |
| Total (RC, std agent) | ~$0.05 per invocation |
| Total (HLS, reasoning) | ~$0.80 per invocation |

Services bill at a margin on top of this cost envelope (exact pricing in Companion 07).

---

## 6. Runbook — "Deploy a new agent version to one tenant"

**Context:** `SCM-A04 v1.2.0` is ready. Tenant `acct-a7f2c-001` wants it rolled out ahead of the broad release.

```bash
# 1. Sanity-check the bundle
node apex-core/tools/apex-validate.js --bundle dist/apex-rc-1.2.0.tar.gz

# 2. Update the tenant manifest override (pin SCM-A04 to 1.2.0 only)
cat > tenant-override.json <<EOF
{
  "agents": { "SCM-A04": { "pinned_version": "1.2.0" } }
}
EOF
node apex-core/tools/apex-sync.js \
    --tenant acct-a7f2c-001 \
    --override-file tenant-override.json

# 3. Verify
node apex-core/tools/apex-validate.js --tenant acct-a7f2c-001
# → expect: deployed SCM-A04 version = 1.2.0; all other agents unchanged

# 4. Smoke test: seed one synthetic excursion
python tools/seed-event.py --tenant acct-a7f2c-001 --fixture cold_chain_minor

# 5. Watch App Insights for the agent invoke span; verify version label = 1.2.0
```

---

## 7. Runbook — "Re-bake Gold views after a schema MINOR bump"

**Context:** `SCML.COLD_CHAIN_TELEMETRY` added a `humidity` column (MINOR). Gold views need to expose it.

```bash
# 1. Regenerate the Gold DDL from the updated manifest
node apex-core/tools/ddl-driver.js \
    --practice rc \
    --layer gold \
    --out dist/ddl/gold/

# 2. Diff against the deployed views
node apex-core/tools/ddl-driver.js --diff \
    --deployed apex-rc-practice-prod \
    --generated dist/ddl/gold/

# 3. Apply the new DDL to the practice workspace's Warehouse
#    (one tenant at a time in prod)
az synapse-spark run ...    # or use the Fabric SQL endpoint

# 4. Recycle the SQL endpoint connections (schemas are cached)
node apex-core/tools/apex-sync.js \
    --tenant acct-a7f2c-001 \
    --sql-endpoint-recycle

# 5. Verify agent invocations read the new column
```

---

## 8. Runbook — "Rollback a failed orchestration change"

**Context:** `ORCH-03 v1.3.0` was released; canary criteria tripped at 14 hours (false-positive rate > 5 %).

```bash
# 1. Agent Service auto-rolls the weight back to 0, but you need to pin tenants
for tenant in $(cat rc-tenants.txt); do
    node apex-core/tools/apex-sync.js \
        --tenant $tenant \
        --pin-orch "ORCH-03@1.2.0"
done

# 2. Invalidate the 5 % of decisions made under v1.3.0 during the canary window
#    by running compensating orchestrations where appropriate
python tools/compensate-canary.py \
    --orch ORCH-03 --from-version 1.3.0 --to-version 1.2.0 \
    --window "2026-04-14T00:00Z/2026-04-14T14:00Z"

# 3. Post-mortem: write a minimal fixture that reproduces the false positive
#    and add it to the fixture-replay test suite as a regression guard

# 4. Unblock future v1.3.x: fix the bug; re-ship as v1.3.1 with
#    the new fixture passing
```

---

## 9. Cross-references

- Shim test that proves backward-compat of the L3 rename: `apex-core/tools/validate-fleet.test.js`
- How the deployed workspace is created: [Companion 01 — Fabric Layering](./01-fabric-layering.md)
- Silver fixture recording: [Companion 02 — Medallion + SOR](./02-medallion-sor.md)
- MCP-server mock pattern: [Companion 03 — MCP Servers](./03-mcp-servers.md)
- Canary-release rollback criteria: [Companion 04 — Agent Lifecycle](./04-agent-lifecycle.md) §6.2
- Telemetry that powers the drift-detection job: [Companion 05 — Observability & Security](./05-observability-security.md)
- Per-service SLO targets used in runbooks: [Companion 07 — Service Catalog](./07-service-catalog.md)
