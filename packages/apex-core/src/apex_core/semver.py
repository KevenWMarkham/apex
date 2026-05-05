"""Semantic-version parsing and bump classification.

Ports ``apex-core/tools/classify-bump.js`` to Python with the same semantics.
Version-string math only — content-diff classification (which SemVer *should*
the change be?) lives in the ``validators`` package in later sprints.

See ``docs/APEX - Design and Build/APEX_Design.md`` §3.3.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Self

from apex_core.types import BumpClass

_SEMVER_PATTERN = re.compile(
    r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)"
    r"(?:-(?P<prerelease>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?"
    r"(?:\+(?P<build>[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?$"
)


@dataclass(frozen=True, slots=True, order=True)
class SemVer:
    """Parsed semantic version (major.minor.patch with optional pre-release/build).

    ``order=True`` gives lexicographic comparison on the field tuple, which
    matches SemVer precedence for the numeric components. Pre-release ordering
    follows SemVer 2.0.0 rules only to first-approximation (pre-release present
    is "less than" pre-release absent); full pre-release comparison is not
    needed at the L1 contract level.
    """

    major: int
    minor: int
    patch: int
    prerelease: str | None = None
    build: str | None = None

    @classmethod
    def parse(cls, value: str) -> Self:
        """Parse a SemVer 2.0.0-ish string.

        Raises:
            ValueError: If ``value`` is not a valid SemVer string.
        """
        match = _SEMVER_PATTERN.match(value)
        if match is None:
            raise ValueError(f"Invalid SemVer: {value!r}")
        return cls(
            major=int(match["major"]),
            minor=int(match["minor"]),
            patch=int(match["patch"]),
            prerelease=match["prerelease"],
            build=match["build"],
        )

    def __str__(self) -> str:
        result = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            result += f"-{self.prerelease}"
        if self.build:
            result += f"+{self.build}"
        return result


def classify_bump(previous: SemVer, current: SemVer) -> BumpClass:
    """Classify the version-number bump from ``previous`` to ``current``.

    Args:
        previous: The baseline version.
        current: The new version (must be strictly forward of ``previous``).

    Returns:
        ``BumpClass.MAJOR`` if the major component changed,
        ``BumpClass.MINOR`` if the minor component changed,
        ``BumpClass.PATCH`` if only the patch component changed.

    Raises:
        ValueError: If ``current`` is not strictly forward of ``previous``
            (e.g. equal, or lower on any component).
    """
    if current == previous:
        raise ValueError(f"No version change: {previous} == {current}")

    if current.major != previous.major:
        if current.major < previous.major:
            raise ValueError(f"Major regression: {previous} -> {current}")
        return BumpClass.MAJOR

    if current.minor != previous.minor:
        if current.minor < previous.minor:
            raise ValueError(f"Minor regression: {previous} -> {current}")
        return BumpClass.MINOR

    if current.patch != previous.patch:
        if current.patch < previous.patch:
            raise ValueError(f"Patch regression: {previous} -> {current}")
        return BumpClass.PATCH

    # major/minor/patch all equal but self != previous implies prerelease/build diff.
    raise ValueError(
        f"Pre-release / build-metadata differences are not a classifiable bump: "
        f"{previous} -> {current}"
    )
