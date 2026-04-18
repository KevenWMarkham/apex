# APEX Changelog

## 2026-04-17 — Core v1.2: Schema Versioning Manifest

### Added
- Four-layer schema versioning manifest model (L1 contract / L2 edition catalog / L3 fleet registry / L4 tenant deployed).
- `apex-core/data/schema-manifest-contract.json` — the L1 contract defining the shape every L2 manifest must conform to.
- `apex-core/conventions/schema-versioning.md` — normative convention doc with SemVer rules, anti-cheating rules, and required/optional field default.
- `apex-core-v1.2-amendment.md` — formal amendment extending Part 11 acceptance criteria with three manifest-related checks.
- `apex-core/tools/apex-validate.js` — dual-mode validator CLI (author + fleet) writing self-contained HTML reports with APEX design-system styling.
- `apex-core/tools/apex-sync.js` — tenant-side pull CLI (status / check / plan / apply) with SemVer-to-gate routing and approval-token enforcement.
- `apex-core/tools/classify-bump.js` — SemVer bump classifier with anti-cheating rules (non-nullable add_column is MAJOR; rename is MAJOR; change_grain is MAJOR).
- `apex-core/tools/validate-manifest.js` — L2 validator enforcing 14 rules (REQ / SCHEMA / ENTITY / CHANGELOG / ENUM / SHAPE families + BUMP-MISMATCH and DETAIL-MISSING anti-cheat rules).
- `apex-core/tools/validate-fleet.js` — L3 validator enforcing opaque account IDs, policy completeness, and pin-vs-catalog consistency.
- `apex-core/tools/render-html.js` — design-system-faithful HTML report renderer.
- `apex-core/tools/ddl-driver.js` — pluggable DDL driver (no-op default; Fabric binding is a future work stream).
- `apex-fleet/data/fleet-registry.json` — seed fleet registry with two synthetic accounts.
- `apex-fleet/tools/release-bundler.js` — stub per-account bundle generator (signing is also a future work stream).
- `apex-rc/data/schemas.manifest.json` — first real L2 manifest covering MERML, SCML, CXML, MKTL with 20 entities total.

### Changed
- Every active edition spec's Part 0 inheritance line bumped from Core v1.0 / v1.1 to Core v1.2, with a manifest pointer added.
- `package.json` test-script glob hardened for Windows cmd.exe (quoted glob resolved by Node's internal matcher rather than shell).

### Deferred (explicit non-goals)
- Real Fabric DDL driver.
- Signed release bundles (currently stub).
- Tenant heartbeat endpoint.
- Power BI in-tenant view.
- Agent / ORCH / Solution Stack versioning (same pattern, separate plan).

### Testing
- 55 tests across node:test suites (contract shape, bump classification, manifest validation with enum + shape + bump-mismatch coverage, CLI exit codes, fleet-mode drift + opaque-ID, sync status/check/plan/apply with approval-token enforcement, release bundler scoping).

## 2026 — Core v1.1: Formal Edition Registry

- `apex-core/data/edition-registry.json` — machine-readable registry of active editions.
- Edition-split policy formalized.

See `apex-core-v1.1-amendment.md`.
