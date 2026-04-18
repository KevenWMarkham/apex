# Companion 02 — Medallion & SOR Integration

**APEX Core v1.2 · Developer Guide v1.0 · 2026-04-18**

> **Parent:** [`APEX-developer-guide.md`](../APEX-developer-guide.md) · **Previous:** [01 Fabric Layering](./01-fabric-layering.md) · **Next:** [03 MCP Servers](./03-mcp-servers.md)

---

## TL;DR

APEX mandates a **three-tier Medallion** where Bronze holds SOR-shape data, Silver holds canonical tokenised contract-compliant data, and Gold holds materialised feature views that agents read through MCP tools. The Silver canonical schemas (SCML, MERML, CXML, HLSCML, ERCML, AXLECML) are the contract between your ingest pipeline and every agent; get Silver right and the rest follows.

**What you'll leave with:**
- A complete picture of ingest pattern choice (stream / batch / REST / CDC)
- The five universal envelope fields every Silver row carries
- PII tokenisation, SCD2, and schema-evolution patterns
- Four worked examples — one per practice — showing Bronze DDL → Silver PySpark → Gold T-SQL
- A SOR-to-Service matrix showing which services depend on which SOR connections

---

## 1. The three layers in APEX terms

| Layer | Shape | Retention | Who writes | Who reads |
|---|---|---|---|---|
| **Bronze** | SOR-native (whatever the source sent) | 30–90 d typical | Ingest pipelines (stream / batch / REST / CDC) | Silver transforms only |
| **Silver** | Canonical — matches `schemas.manifest.json` contract; PII tokenised | 7+ years (domain-dependent) | Silver transforms (PySpark notebooks) | Gold views; compliance queries; rare direct-read via MCP |
| **Gold** | Materialised feature views — shape tuned for agent reads | 90 d rolling (cache-style) | Gold view DDL (T-SQL) / refresh pipelines | MCP tools only |

### Why the layers exist

- **Bronze** exists to **decouple ingest availability from transformation.** If the SOR goes down or the transform has a bug, you haven't lost the source data.
- **Silver** exists to **enforce the contract once, canonically.** Agents don't know whether you got data from Manhattan WMS or SAP EWM — they see `MERML.STORE_INVENTORY_POSITION` and that's it.
- **Gold** exists to **meet agent SLOs.** Agents have 500 ms read budgets. You cannot meet that against raw Silver joins. Gold is pre-joined, pre-aggregated, refresh-cadenced.

---

## 2. Ingest pattern choice

Pick the one that fits the SOR's data emission:

| SOR emits data as… | Ingest pattern | Fabric item |
|---|---|---|
| Kafka / Event Hubs / MQTT stream | **Stream** | Eventstream |
| SQL Server / Cosmos DB / Snowflake table with CDC | **CDC** | Mirrored Database |
| Nightly CSV / EDI / extract file | **Batch** | Data Pipeline (Copy Activity + notebooks) |
| REST API (pull) | **REST pull** | Dataflow Gen2 |
| Webhook (push) | **Webhook → Eventstream** | Custom endpoint → Eventstream |

### Latency budgets (p95, end-to-end SOR → Silver ready)

| Pattern | Budget | Notes |
|---|---|---|
| Stream | **< 60 s** | Eventstream + Delta sink has ~30 s min latency floor |
| CDC | **< 90 s** | Mirrored DB refresh cadence |
| Batch | *defined by schedule* | Typically 15 min, 1 h, or nightly |
| REST pull | *defined by schedule* | Dataflow Gen2 min 15 min |

If your service SLO is `detection_p95_sec ≤ 60`, only **stream** and (sometimes) **CDC** qualify. Choose accordingly; don't promise latency you can't keep.

---

## 3. Silver canonicalisation — the contract

### 3.1 The five universal envelope fields

Every Silver row (except lookup/reference tables) carries these five fields. They are **not optional**. They are validated by `schema-manifest-contract.json`.

| Field | Type | Purpose |
|---|---|---|
| `event_id` | string (UUID or opaque) | Globally unique; idempotency key |
| `event_ts` | timestamp (UTC) | When the logical event happened |
| `entity_id` | string | The primary entity the event is about (store_id, patient_id, meter_id, etc.) |
| `source_system` | string (enum) | Which SOR this came from (`MANHATTAN-WMS`, `EPIC-EHR`, `MONNIT-IOT`, `SAP-ISU`, `PLEX-MES`) |
| `source_system_ts` | timestamp (UTC) | When the SOR stamped it (may differ from `event_ts` for replayed events) |

Plus the contract may require one or both of:
- `pii_tokenized` (boolean) — true iff any PII column in this row was tokenised
- `scd2_current` (boolean) — true iff this is the current row in a SCD2 history (only on slow dimensions)

### 3.2 PII tokenisation at the Silver boundary

**Rule:** cleartext PII never crosses from Bronze to Silver. If it does, it's a contract violation (rule `MANIFEST-PII-CLEARTEXT-LEAK`).

Tokenisation is done in the Silver transform. The tokeniser is a stateful service (Fabric-hosted or external) that:
1. Maps `patient@example.com` → `CUST-TKN-00-8f3a` (stable, reversible only with audit)
2. Logs the unlock event in `apex_audit_log` if ever reversed
3. Honours `consent_contact` flags — if the customer has withdrawn contact consent, the token remains but the reverse-lookup is denied

**Example (Python / PySpark):**

```python
# apex-rc/notebooks/silver/tokenize_customer_incident.py
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType
from apex_tokenizer import Tokenizer

tokenizer = Tokenizer(audience="apex-rc-prod")
tokenize = udf(lambda v: tokenizer.tokenize(v, category="customer_id"), StringType())

bronze = spark.read.table("bronze_customer_incident")
silver = (bronze
    .withColumn("customer_id",      tokenize(col("raw_customer_email")))
    .withColumn("pii_tokenized",    lit(True))
    .withColumn("event_id",         expr("uuid()"))
    .withColumn("event_ts",         col("received_ts"))
    .withColumn("entity_id",        col("store_id"))
    .withColumn("source_system",    lit("CUSTOMER-INCIDENT-PORTAL"))
    .withColumn("source_system_ts", col("portal_received_ts"))
    .drop("raw_customer_email", "raw_customer_phone"))

silver.write.mode("append").saveAsTable("silver_customer_incident")
```

**Example (C# / Azure Function worker):**

```csharp
// apex-rc/mcp/tokenizer/TokenizeWorker.cs
using ApexTokenizer;

public class TokenizeWorker(ITokenizer tokenizer)
{
    public async Task<SilverCustomerIncident> TokenizeAsync(BronzeCustomerIncident src)
    {
        return new SilverCustomerIncident {
            CustomerId      = await tokenizer.TokenizeAsync(src.RawCustomerEmail, "customer_id"),
            PiiTokenized    = true,
            EventId         = Guid.NewGuid().ToString(),
            EventTs         = src.ReceivedTs,
            EntityId        = src.StoreId,
            SourceSystem    = "CUSTOMER-INCIDENT-PORTAL",
            SourceSystemTs  = src.PortalReceivedTs,
            TierClass       = src.TierClass
            // raw_customer_email intentionally dropped
        };
    }
}
```

### 3.3 SCD2 for slowly-changing dimensions

Slowly-changing Silver tables (stores, employees, suppliers, products-at-tenant) are SCD2:

```sql
-- silver_store_master — SCD2
CREATE TABLE silver_store_master (
    store_id        STRING,
    store_name      STRING,
    region          STRING,
    format          STRING,
    -- SCD2 housekeeping:
    effective_from  TIMESTAMP,
    effective_to    TIMESTAMP,     -- '9999-12-31' if current
    scd2_current    BOOLEAN,
    -- envelope:
    event_id        STRING,
    source_system   STRING
) USING DELTA;
```

Every change inserts a new row, ends the previous current row's interval, and flips `scd2_current`.

---

## 4. Gold feature views — the agent read surface

### 4.1 Shape rules

- **Pre-joined.** Agents cannot pay join cost at read time. If the agent needs store + reefer + product data, the Gold view pre-joins them.
- **Materialised.** T-SQL views with `REFRESH` cadence (Fabric supports this via scheduled pipelines). No on-demand compute.
- **Latency-budgeted.** p95 read time ≤ 500 ms. Measure it; if you're over, denormalise more.
- **Versioned.** `gold_cold_chain_state_v1` / `_v2`. Never mutate a view in place; agents pin.
- **Narrow.** Include only the columns the agent uses. An agent that reads 50 columns "just in case" is an anti-pattern.

### 4.2 Example Gold view

```sql
-- apex-rc/ddl/gold/gold_cold_chain_state_v1.sql
CREATE VIEW gold_cold_chain_state_v1 AS
SELECT
    t.entity_id                          AS store_id,
    t.sensor_id,
    t.lot_id,
    t.payload:temp_f::DECIMAL(5,2)       AS current_temp_f,
    t.payload:threshold_f::DECIMAL(5,2)  AS threshold_f,
    CASE WHEN t.payload:temp_f::DECIMAL > t.payload:threshold_f::DECIMAL
         THEN TRUE ELSE FALSE END        AS is_breaching,
    s.store_name,
    s.region,
    i.units_on_hand,
    i.retail_value_usd
FROM silver_cold_chain_telemetry t
JOIN silver_store_master         s  ON s.store_id = t.entity_id AND s.scd2_current
LEFT JOIN silver_store_inventory_position i
                                    ON i.store_id = t.entity_id AND i.lot_id = t.lot_id
WHERE t.event_ts > DATEADD(hour, -24, SYSUTCDATETIME());
```

Agents then hit this view via the `fabric-mcp.read_cold_chain_state` tool, never the Silver tables underneath.

---

## 5. Worked examples — multi-industry composite

### 5.1 RC — Manhattan WMS → MERML.STORE_INVENTORY_POSITION (batch CDC)

**Bronze.** Mirrored Database from Manhattan SQL Server CDC:
```sql
-- table arrives via Mirrored DB, no DDL here — Fabric manages it
-- mirror target: bronze_manhattan_inventory_snapshot
```

**Silver (PySpark):**
```python
# apex-rc/notebooks/silver/merml_store_inventory_position.py
from pyspark.sql.functions import col, expr, lit

bronze = spark.read.table("bronze_manhattan_inventory_snapshot")
silver = (bronze
    .withColumn("event_id",          expr("uuid()"))
    .withColumn("event_ts",          col("snapshot_ts"))
    .withColumn("entity_id",         col("store_id"))
    .withColumn("source_system",     lit("MANHATTAN-WMS"))
    .withColumn("source_system_ts",  col("wms_ts"))
    .withColumn("pii_tokenized",     lit(False))
    .withColumn("on_shelf",          col("units_on_shelf").cast("int"))
    .withColumn("in_backroom",       col("units_in_backroom").cast("int"))
    .withColumn("on_hand",           col("units_on_shelf") + col("units_in_backroom"))
    .select("event_id","event_ts","entity_id","source_system","source_system_ts",
            "pii_tokenized","store_id","product_id","on_hand","on_shelf","in_backroom"))

silver.write.mode("append").saveAsTable("silver_store_inventory_position")
```

**Gold (T-SQL):**
```sql
CREATE VIEW gold_store_inventory_current_v1 AS
SELECT store_id, product_id, on_hand, on_shelf, in_backroom, event_ts
FROM   silver_store_inventory_position
QUALIFY ROW_NUMBER() OVER (PARTITION BY store_id, product_id ORDER BY event_ts DESC) = 1;
```

### 5.2 HLS — Epic EHR → HLSCML.PATIENT_ENCOUNTER (CDC via Mirrored DB, PHI tokenised)

**Silver (Python, abbreviated):**
```python
# apex-hls/notebooks/silver/hlscml_patient_encounter.py
from apex_tokenizer import Tokenizer
tokenize = Tokenizer(audience="apex-hls-prod", phi=True)

bronze = spark.read.table("bronze_epic_encounter_cdc")
silver = (bronze
    .withColumn("patient_id_tkn",    tokenize_udf(col("mrn"), lit("patient_id")))
    .withColumn("event_id",          col("epic_encounter_id"))
    .withColumn("event_ts",          col("encounter_start_ts"))
    .withColumn("entity_id",         col("patient_id_tkn"))
    .withColumn("source_system",     lit("EPIC-EHR"))
    .withColumn("source_system_ts",  col("cdc_ts"))
    .withColumn("pii_tokenized",     lit(True))
    .drop("mrn","patient_name","dob")
)
silver.write.mode("append").saveAsTable("silver_patient_encounter")
```

**Why CDC?** Epic provides CDC via their Clarity/Caboodle export. Mirror that into Fabric. Real-time-ish encounter events (ADT) come via a separate HL7 FHIR Eventstream into a different Silver table.

### 5.3 ER — SAP ISU → ERCML.METER_READING (batch via Pipeline)

**Batch Pipeline (PySpark orchestrated by a scheduled Data Pipeline):**
```python
# apex-er/notebooks/silver/ercml_meter_reading.py
# ISU sends a flat file to OneLake landing; pipeline runs hourly.

bronze = spark.read.option("header",True).csv("Files/landing/isu_meter_readings/*.csv")
silver = (bronze
    .withColumn("event_id",          expr("uuid()"))
    .withColumn("event_ts",          to_timestamp("read_timestamp","yyyy-MM-dd'T'HH:mm:ssX"))
    .withColumn("entity_id",         col("meter_number"))
    .withColumn("source_system",     lit("SAP-ISU"))
    .withColumn("source_system_ts",  col("isu_export_ts"))
    .withColumn("pii_tokenized",     lit(False))
    .withColumn("reading_kwh",       col("kwh_value").cast("decimal(12,3)"))
    .withColumn("read_type",         col("reading_type")))

silver.write.mode("append").saveAsTable("silver_meter_reading")
```

### 5.4 AXLE — Plex MES → AXLECML.PRODUCTION_EVENT (Eventstream)

**Eventstream to Bronze** — no code; configured in Fabric UI.

**Silver (PySpark):**
```python
# apex-axle/notebooks/silver/axlecml_production_event.py
bronze = spark.readStream.table("bronze_plex_production_events")
silver = (bronze
    .withColumn("event_id",          col("plex_event_id"))
    .withColumn("event_ts",          col("event_timestamp"))
    .withColumn("entity_id",         col("line_id"))
    .withColumn("source_system",     lit("PLEX-MES"))
    .withColumn("source_system_ts",  col("plex_received_ts"))
    .withColumn("pii_tokenized",     lit(False))
    .withColumn("units_produced",    col("count_good").cast("int"))
    .withColumn("units_scrapped",    col("count_scrap").cast("int"))
    .withColumn("cycle_time_sec",    col("cycle_ms") / 1000))

(silver.writeStream
    .outputMode("append")
    .option("checkpointLocation","Files/checkpoints/axlecml_production_event")
    .toTable("silver_production_event"))
```

---

## 6. Schema evolution & bump classification

### 6.1 The one question that matters

*"Is this change MAJOR, MINOR, or PATCH?"*

| Change | Bump | Reason |
|---|---|---|
| Add a new column (nullable) | **MINOR** | Additive, no existing consumer breaks |
| Rename a column | **MAJOR** | Every consumer must update |
| Remove a column | **MAJOR** | Consumers referencing it fail |
| Change a column's type (widening, e.g. INT→BIGINT) | **MINOR** | Backwards-compatible read |
| Change a column's type (narrowing) | **MAJOR** | Data loss risk |
| Add an enum value | **MINOR** | Consumers must handle unknown values already |
| Remove an enum value | **MAJOR** | Can't know if consumers still produce it |
| Change primary key | **MAJOR** | Join semantics change |
| Add a new entity | **MINOR** | New table; existing consumers unaffected |
| Remove an entity | **MAJOR** | Consumers break |
| Metadata only (comment, description) | **PATCH** | No functional change |
| Reclassify PII | **MAJOR** | New tokenisation required; downstream masking changes |

### 6.2 Running the classifier

```bash
# after editing schemas.manifest.json
node apex-core/tools/apex-validate.js --schemas apex-rc/data/schemas.manifest.json
node apex-core/tools/classify-bump.js \
    --before HEAD~1:apex-rc/data/schemas.manifest.json \
    --after  apex-rc/data/schemas.manifest.json
```

Output:
```
MINOR — 1 entity added: SCML.COLD_CHAIN_TELEMETRY_V2
      — 0 breaking changes
      — gate map: MINOR → ACK_ONLY (default); override via tenant policy
```

### 6.3 Migration patterns

- **Additive (MINOR).** Write the Silver transform to populate the new column; backfill in a batch job; notify tenants via ACK_ONLY.
- **Breaking (MAJOR).** Ship both old and new shapes in parallel for one edition. Pin consumers. Deprecate the old shape with a timeline.
- **PII reclassification (MAJOR).** Re-tokenise affected columns; issue a Purview label update; audit the re-tokenisation event.

---

## 7. SOR → Service matrix

Which services break if a given SOR connection goes dark:

| SOR | Services that depend on it |
|---|---|
| **Monnit IoT** | APEX-RC-CXP-01 (Cold Chain) |
| **Manhattan WMS** | APEX-RC-CXP-01, APEX-RC-RVD-02, APEX-RC-OSA-04, APEX-RC-BPX-06 |
| **ESL Gateway** | APEX-RC-ESL-03 |
| **POS** | APEX-RC-ESL-03, APEX-RC-SHK-07, APEX-RC-OSA-04 |
| **Customer Incident Portal** | APEX-RC-CXI-08, APEX-RC-RCL-05 |
| **FDA Recall Feed** | APEX-RC-RCL-05, APEX-HLS-SUP-04 |
| **Epic EHR (CDC)** | APEX-HLS-DSR-01, APEX-HLS-SEP-02, APEX-HLS-CTM-05, APEX-HLS-PSI-06 |
| **Epic EHR (ADT stream)** | APEX-HLS-SEP-02, APEX-HLS-DSR-01 |
| **Denial/837 feed** | APEX-HLS-RVC-03 |
| **Pharmacy inventory** | APEX-HLS-SUP-04 |
| **SAP ISU** | APEX-ER-MTR-01, APEX-ER-BIL-03 |
| **SCADA telemetry** | APEX-ER-GRD-02 |
| **Field Service (MS Field Service)** | APEX-ER-FWO-04 |
| **Regulatory feed (FERC / state PUCs)** | APEX-ER-REG-05 |
| **Plex MES** | APEX-AXLE-LDT-01, APEX-AXLE-QEX-02, APEX-AXLE-KPI-05 |
| **Quality system (SAP QM)** | APEX-AXLE-QEX-02, APEX-AXLE-RCL-04 |
| **Supplier portal / EDI** | APEX-AXLE-SCD-03, APEX-RC-RVD-02 |

A SOR outage is scoped to its dependent services — agents pinned to services on other SORs keep running. This is why the SOR-to-Service matrix is a runtime concern (App Insights dashboards include SOR-scoped health) not just a design doc.

---

## 8. Cross-references

- Fabric workspace setup: [Companion 01](./01-fabric-layering.md)
- How agents actually call Gold views through MCP: [Companion 03](./03-mcp-servers.md)
- What bumps trigger what gates: [Companion 04](./04-agent-lifecycle.md)
- Purview label application: [Companion 05](./05-observability-security.md)
- Fixture recording from real SORs: [Companion 06](./06-testing-topology.md)
- Which SORs each service needs: [Companion 07](./07-service-catalog.md)
