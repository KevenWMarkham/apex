"""Scope-context stub (Sprint 10 replaces with the real visibility lattice)."""

from __future__ import annotations

from dataclasses import dataclass, field

from apex_core.types import Classification, Practice


@dataclass(frozen=True, slots=True)
class ScopeContext:
    """The caller's resolved scope for one tool invocation.

    Sprint 7 ships a thin structural shape. Sprint 10 (`apex-identity`)
    replaces the evaluator with the full lattice that composes tenant ×
    practice × persona × classification × row filters.
    """

    tenant_id: str
    practice: Practice | None = None
    persona: str | None = None
    classification_visibility: frozenset[Classification] = field(
        default_factory=frozenset,
    )
    row_filters: dict[str, str] = field(default_factory=dict)


def scope_allows(
    ctx: ScopeContext,
    *,
    required_scopes: list[str],
    data_classifications: list[Classification] | None = None,
) -> bool:
    """Return True iff ``ctx`` satisfies every required scope and can see the data.

    Sprint 7 scope check:

    - Each required scope of form ``"dim:value"`` (e.g. ``"practice:rc"``,
      ``"persona:store-ops-lead"``) matches the context dimension.
    - Every classification in ``data_classifications`` must be in
      ``ctx.classification_visibility`` — else the data is invisible.

    Unknown dimensions return False (fail closed).
    """
    classifications = data_classifications or []
    for cls in classifications:
        if cls not in ctx.classification_visibility:
            return False

    for scope in required_scopes:
        if ":" not in scope:
            return False
        dim, value = scope.split(":", 1)
        dim = dim.strip().lower()
        value = value.strip()
        if dim == "tenant":
            if ctx.tenant_id != value:
                return False
        elif dim == "practice":
            if ctx.practice is None or ctx.practice.value != value.lower():
                return False
        elif dim == "persona":
            if ctx.persona != value:
                return False
        else:
            return False
    return True
