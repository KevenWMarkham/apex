# CFMP Multi-Agent Orchestration on Microsoft Agent Framework v0.1

**Status**: Design + implementation reference for the CFMP demo
**Owner**: Keven Markham, VP — Deloitte's Microsoft Practice
**Date**: 2026-05-23
**Maps to**: APEX-Architecture-v5 §6 (Cloud Profile Contract) · §11 (6-Agent Fleet) · §17 (Agent Intelligence Layer)

---

## 1. Why now

Six months in, the CFMP customer-side agent has accumulated **30+ tools** across catalog search, recipes, dietary filtering, wayfinding, cart, cart-dwell upsell, auto-orders, pickup lots, perishables, profile, prescriptions, special dates, Azure Maps services, and APEX framework introspection. A single-agent topology hits four walls:

| Wall | Symptom in our build |
|---|---|
| **Tool-selection accuracy** | gpt-5-mini's tool-selection accuracy drops sharply past ~20 tools per agent; we already see it misroute wayfinding-vs-search on edge cases |
| **Instruction bloat** | The system prompt is now ~280 lines covering 11 domains; every domain's rules dilute the rest |
| **Latency** | Each turn loads 30+ tool schemas into the model context · larger prompts = more tokens = slower + more expensive |
| **Audit attribution** | Hard to tell from a single LedgerRow whether the agent reasoned about wayfinding *or* auto-orders — the trace is a single decision blob |

The next features (PARS bundle confirmation, Azure Maps drive-here, prescription consent gate, vision-based pantry localization) push us further. **The architecture has to decompose.**

Microsoft Agent Framework (1.6.0 GA, in use today) supports proper multi-agent patterns — sub-agents, agent-as-tool, workflows, magentic orchestration. The APEX 6-Agent Fleet design (Assess · Classify · Quantify · Approve · Act · Evidence-Write) is the **audit wrapper** that goes on top of whatever specialist agents do the domain work. The two compose cleanly.

---

## 2. Target architecture

```
                    ┌──────────────────────────────────────────────┐
                    │           CUSTOMER UTTERANCE                 │
                    │   "Mom's birthday's next week — find a       │
                    │    nice wine I'd like + add bread to my      │
                    │    pickup for this afternoon"                │
                    └──────────────────────┬───────────────────────┘
                                           ▼
                ┌──────────────────────────────────────────────────────┐
                │   ORCHESTRATOR AGENT (gpt-5-mini)                    │
                │   Microsoft Agent Framework `Agent`                  │
                │   Intent classification · route · compose            │
                │                                                       │
                │   Tools = the 6 specialists below (via .as_tool())   │
                └──┬──────────┬──────────┬──────────┬──────────┬──┬───┘
                   │          │          │          │          │  │
        ┌──────────┘          │          │          │          │  └──────────┐
        ▼                     ▼          ▼          ▼          ▼             ▼
 ┌────────────┐ ┌─────────────────┐ ┌──────────┐ ┌─────────────┐ ┌─────────────┐ ┌──────────┐
 │ CATALOG    │ │ AUTO-REPLENISH  │ │ PROFILE  │ │ PERISHABLES │ │ CART+PICKUP │ │ WAYFINDER│
 │  search    │ │  PARS           │ │ + EVENTS │ │ + ALERTS    │ │  + CHECKOUT │ │  + AZURE │
 │  recipes   │ │  enroll/pause   │ │ prefs    │ │ throw-out   │ │  add-to-    │ │  MAPS    │
 │  dietary   │ │  bundles        │ │ events   │ │ auto-reord. │ │  pickup     │ │          │
 │  pairings  │ │  spend YTD      │ │ rx-gate  │ │             │ │  confirm    │ │          │
 └─────┬──────┘ └────────┬────────┘ └────┬─────┘ └──────┬──────┘ └──────┬──────┘ └────┬─────┘
       │                 │               │              │               │             │
       │  Each specialist has a NARROW tool bundle, a FOCUSED prompt,                  │
       │  and runs on the cheapest acceptable model (gpt-4.1-mini for                  │
       │  most; gpt-5-mini only for the orchestrator + Profile)                        │
       │                                                                               │
       └────────────────── shared substrate ────────────────────────────────────────────┘
                                       │
                                       ▼
       ┌───────────────────────────────────────────────────────────────────────┐
       │   APEX 6-AGENT FLEET (audit + governance wrapper)                     │
       │                                                                        │
       │   1. Assess      — what kind of decision is this?                     │
       │   2. Classify    — material? sensitive? consent-required?              │
       │   3. Quantify    — $ impact, time-to-act, urgency band                 │
       │   4. Approve     — HITL gate when threshold trips                      │
       │   5. Act         — dispatch the action (cart, pickup, order)          │
       │   6. Evidence    — append 14-field LedgerRow with hash chain          │
       └───────────────────────────────────────────────────────────────────────┘
```

**Two layers, distinct responsibilities:**

- **Domain layer (specialists)** — own the verbs. Catalog *searches*. Wayfinder *routes*. Auto-Replenish *enrolls*. Each is small, focused, replaceable.
- **Governance layer (APEX 6-Agent Fleet)** — owns the audit. Wraps every customer-facing action with the Assess→Evidence chain. Never invents new actions; it gates and records the ones specialists propose.

---

## 3. Specialist roster

Each specialist is a Microsoft Agent Framework `Agent` instance built via `client.as_agent(name=..., instructions=..., tools=[...])`. The full list:

| # | Specialist | Owns | Tool bundle (existing functions become @tool calls) | Model |
|---|---|---|---|---|
| 1 | **Catalog & Discovery** | Search · recipes · dietary · pairings | `search_products` · `get_product` · `recipe_for_items` · `suggest_pairings` · `apply_dietary_filter` | gpt-4.1-mini |
| 2 | **Wayfinder** | Indoor + outdoor routing | `route_to_product` · `geocode_address` · `drive_to_store` · `store_info` | gpt-4.1-mini |
| 3 | **Auto-Replenish (PARS)** | Enrollment · bundles · history · suggestions | `enroll_auto_order` · `pause_auto_order` · `list_my_auto_orders` · `confirm_bundle` · `list_bundles` · `get_suggestions` · `ytd_spend` | gpt-4.1-mini |
| 4 | **Profile & Events** | Preferences · member ID · special dates · prescriptions | `get_profile` · `update_preferences` · `list_events` · `list_prescriptions` (gated) | gpt-5-mini (better personalization reasoning) |
| 5 | **Perishables & Pantry** | Expiration tracking · alerts · auto-reorder triggers | `list_perishables` · `perishable_alerts` · `mark_thrown_out` · `auto_reorder_trigger` | gpt-4.1-mini |
| 6 | **Cart & Pickup** | Cart actions · BOPIS pickup lots · checkout HITL | `add_to_cart` · `clear_cart` · `add_to_pickup_lot` · `confirm_pickup` · `checkout` | gpt-4.1-mini |
| 7 | **Orchestrator** | Intent classification · routing · response composition | All 6 specialists as `.as_tool()` | gpt-5-mini (decision quality matters) |

Notes:
- **Each specialist has a small, focused system prompt** (~30-50 lines instead of 280). Domain-specific rules don't dilute each other.
- **Models are per-specialist**. Most run on the cheaper gpt-4.1-mini ($0.15/M input, $0.60/M output). Profile + Orchestrator use gpt-5-mini ($0.25/M / $2.00/M) because routing quality and personalization reasoning matter most there.
- **Substantial token savings**: rough math is ~60% reduction vs. monolith.
- **Each tool emits a LedgerRow with specialist attribution** — `payload.specialist = "wayfinder"` etc. — so the audit trail becomes much clearer.

---

## 4. The orchestrator's job

```
turn → orchestrator → [select specialist(s)] → [run specialist(s)] → compose reply
```

The orchestrator does three things and only three things:

1. **Intent classification**. Read the customer utterance + scene context. Tag with one or more specialist intents.
2. **Routing**. Call the specialist(s) — either sequentially (when one depends on another) or in parallel (when independent). Microsoft Agent Framework's `Workflow` supports this declaratively; for v0.1 we use the agent-as-tool pattern.
3. **Composition**. Aggregate specialist outputs into a single coherent reply. Apply the structured JSON contract (reply · follow_ups · mentioned_products · cart_actions · route) the portal expects.

The orchestrator does **not** call domain tools directly. It treats specialists as opaque capabilities. This means a specialist can be swapped (new model, new vendor, new logic) without touching the orchestrator.

### Routing example

> *"Mom's birthday's next week — find a nice wine I'd like + add bread to my pickup for this afternoon"*

| Phase | Agent | Output |
|---|---|---|
| 1. Intent classification | Orchestrator | `[profile, catalog, cart_pickup]` |
| 2a. Profile lookup | Profile & Events | "Mom's birthday is in 5d · gift budget $60 · customer prefers pinot noir / syrah, OR + Napa, $15-35" |
| 2b. Catalog search | Catalog & Discovery | "Found 3 matching wines under $35 · top match: Willamette Pinot Noir 2023, $28" |
| 2c. Add to pickup | Cart & Pickup | "Sourdough loaf added to pickup lot (curbside, ready in 2h) · total $26.45" |
| 3. Composition | Orchestrator | One coherent reply that surfaces the wine card + the pickup confirmation + a follow-up chip "Want me to add the wine to the same pickup?" |

The customer experiences this as one helpful turn. The audit trail shows three separate specialist calls, each with its own LedgerRow, all linked by `trace_id`.

---

## 5. Microsoft Agent Framework patterns we use

The SDK gives us four ways to compose agents. Pick by problem shape:

| Pattern | Microsoft Agent Framework class | When to use | CFMP usage |
|---|---|---|---|
| **Agent-as-tool** | `agent.as_tool()` | One agent delegates to a specialist as if it were a tool — LLM picks at runtime | ✅ **v0.1 — primary pattern**: orchestrator includes specialists as tools |
| **Sequential workflow** | `SequentialOrchestration` / declarative `Workflow` | Fixed pipeline (e.g., Assess → Classify → Quantify → Approve → Act → Evidence) | **v0.2** — wrap APEX 6-Agent Fleet as a SequentialOrchestration over every domain action |
| **Magentic** | `MagenticManager` / `MagenticBuilder` | Open-ended planning where agents collaborate on a multi-step plan | **v0.3** — for the cross-channel attribution scenario from CFMP §6 |
| **Group chat** | `GroupChatOrchestration` | Specialists deliberate before committing | Not used (would dilute audit attribution; CFMP needs single-author decisions) |

For v0.1 we use **Agent-as-tool** because it's the smallest viable change from the existing monolith — same `ask_agent()` signature, same JSON reply contract, same portal endpoints. The orchestrator just delegates instead of doing everything itself.

---

## 6. APEX 6-Agent Fleet integration

APEX's 6-Agent Fleet (per Architecture v5 §11) is the **audit wrapper** that runs around every domain action. The six agents in name order:

1. **Assess** — signals → contextualized exception
2. **Classify** — by severity / type / regulatory class
3. **Quantify** — financial / operational impact estimate
4. **Approve** — HITL Adaptive Card if threshold tripped
5. **Act** — dispatch the action to the SOR
6. **Evidence-Write** — hash-chained LedgerRow

In v0.1, this is **already partially implemented** via `apex_integration.record_decision()` — it computes HITL status (Approve), dispatches the tool calls (Act), and emits the LedgerRow (Evidence-Write). What multi-agent adds is **explicit Assess / Classify / Quantify steps** before the action runs:

```python
def fleet_pipeline(specialist_decision: dict) -> dict:
    """Wrap a specialist's proposed action in the APEX 6-Agent Fleet."""
    ctx     = assess(specialist_decision)             # 1. Assess
    cls     = classify(ctx)                            # 2. Classify
    impact  = quantify(cls)                            # 3. Quantify (e.g., $ delta)
    hitl    = approve_or_wait(impact)                  # 4. Approve (HITL gate)
    if hitl.status == "PENDING": return hitl.card()    # block on approval
    result  = act(specialist_decision, ctx)            # 5. Act (run the tool)
    row_id  = evidence_write(specialist_decision,
                              ctx, cls, impact, hitl,
                              result)                  # 6. Evidence-Write
    return result | {"ledger_row_id": row_id}
```

This pipeline runs **inside the orchestrator's "Act" branch**, after the specialist proposes an action but before the cart / pickup / order is actually committed. The customer-facing latency stays the same (most decisions skip HITL); the audit trail becomes complete.

---

## 7. Implementation plan

### Phase 1 — Build the orchestrator alongside the monolith (this iteration)
- ✅ Write design doc (this file)
- ✅ Create `orchestrator/orchestrator.py` defining 6 specialists + 1 orchestrator
- ✅ Wire `/agent/ask-multi` endpoint as A/B alternative to existing `/agent/ask`
- ✅ Deploy; both paths live; portal still uses `/agent/ask`

### Phase 2 — Migration (next iteration)
- Add a `MULTI_AGENT_ENABLED` env var; flip portal calls to `/agent/ask-multi` once tested
- Refactor existing `@tool` functions into per-specialist modules (`tools/catalog.py`, `tools/wayfinder.py`, etc.)
- Add explicit Assess / Classify / Quantify steps to `apex_integration.record_decision()`
- Deprecate the monolithic agent (`_get_agent()`)

### Phase 3 — Workflow patterns (later)
- Switch APEX 6-Agent Fleet from inline pipeline to `SequentialOrchestration`
- Add Magentic patterns for the cross-channel attribution scenario (in-store + in-home + online unified LEDGER, per CHC v0.2 §8)
- Add specialist health monitoring + per-specialist canary deployments

---

## 8. Why this is the right call now (vs later)

| Argument | Verdict |
|---|---|
| "Single agent works fine for the demo" | True today, false at 40+ tools. We're at 30+. The crossover is now. |
| "Multi-agent is over-engineering for one customer" | Multi-agent is **how the framework was designed to scale**. Microsoft Agent Framework's whole multi-agent surface (agent-as-tool, workflow, magentic) exists for exactly this reason. |
| "Latency goes up with more agent calls" | Specialists run on cheaper/smaller models. Token savings + the orchestrator can call specialists in parallel for independent intents. Net latency typically improves. |
| "Harder to debug" | Cleaner, actually. Each LedgerRow carries `specialist = "wayfinder"` etc. Trace inspection is by specialist, not by tool blob. |
| "Risk of regression during cutover" | Mitigated by A/B with `/agent/ask-multi` — keep the monolith live until the orchestrator is verified across all demo scenarios. |

---

## 9. Cost model

Per-turn token usage (rough estimates for a mid-complexity turn):

| Configuration | Input tokens | Output tokens | Per-turn cost (Azure OpenAI list) |
|---|---|---|---|
| **Monolithic agent** (gpt-5-mini · 30+ tools · 280-line prompt) | ~4,800 | ~600 | $0.0024 |
| **Multi-agent**: orchestrator (gpt-5-mini, light prompt) + 1-2 specialists (gpt-4.1-mini, focused prompts) | ~1,200 + ~2,000 = 3,200 | ~600 | $0.0014 |
| **Savings per turn** | | | **~42%** |

At 500 turns/day (the demo's current rate), that's ~$0.50/day saved. At 50K turns/day production (Pack Standard), that's ~$50/day · ~$1.5K/mo — significant but not the primary motivation. The **routing accuracy and audit-attribution improvements** are.

---

## 10. Related artifacts

- **APEX Architecture v5**: `docs/reference/Architecture-and-Reference/APEX-Architecture-v5.docx` — Ch 11 (6-Agent Fleet) · Ch 17 (Agent Intelligence Layer) · Ch 6 (Cloud Profile Contract — Interface #8 LLM / AI services)
- **CFMP v0.2**: `docs/packs/CFMP-v0.2.md` — §7 (6-Agent Fleet wiring for CFMP)
- **PARS v0.1**: `docs/packs/PARS-Private-Auto-Replenishment-v0.1.md` — §6 (Foundation enhancements, including the autonomy spectrum that gates Approve)
- **Working demo**: `https://ca-visionkit-portal.gentlestone-9b49b099.eastus2.azurecontainerapps.io` — `/agent/ask` (monolith) + `/agent/ask-multi` (this design)
- **APEX teaching deck (parent)**: `docs/reference/_Archive/APEX-Design-v3.pptx` — Slide 11 (6-Agent Fleet) · Slide 33 (Agent Intelligence Layer · v4 extensions: Memory, Reasoning depth, Calibration, Specialists, Outcome learning, Constitution, Persona Model)

---

## 11. Phase 2 architectural decisions (post-v0.1 directives)

Three architectural decisions arrived during v0.1 review that materially change
what the agents *do* and how they reach data. Captured here so the build keeps
pulling toward them.

### 11.1 Profile is **learned**, not filled

The customer never sits down and fills out a preference form. Instead, the
specialist agents continuously observe and propose:

- **Cart & Pickup specialist** watches purchase frequency → learns cadence.
- **Catalog specialist** notices repeated searches for the same family → infers preference (`prefers pinot noir`, `dark roast`, `low-sugar`).
- **Auto-Replenish specialist** detects 3 consecutive same-cycle orders → proposes enrollment.
- **Profile specialist** parses chat utterances ("we just had a baby", "mom's coming next month", "switching to oat milk") → updates the `customer_profile.preferences` JSON blob with a *proposed* delta.

Every learned profile update sits in a `proposed` state until the customer
confirms via an Adaptive Card on the home_kiosk or sonos_voice surface — the
same HITL gate the Auto-Replenish enrollment uses. This is the **APEX 6-Agent
Fleet Approve step** wrapping every implicit-learning event.

```
buying habit OR chat answer
   ↓
specialist observes
   ↓
APEX 6-Agent Fleet — Assess · Classify · Quantify
   ↓
score: learning confidence
   ↓ HIGH (≥0.85) → auto-write to profile (Evidence-Write only)
   ↓ MEDIUM     → write to `proposed_preferences` queue · surface as kiosk card
   ↓ LOW        → discard
```

The portal `/profile` page transitions from an *editor* to a *monitor*. The customer sees
*"We noticed you've ordered Founders Centennial 3 times in the last 6 weeks. Add 'Founders'
to your beer brewery list? [Yes] [Not really] [Why are you asking?]"*

### 11.2 MCP servers as the data plane (Gold Tier Virtual Views)

Specialists currently call `product_db`, `auto_orders`, `customer_profile` Python
modules directly. That's a v0 shortcut. The APEX framework (per Architecture v5
§6, Cloud Profile Interface #4 In-Lake Federator and §11 6-Agent Fleet)
specifies that all agent data access flows through **MCP servers** that map to
**Virtual Views** on the medallion's Gold tier:

```
            Agent specialist
                  │
                  │ MCP tool call (JSON-RPC)
                  ▼
    ┌─────────────────────────────────┐
    │ MCP SERVER                       │
    │  • fabric-mcp                    │
    │  • merml-mcp (Retail Merch)      │
    │  • cxml-mcp  (Customer)          │
    │  • parsml-mcp (Auto-Replenish)   │  ← NEW for PARS
    │  • tcml-mcp  (Telco-Customer)    │  ← NEW for CHC
    └─────────────────────────────────┘
                  │ federated SQL
                  ▼
    ┌─────────────────────────────────┐
    │ GOLD TIER VIRTUAL VIEWS          │
    │  cxml.customer_profile_v         │
    │  cxml.special_dates_v            │
    │  parsml.active_enrollments_v     │
    │  parsml.upcoming_bundles_v       │
    │  parsml.perishable_inventory_v   │
    │  merml.product_with_planogram_v  │
    └─────────────────────────────────┘
                  │ Silver → Gold
                  ▼
              Bronze (medallion)
```

**Why this matters for the demo**: every specialist tool's `result_hash` in
the LedgerRow already points to a content-addressed blob. When we cut over
to MCP, the call site swaps `product_db.search_products(...)` for
`mcp_call("fabric-mcp.search_products", ...)` and the audit trail keeps
working unchanged. The LEDGER becomes the truth substrate; MCP becomes the
read substrate; Virtual Views become the durable contract retailers and
auditors review.

**Phase 2.1** — wrap existing modules with an `mcp_client.py` shim that
mirrors MCP's JSON-RPC signature. Specialists call the shim. No real MCP
server yet; the wrapping creates the *contract surface* so we can swap in
real MCP servers later without touching specialists.

**Phase 2.2** — stand up the first real MCP server (`parsml-mcp` is the
natural starter — small surface, fully demoable). The Virtual Views
(`parsml.active_enrollments_v`, `parsml.upcoming_bundles_v`, etc.) become
the published interface. Other retailers consuming the Pack get the same
view names.

### 11.3 Orders + Profile run in the **background**; HITL is the exception

The customer doesn't drive Auto-Orders. The customer doesn't fill out a
profile. The specialists do all of it, continuously, and **only interrupt
when an APEX 6-Agent Fleet gate trips**:

| Trigger | Threshold | Specialist action | HITL surface |
|---|---|---|---|
| Cart auto-build approaches threshold | $50 / per-day cap | Auto-Replenish builds the next bundle automatically | Kiosk card *"Bundle for Tues delivery — confirm?"* |
| Profile learning event | confidence ≥ 0.85 | Profile specialist writes the inference directly to `customer_profile.preferences` | Daily digest SMS (passive notification) |
| Profile learning event | confidence 0.5–0.85 | Specialist writes to `proposed_preferences` | Kiosk card *"We noticed X — true?"* |
| Sensitive category (Rx, Diaper, OTC) | always | Specialist proposes but never acts | Active HITL · explicit consent · LEDGER attestation |
| Wind-down detection | 2+ cycles without consumption | Specialist proposes pause | Kiosk card *"Haven't seen X for a while — pause?"* |
| Perishable expiring | ≤ 2 days | Auto-Replenish moves next-order-date up | Passive notification *"Milk expires tomorrow; next delivery moved to Mon"* |
| Substitution proposal | promo save ≥ $0.50 | Catalog proposes swap | Passive notification + reversible in-flight |

The portal Auto-Orders and Profile pages are **observability surfaces**, not
control surfaces. They render *"here's what the agents are doing on your
behalf, and here's where they're stuck waiting for you."*

The 6-Agent Fleet's **Approve step** is where the HITL happens. When the
gate doesn't trip, the system runs invisibly. That's the product promise:
the household runs out of milk, but never thinks about milk.

---

## 12. Phase 2 build queue

Concrete next builds, ordered by demo impact:

1. **mcp_client.py shim** (~1 hr) — wrap existing modules in MCP-shape calls; specialists call the shim; no behavior change but contract surface is established.
2. **Background Observer agent** (~2 hr) — periodic scan (every 5 min in demo, every N hours in prod) that:
   - Runs Auto-Replenish detection over recent cart history
   - Runs Profile inference over recent chat history
   - Emits proposed deltas to `proposed_preferences` + `proposed_enrollments` queues
   - Each proposal lands a LedgerRow tagged `apex.agent.proposed`
3. **Proposed-deltas review UI** (~2 hr) — on `/profile` and `/auto-orders` pages, surface pending agent proposals with [Yes / Not really / Tell me more] chip actions
4. **First real MCP server: parsml-mcp** (~1 day) — Python aiohttp service exposing `parsml.active_enrollments_v`, `parsml.upcoming_bundles_v`, etc. via JSON-RPC. Specialists swap from `auto_orders.py` direct calls to MCP calls.
5. **Gold Tier Virtual View definitions** (~1 day) — declarative YAML manifests per VV (per APEX-Architecture-v5 §9 VV manifest spec) for the 6+ views above.

After this queue, every Phase 1 capability is reached through MCP, the
profile becomes silently learned, and the customer-facing surfaces become
observability dashboards rather than data-entry forms.

---

## 13. Live build status (post-deploy update · 2026-05-23)

The following Phase 1 capabilities are now **deployed and reachable in the demo**:

### 13.1 Microsoft Agent Framework Fleet — live
- 1 top-level Orchestrator (gpt-5-mini) + 4 specialist sub-agents:
  - `catalog_specialist` (search · recipes · dietary · pairings)
  - `wayfinder_specialist` (storemap + Azure Maps route)
  - `auto_replenish_specialist` (PARS enroll / pause / view)
  - `concierge_specialist` (proactive moments · weather · life context)
- Wired via the `Agent.as_tool()` pattern in `agent_orchestrator.py`.
- Routed at `/agent/ask-multi` (portal `/api/agent/ask-multi` proxy).
- Per-turn tool log + product list + route slot share the same parser as the monolith, so audit attribution is unified.

### 13.2 Meal Planner — live
- Taste-palette aware, perishable-prioritizing, budget-bounded 7-day plan.
- Tables: `meal_plans`, `meal_plan_slots`, `meal_plan_shopping`, `recipe_library`, `customer_budget`.
- 13 seed recipes spanning breakfast / lunch / dinner / snack with `is_quick` / `is_on_the_go` / `leftover_friendly` flags.
- Leftover-friendly dinner → next-day lunch reheat auto-flow.
- Shopping list separates "have already" (pantry / auto-arriving / expiring) from recipe-driven buys.
- Portal page `/meal-plan`: 7×4 grid + budget bar + palette chips + leftover-tomorrow callout + quick/on-the-go strips + "Suggest a new plan" CTA.
- Every plan generate / archive emits a LedgerRow.

### 13.3 Concierge — live
- Always-on observer over **weather · expirations · events · budget · orders · prescriptions · leftovers · guests · mood**.
- Surfaces short HITL "moments" the customer accepts / dismisses / snoozes.
- Weather feed: **Azure Maps Weather Services** (current + 5-day + severe alerts), 30-min cache in `concierge_weather_cache`.
- Tables: `concierge_moments`, `concierge_weather_cache`, `concierge_settings`.
- De-dupe via `source_signature` so we don't re-emit the same moment hourly.
- Moment kinds emit example nudges like:
  - *"Saturday's a perfect grill day (84°F clear) — want a cookout plan?"*
  - *"PRO-005 expires in 2 days — move salad to tonight?"*
  - *"Mom's birthday in 5 days — celebration plan ready?"*
  - *"This week's plan is $69 over budget — try the cheaper swap?"*
  - *"Lisinopril refill in 4 days — add to pickup lot?"*
  - *"Cold snap Tue-Thu (hi 34°F) — switch to comfort-food plan?"*
- Portal page `/concierge`: weather strip + moments grid with severity-tinted cards + per-kind counts.
- Available to the agent fleet via `concierge_specialist` (tools: `list_concierge_moments`, `get_weather`, `generate_concierge_moments`).
- Every accept / dismiss emits a LedgerRow.

### 13.4 Architecture page updates
`/architecture` now reflects:
- Orchestrator row reads "Microsoft Agent Framework Fleet (Orchestrator + 4 specialists)" with route + module references
- **Azure Maps Weather Services** added under cloud AI services (shares the maps-visionkit account + DEMO_AZURE_MAPS_KEY)
- New apex-substrate rows for the live Fleet + planned MCP-to-Gold-VV mappings:
  - `parsml-mcp → Gold_VV_AutoOrders` (Phase 2)
  - `cxml-mcp → Gold_VV_Customer` (Phase 2)
  - `merml-mcp → Gold_VV_Catalog` (Phase 2)
  - `weather-mcp` (wraps Azure Maps Weather for Concierge — Phase 2)
- CFMP capability rows now include Auto-Orders/PARS · Profile · **Meal Planner** · **Concierge** · **Multi-agent route**

### 13.5 Routes summary

| Route | Surface | What it does |
|---|---|---|
| `/api/agent/ask` | Monolith agent | All-tools single-prompt |
| `/api/agent/ask-multi` | **Fleet** | Orchestrator + 4 specialists |
| `/api/meal-plan` | **Meal Planner snapshot** | Active plan + budget + quick/on-the-go + leftover-lunch |
| `/api/meal-plan/generate` | **Meal Planner** | Build a new 7-day plan |
| `/api/meal-plan/{id}` | **Meal Planner** | Hydrate one plan |
| `/api/meal-plan/{id}/validate` | **Meal Planner** | Palette coverage report |
| `/api/concierge` | **Concierge snapshot** | Moments + weather + counts |
| `/api/concierge/generate` | **Concierge** | Re-scan all signals |
| `/api/concierge/accept`, `/api/concierge/dismiss`, `/api/concierge/snooze` | **Concierge HITL** | Per-moment actions |
| `/api/concierge/weather` | **Concierge** | Azure Maps Weather (cached) |
| `/api/auto-orders/*` | PARS | 7 capabilities |
| `/api/profile/*` | Profile | Preferences · events · pickup · perishables · prescriptions |
| `/api/wayfinding/*` | Wayfinder | Storemap + Azure Maps route |

---

*Internal · Deloitte's Microsoft Technology & Services Practice · Prepared by Keven Markham, VP · 2026-05-23*

