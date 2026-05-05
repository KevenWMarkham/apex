"""Tests for apex_protocols — Sprint 25 OT protocol adapter framework."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from apex_protocols import (
    SUPPORTED_PROTOCOLS,
    AddressNode,
    AddressSpaceError,
    AddressSpaceMapping,
    AuthMode,
    CANFrame,
    ConfigError,
    DecodedSignal,
    IEC61850StubClient,
    J1939Normalizer,
    OPCUAConfig,
    OPCUAStubClient,
    ProtocolEndpoint,
    ProtocolError,
    Sample,
    SignalThrottle,
    build_endpoint,
    decode_frame,
    parse_nodeset,
    parse_scd,
)
from apex_protocols.base import ConnectionError as ProtocolConnectionError
from apex_protocols.datasets import (
    IEC61850_SCD_XML,
    IEC61850_SNAPSHOT,
    J1939_FRAME_CAPTURE,
    OPCUA_NODESET_XML,
    OPCUA_SNAPSHOT,
)
from apex_protocols.datasets.j1939_dataset import frames_with_timestamps
from apex_protocols.j1939_transport.normalizer import SPN_LAYOUTS


# ---------------------------------------------------------------------------
# Common base
# ---------------------------------------------------------------------------


def test_supported_protocols_complete() -> None:
    assert set(SUPPORTED_PROTOCOLS) == {"opcua", "iec61850", "j1939"}


def test_sample_default_classification_empty() -> None:
    s = Sample(node_id="x", value=1)
    assert s.classification == ""
    assert s.quality == "good"


def test_address_space_mapping_annotate_propagates_classification() -> None:
    mapping = AddressSpaceMapping(protocol="opcua", name="test")
    mapping.add(AddressNode(
        node_id="ns=2;s=foo",
        canonical_entity="Foo",
        canonical_field="bar",
        classification="pii",
        units="kg",
    ))
    s = Sample(node_id="ns=2;s=foo", value=42)
    annotated = mapping.annotate(s)
    assert annotated.classification == "pii"
    assert annotated.canonical_entity == "Foo"
    assert annotated.canonical_field == "bar"
    assert annotated.units == "kg"


def test_address_space_mapping_annotate_unknown_node_marks_unknown() -> None:
    """Sprint 25 defensive — unmapped node_id gets ``unknown`` classification."""
    mapping = AddressSpaceMapping(protocol="opcua", name="test")
    s = Sample(node_id="ns=2;s=foo", value=42)
    annotated = mapping.annotate(s)
    assert annotated.classification == "unknown"


# ---------------------------------------------------------------------------
# OPC UA — Task 25.1
# ---------------------------------------------------------------------------


def test_opcua_nodeset_parses_seven_variables() -> None:
    entries = parse_nodeset(OPCUA_NODESET_XML)
    variables = [e for e in entries if e.node_class == "UAVariable"]
    assert len(variables) >= 7


def test_opcua_nodeset_extracts_browse_name_and_display_name() -> None:
    entries = parse_nodeset(OPCUA_NODESET_XML)
    vibration = next(
        e for e in entries
        if e.node_id == "ns=2;s=Line7.Press4.ServoMotor.VibrationRMS"
    )
    assert vibration.browse_name == "2:VibrationRMS"
    assert "Vibration" in vibration.display_name


def test_opcua_nodeset_extracts_parent_via_inverse_hascomponent() -> None:
    entries = parse_nodeset(OPCUA_NODESET_XML)
    press = next(e for e in entries if e.node_id == "ns=2;s=Line7.Press4")
    assert press.parent_node_id == "ns=2;s=Line7"


def test_opcua_nodeset_rejects_empty() -> None:
    with pytest.raises(AddressSpaceError):
        parse_nodeset("")


def test_opcua_nodeset_rejects_non_uanodeset_root() -> None:
    bad = '<?xml version="1.0"?><WrongRoot xmlns="http://opcfoundation.org/UA/2011/03/UANodeSet.xsd"/>'
    with pytest.raises(AddressSpaceError, match="UANodeSet"):
        parse_nodeset(bad)


def test_opcua_nodeset_rejects_malformed_xml() -> None:
    with pytest.raises(AddressSpaceError, match="parse error"):
        parse_nodeset("<<not xml>>")


def test_opcua_config_certificate_mode_requires_paths() -> None:
    with pytest.raises(ConfigError, match="cert_path"):
        OPCUAConfig(
            server_url="opc.tcp://x:4840",
            application_uri="urn:apex:test",
            auth_mode=AuthMode.CERTIFICATE,
        )


def test_opcua_config_username_mode_requires_username() -> None:
    with pytest.raises(ConfigError, match="username"):
        OPCUAConfig(
            server_url="opc.tcp://x:4840",
            application_uri="urn:apex:test",
            auth_mode=AuthMode.USERNAME_PASSWORD,
        )


def test_opcua_config_rejects_non_opc_url() -> None:
    with pytest.raises(ConfigError, match="must start with"):
        OPCUAConfig(
            server_url="http://x:4840",
            application_uri="urn:apex:test",
            auth_mode=AuthMode.ANONYMOUS,
        )


def test_opcua_config_rejects_unknown_security_policy() -> None:
    with pytest.raises(ConfigError, match="security_policy"):
        OPCUAConfig(
            server_url="opc.tcp://x:4840",
            application_uri="urn:apex:test",
            auth_mode=AuthMode.ANONYMOUS,
            security_policy="MysteryPolicy",
        )


def test_build_endpoint_carries_metadata() -> None:
    cfg = OPCUAConfig(
        server_url="opc.tcp://x:4840",
        application_uri="urn:apex:test",
        auth_mode=AuthMode.ANONYMOUS,
        namespace_uris=["http://example.com/Plant"],
    )
    ep = build_endpoint(cfg)
    assert ep.protocol == "opcua"
    assert ep.metadata["application_uri"] == "urn:apex:test"
    assert ep.metadata["namespace_uris"] == ["http://example.com/Plant"]


def test_opcua_stub_client_full_round_trip_with_mapping() -> None:
    mapping = AddressSpaceMapping(protocol="opcua", name="north-plant")
    mapping.add(AddressNode(
        node_id="ns=2;s=Line7.Press4.ServoMotor.VibrationRMS",
        canonical_entity="EquipmentHealth",
        canonical_field="vibration_rms",
        classification="operations",
        units="mm/s",
    ))
    mapping.add(AddressNode(
        node_id="ns=2;s=Line7.OperatorId",
        canonical_entity="ProductionJob",
        canonical_field="operator_id",
        classification="pii",
    ))

    cfg = OPCUAConfig(
        server_url="opc.tcp://historian:4840",
        application_uri="urn:apex:test",
        auth_mode=AuthMode.ANONYMOUS,
    )
    endpoint = build_endpoint(cfg)
    client = OPCUAStubClient(snapshot=OPCUA_SNAPSHOT)
    client.connect(endpoint)
    assert client.is_connected()

    raw_vib = client.read_one("ns=2;s=Line7.Press4.ServoMotor.VibrationRMS")
    annotated = mapping.annotate(raw_vib)
    assert annotated.value == 4.21
    assert annotated.classification == "operations"
    assert annotated.canonical_field == "vibration_rms"

    raw_op = client.read_one("ns=2;s=Line7.OperatorId")
    annotated_op = mapping.annotate(raw_op)
    assert annotated_op.classification == "pii"

    client.disconnect()
    assert not client.is_connected()


def test_opcua_stub_client_rejects_wrong_protocol() -> None:
    client = OPCUAStubClient()
    bad_endpoint = ProtocolEndpoint(protocol="iec61850", url="x")
    with pytest.raises(ProtocolConnectionError, match="opcua"):
        client.connect(bad_endpoint)


def test_opcua_stub_client_read_unknown_node_raises() -> None:
    client = OPCUAStubClient(snapshot={"a": 1})
    cfg = OPCUAConfig(
        server_url="opc.tcp://x:4840",
        application_uri="urn:apex:test",
        auth_mode=AuthMode.ANONYMOUS,
    )
    client.connect(build_endpoint(cfg))
    with pytest.raises(ProtocolConnectionError, match="not in stub snapshot"):
        client.read_one("does-not-exist")


# ---------------------------------------------------------------------------
# IEC 61850 — Task 25.2
# ---------------------------------------------------------------------------


def test_iec61850_scd_parses_one_ied() -> None:
    doc = parse_scd(IEC61850_SCD_XML)
    assert len(doc.ieds) == 1
    assert doc.ieds[0].name == "IED1"
    assert doc.ieds[0].manufacturer == "ACME Relay Co"


def test_iec61850_scd_extracts_logical_devices() -> None:
    doc = parse_scd(IEC61850_SCD_XML)
    ld_insts = {ld.inst for ld in doc.ieds[0].logical_devices}
    assert ld_insts == {"CTRL", "MEAS"}


def test_iec61850_scd_extracts_logical_nodes() -> None:
    doc = parse_scd(IEC61850_SCD_XML)
    ln_classes = {ln.ln_class for ln in doc.all_logical_nodes()}
    assert "XCBR" in ln_classes
    assert "MMXU" in ln_classes
    assert "LLN0" in ln_classes


def test_iec61850_scd_extracts_goose_metadata() -> None:
    """Sprint 25 §25.2.3 — GOOSE control blocks surface as metadata only."""
    doc = parse_scd(IEC61850_SCD_XML)
    goose = doc.all_goose_blocks()
    assert len(goose) >= 1
    assert goose[0].name == "GOOSEPos1"
    assert goose[0].app_id == "0x0001"


def test_iec61850_scd_extracts_sv_metadata() -> None:
    doc = parse_scd(IEC61850_SCD_XML)
    sv = doc.all_sv_blocks()
    assert len(sv) >= 1
    assert sv[0].smp_rate == 4800


def test_iec61850_scd_rejects_empty() -> None:
    with pytest.raises(AddressSpaceError):
        parse_scd("")


def test_iec61850_scd_rejects_non_scl_root() -> None:
    bad = '<?xml version="1.0"?><WrongRoot xmlns="http://www.iec.ch/61850/2003/SCL"/>'
    with pytest.raises(AddressSpaceError, match="SCL"):
        parse_scd(bad)


def test_iec61850_stub_client_connect_and_read() -> None:
    client = IEC61850StubClient(snapshot=IEC61850_SNAPSHOT)
    endpoint = ProtocolEndpoint(
        protocol="iec61850", url="mms://relay:102",
        auth_mode=AuthMode.ANONYMOUS,
    )
    client.connect(endpoint)
    sample = client.read_one("IED1/CTRL/XCBR1.Pos.stVal")
    assert sample.value == "closed"
    assert sample.quality == "good"


def test_iec61850_stub_client_rejects_wrong_protocol() -> None:
    client = IEC61850StubClient()
    bad = ProtocolEndpoint(protocol="opcua", url="x")
    with pytest.raises(ProtocolConnectionError, match="iec61850"):
        client.connect(bad)


def test_iec61850_subscribe_with_classification_propagation() -> None:
    """End-to-end: subscribe → annotate → critical-infrastructure stamp."""
    mapping = AddressSpaceMapping(protocol="iec61850", name="substation")
    mapping.add(AddressNode(
        node_id="IED1/CTRL/XCBR1.Pos.stVal",
        canonical_entity="BreakerStatus",
        canonical_field="position",
        classification="critical-infrastructure",
    ))
    mapping.add(AddressNode(
        node_id="IED1/MEAS/MMXU1.A.phsA.cVal.mag.f",
        canonical_entity="PhaseMeasurement",
        canonical_field="current_amps_phase_a",
        classification="critical-infrastructure",
        units="A",
    ))
    client = IEC61850StubClient(snapshot=IEC61850_SNAPSHOT)
    client.connect(ProtocolEndpoint(protocol="iec61850", url="x"))
    raws = client.subscribe([
        "IED1/CTRL/XCBR1.Pos.stVal",
        "IED1/MEAS/MMXU1.A.phsA.cVal.mag.f",
    ])
    annotated = [mapping.annotate(s) for s in raws]
    assert all(s.classification == "critical-infrastructure" for s in annotated)


# ---------------------------------------------------------------------------
# J1939 transport — Task 25.3
# ---------------------------------------------------------------------------


def test_j1939_decode_engine_hours_pgn() -> None:
    arb_id, data, ts = next(frames_with_timestamps())
    frame = CANFrame(arbitration_id=arb_id, data=data, timestamp=ts)
    signals = decode_frame(frame)
    eng_hours = next(s for s in signals if s.spn == 247)
    assert eng_hours.pgn == 65253
    assert eng_hours.value == pytest.approx(1234.5, rel=1e-3)
    assert eng_hours.units == "h"


def test_j1939_decode_engine_speed_pgn() -> None:
    """PGN 61444 SPN 190 — engine speed 1800 rpm (raw 14400 / 0.125)."""
    frames = list(frames_with_timestamps())
    arb_id, data, ts = frames[1]
    frame = CANFrame(arbitration_id=arb_id, data=data, timestamp=ts)
    signals = decode_frame(frame)
    rpm = next(s for s in signals if s.spn == 190)
    assert rpm.value == pytest.approx(1800.0)


def test_j1939_decode_drops_not_available_values() -> None:
    """Max-bit-pattern frame data must NOT emit a signal."""
    # PGN 65253 with all-FF data (engine-hours 'not available')
    frame = CANFrame(arbitration_id=0x18FEE500, data=bytes([0xFF] * 8))
    signals = decode_frame(frame)
    assert all(s.spn != 247 for s in signals)


def test_j1939_decode_short_frame_skips_oversized_spns() -> None:
    """A 4-byte data payload should still decode short SPNs, not crash."""
    # PGN 61444 SPN 190 lives at byte 3..5 — a 4-byte payload misses it
    frame = CANFrame(arbitration_id=0x0CF00400, data=bytes([0x00, 0x00, 0x00, 0x00]))
    signals = decode_frame(frame)
    assert all(s.spn != 190 for s in signals)


def test_j1939_normalizer_processes_dataset() -> None:
    norm = J1939Normalizer()
    frames = [
        CANFrame(arbitration_id=arb, data=data, timestamp=ts)
        for arb, data, ts in frames_with_timestamps()
    ]
    signals = list(norm.normalize(frames))
    assert norm.frames_processed == len(frames)
    assert norm.signals_emitted >= len(signals)
    # At minimum we should have decoded engine hours, engine speed, fuel
    spns = {s.spn for s in signals}
    assert {247, 190}.issubset(spns)


def test_j1939_known_pgns_covers_aemp_set() -> None:
    norm = J1939Normalizer()
    expected_aemp = {65253, 61444, 61443, 65276, 65248, 65257, 65266}
    assert expected_aemp.issubset(norm.known_pgns())


def test_signal_throttle_drops_in_window_samples() -> None:
    """Burst within the throttle window: only first emission survives."""
    throttle = SignalThrottle(default_min_interval_ms=1000)
    base = datetime(2025, 6, 30, tzinfo=timezone.utc)
    signals = [
        DecodedSignal(pgn=61444, spn=190, source_address=0, value=1800,
                      timestamp=base + timedelta(milliseconds=offset))
        for offset in [0, 100, 500, 1500, 2500]
    ]
    emitted = list(throttle.filter(signals))
    # offsets 0, 1500, 2500 emit; 100 and 500 are dropped (within 1s of 0)
    assert [s.timestamp.timestamp() - base.timestamp() for s in emitted] == [
        pytest.approx(0.0),
        pytest.approx(1.5),
        pytest.approx(2.5),
    ]


def test_signal_throttle_per_pgn_override() -> None:
    """Per-PGN min-interval overrides the default."""
    throttle = SignalThrottle(
        default_min_interval_ms=1000,
        per_pgn_min_interval_ms={61444: 200},
    )
    base = datetime(2025, 6, 30, tzinfo=timezone.utc)
    signals = [
        DecodedSignal(pgn=61444, spn=190, source_address=0, value=1800,
                      timestamp=base + timedelta(milliseconds=offset))
        for offset in [0, 100, 250, 500]
    ]
    emitted = list(throttle.filter(signals))
    # 0, 250, 500 emit (>=200ms apart); 100 dropped
    assert len(emitted) == 3


def test_signal_throttle_separate_keys_per_source_address() -> None:
    """Two ECUs emitting same PGN throttle independently."""
    throttle = SignalThrottle(default_min_interval_ms=1000)
    base = datetime(2025, 6, 30, tzinfo=timezone.utc)
    signals = [
        DecodedSignal(pgn=61444, spn=190, source_address=0x00, value=1800, timestamp=base),
        DecodedSignal(pgn=61444, spn=190, source_address=0x01, value=2200, timestamp=base),
    ]
    emitted = list(throttle.filter(signals))
    # Both emit — different source addresses
    assert len(emitted) == 2


def test_signal_throttle_reset_clears_state() -> None:
    throttle = SignalThrottle(default_min_interval_ms=1000)
    base = datetime(2025, 6, 30, tzinfo=timezone.utc)
    sig = DecodedSignal(pgn=61444, spn=190, source_address=0, value=1800, timestamp=base)
    assert throttle.should_emit(sig)
    assert not throttle.should_emit(sig)  # second call within window
    throttle.reset()
    assert throttle.should_emit(sig)  # reset clears state


# ---------------------------------------------------------------------------
# Conformance — Sprint 25 exit criteria
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_classification_propagates_through_each_protocol() -> None:
    """Sprint 25 exit criterion — classification flows protocol → adapter → Sample."""
    for proto, node, cls in [
        ("opcua",   "ns=2;s=Sensor",            "operations"),
        ("iec61850","IED1/MEAS/MMXU1.A.phsA",   "critical-infrastructure"),
        ("j1939",   "65253/247",                "operations"),
    ]:
        m = AddressSpaceMapping(protocol=proto, name="t")
        m.add(AddressNode(
            node_id=node, canonical_entity="X", canonical_field="y",
            classification=cls,
        ))
        s = Sample(node_id=node, value=0)
        annotated = m.annotate(s)
        assert annotated.classification == cls


@pytest.mark.conformance
def test_conformance_each_protocol_has_smoke_test_dataset() -> None:
    """Sprint 25 exit criterion — each adapter ships a smoke-test dataset."""
    assert OPCUA_NODESET_XML
    assert OPCUA_SNAPSHOT
    assert IEC61850_SCD_XML
    assert IEC61850_SNAPSHOT
    assert J1939_FRAME_CAPTURE


@pytest.mark.conformance
def test_conformance_each_protocol_has_runbook() -> None:
    """Sprint 25 exit criterion — each adapter has a runbook."""
    from pathlib import Path

    runbooks_dir = Path(__file__).resolve().parent.parent / "src" / "apex_protocols" / "runbooks"
    for name in ("opcua-runbook.md", "iec61850-runbook.md", "j1939-runbook.md"):
        assert (runbooks_dir / name).exists(), f"Missing runbook: {name}"


@pytest.mark.conformance
def test_conformance_each_protocol_has_reference_workspace() -> None:
    """Sprint 25 exit criterion — each adapter has a reference workspace."""
    from pathlib import Path

    examples_dir = Path(__file__).resolve().parent.parent / "src" / "apex_protocols" / "examples"
    for name in (
        "opcua_north_plant_mapping.yaml",
        "iec61850_substation_mapping.yaml",
        "j1939_haul_truck_mapping.yaml",
    ):
        assert (examples_dir / name).exists(), f"Missing reference workspace: {name}"


@pytest.mark.conformance
def test_conformance_j1939_named_aemp_pgns_decoded_in_normalizer() -> None:
    """Sprint 25 §25.3.2 — integrate with apex_standards.j1939 (Sprint 21)."""
    aemp_named_pgns = {65253, 61444, 61443, 65276, 65248, 65257, 65266}
    assert aemp_named_pgns.issubset(set(SPN_LAYOUTS))
