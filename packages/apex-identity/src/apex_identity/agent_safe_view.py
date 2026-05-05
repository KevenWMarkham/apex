"""Agent-safe view generator.

Converts a canonical entity instance into its scope-masked projection — the
exact shape an agent should see when its ``required_scopes`` have been
evaluated against the current :class:`ScopeContext`.
"""

from __future__ import annotations

from typing import TypeVar

from pydantic import BaseModel

from mcp_common import ScopeContext

from apex_identity.lattice import evaluate_visibility

_ModelT = TypeVar("_ModelT", bound=BaseModel)


def apply_agent_safe_view(
    instance: _ModelT,
    scope: ScopeContext,
) -> _ModelT | None:
    """Return a copy of ``instance`` with fields outside ``scope`` set to None.

    Behaviour:

    - Row-level filters reject the row → return ``None``.
    - No fields are masked → return ``instance`` (identity — no copy).
    - Otherwise → return ``instance.model_copy(update={...: None})`` with each
      masked field set to None.

    The masked-field-becomes-None policy is deliberate: schemas make masked
    fields optional (``T | None``) so agents gracefully handle the absence.
    """
    row = instance.model_dump()
    decision = evaluate_visibility(type(instance), row, scope)

    if not decision.row_visible:
        return None

    if not decision.masked_fields:
        return instance

    updates = {name: None for name in decision.masked_fields}
    return instance.model_copy(update=updates)
