"""Wave 39 — C1.x audit refresh.

Re-states each L1 capability's status against the actual deployed codebase
(rev bb73ae6 as of 2026-05-26), independently of the prior optimistic
markings. Run AFTER any major C1.x wave to keep the data file honest.

Run from this directory:
    python _refresh_c1_audit.py

Then regen the HTML:
    python _build_capabilities_map.py
"""
from __future__ import annotations
import io, json, pathlib, sys

HERE = pathlib.Path(__file__).parent
DATA = HERE / "_capabilities_data.json"

# Audit-corrected facts. Each entry is what the actual code + deployed
# behavior on the iPhone confirms — NOT what we wish were true. See the
# session transcript for the reasoning behind each call.
AUDIT: dict[str, dict] = {
    "C1.1": {
        "status": "completed",
        "progress_pct": 100,
        "gaps": [],
        "mobile_parity": "live",
        "_note": "Wave 12 flipped / to PreviewPage (Scan-First Home). "
                 "Wave 19 added ZXing fallback for iOS. Wave 22 added "
                 "Identify-items + filmstrip. Wave 36 added Settings → "
                 "theme toggle. Current rev bb73ae6.",
    },
    "C1.2": {
        "status": "completed",
        "progress_pct": 100,
        "gaps": [],
        "mobile_parity": "live",
        "_note": "Wave 8 schema + module + 5 endpoints; Wave 11 LotsStrip; "
                 "Wave 27 added flux_event_id FK column.",
    },
    "C1.3": {
        "status": "completed",
        "progress_pct": 95,
        "gaps": [
            "Live state badges (packed_by → ready → picked_up) ship in "
            "lots.py state machine; mobile renders state chip but the "
            "per-second prep-time stream from picker hardware isn't wired",
        ],
        "mobile_parity": "live",
        "_note": "kind=trip/pickup/delivery + 8 lifecycle states + state "
                 "transition endpoint. Picker-side live-update integration "
                 "is a Sprint 6 deferred per CFMP-Fulfillment-Roadmap.",
    },
    "C1.4": {
        "status": "in_progress",
        "progress_pct": 70,
        "gaps": [
            "kind=stay schema fields (stay_start_date, stay_end_date, "
            "delivery_target_ref) exist; multi-leg delivery scheduling "
            "(staples 24h ahead + cold leg at check-in + mid-stay top-up) "
            "is design-only — needs cabin booking ingest + scheduler.",
        ],
        "mobile_parity": "partial",
        "_note": "Schema slice is real; the orchestration that produces 3 "
                 "scheduled deliveries from a single cabin booking URL is "
                 "Sprint 7 (T7.x StayLot work per orchestrator §7).",
    },
    "C1.5": {
        "status": "in_progress",
        "progress_pct": 70,
        "gaps": [
            "Prescription mask is enforced by scope taxonomy EXCLUSION "
            "(ALL_SCOPES doesn't list 'prescriptions') but the actual "
            "Pharmacy-tenancy isolation is a Sprint 5 cross-cutting "
            "task — until that lands, the exclusion is correct-but-vacuous "
            "(no pharmacy rows anywhere to leak)",
            "Real-invite flow (dependent must accept the caregiver) is "
            "still demo-mode self-service; production wire-up is a "
            "Sprint 5 dependency on the Pharmacy + Identity teams",
        ],
        "mobile_parity": "partial",
        "_note": "WAVE 42 shipped — orchestrator/caregiver_link.py + 6 "
                 "HTTP endpoints + 27 pytest cases; mobile /me/caregivers "
                 "page with seed-demo button; ActingAsBanner sticky at "
                 "top of every page; X-Acting-As header round-trips via "
                 "_resolve_actor authorization check. The grocery half of "
                 "episode 03's care-trip moment works end-to-end; the "
                 "prescription-mask half is taxonomy-enforced (defense in "
                 "depth) until the Pharmacy spec adds real refill rows.",
    },
    "C1.6": {
        "status": "in_progress",
        "progress_pct": 80,
        "gaps": [
            "Demo-mode scan-coupon flow works end-to-end (Wave 40 shipped "
            "the orchestrator branch + mobile CouponVariant); real Kroger "
            "Plus / Instacart coupon ingestion is Sprint 6 (T6.C.x)",
            "apply_coupon CTA currently calls onPrimaryAction stub — needs "
            "wiring to a real applied_coupons row + loyalty-card linkage "
            "when the active CartLot exists (Sprint 3 dependency)",
        ],
        "mobile_parity": "partial",
        "_note": "WAVE 40 shipped — type DEMO-COUPON-DIAPER-100 in the "
                 "manual-barcode-entry input to see the cold-open demo "
                 "(yellow shelf coupon → $1 saving in CouponVariant). "
                 "Real coupon ingestion still pending.",
    },
    "C1.7": {
        "status": "in_progress",
        "progress_pct": 90,
        "gaps": [
            "Recipe → CartLot composition via POST /api/lots/from-recipe "
            "is a Sprint 3 task (T3.A.2) — not yet built (single remaining "
            "gap on this capability now that the shopping-list UI bug is "
            "closed)",
        ],
        "mobile_parity": "partial",
        "_note": "WAVE 41 shipped — orchestrator embeds product_name in "
                 "every shopping_rows entry (was relying on a LEFT JOIN "
                 "that missed for uncatalogued SKUs); portal renders an "
                 "italic SKU + 'catalog lookup pending' for any legacy "
                 "row still missing the name field. Only T3.A.2 outstanding.",
    },
    "C1.8": {
        "status": "completed",
        "progress_pct": 100,
        "gaps": [],
        "mobile_parity": "live",
        "_note": "Wave 6 (T1.B.2) shipped POST /api/scan/identify-image + "
                 "image_ocr.py Azure CV wrapper. Demo-mode keyword fallback "
                 "for Cheerios/Coca-Cola/Coke works without provisioning.",
    },
    "C1.9": {
        "status": "in_progress",
        "progress_pct": 75,
        "gaps": [
            "Reconciliation reports matched / missing / extras correctly; "
            "'Close lot' action wired through to lots.set_state is a "
            "Sprint 3 task (T3.A.x) — Wave 44 ships the read-side report",
            "Real receipts vs canned demo — Azure CV Read API works "
            "end-to-end but no auto-tuning of heuristics from real-world "
            "receipt variants yet (header skip-list + price-regex are "
            "hand-curated)",
        ],
        "mobile_parity": "partial",
        "_note": "WAVE 44 shipped — orchestrator/receipt_ocr.py + 19 "
                 "pytest cases + /api/scan/identify-receipt endpoint + "
                 "mobile ReceiptScanSheet + 'Close a TripLot' section on "
                 "/lots. Two demo paths skip Azure CV: DEMO_RECEIPT_CART_3 "
                 "(clean match) + DEMO_RECEIPT_TRIP_SHRINKAGE (Pampers "
                 "missing). Closes most of the demo gap; full close-action "
                 "wiring deferred to Sprint 3 lots detail page.",
    },
    "C1.10": {
        "status": "in_progress",
        "progress_pct": 80,
        "gaps": [
            "Suggestion flow ships (Wave 43) — user STILL must tap 'Set "
            "auto-replenish' to confirm; production enroll wire-up to the "
            "stub onEnroll callback lands in Sprint 3 (T3.A.x)",
            "Persistent snooze for dismissed suggestions deferred to "
            "Sprint 5 per Reyes-G observation (need usage data on whether "
            "users want hours-vs-weeks snooze)",
        ],
        "mobile_parity": "live",
        "_note": "WAVE 43 shipped — orchestrator auto_orders."
                 "suggest_cadence_from_pantry_scans() walks scan_history "
                 "(dual-mode PG/in-memory), groups by canonical_id, takes "
                 "median inter-scan interval as suggested cadence; new "
                 "/api/auto-orders/cadence-suggestions per-actor endpoint; "
                 "mobile CadenceSuggestionsStrip on Home above LotsStrip. "
                 "13 new pytest cases. Demo path: scan same UPC 3 times "
                 "with days between → strip surfaces.",
    },
    "C1.11": {
        "status": "completed",
        "progress_pct": 100,
        "gaps": [],
        "mobile_parity": "live",
        "_note": "Wave 22 shipped Identify-items button + IdentifiedItemsStrip "
                 "(COCO-SSD via TensorFlow.js, on-device). Wave 17 was the "
                 "underlying AI integration.",
    },
    "C1.12": {
        "status": "in_progress",
        "progress_pct": 45,
        "gaps": [
            "Seeded recipes only (meal_planner.list_recipes returns the "
            "demo set)",
            "No URL ingest flow — user can't paste a Bon Appetit / "
            "Smitten Kitchen link and get a parsed recipe",
            "No friend-share / heirloom capture (text or photo of a "
            "handwritten card, OCR'd into structured ingredients)",
        ],
        "mobile_parity": "partial",
        "_note": "WAVE 46+ — L-size; needs URL fetch + recipe schema "
                 "parser (likely Anthropic-tool-call assisted).",
    },
}


def main() -> int:
    d = json.load(io.open(DATA, encoding="utf-8"))
    updated = 0
    for cap in d["capabilities"]:
        if cap["id"] in AUDIT:
            audit = AUDIT[cap["id"]]
            for k, v in audit.items():
                if k.startswith("_"):
                    continue
                cap[k] = v
            updated += 1
            print(f"  {cap['id']:6} -> {audit['status']:14} {audit['progress_pct']:3}%  "
                  f"gaps={len(audit['gaps'])}")
    d["generated_at"] = "2026-05-26T01:00:00"  # ISO; rough fence-post
    with io.open(DATA, "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)
    print(f"\nWrote {updated} caps to {DATA.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
