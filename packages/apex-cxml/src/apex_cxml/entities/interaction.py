"""CXML Interaction entity."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import Field

from apex_schemas_common import CanonicalEntity


class InteractionChannel(StrEnum):
    IN_STORE = "IN_STORE"
    WEB = "WEB"
    MOBILE = "MOBILE"
    EMAIL = "EMAIL"
    SMS = "SMS"
    PHONE = "PHONE"
    CHAT = "CHAT"


class Interaction(CanonicalEntity):
    """A single customer touch-point across channels."""

    customer_key: str | None = Field(None, description="FK → CXML Customer (null if anonymous).")
    channel: InteractionChannel
    occurred_at: datetime
    duration_seconds: int | None = Field(None, ge=0)
    sentiment_score: float | None = Field(
        None, ge=-1.0, le=1.0, description="NPS-style sentiment in [-1, +1]."
    )
    topic: str | None = None
    resolved: bool = False
