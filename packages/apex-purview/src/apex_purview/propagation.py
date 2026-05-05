"""Classification propagation validator — Sprint 13 Task 13.6.

Walks the lineage chain Silver → Gold → semantic model → Copilot →
agent output and verifies that every downstream node carries a
classification at least as restrictive as the most restrictive of its
inputs.

Subtasks
--------
- **13.6.1** — Silver → Gold → semantic model → Copilot → agent-output
  validator
- **13.6.2** — most-restrictive-label inheritance rule

Severity ordering
-----------------
APEX classifications are partially ordered by restrictiveness. The
ordering used here matches Sellers Guide §8.8.3 retention bands and
§9.11.7 / §10.10.7 / §11.10.7 DLP tables.

A propagation violation is a downstream node whose declared classification
is **less restrictive** than the most-restrictive of its inputs. The
validator returns a structured report listing every violation with the
inputs that triggered it.

Cross-reference: Sellers Guide §8.8.6 audit export — classifications are
part of every audit row's evidence package.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from apex_purview.classifications import APEX_CLASSIFICATIONS, _normalize_key


# ---------------------------------------------------------------------------
# Severity ordering (most-restrictive-wins)
# ---------------------------------------------------------------------------

#: Severity rank for each canonical APEX classification. Higher rank =
#: more restrictive. Equal rank means equally restrictive (e.g., PHI and
#: Genetic both at rank 8 — neither dominates the other; both must be
#: enforced).
CLASSIFICATION_SEVERITY: dict[str, int] = {
    "public": 0,
    "internal": 1,
    "member_only": 2,
    "trade_secret": 3,
    "cpni": 4,
    "pii": 5,
    "pci": 6,
    "phi": 7,
    "genetic": 8,
    "behavioral_health": 8,
    "export_controlled": 9,
    "restricted": 10,
}


def severity(classification: str) -> int:
    """Return the severity rank of a classification."""
    key = _normalize_key(classification)
    if key not in CLASSIFICATION_SEVERITY:
        raise ValueError(f"Unknown classification: {classification!r} (normalized {key!r}).")
    return CLASSIFICATION_SEVERITY[key]


def most_restrictive(classifications: list[str]) -> str:
    """Return the most-restrictive classification from a list."""
    if not classifications:
        raise ValueError("Cannot compute most-restrictive of empty list.")
    return max(classifications, key=lambda c: severity(c))


# ---------------------------------------------------------------------------
# Propagation graph + node model
# ---------------------------------------------------------------------------


@dataclass
class PropagationNode:
    """One node in the propagation graph.

    A node is any classification-bearing entity along the path:
    Silver table, Gold view, semantic-model column, Copilot surface,
    agent output. Inputs are upstream nodes; classification is the
    declared label at this node.
    """

    name: str
    """Qualified name (e.g., ``apex.rc.silver.scml.sku.unit_cost_token``)."""

    layer: str
    """One of ``silver``, ``gold``, ``semantic_model``, ``copilot``, ``agent_output``."""

    classification: str
    """Declared classification at this node."""

    inputs: list[str] = field(default_factory=list)
    """Names of upstream PropagationNodes."""


@dataclass
class PropagationViolation:
    """One propagation-rule violation."""

    node: str
    layer: str
    declared_classification: str
    required_classification: str
    """The most-restrictive classification of the inputs."""

    triggering_inputs: list[tuple[str, str]]
    """``(input_node_name, input_classification)`` pairs that exceed
    the declared severity."""


@dataclass
class PropagationReport:
    """Report from a propagation validation pass."""

    nodes_checked: int = 0
    violations: list[PropagationViolation] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.violations) == 0

    @property
    def exit_code(self) -> int:
        return 0 if self.ok else 1

    def summary(self) -> str:
        return (
            f"Classification propagation: {self.nodes_checked} nodes checked, "
            f"{len(self.violations)} violation(s)."
        )


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------


def validate_propagation(
    nodes: list[PropagationNode],
) -> PropagationReport:
    """Validate that every node respects most-restrictive inheritance.

    For each node with one or more inputs:

    1. Compute the most-restrictive classification across its inputs.
    2. If the node's declared classification is less restrictive than that,
       record a :class:`PropagationViolation`.

    Args:
        nodes: List of nodes — must be self-consistent (every name in
            ``inputs`` must appear as a ``PropagationNode.name`` in the list).

    Returns:
        :class:`PropagationReport` aggregating the result.

    Raises:
        ValueError: if inputs reference unknown node names, or any
            classification is unknown.
    """
    by_name = {n.name: n for n in nodes}

    # Validate references and classifications up front
    for n in nodes:
        if _normalize_key(n.classification) not in CLASSIFICATION_SEVERITY:
            raise ValueError(
                f"Node {n.name!r} carries unknown classification {n.classification!r}."
            )
        for inp in n.inputs:
            if inp not in by_name:
                raise ValueError(
                    f"Node {n.name!r} references unknown input {inp!r}."
                )

    report = PropagationReport()
    for n in nodes:
        report.nodes_checked += 1
        if not n.inputs:
            continue

        input_classifications = [by_name[i].classification for i in n.inputs]
        required = most_restrictive(input_classifications)

        if severity(n.classification) < severity(required):
            triggering: list[tuple[str, str]] = [
                (i, by_name[i].classification)
                for i in n.inputs
                if severity(by_name[i].classification) > severity(n.classification)
            ]
            report.violations.append(
                PropagationViolation(
                    node=n.name,
                    layer=n.layer,
                    declared_classification=n.classification,
                    required_classification=required,
                    triggering_inputs=triggering,
                )
            )

    return report


# ---------------------------------------------------------------------------
# Helper: build propagation graph from schema + lineage spec
# ---------------------------------------------------------------------------


def build_propagation_graph(
    schemas: list[dict],
    lineage_spec: dict | None = None,
) -> list[PropagationNode]:
    """Build a propagation graph from schema YAMLs and an optional lineage spec.

    Silver and Gold node classifications are read from the schemas. The
    lineage spec wires inputs (Silver → Gold edges only — Gold → MCP →
    Agent → Output edges are added by the caller via the runtime).

    Args:
        schemas: List of parsed APEX schema dicts. Each entity becomes
            a Silver node; each attribute with a classification also
            becomes a Silver attribute node.
        lineage_spec: Optional ``kind: lineage`` dict. Currently this
            helper consumes ``silver_to_gold`` edges to wire Gold
            inputs.

    Returns:
        List of :class:`PropagationNode` ready for :func:`validate_propagation`.
    """
    nodes: list[PropagationNode] = []

    for schema in schemas:
        practice = schema.get("practice", "unknown")
        family = schema.get("family", schema.get("name", "unknown"))
        for entity in schema.get("entities", []) or []:
            ent_name = entity.get("name", "unknown")
            ent_class = entity.get("classification", "internal")
            ent_qname = f"apex.{practice}.{family}.{ent_name}".lower()
            nodes.append(
                PropagationNode(
                    name=ent_qname,
                    layer="silver",
                    classification=ent_class,
                )
            )
            for attr in entity.get("attributes", []) or []:
                attr_name = attr.get("name", "unknown")
                attr_class = attr.get("classification", ent_class)
                attr_qname = f"{ent_qname}.{attr_name}".lower()
                nodes.append(
                    PropagationNode(
                        name=attr_qname,
                        layer="silver",
                        classification=attr_class,
                        inputs=[ent_qname],
                    )
                )

    if lineage_spec is not None:
        existing_names = {n.name for n in nodes}
        for edge in lineage_spec.get("edges", []) or []:
            if edge.get("hop") != "silver_to_gold":
                continue
            silver_qnames = edge.get("silver_qualified_names", [])
            gold_qname = edge.get("gold_qualified_name")
            if not gold_qname:
                continue

            # Auto-create placeholder Silver nodes for inputs not present
            # in the supplied schemas. Default classification is 'internal'
            # — explicit-schema declarations always override.
            for s in silver_qnames:
                if s not in existing_names:
                    nodes.append(
                        PropagationNode(
                            name=s,
                            layer="silver",
                            classification="internal",
                        )
                    )
                    existing_names.add(s)

            # Gold node inherits most-restrictive of its silver inputs
            silver_classes = [
                _find_classification(nodes, s) for s in silver_qnames
            ]
            gold_class = (
                most_restrictive(silver_classes) if silver_classes else "internal"
            )
            nodes.append(
                PropagationNode(
                    name=gold_qname,
                    layer="gold",
                    classification=gold_class,
                    inputs=list(silver_qnames),
                )
            )
            existing_names.add(gold_qname)

    return nodes


def _find_classification(nodes: list[PropagationNode], name: str) -> str:
    """Return the classification of a node by name, or ``internal`` if missing."""
    for n in nodes:
        if n.name == name:
            return n.classification
    return "internal"
