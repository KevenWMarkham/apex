"""Replace the broken Flow-picker init with a correct v2.

Changes from v1:
1. Dropdown lists only the 35 FEATURED scenarios (not all 723 compact
   library entries), embedded as a JS constant derived from
   docs/scenarios/_catalog/featured-chains.json.
2. Explicit ID -> APEX_FLOW_DATA key mapping (today only RC-SUPCHN-01
   maps to rc-cold-chain-excursion; everything else is "coming soon").
3. Practice + Domain filters narrow that 35-scenario list; dropdown is
   grouped by Practice for navigation.
4. The flow diagram container is hidden until a scenario with real flow
   data is selected; "coming soon" placeholder shown for non-authored.
5. Removes the old snap-back change handler ("only one scenario authored
   today") that forced value back to rc-cold-chain-excursion.

Idempotent via the <!-- flow-picker-filters-v2 --> marker.
"""

from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HTML = Path("docs/reference/APEX-Stacked-Architecture-Narrated.html")
CHAINS = Path("docs/scenarios/_catalog/featured-chains.json")
CLASSIFICATION = Path("docs/scenarios/_catalog/domain-classification.json")

html = HTML.read_text(encoding="utf-8")
chains = json.load(open(CHAINS, encoding="utf-8"))
classification = json.load(open(CLASSIFICATION, encoding="utf-8"))

MARKER = "<!-- flow-picker-filters-v2 -->"
V1_MARKER = "<!-- flow-picker-filters-v1 -->"

if MARKER in html:
    print("Flow-picker v2 already in place — no-op.")
    sys.exit(0)

# -------- 1. Build the featured scenario list with IDs and flow-keys --------

# Look up each featured chain's domain via the classifier (match by practice+title)
cls_index: dict[tuple[str, str], str] = {}
for item in classification:
    cls_index[(item["practice"], item["title"].lower().strip())] = item["domain_slug"]

DOMAIN_CODES = {
    "clinical-care": "CLIN",
    "network-infrastructure": "NET",
    "engineering-rd": "ENG",
    "supply-chain": "SUPCHN",
    "asset-maintenance": "ASSET",
    "quality-compliance": "QUAL",
    "risk-fraud-security": "RISK",
    "pricing-revenue": "PRICE",
    "customer-experience": "CX",
    "marketing-growth": "MKTG",
    "operations-workforce": "OPS",
    "channel-partner-dealer": "CHAN",
    "other": "OTHER",
}

# Walk the scenario tree to resolve each featured title to its ID + folder path
SCEN_ROOT = Path("docs/scenarios")
title_to_idpath: dict[tuple[str, str], dict[str, str]] = {}
for prac in ["RC", "HLS", "ER", "AXLE", "TMT", "TH", "ICE"]:
    prac_dir = SCEN_ROOT / prac
    if not prac_dir.exists():
        continue
    for dom_dir in prac_dir.iterdir():
        if not dom_dir.is_dir() or dom_dir.name not in DOMAIN_CODES:
            continue
        for scen in dom_dir.iterdir():
            if not scen.is_dir():
                continue
            readme = scen / "README.md"
            if not readme.exists():
                continue
            first = readme.read_text(encoding="utf-8").split("\n", 1)[0].strip()
            title = first[2:].strip() if first.startswith("# ") else ""
            if not title:
                continue
            m = re.match(r"^[A-Z]+-[A-Z]+-(\d{2,3})-(.+)$", scen.name) or \
                re.match(r"^(\d{2,3})-(.+)$", scen.name)
            if not m:
                continue
            idx = int(m.group(1))
            code = DOMAIN_CODES[dom_dir.name]
            sid = f"{prac}-{code}-{idx:02d}"
            rel = f"../scenarios/{prac}/{dom_dir.name}/{scen.name}/"
            title_to_idpath[(prac, title.lower().strip())] = {
                "id": sid, "path": rel, "domain": dom_dir.name,
            }

# Build the featured list
featured_data: list[dict] = []
for c in chains:
    p = c["practice"]
    info = title_to_idpath.get((p, c["title"].lower().strip()))
    if info is None:
        # Fuzzy
        for (kp, kt), v in title_to_idpath.items():
            if kp == p and (kt in c["title"].lower() or c["title"].lower() in kt):
                info = v
                break
    if info is None:
        continue
    featured_data.append({
        "id": info["id"],
        "practice": p,
        "title": c["title"],
        "domain": info["domain"],
        "path": info["path"],
    })

print(f"Built featured list: {len(featured_data)} scenarios")

# Explicit ID -> APEX_FLOW_DATA key map (only one authored today)
ID_TO_FLOW_KEY = {
    "RC-SUPCHN-01": "rc-cold-chain-excursion",
}

# Embed data + mapping in JS
featured_js = json.dumps(featured_data, ensure_ascii=False, separators=(",", ":"))
id_map_js = json.dumps(ID_TO_FLOW_KEY, ensure_ascii=False, separators=(",", ":"))


# -------- 2. Remove the old v1 init JS block -------------------------------

v1_pattern = re.compile(
    r"<script>\s*/\* flow-picker-filters-v1 .*?</script>\s*",
    re.DOTALL,
)
m = v1_pattern.search(html)
if m:
    html = html[:m.start()] + html[m.end():]
    print("Removed v1 flow-picker init script")


# -------- 3. Remove the "only one scenario authored today" snap-back handler --

OLD_SNAPBACK = (
    "  // Scenario picker placeholder behavior \u2014 only one scenario authored today\n"
    "  const picker = document.getElementById('flowScenarioPicker');\n"
    "  if (picker) {\n"
    "    picker.addEventListener('change', function(e) {\n"
    "      const val = e.target.value;\n"
    "      if (val !== 'rc-cold-chain-excursion') {\n"
    "        // Restore selection\n"
    "        e.target.value = 'rc-cold-chain-excursion';\n"
    "      }\n"
    "    });\n"
    "  }"
)
# Try ASCII mdash variant too (just em-dash as 2014 and the regular dash variant)
OLD_SNAPBACK_ALT = OLD_SNAPBACK.replace("\u2014", "—")

for candidate in (OLD_SNAPBACK, OLD_SNAPBACK_ALT):
    if candidate in html:
        html = html.replace(candidate, "")
        print("Removed old snap-back change handler")
        break
else:
    # Fuzzy: try to match via regex
    snap_re = re.compile(
        r"\s*// Scenario picker placeholder behavior[^\n]*\n"
        r"\s*const picker = document\.getElementById\('flowScenarioPicker'\);[\s\S]*?\n\s*\}",
        re.MULTILINE,
    )
    html = snap_re.sub("", html, count=1)
    print("Removed old snap-back handler via regex")


# -------- 4. Inject v2 init JS + CSS for the empty-state + coming-soon note --

INIT_JS = rf"""
<script>
{MARKER}
(function() {{
  'use strict';
  const FEATURED = {featured_js};
  const ID_TO_FLOW_KEY = {id_map_js};
  const DOMAIN_LABELS = {{
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
  }};

  function flowHasData(id) {{
    const key = ID_TO_FLOW_KEY[id];
    return !!(key && typeof APEX_FLOW_DATA !== 'undefined' && APEX_FLOW_DATA[key]);
  }}

  function updateDomainOptions(practiceFilter) {{
    const sel = document.getElementById('flowDomainFilter');
    if (!sel) return;
    const filtered = practiceFilter
      ? FEATURED.filter(function(s) {{ return s.practice === practiceFilter; }})
      : FEATURED;
    const counts = {{}};
    filtered.forEach(function(s) {{
      if (s.domain) counts[s.domain] = (counts[s.domain] || 0) + 1;
    }});
    const current = sel.value;
    sel.innerHTML = '<option value="">All Domains</option>';
    Object.keys(counts).sort(function(a, b) {{
      return (DOMAIN_LABELS[a] || a).localeCompare(DOMAIN_LABELS[b] || b);
    }}).forEach(function(slug) {{
      const opt = document.createElement('option');
      opt.value = slug;
      opt.textContent = (DOMAIN_LABELS[slug] || slug) + ' (' + counts[slug] + ')';
      sel.appendChild(opt);
    }});
    if (current && counts[current]) sel.value = current;
  }}

  function setFlowVisibility(show, scenarioTitle) {{
    // Hide or show the flow diagram based on whether the selected scenario
    // has authored flow data. Also render a "coming soon" panel when hidden.
    const diagramContainers = document.querySelectorAll(
      '.tab-panel[data-tab-panel="flow"] .flow-waves, ' +
      '.tab-panel[data-tab-panel="flow"] .flow-legend, ' +
      '.tab-panel[data-tab-panel="flow"] .flow-scenario-summary'
    );
    diagramContainers.forEach(function(el) {{
      el.style.display = show ? '' : 'none';
    }});
    let placeholder = document.getElementById('flowPlaceholder');
    if (!show) {{
      if (!placeholder) {{
        placeholder = document.createElement('div');
        placeholder.id = 'flowPlaceholder';
        placeholder.className = 'flow-placeholder';
        const picker = document.querySelector('.tab-panel[data-tab-panel="flow"] .flow-picker');
        if (picker && picker.parentNode) picker.parentNode.insertBefore(placeholder, picker.nextSibling);
      }}
      placeholder.innerHTML =
        '<div class="flow-placeholder-inner">' +
          '<div class="flow-placeholder-icon">\u23F3</div>' +
          '<div class="flow-placeholder-title">Flow diagram coming soon</div>' +
          '<div class="flow-placeholder-body">The end-to-end flow for <b>' +
            (scenarioTitle || 'this scenario') + '</b> has not been authored yet. ' +
          'Only <b>RC-SUPCHN-01 Cold-chain excursion</b> has a published flow today.</div>' +
        '</div>';
      placeholder.style.display = '';
    }} else if (placeholder) {{
      placeholder.style.display = 'none';
    }}
  }}

  function flowUpdatePicker() {{
    const pracSel = document.getElementById('flowPracticeFilter');
    const domSel  = document.getElementById('flowDomainFilter');
    const scenSel = document.getElementById('flowScenarioPicker');
    const meta    = document.getElementById('flowPickerMeta');
    if (!scenSel) return;

    const practice = pracSel ? pracSel.value : '';
    updateDomainOptions(practice);
    const domain = domSel ? domSel.value : '';

    let items = FEATURED.slice();
    if (practice) items = items.filter(function(s) {{ return s.practice === practice; }});
    if (domain)   items = items.filter(function(s) {{ return s.domain === domain; }});

    // Sort: authored first, then by ID
    items.sort(function(a, b) {{
      const aHas = flowHasData(a.id) ? 0 : 1;
      const bHas = flowHasData(b.id) ? 0 : 1;
      if (aHas !== bHas) return aHas - bHas;
      return a.id.localeCompare(b.id);
    }});

    // Preserve current selection if still present
    const prevValue = scenSel.value;
    scenSel.innerHTML = '';
    let authoredCount = 0;
    let firstAuthoredId = null;

    // Group by practice with optgroup for navigation clarity
    const byPractice = {{}};
    items.forEach(function(s) {{
      (byPractice[s.practice] = byPractice[s.practice] || []).push(s);
    }});
    Object.keys(byPractice).forEach(function(p) {{
      const grp = document.createElement('optgroup');
      grp.label = p;
      byPractice[p].forEach(function(s) {{
        const has = flowHasData(s.id);
        if (has) authoredCount++;
        const opt = document.createElement('option');
        opt.value = s.id;
        opt.textContent = s.id + ' \u00B7 ' + s.title + (has ? '' : ' \u2014 coming soon');
        opt.disabled = !has;
        if (has && !firstAuthoredId) firstAuthoredId = s.id;
        grp.appendChild(opt);
      }});
      scenSel.appendChild(grp);
    }});

    // Decide initial selection
    let selectedId = null;
    const found = items.find(function(s) {{ return s.id === prevValue && flowHasData(s.id); }});
    if (found) {{
      selectedId = found.id;
    }} else if (firstAuthoredId) {{
      selectedId = firstAuthoredId;
    }}
    if (selectedId) scenSel.value = selectedId;

    // Update meta
    if (meta) {{
      const total = items.length;
      meta.innerHTML = authoredCount + ' authored \u00B7 ' + (total - authoredCount) + ' pending \u00B7 <b>' +
        (practice || 'All') + '</b> \u00B7 ' + (domain ? (DOMAIN_LABELS[domain] || domain) : 'All domains');
    }}

    // Toggle diagram vs placeholder
    const sel = items.find(function(s) {{ return s.id === scenSel.value; }});
    setFlowVisibility(selectedId !== null && flowHasData(selectedId), sel ? sel.title : '');
  }}

  function onScenarioChange() {{
    const scenSel = document.getElementById('flowScenarioPicker');
    if (!scenSel) return;
    const id = scenSel.value;
    const has = flowHasData(id);
    const sel = FEATURED.find(function(s) {{ return s.id === id; }});
    setFlowVisibility(has, sel ? sel.title : '');
  }}

  window.flowUpdatePicker = flowUpdatePicker;
  window.onFlowScenarioChange = onScenarioChange;

  function init() {{
    flowUpdatePicker();
    const scenSel = document.getElementById('flowScenarioPicker');
    if (scenSel) scenSel.addEventListener('change', onScenarioChange);
  }}

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', init);
  }} else {{
    init();
  }}
}})();
</script>
"""

# Inject before </body>
close_body = html.rfind("</body>")
if close_body != -1:
    html = html[:close_body] + INIT_JS + html[close_body:]
    print("Injected v2 init JS")

# CSS for the placeholder panel
CSS = (
    "/* flow-picker-filters-v2 */\n"
    ".flow-placeholder {\n"
    "  margin: 32px auto;\n"
    "  max-width: 720px;\n"
    "  padding: 40px 32px;\n"
    "  background: color-mix(in srgb, var(--bg-2) 60%, transparent);\n"
    "  border: 1px dashed color-mix(in srgb, var(--gold, #E3B657) 40%, transparent);\n"
    "  border-radius: 8px;\n"
    "  text-align: center;\n"
    "}\n"
    ".flow-placeholder-icon { font-size: 38px; margin-bottom: 10px; }\n"
    ".flow-placeholder-title { font-size: 18px; font-weight: 700; margin-bottom: 10px; color: var(--ink-1); }\n"
    ".flow-placeholder-body { font-size: 14px; color: var(--ink-2); line-height: 1.6; }\n"
)
close_style = html.find("</style>")
if close_style != -1:
    html = html[:close_style] + CSS + html[close_style:]

HTML.write_text(html, encoding="utf-8")
print(f"\nWrote {HTML}")
