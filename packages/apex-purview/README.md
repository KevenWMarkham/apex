# apex-purview

APEX Purview integration package. Generates Microsoft Purview / Apache Atlas
API payloads from APEX canonical schema YAMLs.

## Scope

Sprint 13 of the APEX Orchestrator delivers:

| Subtask | Module | Purpose |
|---|---|---|
| 13.1.1 | `classifications` | YAML schema → Purview classification type-defs + entity attachments |
| 13.1.2 | CI workflow step | Register classifications on schema merge |
| 13.2.1 | `lineage.emit_sor_to_bronze` | SOR → Bronze edge (pipeline run ID) |
| 13.2.2 | `lineage.emit_bronze_to_silver` | Bronze → Silver edge (notebook + commit SHA) |
| 13.2.3 | `lineage.emit_silver_to_gold` | Silver → Gold edge (SQL SHA) |
| 13.2.4 | `lineage.emit_gold_to_mcp` | Gold → MCP tool binding |
| 13.2.5 | `lineage.emit_{mcp_to_agent,agent_to_orchestration,orchestration_to_audit}` | MCP → Agent → Orchestration → Audit row |
| 13.3.1 | `dlp` | Label-based redaction policies for Copilot, agent output, Power BI, Teams, email, public web |
| 13.3.2 | `dlp.DLPViolationAlert` | Webhook + audit-row stamping for policy violations |
| 13.4.1 | `retention` | WORM retention bands (P3Y / P7Y / P10Y / PERMANENT) + legal-hold capability |
| 13.5.1 | `catalog.emit_glossary_terms_from_schema` | Business-glossary terms per attribute |
| 13.5.2 | `catalog.emit_relationships_from_schema` | Cross-entity foreign-key relationships |
| 13.6.1 | `propagation.validate_propagation` | Most-restrictive-label inheritance validator |
| 13.6.2 | `propagation.most_restrictive` + `severity()` | Canonical severity ordering of all 12 classifications |
| 13.3 | `dlp` (future) | Label-based redaction policies |
| 13.4 | `retention` (future) | WORM retention (7 y / 10 y / legal-hold) |
| 13.5 | `catalog` (future) | Unified Catalog business-glossary registration |
| 13.6 | `propagation` (future) | Classification propagation chain validator |

## Quick Start

```bash
# Inside the monorepo:
pip install -e packages/apex-core
pip install -e packages/apex-purview

# Emit Purview classification type-defs from a schema:
apex purview emit-classifications packages/apex-scml/data/scml.schema.yaml

# Emit entity-level attachment payloads (which entities get which classifications):
apex purview emit-attachments packages/apex-scml/data/scml.schema.yaml

# Batch — discover every canonical schema and emit payloads in one pass
# (this is what CI runs on every schema merge):
apex purview register-all --root . --output purview-artifacts --strict
```

## CI registration (Subtask 13.1.2)

On every push to `main` and every pull request, the `register-classifications`
GitHub Actions job runs `apex purview register-all --strict` and uploads the
resulting payloads as a build artifact (`purview-classification-payloads`,
retained 30 days). The job fails the build if any schema emits an error —
typically because a schema references a classification that is not in
`APEX_CLASSIFICATIONS`.

Pre-commit runs the same check locally, scoped to schema YAMLs under
`packages/**/data/` and `packages/**/schemas/` and the emitter source itself.
If a committer adds a new classification key to a schema, pre-commit fails
until the classification is either corrected in the schema or added to
`APEX_CLASSIFICATIONS` with Independence review.

## Lineage (Task 13.2)

The `lineage` module emits Atlas v2 Process entities for the seven canonical
APEX hops. Each hop has its own Process typeName (`apex_sor_to_bronze`,
`apex_bronze_to_silver`, …, `apex_orchestration_to_audit`) and carries
hop-specific attributes (`pipeline_run_id`, `commit_sha`, `sql_sha`,
`mcp_tool_version`, `agent_manifest_sha`, `trace_id` + three-version SHAs).

Two usage modes:

1. **Declarative YAML** — author a `kind: lineage` spec enumerating every
   edge; emit with `apex purview emit-lineage <spec.yaml> -o bulk.json`.
   This is the right mode for static medallion relationships.
2. **Programmatic** — call `emit_sor_to_bronze(...)` etc. from the
   orchestrator / Data Factory runtime to emit lineage at the moment
   data moves. Batch assembly via `emit_lineage_batch([...])`.

Bootstrap the seven custom Process type-defs once per tenant with
`apex purview emit-process-typedefs -o processes.json` → POST to
`/api/atlas/v2/types/typedefs`.

The reference Cold Chain lineage at `tests/fixtures/lineage_cold_chain.yaml`
shows every hop with production-grade attributes; see §6.10 and §8.8 of
the Sellers Guide for the architectural reasoning.

## DLP, Retention, Catalog, Propagation (Tasks 13.3 – 13.6)

```bash
# Task 13.3 — DLP
apex purview emit-dlp -o dlp.json
apex purview dlp-lookup phi email          # → "block"
apex purview dlp-lookup restricted copilot_chat  # → "escalate"

# Task 13.4 — Retention
apex purview emit-retention -o retention.json
apex purview retention-lookup phi          # → "P10Y"
apex purview retention-lookup restricted   # → "PERMANENT"

# Task 13.5 — Unified Catalog
apex purview emit-catalog packages/apex-rc/src/apex_rc/data/schemas.manifest.yaml -o catalog.json
apex purview emit-relationship-typedefs -o relationship-types.json

# Task 13.6 — Propagation validator (CI-ready, exits non-zero on violations)
apex purview validate-propagation packages/apex-rc/src/apex_rc/data/schemas.manifest.yaml
```

### Governance defaults at a glance

**DLP matrix** — 12 classifications × 6 surfaces (Copilot chat, agent output,
Power BI export, Teams, email, public web). Public allows everywhere; PHI
blocks email + public web; Restricted escalates everywhere; Genetic and
Behavioral Health are at maximum restrictiveness (block / redact only).

**Retention bands** — P3Y default, P7Y for SOX/PCI/NERC CIP, P10Y for
HIPAA/GINA/42 CFR Part 2, PERMANENT for 21 CFR Part 11 / FSMA 204
records. Tenant overrides never shorten below default.

**Severity ordering** for propagation (most-restrictive wins): public(0) <
internal(1) < member_only(2) < trade_secret(3) < cpni(4) < pii(5) <
pci(6) < phi(7) < genetic/behavioral_health(8) < export_controlled(9) <
restricted(10).

## Design

APEX canonical schemas carry `classification` metadata at entity level and at
attribute level (e.g., `internal`, `trade_secret`, `pii`, `phi`, `pci`,
`restricted`). This package reads those classifications and emits:

1. **Classification type-def payloads** — Atlas-compatible
   `classificationDefs` array, one per unique classification referenced in
   the input schema.
2. **Entity attachment payloads** — lists of
   `{typeName, attributes, entityGuid}` entries that attach the
   classifications to Purview-registered entities / attributes.

Both payloads are regression-fixed against the Purview Atlas v2 REST API
(`POST /api/atlas/v2/types/typedefs`,
`PUT /api/atlas/v2/entity/guid/{guid}/classifications`).

## Cross-reference

- **Sellers Guide §8.8** — Audit architecture end-to-end through Purview
- **Sellers Guide §9.11.7** — DLP / classification taxonomy (RC example)
- **APEX Orchestrator Sprint 13** — Purview Trust Architecture
- **`apex-core`** — schema YAML parsing utilities
- **`apex-schemas-common`** — standards registry (for classification codes
  derived from standards, e.g., HIPAA, 21 CFR Part 11)
