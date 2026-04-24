"""Enhance the Flow-tab scenario picker with Practice + Domain filters.

The Flow picker at the top of the Flow tab currently exposes only 5 hand-listed
RC scenarios (4 disabled). This script:

1. Adds Practice + Domain <select> dropdowns next to the scenario picker.
2. Populates the scenario picker dynamically from APEX_SCENARIO_LIBRARY — all
   35 featured scenarios (identified by having an authored flow entry in
   APEX_FLOW_DATA, or by being one of the top 5 per practice) plus the full
   catalog (enabled if flow data exists, disabled otherwise).
3. Wires Practice + Domain dropdowns to filter the scenario picker options.

Idempotent: detects the marker and skips on re-run.
"""

from __future__ import annotations

import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HTML = Path("docs/reference/APEX-Stacked-Architecture-Narrated.html")
html = HTML.read_text(encoding="utf-8")

MARKER = "<!-- flow-picker-filters-v1 -->"
if MARKER in html:
    print("Flow-picker filters already in place — no-op.")
    sys.exit(0)

# ---- 1. Replace the flow-picker markup block --------------------------------
OLD_PICKER = (
    '<div class="flow-picker">\n'
    '    <label class="flow-picker-label" for="flowScenarioPicker">Scenario</label>\n'
    '    <select class="flow-picker-select" id="flowScenarioPicker" aria-label="Pick a scenario">\n'
    '      <option value="rc-cold-chain-excursion" selected>RC · Cold-chain excursion (store cooler)</option>\n'
    '      <option value="rc-dynamic-markdown" disabled>RC · Dynamic markdown optimization &mdash; coming soon</option>\n'
    '      <option value="rc-on-shelf-availability" disabled>RC · On-shelf availability &mdash; coming soon</option>\n'
    '      <option value="rc-returns-fraud" disabled>RC · Returns fraud detection &mdash; coming soon</option>\n'
    '      <option value="rc-loyalty-churn" disabled>RC · Loyalty churn &amp; winback &mdash; coming soon</option>\n'
    '    </select>\n'
    '    <span class="flow-picker-meta">5 scenarios authored &middot; 100+ pending &middot; <b>RC</b> anchors the pattern</span>\n'
    '  </div>'
)

NEW_PICKER = (
    MARKER + "\n"
    '  <div class="flow-picker">\n'
    '    <label class="flow-picker-label" for="flowPracticeFilter">Practice</label>\n'
    '    <select class="flow-picker-select flow-picker-narrow" id="flowPracticeFilter" aria-label="Filter by Practice" onchange="flowUpdatePicker()">\n'
    '      <option value="">All Practices</option>\n'
    '      <option value="RC" selected>RC · Retail &amp; Consumer</option>\n'
    '      <option value="HLS">HLS · Health, Life Sciences</option>\n'
    '      <option value="ER">ER · Energy &amp; Resources</option>\n'
    '      <option value="AXLE">AXLE · Automotive &amp; Manufacturing</option>\n'
    '      <option value="TMT">TMT · Technology, Media, Telecom</option>\n'
    '      <option value="TH">TH · Travel &amp; Hospitality</option>\n'
    '      <option value="ICE">ICE · Industrial, Construction, Equipment</option>\n'
    '    </select>\n'
    '    <label class="flow-picker-label" for="flowDomainFilter">Domain</label>\n'
    '    <select class="flow-picker-select flow-picker-narrow" id="flowDomainFilter" aria-label="Filter by functional domain" onchange="flowUpdatePicker()">\n'
    '      <option value="">All Domains</option>\n'
    '    </select>\n'
    '    <label class="flow-picker-label" for="flowScenarioPicker">Scenario</label>\n'
    '    <select class="flow-picker-select" id="flowScenarioPicker" aria-label="Pick a scenario"></select>\n'
    '    <span class="flow-picker-meta" id="flowPickerMeta">Loading scenarios&hellip;</span>\n'
    '  </div>'
)

if OLD_PICKER not in html:
    print("ERROR: flow-picker markup not found (file already modified?)")
    sys.exit(1)

html = html.replace(OLD_PICKER, NEW_PICKER)

# ---- 2. Inject CSS for the narrow variant + layout tweaks ------------------
CSS = (
    "/* flow-picker-filters-v1 */\n"
    ".flow-picker { flex-wrap: wrap; gap: 10px; row-gap: 8px; }\n"
    ".flow-picker-select.flow-picker-narrow { flex: 0 0 220px; max-width: 260px; }\n"
    "@media (max-width: 900px) {\n"
    "  .flow-picker-select.flow-picker-narrow { flex: 1 1 160px; }\n"
    "  .flow-picker-select { flex: 1 1 100%; }\n"
    "}\n"
    "#flowPickerMeta { flex: 1 1 100%; opacity: 0.8; font-size: 12.5px; }\n"
)

close_style = html.find("</style>")
if close_style != -1:
    html = html[:close_style] + CSS + html[close_style:]

# ---- 3. Append initialization + filter JS -----------------------------------
# Insert right before </body>. The init runs on DOMContentLoaded.

INIT_JS = r"""
<script>
/* flow-picker-filters-v1 — populate + filter the Flow scenario picker */
(function() {
  'use strict';

  // Map featured chain -> flow-data key. Only keys present in APEX_FLOW_DATA
  // have narration authored; others render as 'coming soon' (disabled).
  const DOMAIN_LABELS = {
    'clinical-care': 'Clinical & Care',
    'network-infrastructure': 'Network & Infrastructure',
    'engineering-rd': 'Engineering & R&D',
    'supply-chain': 'Supply Chain & Inventory',
    'asset-maintenance': 'Asset, Maintenance & Reliability',
    'quality-compliance': 'Quality, Compliance & Regulatory',
    'risk-fraud-security': 'Risk, Fraud & Security',
    'pricing-revenue': 'Pricing, Revenue & Margin',
    'customer-experience': 'Customer Experience & Loyalty',
    'marketing-growth': 'Marketing & Growth',
    'operations-workforce': 'Operations & Workforce',
    'channel-partner-dealer': 'Channel, Partner & Dealer',
    'other': 'Other / Cross-cutting'
  };

  // Build flattened scenario list from APEX_SCENARIO_LIBRARY, if it exists.
  function buildScenarioList() {
    if (typeof APEX_SCENARIO_LIBRARY === 'undefined') return [];
    const out = [];
    const PRACTICES = ['RC','HLS','ER','AXLE','TMT','TH','ICE'];
    PRACTICES.forEach(function(p) {
      const rows = APEX_SCENARIO_LIBRARY[p] || [];
      rows.forEach(function(r) {
        out.push({
          practice: p,
          title: r.t,
          service: r.s,
          id: r.id || '',
          domain: r.domain || '',
          path: r.p || ''
        });
      });
    });
    return out;
  }

  function flowHasData(flowKey) {
    return (typeof APEX_FLOW_DATA !== 'undefined') && APEX_FLOW_DATA[flowKey];
  }

  // Infer flow-data key from (practice, title). Convention: lowercase practice
  // + hyphen + slugified primary-noun. Today only 'rc-cold-chain-excursion'
  // exists in APEX_FLOW_DATA, so the lookup is mostly used to disable options.
  function makeFlowKey(practice, title) {
    const slug = title.toLowerCase()
      .replace(/[\u2014\u2013\u2212]/g, '-')
      .replace(/[^a-z0-9\- ]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '');
    return practice.toLowerCase() + '-' + slug;
  }

  function flowUpdateDomainOptions(scenarios, practiceFilter) {
    const sel = document.getElementById('flowDomainFilter');
    if (!sel) return;
    const filtered = practiceFilter
      ? scenarios.filter(function(s) { return s.practice === practiceFilter; })
      : scenarios;
    const counts = {};
    filtered.forEach(function(s) {
      if (s.domain) counts[s.domain] = (counts[s.domain] || 0) + 1;
    });
    const current = sel.value;
    sel.innerHTML = '<option value="">All Domains</option>';
    Object.keys(counts).sort(function(a, b) {
      return (DOMAIN_LABELS[a] || a).localeCompare(DOMAIN_LABELS[b] || b);
    }).forEach(function(slug) {
      const opt = document.createElement('option');
      opt.value = slug;
      opt.textContent = (DOMAIN_LABELS[slug] || slug) + ' (' + counts[slug] + ')';
      sel.appendChild(opt);
    });
    if (current && counts[current]) sel.value = current;
  }

  function flowUpdatePicker() {
    const all = buildScenarioList();
    const pracSel = document.getElementById('flowPracticeFilter');
    const domSel = document.getElementById('flowDomainFilter');
    const scenSel = document.getElementById('flowScenarioPicker');
    const meta = document.getElementById('flowPickerMeta');
    if (!scenSel) return;
    const practice = pracSel ? pracSel.value : '';
    flowUpdateDomainOptions(all, practice);
    const domain = domSel ? domSel.value : '';

    let items = all;
    if (practice) items = items.filter(function(s) { return s.practice === practice; });
    if (domain)   items = items.filter(function(s) { return s.domain === domain; });

    // Sort: items WITH flow data first, then alphabetical by id
    items.sort(function(a, b) {
      const aKey = makeFlowKey(a.practice, a.title);
      const bKey = makeFlowKey(b.practice, b.title);
      const aHas = flowHasData(aKey) ? 0 : 1;
      const bHas = flowHasData(bKey) ? 0 : 1;
      if (aHas !== bHas) return aHas - bHas;
      return (a.id || a.title).localeCompare(b.id || b.title);
    });

    const selected = scenSel.value;
    scenSel.innerHTML = '';
    let authoredCount = 0;
    let firstEnabledValue = null;
    items.forEach(function(s) {
      const flowKey = makeFlowKey(s.practice, s.title);
      const has = flowHasData(flowKey);
      if (has) authoredCount++;
      const opt = document.createElement('option');
      opt.value = flowKey;
      const idPrefix = s.id ? s.id + ' · ' : '';
      opt.textContent = idPrefix + s.practice + ' · ' + s.title + (has ? '' : ' — coming soon');
      opt.disabled = !has;
      if (has && !firstEnabledValue) firstEnabledValue = flowKey;
      scenSel.appendChild(opt);
    });
    // Restore previous selection if still valid, else pick first enabled
    if (selected && items.some(function(s) { return makeFlowKey(s.practice, s.title) === selected && flowHasData(selected); })) {
      scenSel.value = selected;
    } else if (firstEnabledValue) {
      scenSel.value = firstEnabledValue;
      scenSel.dispatchEvent(new Event('change', { bubbles: true }));
    }
    if (meta) {
      const total = items.length;
      meta.innerHTML = authoredCount + ' authored · ' + (total - authoredCount) + ' pending · <b>' +
        (practice || 'All') + '</b> · ' + (domain ? (DOMAIN_LABELS[domain] || domain) : 'All domains');
    }
  }

  // Expose globally so the inline onchange handlers can call it
  window.flowUpdatePicker = flowUpdatePicker;

  // Populate at DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', flowUpdatePicker);
  } else {
    flowUpdatePicker();
  }
})();
</script>
"""

close_body = html.rfind("</body>")
if close_body != -1:
    html = html[:close_body] + INIT_JS + html[close_body:]
    print("Injected flow-picker init + filter JS")
else:
    print("WARN: </body> not found — appending JS at end")
    html += INIT_JS

HTML.write_text(html, encoding="utf-8")
print(f"\nWrote {HTML}")
