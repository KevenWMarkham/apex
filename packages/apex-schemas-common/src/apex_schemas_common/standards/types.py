"""StandardRef dataclass + canonical identifier types.

Each identifier type is an ``Annotated[str, StringConstraints(pattern=...), StandardRef(...)]``
so that Pydantic validates at construction time and Purview/DDL introspection
discovers the binding automatically.

:class:`StandardRef` references the :data:`STANDARDS` registry by ``standard_id``
so auditing is a direct dict lookup rather than fuzzy matching.

See ``Industry-Standards-Incorporation-Plan.md`` §4.1.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from pydantic import StringConstraints


@dataclass(frozen=True, slots=True)
class StandardRef:
    """Metadata marker: this attribute conforms to an external standard identifier."""

    standard_id: str
    """Registry key (must exist in :data:`STANDARDS`), e.g. ``"gs1-gtin"``."""

    identifier: str
    """Named sub-identifier within the standard, e.g. ``"GTIN-14"`` or ``"SSCC"``."""

    version: str
    """Version of the standard APEX is pinned to."""


# --- GS1 -----------------------------------------------------------------------

GTIN8 = Annotated[
    str,
    StringConstraints(pattern=r"^\d{8}$"),
    StandardRef("gs1-gtin", "GTIN-8", "BMS-1.34"),
]
GTIN12 = Annotated[
    str,
    StringConstraints(pattern=r"^\d{12}$"),
    StandardRef("gs1-gtin", "GTIN-12", "BMS-1.34"),
]
GTIN13 = Annotated[
    str,
    StringConstraints(pattern=r"^\d{13}$"),
    StandardRef("gs1-gtin", "GTIN-13", "BMS-1.34"),
]
GTIN14 = Annotated[
    str,
    StringConstraints(pattern=r"^\d{14}$"),
    StandardRef("gs1-gtin", "GTIN-14", "BMS-1.34"),
]
SSCC = Annotated[
    str,
    StringConstraints(pattern=r"^\d{18}$"),
    StandardRef("gs1-sscc", "SSCC", "BMS-1.34"),
]
GLN = Annotated[
    str,
    StringConstraints(pattern=r"^\d{13}$"),
    StandardRef("gs1-gln", "GLN", "BMS-1.34"),
]


# --- Clinical terminologies / codes --------------------------------------------

LoincCode = Annotated[
    str,
    StringConstraints(pattern=r"^\d{1,5}-\d$"),
    StandardRef("loinc", "LOINC-Code", "2.77"),
]

Icd10Code = Annotated[
    str,
    StringConstraints(pattern=r"^[A-TV-Z][0-9][0-9AB](\.[0-9A-Z]{1,4})?$"),
    StandardRef("icd-10-cm", "Icd10Code", "2026-Q1"),
]

NdcCode = Annotated[
    str,
    StringConstraints(pattern=r"^\d{4,5}-\d{3,4}-\d{1,2}$"),
    StandardRef("ndc", "NDC", "2026"),
]

CptCode = Annotated[
    str,
    StringConstraints(pattern=r"^\d{5}$"),
    StandardRef("cpt", "CPT", "2026"),
]

HcpcsCode = Annotated[
    str,
    StringConstraints(pattern=r"^[A-V]\d{4}$"),
    StandardRef("hcpcs", "HCPCS-L2", "2026"),
]

RxNormConceptId = Annotated[
    str,
    StringConstraints(pattern=r"^\d{1,7}$"),
    StandardRef("rxnorm", "RxCUI", "2026-01"),
]

SnomedCtConceptId = Annotated[
    str,
    StringConstraints(pattern=r"^\d{6,18}$"),
    StandardRef("snomed-ct", "SCTID", "2026-01"),
]


# --- Media / Entertainment -----------------------------------------------------

Eidr = Annotated[
    str,
    StringConstraints(pattern=r"^10\.5240/[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-F0-9]{4}-[A-Z0-9]$"),
    StandardRef("eidr", "Content-ID", "2.1"),
]
