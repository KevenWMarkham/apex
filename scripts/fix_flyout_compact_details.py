"""Rebuild FLYOUT_DATA from the enriched APEX_SCENARIO_LIBRARY (inside the HTML)
so compact-scenario flyout cards show correct Domain + Scenario ID + folder link.
Also enriches the compact-scenario expansion with more fields.

Before: scenarios_by_service was built from the *source* JSON which didn't have
id/path/domain — expanded compact cards showed "DOMAIN —" (empty).

After: rebuilds FLYOUT_DATA by parsing APEX_SCENARIO_LIBRARY from the HTML (where
the enrichment actually landed). Every compact scenario now carries id, path,
domain, and KPI direction. Render adds a KPI direction arrow, Domain full-name
translation, and a "Related in this domain" counter.

Idempotent via /* flyout-compact-enrich-v1 */ marker on the render + CSS.
"""

from __future__ import annotations

import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HTML = Path("docs/reference/APEX-Stacked-Architecture-Narrated.html")
html = HTML.read_text(encoding="utf-8")

# -------- 1. Pull APEX_SCENARIO_LIBRARY out of the HTML (source of truth) ----

lib_m = re.search(r"const APEX_SCENARIO_LIBRARY\s*=\s*(\{.*?\});", html, re.DOTALL)
if not lib_m:
    print("ERROR: APEX_SCENARIO_LIBRARY not found")
    sys.exit(1)
library = json.loads(lib_m.group(1))

# -------- 2. Rebuild FLYOUT_DATA with complete enriched fields ---------------

# Service info from the earlier add_service_flyout.py (hard-coded catalog)
SERVICE_INFO: dict[str, dict[str, str]] = {
    "RC-E2E-03": {"name": "Assortment & Pricing", "practice": "RC",
                  "desc": "Agents that tune assortment depth, markdown cadence, and dynamic pricing. Reads SCML.SKU, MERML.Markdown, MERML.Elasticity. HITL on markdowns above threshold. Typical KPIs: GM%, markdown-to-clear ratio, aged-stock days on hand."},
    "RC-E2E-04": {"name": "Customer Lifecycle & Loyalty", "practice": "RC",
                  "desc": "Personalization, churn prediction, winback, loyalty program lifecycle, cross-channel attribution. Reads CXML.Customer, CXML.Order, MERML.Promotion. Heavy use of tokenized PII at Silver boundary. KPIs: retention rate, LTV, NPS, MROI."},
    "RC-E2E-05": {"name": "Store Operations", "practice": "RC",
                  "desc": "Labor scheduling, task routing, store-level KPI dashboards, shrink investigation. Reads SCML.Lot, CXML.Interaction, MERML.Markdown. Field-facing personas. KPIs: labor hours, shrink cost, OSA, basket size."},
    "RC-E2E-06": {"name": "Fulfillment & Delivery", "practice": "RC",
                  "desc": "BOPIS orchestration, backhaul load planning, last-mile routing, dock scheduling. Reads SCML.Shipment, SCML.Lot, SCML.Location. KPIs: on-time ship rate, BOPIS wait time, cost-per-delivery."},
    "RC-E2E-07": {"name": "Returns & Refund Integrity", "practice": "RC",
                  "desc": "Returns fraud detection, credit-card ring flagging, wardrobing patterns, BORIS abuse. Reads CXML.Customer, CXML.Order history, fraud signal graph. HITL on high-value refund denials. KPIs: fraud loss recovered, false-positive rate."},
    "RC-E2E-08": {"name": "Supplier & Vendor", "practice": "RC",
                  "desc": "Vendor performance, chargeback negotiation, on-time-in-full monitoring, supplier diversity tracking. Reads SCML.Supplier, SCML.Shipment. KPIs: OTIF, chargeback $, supplier scorecard."},
    "RC-E2E-09": {"name": "Product Tracking", "practice": "RC",
                  "desc": "Lot-level provenance, FSMA 204 compliance, recall orchestration, cold-chain excursion triage. Reads SCML.Lot, SCML.Shipment + IoT telemetry. Critical path for food-safety mandates. KPIs: excursion triage time, recall reach rate."},
    "HLS-E2E-02": {"name": "Clinical Decision Support", "practice": "HLS",
                   "desc": "Oncology care pathways, sepsis early warning, ADE prediction, readmission risk. Reads Patient, Observation, MedicationRequest (FHIR-aligned). HITL on every treatment-altering recommendation. KPIs: adherence rate, readmission rate, time-to-treatment."},
    "HLS-E2E-04": {"name": "Care Management & UM", "practice": "HLS",
                   "desc": "Prior authorization automation, utilization management workflows, care-gap closure recommendations. Tokenizes PHI at Bronze\u2192Silver. KPIs: auth cycle time, approval rate, appeal cycle."},
    "HLS-E2E-06": {"name": "Population Health", "practice": "HLS",
                   "desc": "HEDIS measure closure, quality reporting, value-based-care contract performance, social-determinants triage. KPIs: HEDIS score, VBC performance bonus, measure closure rate."},
    "HLS-LS-03": {"name": "Clinical Trial Operations", "practice": "HLS",
                  "desc": "Patient matching to trial criteria, enrollment acceleration, site-feasibility scoring, protocol-deviation detection. KPIs: enrollment rate, screen-fail rate, protocol adherence."},
    "ER-PU-04": {"name": "Distribution Reliability", "practice": "ER",
                 "desc": "Outage triage, restoration orchestration, smart-meter anomaly detection, vegetation-risk modeling. KPIs: SAIDI/SAIFI, MTTR, CMI, crew deployment efficiency."},
    "ER-OG-02": {"name": "Upstream Operations", "practice": "ER",
                 "desc": "Drilling analytics, reservoir production forecasting, completion performance, lease-operator routing. KPIs: production per well, NPT hours, cost per BOE."},
    "ER-OG-03": {"name": "Upstream Reliability", "practice": "ER",
                 "desc": "Predictive maintenance for wellheads, ESPs, artificial-lift, compressor monitoring, gas-lift optimization. KPIs: uptime, failure rate, unplanned downtime cost."},
    "ER-OG-05": {"name": "Refining Optimization", "practice": "ER",
                 "desc": "Yield optimization, crude-selection advisory, catalyst-performance prediction, energy-efficiency tuning. KPIs: yield %, energy per barrel, margin per barrel."},
    "ER-OG-07": {"name": "Midstream Integrity", "practice": "ER",
                 "desc": "Pipeline integrity monitoring, leak detection, hydrostatic-test scheduling, corrosion modeling. KPIs: MTTD leak, integrity violations, shutdown events."},
    "ER-MN-02": {"name": "Environmental & Compliance", "practice": "ER",
                 "desc": "Emissions monitoring, environmental incident reporting, permit-compliance tracking, carbon-credit verification. KPIs: violation count, fine $, disclosure accuracy."},
    "AXLE-Connected-Factory-01": {"name": "Connected Factory", "practice": "AXLE",
                                   "desc": "OEE analytics, stamping-press predictive maintenance, industrial-IoT alarm triage, energy monitoring. KPIs: OEE, unplanned downtime, energy per unit."},
    "AXLE-Ops-03": {"name": "Production Operations", "practice": "AXLE",
                    "desc": "Production scheduling, line-balancing, changeover-time reduction, takt-time management. KPIs: throughput, OTD, schedule adherence."},
    "AXLE-QMS-02": {"name": "Quality Management", "practice": "AXLE",
                    "desc": "Quality-escape detection, SPC automation, 8D-report drafting, CAPA effectiveness tracking, FMEA analysis. KPIs: FPY defects, RCA cycle time, warranty-claim rate."},
    "AXLE-Supply-04": {"name": "Supply Chain & Sourcing", "practice": "AXLE",
                       "desc": "Supply-disruption response, BOM rationalization, sourcing-decision support, inventory optimization. KPIs: on-time rate, expedite $, inventory turns."},
    "AXLE-Supply-07": {"name": "Supplier Risk", "practice": "AXLE",
                       "desc": "Supplier risk scoring, dual-sourcing decisioning, geopolitical risk monitoring, supplier diversity tracking. KPIs: risk score delta, disruption delays, second-source coverage."},
    "TMT-TEL-CC-03": {"name": "Contact Center Intelligence", "practice": "TMT",
                      "desc": "Intent classification, call summarization, next-best-action, agent assist, deflection. KPIs: AHT, FCR, CSAT."},
    "TMT-TEL-NET-02": {"name": "Network Operations", "practice": "TMT",
                       "desc": "Fault prediction, alarm correlation, capacity planning, cell-site energy optimization. KPIs: ticket volume, MTTR, network availability."},
    "TMT-MED-01": {"name": "Subscriber Lifecycle", "practice": "TMT",
                   "desc": "Content recommendation, churn prediction, family-plan optimization, account-sharing detection. KPIs: churn rate, engagement, ARPU."},
    "TMT-MED-03": {"name": "Ad Operations Integrity", "practice": "TMT",
                   "desc": "Ad-fraud detection, invalid-traffic filtering, brand-safety enforcement, creative-effectiveness scoring. KPIs: invalid-traffic %, fill rate, brand-safety pass rate."},
    "TMT-TEC-04": {"name": "Customer Success Intelligence", "practice": "TMT",
                   "desc": "Expansion-ARR scoring, churn prediction for SaaS, usage-pattern anomaly detection, renewal risk. KPIs: NRR, expansion ARR, churn $, CSAT."},
    "TH-AIR-02": {"name": "Irregular Ops", "practice": "TH",
                  "desc": "IROPS re-accommodation, disruption communication, top-tier recovery, weather-triggered rebooking. KPIs: top-tier recovery rate, NPS during IROPS, rebook speed."},
    "TH-AIR-04": {"name": "Baggage Operations", "practice": "TH",
                  "desc": "Proactive baggage resolution, carousel assignment, mishandled-bag prediction. KPIs: mishandled-bag rate, escalation rate, resolution cost."},
    "TH-AIR-06": {"name": "Crew Resource Planning", "practice": "TH",
                  "desc": "Crew scheduling optimization, crew-availability forecasting, fatigue-rule compliance, reserve-crew deployment. KPIs: cancellation cost, crew satisfaction, on-time performance."},
    "TH-HOT-03": {"name": "Revenue Management", "practice": "TH",
                  "desc": "Dynamic pricing, RevPAR optimization, overbooking strategy, length-of-stay optimization, rate-plan design. KPIs: RevPAR, ADR, occupancy."},
    "TH-HOT-05": {"name": "Guest Experience", "practice": "TH",
                  "desc": "Guest sentiment tracking, proactive service recovery, review-response automation, in-stay-issue resolution. KPIs: NPS, complaint rate, review-score delta."},
    "ICE-Aftermarket-01": {"name": "Field Service Dispatch", "practice": "ICE",
                           "desc": "Dispatch optimization, first-time-fix routing, parts-on-truck planning, technician skill matching. KPIs: first-time-fix rate, repeat-visit rate, labor cost per call."},
    "ICE-Aftermarket-03": {"name": "Warranty & Claims", "practice": "ICE",
                           "desc": "Warranty intake, fraud detection, claim-triage, parts-causation analytics. KPIs: fraud $ recovery, cycle time, approval rate."},
    "ICE-Aftermarket-05": {"name": "Parts & Inventory", "practice": "ICE",
                           "desc": "Predictive parts replenishment, stockout prevention, obsolescence management, dealer-inventory balancing. KPIs: stockout rate, capture rate, inventory turns."},
    "ICE-Connected-06": {"name": "Connected Equipment", "practice": "ICE",
                         "desc": "AEMP telemetry analytics, fault-code triage, utilization reporting, dealer forecasting, territory realignment. KPIs: utilization %, forecast accuracy, inventory delta."},
    "ICE-EaaS-04": {"name": "Equipment-as-a-Service", "practice": "ICE",
                    "desc": "EaaS uptime management, SLA tracking, renewal prediction, usage-based billing. KPIs: SLA %, renewal rate, penalty $."},
}

# Aggregate scenarios per service with full enriched fields
by_service: dict[str, list[dict]] = defaultdict(list)
for p, rows in library.items():
    for r in rows:
        code = r.get("s", "").strip()
        if not code:
            continue
        by_service[code].append({
            "title": r.get("t", ""),
            "blurb": r.get("b", ""),
            "kpi": r.get("k", ""),
            "kk": r.get("kk", ""),
            "id": r.get("id", ""),
            "path": r.get("p", ""),
            "domain": r.get("domain", ""),
            "practice": p,
        })

# Per-domain counts per practice — for the "X scenarios in this domain" field
domain_counts: dict[tuple[str, str], int] = defaultdict(int)
for p, rows in library.items():
    for r in rows:
        d = r.get("domain", "")
        if d:
            domain_counts[(p, d)] += 1

# Build final FLYOUT_DATA
flyout_data: dict[str, dict] = {}
for code, meta in SERVICE_INFO.items():
    scens = by_service.get(code, [])
    flyout_data[code] = {
        "code": code,
        "name": meta["name"],
        "practice": meta["practice"],
        "desc": meta["desc"],
        "scenarios": sorted(scens, key=lambda x: x["title"].lower()),
    }

# Also emit DOMAIN_COUNTS as a JS map { practice: { domain: count } }
nested_counts: dict[str, dict[str, int]] = {}
for (p, d), n in domain_counts.items():
    nested_counts.setdefault(p, {})[d] = n

flyout_js = json.dumps(flyout_data, ensure_ascii=False, separators=(",", ":"))
counts_js = json.dumps(nested_counts, ensure_ascii=False, separators=(",", ":"))

# -------- 3. Replace the FLYOUT_DATA declaration in the HTML -----------------

old_decl = re.search(
    r"(const FLYOUT_DATA\s*=\s*)(\{.*?\});",
    html,
    re.DOTALL,
)
if not old_decl:
    print("ERROR: FLYOUT_DATA declaration not found")
    sys.exit(1)

new_decl = f"const FLYOUT_DATA = {flyout_js};\n  const FLYOUT_DOMAIN_COUNTS = {counts_js};"
html = html[:old_decl.start()] + new_decl + html[old_decl.end():]
print("Rewrote FLYOUT_DATA with enriched scenario fields")
print(f"  Services: {len(flyout_data)}")
print(f"  Total scenarios across services: {sum(len(v['scenarios']) for v in flyout_data.values())}")

# -------- 4. Enrich the compact render branch --------------------------------

OLD_COMPACT = (
    "        } else {\n"
    "          // Compact scenario \u2014 lightweight 4-field grid + blurb\n"
    "          detailBody =\n"
    "            '<div class=\"sfs-detail-grid\">' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Domain</div><div class=\"sfs-field-value\">' + escapeHtml(domainLabel || '\u2014') + '</div></div>' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Service</div><div class=\"sfs-field-value\"><code>' + escapeHtml(data.code) + '</code> ' + escapeHtml(data.name) + '</div></div>' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Practice</div><div class=\"sfs-field-value\">' + escapeHtml(data.practice) + '</div></div>' +\n"
    "              (s.id ? '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Scenario ID</div><div class=\"sfs-field-value\"><code>' + escapeHtml(s.id) + '</code></div></div>' : '') +\n"
    "            '</div>' +\n"
    "            '<div class=\"sfs-field sfs-field-full\"><div class=\"sfs-field-label\">Description</div><div class=\"sfs-field-value\">' + escapeHtml(s.blurb) + '</div></div>';\n"
    "        }"
)

NEW_COMPACT = (
    "        } else {\n"
    "          // Compact scenario \u2014 enriched 8-field grid + description + context\n"
    "          /* flyout-compact-enrich-v1 */\n"
    "          const sceneDomain = s.domain || '';\n"
    "          const sceneDomainLabel = sceneDomain\n"
    "            ? sceneDomain.replace(/-/g, ' ').replace(/\\b\\w/g, function(c) { return c.toUpperCase(); })\n"
    "            : (domainLabel || '\u2014');\n"
    "          const kpiArrow = s.kk === 'up' ? '\u2191' : (s.kk === 'down' ? '\u2193' : '\u00B7');\n"
    "          const kpiDirectionClass = s.kk === 'up' ? 'sfs-kpi-up' : (s.kk === 'down' ? 'sfs-kpi-down' : '');\n"
    "          const domainCount = (window.FLYOUT_DOMAIN_COUNTS || {})[data.practice] && (window.FLYOUT_DOMAIN_COUNTS[data.practice][sceneDomain] || 0);\n"
    "          const siblingTxt = domainCount ? ('This is 1 of ' + domainCount + ' scenarios in ' + sceneDomainLabel + ' (' + data.practice + ').') : '';\n"
    "          detailBody =\n"
    "            '<div class=\"sfs-kpi-banner\">' +\n"
    "              '<span class=\"sfs-kpi-banner-label\">Headline KPI</span>' +\n"
    "              '<span class=\"sfs-kpi-banner-value ' + kpiDirectionClass + '\">' + kpiArrow + ' ' + escapeHtml(s.kpi || '\u2014') + '</span>' +\n"
    "            '</div>' +\n"
    "            '<div class=\"sfs-detail-grid\">' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Scenario ID</div><div class=\"sfs-field-value\">' + (s.id ? '<code>' + escapeHtml(s.id) + '</code>' : '\u2014') + '</div></div>' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Practice</div><div class=\"sfs-field-value\">' + escapeHtml(data.practice) + '</div></div>' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Domain</div><div class=\"sfs-field-value\">' + escapeHtml(sceneDomainLabel) + '</div></div>' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Service</div><div class=\"sfs-field-value\"><code>' + escapeHtml(data.code) + '</code> ' + escapeHtml(data.name) + '</div></div>' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">KPI Direction</div><div class=\"sfs-field-value\"><span class=\"' + kpiDirectionClass + '\">' + kpiArrow + ' ' + (s.kk === 'up' ? 'Upside metric' : (s.kk === 'down' ? 'Reduction metric' : 'Neutral')) + '</span></div></div>' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Status</div><div class=\"sfs-field-value\"><span class=\"sfs-badge-compact\">Compact catalog entry</span></div></div>' +\n"
    "            '</div>' +\n"
    "            '<div class=\"sfs-field sfs-field-full\"><div class=\"sfs-field-label\">Description</div><div class=\"sfs-field-value\">' + escapeHtml(s.blurb) + '</div></div>' +\n"
    "            (siblingTxt ? '<div class=\"sfs-sibling-note\">' + escapeHtml(siblingTxt) + ' Browse the rest through its folder or the library modal.</div>' : '') +\n"
    "            '<div class=\"sfs-promote\">' +\n"
    "              '<span class=\"sfs-promote-label\">Promote to featured</span>' +\n"
    "              '<span class=\"sfs-promote-body\">Author the full Scenario \u2192 Solution \u2192 Use Case \u2192 Service \u2192 Persona \u2192 KPI chain in this scenario\\'s README and it graduates into the Chain Views tab with the 35 featured scenarios.</span>' +\n"
    "            '</div>';\n"
    "        }"
)

if OLD_COMPACT in html:
    html = html.replace(OLD_COMPACT, NEW_COMPACT)
    print("Rewrote compact render branch with enriched fields")
else:
    print("ERROR: old compact branch not matched")
    sys.exit(1)

# -------- 5. CSS for the new elements ----------------------------------------

CSS = (
    "/* flyout-compact-enrich-v1 */\n"
    ".sfs-kpi-banner {\n"
    "  display: flex; align-items: center; gap: 12px;\n"
    "  padding: 10px 14px;\n"
    "  margin-bottom: 14px;\n"
    "  background: color-mix(in srgb, var(--gold, #E3B657) 12%, var(--bg-2, #131313));\n"
    "  border: 1px solid color-mix(in srgb, var(--gold, #E3B657) 40%, transparent);\n"
    "  border-radius: 6px;\n"
    "}\n"
    ".sfs-kpi-banner-label {\n"
    "  font-family: 'JetBrains Mono', 'Consolas', monospace;\n"
    "  font-size: 9.5px;\n"
    "  font-weight: 700;\n"
    "  letter-spacing: 0.14em;\n"
    "  text-transform: uppercase;\n"
    "  color: var(--gold, #E3B657);\n"
    "}\n"
    ".sfs-kpi-banner-value {\n"
    "  font-size: 15px;\n"
    "  font-weight: 700;\n"
    "  color: var(--ink-0, #fff);\n"
    "  flex: 1;\n"
    "}\n"
    ".sfs-kpi-up { color: var(--teal, #44B8A8) !important; }\n"
    ".sfs-kpi-down { color: var(--sky, #6FB9E8) !important; }\n"
    ".sfs-kpi-banner .sfs-kpi-up { color: var(--teal, #44B8A8); }\n"
    ".sfs-kpi-banner .sfs-kpi-down { color: var(--sky, #6FB9E8); }\n"
    ".sfs-sibling-note {\n"
    "  font-size: 11.5px;\n"
    "  color: var(--ink-2, #b4b4b4);\n"
    "  font-style: italic;\n"
    "  margin-top: 8px;\n"
    "  padding: 8px 10px;\n"
    "  background: color-mix(in srgb, var(--bg-2, #131313) 50%, transparent);\n"
    "  border-radius: 4px;\n"
    "  border-left: 2px solid color-mix(in srgb, var(--sky, #6FB9E8) 40%, transparent);\n"
    "}\n"
    ".sfs-promote {\n"
    "  display: flex; flex-direction: column; gap: 4px;\n"
    "  margin-top: 10px;\n"
    "  padding: 10px 12px;\n"
    "  background: color-mix(in srgb, var(--gold, #E3B657) 6%, transparent);\n"
    "  border: 1px dashed color-mix(in srgb, var(--gold, #E3B657) 40%, transparent);\n"
    "  border-radius: 6px;\n"
    "}\n"
    ".sfs-promote-label {\n"
    "  font-family: 'JetBrains Mono', monospace;\n"
    "  font-size: 9.5px;\n"
    "  font-weight: 700;\n"
    "  letter-spacing: 0.12em;\n"
    "  text-transform: uppercase;\n"
    "  color: var(--gold, #E3B657);\n"
    "}\n"
    ".sfs-promote-body {\n"
    "  font-size: 11.5px;\n"
    "  color: var(--ink-2, #b4b4b4);\n"
    "  line-height: 1.5;\n"
    "}\n"
    ".sfs-badge-compact {\n"
    "  display: inline-block;\n"
    "  font-size: 10.5px;\n"
    "  font-weight: 600;\n"
    "  padding: 2px 8px;\n"
    "  border-radius: 10px;\n"
    "  background: color-mix(in srgb, var(--ink-3, #8a8a8a) 20%, transparent);\n"
    "  color: var(--ink-2, #b4b4b4);\n"
    "}\n"
)

close_style = html.find("</style>")
if close_style != -1:
    html = html[:close_style] + CSS + html[close_style:]
    print("Injected enriched-compact CSS")

HTML.write_text(html, encoding="utf-8")
print(f"\nWrote {HTML}")
