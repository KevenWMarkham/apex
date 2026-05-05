"""Tests for apex_purview.classifications."""

from __future__ import annotations

from pathlib import Path

import pytest

from apex_purview.classifications import (
    APEX_CLASSIFICATIONS,
    ClassificationAttachment,
    ClassificationDef,
    emit_classification_typedefs,
    emit_entity_classifications,
    enumerate_classifications,
    load_schema_yaml,
)

FIXTURES = Path(__file__).parent / "fixtures"


# ---------------------------------------------------------------------------
# Fixture loaders
# ---------------------------------------------------------------------------


@pytest.fixture
def scml_schema() -> dict:
    return load_schema_yaml(FIXTURES / "schema_scml.yaml")


@pytest.fixture
def empty_schema() -> dict:
    return load_schema_yaml(FIXTURES / "schema_no_classifications.yaml")


@pytest.fixture
def unknown_schema() -> dict:
    return load_schema_yaml(FIXTURES / "schema_unknown_classification.yaml")


@pytest.fixture
def hls_schema() -> dict:
    return load_schema_yaml(FIXTURES / "schema_hls_patient.yaml")


# ---------------------------------------------------------------------------
# enumerate_classifications
# ---------------------------------------------------------------------------


def test_enumerate_returns_set_of_classification_keys(scml_schema: dict) -> None:
    keys = enumerate_classifications(scml_schema)
    assert "internal" in keys
    assert "trade_secret" in keys


def test_enumerate_returns_empty_for_unclassified_schema(empty_schema: dict) -> None:
    assert enumerate_classifications(empty_schema) == set()


def test_enumerate_normalizes_keys() -> None:
    schema = {
        "entities": [
            {
                "name": "x",
                "classification": "Trade Secret",
                "attributes": [
                    {"name": "a", "classification": "trade-secret"},
                    {"name": "b", "classification": "TRADE_SECRET"},
                ],
            }
        ]
    }
    # All three representations must collapse to the canonical snake_case key
    assert enumerate_classifications(schema) == {"trade_secret"}


def test_enumerate_picks_up_hls_phi_pii_genetic(hls_schema: dict) -> None:
    keys = enumerate_classifications(hls_schema)
    assert keys == {"phi", "pii", "genetic"}


# ---------------------------------------------------------------------------
# emit_classification_typedefs
# ---------------------------------------------------------------------------


def test_emit_typedefs_contains_only_referenced_classifications(scml_schema: dict) -> None:
    payload = emit_classification_typedefs(scml_schema)
    names = {d["name"] for d in payload["classificationDefs"]}
    assert names == {"APEX.Internal", "APEX.TradeSecret"}


def test_emit_typedefs_all_classifications_when_include_all(empty_schema: dict) -> None:
    payload = emit_classification_typedefs(empty_schema, include_all=True)
    names = {d["name"] for d in payload["classificationDefs"]}
    # Must contain every canonical APEX classification
    expected = {spec["type_name"] for spec in APEX_CLASSIFICATIONS.values()}
    assert names == expected


def test_emit_typedefs_is_idempotent(scml_schema: dict) -> None:
    """Running the emitter twice must produce byte-identical output."""
    first = emit_classification_typedefs(scml_schema)
    second = emit_classification_typedefs(scml_schema)
    assert first == second


def test_emit_typedefs_has_atlas_v2_shape(scml_schema: dict) -> None:
    payload = emit_classification_typedefs(scml_schema)
    # Required Atlas v2 typedefs envelope keys
    for key in (
        "enumDefs",
        "structDefs",
        "classificationDefs",
        "entityDefs",
        "relationshipDefs",
        "businessMetadataDefs",
    ):
        assert key in payload, f"Atlas v2 envelope missing key: {key}"
    # Each classificationDef has the required Atlas fields
    for d in payload["classificationDefs"]:
        for key in ("category", "name", "description", "typeVersion"):
            assert key in d, f"classificationDef missing required key {key}"
        assert d["category"] == "CLASSIFICATION"


def test_emit_typedefs_rejects_unknown_classification(unknown_schema: dict) -> None:
    with pytest.raises(ValueError, match="Unknown APEX classification"):
        emit_classification_typedefs(unknown_schema)


def test_emit_typedefs_sorted_for_deterministic_diff(empty_schema: dict) -> None:
    """Definitions must come out in sorted order by classification key for
    reviewable CI diffs."""
    payload = emit_classification_typedefs(empty_schema, include_all=True)
    names = [d["name"] for d in payload["classificationDefs"]]
    # APEX.* sorts alphabetically by type_name
    assert names == sorted(names)


# ---------------------------------------------------------------------------
# emit_entity_classifications
# ---------------------------------------------------------------------------


def test_emit_attachments_entity_level(scml_schema: dict) -> None:
    attachments = emit_entity_classifications(scml_schema)
    # SCML fixture has `sku` entity with classification=internal
    sku_entity = [a for a in attachments if a["entityQualifiedName"] == "apex.rc.scml.sku"]
    assert len(sku_entity) == 1
    assert sku_entity[0]["typeName"] == "APEX.Internal"


def test_emit_attachments_attribute_level(scml_schema: dict) -> None:
    attachments = emit_entity_classifications(scml_schema)
    # SCML fixture has sku.unit_cost_token with classification=trade_secret
    trade = [
        a
        for a in attachments
        if a["entityQualifiedName"] == "apex.rc.scml.sku.unit_cost_token"
    ]
    assert len(trade) == 1
    assert trade[0]["typeName"] == "APEX.TradeSecret"


def test_emit_attachments_empty_schema_returns_empty(empty_schema: dict) -> None:
    assert emit_entity_classifications(empty_schema) == []


def test_emit_attachments_hls_schema(hls_schema: dict) -> None:
    attachments = emit_entity_classifications(hls_schema)
    # Entity: patient = phi
    patient = [a for a in attachments if a["entityQualifiedName"] == "apex.hls.patientml.patient"]
    assert patient[0]["typeName"] == "APEX.PHI"
    # Attributes: patient_mrn_token=phi, patient_dob=phi, preferred_name=pii, genomic_panel_token=genetic
    types_by_qname = {a["entityQualifiedName"]: a["typeName"] for a in attachments}
    assert types_by_qname["apex.hls.patientml.patient.patient_mrn_token"] == "APEX.PHI"
    assert types_by_qname["apex.hls.patientml.patient.patient_dob"] == "APEX.PHI"
    assert types_by_qname["apex.hls.patientml.patient.preferred_name"] == "APEX.PII"
    assert types_by_qname["apex.hls.patientml.patient.genomic_panel_token"] == "APEX.Genetic"


def test_emit_attachments_has_atlas_v2_shape(scml_schema: dict) -> None:
    attachments = emit_entity_classifications(scml_schema)
    for a in attachments:
        for key in (
            "typeName",
            "attributes",
            "propagate",
            "removePropagationsOnEntityDelete",
            "entityQualifiedName",
        ):
            assert key in a


def test_emit_attachments_rejects_missing_practice() -> None:
    bad = {"kind": "schema", "family": "scml", "entities": [{"name": "x", "classification": "internal"}]}
    with pytest.raises(ValueError, match="Missing required field: 'practice'"):
        emit_entity_classifications(bad)


def test_emit_attachments_rejects_missing_family() -> None:
    bad = {"kind": "schema", "practice": "rc", "entities": [{"name": "x", "classification": "internal"}]}
    with pytest.raises(ValueError, match="Missing required field: 'family'"):
        emit_entity_classifications(bad)


def test_emit_attachments_is_idempotent(scml_schema: dict) -> None:
    first = emit_entity_classifications(scml_schema)
    second = emit_entity_classifications(scml_schema)
    assert first == second


# ---------------------------------------------------------------------------
# ClassificationDef / ClassificationAttachment dataclasses
# ---------------------------------------------------------------------------


def test_classification_def_to_atlas_shape() -> None:
    d = ClassificationDef(type_name="APEX.Test", description="A test.")
    atlas = d.to_atlas()
    assert atlas["category"] == "CLASSIFICATION"
    assert atlas["name"] == "APEX.Test"
    assert atlas["description"] == "A test."
    assert atlas["superTypes"] == []


def test_classification_attachment_defaults_propagate_true() -> None:
    a = ClassificationAttachment(type_name="APEX.PII", qualified_name="apex.rc.cxml.customer")
    atlas = a.to_atlas()
    assert atlas["propagate"] is True
    assert atlas["removePropagationsOnEntityDelete"] is True


# ---------------------------------------------------------------------------
# load_schema_yaml
# ---------------------------------------------------------------------------


def test_load_schema_yaml_rejects_wrong_kind(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("kind: orchestration\nname: not-a-schema\n", encoding="utf-8")
    with pytest.raises(ValueError, match="kind='orchestration'"):
        load_schema_yaml(bad)


def test_load_schema_yaml_rejects_non_mapping(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("- just-a-list\n- of\n- strings\n", encoding="utf-8")
    with pytest.raises(ValueError, match="must parse to a mapping"):
        load_schema_yaml(bad)


# ---------------------------------------------------------------------------
# Conformance — payload round-trips cleanly through json
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_typedefs_payload_is_json_round_trippable(scml_schema: dict) -> None:
    import json
    payload = emit_classification_typedefs(scml_schema)
    assert json.loads(json.dumps(payload)) == payload


@pytest.mark.conformance
def test_attachments_payload_is_json_round_trippable(scml_schema: dict) -> None:
    import json
    attachments = emit_entity_classifications(scml_schema)
    assert json.loads(json.dumps(attachments)) == attachments
