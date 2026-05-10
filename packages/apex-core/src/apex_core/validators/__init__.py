"""Validators for APEX manifests.

Ports ``apex-core/tools/validate-*.js`` to Python. Public surface:

- :func:`validate_manifest` — one YAML file → ValidationReport
- :func:`validate_practice` — a directory of L3 Practice manifests
- :func:`validate_fleet` — a set of L4 tenant manifests for consistency
- :func:`validate_use_case_personas` — Sprint 47.6 / PSG-15 — verifies
  every active persona has a resolvable binding before prod deploy
"""

from apex_core.validators.fleet import FleetReport, validate_fleet
from apex_core.validators.manifest import ValidationReport, validate_manifest
from apex_core.validators.practice import PracticeReport, validate_practice
from apex_core.validators.use_case_personas import (
    PersonaBindingValidationReport,
    Substrate,
    SYNTHETIC_LAB_PERSONAS,
    quick_check_psg_15,
    validate_use_case_personas,
)

__all__ = [
    "FleetReport",
    "PracticeReport",
    "PersonaBindingValidationReport",
    "SYNTHETIC_LAB_PERSONAS",
    "Substrate",
    "ValidationReport",
    "quick_check_psg_15",
    "validate_fleet",
    "validate_manifest",
    "validate_practice",
    "validate_use_case_personas",
]
