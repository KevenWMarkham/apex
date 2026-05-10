"""Tests for apex_core.protocols.persona_binding (Sprint 47.6)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from apex_core.protocols import (
    BindingMode,
    PersonaPrincipalBinding,
    UseCasePersonaBindings,
)


# ---------------------------------------------------------------------------
# 4 binding modes — happy paths
# ---------------------------------------------------------------------------


def test_entra_group_mode_minimal() -> None:
    b = PersonaPrincipalBinding(
        persona_id="jamie-oconnor-store-manager",
        binding_mode=BindingMode.ENTRA_GROUP,
        entra_group_object_id="8a3c1234-aaaa-bbbb-cccc-456789abcdef",
    )
    assert b.binding_mode is BindingMode.ENTRA_GROUP
    assert b.entra_group_object_id is not None


def test_specific_principals_mode_minimal() -> None:
    b = PersonaPrincipalBinding(
        persona_id="jamie-oconnor-store-manager",
        binding_mode=BindingMode.SPECIFIC_PRINCIPALS,
        fallback_principals=["sarah.kim@bigbox.com", "mike.reyes@bigbox.com"],
    )
    assert b.fallback_principals == ["sarah.kim@bigbox.com", "mike.reyes@bigbox.com"]


def test_shift_roster_mode_minimal() -> None:
    b = PersonaPrincipalBinding(
        persona_id="jamie-oconnor-store-manager",
        binding_mode=BindingMode.SHIFT_ROSTER,
        shift_roster_adapter="workday-shift-adapter",
    )
    assert b.shift_roster_adapter == "workday-shift-adapter"


def test_hybrid_mode_minimal() -> None:
    b = PersonaPrincipalBinding(
        persona_id="jamie-oconnor-store-manager",
        binding_mode=BindingMode.HYBRID,
        entra_group_object_id="8a3c1234-aaaa-bbbb-cccc-456789abcdef",
        fallback_principals=["sarah.kim@bigbox.com"],
    )
    assert b.entra_group_object_id is not None
    assert b.fallback_principals


# ---------------------------------------------------------------------------
# Mode-specific validation
# ---------------------------------------------------------------------------


def test_entra_group_requires_object_id() -> None:
    with pytest.raises(ValidationError, match="entra_group_object_id"):
        PersonaPrincipalBinding(
            persona_id="jamie-oconnor-store-manager",
            binding_mode=BindingMode.ENTRA_GROUP,
        )


def test_specific_principals_requires_fallback_list() -> None:
    with pytest.raises(ValidationError, match="fallback_principals"):
        PersonaPrincipalBinding(
            persona_id="jamie-oconnor-store-manager",
            binding_mode=BindingMode.SPECIFIC_PRINCIPALS,
        )


def test_shift_roster_requires_adapter() -> None:
    with pytest.raises(ValidationError, match="shift_roster_adapter"):
        PersonaPrincipalBinding(
            persona_id="jamie-oconnor-store-manager",
            binding_mode=BindingMode.SHIFT_ROSTER,
        )


def test_hybrid_requires_entra_group() -> None:
    with pytest.raises(ValidationError, match="entra_group_object_id"):
        PersonaPrincipalBinding(
            persona_id="jamie-oconnor-store-manager",
            binding_mode=BindingMode.HYBRID,
            fallback_principals=["sarah@x"],
        )


def test_hybrid_requires_fallback_principals() -> None:
    with pytest.raises(ValidationError, match="fallback_principals"):
        PersonaPrincipalBinding(
            persona_id="jamie-oconnor-store-manager",
            binding_mode=BindingMode.HYBRID,
            entra_group_object_id="8a3c-aaaa",
        )


def test_lifecycle_valid_to_after_valid_from() -> None:
    now = datetime.now(UTC)
    with pytest.raises(ValidationError, match="valid_to must be after valid_from"):
        PersonaPrincipalBinding(
            persona_id="test-persona",
            binding_mode=BindingMode.SPECIFIC_PRINCIPALS,
            fallback_principals=["a@b"],
            valid_from=now + timedelta(days=2),
            valid_to=now + timedelta(days=1),
        )


def test_audit_row_records_unknown_value_rejected() -> None:
    with pytest.raises(ValidationError, match="audit_row_records"):
        PersonaPrincipalBinding(
            persona_id="test-persona",
            binding_mode=BindingMode.SPECIFIC_PRINCIPALS,
            fallback_principals=["a@b"],
            audit_row_records="anything",
        )


def test_teams_chat_resolution_unknown_value_rejected() -> None:
    with pytest.raises(ValidationError, match="teams_chat_resolution"):
        PersonaPrincipalBinding(
            persona_id="test-persona",
            binding_mode=BindingMode.SPECIFIC_PRINCIPALS,
            fallback_principals=["a@b"],
            teams_chat_resolution="raw_token",
        )


# ---------------------------------------------------------------------------
# UseCasePersonaBindings container
# ---------------------------------------------------------------------------


def _bigbox_entra_binding() -> PersonaPrincipalBinding:
    return PersonaPrincipalBinding(
        persona_id="jamie-oconnor-store-manager",
        binding_mode=BindingMode.ENTRA_GROUP,
        entra_group_object_id="8a3c1234-aaaa-bbbb-cccc-456789abcdef",
        fallback_principals=["sarah.kim@bigbox.com"],
    )


def test_container_accepts_well_formed_bindings() -> None:
    binding = _bigbox_entra_binding()
    container = UseCasePersonaBindings(
        bindings={"jamie-oconnor-store-manager": binding},
    )
    assert container.is_persona_bound("jamie-oconnor-store-manager")


def test_container_rejects_key_persona_id_mismatch() -> None:
    binding = _bigbox_entra_binding()  # persona_id = jamie-oconnor-store-manager
    with pytest.raises(ValidationError, match="does not match persona_id"):
        UseCasePersonaBindings(
            bindings={"some-other-key": binding},
        )


def test_unresolved_personas_returns_unbound_list() -> None:
    container = UseCasePersonaBindings(
        bindings={"jamie-oconnor-store-manager": _bigbox_entra_binding()},
    )
    active = ["jamie-oconnor-store-manager", "marisol-reyes-store-ops"]
    unresolved = container.unresolved_personas(active)
    assert unresolved == ["marisol-reyes-store-ops"]


def test_is_persona_bound_returns_false_for_unknown() -> None:
    container = UseCasePersonaBindings(bindings={})
    assert container.is_persona_bound("nobody") is False
