# DEP-006 · Audit-row HMAC as system of record → Microsoft Purview Audit + DSPM for AI

**Status:** Deprecated as system of record (kept as KPI-attribution overlay)
**Date:** 2026-05-09
**Supersedes:** Roadmap.md BL.P.84 (Row signing + hashing) as the *system of record* — the implementation stays as overlay
**Related:** [ADR-003](../adr/ADR-003-audit-row-vs-purview-audit.md)

## What APEX was building

A 14-field audit-row schema with HMAC signing, content-addressed input/output hashes, three-version stamps (manifest / policy / prompt), and downstream-effect cross-references — designed to be the **system of record** for every agent decision (Roadmap.md BL.P.77–84).

## What Microsoft shipped

**Microsoft Purview Audit** (GA) + **DSPM for AI Activity Explorer** (GA) capture every AI interaction natively:

- [Audit logs for Copilot and AI activities](https://learn.microsoft.com/purview/audit-copilot)
- [Microsoft Purview for Agent 365](https://learn.microsoft.com/purview/ai-agent-365)
- [Microsoft Purview for Microsoft Foundry](https://learn.microsoft.com/purview/ai-azure-foundry)

What Purview Audit provides that the bespoke schema cannot:
- Microsoft-managed retention with first-party WORM contract
- Tamper protection without APEX managing keys
- DSPM for AI Activity Explorer cross-references (sensitivity-label-aware)
- Cross-tenant audit-search standardization (Microsoft Sentinel + eDiscovery integration)
- Recognized-by-auditors audit posture

## Migration path

Documented in detail in [ADR-003](../adr/ADR-003-audit-row-vs-purview-audit.md). Summary:

1. **Purview Audit becomes primary** (system of record). APEX-M agents emit through the Foundry hosted-agent runtime, which writes Purview Audit events natively.
2. **APEX audit-row schema demotes to KPI-attribution overlay** (`is_primary=False`). Keeps the `decision_ledger_id` foreign key into Purview, plus the APEX-specific fields (`service_code`, `scenario_id`, `agent_id`, KPI joins) that Purview doesn't model.
3. **HMAC signing of the overlay** stays — still the right WORM protection for the overlay row — but is no longer the audit defense. Purview Audit's tamper protection is.
4. APEX-Core's `AuditLedger` protocol's `is_primary: bool` field surfaces the split; concrete impls of secondary ledgers (e.g., Splunk SIEM via `siem.splunk` adapter) are also `is_primary=False`.

## Independence implications

None. Microsoft Purview is part of the client's existing tenant.

## Engineering implications

**Net-positive.** APEX no longer needs to maintain:

- Signing-key rotation for the audit-row HMAC
- Immutability proofs for compliance audits
- Retention enforcement code paths
- Tamper-detection alerting

All of these become Microsoft's responsibility under Purview Audit. APEX retains responsibility only for the KPI-attribution overlay, which is a much smaller surface.

## What stays

`apex-audit` package (BL.P.77–84) keeps its code; the field set, signing, and content-addressed store all stay. The change is **operational and semantic**: the package is now a KPI-attribution overlay, not the system of record. Roadmap.md amendment in Phase I.3 follow-up sprint reflects this.
