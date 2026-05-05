"""Purview classification payload builder from Pydantic models.

Walks a Pydantic model's annotations and produces a dict suitable for Purview
REST registration. Classifications are discovered via ``Annotated`` metadata
carrying a :class:`apex_core.types.Classification` instance; standards bindings
are discovered via :class:`apex_schemas_common.standards.types.StandardRef`.

See ``docs/APEX - Design and Build/APEX_Design.md`` §14.
"""

from __future__ import annotations

from types import NoneType, UnionType
from typing import Annotated, Any, Union, get_args, get_origin, get_type_hints

from pydantic import BaseModel

from apex_core.types import Classification


def _extract_metadata(annotation: Any) -> list[Any]:
    """Return the list of metadata objects attached via ``Annotated[...]``."""
    origin = get_origin(annotation)

    # Unwrap Optional / Union
    if origin is UnionType or origin is Union:
        for arg in get_args(annotation):
            if arg is NoneType:
                continue
            nested = _extract_metadata(arg)
            if nested:
                return nested
        return []

    if origin is Annotated:
        return list(get_args(annotation)[1:])

    return []


def _find_classification(metadata: list[Any]) -> Classification | None:
    for item in metadata:
        if isinstance(item, Classification):
            return item
    return None


def _find_standard_ref(metadata: list[Any]) -> dict[str, str] | None:
    """Detect a StandardRef without forcing an import dependency here.

    Identified structurally by dataclass-style attributes so ``purview`` can
    stay free of a hard dependency on :mod:`apex_schemas_common.standards`.
    """
    for item in metadata:
        if (
            hasattr(item, "standard_id")
            and hasattr(item, "identifier")
            and hasattr(item, "version")
        ):
            return {
                "standard_id": str(item.standard_id),
                "identifier": str(item.identifier),
                "version": str(item.version),
            }
    return None


def build_purview_payload(
    model_cls: type[BaseModel],
    *,
    family: str | None = None,
    default_classification: Classification = Classification.INTERNAL,
) -> dict[str, Any]:
    """Emit a Purview registration payload for a canonical-entity model.

    Args:
        model_cls: The Pydantic canonical entity class.
        family: Optional schema-family tag (e.g. ``"scml"``).
        default_classification: Applied to fields without an explicit
            ``Annotated[..., Classification.X]`` marker.

    Returns:
        A JSON-serialisable dict with ``entity``, ``family``, and ``fields``.
    """
    hints = get_type_hints(model_cls, include_extras=True)
    fields: list[dict[str, Any]] = []

    for field_name, field_info in model_cls.model_fields.items():
        annotation = hints.get(field_name, str)
        metadata = _extract_metadata(annotation)

        classification = _find_classification(metadata) or default_classification
        standard = _find_standard_ref(metadata)

        entry: dict[str, Any] = {
            "name": field_name,
            "classification": classification.value,
            "required": field_info.is_required(),
            "description": field_info.description or "",
        }
        if standard is not None:
            entry["standard"] = standard

        fields.append(entry)

    return {
        "entity": model_cls.__name__.lower(),
        "family": family,
        "fields": fields,
    }
