"""Visibility lattice evaluator.

Given a Pydantic entity class, a concrete row, and a :class:`ScopeContext`,
decide:

1. Is the row visible at all (row filters match)?
2. Which fields are visible, which are masked?

Semantics — a field is visible when:

- It has no ``Classification`` marker (default-allow, PUBLIC-equivalent), OR
- Its ``Classification`` is in ``scope.classification_visibility``.

Field classifications are discovered via ``Annotated[...]`` metadata — the
same path used by ``apex-schemas-common.purview`` and the tokeniser.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import NoneType, UnionType
from typing import Annotated, Any, Union, get_args, get_origin, get_type_hints

from pydantic import BaseModel

from apex_core.types import Classification
from mcp_common import ScopeContext


@dataclass(frozen=True, slots=True)
class VisibilityDecision:
    """Structured result of a per-row visibility evaluation."""

    entity_name: str
    visible_fields: frozenset[str]
    masked_fields: frozenset[str]
    row_visible: bool
    row_filter_reason: str | None = None


def _find_classification(annotation: Any) -> Classification | None:
    """First ``Classification`` metadata on an annotation, or None."""
    origin = get_origin(annotation)
    if origin is UnionType or origin is Union:
        for arg in get_args(annotation):
            if arg is NoneType:
                continue
            found = _find_classification(arg)
            if found is not None:
                return found
        return None
    if origin is Annotated:
        for meta in get_args(annotation)[1:]:
            if isinstance(meta, Classification):
                return meta
    return None


def _row_filters_pass(row: dict[str, Any], filters: dict[str, str]) -> tuple[bool, str | None]:
    """True iff every filter key matches ``str(row[key])`` exactly.

    Missing keys count as mismatch (fail-closed). Returns a reason string
    when the row fails so callers can log it.
    """
    for key, expected in filters.items():
        actual = row.get(key)
        if actual is None or str(actual) != expected:
            return False, f"row_filter_mismatch:{key}"
    return True, None


def evaluate_visibility(
    entity_cls: type[BaseModel],
    row: dict[str, Any],
    scope: ScopeContext,
) -> VisibilityDecision:
    """Return a :class:`VisibilityDecision` for ``row`` under ``scope``."""
    hints = get_type_hints(entity_cls, include_extras=True)
    visible: set[str] = set()
    masked: set[str] = set()

    for field_name in entity_cls.model_fields:
        annotation = hints.get(field_name, str)
        classification = _find_classification(annotation)
        if classification is None:
            visible.add(field_name)
        elif classification in scope.classification_visibility:
            visible.add(field_name)
        else:
            masked.add(field_name)

    row_visible, reason = _row_filters_pass(row, scope.row_filters)

    return VisibilityDecision(
        entity_name=entity_cls.__name__,
        visible_fields=frozenset(visible),
        masked_fields=frozenset(masked),
        row_visible=row_visible,
        row_filter_reason=reason,
    )
