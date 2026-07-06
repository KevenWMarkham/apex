# APEX Core Changelog

## v1.3 — 2026-07-05

- Added the **Core vs. Domain Pack factoring** convention (`conventions/core-vs-pack-factoring.md`) — normative frame-vs-knowledge split with the "would the Finance-close workspace need this, unchanged?" litmus test.
- Added L1 **pack-manifest-contract.json** — the shape of a Pack (domain workspace) manifest a domain Pack declares to Core (agent / gold-view / KPI / policy / tool descriptors), sibling to the schema-manifest contract. Documents the Core-provided contracts under `core_provides` (recommendation envelope, impact-estimate with `illustrative:true` guardrail, escalation engine, priority taxonomy, `build_workspace(pack)` shell).
- Added **validate-pack.js** (+ 14 tests, `fixtures/valid-rc.pack.json`) — enforces the L1 pack contract: required fields, `pack_code` / `gold_<domain>_v<N>` / schema-code patterns, priority enum, ≥1 agent, per-agent scenario refs, policy escalation role, one-purpose tool names, plus cross-ref warnings (agent→tool, KPI→gold-view).
- No existing edition or schema content invalidated; adoption is additive. The schema-manifest contract (v1.0) is unchanged.
- Follow-on (not in this release): the `build_workspace(pack)` runtime.

## v1.2 — 2026-04-17

- Added L1 schema-manifest-contract.json defining four-layer schema versioning.
- Extended Part 11 acceptance criteria with three manifest-related checks.
- Introduced apex-validate (dual-mode validator with HTML reports) and apex-sync (tenant-side CLI) as Core tools.
- No existing edition content invalidated; adoption is additive.

## v1.1 — (prior)

- Formal edition registry (apex-core/data/edition-registry.json).
- Edition-split policy formalized.
