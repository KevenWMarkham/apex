/**
 * Build a structured validation report from a set of findings.
 *
 * @param {object} params
 * @param {string} params.editionCode
 * @param {string} params.editionFolder
 * @param {string} params.manifestPath
 * @param {Array<{severity: string, rule: string, path: string, message: string}>} params.findings
 * @returns {object}
 */
export function buildReport({ editionCode, editionFolder, manifestPath, findings }) {
  const bySeverity = { critical: 0, warning: 0, info: 0 };
  for (const f of findings) {
    bySeverity[f.severity] = (bySeverity[f.severity] ?? 0) + 1;
  }
  const status =
    bySeverity.critical > 0 ? 'fail' :
    bySeverity.warning > 0 ? 'warn' :
    'pass';
  return {
    generated_utc: new Date().toISOString(),
    edition_code: editionCode,
    edition_folder: editionFolder,
    manifest_path: manifestPath,
    status,
    summary: bySeverity,
    findings
  };
}
