"""Purview lineage edge emitter.

In Apache Atlas / Microsoft Purview, lineage is modeled with **Process**
entities. A Process has ``inputs`` and ``outputs`` arrays referencing
other entities by ``qualifiedName``. The Process entity itself *is* the
lineage edge.

APEX tracks lineage across **seven hops** — the canonical data-and-decision
path for every agent decision:

.. code-block:: text

    SOR → Bronze → Silver → Gold → MCP tool → Agent → Orchestration → Audit row

Each hop has its own Process typeName, its own canonical attributes, and
its own Atlas payload shape. Sprint 13 Task 13.2 subtasks 1–5 cover:

- 13.2.1: SOR → Bronze (with pipeline run ID)
- 13.2.2: Bronze → Silver (with notebook URL + commit SHA)
- 13.2.3: Silver → Gold (with SQL SHA)
- 13.2.4: Gold → MCP tool asset
- 13.2.5: MCP → Agent → Orchestration → Audit row

This module exposes per-hop ``emit_*`` functions and a batch
:func:`emit_lineage_batch` helper that assembles a single
``POST /api/atlas/v2/entity/bulk`` body from a list of Process entities.

A declarative ``kind: lineage`` YAML spec is also supported via
:func:`emit_from_spec` (CLI: ``apex purview emit-lineage <spec.yaml>``).

Cross-reference: Sellers Guide §6.10 (audit row), §8.8 (lineage graph
construction), §9.11.4 (Bronze → Silver → Gold → MCP → Agent path).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Entity reference
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class EntityRef:
    """Atlas entity reference by ``qualifiedName``.

    Every lineage edge references inputs and outputs by qualified name,
    not by GUID. The Purview / Atlas server resolves qualified name to
    GUID at ingestion time.
    """

    type_name: str
    qualified_name: str

    def to_atlas(self) -> dict[str, Any]:
        return {
            "typeName": self.type_name,
            "uniqueAttributes": {"qualifiedName": self.qualified_name},
        }


# ---------------------------------------------------------------------------
# Process entity (lineage edge)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LineageProcess:
    """A single Atlas Process entity — one lineage edge.

    Atlas models lineage through Process entities with inputs and outputs
    arrays. This dataclass is an immutable descriptor that serializes to
    the Atlas v2 ``Process`` entity payload shape.
    """

    type_name: str
    """Process typeName. APEX uses ``apex_*`` prefixed process types so
    lineage is queryable by hop (e.g., ``apex_bronze_to_silver``)."""

    qualified_name: str
    """Globally unique process identifier. Convention:
    ``apex.{practice}.{family}.{hop}.{from_entity}__{to_entity}``."""

    display_name: str
    """Human-readable label shown in Purview UI."""

    inputs: tuple[EntityRef, ...]
    outputs: tuple[EntityRef, ...]

    attributes: dict[str, Any] = field(default_factory=dict)
    """Hop-specific attributes: pipeline_run_id, notebook_url, commit_sha,
    sql_sha, tool_version, trace_id, etc."""

    def to_atlas(self) -> dict[str, Any]:
        """Return the Atlas v2 entity body for this Process."""
        return {
            "typeName": self.type_name,
            "attributes": {
                "qualifiedName": self.qualified_name,
                "name": self.display_name,
                "inputs": [i.to_atlas() for i in self.inputs],
                "outputs": [o.to_atlas() for o in self.outputs],
                **self.attributes,
            },
        }


# ---------------------------------------------------------------------------
# Process typeNames — one per canonical hop
# ---------------------------------------------------------------------------

PROCESS_TYPES: dict[str, str] = {
    "sor_to_bronze": "apex_sor_to_bronze",
    "bronze_to_silver": "apex_bronze_to_silver",
    "silver_to_gold": "apex_silver_to_gold",
    "gold_to_mcp": "apex_gold_to_mcp",
    "mcp_to_agent": "apex_mcp_to_agent",
    "agent_to_orchestration": "apex_agent_to_orchestration",
    "orchestration_to_audit": "apex_orchestration_to_audit",
}


# ---------------------------------------------------------------------------
# Per-hop emit functions
# ---------------------------------------------------------------------------


def emit_sor_to_bronze(
    *,
    sor_qualified_name: str,
    sor_type_name: str,
    bronze_qualified_name: str,
    pipeline_run_id: str,
    ingest_ts: str | None = None,
    ingest_latency_ms: int | None = None,
) -> LineageProcess:
    """Subtask 13.2.1 — SOR → Bronze lineage edge.

    Represents one ingest-pipeline run that moves data from a Source of
    Record into Fabric Bronze. The ``pipeline_run_id`` is the durable
    identifier a forensic investigator uses to replay the ingest from
    Data Factory / Azure Synapse Pipelines activity logs.
    """
    attrs: dict[str, Any] = {"pipeline_run_id": pipeline_run_id}
    if ingest_ts is not None:
        attrs["ingest_ts"] = ingest_ts
    if ingest_latency_ms is not None:
        attrs["ingest_latency_ms"] = ingest_latency_ms

    return LineageProcess(
        type_name=PROCESS_TYPES["sor_to_bronze"],
        qualified_name=f"{bronze_qualified_name}@ingest.{pipeline_run_id}",
        display_name=f"SOR→Bronze: {sor_qualified_name} → {bronze_qualified_name}",
        inputs=(EntityRef(sor_type_name, sor_qualified_name),),
        outputs=(EntityRef("apex_bronze_table", bronze_qualified_name),),
        attributes=attrs,
    )


def emit_bronze_to_silver(
    *,
    bronze_qualified_name: str,
    silver_qualified_name: str,
    notebook_url: str,
    commit_sha: str,
    transform_version: str | None = None,
) -> LineageProcess:
    """Subtask 13.2.2 — Bronze → Silver lineage edge.

    Represents the Spark / PySpark transform that canonicalizes Bronze
    rows into a Silver table against a canonical schema (SCML, PatientML,
    etc.). The ``commit_sha`` pins the exact notebook code that produced
    the Silver row.
    """
    attrs: dict[str, Any] = {
        "notebook_url": notebook_url,
        "commit_sha": commit_sha,
    }
    if transform_version is not None:
        attrs["transform_version"] = transform_version

    return LineageProcess(
        type_name=PROCESS_TYPES["bronze_to_silver"],
        qualified_name=f"{silver_qualified_name}@transform.{commit_sha[:12]}",
        display_name=f"Bronze→Silver: {bronze_qualified_name} → {silver_qualified_name}",
        inputs=(EntityRef("apex_bronze_table", bronze_qualified_name),),
        outputs=(EntityRef("apex_silver_table", silver_qualified_name),),
        attributes=attrs,
    )


def emit_silver_to_gold(
    *,
    silver_qualified_names: list[str] | tuple[str, ...],
    gold_qualified_name: str,
    sql_sha: str,
    view_definition_url: str | None = None,
    gold_type: str = "direct_lake_view",
) -> LineageProcess:
    """Subtask 13.2.3 — Silver → Gold lineage edge.

    Represents the SQL / KQL that joins one or more Silver tables into a
    Gold view for agent consumption. The ``sql_sha`` pins the exact view
    definition. ``gold_type`` is one of ``direct_lake_view``,
    ``warehouse_view``, ``kql_function``.
    """
    attrs: dict[str, Any] = {
        "sql_sha": sql_sha,
        "gold_type": gold_type,
    }
    if view_definition_url is not None:
        attrs["view_definition_url"] = view_definition_url

    inputs = tuple(
        EntityRef("apex_silver_table", qn) for qn in silver_qualified_names
    )

    return LineageProcess(
        type_name=PROCESS_TYPES["silver_to_gold"],
        qualified_name=f"{gold_qualified_name}@sql.{sql_sha[:12]}",
        display_name=f"Silver→Gold: {len(silver_qualified_names)} Silver(s) → {gold_qualified_name}",
        inputs=inputs,
        outputs=(EntityRef("apex_gold_view", gold_qualified_name),),
        attributes=attrs,
    )


def emit_gold_to_mcp(
    *,
    gold_qualified_name: str,
    mcp_tool_qualified_name: str,
    mcp_tool_version: str,
    mcp_server: str,
) -> LineageProcess:
    """Subtask 13.2.4 — Gold → MCP tool lineage edge.

    Binds an MCP tool to the specific Gold view it exposes. Every MCP
    tool in the APEX catalog points at exactly one Gold view; the binding
    is what lets auditors walk from an agent's tool call back to the
    Silver → Gold → Source rows it actually consumed.
    """
    return LineageProcess(
        type_name=PROCESS_TYPES["gold_to_mcp"],
        qualified_name=f"{mcp_tool_qualified_name}@bind.{mcp_tool_version}",
        display_name=f"Gold→MCP: {gold_qualified_name} → {mcp_tool_qualified_name}",
        inputs=(EntityRef("apex_gold_view", gold_qualified_name),),
        outputs=(EntityRef("apex_mcp_tool", mcp_tool_qualified_name),),
        attributes={
            "mcp_tool_version": mcp_tool_version,
            "mcp_server": mcp_server,
        },
    )


def emit_mcp_to_agent(
    *,
    mcp_tool_qualified_name: str,
    agent_qualified_name: str,
    agent_manifest_sha: str,
) -> LineageProcess:
    """Subtask 13.2.5a — MCP tool → Agent lineage edge.

    Represents the agent's authorization to call the MCP tool. The
    ``agent_manifest_sha`` pins the exact manifest that declared this
    tool in the agent's allow-list — part of the three-version rule
    per §6.10.7.
    """
    return LineageProcess(
        type_name=PROCESS_TYPES["mcp_to_agent"],
        qualified_name=f"{agent_qualified_name}@binds.{mcp_tool_qualified_name}",
        display_name=f"MCP→Agent: {mcp_tool_qualified_name} → {agent_qualified_name}",
        inputs=(EntityRef("apex_mcp_tool", mcp_tool_qualified_name),),
        outputs=(EntityRef("apex_agent", agent_qualified_name),),
        attributes={"agent_manifest_sha": agent_manifest_sha},
    )


def emit_agent_to_orchestration(
    *,
    agent_qualified_name: str,
    orchestration_qualified_name: str,
    orchestration_manifest_sha: str,
    archetype_id: str | None = None,
) -> LineageProcess:
    """Subtask 13.2.5b — Agent → Orchestration lineage edge.

    Represents the agent's participation in an orchestration. One agent
    may participate in many orchestrations; one orchestration composes
    many agents. This edge is emitted at orchestration registration time,
    not per-run (per-run emission would be the composite-row edge below).
    """
    attrs: dict[str, Any] = {
        "orchestration_manifest_sha": orchestration_manifest_sha,
    }
    if archetype_id is not None:
        attrs["archetype_id"] = archetype_id

    return LineageProcess(
        type_name=PROCESS_TYPES["agent_to_orchestration"],
        qualified_name=f"{orchestration_qualified_name}@composes.{agent_qualified_name}",
        display_name=f"Agent→Orchestration: {agent_qualified_name} → {orchestration_qualified_name}",
        inputs=(EntityRef("apex_agent", agent_qualified_name),),
        outputs=(EntityRef("apex_orchestration", orchestration_qualified_name),),
        attributes=attrs,
    )


def emit_orchestration_to_audit(
    *,
    orchestration_qualified_name: str,
    audit_row_qualified_name: str,
    trace_id: str,
    decision_id: str,
    manifest_version: str,
    policy_version: str,
    prompt_version: str,
    hitl_status: str | None = None,
) -> LineageProcess:
    """Subtask 13.2.5c — Orchestration → Audit row lineage edge.

    Represents one orchestration run producing one audit row. Carries the
    three-version stamps from §6.10.7 plus the ``trace_id`` that binds
    every participating agent's audit row into one forensic thread.

    Args:
        orchestration_qualified_name: The orchestration being traced.
        audit_row_qualified_name: Typically ``apex.audit.{decision_id}``.
        trace_id: Shared trace identifier across the orchestration's hops.
        decision_id: Unique identifier for this specific decision.
        manifest_version: Git SHA of the orchestration manifest in effect.
        policy_version: Git SHA of the policy bundle in effect.
        prompt_version: Git SHA of the system-prompt bundle in effect.
        hitl_status: Optional — one of {none, pending, approved, modified,
            rejected, overridden}.
    """
    attrs: dict[str, Any] = {
        "trace_id": trace_id,
        "decision_id": decision_id,
        "manifest_version": manifest_version,
        "policy_version": policy_version,
        "prompt_version": prompt_version,
    }
    if hitl_status is not None:
        attrs["hitl_status"] = hitl_status

    return LineageProcess(
        type_name=PROCESS_TYPES["orchestration_to_audit"],
        qualified_name=f"{audit_row_qualified_name}@trace.{trace_id}",
        display_name=f"Orchestration→Audit: {orchestration_qualified_name} → {audit_row_qualified_name}",
        inputs=(EntityRef("apex_orchestration", orchestration_qualified_name),),
        outputs=(EntityRef("apex_audit_row", audit_row_qualified_name),),
        attributes=attrs,
    )


# ---------------------------------------------------------------------------
# Batch emission
# ---------------------------------------------------------------------------


def emit_lineage_batch(edges: list[LineageProcess]) -> dict[str, Any]:
    """Assemble multiple Process entities into a single Atlas bulk body.

    Shape: ``POST /api/atlas/v2/entity/bulk`` accepts
    ``{"entities": [...]}`` containing any number of Atlas entities,
    including Process entities that represent lineage edges.

    Args:
        edges: List of :class:`LineageProcess` to emit.

    Returns:
        Atlas-v2 bulk-body dict ready for POST.
    """
    return {"entities": [e.to_atlas() for e in edges]}


# ---------------------------------------------------------------------------
# Process type definitions (one-time bootstrap)
# ---------------------------------------------------------------------------


def emit_process_typedefs() -> dict[str, Any]:
    """Emit Atlas v2 type-def payload for every APEX lineage Process type.

    Called once at Purview bootstrap time to register the seven custom
    Process types APEX uses. Subsequent lineage POSTs refer to these
    types by name.
    """
    process_defs: list[dict[str, Any]] = []
    for hop, type_name in sorted(PROCESS_TYPES.items()):
        process_defs.append(
            {
                "category": "ENTITY",
                "name": type_name,
                "description": f"APEX {hop.replace('_', ' → ')} lineage process.",
                "typeVersion": "1.0",
                "superTypes": ["Process"],
                "attributeDefs": [
                    {
                        "name": "qualifiedName",
                        "typeName": "string",
                        "isOptional": False,
                        "cardinality": "SINGLE",
                        "isUnique": True,
                        "isIndexable": True,
                    }
                ],
            }
        )

    return {
        "enumDefs": [],
        "structDefs": [],
        "classificationDefs": [],
        "entityDefs": process_defs,
        "relationshipDefs": [],
        "businessMetadataDefs": [],
    }


# ---------------------------------------------------------------------------
# Declarative spec loader
# ---------------------------------------------------------------------------


_HOP_DISPATCH = {
    "sor_to_bronze": emit_sor_to_bronze,
    "bronze_to_silver": emit_bronze_to_silver,
    "silver_to_gold": emit_silver_to_gold,
    "gold_to_mcp": emit_gold_to_mcp,
    "mcp_to_agent": emit_mcp_to_agent,
    "agent_to_orchestration": emit_agent_to_orchestration,
    "orchestration_to_audit": emit_orchestration_to_audit,
}


def emit_from_spec(spec: dict[str, Any]) -> list[LineageProcess]:
    """Emit lineage processes from a declarative ``kind: lineage`` spec.

    Spec shape:

    .. code-block:: yaml

        kind: lineage
        version: 1.0
        edges:
          - hop: sor_to_bronze
            sor_qualified_name: oracle.pos.sku_master
            sor_type_name: oracle_table
            bronze_qualified_name: apex.rc.bronze.sku
            pipeline_run_id: pipe-2026-04-22-001
          - hop: bronze_to_silver
            bronze_qualified_name: apex.rc.bronze.sku
            silver_qualified_name: apex.rc.silver.scml.sku
            notebook_url: adf://pipelines/bronze-to-silver-scml/v1.2.3
            commit_sha: 7f3a9b2c4d5e6f
          ...

    Every edge entry has a ``hop`` key naming one of the seven canonical
    hops; the remaining keys are keyword-arguments forwarded to the
    corresponding ``emit_*`` function.
    """
    if spec.get("kind") != "lineage":
        raise ValueError(
            f"Expected kind='lineage', got kind={spec.get('kind')!r}."
        )

    edges_raw = spec.get("edges")
    if not isinstance(edges_raw, list):
        raise ValueError("Spec must have an 'edges' list.")

    results: list[LineageProcess] = []
    for i, edge in enumerate(edges_raw):
        if not isinstance(edge, dict):
            raise ValueError(f"Edge #{i} is not a mapping.")
        hop = edge.get("hop")
        if hop not in _HOP_DISPATCH:
            raise ValueError(
                f"Edge #{i}: unknown hop={hop!r}. "
                f"Allowed: {sorted(_HOP_DISPATCH.keys())}"
            )
        emitter = _HOP_DISPATCH[hop]
        kwargs = {k: v for k, v in edge.items() if k != "hop"}
        try:
            results.append(emitter(**kwargs))
        except TypeError as exc:
            raise ValueError(
                f"Edge #{i} (hop={hop}): {exc}. "
                f"Keys provided: {sorted(kwargs.keys())}"
            ) from exc

    return results


def load_lineage_spec(path: str | Path) -> dict[str, Any]:
    """Parse a lineage YAML spec from disk."""
    with Path(path).open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValueError(f"Lineage spec {path} must parse to a mapping.")
    return data
