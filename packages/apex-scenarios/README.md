# apex-scenarios

APEX Scenario Library tooling. Sprint 28 deliverables (Python parallel
track for BL.P.169–185).

## Scope

| Subtask | Module | Purpose |
|---|---|---|
| 28.1.2 | `models.Scenario` | Extended JSON schema (Wave 1 / 2 / 3 fields) |
| 28.1.6 | `validators.validate_wave_data_presence` | Every library row has non-empty W1/W2/W3 |
| 28.4.1 | `exporters.write_csv` | CSV export of full or filtered library |
| 28.4.3 | `exporters.csv_filename` | Canonical filename `APEX-scenarios-{practice}-{date}.csv` |
| 28.7.1 | `publication.publish_master_catalog` | Appendix L master catalog (markdown per Practice + index) |
| 28.7.2 | `validators.validate_service_codes` | Every `service_code` resolves to Service Catalog |
| 28.7.3 | `validators.validate_agent_references` | Featured-scenario Solutions name agents in Agent Catalog |
| 28.7.4 | `validators.validate_kpis` | Featured-scenario KPIs resolve to KPI Registry (Appendix C) |
| 28.7.5 | `validators.classify_library_bump` | PATCH / MINOR / MAJOR version classification |
| 28.7.6 | `.github/workflows/ci.yml` `scenarios` lane | All validators run on every PR |

UI deliverables in Sprint 28 (Tabs, modal animations, keyboard
affordances, PPTX export) live in the Stacked Architecture HTML and are
**out of scope** for this Python package.

## Quick Start

```bash
# Inside the monorepo:
pip install -e packages/apex-core packages/apex-scenarios

# Run all governance validators (CI gate):
apex scenarios validate

# Stats summary:
apex scenarios stats

# CSV export (canonical filename auto-generated):
apex scenarios export-csv
apex scenarios export-csv --practice RC

# Publish Appendix L master catalog:
apex scenarios publish-catalog docs/scenarios/_master-catalog/

# Classify a version bump:
apex scenarios bump before.json after.json
```

## Versioning rules (Task 28.7.5)

- **PATCH** — copy edits, KPI re-measurements, no scenario set changes,
  no field-schema changes.
- **MINOR** — at least one scenario added or removed; no field-schema
  change.
- **MAJOR** — at least one field-schema change (key added/removed on
  any row).

## Cross-reference

- Sellers Guide §2.2A (envelope framework) — Wave 1 / 2 / 3 are the
  contractable boundaries
- Sellers Guide §2.2B (value-delivery chain) — Scenario → Solution →
  Use Case → Service → Persona → KPI
- APEX Orchestrator Sprint 28 (BL.P.169–185)
- Sprint 27 Stacked Architecture HTML — front-end consumer of the
  validated library
