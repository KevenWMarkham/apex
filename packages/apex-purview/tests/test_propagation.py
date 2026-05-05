"""Tests for apex_purview.propagation — Sprint 13 Task 13.6."""

from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from apex_purview._cli import purview_app
from apex_purview.classifications import load_schema_yaml
from apex_purview.lineage import load_lineage_spec
from apex_purview.propagation import (
    CLASSIFICATION_SEVERITY,
    PropagationNode,
    build_propagation_graph,
    most_restrictive,
    severity,
    validate_propagation,
)

FIXTURES = Path(__file__).parent / "fixtures"
runner = CliRunner()


# ---------------------------------------------------------------------------
# Severity
# ---------------------------------------------------------------------------


def test_severity_strict_ordering() -> None:
    assert severity("public") < severity("internal")
    assert severity("internal") < severity("pii")
    assert severity("pii") < severity("phi")
    assert severity("phi") < severity("restricted")


def test_severity_normalizes_keys() -> None:
    assert severity("Trade Secret") == severity("trade_secret")
    assert severity("TRADE-SECRET") == severity("trade_secret")


def test_severity_rejects_unknown() -> None:
    with pytest.raises(ValueError, match="Unknown classification"):
        severity("sparklepants")


def test_classification_severity_covers_all_canonical() -> None:
    from apex_purview.classifications import APEX_CLASSIFICATIONS

    for c in APEX_CLASSIFICATIONS:
        assert c in CLASSIFICATION_SEVERITY


def test_most_restrictive_picks_highest() -> None:
    assert most_restrictive(["internal", "pii", "phi"]) == "phi"
    assert most_restrictive(["public", "trade_secret", "restricted"]) == "restricted"


def test_most_restrictive_empty_raises() -> None:
    with pytest.raises(ValueError, match="empty list"):
        most_restrictive([])


# ---------------------------------------------------------------------------
# Validator — happy path
# ---------------------------------------------------------------------------


def test_validate_propagation_no_inputs_no_violations() -> None:
    nodes = [
        PropagationNode(name="a", layer="silver", classification="internal"),
        PropagationNode(name="b", layer="silver", classification="pii"),
    ]
    report = validate_propagation(nodes)
    assert report.ok
    assert report.violations == []
    assert report.nodes_checked == 2
    assert report.exit_code == 0


def test_validate_propagation_input_chain_ok() -> None:
    """Gold inherits the most restrictive of its Silver inputs — happy."""
    nodes = [
        PropagationNode(name="silver.sku", layer="silver", classification="internal"),
        PropagationNode(name="silver.cost", layer="silver", classification="trade_secret"),
        PropagationNode(
            name="gold.view",
            layer="gold",
            classification="trade_secret",  # inherited correctly
            inputs=["silver.sku", "silver.cost"],
        ),
    ]
    assert validate_propagation(nodes).ok


def test_validate_propagation_equal_severity_ok() -> None:
    """Declared classification matches required severity exactly — ok."""
    nodes = [
        PropagationNode(name="silver.a", layer="silver", classification="phi"),
        PropagationNode(
            name="gold.v",
            layer="gold",
            classification="phi",
            inputs=["silver.a"],
        ),
    ]
    assert validate_propagation(nodes).ok


# ---------------------------------------------------------------------------
# Validator — violations
# ---------------------------------------------------------------------------


def test_validate_propagation_relaxed_label_violation() -> None:
    nodes = [
        PropagationNode(name="silver.a", layer="silver", classification="internal"),
        PropagationNode(name="silver.b", layer="silver", classification="phi"),
        PropagationNode(
            name="gold.v",
            layer="gold",
            classification="internal",  # WRONG — must be at least phi
            inputs=["silver.a", "silver.b"],
        ),
    ]
    report = validate_propagation(nodes)
    assert not report.ok
    assert report.exit_code == 1
    assert len(report.violations) == 1
    v = report.violations[0]
    assert v.node == "gold.v"
    assert v.declared_classification == "internal"
    assert v.required_classification == "phi"
    assert ("silver.b", "phi") in v.triggering_inputs


def test_validate_propagation_multiple_triggering_inputs() -> None:
    nodes = [
        PropagationNode(name="a", layer="silver", classification="phi"),
        PropagationNode(name="b", layer="silver", classification="restricted"),
        PropagationNode(
            name="g",
            layer="gold",
            classification="internal",
            inputs=["a", "b"],
        ),
    ]
    report = validate_propagation(nodes)
    assert len(report.violations) == 1
    triggers = {q for q, _ in report.violations[0].triggering_inputs}
    assert triggers == {"a", "b"}


def test_validate_propagation_unknown_input_reference_raises() -> None:
    nodes = [
        PropagationNode(name="g", layer="gold", classification="phi", inputs=["ghost"]),
    ]
    with pytest.raises(ValueError, match="unknown input"):
        validate_propagation(nodes)


def test_validate_propagation_unknown_classification_raises() -> None:
    nodes = [PropagationNode(name="g", layer="gold", classification="sparklepants")]
    with pytest.raises(ValueError, match="unknown classification"):
        validate_propagation(nodes)


# ---------------------------------------------------------------------------
# build_propagation_graph
# ---------------------------------------------------------------------------


def test_build_graph_from_scml_schema() -> None:
    schema = load_schema_yaml(FIXTURES / "schema_scml.yaml")
    nodes = build_propagation_graph([schema])
    # SCML SKU has classification=internal at entity level + trade_secret on unit_cost_token
    sku_entity = next(n for n in nodes if n.name == "apex.rc.scml.sku")
    assert sku_entity.classification == "internal"
    cost_attr = next(n for n in nodes if n.name.endswith("unit_cost_token"))
    assert cost_attr.classification == "trade_secret"
    assert "apex.rc.scml.sku" in cost_attr.inputs


def test_build_graph_attribute_inherits_entity_classification_when_none() -> None:
    """Attribute without explicit classification inherits the entity's."""
    schema = load_schema_yaml(FIXTURES / "schema_scml.yaml")
    nodes = build_propagation_graph([schema])
    # sku_key has no classification → inherits 'internal' from sku entity
    sku_key = next(n for n in nodes if n.name.endswith("sku_key"))
    assert sku_key.classification == "internal"


def test_build_graph_with_lineage_creates_gold_node() -> None:
    schema = load_schema_yaml(FIXTURES / "schema_scml.yaml")
    lineage = {
        "kind": "lineage",
        "edges": [
            {
                "hop": "silver_to_gold",
                "silver_qualified_names": ["apex.rc.scml.sku"],
                "gold_qualified_name": "apex.rc.gold.vw_sku",
                "sql_sha": "abcdef123456",
            }
        ],
    }
    nodes = build_propagation_graph([schema], lineage)
    gold = next(n for n in nodes if n.name == "apex.rc.gold.vw_sku")
    assert gold.layer == "gold"
    # Gold inherits 'internal' from sku entity
    assert gold.classification == "internal"


def test_build_graph_with_lineage_inherits_most_restrictive() -> None:
    schemas = [
        {
            "practice": "rc",
            "family": "scml",
            "entities": [
                {"name": "a", "classification": "internal"},
                {"name": "b", "classification": "phi"},
            ],
        }
    ]
    lineage = {
        "kind": "lineage",
        "edges": [
            {
                "hop": "silver_to_gold",
                "silver_qualified_names": ["apex.rc.scml.a", "apex.rc.scml.b"],
                "gold_qualified_name": "apex.rc.gold.joined",
                "sql_sha": "x",
            }
        ],
    }
    nodes = build_propagation_graph(schemas, lineage)
    gold = next(n for n in nodes if n.name == "apex.rc.gold.joined")
    assert gold.classification == "phi"  # most restrictive of its inputs


# ---------------------------------------------------------------------------
# CLI integration
# ---------------------------------------------------------------------------


def test_cli_validate_propagation_clean() -> None:
    result = runner.invoke(
        purview_app,
        ["validate-propagation", str(FIXTURES / "schema_scml.yaml")],
    )
    assert result.exit_code == 0
    assert "violation" in result.stdout.lower()  # "0 violation(s)" appears in summary


def test_cli_validate_propagation_with_lineage() -> None:
    result = runner.invoke(
        purview_app,
        [
            "validate-propagation",
            str(FIXTURES / "schema_scml.yaml"),
            "--lineage",
            str(FIXTURES / "lineage_cold_chain.yaml"),
        ],
    )
    # Lineage references silver tables not in the SCML fixture (e.g.,
    # apex.rc.silver.scml.shipment); they fall back to 'internal'
    # default. Should still exit 0 — no violations from this fixture pair.
    assert result.exit_code == 0
