# APEX — Agentic Platform for Enterprise eXecution

APEX is a domain-canonical reference framework for deploying agentic AI on Microsoft-native infrastructure. This repository hosts the build specs for APEX Core and its industry editions, along with the schema-versioning tooling introduced in Core v1.2.

## Structure

- `apex-core-build-spec.md` — the parent spec (Core). Defines conventions inherited by every edition.
- `apex-core-v1.1-amendment.md`, `apex-core-v1.2-amendment.md` — formal amendments to Core.
- `apex-<code>-build-spec*.md` — edition specs (RC, ER, HLS, ICE, TH, TMT).
- `apex-core/` — Core-owned artifacts: L1 manifest contract, conventions, shared tools.
- `apex-rc/`, `apex-th/`, ... — edition-owned folders with their L2 manifest (`data/schemas.manifest.json`).
- `apex-fleet/` — Deloitte-side fleet registry (L3) and release bundler.
- `docs/plans/` — design docs and implementation plans.

## Schema versioning (Core v1.2)

Four-layer manifest model: L1 contract (Core) → L2 edition catalog → L3 fleet registry → L4 tenant deployed manifest. GitOps-style pull distribution. Independence-safe.

Design: `docs/plans/2026-04-17-schema-versioning-manifest-design.md`
Implementation plan: `docs/plans/2026-04-17-schema-versioning-manifest-implementation.md`

## Tools

- `node apex-core/tools/apex-validate.js <edition>` — validate an edition's L2 manifest. Writes `report.html` + `report.json`.
- `node apex-core/tools/apex-validate.js --fleet` — validate the fleet registry against all edition manifests.
- `node apex-core/tools/apex-sync.js <status|check|plan|apply>` — tenant-side pull agent. Requires `APEX_DEPLOYED` and `APEX_PINNED` env vars.
- `node apex-fleet/tools/release-bundler.js` — assemble per-account signed bundles from the fleet registry.

## Development

```
npm install        # installs semver (only runtime dep)
npm test           # runs all node:test suites (55 tests at v1.2 landing)
```
