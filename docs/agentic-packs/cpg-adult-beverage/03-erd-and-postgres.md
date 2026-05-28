# 03 — ERD & Postgres Extensions (Beverage Channel)

```sql
-- Beverage order — age-gated, state-rules-aware
CREATE TABLE beverage_order (
    order_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id    UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    person_id       UUID REFERENCES person,
    retailer_vendor_id UUID REFERENCES vendor,
    brand_vendor_id UUID REFERENCES vendor,            -- Sazerac, Diageo, Pernod, Brown-Forman
    state_code      TEXT,                              -- destination state for compliance check
    fulfillment_type TEXT,                             -- 'pickup_licensed','direct_ship_winery','direct_ship_distillery','retailer_ship_in_state'
    age_verified    BOOLEAN,
    age_verification_id UUID REFERENCES age_verification,
    total_usd       NUMERIC,
    status          TEXT,
    placed_at       TIMESTAMPTZ
);

-- Allocation alert
CREATE TABLE allocation_alert (
    alert_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id    UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    sku_token       TEXT,                              -- e.g., 'BTAC-2024-EAGLE-RARE-17'
    retailer_vendor_id UUID REFERENCES vendor,
    quantity_available INT,
    drop_ts         TIMESTAMPTZ,
    hold_expires_ts TIMESTAMPTZ,
    msrp_usd        NUMERIC,
    status          TEXT,                              -- 'reserved','customer_confirmed','expired','converted'
    converted_order_id UUID REFERENCES beverage_order
);

-- Age verification
CREATE TABLE age_verification (
    verification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    person_id       UUID NOT NULL REFERENCES person,
    household_id    UUID NOT NULL,
    method          TEXT,                              -- 'doc_review','provider_veratad','provider_bluecheck','retailer_in_person'
    doc_token       TEXT,                              -- tokenised ID-document reference
    verified_at     TIMESTAMPTZ,
    expires_at      TIMESTAMPTZ,
    verifier_vendor_id UUID REFERENCES vendor
);

-- Cellar inventory
CREATE TABLE cellar_item (
    item_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id    UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    product_id      UUID REFERENCES product,
    bottle_count    NUMERIC,
    bottle_size_ml  INT,
    purchased_at    TIMESTAMPTZ,
    is_open         BOOLEAN,
    opened_at       TIMESTAMPTZ,
    estimated_remaining_pct NUMERIC,
    notes           TEXT
);

-- Tasting event
CREATE TABLE tasting_event (
    event_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    venue           TEXT,
    venue_vendor_id UUID REFERENCES vendor,            -- distillery, retail venue, partner
    name            TEXT,
    starts_at       TIMESTAMPTZ,
    state_code      TEXT,
    capacity        INT,
    price_per_seat_usd NUMERIC,
    description     TEXT
);

CREATE TABLE tasting_booking (
    booking_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_id        UUID REFERENCES tasting_event,
    household_id    UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    seat_count      INT,
    total_usd       NUMERIC,
    booked_at       TIMESTAMPTZ,
    status          TEXT
);

ALTER TABLE beverage_order      ENABLE ROW LEVEL SECURITY;
ALTER TABLE allocation_alert    ENABLE ROW LEVEL SECURITY;
ALTER TABLE age_verification    ENABLE ROW LEVEL SECURITY;
ALTER TABLE cellar_item         ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasting_booking     ENABLE ROW LEVEL SECURITY;
```

## New `vendor.type` values

```
'distillery'           -- Sazerac, Buffalo Trace, Heaven Hill, etc.
'spirits-brand-owner'  -- Diageo, Pernod Ricard, Brown-Forman, Constellation
'licensed-retailer'    -- Total Wine, BevMo, Binny's, independents
'age-verifier'         -- Veratad, AgeChecker, BlueCheck
```

## New Gold views

- `gold.v_tmt_bev_household_cellar`
- `gold.v_tmt_bev_active_alerts`
- `gold.v_tmt_bev_state_eligibility` (per-household-per-state-per-product allowed/denied)
- `gold.v_tmt_bev_upcoming_tastings`
