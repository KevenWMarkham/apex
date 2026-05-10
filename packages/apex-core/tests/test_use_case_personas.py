"""Tests for the Sprint 47.6 / PSG-15 use-case persona-binding validator."""

from __future__ import annotations

import pytest

from apex_core.protocols import (
    BindingMode,
    PersonaPrincipalBinding,
    UseCasePersonaBindings,
)
from apex_core.validators import (
    SYNTHETIC_LAB_PERSONAS,
    Substrate,
    quick_check_psg_15,
    validate_use_case_personas,
)


# ---------------------------------------------------------------------------
# Substrate-aware behaviour
# ---------------------------------------------------------------------------


def _bigbox_entra_binding() -> PersonaPrincipalBinding:
    return PersonaPrincipalBinding(
        persona_id="jamie-oconnor-store-manager",
        binding_mode=BindingMode.ENTRA_GROUP,
        entra_group_object_id="8a3c1234-aaaa-bbbb-cccc-456789abcdef",
        fallback_principals=["sarah.kim@bigbox.com"],
    )


def test_laptop_substrate_allows_synthetic_personas_without_bindings() -> None:
    """Lab worked-example mode — synthetic personas are fine."""
    use_case = {
        "use_case_id": "rc-e2e-05--default",
        "substrate": "laptop",
        "personas_active": [{"id": "jamie-oconnor-store-manager"}],
        "persona_principal_bindings": {},
    }
    report = validate_use_case_personas(use_case)
    assert report.valid is True
    assert report.errors == []
    assert report.fails_psg_15 is False


def test_lab_substrate_warns_on_unbound_personas_but_does_not_fail() -> None:
    use_case = {
        "use_case_id": "rc-e2e-05--default",
        "substrate": "lab",
        "personas_active": [{"id": "jamie-oconnor-store-manager"}],
    }
    report = validate_use_case_personas(use_case)
    assert report.valid is True
    assert report.errors == []
    assert len(report.warnings) >= 1
    assert report.fails_psg_15 is False


def test_prod_substrate_fails_closed_on_unbound_personas() -> None:
    """PSG-15 fail-closed — synthetic personas without bindings on prod."""
    use_case = {
        "use_case_id": "rc-e2e-05--bigbox-prod",
        "substrate": "prod",
        "personas_active": [{"id": "jamie-oconnor-store-manager"}],
        "persona_principal_bindings": {},
    }
    report = validate_use_case_personas(use_case)
    assert report.valid is False
    assert report.fails_psg_15 is True
    assert report.errors


def test_prod_substrate_passes_with_bindings() -> None:
    """When the operator binds the persona, deploy proceeds."""
    use_case = {
        "use_case_id": "rc-e2e-05--bigbox-prod",
        "substrate": "prod",
        "personas_active": [{"id": "jamie-oconnor-store-manager"}],
        "persona_principal_bindings": {
            "jamie-oconnor-store-manager": {
                "binding_mode": "entra_group",
                "entra_group_object_id": "8a3c1234-aaaa-bbbb-cccc-456789abcdef",
            },
        },
    }
    report = validate_use_case_personas(use_case)
    assert report.valid is True
    assert report.fails_psg_15 is False
    assert report.unresolved_personas == []


def test_prod_substrate_partial_binding_fails_for_unbound_persona() -> None:
    """One persona bound + one unbound = still fails on prod."""
    use_case = {
        "use_case_id": "rc-e2e--multi-persona",
        "substrate": "prod",
        "personas_active": [
            {"id": "jamie-oconnor-store-manager"},
            {"id": "marisol-reyes-store-ops"},
        ],
        "persona_principal_bindings": {
            "jamie-oconnor-store-manager": {
                "binding_mode": "entra_group",
                "entra_group_object_id": "group-1",
            },
        },
    }
    report = validate_use_case_personas(use_case)
    assert report.valid is False
    assert "marisol-reyes-store-ops" in report.unresolved_personas


def test_dev_substrate_also_enforces_psg_15() -> None:
    """Dev substrate = same hard-fail as prod."""
    use_case = {
        "use_case_id": "rc-e2e--dev",
        "substrate": "dev",
        "personas_active": [{"id": "jamie-oconnor-store-manager"}],
    }
    report = validate_use_case_personas(use_case)
    assert report.fails_psg_15 is True


# ---------------------------------------------------------------------------
# personas_active shape tolerance
# ---------------------------------------------------------------------------


def test_validator_accepts_list_of_dicts_with_id() -> None:
    use_case = {
        "use_case_id": "x",
        "substrate": "laptop",
        "personas_active": [{"id": "jamie-oconnor-store-manager"}],
    }
    report = validate_use_case_personas(use_case)
    assert report.personas_active == ["jamie-oconnor-store-manager"]


def test_validator_accepts_list_of_strings() -> None:
    use_case = {
        "use_case_id": "x",
        "substrate": "laptop",
        "personas_active": ["jamie-oconnor-store-manager"],
    }
    report = validate_use_case_personas(use_case)
    assert report.personas_active == ["jamie-oconnor-store-manager"]


def test_validator_rejects_unexpected_persona_entry_shape() -> None:
    use_case = {
        "use_case_id": "x",
        "substrate": "laptop",
        "personas_active": [42],
    }
    report = validate_use_case_personas(use_case)
    assert report.valid is False
    assert "unexpected entry shape" in report.errors[0]


# ---------------------------------------------------------------------------
# Schema parsing — embedded PersonaPrincipalBinding dicts
# ---------------------------------------------------------------------------


def test_validator_parses_yaml_dict_into_pydantic_model() -> None:
    use_case = {
        "use_case_id": "x",
        "substrate": "lab",
        "personas_active": [{"id": "test-persona"}],
        "persona_principal_bindings": {
            "test-persona": {
                "binding_mode": "specific_principals",
                "fallback_principals": ["a@b.com"],
            },
        },
    }
    report = validate_use_case_personas(use_case)
    assert report.valid is True
    assert report.bindings_count == 1


def test_validator_rejects_invalid_binding_block() -> None:
    use_case = {
        "use_case_id": "x",
        "substrate": "lab",
        "personas_active": [{"id": "test-persona"}],
        "persona_principal_bindings": {
            "test-persona": {
                "binding_mode": "entra_group",
                # missing entra_group_object_id
            },
        },
    }
    report = validate_use_case_personas(use_case)
    assert report.valid is False
    assert "did not parse against the schema" in report.errors[0]


def test_validator_unknown_substrate_rejected() -> None:
    use_case = {
        "use_case_id": "x",
        "substrate": "moon-base",
        "personas_active": [],
    }
    report = validate_use_case_personas(use_case)
    assert report.valid is False
    assert "substrate" in report.errors[0]


# ---------------------------------------------------------------------------
# quick_check_psg_15 helper
# ---------------------------------------------------------------------------


def test_quick_check_psg_15_returns_true_on_clean_prod() -> None:
    use_case = {
        "use_case_id": "x",
        "substrate": "prod",
        "personas_active": [{"id": "jamie-oconnor-store-manager"}],
        "persona_principal_bindings": {
            "jamie-oconnor-store-manager": {
                "binding_mode": "entra_group",
                "entra_group_object_id": "group-1",
            },
        },
    }
    assert quick_check_psg_15(use_case) is True


def test_quick_check_psg_15_returns_false_on_unbound_prod() -> None:
    use_case = {
        "use_case_id": "x",
        "substrate": "prod",
        "personas_active": [{"id": "jamie-oconnor-store-manager"}],
    }
    assert quick_check_psg_15(use_case) is False


def test_quick_check_psg_15_returns_true_on_laptop_substrate() -> None:
    """Laptop substrate never fails PSG-15 — synthetic personas are fine."""
    use_case = {
        "use_case_id": "x",
        "substrate": "laptop",
        "personas_active": [{"id": "jamie-oconnor-store-manager"}],
    }
    assert quick_check_psg_15(use_case) is True


# ---------------------------------------------------------------------------
# Synthetic-personas catalog coverage
# ---------------------------------------------------------------------------


def test_synthetic_lab_personas_covers_all_6_rc_personas() -> None:
    """Sprint 47.6 — the 6 RC personas in services/_personas.yaml."""
    expected = {
        "marisol-reyes-store-ops",
        "daniel-chen-merch-director",
        "maya-patel-loyalty-crm-director",
        "jamie-oconnor-store-manager",
        "rebecca-hall-returns-ops-mgr",
        "compliance-officer-fsma-204",
    }
    assert SYNTHETIC_LAB_PERSONAS == frozenset(expected)
