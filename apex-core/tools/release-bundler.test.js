import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { bundleForAccount } from '../../apex-fleet/tools/release-bundler.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(__dirname, '../..');

const registry = () => JSON.parse(readFileSync(resolve(repoRoot, 'apex-fleet/data/fleet-registry.json'), 'utf8'));
const editionManifests = () => {
  const rc = JSON.parse(readFileSync(resolve(repoRoot, 'apex-rc/data/schemas.manifest.json'), 'utf8'));
  return new Map([['RC', rc]]);
};

test('bundleForAccount returns bundle scoped to requested account only', () => {
  const b = bundleForAccount(registry(), editionManifests(), 'acct-alpha-001');
  assert.ok(b);
  assert.equal(b.account_id, 'acct-alpha-001');
  // Must contain pinned_schemas but never another account's data.
  assert.ok(Array.isArray(b.pinned_schemas));
  assert.equal(b.pinned_schemas.length, 4);
  assert.ok(!('other_account' in b));
});

test('bundle includes latest changelog entry for each pinned schema', () => {
  const b = bundleForAccount(registry(), editionManifests(), 'acct-alpha-001');
  for (const p of b.pinned_schemas) {
    assert.ok(p.latest_changelog_entry, `${p.code} missing latest_changelog_entry`);
    assert.equal(p.latest_changelog_entry.version, p.version);
  }
});

test('bundle carries auto_upgrade_policy and core_version_required', () => {
  const b = bundleForAccount(registry(), editionManifests(), 'acct-alpha-001');
  assert.ok(b.auto_upgrade_policy);
  assert.equal(b.auto_upgrade_policy.MAJOR, 'HITL');
  assert.equal(b.core_version_required, '1.2');
});

test('bundle has a stubbed signature field', () => {
  const b = bundleForAccount(registry(), editionManifests(), 'acct-alpha-001');
  assert.equal(b.signature, 'SHA256:STUB');
});

test('bundleForAccount returns null for unknown account', () => {
  const b = bundleForAccount(registry(), editionManifests(), 'acct-does-not-exist');
  assert.equal(b, null);
});
