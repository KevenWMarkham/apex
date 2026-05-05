"""Tests for ferc-mcp tools."""

from __future__ import annotations

import pytest

from ferc_mcp import (
    CONTRACTS,
    InMemoryFercBackend,
    get_interconnection_queue_status,
    list_compliance_filings,
    list_enforcement_actions,
    set_ferc_backend,
)
from mcp_common import McpError, McpErrorCode


@pytest.fixture(autouse=True)
def _seed() -> None:
    set_ferc_backend(InMemoryFercBackend(
        enforcement=[
            {"docket": "IN-25-1", "date": "2025-09-15", "party": "Acme Utility"},
            {"docket": "IN-26-3", "date": "2026-02-01", "party": "Beta Power"},
        ],
        interconnection={
            "Q-1001": {"queue_id": "Q-1001", "capacity_mw": 150, "status": "study"},
        },
        filings=[
            {"filer": "utility-A", "filed_date": "2026-03-01", "doc_id": "F-1"},
            {"filer": "utility-A", "filed_date": "2026-01-15", "doc_id": "F-2"},
            {"filer": "utility-B", "filed_date": "2026-03-15", "doc_id": "F-3"},
        ],
    ))


def test_list_enforcement() -> None:
    rows = list_enforcement_actions("2026-01-01")
    assert len(rows) == 1
    assert rows[0]["docket"] == "IN-26-3"


def test_list_enforcement_bad_date() -> None:
    with pytest.raises(McpError) as exc:
        list_enforcement_actions("bad-date")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_get_interconnection() -> None:
    row = get_interconnection_queue_status("Q-1001")
    assert row["capacity_mw"] == 150


def test_get_interconnection_missing() -> None:
    with pytest.raises(McpError) as exc:
        get_interconnection_queue_status("Q-NONE")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_list_filings_by_filer() -> None:
    rows = list_compliance_filings("utility-A", "2026-02-01")
    assert len(rows) == 1
    assert rows[0]["doc_id"] == "F-1"


def test_contracts() -> None:
    assert len(CONTRACTS) == 3
