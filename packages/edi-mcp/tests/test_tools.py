"""Tests for edi-mcp tools."""

from __future__ import annotations

import pytest

from edi_mcp import CONTRACTS, emit_810, parse_850, parse_856
from mcp_common import McpError, McpErrorCode


def test_parse_850() -> None:
    payload = (
        "ISA*00*          *00*          *ZZ*SENDERID       *ZZ*RECEIVERID     *"
        "260420*0823*U*00401*000000001*0*P*>~"
        "GS*PO*SENDERID*RECEIVERID*20260420*0823*1*X*004010~"
        "ST*850*0001~"
        "BEG*00*SA*PO-2026-042**20260420~"
        "PO1*1*10*EA*9.99***BP*SKU-001~"
        "PO1*2*5*EA*4.50***BP*SKU-002~"
        "CTT*2~"
        "SE*7*0001~"
        "GE*1*1~"
        "IEA*1*000000001~"
    )
    result = parse_850(payload)
    assert result["po_number"] == "PO-2026-042"
    assert len(result["lines"]) == 2
    assert result["lines"][0]["quantity"] == "10"


def test_parse_850_missing_beg() -> None:
    with pytest.raises(McpError) as exc:
        parse_850("ST*850*0001~SE*2*0001~")
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_parse_856() -> None:
    payload = (
        "ST*856*0001~"
        "BSN*00*ASN-42*20260420*0830~"
        "HL*1**S~"
        "HL*2*1*O~"
        "HL*3*2*P~"
        "SE*5*0001~"
    )
    result = parse_856(payload)
    assert result["asn_number"] == "ASN-42"
    assert result["hl_segment_count"] == 3


def test_parse_856_missing_bsn() -> None:
    with pytest.raises(McpError):
        parse_856("ST*856*0001~SE*2*0001~")


def test_emit_810() -> None:
    result = emit_810({
        "invoice_number": "INV-42",
        "invoice_date": "2026-04-20",
        "total_amount": "99.00",
    })
    assert "BIG*20260420*INV-42" in result
    assert "TDS*9900" in result


def test_emit_810_missing_fields() -> None:
    with pytest.raises(McpError) as exc:
        emit_810({"invoice_number": "INV-1"})
    assert exc.value.code is McpErrorCode.INVALID_INPUT


def test_contracts() -> None:
    assert len(CONTRACTS) == 3
