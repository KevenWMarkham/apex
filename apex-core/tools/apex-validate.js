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

import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { resolve, basename } from 'node:path';
import { validateManifest } from './validate-manifest.js';
import { validateFleet } from './validate-fleet.js';
import { buildReport } from './report.js';
import { renderHtml } from './render-html.js';

function parseAccountFilter(args) {
  const i = args.indexOf('--account');
  if (i === -1) return undefined;
  return args[i + 1];
}

function discoverEditionManifests(repoRoot) {
  const editions = new Map();
  for (const name of readdirSync(repoRoot)) {
    if (!name.startsWith('apex-') || name === 'apex-core' || name === 'apex-fleet') continue;
    try {
      const mPath = resolve(repoRoot, name, 'data', 'schemas.manifest.json');
      const m = JSON.parse(readFileSync(mPath, 'utf8'));
      if (m.edition_code) editions.set(m.edition_code, m);
    } catch {
      // Edition folder without a manifest — skip silently; the fleet check
      // will flag any account pinning an unknown edition.
    }
  }
  return editions;
}

function runFleetMode({ ci, accountFilter }) {
  const repoRoot = resolve(fileURLRoot(), '..', '..');
  const registryPath = resolve(repoRoot, 'apex-fleet/data/fleet-registry.json');

  let registry;
  try {
    registry = JSON.parse(readFileSync(registryPath, 'utf8'));
  } catch (e) {
    console.error(`cannot read fleet registry at ${registryPath}: ${e.message}`);
    process.exit(3);
  }

  const editionManifests = discoverEditionManifests(repoRoot);
  const { findings, drift } = validateFleet(registry, editionManifests, { accountFilter });

  const report = buildReport({
    editionCode: 'FLEET',
    editionFolder: resolve(repoRoot, 'apex-fleet'),
    manifestPath: registryPath,
    findings
  });
  report.drift = drift;
  if (accountFilter) report.account_filter = accountFilter;

  const outDir = resolve(repoRoot, 'apex-fleet/data');
  writeFileSync(resolve(outDir, 'fleet-report.json'), JSON.stringify(report, null, 2));
  writeFileSync(resolve(outDir, 'fleet-report.html'), renderHtml(report));

  if (ci) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    const c = report.summary.critical ?? 0;
    const w = report.summary.warning ?? 0;
    console.log(`apex-validate --fleet: ${report.status.toUpperCase()} · critical=${c} warning=${w} · ${drift.length} drift row(s)`);
  }

  if ((report.summary.critical ?? 0) > 0) process.exit(2);
  if ((report.summary.warning ?? 0) > 0) process.exit(1);
  process.exit(0);
}

function fileURLRoot() {
  return new URL('.', import.meta.url).pathname.replace(/^\/([a-zA-Z]:)/, '$1');
}

function main(argv) {
  const args = argv.slice(2);
  const ci = args.includes('--ci');

  if (args.includes('--fleet')) {
    const accountFilter = parseAccountFilter(args);
    return runFleetMode({ ci, accountFilter });
  }

  const target = args.find((a) => !a.startsWith('--') && !(args[args.indexOf(a) - 1] === '--account'));

  if (!target) {
    console.error('usage: apex-validate [--ci] <edition-folder>\n       apex-validate --fleet [--account <id>] [--ci]');
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
  writeFileSync(
    resolve(editionFolder, 'data/report.html'),
    renderHtml(report)
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
