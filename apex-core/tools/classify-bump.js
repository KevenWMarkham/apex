const MAJOR_OPS = new Set([
  'remove_entity', 'rename_entity', 'remove_column',
  'change_type', 'change_pk', 'change_grain'
]);
const MINOR_OPS = new Set(['add_entity', 'add_column']);
const PATCH_OPS = new Set(['metadata']);

/**
 * @param {Array<{op: string, target: string, detail: string}>} changes
 * @returns {'MAJOR' | 'MINOR' | 'PATCH'}
 */
export function classifyBump(changes) {
  if (!changes || changes.length === 0) {
    throw new Error('classifyBump: no changes provided');
  }
  let level = 'PATCH';
  for (const c of changes) {
    if (MAJOR_OPS.has(c.op)) return 'MAJOR';
    if (c.op === 'add_column') {
      // Anti-cheat rule 1: non-nullable additions are MAJOR.
      if (isNonNullable(c.detail)) return 'MAJOR';
      level = 'MINOR';
    } else if (MINOR_OPS.has(c.op)) {
      level = 'MINOR';
    }
  }
  return level;
}

function isNonNullable(detail = '') {
  return /\bNOT\s+NULL\b/i.test(detail);
}
