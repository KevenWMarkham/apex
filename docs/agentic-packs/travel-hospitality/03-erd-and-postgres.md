# 03 — ERD & Postgres Extensions

> The Travel & Hospitality pack adds new entities to the schema defined in [`../telco/03-erd-and-postgres.md`](../telco/03-erd-and-postgres.md). All new entities live in the same per-household tenant model, under the same RLS policy, in the same vault. **No new database. No new vault.** Travel context is just additional rows in the existing household's data.

The Mermaid version lives at [`diagrams/mermaid-trip-state.md`](./diagrams/mermaid-trip-state.md).

## 1. New entities

| Entity | Purpose | Tenant-scoped? |
|---|---|---|
| `trip` | The unit of travel — a household member's planned journey | yes (`household_id`, `person_id`) |
| `itinerary_segment` | A leg / segment within a trip (flight, hotel, rental, STR) | yes |
| `booking` | A confirmed reservation tied to a partner | yes |
| `loyalty_program` | Reference catalog of loyalty programs (shared) | no |
| `loyalty_account` | Customer's account within a loyalty program | yes (CPNI-classified, tokenised) |
| `travel_document` | Passport / Global Entry / TSA Pre / Known Traveler — references only, never stored | yes (tokenised references) |
| `trip_state_event` | Append-only log of state transitions | yes |
| `disruption_event` | IROPS, cancellation, walk, lost-bag events | yes |
| `partner_endpoint` | Catalog of travel partner MCP endpoints | no (shared) |

## 2. DDL — new tables

```sql
-- Trip — the unit of travel
CREATE TABLE trip (
    trip_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id   UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    person_id      UUID REFERENCES person,          -- nullable for family / household-level trips
    trip_type      TEXT CHECK (trip_type IN ('leisure','business','mixed','reunion','medical')),
    origin         TEXT,                            -- airport code / city
    destination    TEXT,
    depart_ts      TIMESTAMPTZ,
    return_ts      TIMESTAMPTZ,
    current_state  TEXT NOT NULL DEFAULT 'planned'
                   CHECK (current_state IN
                          ('planned','departing','in_transit','on_location',
                           'returning','reunified','cancelled')),
    rollup_party_size  INT,                         -- number of household members on trip
    notes          TEXT,
    created_at     TIMESTAMPTZ DEFAULT now(),
    updated_at     TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX ON trip (household_id, current_state);
CREATE INDEX ON trip (household_id, depart_ts);

-- Itinerary segment
CREATE TABLE itinerary_segment (
    segment_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trip_id         UUID REFERENCES trip ON DELETE CASCADE,
    household_id    UUID NOT NULL,                  -- denormalized for RLS
    segment_type    TEXT NOT NULL
                    CHECK (segment_type IN ('flight','hotel','str','rental_car','rideshare','train','cruise','experience','dining')),
    sequence_no     INT,
    starts_ts       TIMESTAMPTZ,
    ends_ts         TIMESTAMPTZ,
    origin          TEXT,
    destination     TEXT,
    partner_id      UUID REFERENCES vendor,         -- airline / hotel / OTA / STR / rental / experience
    status          TEXT,                           -- 'planned','booked','checked_in','completed','cancelled','disrupted'
    metadata        JSONB                           -- partner-specific (PNR, room type, etc.)
);
CREATE INDEX ON itinerary_segment (household_id, trip_id, sequence_no);

-- Booking
CREATE TABLE booking (
    booking_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    segment_id      UUID REFERENCES itinerary_segment ON DELETE CASCADE,
    household_id    UUID NOT NULL,
    partner_id      UUID REFERENCES vendor,
    confirmation_code TEXT,                         -- e.g. AA PNR, Marriott confirmation #
    record_locator  TEXT,
    booked_via      TEXT,                           -- 'direct','ota_expedia','ota_booking','partner_app'
    total_cost_usd  NUMERIC,
    currency        TEXT,
    loyalty_account_id UUID REFERENCES loyalty_account,
    booked_at       TIMESTAMPTZ DEFAULT now(),
    raw_confirmation JSONB
);
CREATE INDEX ON booking (household_id, partner_id);

-- Loyalty program (shared catalog)
CREATE TABLE loyalty_program (
    program_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vendor_id       UUID REFERENCES vendor,
    program_code    TEXT UNIQUE,                    -- 'AA-AAdvantage','MARRIOTT-Bonvoy','HERTZ-Gold'
    name            TEXT,
    program_type    TEXT,                           -- 'airline','hotel','car','ota','dining'
    tier_names      TEXT[]                          -- e.g. {'Member','Gold','Platinum','Executive Platinum'}
);

-- Loyalty account (per household, CPNI)
CREATE TABLE loyalty_account (
    account_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id        UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    person_id           UUID REFERENCES person,
    program_id          UUID REFERENCES loyalty_program,
    member_number_token TEXT,                        -- tokenised via apex-tokenizer
    tier                TEXT,
    points_balance      NUMERIC,
    last_synced_ts      TIMESTAMPTZ
);
CREATE INDEX ON loyalty_account (household_id, program_id);

-- Travel documents (tokenised references — never raw)
CREATE TABLE travel_document (
    document_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id    UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    person_id       UUID REFERENCES person,
    doc_type        TEXT CHECK (doc_type IN ('passport','global_entry','tsa_pre','known_traveler','clear','realid')),
    doc_token       TEXT,                            -- tokenised reference to the actual doc
    expires_on      DATE,
    issuing_country TEXT
);

-- Trip state event log (append-only)
CREATE TABLE trip_state_event (
    event_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trip_id        UUID REFERENCES trip,
    household_id   UUID NOT NULL,
    person_id      UUID,
    from_state     TEXT,
    to_state       TEXT,
    trigger        TEXT,                             -- 'calendar','booking','geofence','wifi','telematics','manual'
    event_ts       TIMESTAMPTZ NOT NULL,
    payload        JSONB
);
CREATE INDEX ON trip_state_event (household_id, trip_id, event_ts);

-- Disruption event
CREATE TABLE disruption_event (
    disruption_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trip_id         UUID REFERENCES trip,
    segment_id      UUID REFERENCES itinerary_segment,
    household_id    UUID NOT NULL,
    disruption_type TEXT CHECK (disruption_type IN
                              ('flight_delay','flight_cancellation','baggage_lost','baggage_delayed',
                               'hotel_walk','rental_unavailable','weather','medical','itinerary_conflict')),
    severity        SMALLINT,                       -- 1-5
    detected_ts     TIMESTAMPTZ,
    resolved_ts     TIMESTAMPTZ,
    resolution_path JSONB                            -- log of agent actions taken
);

-- Partner endpoint catalog (shared)
CREATE TABLE partner_endpoint (
    endpoint_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vendor_id       UUID REFERENCES vendor,
    mcp_server_uri  TEXT,
    capabilities    TEXT[],                         -- {'search','book','modify','cancel','status'}
    auth_method     TEXT,                           -- 'oauth2','api_key','mtls'
    tier            TEXT                            -- 'direct','via_ota','via_gds'
);
```

## 3. New `vendor.type` values

Extend the existing `vendor.type` enum (from [`../telco/03-erd-and-postgres.md`](../telco/03-erd-and-postgres.md)) with:

```sql
-- Existing: 'grocer','utility','pharmacy','telematics'
-- New:
'airline','hotel','vacation_rental','rental_car','rideshare',
'ota','train','cruise','experience','dining','tour','travel_insurer'
```

Seed `vendor` rows for the anchor partners:

```sql
INSERT INTO vendor (name, type, api_base_url) VALUES
  ('American Airlines',   'airline',         'https://mcp.americanair.com/v1'),
  ('Delta Air Lines',     'airline',         'https://mcp.delta.com/v1'),
  ('United Airlines',     'airline',         'https://mcp.united.com/v1'),
  ('Marriott',            'hotel',           'https://mcp.marriott.com/v1'),
  ('Hilton',              'hotel',           'https://mcp.hilton.com/v1'),
  ('Hyatt',               'hotel',           'https://mcp.hyatt.com/v1'),
  ('IHG',                 'hotel',           'https://mcp.ihg.com/v1'),
  ('Airbnb',              'vacation_rental', 'https://mcp.airbnb.com/v1'),
  ('Vrbo',                'vacation_rental', 'https://mcp.vrbo.com/v1'),
  ('Expedia',             'ota',             'https://mcp.expedia.com/v1'),
  ('Booking.com',         'ota',             'https://mcp.booking.com/v1'),
  ('Kayak',               'ota',             'https://mcp.kayak.com/v1'),
  ('Hertz',               'rental_car',      'https://mcp.hertz.com/v1'),
  ('Avis',                'rental_car',      'https://mcp.avis.com/v1'),
  ('Turo',                'rental_car',      'https://mcp.turo.com/v1'),
  ('Uber',                'rideshare',       'https://mcp.uber.com/v1'),
  ('Lyft',                'rideshare',       'https://mcp.lyft.com/v1'),
  ('OpenTable',           'dining',          'https://mcp.opentable.com/v1'),
  ('Resy',                'dining',          'https://mcp.resy.com/v1'),
  ('Viator',              'experience',      'https://mcp.viator.com/v1'),
  ('GetYourGuide',        'experience',      'https://mcp.getyourguide.com/v1'),
  ('Allianz Travel',      'travel_insurer',  'https://mcp.allianztravel.com/v1');
-- URIs illustrative; actual integration patterns will vary by partner.
```

## 4. New `loyalty_program` seed data

```sql
INSERT INTO loyalty_program (vendor_id, program_code, name, program_type, tier_names) VALUES
  ((SELECT vendor_id FROM vendor WHERE name='American Airlines'), 'AA-AAdvantage',  'AAdvantage',     'airline', ARRAY['Member','Gold','Platinum','Platinum Pro','Executive Platinum']),
  ((SELECT vendor_id FROM vendor WHERE name='Delta Air Lines'),    'DL-SkyMiles',    'SkyMiles',       'airline', ARRAY['Member','Silver Medallion','Gold Medallion','Platinum Medallion','Diamond Medallion']),
  ((SELECT vendor_id FROM vendor WHERE name='United Airlines'),    'UA-MileagePlus', 'MileagePlus',    'airline', ARRAY['Member','Premier Silver','Premier Gold','Premier Platinum','Premier 1K']),
  ((SELECT vendor_id FROM vendor WHERE name='Marriott'),           'MAR-Bonvoy',     'Marriott Bonvoy','hotel',   ARRAY['Member','Silver','Gold','Platinum','Titanium','Ambassador']),
  ((SELECT vendor_id FROM vendor WHERE name='Hilton'),             'HLT-Honors',     'Hilton Honors',  'hotel',   ARRAY['Member','Silver','Gold','Diamond']),
  ((SELECT vendor_id FROM vendor WHERE name='Hyatt'),              'HYT-World',      'World of Hyatt', 'hotel',   ARRAY['Member','Discoverist','Explorist','Globalist']),
  ((SELECT vendor_id FROM vendor WHERE name='IHG'),                'IHG-One',        'IHG One Rewards','hotel',   ARRAY['Club','Silver','Gold','Platinum','Diamond']),
  ((SELECT vendor_id FROM vendor WHERE name='Hertz'),              'HRTZ-Gold',      'Hertz Gold Plus','car',     ARRAY['Gold','Five Star','President''s Circle']),
  ((SELECT vendor_id FROM vendor WHERE name='Airbnb'),             'AIRBNB',         'Airbnb',         'ota',     ARRAY['Member','Superguest (legacy)']);
```

## 5. RLS — trip tables join the same policy

All new tenant-scoped tables enable RLS using the same `current_setting('app.current_household')` policy already in place for telemetry, inventory, and health metrics:

```sql
ALTER TABLE trip                 ENABLE ROW LEVEL SECURITY;
ALTER TABLE itinerary_segment    ENABLE ROW LEVEL SECURITY;
ALTER TABLE booking              ENABLE ROW LEVEL SECURITY;
ALTER TABLE loyalty_account      ENABLE ROW LEVEL SECURITY;
ALTER TABLE travel_document      ENABLE ROW LEVEL SECURITY;
ALTER TABLE trip_state_event     ENABLE ROW LEVEL SECURITY;
ALTER TABLE disruption_event     ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON trip
    USING (household_id = current_setting('app.current_household')::uuid);
-- repeat for each table
```

## 6. New `consent.scope` values

Extend the consent scope vocabulary in the existing `consent` table:

```
-- Existing: 'health','location','purchases','video','energy'
-- New:
'travel'           -- general trip context (booked-trip metadata)
'travel.location'  -- in-transit / on-location geo tracking
'travel.loyalty'   -- loyalty program credentials
'travel.documents' -- passport / TSA Pre / Known Traveler refs
'travel.payments'  -- partner billing methods
```

Sub-agents declare which scopes they consume; the orchestrator enforces consent at run time.

## 7. Cross-references

- Companion build-spec amendment: [`../../build-specs/apex-tmt-agentic-travel-amendment.md`](../../build-specs/apex-tmt-agentic-travel-amendment.md)
- Bronze landings for new feeds: [`./04-medallion-bronze-silver-gold.md`](./04-medallion-bronze-silver-gold.md)
- Mermaid version of the trip state machine: [`./diagrams/mermaid-trip-state.md`](./diagrams/mermaid-trip-state.md)
