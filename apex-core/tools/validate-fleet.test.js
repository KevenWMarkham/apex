import { test } from 'node:test';
import assert from 'node:assert/strict';
import { validateFleet } from './validate-fleet.js';

test('validate-fleet shim returns FLEET-* rule codes for backward compatibility', () => {
  const result = validateFleet({}, new Map());
  const nonCompliant = result.findings.filter(f => f.rule.startsWith('PRACTICE-'));
  assert.equal(nonCompliant.length, 0, 'shim must translate PRACTICE-* back to FLEET-*');
  // Optional stronger assertion: at least one FLEET-* finding is produced for a clearly invalid input.
  assert.ok(result.findings.some(f => f.rule.startsWith('FLEET-')), 'shim must still produce FLEET-* findings');
});
