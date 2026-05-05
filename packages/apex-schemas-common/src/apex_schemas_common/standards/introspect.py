"""Walk a Pydantic model's annotations to discover standards bindings.

Every ``Annotated[..., StandardRef(...)]`` attached to a field of a canonical
entity is discoverable via :func:`find_standard_refs`. :func:`audit_model`
additionally verifies every discovered ``StandardRef`` has a matching registry
entry with the expected version pin.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import NoneType, UnionType
from typing import Annotated, Any, Union, get_args, get_origin, get_type_hints

from pydantic import BaseModel

from apex_schemas_common.standards.registry import STANDARDS
from apex_schemas_common.standards.types import StandardRef


def _collect_annotated_metadata(annotation: Any) -> list[Any]:
    """Return all metadata objects from ``Annotated[...]``, walking through Optional."""
    origin = get_origin(annotation)
    if origin is UnionType or origin is Union:
        out: list[Any] = []
        for arg in get_args(annotation):
            if arg is NoneType:
                continue
            out.extend(_collect_annotated_metadata(arg))
        return out
    if origin is Annotated:
        return list(get_args(annotation)[1:])
    return []


def find_standard_refs(model_cls: type[BaseModel]) -> dict[str, StandardRef]:
    """Return a mapping from ``field_name`` → :class:`StandardRef` for every binding."""
    hints = get_type_hints(model_cls, include_extras=True)
    refs: dict[str, StandardRef] = {}
    for field_name in model_cls.model_fields:
        for item in _collect_annotated_metadata(hints.get(field_name, str)):
            if isinstance(item, StandardRef):
                refs[field_name] = item
                break
    return refs


@dataclass(frozen=True, slots=True)
class AuditEntry:
    """One finding from an audit of a model's standards bindings."""

    field: str
    ref: StandardRef
    registered: bool
    version_matches: bool


def audit_model(model_cls: type[BaseModel]) -> list[AuditEntry]:
    """Audit a Pydantic model: every ``StandardRef`` must resolve in :data:`STANDARDS`.

    Returns one :class:`AuditEntry` per field-with-binding. Callers decide how
    strictly to enforce (e.g. fail CI when any entry has ``registered=False``
    or ``version_matches=False``).
    """
    entries: list[AuditEntry] = []
    for field, ref in find_standard_refs(model_cls).items():
        spec = STANDARDS.get(ref.standard_id)
        entries.append(
            AuditEntry(
                field=field,
                ref=ref,
                registered=spec is not None,
                version_matches=(
                    spec is not None and spec.apex_pinned_version == ref.version
                ),
            )
        )
    return entries
