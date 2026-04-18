import semver from 'semver';

const ACCOUNT_ID_RE = /^acct-[a-z0-9-]+$/;
const VALID_POLICY_GATES = ['ZERO_TOUCH', 'ACK_ONLY', 'HITL'];
const REQUIRED_POLICY_BUMPS = ['PATCH', 'MINOR', 'MAJOR'];

/**
 * Validate a practice registry against per-edition manifests.
 *
 * @param {object} registry       Parsed practice-registry.json (L3).
 * @param {Map<string, object>} editionManifests  edition_code -> parsed L2 manifest.
 * @param {object} [opts]
 * @param {string} [opts.accountFilter]  If set, only validate the matching account.
 * @returns {{ findings: Array, drift: Array<{ account_id, schema, deployed, pinned, gate }> }}
 */
export function validatePractice(registry, editionManifests, opts = {}) {
  const findings = [];
  const drift = [];

  if (!registry || typeof registry !== 'object' || Array.isArray(registry)) {
    return {
      findings: [{ severity: 'critical', rule: 'PRACTICE-SHAPE-ROOT', path: '$', message: 'practice registry must be a JSON object' }],
      drift
    };
  }

  const accounts = Array.isArray(registry.accounts) ? registry.accounts : [];
  if (!Array.isArray(registry.accounts)) {
    findings.push({ severity: 'critical', rule: 'PRACTICE-SHAPE-ACCOUNTS', path: '$.accounts', message: 'accounts must be an array' });
  }

  const seenIds = new Set();

  for (const [i, acc] of accounts.entries()) {
    if (opts.accountFilter && acc.account_id !== opts.accountFilter) continue;
    const aPath = `$.accounts[${i}]`;

    // Opaque ID: no client-identifiable strings. Lowercase, kebab, starts with acct-.
    if (!acc.account_id || !ACCOUNT_ID_RE.test(acc.account_id)) {
      findings.push({
        severity: 'critical', rule: 'PRACTICE-ACCOUNT-ID',
        path: `${aPath}.account_id`,
        message: `account_id must match /^acct-[a-z0-9-]+$/ to keep IDs opaque; got ${acc.account_id}`
      });
    }

    if (seenIds.has(acc.account_id)) {
      findings.push({
        severity: 'critical', rule: 'PRACTICE-DUPLICATE-ID',
        path: `${aPath}.account_id`,
        message: `duplicate account_id ${acc.account_id}`
      });
    }
    seenIds.add(acc.account_id);

    // Policy must map all three bump levels to a known gate.
    const policy = acc.auto_upgrade_policy ?? {};
    for (const bump of REQUIRED_POLICY_BUMPS) {
      if (!policy[bump]) {
        findings.push({
          severity: 'critical', rule: 'PRACTICE-POLICY-MISSING',
          path: `${aPath}.auto_upgrade_policy.${bump}`,
          message: `auto_upgrade_policy.${bump} is required`
        });
      } else if (!VALID_POLICY_GATES.includes(policy[bump])) {
        findings.push({
          severity: 'critical', rule: 'PRACTICE-POLICY-GATE',
          path: `${aPath}.auto_upgrade_policy.${bump}`,
          message: `policy gate must be ZERO_TOUCH, ACK_ONLY, or HITL; got ${policy[bump]}`
        });
      }
    }

    // Pinned schemas must resolve in the edition manifest.
    const manifest = editionManifests.get(acc.edition_code);
    if (!manifest) {
      findings.push({
        severity: 'critical', rule: 'PRACTICE-EDITION-UNKNOWN',
        path: `${aPath}.edition_code`,
        message: `no manifest found for edition ${acc.edition_code}`
      });
      continue;
    }

    const schemaVersions = new Map();
    for (const s of manifest.schemas ?? []) schemaVersions.set(s.code, s.version);

    for (const [j, p] of (acc.pinned_schemas ?? []).entries()) {
      const pPath = `${aPath}.pinned_schemas[${j}]`;
      if (!semver.valid(p.version)) {
        findings.push({
          severity: 'critical', rule: 'PRACTICE-PIN-SEMVER',
          path: `${pPath}.version`,
          message: `pinned version must be valid SemVer; got ${p.version}`
        });
        continue;
      }
      const catalog = schemaVersions.get(p.code);
      if (!catalog) {
        findings.push({
          severity: 'critical', rule: 'PRACTICE-PIN-UNKNOWN-SCHEMA',
          path: `${pPath}.code`,
          message: `schema ${p.code} does not exist in edition ${acc.edition_code}`
        });
        continue;
      }
      // Record any drift for the report (pinned !== catalog's latest).
      if (semver.gt(catalog, p.version)) {
        drift.push({
          account_id: acc.account_id,
          schema: p.code,
          deployed: p.version,
          pinned: p.version,
          latest: catalog,
          gate: acc.auto_upgrade_policy?.MINOR ?? 'ACK_ONLY'
        });
      } else if (semver.gt(p.version, catalog)) {
        findings.push({
          severity: 'critical', rule: 'PRACTICE-PIN-AHEAD-OF-CATALOG',
          path: `${pPath}.version`,
          message: `pinned ${p.version} is newer than edition catalog's latest ${catalog}`
        });
      }
    }
  }

  return { findings, drift };
}
