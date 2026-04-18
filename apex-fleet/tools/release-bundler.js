import { readFileSync, writeFileSync, mkdirSync, readdirSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

/**
 * Build a signed-bundle slice of the fleet registry for a single account.
 *
 * Returned bundle contains only that account's pinned versions (with
 * latest changelog entries inlined from the edition manifest), the
 * auto_upgrade_policy, and Core version. No other account's data leaks.
 *
 * Signing is currently a stub (`signature: 'SHA256:STUB'`). A production
 * signer would wire Azure Key Vault or sigstore; that is out of scope.
 *
 * @param {object} registry
 * @param {Map<string, object>} editionManifests  edition_code -> parsed L2
 * @param {string} accountId
 * @returns {object|null}
 */
export function bundleForAccount(registry, editionManifests, accountId) {
  const acc = (registry.accounts ?? []).find((a) => a.account_id === accountId);
  if (!acc) return null;
  const manifest = editionManifests.get(acc.edition_code);
  if (!manifest) return null;

  const changelogByCode = new Map();
  for (const s of manifest.schemas ?? []) {
    changelogByCode.set(s.code, { version: s.version, latest: (s.changelog ?? [])[0] });
  }

  const pinnedWithChangelog = (acc.pinned_schemas ?? []).map((p) => {
    const info = changelogByCode.get(p.code) ?? {};
    return {
      code: p.code,
      version: p.version,
      latest_changelog_entry: info.latest
    };
  });

  return {
    account_id: acc.account_id,
    edition_code: acc.edition_code,
    core_version_required: acc.core_version,
    auto_upgrade_policy: acc.auto_upgrade_policy,
    pinned_schemas: pinnedWithChangelog,
    generated_utc: new Date().toISOString(),
    signature: 'SHA256:STUB'
  };
}

/**
 * Bundle every account in the registry into a signed per-account file.
 *
 * @param {string} [repoRoot]
 * @returns {Array<{ account_id: string, path: string }>}
 */
export function bundleAll(repoRoot) {
  repoRoot = repoRoot ?? resolve(dirname(fileURLToPath(import.meta.url)), '..', '..');
  const registry = JSON.parse(readFileSync(resolve(repoRoot, 'apex-fleet/data/fleet-registry.json'), 'utf8'));
  const editionManifests = new Map();
  for (const name of readdirSync(repoRoot)) {
    if (!name.startsWith('apex-') || name === 'apex-core' || name === 'apex-fleet') continue;
    try {
      const m = JSON.parse(readFileSync(resolve(repoRoot, name, 'data', 'schemas.manifest.json'), 'utf8'));
      if (m.edition_code) editionManifests.set(m.edition_code, m);
    } catch { /* skip editions without a manifest */ }
  }
  const outDir = resolve(repoRoot, 'apex-fleet/bundles');
  mkdirSync(outDir, { recursive: true });
  const written = [];
  for (const acc of registry.accounts ?? []) {
    const bundle = bundleForAccount(registry, editionManifests, acc.account_id);
    if (!bundle) continue;
    const outPath = resolve(outDir, `${acc.account_id}.json`);
    writeFileSync(outPath, JSON.stringify(bundle, null, 2));
    written.push({ account_id: acc.account_id, path: outPath });
  }
  return written;
}

// CLI entrypoint
if (import.meta.url === `file://${process.argv[1]}` || process.argv[1]?.endsWith('release-bundler.js')) {
  const written = bundleAll();
  for (const w of written) console.log(`[bundled] ${w.account_id} -> ${w.path}`);
  if (written.length === 0) {
    console.error('no accounts found to bundle');
    process.exit(3);
  }
}
