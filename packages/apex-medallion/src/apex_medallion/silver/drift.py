"""Drift detector — compare a Pydantic entity's expected Delta schema to live Fabric state.

The live schema is supplied as ``dict[column_name, delta_type_string]``; the
caller obtains it from ``spark.catalog.getTable(...)`` or Delta metadata.
Keeping drift detection pure-Python lets CI exercise it without Spark.

See BL.P.34.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import get_type_hints

from pydantic import BaseModel

from apex_schemas_common.ddl import _python_to_delta, _unwrap_optional


@dataclass(frozen=True, slots=True)
class DriftReport:
    """Structured result of a drift audit."""

    model: str
    added: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)
    type_mismatches: list[tuple[str, str, str]] = field(default_factory=list)
    nullability_mismatches: list[str] = field(default_factory=list)

    @property
    def clean(self) -> bool:
        return not (
            self.added or self.removed
            or self.type_mismatches or self.nullability_mismatches
        )

    def summary(self) -> str:
        if self.clean:
            return f"[OK] {self.model} — no drift"
        parts: list[str] = []
        if self.added:
            parts.append(f"{len(self.added)} added")
        if self.removed:
            parts.append(f"{len(self.removed)} removed")
        if self.type_mismatches:
            parts.append(f"{len(self.type_mismatches)} type-mismatch")
        if self.nullability_mismatches:
            parts.append(f"{len(self.nullability_mismatches)} nullability-mismatch")
        return f"[DRIFT] {self.model} — {', '.join(parts)}"


def expected_columns(model_cls: type[BaseModel]) -> dict[str, str]:
    """Return the Delta column → type mapping an APEX model declares."""
    hints = get_type_hints(model_cls, include_extras=True)
    columns: dict[str, str] = {}
    for field_name in model_cls.model_fields:
        annotation = hints.get(field_name, str)
        columns[field_name] = _python_to_delta(annotation)
    return columns


def detect_drift(
    model_cls: type[BaseModel],
    actual_columns: dict[str, str],
) -> DriftReport:
    """Compare the model's expected Delta shape against a live-table snapshot.

    Args:
        model_cls: The APEX canonical-entity Pydantic class.
        actual_columns: ``{column_name: delta_type_string}`` from Spark.

    Returns:
        A :class:`DriftReport` summarising additions, removals, and type drift.
    """
    expected = expected_columns(model_cls)

    expected_names = set(expected)
    actual_names = set(actual_columns)

    added = sorted(actual_names - expected_names)
    removed = sorted(expected_names - actual_names)

    type_mismatches: list[tuple[str, str, str]] = []
    for col in sorted(expected_names & actual_names):
        if _normalise_type(expected[col]) != _normalise_type(actual_columns[col]):
            type_mismatches.append((col, expected[col], actual_columns[col]))

    return DriftReport(
        model=model_cls.__name__,
        added=added,
        removed=removed,
        type_mismatches=type_mismatches,
    )


def _normalise_type(delta_type: str) -> str:
    """Normalise common type aliases so 'BIGINT' matches 'LONG' etc."""
    alias = {
        "LONG": "BIGINT",
        "INT": "INTEGER",
        "DOUBLE PRECISION": "DOUBLE",
    }
    upper = delta_type.strip().upper()
    return alias.get(upper, upper)
