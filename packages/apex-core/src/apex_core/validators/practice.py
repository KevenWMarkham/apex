"""Practice-bundle validator — validates every manifest in a Practice directory.

A Practice directory is laid out as::

    packages/apex-practices/apex-<practice>/
        data/
            schemas/*.yaml
            events/*.yaml
            orchestrations/*.yaml
            agents/*.yaml
            policies/*.yaml
            services/*.yaml
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from apex_core.validators.manifest import ValidationReport, validate_manifest


@dataclass(frozen=True, slots=True)
class PracticeReport:
    """Structured result of a Practice-bundle validation."""

    root: Path
    reports: list[ValidationReport] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return all(r.valid for r in self.reports)

    @property
    def failures(self) -> list[ValidationReport]:
        return [r for r in self.reports if not r.valid]

    def summary(self) -> str:
        total = len(self.reports)
        failed = len(self.failures)
        status = "OK" if self.valid else "FAIL"
        return f"[{status}] {self.root} — {total - failed}/{total} manifests valid"


def validate_practice(root: Path) -> PracticeReport:
    """Validate every ``*.yaml`` / ``*.yml`` manifest under a Practice root.

    Args:
        root: Path to the Practice directory (e.g. ``packages/apex-practices/apex-rc``).

    Returns:
        A :class:`PracticeReport` whose ``reports`` list contains one entry
        per discovered YAML file, in sorted path order.
    """
    reports: list[ValidationReport] = []
    for path in sorted({*root.rglob("*.yaml"), *root.rglob("*.yml")}):
        reports.append(validate_manifest(path))
    return PracticeReport(root=root, reports=reports)
