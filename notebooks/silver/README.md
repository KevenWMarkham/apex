# APEX Silver transform templates

Parameterised PySpark templates for Bronze → Silver transforms (APEX_Design §6.4). One generic template lives here; per-Practice specialisations are thin wrappers that bind a specific canonical entity class.

## What Silver must do

Per row, in order:

1. **Read Bronze** — the source-fidelity row (already envelope-stamped + raw payload attached).
2. **Canonicalise** — map source columns into the Practice's canonical Pydantic shape (e.g. `FhirPatient → HLSCML Patient`).
3. **Tokenise** — run every classified field through `apex_tokenizer.tokenize_classified_fields()`.
4. **Stamp SCD2** — for entities that track history, compute `row_hash` and set `scd2_valid_from / scd2_is_current / row_hash`. Use `apex_medallion.silver.add_scd2_fields_to_instance()` with the entity's `Scd2Config`.
5. **Write Silver** — append the Pydantic `model_dump()` as a Delta row.
6. **Drift check** — periodically run `apex_medallion.silver.detect_drift()` to verify the live schema still matches the Pydantic model.

## Files

- `transform_template.py` — one-entity reference; copy per target Practice.

## Why notebooks here

Identical rationale to `notebooks/bronze/` — these run in Fabric's PySpark runtime, not in the CI venv. See `notebooks/bronze/README.md`.
