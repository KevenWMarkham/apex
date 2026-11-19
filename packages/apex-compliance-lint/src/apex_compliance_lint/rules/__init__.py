"""Rule packs — Sprint 29 Task 29.9.3."""

from apex_compliance_lint.rules.apex_brand import APEX_BRAND
from apex_compliance_lint.rules.apex_typography import APEX_TYPOGRAPHY

__all__ = [
    "APEX_BRAND",
    "APEX_TYPOGRAPHY",
]


# Default rule packs applied unless caller specifies otherwise.
DEFAULT_PACKS = (
    APEX_TYPOGRAPHY,
    APEX_BRAND,
)
