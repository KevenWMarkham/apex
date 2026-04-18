#!/usr/bin/env node
/**
 * apex-sync — tenant-side CLI for comparing deployed vs pinned schema
 * versions and applying drift per the account's auto_upgrade_policy.
 *
 * Commands:
 *   apex-sync status                 Read-only 3-column table
 *   apex-sync check                  Exits 1 if drift exists (CI gate)
 *   apex-sync plan [--schema CODE]   Dry-run: show planned DDL
 *   apex-sync apply [--approve T]    Apply PATCH/MINOR; refuse MAJOR without --approve
 *
 * Env:
 *   APEX_DEPLOYED   Path to deployed-manifest.json (L4)
 *   APEX_PINNED     Path to pinned-manifest.json (slice of L3)
 *
 * Exit codes: 0 success, 1 drift (check only), 2 HITL blocked,
 *             3 DDL failed / shape error / bad args.
 */

import { readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { createHash } from 'node:crypto';
import { classifyBump } from './classify-bump.js';
import { createDdlDriver } from './ddl-driver.js';

const APPROVE_TOKEN_RE = /^ticket:\/\/CHG-\d+$/;
const DEFAULT_POLICY = { PATCH: 'ZERO_TOUCH', MINOR: 'ACK_ONLY', MAJOR: 'HITL' };

function readJson(path, label) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch (e) {
    console.error(`cannot read ${label} at ${path}: ${e.message}`);
    process.exit(3);
  }
}

function loadState() {
  const deployedPath = process.env.APEX_DEPLOYED;
  const pinnedPath = process.env.APEX_PINNED;
  if (!deployedPath || !pinnedPath) {
    console.error('APEX_DEPLOYED and APEX_PINNED env vars must be set');
    process.exit(3);
  }
  return {
    deployedPath,
    pinnedPath,
    deployed: readJson(deployedPath, 'deployed manifest'),
    pinned: readJson(pinnedPath, 'pinned manifest')
  };
}

function computeDrift(deployed, pinned) {
  const deployedBy = new Map();
  for (const s of deployed.deployed_schemas ?? []) deployedBy.set(s.code, s);
  const rows = [];
  for (const p of pinned.pinned_schemas ?? []) {
    const d = deployedBy.get(p.code);
    const deployedVersion = d ? d.version : '(none)';
    if (deployedVersion === p.version) continue;
    const changes = p.latest_changelog_entry?.changes ?? [];
    const bump = changes.length > 0 ? safeClassify(changes) : 'PATCH';
    rows.push({
      code: p.code,
      deployed: deployedVersion,
      pinned: p.version,
      bump,
      changes,
      declaredGate: p.latest_changelog_entry?.gate,
      policyGate: (pinned.auto_upgrade_policy ?? DEFAULT_POLICY)[bump] ?? DEFAULT_POLICY[bump]
    });
  }
  return rows;
}

function safeClassify(changes) {
  try {
    return classifyBump(changes);
  } catch {
    return 'PATCH';
  }
}

function cmdStatus({ deployed, pinned }) {
  const drift = computeDrift(deployed, pinned);
  const rows = (pinned.pinned_schemas ?? []).map((p) => {
    const d = (deployed.deployed_schemas ?? []).find((x) => x.code === p.code);
    const dv = d ? d.version : '(none)';
    const status = dv === p.version
      ? 'OK'
      : `${drift.find((r) => r.code === p.code)?.policyGate ?? DEFAULT_POLICY[drift.find((r) => r.code === p.code)?.bump ?? 'PATCH']} - pending`;
    return { code: p.code, deployed: dv, pinned: p.version, status };
  });
  console.log(`APEX Sync - ${deployed.account_id} - Edition: ${deployed.edition_code} - Core: ${deployed.core_version_deployed}`);
  console.log('');
  console.log('  Schema   Deployed    Pinned     Status');
  console.log('  ------   --------    ------     ----------------');
  for (const r of rows) {
    console.log(`  ${r.code.padEnd(8)} ${r.deployed.padEnd(11)} ${r.pinned.padEnd(10)} ${r.status}`);
  }
  process.exit(drift.length > 0 ? 1 : 0);
}

function cmdCheck({ deployed, pinned }) {
  const drift = computeDrift(deployed, pinned);
  process.exit(drift.length > 0 ? 1 : 0);
}

function cmdPlan({ deployed, pinned }, schemaFilter) {
  const drift = computeDrift(deployed, pinned);
  const rows = schemaFilter ? drift.filter((r) => r.code === schemaFilter) : drift;
  if (rows.length === 0) {
    console.log('apex-sync plan: no drift detected; nothing to apply.');
    process.exit(0);
  }
  for (const r of rows) {
    console.log(`[plan] ${r.code}: ${r.deployed} -> ${r.pinned}  (${r.bump} / ${r.policyGate})`);
    for (const c of r.changes) {
      console.log(`       ${c.op}  ${c.target}${c.detail ? '  -- ' + c.detail : ''}`);
    }
  }
  process.exit(0);
}

async function cmdApply({ deployed, pinned, deployedPath }, args) {
  const approveIdx = args.indexOf('--approve');
  const approveToken = approveIdx >= 0 ? args[approveIdx + 1] : undefined;

  if (approveToken !== undefined && !APPROVE_TOKEN_RE.test(approveToken)) {
    console.error(`apex-sync apply: invalid approval token ${approveToken}; expected format ticket://CHG-<number>`);
    process.exit(3);
  }

  const drift = computeDrift(deployed, pinned);
  if (drift.length === 0) {
    console.log('apex-sync apply: no drift; nothing to do.');
    process.exit(0);
  }

  const driver = createDdlDriver();
  const blocked = [];
  const applied = [];

  for (const r of drift) {
    if (r.policyGate === 'HITL' && !approveToken) {
      blocked.push(r);
      continue;
    }
    const res = await driver.apply({
      schemaCode: r.code,
      fromVersion: r.deployed,
      toVersion: r.pinned,
      changes: r.changes
    });
    if (!res.ok) {
      console.error(`apex-sync apply: DDL failed for ${r.code} (${r.deployed} -> ${r.pinned})`);
      process.exit(3);
    }
    applied.push(r);
  }

  // Update L4 with newly applied schemas.
  const byCode = new Map((deployed.deployed_schemas ?? []).map((s) => [s.code, s]));
  for (const r of applied) {
    const entry = {
      code: r.code,
      version: r.pinned,
      applied_utc: new Date().toISOString(),
      gate: r.policyGate
    };
    if (r.policyGate === 'HITL') entry.approved_by = approveToken;
    byCode.set(r.code, entry);
  }
  const updated = {
    ...deployed,
    last_applied_utc: applied.length > 0 ? new Date().toISOString() : deployed.last_applied_utc,
    deployed_schemas: Array.from(byCode.values()),
    pending_upgrades: blocked.map((r) => ({
      code: r.code,
      deployed: r.deployed,
      pinned: r.pinned,
      gate: 'HITL',
      reason: 'requires --approve ticket://CHG-<id>'
    }))
  };
  updated.manifest_hash = 'sha256:' + createHash('sha256').update(JSON.stringify(updated.deployed_schemas)).digest('hex');

  writeFileSync(deployedPath, JSON.stringify(updated, null, 2));

  for (const r of applied) {
    console.log(`[applied] ${r.code}: ${r.deployed} -> ${r.pinned} (${r.policyGate})`);
  }
  for (const r of blocked) {
    console.log(`[blocked] ${r.code}: ${r.deployed} -> ${r.pinned} (HITL - needs --approve)`);
  }

  if (blocked.length > 0) process.exit(2);
  process.exit(0);
}

async function main(argv) {
  const args = argv.slice(2);
  const cmd = args[0];

  if (!cmd) {
    console.error('usage: apex-sync <status|check|plan|apply> [opts]');
    process.exit(3);
  }

  const state = loadState();

  switch (cmd) {
    case 'status':
      return cmdStatus(state);
    case 'check':
      return cmdCheck(state);
    case 'plan': {
      const schemaIdx = args.indexOf('--schema');
      const schema = schemaIdx >= 0 ? args[schemaIdx + 1] : undefined;
      return cmdPlan(state, schema);
    }
    case 'apply':
      return cmdApply(state, args);
    default:
      console.error(`unknown command: ${cmd}`);
      process.exit(3);
  }
}

main(process.argv);
