# ADR-002 · APEX tenant manifest vs Entra Agent ID blueprints

**Status:** Accepted
**Date:** 2026-05-09
**Resolves:** Open question H.2 from the [Microsoft platform alignment delta](../../plans/2026-05-09-microsoft-platform-alignment-delta.md#h-things-to-validate-open-questions)

## Context

[APEX-M Deployment Guide §3](../../book/Professional-APEX-M-Deployment-Guide.html#ch-3) defines a "tenant manifest" — a YAML artifact that declares the tenant's substrate tier, capacity SKU, identity bindings, and contracts with each Service. It predates Microsoft Entra Agent ID (GA April 2026), which introduces its own first-class concept of **agent identity blueprints** with parent-child relationships, role assignments, lifecycle policy, and Conditional Access bindings.

Question: Does the APEX tenant manifest still earn its keep?

## Decision

**Keep the APEX tenant manifest. It's a different abstraction layer.**

| Concern | Tenant manifest | Entra Agent ID blueprint |
|---|---|---|
| Substrate (lab/dev/stage/prod/pilot/ga) | ✓ | — |
| Fabric capacity SKU | ✓ | — |
| Service-code wave assignments (W1/W2/W3 per service) | ✓ | — |
| Persona registry references | ✓ | — |
| KPI registry references | ✓ | — |
| Agent identity governance + CA + lifecycle | — | ✓ |
| Role assignments on Microsoft resources | — | ✓ |
| Identity hierarchy (parent → child) | — | ✓ |

The two artifacts answer different questions: the tenant manifest is *deployment-time configuration*; the blueprint is *identity-runtime governance*. There is overlap (both touch identity refs), but the overlap is small and benign.

What we **do** simplify: the tenant manifest's `identities:` section now references blueprint ids by name (`apex-m-tenant-root`, `apex-m-rc-e2e-03-blueprint`) instead of redeclaring the identity bindings. Single source of truth for identity moves to Entra Agent ID; tenant manifest becomes a *thin pointer* into the blueprint hierarchy.

## Consequences

- Tenant manifest stays in `apex-workspace/manifest.json` (per Roadmap.md BL.P.04) but its `identities:` block shrinks to ~5 fields (blueprint refs + tenant-id + region) instead of ~20 (per-identity declarations).
- Blueprint provisioning becomes the *canonical* identity setup path; tenant-manifest deployment is *idempotent* with respect to it (re-running tenant-manifest deploy doesn't recreate blueprints, just verifies they exist).
- Updated [agent-identity-blueprints.md](../agent-identity-blueprints.md) §3 documents the cross-reference contract.

## Status

Accepted. Tenant-manifest schema update is a Phase I.1 follow-up sprint; Roadmap.md BL.P.04 stays open as an iteration on the existing manifest schema rather than a rewrite.
