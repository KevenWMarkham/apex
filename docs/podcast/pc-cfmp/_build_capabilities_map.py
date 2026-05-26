"""
CFMP Capabilities Map - code scanner + JSON emitter.

Walks C:\\code\\iot_device\\, maps source files to hand-authored capability
boxes via fnmatch on code_globs, emits a JSON the map HTML embeds inline.

Usage:
    python _build_capabilities_map.py             # prints JSON to stdout
    python _build_capabilities_map.py > data.json # capture
"""
from __future__ import annotations
import json
import re
import sys
import fnmatch
import datetime
from pathlib import Path

# Force UTF-8 stdout for emoji-bearing JSON on Windows.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

IOT = Path(r"C:\code\iot_device")

# --------------------------------------------------------------------------------------
# Lanes (11)
# --------------------------------------------------------------------------------------
LANES = [
    {"id": "L1",  "name": "Discovery & Lot Composition",                "emoji": "\U0001F6D2", "episode": "03", "secondary": ["01"],       "color": "#5DCAA5"},
    {"id": "L2",  "name": "Lot Lifecycle, Replenish & Home",            "emoji": "\U0001F6CD️", "episode": "04", "secondary": [],     "color": "#AFA9EC"},
    {"id": "L3",  "name": "In-Store Experience",                        "emoji": "\U0001F3EA", "episode": "03", "secondary": ["04", "06"], "color": "#F2A623"},
    {"id": "L4",  "name": "Fulfillment & Pickup",                       "emoji": "\U0001F69A", "episode": "07", "secondary": [],          "color": "#E24B4A"},
    {"id": "L5",  "name": "Voice Channel · Sonos",                  "emoji": "\U0001F50A", "episode": "06", "secondary": [],          "color": "#E8C547"},
    {"id": "L6",  "name": "Agent Orchestration & MCP",                  "emoji": "\U0001F916", "episode": "02", "secondary": [],          "color": "#6FB6E5"},
    {"id": "L7",  "name": "Trust, Identity, Consent & HIPAA",           "emoji": "\U0001F512", "episode": "08", "secondary": ["02"],      "color": "#9B7BE0"},
    {"id": "L8",  "name": "Operations, Portal & Multi-Tenant",          "emoji": "⚙️", "episode": "05", "secondary": ["02"],    "color": "#3DD9C4"},
    {"id": "L9",  "name": "Recipe Capture & Cultural Breadth",          "emoji": "\U0001F373", "episode": "11", "secondary": [],          "color": "#E87B3C"},
    {"id": "L10", "name": "Pairings & Mixers",                          "emoji": "\U0001F377", "episode": None, "secondary": [],          "color": "#C89D3A"},
    {"id": "L11", "name": "Privacy-First Architecture · Home & Telco Edge", "emoji": "\U0001F6E1️", "episode": "12", "secondary": [], "color": "#5DCAA5"},
]

# --------------------------------------------------------------------------------------
# Personas (5)
# --------------------------------------------------------------------------------------
PERSONAS = [
    {"id": "sarah",   "name": "Sarah Chen",       "emoji": "\U0001F469‍\U0001F373", "role": "Power-User Parent"},
    {"id": "robert",  "name": "Robert Park",      "emoji": "\U0001F474",                 "role": "Senior Shopper"},
    {"id": "diana",   "name": "Diana Park",       "emoji": "\U0001F91D",                 "role": "Caregiver"},
    {"id": "marcus",  "name": "Marcus Thompson",  "emoji": "\U0001F3D4️",           "role": "Vacation Renter"},
    {"id": "priya",   "name": "Priya",            "emoji": "\U0001F6DF",                 "role": "Operator"},
]

# --------------------------------------------------------------------------------------
# Seller's-playbook discovery openers (7 -- includes the privacy 7th)
# --------------------------------------------------------------------------------------
OPENERS = [
    {"id": "O1", "text": "How many AI copies of customer data do you create?",                                   "lanes": ["L1", "L6", "L7"]},
    {"id": "O2", "text": "When a regulator asks you to reproduce an agent decision, can you?",                   "lanes": ["L6", "L7"]},
    {"id": "O3", "text": "Is your identity reality one primary cloud or genuinely cross-cloud?",                  "lanes": ["L7"]},
    {"id": "O4", "text": "What does your customer hear from your brand when they're not looking at a screen?",   "lanes": ["L5", "L3"]},
    {"id": "O5", "text": "How does your operator know a refill cue was suppressed last night?",                  "lanes": ["L8", "L7", "L5"]},
    {"id": "O6", "text": "How many providers can deliver a single agent-composed shopping plan?",                "lanes": ["L4", "L1"]},
    {"id": "O7", "text": "Does your assistant listen to everything in your home -- or only what you ask?",       "lanes": ["L11", "L5", "L7"]},
]

# --------------------------------------------------------------------------------------
# Capabilities -- hand-authored ~95 boxes across 11 lanes.
# Status taxonomy: completed | in_progress | not_started | implemented_not_podcasted | gap | proposed
# --------------------------------------------------------------------------------------
CAPABILITIES = [
    # ===== L1 -- Discovery & Lot Composition =====
    {
        "id": "C1.1", "lane": "L1", "name": "SCAN-first home screen (camera is the front door)",
        "status": "completed", "progress_pct": 100, "episode": "03",
        "design_ref": "CFMP-Mobile-ScanFirst-Design.md §1-3",
        "personas": ["sarah", "robert", "marcus"],
        "code_globs": ["mobile/app/page.tsx", "mobile/components/CameraScanner.tsx",
                        "mobile/components/ScanResultCard.tsx", "mobile/app/api/scan/identify-image/*",
                        "mobile/app/api/scan/route.ts"],
        "see_also": ["C1.6", "C3.3"], "gaps": [],
        "mobile_parity": "live"
    },
    {
        "id": "C1.2", "lane": "L1", "name": "LOT noun -- the unifying primitive",
        "status": "completed", "progress_pct": 100, "episode": "03",
        "design_ref": "CFMP-Mobile-Design-Document.md §2 (LOT model)",
        "personas": ["sarah", "robert", "diana", "marcus"],
        "code_globs": ["orchestrator/lots.py", "mobile/app/api/lots/*",
                        "mobile/components/LotsStrip.tsx", "db/02_lots.sql"],
        "see_also": ["C2.1"], "gaps": [],
        "mobile_parity": "live"
    },
    {
        "id": "C1.3", "lane": "L1", "name": "Shopping Lot archetype (trip-bound)",
        "status": "completed", "progress_pct": 100, "episode": "03",
        "design_ref": "CFMP-Mobile-Design-Document.md §2.1",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/lots.py", "orchestrator/shopping_trips.py"],
        "see_also": ["C2.1", "C3.1"], "gaps": [],
        "mobile_parity": "live"
    },
    {
        "id": "C1.4", "lane": "L1", "name": "StayLot archetype (vacation/cabin location)",
        "status": "completed", "progress_pct": 100, "episode": "03",
        "design_ref": "CFMP-Mobile-Lots-Expert-Focus.md §3 (StayLot)",
        "personas": ["marcus"],
        "code_globs": ["orchestrator/lots.py"],
        "see_also": ["C11.6"], "gaps": [],
        "mobile_parity": "live"
    },
    {
        "id": "C1.5", "lane": "L1", "name": "Care-Lot archetype (proxy shopping for a dependent)",
        "status": "completed", "progress_pct": 100, "episode": "03",
        "design_ref": "CFMP-Mobile-Lots-Expert-Focus.md §4 (Care-Lot)",
        "personas": ["diana", "robert"],
        "code_globs": ["orchestrator/lots.py", "orchestrator/customer_profile.py"],
        "see_also": ["C7.10"], "gaps": [],
        "mobile_parity": "live"
    },
    {
        "id": "C1.6", "lane": "L1", "name": "Scan-coupon flow (barcode -> instant savings)",
        "status": "completed", "progress_pct": 100, "episode": "03",
        "design_ref": "CFMP-Mobile-Design-Document.md §3 (Coupons)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/coupons.py", "orchestrator/scan_history.py",
                        "db/03_scan_history.sql"],
        "see_also": ["C3.3"], "gaps": [],
        "mobile_parity": "partial"
    },
    {
        "id": "C1.7", "lane": "L1", "name": "Meal-plan composition (recipes -> lot)",
        "status": "in_progress", "progress_pct": 70, "episode": "11",
        "design_ref": "CFMP-Mobile-Design-Document.md §6 (Recipe Library)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/meal_planner.py", "mobile/app/api/meal-plan/route.ts",
                        "mobile/app/plan/*"],
        "see_also": ["C9.1", "C9.2"],
        "gaps": ["Library exists but no capture flows: no YouTube ingest, no friend-shared import, no heirloom OCR"],
        "mobile_parity": "partial"
    },
    {
        "id": "C1.8", "lane": "L1", "name": "Scan photo-of-label (vision identification)",
        "status": "completed", "progress_pct": 100, "episode": "03",
        "design_ref": "CFMP-Mobile-ScanFirst-Design.md §4 (label vision)",
        "personas": ["sarah", "robert"],
        "code_globs": ["mobile/app/api/scan/identify-image/*", "orchestrator/image_ocr.py",
                        "orchestrator/product_resolver.py", "orchestrator/product_db.py"],
        "see_also": ["C1.1"], "gaps": [],
        "mobile_parity": "partial"
    },
    {
        "id": "C1.9", "lane": "L1", "name": "Scan-receipt to close lot",
        "status": "in_progress", "progress_pct": 40, "episode": "03",
        "design_ref": "CFMP-Mobile-Use-Cases.md §5 (receipt close)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/scan_history.py", "orchestrator/shopping_trips.py"],
        "see_also": ["C3.7"],
        "gaps": ["Receipt OCR -> line-item match against trip lot incomplete; no shrinkage reconciliation"],
        "mobile_parity": "partial"
    },
    {
        "id": "C1.10", "lane": "L1", "name": "Scan-pantry to replenish (camera -> auto-orders)",
        "status": "in_progress", "progress_pct": 55, "episode": "04",
        "design_ref": "CFMP-Mobile-Design-Document.md §4 (replenish)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/auto_orders.py", "orchestrator/scan_history.py",
                        "mobile/app/api/scan/history/*"],
        "see_also": ["C2.2"],
        "gaps": ["Scanned-pantry snapshot does not yet feed cadence model; manual approval still required for every order"],
        "mobile_parity": "partial"
    },
    {
        "id": "C1.11", "lane": "L1", "name": "AI-detected on-camera product chips (filmstrip)",
        "status": "completed", "progress_pct": 100, "episode": "03",
        "design_ref": "CFMP-Mobile-ScanFirst-Design.md §5 (filmstrip UI)",
        "personas": ["sarah"],
        "code_globs": ["mobile/components/AiDetectChips.tsx", "mobile/components/IdentifiedItemsStrip.tsx",
                        "mobile/components/ProductFilmstrip.tsx"],
        "see_also": ["C1.1"], "gaps": [],
        "mobile_parity": "live"
    },

    # ===== L2 -- Lot Lifecycle, Replenish & Home =====
    {
        "id": "C2.1", "lane": "L2", "name": "Trip lifecycle (draft -> in-flight -> settling -> closed)",
        "status": "completed", "progress_pct": 100, "episode": "04",
        "design_ref": "CFMP-Mobile-Design-Document.md §4 (Trip lifecycle)",
        "personas": ["sarah", "marcus"],
        "code_globs": ["orchestrator/shopping_trips.py", "mobile/app/api/trips/*",
                        "mobile/app/trip/*"],
        "see_also": ["C1.3", "C3.1"], "gaps": [],
        "mobile_parity": "live"
    },
    {
        "id": "C2.2", "lane": "L2", "name": "Auto-replenish pantry model (standing approval)",
        "status": "completed", "progress_pct": 100, "episode": "04",
        "design_ref": "CFMP-Mobile-Design-Document.md §4.3 (Replenish HITL)",
        "personas": ["sarah", "robert"],
        "code_globs": ["orchestrator/auto_orders.py", "mobile/app/api/auto-orders/*",
                        "portal/app/api/auto-orders/*", "mobile/app/api/auto-orders/bundles/*"],
        "see_also": ["C1.10", "C8.5"], "gaps": [],
        "mobile_parity": "partial"
    },
    {
        "id": "C2.3", "lane": "L2", "name": "Home channel (speaker delivers when phone is closed)",
        "status": "completed", "progress_pct": 100, "episode": "04",
        "design_ref": "CFMP-Sonos-Design-Document.md §2 (home channel)",
        "personas": ["sarah", "robert"],
        "code_globs": ["orchestrator/sonos_cloud.py", "orchestrator/sonos_player.py",
                        "orchestrator/trip_audio.py"],
        "see_also": ["C5.1", "C5.2"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C2.4", "lane": "L2", "name": "Customer preferences profile (smart defaults)",
        "status": "completed", "progress_pct": 100, "episode": "04",
        "design_ref": "CFMP-Mobile-Preferences-Expert-Focus.md §2-4",
        "personas": ["sarah", "robert", "diana"],
        "code_globs": ["orchestrator/customer_profile.py", "mobile/app/api/profile/*",
                        "mobile/app/profile/*", "mobile/app/me/*"],
        "see_also": ["C7.9"], "gaps": [],
        "mobile_parity": "partial"
    },
    {
        "id": "C2.5", "lane": "L2", "name": "Mobile UI revamp (warm-midnight design system)",
        "status": "completed", "progress_pct": 100, "episode": "04",
        "design_ref": "CFMP-Mobile-UI-Revamp.md §1-3",
        "personas": ["sarah", "robert"],
        "code_globs": ["mobile/app/globals.css", "mobile/app/theme.css", "mobile/app/layout.tsx",
                        "mobile/components/BottomNav.tsx"],
        "see_also": [], "gaps": [],
        "mobile_parity": "live"
    },
    {
        "id": "C2.6", "lane": "L2", "name": "Senior mode on Mobile (large type, simplified flows)",
        "status": "in_progress", "progress_pct": 60, "episode": "08",
        "design_ref": "CFMP-Mobile-Design-Document.md §7 (Senior mode)",
        "personas": ["robert"],
        "code_globs": ["mobile/app/theme.css", "mobile/app/me/*"],
        "see_also": ["C7.5"],
        "gaps": ["Toggle in profile but accessibility audit incomplete; no voice-first navigation alternative yet"],
        "mobile_parity": "live"
    },
    {
        "id": "C2.7", "lane": "L2", "name": "Lot bundles (recurring buckets like 'household basics')",
        "status": "in_progress", "progress_pct": 70, "episode": "04",
        "design_ref": "CFMP-Mobile-Lots-Expert-Focus.md §5 (bundles)",
        "personas": ["sarah"],
        "code_globs": ["mobile/app/api/auto-orders/bundles/*"],
        "see_also": ["C2.2"],
        "gaps": ["Bundle definition UI exists, no analytics-driven bundle suggestion"],
        "mobile_parity": "partial"
    },
    {
        "id": "C2.8", "lane": "L2", "name": "Flux household-composition events (vacation/arrival/departure)",
        "status": "completed", "progress_pct": 95, "episode": "10",
        "design_ref": "CFMP-Mobile-Flux-Design.md §1-4",
        "personas": ["sarah", "marcus"],
        "code_globs": ["orchestrator/flux.py", "mobile/app/api/flux/*",
                        "db/04_flux_events.sql", "mobile/components/FluxBanner.tsx",
                        "mobile/components/FluxApprovalSheet.tsx"],
        "see_also": ["C9.5", "C11.8"], "gaps": [],
        "mobile_parity": "live"
    },
    {
        "id": "C2.9", "lane": "L2", "name": "HITL Flux lifecycle (detected -> proposed -> approved -> active)",
        "status": "completed", "progress_pct": 100, "episode": "10",
        "design_ref": "CFMP-Mobile-Flux-Design.md §5 (HITL lifecycle)",
        "personas": ["sarah", "marcus"],
        "code_globs": ["orchestrator/flux.py", "mobile/app/api/flux/[event_id]/*",
                        "mobile/app/api/flux/accept/*", "mobile/app/api/flux/dismiss/*",
                        "mobile/app/api/flux/snooze/*"],
        "see_also": ["C2.8"], "gaps": [],
        "mobile_parity": "live"
    },
    {
        "id": "C2.10", "lane": "L2", "name": "Concierge dispatcher (cross-channel coordination)",
        "status": "completed", "progress_pct": 90, "episode": "04",
        "design_ref": "CFMP-Mobile-Design-Document.md §5.2 (Concierge)",
        "personas": ["sarah", "robert"],
        "code_globs": ["orchestrator/concierge.py", "mobile/app/api/concierge/*",
                        "mobile/app/concierge/*", "portal/app/api/concierge/*",
                        "mobile/components/MobileChat.tsx"],
        "see_also": ["C6.6"], "gaps": [],
        "mobile_parity": "partial"
    },

    # ===== L3 -- In-Store Experience =====
    {
        "id": "C3.1", "lane": "L3", "name": "In-flight trip checklist (live lot view in store)",
        "status": "completed", "progress_pct": 100, "episode": "03",
        "design_ref": "CFMP-Mobile-Design-Document.md §4.1 (in-flight)",
        "personas": ["sarah"],
        "code_globs": ["mobile/app/trip/*", "mobile/app/api/trips/[trip_id]/*"],
        "see_also": ["C2.1"], "gaps": [],
        "mobile_parity": "live"
    },
    {
        "id": "C3.2", "lane": "L3", "name": "Walk-the-aisle store map navigation",
        "status": "in_progress", "progress_pct": 65, "episode": "04",
        "design_ref": "CFMP-Mobile-Design-Document.md §4.2 (storemap)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/storemap.py", "orchestrator/storemap.yaml",
                        "orchestrator/route_optimizer.py", "portal/app/api/wayfinding/*"],
        "see_also": ["C3.4", "C5.4"],
        "gaps": ["Single seeded store layout; no operator UI to upload retailer floorplans"],
        "mobile_parity": "missing"
    },
    {
        "id": "C3.3", "lane": "L3", "name": "Real-time coupon savings on scan",
        "status": "completed", "progress_pct": 100, "episode": "03",
        "design_ref": "CFMP-Mobile-Design-Document.md §3.1 (coupon match)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/coupons.py", "orchestrator/scan_history.py"],
        "see_also": ["C1.6"], "gaps": [],
        "mobile_parity": "live"
    },
    {
        "id": "C3.4", "lane": "L3", "name": "Store-map route optimizer (shortest path through lot)",
        "status": "in_progress", "progress_pct": 60, "episode": "04",
        "design_ref": "CFMP-Mobile-Design-Document.md §4.2.1 (route)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/route_optimizer.py", "orchestrator/storemap.py"],
        "see_also": ["C3.2"],
        "gaps": ["Optimizer treats store as flat grid; no aisle-priority weighting or crowding signal"],
        "mobile_parity": "missing"
    },
    {
        "id": "C3.5", "lane": "L3", "name": "Geofence arrival detection (auto-open in-flight trip)",
        "status": "in_progress", "progress_pct": 40, "episode": "04",
        "design_ref": "CFMP-Mobile-Use-Cases.md §4 (geofence)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/azure_maps.py", "orchestrator/device_context.py"],
        "see_also": ["C3.1"],
        "gaps": ["Azure Maps wrapper present but no client-side geofence subscription; relies on manual 'I am at store' tap"],
        "mobile_parity": "missing"
    },
    {
        "id": "C3.6", "lane": "L3", "name": "Self-checkout via QR (skip the lane)",
        "status": "not_started", "progress_pct": 0, "episode": "03",
        "design_ref": "CFMP-Mobile-Roadmap.md §3 (self-checkout)",
        "personas": ["sarah"],
        "code_globs": [],
        "see_also": ["C3.7"],
        "gaps": [],
        "mobile_parity": "missing"
    },
    {
        "id": "C3.7", "lane": "L3", "name": "Receipt -> pantry handoff (close lot, seed replenish)",
        "status": "in_progress", "progress_pct": 35, "episode": "03",
        "design_ref": "CFMP-Mobile-Design-Document.md §4.5 (receipt close)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/scan_history.py", "orchestrator/auto_orders.py"],
        "see_also": ["C1.9", "C2.2"],
        "gaps": ["Closed-trip outputs not yet wired into replenish cadence; refill model still uses scan-history not receipt-history"],
        "mobile_parity": "partial"
    },
    {
        "id": "C3.8", "lane": "L3", "name": "Manual barcode entry fallback (no camera permission)",
        "status": "completed", "progress_pct": 100, "episode": "03",
        "design_ref": "CFMP-Mobile-Design-Document.md §3.3 (fallback)",
        "personas": ["sarah", "robert"],
        "code_globs": ["mobile/components/ManualBarcodeEntry.tsx"],
        "see_also": ["C1.1"], "gaps": [],
        "mobile_parity": "partial"
    },
    {
        "id": "C3.9", "lane": "L3", "name": "Cart sheet (in-store basket overlay)",
        "status": "completed", "progress_pct": 100, "episode": "03",
        "design_ref": "CFMP-Mobile-Design-Document.md §4.6 (cart UX)",
        "personas": ["sarah"],
        "code_globs": ["mobile/components/CartSheet.tsx", "mobile/components/CartButton.tsx"],
        "see_also": ["C3.1"], "gaps": [],
        "mobile_parity": "partial"
    },

    # ===== L4 -- Fulfillment & Pickup =====
    {
        "id": "C4.1", "lane": "L4", "name": "FulfillmentProvider plug-in ABC (open/closed contract)",
        "status": "completed", "progress_pct": 100, "episode": "07",
        "design_ref": "CFMP-Fulfillment-Design-Document.md §3 (Provider ABC)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/providers/base.py", "orchestrator/providers/__init__.py"],
        "see_also": ["C4.2", "C4.3"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C4.2", "lane": "L4", "name": "ProviderQuote shape (price, ETA, in-stock pct, fee)",
        "status": "completed", "progress_pct": 100, "episode": "07",
        "design_ref": "CFMP-Fulfillment-Design-Document.md §4 (Quote)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/providers/base.py", "orchestrator/fulfillment.py"],
        "see_also": ["C4.1"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C4.3", "lane": "L4", "name": "Quote-aggregator fan-out (parallel multi-provider quotes)",
        "status": "completed", "progress_pct": 100, "episode": "07",
        "design_ref": "CFMP-Fulfillment-Design-Document.md §5 (Aggregator)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/fulfillment.py", "mobile/app/api/fulfillment/quotes/*",
                        "portal/app/api/fulfillment/*"],
        "see_also": ["C4.4"], "gaps": [],
        "mobile_parity": "live"
    },
    {
        "id": "C4.4", "lane": "L4", "name": "Recommendation score (cheapest x in-stock x ETA x split)",
        "status": "completed", "progress_pct": 95, "episode": "07",
        "design_ref": "CFMP-Fulfillment-Design-Document.md §6 (Scoring)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/fulfillment.py"],
        "see_also": ["C4.3", "C6.7"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C4.5", "lane": "L4", "name": "place_order (transactional commit to provider)",
        "status": "completed", "progress_pct": 100, "episode": "07",
        "design_ref": "CFMP-Fulfillment-Design-Document.md §7 (place_order)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/fulfillment.py", "mobile/app/api/fulfillment/place/*",
                        "mobile/app/api/fulfillment/orders/*"],
        "see_also": ["C4.6"], "gaps": [],
        "mobile_parity": "live"
    },
    {
        "id": "C4.6", "lane": "L4", "name": "Substitution flow (dietary-safe at search step)",
        "status": "completed", "progress_pct": 90, "episode": "07",
        "design_ref": "CFMP-Fulfillment-Design-Document.md §8 (Substitution)",
        "personas": ["sarah", "diana"],
        "code_globs": ["orchestrator/fulfillment.py", "orchestrator/providers/instacart_mock.py"],
        "see_also": ["C4.4"],
        "gaps": ["Dietary filter applied at search; runtime swap path lacks pharmacy contraindication check"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C4.7", "lane": "L4", "name": "BOPIS pickup providers (3 mocked, real-shaped)",
        "status": "completed", "progress_pct": 100, "episode": "07",
        "design_ref": "CFMP-Fulfillment-Design-Document.md §9 (BOPIS tier)",
        "personas": ["sarah", "robert"],
        "code_globs": ["orchestrator/providers/kroger_bopis_mock.py",
                        "orchestrator/providers/target_pickup_mock.py",
                        "orchestrator/providers/walmart_pickup_mock.py",
                        "orchestrator/providers/wholefoods_pickup_mock.py",
                        "orchestrator/providers/shipt_mock.py",
                        "orchestrator/providers/instacart_mock.py",
                        "mobile/app/pickup/*", "mobile/app/api/fulfillment/providers/*",
                        "mobile/app/orders/*"],
        "see_also": ["C4.1"], "gaps": [],
        "mobile_parity": "live"
    },
    {
        "id": "C4.8", "lane": "L4", "name": "Pharmacy gate (handles_pharmacy=true attribute)",
        "status": "in_progress", "progress_pct": 65, "episode": "07",
        "design_ref": "CFMP-Fulfillment-Design-Document.md §10 (Pharmacy gate)",
        "personas": ["robert", "diana"],
        "code_globs": ["orchestrator/providers/base.py", "orchestrator/fulfillment.py"],
        "see_also": ["C7.3"],
        "gaps": ["Attribute defined; no provider yet sets it true; no Rx age-gate HITL flow"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C4.9", "lane": "L4", "name": "Status webhooks (provider -> orchestrator order lifecycle)",
        "status": "gap", "progress_pct": 35, "episode": "07",
        "design_ref": "CFMP-Fulfillment-Design-Document.md §7.3 (Webhooks)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/fulfillment.py"],
        "see_also": ["C4.5"],
        "gaps": ["No webhook idempotency table; replay collapses to duplicate ledger rows; no signed-payload verification"],
        "mobile_parity": "missing"
    },
    {
        "id": "C4.10", "lane": "L4", "name": "Cancel & refund flow",
        "status": "gap", "progress_pct": 25, "episode": "07",
        "design_ref": "CFMP-Fulfillment-Design-Document.md §7.4 (Cancel)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/fulfillment.py"],
        "see_also": ["C4.5"],
        "gaps": ["Refund path mocked only on Instacart provider; no audit row reconciliation against original place_order"],
        "mobile_parity": "live"
    },
    {
        "id": "C4.11", "lane": "L4", "name": "Split order across providers (pickup + same-day + warehouse)",
        "status": "completed", "progress_pct": 90, "episode": "07",
        "design_ref": "CFMP-Fulfillment-Design-Document.md §6.4 (Split)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/fulfillment.py"],
        "see_also": ["C4.3", "C4.4"], "gaps": [],
        "mobile_parity": "n/a"
    },

    # ===== L5 -- Voice Channel / Sonos =====
    {
        "id": "C5.1", "lane": "L5", "name": "Cue Bus (queue, suppress, retry contract)",
        "status": "completed", "progress_pct": 100, "episode": "06",
        "design_ref": "CFMP-Sonos-Design-Document.md §3 (Cue Bus)",
        "personas": ["sarah", "robert"],
        "code_globs": ["orchestrator/sonos_cloud.py", "orchestrator/sonos_player.py",
                        "orchestrator/trip_audio.py"],
        "see_also": ["C5.2", "C5.7"], "gaps": [],
        "mobile_parity": "missing"
    },
    {
        "id": "C5.2", "lane": "L5", "name": "Sonos zones (kitchen / living room / bedroom targeting)",
        "status": "completed", "progress_pct": 100, "episode": "06",
        "design_ref": "CFMP-Sonos-Design-Document.md §4 (Zones)",
        "personas": ["sarah", "robert"],
        "code_globs": ["orchestrator/sonos_cloud.py", "portal/app/api/sonos/discover/*",
                        "portal/app/api/sonos/say/*"],
        "see_also": ["C5.1"], "gaps": [],
        "mobile_parity": "missing"
    },
    {
        "id": "C5.3", "lane": "L5", "name": "Cadence law (no more than N cues per 10 min, etc.)",
        "status": "completed", "progress_pct": 95, "episode": "06",
        "design_ref": "CFMP-Sonos-Design-Document.md §5 (Cadence)",
        "personas": ["sarah", "robert"],
        "code_globs": ["orchestrator/sonos_cloud.py", "orchestrator/trip_audio.py"],
        "see_also": ["C5.1"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C5.4", "lane": "L5", "name": "Ducking (lower media when speaking a cue)",
        "status": "in_progress", "progress_pct": 50, "episode": "06",
        "design_ref": "CFMP-Sonos-Design-Document.md §6 (Ducking)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/sonos_cloud.py", "portal/app/api/sonos/volume/*"],
        "see_also": ["C5.1"],
        "gaps": ["Volume ducks but resume-level race condition on multi-cue bursts"],
        "mobile_parity": "missing"
    },
    {
        "id": "C5.5", "lane": "L5", "name": "AirPlay-bridge fallback (works behind any venue Wi-Fi)",
        "status": "completed", "progress_pct": 90, "episode": "06",
        "design_ref": "CFMP-Sonos-Design-Document.md §7 (AirPlay fallback)",
        "personas": ["priya"],
        "code_globs": ["orchestrator/sonos_cloud.py", "orchestrator/speech.py"],
        "see_also": ["C7.8"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C5.6", "lane": "L5", "name": "Voice-in via phone mic (Azure Speech STT)",
        "status": "completed", "progress_pct": 100, "episode": "06",
        "design_ref": "CFMP-Sonos-Design-Document.md §8 (Voice-in)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/speech.py", "mobile/app/api/agent/tts/*",
                        "portal/app/api/upload-audio/*"],
        "see_also": ["C11.1"], "gaps": [],
        "mobile_parity": "partial"
    },
    {
        "id": "C5.7", "lane": "L5", "name": "Sonos OAuth (household-bound credential lifecycle)",
        "status": "completed", "progress_pct": 100, "episode": "06",
        "design_ref": "CFMP-Sonos-Design-Document.md §9 (OAuth)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/sonos_cloud.py"],
        "see_also": ["C5.1"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C5.8", "lane": "L5", "name": "Spoken-cue LedgerRow (original + redacted-as-delivered)",
        "status": "completed", "progress_pct": 100, "episode": "06",
        "design_ref": "CFMP-Sonos-Design-Document.md §5.4 (Audit)",
        "personas": ["sarah", "robert"],
        "code_globs": ["orchestrator/audit_ledger.py", "orchestrator/sonos_cloud.py"],
        "see_also": ["C7.6", "C7.4"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C5.9", "lane": "L5", "name": "SonosStatusBadge (portal traffic-light for delivery health)",
        "status": "completed", "progress_pct": 100, "episode": "05",
        "design_ref": "CFMP-Sonos-Design-Document.md §5 (Portal proxies)",
        "personas": ["priya"],
        "code_globs": ["portal/app/api/sonos/status/*", "portal/app/architecture/*"],
        "see_also": ["C8.1"], "gaps": [],
        "mobile_parity": "missing"
    },

    # ===== L6 -- Agent Orchestration & MCP =====
    {
        "id": "C6.1", "lane": "L6", "name": "gpt-5-mini parent orchestrator",
        "status": "completed", "progress_pct": 100, "episode": "02",
        "design_ref": "CFMP-Mobile-Design-Document.md §5.1 (Parent agent)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/agent.py", "orchestrator/agent_orchestrator.py",
                        "mobile/app/api/agent/ask-multi/*", "portal/app/api/agent/ask/*",
                        "portal/app/api/agent/ask-multi/*"],
        "see_also": ["C6.2", "C6.3", "C6.4", "C6.5", "C6.6"], "gaps": [],
        "mobile_parity": "partial"
    },
    {
        "id": "C6.2", "lane": "L6", "name": "Trips specialist (lot/trip reasoning)",
        "status": "completed", "progress_pct": 100, "episode": "02",
        "design_ref": "CFMP-Mobile-Design-Document.md §5.2 (Specialists)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/shopping_trips.py", "orchestrator/agent_orchestrator.py"],
        "see_also": ["C6.1"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C6.3", "lane": "L6", "name": "Replenish specialist (auto-order timing)",
        "status": "completed", "progress_pct": 100, "episode": "02",
        "design_ref": "CFMP-Mobile-Design-Document.md §5.2 (Specialists)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/auto_orders.py", "orchestrator/agent_orchestrator.py"],
        "see_also": ["C6.1", "C2.2"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C6.4", "lane": "L6", "name": "Coupons specialist (apply, stack, expire)",
        "status": "completed", "progress_pct": 100, "episode": "02",
        "design_ref": "CFMP-Mobile-Design-Document.md §5.2 (Specialists)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/coupons.py", "orchestrator/agent_orchestrator.py"],
        "see_also": ["C6.1"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C6.5", "lane": "L6", "name": "Pharmacy specialist (HIPAA-aware refill reasoning)",
        "status": "in_progress", "progress_pct": 70, "episode": "08",
        "design_ref": "CFMP-Mobile-All-Experts-Panel.md (Yamamoto)",
        "personas": ["robert", "diana"],
        "code_globs": ["orchestrator/agent_orchestrator.py", "orchestrator/customer_profile.py"],
        "see_also": ["C7.3", "C7.4"],
        "gaps": ["Specialist contracts exist; full HIPAA-presence enforcement still in concierge.py, not the specialist"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C6.6", "lane": "L6", "name": "Concierge specialist (cross-channel dispatch)",
        "status": "completed", "progress_pct": 95, "episode": "02",
        "design_ref": "CFMP-Mobile-All-Experts-Panel.md (Mendez)",
        "personas": ["sarah", "robert"],
        "code_globs": ["orchestrator/concierge.py", "mobile/app/api/concierge/*"],
        "see_also": ["C2.10"], "gaps": [],
        "mobile_parity": "partial"
    },
    {
        "id": "C6.7", "lane": "L6", "name": "MCP boundary (single attack surface, single mock surface)",
        "status": "completed", "progress_pct": 100, "episode": "02",
        "design_ref": "MCP-Phase-2-Migration.md §1-3",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/mcp_client.py", "orchestrator/apex_mcp/app.py",
                        "orchestrator/apex_mcp/_common.py"],
        "see_also": ["C6.8", "C11.4"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C6.8", "lane": "L6", "name": "FastMCP servers (cxml, fulfillment, ledger, merml, parsml, weather)",
        "status": "completed", "progress_pct": 100, "episode": "02",
        "design_ref": "MCP-Phase-2-Migration.md §4 (Server inventory)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/apex_mcp/cxml_server.py", "orchestrator/apex_mcp/fulfillment_server.py",
                        "orchestrator/apex_mcp/ledger_server.py", "orchestrator/apex_mcp/merml_server.py",
                        "orchestrator/apex_mcp/parsml_server.py", "orchestrator/apex_mcp/weather_server.py"],
        "see_also": ["C6.7"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C6.9", "lane": "L6", "name": "Tool calls (typed contracts, MCP-callable from any agent)",
        "status": "completed", "progress_pct": 100, "episode": "02",
        "design_ref": "CFMP-Mobile-Design-Document.md §5.3 (Tool contracts)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/mcp_client.py", "orchestrator/apex_mcp/*"],
        "see_also": ["C6.7"], "gaps": [],
        "mobile_parity": "n/a"
    },

    # ===== L7 -- Trust, Identity, Consent & HIPAA =====
    {
        "id": "C7.1", "lane": "L7", "name": "Four-identity chain (customer / household / device / agent)",
        "status": "completed", "progress_pct": 95, "episode": "08",
        "design_ref": "CFMP-Mobile-Identity-Onboarding.md §1-3",
        "personas": ["sarah", "robert", "diana"],
        "code_globs": ["orchestrator/customer_profile.py", "orchestrator/auth_mock.py",
                        "orchestrator/apex_integration.py"],
        "see_also": ["C7.2", "C7.10"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C7.2", "lane": "L7", "name": "Entra External ID integration (B2C identity for customers)",
        "status": "in_progress", "progress_pct": 60, "episode": "08",
        "design_ref": "CFMP-Mobile-Entra-Provisioning-Runbook.md",
        "personas": ["sarah", "robert"],
        "code_globs": ["orchestrator/auth_mock.py", "mobile/app/api/auth/*",
                        "mobile/app/api/auth/me/*", "mobile/components/PhoneOtpSheet.tsx"],
        "see_also": ["C7.1"],
        "gaps": ["Mock OTP wired end-to-end; Entra tenant provisioning runbook complete but live IdP swap not deployed"],
        "mobile_parity": "live"
    },
    {
        "id": "C7.3", "lane": "L7", "name": "Consent gradient (per-domain opt-in, per-cue suppression)",
        "status": "completed", "progress_pct": 90, "episode": "08",
        "design_ref": "CFMP-Mobile-Audit-Participation.md §2-3",
        "personas": ["sarah", "robert", "diana"],
        "code_globs": ["orchestrator/customer_profile.py", "mobile/app/api/profile/*"],
        "see_also": ["C7.9"], "gaps": [],
        "mobile_parity": "partial"
    },
    {
        "id": "C7.4", "lane": "L7", "name": "HIPAA presence-gating (drug-name redaction on second-person)",
        "status": "completed", "progress_pct": 90, "episode": "08",
        "design_ref": "CFMP-Mobile-Design-Document.md §7 (Presence)",
        "personas": ["robert", "diana"],
        "code_globs": ["orchestrator/concierge.py", "orchestrator/audit_ledger.py",
                        "orchestrator/sonos_cloud.py"],
        "see_also": ["C7.5", "C5.8"],
        "gaps": ["Vision-kit presence signal currently mocked; live HAL integration pending"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C7.5", "lane": "L7", "name": "Drug-name redaction (inflight cue rewrite)",
        "status": "completed", "progress_pct": 95, "episode": "08",
        "design_ref": "CFMP-Mobile-Design-Document.md §7.2 (Redaction)",
        "personas": ["robert"],
        "code_globs": ["orchestrator/concierge.py", "orchestrator/sonos_cloud.py"],
        "see_also": ["C7.4"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C7.6", "lane": "L7", "name": "Audit chain Bronze/Silver/Gold tiers",
        "status": "completed", "progress_pct": 100, "episode": "02",
        "design_ref": "CFMP-Mobile-Audit-Participation.md §4 (Bronze/Silver/Gold)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/audit_ledger.py", "orchestrator/bronze_landing.py",
                        "portal/app/bronze/*", "portal/app/api/bronze/*"],
        "see_also": ["C6.7"], "gaps": [],
        "mobile_parity": "missing"
    },
    {
        "id": "C7.7", "lane": "L7", "name": "trace_id propagation (one id end to end)",
        "status": "completed", "progress_pct": 100, "episode": "02",
        "design_ref": "CFMP-Mobile-Audit-Participation.md §5 (trace_id)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/audit_ledger.py", "orchestrator/agent_orchestrator.py",
                        "orchestrator/mcp_client.py"],
        "see_also": ["C7.6"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C7.8", "lane": "L7", "name": "AirPlay audit-tagging (cues delivered through fallback are flagged)",
        "status": "implemented_not_podcasted", "progress_pct": 100, "episode": None,
        "design_ref": "CFMP-Sonos-Design-Document.md §7.3 (Audit on fallback)",
        "personas": ["priya"],
        "code_globs": ["orchestrator/sonos_cloud.py", "orchestrator/audit_ledger.py"],
        "see_also": ["C5.5", "C5.8"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C7.9", "lane": "L7", "name": "Preference Center kill-switch (one tap to suspend all cues)",
        "status": "completed", "progress_pct": 90, "episode": "08",
        "design_ref": "CFMP-Mobile-Preferences-Expert-Focus.md §5 (kill-switch)",
        "personas": ["sarah", "robert"],
        "code_globs": ["mobile/app/profile/*", "mobile/app/api/profile/*",
                        "orchestrator/customer_profile.py"],
        "see_also": ["C7.3"], "gaps": [],
        "mobile_parity": "partial"
    },
    {
        "id": "C7.10", "lane": "L7", "name": "Caregiver delegation (Diana proxies Robert's profile)",
        "status": "in_progress", "progress_pct": 50, "episode": "08",
        "design_ref": "CFMP-Mobile-Identity-Onboarding.md §4 (Delegation)",
        "personas": ["diana", "robert"],
        "code_globs": ["orchestrator/customer_profile.py", "orchestrator/auth_mock.py"],
        "see_also": ["C1.5", "C7.1"],
        "gaps": ["Care-Lot read access works; write-on-behalf consent token + revocation flow not implemented"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C7.11", "lane": "L7", "name": "APEX integration (Independence-minded identity bridge)",
        "status": "implemented_not_podcasted", "progress_pct": 80, "episode": None,
        "design_ref": "CFMP-Mobile-Identity-Onboarding.md §6 (APEX bridge)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/apex_integration.py", "orchestrator/apex_docs.py",
                        "orchestrator/apex_vendor/*"],
        "see_also": ["C7.1"], "gaps": [],
        "mobile_parity": "missing"
    },

    # ===== L8 -- Operations, Portal & Multi-Tenant =====
    {
        "id": "C8.1", "lane": "L8", "name": "Portal /architecture page (the seller's hero artifact)",
        "status": "completed", "progress_pct": 100, "episode": "05",
        "design_ref": "CFMP-Mobile-Design-Document.md §5 (Portal touchpoints)",
        "personas": ["priya"],
        "code_globs": ["portal/app/architecture/*", "portal/app/page.tsx"],
        "see_also": ["C5.9"], "gaps": [],
        "mobile_parity": "missing"
    },
    {
        "id": "C8.2", "lane": "L8", "name": "Operator console (incidents queue, household drill-in)",
        "status": "in_progress", "progress_pct": 75, "episode": "05",
        "design_ref": "CFMP-Mobile-Design-Document.md §5.4 (Operator)",
        "personas": ["priya"],
        "code_globs": ["portal/app/api/events/*", "portal/app/api/trips/*",
                        "portal/app/api/status/*"],
        "see_also": ["C8.3"],
        "gaps": ["Incidents queue renders; bulk-acknowledge + assignment-to-operator missing"],
        "mobile_parity": "missing"
    },
    {
        "id": "C8.3", "lane": "L8", "name": "Chat panel (operator's system-of-action)",
        "status": "completed", "progress_pct": 95, "episode": "05",
        "design_ref": "CFMP-Mobile-Design-Document.md §5.5 (Chat panel)",
        "personas": ["priya"],
        "code_globs": ["portal/app/api/agent/ask/*", "portal/app/api/agent/ask-multi/*",
                        "portal/app/concierge/*", "portal/app/api/concierge/*"],
        "see_also": ["C8.2"], "gaps": [],
        "mobile_parity": "partial"
    },
    {
        "id": "C8.4", "lane": "L8", "name": "Vision-kit camera ops (snapshot, hi-res frame, OCR)",
        "status": "in_progress", "progress_pct": 70, "episode": "05",
        "design_ref": "CFMP-Mobile-Design-Document.md §5.6 (Vision-kit)",
        "personas": ["priya"],
        "code_globs": ["orchestrator/camera_snapshots.py", "orchestrator/image_ocr.py",
                        "portal/app/api/camera-snapshot/*", "portal/app/api/frame/*",
                        "portal/app/api/frame-hi/*", "portal/app/live-scans/*",
                        "mobile/app/api/camera-snapshot/*"],
        "see_also": ["C11.2"],
        "gaps": ["Frame uplift loop works; on-device audio HAL is broken, so audio events fall back to laptop mic"],
        "mobile_parity": "partial"
    },
    {
        "id": "C8.5", "lane": "L8", "name": "Retailer multi-tenant scaffolding (B2B integration partner pattern)",
        "status": "in_progress", "progress_pct": 30, "episode": "05",
        "design_ref": "CFMP-Mobile-Design-Document.md §5.7 (B2B multi-tenant)",
        "personas": ["priya"],
        "code_globs": ["orchestrator/data_360.py", "portal/app/api/apex/*"],
        "see_also": ["C7.11"],
        "gaps": ["Tenant-id propagation through audit chain incomplete; no per-tenant data residency boundary"],
        "mobile_parity": "missing"
    },
    {
        "id": "C8.6", "lane": "L8", "name": "Azure Container Apps deployment (single-region prod)",
        "status": "completed", "progress_pct": 100, "episode": "05",
        "design_ref": "CFMP-Mobile-GitHub-Actions-Runbook.md",
        "personas": ["priya"],
        "code_globs": ["orchestrator/Dockerfile", "orchestrator/entrypoint.sh",
                        "orchestrator/http_server.py", "orchestrator/main.py",
                        "scripts/deploy.ps1", "scripts/azure-setup.ps1"],
        "see_also": ["C8.9"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C8.7", "lane": "L8", "name": "Azure Speech (STT + TTS as managed services)",
        "status": "completed", "progress_pct": 100, "episode": "06",
        "design_ref": "CFMP-Sonos-Design-Document.md §8 (Speech)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/speech.py", "mobile/app/api/agent/tts/*"],
        "see_also": ["C5.6"], "gaps": [],
        "mobile_parity": "live"
    },
    {
        "id": "C8.8", "lane": "L8", "name": "Postgres state (Azure Database for PostgreSQL)",
        "status": "completed", "progress_pct": 100, "episode": "05",
        "design_ref": "CFMP-Mobile-Design-Document.md §8 (Persistence)",
        "personas": ["priya"],
        "code_globs": ["db/schema.sql", "db/02_lots.sql", "db/03_scan_history.sql",
                        "db/04_flux_events.sql", "db/init_and_seed.py", "db/catalog.py"],
        "see_also": [], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C8.9", "lane": "L8", "name": "Operations runbooks (azure-up, monitor, logs)",
        "status": "implemented_not_podcasted", "progress_pct": 100, "episode": None,
        "design_ref": "CFMP-Mobile-GitHub-Actions-Runbook.md §3",
        "personas": ["priya"],
        "code_globs": ["scripts/azure-setup.ps1", "scripts/azure-down.ps1",
                        "scripts/monitor.ps1", "scripts/logs.ps1", "scripts/status.ps1",
                        "scripts/invoke.ps1", "scripts/snpe-threshold.ps1", "scripts/twin.ps1",
                        "scripts/wifi-sync.ps1"],
        "see_also": ["C8.6"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C8.10", "lane": "L8", "name": "Kiosk surface (in-store demo / standalone touchscreen)",
        "status": "implemented_not_podcasted", "progress_pct": 70, "episode": None,
        "design_ref": "CFMP-Mobile-Roadmap.md §5 (Kiosk)",
        "personas": ["sarah", "priya"],
        "code_globs": ["portal/app/kiosk/*", "portal/app/library/*"],
        "see_also": ["C8.1"],
        "gaps": ["Kiosk renders; not yet hardened for unattended public use (no idle-reset, no PIN protection)"],
        "mobile_parity": "missing"
    },

    # ===== L9 -- Recipe Capture & Cultural Breadth =====
    {
        "id": "C9.1", "lane": "L9", "name": "YouTube -> recipe import pipeline",
        "status": "proposed", "progress_pct": 0, "episode": "11",
        "design_ref": "Episode 11 §2 (YouTube ingest)",
        "personas": ["sarah"],
        "code_globs": [],
        "see_also": ["C1.7"],
        "gaps": ["No code; copyright + provenance line still being argued"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C9.2", "lane": "L9", "name": "Friend-shared recipe import (deep-link from text/email)",
        "status": "proposed", "progress_pct": 0, "episode": "11",
        "design_ref": "Episode 11 §3 (Friend-shared)",
        "personas": ["sarah"],
        "code_globs": [],
        "see_also": ["C1.7"], "gaps": ["No code; no share-target intent registered on Mobile"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C9.3", "lane": "L9", "name": "Family heirloom recipe (OCR'd from handwritten card)",
        "status": "proposed", "progress_pct": 0, "episode": "11",
        "design_ref": "Episode 11 §3 (Heirloom OCR)",
        "personas": ["sarah", "diana"],
        "code_globs": ["orchestrator/image_ocr.py"],
        "see_also": ["C9.1"],
        "gaps": ["OCR pipeline exists for product labels; handwriting model + recipe-structure prompt not built"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C9.4", "lane": "L9", "name": "Restaurant-meal repeat (photograph -> recipe)",
        "status": "proposed", "progress_pct": 0, "episode": "11",
        "design_ref": "Episode 11 §4 (Restaurant repeat)",
        "personas": ["sarah"],
        "code_globs": [],
        "see_also": ["C9.1"], "gaps": ["Reverse-image -> recipe inference unimplemented"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C9.5", "lane": "L9", "name": "Holiday favorites coupled to Flux PURPOSE event",
        "status": "proposed", "progress_pct": 0, "episode": "11",
        "design_ref": "Episode 11 §5 (Flux PURPOSE coupling)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/flux.py", "orchestrator/meal_planner.py"],
        "see_also": ["C2.8"],
        "gaps": ["Flux PURPOSE schema field designed; recipe-library tagging by PURPOSE not implemented"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C9.6", "lane": "L9", "name": "Cuisine-breadth discovery (15 cultures by design)",
        "status": "proposed", "progress_pct": 0, "episode": "11",
        "design_ref": "Episode 11 §6 (15 cuisines)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/meal_planner.py"],
        "see_also": [],
        "gaps": ["No cuisine taxonomy seeded; no cross-cultural substitution table"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C9.7", "lane": "L9", "name": "Specialty-ingredient sourcing (gochujang at the right store)",
        "status": "proposed", "progress_pct": 0, "episode": "11",
        "design_ref": "Episode 11 §6.2 (Specialty sourcing)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/fulfillment.py"],
        "see_also": ["C4.7"],
        "gaps": ["Specialty-stockist provider class not in tier; depends on warehouse-club + ethnic-grocer plug-ins"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C9.8", "lane": "L9", "name": "Allergen-aware import gate (block recipes that violate household allergens)",
        "status": "proposed", "progress_pct": 0, "episode": "11",
        "design_ref": "Episode 11 §7 (Allergen gate)",
        "personas": ["sarah", "diana"],
        "code_globs": ["orchestrator/customer_profile.py"],
        "see_also": ["C4.6"],
        "gaps": ["Allergen profile read at search; import-time scanner not built"],
        "mobile_parity": "n/a"
    },

    # ===== L10 -- Pairings & Mixers =====
    {
        "id": "C10.1", "lane": "L10", "name": "Wine pairing for a meal-plan night",
        "status": "proposed", "progress_pct": 0, "episode": None,
        "design_ref": "(no design doc -- v2 backlog)",
        "personas": ["sarah"],
        "code_globs": [], "see_also": ["C10.8"], "gaps": ["No pairing knowledge base; no sommelier prompt"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C10.2", "lane": "L10", "name": "Beer pairing (style guidance per cuisine)",
        "status": "proposed", "progress_pct": 0, "episode": None,
        "design_ref": "(no design doc -- v2 backlog)",
        "personas": ["sarah"],
        "code_globs": [], "see_also": ["C10.1"], "gaps": ["No code"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C10.3", "lane": "L10", "name": "Cocktail composition (mixer + spirit + garnish)",
        "status": "proposed", "progress_pct": 0, "episode": None,
        "design_ref": "(no design doc -- v2 backlog)",
        "personas": ["sarah"],
        "code_globs": [], "see_also": ["C10.6"], "gaps": ["No code; depends on mixer-pantry awareness"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C10.4", "lane": "L10", "name": "Non-alcoholic pairing (mocktails, kombucha, sparkling water)",
        "status": "proposed", "progress_pct": 0, "episode": None,
        "design_ref": "(no design doc -- v2 backlog)",
        "personas": ["sarah", "robert"],
        "code_globs": [], "see_also": ["C10.3"], "gaps": ["No code"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C10.5", "lane": "L10", "name": "Holiday/occasion pairings (Thanksgiving, Diwali, Lunar New Year)",
        "status": "proposed", "progress_pct": 0, "episode": None,
        "design_ref": "(no design doc -- v2 backlog)",
        "personas": ["sarah"],
        "code_globs": [], "see_also": ["C9.5"], "gaps": ["No code; tied to Flux PURPOSE coupling and recipe library"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C10.6", "lane": "L10", "name": "Mixer-pantry awareness (what's in the bar cart already)",
        "status": "proposed", "progress_pct": 0, "episode": None,
        "design_ref": "(no design doc -- v2 backlog)",
        "personas": ["sarah"],
        "code_globs": [], "see_also": ["C2.2"], "gaps": ["No code; would extend auto_orders pantry model to bar inventory"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C10.7", "lane": "L10", "name": "Allergen/dietary-aware pairing (sulfite-free wine, gluten-free beer)",
        "status": "proposed", "progress_pct": 0, "episode": None,
        "design_ref": "(no design doc -- v2 backlog)",
        "personas": ["sarah", "diana"],
        "code_globs": [], "see_also": ["C4.6", "C9.8"], "gaps": ["No code; reuses dietary-safety pattern from Lane 4"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C10.8", "lane": "L10", "name": "Age-gate via handles_alcohol=true provider attribute (HITL)",
        "status": "proposed", "progress_pct": 0, "episode": None,
        "design_ref": "(no design doc -- v2 backlog, reuses Pharmacy gate pattern)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/providers/base.py"],
        "see_also": ["C4.8"],
        "gaps": ["Pattern exists for pharmacy; no alcohol attribute or ID-check HITL flow"],
        "mobile_parity": "n/a"
    },

    # ===== L11 -- Privacy-First Architecture / Home & Telco Edge =====
    {
        "id": "C11.1", "lane": "L11", "name": "Voice on-device (phone mic STT, not cloud-streamed audio)",
        "status": "completed", "progress_pct": 90, "episode": "12",
        "design_ref": "CFMP-Sonos-Design-Document.md §8 (Voice-in privacy)",
        "personas": ["sarah", "robert"],
        "code_globs": ["orchestrator/speech.py", "mobile/app/api/agent/tts/*"],
        "see_also": ["C5.6"],
        "gaps": ["STT call routes through Azure Speech today; on-device Whisper path designed not shipped"],
        "mobile_parity": "live"
    },
    {
        "id": "C11.2", "lane": "L11", "name": "Vision Kit local inference (frames processed at edge)",
        "status": "completed", "progress_pct": 80, "episode": "12",
        "design_ref": "BEELINK_SETUP.md §2 (Vision Kit)",
        "personas": ["sarah", "robert"],
        "code_globs": ["device_app/vam_reader.py", "device_app/frame_uploader.py",
                        "device_app/qmmf_client.py", "device_app/main.py",
                        "device_app/led_status.py", "device_app/watchdog.py",
                        "device_app/ota_model_update.py", "device_app/bootstrap.sh",
                        "device_app/Dockerfile", "BEELINK_SETUP.md"],
        "see_also": ["C8.4"],
        "gaps": ["Local inference works for object detection; selective uplink threshold tuning still manual"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C11.3", "lane": "L11", "name": "Sonos household-local (cloud sends directives, never captures)",
        "status": "completed", "progress_pct": 100, "episode": "12",
        "design_ref": "SONOS.md §2 (Architecture)",
        "personas": ["sarah", "robert"],
        "code_globs": ["orchestrator/sonos_cloud.py", "SONOS.md"],
        "see_also": ["C5.1", "C5.7"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C11.4", "lane": "L11", "name": "MCP boundary as privacy boundary (one auditable surface)",
        "status": "completed", "progress_pct": 100, "episode": "12",
        "design_ref": "MCP-Phase-2-Migration.md §3 (Boundary)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/mcp_client.py", "orchestrator/apex_mcp/app.py"],
        "see_also": ["C6.7"], "gaps": [],
        "mobile_parity": "n/a"
    },
    {
        "id": "C11.5", "lane": "L11", "name": "Customer-owned identity in Entra (not retailer-owned)",
        "status": "in_progress", "progress_pct": 60, "episode": "12",
        "design_ref": "CFMP-Mobile-Identity-Onboarding.md §2 (Customer-owned)",
        "personas": ["sarah", "robert"],
        "code_globs": ["orchestrator/customer_profile.py", "orchestrator/auth_mock.py"],
        "see_also": ["C7.1", "C7.2"],
        "gaps": ["Designed as customer-owned; mock IdP today, live Entra External ID tenant not yet flipped"],
        "mobile_parity": "live"
    },
    {
        "id": "C11.6", "lane": "L11", "name": "Selective uplink (frames upload only on detection threshold)",
        "status": "completed", "progress_pct": 85, "episode": "12",
        "design_ref": "BEELINK_SETUP.md §3 (Uplink policy)",
        "personas": ["sarah"],
        "code_globs": ["device_app/frame_uploader.py", "device_app/vam_reader.py"],
        "see_also": ["C11.2"],
        "gaps": ["Threshold is a fixed config; no learned per-household policy"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C11.7", "lane": "L11", "name": "Telco-edge orchestrator (v2 vision)",
        "status": "proposed", "progress_pct": 0, "episode": "12",
        "design_ref": "Episode 12 §4 (v2 telco-edge)",
        "personas": ["sarah"],
        "code_globs": [],
        "see_also": ["C11.2"],
        "gaps": ["v2 roadmap; cloud orchestrator runs in Azure today, telco-edge is the differentiation argument"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C11.8", "lane": "L11", "name": "On-device LedgerRow witness (v2 vision)",
        "status": "proposed", "progress_pct": 0, "episode": "12",
        "design_ref": "Episode 12 §5 (On-device witness)",
        "personas": ["sarah"],
        "code_globs": ["orchestrator/audit_ledger.py"],
        "see_also": ["C7.6"],
        "gaps": ["Today ledger is cloud-side; v2 adds a co-signed on-device witness row"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C11.9", "lane": "L11", "name": "Local-first fallback (works when cloud is down)",
        "status": "in_progress", "progress_pct": 40, "episode": "12",
        "design_ref": "Episode 12 §6 (Local-first fallback)",
        "personas": ["sarah", "robert"],
        "code_globs": ["orchestrator/sonos_cloud.py", "device_app/watchdog.py"],
        "see_also": ["C5.5"],
        "gaps": ["Sonos AirPlay-bridge fallback works; cached recipe + cached lot read-only mode not implemented"],
        "mobile_parity": "n/a"
    },
    {
        "id": "C11.10", "lane": "L11", "name": "Customer data export (anti-vendor-lock-in)",
        "status": "not_started", "progress_pct": 0, "episode": "12",
        "design_ref": "Episode 12 §7 (Data export)",
        "personas": ["sarah"],
        "code_globs": [],
        "see_also": ["C11.5"],
        "gaps": ["Schema designed; export endpoint not built; GDPR/CCPA portability surface missing"],
        "mobile_parity": "n/a"
    },
]

# --------------------------------------------------------------------------------------
# Scanner
# --------------------------------------------------------------------------------------
ROOTS = ["orchestrator", "mobile/app", "mobile/components", "portal/app", "device_app", "db", "scripts"]
EXTS = {".py", ".ts", ".tsx", ".sql", ".yaml", ".yml", ".md"}
SKIP_DIRS = {
    "node_modules", "__pycache__", ".next", ".git",
    ".venv", "venv", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "site-packages", "dist", "build", ".turbo", ".vercel",
}
TOP_LEVEL_DOCS = ["SONOS.md", "BEELINK_SETUP.md", "README.md"]


def _first_nonblank(s: str) -> str:
    for ln in s.splitlines():
        ln = ln.strip()
        if ln:
            return ln
    return ""


def extract_role(text: str) -> str:
    """Pull a one-line role from the file's docstring / header comment."""
    # Python module docstring
    m = re.search(r'^"""(.+?)"""', text, re.S | re.M)
    if m:
        line = _first_nonblank(m.group(1))
        if line:
            return line[:160]
    # JS/TS JSDoc-style header
    m = re.search(r'^/\*\*(.+?)\*/', text, re.S | re.M)
    if m:
        first = _first_nonblank(m.group(1)).lstrip("* ").rstrip()
        if first:
            return first[:160]
    # JS/TS single-line header `// foo`
    m = re.search(r'^//\s*(.+)$', text, re.M)
    if m:
        return m.group(1).strip()[:160]
    # SQL `-- foo`
    m = re.search(r'^--\s*(.+)$', text, re.M)
    if m:
        return m.group(1).strip()[:160]
    # Markdown first '#' heading
    m = re.search(r'^#+\s+(.+)$', text, re.M)
    if m:
        return m.group(1).strip()[:160]
    # YAML first '#' comment
    m = re.search(r'^#\s+(.+)$', text, re.M)
    if m:
        return m.group(1).strip()[:160]
    return ""


def scan_files():
    files = []
    seen = set()
    for root in ROOTS:
        base = IOT / root
        if not base.exists():
            continue
        for f in base.rglob("*"):
            if not f.is_file():
                continue
            if f.suffix.lower() not in EXTS:
                continue
            if any(p in SKIP_DIRS for p in f.parts):
                continue
            try:
                rel = str(f.relative_to(IOT)).replace("\\", "/")
            except Exception:
                continue
            if rel in seen:
                continue
            seen.add(rel)
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            lines = text.count("\n") + (1 if text else 0)
            try:
                last_mod = datetime.datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")
            except Exception:
                last_mod = ""
            files.append({
                "path": rel,
                "lines": lines,
                "role": extract_role(text),
                "last_mod": last_mod,
            })
    # top-level repo docs
    for name in TOP_LEVEL_DOCS:
        f = IOT / name
        if f.exists() and name not in seen:
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue
            try:
                last_mod = datetime.datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")
            except Exception:
                last_mod = ""
            files.append({
                "path": name,
                "lines": text.count("\n") + 1,
                "role": extract_role(text),
                "last_mod": last_mod,
            })
            seen.add(name)
    return files


def match_caps(file_path: str) -> list[str]:
    """Return all capability ids whose globs match this file."""
    matches = []
    for cap in CAPABILITIES:
        for pat in cap.get("code_globs", []):
            # accept exact match, fnmatch glob match, or directory-prefix match
            prefix = pat.rstrip("*").rstrip("/")
            if (
                file_path == pat
                or fnmatch.fnmatch(file_path, pat)
                or (prefix and (file_path == prefix or file_path.startswith(prefix + "/")))
            ):
                matches.append(cap["id"])
                break
    return matches


def main():
    all_files = scan_files()
    for cap in CAPABILITIES:
        cap["files"] = []
    unmapped = []
    for f in all_files:
        cap_ids = match_caps(f["path"])
        if cap_ids:
            for cap_id in cap_ids:
                for cap in CAPABILITIES:
                    if cap["id"] == cap_id:
                        cap["files"].append(f)
                        break
        else:
            unmapped.append(f)
    histo = {}
    for cap in CAPABILITIES:
        histo[cap["status"]] = histo.get(cap["status"], 0) + 1
    parity_histo = {}
    for cap in CAPABILITIES:
        v = cap.get("mobile_parity", "n/a")
        parity_histo[v] = parity_histo.get(v, 0) + 1
    out = {
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "iot_device_root": str(IOT),
        "lanes": LANES,
        "personas": PERSONAS,
        "openers": OPENERS,
        "capabilities": CAPABILITIES,
        "files_scanned": len(all_files),
        "files_mapped": len(all_files) - len(unmapped),
        "unmapped_count": len(unmapped),
        "unmapped_sample": sorted(unmapped, key=lambda x: x["path"])[:30],
        "status_histogram": histo,
        "mobile_parity_histogram": parity_histo,
    }
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
