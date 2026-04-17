import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CONTRACT_PATH = resolve(__dirname, '../data/schema-manifest-contract.json');

test('L1 contract loads as valid JSON', () => {
  const raw = readFileSync(CONTRACT_PATH, 'utf8');
  const parsed = JSON.parse(raw);
  assert.ok(parsed);
});

test('L1 contract declares contract_version and core_version', () => {
  const contract = JSON.parse(readFileSync(CONTRACT_PATH, 'utf8'));
  assert.equal(contract.contract_version, '1.0');
  assert.equal(contract.core_version, '1.2');
});

test('L1 contract declares required top-level fields', () => {
  const contract = JSON.parse(readFileSync(CONTRACT_PATH, 'utf8'));
  const required = contract.required_fields;
  assert.ok(required.edition_code);
  assert.ok(required.core_version_required);
  assert.ok(required.manifest_version);
  assert.ok(required.schemas);
  assert.equal(required.schemas.min_items, 3);
  assert.equal(required.schemas.max_items, 5);
});

test('L1 contract defines schema_entry with version + changelog', () => {
  const contract = JSON.parse(readFileSync(CONTRACT_PATH, 'utf8'));
  assert.ok(contract.schema_entry.version);
  assert.ok(contract.schema_entry.changelog);
  assert.ok(contract.schema_entry.envelope_required);
});

test('L1 contract defines change_delta op enum with 9 values', () => {
  const contract = JSON.parse(readFileSync(CONTRACT_PATH, 'utf8'));
  const ops = contract.change_delta.op.values;
  assert.equal(ops.length, 9);
  assert.ok(ops.includes('add_entity'));
  assert.ok(ops.includes('remove_entity'));
  assert.ok(ops.includes('rename_entity'));
  assert.ok(ops.includes('add_column'));
  assert.ok(ops.includes('remove_column'));
  assert.ok(ops.includes('change_type'));
  assert.ok(ops.includes('change_pk'));
  assert.ok(ops.includes('change_grain'));
  assert.ok(ops.includes('metadata'));
});
