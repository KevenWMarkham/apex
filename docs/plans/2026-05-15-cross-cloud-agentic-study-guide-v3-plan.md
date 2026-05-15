# Cross-Cloud Agentic Study Guide v3 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Turn the study guide into a working seller tool — a per-episode interactive Client Axis View (axis selectors → Microsoft-attachment likelihood bar → seller actions), a keyword deep-dive treeview with detail modals and saved notes, and a multi-client manager — all in the one HTML file.

**Architecture:** Three new inline build-time JS data objects (`EP_AXES`, `EP_ACTIONS`, `EP_KEYWORDS`) beside the existing `EP_CUES`. A localStorage-backed multi-client store (one JSON key) scopes all engagement state to an active client. Vanilla JS renders 5-point axis selectors onto the existing `.paq` questions, computes a weighted likelihood, extends the v2 player topic list into a keyword treeview with a modal, and collects saved notes in a new tab. The v2 audio player / cue behavior and the APEX opt-in `<details>` are untouched.

**Tech Stack:** Single self-contained HTML · inline CSS + vanilla JS · no libraries · Python 3 + `node --check` for verification.

**Design doc:** `docs/plans/2026-05-15-cross-cloud-agentic-study-guide-v3-design.md` — refer to it for the data model, the four parts, and constraints.

**Target file:** `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic\Cross-Cloud-Agentic-Study-Guide.html` (~236 KB after v2, 9 tabs, 8 episode panels).

## Notes for the executor

- **Order matters.** Every task modifies the same HTML file — run strictly sequentially, never in parallel. CSS (T1) before markup/JS that uses it. Data (T2) before the embed (T3). The client store (T4) before Parts A/B/C (T5–T7) because they scope state to the active client.
- **Every Edit needs a unique `old_string`** — the file is large; episode panels are distinguished by `<h2>` titles and first vocabulary `<dt>` terms.
- **Do not disturb** the v2 audio player (`playerInit`, `EP_CUES`), the APEX `<details>`, the existing `paqInit` checklist beyond the extensions this plan specifies, or the print stylesheet.
- **APEX stays opt-in** — no APEX name on the always-visible surface.
- **Vanilla JS only.** After any JS change, the script must pass `node --check`.

---

## Task 1: v3 CSS block

**Files:**
- Modify: `Cross-Cloud-Agentic-Study-Guide.html` — the `<style>` block

**Step 1: Add the CSS**

Insert a new CSS block immediately before the `footer{` rule (after the v2 `.apex-name` media query, before `footer{`). Comment header: `/* ===== study guide v3: axis view · keywords · notes · clients ===== */`. It must define rules for:

- **Axis selector** — `.axis-sel` (a flex row of 5 segments), `.axis-seg` (one segment: bordered pill, `cursor:pointer`, mono micro-label), `.axis-seg:hover`, `.axis-seg.on` (selected: `background:var(--purple-bg)`, `border-color:var(--purple-dim)`, `color:var(--ink)`), `.axis-seg.ms` (a small marker on the Microsoft-favorable end — e.g. a teal underline/dot). `.axis-sel-labels` (the two pole captions under the strip, space-between, `font-size:11px`, `color:var(--ink-3)`).
- **Likelihood bar** — `.lk` (container card), `.lk-head` (flex: title + the `n of m answered` meta), `.lk-bar` (reuse `.cc-bar` height/border — track), `.lk-fill` (gradient fill, `transition:width .3s ease`), `.lk-band` (the `LIKELY/CONTESTED/OPEN/UNLIKELY` chip — mono uppercase pill; modifiers `.lk-band.likely` teal, `.contested` amber, `.open` purple, `.unlikely` crimson — reuse the `cc-pivot-str` color pattern), `.lk-reason` (the generated sentence, `font-size:13px`, `color:var(--ink-2)`).
- **Seller actions** — reuse `.godeep`/`.gd-body` for the collapsed block (add `.actions` body wrapper if needed); `.act-item` (a row: checkbox + label + detail), `.act-item .act-cb` (accent-color amber, like `.paq-cb`), `.act-label` (weight 600), `.act-detail` (`font-size:12.5px`, `color:var(--ink-3)`), `.act-axis` (mono micro-tag naming the axis), `.act-item.hot` (emphasized — `border-left:3px solid var(--amber)`, `background:var(--amber-bg)`).
- **Keyword treeview** (extends the v2 `.np-list`) — `.np-item.has-kw` (section row that has keywords — shows a disclosure triangle via `::before`, `content:"\25B8"`, rotates when `.np-item.open`), `.kw-children` (the indented child container — `display:none`, shown when parent has `.open`), `.kw-node` (one keyword: indented row, `cursor:pointer`, small dot bullet, `font-size:12.5px`, hover brightens).
- **Modal** — `.modal-overlay` (`position:fixed;inset:0`, dim backdrop `background:rgba(0,0,0,.6)`, `display:none`, flex-center, `z-index:200`; `.modal-overlay.open{display:flex}`), `.modal` (the dialog card — `var(--surface)`, border, `border-radius:14px`, `max-width:520px`, `padding:24px 26px`, `max-height:80vh`, `overflow:auto`), `.modal-close` (top-right × button), `.modal-kw` (the term — Fraunces, ~22px), `.modal-def` / `.modal-why` (body text; `.modal-why` tinted with `--teal-bg` left-border callout), `.modal-links` (link list), `.modal-save` (the Save-to-Notes button — house button style, amber).
- **My Notes tab** — `.notes-empty` (centered muted placeholder), `.note-card` (bordered card: `var(--surface)`, `border-radius:10px`, padding), `.note-kw` (term, weight 600), `.note-meta` (mono micro: episode + date), `.note-detail` (the saved detail text), `.note-user` (a `<textarea>` for the seller's words — full width, house-styled, `min-height:60px`), `.note-del` (small delete button), `.notes-toolbar` (copy-all / clear-all buttons row).
- **Client manager** — `.client-pick` (the nav control — a flex group), `.client-pick select` (house-styled `<select>`), `.client-add` (small `＋` button); `.cprofile` (the Overview Client Profile section card), `.cprofile-grid` (label/field grid), `.cprofile input`, `.cprofile textarea` (house-styled form fields — `background:var(--bg-1)`, border, `color:var(--ink)`), `.cprofile-actions` (add/rename/delete/export/import button row), `.cbtn` (shared small button style for these).

Keep within existing house variables (`--bg`, `--surface`, `--border`, `--ink*`, `--teal`, `--purple`, `--amber`, `--crimson`, `--apex-*`). Add a `@media print` rule hiding `.modal-overlay`, `.client-pick`, `.axis-sel` if needed (the print stylesheet isolates the note card — keep v3 controls out of print).

**Step 2: Verify CSS parses**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python -c "
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
css=html.split('<style>')[1].split('</style>')[0]
assert css.count('{')==css.count('}'), 'CSS brace imbalance'
for cls in ['.axis-sel','.axis-seg','.lk-fill','.lk-band','.act-item','.kw-node','.modal-overlay','.modal','.note-card','.client-pick','.cprofile']:
    assert cls in css, f'missing {cls}'
print('v3 CSS present, braces balanced')
"
```

**Step 3: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/Cross-Cloud-Agentic-Study-Guide.html
git commit -m "feat: study guide v3 — axis view / keywords / notes / clients CSS"
```

---

## Task 2: Curate the v3 build data (controller-prep, no commit)

**Files:**
- Reference only: the existing `.paq` questions in the HTML; the episode Content Breakdowns; `EP_CUES`; the Vocabulary sections.

This task produces three JS object literals held by the controller and embedded in Task 3. No file is written and nothing is committed — it is a preparation task, exactly like v2's cue-curation task.

**Step 1: Build `EP_AXES`**

Read every `.paq` question in all 8 episode panels (section ③). For each, create a descriptor:

```js
{ id:"e2-ax1", label:"<short axis name>",
  poleA:"<left pole text>", poleB:"<right pole text>",
  msPole:"A"|"B",          // the pole that makes a Microsoft-composed path more likely
  weight:1,                 // 1 default; 2 for an axis that strongly drives the recommendation
  baseline:"<the existing BASELINES text>" }
```

`id` = `<panelId>-ax<k>` in document order. `poleA`/`poleB` come from the existing AXIS poles. `msPole` is a judgement: which pole favors composing with Microsoft (e.g. for "bulk replication ↔ federation & mirroring", the federation/mirroring pole is Microsoft-favorable because it is Fabric's productized strength). `weight` is 1 unless the axis is the episode's central decision (then 2).

**Step 2: Build `EP_ACTIONS`**

For each episode, curate 3–6 seller actions — concrete next steps that move the client toward a Microsoft attachment:

```js
{ id:"e2-act1", axis:"e2-ax1", triggerPole:"A",
  label:"<imperative action>",
  detail:"<1–2 sentences: the why, the proof to bring>" }
```

`axis` references an `EP_AXES` id; `triggerPole` is the non-Microsoft pole whose selection makes this action "hot". Draw the actions from the episode's content (the disagreement, the carry-forward, the Cloud Comparison pivot).

**Step 3: Build `EP_KEYWORDS`**

For each episode, keyed by section index (the index into `EP_CUES[ep]`), curate 2–5 deep-dive keywords for that section:

```js
"e2": { "1":[ {term:"Medallion architecture",
               def:"<crisp definition>",
               why:"<why it matters in the deal>",
               links:[{label:"OneLake docs",url:"https://learn.microsoft.com/fabric/onelake/"}]} ], ... }
```

Fold in the episode's Vocabulary (section ⑥) terms where they map to a section. Keys are strings of the `EP_CUES` section index. Sections with no keywords may be omitted.

**Step 4: Hold the three objects** for Task 3. (No commit.)

---

## Task 3: Embed the data objects + annotate the `.paq` markup

**Files:**
- Modify: `Cross-Cloud-Agentic-Study-Guide.html` — `<script>` block + the 8 episode `.paq` blocks

**Step 1: Embed `EP_AXES`, `EP_ACTIONS`, `EP_KEYWORDS`**

Insert the three curated objects (from Task 2) into the `<script>` block immediately after the `EP_CUES` object literal. Each as `const EP_AXES = {...};` etc.

**Step 2: Annotate every `.paq`**

For each `.paq` question div, add three data attributes carrying its axis identity: `data-axis="<id>"`, `data-ms-pole="A|B"`, `data-axis-weight="<n>"`. Anchor each Edit on the question's unique `.pq` text. The attributes let the JS bind a selector to each rendered question without re-parsing prose.

**Step 3: Verify**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python -c "
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
for o in ['EP_AXES','EP_ACTIONS','EP_KEYWORDS']:
    assert ('const '+o) in html, f'missing {o}'
n_axes=html.count('data-axis=')
n_paq=html.count('class=\"paq\"')
assert n_axes==n_paq, f'paq/data-axis mismatch {n_paq}/{n_axes}'
js=html.split('<script>')[1].split('</script>')[0]
open('_sgcheck.js','w',encoding='utf-8').write(js)
print(f'data objects embedded; {n_paq} .paq annotated')
"
node --check _sgcheck.js && echo "JS OK" && rm _sgcheck.js
```

**Step 4: Commit**

```bash
git commit -am "feat: study guide v3 — embed EP_AXES/EP_ACTIONS/EP_KEYWORDS + annotate axes"
```

---

## Task 4: Multi-client store + client manager

**Files:**
- Modify: `Cross-Cloud-Agentic-Study-Guide.html` — nav markup, Overview panel, `<script>` block

**Step 1: Add the client store accessor JS**

Append to the `<script>` block (after the data objects, before `paqInit()`):

```js
/* ---- v3 multi-client store (one localStorage JSON) ---- */
const SG3_KEY='ccap-study-guide-v3';
function sg3Blank(){
  return {schema:3,activeClientId:'general',clients:{
    general:sg3NewClient('general','General (no client)')}};
}
function sg3NewClient(id,name){
  return {id,name,profile:{industry:'',clouds:'',aiMaturity:'',signals:''},
          axes:{},paq:{},actions:{},notes:[]};
}
function sg3Load(){
  let s;
  try{s=JSON.parse(localStorage.getItem(SG3_KEY));}catch(e){s=null;}
  if(!s||s.schema!==3||!s.clients||!s.clients.general) s=sg3Blank();
  // one-time migration of the v2 checklist into general.paq
  try{
    const v2=JSON.parse(localStorage.getItem('ccap-study-guide-checklist-v1')||'null');
    if(v2&&!s.clients.general._migrated){
      Object.assign(s.clients.general.paq,v2);
      s.clients.general._migrated=true;
    }
  }catch(e){}
  return s;
}
function sg3Save(s){ try{localStorage.setItem(SG3_KEY,JSON.stringify(s));}catch(e){} }
let SG3=sg3Load();
function sg3Active(){ return SG3.clients[SG3.activeClientId]||SG3.clients.general; }
```

**Step 2: Add the nav client selector markup**

In the sticky top nav, add a `.client-pick` group — a `<select id="clientSelect">` and a `<button class="client-add">＋</button>`. Anchor on the existing theme-toggle button; place `.client-pick` beside it.

**Step 3: Add the Client Profile section to the Overview tab**

Insert a new `.ov-section` (after the APEX stack section, before `</section>` of the Overview panel) — `<h3>Client profile</h3>`, intro `<p>`, then a `.cprofile` card with: a `.cprofile-grid` of labelled fields (`industry`, `clouds`, `aiMaturity` as `<input>`s; `signals` as `<textarea>`), and a `.cprofile-actions` row of buttons: Add client · Rename · Delete · Export all · Import.

**Step 4: Add the client-manager JS**

Append `clientInit()`:
- populates `#clientSelect` from `SG3.clients`, selects `activeClientId`
- on select change → set `SG3.activeClientId`, `sg3Save`, `hydrateClient()`
- `＋` / Add → `prompt` for a name → create via `sg3NewClient` with a generated id → save → re-render select → switch to it
- Rename → `prompt`, update name. Delete → confirm, remove (block deleting `general`), fall back to `general`.
- Profile fields → on `input`, write into `sg3Active().profile`, `sg3Save`
- Export → build a Blob of `JSON.stringify(SG3,null,2)`, trigger a download `study-guide-clients.json`
- Import → a hidden `<input type="file">`; on change, parse JSON, merge `clients`, save, re-render
- Define a `hydrateClient()` stub that re-reads `sg3Active()` and refreshes the profile fields and the select label (Tasks 5–7 extend it to refresh axes, checkboxes, notes).

Call `clientInit()` at the end of the script.

**Step 5: Verify**

```bash
python -c "
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
for s in ['SG3_KEY','sg3Load','clientInit','hydrateClient','clientSelect','cprofile']:
    assert s in html, f'missing {s}'
js=html.split('<script>')[1].split('</script>')[0]
open('_sgcheck.js','w',encoding='utf-8').write(js)
print('client store + manager present')
"
node --check _sgcheck.js && echo "JS OK" && rm _sgcheck.js
```

**Step 6: Commit**

```bash
git commit -am "feat: study guide v3 — multi-client store + client manager"
```

---

## Task 5: Part A — axis selectors, likelihood bar, seller actions

**Files:**
- Modify: `Cross-Cloud-Agentic-Study-Guide.html` — the 8 `.paq-details` blocks + `<script>` block

**Step 1: Add the likelihood bar + seller-actions markup**

For each episode, inside section ③ after the `.paq-list`, insert: a `.lk` card (head with title + `.lk-meta`, a `.lk-bar`>`.lk-fill`, a `.lk-band`, a `.lk-reason`) and a collapsed `<details class="godeep">` titled "Actions to shift the tide toward Microsoft" with an empty `.actions` body. Both are populated by JS. Use a `data-ep` on the `.lk` and the actions block.

**Step 2: Add the Part A JS**

Append:
- `axisInit()` — for every `.paq` with `data-axis`, build a `.axis-sel` of 5 `.axis-seg` segments (`Strongly A · Leans A · Neutral · Leans B · Strongly B`), mark the segment nearest the `data-ms-pole` end with `.ms`, append the `.axis-sel-labels` (poleA / poleB). On segment click → set `.on`, write position `0..4` into `sg3Active().axes[ep][axisId]`, `sg3Save()`, call `recalcLikelihood(ep)`.
- `axisScore(ep,axisId,pos)` — convert a `0..4` position to a `0..1` Microsoft-favorability: if `msPole==="B"` score is `pos/4`, else `(4-pos)/4`.
- `recalcLikelihood(ep)` — over the episode's answered axes, `pct = 100 * Σ(weight·score) / Σ(weight)`; set `.lk-fill` width, the `.lk-band` class+text by threshold (`≥67 likely · ≥45 contested · ≥25 open · else unlikely`; if 0 answered → "OPEN", reason "No axes answered yet."), the `.lk-meta` `n of m axes answered`, and the `.lk-reason` naming the strongest supporting and the strongest opposing axis by `label`. Then refresh seller-action emphasis.
- `actionsRender(ep)` — fill the actions `<details>` body from `EP_ACTIONS[ep]`: one `.act-item` each (checkbox bound to `sg3Active().actions[id]`, label, detail, `.act-axis` tag). Add `.hot` when the client's current position on `action.axis` is on the `triggerPole` side (or unanswered). Checkbox change → write to `actions`, save.
- Extend `hydrateClient()` to re-apply `axes` (segment `.on` states), `paq` (existing checkboxes — already keyed), `actions` (checkboxes) for the active client, then call `recalcLikelihood` for all 8 episodes.

Call `axisInit()` then `recalcLikelihood` for each episode at script end.

**Step 3: Verify**

```bash
python -c "
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
assert html.count('class=\"lk\"')==8, 'expected 8 likelihood bars'
for s in ['axisInit','recalcLikelihood','axisScore','actionsRender']:
    assert s in html, f'missing {s}'
js=html.split('<script>')[1].split('</script>')[0]
assert js.count('{')==js.count('}') and js.count('(')==js.count(')'), 'JS imbalance'
open('_sgcheck.js','w',encoding='utf-8').write(js); print('Part A present')
"
node --check _sgcheck.js && echo "JS OK" && rm _sgcheck.js
```

**Step 4: Commit**

```bash
git commit -am "feat: study guide v3 — axis selectors + likelihood bar + seller actions"
```

---

## Task 6: Part B — keyword treeview + detail modal

**Files:**
- Modify: `Cross-Cloud-Agentic-Study-Guide.html` — `<script>` block + one modal markup block

**Step 1: Add the modal markup**

Add one shared modal at the end of `<main>` (or before `<footer>`): `<div class="modal-overlay" id="kwModal"><div class="modal">…</div></div>` with a close ×, and empty `.modal-kw` / `.modal-def` / `.modal-why` / `.modal-links` containers and a `.modal-save` button.

**Step 2: Add the Part B JS**

Append:
- `keywordTreeInit()` — runs after `playerInit()`. For each player's `.np-list`, for each section row whose `EP_CUES` index has an `EP_KEYWORDS[ep]` entry: add `.has-kw`, append a `.kw-children` container with a `.kw-node` per keyword; clicking the row toggles `.open`; clicking a `.kw-node` calls `openKeywordModal(ep,kwObj)` (stop propagation).
- `openKeywordModal(ep,kw)` — fill `#kwModal` fields + links, store the current `{ep,kw}` on the modal, add `.open`, focus the close button, trap `Tab`, close on `Esc` / backdrop / ×.
- `.modal-save` click → push `{id,kw:kw.term,ep,detail:kw.def+' — '+kw.why,userText:'',ts:Date.now()}` into `sg3Active().notes`, `sg3Save()`, re-render the Notes tab (Task 7's `renderNotes()`), brief "Saved" confirmation, keep modal open.

Call `keywordTreeInit()` after `playerInit()`.

**Step 3: Verify**

```bash
python -c "
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
assert html.count('id=\"kwModal\"')==1
for s in ['keywordTreeInit','openKeywordModal']:
    assert s in html, f'missing {s}'
js=html.split('<script>')[1].split('</script>')[0]
open('_sgcheck.js','w',encoding='utf-8').write(js); print('Part B present')
"
node --check _sgcheck.js && echo "JS OK" && rm _sgcheck.js
```

**Step 4: Commit**

```bash
git commit -am "feat: study guide v3 — keyword treeview + detail modal"
```

---

## Task 7: Part C — My Notes tab

**Files:**
- Modify: `Cross-Cloud-Agentic-Study-Guide.html` — tab bar, a new panel, `<script>` block

**Step 1: Add the tab + panel**

Add a `<button class="tab" data-panel="notes">` to the tab bar (after the e8 tab) and a `<section class="panel" id="notes">` with an `.ep-head` ("My Notes"), an intro `<p>`, a `.notes-toolbar` (Copy all · Clear all), and an empty `#notesList` container.

**Step 2: Add the Part C JS**

Append:
- `renderNotes()` — empty `#notesList`; if `sg3Active().notes` is empty show `.notes-empty`; else one `.note-card` per note (term, `.note-meta` episode+date, `.note-detail`, a `.note-user` `<textarea>` bound to `note.userText` saving on `input`, a `.note-del`). Delete → splice, save, re-render.
- Copy all → join notes to text, `navigator.clipboard.writeText`. Clear all → confirm, empty `notes`, save, re-render.
- Extend `hydrateClient()` to call `renderNotes()`.

Call `renderNotes()` at script end.

**Step 3: Verify**

```bash
python -c "
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
assert html.count('data-panel=\"notes\"')==1
assert html.count('id=\"notes\"')==1
assert 'renderNotes' in html
js=html.split('<script>')[1].split('</script>')[0]
open('_sgcheck.js','w',encoding='utf-8').write(js); print('Part C present')
"
node --check _sgcheck.js && echo "JS OK" && rm _sgcheck.js
```

**Step 4: Commit**

```bash
git commit -am "feat: study guide v3 — My Notes tab"
```

---

## Task 8: Final verification

**Files:**
- Verify only: `Cross-Cloud-Agentic-Study-Guide.html`

**Step 1: Structural + discipline verification**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python -c "
import sys; sys.stdout.reconfigure(encoding='utf-8')
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
print(f'size: {len(html.encode())//1024} KB')
assert html.count('<section class=\"panel')==10, 'expected 10 panels'
assert html.count('class=\"player\"')==8
assert html.count('class=\"lk\"')==8
assert html.count('id=\"kwModal\"')==1
for o in ['EP_CUES','EP_AXES','EP_ACTIONS','EP_KEYWORDS','SG3_KEY']:
    assert o in html, f'missing {o}'
for tag in ['div','section','details','script','style','audio','ul','textarea']:
    assert html.count(f'<{tag}')==html.count(f'</{tag}>'), f'{tag} imbalance'
js=html.split('<script>')[1].split('</script>')[0]
assert js.count('{')==js.count('}') and js.count('(')==js.count(')'), 'JS imbalance'
open('_sgcheck.js','w',encoding='utf-8').write(js)
# APEX still opt-in
hero=html.split('<header')[1].split('</header>')[0]
assert 'APEX' not in hero, 'APEX leaked into hero'
# content discipline
for t in ['co-sell','strategic partnership','channel partner']:
    assert t.lower() not in html.lower(), f'forbidden {t}'
print('structure OK; tags + JS balanced; APEX opt-in intact; discipline clean')
"
node --check _sgcheck.js && echo "JS SYNTAX OK" && rm _sgcheck.js
```

**Step 2: Browser smoke-test (manual)**

Open the HTML: add a client and switch to it; on an episode tab, move axis selectors and confirm the likelihood bar + reason update and matching actions go `.hot`; expand a timeline section, click a keyword, confirm the modal opens and "Save to Notes" lands a card in My Notes; switch clients and confirm axes/notes re-hydrate; export the JSON and confirm it is valid.

**Step 3: Commit (if fixes were needed)**

```bash
git commit -am "fix: study guide v3 verification fixes" || echo "no fixes needed"
```

---

**End of plan.** 8 tasks. Estimated effort: ~3-4 hours (CSS + data curation + 5 markup/JS passes + verification).
