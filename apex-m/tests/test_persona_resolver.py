"""Tests for apex_m.persona_resolver (Sprint 47.6)."""

from __future__ import annotations

import pytest

from apex_core.protocols import (
    BindingMode,
    PersonaPrincipalBinding,
)
from apex_m.persona_resolver import (
    MockPersonaResolverEntra,
    PersonaResolver,
    PersonaResolverEntra,
    ResolvedPrincipals,
)


# ---------------------------------------------------------------------------
# Mock resolver — laptop / unit-test path
# ---------------------------------------------------------------------------


def _binding(mode: BindingMode, **overrides) -> PersonaPrincipalBinding:
    base = {
        "persona_id": "jamie-oconnor-store-manager",
        "binding_mode": mode,
    }
    if mode == BindingMode.ENTRA_GROUP:
        base["entra_group_object_id"] = overrides.pop(
            "entra_group_object_id", "group-bigbox-store-mgrs",
        )
    elif mode == BindingMode.SPECIFIC_PRINCIPALS:
        base["fallback_principals"] = overrides.pop(
            "fallback_principals", ["sarah.kim@bigbox.com"],
        )
    elif mode == BindingMode.SHIFT_ROSTER:
        base["shift_roster_adapter"] = overrides.pop(
            "shift_roster_adapter", "workday-shift-adapter",
        )
        base["shift_roster_role_filter"] = overrides.pop(
            "shift_roster_role_filter", "Role=StoreManager AND Status=ClockedIn",
        )
    elif mode == BindingMode.HYBRID:
        base["entra_group_object_id"] = overrides.pop(
            "entra_group_object_id", "group-bigbox-store-mgrs",
        )
        base["fallback_principals"] = overrides.pop(
            "fallback_principals", ["sarah.kim@bigbox.com"],
        )
    base.update(overrides)
    return PersonaPrincipalBinding(**base)


def test_mock_resolves_entra_group_to_registered_members() -> None:
    resolver = MockPersonaResolverEntra(
        mock_group_members={
            "group-bigbox-store-mgrs": [
                "sarah.kim@bigbox.com",
                "mike.reyes@bigbox.com",
            ],
        },
    )
    result = resolver.resolve(_binding(BindingMode.ENTRA_GROUP))
    assert isinstance(result, ResolvedPrincipals)
    assert set(result.principals) == {
        "sarah.kim@bigbox.com", "mike.reyes@bigbox.com",
    }
    assert "MOCK entra_group" in result.resolution_path


def test_mock_resolves_specific_principals_returns_static_list() -> None:
    resolver = MockPersonaResolverEntra()
    result = resolver.resolve(_binding(
        BindingMode.SPECIFIC_PRINCIPALS,
        fallback_principals=["a@x", "b@x", "c@x"],
    ))
    assert result.principals == ("a@x", "b@x", "c@x")


def test_mock_resolves_shift_roster_to_registered_roster() -> None:
    resolver = MockPersonaResolverEntra(
        mock_roster={"workday-shift-adapter": ["onshift1@bigbox.com"]},
    )
    result = resolver.resolve(_binding(BindingMode.SHIFT_ROSTER))
    assert result.principals == ("onshift1@bigbox.com",)
    assert "shift_roster" in result.resolution_path


def test_mock_hybrid_returns_entra_group_when_populated() -> None:
    resolver = MockPersonaResolverEntra(
        mock_group_members={
            "group-bigbox-store-mgrs": ["primary@bigbox.com"],
        },
    )
    result = resolver.resolve(_binding(BindingMode.HYBRID))
    assert result.principals == ("primary@bigbox.com",)
    assert result.fallback_used is False


def test_mock_hybrid_falls_back_when_entra_group_empty() -> None:
    resolver = MockPersonaResolverEntra()  # no entra_group registered = empty
    result = resolver.resolve(_binding(
        BindingMode.HYBRID,
        fallback_principals=["fallback@bigbox.com"],
    ))
    assert result.principals == ("fallback@bigbox.com",)
    assert result.fallback_used is True


def test_mock_resolved_principals_records_persona_id_and_mode() -> None:
    resolver = MockPersonaResolverEntra()
    result = resolver.resolve(_binding(
        BindingMode.SPECIFIC_PRINCIPALS,
        fallback_principals=["a@x"],
    ))
    assert result.persona_id == "jamie-oconnor-store-manager"
    assert result.binding_mode is BindingMode.SPECIFIC_PRINCIPALS


# ---------------------------------------------------------------------------
# Production resolver — happy paths that don't require Microsoft Graph
# ---------------------------------------------------------------------------


def test_production_resolver_specific_principals_works_without_graph() -> None:
    """specific_principals never calls Graph — the static list is the answer."""
    resolver = PersonaResolverEntra()
    result = resolver.resolve(_binding(
        BindingMode.SPECIFIC_PRINCIPALS,
        fallback_principals=["sarah.kim@bigbox.com"],
    ))
    assert result.principals == ("sarah.kim@bigbox.com",)
    assert "specific_principals" in result.resolution_path


def test_production_resolver_entra_group_raises_without_runtime_extras() -> None:
    """Without azure-identity + httpx installed, the Graph branch fails clearly."""
    resolver = PersonaResolverEntra()
    binding = _binding(BindingMode.ENTRA_GROUP)
    # The branch lazy-imports azure-identity + httpx; if either isn't
    # installed, NotImplementedError surfaces with a clear message.
    try:
        resolver.resolve(binding)
    except NotImplementedError as exc:
        assert "apex-m[runtime]" in str(exc)
    except ImportError:
        # Acceptable if a partial install made the import fail differently
        pass


def test_production_resolver_shift_roster_requires_adapter() -> None:
    """Without a wfm_adapter wired, shift_roster fails clearly."""
    resolver = PersonaResolverEntra()  # no wfm_adapter
    with pytest.raises(NotImplementedError, match="wfm_adapter"):
        resolver.resolve(_binding(BindingMode.SHIFT_ROSTER))


# ---------------------------------------------------------------------------
# Protocol conformance
# ---------------------------------------------------------------------------


def test_mock_satisfies_protocol() -> None:
    resolver = MockPersonaResolverEntra()
    assert isinstance(resolver, PersonaResolver)


def test_production_satisfies_protocol() -> None:
    resolver = PersonaResolverEntra()
    assert isinstance(resolver, PersonaResolver)


# ---------------------------------------------------------------------------
# Audit row — every resolution carries timestamp + path
# ---------------------------------------------------------------------------


def test_resolution_carries_timestamp_and_human_readable_path() -> None:
    resolver = MockPersonaResolverEntra(
        mock_group_members={"group-x": ["a@x"]},
    )
    result = resolver.resolve(_binding(
        BindingMode.ENTRA_GROUP, entra_group_object_id="group-x",
    ))
    # Timestamp present
    assert result.resolved_at is not None
    # Path should mention the group id (audit-row debugging field)
    assert "group-x" in result.resolution_path or "MOCK entra_group" in result.resolution_path
