"""Tests for fda-mcp tools."""

from __future__ import annotations

import pytest

from fda_mcp import (
    CONTRACTS,
    InMemoryFdaBackend,
    get_recall_detail,
    list_recalls_by_date,
    search_adverse_events,
    set_fda_backend,
)
from mcp_common import McpError, McpErrorCode


@pytest.fixture(autouse=True)
def _seed() -> None:
    set_fda_backend(InMemoryFdaBackend(
        recalls=[
            {"recall_id": "F-2026-001", "event_date": "2026-04-01", "product": "Romaine lettuce",
             "reason": "Listeria monocytogenes", "status": "Ongoing"},
            {"recall_id": "F-2026-002", "event_date": "2026-04-15", "product": "Frozen spinach",
             "reason": "Undeclared allergen", "status": "Completed"},
            {"recall_id": "F-2025-099", "event_date": "2025-12-10", "product": "Beef tenderloin",
             "reason": "E. coli O157:H7", "status": "Completed"},
        ],
        adverse_events=[
            {"event_id": "AE-1", "product": "Acetaminophen 500mg", "reaction": "Hepatotoxicity"},
            {"event_id": "AE-2", "product": "Acetaminophen 325mg", "reaction": "Rash"},
            {"event_id": "AE-3", "product": "Ibuprofen 200mg", "reaction": "GI bleed"},
        ],
    ))


def test_list_recalls_since() -> None:
    rows = list_recalls_by_date("2026-01-01")
    assert len(rows) == 2


def test_list_recalls_respects_limit() -> None:
    rows = list_recalls_by_date("2020-01-01", limit=2)
    assert len(rows) == 2


def test_list_recalls_bad_date() -> None:
    with pytest.raises(McpError) as exc:
        list_recalls_by_date("not-a-date")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_get_recall_detail() -> None:
    row = get_recall_detail("F-2026-001")
    assert row["product"] == "Romaine lettuce"


def test_get_recall_missing() -> None:
    with pytest.raises(McpError) as exc:
        get_recall_detail("nope")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_search_adverse_events_substring() -> None:
    rows = search_adverse_events("Acetaminophen")
    assert len(rows) == 2


def test_search_case_insensitive() -> None:
    rows = search_adverse_events("ibuprofen")  # lowercase
    assert len(rows) == 1


def test_contracts() -> None:
    assert len(CONTRACTS) == 3
