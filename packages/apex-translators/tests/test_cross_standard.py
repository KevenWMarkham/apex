"""Tests for apex_translators.cross_standard — Sprint 24 Tasks 24.2-24.5."""

from __future__ import annotations

import json
from datetime import datetime, timezone

import pytest

from apex_translators import (
    AEMP_EVENT_TYPES,
    CIM_ISO_EQUIPMENT_MAP,
    J1939_PGN_MAP,
    aemp_to_j1939,
    cda_to_fhir,
    cim_to_iso15926,
    hl7v2_to_fhir,
    iso15926_to_cim,
    j1939_to_aemp,
    parse_cda,
    parse_hl7v2,
)
from apex_translators.cross_standard.cim_iso15926 import CIMAsset, ISO15926Asset
from apex_translators.cross_standard.j1939_aemp import (
    AEMP_PGN_MAP,
    AEMPEvent,
    J1939Frame,
)
from apex_translators.fixtures import CDA_FIXTURES, HL7V2_FIXTURES


# ---------------------------------------------------------------------------
# Task 24.2 — HL7 v2 → FHIR R4
# ---------------------------------------------------------------------------


def test_hl7v2_to_fhir_emits_bundle() -> None:
    msg = parse_hl7v2(HL7V2_FIXTURES["ADT^A04"])
    bundle = hl7v2_to_fhir(msg)
    assert bundle["resourceType"] == "Bundle"
    assert bundle["type"] == "collection"
    assert "entry" in bundle


def test_hl7v2_adt_emits_patient_resource() -> None:
    msg = parse_hl7v2(HL7V2_FIXTURES["ADT^A04"])
    bundle = hl7v2_to_fhir(msg)
    types = {e["resource"]["resourceType"] for e in bundle["entry"]}
    assert "Patient" in types


def test_hl7v2_adt_extracts_patient_demographics() -> None:
    msg = parse_hl7v2(HL7V2_FIXTURES["ADT^A04"])
    bundle = hl7v2_to_fhir(msg)
    pat = next(
        e["resource"] for e in bundle["entry"]
        if e["resource"]["resourceType"] == "Patient"
    )
    assert pat["gender"] == "male"
    assert pat["birthDate"] == "1980-01-01"
    assert pat["name"][0]["family"] == "DOE"
    assert "JOHN" in pat["name"][0]["given"]


def test_hl7v2_adt_emits_encounter_resource() -> None:
    msg = parse_hl7v2(HL7V2_FIXTURES["ADT^A04"])
    bundle = hl7v2_to_fhir(msg)
    types = {e["resource"]["resourceType"] for e in bundle["entry"]}
    assert "Encounter" in types


def test_hl7v2_adt_emits_allergy_intolerance() -> None:
    msg = parse_hl7v2(HL7V2_FIXTURES["ADT^A04"])
    bundle = hl7v2_to_fhir(msg)
    allergies = [
        e["resource"] for e in bundle["entry"]
        if e["resource"]["resourceType"] == "AllergyIntolerance"
    ]
    assert len(allergies) >= 1
    assert "PENICILLIN" in allergies[0]["code"]["text"].upper()


def test_hl7v2_oru_emits_observations_and_diagnostic_report() -> None:
    msg = parse_hl7v2(HL7V2_FIXTURES["ORU^R01"])
    bundle = hl7v2_to_fhir(msg)
    types = [e["resource"]["resourceType"] for e in bundle["entry"]]
    assert types.count("Observation") == 2
    assert "DiagnosticReport" in types


def test_hl7v2_oru_observation_value_is_quantity() -> None:
    msg = parse_hl7v2(HL7V2_FIXTURES["ORU^R01"])
    bundle = hl7v2_to_fhir(msg)
    obs = [
        e["resource"] for e in bundle["entry"]
        if e["resource"]["resourceType"] == "Observation"
    ]
    glucose = next(
        o for o in obs
        if "Glucose" in o["code"]["coding"][0].get("display", "")
    )
    assert glucose["valueQuantity"]["value"] == 95
    assert glucose["valueQuantity"]["unit"] == "mg/dL"


def test_hl7v2_oru_uses_loinc_system_uri() -> None:
    msg = parse_hl7v2(HL7V2_FIXTURES["ORU^R01"])
    bundle = hl7v2_to_fhir(msg)
    obs = next(
        e["resource"] for e in bundle["entry"]
        if e["resource"]["resourceType"] == "Observation"
    )
    assert obs["code"]["coding"][0]["system"] == "http://loinc.org"


def test_hl7v2_orm_emits_medication_request() -> None:
    msg = parse_hl7v2(HL7V2_FIXTURES["ORM^O01"])
    bundle = hl7v2_to_fhir(msg)
    types = {e["resource"]["resourceType"] for e in bundle["entry"]}
    assert "MedicationRequest" in types


def test_hl7v2_to_fhir_rejects_wrong_format() -> None:
    from apex_translators.base import FORMAT_EDI_X12, ParsedMessage

    bad = ParsedMessage(format=FORMAT_EDI_X12)
    with pytest.raises(ValueError, match="hl7v2"):
        hl7v2_to_fhir(bad)


def test_hl7v2_to_fhir_output_is_json_serializable() -> None:
    msg = parse_hl7v2(HL7V2_FIXTURES["ADT^A04"])
    bundle = hl7v2_to_fhir(msg)
    # Must round-trip through json without errors
    serialized = json.dumps(bundle)
    parsed = json.loads(serialized)
    assert parsed["resourceType"] == "Bundle"


# ---------------------------------------------------------------------------
# Task 24.3 — HL7 CDA → FHIR R4
# ---------------------------------------------------------------------------


def test_cda_to_fhir_emits_bundle() -> None:
    msg = parse_cda(CDA_FIXTURES["CCD"])
    bundle = cda_to_fhir(msg)
    assert bundle["resourceType"] == "Bundle"
    assert "entry" in bundle


def test_cda_to_fhir_emits_patient_from_record_target() -> None:
    msg = parse_cda(CDA_FIXTURES["CCD"])
    bundle = cda_to_fhir(msg)
    pat = next(
        e["resource"] for e in bundle["entry"]
        if e["resource"]["resourceType"] == "Patient"
    )
    assert pat["gender"] == "male"
    assert pat["name"][0]["family"] == "Doe"


def test_cda_to_fhir_maps_allergies_section_to_allergy_intolerance() -> None:
    msg = parse_cda(CDA_FIXTURES["CCD"])
    bundle = cda_to_fhir(msg)
    types = [e["resource"]["resourceType"] for e in bundle["entry"]]
    assert "AllergyIntolerance" in types


def test_cda_to_fhir_maps_medications_section_to_medication_statement() -> None:
    msg = parse_cda(CDA_FIXTURES["CCD"])
    bundle = cda_to_fhir(msg)
    types = [e["resource"]["resourceType"] for e in bundle["entry"]]
    assert "MedicationStatement" in types


def test_cda_to_fhir_maps_problems_section_to_condition() -> None:
    msg = parse_cda(CDA_FIXTURES["CCD"])
    bundle = cda_to_fhir(msg)
    types = [e["resource"]["resourceType"] for e in bundle["entry"]]
    assert "Condition" in types


def test_cda_to_fhir_maps_results_section_to_observation() -> None:
    msg = parse_cda(CDA_FIXTURES["CCD"])
    bundle = cda_to_fhir(msg)
    types = [e["resource"]["resourceType"] for e in bundle["entry"]]
    assert "Observation" in types


def test_cda_to_fhir_resolves_oid_to_snomed_uri() -> None:
    msg = parse_cda(CDA_FIXTURES["CCD"])
    bundle = cda_to_fhir(msg)
    cond = next(
        e["resource"] for e in bundle["entry"]
        if e["resource"]["resourceType"] == "Condition"
    )
    assert cond["code"]["coding"][0]["system"] == "http://snomed.info/sct"


def test_cda_to_fhir_links_resources_to_patient() -> None:
    msg = parse_cda(CDA_FIXTURES["CCD"])
    bundle = cda_to_fhir(msg)
    pat = next(
        e["resource"] for e in bundle["entry"]
        if e["resource"]["resourceType"] == "Patient"
    )
    pat_ref = f"Patient/{pat['id']}"
    for entry in bundle["entry"]:
        r = entry["resource"]
        if r["resourceType"] == "Patient":
            continue
        ref_field = "subject" if r["resourceType"] != "AllergyIntolerance" else "patient"
        assert r[ref_field]["reference"] == pat_ref


def test_cda_to_fhir_rejects_wrong_format() -> None:
    from apex_translators.base import FORMAT_HL7V2, ParsedMessage

    bad = ParsedMessage(format=FORMAT_HL7V2)
    with pytest.raises(ValueError, match="cda"):
        cda_to_fhir(bad)


# ---------------------------------------------------------------------------
# Task 24.4 — CIM ↔ ISO 15926
# ---------------------------------------------------------------------------


def test_cim_to_iso15926_named_class_round_trips() -> None:
    src = CIMAsset(
        cim_class="Substation",
        mrid="urn:uuid:substation-001",
        name="North Bay Substation",
        description="Distribution substation, 138 kV bus",
        attributes={"voltage_kv": 138},
    )
    iso = cim_to_iso15926(src)
    assert iso.rdl_class == "ELECTRICAL_SUBSTATION"
    assert iso.object_id == src.mrid
    cim_back = iso15926_to_cim(iso)
    assert cim_back.cim_class == "Substation"
    assert cim_back.mrid == src.mrid
    assert cim_back.name == src.name
    assert cim_back.attributes["voltage_kv"] == 138


@pytest.mark.parametrize("cim_class", sorted(CIM_ISO_EQUIPMENT_MAP))
def test_every_named_cim_class_round_trips(cim_class: str) -> None:
    src = CIMAsset(cim_class=cim_class, mrid=f"urn:uuid:{cim_class}-1")
    iso = cim_to_iso15926(src)
    cim_back = iso15926_to_cim(iso)
    assert cim_back.cim_class == cim_class
    assert cim_back.mrid == src.mrid


def test_cim_to_iso15926_rejects_unknown_class() -> None:
    src = CIMAsset(cim_class="MysteriousEquipment", mrid="urn:uuid:1")
    with pytest.raises(KeyError, match="MysteriousEquipment"):
        cim_to_iso15926(src)


def test_iso15926_to_cim_rejects_unknown_class() -> None:
    src = ISO15926Asset(rdl_class="UNKNOWN_CLASS", object_id="x")
    with pytest.raises(KeyError, match="UNKNOWN_CLASS"):
        iso15926_to_cim(src)


def test_cim_iso_map_is_bijection() -> None:
    """Every CIM → ISO mapping has an inverse and they're consistent."""
    from apex_translators.cross_standard.cim_iso15926 import (
        ISO_CIM_EQUIPMENT_MAP,
    )
    for cim, iso in CIM_ISO_EQUIPMENT_MAP.items():
        assert ISO_CIM_EQUIPMENT_MAP[iso] == cim


# ---------------------------------------------------------------------------
# Task 24.5 — SAE J1939 ↔ AEMP 2.0
# ---------------------------------------------------------------------------


def test_j1939_engine_hours_to_aemp() -> None:
    frame = J1939Frame(
        pgn=65253, spn=247, value=1234.5, units="h", source_address=0,
        timestamp=datetime(2025, 6, 30, 14, 30, tzinfo=timezone.utc),
    )
    event = j1939_to_aemp(frame, equipment_id="CAT-D6T-12345", oem="Caterpillar")
    assert event.event_type == "EngineHours"
    assert event.value == 1234.5
    assert event.units == "h"
    assert event.equipment_id == "CAT-D6T-12345"
    assert event.oem == "Caterpillar"


@pytest.mark.parametrize("pgn,mapping", sorted(J1939_PGN_MAP.items()))
def test_every_named_pgn_round_trips(pgn: int, mapping) -> None:
    """Sprint 24 §24.5.2 — round-trip preserves every named cross-OEM signal."""
    frame = J1939Frame(
        pgn=pgn, spn=mapping.spn, value=42.0, units=mapping.units,
        timestamp=datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    event = j1939_to_aemp(frame, equipment_id="ASSET-001")
    assert event.event_type == mapping.aemp_event
    frame_back = aemp_to_j1939(event)
    assert frame_back.pgn == pgn
    assert frame_back.spn == mapping.spn
    assert frame_back.value == 42.0


def test_aemp_to_j1939_round_trip() -> None:
    event = AEMPEvent(
        event_type="FuelLevel",
        value=78,
        units="%",
        equipment_id="JD-9620R-77",
        timestamp=datetime(2025, 6, 30, 14, 30, tzinfo=timezone.utc),
    )
    frame = aemp_to_j1939(event)
    assert frame.pgn == 65276
    assert frame.spn == 96
    event_back = j1939_to_aemp(frame, equipment_id=event.equipment_id)
    assert event_back.event_type == "FuelLevel"
    assert event_back.value == 78


def test_j1939_to_aemp_rejects_unknown_pgn() -> None:
    frame = J1939Frame(pgn=99999, spn=1, value=0)
    with pytest.raises(KeyError, match="99999"):
        j1939_to_aemp(frame, equipment_id="X")


def test_aemp_to_j1939_rejects_unknown_event() -> None:
    event = AEMPEvent(
        event_type="MysteriousSignal", value=0, units="", equipment_id="X"
    )
    with pytest.raises(KeyError, match="MysteriousSignal"):
        aemp_to_j1939(event)


def test_aemp_event_types_covers_named_signals() -> None:
    """AEMP_EVENT_TYPES is a superset of (or equal to) the PGN map's events."""
    pgn_events = {m.aemp_event for m in J1939_PGN_MAP.values()}
    aemp_set = set(AEMP_EVENT_TYPES)
    assert pgn_events.issubset(aemp_set)


def test_j1939_to_aemp_preserves_source_metadata_for_round_trip() -> None:
    frame = J1939Frame(pgn=61444, spn=190, value=1800.0, units="rpm", source_address=0x10)
    event = j1939_to_aemp(frame, equipment_id="X")
    assert event.extras["_source_pgn"] == 61444
    assert event.extras["_source_spn"] == 190
    frame_back = aemp_to_j1939(event)
    assert frame_back.source_address == 0x10


# ---------------------------------------------------------------------------
# Conformance — Sprint 24 exit criteria
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_hl7v2_to_fhir_supports_adt_and_oru() -> None:
    """Sprint 24 §24.2.1 + §24.2.2 — both ADT and ORU produce non-empty Bundles."""
    for msg_type in ["ADT^A04", "ORU^R01"]:
        msg = parse_hl7v2(HL7V2_FIXTURES[msg_type])
        bundle = hl7v2_to_fhir(msg)
        assert bundle["entry"], f"Empty Bundle for {msg_type}"


@pytest.mark.conformance
def test_conformance_cda_to_fhir_maps_four_named_sections() -> None:
    """Sprint 24 §24.3.2 — Allergies, Medications, Problems, Results all map."""
    msg = parse_cda(CDA_FIXTURES["CCD"])
    bundle = cda_to_fhir(msg)
    types = {e["resource"]["resourceType"] for e in bundle["entry"]}
    assert {
        "AllergyIntolerance", "MedicationStatement", "Condition", "Observation"
    }.issubset(types)


@pytest.mark.conformance
def test_conformance_cim_iso_named_classes_present() -> None:
    """Sprint 24 §24.4.2 — at minimum the structural-named subset is mapped."""
    expected = {"Substation", "Feeder", "PowerTransformer", "Breaker", "Asset"}
    assert expected.issubset(set(CIM_ISO_EQUIPMENT_MAP))


@pytest.mark.conformance
def test_conformance_j1939_aemp_minimum_signal_set() -> None:
    """Sprint 24 §24.5.2 — minimum cross-OEM signal set covered."""
    minimum = {"EngineHours", "EngineSpeed", "FuelLevel", "Location"}
    pgn_events = {m.aemp_event for m in J1939_PGN_MAP.values()}
    assert minimum.issubset(pgn_events)


@pytest.mark.conformance
def test_conformance_lossy_cases_doc_present() -> None:
    """Sprint 24 exit criterion — lossy cases documented."""
    from pathlib import Path

    package_root = Path(__file__).resolve().parent.parent
    assert (package_root / "LOSSY_CASES.md").exists()
