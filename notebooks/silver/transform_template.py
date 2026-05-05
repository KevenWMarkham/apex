"""Generic Bronze → Silver transform template (APEX_Design §6.4).

Apply per-Practice by:

1. Replacing ``_parse_source_row`` with the Practice's Bronze-row → Pydantic
   adapter (e.g. ``FhirPatient → HLSCML Patient`` via
   ``apex_hlscml.translators.patient_from_fhir``).
2. Overriding ``SCD2_CONFIG`` with the key / hashable columns for the target
   entity.
3. Pointing ``BRONZE_TABLE`` / ``SILVER_TABLE`` at the concrete Delta tables.

The template deliberately keeps per-row work as a Python function so unit
tests can exercise it without Spark. The notebook body then maps the
function over a Spark DataFrame row-by-row.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

from apex_medallion.silver import (
    Scd2Config,
    add_scd2_fields_to_instance,
    detect_drift,
    tokenise_and_stamp,
)
from apex_tokenizer import InMemoryVaultBackend, TokenService, set_default_service

# --- CUSTOMIZE for the target entity -------------------------------------

# Example wiring for HLSCML Patient. Swap per-Practice.
from apex_hlscml import Patient  # type: ignore[import-not-found]
from apex_hlscml.translators import patient_from_fhir  # type: ignore[import-not-found]
from apex_standards_fhir import FhirPatient

BRONZE_TABLE = "bronze_hlscml.patient_fhir_raw"
SILVER_TABLE = "silver_hlscml.patient"

SCD2_CONFIG = Scd2Config(
    key_columns=("fhir_id",),
    hashable_columns=(
        "fhir_id", "mrn_token", "name_family_token", "name_given_token",
        "gender", "birth_date", "deceased",
    ),
)

# --- end customize --------------------------------------------------------

if TYPE_CHECKING:  # pragma: no cover
    from pyspark.sql import DataFrame, SparkSession


def configure_tokenizer_for_fabric() -> None:
    """In production, wire the Delta-backed vault. Dev/test → in-memory.

    The notebook calls this once at start-up. Sprint 10 will extend this to
    read the tenant's Key Vault secret for HMAC keying.
    """
    set_default_service(TokenService(backend=InMemoryVaultBackend()))


def _parse_source_row(bronze_row: dict[str, Any]) -> Patient:
    """Parse one Bronze row (as a dict) into the canonical Patient entity.

    CUSTOMIZE: this adapter is entity-specific. The FHIR variant uses
    ``patient_from_fhir`` against the raw payload re-hydrated into FhirPatient.
    """
    import json as _json

    raw_payload = bronze_row.get("_raw_payload", "{}")
    fhir_dict = _json.loads(raw_payload) if isinstance(raw_payload, str) else raw_payload
    fhir = FhirPatient.model_validate(fhir_dict)
    source_system = bronze_row.get("source_system", "fhir")
    return patient_from_fhir(fhir, source_system=source_system)


def transform_one_row(
    bronze_row: dict[str, Any],
    *,
    existing_row_hash: str | None = None,
    now: datetime | None = None,
) -> dict[str, Any] | None:
    """Apply the full Silver transform to a single Bronze row.

    Returns ``None`` when the resulting Silver row would be identical to the
    existing current row (SCD2 no-op).
    """
    # 1–2. Parse + canonicalise
    canonical = _parse_source_row(bronze_row)

    # 3. Tokenise classified fields
    tokenised = tokenise_and_stamp(canonical)

    # 4. Stamp SCD2
    stamped = add_scd2_fields_to_instance(
        tokenised, config=SCD2_CONFIG,
        existing_row_hash=existing_row_hash, now=now,
    )

    # Noop detection: if nothing changed, return None
    if existing_row_hash is not None and existing_row_hash == stamped.row_hash:
        return None

    return stamped.model_dump()


def run(spark: "SparkSession") -> None:
    """Fabric entry-point — batch-read Bronze, transform, append to Silver."""
    configure_tokenizer_for_fabric()

    bronze_df = spark.read.format("delta").table(BRONZE_TABLE)
    rows = bronze_df.toJSON().collect()  # one JSON string per row — template only

    import json as _json
    from pyspark.sql import Row

    output_rows: list[Row] = []
    for raw in rows:
        record = _json.loads(raw)
        transformed = transform_one_row(record, now=datetime.now(UTC))
        if transformed is None:
            continue
        output_rows.append(Row(**transformed))

    if output_rows:
        out_df = spark.createDataFrame(output_rows)
        out_df.write.format("delta").mode("append").saveAsTable(SILVER_TABLE)


def check_drift(spark: "SparkSession") -> None:
    """Nightly drift check — compare live Silver schema to Pydantic model."""
    actual = {
        f.name: f.dataType.simpleString().upper()
        for f in spark.table(SILVER_TABLE).schema.fields
    }
    report = detect_drift(Patient, actual)
    print(report.summary())  # noqa: T201 — notebook stdout is the log surface
    if not report.clean:
        for added in report.added:
            print(f"  + {added}")  # noqa: T201
        for removed in report.removed:
            print(f"  - {removed}")  # noqa: T201
        for col, expected, got in report.type_mismatches:
            print(f"  * {col}: expected {expected}, got {got}")  # noqa: T201
