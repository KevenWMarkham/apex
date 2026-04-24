"""Add a right-side flyout panel that opens when a service chip is clicked.

When any .svc-chip in a chain card (or anywhere else) is clicked, a slide-in
panel appears on the right edge showing:
  - Service ID + display name
  - Description (authored per-service below; generic fallback)
  - Scenarios from this Practice that use this service (linked to folder)

Dismissible by close button, ESC key, or clicking the backdrop.

Idempotent: detects <!-- service-flyout-v1 --> marker and skips on re-run.
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
LIB = Path("docs/scenarios/_catalog/scenario-library.json")
html = HTML.read_text(encoding="utf-8")

MARKER = "<!-- service-flyout-v1 -->"
if MARKER in html:
    print("Service flyout already in place — no-op.")
    sys.exit(0)

# -------- 1. Build per-service metadata --------
library = json.load(open(LIB, encoding="utf-8"))

# Aggregate scenarios per service code
scenarios_by_service: dict[str, list[dict]] = defaultdict(list)
for p, rows in library.items():
    for r in rows:
        code = r.get("s", "").strip()
        if not code:
            continue
        scenarios_by_service[code].append({
            "t": r.get("t", ""),
            "b": r.get("b", ""),
            "k": r.get("k", ""),
            "p": r.get("p", ""),
            "id": r.get("id", ""),
            "practice": p,
        })

# Authored service descriptions + the Practice each belongs to
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
                   "desc": "Prior authorization automation, utilization management workflows, care-gap closure recommendations. Tokenizes PHI at Bronze→Silver. KPIs: auth cycle time, approval rate, appeal cycle."},
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

# -------- 2. Build FLYOUT_DATA JS constant --------
flyout_data: dict[str, dict] = {}
for code, meta in SERVICE_INFO.items():
    scens = scenarios_by_service.get(code, [])
    flyout_data[code] = {
        "code": code,
        "name": meta["name"],
        "practice": meta["practice"],
        "desc": meta["desc"],
        "scenarios": [
            {
                "title": s["t"],
                "blurb": s["b"],
                "kpi": s["k"],
                "id": s["id"],
                "path": s["p"],
            }
            for s in sorted(scens, key=lambda x: x["t"].lower())
        ],
    }

flyout_js = json.dumps(flyout_data, ensure_ascii=False, separators=(",", ":"))

# -------- 3. Flyout HTML + CSS + JS --------
FLYOUT_HTML = '''<!-- service-flyout-v1 -->
<div id="svcFlyoutBackdrop" class="svc-flyout-backdrop" onclick="closeServiceFlyout()"></div>
<aside id="svcFlyout" class="svc-flyout" role="dialog" aria-hidden="true" aria-labelledby="svcFlyoutTitle">
  <header class="svc-flyout-head">
    <div class="svc-flyout-eyebrow">
      <span id="svcFlyoutPractice">APEX Service</span>
      <code id="svcFlyoutCode" class="svc-flyout-code">—</code>
    </div>
    <h3 id="svcFlyoutTitle" class="svc-flyout-title">—</h3>
    <button class="svc-flyout-close" type="button" onclick="closeServiceFlyout()" aria-label="Close service details">&times;</button>
  </header>
  <div class="svc-flyout-body">
    <section class="svc-flyout-desc-wrap">
      <div class="svc-flyout-sec-label">What this service does</div>
      <p id="svcFlyoutDesc" class="svc-flyout-desc">—</p>
    </section>
    <section class="svc-flyout-scenarios-wrap">
      <div class="svc-flyout-sec-label">Scenarios using this service <span id="svcFlyoutCount" class="svc-flyout-count"></span></div>
      <div id="svcFlyoutScenarios" class="svc-flyout-scenarios"></div>
    </section>
  </div>
</aside>
'''

FLYOUT_CSS = (
    "/* service-flyout-v1 */\n"
    ".svc-flyout-backdrop {\n"
    "  position: fixed; inset: 0;\n"
    "  background: rgba(0, 0, 0, 0.5);\n"
    "  opacity: 0;\n"
    "  pointer-events: none;\n"
    "  transition: opacity 0.2s ease;\n"
    "  z-index: 9990;\n"
    "}\n"
    ".svc-flyout-backdrop.open {\n"
    "  opacity: 1;\n"
    "  pointer-events: auto;\n"
    "}\n"
    ".svc-flyout {\n"
    "  position: fixed;\n"
    "  top: 0; right: 0; bottom: 0;\n"
    "  width: min(460px, 92vw);\n"
    "  background: var(--bg-1, #0b0b0b);\n"
    "  border-left: 1px solid var(--line, #2a2a2a);\n"
    "  box-shadow: -12px 0 40px rgba(0,0,0,0.5);\n"
    "  transform: translateX(100%);\n"
    "  transition: transform 0.28s cubic-bezier(.4,.0,.2,1);\n"
    "  z-index: 9991;\n"
    "  display: flex;\n"
    "  flex-direction: column;\n"
    "  overflow: hidden;\n"
    "}\n"
    ".svc-flyout.open { transform: translateX(0); }\n"
    ".svc-flyout-head {\n"
    "  padding: 22px 24px 18px;\n"
    "  border-bottom: 1px solid var(--line, #2a2a2a);\n"
    "  position: relative;\n"
    "  flex-shrink: 0;\n"
    "}\n"
    ".svc-flyout-eyebrow {\n"
    "  display: flex; align-items: center; gap: 10px;\n"
    "  font-size: 10.5px;\n"
    "  letter-spacing: 0.14em;\n"
    "  text-transform: uppercase;\n"
    "  color: var(--ink-2, #b4b4b4);\n"
    "  margin-bottom: 8px;\n"
    "}\n"
    ".svc-flyout-code {\n"
    "  font-family: 'JetBrains Mono', monospace;\n"
    "  font-size: 10.5px;\n"
    "  font-weight: 700;\n"
    "  letter-spacing: 0.06em;\n"
    "  color: var(--sky, #6FB9E8);\n"
    "  background: color-mix(in srgb, var(--sky, #6FB9E8) 18%, transparent);\n"
    "  padding: 2px 8px;\n"
    "  border-radius: 3px;\n"
    "}\n"
    ".svc-flyout-title {\n"
    "  font-family: 'Fraunces', Georgia, serif;\n"
    "  font-size: 22px;\n"
    "  font-weight: 600;\n"
    "  margin: 0;\n"
    "  color: var(--ink-0, #fff);\n"
    "  line-height: 1.25;\n"
    "  padding-right: 42px;\n"
    "}\n"
    ".svc-flyout-close {\n"
    "  position: absolute; top: 18px; right: 20px;\n"
    "  background: transparent;\n"
    "  border: 1px solid color-mix(in srgb, var(--ink-3, #8a8a8a) 30%, transparent);\n"
    "  color: var(--ink-2, #b4b4b4);\n"
    "  width: 32px; height: 32px;\n"
    "  border-radius: 50%;\n"
    "  cursor: pointer;\n"
    "  font-size: 18px; line-height: 1;\n"
    "  transition: background 0.15s, color 0.15s;\n"
    "}\n"
    ".svc-flyout-close:hover {\n"
    "  background: color-mix(in srgb, var(--crimson, #D34848) 20%, transparent);\n"
    "  color: #fff;\n"
    "}\n"
    ".svc-flyout-body {\n"
    "  flex: 1 1 auto;\n"
    "  overflow-y: auto;\n"
    "  padding: 22px 24px 28px;\n"
    "}\n"
    ".svc-flyout-sec-label {\n"
    "  font-size: 10.5px;\n"
    "  letter-spacing: 0.14em;\n"
    "  text-transform: uppercase;\n"
    "  color: var(--gold, #E3B657);\n"
    "  margin-bottom: 10px;\n"
    "  display: flex; align-items: center; gap: 8px;\n"
    "}\n"
    ".svc-flyout-count {\n"
    "  font-family: 'JetBrains Mono', monospace;\n"
    "  font-size: 10px;\n"
    "  color: var(--ink-3, #8a8a8a);\n"
    "  letter-spacing: normal;\n"
    "  text-transform: none;\n"
    "}\n"
    ".svc-flyout-desc {\n"
    "  font-size: 14px;\n"
    "  line-height: 1.65;\n"
    "  color: var(--ink-1, #e6edf3);\n"
    "  margin: 0 0 24px;\n"
    "}\n"
    ".svc-flyout-scenarios { display: flex; flex-direction: column; gap: 10px; }\n"
    ".svc-flyout-scenario {\n"
    "  background: color-mix(in srgb, var(--bg-2, #131313) 60%, transparent);\n"
    "  border: 1px solid color-mix(in srgb, var(--line, #2a2a2a) 80%, transparent);\n"
    "  border-radius: 6px;\n"
    "  padding: 12px 14px;\n"
    "  text-decoration: none;\n"
    "  color: inherit;\n"
    "  display: block;\n"
    "  transition: border-color 0.15s, background 0.15s;\n"
    "}\n"
    ".svc-flyout-scenario:hover {\n"
    "  border-color: color-mix(in srgb, var(--sky, #6FB9E8) 60%, transparent);\n"
    "  background: color-mix(in srgb, var(--sky, #6FB9E8) 8%, var(--bg-2, #131313));\n"
    "}\n"
    ".svc-flyout-scenario .sfs-id {\n"
    "  font-family: 'JetBrains Mono', monospace;\n"
    "  font-size: 10px;\n"
    "  font-weight: 700;\n"
    "  letter-spacing: 0.06em;\n"
    "  color: var(--sky, #6FB9E8);\n"
    "  margin-right: 8px;\n"
    "}\n"
    ".svc-flyout-scenario .sfs-title {\n"
    "  font-size: 13.5px;\n"
    "  font-weight: 600;\n"
    "  color: var(--ink-0, #fff);\n"
    "  display: inline;\n"
    "}\n"
    ".svc-flyout-scenario .sfs-blurb {\n"
    "  font-size: 12.5px;\n"
    "  color: var(--ink-2, #b4b4b4);\n"
    "  margin-top: 6px;\n"
    "  line-height: 1.55;\n"
    "}\n"
    ".svc-flyout-scenario .sfs-kpi {\n"
    "  display: inline-block;\n"
    "  font-size: 10.5px;\n"
    "  font-weight: 600;\n"
    "  margin-top: 8px;\n"
    "  padding: 2px 8px;\n"
    "  border-radius: 10px;\n"
    "  background: color-mix(in srgb, var(--gold, #E3B657) 15%, transparent);\n"
    "  color: var(--gold, #E3B657);\n"
    "}\n"
    ".svc-chip { cursor: pointer; }\n"
    ".svc-chip:hover { filter: brightness(1.2); }\n"
)

FLYOUT_JS = rf"""
<script>
/* service-flyout-v1 */
(function() {{
  'use strict';
  const FLYOUT_DATA = {flyout_js};

  function escapeHtml(s) {{
    return String(s || '').replace(/[&<>"']/g, function(c) {{
      return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}}[c];
    }});
  }}

  function openServiceFlyout(code) {{
    const data = FLYOUT_DATA[code];
    if (!data) return;
    document.getElementById('svcFlyoutCode').textContent = data.code;
    document.getElementById('svcFlyoutPractice').textContent = data.practice + ' Service';
    document.getElementById('svcFlyoutTitle').textContent = data.name;
    document.getElementById('svcFlyoutDesc').textContent = data.desc;
    const count = document.getElementById('svcFlyoutCount');
    count.textContent = '(' + data.scenarios.length + ')';
    const list = document.getElementById('svcFlyoutScenarios');
    if (!data.scenarios.length) {{
      list.innerHTML = '<div class="svc-flyout-scenario"><em>No scenarios indexed for this service yet.</em></div>';
    }} else {{
      list.innerHTML = data.scenarios.map(function(s) {{
        const idPart = s.id ? '<span class="sfs-id">' + escapeHtml(s.id) + '</span>' : '';
        const kpiPart = s.kpi ? '<div><span class="sfs-kpi">' + escapeHtml(s.kpi) + '</span></div>' : '';
        const href = s.path || '#';
        return '<a class="svc-flyout-scenario" href="' + escapeHtml(href) + '" target="_blank" rel="noopener">' +
               idPart +
               '<span class="sfs-title">' + escapeHtml(s.title) + '</span>' +
               '<div class="sfs-blurb">' + escapeHtml(s.blurb) + '</div>' +
               kpiPart +
               '</a>';
      }}).join('');
    }}
    document.getElementById('svcFlyoutBackdrop').classList.add('open');
    document.getElementById('svcFlyout').classList.add('open');
    document.getElementById('svcFlyout').setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }}

  function closeServiceFlyout() {{
    document.getElementById('svcFlyoutBackdrop').classList.remove('open');
    document.getElementById('svcFlyout').classList.remove('open');
    document.getElementById('svcFlyout').setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }}

  window.openServiceFlyout = openServiceFlyout;
  window.closeServiceFlyout = closeServiceFlyout;

  // Wire up clicks on any .svc-chip
  document.addEventListener('click', function(e) {{
    const chip = e.target.closest('.svc-chip');
    if (!chip) return;
    // Extract code from inner .svc-code
    const codeEl = chip.querySelector('.svc-code');
    if (!codeEl) return;
    const code = codeEl.textContent.trim();
    openServiceFlyout(code);
  }});

  // ESC to close
  document.addEventListener('keydown', function(e) {{
    if (e.key === 'Escape') closeServiceFlyout();
  }});
}})();
</script>
"""

# -------- 4. Inject CSS + HTML + JS --------

# CSS at end of first <style>
close_style = html.find("</style>")
if close_style != -1:
    html = html[:close_style] + FLYOUT_CSS + html[close_style:]

# HTML + JS before </body>
close_body = html.rfind("</body>")
if close_body != -1:
    html = html[:close_body] + FLYOUT_HTML + FLYOUT_JS + html[close_body:]

HTML.write_text(html, encoding="utf-8")
print(f"Injected service flyout (CSS + HTML + JS)")
print(f"Indexed {len(flyout_data)} services with {sum(len(s['scenarios']) for s in flyout_data.values())} total scenario references")
