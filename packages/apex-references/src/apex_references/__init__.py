"""APEX Reference Deployments — Sprint 18.

Five turnkey Wave-1 deployment blueprints, one per flagship Practice
anchor, composing Sprint 14 (capacity), Sprint 15 (adapters), Sprint 16
(agents), and Sprint 17 (services) into named, scoped, demo-able
engagements:

- ``big-box-store`` (RC) per Sellers Guide §16.13
- ``hospital`` (HLS) per Sellers Guide §10.9
- ``utility`` (ER) per Sellers Guide §11.9
- ``plant`` (AXLE) per Sellers Guide §12.9A
- ``airline`` (TH) per Sellers Guide §14.8
"""

from __future__ import annotations

from apex_references.framework import (
    PRACTICE_CODES,
    CatalogEntry,
    CatalogIssue,
    CatalogReport,
    KpiTarget,
    ReferenceSpec,
    SolutionArchitecture,
    TriggeringScenario,
    UseCase,
    Wave1Scope,
    catalogs_root,
    demo_scripts_root,
    get_reference,
    load_demo_script,
    load_reference_spec,
    scan_all_references,
    total_references,
    validate_references,
)

__all__ = [
    "PRACTICE_CODES",
    "CatalogEntry",
    "CatalogIssue",
    "CatalogReport",
    "KpiTarget",
    "ReferenceSpec",
    "SolutionArchitecture",
    "TriggeringScenario",
    "UseCase",
    "Wave1Scope",
    "catalogs_root",
    "demo_scripts_root",
    "get_reference",
    "load_demo_script",
    "load_reference_spec",
    "scan_all_references",
    "total_references",
    "validate_references",
]

__version__ = "0.1.0"
