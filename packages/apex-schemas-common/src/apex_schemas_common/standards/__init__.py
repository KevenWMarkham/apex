"""APEX standards registry — industry-standard bindings (Pattern A + registry).

Implements `Industry-Standards-Incorporation-Plan.md` §5.

Public surface:

- :class:`StandardRef` — metadata marker attached via ``Annotated[...]``.
- :class:`StandardSpec` — Pydantic model describing a registered standard.
- :data:`STANDARDS` — registry of known standards.
- :func:`lookup`, :func:`audit_model` — registry helpers.
- Identifier types: :data:`GTIN14`, :data:`GTIN13`, :data:`SSCC`, :data:`GLN`,
  :data:`LoincCode`, :data:`Icd10Code`, :data:`NdcCode`, :data:`Eidr`, …
"""

from apex_schemas_common.standards.catalog import (
    CatalogDriftReport,
    CatalogIssue,
    catalog_path,
    check_catalog_drift,
    emit_catalog,
    load_catalog,
    write_catalog,
)
from apex_schemas_common.standards.introspect import audit_model, find_standard_refs
from apex_schemas_common.standards.registry import (
    STANDARDS,
    StandardSpec,
    StandardType,
    list_standards,
    lookup,
)
from apex_schemas_common.standards.types import (
    GLN,
    GTIN8,
    GTIN12,
    GTIN13,
    GTIN14,
    SSCC,
    CptCode,
    Eidr,
    HcpcsCode,
    Icd10Code,
    LoincCode,
    NdcCode,
    RxNormConceptId,
    SnomedCtConceptId,
    StandardRef,
)

__all__ = [
    "GLN",
    "GTIN8",
    "GTIN12",
    "GTIN13",
    "GTIN14",
    "SSCC",
    "STANDARDS",
    "CatalogDriftReport",
    "CatalogIssue",
    "CptCode",
    "Eidr",
    "HcpcsCode",
    "Icd10Code",
    "LoincCode",
    "NdcCode",
    "RxNormConceptId",
    "SnomedCtConceptId",
    "StandardRef",
    "StandardSpec",
    "StandardType",
    "audit_model",
    "catalog_path",
    "check_catalog_drift",
    "emit_catalog",
    "find_standard_refs",
    "list_standards",
    "load_catalog",
    "lookup",
    "write_catalog",
]
