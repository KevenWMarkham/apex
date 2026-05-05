"""Tests for apex_purview.lineage — Sprint 13 Task 13.2."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from apex_purview._cli import purview_app
from apex_purview.lineage import (
    PROCESS_TYPES,
    EntityRef,
    LineageProcess,
    emit_agent_to_orchestration,
    emit_bronze_to_silver,
    emit_from_spec,
    emit_gold_to_mcp,
    emit_lineage_batch,
    emit_mcp_to_agent,
    emit_orchestration_to_audit,
    emit_process_typedefs,
    emit_silver_to_gold,
    emit_sor_to_bronze,
    load_lineage_spec,
)

FIXTURES = Path(__file__).parent / "fixtures"
runner = CliRunner()


# ---------------------------------------------------------------------------
# EntityRef + LineageProcess
# ---------------------------------------------------------------------------


def test_entity_ref_to_atlas_shape() -> None:
    ref = EntityRef("apex_gold_view", "apex.rc.gold.vw_agent_cold_chain")
    assert ref.to_atlas() == {
        "typeName": "apex_gold_view",
        "uniqueAttributes": {"qualifiedName": "apex.rc.gold.vw_agent_cold_chain"},
    }


def test_lineage_process_to_atlas_shape() -> None:
    p = LineageProcess(
        type_name="apex_bronze_to_silver",
        qualified_name="apex.rc.silver.scml.sku@xform.abc",
        display_name="test",
        inputs=(EntityRef("apex_bronze_table", "apex.rc.bronze.sku"),),
        outputs=(EntityRef("apex_silver_table", "apex.rc.silver.scml.sku"),),
        attributes={"commit_sha": "abc123"},
    )
    atlas = p.to_atlas()
    assert atlas["typeName"] == "apex_bronze_to_silver"
    assert atlas["attributes"]["qualifiedName"].endswith("xform.abc")
    assert len(atlas["attributes"]["inputs"]) == 1
    assert atlas["attributes"]["outputs"][0]["typeName"] == "apex_silver_table"
    assert atlas["attributes"]["commit_sha"] == "abc123"


# ---------------------------------------------------------------------------
# Subtask 13.2.1 — SOR → Bronze
# ---------------------------------------------------------------------------


def test_emit_sor_to_bronze_minimal() -> None:
    p = emit_sor_to_bronze(
        sor_qualified_name="oracle.pos.sku_master",
        sor_type_name="oracle_table",
        bronze_qualified_name="apex.rc.bronze.sku",
        pipeline_run_id="pipe-001",
    )
    assert p.type_name == "apex_sor_to_bronze"
    assert "pipe-001" in p.qualified_name
    assert p.attributes["pipeline_run_id"] == "pipe-001"
    assert p.inputs[0].qualified_name == "oracle.pos.sku_master"
    assert p.outputs[0].type_name == "apex_bronze_table"


def test_emit_sor_to_bronze_with_optional_fields() -> None:
    p = emit_sor_to_bronze(
        sor_qualified_name="sap.s4.material_master",
        sor_type_name="sap_table",
        bronze_qualified_name="apex.rc.bronze.material",
        pipeline_run_id="pipe-002",
        ingest_ts="2026-04-22T06:30:00Z",
        ingest_latency_ms=1234,
    )
    assert p.attributes["ingest_ts"] == "2026-04-22T06:30:00Z"
    assert p.attributes["ingest_latency_ms"] == 1234


# ---------------------------------------------------------------------------
# Subtask 13.2.2 — Bronze → Silver
# ---------------------------------------------------------------------------


def test_emit_bronze_to_silver_carries_commit_sha() -> None:
    p = emit_bronze_to_silver(
        bronze_qualified_name="apex.rc.bronze.sku",
        silver_qualified_name="apex.rc.silver.scml.sku",
        notebook_url="adf://notebooks/b-to-s/v1",
        commit_sha="7f3a9b2c4d5e6f1a2b3c",
    )
    assert p.type_name == "apex_bronze_to_silver"
    assert p.attributes["commit_sha"] == "7f3a9b2c4d5e6f1a2b3c"
    assert "7f3a9b2c4d5e" in p.qualified_name  # first 12 chars
    assert p.attributes["notebook_url"].startswith("adf://")


def test_emit_bronze_to_silver_optional_transform_version() -> None:
    p = emit_bronze_to_silver(
        bronze_qualified_name="apex.rc.bronze.lot",
        silver_qualified_name="apex.rc.silver.scml.lot",
        notebook_url="adf://x",
        commit_sha="abcdef012345",
        transform_version="2.0.1",
    )
    assert p.attributes["transform_version"] == "2.0.1"


# ---------------------------------------------------------------------------
# Subtask 13.2.3 — Silver → Gold
# ---------------------------------------------------------------------------


def test_emit_silver_to_gold_multi_input() -> None:
    p = emit_silver_to_gold(
        silver_qualified_names=[
            "apex.rc.silver.scml.shipment",
            "apex.rc.silver.scml.lot",
        ],
        gold_qualified_name="apex.rc.gold.vw_agent_cold_chain",
        sql_sha="5e6f7a8b9c1d2e3f",
    )
    assert p.type_name == "apex_silver_to_gold"
    assert len(p.inputs) == 2
    assert all(i.type_name == "apex_silver_table" for i in p.inputs)
    assert p.outputs[0].type_name == "apex_gold_view"
    assert p.attributes["gold_type"] == "direct_lake_view"  # default


def test_emit_silver_to_gold_custom_gold_type() -> None:
    p = emit_silver_to_gold(
        silver_qualified_names=["apex.rc.silver.merml.price"],
        gold_qualified_name="apex.rc.gold.kql_price_watch",
        sql_sha="deadbeef",
        gold_type="kql_function",
        view_definition_url="github://deloitte/apex/kql/price-watch.kql",
    )
    assert p.attributes["gold_type"] == "kql_function"
    assert p.attributes["view_definition_url"].endswith(".kql")


# ---------------------------------------------------------------------------
# Subtask 13.2.4 — Gold → MCP tool
# ---------------------------------------------------------------------------


def test_emit_gold_to_mcp_binding() -> None:
    p = emit_gold_to_mcp(
        gold_qualified_name="apex.rc.gold.vw_agent_cold_chain",
        mcp_tool_qualified_name="apex.rc.mcp.scml.get_cold_chain_status",
        mcp_tool_version="1.2.0",
        mcp_server="scml-mcp",
    )
    assert p.type_name == "apex_gold_to_mcp"
    assert p.outputs[0].type_name == "apex_mcp_tool"
    assert p.attributes["mcp_tool_version"] == "1.2.0"
    assert p.attributes["mcp_server"] == "scml-mcp"


# ---------------------------------------------------------------------------
# Subtask 13.2.5 — MCP → Agent → Orchestration → Audit
# ---------------------------------------------------------------------------


def test_emit_mcp_to_agent_binds_manifest_sha() -> None:
    p = emit_mcp_to_agent(
        mcp_tool_qualified_name="apex.rc.mcp.scml.get_lot_trace",
        agent_qualified_name="apex.rc.agents.recall_response",
        agent_manifest_sha="a1b2c3d4e5f6",
    )
    assert p.type_name == "apex_mcp_to_agent"
    assert p.attributes["agent_manifest_sha"] == "a1b2c3d4e5f6"
    assert p.inputs[0].type_name == "apex_mcp_tool"
    assert p.outputs[0].type_name == "apex_agent"


def test_emit_agent_to_orchestration_with_archetype() -> None:
    p = emit_agent_to_orchestration(
        agent_qualified_name="apex.rc.agents.cold_chain_response",
        orchestration_qualified_name="apex.rc.orch.cold_chain_excursion_response",
        orchestration_manifest_sha="d4e5f6a7b8c9",
        archetype_id="F1-continuous-monitor-hitl-alert",
    )
    assert p.attributes["archetype_id"] == "F1-continuous-monitor-hitl-alert"
    assert p.outputs[0].type_name == "apex_orchestration"


def test_emit_orchestration_to_audit_carries_three_versions() -> None:
    p = emit_orchestration_to_audit(
        orchestration_qualified_name="apex.rc.orch.cold_chain_excursion_response",
        audit_row_qualified_name="apex.audit.dec-042",
        trace_id="trace-001",
        decision_id="dec-042",
        manifest_version="mfst-sha",
        policy_version="pol-sha",
        prompt_version="prm-sha",
        hitl_status="approved",
    )
    assert p.type_name == "apex_orchestration_to_audit"
    assert p.outputs[0].type_name == "apex_audit_row"
    # Three-version rule
    assert p.attributes["manifest_version"] == "mfst-sha"
    assert p.attributes["policy_version"] == "pol-sha"
    assert p.attributes["prompt_version"] == "prm-sha"
    assert p.attributes["trace_id"] == "trace-001"
    assert p.attributes["decision_id"] == "dec-042"
    assert p.attributes["hitl_status"] == "approved"


def test_emit_orchestration_to_audit_hitl_optional() -> None:
    p = emit_orchestration_to_audit(
        orchestration_qualified_name="o",
        audit_row_qualified_name="a",
        trace_id="t",
        decision_id="d",
        manifest_version="m",
        policy_version="p",
        prompt_version="pr",
    )
    assert "hitl_status" not in p.attributes


# ---------------------------------------------------------------------------
# Batch + typedef bootstrap
# ---------------------------------------------------------------------------


def test_emit_lineage_batch_shape() -> None:
    p1 = emit_sor_to_bronze(
        sor_qualified_name="s",
        sor_type_name="t",
        bronze_qualified_name="b",
        pipeline_run_id="pr",
    )
    p2 = emit_bronze_to_silver(
        bronze_qualified_name="b",
        silver_qualified_name="si",
        notebook_url="u",
        commit_sha="c",
    )
    payload = emit_lineage_batch([p1, p2])
    assert list(payload.keys()) == ["entities"]
    assert len(payload["entities"]) == 2
    # Each entity has Atlas shape
    for e in payload["entities"]:
        assert "typeName" in e
        assert "attributes" in e
        assert "qualifiedName" in e["attributes"]
        assert "inputs" in e["attributes"]
        assert "outputs" in e["attributes"]


def test_emit_process_typedefs_returns_seven_hops() -> None:
    payload = emit_process_typedefs()
    assert len(payload["entityDefs"]) == len(PROCESS_TYPES)
    assert len(payload["entityDefs"]) == 7
    names = {d["name"] for d in payload["entityDefs"]}
    assert names == set(PROCESS_TYPES.values())
    # Every entity def subTypes Process
    for d in payload["entityDefs"]:
        assert d["superTypes"] == ["Process"]


# ---------------------------------------------------------------------------
# Declarative spec loader + end-to-end Cold Chain fixture
# ---------------------------------------------------------------------------


def test_emit_from_spec_cold_chain_fixture_seven_hops() -> None:
    doc = load_lineage_spec(FIXTURES / "lineage_cold_chain.yaml")
    processes = emit_from_spec(doc)
    assert len(processes) == 7
    type_names = [p.type_name for p in processes]
    # In declared order — the seven canonical hops
    assert type_names == [
        "apex_sor_to_bronze",
        "apex_bronze_to_silver",
        "apex_silver_to_gold",
        "apex_gold_to_mcp",
        "apex_mcp_to_agent",
        "apex_agent_to_orchestration",
        "apex_orchestration_to_audit",
    ]


def test_emit_from_spec_cold_chain_audit_row_trace_id() -> None:
    doc = load_lineage_spec(FIXTURES / "lineage_cold_chain.yaml")
    processes = emit_from_spec(doc)
    audit_proc = processes[-1]
    assert audit_proc.attributes["trace_id"] == "trace-20260422-0635-cc-001"
    assert audit_proc.attributes["hitl_status"] == "approved"


def test_emit_from_spec_rejects_wrong_kind() -> None:
    with pytest.raises(ValueError, match="kind='schema'"):
        emit_from_spec({"kind": "schema", "edges": []})


def test_emit_from_spec_rejects_unknown_hop() -> None:
    with pytest.raises(ValueError, match="unknown hop"):
        emit_from_spec(
            {
                "kind": "lineage",
                "edges": [{"hop": "bronze_to_mars"}],
            }
        )


def test_emit_from_spec_rejects_missing_required_kwarg() -> None:
    with pytest.raises(ValueError, match="hop=sor_to_bronze"):
        emit_from_spec(
            {
                "kind": "lineage",
                "edges": [
                    {
                        "hop": "sor_to_bronze",
                        # missing sor_qualified_name etc
                    }
                ],
            }
        )


def test_emit_from_spec_rejects_non_mapping_edge() -> None:
    with pytest.raises(ValueError, match="not a mapping"):
        emit_from_spec(
            {
                "kind": "lineage",
                "edges": ["not a dict"],
            }
        )


def test_emit_from_spec_rejects_missing_edges_key() -> None:
    with pytest.raises(ValueError, match="'edges' list"):
        emit_from_spec({"kind": "lineage"})


def test_load_lineage_spec_rejects_non_mapping(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("- list\n- not mapping\n", encoding="utf-8")
    with pytest.raises(ValueError, match="must parse to a mapping"):
        load_lineage_spec(bad)


# ---------------------------------------------------------------------------
# Idempotency
# ---------------------------------------------------------------------------


def test_emit_from_spec_is_idempotent() -> None:
    doc = load_lineage_spec(FIXTURES / "lineage_cold_chain.yaml")
    first = [p.to_atlas() for p in emit_from_spec(doc)]
    second = [p.to_atlas() for p in emit_from_spec(doc)]
    assert first == second


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_emit_lineage_stdout() -> None:
    result = runner.invoke(
        purview_app,
        ["emit-lineage", str(FIXTURES / "lineage_cold_chain.yaml")],
    )
    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert len(payload["entities"]) == 7


def test_cli_emit_lineage_to_file(tmp_path: Path) -> None:
    out = tmp_path / "lineage.json"
    result = runner.invoke(
        purview_app,
        [
            "emit-lineage",
            str(FIXTURES / "lineage_cold_chain.yaml"),
            "--output",
            str(out),
        ],
    )
    assert result.exit_code == 0
    assert out.exists()
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert len(payload["entities"]) == 7


def test_cli_emit_process_typedefs_stdout() -> None:
    result = runner.invoke(purview_app, ["emit-process-typedefs"])
    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert len(payload["entityDefs"]) == 7


# ---------------------------------------------------------------------------
# Conformance — JSON round-trip for lineage payloads
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_lineage_payload_json_round_trip() -> None:
    doc = load_lineage_spec(FIXTURES / "lineage_cold_chain.yaml")
    processes = emit_from_spec(doc)
    payload = emit_lineage_batch(processes)
    assert json.loads(json.dumps(payload)) == payload


@pytest.mark.conformance
def test_process_typedefs_json_round_trip() -> None:
    payload = emit_process_typedefs()
    assert json.loads(json.dumps(payload)) == payload
