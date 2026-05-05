"""Tests for THML entities + OTA translator."""

from __future__ import annotations

from datetime import UTC, date, datetime
from uuid import uuid4

import pytest

from apex_standards_opentravel import (
    OtaAirReservation,
    OtaAirSegment,
    OtaTraveler,
)
from apex_thml import (
    Disruption,
    DisruptionKind,
    Itinerary,
    ItineraryKind,
    LoyaltyAccount,
    LoyaltyTier,
    Reservation,
    ReservationStatus,
    Segment,
    SegmentStatus,
    Traveler,
    reservation_from_ota_air,
)


def _envelope() -> dict[str, object]:
    return {
        "event_id": uuid4(),
        "event_ts": datetime.now(UTC),
        "entity_id": "test",
        "source_system": "ota",
        "source_system_ts": datetime.now(UTC),
    }


def _scd2() -> dict[str, object]:
    return {
        "scd2_valid_from": datetime.now(UTC),
        "scd2_is_current": True,
        "row_hash": "abc",
    }


def test_traveler_pii_tokenised() -> None:
    t = Traveler(
        traveler_natural="cust-1",
        full_name_token="tok_jane_doe",
        email_token="tok_email",
        phone_token="tok_phone",
        passport_country="USA",
        date_of_birth=date(1985, 1, 1),
        **_envelope(), **_scd2(),
    )  # type: ignore[arg-type]
    assert t.full_name_token == "tok_jane_doe"


def test_reservation_with_travelers() -> None:
    r = Reservation(
        pnr_token="tok_ABC123",
        primary_traveler_key="traveler:t1",
        additional_traveler_keys=["traveler:t2"],
        booked_at=datetime.now(UTC),
        total_amount=599.00,
        **_envelope(),
    )  # type: ignore[arg-type]
    assert r.status is ReservationStatus.BOOKED
    assert len(r.additional_traveler_keys) == 1


def test_itinerary_kinds() -> None:
    it = Itinerary(
        reservation_key="res:1", kind=ItineraryKind.AIR,
        sequence=1, **_envelope(),
    )  # type: ignore[arg-type]
    assert it.kind is ItineraryKind.AIR


def test_segment_for_flight() -> None:
    seg = Segment(
        itinerary_key="itin:1", sequence=1,
        origin="SFO", destination="JFK",
        scheduled_start=datetime(2026, 5, 1, 8, 0, tzinfo=UTC),
        scheduled_end=datetime(2026, 5, 1, 16, 30, tzinfo=UTC),
        carrier_code="UA", flight_number="UA123",
        cabin_class="economy",
        **_envelope(),
    )  # type: ignore[arg-type]
    assert seg.cabin_class == "economy"
    assert seg.status is SegmentStatus.SCHEDULED


def test_loyalty_account_member_token() -> None:
    la = LoyaltyAccount(
        traveler_key="traveler:t1",
        program_code="UA-MP",
        member_number_token="tok_mem_999",
        tier=LoyaltyTier.GOLD,
        points_balance=42500,
        **_envelope(), **_scd2(),
    )  # type: ignore[arg-type]
    assert la.tier is LoyaltyTier.GOLD
    assert la.points_balance == 42500


def test_disruption_with_rebook() -> None:
    d = Disruption(
        segment_key="seg:1",
        kind=DisruptionKind.CANCELLATION,
        occurred_at=datetime.now(UTC),
        severity_minutes=240,
        cause="Mechanical — hydraulics",
        rebooked_segment_key="seg:rebook-1",
        customer_notified=True,
        **_envelope(),
    )  # type: ignore[arg-type]
    assert d.kind is DisruptionKind.CANCELLATION


@pytest.mark.conformance
def test_reservation_from_ota_air() -> None:
    seg = OtaAirSegment(
        flight_number="UA123", airline_code="UA",
        departure_airport="SFO", arrival_airport="JFK",
        departure_datetime=datetime(2026, 5, 1, 8, 0),
        arrival_datetime=datetime(2026, 5, 1, 16, 30),
    )
    ota = OtaAirReservation(
        pnr="ABC123",
        travelers=[
            OtaTraveler(given_name="Jane", surname="Doe"),
            OtaTraveler(given_name="John", surname="Doe"),
        ],
        segments=[seg],
        booking_datetime=datetime.now(),
    )
    res = reservation_from_ota_air(ota)
    assert res.pnr_token.startswith("tok_placeholder_")
    assert "ABC123" in res.pnr_token
    assert res.primary_traveler_key.startswith("traveler:")
    assert len(res.additional_traveler_keys) == 1
