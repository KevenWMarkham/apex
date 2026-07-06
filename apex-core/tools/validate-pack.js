import semver from 'semver';

// Pack code — same family as edition_code but allowing up to 4 chars.
const PACK_CODE_RE = /^[A-Z]{2,4}$/;
// Gold view — the provenance surface `gold_<domain>_v<N>`.
const GOLD_VIEW_RE = /^gold_[a-z0-9_]+_v[0-9]+$/;
// Schema code — mirrors validate-manifest.js (the doc's own examples, e.g.
// MERML/SCML, need 4-6 total chars: 2-4 domain letters + `ML`|`L`).
const SCHEMA_CODE_RE = /^[A-Z]{2,4}(ML|L)$/;

const PRIORITIES = ['Differentiate', 'Optimize', 'Grow'];

/**
 * Validate an L2 Pack (domain workspace) manifest against the L1
 * pack-manifest-contract.json shape.
 *
 * A Pack declares only the seam to Core — agent / gold-view / KPI / policy /
 * tool descriptors. Core provides the recommendation envelope, escalation
 * engine, and build_workspace(pack) shell; this validator does NOT check
 * those (they are Core-owned, not Pack-declared).
 *
 * Returns a flat findings array; consumers inspect `severity`
 * ("critical" vs "warning") and `rule`.
 *
 * @param {object} manifest  Parsed Pack manifest JSON object.
 * @returns {{ findings: Array<{severity: string, rule: string, path: string, message: string}> }}
 */
export function validatePack(manifest) {
  if (!manifest || typeof manifest !== 'object' || Array.isArray(manifest)) {
    return {
      findings: [{
        severity: 'critical',
        rule: 'SHAPE-ROOT',
        path: '$',
        message: 'pack manifest must be a JSON object'
      }]
    };
  }

  const findings = [];
  const crit = (rule, path, message) =>
    findings.push({ severity: 'critical', rule, path, message });
  const warn = (rule, path, message) =>
    findings.push({ severity: 'warning', rule, path, message });

  // REQ-01..REQ-10: top-level required fields.
  for (const [field, rule] of [
    ['pack_code', 'REQ-01'],
    ['core_version_required', 'REQ-02'],
    ['manifest_version', 'REQ-03'],
    ['domain', 'REQ-04'],
    ['priority', 'REQ-05'],
    ['agents', 'REQ-06'],
    ['gold_views', 'REQ-07'],
    ['kpis', 'REQ-08'],
    ['policies', 'REQ-09'],
    ['tools', 'REQ-10']
  ]) {
    if (manifest[field] === undefined || manifest[field] === null) {
      crit(rule, `$.${field}`, `missing required field ${field}`);
    }
  }

  if (manifest.pack_code && !PACK_CODE_RE.test(manifest.pack_code)) {
    crit('REQ-01-PATTERN', '$.pack_code', 'pack_code must match /^[A-Z]{2,4}$/');
  }
  if (manifest.core_version_required && !semver.valid(semver.coerce(manifest.core_version_required) || '')) {
    crit('REQ-02-SEMVER', '$.core_version_required', 'core_version_required must be valid SemVer');
  }
  if (manifest.manifest_version && !semver.valid(manifest.manifest_version)) {
    crit('REQ-03-SEMVER', '$.manifest_version', 'manifest_version must be valid SemVer');
  }
  if (manifest.priority !== undefined && !PRIORITIES.includes(manifest.priority)) {
    crit('ENUM-PRIORITY', '$.priority', `priority must be one of ${PRIORITIES.join(', ')}; got ${manifest.priority}`);
  }

  // Registered names for cross-reference checks.
  const goldViews = Array.isArray(manifest.gold_views) ? manifest.gold_views : [];
  const registeredViews = new Set(goldViews.map((g) => g && g.view).filter(Boolean));
  const tools = Array.isArray(manifest.tools) ? manifest.tools : [];
  const registeredTools = new Set(tools.map((t) => t && t.name).filter(Boolean));

  // --- agents ------------------------------------------------------------
  const agents = Array.isArray(manifest.agents) ? manifest.agents : [];
  if (manifest.agents !== undefined && !Array.isArray(manifest.agents)) {
    crit('SHAPE-AGENTS', '$.agents', 'agents must be an array');
  } else if (agents.length < 1) {
    crit('AGENTS-COUNT', '$.agents', 'a pack must declare at least 1 agent');
  }
  for (const [i, a] of agents.entries()) {
    const p = `$.agents[${i}]`;
    if (!a || !a.name) crit('AGENT-NAME', `${p}.name`, 'agent name is required');
    if (!a || !a.group) crit('AGENT-GROUP', `${p}.group`, 'agent group (rail label) is required');
    if (!a || !Array.isArray(a.scenario_ids) || a.scenario_ids.length < 1) {
      crit('AGENT-SCENARIOS', `${p}.scenario_ids`, 'agent must reference at least 1 scenario_id');
    }
    if (a && a.priority !== undefined && !PRIORITIES.includes(a.priority)) {
      crit('AGENT-PRIORITY', `${p}.priority`, `agent priority must be one of ${PRIORITIES.join(', ')}; got ${a.priority}`);
    }
    for (const [j, tname] of (a && Array.isArray(a.tools) ? a.tools : []).entries()) {
      if (!registeredTools.has(tname)) {
        warn('AGENT-TOOL-REF', `${p}.tools[${j}]`, `agent references tool '${tname}' not registered in $.tools`);
      }
    }
  }

  // --- gold_views --------------------------------------------------------
  if (manifest.gold_views !== undefined && !Array.isArray(manifest.gold_views)) {
    crit('SHAPE-GOLDVIEWS', '$.gold_views', 'gold_views must be an array');
  } else if (goldViews.length < 1) {
    crit('GOLDVIEWS-COUNT', '$.gold_views', 'a pack must register at least 1 gold view');
  }
  for (const [i, g] of goldViews.entries()) {
    const p = `$.gold_views[${i}]`;
    if (!g || !GOLD_VIEW_RE.test(g.view || '')) {
      crit('GOLD-VIEW-PATTERN', `${p}.view`, `view must match /^gold_<domain>_v<N>$/; got ${g && g.view}`);
    }
    if (g && g.schema_code !== undefined && !SCHEMA_CODE_RE.test(g.schema_code)) {
      crit('GOLD-SCHEMA-CODE', `${p}.schema_code`, `invalid schema_code ${g.schema_code}`);
    }
    if (g && g.version !== undefined && !semver.valid(g.version)) {
      crit('GOLD-VERSION-SEMVER', `${p}.version`, 'gold view version must be valid SemVer');
    }
  }

  // --- kpis --------------------------------------------------------------
  const kpis = Array.isArray(manifest.kpis) ? manifest.kpis : [];
  for (const [i, k] of kpis.entries()) {
    const p = `$.kpis[${i}]`;
    if (!k || !k.label) crit('KPI-LABEL', `${p}.label`, 'kpi label is required');
    if (!k || !GOLD_VIEW_RE.test(k.source_view || '')) {
      crit('KPI-SOURCE-PATTERN', `${p}.source_view`, `kpi source_view must match /^gold_<domain>_v<N>$/; got ${k && k.source_view}`);
    } else if (!registeredViews.has(k.source_view)) {
      warn('KPI-SOURCE-REF', `${p}.source_view`, `kpi source_view '${k.source_view}' not registered in $.gold_views`);
    }
  }

  // --- policies ----------------------------------------------------------
  const policies = Array.isArray(manifest.policies) ? manifest.policies : [];
  for (const [i, pol] of policies.entries()) {
    const p = `$.policies[${i}]`;
    if (!pol || !pol.name) crit('POLICY-NAME', `${p}.name`, 'policy name is required');
    if (!pol || !pol.metric) crit('POLICY-METRIC', `${p}.metric`, 'policy metric is required');
    if (!pol || pol.threshold === undefined) crit('POLICY-THRESHOLD', `${p}.threshold`, 'policy threshold is required');
    if (!pol || !pol.escalate_to_role) {
      crit('POLICY-ESCALATE', `${p}.escalate_to_role`, 'policy escalate_to_role is required (escalation targets a named human role)');
    }
  }

  // --- tools -------------------------------------------------------------
  for (const [i, t] of tools.entries()) {
    const p = `$.tools[${i}]`;
    if (!t || !t.name) crit('TOOL-NAME', `${p}.name`, 'tool name is required (one-tool-one-purpose)');
    if (t && t.hitl_required !== undefined && typeof t.hitl_required !== 'boolean') {
      crit('TOOL-HITL-BOOL', `${p}.hitl_required`, 'hitl_required must be a boolean');
    }
    if (t && t.gold_writes !== undefined && !Array.isArray(t.gold_writes)) {
      crit('TOOL-GOLDWRITES-ARRAY', `${p}.gold_writes`, 'gold_writes must be an array');
    }
  }

  return { findings };
}
