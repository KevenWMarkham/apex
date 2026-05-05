"""KQL function generator for real-time Gold over Eventhouse.

Emits a ``.create-or-alter function`` KQL statement that projects a Silver
Eventhouse table's columns and appends inline post-measures defined in KQL.
"""

from __future__ import annotations

from collections.abc import Iterable

from pydantic import BaseModel

from apex_medallion.gold.measure import MeasureDefinition, MeasureLanguage


def generate_kql_function(
    entity_cls: type[BaseModel],
    *,
    function_name: str,
    silver_table: str,
    measures: Iterable[MeasureDefinition] | None = None,
) -> str:
    """Generate an Eventhouse KQL function that projects ``entity_cls`` columns + measures.

    Args:
        entity_cls: Pydantic entity whose fields form the base projection.
        function_name: The KQL function name (Eventhouse identifier).
        silver_table: The Silver Eventhouse table to read from.
        measures: Post-measures to append (only ``MeasureLanguage.KQL`` included).

    Returns:
        A ``.create-or-alter function ... { ... }`` KQL statement.
    """
    project_cols = ", ".join(entity_cls.model_fields.keys())

    extend_clauses: list[str] = []
    if measures:
        for m in measures:
            if m.language is not MeasureLanguage.KQL:
                continue
            extend_clauses.append(f"{m.name} = {m.formula}")

    body = f"    {silver_table}\n    | project {project_cols}"
    if extend_clauses:
        body += "\n    | extend " + ",\n              ".join(extend_clauses)

    return (
        f".create-or-alter function {function_name}() {{\n"
        f"{body}\n"
        f"}}"
    )
