# apex-standards-opentravel

**Pattern-B** mirror for OpenTravel Alliance (OTA) schemas.

**Consumed by:** `apex-thml`.

## Scope (Sprint 3)

- **Air** — `OtaAirReservation`, `OtaAirSegment`, `OtaTraveler`
- **Hotel** — `OtaHotelReservation`, `OtaHotelStay`
- **Car** — `OtaCarReservation`

## What defers

- Loyalty info, ancillary-service messaging, PADIS (Sprint 15 adapter).
- Full OTA corpus (300+ messages) — incremental per consuming agent.

Design anchor: `Sprint-3-Practice-Schemas-Plan.md` §4.5.
