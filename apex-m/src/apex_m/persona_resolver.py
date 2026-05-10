"""APEX-M Persona Resolver — turn a PersonaPrincipalBinding into live UPNs at HITL fire time.

Sprint 47.6 (work-back from Sprint 37 Q&A). The protocol-side schema lives
in ``apex_core.protocols.persona_binding`` (variant-neutral); this module
is APEX-M's resolver that calls Microsoft Graph + (optionally) the tenant's
workforce-management adapter.

Lazy import strategy
====================

This module imports cleanly without ``msal`` / ``azure-identity`` /
``httpx`` installed — runtime SDK calls happen lazily inside the
:class:`PersonaResolverEntra.resolve` method only, behind feature-flagged
branches. The :class:`MockPersonaResolverEntra` satisfies the same contract
for laptop substrate + unit tests.

When the runtime extras are installed:

    pip install -e 'apex-m[runtime]'

...the real resolver issues:

    GET /groups/{entra_group_object_id}/members?$filter=accountEnabled eq true

against Microsoft Graph using DefaultAzureCredential, scoped to
``https://graph.microsoft.com/.default``. Sprint 41's `identity_entra.py`
already wires the OBO + token acquisition machinery; this resolver shares
that token cache.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Protocol, runtime_checkable

from apex_core.protocols import (
    BindingMode,
    PersonaPrincipalBinding,
)


# ---------------------------------------------------------------------------
# Resolution result
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ResolvedPrincipals:
    """Output of :meth:`PersonaResolver.resolve` — live UPNs at HITL time.

    The Decide agent's HITL fan-out consumes this. The audit row records
    the resolved list (so an auditor can replay "Marisol approved this"
    even after Marisol leaves the company).
    """

    persona_id: str
    binding_mode: BindingMode
    principals: tuple[str, ...]
    resolved_at: datetime
    resolution_path: str    # human-readable trace of the resolver branch taken
    fallback_used: bool = False
    notes: str = ""


# ---------------------------------------------------------------------------
# Protocol — the contract APEX-G + APEX-A also implement
# ---------------------------------------------------------------------------


@runtime_checkable
class PersonaResolver(Protocol):
    """Resolve a :class:`PersonaPrincipalBinding` to live principals.

    Implementations:

    - :class:`PersonaResolverEntra` — APEX-M, calls Microsoft Graph
    - APEX-G ``PersonaResolverCloudIdentity`` (future) — Google Cloud Identity
    - APEX-A ``PersonaResolverIam`` (future) — AWS IAM Identity Center
    - :class:`MockPersonaResolverEntra` — laptop / unit-test substrate
    """

    def resolve(
        self,
        binding: PersonaPrincipalBinding,
        *,
        operator_obo_token: str | None = None,
    ) -> ResolvedPrincipals:
        """Return live principals authorised for the bound persona role.

        Empty ``principals`` tuple means no live members — the caller
        should NOT auto-approve and instead surface a "no available
        approver" alert (the framework's fail-closed posture).
        """
        ...


# ---------------------------------------------------------------------------
# APEX-M production resolver (Microsoft Graph)
# ---------------------------------------------------------------------------


class PersonaResolverEntra:
    """Concrete :class:`PersonaResolver` for APEX-M.

    Sprint 47.6 ships the resolver shape + dispatch logic. The Microsoft
    Graph SDK calls are still lazy-imported and gated behind feature
    flags — Sprint 41 production wiring lights them up.
    """

    variant = "APEX-M"

    def __init__(
        self,
        *,
        graph_token_provider: object | None = None,
        wfm_adapter: object | None = None,
    ) -> None:
        self._graph_token_provider = graph_token_provider
        self._wfm_adapter = wfm_adapter

    def resolve(
        self,
        binding: PersonaPrincipalBinding,
        *,
        operator_obo_token: str | None = None,
    ) -> ResolvedPrincipals:
        """Dispatch to the right binding-mode branch.

        Each branch is documented + reachable from tests. Sprint 41's
        production wiring ships the actual Graph + WFM HTTP calls; the
        skeleton is here so the dispatcher is testable today.
        """
        ts = datetime.now(UTC)

        if binding.binding_mode == BindingMode.SPECIFIC_PRINCIPALS:
            return ResolvedPrincipals(
                persona_id=binding.persona_id,
                binding_mode=binding.binding_mode,
                principals=tuple(binding.fallback_principals),
                resolved_at=ts,
                resolution_path="specific_principals → static list",
            )

        if binding.binding_mode == BindingMode.ENTRA_GROUP:
            principals = self._resolve_entra_group(binding, operator_obo_token)
            return ResolvedPrincipals(
                persona_id=binding.persona_id,
                binding_mode=binding.binding_mode,
                principals=tuple(principals),
                resolved_at=ts,
                resolution_path=(
                    f"entra_group → MSGraph GET /groups/{binding.entra_group_object_id}/members"
                ),
            )

        if binding.binding_mode == BindingMode.SHIFT_ROSTER:
            principals = self._resolve_shift_roster(binding, operator_obo_token)
            return ResolvedPrincipals(
                persona_id=binding.persona_id,
                binding_mode=binding.binding_mode,
                principals=tuple(principals),
                resolved_at=ts,
                resolution_path=(
                    f"shift_roster → adapter={binding.shift_roster_adapter} "
                    f"filter={binding.shift_roster_role_filter}"
                ),
            )

        if binding.binding_mode == BindingMode.HYBRID:
            # Try Entra group first; fall back to specific_principals if empty.
            primary = self._resolve_entra_group(binding, operator_obo_token)
            if primary:
                return ResolvedPrincipals(
                    persona_id=binding.persona_id,
                    binding_mode=binding.binding_mode,
                    principals=tuple(primary),
                    resolved_at=ts,
                    resolution_path=(
                        f"hybrid → entra_group({binding.entra_group_object_id}) "
                        f"returned {len(primary)} members"
                    ),
                )
            return ResolvedPrincipals(
                persona_id=binding.persona_id,
                binding_mode=binding.binding_mode,
                principals=tuple(binding.fallback_principals),
                resolved_at=ts,
                resolution_path="hybrid → entra_group empty; falling back to specific_principals",
                fallback_used=True,
                notes=(
                    "Primary Entra group returned no on-shift / accountEnabled members. "
                    "Static fallback list applied."
                ),
            )

        raise ValueError(
            f"Unknown binding_mode {binding.binding_mode!r} — "
            "Sprint 47.6 schema bug"
        )

    # ------------------------------------------------------------------
    # Branch implementations — Sprint 41 production wiring lights up real
    # Microsoft Graph + tenant WFM HTTP calls. Today these raise
    # NotImplementedError when invoked without the runtime extras
    # installed; the mock resolver covers the test path.
    # ------------------------------------------------------------------

    def _resolve_entra_group(
        self,
        binding: PersonaPrincipalBinding,
        operator_obo_token: str | None,
    ) -> list[str]:
        try:
            import httpx                 # type: ignore[import-not-found]
            from azure.identity import DefaultAzureCredential  # type: ignore[import-not-found]
        except ImportError:               # pragma: no cover — unit-test path
            raise NotImplementedError(
                "PersonaResolverEntra._resolve_entra_group requires apex-m[runtime] "
                "extras (azure-identity + httpx). Use MockPersonaResolverEntra in "
                "non-Lab environments."
            )

        cred = self._graph_token_provider or DefaultAzureCredential()
        token = cred.get_token("https://graph.microsoft.com/.default").token  # type: ignore[union-attr]
        url = (
            f"https://graph.microsoft.com/v1.0/groups/"
            f"{binding.entra_group_object_id}/members"
            f"?$filter=accountEnabled eq true&$select=userPrincipalName"
        )
        headers = {"Authorization": f"Bearer {token}"}
        with httpx.Client(timeout=30.0) as client:  # pragma: no cover
            response = client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return [m["userPrincipalName"] for m in data.get("value", [])]

    def _resolve_shift_roster(
        self,
        binding: PersonaPrincipalBinding,
        operator_obo_token: str | None,
    ) -> list[str]:
        if self._wfm_adapter is None:
            raise NotImplementedError(
                "PersonaResolverEntra._resolve_shift_roster requires a wfm_adapter "
                f"(use-case declared shift_roster_adapter={binding.shift_roster_adapter!r})."
            )
        # Sprint 41 / per-engagement: the adapter is duck-typed; supports
        # query_active_principals(role_filter=...) returning list[str].
        return self._wfm_adapter.query_active_principals(  # type: ignore[no-any-return,attr-defined]
            role_filter=binding.shift_roster_role_filter,
        )


# ---------------------------------------------------------------------------
# Mock — laptop / unit-test resolver
# ---------------------------------------------------------------------------


@dataclass
class MockPersonaResolverEntra:
    """Test / laptop resolver. Returns canned principals per binding mode.

    Mock semantics:

    - ``ENTRA_GROUP``: returns ``mock_group_members[entra_group_object_id]`` if
      registered, else empty list.
    - ``SPECIFIC_PRINCIPALS``: returns ``binding.fallback_principals`` verbatim.
    - ``SHIFT_ROSTER``: returns ``mock_roster[shift_roster_adapter]`` if
      registered, else empty list.
    - ``HYBRID``: tries entra_group; falls back to specific_principals when empty.
    """

    variant: str = "APEX-M-mock"
    mock_group_members: dict[str, list[str]] = field(default_factory=dict)
    mock_roster: dict[str, list[str]] = field(default_factory=dict)

    def resolve(
        self,
        binding: PersonaPrincipalBinding,
        *,
        operator_obo_token: str | None = None,
    ) -> ResolvedPrincipals:
        ts = datetime.now(UTC)

        if binding.binding_mode == BindingMode.SPECIFIC_PRINCIPALS:
            return ResolvedPrincipals(
                persona_id=binding.persona_id,
                binding_mode=binding.binding_mode,
                principals=tuple(binding.fallback_principals),
                resolved_at=ts,
                resolution_path="MOCK specific_principals → static list",
            )

        if binding.binding_mode == BindingMode.ENTRA_GROUP:
            members = self.mock_group_members.get(binding.entra_group_object_id or "", [])
            return ResolvedPrincipals(
                persona_id=binding.persona_id,
                binding_mode=binding.binding_mode,
                principals=tuple(members),
                resolved_at=ts,
                resolution_path=(
                    f"MOCK entra_group → {len(members)} members for "
                    f"group_id={binding.entra_group_object_id!r}"
                ),
            )

        if binding.binding_mode == BindingMode.SHIFT_ROSTER:
            members = self.mock_roster.get(binding.shift_roster_adapter or "", [])
            return ResolvedPrincipals(
                persona_id=binding.persona_id,
                binding_mode=binding.binding_mode,
                principals=tuple(members),
                resolved_at=ts,
                resolution_path=(
                    f"MOCK shift_roster → {len(members)} on-shift via adapter "
                    f"{binding.shift_roster_adapter!r}"
                ),
            )

        if binding.binding_mode == BindingMode.HYBRID:
            primary = self.mock_group_members.get(binding.entra_group_object_id or "", [])
            if primary:
                return ResolvedPrincipals(
                    persona_id=binding.persona_id,
                    binding_mode=binding.binding_mode,
                    principals=tuple(primary),
                    resolved_at=ts,
                    resolution_path=(
                        f"MOCK hybrid → entra_group returned {len(primary)} members"
                    ),
                )
            return ResolvedPrincipals(
                persona_id=binding.persona_id,
                binding_mode=binding.binding_mode,
                principals=tuple(binding.fallback_principals),
                resolved_at=ts,
                resolution_path="MOCK hybrid → entra_group empty; static fallback applied",
                fallback_used=True,
            )

        raise ValueError(f"Unknown binding_mode {binding.binding_mode!r}")
