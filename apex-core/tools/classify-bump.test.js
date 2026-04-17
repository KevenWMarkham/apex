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
