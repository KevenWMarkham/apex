# apex-medallion

Shared helpers consumed by Fabric PySpark notebooks (`notebooks/bronze/`, `notebooks/silver/`, `notebooks/gold/`).

## Sprint 4 scope — Bronze layer

- `bronze.config` — `BronzeLandingConfig` parameterises every Bronze template
- `bronze.retention` — `RetentionPolicy` + Purview payload emitter (BL.P.25)
- `bronze.partitioning` — default + override partition strategies (BL.P.25)
- `bronze.dead_letter` — `DeadLetterRecord` schema + DDL generator
- `bronze.schema` — Bronze table DDL with canonical envelope + `_raw_payload`

## Sprint 5+ (later)

- `silver/` — canonical-transform helpers, tokenisation hooks
- `gold/` — Direct Lake + Warehouse view generators, pre/post measure helpers

## Notebook templates live at repo root

See `notebooks/bronze/README.md` for the 5 parameterised PySpark templates that consume this package.
