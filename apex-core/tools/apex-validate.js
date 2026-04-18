#!/usr/bin/env node
/**
 * apex-validate — author-mode L2 manifest validator CLI.
 *
 * Usage:
 *   apex-validate <edition-folder>
 *   apex-validate --ci <edition-folder>
 *
 * Reads <edition-folder>/data/schemas.manifest.json, runs the L2 validator,
 * writes report.json (and eventually report.html) alongside, emits a one-line
 * summary on stdout. Exit codes: 0 = pass, 1 = warnings, 2 = criticals,
 * 3 = manifest shape broken (cannot read file or not valid JSON).
 */

import { readFileSync, writeFileSync } from 'node:fs';
import { resolve, basename } from 'node:path';
import { validateManifest } from './validate-manifest.js';
import { buildReport } from './report.js';

function main(argv) {
  const args = argv.slice(2);
  const ci = args.includes('--ci');
  const target = args.find((a) => !a.startsWith('--'));

  if (!target) {
    console.error('usage: apex-validate [--ci] <edition-folder>');
    process.exit(3);
  }

  const editionFolder = resolve(target);
  const manifestPath = resolve(editionFolder, 'data/schemas.manifest.json');

  let manifest;
  try {
    manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
  } catch (e) {
    console.error(`cannot read manifest at ${manifestPath}: ${e.message}`);
    process.exit(3);
  }

  const { findings } = validateManifest(manifest);
  const report = buildReport({
    editionCode: manifest.edition_code ?? basename(editionFolder),
    editionFolder,
    manifestPath,
    findings
  });

  writeFileSync(
    resolve(editionFolder, 'data/report.json'),
    JSON.stringify(report, null, 2)
  );

  if (ci) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    const w = report.summary.warning ?? 0;
    const c = report.summary.critical ?? 0;
    console.log(`apex-validate: ${report.status.toUpperCase()} · critical=${c} warning=${w}`);
  }

  if ((report.summary.critical ?? 0) > 0) process.exit(2);
  if ((report.summary.warning ?? 0) > 0) process.exit(1);
  process.exit(0);
}

main(process.argv);
