"""Tests for pharma-recall-mcp tools."""

from __future__ import annotations

import pytest

from mcp_common import McpError, McpErrorCode
from pharma_recall_mcp import (
    CONTRACTS,
    InMemoryPharmaRecallBackend,
    get_recall_detail,
    list_pharma_recalls,
    search_recalls_by_ndc,
    set_pharma_backend,
)


@pytest.fixture(autouse=True)
def _seed() -> None:
    set_pharma_backend(InMemoryPharmaRecallBackend(
        recalls=[
            {
                "recall_id": "PR-2026-01", "recall_date": "2026-03-15",
                "product": "Acetaminophen 325mg", "firm": "AcmeGen",
                "ndc_codes": ["12345-678-90", "12345-678-91"],
                "reason": "label mix-up",
            },
            {
                "recall_id": "PR-2026-02", "recall_date": "2026-04-10",
                "product": "Ibuprofen 200mg", "firm": "BetaPharma",
                "ndc_codes": ["98765-432-10"],
                "reason": "subpotent",
            },
        ],
    ))


def test_list_since() -> None:
    rows = list_pharma_recalls("2026-01-01")
    assert len(rows) == 2


def test_list_bad_date() -> None:
    with pytest.raises(McpError) as exc:
        list_pharma_recalls("nope")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_search_by_ndc_hit() -> None:
    rows = search_recalls_by_ndc("12345-678-90")
    assert len(rows) == 1
    assert rows[0]["recall_id"] == "PR-2026-01"


def test_search_by_ndc_miss() -> None:
    rows = search_recalls_by_ndc("00000-000-00")
    assert rows == []


def test_search_by_ndc_invalid_format() -> None:
    with pytest.raises(McpError) as exc:
        search_recalls_by_ndc("not-an-ndc")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_get_recall() -> None:
    row = get_recall_detail("PR-2026-01")
    assert row["firm"] == "AcmeGen"


def test_get_recall_missing() -> None:
    with pytest.raises(McpError) as exc:
        get_recall_detail("PR-nope")
    assert exc.value.code is McpErrorCode.NOT_FOUND


def test_contracts() -> None:
    assert len(CONTRACTS) == 3
