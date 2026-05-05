"""edi-mcp tool implementations — minimal X12 segment parsing."""

from __future__ import annotations

from apex_core.types import Classification
from mcp_common import McpError, McpErrorCode, ToolContract, traced_call

SERVER_NAME = "edi-mcp"
TOOL_VERSION = "1.0.0"


def _parse_segments(payload: str, sep: str = "~") -> list[list[str]]:
    """Split X12 payload into (segment-name, elements) pairs."""
    segs: list[list[str]] = []
    for raw in payload.split(sep):
        s = raw.strip()
        if not s:
            continue
        segs.append(s.split("*"))
    return segs


def parse_850(
    payload: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict:
    """Parse an X12 850 Purchase Order — extracts BEG + PO1 line items."""
    if "BEG" not in payload:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="850 must contain a BEG (Beginning) segment",
        )
    with traced_call(
        tool_name=f"{SERVER_NAME}.parse_850",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"payload_length": len(payload)},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        segs = _parse_segments(payload)
        po_number: str | None = None
        order_date: str | None = None
        lines: list[dict] = []
        for seg in segs:
            if seg[0] == "BEG" and len(seg) >= 5:
                po_number = seg[3]
                order_date = seg[4]
            elif seg[0] == "PO1" and len(seg) >= 5:
                lines.append({
                    "line_no": seg[1] if len(seg) > 1 else "",
                    "quantity": seg[2] if len(seg) > 2 else "",
                    "uom": seg[3] if len(seg) > 3 else "",
                    "unit_price": seg[4] if len(seg) > 4 else "",
                })
        result = {"po_number": po_number, "order_date": order_date, "lines": lines}
        ctx["result"] = result
        return result


def parse_856(
    payload: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict:
    """Parse an X12 856 Advance Ship Notice — extracts BSN + HL hierarchy roots."""
    if "BSN" not in payload:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message="856 must contain a BSN (Beginning Segment) segment",
        )
    with traced_call(
        tool_name=f"{SERVER_NAME}.parse_856",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"payload_length": len(payload)},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        segs = _parse_segments(payload)
        asn_no: str | None = None
        shipment_date: str | None = None
        hl_count = 0
        for seg in segs:
            if seg[0] == "BSN" and len(seg) >= 4:
                asn_no = seg[2]
                shipment_date = seg[3]
            elif seg[0] == "HL":
                hl_count += 1
        result = {"asn_number": asn_no, "shipment_date": shipment_date, "hl_segment_count": hl_count}
        ctx["result"] = result
        return result


def emit_810(
    invoice: dict,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> str:
    """Emit a minimal X12 810 Invoice from a dict payload."""
    required = {"invoice_number", "invoice_date", "total_amount"}
    missing = required - invoice.keys()
    if missing:
        raise McpError(
            code=McpErrorCode.INVALID_INPUT,
            message=f"Missing invoice fields: {sorted(missing)}",
        )
    with traced_call(
        tool_name=f"{SERVER_NAME}.emit_810",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"invoice_number": invoice["invoice_number"]},
        classification_applied=[Classification.INTERNAL],
    ) as ctx:
        date_fmt = invoice["invoice_date"].replace("-", "")
        lines = [
            f"BIG*{date_fmt}*{invoice['invoice_number']}*********",
            f"TDS*{int(float(invoice['total_amount']) * 100)}",
            "SE*2*0001",
        ]
        payload = "~".join(lines) + "~"
        ctx["result"] = payload
        return payload


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.parse_850", version=TOOL_VERSION,
        description="Parse X12 850 Purchase Order — extract PO number, date, line items.",
        classification_propagation=[Classification.INTERNAL],
    ),
    ToolContract(
        name=f"{SERVER_NAME}.parse_856", version=TOOL_VERSION,
        description="Parse X12 856 Advance Ship Notice — extract ASN + HL counts.",
        classification_propagation=[Classification.INTERNAL],
    ),
    ToolContract(
        name=f"{SERVER_NAME}.emit_810", version=TOOL_VERSION,
        description="Emit a minimal X12 810 Invoice payload from a dict.",
        classification_propagation=[Classification.INTERNAL],
    ),
]
