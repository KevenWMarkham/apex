"""Tests for apex_translators — Sprint 23 round-trip + structural conformance.

Coverage:

- EDI X12 (Task 23.1) — round-trip parse → emit → parse for all 8 fixtures
- HL7 v2 (Task 23.2) — round-trip + MLLP framing helpers
- HL7 CDA (Task 23.3) — one-way structural extraction (CCD with all 4 sections)
- EPCIS 2.0 (Task 23.4) — JSON + XML parse, JSON round-trip
- OAGIS BOD (Task 23.5) — round-trip across 3 verb/noun combos
- IATA PADIS (Task 23.6) — one-way structural extraction (PNL, ADL, PRL)
"""

from __future__ import annotations

import json

import pytest

from apex_translators import (
    EmitError,
    ParseError,
    ParsedMessage,
    emit_epcis_json,
    emit_hl7v2,
    emit_oagis,
    emit_x12,
    parse_cda,
    parse_epcis,
    parse_hl7v2,
    parse_oagis,
    parse_padis,
    parse_x12,
    strip_mllp,
    wrap_mllp,
)
from apex_translators.fixtures import (
    CDA_FIXTURES,
    EDI_X12_FIXTURES,
    EPCIS_FIXTURES,
    HL7V2_FIXTURES,
    OAGIS_FIXTURES,
    PADIS_FIXTURES,
)
from apex_translators.edi_x12.parser import iter_transaction_sets


# ---------------------------------------------------------------------------
# EDI X12 — Task 23.1
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("tx_id", sorted(EDI_X12_FIXTURES))
def test_edi_x12_parses_envelope(tx_id: str) -> None:
    fixture = EDI_X12_FIXTURES[tx_id]
    msg = parse_x12(fixture)
    assert msg.format == "edi-x12"
    assert msg.first("ISA") is not None
    assert msg.first("GS") is not None
    assert msg.first("ST") is not None
    assert msg.first("SE") is not None
    assert msg.first("GE") is not None
    assert msg.first("IEA") is not None


@pytest.mark.parametrize("tx_id", sorted(EDI_X12_FIXTURES))
def test_edi_x12_message_type_extracted(tx_id: str) -> None:
    msg = parse_x12(EDI_X12_FIXTURES[tx_id])
    assert msg.message_type == tx_id


@pytest.mark.parametrize("tx_id", sorted(EDI_X12_FIXTURES))
def test_edi_x12_round_trip(tx_id: str) -> None:
    fixture = EDI_X12_FIXTURES[tx_id]
    msg = parse_x12(fixture)
    rendered = emit_x12(msg)
    msg2 = parse_x12(rendered)
    # Same number of segments + same segment ordering
    assert len(msg.segments) == len(msg2.segments)
    for s1, s2 in zip(msg.segments, msg2.segments, strict=True):
        assert s1.name == s2.name
        assert s1.elements == s2.elements


def test_edi_x12_parse_envelope_metadata() -> None:
    msg = parse_x12(EDI_X12_FIXTURES["850"])
    assert msg.sender == "SENDERID01"
    assert msg.receiver == "RECEIVERID01"
    assert msg.control_number == "000000001"
    assert msg.version == "00501"
    assert msg.sent_at is not None


def test_edi_x12_iter_transaction_sets() -> None:
    msg = parse_x12(EDI_X12_FIXTURES["850"])
    sets = list(iter_transaction_sets(msg))
    assert len(sets) == 1
    assert sets[0][0].name == "ST"
    assert sets[0][-1].name == "SE"


def test_edi_x12_rejects_non_isa() -> None:
    with pytest.raises(ParseError, match="ISA"):
        parse_x12("GS*PO*A*B*20250101*1200*1*X*005010~")


def test_edi_x12_rejects_empty() -> None:
    with pytest.raises(ParseError):
        parse_x12("")


def test_edi_x12_emit_rejects_empty_message() -> None:
    msg = ParsedMessage(format="edi-x12")
    with pytest.raises(EmitError):
        emit_x12(msg)


# ---------------------------------------------------------------------------
# HL7 v2 — Task 23.2
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("msg_type", sorted(HL7V2_FIXTURES))
def test_hl7v2_parses_msh(msg_type: str) -> None:
    msg = parse_hl7v2(HL7V2_FIXTURES[msg_type])
    assert msg.format == "hl7v2"
    assert msg.first("MSH") is not None


@pytest.mark.parametrize("msg_type", sorted(HL7V2_FIXTURES))
def test_hl7v2_round_trip(msg_type: str) -> None:
    fixture = HL7V2_FIXTURES[msg_type]
    msg = parse_hl7v2(fixture)
    rendered = emit_hl7v2(msg)
    msg2 = parse_hl7v2(rendered)
    assert len(msg.segments) == len(msg2.segments)
    for s1, s2 in zip(msg.segments, msg2.segments, strict=True):
        assert s1.name == s2.name
        # MSH special-case: element[0] is the field separator itself
        if s1.name == "MSH":
            # Allow re-rendering to drop or keep the leading sep marker
            assert s1.elements[1:] == s2.elements[1:] or s1.elements == s2.elements
        else:
            assert s1.elements == s2.elements


def test_hl7v2_extracts_envelope_metadata() -> None:
    msg = parse_hl7v2(HL7V2_FIXTURES["ADT^A04"])
    assert msg.sender == "REGISTRATION"
    assert msg.receiver == "EHR"
    assert msg.control_number == "MSG00001"
    assert msg.version == "2.5.1"
    assert msg.sent_at is not None


def test_hl7v2_pid_segment_present() -> None:
    msg = parse_hl7v2(HL7V2_FIXTURES["ADT^A04"])
    pid = msg.first("PID")
    assert pid is not None
    assert pid.elements[0] == "1"  # PID-1 set ID


def test_hl7v2_rejects_non_msh_start() -> None:
    with pytest.raises(ParseError, match="MSH"):
        parse_hl7v2("PID|1||PATID")


def test_mllp_round_trip() -> None:
    payload = HL7V2_FIXTURES["ADT^A04"]
    framed = wrap_mllp(payload)
    assert framed.startswith(b"\x0b")
    assert framed.endswith(b"\x1c\r")
    unwrapped = strip_mllp(framed)
    assert unwrapped == payload


def test_mllp_strip_handles_unframed_string() -> None:
    """strip_mllp is a no-op when no framing bytes present."""
    plain = "MSH|^~\\&|"
    assert strip_mllp(plain) == plain


# ---------------------------------------------------------------------------
# HL7 CDA — Task 23.3
# ---------------------------------------------------------------------------


def test_cda_parses_ccd() -> None:
    msg = parse_cda(CDA_FIXTURES["CCD"])
    assert msg.format == "cda"


def test_cda_extracts_patient_demographics() -> None:
    msg = parse_cda(CDA_FIXTURES["CCD"])
    pat = msg.metadata.get("patient", {})
    assert pat.get("given") == "John"
    assert pat.get("family") == "Doe"
    assert pat.get("gender") == "M"


def test_cda_extracts_all_named_sections() -> None:
    msg = parse_cda(CDA_FIXTURES["CCD"])
    section_names = {s.name for s in msg.segments}
    assert "Allergies" in section_names
    assert "Medications" in section_names
    assert "Problems" in section_names
    assert "Results" in section_names


def test_cda_extracts_section_entries() -> None:
    msg = parse_cda(CDA_FIXTURES["CCD"])
    allergies = msg.first("Allergies")
    assert allergies is not None
    entries = allergies.data.get("entries", [])
    assert any("Penicillin" in str(e.get("value", "")) for e in entries)


def test_cda_rejects_non_clinical_document() -> None:
    bad = '<?xml version="1.0"?><Random xmlns="urn:hl7-org:v3"/>'
    with pytest.raises(ParseError, match="ClinicalDocument"):
        parse_cda(bad)


def test_cda_rejects_malformed_xml() -> None:
    with pytest.raises(ParseError, match="parse error"):
        parse_cda("<<not xml>>")


# ---------------------------------------------------------------------------
# EPCIS 2.0 — Task 23.4
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("event_type", ["ObjectEvent", "AggregationEvent", "TransactionEvent"])
def test_epcis_json_parses(event_type: str) -> None:
    msg = parse_epcis(EPCIS_FIXTURES[event_type])
    assert msg.format == "epcis"
    assert msg.version == "2.0"
    assert msg.first(event_type) is not None


def test_epcis_xml_parses() -> None:
    msg = parse_epcis(EPCIS_FIXTURES["XML-ObjectEvent"])
    assert msg.format == "epcis"
    assert msg.first("ObjectEvent") is not None


def test_epcis_object_event_carries_epc_list() -> None:
    msg = parse_epcis(EPCIS_FIXTURES["ObjectEvent"])
    obj = msg.first("ObjectEvent")
    assert obj is not None
    epcs = obj.data.get("epcList", [])
    assert any("urn:epc:id:sgtin" in epc for epc in epcs)


def test_epcis_aggregation_carries_parent_and_children() -> None:
    msg = parse_epcis(EPCIS_FIXTURES["AggregationEvent"])
    agg = msg.first("AggregationEvent")
    assert agg is not None
    assert "urn:epc:id:sscc" in agg.data.get("parentID", "")
    assert len(agg.data.get("childEPCs", [])) == 2


@pytest.mark.parametrize("event_type", ["ObjectEvent", "AggregationEvent", "TransactionEvent"])
def test_epcis_json_round_trip(event_type: str) -> None:
    msg = parse_epcis(EPCIS_FIXTURES[event_type])
    rendered = emit_epcis_json(msg, indent=2)
    # Re-parse and assert the event survives round-trip
    msg2 = parse_epcis(rendered)
    assert msg2.first(event_type) is not None
    # Confirm the rendered output is valid JSON
    json.loads(rendered)


def test_epcis_rejects_empty() -> None:
    with pytest.raises(ParseError):
        parse_epcis("")


def test_epcis_rejects_non_json_non_xml() -> None:
    with pytest.raises(ParseError, match="must be"):
        parse_epcis("plain text")


# ---------------------------------------------------------------------------
# OAGIS BOD — Task 23.5
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("bod", ["ProcessItem", "SyncCarrier", "GetManufacturingFacility"])
def test_oagis_parses_bod(bod: str) -> None:
    msg = parse_oagis(OAGIS_FIXTURES[bod])
    assert msg.format == "oagis"
    assert msg.message_type == bod


@pytest.mark.parametrize("bod,expected_verb,expected_noun", [
    ("ProcessItem", "Process", "Item"),
    ("SyncCarrier", "Sync", "Carrier"),
    ("GetManufacturingFacility", "Get", "ManufacturingFacility"),
])
def test_oagis_decomposes_verb_and_noun(bod: str, expected_verb: str, expected_noun: str) -> None:
    msg = parse_oagis(OAGIS_FIXTURES[bod])
    assert msg.metadata["verb"] == expected_verb
    assert msg.metadata["noun"] == expected_noun


def test_oagis_extracts_application_area() -> None:
    msg = parse_oagis(OAGIS_FIXTURES["ProcessItem"])
    assert msg.sender == "SAP-S4HANA-PROD"
    assert msg.control_number == "BOD-PROC-12345"


@pytest.mark.parametrize("bod", ["ProcessItem", "SyncCarrier", "GetManufacturingFacility"])
def test_oagis_round_trip_preserves_message_type(bod: str) -> None:
    msg = parse_oagis(OAGIS_FIXTURES[bod])
    rendered = emit_oagis(msg)
    msg2 = parse_oagis(rendered)
    assert msg2.message_type == bod
    assert msg2.metadata["verb"] == msg.metadata["verb"]


def test_oagis_rejects_non_oagis_root() -> None:
    bad = '<?xml version="1.0"?><RandomThing><DataArea><Foo/></DataArea></RandomThing>'
    with pytest.raises(ParseError, match="verb"):
        parse_oagis(bad)


# ---------------------------------------------------------------------------
# IATA PADIS — Task 23.6
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("msg_type", sorted(PADIS_FIXTURES))
def test_padis_parses_header(msg_type: str) -> None:
    msg = parse_padis(PADIS_FIXTURES[msg_type])
    assert msg.format == "padis"
    assert msg.message_type == msg_type


def test_padis_extracts_flight_key() -> None:
    msg = parse_padis(PADIS_FIXTURES["PNL"])
    flight = msg.metadata.get("flight", {})
    assert flight.get("carrier") == "DL"
    assert flight.get("flight_number") == "0123"
    assert flight.get("origin") == "JFK"
    assert flight.get("destination") == "LHR"


def test_padis_extracts_pax_records() -> None:
    msg = parse_padis(PADIS_FIXTURES["PNL"])
    pax = msg.find("PAX")
    assert len(pax) >= 2
    surnames = {p.data["surname"] for p in pax}
    assert "HOLLAND" in surnames


def test_padis_attaches_continuation_to_preceding_pax() -> None:
    msg = parse_padis(PADIS_FIXTURES["PNL"])
    holland = next(p for p in msg.find("PAX") if p.data["surname"] == "HOLLAND")
    cont = holland.data.get("continuations", [])
    assert any("SSR DOCS" in line for line in cont)


def test_padis_rejects_unknown_message_type() -> None:
    with pytest.raises(ParseError, match="not in supported"):
        parse_padis("XYZ\nSomeBody")


def test_padis_rejects_empty() -> None:
    with pytest.raises(ParseError):
        parse_padis("")


# ---------------------------------------------------------------------------
# Conformance markers — Sprint 23 exit criteria
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_edi_x12_eight_named_transactions() -> None:
    """Sprint 23 §23.1.1 + §23.1.2 — RC + HLS named transactions all parse."""
    expected = {"850", "856", "810", "820", "837", "835", "270", "271"}
    assert expected.issubset(EDI_X12_FIXTURES.keys())
    for tx in expected:
        msg = parse_x12(EDI_X12_FIXTURES[tx])
        assert msg.message_type == tx


@pytest.mark.conformance
def test_conformance_hl7v2_named_segments_present() -> None:
    """Sprint 23 §23.2.2 — supported segment library covered by fixtures."""
    seen: set[str] = set()
    for fixture in HL7V2_FIXTURES.values():
        msg = parse_hl7v2(fixture)
        for seg in msg.segments:
            seen.add(seg.name)
    expected = {"MSH", "PID", "PV1", "OBR", "OBX", "ORC", "RXE", "AL1"}
    assert expected.issubset(seen), f"Missing: {expected - seen}"


@pytest.mark.conformance
def test_conformance_cda_four_named_sections() -> None:
    """Sprint 23 §23.3.2 — Allergies, Medications, Problems, Results extracted."""
    msg = parse_cda(CDA_FIXTURES["CCD"])
    section_names = {s.name for s in msg.segments}
    assert {"Allergies", "Medications", "Problems", "Results"}.issubset(section_names)


@pytest.mark.conformance
def test_conformance_epcis_four_event_types_supported() -> None:
    """Sprint 23 §23.4.1 — Object/Aggregation/Transaction/Transformation."""
    from apex_translators.epcis.parser import EPCIS_EVENT_TYPES
    expected = {"ObjectEvent", "AggregationEvent", "TransactionEvent", "TransformationEvent"}
    assert expected.issubset(set(EPCIS_EVENT_TYPES))


@pytest.mark.conformance
def test_conformance_oagis_three_nouns_covered() -> None:
    """Sprint 23 §23.5.2 — Item, Carrier, ManufacturingFacility."""
    nouns = {parse_oagis(f).metadata["noun"] for f in OAGIS_FIXTURES.values()}
    assert {"Item", "Carrier", "ManufacturingFacility"}.issubset(nouns)


@pytest.mark.conformance
def test_conformance_padis_three_message_types() -> None:
    """Sprint 23 §23.6.1 — PNL, ADL, PRL covered."""
    types = {parse_padis(f).message_type for f in PADIS_FIXTURES.values()}
    assert {"PNL", "ADL", "PRL"}.issubset(types)
