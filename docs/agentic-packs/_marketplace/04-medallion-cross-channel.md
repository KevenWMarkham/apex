# 04 — Medallion: Cross-Channel Patterns

> The medallion build does not change for the marketplace. What changes is the **discipline** with which each new Channel's pack follows the same Bronze / Silver / Gold conventions, so cross-channel measures and views compose without rework.

## 1. The cross-channel rule

Every Channel pack — Home, Travel, Retail, Mobility, CPG — follows the same Bronze envelope, the same Silver Pydantic entity pattern, the same Gold view convention with `MeasureDefinition` registration. This means:

- Bronze tables across Channels share `event_id, event_ts, entity_id, source_system, source_system_ts, ingest_ts, ingest_date, run_id, _raw_payload, _classification`
- Silver entities all expose `household_id` for RLS
- Gold views all stamp `view_definition_sha(ddl)` for audit
- All classifications (`internal`, `pii`, `phi`, `cpni`) propagate consistently

No Channel gets to invent its own Bronze envelope. No Channel gets to invent its own RLS strategy. No Channel gets to bypass the classification taxonomy.

## 2. Channel-specific Bronze prefixes

| Channel | Bronze schema |
|---|---|
| Home | `bronze.tmt_hom.*` |
| Travel | `bronze.tmt_hom.*` (sub-family — airline_pnr, hotel_reservation, etc.) |
| Retail | `bronze.tmt_rtl.*` |
| Mobility | `bronze.tmt_mob.*` |
| CPG / Beverage | `bronze.tmt_bev.*` |
| Health (future) | `bronze.tmt_hlt.*` |
| Finance (future) | `bronze.tmt_fin.*` |

Each Channel pack publishes its Bronze landings under its own schema. The orchestrator and cross-channel measures read across schemas with read-only Gold views.

## 3. Cross-channel measures

Some measures span Channels by design. These are registered in `packages/apex-medallion/src/apex_medallion/gold/marketplace_measures.py` and referenced by multiple Channel agents:

| Measure | Span | Consumed by |
|---|---|---|
| `household_rollup_state` | Home + Travel | Energy, security, eldercare, trip orchestrator |
| `marketplace_engagement_score` | All Channels | Marketplace retention agent, customer portal |
| `cross_channel_intent_routing_confidence` | Orchestrator | `HOM-99` orchestrator decisioning |
| `loyalty_portfolio_value_usd` | Travel + Retail | Travel concierges, retail membership optimizer |
| `multi_channel_churn_propensity` | All Channels | Marketplace retention agent |

## 4. Cross-channel views

Two Gold views serve marketplace-level surfaces:

```sql
-- Marketplace-level household view (see ../03-erd-and-postgres.md §6)
gold.v_marketplace_household_view

-- Cross-channel intent log
CREATE OR ALTER VIEW gold.v_marketplace_intent_log AS
SELECT
  ar.household_id,
  ar.run_id,
  ar.started_at,
  a.code AS agent_code,
  c.channel_code,
  ar.trigger,
  ar.status,
  ar.cost_usd
FROM agent_run ar
JOIN agent a ON a.agent_id = ar.agent_id
JOIN channel c ON c.service_code_prefix = SUBSTRING(a.code FROM 1 FOR POSITION('-' IN a.code) - 1)
;
```

## 5. Anti-patterns to avoid

| Anti-pattern | Why it breaks the marketplace |
|---|---|
| One Channel inventing its own envelope | Cross-channel measures can't join its Bronze cleanly |
| One Channel reading another Channel's raw Bronze | Tight coupling; orchestrator routes break |
| Cross-Channel writes without orchestrator routing | The orchestrator-routing audit trail goes opaque |
| Channel-specific tokenization that doesn't share KMS scope | Vault export becomes inconsistent across Channels |
| A Channel skipping classification stamps | Compliance posture breaks at the marketplace level |

The marketplace's coherence is **enforced by lint** (the `apex-validate.js` schema-manifest check) plus **enforced by review** (the Channel pack template requires explicit declaration of medallion conformance).

## 6. The classification matrix per Channel

| Channel | Predominant classifications |
|---|---|
| Home | `internal`, `pii`, `phi`, `cpni` |
| Travel | `pii`, `cpni` (loyalty + docs) |
| Retail | `pii`, with limited `phi` for pharmacy / health-adjacent products |
| Mobility | `pii`, with `cpni` for connected-vehicle SIM identity |
| CPG / Beverage | `pii` only — but **age-verification** flag requires a dedicated `age_verified` boolean stamped on bookings |
| Health (future) | `phi` predominant |
| Finance (future) | `pii` + GLBA-class identifiers |

The Telco's compliance team can plan Channel rollout against this matrix — `cpg` and `retail` are the lightest-touch Channels after Home; Health and Finance materially raise the compliance footprint.
