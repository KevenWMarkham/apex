/**
 * Pluggable DDL driver. The default is a no-op that only logs what would
 * have been executed — useful for tests and dry-runs. A production driver
 * would wire Fabric Lakehouse DDL execution with tenant-local credentials
 * (out of scope for Core).
 *
 * @param {object} [opts]
 * @param {string} [opts.kind='noop']
 * @param {{log: Function}} [opts.logger=console]
 */
export function createDdlDriver({ kind = 'noop', logger = console } = {}) {
  if (kind === 'noop') {
    return {
      async apply({ schemaCode, fromVersion, toVersion, changes }) {
        logger.log(`[ddl-noop] ${schemaCode}: ${fromVersion} -> ${toVersion} (${changes.length} change${changes.length === 1 ? '' : 's'})`);
        return { ok: true };
      }
    };
  }
  throw new Error(`unknown ddl driver: ${kind}`);
}
