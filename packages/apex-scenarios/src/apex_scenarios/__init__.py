"""APEX Scenario Library tooling — Sprint 28."""

from __future__ import annotations

from apex_scenarios.exporters import (
    CSV_COLUMNS,
    csv_filename,
    write_csv,
    write_csv_string,
)
from apex_scenarios.foundation import (
    CATALOG as FOUNDATION_CATALOG,
    FOUNDATION_CLASSES,
    EffortRollup,
    FoundationBlock,
    FoundationClass,
    all_blocks as all_foundation_blocks,
    blocks_by_class as foundation_blocks_by_class,
    blocks_unblocking_scenario,
    dependency_graph_edges,
    effort_rollup,
    get_block as get_foundation_block,
    transitive_prerequisites,
)
from apex_scenarios.fusion import (
    CATALOG as FUSION_CATALOG,
    FusionMesh,
    all_meshes as all_fusion_meshes,
    get_mesh as get_fusion_mesh,
    mesh_by_w2_service_code,
    meshes_by_practice as fusion_meshes_by_practice,
    per_practice_counts as fusion_per_practice_counts,
)
from apex_scenarios.library import (
    DEFAULT_FEATURED_PATH,
    DEFAULT_LIBRARY_PATH,
    ScenarioIndex,
    load_featured_chains,
    load_scenario_library,
    write_extended_library,
)
from apex_scenarios.models import (
    KPI_DIRECTIONS,
    PRACTICE_CODES,
    FeaturedChain,
    Scenario,
    ScenarioCompact,
    compact_to_extended,
    extended_to_compact,
)
from apex_scenarios.publication import (
    PRACTICE_LONG_NAME,
    publish_master_catalog,
    render_index_markdown,
    render_practice_markdown,
)
from apex_scenarios.validators import (
    ValidationIssue,
    ValidationReport,
    VersioningClassification,
    classify_library_bump,
    extract_agent_references,
    extract_kpi_name,
    validate_agent_references,
    validate_kpis,
    validate_service_codes,
    validate_wave_data_presence,
)

__all__ = [
    # models
    "KPI_DIRECTIONS",
    "PRACTICE_CODES",
    "FeaturedChain",
    "Scenario",
    "ScenarioCompact",
    "compact_to_extended",
    "extended_to_compact",
    # library
    "DEFAULT_FEATURED_PATH",
    "DEFAULT_LIBRARY_PATH",
    "ScenarioIndex",
    "load_featured_chains",
    "load_scenario_library",
    "write_extended_library",
    # exporters
    "CSV_COLUMNS",
    "csv_filename",
    "write_csv",
    "write_csv_string",
    # publication
    "PRACTICE_LONG_NAME",
    "publish_master_catalog",
    "render_index_markdown",
    "render_practice_markdown",
    # validators
    "ValidationIssue",
    "ValidationReport",
    "VersioningClassification",
    "classify_library_bump",
    "extract_agent_references",
    "extract_kpi_name",
    "validate_agent_references",
    "validate_kpis",
    "validate_service_codes",
    "validate_wave_data_presence",
    # foundation (Sprint 28 Task 28.2)
    "FOUNDATION_CATALOG",
    "FOUNDATION_CLASSES",
    "EffortRollup",
    "FoundationBlock",
    "FoundationClass",
    "all_foundation_blocks",
    "blocks_unblocking_scenario",
    "dependency_graph_edges",
    "effort_rollup",
    "foundation_blocks_by_class",
    "get_foundation_block",
    "transitive_prerequisites",
    # fusion (Sprint 28 Task 28.3)
    "FUSION_CATALOG",
    "FusionMesh",
    "all_fusion_meshes",
    "fusion_meshes_by_practice",
    "fusion_per_practice_counts",
    "get_fusion_mesh",
    "mesh_by_w2_service_code",
]

__version__ = "0.1.0"
