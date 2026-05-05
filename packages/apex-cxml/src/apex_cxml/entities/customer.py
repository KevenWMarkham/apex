"""CXML Customer entity.

Every direct-identifier field is suffixed ``_token`` and carries
``Classification.PII``. Raw values never cross the Bronze→Silver boundary
(see APEX_Design §5.7, §6.4.1). The tokens in Silver are the only values
agents ever see; cleartext lookup is gated by the tokenizer-mcp service.
"""

from __future__ import annotations

from datetime import date
from enum import StrEnum
from typing import Annotated

from pydantic import Field

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity, ScdType2Fields


class CustomerStatus(StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    OPTED_OUT = "OPTED_OUT"
    SUPPRESSED = "SUPPRESSED"


class Customer(CanonicalEntity, ScdType2Fields):
    """Canonical customer record.

    Identity resolution resolves multiple SOR identities into one canonical
    record (see APEX_Design §5.5 — deterministic + probabilistic match).
    """

    customer_natural: str = Field(..., description="Primary source-system natural key.")
    status: CustomerStatus = CustomerStatus.ACTIVE

    # --- Tokenised direct identifiers (PII) ---------------------------------
    full_name_token: Annotated[str, Classification.PII] | None = Field(
        None, description="Tokenised full name."
    )
    email_token: Annotated[str, Classification.PII] | None = Field(
        None, description="Tokenised email."
    )
    phone_token: Annotated[str, Classification.PII] | None = Field(
        None, description="Tokenised phone."
    )
    address_token: Annotated[str, Classification.PII] | None = Field(
        None, description="Tokenised structured address."
    )

    # --- Non-identifier attributes ------------------------------------------
    birth_year: int | None = Field(None, ge=1900, le=2100)
    preferred_language: str | None = Field(None, min_length=2, max_length=5)
    consent_marketing: bool = False
    consent_analytics: bool = False
    opted_out_date: date | None = None
