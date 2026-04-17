# APEX Schema Versioning Convention

**Status:** Normative. Applies to APEX Core v1.2 and later.
**Scope:** Schema versioning and deployment visibility only. Does not cover agent, orchestration, or Solution Stack versioning.

---

## Purpose

APEX editions define 3-5 canonical schemas each. These schemas are the data grammar that agents and orchestrations contract against. When a schema changes, consumers need a stable version number to pin against, a machine-readable record of what changed at entity granularity, and a view of what is deployed where across the client fleet. This convention establishes the four-layer manifest model that delivers those three things, the SemVer rules that govern every bump, and the default conventions a downstream validator relies on when reading the L1 contract.

---

## The Four Layers

Each layer is owned by a different stakeholder and written as JSON conforming to the layer above it.

| Layer | File | Owner | Purpose |
|---|---|---|---|
| **L1 - Contract** | `apex-core/data/schema-manifest-contract.json` | APEX SteerCo (Core maintainers) | Defines the shape, required fields, and SemVer rules every downstream manifest must obey. |
| **L2 - Edition catalog** | `apex-<code>/data/schemas.manifest.json` | Edition maintainers | Declares the schemas this edition offers and the SemVer of each. Carries the full entity-level changelog. |
| **L3 - Fleet registry** | `apex-fleet/data/fleet-registry.json` | DMTSP Account Teams (Deloitte-side) | Source of truth for which client accounts are pinned to which schema versions, plus per-account upgrade policy. |
| **L4 - Tenant deployed manifest** | `<client-onelake>/apex-sync/deployed-manifest.json` | Client tenant (written by the pull pipeline) | Read-only record of what is currently running in that one tenant. Never leaves the tenant. |

The design doc at `docs/plans/2026-04-17-schema-versioning-manifest-design.md` covers the rationale for four layers, the distribution pattern (GitOps-style pull, no push), and the Independence posture that makes L4 tenant-local.

---

## SemVer Rules (Normative)

The validator and `apex-sync` both depend on these rules. Every schema PR must declare the bump; the validator verifies the declared bump matches the actual delta against the previous version.

### Decision table

| Bump | Triggered by any of | Gate |
|---|---|---|
| **MAJOR** | `remove_entity`, `rename_entity`, `remove_column`, `change_type`, `change_pk`, `change_grain`, toggling `envelope_required`, dropping Core version compatibility, adding a non-nullable column | `HITL` |
| **MINOR** | `add_entity`, `add_column` with `NULL` allowed, new Gold view contract, new dimensional anchor, new controlled-vocabulary value in `business_step`/`disposition`, `deprecated_in` marker added to an entity or column | `ACK_ONLY` |
| **PATCH** | `metadata` only: description text, comment, grain clarification that preserves the same grain, PII classification refinement, formatting | `ZERO_TOUCH` |

---

## Anti-Cheating Rules

1. **Adding a non-nullable column is MAJOR.** It breaks inserts from existing producers. If you want a non-nullable column in practice, do it in two steps: MINOR to add it as nullable with a default-populator, then MAJOR in a later release to tighten the constraint.
2. **Renaming is MAJOR.** Never rename in place. The required pattern is: MINOR to add the new name with the same grain, MINOR to mark the old name `deprecated_in`, MAJOR in a later release to remove it.
3. **Grain refinements that change the grain are MAJOR.** Clarifying prose in the `grain` string without changing what the grain actually *is* is PATCH.
4. **Core version compatibility.** If `core_version_required` increases by MAJOR, every schema in the edition manifest inherits a MAJOR on its next release.

### Event envelope

The shared canonical event envelope is versioned by Core, not by edition manifests. Editions declare `envelope_required: true` on every schema that uses it. If Core MAJOR-bumps the envelope, editions must MAJOR-bump every affected schema in their next release cycle.

---

## Required / Optional Field Default Convention

The L1 contract (`apex-core/data/schema-manifest-contract.json`) marks some fields with `"required": true` and some with `"optional": true`, but most are unflagged. To prevent ambiguity when the validator reads the contract, the following default convention is normative:

- Fields listed under the top-level `required_fields` block are **required** in every manifest.
- Within each template (`schema_entry`, `entity_entry`, `change_entry`, `change_delta`), a field is **required** unless it carries `"optional": true`. The explicit `"required": true` flag is for emphasis only; its absence does not mean optional.
- The only explicitly optional field in the current contract (v1.0) is `entity_entry.deprecated_in`.

This is the normative rule. Future L1 contract versions may change the convention - if so, the change must appear here first.

---

## References

- Amendment landing this convention: `apex-core-v1.2-amendment.md`
- Full design and rationale: `docs/plans/2026-04-17-schema-versioning-manifest-design.md`
- L1 contract artifact: `apex-core/data/schema-manifest-contract.json`
- Prior amendment precedent: `apex-core-v1.1-amendment.md`

---

**End of APEX Schema Versioning Convention**
