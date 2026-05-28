# ERD — Telco Home Agentic

> Mermaid ER diagram for the logical schema in [`../03-erd-and-postgres.md`](../03-erd-and-postgres.md).

```mermaid
erDiagram
    HOUSEHOLD ||--o{ PERSON : "has members"
    HOUSEHOLD ||--o{ DEVICE : "owns"
    HOUSEHOLD ||--o{ VAULT : "owns 1 private vault"
    HOUSEHOLD ||--o{ CONSENT : "grants"
    HOUSEHOLD ||--o{ AGENT_SUBSCRIPTION : "subscribes to"
    HOUSEHOLD ||--o{ VENDOR_INTEGRATION : "links accounts"
    PERSON ||--o{ WEARABLE_PROFILE : "has"
    PERSON ||--o{ CONSENT : "individually grants"
    DEVICE_CATEGORY ||--o{ DEVICE_MODEL : "classifies"
    DEVICE_MODEL ||--o{ DEVICE : "instance of"
    DEVICE_MODEL ||--o{ CAPABILITY : "supports"
    DEVICE ||--o{ DATA_STREAM : "emits"
    DATA_STREAM ||--o{ TELEMETRY_EVENT : "produces (time-series)"
    DEVICE ||--o{ INVENTORY_ITEM : "tracks (fridge/pantry)"
    PRODUCT ||--o{ INVENTORY_ITEM : "identifies"
    PRODUCT ||--o{ PURCHASE_HISTORY : "appears in"
    VENDOR ||--o{ PURCHASE_HISTORY : "sold via"
    VENDOR ||--o{ VENDOR_INTEGRATION : "supports OAuth"
    AGENT ||--o{ AGENT_SUBSCRIPTION : "available as"
    AGENT ||--o{ AGENT_RUN : "executed as"
    AGENT_SUBSCRIPTION ||--o{ AGENT_RUN : "triggers"
    AGENT_RUN ||--o{ AGENT_ACTION : "proposes/executes"
    AGENT ||--o{ AGENT_DEPENDENCY : "requires capability"
    CAPABILITY ||--o{ AGENT_DEPENDENCY : "fulfills"
    AGENT_RUN ||--o{ CONTEXT_EMBEDDING : "produces (pgvector)"
    SUBSCRIPTION_PLAN ||--o{ AGENT_SUBSCRIPTION : "billed under"
    HOUSEHOLD ||--o{ BILLING_EVENT : "incurs"
```

## How to read this diagram

- **HOUSEHOLD** is the tenant root. Every tenant-scoped table has a `household_id` enforced by Row-Level Security.
- **DEVICE_CATEGORY**, **DEVICE_MODEL**, and **CAPABILITY** are the shared catalog — they are not tenant-scoped. The Matter device library populates them.
- **DEVICE** and **DATA_STREAM** are per-household instances of the shared catalog.
- **TELEMETRY_EVENT** is the time-series hypertable (TimescaleDB). All raw telemetry lands here; domain projections fan out from it.
- **AGENT** + **AGENT_DEPENDENCY** + **AGENT_SUBSCRIPTION** + **AGENT_RUN** + **AGENT_ACTION** form the agentic lineage — every household action is traceable end-to-end.
- **VAULT** is the per-household private-cloud root. The customer holds its KMS key.
