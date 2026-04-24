"""Add the full 47-archetype catalog to the Reasoning (Layer 06) page.

Extracts ARCHETYPES from packages/apex-orchestrator/.../catalog.py and
renders them as an interactive filterable grid on the Reasoning page,
right after the 4-primitive pattern cards. Each archetype:
  - shows ID + name + pattern pill + status pill
  - is clickable → modal with full description + practice tag
  - filterable by pattern (sequential / parallel / hierarchical / feedback)
    and by status (impl / manifest-only)

Idempotent via /* archetypes-catalog-v1 */ marker.
"""

from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HTML = Path("docs/reference/APEX-Stacked-Architecture-Narrated.html")
CATALOG = Path("packages/apex-orchestrator/src/apex_orchestrator/archetypes/catalog.py")

html = HTML.read_text(encoding="utf-8")

MARKER = "/* archetypes-catalog-v1 */"
if MARKER in html:
    print("Archetype catalog already injected — no-op.")
    sys.exit(0)

# ---- 1. Extract 47 archetypes from catalog.py via regex --------------------

src = CATALOG.read_text(encoding="utf-8")
row_re = re.compile(
    r'Archetype\(\s*"([^"]+)",\s*"([^"]+)",\s*OrchestrationPattern\.([A-Z_]+),\s*"([^"]+)",\s*"([^"]+)"\s*\)'
)
archetypes = []
for m in row_re.finditer(src):
    archetypes.append({
        "id": m.group(1),
        "name": m.group(2),
        "pattern": m.group(3).lower().replace("_", "-"),
        "desc": m.group(4),
        "status": m.group(5),
    })

# Tag each with practice based on ID prefix / description keywords
def tag_practice(a: dict) -> str:
    d = (a["desc"] + " " + a["name"]).lower()
    if any(k in d for k in ["rc ", "markdown", "cold chain", "recall", "bopis"]):
        return "RC"
    if any(k in d for k in ["hls ", "clinical", "sepsis", "claim", "patient"]):
        return "HLS"
    if any(k in d for k in ["er ", "outage", "maintenance sched", "grid", "asset maintenance"]):
        return "ER"
    if any(k in d for k in ["axle ", "connected factory", "predictive maint", "quality optim", "supply chain resil"]):
        return "AXLE"
    if any(k in d for k in ["tmt ", "contact center", "content reco", "network optim", "churn"]):
        return "TMT"
    if any(k in d for k in ["th ", "revenue optim", "crew schedule", "irop", "personalised offer"]):
        return "TH"
    if any(k in d for k in ["ice ", "fleet optim", "predictive service", "dealer"]):
        return "ICE"
    return "Cross"

for a in archetypes:
    a["practice"] = tag_practice(a)

print(f"Extracted {len(archetypes)} archetypes")
assert len(archetypes) == 47, f"expected 47, got {len(archetypes)}"

archetypes_js = json.dumps(archetypes, ensure_ascii=False, separators=(",", ":"))


# ---- 2. Build the injected HTML fragment -----------------------------------

INJECTED_HTML = f"""
<!-- archetypes-catalog-v1 -->
<div class="archetypes-full-catalog">
  <div class="afc-header">
    <h3>All 47 archetypes</h3>
    <p class="afc-subhead">Each primitive pattern has a catalogue of named archetypes. Click any card for the full decision shape; filter by pattern, status, or Practice.</p>
  </div>
  <div class="afc-filters">
    <div class="afc-filter-group">
      <span class="afc-filter-label">Pattern:</span>
      <button class="afc-chip active" data-filter-pattern="all">All</button>
      <button class="afc-chip" data-filter-pattern="sequential">Sequential</button>
      <button class="afc-chip" data-filter-pattern="parallel">Parallel</button>
      <button class="afc-chip" data-filter-pattern="hierarchical">Hierarchical</button>
      <button class="afc-chip" data-filter-pattern="feedback-loop">Feedback</button>
    </div>
    <div class="afc-filter-group">
      <span class="afc-filter-label">Status:</span>
      <button class="afc-chip active" data-filter-status="all">All</button>
      <button class="afc-chip" data-filter-status="impl">Implemented (10)</button>
      <button class="afc-chip" data-filter-status="manifest-only">Manifest-only (37)</button>
    </div>
    <div class="afc-filter-group">
      <span class="afc-filter-label">Practice:</span>
      <button class="afc-chip active" data-filter-practice="all">All</button>
      <button class="afc-chip" data-filter-practice="RC">RC</button>
      <button class="afc-chip" data-filter-practice="HLS">HLS</button>
      <button class="afc-chip" data-filter-practice="ER">ER</button>
      <button class="afc-chip" data-filter-practice="AXLE">AXLE</button>
      <button class="afc-chip" data-filter-practice="TMT">TMT</button>
      <button class="afc-chip" data-filter-practice="TH">TH</button>
      <button class="afc-chip" data-filter-practice="ICE">ICE</button>
      <button class="afc-chip" data-filter-practice="Cross">Cross</button>
    </div>
    <span class="afc-count" id="afcCount">47 of 47</span>
  </div>
  <div class="afc-grid" id="afcGrid"></div>
</div>

<div id="afcModalBackdrop" class="afc-modal-backdrop" onclick="closeArchetypeModal()"></div>
<div id="afcModal" class="afc-modal" role="dialog" aria-modal="true" aria-hidden="true">
  <button class="afc-modal-close" type="button" onclick="closeArchetypeModal()" aria-label="Close">&times;</button>
  <div class="afc-modal-body">
    <div class="afc-modal-eyebrow">
      <code id="afcModalId">—</code>
      <span id="afcModalPattern" class="afc-pattern-pill">—</span>
      <span id="afcModalStatus" class="afc-status-pill">—</span>
      <span id="afcModalPractice" class="afc-practice-pill">—</span>
    </div>
    <h3 id="afcModalTitle" class="afc-modal-title">—</h3>
    <div class="afc-modal-section">
      <div class="afc-modal-label">Decision shape</div>
      <p id="afcModalDesc" class="afc-modal-desc">—</p>
    </div>
    <div class="afc-modal-section">
      <div class="afc-modal-label">Pattern meaning</div>
      <p id="afcModalPatternDesc" class="afc-modal-desc">—</p>
    </div>
    <div class="afc-modal-section">
      <div class="afc-modal-label">Cross-references</div>
      <div class="afc-modal-refs">
        <span class="afc-ref">§10 Orchestration</span>
        <span class="afc-ref">§10.2 Four Primitives</span>
        <span class="afc-ref">§10.3 47 Archetypes</span>
        <span class="afc-ref">§11 Audit Row</span>
      </div>
    </div>
  </div>
</div>
<!-- /archetypes-catalog-v1 -->
"""


CSS = (
    MARKER + "\n"
    ".archetypes-full-catalog {\n"
    "  margin-top: 40px;\n"
    "  padding-top: 32px;\n"
    "  border-top: 1px solid color-mix(in srgb, var(--line, #2a2a2a) 50%, transparent);\n"
    "}\n"
    ".afc-header h3 {\n"
    "  font-family: 'Fraunces', Georgia, serif;\n"
    "  font-size: 22px;\n"
    "  font-weight: 600;\n"
    "  color: var(--ink-0, #fff);\n"
    "  margin: 0 0 6px;\n"
    "}\n"
    ".afc-subhead {\n"
    "  font-size: 13.5px;\n"
    "  color: var(--ink-2, #b4b4b4);\n"
    "  line-height: 1.55;\n"
    "  margin: 0 0 20px;\n"
    "  max-width: 780px;\n"
    "}\n"
    ".afc-filters {\n"
    "  display: flex; flex-wrap: wrap; align-items: center;\n"
    "  gap: 8px 18px;\n"
    "  padding: 12px 14px;\n"
    "  background: color-mix(in srgb, var(--bg-2, #131313) 60%, transparent);\n"
    "  border: 1px solid var(--line, #2a2a2a);\n"
    "  border-radius: 6px;\n"
    "  margin-bottom: 20px;\n"
    "}\n"
    ".afc-filter-group { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }\n"
    ".afc-filter-label {\n"
    "  font-family: 'JetBrains Mono', monospace;\n"
    "  font-size: 10px;\n"
    "  font-weight: 700;\n"
    "  letter-spacing: 0.12em;\n"
    "  text-transform: uppercase;\n"
    "  color: var(--ink-3, #8a8a8a);\n"
    "  margin-right: 4px;\n"
    "}\n"
    ".afc-chip {\n"
    "  font-family: 'IBM Plex Sans', system-ui, sans-serif;\n"
    "  font-size: 11.5px;\n"
    "  font-weight: 500;\n"
    "  padding: 4px 10px;\n"
    "  border: 1px solid color-mix(in srgb, var(--ink-3, #8a8a8a) 40%, transparent);\n"
    "  background: transparent;\n"
    "  color: var(--ink-2, #b4b4b4);\n"
    "  border-radius: 14px;\n"
    "  cursor: pointer;\n"
    "  transition: all 0.15s;\n"
    "}\n"
    ".afc-chip:hover { border-color: var(--sky, #6FB9E8); color: var(--sky, #6FB9E8); }\n"
    ".afc-chip.active {\n"
    "  background: var(--sky, #6FB9E8);\n"
    "  border-color: var(--sky, #6FB9E8);\n"
    "  color: #0b0b0b;\n"
    "  font-weight: 600;\n"
    "}\n"
    ".afc-count {\n"
    "  margin-left: auto;\n"
    "  font-family: 'JetBrains Mono', monospace;\n"
    "  font-size: 11px;\n"
    "  color: var(--ink-3, #8a8a8a);\n"
    "}\n"
    ".afc-grid {\n"
    "  display: grid;\n"
    "  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));\n"
    "  gap: 12px;\n"
    "}\n"
    ".afc-card {\n"
    "  position: relative;\n"
    "  padding: 14px 16px;\n"
    "  background: color-mix(in srgb, var(--bg-2, #131313) 60%, transparent);\n"
    "  border: 1px solid var(--line, #2a2a2a);\n"
    "  border-left: 3px solid var(--sky, #6FB9E8);\n"
    "  border-radius: 6px;\n"
    "  cursor: pointer;\n"
    "  transition: border-color 0.15s, background 0.15s, transform 0.15s;\n"
    "}\n"
    ".afc-card:hover {\n"
    "  background: color-mix(in srgb, var(--bg-2, #131313) 90%, transparent);\n"
    "  transform: translateY(-1px);\n"
    "}\n"
    ".afc-card.hidden { display: none; }\n"
    ".afc-card.pattern-sequential { border-left-color: var(--sky, #6FB9E8); }\n"
    ".afc-card.pattern-parallel { border-left-color: var(--teal, #44B8A8); }\n"
    ".afc-card.pattern-hierarchical { border-left-color: var(--violet, #8E7AD6); }\n"
    ".afc-card.pattern-feedback-loop { border-left-color: var(--gold, #E3B657); }\n"
    ".afc-card-id {\n"
    "  font-family: 'JetBrains Mono', monospace;\n"
    "  font-size: 10px;\n"
    "  font-weight: 700;\n"
    "  letter-spacing: 0.06em;\n"
    "  color: var(--ink-3, #8a8a8a);\n"
    "  margin-bottom: 4px;\n"
    "}\n"
    ".afc-card-name {\n"
    "  font-size: 13.5px;\n"
    "  font-weight: 600;\n"
    "  color: var(--ink-0, #fff);\n"
    "  margin: 0 0 6px;\n"
    "  line-height: 1.35;\n"
    "}\n"
    ".afc-card-desc {\n"
    "  font-size: 11.5px;\n"
    "  color: var(--ink-2, #b4b4b4);\n"
    "  line-height: 1.55;\n"
    "  margin: 0 0 10px;\n"
    "}\n"
    ".afc-card-meta {\n"
    "  display: flex; flex-wrap: wrap; gap: 4px 6px;\n"
    "}\n"
    ".afc-pattern-pill,\n"
    ".afc-status-pill,\n"
    ".afc-practice-pill {\n"
    "  font-family: 'JetBrains Mono', monospace;\n"
    "  font-size: 9.5px;\n"
    "  font-weight: 700;\n"
    "  letter-spacing: 0.06em;\n"
    "  padding: 2px 7px;\n"
    "  border-radius: 3px;\n"
    "  text-transform: uppercase;\n"
    "}\n"
    ".afc-pattern-pill.pattern-sequential { background: color-mix(in srgb, var(--sky, #6FB9E8) 18%, transparent); color: var(--sky, #6FB9E8); }\n"
    ".afc-pattern-pill.pattern-parallel { background: color-mix(in srgb, var(--teal, #44B8A8) 18%, transparent); color: var(--teal, #44B8A8); }\n"
    ".afc-pattern-pill.pattern-hierarchical { background: color-mix(in srgb, var(--violet, #8E7AD6) 18%, transparent); color: var(--violet, #8E7AD6); }\n"
    ".afc-pattern-pill.pattern-feedback-loop { background: color-mix(in srgb, var(--gold, #E3B657) 18%, transparent); color: var(--gold, #E3B657); }\n"
    ".afc-status-pill.status-impl { background: color-mix(in srgb, var(--teal, #44B8A8) 22%, transparent); color: var(--teal, #44B8A8); }\n"
    ".afc-status-pill.status-manifest-only { background: color-mix(in srgb, var(--ink-3, #8a8a8a) 22%, transparent); color: var(--ink-3, #8a8a8a); }\n"
    ".afc-practice-pill {\n"
    "  background: color-mix(in srgb, var(--gold, #E3B657) 16%, transparent);\n"
    "  color: var(--gold, #E3B657);\n"
    "}\n"
    "/* Archetype modal */\n"
    ".afc-modal-backdrop {\n"
    "  position: fixed; inset: 0;\n"
    "  background: rgba(0,0,0,.6);\n"
    "  opacity: 0; pointer-events: none;\n"
    "  transition: opacity .2s ease;\n"
    "  z-index: 9998;\n"
    "}\n"
    ".afc-modal-backdrop.open { opacity: 1; pointer-events: auto; }\n"
    ".afc-modal {\n"
    "  position: fixed;\n"
    "  top: 50%; left: 50%;\n"
    "  transform: translate(-50%, -48%) scale(.96);\n"
    "  width: min(640px, 92vw);\n"
    "  max-height: 82vh;\n"
    "  background: var(--bg-1, #0b0b0b);\n"
    "  border: 1px solid var(--line, #2a2a2a);\n"
    "  border-radius: 10px;\n"
    "  box-shadow: 0 24px 80px rgba(0,0,0,.6);\n"
    "  opacity: 0; pointer-events: none;\n"
    "  transition: transform .22s cubic-bezier(.4,0,.2,1), opacity .2s ease;\n"
    "  z-index: 9999;\n"
    "  overflow: hidden;\n"
    "  display: flex; flex-direction: column;\n"
    "}\n"
    ".afc-modal.open {\n"
    "  transform: translate(-50%, -50%) scale(1);\n"
    "  opacity: 1; pointer-events: auto;\n"
    "}\n"
    ".afc-modal-close {\n"
    "  position: absolute; top: 14px; right: 16px;\n"
    "  width: 32px; height: 32px;\n"
    "  border: 1px solid color-mix(in srgb, var(--ink-3, #8a8a8a) 30%, transparent);\n"
    "  background: transparent;\n"
    "  color: var(--ink-2, #b4b4b4);\n"
    "  border-radius: 50%;\n"
    "  font-size: 18px; line-height: 1;\n"
    "  cursor: pointer;\n"
    "  z-index: 2;\n"
    "}\n"
    ".afc-modal-close:hover { background: color-mix(in srgb, var(--crimson, #D34848) 30%, transparent); color: #fff; }\n"
    ".afc-modal-body { overflow-y: auto; padding: 28px 32px 32px; flex: 1; }\n"
    ".afc-modal-eyebrow {\n"
    "  display: flex; flex-wrap: wrap; align-items: center; gap: 6px 8px;\n"
    "  margin-bottom: 10px;\n"
    "}\n"
    ".afc-modal-eyebrow code {\n"
    "  font-family: 'JetBrains Mono', monospace;\n"
    "  font-size: 11px; font-weight: 700;\n"
    "  color: var(--ink-3, #8a8a8a);\n"
    "}\n"
    ".afc-modal-title {\n"
    "  font-family: 'Fraunces', Georgia, serif;\n"
    "  font-size: 24px; font-weight: 600;\n"
    "  color: var(--ink-0, #fff);\n"
    "  margin: 0 42px 0 0;\n"
    "  line-height: 1.25;\n"
    "}\n"
    ".afc-modal-section { margin-top: 18px; }\n"
    ".afc-modal-label {\n"
    "  font-family: 'JetBrains Mono', monospace;\n"
    "  font-size: 10px; font-weight: 700;\n"
    "  letter-spacing: 0.14em; text-transform: uppercase;\n"
    "  color: var(--sky, #6FB9E8);\n"
    "  margin-bottom: 6px;\n"
    "}\n"
    ".afc-modal-desc {\n"
    "  font-size: 13.5px;\n"
    "  line-height: 1.65;\n"
    "  color: var(--ink-1, #e6edf3);\n"
    "  margin: 0;\n"
    "}\n"
    ".afc-modal-refs { display: flex; flex-wrap: wrap; gap: 4px 8px; }\n"
    ".afc-ref {\n"
    "  font-family: 'JetBrains Mono', monospace;\n"
    "  font-size: 10.5px;\n"
    "  color: var(--sky, #6FB9E8);\n"
    "  padding: 2px 6px;\n"
    "  background: color-mix(in srgb, var(--sky, #6FB9E8) 10%, transparent);\n"
    "  border-radius: 3px;\n"
    "}\n"
)


JS = r"""
<script>
/* archetypes-catalog-v1 */
(function() {
  'use strict';
  const ARCHETYPES = __ARCHETYPES_JSON__;
  const PATTERN_DESC = {
    'sequential':    'Order-dependent decisions where each agent\u2019s output becomes the next one\u2019s input. Precedence is semantic \u2014 triage, enrich, decide, act.',
    'parallel':      'Independent specialists fan out from one trigger and reconverge at a composite decision. Used when multiple concerns contribute to one verdict.',
    'hierarchical':  'A supervisor agent decomposes the task, delegates to worker children, and synthesizes the aggregate result. Natural fit for exception-handling and escalation.',
    'feedback-loop': 'Proposer \u21C4 critic iteration until a criterion or gate is met. Used for generative tasks where first-pass outputs need refinement.'
  };

  function escapeHtml(s) {
    return String(s || '').replace(/[&<>"']/g, function(c) {
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }

  function patternLabel(p) {
    return p === 'feedback-loop' ? 'Feedback' :
           (p.charAt(0).toUpperCase() + p.slice(1));
  }

  function renderGrid() {
    const grid = document.getElementById('afcGrid');
    if (!grid) return;
    grid.innerHTML = ARCHETYPES.map(function(a) {
      return (
        '<div class="afc-card pattern-' + escapeHtml(a.pattern) + '" ' +
             'data-pattern="' + escapeHtml(a.pattern) + '" ' +
             'data-status="'  + escapeHtml(a.status)  + '" ' +
             'data-practice="' + escapeHtml(a.practice) + '" ' +
             'data-archetype-id="' + escapeHtml(a.id) + '">' +
          '<div class="afc-card-id">' + escapeHtml(a.id) + '</div>' +
          '<h4 class="afc-card-name">' + escapeHtml(a.name) + '</h4>' +
          '<p class="afc-card-desc">' + escapeHtml(a.desc) + '</p>' +
          '<div class="afc-card-meta">' +
            '<span class="afc-pattern-pill pattern-' + escapeHtml(a.pattern) + '">' + escapeHtml(patternLabel(a.pattern)) + '</span>' +
            '<span class="afc-status-pill status-' + escapeHtml(a.status) + '">' + (a.status === 'impl' ? 'Implemented' : 'Manifest') + '</span>' +
            '<span class="afc-practice-pill">' + escapeHtml(a.practice) + '</span>' +
          '</div>' +
        '</div>'
      );
    }).join('');
    updateCount();
  }

  function state() {
    const getActive = function(sel) {
      const btn = document.querySelector('[data-filter-' + sel + '].active');
      return btn ? btn.getAttribute('data-filter-' + sel) : 'all';
    };
    return {
      pattern:  getActive('pattern'),
      status:   getActive('status'),
      practice: getActive('practice'),
    };
  }

  function applyFilters() {
    const s = state();
    let shown = 0;
    document.querySelectorAll('.afc-card').forEach(function(card) {
      const p = card.getAttribute('data-pattern');
      const st = card.getAttribute('data-status');
      const pr = card.getAttribute('data-practice');
      const ok = (s.pattern === 'all' || p === s.pattern) &&
                 (s.status === 'all' || st === s.status) &&
                 (s.practice === 'all' || pr === s.practice);
      card.classList.toggle('hidden', !ok);
      if (ok) shown++;
    });
    updateCount(shown);
  }

  function updateCount(shown) {
    const el = document.getElementById('afcCount');
    if (!el) return;
    const total = ARCHETYPES.length;
    if (shown === undefined) shown = total;
    el.textContent = shown + ' of ' + total;
  }

  function openArchetypeModal(id) {
    const a = ARCHETYPES.find(function(x) { return x.id === id; });
    if (!a) return;
    document.getElementById('afcModalId').textContent = a.id;
    const pat = document.getElementById('afcModalPattern');
    pat.textContent = patternLabel(a.pattern);
    pat.className = 'afc-pattern-pill pattern-' + a.pattern;
    const st = document.getElementById('afcModalStatus');
    st.textContent = a.status === 'impl' ? 'Implemented' : 'Manifest only';
    st.className = 'afc-status-pill status-' + a.status;
    document.getElementById('afcModalPractice').textContent = a.practice;
    document.getElementById('afcModalTitle').textContent = a.name;
    document.getElementById('afcModalDesc').textContent = a.desc;
    document.getElementById('afcModalPatternDesc').textContent = PATTERN_DESC[a.pattern] || '';
    document.getElementById('afcModal').classList.add('open');
    document.getElementById('afcModalBackdrop').classList.add('open');
    document.getElementById('afcModal').setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    document.querySelector('#afcModal .afc-modal-body').scrollTop = 0;
  }

  function closeArchetypeModal() {
    document.getElementById('afcModal').classList.remove('open');
    document.getElementById('afcModalBackdrop').classList.remove('open');
    document.getElementById('afcModal').setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  window.openArchetypeModal = openArchetypeModal;
  window.closeArchetypeModal = closeArchetypeModal;

  function init() {
    renderGrid();
    // Filter chip handlers (single-select per group)
    ['pattern', 'status', 'practice'].forEach(function(grp) {
      document.querySelectorAll('[data-filter-' + grp + ']').forEach(function(btn) {
        btn.addEventListener('click', function() {
          document.querySelectorAll('[data-filter-' + grp + ']').forEach(function(b) {
            b.classList.remove('active');
          });
          btn.classList.add('active');
          applyFilters();
        });
      });
    });
    // Card click -> modal
    document.addEventListener('click', function(e) {
      const card = e.target.closest('.afc-card');
      if (!card) return;
      const id = card.getAttribute('data-archetype-id');
      if (id) openArchetypeModal(id);
    });
    // ESC closes
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') closeArchetypeModal();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>
"""

JS = JS.replace("__ARCHETYPES_JSON__", archetypes_js)


# ---- 3. Insert the HTML fragment into the Reasoning page -------------------
# Find the end of the 4-primitive archetype-grid and insert right after.

# Locate the closing of the archetype-grid we already have
insertion_marker = (
    '<div class="archetype">\n        <h4>Feedback</h4>'
)
idx = html.find(insertion_marker)
if idx < 0:
    # alt formatting
    idx = html.find('<div class="archetype">\n        <h4>Feedback</h4>')
if idx < 0:
    print("ERROR: couldn't find Feedback archetype div")
    sys.exit(1)

# Walk forward to the closing </div> of the archetype-grid (it ends with
# </div>\n    </div>\n  </div> pattern — need to be careful)
# Strategy: find "</div>\n    </div>" after the Feedback block
scan_from = idx
depth = 1
pos = html.find('</div>', scan_from + 40)
# Instead just find the closing </div>\n    </div> that ends archetype-grid
# We know the structure: <div class="archetype-grid">...</div> then next sibling
# Let me search for archetype-grid close
grid_close_re = re.compile(r'</div>\s*</div>\s*(?:</div>)?\s*(?:<|$)', re.DOTALL)
# Safer: search for the END of the archetype-grid block — after all 4 archetype cards
# The Feedback archetype ends with its own </div>. The grid wraps them. Then the deep-section continues or ends.
# Let me find the specific pattern: Feedback </p> ... </div>\n    </div>
fb_section = html.find(insertion_marker)
# Find the </div></div> that closes the archetype-grid after the Feedback card
close_grid = html.find('</div>\n    </div>', fb_section)
if close_grid < 0:
    close_grid = html.find('</div>\n      </div>', fb_section)
if close_grid < 0:
    print("ERROR: couldn't find archetype-grid close")
    sys.exit(1)

# Insert our new HTML between the grid close and whatever comes after
# The </div>\n    </div> we found closes the last archetype card AND the archetype-grid
insertion_point = close_grid + len('</div>\n    </div>')

html = html[:insertion_point] + "\n" + INJECTED_HTML + html[insertion_point:]
print(f"Inserted archetype catalog HTML at byte {insertion_point}")


# ---- 4. Inject CSS + JS ----------------------------------------------------
close_style = html.find("</style>")
if close_style != -1:
    html = html[:close_style] + CSS + html[close_style:]
    print("Injected CSS")

close_body = html.rfind("</body>")
if close_body != -1:
    html = html[:close_body] + JS + html[close_body:]
    print("Injected JS")

HTML.write_text(html, encoding="utf-8")
print(f"\nWrote {HTML}")
