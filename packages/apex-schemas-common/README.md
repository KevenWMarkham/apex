# apex-schemas-common

Shared infrastructure consumed by every APEX canonical-schema package (`apex-scml`, `apex-merml`, `apex-cxml`, `apex-hlscml`, …).

## What it provides

- **`entity`** — `CanonicalEntity` (inherits the 5-field envelope) + `ScdType2Fields` mixin for history-tracked rows.
- **`ddl`** — `generate_delta_ddl(model)` → Delta / Spark SQL `CREATE TABLE` from a Pydantic model.
- **`purview`** — `build_purview_payload(model)` → Purview classification registration dict.
- **`standards`** — `StandardRef` + `StandardSpec` + `STANDARDS` registry + identifier types (`GTIN14`, `SSCC`, `GLN`, `LoincCode`, `Icd10Code`, …).

Design: see `docs/APEX - Design and Build/APEX_Design.md` §5, §14 and `Industry-Standards-Incorporation-Plan.md`.
