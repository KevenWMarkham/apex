# 03 — ERD & Postgres Extensions (Automobile Channel)

> Extensions to schema in [`../telco/03-erd-and-postgres.md`](../telco/03-erd-and-postgres.md) and [`../mobility-auto/03-erd-and-postgres.md`](../mobility-auto/03-erd-and-postgres.md). Reuses `vehicle`, `auto_loan_lease`, `auto_policy` from mobility-auto; adds lifecycle, transaction, and aftermarket entities.

## 1. New entities

```sql
-- Lifecycle state attached to vehicle (extends mobility-auto vehicle table)
ALTER TABLE vehicle ADD COLUMN lifecycle_state TEXT
    CHECK (lifecycle_state IN
           ('researching','shopping','purchasing','owning_warranty',
            'owning_post_warranty','preparing_resale','resold'))
    DEFAULT 'owning_warranty';
ALTER TABLE vehicle ADD COLUMN lifecycle_state_since TIMESTAMPTZ;

-- Vehicle listing (for-sale inventory the household is researching/shopping)
CREATE TABLE vehicle_listing (
    listing_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id    UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    listing_source_vendor_id UUID REFERENCES vendor,    -- 'autonation','carmax','carvana','autotrader','dealer-direct'
    oem             TEXT,
    model           TEXT,
    model_year      INT,
    vin_token       TEXT,
    asking_price_usd NUMERIC,
    msrp_usd        NUMERIC,
    mileage_km      NUMERIC,
    location_zip    TEXT,
    listing_url     TEXT,
    captured_at     TIMESTAMPTZ DEFAULT now(),
    shortlisted     BOOLEAN DEFAULT FALSE,
    status          TEXT                                -- 'active','sold','removed'
);
CREATE INDEX ON vehicle_listing (household_id, shortlisted);

-- Purchase offer (negotiation state)
CREATE TABLE purchase_offer (
    offer_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    listing_id      UUID REFERENCES vehicle_listing,
    household_id    UUID NOT NULL,
    dealer_vendor_id UUID REFERENCES vendor,
    out_the_door_price_usd NUMERIC,
    trade_in_value_usd NUMERIC,
    financing_attached_id UUID,                          -- FK to financing_application
    insurance_attached_id UUID,                          -- FK to auto_policy
    expires_at      TIMESTAMPTZ,
    state           TEXT,                                -- 'drafted','submitted','accepted','rejected','executed'
    created_at      TIMESTAMPTZ DEFAULT now()
);

-- Financing application
CREATE TABLE financing_application (
    application_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id    UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    lender_vendor_id UUID REFERENCES vendor,            -- 'capital-one-auto','ally','chase-auto','usaa','autonation-finance','tfs'
    application_type TEXT,                              -- 'pre-approval','final','refi'
    requested_amount_usd NUMERIC,
    term_months     INT,
    submitted_at    TIMESTAMPTZ,
    decision        TEXT,                               -- 'pending','approved','declined','withdrawn'
    apr             NUMERIC,
    approved_amount_usd NUMERIC,
    classification  TEXT DEFAULT 'cpni'
);

-- Insurance quote
CREATE TABLE insurance_quote (
    quote_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id    UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    carrier_vendor_id UUID REFERENCES vendor,           -- 'progressive','state-farm','allstate','geico','usaa','root','lemonade-car'
    vehicle_listing_id UUID REFERENCES vehicle_listing,
    coverage_type   TEXT,                               -- 'liability_only','standard','full'
    annual_premium_usd NUMERIC,
    deductible_usd  NUMERIC,
    ubi_eligible    BOOLEAN,                            -- e.g., Progressive Snapshot eligible
    ubi_projected_discount_pct NUMERIC,                 -- projected based on household telematics
    quoted_at       TIMESTAMPTZ DEFAULT now(),
    expires_at      TIMESTAMPTZ,
    status          TEXT                                -- 'quoted','bound','expired','rejected'
);

-- Aftermarket parts / accessories order
CREATE TABLE aftermarket_order (
    order_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id    UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    vehicle_id      UUID REFERENCES vehicle,
    retailer_vendor_id UUID REFERENCES vendor,          -- 'autozone','advance','oreilly','napa','rockauto','amazon'
    items           JSONB,                              -- [{part_number, qty, price}]
    total_usd       NUMERIC,
    order_state     TEXT,                               -- 'submitted','ready','picked_up','shipped','delivered'
    placed_at       TIMESTAMPTZ
);

-- Charging session (extends HOM-07 with multi-network roaming)
CREATE TABLE charging_session (
    session_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id    UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    vehicle_id      UUID REFERENCES vehicle,
    network_vendor_id UUID REFERENCES vendor,           -- 'chargepoint','evgo','electrify-america','tesla-supercharger'
    location_zip    TEXT,
    starts_at       TIMESTAMPTZ,
    ends_at         TIMESTAMPTZ,
    kwh_delivered   NUMERIC,
    cost_usd        NUMERIC,
    cost_per_kwh    NUMERIC
);

-- Fuel transaction (similar to charging, for ICE/hybrid)
CREATE TABLE fuel_transaction (
    transaction_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id    UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    vehicle_id      UUID REFERENCES vehicle,
    retailer_vendor_id UUID REFERENCES vendor,          -- 'shell','chevron','bp','costco-gas','exxonmobil'
    gallons         NUMERIC,
    cost_usd        NUMERIC,
    price_per_gallon NUMERIC,
    grade           TEXT,
    purchased_at    TIMESTAMPTZ,
    location_zip    TEXT
);

-- Fleet vehicle assignment
CREATE TABLE fleet_assignment (
    assignment_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehicle_id      UUID REFERENCES vehicle,
    household_id    UUID NOT NULL,
    primary_driver_person_id UUID REFERENCES person,
    purpose         TEXT,                               -- 'personal','commute','business','rideshare-driver','delivery'
    mileage_log_enabled BOOLEAN,
    tax_deduction_eligible BOOLEAN
);

-- Resale listing
CREATE TABLE resale_listing (
    resale_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehicle_id      UUID REFERENCES vehicle,
    household_id    UUID NOT NULL,
    channel         TEXT,                               -- 'trade-in','private','carmax','carvana','peddle','donate'
    listed_at       TIMESTAMPTZ,
    asking_price_usd NUMERIC,
    accepted_offer_usd NUMERIC,
    closed_at       TIMESTAMPTZ,
    status          TEXT
);

-- Vehicle lifecycle event (append-only audit)
CREATE TABLE vehicle_lifecycle_event (
    event_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehicle_id      UUID REFERENCES vehicle,
    household_id    UUID NOT NULL,
    from_state      TEXT,
    to_state        TEXT,
    trigger         TEXT,
    event_ts        TIMESTAMPTZ NOT NULL,
    payload         JSONB
);

-- All new tables join standard RLS policy
ALTER TABLE vehicle_listing         ENABLE ROW LEVEL SECURITY;
ALTER TABLE purchase_offer          ENABLE ROW LEVEL SECURITY;
ALTER TABLE financing_application   ENABLE ROW LEVEL SECURITY;
ALTER TABLE insurance_quote         ENABLE ROW LEVEL SECURITY;
ALTER TABLE aftermarket_order       ENABLE ROW LEVEL SECURITY;
ALTER TABLE charging_session        ENABLE ROW LEVEL SECURITY;
ALTER TABLE fuel_transaction        ENABLE ROW LEVEL SECURITY;
ALTER TABLE fleet_assignment        ENABLE ROW LEVEL SECURITY;
ALTER TABLE resale_listing          ENABLE ROW LEVEL SECURITY;
ALTER TABLE vehicle_lifecycle_event ENABLE ROW LEVEL SECURITY;
```

## 2. New `vendor.type` values

```
'dealer-group'           -- AutoNation, Lithia, Penske, Group 1, Sonic
'used-car-retailer'      -- CarMax, Carvana, Vroom, Peddle
'auto-data-aggregator'   -- Cox Automotive, KBB, Edmunds, Autotrader, TrueCar
'auto-lender'            -- Capital One Auto, Ally, Chase Auto, USAA
'aftermarket-parts'      -- AutoZone, Advance Auto, O'Reilly, NAPA, RockAuto
'fuel-network'           -- Shell, Chevron, BP, ExxonMobil, Costco Gas
'fleet-mgmt'             -- Element, Wheels Donlen
'dmv-automation'         -- Vitu, ALG
'auto-insurer'           -- already in mobility-auto; extends bench
```

## 3. Anchor seed data

```sql
INSERT INTO vendor (name, type) VALUES
  -- Anchors
  ('AutoNation',           'dealer-group'),
  ('Cox Automotive',       'auto-data-aggregator'),
  ('Kelley Blue Book',     'auto-data-aggregator'),
  ('Autotrader',           'auto-data-aggregator'),
  ('Progressive',          'auto-insurer'),
  -- Dealer-group bench
  ('Lithia Motors',        'dealer-group'),
  ('Penske Automotive',    'dealer-group'),
  ('Group 1 Automotive',   'dealer-group'),
  ('Sonic Automotive',     'dealer-group'),
  -- Used-car retailers
  ('CarMax',               'used-car-retailer'),
  ('Carvana',              'used-car-retailer'),
  ('Peddle',               'used-car-retailer'),
  -- Lenders
  ('Capital One Auto',     'auto-lender'),
  ('Ally Auto',            'auto-lender'),
  ('Chase Auto',           'auto-lender'),
  ('USAA Auto',            'auto-lender'),
  -- Insurance bench
  ('State Farm',           'auto-insurer'),
  ('Geico',                'auto-insurer'),
  ('Allstate',             'auto-insurer'),
  ('Liberty Mutual',       'auto-insurer'),
  ('Root Insurance',       'auto-insurer'),
  ('Lemonade Car',         'auto-insurer'),
  -- Parts
  ('AutoZone',             'aftermarket-parts'),
  ('Advance Auto Parts',   'aftermarket-parts'),
  ('O''Reilly Auto Parts', 'aftermarket-parts'),
  ('NAPA Auto Parts',      'aftermarket-parts'),
  ('RockAuto',             'aftermarket-parts'),
  -- Fuel
  ('Shell',                'fuel-network'),
  ('Chevron',              'fuel-network'),
  ('BP',                   'fuel-network'),
  ('ExxonMobil',           'fuel-network'),
  ('Costco Gas',           'fuel-network'),
  ('GasBuddy',             'fuel-network');
```

## 4. New consent scopes

Extend `consent.scope`:
- `vehicle.purchase` — research history, shortlist, comparison data
- `vehicle.financing` — credit-pull authorization, financing applications
- `vehicle.insurance` — quote requests, policy data, UBI participation
- `vehicle.fueling` — fuel + charging transactions
- `vehicle.aftermarket` — parts orders, accessory installations

## 5. New Gold views

- `gold.v_tmt_aut_household_vehicle_portfolio` — single rollup of all owned + researching vehicles
- `gold.v_tmt_aut_shortlist_comparison` — side-by-side comparison of shortlisted listings
- `gold.v_tmt_aut_financing_offer_table` — pre-approval offers across lenders
- `gold.v_tmt_aut_insurance_quote_table` — quote comparison across carriers
- `gold.v_tmt_aut_fueling_cost_optimization` — historical fueling + projected lowest-cost options
- `gold.v_tmt_aut_resale_value_track` — trailing valuation track per vehicle for replacement signaling
- `gold.v_tmt_aut_fleet_mileage_log` — IRS-compliant mileage log for tax purposes

## 6. Cross-references

- Sibling mobility-auto/ ERD: [`../mobility-auto/03-erd-and-postgres.md`](../mobility-auto/03-erd-and-postgres.md)
- Build-spec amendment: [`../../build-specs/apex-tmt-agentic-automobile-amendment.md`](../../build-specs/apex-tmt-agentic-automobile-amendment.md)
