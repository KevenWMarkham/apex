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

test('add_column without detail is critical', () => {
  const m = loadFixture('valid-rc.manifest.json');
  m.schemas[0].changelog[0].changes = [{ op: 'add_column', target: 'T.col' }];
  m.schemas[0].changelog[0].bump = 'MINOR';
  const result = validateManifest(m);
  assert.ok(result.findings.some((f) => f.rule === 'DETAIL-MISSING'));
});

test('null manifest returns a SHAPE-ROOT critical', () => {
  const result = validateManifest(null);
  assert.equal(result.findings.length, 1);
  assert.equal(result.findings[0].rule, 'SHAPE-ROOT');
});

test('findings include a precise JSONPath for the offending field', () => {
  const m = loadFixture('valid-rc.manifest.json');
  m.schemas[0].entities[0].primary_key = [];
  const result = validateManifest(m);
  const pkFinding = result.findings.find((f) => f.rule === 'PK-EMPTY');
  assert.ok(pkFinding);
  assert.equal(pkFinding.path, '$.schemas[0].entities[0].primary_key');
  assert.equal(pkFinding.severity, 'critical');
});

test('entity with invalid layer is critical (ENUM-LAYER)', () => {
  const m = loadFixture('valid-rc.manifest.json');
  m.schemas[0].entities[0].layer = 'silver';
  const result = validateManifest(m);
  assert.ok(result.findings.some((f) => f.rule === 'ENUM-LAYER'));
});

test('changelog entry with invalid bump is critical (ENUM-BUMP)', () => {
  const m = loadFixture('valid-rc.manifest.json');
  m.schemas[0].changelog[0].bump = 'MIN0R';
  const result = validateManifest(m);
  assert.ok(result.findings.some((f) => f.rule === 'ENUM-BUMP'));
});

test('changelog entry with invalid gate is critical (ENUM-GATE)', () => {
  const m = loadFixture('valid-rc.manifest.json');
  m.schemas[0].changelog[0].gate = 'HUMAN';
  const result = validateManifest(m);
  assert.ok(result.findings.some((f) => f.rule === 'ENUM-GATE'));
});
