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
