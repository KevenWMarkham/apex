"""Use-case persona-binding validator (Sprint 47.6 / PSG-15).

Walks a use-case YAML structure and verifies every entry in
``personas_active`` has a resolvable binding in
``persona_principal_bindings``. The Pre-deployment Security Gate's
PSG-15 check fires this before the deploy button enables on the wizard.

Fail-closed semantics
=====================

The validator's behaviour depends on the use-case ``substrate`` field:

- ``laptop`` — synthetic personas (e.g., ``jamie-oconnor-store-manager``)
  are allowed; this is the framework's worked-example mode. No bindings
  required.
- ``lab`` — bindings are recommended but not required. The validator
  returns warnings but does not fail.
- ``dev`` / ``stage`` / ``prod`` — every active persona MUST have a
  resolvable binding. Synthetic Lab personas without a binding cause a
  hard failure. The wizard surfaces the failure and disables deploy.

This three-tier behaviour matches the apex_m.runtime_foundry's
``substrate``-aware mock vs real swap.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from apex_core.protocols.persona_binding import (
    PersonaPrincipalBinding,
    UseCasePersonaBindings,
)


# ---------------------------------------------------------------------------
# Substrate awareness
# ---------------------------------------------------------------------------


class Substrate(StrEnum):
    LAPTOP = "laptop"
    LAB = "lab"
    DEV = "dev"
    STAGE = "stage"
    PROD = "prod"


# Personas that ship with the framework as Lab worked examples.
# Real client tenants must NOT have these in personas_active on prod
# substrate without a binding (the PSG-15 lint catches this).
SYNTHETIC_LAB_PERSONAS: frozenset[str] = frozenset({
    "marisol-reyes-store-ops",
    "daniel-chen-merch-director",
    "maya-patel-loyalty-crm-director",
    "jamie-oconnor-store-manager",
    "rebecca-hall-returns-ops-mgr",
    "compliance-officer-fsma-204",
})


# ---------------------------------------------------------------------------
# Validation report
# ---------------------------------------------------------------------------


@dataclass
class PersonaBindingValidationReport:
    """Output of :func:`validate_use_case_personas`.

    The wizard's pre-deployment Security Gate page renders this as a
    structured failure list.
    """

    use_case_id: str
    substrate: Substrate
    personas_active: list[str]
    bindings_count: int
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    synthetic_personas_present_on_non_laptop: list[str] = field(default_factory=list)
    unresolved_personas: list[str] = field(default_factory=list)

    @property
    def fails_psg_15(self) -> bool:
        """True iff PSG-15 should block deploy (substrate ≥ dev with errors)."""
        return self.substrate in (Substrate.DEV, Substrate.STAGE, Substrate.PROD) and bool(self.errors)


# ---------------------------------------------------------------------------
# Validator entry-point
# ---------------------------------------------------------------------------


def validate_use_case_personas(
    use_case_data: dict[str, Any],
    *,
    bindings: UseCasePersonaBindings | None = None,
) -> PersonaBindingValidationReport:
    """Validate the persona-bindings of a parsed use-case YAML dict.

    Args:
        use_case_data: The parsed use-case YAML — must contain
            ``use_case_id``, ``substrate``, ``personas_active`` keys at
            minimum. ``persona_principal_bindings`` is optional in the
            YAML (the wizard may inject bindings at deploy time from a
            tenant config file).
        bindings: Pre-validated :class:`UseCasePersonaBindings` if the
            caller already parsed them. When ``None``, the validator
            reads ``use_case_data['persona_principal_bindings']`` and
            constructs the model itself (raising ``ValueError`` on a
            schema-invalid block).

    Returns:
        Structured report with `valid`, `errors`, `warnings`,
        `synthetic_personas_present_on_non_laptop`, `unresolved_personas`.

    Per Sprint 47.6 + PSG-15 — wizard fails closed when ``fails_psg_15``
    is True.
    """
    use_case_id = use_case_data.get("use_case_id") or "<unknown>"

    # Substrate parse — default to lab when missing (the framework default).
    raw_substrate = use_case_data.get("substrate") or "lab"
    try:
        substrate = Substrate(raw_substrate)
    except ValueError:
        return PersonaBindingValidationReport(
            use_case_id=use_case_id,
            substrate=Substrate.LAB,
            personas_active=[],
            bindings_count=0,
            valid=False,
            errors=[
                f"substrate {raw_substrate!r} is not one of {list(Substrate)}; "
                "use-case YAML schema invalid"
            ],
        )

    # personas_active parse — accept the framework's mixed shape (list of
    # dicts with `id` keys, or list of strings).
    raw_active = use_case_data.get("personas_active") or []
    personas_active: list[str] = []
    for entry in raw_active:
        if isinstance(entry, dict) and "id" in entry:
            personas_active.append(str(entry["id"]))
        elif isinstance(entry, str):
            personas_active.append(entry)
        else:
            return PersonaBindingValidationReport(
                use_case_id=use_case_id,
                substrate=substrate,
                personas_active=[],
                bindings_count=0,
                valid=False,
                errors=[
                    f"personas_active contains an unexpected entry shape: {entry!r}"
                ],
            )

    # Bindings parse — accept passed-in or read from YAML.
    if bindings is None:
        raw_bindings = use_case_data.get("persona_principal_bindings") or {}
        # Map nested format → typed model. Each value should be a dict
        # parseable as PersonaPrincipalBinding (with persona_id key).
        try:
            parsed: dict[str, PersonaPrincipalBinding] = {}
            for persona_id, binding_dict in raw_bindings.items():
                # Inject the persona_id when missing (matches the YAML
                # convention where the key is the id).
                if "persona_id" not in binding_dict:
                    binding_dict = {"persona_id": persona_id, **binding_dict}
                parsed[persona_id] = PersonaPrincipalBinding(**binding_dict)
            bindings = UseCasePersonaBindings(bindings=parsed)
        except (ValueError, TypeError) as exc:
            return PersonaBindingValidationReport(
                use_case_id=use_case_id,
                substrate=substrate,
                personas_active=personas_active,
                bindings_count=len(raw_bindings),
                valid=False,
                errors=[
                    f"persona_principal_bindings YAML did not parse against the schema: {exc}"
                ],
            )

    report = PersonaBindingValidationReport(
        use_case_id=use_case_id,
        substrate=substrate,
        personas_active=personas_active,
        bindings_count=len(bindings.bindings),
        valid=True,
    )

    # Check 1: every active persona has a binding (substrate-dependent).
    unresolved = bindings.unresolved_personas(personas_active)
    report.unresolved_personas = unresolved
    if unresolved:
        msg = (
            f"{len(unresolved)} persona(s) in personas_active have no binding "
            f"in persona_principal_bindings: {unresolved}"
        )
        if substrate in (Substrate.DEV, Substrate.STAGE, Substrate.PROD):
            report.errors.append(msg)
            report.valid = False
        elif substrate == Substrate.LAB:
            report.warnings.append(msg)
        # laptop: synthetic personas allowed; no warning needed.

    # Check 2: synthetic personas on non-laptop substrate.
    synthetic_present = [
        p for p in personas_active if p in SYNTHETIC_LAB_PERSONAS
    ]
    report.synthetic_personas_present_on_non_laptop = (
        synthetic_present if substrate != Substrate.LAPTOP else []
    )
    if synthetic_present and substrate != Substrate.LAPTOP:
        # Only an error when synthetic + unbound. If the operator
        # explicitly bound the synthetic persona to real principals,
        # that's a deliberate Lab-personas-on-real-tenant choice.
        unbound_synthetic = [p for p in synthetic_present if p in unresolved]
        if unbound_synthetic and substrate in (Substrate.DEV, Substrate.STAGE, Substrate.PROD):
            report.errors.append(
                f"Synthetic Lab personas {unbound_synthetic} appear in "
                f"personas_active on substrate={substrate.value} without "
                "persona_principal_bindings entries. The wizard fails closed "
                "(PSG-15) — clone _default to <client>/ and bind these to "
                "the client's Entra group / static UPN list / shift roster."
            )
            report.valid = False

    return report


def quick_check_psg_15(use_case_data: dict[str, Any]) -> bool:
    """One-line answer for the wizard's pre-deployment gate.

    Returns ``True`` when the use-case PASSES PSG-15 (deploy may proceed),
    ``False`` when it FAILS (deploy must be blocked).

    Equivalent to ``not validate_use_case_personas(...).fails_psg_15``.
    """
    report = validate_use_case_personas(use_case_data)
    return not report.fails_psg_15
