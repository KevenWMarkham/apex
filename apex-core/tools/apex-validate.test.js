import { test } from 'node:test';
import assert from 'node:assert/strict';
import { execSync } from 'node:child_process';
import { readFileSync, existsSync, unlinkSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CLI = resolve(__dirname, 'apex-validate.js');
const EDITION = resolve(__dirname, '../../apex-rc');

function run(args) {
  try {
    const stdout = execSync(`node "${CLI}" ${args}`, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    return { code: 0, stdout };
  } catch (e) {
    return { code: e.status ?? -1, stdout: e.stdout?.toString() ?? '', stderr: e.stderr?.toString() ?? '' };
  }
}

test('apex-validate <edition> exits 0 for valid edition and writes report.json', () => {
  const reportPath = resolve(EDITION, 'data/report.json');
  if (existsSync(reportPath)) unlinkSync(reportPath);
  const { code } = run(`"${EDITION}"`);
  assert.equal(code, 0, 'expected exit 0');
  assert.ok(existsSync(reportPath), 'report.json should be written');
  const report = JSON.parse(readFileSync(reportPath, 'utf8'));
  assert.equal(report.status, 'pass');
  assert.equal(report.summary.critical, 0);
});

test('apex-validate --ci emits machine-readable JSON to stdout', () => {
  const { code, stdout } = run(`--ci "${EDITION}"`);
  assert.equal(code, 0);
  const parsed = JSON.parse(stdout);
  assert.ok(parsed.summary);
  assert.equal(typeof parsed.summary.critical, 'number');
  assert.equal(parsed.edition_code, 'RC');
});

test('apex-validate exits 3 on missing manifest', () => {
  const { code } = run(`"${resolve(__dirname, 'does-not-exist')}"`);
  assert.equal(code, 3);
});

test('apex-validate exits 3 with no arguments', () => {
  const { code } = run('');
  assert.equal(code, 3);
});
