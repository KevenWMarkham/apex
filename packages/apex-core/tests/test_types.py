"""Tests for ``apex_core.types``."""

from __future__ import annotations

from apex_core.types import BumpClass, Classification, GateKind, GateVariant, Practice


def test_classifications_are_lowercase() -> None:
    assert Classification.PII.value == "pii"
    assert Classification.TRADE_SECRET.value == "trade_secret"


def test_bump_classes_uppercase() -> None:
    assert BumpClass.PATCH.value == "PATCH"
    assert BumpClass.MINOR.value == "MINOR"
    assert BumpClass.MAJOR.value == "MAJOR"


def test_four_gate_kinds() -> None:
    assert {g.value for g in GateKind} == {"ZERO_TOUCH", "ACK_ONLY", "HITL", "ESCALATION"}


def test_four_gate_variants() -> None:
    assert {v.value for v in GateVariant} == {"hard", "soft", "policy", "escalation"}


def test_seven_practices() -> None:
    assert {p.value for p in Practice} == {"rc", "hls", "er", "axle", "tmt", "th", "ice"}
