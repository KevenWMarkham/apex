import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { validatePack } from './validate-pack.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const loadFixture = (name) =>
  JSON.parse(readFileSync(resolve(__dirname, 'fixtures', name), 'utf8'));
const criticals = (r) => r.findings.filter((f) => f.severity === 'critical');

test('valid RC pack manifest returns no critical findings', () => {
  const result = validatePack(loadFixture('valid-rc.pack.json'));
  assert.equal(criticals(result).length, 0, JSON.stringify(criticals(result), null, 2));
});

test('valid RC pack manifest returns no warnings (refs all resolve)', () => {
  const result = validatePack(loadFixture('valid-rc.pack.json'));
  const warnings = result.findings.filter((f) => f.severity === 'warning');
  assert.equal(warnings.length, 0, JSON.stringify(warnings, null, 2));
});

test('null manifest returns a SHAPE-ROOT critical', () => {
  const result = validatePack(null);
  assert.equal(result.findings.length, 1);
  assert.equal(result.findings[0].rule, 'SHAPE-ROOT');
});

test('missing pack_code is critical (REQ-01)', () => {
  const m = loadFixture('valid-rc.pack.json');
  delete m.pack_code;
  assert.ok(validatePack(m).findings.some((f) => f.rule === 'REQ-01'));
});

test('missing gold_views is critical (REQ-07)', () => {
  const m = loadFixture('valid-rc.pack.json');
  delete m.gold_views;
  assert.ok(validatePack(m).findings.some((f) => f.rule === 'REQ-07'));
});

test('bad pack_code pattern is critical', () => {
  const m = loadFixture('valid-rc.pack.json');
  m.pack_code = 'retail';
  assert.ok(validatePack(m).findings.some((f) => f.rule === 'REQ-01-PATTERN'));
});

test('invalid priority is critical (ENUM-PRIORITY)', () => {
  const m = loadFixture('valid-rc.pack.json');
  m.priority = 'Differentiaite';
  assert.ok(validatePack(m).findings.some((f) => f.rule === 'ENUM-PRIORITY'));
});

test('pack with zero agents is critical (AGENTS-COUNT)', () => {
  const m = loadFixture('valid-rc.pack.json');
  m.agents = [];
  assert.ok(validatePack(m).findings.some((f) => f.rule === 'AGENTS-COUNT'));
});

test('agent without scenario_ids is critical (AGENT-SCENARIOS)', () => {
  const m = loadFixture('valid-rc.pack.json');
  m.agents[0].scenario_ids = [];
  assert.ok(validatePack(m).findings.some((f) => f.rule === 'AGENT-SCENARIOS'));
});

test('malformed gold view name is critical (GOLD-VIEW-PATTERN)', () => {
  const m = loadFixture('valid-rc.pack.json');
  m.gold_views[0].view = 'pricing_gold';
  assert.ok(validatePack(m).findings.some((f) => f.rule === 'GOLD-VIEW-PATTERN'));
});

test('policy without escalate_to_role is critical (POLICY-ESCALATE)', () => {
  const m = loadFixture('valid-rc.pack.json');
  delete m.policies[0].escalate_to_role;
  assert.ok(validatePack(m).findings.some((f) => f.rule === 'POLICY-ESCALATE'));
});

test('kpi source_view not registered in gold_views is a warning (KPI-SOURCE-REF)', () => {
  const m = loadFixture('valid-rc.pack.json');
  m.kpis[0].source_view = 'gold_unregistered_v1';
  const result = validatePack(m);
  assert.ok(result.findings.some((f) => f.rule === 'KPI-SOURCE-REF' && f.severity === 'warning'));
});

test('agent referencing an unregistered tool is a warning (AGENT-TOOL-REF)', () => {
  const m = loadFixture('valid-rc.pack.json');
  m.agents[0].tools = ['ghost_tool'];
  const result = validatePack(m);
  assert.ok(result.findings.some((f) => f.rule === 'AGENT-TOOL-REF' && f.severity === 'warning'));
});

test('findings include a precise JSONPath for the offending field', () => {
  const m = loadFixture('valid-rc.pack.json');
  delete m.policies[0].escalate_to_role;
  const finding = validatePack(m).findings.find((f) => f.rule === 'POLICY-ESCALATE');
  assert.ok(finding);
  assert.equal(finding.path, '$.policies[0].escalate_to_role');
  assert.equal(finding.severity, 'critical');
});
