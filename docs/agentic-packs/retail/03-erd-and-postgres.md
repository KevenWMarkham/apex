# 03 — ERD & Postgres Extensions

> Extensions to the schema in [`../telco/03-erd-and-postgres.md`](../telco/03-erd-and-postgres.md). All new entities tenant-scoped, RLS-enforced.

## 1. New entities

```sql
-- Retail order — extends purchase_history with multi-retailer + order-level granularity
CREATE TABLE retail_order (
    order_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id    UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    person_id       UUID REFERENCES person,
    retailer_vendor_id UUID REFERENCES vendor,        -- walmart / target / costco / homedepot / etc.
    order_type      TEXT,                              -- 'pickup','delivery','in_store','digital'
    order_status    TEXT,                              -- 'draft','submitted','in_progress','ready','picked_up','delivered','cancelled'
    total_usd       NUMERIC,
    placed_at       TIMESTAMPTZ,
    ready_at        TIMESTAMPTZ,
    fulfilled_at    TIMESTAMPTZ
);

CREATE TABLE retail_order_line (
    line_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id        UUID REFERENCES retail_order ON DELETE CASCADE,
    household_id    UUID NOT NULL,
    product_id      UUID REFERENCES product,
    quantity        NUMERIC,
    unit_price_usd  NUMERIC,
    sponsored       BOOLEAN DEFAULT FALSE              -- Walmart Connect-style sponsored placement
);

-- Prescription — PHI-classified; Walmart Pharmacy + Walgreens + CVS + others
CREATE TABLE prescription (
    rx_id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id    UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    person_id       UUID REFERENCES person,
    pharmacy_vendor_id UUID REFERENCES vendor,
    rx_number_token TEXT,                              -- tokenised; never raw
    drug_name       TEXT,
    quantity        NUMERIC,
    refills_remaining INT,
    last_filled_at  TIMESTAMPTZ,
    next_due_at     TIMESTAMPTZ,
    status          TEXT,                              -- 'active','expired','transferred','cancelled'
    classification  TEXT DEFAULT 'phi'
);

-- Auto-service appointment — at Walmart TLE / Jiffy Lube / dealer
CREATE TABLE auto_service_appointment (
    appointment_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id    UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    vehicle_id      UUID,
    provider_vendor_id UUID REFERENCES vendor,        -- 'walmart-tle','jiffy-lube','toyota-dealer'
    service_type    TEXT,                              -- 'oil_change','tire_rotation','battery'
    scheduled_at    TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    status          TEXT,
    cost_usd        NUMERIC
);

-- Membership tier — Walmart+ / Costco / Sam's Club / Amazon Prime
CREATE TABLE membership_tier (
    membership_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id    UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    program_vendor_id UUID REFERENCES vendor,
    program_code    TEXT,                              -- 'walmart-plus','costco-gold','sams-plus','prime'
    tier            TEXT,
    annual_fee_usd  NUMERIC,
    renews_on       DATE,
    benefits_used   JSONB                              -- log of which benefits were used vs available
);

ALTER TABLE retail_order            ENABLE ROW LEVEL SECURITY;
ALTER TABLE retail_order_line       ENABLE ROW LEVEL SECURITY;
ALTER TABLE prescription            ENABLE ROW LEVEL SECURITY;
ALTER TABLE auto_service_appointment ENABLE ROW LEVEL SECURITY;
ALTER TABLE membership_tier         ENABLE ROW LEVEL SECURITY;
-- Standard tenant_isolation policy applied to all
```

## 2. New `vendor.type` values

```
'retailer-supercenter'      -- Walmart, Target
'retailer-wholesale-club'   -- Costco, Sam's Club
'retailer-electronics'      -- Best Buy
'retailer-home-improvement' -- Home Depot, Lowes
'pharmacy'                  -- (already exists; Walmart Pharmacy, CVS, Walgreens fit here)
'auto-service-chain'        -- Walmart TLE, Jiffy Lube, Firestone
```

## 3. Seed data — anchor + bench

```sql
INSERT INTO vendor (name, type) VALUES
  ('Walmart',           'retailer-supercenter'),
  ('Target',            'retailer-supercenter'),
  ('Costco',            'retailer-wholesale-club'),
  ('Sam''s Club',       'retailer-wholesale-club'),
  ('Best Buy',          'retailer-electronics'),
  ('Home Depot',        'retailer-home-improvement'),
  ('Lowes',             'retailer-home-improvement'),
  ('Walmart Pharmacy',  'pharmacy'),
  ('Walmart Health',    'pharmacy'),
  ('Walmart Auto Care', 'auto-service-chain');
```

## 4. New Gold views

- `gold.v_tmt_rtl_household_retail_360` — single household-level retail rollup
- `gold.v_tmt_rtl_prescription_state` — active prescriptions, PHI-classified, RLS-enforced
- `gold.v_tmt_rtl_errand_chain_proposal` — pending errand chains the orchestrator drafted

## 5. Cross-references

- Companion build-spec amendment: [`../../build-specs/apex-tmt-agentic-retail-amendment.md`](../../build-specs/apex-tmt-agentic-retail-amendment.md)
- Marketplace ERD: [`../_marketplace/03-erd-and-postgres.md`](../_marketplace/03-erd-and-postgres.md)
