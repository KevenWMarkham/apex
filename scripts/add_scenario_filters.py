"""Add Domain + Practice filter dropdowns to the scenario modal.

Splices:
1. Filter-bar HTML — adds two <select> dropdowns beside the existing text filter.
2. filterScenarioModal() JS — combines text query AND domain filter AND practice filter.
3. openScenarioModal() JS — populates the Domain dropdown from scenarios in this practice,
   and shows/hides the Practice dropdown based on whether opened for one practice or all.

Idempotent: detects marker comments and skips if already applied.
"""

from __future__ import annotations

import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HTML_PATH = Path("docs/reference/APEX-Stacked-Architecture-Narrated.html")
html = HTML_PATH.read_text(encoding="utf-8")

MARKER = "<!-- scenario-filters-v1 -->"
if MARKER in html:
    print("Filters already added — no-op.")
    sys.exit(0)

# ---- 1. Replace the filter-bar HTML ---------------------------------------

OLD_FILTER_BAR = (
    '<div class="scenario-modal-filter">\n'
    '        <svg class="smf-icon" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>\n'
    '        <input type="text" id="scenarioModalFilter" placeholder="Filter scenarios..." autocomplete="off" oninput="filterScenarioModal()"/>\n'
    '        <span class="smf-count" id="scenarioModalFilterCount"></span>\n'
    '      </div>'
)

NEW_FILTER_BAR = (
    MARKER + "\n"
    '      <div class="scenario-modal-filter">\n'
    '        <svg class="smf-icon" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>\n'
    '        <input type="text" id="scenarioModalFilter" placeholder="Filter by ID, title, service, or description..." autocomplete="off" oninput="filterScenarioModal()"/>\n'
    '        <select id="scenarioModalPracticeFilter" onchange="filterScenarioModal()" title="Filter by Practice" class="smf-select">\n'
    '          <option value="">All Practices</option>\n'
    '          <option value="RC">RC</option>\n'
    '          <option value="HLS">HLS</option>\n'
    '          <option value="ER">ER</option>\n'
    '          <option value="AXLE">AXLE</option>\n'
    '          <option value="TMT">TMT</option>\n'
    '          <option value="TH">TH</option>\n'
    '          <option value="ICE">ICE</option>\n'
    '        </select>\n'
    '        <select id="scenarioModalDomainFilter" onchange="filterScenarioModal()" title="Filter by Functional Domain" class="smf-select">\n'
    '          <option value="">All Domains</option>\n'
    '        </select>\n'
    '        <span class="smf-count" id="scenarioModalFilterCount"></span>\n'
    '      </div>'
)

if OLD_FILTER_BAR not in html:
    print("ERROR: filter-bar markup not found (file already modified?)")
    sys.exit(1)

html = html.replace(OLD_FILTER_BAR, NEW_FILTER_BAR)

# ---- 2. CSS for the new selects -------------------------------------------

CSS_BLOCK = (
    "/* scenario-filters-v1 */\n"
    ".scenario-modal-filter { flex-wrap: wrap; gap: 8px; }\n"
    ".smf-select {\n"
    "  font-family: 'IBM Plex Sans', system-ui, sans-serif;\n"
    "  font-size: 12.5px;\n"
    "  padding: 5px 10px;\n"
    "  border: 1px solid rgba(255, 255, 255, 0.15);\n"
    "  border-radius: 4px;\n"
    "  background: rgba(0, 0, 0, 0.25);\n"
    "  color: inherit;\n"
    "  cursor: pointer;\n"
    "  min-width: 110px;\n"
    "}\n"
    ".smf-select:hover { border-color: rgba(68, 184, 168, 0.5); }\n"
    ".smf-select:focus {\n"
    "  outline: none;\n"
    "  border-color: var(--teal, #44B8A8);\n"
    "  box-shadow: 0 0 0 2px rgba(68, 184, 168, 0.2);\n"
    "}\n"
    ".scenario-row.hidden { display: none !important; }\n"
)

close_style = html.find("</style>")
if close_style != -1:
    html = html[:close_style] + CSS_BLOCK + html[close_style:]

# ---- 3. Rewrite filterScenarioModal() + extend openScenarioModal() -------

OLD_FILTER_FN = (
    "function filterScenarioModal() {\n"
    "  const input = document.getElementById('scenarioModalFilter');\n"
    "  if (!input) return;\n"
    "  const q = input.value.trim().toLowerCase();\n"
    "  const rows = document.querySelectorAll('#scenarioModalBody .scenario-row');\n"
    "  let shown = 0;\n"
    "  rows.forEach(function(row) {\n"
    "    const haystack = row.getAttribute('data-search') || '';\n"
    "    const match = q === '' || haystack.indexOf(q) !== -1;\n"
    "    row.classList.toggle('hidden', !match);\n"
    "    if (match) shown++;\n"
    "  });\n"
    "  updateFilterCount(shown, rows.length);\n"
    "}"
)

NEW_FILTER_FN = (
    "function filterScenarioModal() {\n"
    "  const input = document.getElementById('scenarioModalFilter');\n"
    "  if (!input) return;\n"
    "  const q = input.value.trim().toLowerCase();\n"
    "  const domSel = document.getElementById('scenarioModalDomainFilter');\n"
    "  const pracSel = document.getElementById('scenarioModalPracticeFilter');\n"
    "  const domFilter = domSel ? domSel.value : '';\n"
    "  const pracFilter = pracSel ? pracSel.value : '';\n"
    "  const rows = document.querySelectorAll('#scenarioModalBody .scenario-row');\n"
    "  let shown = 0;\n"
    "  rows.forEach(function(row) {\n"
    "    const haystack = row.getAttribute('data-search') || '';\n"
    "    const rowDomain = row.getAttribute('data-domain') || '';\n"
    "    const rowPractice = row.getAttribute('data-practice') || '';\n"
    "    const qMatch = q === '' || haystack.indexOf(q) !== -1;\n"
    "    const dMatch = domFilter === '' || rowDomain === domFilter;\n"
    "    const pMatch = pracFilter === '' || rowPractice === pracFilter;\n"
    "    const match = qMatch && dMatch && pMatch;\n"
    "    row.classList.toggle('hidden', !match);\n"
    "    if (match) shown++;\n"
    "  });\n"
    "  updateFilterCount(shown, rows.length);\n"
    "}\n"
    "\n"
    "function populateDomainFilter(items) {\n"
    "  const sel = document.getElementById('scenarioModalDomainFilter');\n"
    "  if (!sel) return;\n"
    "  const DOMAIN_LABELS = {\n"
    "    'clinical-care': 'Clinical & Care',\n"
    "    'network-infrastructure': 'Network & Infrastructure',\n"
    "    'engineering-rd': 'Engineering & R&D',\n"
    "    'supply-chain': 'Supply Chain & Inventory',\n"
    "    'asset-maintenance': 'Asset, Maintenance & Reliability',\n"
    "    'quality-compliance': 'Quality, Compliance & Regulatory',\n"
    "    'risk-fraud-security': 'Risk, Fraud & Security',\n"
    "    'pricing-revenue': 'Pricing, Revenue & Margin',\n"
    "    'customer-experience': 'Customer Experience & Loyalty',\n"
    "    'marketing-growth': 'Marketing & Growth',\n"
    "    'operations-workforce': 'Operations & Workforce',\n"
    "    'channel-partner-dealer': 'Channel, Partner & Dealer',\n"
    "    'other': 'Other / Cross-cutting'\n"
    "  };\n"
    "  const counts = {};\n"
    "  items.forEach(function(it) { if (it.domain) counts[it.domain] = (counts[it.domain] || 0) + 1; });\n"
    "  // Preserve current selection\n"
    "  const currentVal = sel.value;\n"
    "  sel.innerHTML = '<option value=\"\">All Domains</option>';\n"
    "  Object.keys(counts).sort(function(a, b) {\n"
    "    return (DOMAIN_LABELS[a] || a).localeCompare(DOMAIN_LABELS[b] || b);\n"
    "  }).forEach(function(slug) {\n"
    "    const opt = document.createElement('option');\n"
    "    opt.value = slug;\n"
    "    opt.textContent = (DOMAIN_LABELS[slug] || slug) + ' (' + counts[slug] + ')';\n"
    "    sel.appendChild(opt);\n"
    "  });\n"
    "  if (currentVal && counts[currentVal]) sel.value = currentVal;\n"
    "}"
)

if OLD_FILTER_FN in html:
    html = html.replace(OLD_FILTER_FN, NEW_FILTER_FN)
    print("Rewrote filterScenarioModal() + added populateDomainFilter()")
else:
    print("WARN: filterScenarioModal function not matched exactly")

# ---- 4. Extend openScenarioModal() to populate the domain filter + set practice selector ----
# Find the scenario-row template replacement point where items are rendered.
# After items are rendered, call populateDomainFilter(items).

OLD_RENDER_CALL = (
    "  // Reset filter state\n"
    "  const filterInput = document.getElementById('scenarioModalFilter');\n"
    "  if (filterInput) filterInput.value = '';\n"
    "  updateFilterCount(items.length, items.length);"
)

NEW_RENDER_CALL = (
    "  // Reset filter state\n"
    "  const filterInput = document.getElementById('scenarioModalFilter');\n"
    "  if (filterInput) filterInput.value = '';\n"
    "  const domSel = document.getElementById('scenarioModalDomainFilter');\n"
    "  if (domSel) domSel.value = '';\n"
    "  const pracSel = document.getElementById('scenarioModalPracticeFilter');\n"
    "  if (pracSel) pracSel.value = practiceCode || '';\n"
    "  populateDomainFilter(items);\n"
    "  updateFilterCount(items.length, items.length);"
)

if OLD_RENDER_CALL in html:
    html = html.replace(OLD_RENDER_CALL, NEW_RENDER_CALL)
    print("Wired openScenarioModal to populate domain filter + set practice selector")
else:
    print("WARN: render-call block not matched exactly")

# ---- 5. Add data-practice to the scenario-row template (needed for practice filter) --
# The v1 enrichment adds data-domain; we need data-practice too.

OLD_ROW = '<div class=\\"scenario-row\\" role=\\"listitem\\" data-search=\\"\' + escapeHtml(searchData) + \'\\" data-domain=\\"\' + escapeHtml(item.domain || \'\') + \'\\">'
# Instead, do a literal textual swap that's easier to read
OLD_ROW_LITERAL = 'data-search="\' + escapeHtml(searchData) + \'" data-domain="\' + escapeHtml(item.domain || \'\') + \'"'
NEW_ROW_LITERAL = 'data-search="\' + escapeHtml(searchData) + \'" data-domain="\' + escapeHtml(item.domain || \'\') + \'" data-practice="\' + escapeHtml(practiceCode || \'\') + \'"'

if OLD_ROW_LITERAL in html and NEW_ROW_LITERAL not in html:
    html = html.replace(OLD_ROW_LITERAL, NEW_ROW_LITERAL)
    print("Added data-practice to scenario-row template")

HTML_PATH.write_text(html, encoding="utf-8")
print(f"\nFilter UI added to {HTML_PATH}")
