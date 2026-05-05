# apex-audit

Sprint 12 — Decision Audit Row.

Closes **BL.P.77–P.84**:

- 14-field immutable audit-row schema (`AuditRow`)
- Trace-ID discipline: runtime rejects emissions missing `trace_id`
- Three-version rule: `manifest_version` + `policy_version` + `prompt_version` stamped at pre-invocation
- Reasoning-trace capture with DLP scrub (sensitive tokens never inline)
- Orchestration composite row (parent references participating agents via shared `trace_id`)
- Content-addressed I/O store (inputs/outputs by hash)
- HMAC-SHA256 row signing + tamper-evidence verification

## Scope

This package produces and validates the row; `ledger-mcp` is the append store.
