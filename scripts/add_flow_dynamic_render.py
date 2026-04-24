"""Make the Flow diagram actually re-render when the scenario dropdown changes.

The diagram is authored as static SVG. Each node is a <g data-node="NODE_ID">
with <text class="node-title"> and <text class="node-subtitle">. We add a
runtime that reads APEX_FLOW_DATA[currentScenarioKey] and rewrites every node's
title, subtitle, aria-label. Also updates the two .fss-card summary panels at
the bottom.

Calls the update once at page load (so the initial cold-chain state is
preserved), and on every scenario dropdown change.

Idempotent via /* flow-dynamic-render-v1 */ marker.
"""

from __future__ import annotations

import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HTML = Path("docs/reference/APEX-Stacked-Architecture-Narrated.html")
html = HTML.read_text(encoding="utf-8")

MARKER = "/* flow-dynamic-render-v1 */"
if MARKER in html:
    print("Dynamic render already in place — no-op.")
    sys.exit(0)

# The runtime — injected at the end of body. Hooks into the scenario dropdown's
# change event + fires once on load. Reads APEX_FLOW_DATA + FEATURED_CHAINS_BY_ID
# + ID_TO_FLOW_KEY (all already present in the page).

RENDER_JS = r"""
<script>
/* flow-dynamic-render-v1 */
(function() {
  'use strict';

  // Reverse map: flow_key -> scenario_id (for chain lookup)
  function flowKeyToScenarioId(fk) {
    const map = window.ID_TO_FLOW_KEY || {};
    for (const sid in map) {
      if (map[sid] === fk) return sid;
    }
    return null;
  }

  // Split a title at a reasonable word boundary for 2-line SVG rendering
  function splitTitle(title, parts) {
    if (parts <= 1) return [title];
    // Try to split near the middle at a space, prefer ' · ' or ' + ' or ' — '
    const len = title.length;
    const splitters = [' · ', ' + ', ' — ', ' - ', ': ', ' '];
    for (const sep of splitters) {
      const idx = title.indexOf(sep);
      if (idx > 6 && idx < len - 4) {
        return [
          title.slice(0, idx + (sep.length > 1 ? sep.length : 0)),
          title.slice(idx + sep.length),
        ];
      }
    }
    // Fallback: split midword
    const mid = Math.ceil(len / 2);
    return [title.slice(0, mid), title.slice(mid)];
  }

  function setTextContent(textEl, s) {
    // Preserve styling, replace text nodes
    textEl.textContent = s || '';
  }

  function updateNode(nodeEl, nodeData) {
    if (!nodeData) return;
    nodeEl.setAttribute('aria-label', nodeData.title || '');
    const titleEls = Array.from(nodeEl.querySelectorAll('text.node-title'));
    const subtitleEls = Array.from(nodeEl.querySelectorAll('text.node-subtitle'));
    if (titleEls.length === 1) {
      setTextContent(titleEls[0], nodeData.title);
    } else if (titleEls.length >= 2) {
      const parts = splitTitle(nodeData.title || '', titleEls.length);
      titleEls.forEach(function(t, i) { setTextContent(t, parts[i] || ''); });
    }
    if (subtitleEls.length >= 1 && nodeData.subtitle !== undefined) {
      setTextContent(subtitleEls[0], nodeData.subtitle);
    }
  }

  function updateScenarioSummaryCards(chain, scenarioId, flowKey) {
    // Two .fss-card divs at the bottom of the Flow tab
    const pane = document.querySelector('.tab-panel[data-tab-panel="flow"]');
    if (!pane) return;
    const cards = pane.querySelectorAll('.fss-card');
    if (cards.length < 2) return;

    // Card 1: Scenario
    const titleEl = cards[0].querySelector('.fss-title');
    const metaEl = cards[0].querySelector('.fss-meta');
    if (titleEl && chain) {
      titleEl.textContent = chain.title || '';
    }
    if (metaEl) {
      // Use Service row if present (strip HTML), plus persona, plus scenario id
      const svcText = (chain && chain.service_text) ? chain.service_text : '';
      const personaText = (chain && chain.persona) ? chain.persona : '';
      const personaShort = personaText.split(/[·\.]/)[0].trim();
      const parts = [];
      if (svcText) parts.push(svcText.replace(/\s+/g, ' ').slice(0, 110));
      if (personaShort) parts.push('Primary persona <b>' + escapeHtml(personaShort) + '</b>');
      if (scenarioId) parts.push('<code>' + escapeHtml(scenarioId) + '</code>');
      metaEl.innerHTML = parts.join(' · ');
    }

    // Card 2: "What to see" — keep generic wave-ribbon guidance but mention scenario
    const body2 = cards[1].querySelector('.fss-body');
    if (body2 && chain) {
      body2.innerHTML =
        'Follow the amber <b>W2 Pilot</b> lane — it is <b>' + escapeHtml(chain.title) + '</b> at its proof-point scale. ' +
        'Sky <b>W1 Foundation</b> is what had to be true before; amber <b>W3 Scale &amp; Fuse</b> is what enterprise scope unlocks. ' +
        'The <b>three amber cross-wave arrows</b> bind the progression: ' +
        'W1 HITL template powers the W2 approval, W1 LEDGER accumulates W2 audit rows, W2 proven KPIs unlock W3 scaling.';
    }
  }

  function escapeHtml(s) {
    return String(s || '').replace(/[&<>"']/g, function(c) {
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }

  function renderFlowForKey(flowKey) {
    const allData = window.APEX_FLOW_DATA || {};
    const nodes = allData[flowKey];
    if (!nodes) return;

    // Update every SVG node whose data-node matches a key in `nodes`
    document.querySelectorAll('g.flow-node[data-node]').forEach(function(el) {
      const id = el.getAttribute('data-node');
      const nd = nodes[id];
      if (nd) updateNode(el, nd);
    });

    // Update the scenario summary cards
    const scenarioId = flowKeyToScenarioId(flowKey);
    const chain = (window.FEATURED_CHAINS_BY_ID || {})[scenarioId];
    updateScenarioSummaryCards(chain, scenarioId, flowKey);
  }

  window.renderFlowForKey = renderFlowForKey;

  // Hook into the scenario dropdown change; also expose a direct re-render
  function init() {
    const scenSel = document.getElementById('flowScenarioPicker');
    if (!scenSel) return;

    scenSel.addEventListener('change', function() {
      const key = scenSel.value;
      if (key) renderFlowForKey(key);
    });

    // Initial render of whatever is selected (defaults to rc-cold-chain-excursion)
    if (scenSel.value) renderFlowForKey(scenSel.value);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    // If DOM is already ready, defer slightly so flowUpdatePicker (which sets
    // the initial option list) runs first.
    setTimeout(init, 0);
  }
})();
</script>
"""

# Expose APEX_FLOW_DATA + ID_TO_FLOW_KEY + FEATURED_CHAINS_BY_ID as window globals
# so this script can find them regardless of declaration order. They're already
# declared with `const` in the main page; add tiny shim aliases.
SHIM_JS = r"""
<script>
/* flow-dynamic-render-v1 shim — expose page-scope consts to window */
(function() {
  if (typeof APEX_FLOW_DATA !== 'undefined')    window.APEX_FLOW_DATA    = APEX_FLOW_DATA;
  if (typeof ID_TO_FLOW_KEY  !== 'undefined')   window.ID_TO_FLOW_KEY    = ID_TO_FLOW_KEY;
  /* FEATURED_CHAINS_BY_ID is already set on window in its declaration */
})();
</script>
"""

# Inject both blocks immediately before </body>
close_body = html.rfind("</body>")
if close_body == -1:
    print("ERROR: </body> not found")
    sys.exit(1)

html = html[:close_body] + SHIM_JS + RENDER_JS + html[close_body:]

HTML.write_text(html, encoding="utf-8")
print(f"Injected dynamic flow render runtime")
print(f"Wrote {HTML}")
