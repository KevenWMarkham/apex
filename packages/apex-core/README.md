# apex-core

**APEX L1 Contract layer.**

This package defines the normative APEX Core specification:

- Canonical 5-field envelope (`event_id`, `event_ts`, `entity_id`, `source_system`, `source_system_ts`)
- Manifest Pydantic schemas: schema, event, orchestration, agent, tenant, policy, service
- SemVer bump classification (`classify_bump`)
- Validators for manifest, practice, and fleet
- `apex` CLI (runs via `uv run apex`)

Design reference: `docs/APEX - Design and Build/APEX_Design.md` §3.

## Development

```bash
uv sync --all-packages
uv run pytest packages/apex-core
uv run mypy packages/apex-core
uv run ruff check packages/apex-core
```

## CLI

```bash
uv run apex --help
uv run apex version
```

Sprint 1 will add:

```bash
uv run apex validate <manifest.yaml>
uv run apex classify-bump <old.yaml> <new.yaml>
uv run apex report --html
```
