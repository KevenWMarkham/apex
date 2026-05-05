"""Tests for ``apex_core.semver``."""

from __future__ import annotations

import pytest

from apex_core.semver import SemVer, classify_bump
from apex_core.types import BumpClass


class TestSemVerParse:
    def test_plain_triplet(self) -> None:
        v = SemVer.parse("1.2.3")
        assert v.major == 1
        assert v.minor == 2
        assert v.patch == 3
        assert v.prerelease is None
        assert v.build is None

    def test_with_prerelease(self) -> None:
        v = SemVer.parse("1.0.0-alpha.1")
        assert v.prerelease == "alpha.1"

    def test_with_build(self) -> None:
        v = SemVer.parse("1.0.0+build.123")
        assert v.build == "build.123"

    def test_with_both(self) -> None:
        v = SemVer.parse("2.0.0-rc.2+20260419")
        assert v.prerelease == "rc.2"
        assert v.build == "20260419"

    def test_rejects_non_semver(self) -> None:
        with pytest.raises(ValueError):
            SemVer.parse("1.2")
        with pytest.raises(ValueError):
            SemVer.parse("v1.2.3")
        with pytest.raises(ValueError):
            SemVer.parse("not-semver")

    def test_str_round_trip(self) -> None:
        for s in ["0.1.0", "1.2.3", "1.0.0-alpha.1", "2.0.0-rc.2+20260419"]:
            assert str(SemVer.parse(s)) == s


class TestClassifyBump:
    def test_patch(self) -> None:
        assert classify_bump(SemVer.parse("1.2.3"), SemVer.parse("1.2.4")) == BumpClass.PATCH

    def test_minor(self) -> None:
        assert classify_bump(SemVer.parse("1.2.3"), SemVer.parse("1.3.0")) == BumpClass.MINOR

    def test_major(self) -> None:
        assert classify_bump(SemVer.parse("1.2.3"), SemVer.parse("2.0.0")) == BumpClass.MAJOR

    def test_same_version_errors(self) -> None:
        v = SemVer.parse("1.0.0")
        with pytest.raises(ValueError, match="No version change"):
            classify_bump(v, v)

    def test_regression_errors(self) -> None:
        with pytest.raises(ValueError, match="regression"):
            classify_bump(SemVer.parse("1.2.3"), SemVer.parse("1.2.2"))
        with pytest.raises(ValueError, match="regression"):
            classify_bump(SemVer.parse("2.0.0"), SemVer.parse("1.9.9"))

    def test_minor_beats_patch(self) -> None:
        # Even if both minor AND patch changed, the classification is MINOR.
        assert (
            classify_bump(SemVer.parse("1.2.3"), SemVer.parse("1.3.5"))
            == BumpClass.MINOR
        )
