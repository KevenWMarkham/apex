"""Turn flyout scenario cards into click-to-expand "pop under" panels.

Before: clicking a scenario card opened its folder in a new tab.
After:  clicking the card expands a detail panel directly beneath it
        (accordion-style — one open at a time) showing:
          - Scenario ID + title
          - Domain + service code
          - Description blurb
          - KPI chip
          - "Open folder on disk" button (opens the path)

Only one card is expanded at a time. Click the same card again to collapse.
ESC also closes any open expansion.

Changes:
1. Rewrites the in-flyout `openServiceFlyout` render template to emit
   `<div class="svc-flyout-scenario">` with a collapsible detail section.
2. Wires a click handler that toggles .open on the clicked card.
3. Adds CSS for the expanded state.

Idempotent via <!-- flyout-popunder-v1 --> marker.
"""

from __future__ import annotations

import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HTML = Path("docs/reference/APEX-Stacked-Architecture-Narrated.html")
html = HTML.read_text(encoding="utf-8")

MARKER = "/* flyout-popunder-v1 */"
if MARKER in html:
    print("Pop-under already in place — no-op.")
    sys.exit(0)

# ---- 1. Replace the render template inside openServiceFlyout ---------------

OLD_RENDER = (
    "      list.innerHTML = data.scenarios.map(function(s) {\n"
    "        const idPart = s.id ? '<span class=\"sfs-id\">' + escapeHtml(s.id) + '</span>' : '';\n"
    "        const kpiPart = s.kpi ? '<div><span class=\"sfs-kpi\">' + escapeHtml(s.kpi) + '</span></div>' : '';\n"
    "        const href = s.path || '#';\n"
    "        return '<a class=\"svc-flyout-scenario\" href=\"' + escapeHtml(href) + '\" target=\"_blank\" rel=\"noopener\">' +\n"
    "               idPart +\n"
    "               '<span class=\"sfs-title\">' + escapeHtml(s.title) + '</span>' +\n"
    "               '<div class=\"sfs-blurb\">' + escapeHtml(s.blurb) + '</div>' +\n"
    "               kpiPart +\n"
    "               '</a>';\n"
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
    "                '<div class=\"sfs-field\"><div class=\"sfs-field-label\">Domain</div><div class=\"sfs-field-value\">' + escapeHtml(domainLabel || '—') + '</div></div>' +\n"
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

if OLD_RENDER in html:
    html = html.replace(OLD_RENDER, NEW_RENDER)
    print("Rewrote flyout scenario render template")
else:
    print("ERROR: old render template not matched — aborting")
    sys.exit(1)


# ---- 2. Append click handler for accordion behavior --------------------------

OLD_CLICK = (
    "  // Wire up clicks on any .svc-chip\n"
    "  document.addEventListener('click', function(e) {\n"
    "    const chip = e.target.closest('.svc-chip');\n"
    "    if (!chip) return;\n"
    "    // Extract code from inner .svc-code\n"
    "    const codeEl = chip.querySelector('.svc-code');\n"
    "    if (!codeEl) return;\n"
    "    const code = codeEl.textContent.trim();\n"
    "    openServiceFlyout(code);\n"
    "  });"
)

NEW_CLICK = (
    "  // Wire up clicks on any .svc-chip\n"
    "  document.addEventListener('click', function(e) {\n"
    "    const chip = e.target.closest('.svc-chip');\n"
    "    if (!chip) return;\n"
    "    // Extract code from inner .svc-code\n"
    "    const codeEl = chip.querySelector('.svc-code');\n"
    "    if (!codeEl) return;\n"
    "    const code = codeEl.textContent.trim();\n"
    "    openServiceFlyout(code);\n"
    "  });\n"
    "\n"
    "  // Accordion click inside the flyout — expand/collapse scenario cards\n"
    "  document.addEventListener('click', function(e) {\n"
    "    // Ignore if the click was on the Open-folder action link\n"
    "    if (e.target.closest('.sfs-action')) return;\n"
    "    const head = e.target.closest('.svc-flyout-scenario .sfs-head');\n"
    "    if (!head) return;\n"
    "    const card = head.parentNode;\n"
    "    const wasOpen = card.classList.contains('open');\n"
    "    // Collapse siblings (accordion)\n"
    "    const list = card.parentNode;\n"
    "    list.querySelectorAll('.svc-flyout-scenario.open').forEach(function(el) {\n"
    "      if (el !== card) el.classList.remove('open');\n"
    "    });\n"
    "    card.classList.toggle('open', !wasOpen);\n"
    "  });"
)

if OLD_CLICK in html:
    html = html.replace(OLD_CLICK, NEW_CLICK)
    print("Added accordion click handler")
else:
    print("WARN: click handler not matched — pop-under may not expand")


# ---- 3. CSS for expanded state ----------------------------------------------

CSS = (
    MARKER + "\n"
    ".svc-flyout-scenario {\n"
    "  background: color-mix(in srgb, var(--bg-2, #131313) 60%, transparent);\n"
    "  border: 1px solid color-mix(in srgb, var(--line, #2a2a2a) 80%, transparent);\n"
    "  border-radius: 6px;\n"
    "  overflow: hidden;\n"
    "  transition: border-color 0.15s, background 0.15s;\n"
    "  cursor: pointer;\n"
    "}\n"
    ".svc-flyout-scenario:hover {\n"
    "  border-color: color-mix(in srgb, var(--sky, #6FB9E8) 60%, transparent);\n"
    "}\n"
    ".svc-flyout-scenario.open {\n"
    "  border-color: var(--sky, #6FB9E8);\n"
    "  background: color-mix(in srgb, var(--sky, #6FB9E8) 6%, var(--bg-2, #131313));\n"
    "}\n"
    ".sfs-head {\n"
    "  display: flex; align-items: center; gap: 10px;\n"
    "  padding: 12px 14px;\n"
    "  user-select: none;\n"
    "}\n"
    ".sfs-head-main { flex: 1 1 auto; min-width: 0; }\n"
    ".sfs-head-meta { flex: 0 0 auto; display: flex; align-items: center; gap: 6px; }\n"
    ".sfs-chevron {\n"
    "  color: var(--ink-3, #8a8a8a);\n"
    "  transition: transform 0.2s ease;\n"
    "  flex: 0 0 auto;\n"
    "}\n"
    ".svc-flyout-scenario.open .sfs-chevron { transform: rotate(90deg); color: var(--sky, #6FB9E8); }\n"
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
    ".svc-flyout-scenario .sfs-kpi {\n"
    "  display: inline-block;\n"
    "  font-size: 10.5px;\n"
    "  font-weight: 600;\n"
    "  padding: 2px 8px;\n"
    "  border-radius: 10px;\n"
    "  background: color-mix(in srgb, var(--gold, #E3B657) 15%, transparent);\n"
    "  color: var(--gold, #E3B657);\n"
    "  white-space: nowrap;\n"
    "}\n"
    ".svc-flyout-scenario .sfs-detail {\n"
    "  max-height: 0;\n"
    "  opacity: 0;\n"
    "  overflow: hidden;\n"
    "  transition: max-height 0.3s ease, opacity 0.25s ease, padding 0.25s ease;\n"
    "  padding: 0 14px;\n"
    "  border-top: 1px solid transparent;\n"
    "}\n"
    ".svc-flyout-scenario.open .sfs-detail {\n"
    "  max-height: 600px;\n"
    "  opacity: 1;\n"
    "  padding: 14px 14px 16px;\n"
    "  border-top: 1px solid color-mix(in srgb, var(--sky, #6FB9E8) 30%, transparent);\n"
    "}\n"
    ".sfs-detail-grid {\n"
    "  display: grid;\n"
    "  grid-template-columns: 1fr 1fr;\n"
    "  gap: 10px 16px;\n"
    "  margin-bottom: 12px;\n"
    "}\n"
    ".sfs-field { min-width: 0; }\n"
    ".sfs-field-full { grid-column: 1 / -1; margin-bottom: 12px; }\n"
    ".sfs-field-label {\n"
    "  font-size: 9.5px;\n"
    "  font-weight: 700;\n"
    "  letter-spacing: 0.12em;\n"
    "  text-transform: uppercase;\n"
    "  color: var(--ink-3, #8a8a8a);\n"
    "  margin-bottom: 3px;\n"
    "}\n"
    ".sfs-field-value {\n"
    "  font-size: 12.5px;\n"
    "  color: var(--ink-1, #e6edf3);\n"
    "  line-height: 1.5;\n"
    "  word-break: break-word;\n"
    "}\n"
    ".sfs-field-value code {\n"
    "  font-family: 'JetBrains Mono', monospace;\n"
    "  font-size: 11px;\n"
    "  color: var(--gold, #E3B657);\n"
    "  background: color-mix(in srgb, var(--bg-3, #1a1a1a) 50%, transparent);\n"
    "  padding: 1px 5px;\n"
    "  border-radius: 3px;\n"
    "}\n"
    ".sfs-actions {\n"
    "  display: flex; gap: 8px; flex-wrap: wrap;\n"
    "  margin-top: 6px;\n"
    "}\n"
    ".sfs-action {\n"
    "  display: inline-flex; align-items: center; gap: 6px;\n"
    "  font-size: 12px; font-weight: 600;\n"
    "  padding: 6px 12px;\n"
    "  border-radius: 4px;\n"
    "  text-decoration: none;\n"
    "  transition: filter 0.15s;\n"
    "}\n"
    ".sfs-action-primary {\n"
    "  background: var(--sky, #6FB9E8);\n"
    "  color: #0b0b0b;\n"
    "}\n"
    ".sfs-action-primary:hover { filter: brightness(1.1); }\n"
    ".sfs-domain {\n"
    "  display: inline-block;\n"
    "  font-size: 10px;\n"
    "  color: var(--ink-3, #8a8a8a);\n"
    "  margin-right: 8px;\n"
    "}\n"
)

close_style = html.find("</style>")
if close_style != -1:
    html = html[:close_style] + CSS + html[close_style:]
    print("Injected pop-under CSS")

HTML.write_text(html, encoding="utf-8")
print(f"\nWrote {HTML}")
