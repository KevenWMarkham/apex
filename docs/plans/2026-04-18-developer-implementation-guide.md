# APEX Developer Implementation Guide — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Deliver a mixed-audience APEX Developer Implementation Guide (spine + 7 companions, rendered to .md and .docx), rename the L3 layer from "Fleet" to "Practice" across APEX Core, and promote Services to a first-class, validated APEX artifact with 24 service fixtures across 4 Practices.

**Architecture:** Markdown sources under `docs/` and `docs/dev-guide/`, rendered to .docx via the existing `build-docx.cjs` pipeline. New JSON contracts in `apex-core/data/`, new Node ES-module validators in `apex-core/tools/` (each with matching `.test.js`), service fixtures in `apex-core/fixtures/services/`. Catalog companion is generated from fixtures so doc and data stay in sync.

**Tech Stack:** Node.js 20+ (ES modules), `node:test` runner, `semver`, `docx` (CommonJS for Word rendering), Mermaid for diagrams (pre-processed to PNG during .docx build).

**Reference:** This plan implements the design at `docs/plans/2026-04-18-developer-implementation-guide-design.md`.

---

## Sequencing

```
Phase 0  Foundation — rename fleet → practice (+ deprecation shim)
Phase 1  New APEX Core artifacts — contracts, validators, wiring
Phase 2  Service fixtures — 24 services across RC/HLS/ER/AXLE
Phase 3  Build tooling — catalog generator + docx extension
Phase 4  Write the guide — spine + 7 companions (TDD for code snippets only)
Phase 5  Migration — update existing artifacts to Practice terminology
Phase 6  Final validation — full test suite, render all .docx, cross-ref audit
```

**Commit cadence:** commit after each task. Tests run via `npm test` from repo root.

---

## Phase 0 — Foundation: Rename Fleet → Practice

### Task 0.1: Copy validate-fleet.js to validate-practice.js (deprecation shim stays)

**Files:**
- Create: `apex-core/tools/validate-practice.js`
- Create: `apex-core/tools/validate-practice.test.js`
- Keep: `apex-core/tools/validate-fleet.js` (becomes a shim)

**Step 1: Write the failing test**

Create `apex-core/tools/validate-practice.test.js`:

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validatePractice } from './validate-practice.js';

test('validatePractice exports a function', () => {
  assert.equal(typeof validatePractice, 'function');
});

test('validatePractice returns findings array for empty registry', () => {
  const result = validatePractice({}, new Map());
  assert.ok(Array.isArray(result.findings));
});

test('validatePractice is behavior-compatible with validateFleet', async () => {
  const { validateFleet } = await import('./validate-fleet.js');
  const empty = { accounts: [] };
  const editions = new Map();
  const fleetResult = validateFleet(empty, editions);
  const practiceResult = validatePractice(empty, editions);
  assert.deepEqual(practiceResult.findings.length, fleetResult.findings.length);
});
```

**Step 2: Run test to verify it fails**

Run: `npm test -- apex-core/tools/validate-practice.test.js`
Expected: FAIL with "Cannot find module './validate-practice.js'"

**Step 3: Create validate-practice.js with renamed exports**

Copy `apex-core/tools/validate-fleet.js` to `apex-core/tools/validate-practice.js`, then in the new file:
- Rename exported function `validateFleet` → `validatePractice`
- Rename JSDoc param `registry` from "fleet-registry.json" → "practice-registry.json"
- Rename rule prefixes `FLEET-*` → `PRACTICE-*` (e.g., `FLEET-SHAPE-ROOT` → `PRACTICE-SHAPE-ROOT`)
- Keep all internal logic identical

**Step 4: Make validate-fleet.js a shim**

Replace the full contents of `apex-core/tools/validate-fleet.js` with:

```javascript
// DEPRECATED: This module is retained for backward compatibility only.
// Use validate-practice.js instead. This shim will be removed in Core v1.3.
//
// The L3 layer was renamed from "Fleet" to "Practice" in Core v1.2.1 to
// reflect that L3 bundles schemas, agents, MCP tools, orchestrations, gates,
// services, personas, and KPIs — not just agents.
import { validatePractice } from './validate-practice.js';

export function validateFleet(registry, editionManifests, opts = {}) {
  const result = validatePractice(registry, editionManifests, opts);
  // Translate PRACTICE-* rules back to FLEET-* for callers still parsing them.
  return {
    ...result,
    findings: result.findings.map(f => ({
      ...f,
      rule: f.rule.replace(/^PRACTICE-/, 'FLEET-')
    }))
  };
}
```

**Step 5: Run tests to verify all pass (including existing fleet tests)**

Run: `npm test`
Expected: all previous `validate-fleet.test.js` tests still pass + new practice tests pass.

**Step 6: Commit**

```bash
git add apex-core/tools/validate-practice.js apex-core/tools/validate-practice.test.js apex-core/tools/validate-fleet.js
git commit -m "feat(core): add validate-practice as canonical L3 validator; keep validate-fleet as shim

L3 layer renamed from 'Fleet' to 'Practice'. validate-practice.js is the
new canonical implementation. validate-fleet.js is preserved as a shim
that delegates to validate-practice and translates rule codes back to
FLEET-* for any downstream caller still parsing them. Shim removal is
scheduled for Core v1.3.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 0.2: Rename validate-fleet tests to validate-practice tests

**Files:**
- Modify: `apex-core/tools/validate-fleet.test.js` (shrink to minimal shim test)
- Modify: `apex-core/tools/validate-practice.test.js` (absorb original tests with updated rule codes)

**Step 1: Write failing assertion**

In `apex-core/tools/validate-practice.test.js`, copy all tests from `validate-fleet.test.js` and update rule code expectations (`FLEET-*` → `PRACTICE-*`).

**Step 2: Run tests**

Run: `npm test -- apex-core/tools/validate-practice.test.js`
Expected: PASS for all absorbed tests.

**Step 3: Shrink validate-fleet.test.js to a single "shim still works" test**

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validateFleet } from './validate-fleet.js';

test('validate-fleet shim returns FLEET-* rule codes for backward compatibility', () => {
  const result = validateFleet({}, new Map());
  const nonCompliant = result.findings.filter(f => f.rule.startsWith('PRACTICE-'));
  assert.equal(nonCompliant.length, 0, 'shim must translate PRACTICE-* back to FLEET-*');
});
```

**Step 4: Commit**

```bash
git add apex-core/tools/validate-fleet.test.js apex-core/tools/validate-practice.test.js
git commit -m "test(core): migrate fleet tests to practice; keep shim-coverage test"
```

---

## Phase 1 — New APEX Core Artifacts

### Task 1.1: Persona catalog data file + contract

**Files:**
- Create: `apex-core/data/persona-catalog.json`
- Create: `apex-core/data/persona-catalog-contract.json`
- Create: `apex-core/tools/validate-persona-catalog.js`
- Create: `apex-core/tools/validate-persona-catalog.test.js`

**Step 1: Write the failing test**

Create `apex-core/tools/validate-persona-catalog.test.js`:

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { validatePersonaCatalog } from './validate-persona-catalog.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const loadJson = (p) => JSON.parse(readFileSync(p, 'utf8'));
const catalog = () => loadJson(resolve(__dirname, '../data/persona-catalog.json'));

test('valid persona catalog returns no critical findings', () => {
  const result = validatePersonaCatalog(catalog());
  const crits = result.findings.filter(f => f.severity === 'critical');
  assert.equal(crits.length, 0, JSON.stringify(crits, null, 2));
});

test('persona id must match pattern', () => {
  const c = { personas: [{ id: 'Not-Valid-ID', name: 'X', practices: ['RC'] }] };
  const result = validatePersonaCatalog(c);
  assert.ok(result.findings.some(f => f.rule === 'PERSONA-ID-PATTERN'));
});

test('duplicate persona ids are flagged', () => {
  const c = { personas: [
    { id: 'store-mod', name: 'A', practices: ['RC'] },
    { id: 'store-mod', name: 'B', practices: ['RC'] }
  ]};
  const result = validatePersonaCatalog(c);
  assert.ok(result.findings.some(f => f.rule === 'PERSONA-DUPLICATE-ID'));
});

test('persona must reference a known practice', () => {
  const c = { personas: [{ id: 'x', name: 'X', practices: ['ZZZ'] }] };
  const result = validatePersonaCatalog(c);
  assert.ok(result.findings.some(f => f.rule === 'PERSONA-UNKNOWN-PRACTICE'));
});
```

**Step 2: Create the data file**

Create `apex-core/data/persona-catalog.json`:

```json
{
  "catalog_version": "1.0",
  "last_updated": "2026-04-18",
  "valid_practices": ["RC", "HLS", "ER", "AXLE", "TMT", "TH", "ICE"],
  "personas": [
    { "id": "store-mod", "name": "Store Manager on Duty", "practices": ["RC"], "description": "Front-line operator running a retail store's shift. Owns HITL approvals for in-store APEX decisions." },
    { "id": "regional-ops-director", "name": "Regional Operations Director", "practices": ["RC"], "description": "Oversees a cluster of stores; consumer of escalations and cross-store analytics." },
    { "id": "compliance-officer", "name": "Compliance Officer", "practices": ["RC", "HLS", "ER"], "description": "Regulatory and audit accountability; consumes recall & incident service outputs." },
    { "id": "merchandising-analyst", "name": "Merchandising Analyst", "practices": ["RC"], "description": "Pricing, assortment, ESL state; owns pricing-integrity decisions." },
    { "id": "loss-prevention-lead", "name": "Loss Prevention Lead", "practices": ["RC"], "description": "Shrink investigations; consumes shrink & void escalations." },
    { "id": "customer-care-agent", "name": "Customer Care Agent", "practices": ["RC", "HLS", "ER"], "description": "Front-line customer-facing resolver; HITL for substitution & incident gates." },
    { "id": "charge-nurse", "name": "Charge Nurse", "practices": ["HLS"], "description": "Unit-level clinical lead; HITL for discharge-readiness and sepsis-warning decisions." },
    { "id": "clinical-informaticist", "name": "Clinical Informaticist", "practices": ["HLS"], "description": "Bridges clinical workflow and data; tunes agent thresholds." },
    { "id": "revenue-cycle-analyst", "name": "Revenue Cycle Analyst", "practices": ["HLS"], "description": "Denials, claims, reimbursement; HITL for rev-cycle decisions." },
    { "id": "supply-chain-pharm", "name": "Pharmacy Supply Lead", "practices": ["HLS"], "description": "Medication & supply expiry; HITL for clinical supply decisions." },
    { "id": "trial-coordinator", "name": "Clinical Trial Coordinator", "practices": ["HLS"], "description": "Patient-trial matching and enrolment." },
    { "id": "patient-safety-officer", "name": "Patient Safety Officer", "practices": ["HLS"], "description": "Incident review and reporting." },
    { "id": "grid-ops-engineer", "name": "Grid Operations Engineer", "practices": ["ER"], "description": "Real-time grid state; HITL for anomaly responses." },
    { "id": "field-dispatcher", "name": "Field Dispatcher", "practices": ["ER"], "description": "Work-order optimisation and crew assignment." },
    { "id": "meter-ops-lead", "name": "Meter Operations Lead", "practices": ["ER"], "description": "Meter reading, outage detection, revenue-assurance." },
    { "id": "billing-ops-analyst", "name": "Billing Operations Analyst", "practices": ["ER"], "description": "Billing-exception resolution." },
    { "id": "regulatory-affairs", "name": "Regulatory Affairs Officer", "practices": ["ER", "HLS"], "description": "Regulatory filings and compliance events." },
    { "id": "plant-supervisor", "name": "Plant Floor Supervisor", "practices": ["AXLE"], "description": "Shift-level production lead; HITL for line-down and quality decisions." },
    { "id": "quality-engineer", "name": "Quality Engineer", "practices": ["AXLE"], "description": "Quality excursions, traceability, CAPA." },
    { "id": "supply-chain-planner", "name": "Supply Chain Planner", "practices": ["AXLE", "RC"], "description": "Supply-disruption triage and expediting." },
    { "id": "plant-manager", "name": "Plant Manager", "practices": ["AXLE"], "description": "Plant-wide KPIs, executive escalation." },
    { "id": "recall-coordinator", "name": "Recall Coordinator", "practices": ["AXLE", "RC", "HLS"], "description": "Traceability and customer notification for recalls." }
  ]
}
```

**Step 3: Create the validator**

Create `apex-core/tools/validate-persona-catalog.js`:

```javascript
const PERSONA_ID_RE = /^[a-z][a-z0-9-]{1,39}$/;

export function validatePersonaCatalog(catalog) {
  const findings = [];
  if (!catalog || typeof catalog !== 'object') {
    return { findings: [{ severity: 'critical', rule: 'PERSONA-SHAPE-ROOT', path: '$', message: 'catalog must be an object' }] };
  }
  const validPractices = new Set(catalog.valid_practices || []);
  const seen = new Set();
  const personas = Array.isArray(catalog.personas) ? catalog.personas : [];
  if (!Array.isArray(catalog.personas)) {
    findings.push({ severity: 'critical', rule: 'PERSONA-SHAPE-LIST', path: '$.personas', message: 'personas must be an array' });
  }
  for (const [i, p] of personas.entries()) {
    const path = `$.personas[${i}]`;
    if (!p.id || !PERSONA_ID_RE.test(p.id)) {
      findings.push({ severity: 'critical', rule: 'PERSONA-ID-PATTERN', path: `${path}.id`, message: `id must match /^[a-z][a-z0-9-]{1,39}$/; got ${p.id}` });
    }
    if (seen.has(p.id)) {
      findings.push({ severity: 'critical', rule: 'PERSONA-DUPLICATE-ID', path: `${path}.id`, message: `duplicate persona id ${p.id}` });
    }
    seen.add(p.id);
    if (!p.name || typeof p.name !== 'string') {
      findings.push({ severity: 'critical', rule: 'PERSONA-NAME-REQUIRED', path: `${path}.name`, message: 'name is required' });
    }
    const practices = Array.isArray(p.practices) ? p.practices : [];
    if (practices.length === 0) {
      findings.push({ severity: 'critical', rule: 'PERSONA-PRACTICE-REQUIRED', path: `${path}.practices`, message: 'at least one practice required' });
    }
    for (const pr of practices) {
      if (validPractices.size && !validPractices.has(pr)) {
        findings.push({ severity: 'critical', rule: 'PERSONA-UNKNOWN-PRACTICE', path: `${path}.practices`, message: `unknown practice ${pr}` });
      }
    }
  }
  return { findings };
}
```

**Step 4: Run tests**

Run: `npm test -- apex-core/tools/validate-persona-catalog.test.js`
Expected: PASS (4 tests).

**Step 5: Commit**

```bash
git add apex-core/data/persona-catalog.json apex-core/tools/validate-persona-catalog.js apex-core/tools/validate-persona-catalog.test.js
git commit -m "feat(core): add persona catalog data + validator

Master persona catalog with 22 personas across RC, HLS, ER, AXLE practices.
Used by service-manifest.personas.{primary,secondary,consumer} for validation.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 1.2: Write service-manifest-contract.json

**Files:**
- Create: `apex-core/data/service-manifest-contract.json`

**Step 1: Author the contract**

Write the JSON schema-shaped contract documenting service-manifest required fields, patterns, and enums. Structure mirrors `schema-manifest-contract.json`:

```json
{
  "contract_version": "1.0",
  "core_version": "1.2",
  "last_updated": "2026-04-18",
  "required_fields": {
    "service_id": { "type": "string", "pattern": "^APEX-(RC|HLS|ER|AXLE|TMT|TH|ICE)-[A-Z]{2,4}-[0-9]{2}$" },
    "service_name": { "type": "string" },
    "practice": { "type": "enum", "values": ["RC", "HLS", "ER", "AXLE", "TMT", "TH", "ICE"] },
    "version": { "type": "semver" },
    "lifecycle": { "type": "enum", "values": ["Preview", "GA", "Deprecated"] },
    "tier": { "type": "array", "items_enum": ["Essentials", "Pro", "Enterprise"], "min_items": 1 },
    "scenario": { "type": "object", "required_keys": ["trigger", "business_pain", "cadence"] },
    "personas": { "type": "object", "required_keys": ["primary"] },
    "kpis": { "type": "array", "min_items": 1, "item_shape": "kpi_entry" },
    "slos": { "type": "object" },
    "artifacts": { "type": "object", "required_keys": ["schemas", "agents", "orchestration", "hitl_gate"] },
    "prerequisites": { "type": "object", "required_keys": ["practice_min_version"] },
    "commercial": { "type": "object" }
  },
  "kpi_entry": {
    "id": { "type": "string", "pattern": "^[a-z][a-z0-9_]+$" },
    "target": { "type": "number" },
    "direction": { "type": "enum", "values": ["maximize", "minimize"] }
  },
  "scenario_shape": {
    "trigger": { "type": "string" },
    "business_pain": { "type": "string" },
    "cadence": { "type": "enum", "values": ["continuous", "episodic", "nightly", "on-demand"] }
  },
  "slo_keys": {
    "detection_p95_sec": { "type": "number", "min": 0 },
    "decision_p95_min": { "type": "number", "min": 0 },
    "false_positive_rate": { "type": "number", "min": 0, "max": 1 },
    "availability_pct": { "type": "number", "min": 0, "max": 100 }
  },
  "artifacts_shape": {
    "schemas": { "type": "array", "min_items": 1 },
    "agents": { "type": "array", "min_items": 1 },
    "mcp_tools": { "type": "array" },
    "orchestration": { "type": "string", "pattern": "^ORCH-[0-9]{2}$" },
    "hitl_gate": { "type": "enum", "values": ["HITL", "ACK_ONLY", "ZERO_TOUCH", "ESCALATION"] }
  }
}
```

**Step 2: Commit**

```bash
git add apex-core/data/service-manifest-contract.json
git commit -m "feat(core): add service-manifest-contract v1.0

Formalises service SKU shape so services become first-class, validated
APEX artifacts.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 1.3: validate-service-manifest.js (TDD)

**Files:**
- Create: `apex-core/tools/validate-service-manifest.js`
- Create: `apex-core/tools/validate-service-manifest.test.js`
- Create: `apex-core/tools/fixtures/valid-service.json` (minimal valid fixture)

**Step 1: Author minimal valid fixture**

Create `apex-core/tools/fixtures/valid-service.json`:

```json
{
  "service_id": "APEX-RC-CXP-01",
  "service_name": "Cold Chain Excursion Response",
  "practice": "RC",
  "version": "1.2.0",
  "lifecycle": "GA",
  "tier": ["Pro", "Enterprise"],
  "scenario": { "trigger": "Reefer breach > 2h", "business_pain": "Write-offs", "cadence": "continuous" },
  "personas": { "primary": ["store-mod"], "secondary": ["regional-ops-director"] },
  "kpis": [ { "id": "writeoff_avoided_pct", "target": 0.65, "direction": "maximize" } ],
  "slos": { "detection_p95_sec": 60, "decision_p95_min": 8, "false_positive_rate": 0.03, "availability_pct": 99.5 },
  "artifacts": {
    "schemas": ["SCML.COLD_CHAIN_TELEMETRY"], "agents": ["SCM-A04"],
    "mcp_tools": ["fabric-mcp.read_telemetry"], "orchestration": "ORCH-03", "hitl_gate": "HITL"
  },
  "prerequisites": { "practice_min_version": "1.2.0", "sor_connections": ["monnit-iot"], "fabric_capacity": "F8", "identity_group": "store-mod" },
  "commercial": { "subscription_model": "per_store_year + per_invocation", "support_tiers": ["Pro", "Enterprise"], "onboarding_days": 14 }
}
```

**Step 2: Write failing tests**

Create `apex-core/tools/validate-service-manifest.test.js`:

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { validateServiceManifest } from './validate-service-manifest.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const load = (p) => JSON.parse(readFileSync(p, 'utf8'));
const valid = () => load(resolve(__dirname, 'fixtures/valid-service.json'));

test('valid service manifest produces no critical findings', () => {
  const r = validateServiceManifest(valid());
  const crits = r.findings.filter(f => f.severity === 'critical');
  assert.equal(crits.length, 0, JSON.stringify(crits, null, 2));
});

test('service_id must match APEX-<practice>-<domain>-<nn> pattern', () => {
  const s = valid(); s.service_id = 'bad-id';
  const r = validateServiceManifest(s);
  assert.ok(r.findings.some(f => f.rule === 'SERVICE-ID-PATTERN'));
});

test('practice must be valid enum', () => {
  const s = valid(); s.practice = 'ZZZ';
  const r = validateServiceManifest(s);
  assert.ok(r.findings.some(f => f.rule === 'SERVICE-PRACTICE-ENUM'));
});

test('version must be semver', () => {
  const s = valid(); s.version = 'not-semver';
  const r = validateServiceManifest(s);
  assert.ok(r.findings.some(f => f.rule === 'SERVICE-VERSION-SEMVER'));
});

test('lifecycle must be valid enum', () => {
  const s = valid(); s.lifecycle = 'Alpha';
  const r = validateServiceManifest(s);
  assert.ok(r.findings.some(f => f.rule === 'SERVICE-LIFECYCLE-ENUM'));
});

test('kpis must have at least one entry', () => {
  const s = valid(); s.kpis = [];
  const r = validateServiceManifest(s);
  assert.ok(r.findings.some(f => f.rule === 'SERVICE-KPIS-EMPTY'));
});

test('kpi direction must be maximize or minimize', () => {
  const s = valid(); s.kpis[0].direction = 'sideways';
  const r = validateServiceManifest(s);
  assert.ok(r.findings.some(f => f.rule === 'SERVICE-KPI-DIRECTION'));
});

test('slo detection_p95_sec must be < decision_p95_min * 60', () => {
  const s = valid(); s.slos.detection_p95_sec = 99999;
  const r = validateServiceManifest(s);
  assert.ok(r.findings.some(f => f.rule === 'SERVICE-SLO-ORDER'));
});

test('hitl_gate must be valid enum', () => {
  const s = valid(); s.artifacts.hitl_gate = 'NEVER';
  const r = validateServiceManifest(s);
  assert.ok(r.findings.some(f => f.rule === 'SERVICE-GATE-ENUM'));
});

test('orchestration must match ORCH-NN pattern', () => {
  const s = valid(); s.artifacts.orchestration = 'bad';
  const r = validateServiceManifest(s);
  assert.ok(r.findings.some(f => f.rule === 'SERVICE-ORCH-PATTERN'));
});

test('personas.primary must reference known personas when catalog supplied', () => {
  const s = valid();
  const r = validateServiceManifest(s, { knownPersonas: new Set(['regional-ops-director']) });
  assert.ok(r.findings.some(f => f.rule === 'SERVICE-PERSONA-UNKNOWN'));
});
```

**Step 3: Run tests to verify failure**

Run: `npm test -- apex-core/tools/validate-service-manifest.test.js`
Expected: FAIL with "Cannot find module".

**Step 4: Implement validate-service-manifest.js**

Create `apex-core/tools/validate-service-manifest.js`:

```javascript
import semver from 'semver';

const SERVICE_ID_RE = /^APEX-(RC|HLS|ER|AXLE|TMT|TH|ICE)-[A-Z]{2,4}-[0-9]{2}$/;
const KPI_ID_RE = /^[a-z][a-z0-9_]+$/;
const ORCH_RE = /^ORCH-[0-9]{2}$/;
const VALID_PRACTICES = new Set(['RC', 'HLS', 'ER', 'AXLE', 'TMT', 'TH', 'ICE']);
const VALID_LIFECYCLE = new Set(['Preview', 'GA', 'Deprecated']);
const VALID_TIER = new Set(['Essentials', 'Pro', 'Enterprise']);
const VALID_CADENCE = new Set(['continuous', 'episodic', 'nightly', 'on-demand']);
const VALID_GATE = new Set(['HITL', 'ACK_ONLY', 'ZERO_TOUCH', 'ESCALATION']);
const VALID_DIRECTION = new Set(['maximize', 'minimize']);

export function validateServiceManifest(svc, opts = {}) {
  const findings = [];
  const add = (rule, path, message, severity = 'critical') =>
    findings.push({ severity, rule, path, message });

  if (!svc || typeof svc !== 'object') {
    return { findings: [{ severity: 'critical', rule: 'SERVICE-SHAPE-ROOT', path: '$', message: 'service must be an object' }] };
  }

  if (!SERVICE_ID_RE.test(svc.service_id || '')) {
    add('SERVICE-ID-PATTERN', '$.service_id', `service_id must match APEX-<practice>-<domain>-<nn>; got ${svc.service_id}`);
  }
  if (!svc.service_name || typeof svc.service_name !== 'string') {
    add('SERVICE-NAME-REQUIRED', '$.service_name', 'service_name is required');
  }
  if (!VALID_PRACTICES.has(svc.practice)) {
    add('SERVICE-PRACTICE-ENUM', '$.practice', `practice must be one of ${[...VALID_PRACTICES].join(', ')}; got ${svc.practice}`);
  }
  if (!svc.version || !semver.valid(svc.version)) {
    add('SERVICE-VERSION-SEMVER', '$.version', `version must be semver; got ${svc.version}`);
  }
  if (!VALID_LIFECYCLE.has(svc.lifecycle)) {
    add('SERVICE-LIFECYCLE-ENUM', '$.lifecycle', `lifecycle must be Preview|GA|Deprecated; got ${svc.lifecycle}`);
  }
  const tiers = Array.isArray(svc.tier) ? svc.tier : [];
  if (tiers.length === 0) {
    add('SERVICE-TIER-EMPTY', '$.tier', 'at least one tier required');
  }
  for (const t of tiers) {
    if (!VALID_TIER.has(t)) add('SERVICE-TIER-ENUM', '$.tier', `unknown tier ${t}`);
  }

  // scenario
  const scen = svc.scenario || {};
  for (const k of ['trigger', 'business_pain']) {
    if (!scen[k]) add('SERVICE-SCENARIO-FIELD', `$.scenario.${k}`, `${k} required`);
  }
  if (!VALID_CADENCE.has(scen.cadence)) {
    add('SERVICE-CADENCE-ENUM', '$.scenario.cadence', `cadence must be continuous|episodic|nightly|on-demand; got ${scen.cadence}`);
  }

  // personas
  const pers = svc.personas || {};
  const primary = Array.isArray(pers.primary) ? pers.primary : [];
  if (primary.length === 0) add('SERVICE-PERSONA-PRIMARY', '$.personas.primary', 'at least one primary persona required');
  if (opts.knownPersonas) {
    for (const group of ['primary', 'secondary', 'consumer']) {
      for (const p of (pers[group] || [])) {
        if (!opts.knownPersonas.has(p)) {
          add('SERVICE-PERSONA-UNKNOWN', `$.personas.${group}`, `unknown persona ${p}`);
        }
      }
    }
  }

  // kpis
  const kpis = Array.isArray(svc.kpis) ? svc.kpis : [];
  if (kpis.length === 0) add('SERVICE-KPIS-EMPTY', '$.kpis', 'at least one KPI required');
  for (const [i, k] of kpis.entries()) {
    const kp = `$.kpis[${i}]`;
    if (!KPI_ID_RE.test(k.id || '')) add('SERVICE-KPI-ID', `${kp}.id`, `kpi id must match ${KPI_ID_RE}; got ${k.id}`);
    if (typeof k.target !== 'number') add('SERVICE-KPI-TARGET', `${kp}.target`, 'target must be a number');
    if (!VALID_DIRECTION.has(k.direction)) add('SERVICE-KPI-DIRECTION', `${kp}.direction`, `direction must be maximize|minimize; got ${k.direction}`);
  }

  // slos
  const s = svc.slos || {};
  if (typeof s.detection_p95_sec === 'number' && typeof s.decision_p95_min === 'number') {
    if (s.detection_p95_sec >= s.decision_p95_min * 60) {
      add('SERVICE-SLO-ORDER', '$.slos', 'detection_p95_sec must be less than decision_p95_min * 60');
    }
  }
  if (typeof s.false_positive_rate === 'number' && (s.false_positive_rate < 0 || s.false_positive_rate > 1)) {
    add('SERVICE-SLO-FPR', '$.slos.false_positive_rate', 'false_positive_rate must be in [0,1]');
  }

  // artifacts
  const a = svc.artifacts || {};
  if (!Array.isArray(a.schemas) || a.schemas.length === 0) add('SERVICE-ARTIFACT-SCHEMAS', '$.artifacts.schemas', 'at least one schema required');
  if (!Array.isArray(a.agents) || a.agents.length === 0) add('SERVICE-ARTIFACT-AGENTS', '$.artifacts.agents', 'at least one agent required');
  if (!ORCH_RE.test(a.orchestration || '')) add('SERVICE-ORCH-PATTERN', '$.artifacts.orchestration', `orchestration must match ORCH-NN; got ${a.orchestration}`);
  if (!VALID_GATE.has(a.hitl_gate)) add('SERVICE-GATE-ENUM', '$.artifacts.hitl_gate', `hitl_gate must be HITL|ACK_ONLY|ZERO_TOUCH|ESCALATION; got ${a.hitl_gate}`);

  // prerequisites
  const pre = svc.prerequisites || {};
  if (!semver.valid(pre.practice_min_version)) {
    add('SERVICE-PRE-MINVER', '$.prerequisites.practice_min_version', `practice_min_version must be semver; got ${pre.practice_min_version}`);
  }

  return { findings };
}
```

**Step 5: Run tests**

Run: `npm test -- apex-core/tools/validate-service-manifest.test.js`
Expected: all 11 tests PASS.

**Step 6: Commit**

```bash
git add apex-core/tools/validate-service-manifest.js apex-core/tools/validate-service-manifest.test.js apex-core/tools/fixtures/valid-service.json
git commit -m "feat(core): add validate-service-manifest with 11 TDD tests

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 1.4: Wire service + persona validation into apex-validate.js

**Files:**
- Modify: `apex-core/tools/apex-validate.js`
- Modify: `apex-core/tools/apex-validate.test.js`

**Step 1: Read apex-validate.js to understand the orchestration entry point**

Run: `cat apex-core/tools/apex-validate.js | head -60`

**Step 2: Extend apex-validate.js**

Add near the top imports:

```javascript
import { validateServiceManifest } from './validate-service-manifest.js';
import { validatePersonaCatalog } from './validate-persona-catalog.js';
```

Add a new CLI sub-mode `--services` that globs `apex-core/fixtures/services/*.json`, loads the persona catalog into a `knownPersonas` Set, and runs `validateServiceManifest` on each, aggregating findings. Pattern after the existing manifest validation block.

**Step 3: Add test coverage**

In `apex-core/tools/apex-validate.test.js` add:

```javascript
test('apex-validate --services runs without errors when fixtures dir exists', async () => {
  // spawn node apex-validate.js --services and assert exit code 0 or documented error
});
```

**Step 4: Run tests**

Run: `npm test`
Expected: all tests PASS.

**Step 5: Commit**

```bash
git add apex-core/tools/apex-validate.js apex-core/tools/apex-validate.test.js
git commit -m "feat(core): apex-validate now runs service + persona validators"
```

---

## Phase 2 — Author 24 Service Manifest Fixtures

All fixtures live in `apex-core/fixtures/services/*.json` and must pass `validate-service-manifest` + persona cross-check. Fixtures are validated in CI via `apex-validate --services`.

### Task 2.1: Scaffold the services fixtures directory + a roundtrip test

**Files:**
- Create: `apex-core/fixtures/services/.gitkeep`
- Create: `apex-core/tools/validate-all-services.test.js`

**Step 1: Write failing test**

Create `apex-core/tools/validate-all-services.test.js`:

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { validateServiceManifest } from './validate-service-manifest.js';
import { validatePersonaCatalog } from './validate-persona-catalog.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const servicesDir = resolve(__dirname, '../fixtures/services');
const catalog = JSON.parse(readFileSync(resolve(__dirname, '../data/persona-catalog.json'), 'utf8'));
const knownPersonas = new Set(catalog.personas.map(p => p.id));

test('every service fixture validates cleanly', () => {
  const files = readdirSync(servicesDir).filter(f => f.endsWith('.json'));
  assert.ok(files.length >= 1, 'expected at least one service fixture');
  for (const f of files) {
    const svc = JSON.parse(readFileSync(resolve(servicesDir, f), 'utf8'));
    const { findings } = validateServiceManifest(svc, { knownPersonas });
    const crits = findings.filter(x => x.severity === 'critical');
    assert.equal(crits.length, 0, `${f}: ${JSON.stringify(crits, null, 2)}`);
  }
});

test('service_ids are unique across the catalog', () => {
  const files = readdirSync(servicesDir).filter(f => f.endsWith('.json'));
  const ids = files.map(f => JSON.parse(readFileSync(resolve(servicesDir, f), 'utf8')).service_id);
  assert.equal(new Set(ids).size, ids.length, 'duplicate service_id detected');
});
```

**Step 2: Add first fixture (RC-CXP-01) so the test can actually pass**

Move the existing `apex-core/tools/fixtures/valid-service.json` to `apex-core/fixtures/services/apex-rc-cxp-01.json` (or copy its content).

**Step 3: Run tests**

Run: `npm test -- apex-core/tools/validate-all-services.test.js`
Expected: PASS (1 fixture, unique id).

**Step 4: Commit**

```bash
git add apex-core/fixtures/services/ apex-core/tools/validate-all-services.test.js
git commit -m "test(core): add services fixture directory with roundtrip validation"
```

---

### Tasks 2.2 – 2.9: RC Practice services (8 fixtures)

Create each fixture file one at a time, run `npm test -- apex-core/tools/validate-all-services.test.js` after each, commit. Each fixture follows the template at `apex-core/tools/fixtures/valid-service.json`.

| Task | File | Service ID | Name |
|---|---|---|---|
| 2.2 | `apex-rc-cxp-01.json` | APEX-RC-CXP-01 | Cold Chain Excursion Response |
| 2.3 | `apex-rc-rvd-02.json` | APEX-RC-RVD-02 | Receiving Variance Dispute |
| 2.4 | `apex-rc-esl-03.json` | APEX-RC-ESL-03 | ESL Pricing Integrity |
| 2.5 | `apex-rc-osa-04.json` | APEX-RC-OSA-04 | Phantom-OOS Detection |
| 2.6 | `apex-rc-rcl-05.json` | APEX-RC-RCL-05 | Recall Response |
| 2.7 | `apex-rc-bpx-06.json` | APEX-RC-BPX-06 | BOPIS Exception Handling |
| 2.8 | `apex-rc-shk-07.json` | APEX-RC-SHK-07 | Shrink & Void Anomaly |
| 2.9 | `apex-rc-cxi-08.json` | APEX-RC-CXI-08 | Customer Incident Triage |

**Workflow per fixture:**
1. Copy the prior fixture as a starting point.
2. Update every field to match the Service Catalog entry (scenario, personas, KPIs, SLOs, artifacts from the existing `apex-rc` agent catalog, orchestration id from `apex-rc-build-spec-v2.md`, HITL gate from the demo).
3. Run `npm test`.
4. Commit: `feat(services): add APEX-RC-<DOM>-<nn> <name>`.

---

### Tasks 2.10 – 2.15: HLS Practice services (6 fixtures)

| Task | File | Service ID | Name |
|---|---|---|---|
| 2.10 | `apex-hls-dsr-01.json` | APEX-HLS-DSR-01 | Discharge Ready Surveillance |
| 2.11 | `apex-hls-sep-02.json` | APEX-HLS-SEP-02 | Sepsis Early Warning |
| 2.12 | `apex-hls-rvc-03.json` | APEX-HLS-RVC-03 | Revenue-Cycle Denial Recovery |
| 2.13 | `apex-hls-sup-04.json` | APEX-HLS-SUP-04 | Supply Expiry Management |
| 2.14 | `apex-hls-ctm-05.json` | APEX-HLS-CTM-05 | Clinical Trial Matching |
| 2.15 | `apex-hls-psi-06.json` | APEX-HLS-PSI-06 | Patient Safety Incident |

Same per-fixture workflow. Personas primarily reference `charge-nurse`, `clinical-informaticist`, `revenue-cycle-analyst`, `supply-chain-pharm`, `trial-coordinator`, `patient-safety-officer`.

---

### Tasks 2.16 – 2.20: ER Practice services (5 fixtures)

| Task | File | Service ID | Name |
|---|---|---|---|
| 2.16 | `apex-er-mtr-01.json` | APEX-ER-MTR-01 | Meter Outage Detection |
| 2.17 | `apex-er-grd-02.json` | APEX-ER-GRD-02 | Grid Anomaly Response |
| 2.18 | `apex-er-bil-03.json` | APEX-ER-BIL-03 | Billing Exception Handling |
| 2.19 | `apex-er-fwo-04.json` | APEX-ER-FWO-04 | Field Work-Order Optimisation |
| 2.20 | `apex-er-reg-05.json` | APEX-ER-REG-05 | Regulatory Event Response |

Personas: `meter-ops-lead`, `grid-ops-engineer`, `billing-ops-analyst`, `field-dispatcher`, `regulatory-affairs`.

---

### Tasks 2.21 – 2.25: AXLE Practice services (5 fixtures)

| Task | File | Service ID | Name |
|---|---|---|---|
| 2.21 | `apex-axle-ldt-01.json` | APEX-AXLE-LDT-01 | Line-Down Triage |
| 2.22 | `apex-axle-qex-02.json` | APEX-AXLE-QEX-02 | Quality Excursion Response |
| 2.23 | `apex-axle-scd-03.json` | APEX-AXLE-SCD-03 | Supply-Chain Disruption |
| 2.24 | `apex-axle-rcl-04.json` | APEX-AXLE-RCL-04 | Recall Traceability |
| 2.25 | `apex-axle-kpi-05.json` | APEX-AXLE-KPI-05 | Plant KPI Drift |

Personas: `plant-supervisor`, `quality-engineer`, `supply-chain-planner`, `plant-manager`, `recall-coordinator`.

**Checkpoint at end of Phase 2:**
- Run: `npm test`
- Expected: 24 fixtures, all passing; `new Set(ids).size === 24`.

---

## Phase 3 — Build Tooling

### Task 3.1: build-service-catalog.cjs — render Companion 07 from fixtures

**Files:**
- Create: `build-service-catalog.cjs`
- Modify: `package.json` (add `"build:catalog"` script)

**Step 1: Scaffold the script**

```javascript
// build-service-catalog.cjs — render dev-guide/07-service-catalog.md from fixtures
const fs = require('fs');
const path = require('path');

const SERVICES_DIR = path.join(__dirname, 'apex-core/fixtures/services');
const PERSONAS_PATH = path.join(__dirname, 'apex-core/data/persona-catalog.json');
const OUTPUT = path.join(__dirname, 'docs/dev-guide/07-service-catalog.md');

const personas = JSON.parse(fs.readFileSync(PERSONAS_PATH, 'utf8'));
const byId = new Map(personas.personas.map(p => [p.id, p.name]));

const fixtures = fs.readdirSync(SERVICES_DIR)
  .filter(f => f.endsWith('.json'))
  .map(f => JSON.parse(fs.readFileSync(path.join(SERVICES_DIR, f), 'utf8')));

const groups = {};
for (const s of fixtures) (groups[s.practice] ||= []).push(s);
for (const k of Object.keys(groups)) groups[k].sort((a, b) => a.service_id.localeCompare(b.service_id));

function renderService(s) {
  const lines = [];
  lines.push(`### ${s.service_id} — ${s.service_name}`, '');
  lines.push(`**Tier:** ${s.tier.join(' / ')}  ·  **Status:** ${s.lifecycle} v${s.version}  ·  **Gate:** ${s.artifacts.hitl_gate}`, '');
  lines.push(`**Scenario.** ${s.scenario.trigger}. _${s.scenario.business_pain}._ Cadence: ${s.scenario.cadence}.`, '');
  const primary = (s.personas.primary || []).map(id => byId.get(id) || id).join(', ');
  const secondary = (s.personas.secondary || []).map(id => byId.get(id) || id).join(', ');
  lines.push(`**Personas.** Primary: ${primary}${secondary ? ` · Secondary: ${secondary}` : ''}`, '');
  lines.push('**KPIs.**');
  for (const k of s.kpis) lines.push(`- \`${k.id}\` — target ${k.target} (${k.direction})`);
  lines.push('', '**SLOs.** ' +
    `detection p95 ≤ ${s.slos.detection_p95_sec}s · ` +
    `decision p95 ≤ ${s.slos.decision_p95_min}min · ` +
    `FPR ≤ ${s.slos.false_positive_rate * 100}% · ` +
    `availability ≥ ${s.slos.availability_pct}%`, '');
  lines.push('**Artifacts.** ' +
    `Schemas: ${s.artifacts.schemas.join(', ')} · ` +
    `Agents: ${s.artifacts.agents.join(', ')} · ` +
    `Orch: ${s.artifacts.orchestration}`, '');
  lines.push('**Prerequisites.** ' +
    `Practice ≥ v${s.prerequisites.practice_min_version} · ` +
    `SORs: ${(s.prerequisites.sor_connections || []).join(', ')} · ` +
    `Capacity: ${s.prerequisites.fabric_capacity}`, '');
  lines.push('');
  return lines.join('\n');
}

const out = [];
out.push('# Companion 07 — Service Catalog', '');
out.push('> Auto-generated from `apex-core/fixtures/services/*.json` by `build-service-catalog.cjs`. Do not edit directly.', '');
for (const practice of ['RC', 'HLS', 'ER', 'AXLE']) {
  if (!groups[practice]) continue;
  out.push(`## ${practice} Practice`, '');
  for (const s of groups[practice]) out.push(renderService(s));
}
fs.writeFileSync(OUTPUT, out.join('\n'));
console.log(`Wrote ${OUTPUT} (${fixtures.length} services)`);
```

**Step 2: Register npm script**

In `package.json` scripts: `"build:catalog": "node build-service-catalog.cjs"`.

**Step 3: Run**

Run: `npm run build:catalog`
Expected: writes `docs/dev-guide/07-service-catalog.md` with all 24 services grouped by Practice.

**Step 4: Commit**

```bash
git add build-service-catalog.cjs package.json docs/dev-guide/07-service-catalog.md
git commit -m "feat(build): render service catalog from fixtures

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

### Task 3.2: Extend build-docx.cjs for the dev guide set

**Files:**
- Modify: `build-docx.cjs` (or duplicate into `build-dev-guide-docx.cjs` if existing script is single-purpose)
- Modify: `package.json` (add `"build:dev-guide"`)

**Step 1: Inspect existing build-docx.cjs** — it currently targets the Solution Overview. Factor shared helpers into a tiny module or duplicate the script. Prefer a new `build-dev-guide-docx.cjs` keyed off a list of 8 source files.

**Step 2: Register script**

`"build:dev-guide": "node build-dev-guide-docx.cjs"` in `package.json`.

**Step 3: Smoke test**

Run: `npm run build:dev-guide`
Expected: 8 `.docx` files written alongside their `.md` sources (spine + 7 companions). Stubs OK if guide content not yet authored.

**Step 4: Commit**

```bash
git add build-dev-guide-docx.cjs package.json
git commit -m "feat(build): add dev-guide docx build script (renders 8 files)"
```

---

## Phase 4 — Author the Guide (Spine + 6 Companions)

Companion 07 is generated in Phase 3; this phase authors the other 7 files. Target page counts per the design doc. Each Markdown file is the single source of truth; `build:dev-guide` renders the .docx.

**Authoring discipline (applies to every guide task):**
- Start each file with the versioning header: `APEX Core v1.2 · Developer Guide v1.0 · 2026-04-18`
- Open with TL;DR section
- Use consistent H2/H3 hierarchy matching the design-doc outline
- Every code example: render Python + C# side-by-side using a 2-column Markdown table or alternating fenced-code blocks with language headings
- Mermaid diagrams for architecture; tables for matrices
- Cross-reference terms back to the spine glossary via relative anchors (`[term](../APEX-developer-guide.md#glossary-term)`)

### Task 4.1: Spine — `docs/APEX-developer-guide.md`

**File:** Create `docs/APEX-developer-guide.md` using the 8-section outline from the design doc §5. Target 18–22 pages.

**Completion checklist:**
- [ ] §1 Executive TL;DR written (1–2 pp)
- [ ] §2 Fabric layering overview with one Mermaid architecture diagram (3–4 pp)
- [ ] §3 Developer mental model: L1→L4 layers + five lanes (2–3 pp)
- [ ] §4 Repo & workspace layout (2–3 pp)
- [ ] §5 7-step developer workflow (2 pp)
- [ ] §6 Service-first view (1–2 pp)
- [ ] §7 Guide to the companions — table of contents with use-cases (1–2 pp)
- [ ] §8 Glossary — all terms defined once (2–3 pp)
- [ ] Render: `npm run build:dev-guide` produces `docs/APEX-developer-guide.docx`

**Commit:** `docs(dev-guide): author spine (APEX-developer-guide.md)`.

### Task 4.2: Companion 01 — Fabric Layering

**File:** Create `docs/dev-guide/01-fabric-layering.md` per design-doc §6.1.

**Code examples required (Python + C# side-by-side):**
- Provisioning a Fabric workspace via Fabric REST API + managed identity
- Creating a OneLake shortcut to an L3 Practice canonical Silver table
- Reading a Silver table from a notebook (PySpark) vs from an Azure Function (C# .NET 8)

**Mermaid required:**
- End-to-end Fabric + APEX component map (OneLake / Lakehouse / Eventstream / Agent Service / Logic Apps / Teams)
- Workspace topology diagram (Dev/Test/Prod × L3 Practice / L4 Tenant)

**Worked example:** Stand up a new L4 tenant workspace — scripted end-to-end.

**Commit:** `docs(dev-guide): author companion 01 Fabric layering`.

### Task 4.3: Companion 02 — Medallion + SOR Integration

**File:** Create `docs/dev-guide/02-medallion-sor.md` per design-doc §6.2.

**Code examples required:**
- Bronze DDL for a delta table (SQL)
- Silver transform notebook (PySpark) + equivalent using Azure Data Factory + C# Custom Activity for comparison
- Gold feature view (T-SQL)
- PII tokenisation snippet with Fabric native masking + Purview label application (Python + C#)
- Running `apex-validate` + `classify-bump` in CI (YAML + shell)

**Worked examples required:**
- RC: Manhattan WMS → MERML.STORE_INVENTORY_POSITION (batch pipeline)
- HLS: Epic EHR → HLSCML.PATIENT_ENCOUNTER (CDC mirrored DB + PHI tokenisation)
- ER: SAP ISU → ERCML.METER_READING (batch)
- AXLE: Plex MES → AXLECML.PRODUCTION_EVENT (eventstream)

**SOR → Service matrix:** Table mapping each SOR connection to the service_ids that depend on it (read from fixtures to keep accurate).

**Commit:** `docs(dev-guide): author companion 02 Medallion + SOR`.

### Task 4.4: Companion 03 — MCP Servers & Tooling

**File:** Create `docs/dev-guide/03-mcp-servers.md` per design-doc §6.3.

**Code examples required:**
- Minimal FastMCP server in Python (exports 1 tool + 1 resource + auth) alongside
- Equivalent C# server using .NET MCP SDK with identical tool contract
- Tool schema definition (input/output types, error model) in both
- Auth wiring: managed identity for Fabric data access (Python + C#)
- Local-dev: MCP Inspector config + VS Code launch.json for stdio debugging

**Mermaid required:**
- MCP protocol sequence diagram (client ↔ server ↔ Fabric)
- MCP server taxonomy (domain servers, utility servers, Fabric-MCP, external-MCP)

**Worked example:** Build `fetch_cold_chain_telemetry(since, store_id)` end-to-end in both languages — author tool → wire to Silver table → register with Azure AI Agent Service → invoke from a live agent session via MCP Inspector.

**Commit:** `docs(dev-guide): author companion 03 MCP servers`.

### Task 4.5: Companion 04 — Agent & Orchestration Lifecycle + HITL

**File:** Create `docs/dev-guide/04-agent-lifecycle.md` per design-doc §6.4.

**Code examples required:**
- Agent manifest JSON (schemas, MCP tools, HITL gate wiring)
- Logic Apps ARM/Bicep definition for ORCH-03 (Cold Chain) declarative DAG
- Equivalent Durable Function orchestration in C# and Python (functions-python) with identical contract
- Teams approval card adaptive-card JSON + handler (Python + C#)
- Pre-commit hook script running `apex-validate` + `classify-bump`
- Azure DevOps YAML pipeline stub for canary (5% for 72h) + rollback

**Mermaid required:**
- Agent lifecycle state diagram (draft → test → canary → GA → deprecated)
- SemVer bump → gate kind decision tree

**Service impact section:** cross-reference from an agent_id back to the service_ids shipping it (generated from fixtures).

**Commit:** `docs(dev-guide): author companion 04 agent lifecycle + HITL`.

### Task 4.6: Companion 05 — Observability & Security

**File:** Create `docs/dev-guide/05-observability-security.md` per design-doc §6.5.

**Code examples required:**
- App Insights / OpenTelemetry instrumentation for an agent invocation (Python + C#)
- Azure Monitor workbook JSON for APEX dashboard
- KQL queries for the top 5 KPIs (success rate, MTTD, HITL queue depth, schema drift, MCP failure rate)
- Managed identity wiring — Agent Service → OneLake (Python + C#)
- Purview label application during Silver tokenisation (Python + C#)
- Right-to-erasure re-tokenisation + replay script skeleton

**Compliance matrix:** Table mapping Practice → applicable regimes (HIPAA / SOX / PCI / GDPR) → required controls.

**Commit:** `docs(dev-guide): author companion 05 observability & security`.

### Task 4.7: Companion 06 — Testing & Environment Topology

**File:** Create `docs/dev-guide/06-testing-topology.md` per design-doc §6.6.

**Code examples required:**
- Test-pyramid scaffolding: unit / contract / integration / e2e / synthetic-load examples (Python `pytest` + C# `xUnit`)
- MCP-server mock pattern (Python + C#)
- Fixture-recording script: capture real SOR payload → anonymise → save to `fixtures/sor/`
- Fabric workspace topology diagram
- Bash/PowerShell runbooks: "Deploy new agent version to one tenant", "Re-bake Gold after MINOR bump", "Rollback failed orch change"

**L3 → L4 binding explainer:** How a tenant pins a specific Practice release; tenant-scoped overrides without forking; drift detection logic.

**Commit:** `docs(dev-guide): author companion 06 testing & topology`.

### Task 4.8: Render all 8 docs to Word

Run: `npm run build:catalog && npm run build:dev-guide`
Expected: 8 `.docx` files exist under `docs/` and `docs/dev-guide/`.

**Commit:** `docs(dev-guide): render full Word doc set`.

---

## Phase 5 — Migration: Update existing artifacts to Practice terminology

The new guide ships with the Practice terminology; Phase 5 reconciles the **existing** APEX artifacts so the whole framework is consistent.

### Task 5.1: Inventory existing "fleet" references

**Step 1:** Run: `grep -ril "fleet" "C:\Stage\Clients\Industries\APEX" --include="*.md" --include="*.json" | head -60`

**Step 2:** Save the grep output to `docs/plans/fleet-rename-inventory.txt` (gitignored working file).

**Step 3:** Group the hits into 4 buckets:
1. **Normative code** — `apex-core/tools/*.js`, `apex-core/data/*.json` (handled by Phase 0 shim; nothing further in Phase 5)
2. **Build specs** — `apex-core-*.md`, `apex-<practice>-build-spec*.md`
3. **Existing docs** — `docs/APEX-solution-overview.md`, `docs/APEX-Store-100-facilitator-guide.md`
4. **Changelog/README**

(No commit — this is a survey step.)

### Task 5.2: Rename build specs (code + docs)

**Files (expected):**
- `apex-core-build-spec.md` · `apex-core-v1.1-amendment.md` · `apex-core-v1.2-amendment.md`
- `apex-rc-build-spec-v2.md` · `apex-hls-build-spec.md` · `apex-er-build-spec.md` · `apex-ice-build-spec.md` · `apex-th-build-spec.md` · `apex-tmt-build-spec.md`

**Step 1:** For each file, replace "Fleet" (capitalised) → "Practice" and "fleet" (lowercase) → "practice" **only in narrative text**. Preserve legacy terms where they appear in code snippets referencing the old identifier (call them out with a "deprecated alias" footnote).

**Step 2:** After each file, verify the rendered markdown still reads cleanly (no accidental "Practice" in proper nouns like "fleet management vehicle", if such a phrase exists).

**Step 3:** Commit each file separately: `docs(<practice>): rename fleet → practice terminology`.

### Task 5.3: Rename the `apex-fleet/` directory

**Step 1:** `git mv apex-fleet apex-practice`
**Step 2:** Update any file references (`find . -type f -name "*.js" -o -name "*.md" -o -name "*.json" | xargs grep -l "apex-fleet"`) and replace paths with `apex-practice`.
**Step 3:** Run: `npm test` — expected: all tests pass (the rename must not break validate-practice's fixture resolution).
**Step 4:** Commit: `refactor(core): rename apex-fleet directory to apex-practice`.

### Task 5.4: Update existing Word-rendered docs

**Step 1:** For each of `docs/APEX-solution-overview.md`, `docs/APEX-Store-100-facilitator-guide.md`, `docs/APEX-RC-agent-catalog.docx` (source .cjs):
   - Update terminology in the source `.md` / `.cjs`
   - Re-render to `.docx`
**Step 2:** Commit: `docs: update existing deliverables to Practice terminology + rerender`.

### Task 5.5: CHANGELOG entry + README

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `README.md`

**Step 1:** Add a CHANGELOG entry:

```markdown
## [1.2.1] - 2026-04-18

### Changed (MINOR)
- **L3 layer renamed from "Fleet" to "Practice"** across APEX Core docs, build specs, and tooling.
  Captures the full scope of L3 (schemas + agents + MCP tools + orchestrations + gates + services + personas + KPIs).
  `validate-fleet.js` is retained as a backward-compatible shim (removal scheduled v1.3).

### Added
- **Developer Implementation Guide v1.0** — spine + 7 companions at `docs/APEX-developer-guide.md` and `docs/dev-guide/`.
- **Service Catalog** — 24 subscribable services across RC/HLS/ER/AXLE Practices with full manifest validation.
- **Persona catalog** — 22 personas at `apex-core/data/persona-catalog.json`.
- **New validators:** `validate-practice.js`, `validate-service-manifest.js`, `validate-persona-catalog.js`.
- **New build scripts:** `build-service-catalog.cjs`, `build-dev-guide-docx.cjs`.
```

**Step 2:** Update `README.md` to mention the new Developer Guide, the Service Catalog, and the Fleet→Practice rename.

**Step 3:** Commit: `docs: CHANGELOG + README for Developer Guide v1.0 and Fleet→Practice rename`.

---

## Phase 6 — Final Validation

### Task 6.1: Full test suite

Run: `npm test`
Expected: all passing; no warnings; coverage includes validate-practice, validate-service-manifest, validate-persona-catalog, validate-all-services.

### Task 6.2: Render all documents

Run: `npm run build:catalog && npm run build:dev-guide`
Expected: 8 `.docx` files present and non-empty; `07-service-catalog.md` reflects all 24 fixtures.

### Task 6.3: Cross-reference audit

**Step 1:** Manually spot-check that spine glossary terms (L1/L2/L3/L4, Practice, Service, MCP, HITL, SCD2) are linked-to from companions.

**Step 2:** Verify no companion references a schema_id / agent_id / orch_id that isn't present in the corresponding practice's build spec.

**Step 3:** Verify the SOR→Service matrix in companion 02 matches the actual `prerequisites.sor_connections` across fixtures.

### Task 6.4: Deprecation notice in `apex-fleet` shim

**Step 1:** Add a console.warn at the top of `validate-fleet.js` that fires on import:

```javascript
// eslint-disable-next-line no-console
if (!globalThis.__apexFleetShimWarned) {
  console.warn('[apex-core] validate-fleet.js is deprecated. Use validate-practice.js. Shim removal: Core v1.3.');
  globalThis.__apexFleetShimWarned = true;
}
```

**Step 2:** Run: `npm test`
Expected: warning emitted once, tests pass.

**Step 3:** Commit: `chore(core): add one-shot deprecation warning to validate-fleet shim`.

### Task 6.5: Merge commit / final tag

**Step 1:** Run: `git log --oneline` and verify the linear commit history is clean (one logical change per commit).

**Step 2:** Tag: `git tag -a v1.2.1 -m "Developer Implementation Guide v1.0 + Fleet→Practice rename"`.

**Step 3:** Push when the user approves: `git push origin main --tags`.

---

## Appendix A — Test running cheatsheet

| What | Command |
|---|---|
| All tests | `npm test` |
| Single file | `npm test -- apex-core/tools/validate-service-manifest.test.js` |
| Specific test | `node --test --test-name-pattern "valid service" apex-core/tools/validate-service-manifest.test.js` |
| Validate all service fixtures | `node apex-core/tools/apex-validate.js --services` |
| Render catalog | `npm run build:catalog` |
| Render dev-guide .docx | `npm run build:dev-guide` |

## Appendix B — Commit message prefixes (conventional)

- `feat(core):` — new APEX Core functionality
- `feat(build):` — new build/render tooling
- `feat(services):` — new service fixture
- `docs(dev-guide):` — new/changed developer-guide content
- `docs(<practice>):` — existing practice docs touched by rename
- `test(core):` — tests only
- `refactor(core):` — internal refactor, no behaviour change
- `chore(core):` — housekeeping, shim deprecations, version bumps

## Appendix C — "When in doubt" escalations

- **Ambiguous service KPI target value?** Leave the task pending and ask for guidance before committing a fabricated number.
- **Rename hits a business-spec bullet that quotes the old term deliberately?** Preserve the quote and add a `[since Core v1.2.1: Practice]` bracketed annotation.
- **A test fails intermittently?** Stop, use `superpowers:systematic-debugging`, fix root cause before continuing the plan.
