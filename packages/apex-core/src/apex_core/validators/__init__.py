"""Validators for APEX manifests.

Ports ``apex-core/tools/validate-*.js`` to Python. Public surface:

- :func:`validate_manifest` — one YAML file → ValidationReport
- :func:`validate_practice` — a directory of L3 Practice manifests
- :func:`validate_fleet` — a set of L4 tenant manifests for consistency
"""

from apex_core.validators.fleet import FleetReport, validate_fleet
from apex_core.validators.manifest import ValidationReport, validate_manifest
from apex_core.validators.practice import PracticeReport, validate_practice

__all__ = [
    "FleetReport",
    "PracticeReport",
    "ValidationReport",
    "validate_fleet",
    "validate_manifest",
    "validate_practice",
]
