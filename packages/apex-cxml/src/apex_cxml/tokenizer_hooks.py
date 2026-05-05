"""CXML tokenisation hooks.

Enumerates the attributes that the Silver-transform step (and the
``tokenizer-mcp`` utility server) must tokenise at the Bronze→Silver
boundary. The enumeration is derived automatically from each entity's
Pydantic annotations — any field marked ``Annotated[..., Classification.X]``
where ``X ∈ {PII, PHI, PCI, TRADE_SECRET, MEMBER_ONLY}`` is included.

See ``docs/APEX - Design and Build/APEX_Design.md`` §6.4.1 for the
tokenisation contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import NoneType, UnionType
from typing import Annotated, Any, Union, get_args, get_origin, get_type_hints

from pydantic import BaseModel

from apex_core.types import Classification

_TOKENISED_CLASSIFICATIONS: frozenset[Classification] = frozenset({
    Classification.PII,
    Classification.PHI,
    Classification.PCI,
    Classification.TRADE_SECRET,
    Classification.MEMBER_ONLY,
})


@dataclass(frozen=True, slots=True)
class TokenisedField:
    """One field scheduled for tokenisation in the Silver transform."""

    entity: str
    field: str
    classification: Classification


def _extract_classifications(annotation: Any) -> list[Classification]:
    """Pull every ``Classification`` from ``Annotated[...]`` metadata (through Optional)."""
    origin = get_origin(annotation)
    if origin is UnionType or origin is Union:
        out: list[Classification] = []
        for arg in get_args(annotation):
            if arg is NoneType:
                continue
            out.extend(_extract_classifications(arg))
        return out
    if origin is Annotated:
        return [m for m in get_args(annotation)[1:] if isinstance(m, Classification)]
    return []


def tokenized_fields(*entities: type[BaseModel]) -> list[TokenisedField]:
    """Return every field requiring tokenisation across the given entities.

    Args:
        *entities: Pydantic canonical entity classes.

    Returns:
        A list of :class:`TokenisedField`, sorted by ``(entity, field)``.
    """
    results: list[TokenisedField] = []
    for entity_cls in entities:
        hints = get_type_hints(entity_cls, include_extras=True)
        for field_name in entity_cls.model_fields:
            for classification in _extract_classifications(hints.get(field_name, str)):
                if classification in _TOKENISED_CLASSIFICATIONS:
                    results.append(
                        TokenisedField(
                            entity=entity_cls.__name__,
                            field=field_name,
                            classification=classification,
                        )
                    )
                    break
    return sorted(results, key=lambda t: (t.entity, t.field))
