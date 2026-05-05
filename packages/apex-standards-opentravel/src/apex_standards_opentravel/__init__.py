"""APEX OpenTravel (OTA) Pattern-B mirror — Air / Hotel / Car subsets."""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

_OTA_CONFIG = ConfigDict(extra="forbid")


# --- Common ------------------------------------------------------------------


class OtaTraveler(BaseModel):
    """OTA Traveler — passenger / guest identity."""

    model_config = _OTA_CONFIG
    given_name: str
    surname: str
    date_of_birth: date | None = None
    passport_number: str | None = None
    passport_country: str | None = Field(None, min_length=2, max_length=3)
    loyalty_number: str | None = None


# --- Air --------------------------------------------------------------------


class OtaAirSegment(BaseModel):
    """A single flight segment on an air reservation."""

    model_config = _OTA_CONFIG
    flight_number: str
    airline_code: str = Field(..., min_length=2, max_length=3)
    departure_airport: str = Field(..., min_length=3, max_length=3)
    arrival_airport: str = Field(..., min_length=3, max_length=3)
    departure_datetime: datetime
    arrival_datetime: datetime
    cabin_class: Literal["economy", "premium_economy", "business", "first"] = "economy"


class OtaAirReservation(BaseModel):
    """OTA Air reservation — a multi-segment itinerary for a traveler."""

    model_config = _OTA_CONFIG
    pnr: str = Field(..., min_length=6, max_length=6, description="PNR locator (6-char GDS-style).")
    travelers: list[OtaTraveler]
    segments: list[OtaAirSegment]
    booking_datetime: datetime
    status: Literal["booked", "ticketed", "cancelled"] = "booked"


# --- Hotel ------------------------------------------------------------------


class OtaHotelStay(BaseModel):
    """A single hotel stay (one property, date range)."""

    model_config = _OTA_CONFIG
    property_code: str
    check_in: date
    check_out: date
    room_type_code: str | None = None
    rate_plan_code: str | None = None
    guests: int = Field(..., ge=1)


class OtaHotelReservation(BaseModel):
    """OTA Hotel reservation — one or more stays (chain-level booking)."""

    model_config = _OTA_CONFIG
    confirmation_number: str
    primary_traveler: OtaTraveler
    additional_travelers: list[OtaTraveler] = Field(default_factory=list)
    stays: list[OtaHotelStay]
    booking_datetime: datetime
    status: Literal["confirmed", "cancelled", "checked_in", "checked_out"] = "confirmed"


# --- Car --------------------------------------------------------------------


class OtaCarReservation(BaseModel):
    """OTA Car reservation."""

    model_config = _OTA_CONFIG
    confirmation_number: str
    traveler: OtaTraveler
    pickup_location: str
    return_location: str
    pickup_datetime: datetime
    return_datetime: datetime
    vehicle_category_code: str = Field(..., description="ACRISS-style 4-char category code.")
    status: Literal["confirmed", "cancelled", "picked_up", "returned"] = "confirmed"


__all__ = [
    "OtaAirReservation",
    "OtaAirSegment",
    "OtaCarReservation",
    "OtaHotelReservation",
    "OtaHotelStay",
    "OtaTraveler",
]
