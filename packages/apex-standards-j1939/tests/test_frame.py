"""Tests for the CAN frame shape."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from apex_standards_j1939 import CanFrame


def test_minimal_frame() -> None:
    frame = CanFrame(pgn=61444, source_address=0, data=b"\x00\x00\x00\x00\x00\x00\x00\x00")
    assert frame.pgn == 61444
    assert len(frame.data) == 8


def test_priority_default_6() -> None:
    f = CanFrame(pgn=61444, source_address=10, data=b"")
    assert f.priority == 6


def test_can_id_assembly() -> None:
    f = CanFrame(pgn=0xF004, source_address=0x00, priority=3, data=b"")
    # (priority << 26) | (pgn << 8) | source_address
    expected = (3 << 26) | (0xF004 << 8) | 0x00
    assert f.can_id == expected


def test_reject_oversized_payload() -> None:
    with pytest.raises(ValidationError):
        CanFrame(pgn=61444, source_address=0, data=b"\x00" * 9)


def test_reject_bad_priority() -> None:
    with pytest.raises(ValidationError):
        CanFrame(pgn=61444, source_address=0, priority=10, data=b"")


def test_timestamp_optional() -> None:
    f = CanFrame(pgn=61444, source_address=0, data=b"", timestamp=datetime.now(UTC))
    assert f.timestamp is not None
