"""APEX shared schema infrastructure.

Public surface:

- :class:`CanonicalEntity` — base class for every canonical Silver entity.
- :class:`ScdType2Fields` — mixin that adds SCD Type 2 history fields.
- :func:`generate_delta_ddl` — Pydantic model → Delta / Spark SQL ``CREATE TABLE``.
- :func:`build_purview_payload` — Pydantic model → Purview classification dict.
- :mod:`apex_schemas_common.standards` — standards registry (Pattern A identifier types).
"""

from apex_schemas_common.ddl import generate_delta_ddl
from apex_schemas_common.entity import CanonicalEntity, ScdType2Fields
from apex_schemas_common.purview import build_purview_payload

__all__ = [
    "CanonicalEntity",
    "ScdType2Fields",
    "build_purview_payload",
    "generate_delta_ddl",
]
