# APEX Fleet

Deloitte-side operational registry for the APEX client fleet. Records which client accounts are pinned to which schema versions, per edition.

## Independence posture

This folder holds *intent* (what should be deployed, per account), not *state* and not *client data*. Only three fields ever cross the tenant boundary: opaque `account_id`, `last_heartbeat_utc`, and `last_heartbeat_manifest_hash` (a SHA-256 of the tenant's L4 manifest). No row-level data, no client credentials, no runtime handles on any tenant.

## Files

- `data/fleet-registry.json` — L3 registry. Source of truth for deployment intent. Updated via pull request by Account Teams when onboarding an account or pinning a schema version.
- `tools/` — reserved for the release-bundler and related operational tools.

## Usage

- `node apex-core/tools/apex-validate.js --fleet` — validate the full registry against all edition manifests; write `fleet-report.html` + `fleet-report.json` to `apex-fleet/data/`.
- `node apex-core/tools/apex-validate.js --fleet --account acct-alpha-001` — single-account drill-down.

Conforms to the Core v1.2 contract at `apex-core/data/schema-manifest-contract.json`.
