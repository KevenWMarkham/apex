# APEX Schema Versioning — Manifest Design & Update Process

**Document class:** APEX Core design proposal (will land as Core v1.2 amendment)
**Date:** 2026-04-17
**Status:** Draft for SteerCo review
**Supersedes:** Nothing; additive to Core v1.1
**Downstream impact:** All active editions (RC, TH, HLS, TMT, ER, ICE); no content invalidation

---

## Part 0 — Compliance & Language Constraints (Inherited)

This document inherits Part 0 of APEX Core v1.0 unchanged. Every restriction on terminology, PII, and Independence posture applies here. In particular:

- **Independence posture:** the fleet-registry and any distribution channel described below must not retain client-identifiable data on the Deloitte side. Only manifest hashes, pinned versions, and opaque account IDs travel across the boundary.
- **Terminology:** the usual forbidden terms (partner, alliance, strategic alliance) do not appear here and must not appear in any derived artifacts.
- **PII:** all example data in this document (account IDs, hashes, ticket IDs) is synthetic and clearly fictional.

---

## Part 1 — Why This Exists

APEX editions define 3–5 canonical schemas each (MERML, SCML, CXML, MKTL in RC; HOSML, REVML, etc. in TH; and so on). These schemas are the data grammar that agents and orchestrations contract against. When a schema changes — an entity is added, a grain is refined, a column is deprecated — consumers need three things:

1. **A stable version number** that agents and ORCH contracts can pin against.
2. **A record of what actually changed** between two versions, machine-readable, at entity granularity.
3. **A view of what is deployed where** across the client fleet, so Account Teams can coordinate upgrades and detect drift.

Today none of these exist as first-class artifacts. Schema changes propagate by PR review and tribal memory. This design closes that gap using the same inheritance model APEX Core v1.1 established for the edition registry — Core owns the contract, editions own the content, a new fleet layer records deployment state, and a validation tool surfaces the whole picture.

The design is deliberately narrow in scope: **schema versioning and deployment visibility only.** It does not version agents, orchestrations, or Solution Stack rows. Those are separate concerns that can adopt the same pattern later if useful.

---

## Part 2 — The Layered Manifest Model

Four layers. Each owned by a different stakeholder. Each written as JSON conforming to the layer above it.

### 2.1 Layer summary

| Layer | File | Owner | Purpose | Lifecycle |
|---|---|---|---|---|
| **L1 — Contract** | `apex-core/data/schema-manifest-contract.json` | APEX SteerCo (Core maintainers) | Defines the shape, required fields, and SemVer rules every downstream manifest must obey. Versioned with Core. | Changes rarely; every change is a Core amendment. |
| **L2 — Edition catalog** | `apex-<code>/data/schemas.manifest.json` | Edition maintainers (one per edition) | Declares the schemas this edition offers and the SemVer of each (e.g., MERML@1.3.0, SCML@1.0.0). Carries the full entity-level changelog. | Changes with every schema bump. |
| **L3 — Fleet registry** | `apex-fleet/data/fleet-registry.json` (new Deloitte-side repo or subfolder) | DMTSP Account Teams | Source of truth for which client accounts are pinned to which schema versions, plus per-account upgrade policy. | Changes when an account is onboarded, a version is pinned, or a heartbeat is recorded. |
| **L4 — Tenant deployed manifest** | `<client-onelake>/apex-sync/deployed-manifest.json` | Client tenant (written by pull pipeline) | Read-only record of what is currently running in that one tenant. Read by the in-tenant Power BI view. Never leaves the tenant. | Rewritten on every successful `apex-sync apply`. |

### 2.2 Why four layers, not fewer

- **Separating L1 from L2** mirrors the Core v1.1 `edition-registry.json` precedent. Core defines grammar; editions populate. Anyone fluent in APEX already recognizes this pattern.
- **L3 is its own layer** because fleet state is a Deloitte operational concern, not an edition-authoring concern. Keeping it separate prevents client onboarding churn from polluting edition spec history.
- **L4 exists because of Independence.** The tenant must own its own state locally; the fleet registry only holds the *intent* (what should be deployed) and a hash of the last heartbeat (what actually is). No data flows out of the tenant except the hash.

### 2.3 Distribution pattern — GitOps-style pull, no push

The Git repository containing L1, L2, and L3 is the authoritative source. On merge to `main`:

1. A release job assembles a per-account manifest bundle by filtering L3 to each account's entry.
2. Each bundle is signed and published to an Azure DevOps artifact feed (or equivalent signed release channel).
3. Each client tenant runs a scheduled Logic App or Fabric Data Factory pipeline that pulls *only its own bundle* (scoped by tenant ID on the release side) and applies it locally.

Deloitte does not push to tenants. Deloitte does not hold tenant credentials. The pattern is GitOps — declarative artifacts in Git, reconciled by a pull agent — applied to data schemas instead of Kubernetes manifests.

---

## Part 3 — Manifest Shapes

The four JSON shapes below are the contracts. Full examples; fields can grow in MINOR bumps of the contract itself.

### 3.1 L1 — Contract

```json
{
  "contract_version": "1.0",
  "core_version": "1.2",
  "last_updated": "2026-04-17",
  "required_fields": {
    "edition_code": { "type": "string", "pattern": "^[A-Z]{2,3}$" },
    "core_version_required": { "type": "semver" },
    "manifest_version": { "type": "semver" },
    "schemas": { "type": "array", "min_items": 3, "max_items": 5 }
  },
  "schema_entry": {
    "code":                { "type": "string", "pattern": "^[A-Z]{4,5}(ML|L)$" },
    "version":             { "type": "semver", "required": true },
    "domain":              { "type": "string", "required": true },
    "entity_count":        { "type": "integer", "min": 1 },
    "entities":            { "type": "array", "items": "entity_entry" },
    "changelog":           { "type": "array", "items": "change_entry" },
    "envelope_required":   { "type": "boolean", "default": true }
  },
  "entity_entry": {
    "name":           { "type": "string", "pattern": "^[A-Z_]+$" },
    "layer":          { "type": "enum", "values": ["Bronze", "Silver", "Gold"] },
    "grain":          { "type": "string", "required": true },
    "primary_key":    { "type": "array", "min_items": 1 },
    "scd2":           { "type": "boolean" },
    "pii_classes":    { "type": "array" },
    "added_in":       { "type": "semver" },
    "deprecated_in":  { "type": "semver", "optional": true }
  },
  "change_entry": {
    "version":     { "type": "semver" },
    "bump":        { "type": "enum", "values": ["MAJOR", "MINOR", "PATCH"] },
    "gate":        { "type": "enum", "values": ["HITL", "ACK_ONLY", "ZERO_TOUCH"] },
    "date":        { "type": "date" },
    "author":      { "type": "string" },
    "rationale":   { "type": "string" },
    "changes":     { "type": "array", "items": "change_delta" }
  },
  "change_delta": {
    "op": {
      "type": "enum",
      "values": [
        "add_entity", "remove_entity", "rename_entity",
        "add_column", "remove_column", "change_type",
        "change_pk", "change_grain", "metadata"
      ]
    },
    "target": { "type": "string" },
    "detail": { "type": "string" }
  }
}
```

### 3.2 L2 — Edition manifest (RC example)

```json
{
  "edition_code": "RC",
  "core_version_required": "1.2",
  "manifest_version": "1.0.0",
  "last_updated": "2026-04-17",
  "schemas": [
    {
      "code": "MERML",
      "version": "1.3.0",
      "domain": "Merchandising",
      "entity_count": 40,
      "envelope_required": true,
      "changelog": [
        {
          "version": "1.3.0",
          "bump": "MINOR",
          "gate": "ACK_ONLY",
          "date": "2026-04-10",
          "author": "rc-maintainers",
          "rationale": "Planogram compliance telemetry now sourced from shelf CV feed.",
          "changes": [
            { "op": "add_entity", "target": "PLANOGRAM_COMPLIANCE_EVENT", "detail": "Silver; grain=per shelf audit" },
            { "op": "add_column", "target": "STORE_INVENTORY_POSITION", "detail": "expected_facings INT NULL" }
          ]
        },
        {
          "version": "1.2.0",
          "bump": "MINOR",
          "gate": "ACK_ONLY",
          "date": "2026-02-18",
          "rationale": "Markdown lifecycle now instrumented end-to-end.",
          "changes": [
            { "op": "add_entity", "target": "MARKDOWN_EVENT", "detail": "Silver; markdown lifecycle" }
          ]
        },
        {
          "version": "1.0.0",
          "bump": "MAJOR",
          "gate": "HITL",
          "date": "2026-01-01",
          "rationale": "Initial GA release.",
          "changes": [ { "op": "metadata", "target": "schema", "detail": "initial GA release" } ]
        }
      ],
      "entities": [
        {
          "name": "STORE_INVENTORY_POSITION",
          "layer": "Silver",
          "grain": "store × product × timestamp",
          "primary_key": ["store_id", "product_id", "event_ts"],
          "scd2": false,
          "pii_classes": [],
          "added_in": "1.0.0"
        },
        {
          "name": "MARKDOWN_EVENT",
          "layer": "Silver",
          "grain": "product × store × markdown cycle",
          "primary_key": ["markdown_id"],
          "scd2": false,
          "pii_classes": [],
          "added_in": "1.2.0"
        },
        {
          "name": "PLANOGRAM_COMPLIANCE_EVENT",
          "layer": "Silver",
          "grain": "shelf audit event",
          "primary_key": ["audit_id"],
          "scd2": false,
          "pii_classes": [],
          "added_in": "1.3.0"
        }
      ]
    },
    { "code": "SCML", "version": "1.0.0", "domain": "Supply Chain", "entity_count": 35, "envelope_required": true, "changelog": [], "entities": [] },
    { "code": "CXML", "version": "1.1.0", "domain": "Customer Experience", "entity_count": 30, "envelope_required": true, "changelog": [], "entities": [] },
    { "code": "MKTL", "version": "1.0.0", "domain": "Marketing", "entity_count": 25, "envelope_required": true, "changelog": [], "entities": [] }
  ]
}
```

### 3.3 L3 — Fleet registry

```json
{
  "registry_version": "1.0.0",
  "last_updated": "2026-04-17",
  "accounts": [
    {
      "account_id": "acct-alpha-001",
      "account_alias": "Alpha Retail",
      "edition_code": "RC",
      "core_version": "1.2",
      "wave_stage": "W2",
      "quiet_window_hours_local": "02:00-04:00",
      "heartbeat_sla_hours": 48,
      "auto_upgrade_policy": {
        "PATCH": "ZERO_TOUCH",
        "MINOR": "ACK_ONLY",
        "MAJOR": "HITL"
      },
      "pinned_schemas": [
        { "code": "MERML", "version": "1.3.0" },
        { "code": "SCML",  "version": "1.0.0" },
        { "code": "CXML",  "version": "1.1.0" },
        { "code": "MKTL",  "version": "1.0.0" }
      ],
      "last_heartbeat_utc": "2026-04-17T03:12:00Z",
      "last_heartbeat_manifest_hash": "sha256:ab12cd34..."
    }
  ]
}
```

Note: `account_id` is opaque; `account_alias` is a Deloitte-side label; `last_heartbeat_manifest_hash` is a SHA-256 of the tenant's L4 file as it stood at its last heartbeat — the only thing besides the ID that crosses the tenant boundary.

### 3.4 L4 — Tenant deployed manifest

```json
{
  "account_id": "acct-alpha-001",
  "edition_code": "RC",
  "core_version_deployed": "1.2",
  "last_applied_utc": "2026-04-17T03:14:22Z",
  "applied_by": "fabric-pipeline://apex-sync-nightly",
  "deployed_schemas": [
    { "code": "MERML", "version": "1.3.0", "applied_utc": "2026-04-17T03:14:15Z", "gate": "ACK_ONLY" },
    { "code": "SCML",  "version": "1.0.0", "applied_utc": "2026-01-05T02:30:00Z", "gate": "HITL", "approved_by": "ticket://CHG-4411" },
    { "code": "CXML",  "version": "1.1.0", "applied_utc": "2026-03-02T02:30:00Z", "gate": "ACK_ONLY" },
    { "code": "MKTL",  "version": "1.0.0", "applied_utc": "2026-01-05T02:30:00Z", "gate": "HITL", "approved_by": "ticket://CHG-4411" }
  ],
  "pending_upgrades": [],
  "manifest_hash": "sha256:ab12cd34..."
}
```

---

## Part 4 — SemVer Rules (Normative)

The validator and `apex-sync` both depend on these rules. Every schema PR must declare the bump; the validator verifies the declared bump matches the actual delta against the previous version.

### 4.1 Decision table

| Bump | Triggered by any of | Gate |
|---|---|---|
| **MAJOR** | `remove_entity`, `rename_entity`, `remove_column`, `change_type`, `change_pk`, `change_grain`, toggling `envelope_required`, dropping Core version compatibility, adding a non-nullable column | `HITL` |
| **MINOR** | `add_entity`, `add_column` with `NULL` allowed, new Gold view contract, new dimensional anchor, new controlled-vocabulary value in `business_step`/`disposition`, `deprecated_in` marker added to an entity or column | `ACK_ONLY` |
| **PATCH** | `metadata` only: description text, comment, grain clarification that preserves the same grain, PII classification refinement, formatting | `ZERO_TOUCH` |

### 4.2 Anti-cheating rules

1. **Adding a non-nullable column is MAJOR.** It breaks inserts from existing producers. If you want a non-nullable column in practice, do it in two steps: MINOR to add it as nullable with a default-populator, then MAJOR in a later release to tighten the constraint.
2. **Renaming is MAJOR.** Never rename in place. The required pattern is: MINOR to add the new name with the same grain, MINOR to mark the old name `deprecated_in`, MAJOR in a later release to remove it.
3. **Grain refinements that change the grain are MAJOR.** Clarifying prose in the `grain` string without changing what the grain actually *is* is PATCH.
4. **Core version compatibility.** If `core_version_required` increases by MAJOR, every schema in the edition manifest inherits a MAJOR on its next release.

### 4.3 Event envelope (Core Part 7.4)

The shared canonical event envelope is versioned by Core, not by edition manifests. Editions declare `envelope_required: true` on every schema that uses it. If Core MAJOR-bumps the envelope, editions must MAJOR-bump every affected schema in their next release cycle.

---

## Part 5 — The Schema Update Process (Verbose)

Five distinct processes, one per role. Read the one that matches your role. The processes reference each other where they cross boundaries.

### 5.1 Role: Edition Author — making a MINOR bump

**Scenario:** MERML needs a new entity `PLANOGRAM_COMPLIANCE_EVENT` because the new shelf CV feed produces events that don't fit any existing entity. This is additive, so it's a MINOR bump.

**Step 1 — Open a branch on the edition repo.**
Branch naming: `schema/<schema-code>/<short-description>`. Example: `schema/merml/planogram-compliance-event`.

**Step 2 — Update the schema source.**
Add the new entity to the edition's existing `apex-rc/data/schemas.json` (the detailed schema registry that already exists per the edition spec). Include the full entity definition per Core Part 7.3 template: `entity_name`, `layer`, `scd2`, `grain`, `primary_key`, `columns`, `foreign_keys`, `retention`, `tool_bindings`.

**Step 3 — Update the manifest (`apex-rc/data/schemas.manifest.json`).**

- Bump the MERML schema `version` field from `1.2.0` to `1.3.0`.
- Prepend a new entry to MERML's `changelog` array describing the change. Required fields: `version`, `bump: "MINOR"`, `gate: "ACK_ONLY"`, `date`, `author`, `rationale`, `changes`.
- Add an entry to MERML's `entities` array for `PLANOGRAM_COMPLIANCE_EVENT` with `added_in: "1.3.0"`.
- Update `entity_count` to match.

**Step 4 — Run the validator in author mode.**
```
apex-validate apex-rc/
```
The validator checks:
- Manifest conforms to L1 contract.
- Bump declared in the changelog matches the computed delta (it should auto-detect that adding a new entity with no `deprecated_in` is MINOR).
- All entities listed in the manifest exist in `schemas.json`.
- All PKs resolve against declared columns.
- No MAJOR-shaped change hidden under a MINOR declaration.
- Entity count matches.
- `core_version_required` matches the Core version in effect.

On pass, it writes `apex-rc/data/report.html` and `apex-rc/data/report.json`. Attach both to the PR.

**Step 5 — Open the PR.**
PR description should link to the report and name the bump explicitly. Reviewers (edition maintainers + one SteerCo member for the contract change, if any) read the visual report rather than the raw diff.

**Step 6 — CI runs automatically.**
`apex-validate --ci apex-rc/` runs on every push. Exit code 0 for clean, 1 for warnings, 2 for criticals. PR merge is blocked on exit code 2.

**Step 7 — Merge.**
On merge to `main`, the Core release job rebuilds the edition manifest bundle for every account pinned to RC in L3, signs each bundle, and publishes to the release feed. This does not change any account's pinned version — it only makes the new manifest *available* for fleet-registry PRs (Part 5.3) to pin against.

---

### 5.2 Role: Edition Author — making a MAJOR bump

**Scenario:** `CUSTOMER_INCIDENT` in CXML needs its grain changed from "one row per incident" to "one row per incident per affected customer." This is a breaking change — downstream consumers that assumed the old grain will produce wrong counts.

**Step 1 — Before writing any code, draft a deprecation proposal.**
MAJOR bumps require a human-readable deprecation proposal posted to the edition's RFC channel 2 weeks before the PR. The proposal names: what is changing, why, which consumers are affected (enumerate by agent ID and ORCH ID from the edition spec), what the migration path is, and what the rollout window is.

**Step 2 — Confirm that the deprecation ladder is possible.**
Can this be staged as MINOR + MINOR + MAJOR (add new, deprecate old, remove old)? For a grain change, usually yes: add `CUSTOMER_INCIDENT_V2` with the new grain (MINOR), mark `CUSTOMER_INCIDENT` `deprecated_in` (MINOR), remove `CUSTOMER_INCIDENT` in a later release (MAJOR). Only go straight to MAJOR when deprecation-laddering is genuinely impossible.

**Step 3 — Update the edition spec, the schema source, and the manifest together.**
A MAJOR bump often involves touching the edition's build-spec markdown as well as the JSON. All three change in the same PR.

- Edition spec: update the entity description, grain, and any prose references.
- `schemas.json`: change the entity definition.
- `schemas.manifest.json`: bump the schema's `version` MAJOR (e.g., `1.1.0` → `2.0.0`), add a changelog entry with `bump: "MAJOR"`, `gate: "HITL"`, full `rationale`.

**Step 4 — Run the validator.**
The validator will *require* that the PR description include a link to the deprecation proposal for any MAJOR bump. Missing link = hard failure (exit 3).

**Step 5 — Require SteerCo sign-off.**
MAJOR bumps require approval from at least one SteerCo member in addition to edition maintainers. This is a branch protection rule on the edition repo.

**Step 6 — Merge.**
On merge, the release job builds and publishes the new manifest bundle. **No tenant auto-upgrades to a MAJOR version.** Every pinned account stays on the prior version until an Account Team PR to L3 explicitly pins the new MAJOR version (Part 5.3).

---

### 5.3 Role: Account Team — pinning a client to a new schema version

**Scenario:** Alpha Retail (acct-alpha-001) is currently pinned to MERML@1.2.0. MERML@1.3.0 is available. The Account Team wants to roll it out.

**Step 1 — Read the edition manifest.**
Review the L2 changelog for MERML. Read the `rationale` and the `changes` list. Skim the validator report artifact for MERML@1.3.0.

**Step 2 — Confirm the upgrade is safe for this client.**
Check the account's `auto_upgrade_policy` in L3. For a MINOR bump, the policy is typically `ACK_ONLY`, meaning the client tenant will apply it automatically within its quiet window and post an ACK notification. Confirm:

- Nothing in this client's ORCH inventory depends on the *absence* of the new entity.
- The client's quiet window is long enough for the DDL to complete (Fabric DDL on a 40-entity schema typically completes in seconds; still, honor the window).
- No ongoing incident in the client tenant that would make a nightly change unwelcome.

If the bump is MAJOR, additionally:
- Confirm an approver has been identified in the client's ops team (they will be prompted to run `apex-sync apply --approve <ticket>`).
- Schedule a calendar window explicitly; do not rely on the quiet window alone.
- Confirm the client has reviewed the deprecation proposal from Part 5.2.

**Step 3 — Open a PR on the fleet-registry repo.**
Edit the entry for `acct-alpha-001`. Change:

```json
{ "code": "MERML", "version": "1.2.0" }
```

to:

```json
{ "code": "MERML", "version": "1.3.0" }
```

PR title: `pin acct-alpha-001 MERML@1.3.0`. Description: link the L2 changelog entry, the validator report, and the client's change-management ticket.

**Step 4 — CI runs `apex-validate --fleet --account acct-alpha-001`.**
Validator checks:
- Pinned version exists in the edition manifest.
- Pinned version is `>=` currently pinned (no silent downgrade).
- Core version compatibility is intact.
- If MAJOR, the account's auto_upgrade_policy allows MAJOR as `HITL`, not `ZERO_TOUCH`.

**Step 5 — Merge.**
On merge, the release job rebuilds Alpha Retail's signed manifest bundle. The next nightly `apex-sync` run in the tenant will detect the drift and route per Part 6.

**Step 6 — Wait for the heartbeat.**
After the tenant's quiet window passes, the fleet dashboard should show Alpha Retail's MERML cell flip from amber (pending) to green (deployed). If the heartbeat doesn't arrive within `heartbeat_sla_hours`, the dashboard flags grey. Escalate per runbook.

---

### 5.4 Role: Tenant Operator — approving a MAJOR bump

**Scenario:** Alpha Retail's fleet-registry entry has been updated to pin CXML@2.0.0, replacing CXML@1.1.0. This is a MAJOR bump. The tenant's nightly `apex-sync` run has detected drift and, per policy, refused to auto-apply; it has written a `pending_upgrades` entry to `deployed-manifest.json` and posted a notification to the client's Teams channel.

**Step 1 — Inspect the planned change.**
From the tenant ops workstation:

```
apex-sync status
```

Output:

```
APEX Sync — acct-alpha-001 — Edition: RC — Core: 1.2

  Schema   Deployed    Pinned     Latest     Status
  ------   --------    ------     ------     ----------------
  MERML    1.3.0       1.3.0      1.3.0      OK
  SCML     1.0.0       1.0.0      1.0.0      OK
  CXML     1.1.0       2.0.0      2.0.0      HITL — pending
  MKTL     1.0.0       1.0.0      1.0.0      OK
```

**Step 2 — Dry-run the change.**

```
apex-sync plan --schema CXML
```

Output lists:
- The DDL that will execute (CREATE / DROP / ALTER statements).
- The entities that will be affected.
- The estimated runtime based on recent DDL telemetry.
- A pointer to the edition's deprecation proposal for this MAJOR bump.
- A summary of downstream ORCH IDs that consume CXML and must be regression-tested post-apply.

**Step 3 — Obtain change approval.**
Per client change-management, file or reference a change ticket. Standard practice is one ticket per MAJOR bump, reviewed by the client's data-platform owner.

**Step 4 — Apply with approval.**

```
apex-sync apply --approve ticket://CHG-4411
```

The tool:
1. Re-verifies the approval ticket format (regex enforced by contract).
2. Acquires the tenant-local quiet-window lock.
3. Executes the DDL in a Fabric transaction.
4. On success, updates `deployed-manifest.json`:
   - Sets CXML's `version` to `2.0.0`.
   - Sets `applied_utc` to now.
   - Sets `gate` to `HITL`.
   - Sets `approved_by` to the ticket URL.
   - Recomputes and writes `manifest_hash`.
5. Posts a success notification to the Teams channel.
6. On any failure, rolls the transaction back and leaves the manifest untouched. Does not mark the upgrade as applied.

**Step 5 — Post-apply verification.**
Run the client's regression test suite against the schemas that depend on CXML. The `apex-sync plan` output listed these ORCH IDs; re-run their contract tests.

**Step 6 — Heartbeat.**
The next nightly `apex-sync` run posts an updated heartbeat with the new `manifest_hash`. The fleet dashboard will flip Alpha Retail's CXML cell to green.

---

### 5.5 Role: Core Maintainer — amending the contract

**Scenario:** A new required field (`data_contract_owner`) needs to be added to `entity_entry` in L1.

**Step 1 — Classify the amendment.**
Is this a MAJOR, MINOR, or PATCH contract bump? Adding a required field is MAJOR (every edition manifest now fails validation until they comply). Adding an optional field with a default is MINOR. Clarifying prose is PATCH.

**Step 2 — Draft a Core amendment document.**
Follow the precedent set by `apex-core-v1.1-amendment.md`. Name the file `apex-core-v1.X-amendment.md` where X is the next available minor. Sections: rationale, new contract shape, validation harness changes, downstream impact, handoff notes.

**Step 3 — Post the amendment to the SteerCo channel for a two-week review.**
MAJOR amendments to L1 trigger a mandatory migration window; the amendment document must declare the window in writing.

**Step 4 — Land the amendment.**
On SteerCo approval, merge the amendment, bump `contract_version` in L1, bump `core_version` in L1, update `apex-core/CHANGELOG.md`, and update Core's Part 0 inheritance declarations in every active edition spec.

**Step 5 — Require downstream editions to conform.**
For a MAJOR contract bump: every active edition has until the migration-window deadline to update its L2 manifest. The validator flags any edition still on the prior contract version after the deadline. For a MINOR bump: editions adopt at their own pace.

---

## Part 6 — The Version-Check & Upgrade Flow (Runtime)

This is the nightly pipeline that runs in every tenant. It implements the decisions made by Parts 4 (SemVer rules) and 5.3 (fleet pinning).

### 6.1 Mapping SemVer to HITL gates

Reuses the Core Part 8.3 HITL taxonomy unchanged.

| SemVer bump | Change class | APEX gate | Auto-apply? |
|---|---|---|---|
| **PATCH** (1.2.0 → 1.2.1) | Docs, metadata, comments | `ZERO_TOUCH` | Yes, silent |
| **MINOR** (1.2.x → 1.3.0) | Additive: new entity, new nullable column | `ACK_ONLY` | Yes, logged, Teams notification |
| **MAJOR** (1.x → 2.0) | Breaking: drop, rename, change type/grain | `HITL` | No — explicit approval required |

### 6.2 Three artifacts the sync agent compares

- `deployed-manifest.json` — what is currently running (local, tenant-side, L4).
- `pinned-manifest.json` — what the fleet registry says should run (pulled from signed release, derived from L3).
- `latest-catalog.json` — highest version available in the edition catalog (informational, derived from L2).

The sync agent only *acts on* the first two. The third is displayed in the in-tenant view so operators see upgrade candidates even before the Account Team has pinned them.

### 6.3 Runtime sequence (per tenant, nightly)

1. **Scheduled trigger** fires inside the tenant's quiet window.
2. **Pull pinned manifest.** Fabric pipeline authenticates to the release feed with the tenant's own service principal, requests the bundle scoped to its `account_id`.
3. **Validate signature.** Bundle signature is verified against the published public key. On failure, abort and alert.
4. **Compute diff.** `apex-sync` compares deployed-vs-pinned per schema. For each drift:
   - Classify the bump from the changelog entry in the bundled L2 fragment.
   - Look up the account's `auto_upgrade_policy` (bundled with the pinned manifest).
   - Route to the appropriate gate handler.
5. **Execute by gate type:**
   - `ZERO_TOUCH`: apply DDL inside a Fabric transaction. Log. Update L4.
   - `ACK_ONLY`: apply DDL. Log. Update L4. Post notification to Teams webhook.
   - `HITL`: do not apply. Write `pending_upgrades` entry to L4. Post notification. Wait for `apex-sync apply --approve`.
6. **Heartbeat.** Regardless of outcome, compute `manifest_hash` of L4 and post `{ account_id, heartbeat_utc, manifest_hash }` to the fleet endpoint. Only these three fields cross the boundary.

### 6.4 `apex-sync` CLI reference

| Command | Behavior | Exit codes |
|---|---|---|
| `apex-sync status` | Read-only. Prints Deployed/Pinned/Latest table. | `0` clean, `1` drift |
| `apex-sync check` | CI gate. Silent on parity; non-zero if drift exists. | `0`/`1` |
| `apex-sync plan [--schema CODE]` | Dry-run. Prints DDL that would execute, lists dependent ORCHs. | `0` |
| `apex-sync apply [--approve TICKET]` | Applies PATCH/MINOR automatically. Refuses MAJOR without `--approve`. Writes L4 on success. | `0` success, `2` HITL blocked, `3` DDL failed |
| `apex-sync rollback --to VERSION` | Emergency. Rolls a specific schema to a previous version from L4 history. Requires `--approve`. | `0`/`2`/`3` |

---

## Part 7 — The Validation Tool with Visual Output (`apex-validate`)

### 7.1 Two modes

| Mode | Input | Audience | When run |
|---|---|---|---|
| **Author mode** | A single edition folder | Edition authors; CI | Every PR against an edition |
| **Fleet mode** | Fleet registry + all edition manifests | Account Teams; DMTSP internal | On merge to `main`; on demand |

Both modes share a single engine. Fleet mode is author mode executed across all editions and rolled up by account.

### 7.2 Output surfaces

Every run writes two files:

- `report.html` — self-contained, APEX design-system-styled, single-file static report. Portable to PR comments, email attachments, and the edition site under `validation/`.
- `report.json` — machine-readable; stable schema; versioned with L1.

### 7.3 Rendering (APEX design system, Part 9 inheritance)

- Typography: Fraunces display, Instrument Sans body, JetBrains Mono for codes.
- Theme: dark default with toggle, Core Part 9 tokens.
- Semantic colors: teal = pass; amber = MINOR pending (`ACK_ONLY`); crimson = MAJOR pending (`HITL`) or contract violation; slate = PATCH/metadata; muted = reserved/unused.
- Widgets: reuses Core Part 10 components — `solution-stack.js`, `cmm-filter.js`, `domain-tabs.js`, `arch-diagram.js`. No new widget library.

### 7.4 Four visual surfaces

**1. Compliance heatmap** (author-mode headline). Grid: rows = schemas, columns = acceptance checks (Core Part 11 + L1 contract checks). Cells are teal/amber/crimson dots. Click for failing-entity detail.

**2. Version timeline** (per-schema drill-down). Horizontal timeline, one node per version, entity-level diff on hover/click. Answers "why did this bump."

**3. Fleet drift matrix** (fleet-mode headline). Rows = accounts, columns = schemas. Each cell: `deployed → pinned` colored by required gate. Filters by edition, by wave, by heartbeat age. Sortable by severity.

**4. Validation summary card.** Compact header: total checks, pass/warn/critical counts, Core version, timestamp. Mirrored as `report.json` for CI consumption.

### 7.5 CLI reference

| Command | Behavior |
|---|---|
| `apex-validate <edition-folder>` | Author mode. Writes `report.html` + `report.json` into the edition's folder. |
| `apex-validate --fleet` | Fleet mode. Writes `fleet-report.html` + `fleet-report.json` into `apex-fleet/`. |
| `apex-validate --fleet --account <id>` | Single-account drill-down. |
| `apex-validate --ci` | Pipeline-friendly. Machine-readable stdout; non-zero on criticals. |
| `apex-validate --check-contract` | Verifies L1 alone is well-formed. Used in Core CI. |

Exit codes: `0` clean, `1` warnings only, `2` criticals present, `3` contract or manifest shape broken.

---

## Part 8 — File Structure Additions

```
apex-core/
├── data/
│   ├── edition-registry.json                  (existing, v1.1)
│   └── schema-manifest-contract.json          (NEW — L1)
├── conventions/
│   └── schema-versioning.md                   (NEW — convention doc)
└── tools/
    ├── validate-edition.js                    (existing, extended)
    ├── validate-registry.js                   (existing, v1.1)
    ├── apex-validate.js                       (NEW — dual-mode tool, may subsume validate-edition)
    └── apex-sync.js                           (NEW — tenant-side CLI)

apex-rc/
└── data/
    ├── schemas.json                           (existing)
    └── schemas.manifest.json                  (NEW — L2)

apex-th/
└── data/
    └── schemas.manifest.json                  (NEW — L2)

apex-hls/, apex-tmt/, apex-er/, apex-ice/      (same pattern as editions come online)

apex-fleet/                                    (NEW — Deloitte-side, separate repo or subfolder)
├── data/
│   └── fleet-registry.json                    (L3)
├── tools/
│   └── release-bundler.js                     (assembles signed per-account bundles)
└── dashboards/
    └── fleet-report.html                      (generated by apex-validate --fleet)
```

The tenant side lives inside each client's OneLake and is not tracked in any Deloitte repo:

```
<client-onelake>/apex-sync/
├── deployed-manifest.json                     (L4)
└── history/
    └── deployed-manifest-<timestamp>.json     (rotating backup)
```

---

## Part 9 — Core v1.2 Amendment (Acceptance)

This design lands as APEX Core v1.2. The amendment document (`apex-core-v1.2-amendment.md`) will:

1. **Add L1 artifact.** Writes `apex-core/data/schema-manifest-contract.json` with the shape in Part 3.1.
2. **Add convention doc.** Writes `apex-core/conventions/schema-versioning.md` referencing this design.
3. **Extend Part 11 acceptance criteria.** Adds three new criteria an edition must satisfy:
   - `☑ Edition includes schemas.manifest.json conforming to Core v1.2 contract.`
   - `☑ Every schema declares version + changelog + envelope_required.`
   - `☑ apex-validate exits 0 or 1 (no criticals) against the edition.`
4. **Introduce the fleet layer.** Declares L3/L4 as Deloitte-side operational artifacts; names the new `apex-fleet/` folder convention; clarifies that fleet state is not an edition-authoring concern.
5. **Introduce the tools.** `apex-validate` and `apex-sync` become Core-shipped tools; the existing Phase 4 harness is extended rather than replaced.
6. **Update Part 0 inheritance.** Every active edition spec updates its Part 0 line: *"This spec inherits from APEX Core v1.2."*

No existing content is invalidated. Every edition manifest not yet written is optional until each edition elects to adopt v1.2 (one-line spec update + one new manifest file).

---

## Part 10 — Build Sequence for Claude Code

Four phases; each independently valuable and mergeable.

### Phase 1 — Contract & conventions

**Deliverables:**
- `apex-core/data/schema-manifest-contract.json`
- `apex-core/conventions/schema-versioning.md`
- `apex-core-v1.2-amendment.md`
- Updated `apex-core/CHANGELOG.md`

**Acceptance:** Contract passes `apex-validate --check-contract`. Amendment doc reviewed by SteerCo.

### Phase 2 — Validation tool

**Deliverables:**
- `apex-core/tools/apex-validate.js` with author mode first.
- HTML + JSON report generators.
- CI integration examples.

**Acceptance:** Running `apex-validate apex-rc/` against a sample manifest produces a valid HTML/JSON pair, matches fixtures, exits 0.

### Phase 3 — Edition onboarding

**Deliverables:**
- `apex-rc/data/schemas.manifest.json` (populated from existing `schemas.json`).
- Repeat for TH, HLS, TMT, ER, ICE as each edition lands.
- Each edition spec updated with the v1.2 inheritance line.

**Acceptance:** Every active edition produces `apex-validate` exit 0.

### Phase 4 — Fleet & sync

**Deliverables:**
- `apex-fleet/` repo scaffold + `fleet-registry.json` seed.
- `apex-core/tools/apex-sync.js` CLI.
- Fleet-mode support in `apex-validate`.
- Signed release bundler (`apex-fleet/tools/release-bundler.js`).
- Reference Fabric Data Factory pipeline spec for the tenant side.

**Acceptance:** Synthetic two-account fleet demonstrates: author-mode validation passes on each edition; fleet-mode shows correct drift matrix; a MINOR bump propagates to both synthetic tenants via the pull cycle; a MAJOR bump is blocked until `apex-sync apply --approve` is invoked.

---

## Part 11 — Handoff Notes

**This design is additive.** No existing APEX content is invalidated. An edition that has not yet written an L2 manifest is still a valid APEX edition under Core v1.1; adopting v1.2 is a one-line spec change plus one new JSON file.

**GitOps, not Kubernetes.** The pull/reconcile pattern is borrowed from GitOps but applied to declarative data-schema artifacts. Kubernetes is not in the APEX reference stack and is not introduced here.

**Independence is preserved by construction.** No client row data, no client credentials, no Deloitte-side runtime handle on any tenant. The only things that cross the boundary are: opaque account ID, pinned versions, manifest hash, heartbeat timestamp.

**Reuse before invention.** The gate taxonomy (HITL / ACK_ONLY / ZERO_TOUCH / ESCALATION) comes straight from Core Part 8.3. The inheritance pattern comes straight from the v1.1 edition-registry precedent. The design system for the report comes straight from Core Part 9. No new frameworks.

**When editions disagree with the contract, the contract wins.** If an edition needs a new change-op code, a new bump rule, or a new gate mapping, that is a Core amendment — never a silent edition override. Propose the amendment, bump Core, update every downstream edition.

**What this design deliberately does not do:**
- Does not version agents (e.g., MER-A01@2.1).
- Does not version orchestrations (e.g., ORCH-04@1.3).
- Does not version Solution Stack rows.
- Does not model schema-to-schema cross-references beyond the envelope.

These are deferred intentionally. Each can adopt the same L1/L2/L3/L4 pattern when the need is real. This design is the template.

---

**End of APEX Schema Versioning Manifest Design — 2026-04-17**

*Next step on approval: writing-plans skill produces a step-by-step implementation plan keyed to Part 10 phases.*
