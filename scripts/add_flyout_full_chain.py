"""Enrich the flyout pop-under with the full 6-row chain for featured scenarios.

For each of the 35 featured scenarios, inject its full chain content
(Scenario / Solution / Use Case / Service / Persona / KPI) into the HTML
as a JS constant (FEATURED_CHAINS_BY_ID). Rewrite the flyout pop-under
render so that when the user expands a featured scenario, they see all
six colored rows matching the Chain Views tab styling.

For compact scenarios without full chain data, keep the existing
lightweight 4-field render.

Idempotent via /* flyout-full-chain-v1 */ marker.
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

html = HTML.read_text(encoding="utf-8")
chains = json.load(open(CHAINS, encoding="utf-8"))

MARKER = "/* flyout-full-chain-v1 */"
if MARKER in html:
    print("Full-chain flyout already in place — no-op.")
    sys.exit(0)

# ---- 1. Map featured chains to their scenario IDs via the filesystem --------

PRACTICES = ["RC", "HLS", "ER", "AXLE", "TMT", "TH", "ICE"]
DOMAIN_CODES = {
    "clinical-care": "CLIN", "network-infrastructure": "NET", "engineering-rd": "ENG",
    "supply-chain": "SUPCHN", "asset-maintenance": "ASSET", "quality-compliance": "QUAL",
    "risk-fraud-security": "RISK", "pricing-revenue": "PRICE", "customer-experience": "CX",
    "marketing-growth": "MKTG", "operations-workforce": "OPS", "channel-partner-dealer": "CHAN",
    "other": "OTHER",
}

SCEN_ROOT = Path("docs/scenarios")
title_to_id: dict[tuple[str, str], str] = {}
for p in PRACTICES:
    pdir = SCEN_ROOT / p
    if not pdir.exists():
        continue
    for dom in pdir.iterdir():
        if not dom.is_dir() or dom.name not in DOMAIN_CODES:
            continue
        code = DOMAIN_CODES[dom.name]
        for scen in dom.iterdir():
            if not scen.is_dir():
                continue
            readme = scen / "README.md"
            if not readme.exists():
                continue
            first = readme.read_text(encoding="utf-8").split("\n", 1)[0].strip()
            if not first.startswith("# "):
                continue
            title = first[2:].strip()
            m = re.match(r"^[A-Z]+-[A-Z]+-(\d{2,3})-", scen.name)
            if not m:
                continue
            idx = int(m.group(1))
            sid = f"{p}-{code}-{idx:02d}"
            title_to_id[(p, title.lower().strip())] = sid

# Build FEATURED_CHAINS_BY_ID
chains_by_id: dict[str, dict[str, str]] = {}
for c in chains:
    sid = title_to_id.get((c["practice"], c["title"].lower().strip()))
    if not sid:
        # fuzzy
        for (kp, kt), v in title_to_id.items():
            if kp == c["practice"] and (kt in c["title"].lower() or c["title"].lower() in kt):
                sid = v
                break
    if not sid:
        continue
    chains_by_id[sid] = {
        "title": c["title"],
        "scenario": c.get("Scenario", ""),
        "solution": c.get("Solution", ""),
        "use_case": c.get("Use Case", ""),
        "service_text": c.get("Service", ""),
        "persona": c.get("Persona", ""),
        "kpi": c.get("KPI", ""),
    }

print(f"Mapped {len(chains_by_id)} featured chains to scenario IDs")

chains_js = json.dumps(chains_by_id, ensure_ascii=False, separators=(",", ":"))

# ---- 2. Inject FEATURED_CHAINS_BY_ID as a JS constant -----------------------

CONST_BLOCK = f"""
<script>
/* flyout-full-chain-v1 — full chain content for the 35 featured scenarios */
window.FEATURED_CHAINS_BY_ID = {chains_js};
</script>
"""

# Place right after the flyout script's closing </script> — near the end of body
# We'll inject before the final </body>
close_body = html.rfind("</body>")
if close_body != -1:
    html = html[:close_body] + CONST_BLOCK + html[close_body:]
    print("Injected FEATURED_CHAINS_BY_ID constant")

# ---- 3. Rewrite the render template to use full chain when available --------

OLD_RENDER = (
    "      list.innerHTML = data.scenarios.map(function(s) {\n"
    "        const idPart = s.id ? '<span class=\"sfs-id\">' + escapeHtml(s.id) + '</span>' : '';\n"
    "        const kpiPart = s.kpi ? '<span class=\"sfs-kpi\">' + escapeHtml(s.kpi) + '</span>' : '';\n"
    "        const href = s.path || '#';\n"
    "        // Derive domain from path: path = ../scenarios/<PRACTICE>/<domain>/<ID-slug>/\n"
    "        let domain = '';\n"
    "        if (s.path) {\n"
    "          const parts = s.path.split('/');\n"
    "          if (parts.length >= 5) domain = parts[3] || '';\n"
    "        }\n"
    "        const domainLabel = domain\n"
    "          ? domain.replace(/-/g, ' ').replace(/\\b\\w/g, function(c) { return c.toUpperCase(); })\n"
    "          : '';\n"
    "        const domainPart = domain ? '<span class=\"sfs-domain\">' + escapeHtml(domainLabel) + '</span>' : '';\n"
    "        return (\n"
    "          '<div class=\"svc-flyout-scenario\" data-scenario-id=\"' + escapeHtml(s.id || '') + '\">' +\n"
    "            '<div class=\"sfs-head\">' +\n"
    "              '<div class=\"sfs-head-main\">' +\n"
    "                idPart +\n"
    "                '<span class=\"sfs-title\">' + escapeHtml(s.title) + '</span>' +\n"
    "              '</div>' +\n"
    "              '<div class=\"sfs-head-meta\">' + kpiPart + '</div>' +\n"
    "              '<svg class=\"sfs-chevron\" viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><polyline points=\"9 18 15 12 9 6\"></polyline></svg>' +\n"
    "            '</div>' +\n"
    "            '<div class=\"sfs-detail\">' +\n"
    "              '<div class=\"sfs-detail-grid\">' +\n"
    "                '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Domain</div><div class=\"sfs-field-value\">' + escapeHtml(domainLabel || '\u2014') + '</div></div>' +\n"
    "                '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Service</div><div class=\"sfs-field-value\"><code>' + escapeHtml(data.code) + '</code> ' + escapeHtml(data.name) + '</div></div>' +\n"
    "                '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Practice</div><div class=\"sfs-field-value\">' + escapeHtml(data.practice) + '</div></div>' +\n"
    "                (s.id ? '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Scenario ID</div><div class=\"sfs-field-value\"><code>' + escapeHtml(s.id) + '</code></div></div>' : '') +\n"
    "              '</div>' +\n"
    "              '<div class=\"sfs-field sfs-field-full\"><div class=\"sfs-field-label\">Description</div><div class=\"sfs-field-value\">' + escapeHtml(s.blurb) + '</div></div>' +\n"
    "              '<div class=\"sfs-actions\">' +\n"
    "                (href !== '#' ? '<a class=\"sfs-action sfs-action-primary\" href=\"' + escapeHtml(href) + '\" target=\"_blank\" rel=\"noopener\">' +\n"
    "                  '<svg viewBox=\"0 0 24 24\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6\"></path><polyline points=\"15 3 21 3 21 9\"></polyline><line x1=\"10\" y1=\"14\" x2=\"21\" y2=\"3\"></line></svg>' +\n"
    "                  'Open folder on disk' +\n"
    "                '</a>' : '') +\n"
    "              '</div>' +\n"
    "            '</div>' +\n"
    "          '</div>'\n"
    "        );\n"
    "      }).join('');"
)

NEW_RENDER = (
    "      list.innerHTML = data.scenarios.map(function(s) {\n"
    "        const idPart = s.id ? '<span class=\"sfs-id\">' + escapeHtml(s.id) + '</span>' : '';\n"
    "        const kpiPart = s.kpi ? '<span class=\"sfs-kpi\">' + escapeHtml(s.kpi) + '</span>' : '';\n"
    "        const href = s.path || '#';\n"
    "        // Derive domain from path: path = ../scenarios/<PRACTICE>/<domain>/<ID-slug>/\n"
    "        let domain = '';\n"
    "        if (s.path) {\n"
    "          const parts = s.path.split('/');\n"
    "          if (parts.length >= 5) domain = parts[3] || '';\n"
    "        }\n"
    "        const domainLabel = domain\n"
    "          ? domain.replace(/-/g, ' ').replace(/\\b\\w/g, function(c) { return c.toUpperCase(); })\n"
    "          : '';\n"
    "\n"
    "        // If this scenario has a full authored chain (one of the 35 featured),\n"
    "        // render the 6-row chain matching the Chain Views tab style.\n"
    "        const chain = (window.FEATURED_CHAINS_BY_ID || {})[s.id];\n"
    "        let detailBody;\n"
    "        if (chain) {\n"
    "          detailBody =\n"
    "            '<div class=\"sfs-chain\">' +\n"
    "              (chain.scenario  ? '<div class=\"sfs-row sfs-r-scenario\"><span class=\"sfs-row-label\">Scenario</span><div class=\"sfs-row-body\">' + escapeHtml(chain.scenario) + '</div></div>' : '') +\n"
    "              (chain.solution  ? '<div class=\"sfs-row sfs-r-solution\"><span class=\"sfs-row-label\">Solution</span><div class=\"sfs-row-body\">' + escapeHtml(chain.solution) + '</div></div>' : '') +\n"
    "              (chain.use_case  ? '<div class=\"sfs-row sfs-r-usecase\"><span class=\"sfs-row-label\">Use Case</span><div class=\"sfs-row-body\">' + escapeHtml(chain.use_case) + '</div></div>' : '') +\n"
    "              (chain.service_text ? '<div class=\"sfs-row sfs-r-service\"><span class=\"sfs-row-label\">Service</span><div class=\"sfs-row-body\">' + escapeHtml(chain.service_text) + '</div></div>' : '') +\n"
    "              (chain.persona   ? '<div class=\"sfs-row sfs-r-persona\"><span class=\"sfs-row-label\">Persona</span><div class=\"sfs-row-body\">' + escapeHtml(chain.persona) + '</div></div>' : '') +\n"
    "              (chain.kpi       ? '<div class=\"sfs-row sfs-r-kpi\"><span class=\"sfs-row-label\">KPI</span><div class=\"sfs-row-body\">' + escapeHtml(chain.kpi) + '</div></div>' : '') +\n"
    "            '</div>' +\n"
    "            '<div class=\"sfs-detail-grid sfs-meta-grid\">' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Domain</div><div class=\"sfs-field-value\">' + escapeHtml(domainLabel || '\u2014') + '</div></div>' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Practice</div><div class=\"sfs-field-value\">' + escapeHtml(data.practice) + '</div></div>' +\n"
    "              (s.id ? '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Scenario ID</div><div class=\"sfs-field-value\"><code>' + escapeHtml(s.id) + '</code></div></div>' : '') +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Status</div><div class=\"sfs-field-value\"><span class=\"sfs-badge-featured\">\u2B50 Featured chain</span></div></div>' +\n"
    "            '</div>';\n"
    "        } else {\n"
    "          // Compact scenario — lightweight 4-field grid + blurb\n"
    "          detailBody =\n"
    "            '<div class=\"sfs-detail-grid\">' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Domain</div><div class=\"sfs-field-value\">' + escapeHtml(domainLabel || '\u2014') + '</div></div>' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Service</div><div class=\"sfs-field-value\"><code>' + escapeHtml(data.code) + '</code> ' + escapeHtml(data.name) + '</div></div>' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Practice</div><div class=\"sfs-field-value\">' + escapeHtml(data.practice) + '</div></div>' +\n"
    "              (s.id ? '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Scenario ID</div><div class=\"sfs-field-value\"><code>' + escapeHtml(s.id) + '</code></div></div>' : '') +\n"
    "            '</div>' +\n"
    "            '<div class=\"sfs-field sfs-field-full\"><div class=\"sfs-field-label\">Description</div><div class=\"sfs-field-value\">' + escapeHtml(s.blurb) + '</div></div>';\n"
    "        }\n"
    "\n"
    "        return (\n"
    "          '<div class=\"svc-flyout-scenario\" data-scenario-id=\"' + escapeHtml(s.id || '') + '\">' +\n"
    "            '<div class=\"sfs-head\">' +\n"
    "              '<div class=\"sfs-head-main\">' +\n"
    "                idPart +\n"
    "                '<span class=\"sfs-title\">' + escapeHtml(s.title) + '</span>' +\n"
    "              '</div>' +\n"
    "              '<div class=\"sfs-head-meta\">' + kpiPart + '</div>' +\n"
    "              '<svg class=\"sfs-chevron\" viewBox=\"0 0 24 24\" width=\"16\" height=\"16\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><polyline points=\"9 18 15 12 9 6\"></polyline></svg>' +\n"
    "            '</div>' +\n"
    "            '<div class=\"sfs-detail\">' +\n"
    "              detailBody +\n"
    "              '<div class=\"sfs-actions\">' +\n"
    "                (href !== '#' ? '<a class=\"sfs-action sfs-action-primary\" href=\"' + escapeHtml(href) + '\" target=\"_blank\" rel=\"noopener\">' +\n"
    "                  '<svg viewBox=\"0 0 24 24\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6\"></path><polyline points=\"15 3 21 3 21 9\"></polyline><line x1=\"10\" y1=\"14\" x2=\"21\" y2=\"3\"></line></svg>' +\n"
    "                  'Open folder on disk' +\n"
    "                '</a>' : '') +\n"
    "              '</div>' +\n"
    "            '</div>' +\n"
    "          '</div>'\n"
    "        );\n"
    "      }).join('');"
)

if OLD_RENDER in html:
    html = html.replace(OLD_RENDER, NEW_RENDER)
    print("Rewrote flyout render template with full-chain branch")
else:
    print("ERROR: old render template not matched — aborting")
    sys.exit(1)

# ---- 4. CSS for the 6-row chain + featured badge + meta-grid ----------------

CSS = (
    MARKER + "\n"
    ".svc-flyout-scenario.open .sfs-detail {\n"
    "  max-height: 1200px;\n"
    "}\n"
    ".sfs-chain {\n"
    "  display: flex; flex-direction: column; gap: 8px;\n"
    "  margin-bottom: 14px;\n"
    "}\n"
    ".sfs-row {\n"
    "  display: flex; gap: 10px; align-items: flex-start;\n"
    "  padding: 8px 10px;\n"
    "  border-radius: 4px;\n"
    "  background: color-mix(in srgb, var(--bg-2, #131313) 45%, transparent);\n"
    "  border-left: 3px solid transparent;\n"
    "}\n"
    ".sfs-row-label {\n"
    "  font-family: 'JetBrains Mono', 'Consolas', monospace;\n"
    "  font-size: 9.5px;\n"
    "  font-weight: 700;\n"
    "  letter-spacing: 0.14em;\n"
    "  text-transform: uppercase;\n"
    "  min-width: 68px;\n"
    "  flex-shrink: 0;\n"
    "  padding-top: 2px;\n"
    "}\n"
    ".sfs-row-body {\n"
    "  font-size: 12.5px;\n"
    "  line-height: 1.55;\n"
    "  color: var(--ink-1, #e6edf3);\n"
    "  flex: 1 1 auto;\n"
    "}\n"
    ".sfs-r-scenario { border-left-color: var(--amber, #E3B657); }\n"
    ".sfs-r-scenario .sfs-row-label { color: var(--amber, #E3B657); }\n"
    ".sfs-r-solution { border-left-color: var(--teal, #44B8A8); }\n"
    ".sfs-r-solution .sfs-row-label { color: var(--teal, #44B8A8); }\n"
    ".sfs-r-usecase { border-left-color: var(--sky, #6FB9E8); }\n"
    ".sfs-r-usecase .sfs-row-label { color: var(--sky, #6FB9E8); }\n"
    ".sfs-r-service { border-left-color: var(--violet, #8E7AD6); }\n"
    ".sfs-r-service .sfs-row-label { color: var(--violet, #8E7AD6); }\n"
    ".sfs-r-persona { border-left-color: var(--crimson, #D34848); }\n"
    ".sfs-r-persona .sfs-row-label { color: var(--crimson, #D34848); }\n"
    ".sfs-r-kpi { border-left-color: var(--gold, #E3B657); }\n"
    ".sfs-r-kpi .sfs-row-label { color: var(--gold, #E3B657); }\n"
    ".sfs-r-kpi .sfs-row-body { font-weight: 600; color: var(--ink-0, #fff); }\n"
    ".sfs-meta-grid {\n"
    "  margin-top: 4px;\n"
    "  padding-top: 12px;\n"
    "  border-top: 1px solid color-mix(in srgb, var(--line, #2a2a2a) 60%, transparent);\n"
    "}\n"
    ".sfs-badge-featured {\n"
    "  display: inline-block;\n"
    "  font-size: 10.5px;\n"
    "  font-weight: 600;\n"
    "  padding: 2px 8px;\n"
    "  border-radius: 10px;\n"
    "  background: color-mix(in srgb, var(--gold, #E3B657) 18%, transparent);\n"
    "  color: var(--gold, #E3B657);\n"
    "}\n"
)

close_style = html.find("</style>")
if close_style != -1:
    html = html[:close_style] + CSS + html[close_style:]
    print("Injected full-chain CSS")

HTML.write_text(html, encoding="utf-8")
print(f"\nWrote {HTML}")
