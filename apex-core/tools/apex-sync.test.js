import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execSync } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync, copyFileSync, unlinkSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CLI = resolve(__dirname, 'apex-sync.js');
const DEPLOYED_FIXTURE = resolve(__dirname, 'fixtures/deployed-manifest.json');
const PINNED_FIXTURE = resolve(__dirname, 'fixtures/pinned-manifest.json');
const TMP_DEPLOYED = resolve(__dirname, 'fixtures/.deployed.test.json');

function run(cmd, { env = {} } = {}) {
  try {
    const stdout = execSync(`node "${CLI}" ${cmd}`, {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      env: { ...process.env, APEX_DEPLOYED: DEPLOYED_FIXTURE, APEX_PINNED: PINNED_FIXTURE, ...env }
    });
    return { code: 0, stdout };
  } catch (e) {
    return { code: e.status ?? -1, stdout: e.stdout?.toString() ?? '', stderr: e.stderr?.toString() ?? '' };
  }
}

function resetTmpDeployed() {
  copyFileSync(DEPLOYED_FIXTURE, TMP_DEPLOYED);
}

// The fixture has MERML/SCML/MKTL in sync but CXML deployed@1.1.0 vs pinned@2.0.0 (MAJOR/HITL drift).

test('apex-sync status exits 1 when drift exists and prints table', () => {
  const { code, stdout } = run('status');
  assert.equal(code, 1);
  assert.match(stdout, /Schema   Deployed    Pinned     Status/);
  assert.match(stdout, /CXML/);
  assert.match(stdout, /HITL - pending/);
});

test('apex-sync check exits 1 silently on drift', () => {
  const { code, stdout } = run('check');
  assert.equal(code, 1);
  assert.equal(stdout, '');
});

test('apex-sync plan --schema CXML prints planned changes', () => {
  const { code, stdout } = run('plan --schema CXML');
  assert.equal(code, 0);
  assert.match(stdout, /\[plan\] CXML: 1\.1\.0 -> 2\.0\.0/);
  assert.match(stdout, /change_grain/);
});

test('apex-sync apply refuses MAJOR drift without --approve (exit 2)', () => {
  resetTmpDeployed();
  const { code, stdout } = run('apply', { env: { APEX_DEPLOYED: TMP_DEPLOYED } });
  assert.equal(code, 2);
  assert.match(stdout, /\[blocked\] CXML/);
  const updated = JSON.parse(readFileSync(TMP_DEPLOYED, 'utf8'));
  // CXML should remain at 1.1.0 (not applied).
  const cxml = updated.deployed_schemas.find((s) => s.code === 'CXML');
  assert.equal(cxml.version, '1.1.0');
  // pending_upgrades should reflect CXML.
  assert.equal(updated.pending_upgrades.length, 1);
  assert.equal(updated.pending_upgrades[0].code, 'CXML');
});

test('apex-sync apply --approve ticket applies MAJOR drift (exit 0)', () => {
  resetTmpDeployed();
  const { code, stdout } = run('apply --approve ticket://CHG-9999', { env: { APEX_DEPLOYED: TMP_DEPLOYED } });
  assert.equal(code, 0);
  assert.match(stdout, /\[applied\] CXML/);
  const updated = JSON.parse(readFileSync(TMP_DEPLOYED, 'utf8'));
  const cxml = updated.deployed_schemas.find((s) => s.code === 'CXML');
  assert.equal(cxml.version, '2.0.0');
  assert.equal(cxml.approved_by, 'ticket://CHG-9999');
  assert.equal(updated.pending_upgrades.length, 0);
  // cleanup
  if (existsSync(TMP_DEPLOYED)) unlinkSync(TMP_DEPLOYED);
});

test('apex-sync apply with malformed approval token exits 3', () => {
  const { code, stderr } = run('apply --approve bogus');
  assert.equal(code, 3);
  assert.match(stderr, /invalid approval token/);
});

test('apex-sync with no command exits 3', () => {
  const { code, stderr } = run('');
  assert.equal(code, 3);
  assert.match(stderr, /usage: apex-sync/);
});
