# 04 — Medallion: Bronze, Silver, Gold (Travel & Hospitality extensions)

> Extensions to the medallion build in [`../telco/04-medallion-bronze-silver-gold.md`](../telco/04-medallion-bronze-silver-gold.md). New Bronze landings for partner data feeds, new Silver canonical entities for trip/booking/loyalty, new Gold views for `v_traveler_360_household`, `v_trip_current_state`, `v_disruption_inflight`, and `v_loyalty_balances`.

## 1. New Bronze landings

| Bronze table | `source_system` | `source_pattern` | classification | Feeds Silver entity |
|---|---|---|---|---|
| `bronze.tmt_hom.airline_pnr` | `american-airlines`, `delta-airlines`, `united-airlines`, `southwest`, `alaska`, `jetblue` | `eventstream` | `pii` | `Trip, ItinerarySegment, Booking` |
| `bronze.tmt_hom.airline_disruption` | `american-airlines`, `delta-airlines`, `united-airlines` | `eventstream` | `pii` | `DisruptionEvent` |
| `bronze.tmt_hom.hotel_reservation` | `marriott-bonvoy`, `hilton-honors`, `hyatt-world`, `ihg-one`, `accor-all` | `mirrored_database` | `pii` | `Booking, ItinerarySegment` |
| `bronze.tmt_hom.hotel_stay_events` | `marriott-bonvoy`, `hilton-honors` | `eventstream` | `pii` | `ItinerarySegment` (status changes) |
| `bronze.tmt_hom.ota_itinerary` | `expedia`, `booking-com`, `kayak`, `google-travel` | `mirrored_database` | `pii` | `Trip, ItinerarySegment, Booking` |
| `bronze.tmt_hom.str_booking` | `airbnb`, `vrbo`, `plum-guide`, `sonder` | `mirrored_database` | `pii` | `Booking, ItinerarySegment` |
| `bronze.tmt_hom.rental_car` | `hertz`, `avis`, `enterprise`, `turo`, `zipcar` | `mirrored_database` | `pii` | `Booking, ItinerarySegment` |
| `bronze.tmt_hom.rideshare` | `uber`, `lyft` | `eventstream` | `pii` | `ItinerarySegment` (in-trip transport) |
| `bronze.tmt_hom.dining_reservation` | `opentable`, `resy`, `tock` | `eventstream` | `pii` | `ItinerarySegment, Booking` |
| `bronze.tmt_hom.experience_booking` | `viator`, `getyourguide` | `mirrored_database` | `pii` | `ItinerarySegment, Booking` |
| `bronze.tmt_hom.loyalty_sync` | `aa-aadvantage`, `dl-skymiles`, `ua-mileageplus`, `marriott-bonvoy`, `hilton-honors`, `hertz-gold` | `mirrored_database` | `cpni` | `LoyaltyAccount` |
| `bronze.tmt_hom.travel_document_refs` | `apex-identity` | `custom_endpoint` | `cpni` | `TravelDocument` (tokenised) |
| `bronze.tmt_hom.travel_insurance` | `allianz-travel`, `aig-travel`, `travelguard` | `mirrored_database` | `pii` | `Booking` (insurance segment) |

All conform to `BronzeLandingConfig` + `generate_bronze_ddl(...)` from `apex_medallion.bronze.schema`.

## 2. New Silver canonical entities

These slot into the existing `packages/apex-tmtcml/src/apex_tmtcml/entities/home/` namespace (or a new `…/entities/travel/` sub-package). All carry classification + tokenization.

```python
# packages/apex-tmtcml/src/apex_tmtcml/entities/travel/trip.py
from datetime import datetime
from pydantic import BaseModel, Field
from apex_core.types import Classification

class Trip(BaseModel):
    trip_id: str = Field(..., classification=Classification.PII)
    household_id: str = Field(..., classification=Classification.PII)
    person_id: str | None = Field(None, classification=Classification.PII)
    trip_type: str                       # 'leisure','business','mixed','reunion','medical'
    origin: str
    destination: str
    depart_ts: datetime
    return_ts: datetime
    current_state: str                   # 'planned','departing','in_transit','on_location','returning','reunified','cancelled'
    rollup_party_size: int

class ItinerarySegment(BaseModel):
    segment_id: str = Field(..., classification=Classification.PII)
    trip_id: str
    household_id: str
    segment_type: str                    # 'flight','hotel','str','rental_car','rideshare','train','cruise','experience','dining'
    sequence_no: int
    starts_ts: datetime
    ends_ts: datetime
    origin: str | None
    destination: str | None
    partner_id: str                      # vendor.vendor_id
    status: str
    metadata: dict                       # partner-specific JSON

class Booking(BaseModel):
    booking_id: str = Field(..., classification=Classification.PII)
    segment_id: str
    household_id: str
    partner_id: str
    confirmation_code: str               # PNR / hotel confirmation
    record_locator: str | None
    booked_via: str                      # 'direct','ota_expedia','ota_booking','partner_app'
    total_cost_usd: float
    currency: str
    loyalty_account_id: str | None
    booked_at: datetime

class LoyaltyAccount(BaseModel):
    account_id: str
    household_id: str = Field(..., classification=Classification.PII)
    person_id: str
    program_id: str
    member_number_token: str = Field(..., classification=Classification.CPNI)
    tier: str
    points_balance: float
    last_synced_ts: datetime

class TravelDocument(BaseModel):
    document_id: str
    household_id: str
    person_id: str
    doc_type: str                        # 'passport','global_entry','tsa_pre','known_traveler','clear','realid'
    doc_token: str = Field(..., classification=Classification.CPNI)
    expires_on: str
    issuing_country: str

class TripStateEvent(BaseModel):
    event_id: str
    event_ts: datetime
    trip_id: str
    household_id: str
    person_id: str | None
    from_state: str
    to_state: str
    trigger: str                          # 'calendar','booking','geofence','wifi','telematics','manual'
    payload: dict | None

class DisruptionEvent(BaseModel):
    disruption_id: str
    event_ts: datetime
    trip_id: str
    segment_id: str
    household_id: str
    disruption_type: str                  # 'flight_delay','flight_cancellation','baggage_lost',...
    severity: int                         # 1-5
    detected_ts: datetime
    resolved_ts: datetime | None
    resolution_path: list[dict]           # log of agent actions taken
```

## 3. New anchor measures

```python
# packages/apex-medallion/src/apex_medallion/gold/tmt_hom_travel_measures.py

TRIP_DAYS_AWAY = MeasureDefinition(
    name="trip_days_away",
    kind=MeasureKind.PRE_MEASURE,
    language=MeasureLanguage.PYSPARK,
    owner="tmt-practice-lead",
    description="Days remaining in current trip; negative if past return.",
    formula="(F.col('trip_return_ts').cast('long') - F.unix_timestamp()) / 86400.0",
    depends_on=["trip_return_ts"],
    consumer_map=["tmt-hom-trip-orchestrator"],
)

HOUSEHOLD_ROLLUP_STATE = MeasureDefinition(
    name="household_rollup_state",
    kind=MeasureKind.PRE_MEASURE,
    language=MeasureLanguage.PYSPARK,
    owner="tmt-practice-lead",
    description="fully-occupied / partially-away / fully-away rollup of per-person trip states.",
    formula=(
        "F.when(F.col('away_count') == 0, F.lit('fully-occupied'))"
        ".when(F.col('away_count') < F.col('member_count'), F.lit('partially-away'))"
        ".otherwise(F.lit('fully-away'))"
    ),
    depends_on=["away_count","member_count"],
    consumer_map=["tmt-hom-trip-orchestrator","tmt-hom-energy-agent","tmt-hom-security-agent"],
)

DISRUPTION_RECOVERY_TIME = MeasureDefinition(
    name="disruption_recovery_minutes",
    kind=MeasureKind.PRE_MEASURE,
    language=MeasureLanguage.PYSPARK,
    owner="tmt-practice-lead",
    description="Minutes between disruption detection and resolution.",
    formula="(F.col('resolved_ts').cast('long') - F.col('detected_ts').cast('long')) / 60.0",
    depends_on=["detected_ts","resolved_ts"],
    consumer_map=["tmt-hom-flight-concierge","tmt-hom-hotel-concierge"],
)

LOYALTY_PORTFOLIO_VALUE = MeasureDefinition(
    name="loyalty_portfolio_value_usd",
    kind=MeasureKind.POST_MEASURE,
    language=MeasureLanguage.TSQL,
    owner="tmt-practice-lead",
    description="Estimated USD value of the household's combined loyalty balances at posted redemption rates.",
    formula=(
        "SUM(points_balance * COALESCE(posted_redemption_rate_usd_per_point, 0))"
    ),
    depends_on=["points_balance","posted_redemption_rate_usd_per_point"],
    consumer_map=["tmt-hom-trip-orchestrator","customer-portal"],
)
```

## 4. New Gold virtual views

```sql
-- v_traveler_360_household: single-row-per-household travel posture
CREATE OR ALTER VIEW gold.v_tmt_hom_traveler_360_household AS
SELECT
  household_id,
  household_rollup_state,           -- pre-measure
  active_trip_count,
  next_departure_ts,
  most_recent_return_ts,
  loyalty_portfolio_value_usd,       -- post-measure
  active_disruption_count,
  _classification
FROM silver.tmt_hom.trip_current_household
;

-- v_trip_current_state: per-person trip status
CREATE OR ALTER VIEW gold.v_tmt_hom_trip_current_state AS
SELECT
  household_id,
  person_id,
  trip_id,
  current_state,                     -- planned / departing / in_transit / on_location / returning / reunified
  origin,
  destination,
  depart_ts,
  return_ts,
  trip_days_away,                    -- pre-measure
  next_segment_partner,
  next_segment_starts_ts,
  _classification
FROM silver.tmt_hom.trip_current
;

-- v_disruption_inflight: open disruption events with recovery posture
CREATE OR ALTER VIEW gold.v_tmt_hom_disruption_inflight AS
SELECT
  household_id,
  trip_id,
  disruption_id,
  disruption_type,
  severity,
  detected_ts,
  disruption_recovery_minutes,        -- pre-measure
  resolution_state,                   -- 'detected','agent_proposing','user_review','executing','resolved'
  partner_name,
  proposed_action,
  _classification
FROM silver.tmt_hom.disruption_state
;

-- v_loyalty_balances: cross-partner loyalty portfolio
CREATE OR ALTER VIEW gold.v_tmt_hom_loyalty_balances AS
SELECT
  household_id,
  person_id,
  program_code,                       -- 'AA-AAdvantage', 'MAR-Bonvoy', 'HRTZ-Gold', etc.
  tier,
  points_balance,
  posted_redemption_rate_usd_per_point,
  estimated_value_usd,
  last_synced_ts,
  _classification
FROM silver.tmt_hom.loyalty_current
;
```

## 5. End-to-end flow — IROPS recovery

```
American Airlines disruption signal (flight cancellation, AA1234)
   ↓ Bronze:   bronze.tmt_hom.airline_disruption  (raw AA payload)
   ↓ Silver:   DisruptionEvent + ItinerarySegment status update
   ↓ Gold:     v_tmt_hom_disruption_inflight  (severity=4, detected now)
   ↓ Agent:    apex.tmt.agents.home-flight-concierge
              + cross-references v_tmt_hom_trip_current_state
              + cross-references household calendar (kid's recital tomorrow)
              + queries Expedia for alternate routings
   ↓ Action:   apex.tmt.mcp.aa.submit_rebook (preferred Delta routing returned via partner-search)
              (HITL gate: customer mobile-push approval within 5 minutes)
   ↓ Audit:    agent_run + agent_action + view_definition_sha + tools_called.result_hash
```

The same flow shape applies to hotel walks, rental unavailability, lost baggage, weather diversions, and itinerary conflicts. See [`diagrams/flow-irops-end-to-end.md`](./diagrams/flow-irops-end-to-end.md) for the rendered diagram.
