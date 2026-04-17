import semver from 'semver';
import { classifyBump } from './classify-bump.js';

const EDITION_CODE_RE = /^[A-Z]{2,3}$/;
// Schema code pattern. Design doc §3.2 specifies `^[A-Z]{4,5}(ML|L)$`, but
// the doc's own examples (SCML = 4 chars, CXML = 4 chars, MKTL = 4 chars)
// require a minimum of 4 total chars, not 5. Interpreting the intent: 2-4
// letters of domain code followed by an `ML` or `L` suffix, total 3-6 chars.
const SCHEMA_CODE_RE = /^[A-Z]{2,4}(ML|L)$/;

/**
 * Validate an L2 edition manifest against the L1 contract shape and
 * semver / bump-classification rules.
 *
 * Returns a flat findings array. Consumers inspect `severity` ("critical"
 * vs "warning") and `rule` to decide how to surface issues.
 *
 * @param {object} manifest  Parsed manifest JSON object.
 * @returns {{ findings: Array<{severity: string, rule: string, path: string, message: string}> }}
 */
export function validateManifest(manifest) {
  const findings = [];

  // REQ-01 through REQ-04: top-level required fields.
  for (const [field, rule] of [
    ['edition_code', 'REQ-01'],
    ['core_version_required', 'REQ-02'],
    ['manifest_version', 'REQ-03'],
    ['schemas', 'REQ-04']
  ]) {
    if (!manifest[field]) {
      findings.push({
        severity: 'critical',
        rule,
        path: `$.${field}`,
        message: `missing required field ${field}`
      });
    }
  }

  if (manifest.edition_code && !EDITION_CODE_RE.test(manifest.edition_code)) {
    findings.push({
      severity: 'critical',
      rule: 'REQ-01-PATTERN',
      path: '$.edition_code',
      message: 'edition_code must match /^[A-Z]{2,3}$/'
    });
  }

  if (manifest.manifest_version && !semver.valid(manifest.manifest_version)) {
    findings.push({
      severity: 'critical',
      rule: 'REQ-03-SEMVER',
      path: '$.manifest_version',
      message: 'manifest_version must be valid SemVer'
    });
  }

  const schemas = manifest.schemas ?? [];
  if (schemas.length < 3 || schemas.length > 5) {
    findings.push({
      severity: 'critical',
      rule: 'REQ-04-COUNT',
      path: '$.schemas',
      message: `expected 3-5 schemas, got ${schemas.length}`
    });
  }

  for (const [i, s] of schemas.entries()) {
    const sPath = `$.schemas[${i}]`;

    if (!SCHEMA_CODE_RE.test(s.code || '')) {
      findings.push({
        severity: 'critical',
        rule: 'SCHEMA-CODE',
        path: `${sPath}.code`,
        message: `invalid schema code ${s.code}`
      });
    }
    if (!semver.valid(s.version)) {
      findings.push({
        severity: 'critical',
        rule: 'SCHEMA-VERSION',
        path: `${sPath}.version`,
        message: 'version must be valid SemVer'
      });
    }

    // Entity checks: primary_key non-empty, grain present.
    for (const [j, e] of (s.entities || []).entries()) {
      const ePath = `${sPath}.entities[${j}]`;
      if (!e.primary_key || e.primary_key.length === 0) {
        findings.push({
          severity: 'critical',
          rule: 'PK-EMPTY',
          path: `${ePath}.primary_key`,
          message: 'primary_key must have at least 1 column'
        });
      }
      if (!e.grain) {
        findings.push({
          severity: 'critical',
          rule: 'GRAIN-MISSING',
          path: `${ePath}.grain`,
          message: 'grain is required'
        });
      }
    }

    // Changelog checks.
    const changelog = s.changelog || [];
    if (changelog.length > 0) {
      const latest = changelog[0];
      if (latest.version !== s.version) {
        findings.push({
          severity: 'critical',
          rule: 'VERSION-CHANGELOG-MISMATCH',
          path: `${sPath}.version`,
          message: `schema.version (${s.version}) must match first changelog entry (${latest.version})`
        });
      }

      for (const [k, entry] of changelog.entries()) {
        const cPath = `${sPath}.changelog[${k}]`;
        const changes = entry.changes || [];

        // DETAIL-MISSING: add_column must carry a non-empty detail so the
        // classifier can detect `NOT NULL` (anti-cheat rule 1). An empty
        // detail silently classifies as MINOR even when the column is
        // non-nullable, which is the exact foot-gun the validator closes.
        for (const [m, c] of changes.entries()) {
          if (c.op === 'add_column' && (!c.detail || String(c.detail).trim() === '')) {
            findings.push({
              severity: 'critical',
              rule: 'DETAIL-MISSING',
              path: `${cPath}.changes[${m}].detail`,
              message: 'add_column requires a non-empty detail (e.g. "INT NOT NULL") so nullability can be classified'
            });
          }
        }

        // BUMP-MISMATCH: declared bump must match the classifier's computed
        // bump. Carve-out: initial GA (version 1.0.0) where the only changes
        // are `metadata` ops. Without this, every initial release declared as
        // MAJOR would trip the rule because metadata-only classifies as PATCH.
        // The initial GA is conventionally MAJOR regardless of the delta, so
        // skip the check rather than weaken it for non-initial entries.
        const isInitialGA =
          entry.version === '1.0.0' &&
          changes.length > 0 &&
          changes.every((c) => c.op === 'metadata');

        if (!isInitialGA && changes.length > 0) {
          const computed = classifyBump(changes);
          if (entry.bump !== computed) {
            findings.push({
              severity: 'critical',
              rule: 'BUMP-MISMATCH',
              path: `${cPath}.bump`,
              message: `declared ${entry.bump} but changes compute to ${computed}`
            });
          }
        }
      }
    }
  }

  return { findings };
}
