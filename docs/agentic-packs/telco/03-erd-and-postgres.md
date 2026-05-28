# 03 — ERD & Postgres Reference Schema

> A logical ERD and a reference PostgreSQL implementation. Designed around the "personal data vault per household" requirement: every household's data is isolated by **Row-Level Security** at the database engine, with a shared catalog layer for devices, products, and agents that all tenants benefit from.

The Mermaid version of this ERD lives at [`diagrams/mermaid-erd.md`](./diagrams/mermaid-erd.md).

## 1. Logical layers

| Layer | Tables | Purpose |
|---|---|---|
| Tenancy / identity | `household`, `person`, `vault`, `consent` | Customer, members, vault root, granular data permissions |
| Device catalog (shared) | `device_category`, `device_model`, `capability` | Manufacturer-agnostic taxonomy (Matter / Thread aware) |
| Device instances (per tenant) | `device`, `data_stream` | Physical units the customer owns |
| Telemetry (time-series) | `telemetry_event` | Raw signal; partitioned, JSONB payload |
| Domain projections | `inventory_item`, `inventory_snapshot`, `purchase_history`, `energy_reading`, `health_metric` | Derived / normalized views for agents |
| Product / vendor | `product`, `vendor`, `vendor_integration` | UPC lookup, OAuth tokens for grocers / utilities |
| Agentic layer | `agent`, `agent_dependency`, `agent_subscription`, `agent_run`, `agent_action`, `context_embedding` | Orchestrator + sub-agents + execution log |
| Commerce | `subscription_plan`, `billing_event` | Telco billing integration |

## 2. Extensions

```sql
CREATE EXTENSION IF NOT EXISTS "pgcrypto";        -- UUIDs, encryption
CREATE EXTENSION IF NOT EXISTS "timescaledb";     -- time-series hypertables
CREATE EXTENSION IF NOT EXISTS "vector";          -- pgvector for agent memory
CREATE EXTENSION IF NOT EXISTS "pg_partman";      -- automatic partition mgmt
CREATE EXTENSION IF NOT EXISTS "citext";          -- case-insensitive email
```

## 3. Tenancy & identity

```sql
CREATE TABLE household (
    household_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    telco_account  TEXT UNIQUE NOT NULL,
    address        JSONB,
    created_at     TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE person (
    person_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id   UUID REFERENCES household ON DELETE CASCADE,
    full_name      TEXT,
    role           TEXT CHECK (role IN ('primary','adult','child','dependent','guest')),
    dob            DATE,
    email          CITEXT,
    phone          TEXT
);

CREATE TABLE vault (
    vault_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id   UUID UNIQUE REFERENCES household ON DELETE CASCADE,
    cloud_provider TEXT,                  -- 'aws','azure','gcp','telco-edge'
    bucket_uri     TEXT,                  -- s3://vault-<hh>/
    kms_key_arn    TEXT,                  -- customer-managed key
    created_at     TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE consent (
    consent_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id   UUID REFERENCES household ON DELETE CASCADE,
    person_id      UUID REFERENCES person,
    scope          TEXT NOT NULL,         -- 'health','location','purchases','video'
    purpose        TEXT NOT NULL,         -- 'grocery-agent','energy-agent'
    granted        BOOLEAN DEFAULT TRUE,
    granted_at     TIMESTAMPTZ DEFAULT now(),
    revoked_at     TIMESTAMPTZ
);
```

## 4. Device catalog & instances

```sql
CREATE TABLE device_category (
    category_id    SERIAL PRIMARY KEY,
    name           TEXT UNIQUE NOT NULL,   -- 'refrigerator','thermostat','wearable'
    parent_id      INT REFERENCES device_category
);

CREATE TABLE device_model (
    model_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_id    INT REFERENCES device_category,
    manufacturer   TEXT,
    model_number   TEXT,
    protocol       TEXT[],                 -- {'matter','zigbee','wifi','ble'}
    UNIQUE (manufacturer, model_number)
);

CREATE TABLE capability (
    capability_id  SERIAL PRIMARY KEY,
    code           TEXT UNIQUE NOT NULL,   -- 'temp.read','door.state','image.capture'
    unit           TEXT,                   -- 'celsius','kwh','bpm'
    data_type      TEXT                    -- 'numeric','enum','image','json'
);

CREATE TABLE device_model_capability (
    model_id       UUID REFERENCES device_model ON DELETE CASCADE,
    capability_id  INT REFERENCES capability,
    PRIMARY KEY (model_id, capability_id)
);

CREATE TABLE device (
    device_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id   UUID REFERENCES household ON DELETE CASCADE,
    model_id       UUID REFERENCES device_model,
    friendly_name  TEXT,                   -- "Kitchen Fridge"
    location       TEXT,                   -- "kitchen","garage"
    serial_number  TEXT,
    installed_at   TIMESTAMPTZ,
    last_seen      TIMESTAMPTZ,
    status         TEXT DEFAULT 'active'
);
CREATE INDEX ON device (household_id);

CREATE TABLE data_stream (
    stream_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    device_id      UUID REFERENCES device ON DELETE CASCADE,
    capability_id  INT REFERENCES capability,
    sample_rate_s  INT,
    UNIQUE (device_id, capability_id)
);
```

## 5. Time-series telemetry (TimescaleDB)

```sql
CREATE TABLE telemetry_event (
    event_time     TIMESTAMPTZ NOT NULL,
    stream_id      UUID NOT NULL REFERENCES data_stream,
    household_id   UUID NOT NULL,          -- denormalized for RLS + partition pruning
    numeric_value  DOUBLE PRECISION,
    text_value     TEXT,
    payload        JSONB,                  -- raw vendor payload
    quality        SMALLINT DEFAULT 100    -- 0-100 confidence
);
SELECT create_hypertable('telemetry_event','event_time',
        chunk_time_interval => INTERVAL '1 day');
SELECT add_dimension('telemetry_event','household_id', number_partitions => 16);
CREATE INDEX ON telemetry_event (household_id, stream_id, event_time DESC);

-- Retention: keep raw 90 days, then roll up
SELECT add_retention_policy('telemetry_event', INTERVAL '90 days');
```

## 6. Domain projections

```sql
CREATE TABLE product (
    product_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    upc          TEXT UNIQUE,
    name         TEXT,
    brand        TEXT,
    category     TEXT,
    pack_size    TEXT,
    attributes   JSONB                     -- nutrition, allergens, etc.
);

CREATE TABLE inventory_item (
    item_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id  UUID REFERENCES household ON DELETE CASCADE,
    device_id     UUID REFERENCES device,
    product_id    UUID REFERENCES product,
    quantity      NUMERIC,
    unit          TEXT,
    expires_on    DATE,
    first_seen    TIMESTAMPTZ DEFAULT now(),
    last_seen     TIMESTAMPTZ DEFAULT now(),
    confidence    NUMERIC
);
CREATE INDEX ON inventory_item (household_id, product_id);

CREATE TABLE purchase_history (
    purchase_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id  UUID REFERENCES household ON DELETE CASCADE,
    vendor_id     UUID,
    product_id    UUID REFERENCES product,
    quantity      NUMERIC,
    unit_price    NUMERIC,
    purchased_at  TIMESTAMPTZ
);

CREATE TABLE energy_reading (
    household_id  UUID NOT NULL,
    device_id     UUID,
    read_time     TIMESTAMPTZ NOT NULL,
    kwh           NUMERIC,
    cost_usd      NUMERIC
);
SELECT create_hypertable('energy_reading','read_time');

CREATE TABLE health_metric (
    person_id     UUID NOT NULL REFERENCES person,
    household_id  UUID NOT NULL,
    metric_time   TIMESTAMPTZ NOT NULL,
    metric_code   TEXT,                    -- 'hr','spo2','glucose','steps','sleep_score'
    value         NUMERIC,
    unit          TEXT
);
SELECT create_hypertable('health_metric','metric_time');
```

## 7. Vendor & integration

```sql
CREATE TABLE vendor (
    vendor_id     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name          TEXT,
    type          TEXT,                    -- 'grocer','utility','pharmacy','telematics'
    api_base_url  TEXT
);

CREATE TABLE vendor_integration (
    integration_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id   UUID REFERENCES household ON DELETE CASCADE,
    vendor_id      UUID REFERENCES vendor,
    oauth_token    BYTEA,                  -- encrypted with pgcrypto
    refresh_token  BYTEA,
    expires_at     TIMESTAMPTZ,
    scopes         TEXT[]
);
```

## 8. Agentic layer

```sql
CREATE TABLE agent (
    agent_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code          TEXT UNIQUE,             -- 'grocery','energy','eldercare','orchestrator'
    name          TEXT,
    version       TEXT,
    role          TEXT CHECK (role IN ('orchestrator','sub-agent')),
    description   TEXT,
    model_ref     TEXT                     -- 'claude-opus-4-7', etc.
);

CREATE TABLE agent_dependency (
    agent_id      UUID REFERENCES agent ON DELETE CASCADE,
    capability_id INT REFERENCES capability,
    required      BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (agent_id, capability_id)
);

CREATE TABLE agent_subscription (
    subscription_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id    UUID REFERENCES household ON DELETE CASCADE,
    agent_id        UUID REFERENCES agent,
    plan_id         UUID,
    status          TEXT,                  -- 'active','paused','cancelled'
    started_at      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE agent_run (
    run_id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id   UUID NOT NULL,
    agent_id       UUID REFERENCES agent,
    parent_run_id  UUID REFERENCES agent_run,
    trigger        TEXT,                   -- 'schedule','event','user'
    started_at     TIMESTAMPTZ DEFAULT now(),
    finished_at    TIMESTAMPTZ,
    status         TEXT,
    cost_usd       NUMERIC
);

CREATE TABLE agent_action (
    action_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    run_id         UUID REFERENCES agent_run ON DELETE CASCADE,
    action_type    TEXT,                   -- 'order_grocery','adjust_thermostat'
    target         JSONB,                  -- {"vendor":"instacart","cart":[...]}
    state          TEXT,                   -- 'proposed','user-approved','executed','failed'
    executed_at    TIMESTAMPTZ
);

CREATE TABLE context_embedding (
    embedding_id   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id   UUID NOT NULL,
    source_table   TEXT,
    source_id      UUID,
    embedding      VECTOR(1536),
    created_at     TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX ON context_embedding USING ivfflat (embedding vector_cosine_ops);
```

## 9. Commerce

```sql
CREATE TABLE subscription_plan (
    plan_id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code          TEXT UNIQUE,             -- 'agent-grocery-basic'
    monthly_price NUMERIC,
    included_runs INT
);

CREATE TABLE billing_event (
    event_id      UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    household_id  UUID REFERENCES household,
    plan_id       UUID REFERENCES subscription_plan,
    amount        NUMERIC,
    occurred_at   TIMESTAMPTZ DEFAULT now()
);
```

## 10. The private-vault enforcement — Row-Level Security

This is the piece that makes the Telco pitch defensible vs. Big Tech. Every tenant-scoped table enforces isolation at the database engine, not at the application layer:

```sql
ALTER TABLE telemetry_event   ENABLE ROW LEVEL SECURITY;
ALTER TABLE inventory_item    ENABLE ROW LEVEL SECURITY;
ALTER TABLE health_metric     ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_run         ENABLE ROW LEVEL SECURITY;
-- repeat for all tenant tables

CREATE POLICY tenant_isolation ON telemetry_event
    USING (household_id = current_setting('app.current_household')::uuid);
```

The application sets `SET LOCAL app.current_household = '<uuid>'` at the start of every request / agent run — no cross-tenant leakage is possible even with a bug at the app layer.

## 11. Recommended physical architecture

| Concern | Recommendation |
|---|---|
| Hot telemetry | TimescaleDB hypertables, 90-day raw retention, continuous aggregates for daily / hourly rollups |
| Cold archive | Move chunks > 90 days to S3 / Glacier in the customer's vault (Timescale tiered storage) |
| Per-tenant isolation | Single DB + RLS for scale; optional per-tenant schema for premium tiers |
| Encryption | `pgcrypto` for OAuth tokens; TDE at rest; customer-held KMS key for the vault bucket |
| Agent memory | `pgvector` for episodic memory and retrieval-augmented context |
| Edge collection | Lightweight collector on the Telco gateway / ONT publishes to MQTT → Kafka → Postgres |
| Schema evolution | JSONB payload column absorbs new device fields without migrations |

## 12. Mapping to APEX Bronze / Silver / Gold

This Postgres reference schema is the **operational store**. Inside the APEX medallion, it is hydrated **from** Bronze landings and **projects into** Silver canonical entities and Gold virtual views. See [`04-medallion-bronze-silver-gold.md`](./04-medallion-bronze-silver-gold.md) for the full crosswalk.
