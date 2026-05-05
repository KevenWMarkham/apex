"""Tests for apex_purview.catalog — Sprint 13 Task 13.5."""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from apex_purview._cli import purview_app
from apex_purview.catalog import (
    EntityRelationship,
    GlossaryDef,
    GlossaryTerm,
    emit_catalog_bundle,
    emit_glossary_def,
    emit_glossary_terms_from_schema,
    emit_relationship_typedefs,
    emit_relationships_from_schema,
)
from apex_purview.classifications import load_schema_yaml

FIXTURES = Path(__file__).parent / "fixtures"
runner = CliRunner()


# ---------------------------------------------------------------------------
# Glossary term emission
# ---------------------------------------------------------------------------


def test_glossary_term_to_atlas_shape() -> None:
    term = GlossaryTerm(
        name="SKU.unit_cost_token",
        qualified_name="apex.rc.scml.sku.unit_cost_token@apex-glossary",
        short_description="Tokenised supplier-confidential unit cost.",
        related_entity_qnames=("apex.rc.scml.sku.unit_cost_token",),
    )
    payload = term.to_atlas()
    assert payload["name"] == "SKU.unit_cost_token"
    assert payload["qualifiedName"].endswith("@apex-glossary")
    assert "Tokenised" in payload["shortDescription"]
    assert len(payload["assignedEntities"]) == 1


def test_emit_glossary_terms_from_scml() -> None:
    schema = load_schema_yaml(FIXTURES / "schema_scml.yaml")
    terms = emit_glossary_terms_from_schema(schema)
    # SCML fixture has descriptions on sku_key and unit_cost_token
    # (the sku entity itself has no description in the fixture)
    names = [t.name for t in terms]
    assert "sku.sku_key" in names
    assert "sku.unit_cost_token" in names
    # Every emitted term carries a non-empty description
    assert all(t.short_description for t in terms)


def test_emit_glossary_terms_no_descriptions_returns_empty() -> None:
    schema = load_schema_yaml(FIXTURES / "schema_no_classifications.yaml")
    # The fixture has no descriptions on its widget entity attributes
    terms = emit_glossary_terms_from_schema(schema)
    # Only entries with descriptions appear
    assert all(t.short_description for t in terms)


def test_emit_glossary_def_top_level() -> None:
    payload = emit_glossary_def()
    assert payload["qualifiedName"] == "APEX@apex-glossary"
    assert payload["name"] == "APEX Business Glossary"


def test_glossary_term_short_description_truncated_at_200() -> None:
    long = "x" * 500
    term = GlossaryTerm(
        name="t",
        qualified_name="q@apex-glossary",
        short_description=long[:200],
        long_description=long,
    )
    payload = term.to_atlas()
    assert len(payload["shortDescription"]) == 200
    assert len(payload["longDescription"]) == 500


def test_glossary_def_dataclass_overrides() -> None:
    g = GlossaryDef(
        qualified_name="custom@g",
        name="Custom",
        short_description="Custom.",
        language="French",
        usage="Pilot",
    )
    payload = g.to_atlas()
    assert payload["qualifiedName"] == "custom@g"
    assert payload["language"] == "French"


# ---------------------------------------------------------------------------
# Relationship emission
# ---------------------------------------------------------------------------


def test_entity_relationship_to_atlas_shape() -> None:
    rel = EntityRelationship(
        relationship_type="apex_fk",
        end1_type="apex_silver_table",
        end1_qualified_name="apex.rc.scml.sku",
        end2_type="apex_silver_table",
        end2_qualified_name="apex.rc.scml.supplier",
        cardinality="N:1",
        label="supplier",
    )
    payload = rel.to_atlas()
    assert payload["typeName"] == "apex_fk"
    assert payload["end1"]["uniqueAttributes"]["qualifiedName"] == "apex.rc.scml.sku"
    assert payload["end2"]["uniqueAttributes"]["qualifiedName"] == "apex.rc.scml.supplier"
    assert payload["attributes"]["cardinality"] == "N:1"


def test_emit_relationships_from_scml_finds_supplier_fk() -> None:
    schema = load_schema_yaml(FIXTURES / "schema_scml.yaml")
    rels = emit_relationships_from_schema(schema)
    # SCML SKU declares a relationship "supplier" → supplier with cardinality N:1
    sku_to_supplier = [
        r
        for r in rels
        if r.end1_qualified_name == "apex.rc.scml.sku"
        and r.end2_qualified_name == "apex.rc.scml.supplier"
    ]
    assert len(sku_to_supplier) == 1
    assert sku_to_supplier[0].cardinality == "N:1"
    assert sku_to_supplier[0].label == "supplier"


def test_emit_relationships_empty_when_none_declared() -> None:
    schema = load_schema_yaml(FIXTURES / "schema_no_classifications.yaml")
    assert emit_relationships_from_schema(schema) == []


# ---------------------------------------------------------------------------
# Bundle + relationshipDefs
# ---------------------------------------------------------------------------


def test_emit_catalog_bundle_includes_all_three_sections() -> None:
    schema = load_schema_yaml(FIXTURES / "schema_scml.yaml")
    bundle = emit_catalog_bundle(schema)
    assert "glossary" in bundle
    assert "terms" in bundle
    assert "relationships" in bundle
    assert isinstance(bundle["glossary"], dict)
    assert isinstance(bundle["terms"], list)
    assert isinstance(bundle["relationships"], list)


def test_relationship_typedefs_register_apex_fk_and_apex_join() -> None:
    payload = emit_relationship_typedefs()
    names = {d["name"] for d in payload["relationshipDefs"]}
    assert names == {"apex_fk", "apex_join"}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_emit_catalog_stdout() -> None:
    result = runner.invoke(
        purview_app,
        ["emit-catalog", str(FIXTURES / "schema_scml.yaml")],
    )
    assert result.exit_code == 0, result.stdout
    bundle = json.loads(result.stdout)
    assert bundle["glossary"]["name"] == "APEX Business Glossary"


def test_cli_emit_relationship_typedefs_stdout() -> None:
    result = runner.invoke(purview_app, ["emit-relationship-typedefs"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert len(payload["relationshipDefs"]) == 2
