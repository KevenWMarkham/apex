// DEPRECATED: This module is retained for backward compatibility only.
// Use validate-practice.js instead. This shim will be removed in Core v1.3.
//
// The L3 layer was renamed from "Fleet" to "Practice" in Core v1.2.1 to
// reflect that L3 bundles schemas, agents, MCP tools, orchestrations, gates,
// services, personas, and KPIs — not just agents.
import { validatePractice } from './validate-practice.js';

export function validateFleet(registry, editionManifests, opts = {}) {
  const result = validatePractice(registry, editionManifests, opts);
  return {
    ...result,
    findings: result.findings.map(f => ({
      ...f,
      rule: f.rule.replace(/^PRACTICE-/, 'FLEET-')
    }))
  };
}
