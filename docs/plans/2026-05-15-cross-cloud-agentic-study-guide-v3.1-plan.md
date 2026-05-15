# Cross-Cloud Agentic Study Guide v3.1 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a new per-episode section ⑦ "Win the Deal" — a How-to-say-it / How-to-position-it talk-track plus a References & follow-up list of the episode's cited references as curated authoritative links, each saveable into My Notes.

**Architecture:** Two new inline build-time JS data objects (`EP_POSITIONING`, `EP_REFS`) beside the existing v3 objects. A new visible `.block` (section ⑦) appended to each of the 8 episode panels after ⑥ Vocabulary, filled at runtime by a `winDealInit()` function. The references' "Save to My Notes" reuses the v3 multi-client notes store; `renderNotes()` gains a small tweak so a URL inside a note renders as a link.

**Tech Stack:** Single self-contained HTML · inline CSS + vanilla JS · no libraries · Python 3 + `node --check` for verification.

**Design doc:** `docs/plans/2026-05-15-cross-cloud-agentic-study-guide-v3.1-design.md`.

**Target file:** `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic\Cross-Cloud-Agentic-Study-Guide.html` (~322 KB after v3, 10 tabs, 8 episode panels each with sections ①–⑥).

## Notes for the executor

- Every task modifies the same HTML file — run strictly sequentially. CSS (T1) before markup/JS. Data (T2) before embed (T3).
- Every Edit needs a unique `old_string` — anchor on episode-unique text (episode `<h2>` titles, last Vocabulary `<dt>` terms).
- Do not disturb the v3 axis view, keyword modal, multi-client store, the APEX `<details>`, or the v2 player.
- Vanilla JS only; after any JS change the script must pass `node --check`.
- Commit each task with `git add <path>` then `git commit` — never `git commit -a`.

---

## Task 1: v3.1 CSS block

**Files:**
- Modify: `Cross-Cloud-Agentic-Study-Guide.html` — the `<style>` block

**Step 1: Add the CSS**

Insert a new CSS block immediately before the `footer{` rule (after the v3 print `@media` rule that ends the v3 block). Comment header: `/* ===== study guide v3.1: Win the Deal ===== */`. Define:

- `.wtd` — section wrapper: flex column, `gap:16px`, `margin-top:4px`.
- `.wtd-h` — sub-heading: `"Instrument Sans"`, `font-weight:600`, `font-size:13px`, `color:var(--ink)`, `text-transform:uppercase`, `letter-spacing:.05em`.
- `.say-list` — flex column, `gap:10px`.
- `.say-card` — paired card: `border:1px solid var(--border)`, `border-left:3px solid var(--gold-dim)`, `border-radius:9px`, `background:var(--surface)`, `padding:13px 16px`.
- `.say-it` — the verbatim line: `font-family:"Fraunces",serif`, `font-size:16px`, `line-height:1.45`, `color:var(--ink)`. Prefix it with an open-quote feel via `.say-it::before{content:"\201C";color:var(--gold)}` and `.say-it::after{content:"\201D";color:var(--gold)}`.
- `.position-it` — supporting line: `font-size:13px`, `line-height:1.55`, `color:var(--ink-2)`, `margin-top:7px`. Give it a leading mono tag via a child or `::before` — define `.position-it .pos-tag{font-family:"JetBrains Mono",monospace;font-size:9.5px;letter-spacing:.07em;color:var(--gold);margin-right:8px}`.
- `.ref-list` — flex column, `gap:14px`.
- `.ref-group` — one category group: flex column, `gap:6px`.
- `.ref-cat` — category heading: `font-family:"JetBrains Mono",monospace`, `font-size:10px`, `letter-spacing:.09em`, `text-transform:uppercase`, `color:var(--purple)`.
- `.ref-row` — `display:flex`, `align-items:flex-start`, `gap:12px`, `padding:9px 12px`, `border:1px solid var(--border)`, `border-radius:8px`, `background:var(--surface)`.
- `.ref-row > div` — `flex:1` (the text column).
- `.ref-link` — the `<a>`: `color:var(--purple)`, `font-weight:600`, `font-size:13.5px`, `text-decoration:none`; `.ref-link::after{content:" \2197";font-size:11px}`; hover underline.
- `.ref-note` — `display:block`, `font-size:12px`, `color:var(--ink-3)`, `margin-top:2px`.
- `.ref-save` — small button: `flex:none`, `background:var(--surface-2)`, `border:1px solid var(--border)`, `color:var(--ink-2)`, `font-family:"JetBrains Mono",monospace`, `font-size:9.5px`, `letter-spacing:.03em`, `padding:6px 10px`, `border-radius:6px`, `cursor:pointer`, `transition:all .15s ease`; hover `color:var(--ink);border-color:var(--border-2)`.
- Append a `@media print{.wtd,.ref-save{}}` only if needed — otherwise omit (section ⑦ is screen-only; the existing print rule isolates the Note Card).

Use only existing house variables. Do not redefine anything.

**Step 2: Verify**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python -c "
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
css=html.split('<style>')[1].split('</style>')[0]
assert css.count('{')==css.count('}'), 'CSS brace imbalance'
for cls in ['.wtd','.say-card','.say-it','.position-it','.ref-row','.ref-link','.ref-save','.ref-cat']:
    assert cls in css, f'missing {cls}'
print('v3.1 CSS present, braces balanced')
"
```

**Step 3: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/Cross-Cloud-Agentic-Study-Guide.html
git commit -m "feat: study guide v3.1 — Win the Deal CSS"
```

---

## Task 2: Curate `EP_POSITIONING` + `EP_REFS` (controller-prep, no commit)

**Files:**
- Reference: the 8 episode scripts `01-*.md` … `08-*.md` (their `## Further reading` sections); the episode panels in the HTML (Content Breakdown, the Cloud Comparison pivot, the carry-forward).

Produces two JS object literals held for Task 3. No file committed.

**Step 1: Build `EP_POSITIONING`**

Per episode, an array of **3–4** `{say, position}` entries:
- `say` — a short verbatim line (10–25 words) the seller can say in the room.
- `position` — 1–2 sentences: the strategic move behind the line and why it lands.
Draw from each episode's pivot, disagreement resolution, and carry-forward. Generic seller language; "the Acceleration Framework"; no forbidden vocabulary; no client names.

**Step 2: Build `EP_REFS`**

For each episode, read its `## Further reading` section in the `.md` script. Produce an array of `{category, label, url, note}`:
- `category` — the sub-heading group (e.g. `Analyst`, `Standards`, `Microsoft`, `AWS`, `Google Cloud`, `Independence`). Normalise to a short title-case label.
- `label` — the reference name.
- `note` — a one-line descriptor (condense the script's dash-text).
- `url` — a real authoritative URL: use the script's URL where present; otherwise curate a stable hub URL — Microsoft Learn (`https://learn.microsoft.com/...`), AWS docs (`https://docs.aws.amazon.com/` or the product page), Google Cloud docs (`https://cloud.google.com/...`), `https://www.nist.gov/itl/ai-risk-management-framework`, the EU AI Act (`https://artificial-intelligence-act.eu/`), analyst firms' public pages (gartner.com, forrester.com, mckinsey.com, idc.com). Every entry MUST have a non-empty `url`. Omit internal cross-references that have no public URL (e.g. "Episode 1", "Trilogy Services Ep 3") — these are not external references.

**Step 3: Hold both objects** for Task 3 (no commit).

---

## Task 3: Embed the data + insert the 8 section-⑦ blocks

**Files:**
- Modify: `Cross-Cloud-Agentic-Study-Guide.html` — `<script>` block + the 8 episode panels

**Step 1: Embed the data objects**

Insert `const EP_POSITIONING = {...};` and `const EP_REFS = {...};` (from Task 2) into the `<script>` block immediately after the `EP_KEYWORDS` object's closing `};`.

**Step 2: Insert section ⑦ into each episode panel**

For each episode `eN`, insert this block immediately after that episode's ⑥ Vocabulary `.block` closing `</div>` and before the episode panel's `</section>`:

```html
  <div class="block">
    <div class="block-label"><div class="block-num">7</div><h3>Win the Deal</h3><span class="hint">talk-track &amp; follow-up references</span></div>
    <div class="wtd" data-ep="eN">
      <div class="wtd-h">How to say it · how to position it</div>
      <div class="say-list"></div>
      <details class="godeep wtd-refs">
        <summary><span class="gd-sum-label">References &amp; follow-up</span><span class="gd-sum-meta">cited sources · click to open</span></summary>
        <div class="gd-body"><div class="ref-list"></div></div>
      </details>
    </div>
  </div>
```

Anchor each Edit on the episode's last Vocabulary `<dt>` term (unique per episode) plus the `</dl>` / `</div>` / `</section>` close. The `.say-list` and `.ref-list` ship empty — Task 4's JS fills them.

**Step 3: Verify**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python -c "
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
for o in ['const EP_POSITIONING','const EP_REFS']:
    assert o in html, f'missing {o}'
assert html.count('<h3>Win the Deal</h3>')==8, 'expected 8 Win the Deal blocks'
assert html.count('class=\"wtd\"')==8
assert html.count('<section class=\"panel')==10
for tag in ['div','section','details']:
    assert html.count('<'+tag)==html.count('</'+tag+'>'), f'{tag} imbalance'
js=html.split('<script>')[1].split('</script>')[0]
open('_sgcheck.js','w',encoding='utf-8').write(js)
print('data embedded; 8 Win the Deal blocks')
"
node --check _sgcheck.js && echo "JS OK" && rm _sgcheck.js
```

**Step 4: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/Cross-Cloud-Agentic-Study-Guide.html
git commit -m "feat: study guide v3.1 — embed data + Win the Deal section in 8 episodes"
```

---

## Task 4: `winDealInit()` JS + Save-to-Notes + My Notes URL rendering

**Files:**
- Modify: `Cross-Cloud-Agentic-Study-Guide.html` — `<script>` block

**Step 1: Add `winDealInit()`**

Append to the `<script>` block, before the final init calls:

```js
/* ---- v3.1 Win the Deal: talk-track + references ---- */
function winDealInit(){
  document.querySelectorAll('.wtd').forEach(wtd=>{
    const ep=wtd.dataset.ep;
    const sayList=wtd.querySelector('.say-list');
    (EP_POSITIONING[ep]||[]).forEach(p=>{
      const card=document.createElement('div'); card.className='say-card';
      const s=document.createElement('div'); s.className='say-it'; s.textContent=p.say;
      const po=document.createElement('div'); po.className='position-it';
      const tag=document.createElement('span'); tag.className='pos-tag'; tag.textContent='POSITION';
      po.appendChild(tag);
      po.appendChild(document.createTextNode(p.position));
      card.appendChild(s); card.appendChild(po);
      sayList.appendChild(card);
    });
    const refList=wtd.querySelector('.ref-list');
    const refs=EP_REFS[ep]||[];
    const cats=[];
    refs.forEach(r=>{ if(cats.indexOf(r.category)<0) cats.push(r.category); });
    cats.forEach(cat=>{
      const grp=document.createElement('div'); grp.className='ref-group';
      const h=document.createElement('div'); h.className='ref-cat'; h.textContent=cat;
      grp.appendChild(h);
      refs.filter(r=>r.category===cat).forEach(r=>{
        const row=document.createElement('div'); row.className='ref-row';
        const txt=document.createElement('div');
        const a=document.createElement('a'); a.className='ref-link';
        a.href=r.url; a.target='_blank'; a.rel='noopener'; a.textContent=r.label;
        const note=document.createElement('span'); note.className='ref-note'; note.textContent=r.note;
        txt.appendChild(a); txt.appendChild(note);
        const save=document.createElement('button'); save.className='ref-save'; save.type='button';
        save.textContent='＋ Save to My Notes';
        save.addEventListener('click',()=>{
          const n={id:'n'+Date.now().toString(36)+Math.floor(Math.random()*1e4).toString(36),
                   kw:r.label, ep:ep, detail:r.note+'  '+r.url, userText:'', ts:Date.now()};
          sg3Active().notes.push(n); sg3Save();
          if(window.renderNotes) renderNotes();
          save.textContent='✓ Saved';
          setTimeout(()=>{ save.textContent='＋ Save to My Notes'; },1400);
        });
        row.appendChild(txt); row.appendChild(save);
        grp.appendChild(row);
      });
      refList.appendChild(grp);
    });
  });
}
```

Add `winDealInit();` to the end-of-script init calls (after `clientInit()` — it does not depend on hydration).

**Step 2: Tweak `renderNotes()` so a URL in a note becomes a link**

In the existing `renderNotes()` function, the note detail line is built as `det.textContent=n.detail`. Replace that single line with a call to a new helper, and add the helper near `renderNotes`:

```js
function noteDetailRender(el,text){
  const m=String(text||'').match(/https?:\/\/\S+/);
  if(!m){ el.textContent=text||''; return; }
  const url=m[0], i=text.indexOf(url);
  el.appendChild(document.createTextNode(text.slice(0,i)));
  const a=document.createElement('a');
  a.href=url; a.target='_blank'; a.rel='noopener'; a.textContent=url;
  el.appendChild(a);
  el.appendChild(document.createTextNode(text.slice(i+url.length)));
}
```

So the line `det.textContent=n.detail||'';` becomes `noteDetailRender(det,n.detail);`.

**Step 3: Verify**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python -c "
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
for s in ['winDealInit','noteDetailRender','winDealInit();']:
    assert s in html, f'missing {s}'
js=html.split('<script>')[1].split('</script>')[0]
assert js.count('{')==js.count('}') and js.count('(')==js.count(')'), 'JS imbalance'
open('_sgcheck.js','w',encoding='utf-8').write(js); print('Win the Deal JS present')
"
node --check _sgcheck.js && echo "JS OK" && rm _sgcheck.js
```

**Step 4: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/Cross-Cloud-Agentic-Study-Guide.html
git commit -m "feat: study guide v3.1 — winDealInit + reference Save-to-Notes"
```

---

## Task 5: Final verification

**Files:**
- Verify only: `Cross-Cloud-Agentic-Study-Guide.html`

**Step 1: Structural verification**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python -c "
import sys; sys.stdout.reconfigure(encoding='utf-8')
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
print(f'size: {len(html.encode())//1024} KB')
assert html.count('<section class=\"panel')==10
assert html.count('<h3>Win the Deal</h3>')==8
assert html.count('class=\"wtd\"')==8
for o in ['EP_POSITIONING','EP_REFS','winDealInit']:
    assert o in html, f'missing {o}'
for tag in ['div','section','details','script','style','ul','textarea']:
    assert html.count('<'+tag)==html.count('</'+tag+'>'), f'{tag} imbalance'
js=html.split('<script>')[1].split('</script>')[0]
assert js.count('{')==js.count('}') and js.count('(')==js.count(')'), 'JS imbalance'
open('_sgcheck.js','w',encoding='utf-8').write(js)
hero=html.split('<header')[1].split('</header>')[0]
assert 'APEX' not in hero, 'APEX leaked into hero'
for t in ['co-sell','strategic partnership','channel partner']:
    assert t.lower() not in html.lower(), 'forbidden '+t
print('structure OK; tags + JS balanced; discipline clean')
"
node --check _sgcheck.js && echo "JS SYNTAX OK" && rm _sgcheck.js
```

**Step 2: Browser smoke-test (controller, via preview)**

Load the file; on an episode tab confirm section ⑦ shows the talk-track cards and a collapsed References block; expand it, click a reference link, click "Save to My Notes", confirm the note appears in My Notes with a clickable URL; confirm every `EP_REFS` entry rendered a link.

**Step 3: Commit (if fixes were needed)**

```bash
git commit -am "fix: study guide v3.1 verification fixes" || echo "no fixes needed"
```

---

**End of plan.** 5 tasks. Estimated effort: ~1.5–2 hours (CSS + reference/talk-track curation + embed + JS + verification).
