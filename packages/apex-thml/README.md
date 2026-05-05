# apex-thml

**APEX THML** — Travel & Hospitality canonical entities over OpenTravel + IATA NDC.

Entities: `Traveler` · `Reservation` · `Itinerary` · `Segment` · `LoyaltyAccount` · `Disruption`.

Translator: `ota_to_thml.py` — OpenTravel Air/Hotel/Car reservations → THML.

PII-heavy: name, email, phone, passport, loyalty number are all tokenised.

Design anchor: `Sprint-3-Practice-Schemas-Plan.md` §3.5.
