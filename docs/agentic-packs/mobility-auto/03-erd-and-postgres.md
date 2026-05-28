# 03 — ERD & Postgres Extensions (Mobility Channel)

> Extensions to the schema in [`../telco/03-erd-and-postgres.md`](../telco/03-erd-and-postgres.md). Builds on the existing `device` table; adds vehicle-specific entities tenant-scoped under RLS.

## 1. New entities

```sql
-- Vehicle — extends Device with auto-specific fields
CREATE TABLE vehicle (
    vehicle_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id    UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    device_id       UUID REFERENCES device,            -- nullable; ties to telematics device
    oem             TEXT,                              -- 'toyota','ford','gm','tesla','honda','hyundai','stellantis'
    model           TEXT,
    model_year      INT,
    vin_token       TEXT,                              -- tokenised VIN
    primary_driver_person_id UUID REFERENCES person,
    purchased_at    DATE,
    ownership_type  TEXT,                              -- 'owned','leased','financed'
    powertrain      TEXT,                              -- 'ICE','HEV','PHEV','BEV','FCEV'
    odometer_km     NUMERIC,
    last_telemetry_ts TIMESTAMPTZ
);

-- Vehicle recall
CREATE TABLE vehicle_recall (
    recall_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehicle_id      UUID REFERENCES vehicle,
    household_id    UUID NOT NULL,
    nhtsa_campaign  TEXT,                              -- e.g., '21V-573'
    oem_campaign    TEXT,
    summary         TEXT,
    remedy          TEXT,
    severity        SMALLINT,
    notified_at     TIMESTAMPTZ,
    scheduled_at    TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    status          TEXT                                -- 'open','scheduled','completed'
);

-- Dealer service appointment
CREATE TABLE dealer_appointment (
    appointment_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehicle_id      UUID REFERENCES vehicle,
    household_id    UUID NOT NULL,
    dealer_vendor_id UUID REFERENCES vendor,
    service_types   TEXT[],                            -- ['recall','oil','tires','battery','brakes']
    scheduled_at    TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    cost_usd        NUMERIC,
    loaner_provided BOOLEAN,
    status          TEXT
);

-- Auto loan / lease
CREATE TABLE auto_loan_lease (
    contract_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehicle_id      UUID REFERENCES vehicle,
    household_id    UUID NOT NULL,
    lender_vendor_id UUID REFERENCES vendor,           -- TFS / Ford Credit / GM Financial / etc.
    contract_type   TEXT,                              -- 'loan','lease'
    principal_usd   NUMERIC,
    apr             NUMERIC,
    term_months     INT,
    monthly_payment_usd NUMERIC,
    starts_on       DATE,
    matures_on      DATE,
    payoff_balance_usd NUMERIC,
    classification  TEXT DEFAULT 'cpni'
);

-- Auto insurance policy
CREATE TABLE auto_policy (
    policy_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehicle_id      UUID REFERENCES vehicle,
    household_id    UUID NOT NULL,
    carrier_vendor_id UUID REFERENCES vendor,
    policy_number_token TEXT,
    annual_premium_usd NUMERIC,
    coverage_type   TEXT,                              -- 'full','liability_only'
    ubi_score       NUMERIC,                           -- telematics-based score where applicable
    renews_on       DATE
);

ALTER TABLE vehicle             ENABLE ROW LEVEL SECURITY;
ALTER TABLE vehicle_recall      ENABLE ROW LEVEL SECURITY;
ALTER TABLE dealer_appointment  ENABLE ROW LEVEL SECURITY;
ALTER TABLE auto_loan_lease     ENABLE ROW LEVEL SECURITY;
ALTER TABLE auto_policy         ENABLE ROW LEVEL SECURITY;
```

## 2. New `vendor.type` values

```
'oem-auto'              -- Toyota, Ford, GM, Tesla, Honda, Hyundai, Stellantis
'dealer'                -- specific dealership entities
'auto-finance'          -- TFS, Ford Credit, GM Financial
'auto-insurer'          -- TIMS, State Farm, Progressive, Allstate, Root
```

## 3. New Gold views

- `gold.v_tmt_mob_household_fleet_360` — single rollup of the household's full vehicle fleet
- `gold.v_tmt_mob_open_recalls` — outstanding recalls across the fleet
- `gold.v_tmt_mob_service_due` — upcoming + overdue services
- `gold.v_tmt_mob_lease_end_horizon` — next-vehicle decisioning trigger window
- `gold.v_tmt_mob_insurance_renewal_horizon` — policy-renewal triggers

## 4. Cross-Channel coordination

- HOM-07 (vehicle, Home pack) provides raw telematics; this Channel adds OEM-direct + dealer + finance + insurance layers
- RTL-03 (Walmart Auto Care, Retail Channel) provides independent-network alternative for routine maintenance; orchestrator picks
- Travel Channel (HOM-15 ground mobility) handles in-trip vehicle/rideshare
