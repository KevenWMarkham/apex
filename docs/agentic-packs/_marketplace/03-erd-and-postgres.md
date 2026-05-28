# 03 — ERD & Postgres — Channel Registry

> The marketplace adds four shared tables to the schema introduced in [`../telco/03-erd-and-postgres.md`](../telco/03-erd-and-postgres.md): `channel`, `channel_subscription`, `channel_bundle`, `partner_directory`. All four are **shared catalog** tables, not tenant-scoped — they describe which Channels and bundles exist in the marketplace, not the customer's data.

## 1. New entities

```sql
-- Channel — the unit a customer subscribes to
CREATE TABLE channel (
    channel_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    channel_code     TEXT UNIQUE NOT NULL,                -- 'home','travel','retail-walmart','mobility-toyota','beverage-sazerac'
    category         TEXT NOT NULL,                       -- 'home','travel','retail','mobility','cpg','health','finance'
    operator         TEXT,                                -- 'telco-own','partner-walmart','partner-toyota','partner-sazerac'
    name             TEXT,
    description      TEXT,
    service_code_prefix TEXT,                             -- 'TMT-TEL-HOM','TMT-TEL-RTL', etc.
    status           TEXT CHECK (status IN ('planned','beta','live','deprecated','retired')),
    launched_at      TIMESTAMPTZ,
    retired_at       TIMESTAMPTZ
);

-- Channel subscription — household subscribes to a channel
CREATE TABLE channel_subscription (
    subscription_id  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id     UUID NOT NULL REFERENCES household ON DELETE CASCADE,
    channel_id       UUID REFERENCES channel,
    plan_id          UUID REFERENCES subscription_plan,
    status           TEXT,                                -- 'active','paused','cancelled','trial'
    monthly_price_usd NUMERIC,
    bundle_id        UUID REFERENCES channel_bundle,       -- if this channel is part of a bundle
    started_at       TIMESTAMPTZ DEFAULT now(),
    ends_at          TIMESTAMPTZ
);
CREATE INDEX ON channel_subscription (household_id, status);

-- Channel bundle — Telco-curated bundles of channels
CREATE TABLE channel_bundle (
    bundle_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bundle_code      TEXT UNIQUE NOT NULL,                -- 'home-essential','home-family','travel-premium','full-marketplace'
    name             TEXT,
    monthly_price_usd NUMERIC,
    channel_ids      UUID[],                              -- channels included in this bundle
    discount_pct     NUMERIC,                             -- % discount vs sum of à-la-carte
    status           TEXT
);

-- Partner directory — every consumer brand listable on the marketplace
CREATE TABLE partner_directory (
    partner_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vendor_id        UUID REFERENCES vendor,
    legal_name       TEXT,
    brand_name       TEXT,                                -- 'American Airlines','Marriott','Walmart','Toyota','Sazerac'
    channel_ids      UUID[],                              -- which Channels this partner participates in
    onboarded_at     TIMESTAMPTZ,
    mcp_spec_version TEXT,                                -- 'apex.tmt.mcp.partner.v1','...v2'
    compliance_attestations JSONB,                       -- privacy, security, accessibility
    status           TEXT CHECK (status IN ('candidate','onboarding','live','suspended','offboarded'))
);

-- Channel-partner participation (M:N)
CREATE TABLE channel_partner_participation (
    channel_id       UUID REFERENCES channel ON DELETE CASCADE,
    partner_id       UUID REFERENCES partner_directory ON DELETE CASCADE,
    role             TEXT,                                -- 'anchor','bench','marketplace'
    PRIMARY KEY (channel_id, partner_id)
);
```

## 2. Seed data — channels

```sql
INSERT INTO channel (channel_code, category, operator, name, service_code_prefix, status, launched_at) VALUES
  ('home',                     'home',     'telco-own',         'Home',                     'TMT-TEL-HOM',     'live',    now()),
  ('travel',                   'travel',   'telco-own',         'Travel & Hospitality',     'TMT-TEL-HOM-10',  'beta',    now()),
  ('retail-walmart',           'retail',   'partner-walmart',   'Walmart Retail',           'TMT-TEL-RTL',     'planned', NULL),
  ('mobility-toyota',          'mobility', 'partner-toyota',    'Toyota Connected',         'TMT-TEL-MOB',     'planned', NULL),
  ('beverage-sazerac',         'cpg',      'partner-sazerac',   'Sazerac House',            'TMT-TEL-BEV',     'planned', NULL);
```

> The `travel` channel is technically scoped under `TMT-TEL-HOM-10..17` (a sub-family of the Home service codes) for historical reasons, but is registered as its own Channel in the marketplace.

## 3. Seed data — bundles

```sql
INSERT INTO channel_bundle (bundle_code, name, monthly_price_usd, channel_ids, discount_pct) VALUES
  ('home-essential',
   'Home Essential',
   9.99,
   ARRAY[(SELECT channel_id FROM channel WHERE channel_code='home')],
   0),
  ('home-family',
   'Home Family',
   19.99,
   ARRAY[(SELECT channel_id FROM channel WHERE channel_code='home')],
   0),
  ('travel-premium',
   'Travel Premium',
   14.99,
   ARRAY[(SELECT channel_id FROM channel WHERE channel_code='travel')],
   0),
  ('marketplace-everything',
   'Marketplace — Everything Bundle',
   49.99,
   ARRAY[
       (SELECT channel_id FROM channel WHERE channel_code='home'),
       (SELECT channel_id FROM channel WHERE channel_code='travel'),
       (SELECT channel_id FROM channel WHERE channel_code='retail-walmart'),
       (SELECT channel_id FROM channel WHERE channel_code='mobility-toyota'),
       (SELECT channel_id FROM channel WHERE channel_code='beverage-sazerac')
   ],
   33);
```

## 4. Seed data — anchor partners

```sql
INSERT INTO partner_directory (legal_name, brand_name, mcp_spec_version, status, onboarded_at) VALUES
  ('American Airlines, Inc.',         'American Airlines', 'apex.tmt.mcp.partner.v1', 'live',       now()),
  ('Marriott International, Inc.',    'Marriott',          'apex.tmt.mcp.partner.v1', 'live',       now()),
  ('Expedia Group, Inc.',             'Expedia',           'apex.tmt.mcp.partner.v1', 'live',       now()),
  ('Airbnb, Inc.',                    'Airbnb',            'apex.tmt.mcp.partner.v1', 'live',       now()),
  ('Walmart Inc.',                    'Walmart',           'apex.tmt.mcp.partner.v1', 'onboarding', NULL),
  ('Toyota Motor North America, Inc.','Toyota',            'apex.tmt.mcp.partner.v1', 'onboarding', NULL),
  ('Sazerac Company, Inc.',           'Sazerac',           'apex.tmt.mcp.partner.v1', 'onboarding', NULL);
```

## 5. RLS

`channel_subscription` is tenant-scoped and joins the existing RLS policy. The other tables (`channel`, `channel_bundle`, `partner_directory`, `channel_partner_participation`) are **shared catalog** — read-allowed for any authenticated agent context.

```sql
ALTER TABLE channel_subscription ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON channel_subscription
    USING (household_id = current_setting('app.current_household')::uuid);
```

## 6. Gold view — marketplace household view

```sql
CREATE OR ALTER VIEW gold.v_marketplace_household_view AS
SELECT
  cs.household_id,
  c.channel_code,
  c.name AS channel_name,
  c.category,
  c.operator,
  cs.status,
  cs.monthly_price_usd,
  cb.bundle_code,
  cs.started_at,
  -- engagement
  COUNT(ar.run_id) FILTER (WHERE ar.started_at > now() - INTERVAL '30 days') AS runs_30d,
  COUNT(aa.action_id) FILTER (WHERE aa.executed_at > now() - INTERVAL '30 days' AND aa.state='executed') AS actions_30d
FROM channel_subscription cs
JOIN channel c ON c.channel_id = cs.channel_id
LEFT JOIN channel_bundle cb ON cb.bundle_id = cs.bundle_id
LEFT JOIN agent_subscription asub ON asub.household_id = cs.household_id
LEFT JOIN agent_run ar ON ar.household_id = cs.household_id
LEFT JOIN agent_action aa ON aa.run_id = ar.run_id
GROUP BY cs.household_id, c.channel_code, c.name, c.category, c.operator,
         cs.status, cs.monthly_price_usd, cb.bundle_code, cs.started_at
;
```

This view is the **single household-level rollup** that drives the Customer Portal's "My Channels" tab and the Telco's marketplace-engagement dashboards.
