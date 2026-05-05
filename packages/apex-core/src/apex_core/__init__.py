"""APEX Core — L1 Contract layer.

Provides manifest schemas, validators, canonical envelope, and SemVer bump
classification. This is the normative contract that every L2 Edition, L3
Practice, and L4 Tenant pins against.

See ``docs/APEX - Design and Build/APEX_Design.md`` §3 for the four-layer model.
"""

from apex_core._version import __version__
from apex_core.envelope import (
    CORE_ENVELOPE_FIELDS,
    ENVELOPE_FIELDS,
    CanonicalEnvelope,
)
from apex_core.quality import (
    QUALITY_FIELDS,
    DataQualityMetadata,
    QualityDimension,
)

__all__ = [
    "CORE_ENVELOPE_FIELDS",
    "CanonicalEnvelope",
    "DataQualityMetadata",
    "ENVELOPE_FIELDS",
    "QUALITY_FIELDS",
    "QualityDimension",
    "__version__",
]
