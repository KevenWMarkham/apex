"""Tests for apex_identity.agent_safe_view.apply_agent_safe_view."""

from __future__ import annotations

from typing import Annotated

from pydantic import BaseModel

from apex_core.types import Classification, Practice
from apex_identity import apply_agent_safe_view
from mcp_common import ScopeContext


class _Patient(BaseModel):
    fhir_id: str
    mrn_token: Annotated[str, Classification.PHI] | None = None
    name_family_token: Annotated[str, Classification.PHI] | None = None
    birth_year: int | None = None
    gender: str | None = None
    region: str = "US-WEST"


def _scope(
    *, classifications: set[Classification] | None = None,
    row_filters: dict[str, str] | None = None,
) -> ScopeContext:
    return ScopeContext(
        tenant_id="t", practice=Practice.HLS,
        classification_visibility=frozenset(classifications or set()),
        row_filters=row_filters or {},
    )


def test_masks_phi_when_not_in_scope() -> None:
    p = _Patient(
        fhir_id="ex", mrn_token="tok_mrn",
        name_family_token="tok_fam", birth_year=1990, gender="female",
    )
    masked = apply_agent_safe_view(p, _scope())
    assert masked is not None
    assert masked.mrn_token is None
    assert masked.name_family_token is None
    assert masked.birth_year == 1990  # no classification → visible
    assert masked.fhir_id == "ex"


def test_preserves_phi_when_in_scope() -> None:
    p = _Patient(fhir_id="ex", mrn_token="tok_mrn")
    unmasked = apply_agent_safe_view(p, _scope(classifications={Classification.PHI}))
    assert unmasked is p  # identity — no mask needed


def test_row_filter_mismatch_returns_none() -> None:
    p = _Patient(fhir_id="ex", region="EU-EAST")
    result = apply_agent_safe_view(
        p, _scope(row_filters={"region": "US-WEST"}),
    )
    assert result is None


def test_row_filter_match_with_masking() -> None:
    p = _Patient(fhir_id="ex", mrn_token="tok_x", region="US-WEST")
    result = apply_agent_safe_view(
        p, _scope(row_filters={"region": "US-WEST"}),
    )
    assert result is not None
    assert result.mrn_token is None  # still masked — no PHI scope
