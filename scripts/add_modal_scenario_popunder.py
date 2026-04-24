"""Make scenario rows in the library modal click-to-expand (pop-under).

Before: clicking the ID pill on a scenario row opened the folder path
in a new tab; clicking elsewhere on the row did nothing.

After: clicking anywhere on a row toggles a pop-under detail panel
directly beneath it (accordion — only one open at a time). The detail
panel content mirrors the service-flyout pop-under:
  - Featured scenarios (35) → full 6-row chain (Scenario / Solution /
    Use Case / Service / Persona / KPI) with colored row labels
  - Compact scenarios (688)   → headline KPI banner + 6-field metadata
    grid + description + sibling note + "promote to featured" hint
  - Both show an "Open folder on disk" primary action button at the
    bottom of the expanded panel

The existing sr-id visual treatment is preserved as a non-link badge
so the ID is still readable at a glance — the click action moves from
the <a> to the whole row.

Idempotent via /* modal-scenario-popunder-v1 */ marker.
"""

from __future__ import annotations

import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HTML = Path("docs/reference/APEX-Stacked-Architecture-Narrated.html")
html = HTML.read_text(encoding="utf-8")

MARKER = "/* modal-scenario-popunder-v1 */"
if MARKER in html:
    print("Modal scenario pop-under already in place — no-op.")
    sys.exit(0)

# ---- 1. Replace the scenario-row render template -----------------------------

OLD_ROW = (
    "'<div class=\"scenario-row\" role=\"listitem\" data-search=\"' + escapeHtml(searchData) + '\" data-domain=\"' + escapeHtml(item.domain || '') + '\" data-practice=\"' + escapeHtml(practiceCode || '') + '\">' +\n"
    "        '<div class=\"sr-main\">' +\n"
    "          (item.id ? '<a class=\"sr-id\" href=\"' + escapeHtml(item.p || '#') + '\" target=\"_blank\" rel=\"noopener\" title=\"Open folder\">' + escapeHtml(item.id) + '</a>' : '') +\n"
    "          '<div class=\"sr-title\">' + titleSafe + '</div>' +\n"
    "          '<div class=\"sr-brief\">' + briefSafe + '</div>' +\n"
    "        '</div>' +\n"
    "        '<div class=\"sr-service\">' + serviceSafe + '</div>' +\n"
    "        '<div class=\"sr-kpi-wrap\"><span class=\"sr-kpi ' + kk + '\">' + kpiSafe + '</span></div>' +\n"
    "      '</div>';"
)

# Helper JS that computes the detail body (full chain for featured, enriched
# compact otherwise). Same logic as the flyout pop-under, slightly adapted.

NEW_ROW = (
    "(function() {\n"
    "        const hasChain = !!((window.FEATURED_CHAINS_BY_ID || {})[item.id]);\n"
    "        const chain = hasChain ? window.FEATURED_CHAINS_BY_ID[item.id] : null;\n"
    "        const sceneDomain = item.domain || '';\n"
    "        const sceneDomainLabel = sceneDomain\n"
    "          ? sceneDomain.replace(/-/g, ' ').replace(/\\b\\w/g, function(c) { return c.toUpperCase(); })\n"
    "          : '\u2014';\n"
    "        const kpiArrow = kk === 'up' ? '\u2191' : (kk === 'down' ? '\u2193' : '\u00B7');\n"
    "        const kpiDirClass = kk === 'up' ? 'sfs-kpi-up' : (kk === 'down' ? 'sfs-kpi-down' : '');\n"
    "        const domainCount = (window.FLYOUT_DOMAIN_COUNTS || {})[practiceCode] && (window.FLYOUT_DOMAIN_COUNTS[practiceCode][sceneDomain] || 0);\n"
    "        const siblingTxt = domainCount ? ('This is 1 of ' + domainCount + ' scenarios in ' + sceneDomainLabel + ' (' + practiceCode + ').') : '';\n"
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
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Domain</div><div class=\"sfs-field-value\">' + escapeHtml(sceneDomainLabel) + '</div></div>' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Practice</div><div class=\"sfs-field-value\">' + escapeHtml(practiceCode) + '</div></div>' +\n"
    "              (item.id ? '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Scenario ID</div><div class=\"sfs-field-value\"><code>' + escapeHtml(item.id) + '</code></div></div>' : '') +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Status</div><div class=\"sfs-field-value\"><span class=\"sfs-badge-featured\">\u2B50 Featured chain</span></div></div>' +\n"
    "            '</div>';\n"
    "        } else {\n"
    "          detailBody =\n"
    "            '<div class=\"sfs-kpi-banner\">' +\n"
    "              '<span class=\"sfs-kpi-banner-label\">Headline KPI</span>' +\n"
    "              '<span class=\"sfs-kpi-banner-value ' + kpiDirClass + '\">' + kpiArrow + ' ' + escapeHtml(item.k || '\u2014') + '</span>' +\n"
    "            '</div>' +\n"
    "            '<div class=\"sfs-detail-grid\">' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Scenario ID</div><div class=\"sfs-field-value\">' + (item.id ? '<code>' + escapeHtml(item.id) + '</code>' : '\u2014') + '</div></div>' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Practice</div><div class=\"sfs-field-value\">' + escapeHtml(practiceCode) + '</div></div>' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Domain</div><div class=\"sfs-field-value\">' + escapeHtml(sceneDomainLabel) + '</div></div>' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Service</div><div class=\"sfs-field-value\"><code>' + escapeHtml(item.s || '') + '</code></div></div>' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">KPI Direction</div><div class=\"sfs-field-value\"><span class=\"' + kpiDirClass + '\">' + kpiArrow + ' ' + (kk === 'up' ? 'Upside metric' : (kk === 'down' ? 'Reduction metric' : 'Neutral')) + '</span></div></div>' +\n"
    "              '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Status</div><div class=\"sfs-field-value\"><span class=\"sfs-badge-compact\">Compact catalog entry</span></div></div>' +\n"
    "            '</div>' +\n"
    "            '<div class=\"sfs-field sfs-field-full\"><div class=\"sfs-field-label\">Description</div><div class=\"sfs-field-value\">' + escapeHtml(item.b) + '</div></div>' +\n"
    "            (siblingTxt ? '<div class=\"sfs-sibling-note\">' + escapeHtml(siblingTxt) + ' Browse the rest through its folder.</div>' : '') +\n"
    "            '<div class=\"sfs-promote\">' +\n"
    "              '<span class=\"sfs-promote-label\">Promote to featured</span>' +\n"
    "              '<span class=\"sfs-promote-body\">Author the full Scenario \u2192 Solution \u2192 Use Case \u2192 Service \u2192 Persona \u2192 KPI chain in this scenario\\'s README and it graduates into the Chain Views tab with the 35 featured scenarios.</span>' +\n"
    "            '</div>';\n"
    "        }\n"
    "        const href = item.p || '';\n"
    "        const actionBtn = href ? (\n"
    "          '<div class=\"sfs-actions\">' +\n"
    "            '<a class=\"sfs-action sfs-action-primary\" href=\"' + escapeHtml(href) + '\" target=\"_blank\" rel=\"noopener\" onclick=\"event.stopPropagation();\">' +\n"
    "              '<svg viewBox=\"0 0 24 24\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"><path d=\"M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6\"></path><polyline points=\"15 3 21 3 21 9\"></polyline><line x1=\"10\" y1=\"14\" x2=\"21\" y2=\"3\"></line></svg>' +\n"
    "              'Open folder on disk' +\n"
    "            '</a>' +\n"
    "          '</div>'\n"
    "        ) : '';\n"
    "        return (\n"
    "          '<div class=\"scenario-row\" role=\"listitem\" data-search=\"' + escapeHtml(searchData) + '\" data-domain=\"' + escapeHtml(item.domain || '') + '\" data-practice=\"' + escapeHtml(practiceCode || '') + '\">' +\n"
    "            '<div class=\"sr-head\">' +\n"
    "              '<div class=\"sr-main\">' +\n"
    "                (item.id ? '<span class=\"sr-id\" title=\"Click the row to expand details\">' + escapeHtml(item.id) + '</span>' : '') +\n"
    "                '<div class=\"sr-title\">' + titleSafe + '</div>' +\n"
    "                '<div class=\"sr-brief\">' + briefSafe + '</div>' +\n"
    "              '</div>' +\n"
    "              '<div class=\"sr-service\">' + serviceSafe + '</div>' +\n"
    "              '<div class=\"sr-kpi-wrap\"><span class=\"sr-kpi ' + kk + '\">' + kpiSafe + '</span></div>' +\n"
    "              '<svg class=\"sr-chevron\" viewBox=\"0 0 24 24\" width=\"14\" height=\"14\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.5\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><polyline points=\"9 18 15 12 9 6\"></polyline></svg>' +\n"
    "            '</div>' +\n"
    "            '<div class=\"sr-detail\">' +\n"
    "              detailBody +\n"
    "              actionBtn +\n"
    "            '</div>' +\n"
    "          '</div>'\n"
    "        );\n"
    "      })()"
)

if OLD_ROW in html:
    html = html.replace(OLD_ROW, NEW_ROW)
    print("Rewrote scenario-row render template")
else:
    print("ERROR: old row template not matched")
    sys.exit(1)


# ---- 2. Accordion click handler ---------------------------------------------

CLICK_HANDLER = r"""
<script>
/* modal-scenario-popunder-v1 */
(function() {
  'use strict';
  document.addEventListener('click', function(e) {
    // Ignore clicks on primary action buttons inside a row
    if (e.target.closest('.sfs-action')) return;
    const head = e.target.closest('#scenarioModalBody .scenario-row .sr-head');
    if (!head) return;
    const row = head.parentNode;
    const wasOpen = row.classList.contains('open');
    // Close siblings (accordion)
    const body = document.getElementById('scenarioModalBody');
    if (body) {
      body.querySelectorAll('.scenario-row.open').forEach(function(el) {
        if (el !== row) el.classList.remove('open');
      });
    }
    row.classList.toggle('open', !wasOpen);
    // Scroll the opened row into view if it's near the bottom
    if (!wasOpen) {
      setTimeout(function() {
        row.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }, 120);
    }
  });
})();
</script>
"""

close_body = html.rfind("</body>")
if close_body != -1:
    html = html[:close_body] + CLICK_HANDLER + html[close_body:]
    print("Injected accordion click handler")


# ---- 3. CSS additions ------------------------------------------------------

CSS = (
    "/* modal-scenario-popunder-v1 */\n"
    ".scenario-row {\n"
    "  cursor: pointer;\n"
    "  display: flex;\n"
    "  flex-direction: column;\n"
    "  border-radius: 0;\n"
    "  border-bottom: 1px solid var(--line);\n"
    "  background: transparent;\n"
    "  transition: background 0.15s;\n"
    "}\n"
    ".scenario-row:hover { background: color-mix(in srgb, var(--bg-2) 50%, transparent); }\n"
    ".scenario-row.open { background: color-mix(in srgb, var(--sky, #6FB9E8) 4%, var(--bg-1)); }\n"
    ".sr-head {\n"
    "  display: grid;\n"
    "  grid-template-columns: 1fr auto auto auto;\n"
    "  align-items: center;\n"
    "  gap: 12px;\n"
    "  padding: 10px 16px;\n"
    "}\n"
    ".sr-chevron {\n"
    "  color: var(--ink-3, #8a8a8a);\n"
    "  transition: transform 0.2s ease, color 0.2s;\n"
    "  flex: 0 0 auto;\n"
    "}\n"
    ".scenario-row.open .sr-chevron {\n"
    "  transform: rotate(90deg);\n"
    "  color: var(--sky, #6FB9E8);\n"
    "}\n"
    ".sr-id {\n"
    "  display: inline-block;\n"
    "  font-family: 'JetBrains Mono', 'Consolas', monospace;\n"
    "  font-size: 10.5px;\n"
    "  font-weight: 700;\n"
    "  letter-spacing: 0.06em;\n"
    "  color: var(--sky, #6FB9E8);\n"
    "  background: color-mix(in srgb, var(--sky, #6FB9E8) 14%, transparent);\n"
    "  border: 1px solid color-mix(in srgb, var(--sky, #6FB9E8) 40%, transparent);\n"
    "  padding: 2px 8px;\n"
    "  border-radius: 3px;\n"
    "  margin-right: 10px;\n"
    "  text-decoration: none;\n"
    "  vertical-align: baseline;\n"
    "}\n"
    ".sr-detail {\n"
    "  max-height: 0;\n"
    "  opacity: 0;\n"
    "  overflow: hidden;\n"
    "  transition: max-height 0.35s ease, opacity 0.25s ease, padding 0.25s ease;\n"
    "  padding: 0 16px;\n"
    "  border-top: 1px solid transparent;\n"
    "}\n"
    ".scenario-row.open .sr-detail {\n"
    "  max-height: 1400px;\n"
    "  opacity: 1;\n"
    "  padding: 16px 16px 20px 16px;\n"
    "  border-top: 1px solid color-mix(in srgb, var(--sky, #6FB9E8) 30%, transparent);\n"
    "  overflow: visible;\n"
    "}\n"
    ".scenario-row.open .sr-detail .sfs-actions { margin-top: 10px; }\n"
)

close_style = html.find("</style>")
if close_style != -1:
    html = html[:close_style] + CSS + html[close_style:]
    print("Injected pop-under CSS")

HTML.write_text(html, encoding="utf-8")
print(f"\nWrote {HTML}")
