"""Tests for apex_scenarios.foundation + .fusion — Sprint 28 Tasks 28.2 + 28.3."""

from __future__ import annotations

import pytest

from apex_scenarios import (
    FOUNDATION_CATALOG,
    FOUNDATION_CLASSES,
    FUSION_CATALOG,
    EffortRollup,
    FoundationBlock,
    FusionMesh,
    PRACTICE_CODES,
    all_foundation_blocks,
    all_fusion_meshes,
    blocks_unblocking_scenario,
    dependency_graph_edges,
    effort_rollup,
    foundation_blocks_by_class,
    fusion_meshes_by_practice,
    fusion_per_practice_counts,
    get_foundation_block,
    get_fusion_mesh,
    mesh_by_w2_service_code,
    transitive_prerequisites,
)


# ---------------------------------------------------------------------------
# Foundation catalog — Task 28.2
# ---------------------------------------------------------------------------


def test_foundation_catalog_meets_minimum_count() -> None:
    """Sprint 28 §28.2.1 requires ~40 blocks."""
    assert len(all_foundation_blocks()) >= 40


def test_foundation_classes_complete() -> None:
    """Five canonical classes per §28.2.1: schema, ledger, mcp, hitl, policy."""
    assert set(FOUNDATION_CLASSES) == {"schema", "ledger", "mcp", "hitl", "policy"}


def test_every_block_has_required_fields() -> None:
    for b in all_foundation_blocks():
        assert b.name
        assert b.cls in FOUNDATION_CLASSES
        assert b.description
        assert b.effort_story_points >= 0
        assert b.effort_calendar_weeks >= 0


def test_every_class_has_at_least_one_block() -> None:
    for cls in FOUNDATION_CLASSES:
        assert foundation_blocks_by_class(cls), f"class {cls!r} has no blocks"


def test_blocks_by_class_rejects_unknown() -> None:
    with pytest.raises(ValueError, match="unknown foundation class"):
        foundation_blocks_by_class("nonsense")  # type: ignore[arg-type]


def test_get_block_lookup() -> None:
    b = get_foundation_block("scml-bronze-silver")
    assert b is not None
    assert b.cls == "schema"
    assert "SCML" in b.schemas_touched
    assert get_foundation_block("does-not-exist") is None


def test_blocks_unblocking_scenario_returns_correct_set() -> None:
    """RC-E2E-04 (cold-chain) should be unblocked by SCML + audit-row + FSMA-204 ledger."""
    blocks = blocks_unblocking_scenario("RC-E2E-04")
    names = {b.name for b in blocks}
    assert "scml-bronze-silver" in names
    assert "fsma-204-ledger" in names


def test_blocks_unblocking_scenario_handles_unknown_code() -> None:
    blocks = blocks_unblocking_scenario("NOPE-X-99")
    assert blocks == ()


def test_transitive_prerequisites_includes_self_and_chain() -> None:
    """fsma-204-ledger depends on scml-bronze-silver + audit-row-pipeline."""
    chain = transitive_prerequisites("fsma-204-ledger")
    names = [b.name for b in chain]
    assert "fsma-204-ledger" in names
    assert "scml-bronze-silver" in names
    assert "audit-row-pipeline" in names
    # The block itself should appear AFTER its prereqs (topological)
    target_idx = names.index("fsma-204-ledger")
    for p in ("scml-bronze-silver", "audit-row-pipeline"):
        assert names.index(p) < target_idx


def test_transitive_prerequisites_unknown_block_raises() -> None:
    with pytest.raises(KeyError, match="unknown foundation block"):
        transitive_prerequisites("nope")


def test_no_prereq_dangles() -> None:
    """Every prerequisite name must resolve to an actual block."""
    block_names = {b.name for b in all_foundation_blocks()}
    for b in all_foundation_blocks():
        for p in b.prerequisites:
            assert p in block_names, (
                f"block {b.name!r} declares dangling prerequisite {p!r}"
            )


def test_dependency_graph_edges_match_prerequisites() -> None:
    """Every (prereq, block) edge in the graph corresponds to a real prerequisite."""
    edges = dependency_graph_edges()
    for prereq, block_name in edges:
        b = get_foundation_block(block_name)
        assert b is not None
        assert prereq in b.prerequisites


def test_effort_rollup_sums_correctly() -> None:
    """SoW-quotable rollup — story points + calendar weeks sum across selection."""
    selection = [
        get_foundation_block("scml-bronze-silver"),
        get_foundation_block("audit-row-pipeline"),
        get_foundation_block("fsma-204-ledger"),
    ]
    selection = [b for b in selection if b is not None]
    rollup = effort_rollup(selection)
    assert rollup.selected_count == 3
    assert rollup.total_story_points == 8 + 8 + 5  # = 21
    assert rollup.total_calendar_weeks == 5.0  # 2.0 + 2.0 + 1.0


def test_effort_rollup_parallelizes_along_critical_path() -> None:
    """Parallelizable wall-clock = longest prerequisite chain in selection."""
    selection = [
        get_foundation_block("scml-bronze-silver"),       # 2.0w, no deps
        get_foundation_block("audit-row-pipeline"),       # 2.0w, no deps
        get_foundation_block("fsma-204-ledger"),          # 1.0w, depends on both above
    ]
    selection = [b for b in selection if b is not None]
    rollup = effort_rollup(selection)
    # Sequential: 5.0w. Parallel: max(2.0, 2.0) + 1.0 = 3.0w
    assert rollup.parallelizable_calendar_weeks == 3.0
    assert rollup.total_calendar_weeks == 5.0


def test_effort_rollup_empty_selection() -> None:
    rollup = effort_rollup([])
    assert rollup.selected_count == 0
    assert rollup.total_story_points == 0
    assert rollup.total_calendar_weeks == 0
    assert rollup.parallelizable_calendar_weeks == 0


def test_effort_rollup_returns_dataclass_with_class_breakdown() -> None:
    selection = list(all_foundation_blocks())
    rollup = effort_rollup(selection)
    assert isinstance(rollup, EffortRollup)
    assert rollup.selected_count == len(FOUNDATION_CATALOG)
    # Every class represented
    for cls in FOUNDATION_CLASSES:
        assert rollup.by_class.get(cls, 0) > 0


# ---------------------------------------------------------------------------
# Fusion catalog — Task 28.3
# ---------------------------------------------------------------------------


def test_fusion_catalog_meets_count_band() -> None:
    """Sprint 28 §28.3.1 mandates 35-56 meshes total."""
    n = len(all_fusion_meshes())
    assert 35 <= n <= 56, f"expected 35-56 meshes, got {n}"


def test_every_practice_has_5_to_8_meshes() -> None:
    """Sprint 28 §28.3.1 — 5 to 8 meshes per Practice."""
    counts = fusion_per_practice_counts()
    practices_we_ship = {"rc", "hls", "er", "axle", "tmt", "th", "ice"}
    for p in practices_we_ship:
        n = counts.get(p, 0)
        assert 5 <= n <= 8, f"practice {p!r} has {n} meshes (expected 5-8)"


def test_every_mesh_has_required_fields() -> None:
    for m in all_fusion_meshes():
        assert m.mesh_id.startswith("mesh.")
        assert m.practice
        assert m.name
        assert m.description
        assert m.composed_outcomes  # at least one composed outcome
        assert m.orchestration_archetype.startswith("arch.")


def test_get_mesh_lookup() -> None:
    m = get_fusion_mesh("mesh.rc.perishables-economics")
    assert m is not None
    assert m.practice == "rc"
    assert "Cold-chain" in m.description or "cold-chain" in m.description.lower()
    assert get_fusion_mesh("mesh.does.not.exist") is None


def test_meshes_by_practice() -> None:
    rc_meshes = fusion_meshes_by_practice("RC")
    assert all(m.practice == "rc" for m in rc_meshes)
    assert len(rc_meshes) >= 5


def test_named_reference_meshes_present() -> None:
    """Sprint 28 §28.3.2 calls out three reference meshes by name."""
    names = {m.name for m in all_fusion_meshes()}
    assert "Perishables Economics Mesh" in names
    assert "Revenue-and-Outcomes Mesh" in names
    assert "Grid Reliability Mesh" in names


def test_mesh_by_w2_service_code_round_trips() -> None:
    """The cross-link helper finds meshes that include a given W2 service code."""
    meshes = mesh_by_w2_service_code("RC-E2E-04")
    mesh_ids = {m.mesh_id for m in meshes}
    assert "mesh.rc.perishables-economics" in mesh_ids


def test_mesh_by_w2_service_code_unknown_returns_empty() -> None:
    assert mesh_by_w2_service_code("NOPE-X-99") == ()


def test_every_mesh_orchestration_archetype_matches_format() -> None:
    """Sprint 19 archetype ids look like ``arch.<family>.<id>``."""
    for m in all_fusion_meshes():
        parts = m.orchestration_archetype.split(".")
        assert len(parts) == 3, f"mesh {m.mesh_id!r} archetype malformed: {m.orchestration_archetype!r}"
        assert parts[0] == "arch"


def test_per_practice_counts_sum_matches_total() -> None:
    counts = fusion_per_practice_counts()
    assert sum(counts.values()) == len(FUSION_CATALOG)


# ---------------------------------------------------------------------------
# Conformance — Sprint 28 acceptance markers
# ---------------------------------------------------------------------------


@pytest.mark.conformance
def test_conformance_foundation_catalog_min_40() -> None:
    """Sprint 28 §28.2.1 — at least 40 reusable W1 building blocks."""
    assert len(all_foundation_blocks()) >= 40


@pytest.mark.conformance
def test_conformance_foundation_five_classes_complete() -> None:
    """Sprint 28 §28.2.1 — schema / ledger / mcp / hitl / policy."""
    seen = {b.cls for b in all_foundation_blocks()}
    assert seen == set(FOUNDATION_CLASSES)


@pytest.mark.conformance
def test_conformance_fusion_total_in_band() -> None:
    """Sprint 28 §28.3.1 — 35-56 meshes total."""
    n = len(all_fusion_meshes())
    assert 35 <= n <= 56


@pytest.mark.conformance
def test_conformance_fusion_per_practice_in_band() -> None:
    """Sprint 28 §28.3.1 — 5-8 per Practice."""
    counts = fusion_per_practice_counts()
    for p in ("rc", "hls", "er", "axle", "tmt", "th", "ice"):
        assert 5 <= counts.get(p, 0) <= 8


@pytest.mark.conformance
def test_conformance_w1_to_w2_dependency_edges_resolve() -> None:
    """Sprint 28 §28.2.4 — every W1 block's `unblocks_w2_scenarios` is a list of valid service codes."""
    # Service-code shape: PRACTICE-Track-NN per Sprint 28 validators
    import re
    pattern = re.compile(r"^(RC|HLS|ER|AXLE|TMT|TH|ICE)-")
    for b in all_foundation_blocks():
        for sc in b.unblocks_w2_scenarios:
            assert pattern.match(sc), \
                f"block {b.name!r} unblocks malformed service code {sc!r}"
