"""Rule packs — Sprint 29 Task 29.9.3."""

from apex_compliance_lint.rules.deloitte_microsoft_independence import (
    DELOITTE_MICROSOFT_INDEPENDENCE,
)
from apex_compliance_lint.rules.apex_typography import APEX_TYPOGRAPHY
from apex_compliance_lint.rules.apex_brand import APEX_BRAND

__all__ = [
    "APEX_BRAND",
    "APEX_TYPOGRAPHY",
    "DELOITTE_MICROSOFT_INDEPENDENCE",
]


# Default rule packs applied unless caller specifies otherwise.
DEFAULT_PACKS = (
    DELOITTE_MICROSOFT_INDEPENDENCE,
    APEX_TYPOGRAPHY,
    APEX_BRAND,
)
