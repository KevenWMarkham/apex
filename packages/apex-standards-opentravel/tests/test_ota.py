"""Tests for the OpenTravel air / hotel / car subsets."""

from __future__ import annotations

from datetime import date, datetime, timedelta

import pytest
from pydantic import ValidationError

from apex_standards_opentravel import (
    OtaAirReservation,
    OtaAirSegment,
    OtaCarReservation,
    OtaHotelReservation,
    OtaHotelStay,
    OtaTraveler,
)


def _traveler() -> OtaTraveler:
    return OtaTraveler(given_name="Jane", surname="Doe", date_of_birth=date(1985, 6, 1))


def test_air_reservation_pnr_exactly_six_chars() -> None:
    seg = OtaAirSegment(
        flight_number="UA123", airline_code="UA",
        departure_airport="SFO", arrival_airport="JFK",
        departure_datetime=datetime(2026, 5, 1, 8, 0),
        arrival_datetime=datetime(2026, 5, 1, 16, 30),
    )
    res = OtaAirReservation(
        pnr="ABC123",
        travelers=[_traveler()],
        segments=[seg],
        booking_datetime=datetime.now(),
    )
    assert res.pnr == "ABC123"
    assert res.segments[0].cabin_class == "economy"


def test_air_reservation_rejects_bad_pnr_length() -> None:
    seg = OtaAirSegment(
        flight_number="UA1", airline_code="UA",
        departure_airport="SFO", arrival_airport="JFK",
        departure_datetime=datetime(2026, 5, 1),
        arrival_datetime=datetime(2026, 5, 1),
    )
    with pytest.raises(ValidationError):
        OtaAirReservation(
            pnr="TOO-LONG-PNR",
            travelers=[_traveler()],
            segments=[seg],
            booking_datetime=datetime.now(),
        )


def test_hotel_reservation_multi_stay() -> None:
    stays = [
        OtaHotelStay(
            property_code="HIL-SFO", check_in=date(2026, 5, 1),
            check_out=date(2026, 5, 3), guests=1,
        ),
        OtaHotelStay(
            property_code="HIL-NYC", check_in=date(2026, 5, 3),
            check_out=date(2026, 5, 5), guests=1,
        ),
    ]
    res = OtaHotelReservation(
        confirmation_number="CONF-999",
        primary_traveler=_traveler(),
        stays=stays,
        booking_datetime=datetime.now(),
    )
    assert len(res.stays) == 2


def test_car_reservation_with_acriss_code() -> None:
    now = datetime.now()
    res = OtaCarReservation(
        confirmation_number="CAR-42",
        traveler=_traveler(),
        pickup_location="SFO",
        return_location="SFO",
        pickup_datetime=now,
        return_datetime=now + timedelta(days=3),
        vehicle_category_code="ICAR",
    )
    assert res.vehicle_category_code == "ICAR"


def test_airport_code_validation() -> None:
    with pytest.raises(ValidationError):
        OtaAirSegment(
            flight_number="UA1", airline_code="UA",
            departure_airport="TOO_LONG",  # > 3 chars
            arrival_airport="JFK",
            departure_datetime=datetime.now(),
            arrival_datetime=datetime.now(),
        )


def test_guests_must_be_at_least_one() -> None:
    with pytest.raises(ValidationError):
        OtaHotelStay(
            property_code="HIL-SFO", check_in=date(2026, 5, 1),
            check_out=date(2026, 5, 3), guests=0,
        )
