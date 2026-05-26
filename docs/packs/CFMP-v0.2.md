# Customer Focused Merchandise Pack (CFMP) — v0.2 Design

**Status**: Draft for ARB review (aligned with APEX-Architecture-v5.docx, May 2026)
**Owner**: Keven Markham, VP — Deloitte's Microsoft Practice (DMTSP)
**Date**: 2026-05-23
**Version history**:
- **v0.2** (2026-05-23): Wayfinding service refactored to Azure Maps Creator; cross-references to APEX-Architecture-v5 added; Section 4 rewritten; portal landing reframed as CFMP demo.
- v0.1 (2026-05-23): Initial 10-asset bundle design.

**Pack position**: Customer-side counterpart to the architecture's **Retail Merchandising Pack v1** (Chief Merchant / DMM persona; MERML; ships Q2 FY27 per Architecture v5 §9.6). CFMP is a sibling, not a replacement — different buyer (CMO/CX-VP), different HITL surface (`customer_phone`, not Teams), different persona type (`customer`, not employee).

**Cloud profiles**: APEX-M primary; APEX-G / APEX-A via shared 10-asset bundle
**Primary schemas**: MERML (merchandise) + CXML (customer experience), with SCML (inventory) for OSA scenarios
**New schema introduced**: `CFMP.StoreMap` (thin manifest mapping retailer floor plan → Azure Maps Creator Dataset ID)
**Status of working demo**: Live at `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io` on `gpt-5-mini` (Microsoft Agent Framework 1.6.0 GA). Wayfinding currently runs the local-fallback path; Azure Maps Creator activates on env-var configuration (see §4.4).

---

## 1. Why CFMP

Existing RC packs (Store Ops, Pricing, Returns) are organized by **operator function**. CFMP is the first APEX pack organized by **customer moment-in-life** — choose, select, buy, services. That reframing matters because:

- The buyer is different (CMO / CX-VP, not Ops VP).
- The HITL surface is different (customer's phone, not Teams).
- The persona model is different (loyalty ID + consent, not Entra group).
- The value-narrative ties directly to **trip conversion, basket size, NPS, loyalty retention** — what marketing-funded execs are graded on.

Our existing Vision AI Dev Kit work already lights up **3 of the catalog's device-led scenarios** (`rc-sampling-table-engagement`, `rc-cart-dwell-abandonment-rescue`, `rc-greeter-impact-measurement`). CFMP packages that work as a scoped **Deloitte agentic-services delivery engagement** and extends it across the full customer journey.

> **Positioning note: CFMP is not a product.** It is a scoped Deloitte delivery engagement on the APEX framework, sold per industry under the standard Service Envelope tiers (BVA · DCIF · ISV Marketplace burndown · SI Teaming POC · T&M · Client direct). Deloitte never receives ECIF directly on APEX-M (Independence rule).

---

## 2. The Customer Journey Spine

The Pack is organized around four customer moments. Every scenario, every Adaptive Card, every Virtual View in the Pack maps to exactly one phase.

| Phase | Customer's question | Pack capability | Primary device |
|---|---|---|---|
| **CHOOSE** | "What should I buy?" | Recipes, pairings, dietary filters, personalized offers, in-store ad attribution | Phone app, kiosk, sampling-table camera |
| **SELECT** | "Where is it / is it on the shelf?" | Indoor wayfinding, aisle locator, OSA / shelf-gap detection, planogram compliance | Phone app + ceiling cams |
| **BUY** | "How do I pay & leave?" | Scan-and-go, self-checkout assist, queue prediction, BOPIS pickup, returns trust | SCO cam, phone, BOPIS counter cam |
| **SERVICES** | "What's next from you?" | Loyalty winback, complaint triage, review summarization, sentiment, NPS | Phone, contact center |

---

## 3. Scenario shortlist — 18 scenarios

All 18 are sourced from `APEX-Scenario-Chains.xlsx` except `cfmp-wayfinding-walk-to-product`, which is net-new and authored here (see Section 4). Full chain detail per scenario is in `CFMP-Scenario-Chains-v0.1.xlsx`.

### CHOOSE (5)
| Scenario ID | KPI | Device |
|---|---|---|
| `rc-personalized-offer-targeting` | +24% redemption | – |
| `rc-product-review-summary-generation` | +8% PDP conversion | – |
| `rc-product-search-relevance` | +19% search conversion | – |
| `rc-in-store-advertising-impact` | +9% trip-conversion | Vision AI Dev Kit · ad / screen engagement |
| `rc-sampling-table-engagement` | +50% promo ROI clarity | Vision AI Dev Kit · **shipping today** |

### SELECT (6)
| Scenario ID | KPI | Device |
|---|---|---|
| **`cfmp-wayfinding-walk-to-product`** (NEW) | Time-to-find −60% · trip basket +8% | Phone + storemap |
| `rc-on-shelf-availability-oos-reduction` | −34% OOS | Vision AI Dev Kit · shelf-facing OOS |
| `rc-shelf-gap-realtime-restock-dispatch` | OOS minutes −45% · lost-sale +2.1pp | Vision AI Dev Kit · shelf-void (custom DLC) |
| `rc-aisle-engagement-attribution` | +1.5pp category conversion | Vision AI Dev Kit · aisle dwell + pickup |
| `rc-end-cap-display-roi-tracking` | +22% display ROI | Vision AI Dev Kit · end-cap dwell |
| `rc-shelf-price-label-compliance-audit` | −92% SPL errors | Vision AI Dev Kit · SPL audit |

### BUY (4)
| Scenario ID | KPI | Device |
|---|---|---|
| `rc-customer-wait-time-prediction-at-checkout` | −41% wait time | Vision AI Dev Kit · queue-length count |
| `rc-cart-dwell-abandonment-rescue` | physical cart-abandon recovery +12% | Vision AI Dev Kit · **shipping today** |
| `rc-self-checkout-shrink-detection` | −48% SCO shrink | Vision AI Dev Kit · SCO SKU-mismatch |
| `rc-bopis-pickup-counter-load` | BOPIS wait −40% · NPS +8pt | Vision AI Dev Kit · BOPIS counter queue |

### SERVICES (3)
| Scenario ID | KPI | Device |
|---|---|---|
| `rc-loyalty-churn-prediction-winback` ⭐ | −22% churn | – |
| `rc-loyalty-tier-migration-prediction` | +9pp tier retention | – |
| `rc-product-complaint-triage` | −34% response time | – |

⭐ = APEX Featured Chain (full chain published in parent xlsx).

**Sub-tier mapping**: Pack Lite ships 3 scenarios. Standard ships 10. Enterprise ships all 18. Strict APEX sub-tier additive rule applies — no scenario re-platforms when a client moves up a sub-tier.

---

## 4. Indoor Wayfinding — architectural design

### 4.1 Technology decision: Azure Maps Creator

**v0.2 update**: Wayfinding runs on **Azure Maps Creator** (Indoor Maps + Wayfinding REST API), not a custom storemap-yaml runtime. This decision flows from three principles:

1. **Don't build what Azure ships.** Microsoft already runs a productized indoor-maps platform with Drawing-Package conversion, dataset/tileset/stateset lifecycle, live occupancy, accessibility routing, and a Web SDK indoor renderer.
2. **APEX-M is cloud-native by design.** Per APEX-Architecture-v5 §6 (Cloud Profile contract), every service the framework consumes is reached through the 14-interface contract. Azure Maps slots in as a profile-specific implementation of "Maps & Wayfinding," shared across the family (APEX-G uses Google Maps Geospatial Creator; APEX-A uses Amazon Location Service indoor maps; the abstract interface stays identical).
3. **The storemap is still the moat, but as data, not code.** Once a retailer's CAD floor plans are captured as Azure Maps Creator Drawing Packages, the indoor dataset is the durable asset. Switching cost is high; we are not in the business of writing graph routers.

### 4.2 Reference architecture

```
                  ┌──────────────────────────────────────────────────┐
                  │  Retailer's CAD / GIS team                        │
                  │  (one-time per store + on remodel)                │
                  └────────────────────┬─────────────────────────────┘
                                       │  DWG / IndoorML drawing pkg
                                       ▼
   ┌────────────────────────────────────────────────────────────────┐
   │  Azure Maps Creator (per-tenant Creator resource)              │
   │  ├─ Drawing-Package Conversion Service                         │
   │  ├─ Dataset    (vector geometry: units, levels, openings)     │
   │  ├─ Tileset    (rendered tiles for Web SDK indoor view)        │
   │  ├─ Stateset   (live occupancy / availability state)           │
   │  └─ Wayfinding REST API  (POST /wayfinding/route)              │
   └────────────────────┬───────────────────────────────────────────┘
                        │
                        │  Wayfinding REST (signed)
                        ▼
   ┌────────────────────────────────────────────────────────────────┐
   │  APEX-M CFMP Wayfinding Service  (interface implementation)    │
   │  orchestrator/azure_maps.py                                    │
   │   - SKU → planogram unit_id resolver (MERML)                   │
   │   - Customer beacon node → Creator point                       │
   │   - Calls Azure Maps; renders to canonical route dict          │
   │   - Falls back to local storemap.yaml for dev/offline          │
   └────────────────────┬───────────────────────────────────────────┘
                        │  canonical route { zone, aisle, distance_m, directions, geometry }
                        ▼
   ┌────────────────────────────────────────────────────────────────┐
   │  Agent Framework tool: route_to_product                        │
   │  Surfaces route in structured JSON reply                       │
   └────────────────────┬───────────────────────────────────────────┘
                        ▼
   ┌────────────────────────────────────────────────────────────────┐
   │  Customer phone Adaptive Card (HITL surface = customer_phone)  │
   │  ├─ Inline route card (zone/aisle badges + steps)              │
   │  └─ Azure Maps Web SDK indoor view (v0.3 — renders geometry)   │
   └────────────────────────────────────────────────────────────────┘
```

### 4.3 What Azure Maps Creator gives us (vs. building it ourselves)

| Capability | Azure Maps Creator | Build-it-yourself |
|---|---|---|
| Indoor floor-plan ingestion | Drawing-Package Conversion (DWG → IndoorML → Dataset) | Custom GIS pipeline + format spec |
| Multi-floor / multi-level | Native (level, units, openings) | Custom graph + level-traversal logic |
| Wayfinding routing | `POST /wayfinding/route` w/ accessibility constraints (min-width, avoid stairs) | Hand-coded Dijkstra + accessibility hand-rolled |
| Live state (open/closed/occupied) | Stateset (PATCH at event time) | Custom store + cache + invalidation |
| Web rendering | Azure Maps Web SDK indoor view w/ floor selector, route polyline, custom layers | Custom canvas/SVG + viewport state mgmt |
| Multi-region / GA | GA in US + EU; per-tenant Creator resource | Build region failover yourself |
| Auth | Subscription key OR managed identity (Entra) | Build auth |
| Integration with APEX-G / APEX-A | Maps interface abstract; Creator-equivalents on each cloud | N/A (custom code re-platforms) |

### 4.4 Configuration (per-tenant env vars)

The CFMP orchestrator activates Azure Maps Creator when both of these are set on the Container App:

| Env var | Purpose |
|---|---|
| `DEMO_AZURE_MAPS_DATASET_ID` | Creator Dataset ID for this retailer's flagship store |
| `DEMO_AZURE_MAPS_KEY` | Subscription key (shared-signature path) |
| **OR** `DEMO_AZURE_MAPS_CLIENT_ID` + managed identity | Azure-native key-less path (preferred for production) |
| `DEMO_AZURE_MAPS_GEOGRAPHY` | `us` (default) or `eu` (Creator account geography) |

When unset, the orchestrator returns a route from a local YAML graph (`storemap.yaml`) and tags the response with `source: "local_storemap_yaml"`. The portal renders an honest "local fallback" badge on the route card so the demo narrative is transparent.

### 4.5 The CFMP.StoreMap manifest (Pack asset #1, new VV)

This is the thin Pack-side overlay on top of Azure Maps Creator. It tells the orchestrator which Creator Dataset corresponds to which store, and which planogram feed populates the SKU → unit_id mapping. Captured once per store at onboarding.

```yaml
# views/cfmp.storemap_view.yaml
view_id: cfmp.storemap_view
schema: CFMP.StoreMap
source:
  retailer_store_id: 100
  azure_maps:
    dataset_id: "01234567-89ab-cdef-0123-456789abcdef"
    tileset_id: "76543210-fedc-ba98-7654-3210fedcba98"
    stateset_id: "11111111-2222-3333-4444-555555555555"
    geography: "us"
  planogram_feed: merml.planogram_v3
sku_to_unit:
  source_table: merml.planogram_unit_assignment
  refresh: nightly
```

### 4.6 The agent tool (unchanged shape, new backend)

```python
@tool
def route_to_product_tool(
    sku: Annotated[str, Field(description="The SKU the customer wants to find.")],
    from_node: Annotated[str, Field(description="Customer's current Azure Maps Creator point id, or a beacon/QR anchor that resolves to one.")] = "n_entry",
) -> str:
    """Compute the walking route from the customer's current position to the
    product's shelf location. Backed by Azure Maps Creator Wayfinding REST
    API when configured, with local-storemap fallback for dev."""
```

### 4.7 Data sources

| Data | Source | Refresh cadence |
|---|---|---|
| Store layout | Retailer CAD/DWG → Drawing Package → Creator Dataset | Once per store + on remodel |
| Product → Creator unit_id | Planogram (MERML) joined to Creator Dataset's unit_assignment | Nightly |
| Live unit state (open/closed/occupied) | Creator Stateset (PATCH from device events) | Realtime |
| Customer location (beacon → point) | Phone BLE / Wi-Fi RTT → APEX-side resolver | Every ~2 s |
| Camera fallback "you-are-here" | Existing ceiling cams (Vision AI Dev Kit) | On request |

### 4.8 What the storemap unlocks beyond wayfinding

Once the Azure Maps Creator dataset is in place, **8 other CFMP capabilities ride on it for free**:

- "Find an associate" — associate phone reports last beacon → Creator point
- "Skip the queue" — Stateset for SCO lanes (open/closed/queue length)
- "Get a tour" — multi-waypoint wayfinding through promo end-caps
- BOPIS counter routing — same Wayfinding API, different unit_id target
- Spill-hazard alerts that include "you're 12m from one" — distance via Wayfinding API
- Aisle-engagement attribution gets real x/y coordinates (Stateset)
- Shelf-gap dispatch knows which associate is closest (Wayfinding distance matrix)
- Accessibility routing (min-width + avoid-stairs constraints, native to the API)

**Strategic note**: the moat is the captured Creator dataset, not custom code. Retailer's CAD onboarding is the high-friction step; afterwards, every CFMP scenario benefits.

### 4.9 v0.3 roadmap: Azure Maps Web SDK indoor view

Demo currently surfaces the route as a card (badges + numbered directions). v0.3 adds the **Azure Maps Web SDK indoor view** to the portal — renders the Tileset, drops a customer marker at `from_unit_id`, paints the route polyline returned by the Wayfinding API. ~3 days of portal work; deferred until a real retailer Creator dataset is available (synthetic SVG render is not worth the time).

---

## 5. The 10-Asset Bundle (per APEX standard, customized for CFMP)

| # | Asset | CFMP specifics |
|---|---|---|
| 1 | **VV manifests** (`views/`) | `merml.product_with_planogram_location`, `merml.osa_by_aisle`, `cxml.customer_session_with_route`, `cxml.cart_dwell_event`, `cxml.dietary_profile`, `cfmp.storemap_view` (new) |
| 2 | **Scenario manifests** (`scenarios/`) | 18 YAMLs (3 Lite / 10 Standard / 18 Enterprise) |
| 3 | **Source adapters** (`adapters/`) | POS + Loyalty CRM + Planogram + Beacon vendor (Estimote/Kontakt) + Vision AI Dev Kit MQTT + Phone-app event stream |
| 4 | **Adaptive Cards** (`cards/`) | Customer-facing JSON for phone + kiosk (NEW transport — see §6.2) + operator cards for Teams (associate dispatch, restock alerts) |
| 5 | **Persona map** (`personas.yaml`) | **`customer`** (NEW persona type), `store_associate`, `assistant_manager`, `store_manager`, `merch_director`, `loyalty_director` |
| 6 | **Demo data** (`demo-data/`) | Synthetic store with 800 products + planogram, 30 beacons, 50 simulated shoppers — runs on a laptop (extends our existing pgvector seed) |
| 7 | **BVA worksheet** (`bva/cfmp-roi.xlsx`) | Roll-up of journey-phase KPIs: trip conversion, basket size, NPS, churn, BOPIS attach |
| 8 | **Sample SOW** (`envelopes/`) | Lite / Standard / Enterprise templates; pricing $150K / $750K / $2.4M |
| 9 | **Acceptance tests** (`tests/`) | 80+ tests: scenario chain dry-runs, MCP contract tests, wayfinding shortest-path correctness, beacon-loss recovery, customer-consent gating |
| 10 | **Runbook + training** (`runbooks/`) | Field install guide for beacons + storemap capture, store-team training deck, customer-consent FAQ |

---

## 6. Foundation enhancements required (ARB items)

These are the design decisions to flag for the ARB. **All three are Foundation enhancements, not just CFMP costs** — they unlock the entire customer-side of the APEX market and benefit every future customer-facing Pack (Banking-Customer, Telco-Customer, Hospitality-Guest).

Per APEX-Architecture-v5 §6 (Cloud Profile Contract), these are extensions to the 14-interface set.

### 6.1 New persona type: `customer`

Existing APEX personas are all employees with Entra/identity-group bindings. The customer has none of that. Extend `personas.yaml` to support:

```yaml
- id: customer
  identity_binding:
    source: loyalty_id
    scope: opted_in_only
  consent_gate: required
  channel: customer_phone
```

Reusable across future Packs. Drives all customer-side LedgerRow attribution.

### 6.2 New HITL surface: `customer_phone`

APEX-M's default HITL is Teams (interface #9 per Architecture v5 §6). The customer doesn't have Teams. The customer's "approve" gate is on their phone (consent prompt). Add a new transport binding:

- **APEX-M**: signed-link push via Azure Notification Hubs → phone app → MCP callback
- **APEX-G**: Firebase Cloud Messaging
- **APEX-A**: Amazon Pinpoint / SNS

Implementation = signed-link push + MCP callback. Same model on all three clouds.

### 6.3 New interface: Maps & Wayfinding (proposed interface #15)

Architecture v5 lists 14 interfaces today (#1–#12 base + #13 Cache/Redis + #14 Live Reference Data per Chapter 21). CFMP proposes **#15: Maps & Wayfinding**, with these cloud-profile implementations:

| Profile | Implementation |
|---|---|
| APEX-M | Azure Maps Creator (Indoor Maps + Wayfinding REST API + Web SDK) |
| APEX-G | Google Maps Geospatial Creator |
| APEX-A | Amazon Location Service indoor maps + routing |

The agent code consumes the abstract interface only; profile YAML wires the implementation. Same swap-rule as every other interface.

---

## 7. 6-Agent Fleet wiring for CFMP

Same six agents, customer-specific manifests. Notable HITL changes:

| Agent | Role in CFMP | HITL gate |
|---|---|---|
| 1. Assess | "Customer is near aisle 7 + dwell 90s + no pickup" → maybe needs help | Auto |
| 2. Classify | "Browsing" vs "stuck" vs "lost" vs "abandoning" | Auto |
| 3. Quantify | Trip-conversion risk, expected basket-loss $ | Auto |
| 4. Approve | **Two-track**: (a) operator card to associate (Teams), (b) customer-side nudge on phone with opt-out | **Both** — operator approves dispatch; customer consents to nudge |
| 5. Act | Dispatch associate + push phone nudge + log to LEDGER | – |
| 6. Evidence | LedgerRow + reasoning-trace + **customer-consent hash** (audit-defensible privacy) | – |

The customer-consent hash in Evidence-Write is the GDPR/CCPA-safe substrate. Every customer-facing action lands a row that says "we did X to customer Y at timestamp Z under consent token C" — provably attributable.

---

## 8. Roadmap from current demo

### What's live today (verified 2026-05-23, post-v0.2)
- `rc-sampling-table-engagement` (Vision AI Dev Kit demo)
- `rc-cart-dwell-abandonment-rescue` (proactive associate)
- **`cfmp-wayfinding-walk-to-product`** (route_to_product agent tool — currently on local-fallback path; Azure Maps Creator activates on env-var configuration)
- 800-product catalog in pgvector with semantic search
- gpt-5-mini agent w/ recipes, pairings, dietary, cart, scan-and-go barcode, follow-up chips, route cards
- Microsoft Agent Framework SDK (1.6.0 GA) + multi-provider toggle (OpenAI / Anthropic)
- Portal landing reframed as CFMP demo (CHOOSE · SELECT · BUY · SERVICES journey)

### Gap to Pack Lite ($150–250K, 4–6w)
1. **Wayfinding production path** — provision Creator resource per tenant, upload retailer Drawing Package, populate `CFMP.StoreMap` manifest (1 wk dev, 2 wks Creator dataset capture)
2. **Azure Maps Web SDK indoor view** in the portal — render Tileset + route polyline (3 days)
3. BVA worksheet with our 3 existing scenarios + wayfinding (1 wk)
4. Sample SOW template (2 days)
5. Lite acceptance test suite (1 wk)

### Gap to Pack Standard ($750K–$1.5M, 12–16w)
Add 7 more scenarios from the shortlist (OSA, shelf-gap, end-cap ROI, queue prediction, loyalty churn, complaint triage, in-store ad impact) — each is one agent tool + one Adaptive Card + one VV manifest. Standard engineering work, parallelizable.

### Gap to Pack Enterprise ($1.5–3.5M, 6–9m)
All 18 scenarios + multi-store rollout playbook + Operate readiness + cross-pack Fuse with MFG (cold-chain) and **AXLE** (dealer/parts for big-box hardware).

---

## 9. Roll-up KPIs (for the BVA worksheet)

Pack-level outcomes that tie all 18 scenarios together — these are what the BVA workshop proves.

| Pack-level KPI | Mechanism | Wave-2 target |
|---|---|---|
| Trip conversion | Choose + Select scenarios | **+14%** |
| Basket size | Recipes + pairings + offers + wayfinding | **+8% units / trip** |
| First-time wayfinder success | Wayfinding scenario | **>92% reach product** |
| In-store NPS | Greeter + spill + queue + wayfinding | **+9 pt** |
| Cart-abandon recovery (physical) | Proactive + cart-dwell | **+12%** |
| Loyalty churn (top tier) | Featured chain `loyalty-churn-winback` | **−22%** |
| Operate-readiness | Pack-level | All 18 scenarios green in CI |

---

## 10. Open questions for Wave-1 BVA workshop

1. **Beacons or Wi-Fi RTT** as the localization primary? Pick one to keep adapter count down.
2. **Whose phone app?** SDK into retailer's existing app (path to production) vs CFMP-branded Deloitte demo app (path to closeable pilot)?
3. **Customer-identity binding** — loyalty ID is the obvious primary, but the anonymous-customer flow needs design (consent-on-first-tap).
4. **CFMP merges into RC Store Ops pack, or stays separate?** Recommendation: separate. Different buyer (CMO/CX-VP, not Ops VP), different envelope curve.

---

## 11. Independence stance

CFMP commercial materials follow APEX standard:
- "Deloitte's Microsoft practice" / "DMTSP" — never "partner" or "alliance"
- Microsoft funding routes via ISV Marketplace + SI Teaming, never direct ECIF to Deloitte
- APEX-G / APEX-A versions have no independence wrinkle (Deloitte does not audit Google or AWS)

---

## 12. Related artifacts

- `CFMP-Scenario-Chains-v0.1.xlsx` — full 18-scenario chain (W1/W2/W3, persona, KPI, device)
- `APEX-Scenario-Chains.xlsx` — parent catalog (source of 17 of 18 scenarios)
- **`APEX-Architecture-v5.docx`** — parent architecture (25 chapters, ConCon conformance package). CFMP-relevant chapters: §6 Cloud Profile Contract (14 interfaces), §9.6 Retail Merchandising Pack (sibling), §10 Scenario Chains, §11 Service Envelopes, §17 Agent Intelligence Layer, §21 Live Translation Layer (interface #14)
- `APEX-Design-v3.pptx` — APEX framework teaching deck (28 slides)
- **Azure Maps Creator** documentation:
  - Indoor Maps overview: https://learn.microsoft.com/azure/azure-maps/creator-indoor-maps
  - Wayfinding REST API (preview): https://learn.microsoft.com/rest/api/maps-creator/wayfinding
  - Drawing Package format (IndoorML): https://learn.microsoft.com/azure/azure-maps/drawing-requirements
- Working demo: `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io` (CFMP v0.2 — sampling-table + cart + proactive + dietary + recipes + wayfinding, gpt-5-mini, Azure Maps fallback active until per-tenant Creator dataset is provisioned)

---

*Internal · Deloitte Microsoft Technology & Services Practice · Prepared by Keven Markham, VP*
