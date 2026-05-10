"""PersonaPrincipalBinding — provider-neutral schema for role → live-principal mapping.

Sprint 47.6 (work-back from Sprint 37 Q&A on persona-vs-principal).

The framework's agent.yaml `hitl_persona` field carries a stable **role**
identifier (e.g. ``jamie-oconnor-store-manager``). Real client tenants need
to bind that role to **live principals** — the actual people who occupy the
role at the client. This module defines the canonical four binding modes
the use-case YAML uses to declare those bindings.

Why provider-neutral
====================

This lives in ``apex-core`` (not ``apex-m``) because:

- APEX-G + APEX-A variants need the same binding semantics.
- The validator (used by the Pre-deployment Security Gate PSG-15 lint)
  must work without importing any cloud SDK.
- Only the *resolver* — turning a binding into a live principal list at
  HITL fire time — is variant-specific. APEX-M's resolver lives in
  ``apex_m.persona_resolver`` and uses Microsoft Graph.

References
----------

- Cross-Service-Boundaries.md (Sprint 39)
- Pre-deployment-Security-Gate.md PSG-15 (Sprint 47.6 — adds the lint)
- agent-identity-blueprints.md (Phase I.1 design)
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator


class BindingMode(StrEnum):
    """How a persona resolves to live principals at HITL fire time."""

    ENTRA_GROUP = "entra_group"
    """Resolves via Microsoft Graph group-members lookup. Default for most clients —
    a group of 5–15 managers across shifts. APEX-M reads via Graph; APEX-G via
    Cloud Identity; APEX-A via IAM groups."""

    SPECIFIC_PRINCIPALS = "specific_principals"
    """Static list of UPNs / email-like identifiers in the use-case YAML.
    Use when the client has a fixed roster (e.g. small store with 1–3 named managers).
    No directory lookup at runtime."""

    SHIFT_ROSTER = "shift_roster"
    """Resolves at runtime by querying the tenant's workforce-management SOR
    for who holds the role on shift right now. Use for 24×7 operations with
    on-shift logic. APEX-M's resolver wraps the configured WFM adapter."""

    HYBRID = "hybrid"
    """Tries entra_group first; falls back to specific_principals if no on-shift
    members found. Production default for real clients — group for routine,
    static list for after-hours escalation."""


class PersonaPrincipalBinding(BaseModel):
    """Bind a framework persona role to live principals at the client tenant.

    Carried in the use-case YAML under ``persona_principal_bindings``.
    The Pre-deployment Security Gate PSG-15 lint verifies every persona in
    ``personas_active`` has a binding before the deploy button enables.

    The schema is variant-neutral. APEX-M's resolver
    (``apex_m.persona_resolver``) interprets ``entra_group_object_id`` as a
    Microsoft Graph group id; APEX-G's resolver would interpret it as a
    Cloud Identity group id; APEX-A's as an IAM group.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    persona_id: Annotated[str, StringConstraints(min_length=3, max_length=128)] = Field(
        ...,
        description="Stable framework role identifier (e.g. jamie-oconnor-store-manager). "
                    "Must match a key in services/_personas.yaml."
    )

    binding_mode: BindingMode

    # --- entra_group / hybrid mode --------------------------------------
    entra_group_object_id: Annotated[str, StringConstraints(max_length=128)] | None = Field(
        None,
        description="Required when binding_mode in [entra_group, hybrid]. "
                    "GUID of the Entra group containing authorised principals."
    )

    # --- specific_principals / hybrid mode (fallback) -------------------
    fallback_principals: list[str] = Field(
        default_factory=list,
        description="UPNs (or provider-equivalent identifiers) authorised for this role. "
                    "Required when binding_mode == specific_principals; optional fallback "
                    "for hybrid; ignored in entra_group + shift_roster modes."
    )

    # --- shift_roster / hybrid mode -------------------------------------
    shift_roster_adapter: Annotated[str, StringConstraints(max_length=64)] | None = Field(
        None,
        description="Required when binding_mode in [shift_roster, hybrid]. "
                    "Adapter id from client_approved_architecture (e.g. 'workday-shift-adapter')."
    )
    shift_roster_role_filter: Annotated[str, StringConstraints(max_length=128)] | None = Field(
        None,
        description="Role-filter expression the WFM adapter understands "
                    "(e.g. 'Role=StoreManager AND Status=ClockedIn')."
    )

    # --- runtime + audit ----------------------------------------------
    teams_chat_resolution: Annotated[str, StringConstraints(max_length=32)] = Field(
        "directory_lookup",
        description="How the chat client renders display names. "
                    "directory_lookup = resolve UPN → display name at render time. "
                    "raw_upn = show the UPN literally (rare; debugging only)."
    )
    audit_row_records: Annotated[str, StringConstraints(max_length=32)] = Field(
        "principal_only",
        description="What gets recorded in the audit row's operator_principal field. "
                    "principal_only = UPN; principal_and_persona = both UPN + persona_id; "
                    "persona_only = persona_id (NOT recommended — loses individual accountability)."
    )

    # --- lifecycle ------------------------------------------------------
    valid_from: datetime | None = Field(
        None,
        description="When this binding becomes active. Null = always active."
    )
    valid_to: datetime | None = Field(
        None,
        description="When this binding expires. Null = no expiry."
    )

    @model_validator(mode="after")
    def _validate_binding_mode_fields(self) -> "PersonaPrincipalBinding":
        """Each binding_mode requires its own field set."""
        if self.binding_mode == BindingMode.ENTRA_GROUP:
            if not self.entra_group_object_id:
                raise ValueError(
                    "binding_mode=entra_group requires entra_group_object_id"
                )

        elif self.binding_mode == BindingMode.SPECIFIC_PRINCIPALS:
            if not self.fallback_principals:
                raise ValueError(
                    "binding_mode=specific_principals requires fallback_principals "
                    "(the static UPN list)"
                )

        elif self.binding_mode == BindingMode.SHIFT_ROSTER:
            if not self.shift_roster_adapter:
                raise ValueError(
                    "binding_mode=shift_roster requires shift_roster_adapter"
                )

        elif self.binding_mode == BindingMode.HYBRID:
            if not self.entra_group_object_id:
                raise ValueError(
                    "binding_mode=hybrid requires entra_group_object_id (primary path)"
                )
            if not self.fallback_principals:
                raise ValueError(
                    "binding_mode=hybrid requires fallback_principals (fallback path)"
                )

        return self

    @model_validator(mode="after")
    def _validate_lifecycle(self) -> "PersonaPrincipalBinding":
        if self.valid_from is not None and self.valid_to is not None:
            if self.valid_to <= self.valid_from:
                raise ValueError("valid_to must be after valid_from")
        return self

    @model_validator(mode="after")
    def _validate_audit_row_records(self) -> "PersonaPrincipalBinding":
        if self.audit_row_records not in (
            "principal_only", "principal_and_persona", "persona_only",
        ):
            raise ValueError(
                f"audit_row_records {self.audit_row_records!r} not in "
                "{principal_only, principal_and_persona, persona_only}"
            )
        return self

    @model_validator(mode="after")
    def _validate_teams_chat_resolution(self) -> "PersonaPrincipalBinding":
        if self.teams_chat_resolution not in ("directory_lookup", "raw_upn"):
            raise ValueError(
                f"teams_chat_resolution {self.teams_chat_resolution!r} not in "
                "{directory_lookup, raw_upn}"
            )
        return self


class UseCasePersonaBindings(BaseModel):
    """Top-level container in the use-case YAML.

    Maps each entry in ``personas_active`` to its
    :class:`PersonaPrincipalBinding`. The Pre-deployment Security Gate
    PSG-15 lint walks this structure on prod-substrate deploys and
    fails closed on any unbound persona.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    bindings: dict[str, PersonaPrincipalBinding] = Field(
        default_factory=dict,
        description="Map of persona_id (matching personas_active entries) "
                    "to their binding. Each binding's persona_id field MUST "
                    "match its key (validator enforces).",
    )

    @model_validator(mode="after")
    def _validate_keys_match_persona_ids(self) -> "UseCasePersonaBindings":
        for key, binding in self.bindings.items():
            if binding.persona_id != key:
                raise ValueError(
                    f"binding key {key!r} does not match persona_id "
                    f"{binding.persona_id!r}"
                )
        return self

    def is_persona_bound(self, persona_id: str) -> bool:
        """Return True if a binding exists for the given persona_id."""
        return persona_id in self.bindings

    def unresolved_personas(self, personas_active: list[str]) -> list[str]:
        """Return personas_active entries that have no binding.

        This is the helper the PSG-15 lint calls. A non-empty result means
        the use-case still has framework synthetic personas (e.g.
        jamie-oconnor-store-manager) without a real-client binding —
        deploy must fail closed.
        """
        return [p for p in personas_active if not self.is_persona_bound(p)]
