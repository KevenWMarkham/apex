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
