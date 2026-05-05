# APEX Schema Versioning Manifest Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implement the four-layer schema-versioning manifest system (L1 contract, L2 edition, L3 fleet, L4 tenant) plus the `apex-validate` visual tool and `apex-sync` CLI, landing as APEX Core v1.2.

**Architecture:** Node.js (ESM, no transpile) tooling in `apex-core/tools/`. Manifest files are plain JSON. Validator is a single binary with author + fleet modes that emit `report.html` (self-contained, APEX design-system styled) and `report.json`. Tenant sync is a thin CLI that pulls pinned manifests, classifies SemVer bumps, and applies DDL via a pluggable driver. GitOps-style pull distribution — no Kubernetes, no push.

**Tech Stack:** Node.js ≥20, ESM modules, `node:test` (built-in test runner), `semver` (industry standard SemVer parsing), zero other runtime deps. Hand-rolled JSON contract validator to avoid `ajv` bloat. Vanilla HTML/CSS/JS for reports using Core Part 9 design tokens.

**Design doc:** `docs/plans/2026-04-17-schema-versioning-manifest-design.md` (read first).

**Execution notes:**
- Project is currently a greenfield directory with build-spec `.md` files. Phase 0 scaffolds the repo.
- Git is not initialized. Task 1 initializes it. Every task ends with a commit so progress is reviewable.
- On Windows paths use forward slashes in config/code, native backslashes when the user copies commands to PowerShell.

---

## Phase 0 — Scaffold

### Task 1: Initialize repo & package.json

**Files:**
- Create: `.gitignore`
- Create: `package.json`
- Create: `README.md` (minimal, one-paragraph pointer to the build specs)

**Step 1: Init git and set ignore**

Run: `git init && git branch -m main`

Create `.gitignore`:
```
node_modules/
*.log
.DS_Store
/apex-core/tools/coverage/
/apex-fleet/bundles/
report.html
report.json
fleet-report.html
fleet-report.json
```

**Step 2: Write `package.json`**

```json
{
  "name": "apex",
  "version": "1.2.0-dev",
  "private": true,
  "type": "module",
  "engines": { "node": ">=20" },
  "scripts": {
    "test": "node --test apex-core/tools/**/*.test.js",
    "validate": "node apex-core/tools/apex-validate.js",
    "sync": "node apex-core/tools/apex-sync.js"
  },
  "dependencies": {
    "semver": "^7.6.0"
  }
}
```

**Step 3: Install deps & verify**

Run: `npm install`
Expected: `semver` installs, no errors.
Run: `node --version` → expect `v20.x` or higher.

**Step 4: Commit**

```bash
git add .gitignore package.json package-lock.json README.md
git commit -m "chore: scaffold APEX repo with package.json and .gitignore"
```

---

### Task 2: Create Core folder structure

**Files:**
- Create: `apex-core/data/.gitkeep`
- Create: `apex-core/conventions/.gitkeep`
- Create: `apex-core/tools/.gitkeep`
- Create: `apex-core/tools/fixtures/.gitkeep`

**Step 1: Create folders**

Run (bash):
```bash
mkdir -p apex-core/data apex-core/conventions apex-core/tools/fixtures apex-fleet/data apex-fleet/tools
touch apex-core/data/.gitkeep apex-core/conventions/.gitkeep apex-core/tools/.gitkeep apex-core/tools/fixtures/.gitkeep apex-fleet/data/.gitkeep apex-fleet/tools/.gitkeep
```

**Step 2: Commit**

```bash
git add apex-core/ apex-fleet/
git commit -m "chore: create apex-core and apex-fleet folder structure"
```

---

## Phase 1 — Contract & Conventions

### Task 3: Write L1 contract JSON

**Files:**
- Create: `apex-core/data/schema-manifest-contract.json`
- Create: `apex-core/tools/contract.test.js`

**Step 1: Write the failing test**

`apex-core/tools/contract.test.js`:
```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CONTRACT_PATH = resolve(__dirname, '../data/schema-manifest-contract.json');

test('L1 contract loads as valid JSON', () => {
  const raw = readFileSync(CONTRACT_PATH, 'utf8');
  const parsed = JSON.parse(raw);
  assert.ok(parsed);
});

test('L1 contract declares contract_version and core_version', () => {
  const contract = JSON.parse(readFileSync(CONTRACT_PATH, 'utf8'));
  assert.equal(contract.contract_version, '1.0');
  assert.equal(contract.core_version, '1.2');
});

test('L1 contract declares required top-level fields', () => {
  const contract = JSON.parse(readFileSync(CONTRACT_PATH, 'utf8'));
  const required = contract.required_fields;
  assert.ok(required.edition_code);
  assert.ok(required.core_version_required);
  assert.ok(required.manifest_version);
  assert.ok(required.schemas);
  assert.equal(required.schemas.min_items, 3);
  assert.equal(required.schemas.max_items, 5);
});

test('L1 contract defines schema_entry with version + changelog', () => {
  const contract = JSON.parse(readFileSync(CONTRACT_PATH, 'utf8'));
  assert.ok(contract.schema_entry.version);
  assert.ok(contract.schema_entry.changelog);
  assert.ok(contract.schema_entry.envelope_required);
});

test('L1 contract defines change_delta op enum with 9 values', () => {
  const contract = JSON.parse(readFileSync(CONTRACT_PATH, 'utf8'));
  const ops = contract.change_delta.op.values;
  assert.equal(ops.length, 9);
  assert.ok(ops.includes('add_entity'));
  assert.ok(ops.includes('remove_entity'));
  assert.ok(ops.includes('rename_entity'));
  assert.ok(ops.includes('add_column'));
  assert.ok(ops.includes('remove_column'));
  assert.ok(ops.includes('change_type'));
  assert.ok(ops.includes('change_pk'));
  assert.ok(ops.includes('change_grain'));
  assert.ok(ops.includes('metadata'));
});
```

**Step 2: Run test to verify it fails**

Run: `npm test`
Expected: FAIL, `ENOENT: no such file or directory, open ...schema-manifest-contract.json`.

**Step 3: Write the contract**

`apex-core/data/schema-manifest-contract.json` — copy the JSON from Part 3.1 of the design doc verbatim. (See `docs/plans/2026-04-17-schema-versioning-manifest-design.md` section 3.1 for the full content.)

**Step 4: Run test to verify it passes**

Run: `npm test`
Expected: PASS (5 tests).

**Step 5: Commit**

```bash
git add apex-core/data/schema-manifest-contract.json apex-core/tools/contract.test.js
git commit -m "feat(core): add L1 schema-manifest-contract v1.0"
```

---

### Task 4: Write convention doc & v1.2 amendment

**Files:**
- Create: `apex-core/conventions/schema-versioning.md`
- Create: `apex-core-v1.2-amendment.md` (top-level, matching v1.1 precedent)
- Modify: `apex-core/CHANGELOG.md` (create)

**Step 1: Write the convention doc**

`apex-core/conventions/schema-versioning.md` — one page. Sections:
- Purpose (one paragraph)
- The four layers (pointer table to L1/L2/L3/L4 files)
- SemVer rules (copy Part 4 decision table from design doc verbatim)
- Anti-cheating rules (copy Part 4.2 from design doc)
- Pointer to `apex-core-v1.2-amendment.md` and the design doc

**Step 2: Write the v1.2 amendment**

`apex-core-v1.2-amendment.md` — follow the structure of `apex-core-v1.1-amendment.md` (read it for the pattern). Sections:
- Rationale (copy Part 1 of design doc)
- New Part 11 acceptance criteria additions (the three bullets from Part 9 of design doc)
- New Core tools introduced (`apex-validate`, `apex-sync`)
- Downstream spec updates required (one-line Part 0 bump on each active edition spec)
- Handoff notes

**Step 3: Write initial CHANGELOG entry**

`apex-core/CHANGELOG.md`:
```markdown
# APEX Core Changelog

## v1.2 — 2026-04-17

- Added L1 schema-manifest-contract.json defining four-layer schema versioning.
- Extended Part 11 acceptance criteria with three manifest-related checks.
- Introduced apex-validate (dual-mode validator with HTML reports) and apex-sync (tenant-side CLI) as Core tools.
- No existing edition content invalidated; adoption is additive.

## v1.1 — (prior)

- Formal edition registry (apex-core/data/edition-registry.json).
- Edition-split policy formalized.
```

**Step 4: Commit**

```bash
git add apex-core/conventions/schema-versioning.md apex-core-v1.2-amendment.md apex-core/CHANGELOG.md
git commit -m "docs(core): add schema-versioning convention, v1.2 amendment, CHANGELOG"
```

---

## Phase 2 — Validator Core

### Task 5: Implement SemVer bump classifier — PATCH cases

**Files:**
- Create: `apex-core/tools/classify-bump.js`
- Create: `apex-core/tools/classify-bump.test.js`

**Step 1: Write the failing test**

`apex-core/tools/classify-bump.test.js`:
```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { classifyBump } from './classify-bump.js';

test('metadata-only change is PATCH', () => {
  const changes = [
    { op: 'metadata', target: 'schema', detail: 'description clarified' }
  ];
  assert.equal(classifyBump(changes), 'PATCH');
});

test('multiple metadata ops still PATCH', () => {
  const changes = [
    { op: 'metadata', target: 'STORE_INVENTORY_POSITION', detail: 'PII class refined' },
    { op: 'metadata', target: 'schema', detail: 'comment updated' }
  ];
  assert.equal(classifyBump(changes), 'PATCH');
});

test('empty change list throws', () => {
  assert.throws(() => classifyBump([]), /no changes/i);
});
```

**Step 2: Run test to verify it fails**

Run: `npm test`
Expected: FAIL, cannot find module `./classify-bump.js`.

**Step 3: Implement minimal classifier**

`apex-core/tools/classify-bump.js`:
```javascript
const MAJOR_OPS = new Set([
  'remove_entity', 'rename_entity', 'remove_column',
  'change_type', 'change_pk', 'change_grain'
]);
const MINOR_OPS = new Set(['add_entity', 'add_column']);
const PATCH_OPS = new Set(['metadata']);

/**
 * @param {Array<{op: string, target: string, detail: string}>} changes
 * @returns {'MAJOR' | 'MINOR' | 'PATCH'}
 */
export function classifyBump(changes) {
  if (!changes || changes.length === 0) {
    throw new Error('classifyBump: no changes provided');
  }
  let level = 'PATCH';
  for (const c of changes) {
    if (MAJOR_OPS.has(c.op)) return 'MAJOR';
    if (MINOR_OPS.has(c.op)) level = 'MINOR';
  }
  return level;
}
```

**Step 4: Run test to verify it passes**

Run: `npm test`
Expected: PASS (3 new tests).

**Step 5: Commit**

```bash
git add apex-core/tools/classify-bump.js apex-core/tools/classify-bump.test.js
git commit -m "feat(validator): classify-bump PATCH cases"
```

---

### Task 6: Extend classifier for MINOR + MAJOR + anti-cheating rules

**Files:**
- Modify: `apex-core/tools/classify-bump.js`
- Modify: `apex-core/tools/classify-bump.test.js`

**Step 1: Write the failing tests**

Append to `classify-bump.test.js`:
```javascript
test('add_entity is MINOR', () => {
  assert.equal(
    classifyBump([{ op: 'add_entity', target: 'NEW_ENTITY', detail: 'Silver' }]),
    'MINOR'
  );
});

test('nullable add_column is MINOR', () => {
  assert.equal(
    classifyBump([{ op: 'add_column', target: 'T.col', detail: 'INT NULL' }]),
    'MINOR'
  );
});

test('non-nullable add_column is MAJOR (anti-cheat rule 1)', () => {
  assert.equal(
    classifyBump([{ op: 'add_column', target: 'T.col', detail: 'INT NOT NULL' }]),
    'MAJOR'
  );
});

test('remove_entity is MAJOR', () => {
  assert.equal(classifyBump([{ op: 'remove_entity', target: 'OLD' }]), 'MAJOR');
});

test('rename_entity is MAJOR (anti-cheat rule 2)', () => {
  assert.equal(classifyBump([{ op: 'rename_entity', target: 'OLD>NEW' }]), 'MAJOR');
});

test('change_grain is MAJOR (anti-cheat rule 3)', () => {
  assert.equal(classifyBump([{ op: 'change_grain', target: 'T' }]), 'MAJOR');
});

test('mixed changes take the highest severity', () => {
  const changes = [
    { op: 'metadata', target: 'schema', detail: 'x' },
    { op: 'add_entity', target: 'A', detail: 'y' },
    { op: 'remove_column', target: 'T.col', detail: 'z' }
  ];
  assert.equal(classifyBump(changes), 'MAJOR');
});
```

**Step 2: Run tests to verify new ones fail**

Run: `npm test`
Expected: the non-nullable add_column test fails (currently returns MINOR).

**Step 3: Implement the nullable check**

Modify `classifyBump` to inspect `add_column` details:
```javascript
export function classifyBump(changes) {
  if (!changes || changes.length === 0) {
    throw new Error('classifyBump: no changes provided');
  }
  let level = 'PATCH';
  for (const c of changes) {
    if (MAJOR_OPS.has(c.op)) return 'MAJOR';
    if (c.op === 'add_column') {
      // Anti-cheat rule 1: non-nullable additions are MAJOR.
      if (isNonNullable(c.detail)) return 'MAJOR';
      level = 'MINOR';
    } else if (MINOR_OPS.has(c.op)) {
      level = 'MINOR';
    }
  }
  return level;
}

function isNonNullable(detail = '') {
  return /\bNOT\s+NULL\b/i.test(detail);
}
```

**Step 4: Run tests**

Run: `npm test`
Expected: all 10 tests pass.

**Step 5: Commit**

```bash
git add apex-core/tools/classify-bump.js apex-core/tools/classify-bump.test.js
git commit -m "feat(validator): classify MINOR/MAJOR with anti-cheating rules"
```

---

### Task 7: Implement L2 manifest validator

**Files:**
- Create: `apex-core/tools/validate-manifest.js`
- Create: `apex-core/tools/validate-manifest.test.js`
- Create: `apex-core/tools/fixtures/valid-rc.manifest.json`
- Create: `apex-core/tools/fixtures/invalid-bump.manifest.json`

**Step 1: Create the fixtures**

`apex-core/tools/fixtures/valid-rc.manifest.json` — minimal RC manifest with two schemas (MERML, SCML), each with a valid changelog entry and matching entities. Copy shape from Part 3.2 of design doc, trim to essentials.

`apex-core/tools/fixtures/invalid-bump.manifest.json` — same shape but declares `bump: "MINOR"` on a changelog entry whose `changes` include `remove_entity`. This should fail validation.

**Step 2: Write failing tests**

`apex-core/tools/validate-manifest.test.js`:
```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { validateManifest } from './validate-manifest.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const loadFixture = (name) =>
  JSON.parse(readFileSync(resolve(__dirname, 'fixtures', name), 'utf8'));

test('valid RC manifest returns no critical findings', () => {
  const result = validateManifest(loadFixture('valid-rc.manifest.json'));
  const criticals = result.findings.filter((f) => f.severity === 'critical');
  assert.equal(criticals.length, 0, JSON.stringify(criticals, null, 2));
});

test('manifest missing edition_code is critical', () => {
  const m = loadFixture('valid-rc.manifest.json');
  delete m.edition_code;
  const result = validateManifest(m);
  assert.ok(result.findings.some((f) => f.severity === 'critical' && f.rule === 'REQ-01'));
});

test('declared MINOR bump with a remove_entity change is critical', () => {
  const result = validateManifest(loadFixture('invalid-bump.manifest.json'));
  const criticals = result.findings.filter((f) => f.severity === 'critical');
  assert.ok(criticals.some((f) => f.rule === 'BUMP-MISMATCH'));
});

test('every entity with primary_key references at least 1 column', () => {
  const m = loadFixture('valid-rc.manifest.json');
  m.schemas[0].entities[0].primary_key = [];
  const result = validateManifest(m);
  assert.ok(result.findings.some((f) => f.rule === 'PK-EMPTY'));
});

test('schema version mismatches latest changelog entry is critical', () => {
  const m = loadFixture('valid-rc.manifest.json');
  m.schemas[0].version = '9.9.9';
  const result = validateManifest(m);
  assert.ok(result.findings.some((f) => f.rule === 'VERSION-CHANGELOG-MISMATCH'));
});
```

**Step 3: Run tests to verify they fail**

Run: `npm test`
Expected: FAIL, cannot find `./validate-manifest.js`.

**Step 4: Implement `validate-manifest.js`**

```javascript
import semver from 'semver';
import { classifyBump } from './classify-bump.js';

const EDITION_CODE_RE = /^[A-Z]{2,3}$/;
const SCHEMA_CODE_RE = /^[A-Z]{4,5}(ML|L)$/;

/**
 * @param {object} manifest
 * @returns {{ findings: Array<{severity: string, rule: string, path: string, message: string}> }}
 */
export function validateManifest(manifest) {
  const findings = [];

  // REQ-01 through REQ-04: top-level required fields
  for (const [field, rule] of [
    ['edition_code', 'REQ-01'],
    ['core_version_required', 'REQ-02'],
    ['manifest_version', 'REQ-03'],
    ['schemas', 'REQ-04']
  ]) {
    if (!manifest[field]) {
      findings.push({ severity: 'critical', rule, path: `$.${field}`, message: `missing required field ${field}` });
    }
  }

  if (manifest.edition_code && !EDITION_CODE_RE.test(manifest.edition_code)) {
    findings.push({ severity: 'critical', rule: 'REQ-01-PATTERN', path: '$.edition_code', message: 'edition_code must match /^[A-Z]{2,3}$/' });
  }

  if (manifest.manifest_version && !semver.valid(manifest.manifest_version)) {
    findings.push({ severity: 'critical', rule: 'REQ-03-SEMVER', path: '$.manifest_version', message: 'manifest_version must be valid SemVer' });
  }

  const schemas = manifest.schemas ?? [];
  if (schemas.length < 3 || schemas.length > 5) {
    findings.push({ severity: 'critical', rule: 'REQ-04-COUNT', path: '$.schemas', message: `expected 3–5 schemas, got ${schemas.length}` });
  }

  for (const [i, s] of schemas.entries()) {
    const sPath = `$.schemas[${i}]`;
    if (!SCHEMA_CODE_RE.test(s.code || '')) {
      findings.push({ severity: 'critical', rule: 'SCHEMA-CODE', path: sPath + '.code', message: `invalid schema code ${s.code}` });
    }
    if (!semver.valid(s.version)) {
      findings.push({ severity: 'critical', rule: 'SCHEMA-VERSION', path: sPath + '.version', message: 'version must be valid SemVer' });
    }

    // entity checks
    for (const [j, e] of (s.entities || []).entries()) {
      const ePath = `${sPath}.entities[${j}]`;
      if (!e.primary_key || e.primary_key.length === 0) {
        findings.push({ severity: 'critical', rule: 'PK-EMPTY', path: ePath + '.primary_key', message: 'primary_key must have ≥1 column' });
      }
      if (!e.grain) {
        findings.push({ severity: 'critical', rule: 'GRAIN-MISSING', path: ePath + '.grain', message: 'grain is required' });
      }
    }

    // changelog checks
    const changelog = s.changelog || [];
    if (changelog.length > 0) {
      const latest = changelog[0];
      if (latest.version !== s.version) {
        findings.push({
          severity: 'critical', rule: 'VERSION-CHANGELOG-MISMATCH',
          path: sPath + '.version',
          message: `schema.version (${s.version}) must match first changelog entry (${latest.version})`
        });
      }
      for (const [k, entry] of changelog.entries()) {
        const cPath = `${sPath}.changelog[${k}]`;
        const computed = classifyBump(entry.changes || []);
        if (entry.bump !== computed) {
          findings.push({
            severity: 'critical', rule: 'BUMP-MISMATCH', path: cPath + '.bump',
            message: `declared ${entry.bump} but changes compute to ${computed}`
          });
        }
      }
    }
  }

  return { findings };
}
```

**Step 5: Run tests**

Run: `npm test`
Expected: all validate-manifest tests pass.

**Step 6: Commit**

```bash
git add apex-core/tools/validate-manifest.js apex-core/tools/validate-manifest.test.js apex-core/tools/fixtures/
git commit -m "feat(validator): L2 manifest validator with BUMP-MISMATCH and PK rules"
```

---

### Task 8: Implement `apex-validate` CLI (author mode) with JSON report

**Files:**
- Create: `apex-core/tools/apex-validate.js`
- Create: `apex-core/tools/report.js`
- Create: `apex-core/tools/apex-validate.test.js`
- Create: `apex-rc/data/schemas.manifest.json` (test fixture; real content in Task 11)

**Step 1: Seed a minimal apex-rc manifest**

`apex-rc/data/schemas.manifest.json` — copy `apex-core/tools/fixtures/valid-rc.manifest.json` content. This is the first real edition manifest; we'll replace with full content in Task 11.

**Step 2: Write failing tests**

`apex-core/tools/apex-validate.test.js`:
```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execSync } from 'node:child_process';
import { readFileSync, existsSync, unlinkSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CLI = resolve(__dirname, 'apex-validate.js');
const EDITION = resolve(__dirname, '../../apex-rc');

test('apex-validate <edition> exits 0 for valid edition and writes report.json', () => {
  const reportPath = resolve(EDITION, 'data/report.json');
  if (existsSync(reportPath)) unlinkSync(reportPath);
  execSync(`node "${CLI}" "${EDITION}"`, { stdio: 'pipe' });
  assert.ok(existsSync(reportPath));
  const report = JSON.parse(readFileSync(reportPath, 'utf8'));
  assert.equal(report.status, 'pass');
});

test('apex-validate --ci emits machine-readable stdout', () => {
  const stdout = execSync(`node "${CLI}" --ci "${EDITION}"`, { encoding: 'utf8' });
  const parsed = JSON.parse(stdout);
  assert.ok(parsed.summary);
  assert.equal(typeof parsed.summary.critical, 'number');
});
```

**Step 3: Run tests to verify failure**

Run: `npm test`
Expected: FAIL, CLI missing.

**Step 4: Implement the CLI and JSON report**

`apex-core/tools/report.js`:
```javascript
export function buildReport({ editionCode, editionFolder, manifestPath, findings }) {
  const bySeverity = { critical: 0, warning: 0, info: 0 };
  for (const f of findings) bySeverity[f.severity] = (bySeverity[f.severity] ?? 0) + 1;
  const status = bySeverity.critical > 0 ? 'fail' : (bySeverity.warning > 0 ? 'warn' : 'pass');
  return {
    generated_utc: new Date().toISOString(),
    edition_code: editionCode,
    edition_folder: editionFolder,
    manifest_path: manifestPath,
    status,
    summary: bySeverity,
    findings
  };
}
```

`apex-core/tools/apex-validate.js`:
```javascript
#!/usr/bin/env node
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve, basename } from 'node:path';
import { validateManifest } from './validate-manifest.js';
import { buildReport } from './report.js';

function main(argv) {
  const args = argv.slice(2);
  const ci = args.includes('--ci');
  const target = args.find((a) => !a.startsWith('--'));
  if (!target) {
    console.error('usage: apex-validate [--ci] <edition-folder>');
    process.exit(3);
  }
  const editionFolder = resolve(target);
  const manifestPath = resolve(editionFolder, 'data/schemas.manifest.json');

  let manifest;
  try {
    manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
  } catch (e) {
    console.error(`cannot read manifest at ${manifestPath}: ${e.message}`);
    process.exit(3);
  }

  const { findings } = validateManifest(manifest);
  const report = buildReport({
    editionCode: manifest.edition_code ?? basename(editionFolder),
    editionFolder,
    manifestPath,
    findings
  });
  writeFileSync(resolve(editionFolder, 'data/report.json'), JSON.stringify(report, null, 2));

  if (ci) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log(`apex-validate: ${report.status.toUpperCase()} · critical=${report.summary.critical} warning=${report.summary.warning ?? 0}`);
  }

  if (report.summary.critical > 0) process.exit(2);
  if ((report.summary.warning ?? 0) > 0) process.exit(1);
  process.exit(0);
}

main(process.argv);
```

**Step 5: Run tests**

Run: `npm test`
Expected: both CLI tests pass.

**Step 6: Commit**

```bash
git add apex-core/tools/apex-validate.js apex-core/tools/report.js apex-core/tools/apex-validate.test.js apex-rc/data/schemas.manifest.json
git commit -m "feat(validator): apex-validate CLI author mode with JSON report"
```

---

### Task 9: Add HTML report generator using Core design tokens

**Files:**
- Create: `apex-core/tools/render-html.js`
- Create: `apex-core/tools/render-html.test.js`
- Modify: `apex-core/tools/apex-validate.js`

**Step 1: Write failing test**

`apex-core/tools/render-html.test.js`:
```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { renderHtml } from './render-html.js';

const sample = {
  generated_utc: '2026-04-17T12:00:00Z',
  edition_code: 'RC',
  status: 'pass',
  summary: { critical: 0, warning: 0, info: 0 },
  findings: []
};

test('renderHtml returns a self-contained HTML document', () => {
  const html = renderHtml(sample);
  assert.match(html, /^<!doctype html>/i);
  assert.match(html, /Fraunces/);
  assert.match(html, /Instrument Sans/);
  assert.match(html, /--teal/);
  assert.match(html, /--amber/);
  assert.match(html, /--crimson/);
  assert.match(html, /RC/);
  assert.match(html, /PASS/);
});

test('renderHtml surfaces critical findings in crimson', () => {
  const html = renderHtml({
    ...sample,
    status: 'fail',
    summary: { critical: 1, warning: 0, info: 0 },
    findings: [{ severity: 'critical', rule: 'REQ-01', path: '$.edition_code', message: 'missing required field' }]
  });
  assert.match(html, /REQ-01/);
  assert.match(html, /crimson/i);
});
```

**Step 2: Run test to verify failure**

Run: `npm test` → FAIL, missing module.

**Step 3: Implement `render-html.js`**

Single self-contained function. Inline CSS with Core Part 9 dark-theme tokens. No external fonts fetched; use Google Fonts `<link>` tags in the `<head>`. Structure:
- `<header>` — summary card (status chip colored per severity)
- `<section>` — compliance heatmap grid (rows = schemas, columns = rule IDs touched)
- `<section>` — findings list with severity-colored dots
- `<footer>` — generated timestamp + Core version

Keep it ~150 lines. Template literal for the HTML.

**Step 4: Wire into `apex-validate.js`**

In `apex-validate.js`, import `renderHtml` and write `report.html` alongside `report.json`:
```javascript
import { renderHtml } from './render-html.js';
// ...
writeFileSync(resolve(editionFolder, 'data/report.html'), renderHtml(report));
```

**Step 5: Run tests**

Run: `npm test`
Expected: all tests pass.

**Step 6: Manually verify the HTML**

Run: `node apex-core/tools/apex-validate.js apex-rc`
Open `apex-rc/data/report.html` in a browser. Confirm: Fraunces/Instrument Sans load, dark theme, PASS chip is teal.

**Step 7: Commit**

```bash
git add apex-core/tools/render-html.js apex-core/tools/render-html.test.js apex-core/tools/apex-validate.js
git commit -m "feat(validator): HTML report renderer with Core design tokens"
```

---

## Phase 3 — Edition Onboarding

### Task 10: Populate real RC manifest from existing schemas.json contract

**Files:**
- Modify: `apex-rc/data/schemas.manifest.json` (replace seed with full content)
- Create: `apex-rc/data/schemas.json` (consolidated from `apex-rc-build-spec-v2.md` Part 4)
- Create: `apex-rc/README.md` (1 paragraph + inheritance line per v1.2)

**Step 1: Extract MERML/SCML/CXML/MKTL entity lists**

Read `apex-rc-build-spec-v2.md` section 4.3 — entity names are enumerated there. For each schema build an initial `entities` array; one entity per name with placeholder `grain` and `primary_key` values matching the build spec's prose. The goal is *passing the validator*, not shipping a production schema registry (that comes in a follow-up work stream).

Minimum viable: for each of the 4 RC schemas, include the 3-5 most important entities with real grain/PK.

**Step 2: Write full `schemas.manifest.json`**

Use the Part 3.2 example from the design doc as a template. Bump versions and populate entities per step 1.

**Step 3: Add the inheritance line to the edition spec**

Modify the top of `apex-rc-build-spec-v2.md` — change the "Spec version" line to reference Core v1.2, and add a line: `**Manifest:** apex-rc/data/schemas.manifest.json — see Core v1.2`.

**Step 4: Run validator**

Run: `node apex-core/tools/apex-validate.js apex-rc`
Expected: exits 0, writes `apex-rc/data/report.html` and `report.json`, both show PASS.

**Step 5: Fix any surfaced issues**

If the validator flags issues, fix the manifest — not the validator. The validator is the contract now.

**Step 6: Commit**

```bash
git add apex-rc/
git commit -m "feat(rc): populate schemas.manifest.json for RC edition"
```

---

## Phase 4 — Fleet & Sync

### Task 11: L3 fleet registry seed + fleet-mode validator

**Files:**
- Create: `apex-fleet/data/fleet-registry.json`
- Create: `apex-fleet/README.md` (paragraph + Independence note)
- Create: `apex-core/tools/validate-fleet.js`
- Create: `apex-core/tools/validate-fleet.test.js`
- Modify: `apex-core/tools/apex-validate.js` (add `--fleet` flag)

**Step 1: Seed the registry**

`apex-fleet/data/fleet-registry.json` — two synthetic accounts per Part 3.3 of the design doc. Synthetic-only, clearly fictional IDs.

**Step 2: Write failing tests**

`validate-fleet.test.js` covers:
- Every `pinned_schema.version` exists in the referenced edition's `schemas.manifest.json`.
- No silent downgrade: if an L4 `deployed_schemas` entry exists with a higher version than L3's `pinned_schemas`, that's a critical.
- `auto_upgrade_policy` must map all three bump levels.
- Opaque-ID check: `account_id` must match `^acct-[a-z0-9-]+$` (no client-identifiable strings).

**Step 3: Implement `validate-fleet.js`**

Takes the fleet registry path + a folder of edition manifests; resolves each pin; returns findings in the same shape `validate-manifest` does.

**Step 4: Extend the CLI**

In `apex-validate.js`, add:
- `--fleet` mode → runs fleet validation across `apex-fleet/data/fleet-registry.json` and every discoverable `apex-*/data/schemas.manifest.json`; writes `apex-fleet/data/fleet-report.{html,json}`.
- `--fleet --account <id>` → scopes the report to a single account.

**Step 5: Add a fleet-mode section to `render-html.js`**

Render the drift matrix (rows=accounts, columns=schemas). Each cell shows `deployed → pinned` colored by required gate per Part 7.4 of design doc.

**Step 6: Run tests**

Run: `npm test` — all pass.
Run: `node apex-core/tools/apex-validate.js --fleet` — writes fleet report, exits 0.

**Step 7: Commit**

```bash
git add apex-fleet/ apex-core/tools/validate-fleet.js apex-core/tools/validate-fleet.test.js apex-core/tools/apex-validate.js apex-core/tools/render-html.js
git commit -m "feat(fleet): fleet-mode validator with drift matrix rendering"
```

---

### Task 12: `apex-sync` CLI — status + check + plan (read-only slice)

**Files:**
- Create: `apex-core/tools/apex-sync.js`
- Create: `apex-core/tools/apex-sync.test.js`
- Create: `apex-core/tools/fixtures/deployed-manifest.json`
- Create: `apex-core/tools/fixtures/pinned-manifest.json`

**Step 1: Create fixtures**

Synthetic L4 and a derived "pinned" slice for one account. `pinned-manifest.json` has MERML@1.3.0 and CXML@2.0.0 vs `deployed-manifest.json` on MERML@1.3.0 and CXML@1.1.0 — so the test drift is one HITL-blocked upgrade.

**Step 2: Write failing tests**

`apex-sync.test.js`:
- `apex-sync status` exits 1 when drift exists, prints a 3-column table to stdout.
- `apex-sync check` exits 1 when drift exists, silent.
- `apex-sync plan --schema CXML` prints planned DDL outline and lists dependent ORCHs (stubbed for now — look up by schema code in a lookup table).

**Step 3: Implement the CLI**

Four subcommands: `status`, `check`, `plan`, `apply`. For Task 12 implement only `status`, `check`, `plan`. `apply` prints "not yet implemented — will execute Fabric DDL in Task 13" and exits 3.

`apex-sync` reads `deployed-manifest.json` and `pinned-manifest.json` from two configurable paths (env vars `APEX_DEPLOYED` and `APEX_PINNED`). In production these are wired to the tenant OneLake; in tests they point to fixtures.

**Step 4: Run tests**

Run: `npm test` — all pass.

**Step 5: Commit**

```bash
git add apex-core/tools/apex-sync.js apex-core/tools/apex-sync.test.js apex-core/tools/fixtures/deployed-manifest.json apex-core/tools/fixtures/pinned-manifest.json
git commit -m "feat(sync): apex-sync status/check/plan read-only commands"
```

---

### Task 13: `apex-sync apply` with gate-based routing + approval token

**Files:**
- Modify: `apex-core/tools/apex-sync.js`
- Modify: `apex-core/tools/apex-sync.test.js`
- Create: `apex-core/tools/ddl-driver.js` (pluggable; default is a no-op logger)

**Step 1: Write failing tests**

Extend `apex-sync.test.js`:
- `apex-sync apply` with a MINOR drift applies automatically and updates the deployed manifest with new versions, timestamps, and `gate: 'ACK_ONLY'`.
- `apex-sync apply` with a MAJOR drift without `--approve` exits 2 and does not modify L4.
- `apex-sync apply --approve ticket://CHG-9999` with MAJOR drift applies and sets `approved_by: "ticket://CHG-9999"`.
- Approve token regex enforced: `--approve bogus` exits 3 with "invalid approval token".

**Step 2: Implement pluggable DDL driver**

`apex-core/tools/ddl-driver.js`:
```javascript
export function createDdlDriver({ kind = 'noop', logger = console } = {}) {
  if (kind === 'noop') {
    return {
      async apply({ schemaCode, fromVersion, toVersion, changes }) {
        logger.log(`[ddl-noop] ${schemaCode}: ${fromVersion} → ${toVersion} (${changes.length} changes)`);
        return { ok: true };
      }
    };
  }
  throw new Error(`unknown ddl driver: ${kind}`);
}
```

Production will wire a Fabric driver; default `noop` is fine for tests.

**Step 3: Implement `apply`**

Classify each drift's bump. Look up policy in the pinned manifest's auto_upgrade_policy. Route:
- `ZERO_TOUCH` / `ACK_ONLY` → call driver.apply, update L4.
- `HITL` without `--approve` → print pending entry, exit 2.
- `HITL` with valid `--approve` → call driver.apply, record `approved_by`, update L4.

Approval regex: `^ticket://CHG-\d+$`.

**Step 4: Run tests**

Run: `npm test` — all pass.

**Step 5: Commit**

```bash
git add apex-core/tools/apex-sync.js apex-core/tools/apex-sync.test.js apex-core/tools/ddl-driver.js
git commit -m "feat(sync): apex-sync apply with gate routing and approval tokens"
```

---

### Task 14: Release bundler stub

**Files:**
- Create: `apex-fleet/tools/release-bundler.js`
- Create: `apex-fleet/tools/release-bundler.test.js`

**Step 1: Write failing test**

The bundler reads the fleet registry, reads each edition manifest, and for each account emits a JSON bundle scoped to that account at `apex-fleet/bundles/<account_id>.json`. The bundle contains only: `account_id`, `pinned_schemas` with full changelog entries inlined, `auto_upgrade_policy`, `core_version`.

Test: run bundler, verify bundle files exist, verify each bundle references only that account's pinned versions.

**Step 2: Implement**

Pure function: `bundleForAccount(registry, editionManifests, accountId)` → bundle object. Signing is a stub (`signature: 'SHA256:STUB'`) — real signing is a Task 15 follow-up.

**Step 3: Run tests & commit**

```bash
git add apex-fleet/tools/release-bundler.js apex-fleet/tools/release-bundler.test.js
git commit -m "feat(fleet): release-bundler stub (unsigned)"
```

---

## Phase 5 — Finishing

### Task 15: Update active edition specs with v1.2 inheritance

**Files:**
- Modify: `apex-th-build-spec.md`, `apex-hls-build-spec.md`, `apex-tmt-build-spec.md`, `apex-er-build-spec.md`, `apex-ice-build-spec.md`, `apex-rc-build-spec-v2.md`

**Step 1: One-line bump in each spec**

For each active edition, update Part 0's "This spec inherits from APEX Core v1.1." line to "v1.2" and add the manifest pointer:

```
**Manifest:** apex-<code>/data/schemas.manifest.json — conforms to Core v1.2 contract.
```

**Step 2: Commit**

```bash
git add apex-*-build-spec*.md
git commit -m "docs(editions): bump inheritance to Core v1.2"
```

---

### Task 16: README + top-level CHANGELOG

**Files:**
- Modify: `README.md` (top-level)
- Create: `CHANGELOG.md` (top-level)

**Step 1: Root README**

One paragraph: what APEX is. Pointers to the build specs, the design doc, and the tools.

**Step 2: Root CHANGELOG**

```markdown
# APEX Changelog

## 2026-04-17 — v1.2 Schema Versioning Manifest

- Landed 4-layer manifest model (L1 contract, L2 edition, L3 fleet, L4 tenant).
- Introduced apex-validate (dual-mode) and apex-sync CLIs.
- RC edition onboarded as reference implementation.
- Full design: docs/plans/2026-04-17-schema-versioning-manifest-design.md
```

**Step 3: Commit**

```bash
git add README.md CHANGELOG.md
git commit -m "docs: root README and CHANGELOG for v1.2 landing"
```

---

## Deferred (explicit non-goals for this plan)

- **Real Fabric DDL driver.** Task 13 ships a no-op driver. Wiring Fabric Lakehouse DDL execution is a separate work stream with client-tenant-specific credentials and is out of scope.
- **Signed release bundles.** Task 14 uses a stub signature. Real signing (Azure Key Vault or sigstore) is a separate hardening task.
- **Tenant heartbeat endpoint.** The fleet registry's `last_heartbeat_*` fields are written by hand in Phase 4. The Azure Function/Logic App that receives tenant heartbeats and posts back to Git via PR automation is a follow-up plan.
- **Power BI in-tenant view.** The DAX / Power BI artifact is specified in the design but not implemented here — it's a separate content work stream.
- **Agent/ORCH/Solution Stack versioning.** The design explicitly defers these. The same L1/L2/L3/L4 pattern can be adopted later.

---

## Verification Checklist (run before declaring done)

1. `npm test` — all tests pass.
2. `node apex-core/tools/apex-validate.js apex-rc` — exits 0, produces `report.html` and `report.json`.
3. Open `apex-rc/data/report.html` in a browser — Fraunces loads, teal PASS chip, no console errors.
4. `node apex-core/tools/apex-validate.js --fleet` — exits 0, produces fleet-report with at least 2 accounts rendered.
5. `node apex-core/tools/apex-sync.js status` with the sync fixtures — exits 1, shows HITL drift row for CXML.
6. `node apex-core/tools/apex-sync.js apply` without approval — exits 2, L4 unchanged.
7. `node apex-core/tools/apex-sync.js apply --approve ticket://CHG-9999` — exits 0, L4 updated with new version + `approved_by`.
8. `git log --oneline` shows a commit per task, descriptive messages, no `[skip ci]` or `--no-verify`.

---

**End of implementation plan — 2026-04-17**
