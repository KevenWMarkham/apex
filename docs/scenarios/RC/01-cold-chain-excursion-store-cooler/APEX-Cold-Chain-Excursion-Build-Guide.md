# APEX Build Guide — Cold-Chain Excursion (RC Scenario 01)

**Scenario anchor:** RC-E2E-03 + RC-E2E-09 · Cold-chain excursion, dairy case at Big Box Store 100
**Primary persona:** Marisol Reyes · Store Operations Lead
**Canonical trace:** `trc_2026-04-23_0608_bb100_a3`
**Design references:** APEX_Design.md §§4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 20
**Status:** Canonical build walkthrough · Wave 1 Foundation → Wave 2 Pilot → Wave 3 Scale & Fuse
**Date:** 2026-04-23 (v1.0)
**Audience:** Delivery Lead, Solution Architect, Platform Engineer, Practice Lead, RC Service Owner

---

## How to use this guide

This is an end-to-end, step-by-step build walkthrough for **one** scenario — Cold-Chain Excursion — taken from first client conversation through Wave 3 enterprise scale. It intentionally does not skip steps. Every architectural component that appears in the Flow tab of the APEX Stacked Architecture Narrated HTML is represented here with its concrete implementation.

Read linearly if you are a Delivery Lead onboarding to APEX. Use the table of contents below if you are an architect looking for a specific step.

Each step carries:
- **Purpose** — what the step produces
- **Inputs** — what must already exist
- **Outputs** — what the step creates
- **Owner** — role accountable
- **Estimated effort** — story points (SP) and calendar time
- **Exit criteria** — how we know the step is done

---

## Table of Contents

### Approach
1. [Addressing the scenario with the client](#1-addressing-the-scenario-with-the-client)
2. [Discovery — mapping scenario to canonical chain](#2-discovery--mapping-scenario-to-canonical-chain)
3. [SOR selection and schema discovery](#3-sor-selection-and-schema-discovery)

### Wave 1 — Foundation (prerequisites)
4. [W1.1 — Tenant manifest and landing zone](#4-w11--tenant-manifest-and-landing-zone)
5. [W1.2 — Real-Time Hub and Bronze landing](#5-w12--real-time-hub-and-bronze-landing)
6. [W1.3 — Tokenizer at the Bronze→Silver boundary](#6-w13--tokenizer-at-the-bronzesilver-boundary)
7. [W1.4 — Silver canonical schemas](#7-w14--silver-canonical-schemas)
8. [W1.5 — Gold agent-safe views](#8-w15--gold-agent-safe-views)
9. [W1.6 — MCP server integration](#9-w16--mcp-server-integration)
10. [W1.7 — Entra managed identities and visibility lattice](#10-w17--entra-managed-identities-and-visibility-lattice)
11. [W1.8 — LEDGER instantiation](#11-w18--ledger-instantiation)
12. [W1.9 — HITL surface templates](#12-w19--hitl-surface-templates)
13. [W1 Exit Gate](#13-w1-exit-gate)

### Wave 2 — Pilot (the scenario live)
14. [W2.1 — Event trigger wiring (Data Activator reflex)](#14-w21--event-trigger-wiring)
15. [W2.2 — Orchestration manifest (DAG)](#15-w22--orchestration-manifest)
16. [W2.3 — Agent 1 · Assess](#16-w23--agent-1--assess)
17. [W2.4 — Agent 2 · Classify (FSMA 204 policy)](#17-w24--agent-2--classify)
18. [W2.5 — Agent 3 · Quantify](#18-w25--agent-3--quantify)
19. [W2.6 — HITL gate moment (Marisol)](#19-w26--hitl-gate-moment)
20. [W2.7 — Agent 4 · Act (parallel downstream)](#20-w27--agent-4--act)
21. [W2.8 — KPI attribution and audit-row closeout](#21-w28--kpi-attribution-and-audit-row-closeout)
22. [W2 Exit Gate](#22-w2-exit-gate)

### Wave 3 — Scale & Fuse (enterprise + mesh)
23. [W3.1 — Tenant-scope expansion (250 → 2,400 stores)](#23-w31--tenant-scope-expansion)
24. [W3.2 — Fusion · Dynamic Markdown mesh](#24-w32--fusion--dynamic-markdown-mesh)
25. [W3.3 — Fusion · Loyalty Churn mesh](#25-w33--fusion--loyalty-churn-mesh)
26. [W3.4 — Purview trust at enterprise scale](#26-w34--purview-trust-at-enterprise-scale)
27. [W3.5 — LEDGER feedback loop → manifest evolution](#27-w35--ledger-feedback-loop)
28. [W3.6 — Enterprise KPI roll-up](#28-w36--enterprise-kpi-roll-up)
29. [W3 Exit Gate](#29-w3-exit-gate)

### Appendices
- [Appendix A — RACI by step](#appendix-a--raci-by-step)
- [Appendix B — Manifest inventory](#appendix-b--manifest-inventory)
- [Appendix C — Commercial envelope summary](#appendix-c--commercial-envelope-summary)

---

# Approach

## 1. Addressing the scenario with the client

### 1.1 Before the first client meeting

The Deloitte Account Team has pre-qualified that the client (e.g., "Big Box Store Co.") has a perishables-shrink problem and that cold-chain excursion response is manually triaged today. The Practice Lead confirms RC as the target Practice. The seller has the Stacked Architecture Narrated HTML open, Chains tab selected, RC practice group visible.

**Pre-meeting checklist:**

- [ ] Confirm client's annual perishables-shrink exposure (typical RC client: $30M–$80M/yr)
- [ ] Confirm cold-chain incidents/week (typical: 1–4 per store × store count)
- [ ] Confirm FSMA 204 compliance posture (is the client already on the FDA timeline for lot-traceability?)
- [ ] Confirm Microsoft-native posture (Azure tenant? Fabric presence? Entra ID as IdP?)
- [ ] Align on Independence language: APEX is Deloitte-delivered on Microsoft platform capabilities — never "partner/alliance"

### 1.2 The opening conversation

The seller walks the value-delivery chain **top-down** in this order:

1. **Scenario** — "Dairy case at Store 100 exceeds 41°F for 4h 12m. 412 units across 28 SKUs at risk. Manager must decide: sell-through, markdown, destroy. Today that decision takes 12 minutes. 65% of the shift goes to gathering info."
2. **Solution** — "An agentic perishables-integrity response. The agent fuses SKU-level elasticity with FSMA 204 lot provenance and proposes the action. Manager approves via Teams Adaptive Card in 90 seconds."
3. **Use Case** — "Excursion triage + markdown decisioning. Wave 2 at 250-store pilot."
4. **Service** — "RC-E2E-03 Assortment & Pricing + RC-E2E-09 Product Tracking. Commercial envelope per store tier."
5. **Persona** — "Primary: Store Operations Lead (Marisol Reyes). Secondary: Pull-Team Lead, Store Manager, Inventory Control, Refrigeration Vendor, Food Safety Compliance Lead."
6. **KPI** — "Manager time returned 5.2 hrs/shift. Shrink cost down 18%. Write-off avoided $1,313 per event. Audit-row attributed."

The architect walks the same chain **bottom-up** in technical conversations (KPI → Service → Use Case → Solution → Scenario). Chain direction is audience-driven; the chain itself is the same.

### 1.3 Framing the three Waves

After buy-in on the chain, the seller shows the Flow tab of the Stacked Architecture Narrated HTML and walks W1 → W2 → W3:

- **W1 Foundation (4–8 weeks, $500K–$2M)** — the rails. Schema projection, LEDGER instantiation, MCP tools, HITL surfaces. Not the scenario itself; what must be true before the scenario can run. One-time investment per tenant. Enables every subsequent scenario cheaply.
- **W2 Pilot (6–15 months, $5M–$15M)** — the scenario live at proof-point scale. 250 stores (NA pilot cluster), dairy + deli + produce fixtures. Goal: prove 5.2 hr/shift time-return and 18% shrink reduction with an auditable trace to each event. Decision gate at the end.
- **W3 Scale & Fuse (multi-year, $8M–$30M)** — same scenario, 2,400 stores, all fixture classes, fused with dynamic-markdown and loyalty-churn agents. Enterprise KPI aggregates to $42M/yr.

### 1.4 Outputs of the approach stage

- [ ] Signed executive sponsor agreement to pilot RC Cold-Chain Excursion
- [ ] Tenant name agreed (e.g., `bigbox`)
- [ ] Pilot store list agreed (typically 1 anchor store + expansion to 250)
- [ ] Commercial envelope range agreed for W1 + W2
- [ ] Practice Lead, Delivery Lead, Solution Architect, Governance Owner assigned on both sides
- [ ] Date locked for Discovery Workshop (Step 2)

---

## 2. Discovery — mapping scenario to canonical chain

### 2.1 Discovery Workshop (2-day on-site + 3 days follow-up)

**Attendees (client side):** Store Operations VP · Food Safety Compliance Lead · IT Enterprise Architect · Data & Analytics Lead · Refrigeration Vendor liaison · Finance Controller (perishables category) · one anchor-store GM (Marisol's equivalent)

**Attendees (Deloitte side):** Delivery Lead · Solution Architect · RC Practice Lead · Governance Owner · Data Engineer

**Day-1 agenda:**

- Morning — walk a real cold-chain excursion end-to-end on the anchor store's operational floor. Interview Marisol's equivalent. Capture current state exactly (no abstraction).
- Afternoon — map current state to the APEX canonical chain (Scenario → KPI). Identify all system touches (POS, ERP, refrigeration controller, WMS, pricing engine, vendor portal, email/Teams, phone, paper).

**Day-2 agenda:**

- Morning — map to canonical schemas and SORs (Step 3).
- Afternoon — confirm personas (primary + 3–5 secondary) with named people where possible.

**Follow-up (3 days):**

- Discovery write-up doc
- SOR shortlist with schema excerpts
- Target persona roster
- Gap analysis (what data is missing? what API is unavailable? what lot-traceability gap exists?)

### 2.2 Discovery deliverables

- [ ] `discovery-report-cold-chain.md` — narrative of current state vs canonical chain
- [ ] `sor-shortlist.md` — every system touched during current-state excursion response
- [ ] `persona-roster.md` — named primary + secondary personas
- [ ] `gap-analysis.md` — data gaps, API gaps, regulatory readiness gaps
- [ ] `success-criteria.md` — KPI targets signed by Store Operations VP + Food Safety Lead

---

## 3. SOR selection and schema discovery

### 3.1 Identify every System of Record touched

For Cold-Chain Excursion the SOR inventory is typically:

| SOR | Vendor (typical) | Role in scenario | Integration pattern | Canonical schema target |
|-----|------------------|------------------|---------------------|--------------------------|
| **Refrigeration Controller** | Emerson E2, Danfoss, Honeywell, Copeland | Temperature + door-open telemetry | OPC-UA or MQTT stream via Real-Time Hub | SCML.Fixture + SCML.SensorReading (new entities) |
| **POS** | NCR, Toshiba, Oracle Xstore | Sales velocity for markdown-impact modeling | Batch EOD to Eventhouse; real-time via Eventstream if available | MERML.Transaction |
| **ERP (receiving + inventory)** | SAP S/4HANA or Oracle Retail Suite | Lot-traceability (FSMA 204) + inventory position | Fabric Mirrored Database (CDC) | SCML.Lot + SCML.Inventory |
| **Price Master** | Oracle Retail Price, JDA, SAP Customer Activity Repository | Current shelf price + elasticity history | Data Pipeline daily refresh | MERML.Price + MERML.Elasticity |
| **Markdown Engine** | (often same as Price Master) | Markdown cadence history | Data Pipeline daily refresh | MERML.Markdown |
| **Loyalty / CRM** | Salesforce Commerce, Oracle CX, custom | Customer-transaction join for W3 fusion | Dataflow Gen2 (SaaS API) | CXML.LoyaltyMember + CXML.Transaction |
| **WMS / Store Inventory** | Manhattan Active, SAP EWM | Real-time shelf position | Mirrored Database | SCML.Inventory |
| **Refrigeration Vendor Portal** | ServiceChannel, Corrigo, Ecotrak | Service-ticket destination | Custom Endpoint (webhook) or REST | vendor-portal-mcp (External MCP) |
| **Teams** | Microsoft Teams | HITL surface for Marisol | Azure Communication Services SDK + approvals-mcp | — (Experience Plane) |
| **Power BI** | Microsoft Power BI | KPI dashboard for Store Operations VP | Direct Lake semantic model | Gold views |

### 3.2 Schema discovery per SOR

For each SOR, the data engineer runs schema introspection and maps source fields to canonical schemas.

**Refrigeration controller (Emerson E2 example):**

```
# Native stream schema (OPC-UA)
NodeId           : ns=2;s=BB100.DAIRY.A3.TempSensor.Value
BrowseName       : TempSensor_Value
DataType         : Float
Units            : degF
SampleRate       : 30 seconds

# Canonical target: SCML.SensorReading
sensor_id        : FIX_BB100_DAIRY_A3_TEMP
fixture_id       : FIX_BB100_DAIRY_A3
reading_type     : TEMPERATURE
value            : 48.2
unit             : degF
event_ts         : 2026-04-23T06:08:00.000Z
source_system    : emerson-e2-bb100
source_system_ts : 2026-04-23T06:08:00.000Z
```

**SAP ERP lot-traceability (example):**

```
# Native table: MARA (material master) + LQUA (quants) + MCHB (batch stock)
MATNR            : material number
CHARG            : batch/lot
LGORT            : storage location (= store + fixture)
MEINS            : base UoM
MHDAT            : expiration date
HERKL            : country of origin

# Canonical target: SCML.Lot (FSMA 204 bindings)
lot_id           : LOT_DAIRY_00479231
material_id      : MAT_SKU_DAIRY_1GAL_MILK
origin_facility  : FAC_MILK_PROD_PA_DAIRY_001
ship_to          : FAC_DC_NE_001 → FAC_BB100_STORE
gtin             : 00885310023457
expiry_date      : 2026-05-01
fsma_204_ctes    : [receiving, transformation, shipping]  -- Critical Tracking Events
kdes             : [receiving_ts, shipping_ts, temperature_on_receipt, ...]  -- Key Data Elements
```

### 3.3 Schema discovery deliverable

- [ ] `schema-mapping.md` — one table per SOR mapping native fields → canonical schema
- [ ] `schema-gap-analysis.md` — attributes the canonical schema expects but the SOR does not have
- [ ] `fsma-204-binding.md` — explicit CTE + KDE mapping against SCML.Lot

**Owner:** Solution Architect · Data Engineer
**Effort:** 8 SP (~2 weeks)
**Exit criteria:** Schema mapping signed by client's Enterprise Architect + Food Safety Compliance Lead

---

# Wave 1 — Foundation

W1 is the one-time investment per tenant. It makes the scenario possible and every subsequent scenario cheap.

**W1 total effort:** ~40 SP · 4–8 weeks · $500K–$2M commercial envelope
**W1 exit criteria:** every cell in Section 13 checked

---

## 4. W1.1 — Tenant manifest and landing zone

### 4.1 Purpose

Establish the tenant's isolation boundary in Azure and APEX. `bigbox` becomes a distinct resource set — its own Fabric workspace(s), its own Foundry project(s), its own Entra app registrations, its own Purview governance domain. APEX does **not** use multi-tenant logical isolation. Governance requires resource-level isolation.

### 4.2 Inputs

- [ ] Tenant name agreed (Step 1.4): `bigbox`
- [ ] Azure subscription identified (client's or Deloitte-delivery sub)
- [ ] Region(s) confirmed (typically one primary + one DR per regulatory residency)

### 4.3 Outputs

- [ ] Tenant manifest file: `apex-bigbox/tenants/bigbox.manifest.json`
- [ ] Azure landing zone provisioned
- [ ] Fabric capacity provisioned
- [ ] Foundry project provisioned
- [ ] Key Vault provisioned
- [ ] Private network established

### 4.4 Steps

**4.4.1 — Author the tenant manifest**

Example `bigbox.manifest.json`:

```json
{
  "manifest_kind": "tenant",
  "manifest_version": "1.0.0",
  "tenant_id": "bigbox",
  "tenant_display_name": "Big Box Store Co.",
  "practice_pin": {
    "practice_id": "rc",
    "edition_version": "v2.0.0"
  },
  "subscriptions": [
    { "service_id": "RC-E2E-03", "service_version": "v1.2.0" },
    { "service_id": "RC-E2E-09", "service_version": "v1.0.0" }
  ],
  "classifications": {
    "default": "INTERNAL",
    "lot_data": "INTERNAL",
    "customer_data": "CONFIDENTIAL"
  },
  "policies": {
    "markdown_authority_threshold_pct": 30,
    "destroy_authority_role": "store_ops_lead",
    "hitl_mode": "HITL"
  },
  "azure": {
    "subscription_id": "<guid>",
    "resource_group_prefix": "rg-apex-bigbox-",
    "primary_region": "eastus2",
    "dr_region": "westus2"
  }
}
```

**4.4.2 — Validate the manifest**

```bash
apex validate tenant apex-bigbox/tenants/bigbox.manifest.json
```

Must pass before the landing zone provisions. CI fails if it doesn't.

**4.4.3 — Provision Azure landing zone (Terraform)**

Terraform modules:
- `apex-landing-zone/tenant` — resource groups, networking, Key Vault, Log Analytics
- `apex-landing-zone/fabric` — Fabric capacity (F-SKU)
- `apex-landing-zone/foundry` — Azure AI Foundry project

F-SKU sizing for Cold-Chain Excursion W1:

| Pilot size | F-SKU | Monthly (USD) |
|------------|-------|----------------|
| 1 anchor store | F8 | ~$1,050 |
| 25-store pilot | F16 | ~$2,100 |
| 250-store W2 | F32 | ~$4,200 |

```bash
cd apex-landing-zone
terraform init
terraform workspace new bigbox
terraform apply -var-file=tenants/bigbox.tfvars
```

**4.4.4 — Establish private networking**

- VNet per tenant
- Private endpoints for Fabric, Foundry, Key Vault, Storage
- NSG rules: agents cannot reach public internet except via MCP-allowlisted external endpoints

**4.4.5 — Provision Purview governance domain**

- Purview account for `bigbox`
- Governance domain registered
- Classification-rule library imported (inherits from APEX Core)

### 4.5 Owner · Effort · Exit

- **Owner:** Platform Engineer · Solution Architect
- **Effort:** 6 SP · ~1 week
- **Exit criteria:** `apex validate tenant` passes; landing zone health checks pass; Purview domain visible

### 4.6 Cross-reference

- APEX_Design.md §3 (Four-Layer Manifest), §4 (Five-Plane Platform), §12 (Fabric), §14 (Purview)
- Flow tab: node `w1-identity` will attach to this tenant manifest (Step 10)

---

## 5. W1.2 — Real-Time Hub and Bronze landing

### 5.1 Purpose

Land raw SOR data into Bronze medallion layer. Schema-on-read, WORM retention, Purview-classified at point of ingest. Bronze is untransformed — no business logic runs here.

### 5.2 Inputs

- [ ] Step 4 complete (tenant manifest + landing zone)
- [ ] SOR shortlist from Step 3

### 5.3 Outputs

- [ ] Bronze Eventhouse table per streaming source
- [ ] Bronze Lakehouse table per batch/mirrored source
- [ ] Dead-letter containers per source
- [ ] Purview classification tags applied at ingest

### 5.4 Steps

**5.4.1 — Provision Fabric workspace structure**

```
Workspace: ws-bigbox-rc-bronze
├── Eventhouse: eh-bigbox-refrigeration
│   └── Database: db_refrigeration
│       ├── Table: raw_temp_readings (from Emerson E2)
│       ├── Table: raw_door_events
│       └── Table: raw_alarm_events
├── Lakehouse: lh-bigbox-bronze-batch
│   └── Tables/
│       ├── raw_sap_lot/        (mirrored from SAP MCHB)
│       ├── raw_sap_inventory/  (mirrored from SAP LQUA)
│       ├── raw_pos_transactions/
│       └── raw_price_master/
└── Data Pipelines: pipelines for batch sources
```

**5.4.2 — Configure Eventstream for refrigeration OPC-UA**

The refrigeration controller publishes OPC-UA over a site-local broker. An Azure IoT Edge gateway on the store LAN (or a Logic App for cloud-side controllers) bridges OPC-UA → Event Hubs → Fabric Real-Time Hub.

Eventstream pipeline:

```
Source: Event Hubs (ns-bigbox-iot.servicebus.windows.net)
Transform: schema-on-read — JSON → columnar
Sink: Eventhouse db_refrigeration.raw_temp_readings
Dead-letter: container dl-refrigeration/
```

Eventhouse schema (KQL):

```kusto
.create table raw_temp_readings (
    ingestion_ts: datetime,
    sensor_id: string,
    fixture_id: string,
    store_id: string,
    reading_type: string,
    value_num: real,
    unit: string,
    source_ts: datetime,
    source_system: string,
    raw_payload: dynamic
)
.create table raw_temp_readings ingestion time policy enable = true
.alter table raw_temp_readings policy retention softdelete = 90d recoverability = enabled
```

**5.4.3 — Configure Mirrored Database for SAP**

```
Source: SAP S/4HANA (via SAP CDC connector)
Target: Lakehouse lh-bigbox-bronze-batch/Tables/raw_sap_lot
Sync mode: continuous CDC (latency 60–180s)
Tables mirrored: MARA, MCHB, LQUA, BATCH_EXP
```

**5.4.4 — Configure Data Pipeline for Price Master**

```json
{
  "name": "bronze-price-master-daily",
  "trigger": { "type": "schedule", "cron": "0 2 * * *" },
  "activities": [
    {
      "name": "copy-price-master",
      "type": "Copy",
      "source": { "type": "OracleSource", "query": "SELECT * FROM PRICE_MASTER WHERE UPDATED_TS > @prev_run" },
      "sink": { "type": "LakehouseSink", "table": "raw_price_master" }
    }
  ]
}
```

**5.4.5 — Configure Custom Endpoint for refrigeration vendor webhook**

FastAPI app deployed as Azure Function:

```python
# notebooks/bronze/custom_endpoint.py
from fastapi import FastAPI, Header, HTTPException
import hmac, hashlib, json

app = FastAPI()

@app.post("/webhook/refrigeration-vendor")
async def vendor_webhook(payload: dict, x_signature: str = Header(...)):
    # HMAC verification
    expected = hmac.new(VENDOR_SECRET, json.dumps(payload).encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, x_signature):
        raise HTTPException(401, "invalid signature")
    # Land in Bronze
    await land_to_bronze("raw_vendor_tickets", payload)
    return {"status": "accepted"}
```

**5.4.6 — Apply Purview classifications at ingest**

Purview classification rules registered:

- `raw_temp_readings.value_num` → `INTERNAL`
- `raw_sap_lot.*` → `INTERNAL` with FSMA-204 traceability tag
- `raw_sap_inventory.*` → `INTERNAL`
- `raw_pos_transactions.loyalty_id` → `CONFIDENTIAL` (will be tokenized at Silver boundary)

**5.4.7 — Configure retention policies**

| Table | Retention | Archive |
|-------|-----------|---------|
| raw_temp_readings | 90d hot | 7y WORM archive |
| raw_sap_lot | 180d hot | permanent legal-hold eligible |
| raw_pos_transactions | 90d hot | 7y WORM archive |

### 5.5 Owner · Effort · Exit

- **Owner:** Data Engineer · Platform Engineer
- **Effort:** 12 SP · ~2 weeks
- **Exit criteria:** all Bronze tables accepting data; 24-hour smoke test shows <1% dead-letter rate; Purview shows classifications on all columns

### 5.6 Cross-reference

- APEX_Design.md §6.2 (Bronze landing patterns), §6.3 (retention & partitioning), §12.4 (OneLake), §13 (SOR integration playbook)
- Roadmap BL.P.20–25

---

## 6. W1.3 — Tokenizer at the Bronze→Silver boundary

### 6.1 Purpose

PII and PHI never cross the Bronze → Silver boundary in cleartext. Agents hold tokens only. Cleartext detokenization occurs only at user-surface time, for authorized Entra identities. This is APEX's core data-protection contract.

For Cold-Chain Excursion, this is relevant when CXML.Transaction joins happen in W3 fusion (loyalty-churn agent). Setting up the tokenizer in W1 Foundation — even though W2 Pilot doesn't need it yet — is intentional: tokens must exist from day 1 or retro-tokenization becomes a migration project.

### 6.2 Inputs

- [ ] Step 5 complete (Bronze is landing data)
- [ ] Key Vault provisioned (Step 4)

### 6.3 Outputs

- [ ] `apex-tokenizer` package installed in Silver transform notebook
- [ ] HMAC key material in Key Vault
- [ ] Token vault Delta table (for reverse lookup)
- [ ] Tokenization smoke test passing

### 6.4 Steps

**6.4.1 — Generate HMAC key material**

```bash
# Generate a 256-bit HMAC key
openssl rand -base64 32 > /tmp/hmac.key

# Store in Key Vault
az keyvault secret set \
  --vault-name kv-apex-bigbox \
  --name apex-tokenizer-hmac \
  --file /tmp/hmac.key

# Tag for governance
az keyvault secret set-attributes \
  --vault-name kv-apex-bigbox \
  --name apex-tokenizer-hmac \
  --tags "purpose=tokenizer" "rotation=annual" "classification=RESTRICTED"

# Shred local
shred -u /tmp/hmac.key
```

**6.4.2 — Provision token vault**

```sql
-- Delta table for reverse-lookup (tokenized_value → cleartext)
CREATE TABLE apex_tokenizer.token_vault (
    token_value        STRING,
    cleartext_value    STRING,
    field_name         STRING,
    classification     STRING,
    tenant_id          STRING,
    created_ts         TIMESTAMP,
    accessed_ts        TIMESTAMP
) USING DELTA
LOCATION 'Files/apex-tokenizer/token_vault'
PARTITIONED BY (tenant_id, field_name);

-- WORM: append-only, no updates
ALTER TABLE apex_tokenizer.token_vault
  SET TBLPROPERTIES ('delta.appendOnly' = 'true');
```

**6.4.3 — Register tokenizable fields in Silver transform config**

```yaml
# apex-rc/silver/tokenization-config.yaml
tokenization_rules:
  - source_table: raw_pos_transactions
    field: loyalty_id
    classification: CONFIDENTIAL
    strategy: deterministic_hmac
    target_field: loyalty_id_token
  - source_table: raw_pos_transactions
    field: payment_token
    classification: PCI
    strategy: deterministic_hmac
    target_field: payment_token_hash
```

**6.4.4 — Smoke test tokenizer**

```python
from apex_tokenizer import TokenService, DeltaVaultBackend

ts = TokenService(
    vault=DeltaVaultBackend(delta_path="Files/apex-tokenizer/token_vault"),
    hmac_key_secret_name="apex-tokenizer-hmac",
    tenant_id="bigbox"
)

# Tokenize
t1 = ts.tokenize("member_12345", field="loyalty_id", classification="CONFIDENTIAL")
t2 = ts.tokenize("member_12345", field="loyalty_id", classification="CONFIDENTIAL")
assert t1 == t2, "determinism required for joins"

# Reverse-lookup (only for authorized identity)
ct = ts.detokenize(t1, field="loyalty_id", requester_identity=AUTHORIZED_SPN)
assert ct == "member_12345"

# Unauthorized detokenize raises
try:
    ts.detokenize(t1, field="loyalty_id", requester_identity=RANDOM_SPN)
    assert False, "should have raised"
except PermissionError:
    pass
```

### 6.5 Owner · Effort · Exit

- **Owner:** Data Engineer · Governance Owner
- **Effort:** 5 SP · ~1 week
- **Exit criteria:** tokenizer smoke test passing; Key Vault secret tagged; token vault schema matches spec; tokenization deterministic across runs

### 6.6 Cross-reference

- APEX_Design.md §6.4.1 (Tokenization)
- Roadmap BL.P.27 (already complete: Sprint 5)

---

## 7. W1.4 — Silver canonical schemas

### 7.1 Purpose

Project raw SOR data into APEX canonical schemas. Every Silver row carries the canonical envelope (`event_id`, `event_ts`, `entity_id`, `source_system`, `source_system_ts`). Schemas are typed, SCD2-enabled, tokenized, Purview-classified.

For Cold-Chain Excursion the required canonical entities are:

- `SCML.Lot` — FSMA 204 lot-traceability
- `SCML.Inventory` — stock position per fixture
- `SCML.Fixture` — refrigerated-case master (new for W1)
- `SCML.SensorReading` — telemetry time-series (new for W1)
- `MERML.Price` — shelf price per SKU
- `MERML.Markdown` — markdown history
- `MERML.Elasticity` — price-response curve per SKU (optional W1, required for W3 fusion)
- `MERML.Transaction` — POS sales per SKU

### 7.2 Inputs

- [ ] Step 5 complete (Bronze data flowing)
- [ ] Step 6 complete (Tokenizer available)
- [ ] Schema mapping document from Step 3

### 7.3 Outputs

- [ ] Silver Delta tables per canonical entity
- [ ] Silver transform notebooks (PySpark)
- [ ] SCD2 history enabled on all dimension entities
- [ ] Drift detector configured

### 7.4 Steps

**7.4.1 — Provision Silver workspace**

```
Workspace: ws-bigbox-rc-silver
├── Lakehouse: lh-bigbox-silver
│   └── Tables/
│       ├── scml_lot/
│       ├── scml_inventory/
│       ├── scml_fixture/
│       ├── scml_sensor_reading/
│       ├── merml_price/
│       ├── merml_markdown/
│       ├── merml_elasticity/
│       └── merml_transaction/
```

**7.4.2 — Install canonical schema packages**

```bash
pip install apex-scml==2.3.0 apex-merml==2.1.0 apex-schemas-common==1.2.0
```

**7.4.3 — Author Silver transform notebook (SCML.Lot example)**

```python
# notebooks/silver/scml_lot_transform.py
from apex_scml.models import Lot
from apex_scml.translators.sap import map_mchb_to_lot
from apex_medallion.silver import transform
from apex_medallion.silver.scd2 import Scd2Config, next_scd2_fields
from apex_tokenizer import TokenService
from apex_standards.gs1 import validate_gtin

# Read Bronze
bronze_lot = spark.read.format("delta").load("Tables/raw_sap_lot")

# Apply canonical envelope
silver_lot = bronze_lot.transform(transform.add_canonical_envelope)

# Map SAP fields → canonical Lot
silver_lot = silver_lot.rdd.map(map_mchb_to_lot).toDF()

# Validate GTINs
silver_lot = silver_lot.filter(validate_gtin(col("gtin")))

# SCD2 history
scd2 = Scd2Config(key_cols=["lot_id"], change_cols=["inventory_qty", "current_location"])
silver_lot = silver_lot.transform(scd2.apply)

# Add FSMA 204 CTE/KDE flags
silver_lot = silver_lot.withColumn("fsma_204_cte_count", expr("size(cte_events)"))

# Write Silver
silver_lot.write.format("delta").mode("merge").saveAsTable("scml_lot")
```

**7.4.4 — Author new SCML.Fixture entity (not in canonical package today)**

Because refrigerated-fixture is specific to cold-chain scenarios, a new canonical sub-entity is authored and contributed back to SCML:

```python
# apex-scml/models/fixture.py (proposed addition)
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal
from apex_standards.types import GLN

class Fixture(BaseModel):
    """Physical storage fixture (refrigerated case, freezer, shelf-unit) within a store."""
    fixture_id: str = Field(..., description="stable fixture ID")
    store_id: GLN  # GS1 GLN
    fixture_type: Literal["REFRIGERATED_CASE", "FREEZER", "AMBIENT_SHELF", "DAIRY_WALK_IN", ...]
    category: str  # DAIRY, DELI, PRODUCE, ...
    capacity_units: int
    temp_setpoint_min: float | None
    temp_setpoint_max: float | None
    installed_ts: datetime
    vendor: str | None
    vendor_model: str | None
    fsma_204_relevant: bool = False
```

Manifest versioning:

```yaml
# apex-scml/manifests/change-log.yaml
- version: 2.3.0 -> 2.4.0
  bump: MINOR
  reason: "Add SCML.Fixture entity for cold-chain scenarios"
  breaking: false
```

**7.4.5 — Author SCML.SensorReading transform**

```python
# notebooks/silver/scml_sensor_reading_transform.py
from apex_scml.models import SensorReading
from apex_medallion.silver import transform

bronze = spark.read.format("delta").load("Tables/raw_temp_readings")

silver_sr = (bronze
    .transform(transform.add_canonical_envelope)
    .withColumnRenamed("value_num", "value")
    .withColumn("reading_type", lit("TEMPERATURE"))
    .withColumn("classification", lit("INTERNAL"))
)

# Fixture FK resolution
fixtures = spark.table("scml_fixture")
silver_sr = silver_sr.join(fixtures, on="fixture_id", how="left")

silver_sr.write.format("delta").mode("append").saveAsTable("scml_sensor_reading")
```

**7.4.6 — Author MERML transforms**

```python
# MERML.Price — daily truncate-and-rebuild (current-state snapshot)
# MERML.Markdown — SCD2 history
# MERML.Transaction — append-only with partitioning by date
# MERML.Elasticity — computed from 90d transaction + markdown history (spark.ml pipeline)
```

**7.4.7 — Tokenization pass**

```python
# Apply tokenization to classified fields before Silver write
from apex_tokenizer import tokenize_classified_fields

silver_tx = tokenize_classified_fields(
    df=silver_tx,
    rules=[("loyalty_id", "CONFIDENTIAL", "loyalty_id_token")]
)
```

**7.4.8 — Drift detector**

```python
from apex_medallion.silver.drift import detect_drift

report = detect_drift(
    expected_schema=Lot,
    actual_df=silver_lot,
    classification_map={"gtin": "INTERNAL", "origin_facility": "INTERNAL"}
)
assert not report.has_drift, f"Silver drift detected: {report.violations}"
```

Drift-detector runs on every Silver refresh; CI fails the pipeline if drift is detected.

### 7.5 Owner · Effort · Exit

- **Owner:** Data Engineer · Solution Architect · RC Practice Lead
- **Effort:** 15 SP · ~3 weeks
- **Exit criteria:** All 8 Silver tables populated; SCD2 history verified; tokenization verified on classified fields; drift detector green; FSMA 204 CTE completeness >98%

### 7.6 Cross-reference

- APEX_Design.md §5 (Canonical Schemas), §6.4 (Silver)
- Roadmap BL.P.08, BL.P.09, BL.P.26, BL.P.28, BL.P.34

---

## 8. W1.5 — Gold agent-safe views

### 8.1 Purpose

Gold materializes agent-consumable views with classification-aware masking, scoped to agent tenant/practice/persona. Gold views pre-join Silver entities so a single agent tool call returns exactly the joined shape the agent needs. Direct Lake semantic models back Power BI; Warehouse T-SQL views back MCP tools; KQL functions back real-time queries.

### 8.2 Inputs

- [ ] Step 7 complete (Silver populated)

### 8.3 Outputs

- [ ] Gold Direct Lake semantic model (for Power BI)
- [ ] Gold Warehouse views (for MCP tools)
- [ ] Gold KQL functions (for real-time queries)
- [ ] Agent-safe view derivatives with RLS/OLS applied

### 8.4 Steps

**8.4.1 — Author the primary Gold view: `gold.sku_at_risk`**

This view is the workhorse for the Cold-Chain Excursion agent:

```sql
-- Warehouse T-SQL view
CREATE VIEW gold.sku_at_risk AS
SELECT
    f.fixture_id,
    f.store_id,
    f.category,
    l.lot_id,
    l.material_id AS sku_id,
    l.gtin,
    l.expiry_date,
    i.on_hand_units,
    p.current_price,
    p.cost,
    (i.on_hand_units * p.current_price) AS retail_value,
    (i.on_hand_units * p.cost) AS cost_value,
    l.fsma_204_cte_count,
    CASE
        WHEN e.elasticity_segment IS NULL THEN 'MEDIUM'
        ELSE e.elasticity_segment
    END AS elasticity_segment,
    f.fsma_204_relevant,
    CURRENT_TIMESTAMP AS gold_refresh_ts
FROM silver.scml_fixture f
INNER JOIN silver.scml_inventory i
    ON i.fixture_id = f.fixture_id
    AND i.is_current = TRUE
INNER JOIN silver.scml_lot l
    ON l.lot_id = i.lot_id
    AND l.is_current = TRUE
    AND l.expiry_date > CURRENT_TIMESTAMP
LEFT JOIN silver.merml_price p
    ON p.sku_id = l.material_id
    AND p.store_id = f.store_id
    AND p.is_current = TRUE
LEFT JOIN silver.merml_elasticity e
    ON e.sku_id = l.material_id;
```

**8.4.2 — Author the telemetry Gold function: `fn_excursion_window`**

This KQL function returns the full temperature time-series for a fixture within a window:

```kusto
.create-or-alter function fn_excursion_window(fixture_id:string, start_ts:datetime, end_ts:datetime) {
    scml_sensor_reading
    | where fixture_id == fixture_id
    | where reading_type == "TEMPERATURE"
    | where event_ts between (start_ts .. end_ts)
    | project event_ts, value, unit, source_system
    | order by event_ts asc
}
```

**8.4.3 — Author the markdown-candidate Gold view**

```sql
CREATE VIEW gold.markdown_candidate AS
SELECT
    s.sku_id,
    s.store_id,
    s.on_hand_units,
    s.current_price,
    e.elasticity_curve_json,
    e.optimal_markdown_pct,
    e.expected_sell_through_units,
    DATEDIFF(day, CURRENT_DATE, l.expiry_date) AS days_to_expiry
FROM gold.sku_at_risk s
INNER JOIN silver.merml_elasticity e ON e.sku_id = s.sku_id
INNER JOIN silver.scml_lot l ON l.lot_id = s.lot_id;
```

**8.4.4 — Apply agent-safe-view masking**

The cold-chain agent runs at classification `INTERNAL`. It can see `SCML.Lot` and `MERML.Price`. It cannot see `CXML.Transaction.loyalty_id` (CONFIDENTIAL). Agent-safe views enforce this:

```python
from apex_identity import AgentRole, apply_agent_safe_view

cold_chain_agent_role = AgentRole(
    agent_id="agent-cold-chain",
    tenant_id="bigbox",
    practice_id="rc",
    classification_ceiling="INTERNAL",
    allowed_views=["gold.sku_at_risk", "gold.markdown_candidate"]
)
```

The `fabric-mcp` utility server enforces this at query time — it rejects calls from agents that exceed their classification ceiling.

**8.4.5 — Publish Direct Lake semantic model**

```python
# TMDL semantic model
from apex_medallion.gold.direct_lake import SemanticModelSpec, render_tmdl

spec = SemanticModelSpec(
    model_name="rc_cold_chain_sem",
    tables=["gold.sku_at_risk", "gold.markdown_candidate"],
    measures=["effective_margin_pct", "stock_days_remaining", "time_since_last_event_seconds"],
    row_level_security={"store_id": "current_user_store"}
)

tmdl_content = render_tmdl(spec)
# Deploy via Fabric REST API
```

**8.4.6 — Pre-measure library**

```python
# apex-medallion/gold/rc_measures.py
def effective_margin_pct(row):
    return (row["current_price"] - row["cost"]) / row["current_price"]

def stock_days_remaining(row):
    # velocity-based
    return row["on_hand_units"] / max(row["daily_velocity"], 0.01)

def time_since_last_event_seconds(row):
    return (datetime.utcnow() - row["event_ts"]).total_seconds()
```

### 8.5 Owner · Effort · Exit

- **Owner:** Data Engineer · Analytics Engineer
- **Effort:** 10 SP · ~2 weeks
- **Exit criteria:** `gold.sku_at_risk` returns <200ms for single-fixture query; semantic model refreshes <1s; agent-safe-view masking verified by security test

### 8.6 Cross-reference

- APEX_Design.md §6.5 (Gold), §6.6 (Measures), §8 (Visibility Lattice)
- Roadmap BL.P.29–34

---

## 9. W1.6 — MCP server integration

### 9.1 Purpose

MCP servers expose Gold views as typed, contract-validated tools for agents. Every tool carries an input-schema, output-schema, SLO, classification-propagation rule, and trace instrumentation. For Cold-Chain Excursion the agent needs 6 MCP servers across 3 classes (domain, utility, external).

### 9.2 Inputs

- [ ] Step 8 complete (Gold views queryable)

### 9.3 Outputs

- [ ] `scml-mcp` deployed (domain)
- [ ] `merml-mcp` deployed (domain)
- [ ] `fabric-mcp` deployed (utility)
- [ ] `policy-mcp` deployed (utility)
- [ ] `approvals-mcp` deployed (utility)
- [ ] `ledger-mcp` deployed (utility)
- [ ] `telemetry-mcp` deployed (utility)
- [ ] `vendor-portal-mcp` deployed (external)
- [ ] MCP tool contracts published and validated

### 9.4 Steps

**9.4.1 — Deploy domain MCP: `scml-mcp`**

```python
# mcp-servers/scml-mcp/server.py
from mcp_common import Server, tool, ToolContract, SloSpec
from apex_scml.mcp import get_lot_provenance, list_inventory_by_fixture

CONTRACTS = [
    ToolContract(
        name="list_inventory_by_fixture",
        input_schema={"fixture_id": {"type": "string", "required": True}},
        output_schema={
            "fixture_id": "string",
            "skus": [{"sku_id": "string", "on_hand_units": "integer", ...}],
            "total_retail_value": "number"
        },
        classification_propagation={"default": "INTERNAL"},
        slo=SloSpec(p95_latency_ms=250, availability_pct=99.9),
        scope_required="practice:rc"
    ),
    ToolContract(
        name="get_lot_provenance",
        input_schema={"lot_id": {"type": "string", "required": True}},
        output_schema={"lot_id": "string", "fsma_204_ctes": "array", ...},
        slo=SloSpec(p95_latency_ms=500, availability_pct=99.9),
        scope_required="practice:rc"
    ),
]

server = Server("scml-mcp", contracts=CONTRACTS)

@tool(contract=CONTRACTS[0])
async def list_inventory_by_fixture(fixture_id: str):
    result = await fabric.query(
        "SELECT * FROM gold.sku_at_risk WHERE fixture_id = @fixture_id",
        params={"fixture_id": fixture_id}
    )
    return {
        "fixture_id": fixture_id,
        "skus": result,
        "total_retail_value": sum(r["retail_value"] for r in result)
    }

if __name__ == "__main__":
    server.run(port=8001)
```

**9.4.2 — Deploy domain MCP: `merml-mcp`**

Tools exposed:
- `get_current_price(sku_id, store_id)` → price
- `get_elasticity(sku_id)` → markdown-response curve
- `list_recent_markdowns(sku_id, window_days)` → markdown history

**9.4.3 — Deploy utility MCPs**

These are APEX-provided, tenant-agnostic:

| MCP server | Tools |
|------------|-------|
| `fabric-mcp` | `get_entity_by_key`, `query_gold_view`, `query_eventhouse`, `list_classifications` |
| `policy-mcp` | `evaluate_policy`, `check_compliance`, `classify_bump`, `evaluate_fsma_204` |
| `approvals-mcp` | `request_approval`, `get_approval_status`, `record_decision` |
| `ledger-mcp` | `append_audit_row`, `fetch_row_by_trace`, `verify_row_signature` |
| `telemetry-mcp` | `emit_trace`, `log_event`, `query_latency_percentile` |

**9.4.4 — Register FSMA 204 policy corpus in policy-mcp**

```yaml
# apex-bigbox/policies/fsma-204-cold-chain.yaml
policy_id: fsma-204-cold-chain
version: 1.0.0
jurisdiction: US
category: food_safety
rules:
  - rule_id: dairy_temp_sell_through
    condition: "category=DAIRY AND peak_temp < 45 AND duration_hours < 2"
    action: sell_through
    severity: MINOR
    gate_kind: ZERO_TOUCH
  - rule_id: dairy_temp_markdown
    condition: "category=DAIRY AND peak_temp BETWEEN 45 AND 50 AND duration_hours < 4"
    action: markdown
    severity: MODERATE
    gate_kind: HITL
  - rule_id: dairy_temp_destroy
    condition: "category=DAIRY AND (peak_temp > 50 OR duration_hours > 4)"
    action: destroy
    severity: MAJOR
    gate_kind: HITL
```

Register via policy-mcp:

```bash
apex policy register --file apex-bigbox/policies/fsma-204-cold-chain.yaml
```

**9.4.5 — Deploy external MCP: `vendor-portal-mcp`**

Wraps the refrigeration-vendor's REST API (ServiceChannel / Corrigo / Ecotrak):

```python
@tool
async def create_service_ticket(
    fixture_id: str,
    issue_class: str,
    severity: str,
    description: str,
    classification: str = "INTERNAL"
):
    payload = {"facility": fixture_id, "priority": severity, "issue_type": issue_class, "desc": description}
    response = await httpx.post(
        f"{VENDOR_API_URL}/tickets",
        json=payload,
        headers={"Authorization": f"Bearer {await get_vendor_token()}"}
    )
    return {"ticket_id": response.json()["id"], "vendor": "corrigo", "created_ts": datetime.utcnow()}
```

**9.4.6 — Provision MCP tool catalog registration**

All 8 MCP servers register themselves to the APEX tool catalog at startup. Catalog is queryable:

```bash
apex mcp list
# NAME              CLASS     TENANT   SCOPE         TOOLS
# scml-mcp          domain    bigbox   practice:rc   7
# merml-mcp         domain    bigbox   practice:rc   5
# fabric-mcp        utility   bigbox   *             3
# policy-mcp        utility   bigbox   *             4
# approvals-mcp     utility   bigbox   *             3
# ledger-mcp        utility   bigbox   *             3
# telemetry-mcp     utility   bigbox   *             3
# vendor-portal-mcp external  bigbox   practice:rc   4
```

**9.4.7 — Private endpoint networking**

Each MCP server deployed to a private endpoint. Agents reach them over the tenant VNet, not the public internet.

### 9.5 Owner · Effort · Exit

- **Owner:** Platform Engineer · MCP Owner · RC Practice Lead
- **Effort:** 14 SP · ~3 weeks
- **Exit criteria:** All 8 MCP servers running; tool-contract validation passing; private-endpoint connectivity verified; trace records flowing to telemetry-mcp; FSMA 204 policy corpus returns correct decisions on test fixtures

### 9.6 Cross-reference

- APEX_Design.md §7 (MCP topology)
- Roadmap BL.P.35–52

---

## 10. W1.7 — Entra managed identities and visibility lattice

### 10.1 Purpose

Every APEX agent runs under a unique Entra managed-identity with a typed scope. The visibility lattice composes tenant × practice × persona × classification × row filters to determine what the agent can see. Fails closed — unknown agent, missing role, or tenant mismatch denies access.

### 10.2 Inputs

- [ ] Step 4 complete (tenant landing zone)
- [ ] Step 9 complete (MCP servers know about scopes)

### 10.3 Outputs

- [ ] Managed identity per agent
- [ ] `AgentRole` definitions in `apex-identity`
- [ ] Row-level security policies on Silver/Gold tables
- [ ] Agent-safe view runtime configured

### 10.4 Steps

**10.4.1 — Provision managed identities**

```bash
# Cold-chain agent (anchor of W2)
az identity create \
  --name id-apex-agent-cold-chain-bigbox \
  --resource-group rg-apex-bigbox-identity \
  --location eastus2

# Additional W2 agents
for agent in assess classify quantify act; do
  az identity create \
    --name id-apex-agent-$agent-bigbox \
    --resource-group rg-apex-bigbox-identity
done
```

**10.4.2 — Author AgentRole definitions**

```python
# apex-bigbox/identity/agent-roles.py
from apex_identity import AgentRole

COLD_CHAIN_ROLE = AgentRole(
    agent_id="agent-cold-chain",
    tenant_id="bigbox",
    practice_id="rc",
    classification_ceiling="INTERNAL",
    allowed_mcp_tools=[
        "scml-mcp.list_inventory_by_fixture",
        "scml-mcp.get_lot_provenance",
        "merml-mcp.get_current_price",
        "merml-mcp.get_elasticity",
        "fabric-mcp.query_eventhouse",
        "policy-mcp.evaluate_fsma_204",
        "approvals-mcp.request_approval",
        "approvals-mcp.get_approval_status",
        "ledger-mcp.append_audit_row",
        "telemetry-mcp.emit_trace",
        "vendor-portal-mcp.create_service_ticket",
    ],
    row_filters={"store_id": ["100"]},  # W1: anchor store only; W2 expands
    denied_fields=["*.loyalty_id", "*.payment_token", "*.pii_*"]
)
```

**10.4.3 — Register roles with scope resolver**

```python
from apex_identity.provisioning import register_agent

await register_agent(COLD_CHAIN_ROLE)
```

**10.4.4 — Apply Row-Level Security (RLS) on Gold**

```sql
-- Silver RLS
CREATE SECURITY POLICY scml_lot_filter
ADD FILTER PREDICATE apex_rls.allow_by_agent_scope(store_id)
ON silver.scml_lot
WITH (STATE = ON);

-- Same pattern on scml_inventory, scml_fixture, merml_price, merml_transaction
```

**10.4.5 — Test fail-closed semantics**

```python
# Authorized access
decision = evaluate_visibility(COLD_CHAIN_ROLE, "scml_lot", {"store_id": "100"})
assert decision.allowed == True

# Store not in row filter
decision = evaluate_visibility(COLD_CHAIN_ROLE, "scml_lot", {"store_id": "101"})
assert decision.allowed == False

# Wrong tenant
wrong_tenant = COLD_CHAIN_ROLE.model_copy(update={"tenant_id": "other-tenant"})
decision = evaluate_visibility(wrong_tenant, "scml_lot", {"store_id": "100"})
assert decision.allowed == False

# Classification above ceiling
decision = evaluate_visibility(COLD_CHAIN_ROLE, "cxml_transaction", {"store_id": "100"})
assert decision.allowed == False  # CXML is CONFIDENTIAL, agent ceiling is INTERNAL
```

**10.4.6 — Response signing**

Every agent response is HMAC-signed by the agent's identity. Consumers verify signatures before acting on agent output.

```python
from apex_identity import sign_response, verify_response

signed = sign_response(
    agent_id="agent-cold-chain",
    tenant_id="bigbox",
    payload={"proposed_action": "markdown", "depth_pct": 35}
)
# signed = {"payload": {...}, "signature": "hmac:...", "key_ref": "kv://apex-bigbox/agent-cold-chain-signing"}

verify_response(signed)  # raises if tampered
```

### 10.5 Owner · Effort · Exit

- **Owner:** Security Engineer · Solution Architect · Governance Owner
- **Effort:** 8 SP · ~2 weeks
- **Exit criteria:** all 5 managed identities provisioned; AgentRole test suite passing; RLS verified on Silver + Gold; response signing round-trips; fail-closed test cases all reject

### 10.6 Cross-reference

- APEX_Design.md §8 (Identity & Visibility Lattice)
- Roadmap BL.P.53–57 (complete: Sprint 10)

---

## 11. W1.8 — LEDGER instantiation

### 11.1 Purpose

LEDGER is the append-only decision-provenance store. Every agent decision emits a 14-field audit row carrying trace-id, three-version stamps (manifest + policy + prompt), reasoning trace, HITL status, and downstream-effect cross-reference. For Cold-Chain Excursion, LEDGER is also where the FSMA 204 policy corpus lives.

### 11.2 Inputs

- [ ] Step 9 complete (ledger-mcp deployed)
- [ ] Step 10 complete (agent identities provisioned)

### 11.3 Outputs

- [ ] Audit-row Delta store provisioned
- [ ] WORM retention applied
- [ ] Three-version stamp registry
- [ ] Content-addressed hash store

### 11.4 Steps

**11.4.1 — Provision audit-row Delta store**

```sql
CREATE TABLE apex_ledger.audit_row (
    audit_row_id          STRING,
    trace_id              STRING,
    tenant_id             STRING,
    agent_id              STRING,
    event_kind            STRING,
    event_ts              TIMESTAMP,
    manifest_version      STRING,
    policy_version        STRING,
    prompt_version        STRING,
    inputs_content_hash   STRING,
    outputs_content_hash  STRING,
    reasoning_ref         STRING,
    hitl_status           STRING,
    downstream_effect_ref STRING,
    signed_row_hash       STRING
) USING DELTA
LOCATION 'Files/apex-ledger/audit_row'
PARTITIONED BY (tenant_id, event_ts)
TBLPROPERTIES (
    'delta.appendOnly' = 'true',
    'delta.enableChangeDataFeed' = 'true'
);
```

**11.4.2 — Enable WORM retention (Azure Storage Immutable Blob)**

```bash
az storage account blob-service-properties update \
  --account-name stapexbigbox \
  --enable-versioning true \
  --enable-change-feed true

# Immutable-storage policy: 7-year WORM
az storage container immutability-policy create \
  --account-name stapexbigbox \
  --container-name apex-ledger \
  --period 2555 \
  --allow-protected-append-writes true
```

**11.4.3 — Register three-version stamps**

```python
from apex_audit.versions import VersionStamps, stamp_versions

stamps = VersionStamps(
    manifest_version="rc-cold-chain-orchestration-v1.2.0",
    policy_version="fsma-204-cold-chain-v1.0.0",
    prompt_version="agent-classify-v3.1.0-sha:abc123"
)

# Every audit row stamps these at emission
await ledger_mcp.append_audit_row(
    trace_id=trace_id,
    versions=stamps,
    ...
)
```

**11.4.4 — Content-addressed input/output hash store**

```python
from apex_audit.content_store import ContentAddressedStore

store = ContentAddressedStore(delta_path="Files/apex-ledger/content_store")

# Store input blob
inputs_hash = await store.put({"fixture_id": "...", "window": [...]})
# inputs_hash = "sha256:8f2a..."

# Retrieve later
inputs = await store.get(inputs_hash)
```

**11.4.5 — Restricted reasoning-trace store**

Chain-of-thought reasoning is stored separately with stricter access controls; only the emitted audit-row carries the DLP-scrubbed summary:

```python
from apex_audit.reasoning import RestrictedTraceStore

trace_store = RestrictedTraceStore(delta_path="Files/apex-ledger/reasoning", dlp_scrub=True)
reasoning_ref = await trace_store.put(raw_cot="...", scrubbed_summary="...")
```

**11.4.6 — Register FSMA 204 policy corpus in LEDGER**

```bash
apex ledger register-policy \
  --file apex-bigbox/policies/fsma-204-cold-chain.yaml \
  --tenant bigbox
```

The ledger-mcp now serves this as retrievable context for the classify agent.

**11.4.7 — Smoke test append + verify**

```python
from apex_audit import AuditRow
from ledger_mcp.client import append_audit_row, fetch_row_by_trace

row = AuditRow(
    trace_id="test-trace-001",
    tenant_id="bigbox",
    agent_id="agent-cold-chain",
    event_kind="smoke_test",
    ...
)
result = await append_audit_row(row)
assert result.signed_row_hash is not None

# Fetch
fetched = await fetch_row_by_trace("test-trace-001")
assert fetched.agent_id == "agent-cold-chain"

# Verify signature
from apex_audit.signing import verify_row
assert verify_row(fetched)

# Attempt overwrite raises
try:
    await append_audit_row(row)  # same trace-id + event_kind
    assert False
except AppendOnlyViolationError:
    pass
```

### 11.5 Owner · Effort · Exit

- **Owner:** Platform Engineer · Governance Owner
- **Effort:** 7 SP · ~1.5 weeks
- **Exit criteria:** audit-row append works; WORM retention verified (attempted delete blocked by Azure Storage policy); three-version stamps present on every test row; content-addressed hash store round-trips; FSMA 204 corpus registered and queryable; signature verification passes; overwrite attempts fail closed

### 11.6 Cross-reference

- APEX_Design.md §11 (Decision Audit Row)
- Roadmap BL.P.77–84 (complete: Sprint 12)

---

## 12. W1.9 — HITL surface templates

### 12.1 Purpose

Register the Teams Adaptive Card template that the cold-chain agent will surface to Marisol Reyes. Bind Marisol's markdown/destroy-authority policy in LEDGER. Wire approvals-mcp to the template. Agent in W2 will call `approvals-mcp.request_approval(template='cold-chain-excursion-v1', ...)` and the card fires.

### 12.2 Inputs

- [ ] Step 9 complete (approvals-mcp deployed)
- [ ] Step 11 complete (LEDGER accepting policy registrations)
- [ ] Persona roster from Step 2 (Marisol Reyes identified)

### 12.3 Outputs

- [ ] Adaptive Card template registered
- [ ] HITL authority policy in LEDGER
- [ ] Teams bot installed at Big Box Store 100
- [ ] Timeout escalation path configured

### 12.4 Steps

**12.4.1 — Author the Adaptive Card template**

```json
{
  "type": "AdaptiveCard",
  "version": "1.5",
  "body": [
    {
      "type": "TextBlock",
      "size": "Large",
      "weight": "Bolder",
      "text": "⚠ Cold-Chain Excursion · Store {{store_id}} · Fixture {{fixture_id}}"
    },
    {
      "type": "FactSet",
      "facts": [
        { "title": "Duration", "value": "{{duration_min}} min" },
        { "title": "Peak temp", "value": "{{peak_temp}}°F" },
        { "title": "Avg temp",  "value": "{{avg_temp}}°F" },
        { "title": "At-risk units", "value": "{{total_units}} across {{sku_count}} SKUs" },
        { "title": "Retail value at risk", "value": "${{retail_value_usd}}" }
      ]
    },
    {
      "type": "Container",
      "separator": true,
      "items": [
        { "type": "TextBlock", "text": "Proposed actions", "weight": "Bolder" },
        { "type": "TextBlock", "text": "• **Sell-through** {{sell_through_units}} units (est. ${{sell_through_value}})", "wrap": true },
        { "type": "TextBlock", "text": "• **Markdown** {{markdown_units}} units at {{markdown_pct}}% (recovers ~${{markdown_value}})", "wrap": true },
        { "type": "TextBlock", "text": "• **Destroy** {{destroy_units}} units (write-off ${{destroy_value}})", "wrap": true }
      ]
    }
  ],
  "actions": [
    { "type": "Action.Submit", "title": "Approve all 3", "data": { "decision": "approve_all" }, "style": "positive" },
    { "type": "Action.Submit", "title": "Modify", "data": { "decision": "modify" } },
    { "type": "Action.Submit", "title": "Reject", "data": { "decision": "reject" }, "style": "destructive" }
  ]
}
```

**12.4.2 — Register the template with approvals-mcp**

```bash
apex approvals register-template \
  --id cold-chain-excursion-v1 \
  --file apex-bigbox/hitl/cold-chain-card.json \
  --tenant bigbox
```

**12.4.3 — Bind Marisol's authority policy in LEDGER**

```yaml
# apex-bigbox/policies/hitl-authority-rc.yaml
policy_id: hitl-authority-rc-store-ops-lead
version: 1.0.0
bindings:
  - scenario: cold-chain-excursion
    primary_persona: store_ops_lead
    named_person: "Marisol Reyes"  # placeholder; resolves via Entra group lookup at runtime
    thresholds:
      markdown_pct_ceiling: 50
      destroy_value_ceiling_usd: 5000
    escalation_path:
      - role: store_manager  # Jamie O'Connor
        after_seconds: 300
      - role: district_manager
        after_seconds: 900
```

Register:

```bash
apex policy register --file apex-bigbox/policies/hitl-authority-rc.yaml
```

**12.4.4 — Install the Teams bot**

Deploy Azure Bot Service instance bound to the tenant's Teams app. Bot handles Adaptive Card posts and receives decision callbacks. Posts the card to Marisol's Teams channel on `approvals-mcp.request_approval()`.

**12.4.5 — Configure escalation timer**

`approvals-mcp` uses the hitl-authority policy's `after_seconds` to re-post to next-tier persona if no response received:

```python
async def request_approval(template_id, recipient, payload, tenant_id):
    decision_id = uuid4()
    await ledger.append_pending_decision(decision_id, payload, deadline=300)
    await teams_bot.post_card(recipient, template_id, payload, decision_id)
    asyncio.create_task(escalation_watch(decision_id, tenant_id))
    return {"decision_id": str(decision_id), "pending"}
```

**12.4.6 — Smoke test the HITL loop**

From the command line:

```bash
apex hitl test \
  --template cold-chain-excursion-v1 \
  --recipient marisol.reyes@bigbox.example.com \
  --payload '{"store_id": "100", "fixture_id": "DAIRY_A3", ...}'
```

Marisol receives a test card in Teams. She taps "Approve all 3" (smoke-test mode marks it as test). The decision record appears in LEDGER within 2 seconds.

### 12.5 Owner · Effort · Exit

- **Owner:** Solution Architect · RC Practice Lead · Client's Teams admin
- **Effort:** 6 SP · ~1.5 weeks
- **Exit criteria:** template registered; authority policy in LEDGER; bot installed at Store 100; escalation timer fires correctly; smoke-test decision round-trips in <3s

### 12.6 Cross-reference

- APEX_Design.md §9 (HITL Gates), §17 (Human Oversight Spectrum)
- Roadmap BL.P.69–76

---

## 13. W1 Exit Gate

W1 is complete when **every box below is checked**. This is not an informal list — the Delivery Lead cannot move to W2 without all 10.

### 13.1 Hard gates

- [ ] **G1** — Tenant manifest validates (§4) and landing zone provisioned
- [ ] **G2** — Bronze is ingesting every SOR identified in Discovery (§5); dead-letter rate <1% over 48h
- [ ] **G3** — Tokenizer smoke test passes; deterministic on classified fields (§6)
- [ ] **G4** — All 8 Silver tables populated; SCD2 history verified; drift detector green (§7)
- [ ] **G5** — Gold views return <300ms p95 for single-fixture query; semantic model publishes (§8)
- [ ] **G6** — All 8 MCP servers deployed; tool-contract validation green; FSMA 204 policy registered (§9)
- [ ] **G7** — Managed identities provisioned; AgentRole fail-closed tests pass; response signing round-trips (§10)
- [ ] **G8** — LEDGER audit-row store live; WORM enforced; three-version stamps present; overwrite attempts fail (§11)
- [ ] **G9** — HITL Adaptive Card template registered; authority policy in LEDGER; Teams bot installed; smoke-test round-trips (§12)
- [ ] **G10** — End-to-end smoke: inject synthetic temperature excursion → Silver row → Gold view returns → MCP call succeeds → audit row emitted. Round-trip <5s.

### 13.2 Soft gates (recommended, not blocking)

- [ ] **S1** — Power BI KPI dashboard scaffold published (even if no real data yet)
- [ ] **S2** — Runbook published to client's ops team (emergency contacts, rollback procedure)
- [ ] **S3** — 2-week change freeze window planned before W2 launch

### 13.3 Commercial envelope review

At W1 exit the Delivery Lead reviews actual vs estimated for:

- Calendar time (target 4–8 weeks)
- Effort consumed (target ~40 SP across all W1 steps)
- Cost envelope (target $500K–$2M)
- Commercial learnings feed into the W2 SoW

---

# Wave 2 — Pilot

W2 runs the scenario live at proof-point scale. 250 stores, dairy + deli + produce fixtures. Every cold-chain excursion event exercises the full chain.

**W2 total effort:** ~35 SP · 6–15 months · $5M–$15M commercial envelope
**W2 goal KPIs:** 5.2 hr/shift time returned to manager; 18% shrink reduction; $1,313 avg savings per event; 90s median manager touch-time; 100% audit-trail completeness

---

## 14. W2.1 — Event trigger wiring

### 14.1 Purpose

A Data Activator reflex rule watches Bronze Eventhouse. When a fixture's temperature exceeds threshold for >15 minutes, a structured event fires and reaches the orchestrator.

### 14.2 Inputs

- [ ] W1 complete
- [ ] Gate G10 passed (end-to-end smoke succeeds)

### 14.3 Outputs

- [ ] Data Activator reflex rule provisioned
- [ ] Event schema published
- [ ] Connection to orchestrator established

### 14.4 Steps

**14.4.1 — Author the reflex rule**

```kusto
// Data Activator rule: cold-chain excursion detection
// Fires when any REFRIGERATED_CASE or FREEZER exceeds setpoint for >15 minutes
scml_sensor_reading
| where reading_type == "TEMPERATURE"
| where event_ts > ago(16m)
| join kind=inner scml_fixture on fixture_id
| where fixture_type in ("REFRIGERATED_CASE", "FREEZER")
| where value > temp_setpoint_max
| summarize
    start_ts = min(event_ts),
    last_ts = max(event_ts),
    peak_temp = max(value),
    avg_temp = avg(value),
    reading_count = count()
    by fixture_id, store_id
| where datetime_diff('minute', last_ts, start_ts) >= 15
| project fixture_id, store_id, start_ts, last_ts, peak_temp, avg_temp, reading_count
```

Register:

```bash
fabric reflex create \
  --name cold-chain-excursion-reflex \
  --query-file reflex.kql \
  --sink event-hub://ns-bigbox-events/excursion-detected
```

**14.4.2 — Publish event schema**

```yaml
# apex-bigbox/events/cold-chain-excursion.event-manifest.yaml
event_id: cold-chain-excursion-detected
version: 1.0.0
trigger: data_activator_reflex
payload_schema:
  fixture_id: { type: string, required: true }
  store_id: { type: string, required: true }
  start_ts: { type: datetime, required: true }
  last_ts: { type: datetime, required: true }
  peak_temp: { type: number, required: true }
  avg_temp: { type: number, required: true }
  reading_count: { type: integer, required: true }
classification: INTERNAL
routes_to: orchestration://rc-cold-chain-response-v1.2
```

Validate:

```bash
apex validate event apex-bigbox/events/cold-chain-excursion.event-manifest.yaml
```

**14.4.3 — Connect reflex to orchestrator**

Event Hub → Azure Function trigger → `apex-orchestrator` entry point → `rc-cold-chain-response-v1.2` orchestration manifest.

### 14.5 Owner · Effort · Exit

- **Owner:** Data Engineer · RC Practice Lead
- **Effort:** 4 SP · ~1 week
- **Exit criteria:** synthetic excursion injection triggers reflex within <30s of last reading; event schema validates; orchestrator receives event with correct payload shape

### 14.6 Cross-reference

- APEX_Design.md §12.5 (Data Activator)
- Flow tab node `w2-event`

---

## 15. W2.2 — Orchestration manifest

### 15.1 Purpose

Compose 5 agents (Assess, Classify, Quantify, Act) plus a HITL gate into a DAG. Manifest-pinned versions, gate placements, trace-id binding. Sequential with branching — if Classify returns severity=CRITICAL, skip markdown path and go straight to destroy with HITL.

### 15.2 Inputs

- [ ] Steps 10, 11, 12 complete (identities, LEDGER, HITL all ready)
- [ ] Step 14 complete (events firing)

### 15.3 Outputs

- [ ] Orchestration manifest authored and validated
- [ ] Orchestrator runtime configured
- [ ] Trace-id binding test passing

### 15.4 Steps

**15.4.1 — Author orchestration manifest**

```yaml
# apex-bigbox/orchestrations/rc-cold-chain-response-v1.2.yaml
manifest_kind: orchestration
manifest_version: 1.2.0
orchestration_id: rc-cold-chain-response
description: "Cold-Chain Excursion end-to-end response for Practice RC"
trigger_event: cold-chain-excursion-detected
trace_id_strategy: inherit_from_event
agents:
  - role: assess
    agent_id: agent-cold-chain-assess
    agent_version: 1.3.0
    model_pin: gpt-4o-2024-08-06
    prompt_version: assess-v2.1-sha:a1b2
  - role: classify
    agent_id: agent-cold-chain-classify
    agent_version: 1.4.0
    prompt_version: classify-v3.1-sha:abc1
  - role: quantify
    agent_id: agent-cold-chain-quantify
    agent_version: 1.2.0
    prompt_version: quantify-v2.0-sha:def2
  - role: act
    agent_id: agent-cold-chain-act
    agent_version: 1.1.0
    prompt_version: act-v1.5-sha:ghi3
flow:
  - type: sequential
    steps:
      - agent: assess
      - agent: classify
      - agent: quantify
      - gate:
          kind: HITL
          policy: hitl-authority-rc-store-ops-lead
          template: cold-chain-excursion-v1
          timeout_s: 300
      - agent: act
hitl_branches:
  - condition: "classify.severity == 'CRITICAL'"
    override_gate:
      kind: ESCALATION
      escalate_to: district_manager
audit:
  emit_composite: true
  emit_per_agent: true
```

**15.4.2 — Validate**

```bash
apex validate orchestration apex-bigbox/orchestrations/rc-cold-chain-response-v1.2.yaml
```

**15.4.3 — Deploy to orchestrator runtime**

```bash
apex orchestrator deploy \
  --manifest apex-bigbox/orchestrations/rc-cold-chain-response-v1.2.yaml \
  --tenant bigbox
```

**15.4.4 — Bind trace-id discipline**

Every step in the orchestration inherits the event's trace-id (e.g., `trc_2026-04-23_0608_bb100_a3`). Every MCP tool call carries it. Every audit row emits it. The three-version rule applies everywhere.

### 15.5 Owner · Effort · Exit

- **Owner:** RC Practice Lead · Solution Architect
- **Effort:** 5 SP · ~1 week
- **Exit criteria:** manifest validates; deployed orchestration picks up events; trace-id propagates end-to-end; branching logic for CRITICAL severity verified

### 15.6 Cross-reference

- APEX_Design.md §10 (Orchestration Framework), §11.6 (Trace-ID discipline)
- Flow tab node `w2-orchestrator`

---

## 16. W2.3 — Agent 1 · Assess

### 16.1 Purpose

Read the excursion event, pull the full temperature time-series from Bronze Eventhouse, characterize severity (peak temp, duration, avg temp, door-open events). Writes structured assessment to its audit row.

### 16.2 Inputs

- [ ] Step 15 complete (orchestration dispatches to this agent)

### 16.3 Outputs

- [ ] Agent deployed to Foundry project
- [ ] Agent manifest registered
- [ ] Assess audit-row subtype emitting

### 16.4 Steps

**16.4.1 — Author agent system prompt**

```
You are the Assess agent in APEX cold-chain excursion response.
You read an excursion event and a temperature time-series.
You produce a structured assessment: peak_temp, duration_min, avg_temp, door_event_count, adjacent_fixture_alarm.
You do not make business decisions. You only describe what happened.
If the time-series is incomplete, you surface the gap — do not guess.
Output must match the AssessmentOutput pydantic schema exactly.
```

Hashed and pinned as `assess-v2.1-sha:a1b2`.

**16.4.2 — Author structured output schema**

```python
from pydantic import BaseModel
from datetime import datetime

class AssessmentOutput(BaseModel):
    fixture_id: str
    window_start_ts: datetime
    window_end_ts: datetime
    duration_min: int
    peak_temp: float
    avg_temp: float
    door_event_count: int
    reading_count: int
    data_completeness_pct: float  # how much of the window had readings
    adjacent_fixture_alarm: bool
```

**16.4.3 — Deploy agent**

```bash
apex agent deploy \
  --agent-id agent-cold-chain-assess \
  --version 1.3.0 \
  --prompt apex-bigbox/prompts/assess-v2.1.txt \
  --model gpt-4o-2024-08-06 \
  --tenant bigbox \
  --identity id-apex-agent-assess-bigbox \
  --allowed-tools "fabric-mcp.query_eventhouse,telemetry-mcp.emit_trace,ledger-mcp.append_audit_row"
```

**16.4.4 — Smoke test**

```bash
apex agent invoke agent-cold-chain-assess \
  --input '{"fixture_id": "FIX_BB100_DAIRY_A3", "window_start": "2026-04-23T06:08:00Z", "window_end": "2026-04-23T10:20:00Z"}'
# Expected output:
# {"fixture_id": "FIX_BB100_DAIRY_A3", "duration_min": 252, "peak_temp": 52.0, "avg_temp": 49.1, ...}
```

### 16.5 Owner · Effort · Exit

- **Owner:** Agent Engineer · RC Practice Lead
- **Effort:** 3 SP · ~4 days
- **Exit criteria:** 50-scenario test battery passes; output always matches AssessmentOutput schema; audit row emitted with correct trace-id

### 16.6 Cross-reference

- APEX_Design.md §4 (Reasoning Plane)
- Flow tab node `w2-agent-assess`

---

## 17. W2.4 — Agent 2 · Classify

### 17.1 Purpose

Run FSMA 204 policy corpus against the assessment. Produce severity classification (MINOR / MODERATE / MAJOR / CRITICAL) and per-SKU disposition recommendation.

### 17.2 Inputs

- [ ] Step 16 complete
- [ ] W1 step 9 complete (policy-mcp registered FSMA 204 corpus)

### 17.3 Outputs

- [ ] Classify agent deployed
- [ ] Classification returns per-SKU dispositions
- [ ] Policy-version stamped on every output

### 17.4 Steps

**17.4.1 — Classify agent tool set**

The agent's `allowed_tools`:

- `scml-mcp.list_inventory_by_fixture` — pull the SKUs in the affected fixture
- `scml-mcp.get_lot_provenance` — FSMA 204 lot data per SKU
- `policy-mcp.evaluate_fsma_204` — rule-evaluation tool
- `ledger-mcp.append_audit_row` — emission
- `telemetry-mcp.emit_trace` — trace

**17.4.2 — Output schema**

```python
class Disposition(BaseModel):
    sku_id: str
    units_affected: int
    recommended_action: Literal["SELL_THROUGH", "MARKDOWN", "DESTROY"]
    markdown_pct: int | None = None
    policy_rule_matched: str  # e.g., "dairy_temp_markdown"
    severity: Literal["MINOR", "MODERATE", "MAJOR", "CRITICAL"]

class ClassifyOutput(BaseModel):
    fixture_id: str
    overall_severity: Literal["MINOR", "MODERATE", "MAJOR", "CRITICAL"]
    dispositions: list[Disposition]
    policy_version_used: str
    total_units: int
    total_sku_count: int
```

**17.4.3 — Deploy and smoke test**

```bash
apex agent deploy agent-cold-chain-classify ...
apex agent invoke agent-cold-chain-classify --input <assess output>
# Output validates that 289 units → DESTROY, 91 → MARKDOWN, 32 → SELL_THROUGH on the reference scenario
```

### 17.5 Owner · Effort · Exit

- **Owner:** Agent Engineer · Food Safety SME (client side)
- **Effort:** 5 SP · ~1 week
- **Exit criteria:** classification outputs match client's Food Safety Lead manual classification on a 100-event historical backtest within 96% agreement rate

### 17.6 Cross-reference

- APEX_Design.md §14 (Purview Trust — classification propagation)
- Flow tab node `w2-agent-classify`

---

## 18. W2.5 — Agent 3 · Quantify

### 18.1 Purpose

Turn the classification into dollars. Retail value at full price · markdown value · shrink cost · projected sell-through within expiry window.

### 18.2 Steps summarized

Agent tool set: `merml-mcp.get_current_price`, `merml-mcp.get_elasticity`, `scml-mcp.get_lot_provenance` (for expiry), `ledger-mcp.append_audit_row`.

Output schema:

```python
class QuantifyOutput(BaseModel):
    fixture_id: str
    scenarios: list[Scenario]  # [{action: SELL_THROUGH, units: 32, value: 384.00}, ...]
    total_retail_value_at_full_price: float
    total_expected_value_per_action_plan: float
    total_writeoff: float
    net_savings_vs_destroy_all: float
```

Reference scenario: sell-through 32 units @ full price = $384. Markdown 91 units @ 35% off = $592 recovered. Destroy 289 units = $1,313 write-off. **Net savings vs destroy-all = $1,313.**

### 18.3 Owner · Effort · Exit

- **Owner:** Agent Engineer · Finance SME (client side)
- **Effort:** 4 SP · ~1 week
- **Exit criteria:** dollar calculations match Finance SME's spreadsheet within ±2%

### 18.4 Cross-reference

- APEX_Design.md §16 (Value-Delivery Chain)
- Flow tab node `w2-agent-quantify`

---

## 19. W2.6 — HITL gate moment

### 19.1 Purpose

The orchestrator pauses. Adaptive Card fires to Marisol via Teams. She has 90s median touch-time to approve / modify / reject. Decision stamps into the parent audit row.

### 19.2 Steps

**19.2.1 — Agent calls approvals-mcp**

The Quantify agent's final action:

```python
approval_req = await approvals_mcp.request_approval(
    template_id="cold-chain-excursion-v1",
    recipient_persona="store_ops_lead",
    recipient_store_id="100",
    payload={
        "store_id": "100",
        "fixture_id": "DAIRY_A3",
        "duration_min": 252,
        "peak_temp": 52.0,
        "avg_temp": 49.1,
        "total_units": 412,
        "sku_count": 28,
        "retail_value_usd": 1867,
        "sell_through_units": 32,
        "sell_through_value": 384,
        "markdown_units": 91,
        "markdown_pct": 35,
        "markdown_value": 592,
        "destroy_units": 289,
        "destroy_value": 1313
    },
    trace_id="trc_2026-04-23_0608_bb100_a3",
    timeout_s=300
)
# Returns: {"decision_id": "...", "pending"}
```

**19.2.2 — Orchestrator pauses**

`apex-orchestrator` transitions the run to `paused_for_hitl` state. Poll (or webhook callback) resumes when decision is recorded.

**19.2.3 — Marisol decides**

6:15:00 AM — Card fires to Marisol's Teams mobile.
6:16:30 AM — Marisol taps "Approve all 3".
Teams bot calls `approvals-mcp.record_decision(decision_id, approver_id, decision="approve_all", timestamp)`.

**19.2.4 — Orchestrator resumes**

`record_decision` stamps into the parent audit row's `hitl_status`. Orchestrator resumes with decision payload passed to Agent 4.

**19.2.5 — Audit-row fields at this step**

```
hitl_status            = approved
hitl_approver_id       = marisol.reyes@bigbox.example.com
hitl_approver_role     = store_ops_lead
hitl_decision_payload  = {"decision": "approve_all", "modifications": null}
hitl_elapsed_seconds   = 90
hitl_authority_policy  = hitl-authority-rc-store-ops-lead-v1.0.0
```

### 19.3 Owner · Effort · Exit

- **Owner:** RC Practice Lead · Field Enablement (for Marisol training)
- **Effort:** 4 SP · ~1 week + 2 weeks shadowing
- **Exit criteria:** 10 shadowed events pass — Marisol's decisions match agent recommendations 80%+; median touch-time <120s by event 10

### 19.4 Cross-reference

- APEX_Design.md §9 (HITL Gates), §17 (Human Oversight)
- Flow tab node `w2-hitl`

---

## 20. W2.7 — Agent 4 · Act

### 20.1 Purpose

Execute three parallel downstream actions: POS markdown upload, destroy ticket to refrigeration vendor, pull-team task in store-ops app. Each action emits its own child audit row referencing the parent trace-id.

### 20.2 Steps

**20.2.1 — Parallel action fan-out**

```python
async def act(hitl_payload, quantify_output, trace_id):
    # Parallel execution
    results = await asyncio.gather(
        action_markdown_to_pos(quantify_output, trace_id),
        action_destroy_ticket_to_vendor(quantify_output, trace_id),
        action_pull_team_task(quantify_output, trace_id),
        return_exceptions=True
    )
    # Composite audit row
    await ledger_mcp.append_composite_audit_row(
        parent_trace_id=trace_id,
        child_actions=results
    )
```

**20.2.2 — Action: POS markdown**

```python
async def action_markdown_to_pos(quantify, trace_id):
    # Via scml-mcp or direct Bronze-write depending on integration
    for disp in quantify.dispositions:
        if disp.recommended_action == "MARKDOWN":
            await scml_mcp.apply_markdown(
                sku_id=disp.sku_id,
                store_id=100,
                markdown_pct=disp.markdown_pct,
                reason="cold_chain_excursion",
                trace_id=trace_id
            )
    return {"action": "markdown_to_pos", "status": "success", "units_affected": 91}
```

**20.2.3 — Action: destroy ticket**

```python
async def action_destroy_ticket_to_vendor(quantify, trace_id):
    ticket = await vendor_portal_mcp.create_service_ticket(
        fixture_id="FIX_BB100_DAIRY_A3",
        issue_class="REFRIGERATION_FAILURE",
        severity="high",
        description=f"Temperature excursion 4h 12m, peak 52°F. 289 units condemned.",
        trace_ref=trace_id
    )
    return {"action": "vendor_ticket", "status": "success", "ticket_id": ticket.ticket_id}
```

**20.2.4 — Action: pull-team task**

```python
async def action_pull_team_task(quantify, trace_id):
    task = await store_ops_app.create_task(
        store_id=100,
        task_type="PULL_MARKDOWN",
        sku_list=[d.sku_id for d in quantify.dispositions if d.recommended_action == "MARKDOWN"],
        priority="high",
        assignee_role="pull_team_lead",
        trace_ref=trace_id
    )
    return {"action": "pull_team_task", "status": "success", "task_id": task.id}
```

### 20.3 Owner · Effort · Exit

- **Owner:** Agent Engineer · RC Practice Lead
- **Effort:** 6 SP · ~1.5 weeks
- **Exit criteria:** all 3 actions complete within 30s of HITL approval; composite audit row shows all 3 child actions; idempotent retries verified

### 20.4 Cross-reference

- APEX_Design.md §11.5 (Composite audit row)
- Flow tab node `w2-agent-act`

---

## 21. W2.8 — KPI attribution and audit-row closeout

### 21.1 Purpose

Per-event KPIs emit to the Direct Lake semantic model. Weekly Power BI dashboard rolls up: events-handled, write-off-avoided ($), time-to-brief (min), manager-touch-time (sec), audit-trail completeness (%). Every KPI attributes back to a specific trace-id — not just the aggregate.

### 21.2 Steps

**21.2.1 — Emit KPI fields in audit-row closeout**

```python
await ledger_mcp.append_audit_row(
    trace_id="trc_2026-04-23_0608_bb100_a3",
    event_kind="cold_chain_closeout",
    kpi_fields={
        "writeoff_avoided_usd": 1313,
        "time_to_brief_sec": 480,  # 8 min
        "manager_touch_time_sec": 90,
        "audit_trail_completeness_pct": 100,
        "agent_model_pins": {
            "assess": "gpt-4o-2024-08-06",
            "classify": "gpt-4o-2024-08-06",
            "quantify": "gpt-4o-2024-08-06",
            "act": "gpt-4o-2024-08-06"
        },
        "policy_versions": {"fsma_204": "fsma-204-cold-chain-v1.0.0"}
    }
)
```

**21.2.2 — Publish KPIs to Direct Lake**

Gold measure `writeoff_avoided_usd_sum_weekly` reads `ledger.audit_row` filtered to `event_kind = 'cold_chain_closeout'` and aggregates. Power BI dashboard refreshes every 5 minutes.

**21.2.3 — Dashboard scaffold**

Dashboard for Store Operations VP:

- **Events handled (weekly)** — count
- **Write-off avoided (weekly $)** — sum
- **Median time-to-brief** — p50 duration
- **Median manager touch-time** — p50 seconds
- **Audit-trail completeness** — min across events (target 100%)
- **Drill-through**: any cell drills to the specific trace-id and its full audit row

### 21.3 Owner · Effort · Exit

- **Owner:** Analytics Engineer · Store Operations VP (consumer)
- **Effort:** 4 SP · ~1 week
- **Exit criteria:** dashboard renders; drill-through from KPI aggregate to individual audit row works; attribution verified on 20-event sample

### 21.4 Cross-reference

- APEX_Design.md §16.2 (Worked Example), §11.3 (Downstream Effect)
- Flow tab node `w2-kpi`

---

## 22. W2 Exit Gate

- [ ] **E1** — 30 consecutive events handled end-to-end with no pipeline failure
- [ ] **E2** — Median manager touch-time <120s; p95 <300s
- [ ] **E3** — Median time-to-brief <10min; p95 <15min
- [ ] **E4** — Write-off-avoided KPI tracking within ±10% of pre-pilot baseline model
- [ ] **E5** — Audit-trail completeness = 100% for every event
- [ ] **E6** — FSMA 204 compliance audit (internal) finds no gaps
- [ ] **E7** — Marisol (primary persona) self-reported hours-returned >4 hrs/shift
- [ ] **E8** — 30-event classification-agreement rate with Food Safety Lead >95%
- [ ] **E9** — Commercial envelope (target $5M–$15M) reconciled
- [ ] **E10** — Steering Committee formal approval to scale to W3

---

# Wave 3 — Scale & Fuse

Same scenario, enterprise scope. 2,400 stores. 4,400 fixtures. 85 events/week. Fused with dynamic-markdown and loyalty-churn agents into the Perishables Economics Mesh.

**W3 total effort:** ~50 SP initial + ongoing mesh expansion · multi-year · $8M–$30M envelope
**W3 goal:** $42M/yr network-wide write-off avoided; +52% margin recovery on markdown units (up from 35%); 0 customer complaints from affected top-tier members

---

## 23. W3.1 — Tenant-scope expansion

### 23.1 Steps

- Update tenant manifest: `row_filters.store_id` expands from `["100"]` to all 2,400 stores
- Agent-role updates: `AgentRole.row_filters` mirrors the expansion
- HITL authority policy extends: tier-specific approval — district managers for >$10K write-offs, corporate FSQA for multi-store incidents
- Bronze ingestion scales: from 1 store's OPC-UA feed to 2,400 (regional IoT Edge gateways per geography)
- Vendor-portal-mcp expands: 1 vendor → 4 (typical for 2,400-store network)
- Fabric capacity scales: F32 → F128 or F256

### 23.2 Owner · Effort · Exit

- **Owner:** Practice Lead · Platform Engineer · Delivery Lead
- **Effort:** 10 SP · ~1 month rollout
- **Exit criteria:** 100-store increments successfully onboarded per week; no regression on any W2 KPI

---

## 24. W3.2 — Fusion · Dynamic Markdown mesh

### 24.1 Purpose

The cold-chain agent no longer sets markdown depth in isolation. It calls the Dynamic Markdown agent (rc-markdown-agent) which understands category-wide elasticity and aged-stock trajectory.

### 24.2 Steps

**24.2.1 — Author fusion manifest**

```yaml
# apex-bigbox/meshes/rc-perishables-economics-mesh-v1.0.yaml
manifest_kind: fusion_mesh
mesh_id: rc-perishables-economics-mesh
version: 1.0.0
constituent_agents:
  - agent: agent-cold-chain-classify
    role: excursion_classifier
  - agent: agent-cold-chain-quantify
    role: value_quantifier
  - agent: rc-markdown-agent
    role: elasticity_aware_pricer
handoffs:
  - from: agent-cold-chain-classify
    to: rc-markdown-agent
    on_event: markdown_dispositions_identified
    payload: [sku_ids, per_sku_units, fixture_id]
    payload_enrichment:
      from_tool: merml-mcp.get_elasticity
composed_outcomes:
  - name: sku_specific_markdown_depth
    replaces: cold_chain_blanket_markdown_pct
    expected_margin_lift_pp: 17
```

**24.2.2 — Modify classify agent behavior**

In the old path, Classify set `markdown_pct = 35` (blanket). In the fusion path, Classify emits `recommended_action = MARKDOWN` and the handoff to the markdown agent determines per-SKU depth (15–45%) based on elasticity curves.

**24.2.3 — Commercial envelope expands**

Pilot envelope didn't include rc-markdown-agent. W3 envelope adds it as an included service.

### 24.3 Owner · Effort · Exit

- **Owner:** RC Practice Lead · Analytics Engineer
- **Effort:** 8 SP · ~2 weeks
- **Exit criteria:** 90-event fusion backtest shows margin recovery improves from 35% to >48% on markdown-disposition units

---

## 25. W3.3 — Fusion · Loyalty Churn mesh

### 25.1 Steps

**25.1.1 — Cold-chain emits fused event with at-risk SKU list**

```python
# After classify but before HITL
if len(top_tier_customers_affected) > 0:
    await fusion_bus.emit(
        event="affected_top_tier_customers",
        payload={"sku_list": [...], "48h_purchase_window": "2026-04-21T06:08Z..2026-04-23T06:08Z"}
    )
```

**25.1.2 — Loyalty-churn agent activates**

Joins `CXML.Transaction` (tokenized!) in the 48h window, identifies top-tier members who bought affected SKUs, generates proactive outreach (Teams-mediated "we're tracking this, here's a replacement credit").

**25.1.3 — Detokenization for outreach surface only**

At user-surface time (email-send or in-app notification), `apex-tokenizer.detokenize()` is called by the outreach-surface identity — not by the agent.

### 25.2 Owner · Effort · Exit

- **Owner:** CRM Lead · Loyalty Director (client side)
- **Effort:** 10 SP · ~3 weeks
- **Exit criteria:** 0 customer complaints from affected top-tier members on 30 consecutive excursion events; LTV-recovery tracking verified

---

## 26. W3.4 — Purview trust at enterprise scale

### 26.1 Steps

- Full lineage: SOR → Bronze → Silver → Gold → MCP → Agent → Audit row → KPI — every hop classification-tagged
- DLP policies prevent PHI/PII leakage into Copilot surfaces
- Unified Catalog exposes agent catalog + KPI registry to the business
- Auditor-view: "show me every row that influenced the 6:08 AM Store 100 destroy decision"

### 26.2 Owner · Effort · Exit

- **Owner:** Governance Owner · Internal Audit (client side)
- **Effort:** 12 SP · ~4 weeks
- **Exit criteria:** external FSMA 204 audit passes on 10-event sample; lineage query returns <5s

---

## 27. W3.5 — LEDGER feedback loop

### 27.1 Purpose

LEDGER's aggregated audit rows drive manifest evolution. Patterns in HITL overrides ("managers always reject destroy on SKU X") inform policy refinement.

### 27.2 Steps

- Quarterly LEDGER-derived pattern analysis
- Example pattern: Managers overrode destroy on 12% of produce excursions (vs 2% on dairy)
- Action: policy v1.3 adjusts produce destroy-threshold from 4h to 6h
- Tenants PATCH-upgrade auto on policy bumps

### 27.3 Owner · Effort · Exit

- **Owner:** Practice Lead · Food Safety Compliance Lead (client side)
- **Effort:** ongoing — 4 SP/quarter
- **Exit criteria:** at least 1 manifest or policy evolution per quarter grounded in LEDGER evidence

---

## 28. W3.6 — Enterprise KPI roll-up

### 28.1 Enterprise metrics

| Metric | W2 Pilot | W3 Enterprise |
|--------|----------|----------------|
| Stores | 250 | 2,400 |
| Fixtures | ~1,400 | ~4,400 |
| Events/week | 8 | 85 |
| Write-off avoided | $1,313/event | $42M/yr |
| Manager time returned | 5.2 hr/shift | 22,464 hr/day network-wide |
| Audit completeness | 100% | 100% |
| Margin on markdown | 35% | 52% |
| Top-tier customer complaints per event | baseline | 0 |

### 28.2 Owner · Effort · Exit

- **Owner:** Store Operations VP · CFO
- **Effort:** ongoing — dashboard maintenance
- **Exit criteria:** Enterprise KPI matches network aggregation within ±2%; CFO signs off on the $42M annual run-rate

---

## 29. W3 Exit Gate

- [ ] **W3.G1** — 2,400 stores fully onboarded
- [ ] **W3.G2** — Fusion mesh live; both rc-markdown and loyalty-churn handoffs operating
- [ ] **W3.G3** — Purview enterprise lineage query functional
- [ ] **W3.G4** — Annualized write-off-avoided ≥$35M
- [ ] **W3.G5** — Manifest evolution cadence established (≥1 PATCH/MINOR per quarter grounded in LEDGER)
- [ ] **W3.G6** — CFO run-rate sign-off

---

# Appendices

## Appendix A — RACI by step

| Step | Responsible | Accountable | Consulted | Informed |
|------|-------------|-------------|-----------|----------|
| 1 Addressing | Seller | Account Team Lead | Practice Lead | Delivery Lead |
| 2 Discovery | Solution Architect | Delivery Lead | Food Safety · Store Ops | Practice Lead |
| 3 SOR/Schema | Solution Architect · Data Engineer | Delivery Lead | Client EA | Governance |
| 4 Tenant | Platform Engineer | Solution Architect | Azure Admin | Governance |
| 5 Bronze | Data Engineer | Platform Engineer | SOR Owners | Solution Architect |
| 6 Tokenizer | Data Engineer | Governance Owner | Security | Delivery Lead |
| 7 Silver | Data Engineer | RC Practice Lead | Food Safety | Solution Architect |
| 8 Gold | Analytics Engineer | Data Engineer | Analytics Consumers | Practice Lead |
| 9 MCP | MCP Owner | Platform Engineer | Agent Engineers | Practice Lead |
| 10 Identity | Security Engineer | Governance Owner | Entra Admin | Solution Architect |
| 11 LEDGER | Platform Engineer | Governance Owner | Auditor (internal) | Practice Lead |
| 12 HITL | Practice Lead | Solution Architect | Primary Persona (Marisol) | Field Enablement |
| 14 Event | Data Engineer | RC Practice Lead | Ops Center | Solution Architect |
| 15 Orchestration | RC Practice Lead | Solution Architect | Agent Engineers | Delivery Lead |
| 16–18 Agents | Agent Engineer | RC Practice Lead | SMEs (client) | Solution Architect |
| 19 HITL live | Practice Lead | Field Enablement | Primary Persona | Delivery Lead |
| 20 Act | Agent Engineer | RC Practice Lead | Vendor Integrations | Solution Architect |
| 21 KPI | Analytics Engineer | Store Ops VP | CFO | Practice Lead |
| 23 Scale | Practice Lead · Platform Engineer | Delivery Lead | Change Management | CFO |
| 24 Markdown fusion | RC Practice Lead | Solution Architect | Merchandising Director | Analytics |
| 25 Loyalty fusion | CRM Lead | Loyalty Director | Privacy Officer | Practice Lead |
| 26 Purview | Governance Owner | Internal Audit | External Auditor | CFO |
| 27 Feedback | Practice Lead | Food Safety Lead | Policy Owner | Compliance |
| 28 Enterprise KPI | Store Ops VP | CFO | Practice Lead | Board |

## Appendix B — Manifest inventory

Manifests created during the build:

1. `apex-bigbox/tenants/bigbox.manifest.json` (§4)
2. `apex-bigbox/silver/tokenization-config.yaml` (§6)
3. `apex-bigbox/policies/fsma-204-cold-chain.yaml` (§9, §11)
4. `apex-bigbox/policies/hitl-authority-rc.yaml` (§12)
5. `apex-bigbox/hitl/cold-chain-card.json` (§12)
6. `apex-bigbox/events/cold-chain-excursion.event-manifest.yaml` (§14)
7. `apex-bigbox/orchestrations/rc-cold-chain-response-v1.2.yaml` (§15)
8. `apex-bigbox/agents/agent-cold-chain-assess.agent-manifest.yaml` (§16)
9. `apex-bigbox/agents/agent-cold-chain-classify.agent-manifest.yaml` (§17)
10. `apex-bigbox/agents/agent-cold-chain-quantify.agent-manifest.yaml` (§18)
11. `apex-bigbox/agents/agent-cold-chain-act.agent-manifest.yaml` (§20)
12. `apex-bigbox/meshes/rc-perishables-economics-mesh-v1.0.yaml` (§24)

All manifests are Git-versioned. PATCH/MINOR/MAJOR bump classification enforced by `apex classify-bump`. Promotion discipline: Dev → Test → UAT → Prod per the bundled-versioning rule (APEX_Design.md §3).

## Appendix C — Commercial envelope summary

| Wave | Duration | Cost envelope | Effort | Primary deliverable |
|------|----------|----------------|--------|----------------------|
| Approach (§§1–3) | 2–4 weeks | $150K–$400K | 18 SP | Discovery + Schema Mapping + SoW |
| **W1 Foundation** | 4–8 weeks | $500K–$2M | 40 SP | Tenant rails operational; end-to-end smoke green |
| **W2 Pilot** | 6–15 months | $5M–$15M | 35 SP + ongoing | 30 events handled; KPIs proven; SteerCo approval |
| **W3 Scale & Fuse** | Multi-year | $8M–$30M | 50 SP + ongoing | 2,400 stores; fusion mesh live; $42M/yr run-rate |

Total program envelope: $13M–$47M over 18–36 months; durable annual value $42M+.

---

**End of Build Guide.**

For cross-referenced design material: APEX_Design.md §§4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 19, 20
For roadmap traceability: Roadmap.md BL.P.* items referenced in each step
For delivery schedule: Orchestrator.md Sprints 1–27 (many already complete)
For visual context: APEX-Stacked-Architecture-Narrated.html Flow tab — the 24-node walk this guide implements
