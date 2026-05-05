"""AXLECML QualityResult entity — per-unit / per-batch quality measurement."""

from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity


class QualityStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    CONDITIONAL_PASS = "conditional_pass"
    WAIVED = "waived"
    PENDING = "pending"


class QualityResult(CanonicalEntity):
    """A quality measurement against a batch or unit."""

    test_code: str = Field(..., description="Test method or parameter identifier.")
    batch_id: str | None = None
    unit_id: str | None = None
    equipment_key: str | None = None
    measured_at: datetime
    measurement_value: Decimal | None = None
    measurement_unit: str | None = None
    target_value: Decimal | None = None
    lower_limit: Decimal | None = None
    upper_limit: Decimal | None = None
    status: QualityStatus = QualityStatus.PENDING
    inspector_id: str | None = None
    notes: str = ""
