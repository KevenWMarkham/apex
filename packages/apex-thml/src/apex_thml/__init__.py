"""APEX THML — Travel & Hospitality canonical entities."""

from __future__ import annotations

from datetime import UTC, date, datetime
from enum import StrEnum
from typing import Annotated, Literal
from uuid import uuid4

from pydantic import Field

from apex_core.types import Classification
from apex_schemas_common import CanonicalEntity, ScdType2Fields
from apex_standards_opentravel import OtaAirReservation


# --- Entities --------------------------------------------------------------


class Traveler(CanonicalEntity, ScdType2Fields):
    """Canonical traveler identity — PII tokenised."""

    traveler_natural: str = Field(..., description="Source-system traveler id.")
    full_name_token: Annotated[str, Classification.PII] | None = None
    email_token: Annotated[str, Classification.PII] | None = None
    phone_token: Annotated[str, Classification.PII] | None = None
    passport_number_token: Annotated[str, Classification.PII] | None = None
    passport_country: str | None = Field(None, min_length=2, max_length=3)
    date_of_birth: date | None = None
    loyalty_keys: list[str] = Field(default_factory=list)


class ReservationStatus(StrEnum):
    BOOKED = "booked"
    TICKETED = "ticketed"
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class Reservation(CanonicalEntity):
    """A reservation container — one or more itineraries."""

    pnr_token: Annotated[str, Classification.PII] = Field(
        ..., description="Tokenised PNR / record locator."
    )
    primary_traveler_key: str
    additional_traveler_keys: list[str] = Field(default_factory=list)
    status: ReservationStatus = ReservationStatus.BOOKED
    booked_at: datetime
    total_amount: float | None = Field(None, ge=0.0)
    currency: str = Field("USD", min_length=3, max_length=3)


class ItineraryKind(StrEnum):
    AIR = "air"
    HOTEL = "hotel"
    CAR = "car"
    RAIL = "rail"
    CRUISE = "cruise"


class Itinerary(CanonicalEntity):
    """A leg of a Reservation — typically one per transport / stay mode."""

    reservation_key: str
    kind: ItineraryKind
    sequence: int = Field(..., ge=1)
    start_at: datetime | None = None
    end_at: datetime | None = None


class SegmentStatus(StrEnum):
    SCHEDULED = "scheduled"
    BOARDED = "boarded"
    DEPARTED = "departed"
    ARRIVED = "arrived"
    CANCELLED = "cancelled"
    DELAYED = "delayed"
    REBOOKED = "rebooked"


class Segment(CanonicalEntity):
    """A single leg within an Itinerary."""

    itinerary_key: str
    sequence: int = Field(..., ge=1)
    origin: str = Field(..., description="Airport / city / property / pickup code.")
    destination: str
    scheduled_start: datetime
    scheduled_end: datetime
    actual_start: datetime | None = None
    actual_end: datetime | None = None
    carrier_code: str | None = None
    operator_code: str | None = None
    flight_number: str | None = None
    cabin_class: Literal["economy", "premium_economy", "business", "first"] | None = None
    property_code: str | None = None
    vehicle_category_code: str | None = None
    status: SegmentStatus = SegmentStatus.SCHEDULED


class LoyaltyTier(StrEnum):
    BASE = "base"
    SILVER = "silver"
    GOLD = "gold"
    PLATINUM = "platinum"
    DIAMOND = "diamond"


class LoyaltyAccount(CanonicalEntity, ScdType2Fields):
    """Loyalty-program membership."""

    traveler_key: str
    program_code: str
    member_number_token: Annotated[str, Classification.MEMBER_ONLY] = Field(...)
    tier: LoyaltyTier = LoyaltyTier.BASE
    points_balance: int = Field(0, ge=0)
    miles_balance: int = Field(0, ge=0)
    joined_date: date | None = None
    active: bool = True


class DisruptionKind(StrEnum):
    CANCELLATION = "cancellation"
    DELAY = "delay"
    EQUIPMENT_SWAP = "equipment_swap"
    SCHEDULE_CHANGE = "schedule_change"
    DIVERSION = "diversion"
    OVERBOOKING = "overbooking"
    WEATHER = "weather"
    CREW = "crew"
    MECHANICAL = "mechanical"


class Disruption(CanonicalEntity):
    """An IROP event affecting a Segment (or Itinerary)."""

    segment_key: str = Field(..., description="FK → Segment.entity_id.")
    kind: DisruptionKind
    occurred_at: datetime
    severity_minutes: int | None = Field(None, ge=0)
    cause: str = ""
    rebooked_segment_key: str | None = None
    customer_notified: bool = False


# --- Translator ------------------------------------------------------------


def _envelope(*, entity_id: str, source_system: str = "ota") -> dict[str, object]:
    now = datetime.now(UTC)
    return {
        "event_id": uuid4(),
        "event_ts": now,
        "entity_id": entity_id,
        "source_system": source_system,
        "source_system_ts": now,
    }


def reservation_from_ota_air(ota: OtaAirReservation) -> Reservation:
    """Translate an OpenTravel Air reservation into an APEX THML Reservation.

    Tokens are placeholder-only until Sprint 5's tokenizer-mcp ships.
    """
    primary = ota.travelers[0] if ota.travelers else None
    primary_key = (
        f"traveler:{primary.surname}:{primary.given_name}" if primary else "traveler:unknown"
    )
    return Reservation(
        **_envelope(entity_id=f"reservation:{ota.pnr}"),
        pnr_token=f"tok_placeholder_{ota.pnr}",
        primary_traveler_key=primary_key,
        additional_traveler_keys=[
            f"traveler:{t.surname}:{t.given_name}" for t in ota.travelers[1:]
        ],
        status=ReservationStatus(ota.status) if ota.status in {
            s.value for s in ReservationStatus
        } else ReservationStatus.BOOKED,
        booked_at=ota.booking_datetime,
    )  # type: ignore[arg-type]


__all__ = [
    "Disruption",
    "DisruptionKind",
    "Itinerary",
    "ItineraryKind",
    "LoyaltyAccount",
    "LoyaltyTier",
    "Reservation",
    "ReservationStatus",
    "Segment",
    "SegmentStatus",
    "Traveler",
    "reservation_from_ota_air",
]
