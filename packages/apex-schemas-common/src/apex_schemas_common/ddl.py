"""Delta / Spark SQL DDL generator from Pydantic models.

Walks a Pydantic v2 model's field annotations and emits a ``CREATE TABLE``
statement suitable for Fabric Lakehouse or Warehouse.

See ``docs/APEX - Design and Build/APEX_Design.md`` §5.6, §6.4.2.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from types import NoneType, UnionType
from typing import Annotated, Any, Literal, Union, get_args, get_origin, get_type_hints
from uuid import UUID

from pydantic import BaseModel

_SCALAR_TO_DELTA: dict[type, str] = {
    str: "STRING",
    int: "BIGINT",
    float: "DOUBLE",
    bool: "BOOLEAN",
    bytes: "BINARY",
    datetime: "TIMESTAMP",
    date: "DATE",
    Decimal: "DECIMAL(18, 6)",
    UUID: "STRING",
}


def _unwrap_optional(tp: Any) -> tuple[Any, bool]:
    """Peel ``Optional[X]`` / ``X | None`` / ``Union[X, None]`` → ``(X, True)``."""
    origin = get_origin(tp)
    if origin is UnionType or origin is Union:
        args = tuple(a for a in get_args(tp) if a is not NoneType)
        if len(args) == 1:
            return args[0], True
    return tp, False


def _unwrap_annotated(tp: Any) -> Any:
    """If ``tp`` is ``Annotated[T, ...]``, return ``T``; else return ``tp``."""
    if get_origin(tp) is Annotated:
        return get_args(tp)[0]
    return tp


def _python_to_delta(tp: Any) -> str:
    """Translate a Python / Pydantic type annotation to a Delta type string."""
    inner, _ = _unwrap_optional(tp)
    inner = _unwrap_annotated(inner)

    # Primitives
    if isinstance(inner, type) and inner in _SCALAR_TO_DELTA:
        return _SCALAR_TO_DELTA[inner]

    # Enums → STRING
    if isinstance(inner, type) and issubclass(inner, Enum):
        return "STRING"

    # Literal[...] → STRING
    if get_origin(inner) is Literal:
        return "STRING"

    # Generic containers
    origin = get_origin(inner)
    if origin in (list, set, tuple, frozenset):
        args = get_args(inner) or (str,)
        return f"ARRAY<{_python_to_delta(args[0])}>"
    if origin is dict:
        k_t, v_t = (get_args(inner) + (str, str))[:2]
        return f"MAP<{_python_to_delta(k_t)}, {_python_to_delta(v_t)}>"

    # Nested Pydantic model → STRUCT (shallow; recursive expansion out of scope for v0.1)
    if isinstance(inner, type) and issubclass(inner, BaseModel):
        return "STRUCT"

    # Fallback
    return "STRING"


def generate_delta_ddl(
    model_cls: type[BaseModel],
    *,
    table_name: str | None = None,
    database: str | None = None,
    partition_by: list[str] | None = None,
    tbl_properties: dict[str, str] | None = None,
) -> str:
    """Generate a Delta ``CREATE TABLE`` statement from a Pydantic model.

    Args:
        model_cls: The Pydantic model describing the canonical entity.
        table_name: Override the table name (defaults to the model class name lowercased).
        database: Optional schema / database qualifier (e.g. ``silver_scml``).
        partition_by: Columns to ``PARTITION BY``.
        tbl_properties: Additional Delta ``TBLPROPERTIES``. A sensible default
            enabling change-data-feed is applied when omitted.

    Returns:
        A semicolon-terminated ``CREATE TABLE ... USING DELTA`` statement.
    """
    name = table_name or model_cls.__name__.lower()
    qualified = f"{database}.{name}" if database else name

    hints = get_type_hints(model_cls, include_extras=True)

    columns: list[str] = []
    for field_name, field_info in model_cls.model_fields.items():
        annotation = hints.get(field_name, str)
        _, is_optional = _unwrap_optional(annotation)
        delta_type = _python_to_delta(annotation)

        nullable = is_optional or not field_info.is_required()
        nullability = "" if nullable else " NOT NULL"

        comment = ""
        if field_info.description:
            safe = field_info.description.replace("'", "''")
            comment = f" COMMENT '{safe}'"

        columns.append(f"  {field_name:<24} {delta_type}{nullability}{comment}")

    body = ",\n".join(columns)
    props = tbl_properties or {"delta.enableChangeDataFeed": "true"}
    props_lines = ",\n".join(f"  '{k}' = '{v}'" for k, v in props.items())

    parts = [f"CREATE TABLE {qualified} (", body, ")", "USING DELTA"]
    if partition_by:
        parts.append(f"PARTITIONED BY ({', '.join(partition_by)})")
    parts.append(f"TBLPROPERTIES (\n{props_lines}\n)")

    return "\n".join(parts) + ";"
