import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { validateFleet } from './validate-fleet.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const loadJson = (p) => JSON.parse(readFileSync(p, 'utf8'));

const registry = () => loadJson(resolve(__dirname, '../../apex-fleet/data/fleet-registry.json'));
const manifests = () => {
  const rc = loadJson(resolve(__dirname, '../../apex-rc/data/schemas.manifest.json'));
  return new Map([['RC', rc]]);
};

test('valid fleet registry returns no critical findings', () => {
  const result = validateFleet(registry(), manifests());
  const criticals = result.findings.filter((f) => f.severity === 'critical');
  assert.equal(criticals.length, 0, JSON.stringify(criticals, null, 2));
});

test('fleet registry flags pinned version ahead of catalog', () => {
  const r = registry();
  r.accounts[0].pinned_schemas[0].version = '9.9.9';
  const result = validateFleet(r, manifests());
  assert.ok(result.findings.some((f) => f.rule === 'FLEET-PIN-AHEAD-OF-CATALOG'));
});

test('fleet registry flags pin to unknown schema', () => {
  const r = registry();
  r.accounts[0].pinned_schemas[0].code = 'XXYZL';
  const result = validateFleet(r, manifests());
  assert.ok(result.findings.some((f) => f.rule === 'FLEET-PIN-UNKNOWN-SCHEMA'));
});

test('fleet registry flags non-opaque account_id', () => {
  const r = registry();
  r.accounts[0].account_id = 'Walmart Inc';
  const result = validateFleet(r, manifests());
  assert.ok(result.findings.some((f) => f.rule === 'FLEET-ACCOUNT-ID'));
});

test('fleet registry requires all three bump-level policy entries', () => {
  const r = registry();
  delete r.accounts[0].auto_upgrade_policy.MAJOR;
  const result = validateFleet(r, manifests());
  assert.ok(result.findings.some((f) => f.rule === 'FLEET-POLICY-MISSING' && f.path.endsWith('.MAJOR')));
});

test('fleet registry flags unknown edition_code', () => {
  const r = registry();
  r.accounts[0].edition_code = 'ZZ';
  const result = validateFleet(r, manifests());
  assert.ok(result.findings.some((f) => f.rule === 'FLEET-EDITION-UNKNOWN'));
});

test('fleet registry flags duplicate account_id', () => {
  const r = registry();
  r.accounts[1].account_id = r.accounts[0].account_id;
  const result = validateFleet(r, manifests());
  assert.ok(result.findings.some((f) => f.rule === 'FLEET-DUPLICATE-ID'));
});

test('fleet registry filters by account when opts.accountFilter is set', () => {
  const r = registry();
  r.accounts[1].pinned_schemas[0].version = '9.9.9';
  const filtered = validateFleet(r, manifests(), { accountFilter: 'acct-alpha-001' });
  const aheadIssues = filtered.findings.filter((f) => f.rule === 'FLEET-PIN-AHEAD-OF-CATALOG');
  assert.equal(aheadIssues.length, 0);
});
