# Cross-Cloud Agentic Study Guide v3.2 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a runnable client-intake Markdown template, an Import pipeline that prepopulates the guide from a client `.md`, and keyword-treeview fixes (auto-expand + highlight the section being played, and stop a keyword/section click from reseeking the audio).

**Architecture:** A new prompt-template file under a new `clients/` folder produces per-client `.md` files that carry a fenced `json` block. The guide's Overview Import is extended to read that block and prepopulate the multi-client store. The v3 `keywordTreeInit()` is rewritten to use a real toggle element and to drive auto-expand/highlight off the audio's `timeupdate`.

**Tech Stack:** Markdown prompt template · single self-contained HTML · inline CSS + vanilla JS · `node --check` for verification.

**Design doc:** `docs/plans/2026-05-15-cross-cloud-agentic-study-guide-v3.2-design.md`.

**Target file:** `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic\Cross-Cloud-Agentic-Study-Guide.html` (~375 KB after v3.1).

## Notes for the executor

- Tasks 2 and 3 modify the same HTML file — run sequentially. Task 1 is independent (a new file).
- Vanilla JS only; after any JS change the script must pass `node --check`.
- Commit each task with `git add <path>` then `git commit` — never `git commit -a`.

---

## Task 1: Client intake template + `clients/` folder

**Files:**
- Create: `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic\clients\_client-intake-template.md`

**Step 1: Create the folder and file**

Create the `clients/` folder and write `_client-intake-template.md` with EXACTLY this content:

````markdown
# Client Intake — Cross-Cloud Agentic Study Guide

**Purpose:** Produce a comprehensive per-client briefing that prepopulates the Cross-Cloud Agentic study guide — the client profile, a position on all 24 axis questions, and the research behind each. Run this template in Claude.

## How to run

1. **Pick the client.** List the files already in this `clients/` folder (every `*.md` except this template). Show the operator that list and ask: refresh one of those, or create a new client? If new, ask for the client's name.
2. **Research the client** from public sources — recent news, earnings commentary, cloud and AI announcements, partnerships, leadership changes, job postings. Note what you find and what you could not.
3. **Position the client** on each of the 24 axes below. For each axis pick an integer **0–4**: `0` = strongly the left pole, `2` = neutral, `4` = strongly the right pole. Add a one-line rationale and a confidence flag (`high` / `medium` / `low` — use `low` where research was thin). The "MS-favorable pole" tells you which end strengthens a Microsoft-attached recommendation; it does not change the client's actual position — record where the client truly sits.
4. **Draft the client profile** — industry, current clouds, AI maturity, key signals.
5. **Write the output file** `clients/<client-slug>.md` per the "Output" section. `<client-slug>` is the lowercased, hyphenated client name.

## The 24 axes

Scale for every axis: `0` = strongly [left pole] · `2` = neutral · `4` = strongly [right pole].

### Episode 1 — The Agentic Stack
- **e1-ax1** — *Of the systems your teams already call "agents," how many satisfy all four criteria — reasoning, tool use, state, and an audit substrate?* — `pipelines relabelled as agents` ↔ `systems that meet all four criteria` — MS-favorable: right.
- **e1-ax2** — *When you evaluate a cloud for agentic AI, are you deciding on the agent runtime, or on the data foundation and control plane underneath it?* — `runtime-first selection` ↔ `architecture-first selection` — MS-favorable: right.
- **e1-ax3** — *If your preferred cloud reached capability parity with the others in eighteen months, what would still make it the right choice?* — `productization lead today` ↔ `durable architectural fit` — MS-favorable: right.

### Episode 2 — Data Foundation
- **e2-ax1** — *When a new AI project starts today, does it get a fresh copy of the data, or does it compose against sources in place?* — `bulk replication into a new lake` ↔ `federation & mirroring, sources untouched` — MS-favorable: right.
- **e2-ax2** — *Is the data your agents need spread across multiple clouds, or concentrated in one?* — `cross-cloud-spread data` ↔ `single-cloud-concentrated data` — MS-favorable: right.
- **e2-ax3** — *Does your warehouse's Gold layer serve analyst dashboards, or is there a substrate shaped for agent reasoning?* — `BI-shaped Gold (aggregation)` ↔ `agent-shaped Gold (per-entity composition)` — MS-favorable: right.

### Episode 3 — Agent Runtime
- **e3-ax1** — *Do your agents' tool calls land on composed views, or directly on source systems and the data warehouse?* — `source-direct tool calls` ↔ `Gold-Tier-routed tool calls` — MS-favorable: right.
- **e3-ax2** — *Is there a specific model your teams must use — and is that preference strong enough to choose the cloud?* — `model-dominant requirement` ↔ `architecture-dominant requirement` — MS-favorable: right.
- **e3-ax3** — *For your highest-value use case, have you tested retrieval (RAG) before reaching for fine-tuning?* — `retrieval-first adaptation` ↔ `training-first adaptation` — MS-favorable: left.

### Episode 4 — Governance & Identity
- **e4-ax1** — *Does your current data-loss-prevention policy tell an agent tool call apart from a human query?* — `human-era DLP` ↔ `AI-aware DSPM` — MS-favorable: right.
- **e4-ax2** — *Is your identity reality one primary cloud with a federated SaaS workforce, or genuinely cross-cloud workloads?* — `enterprise-SaaS-federation reality` ↔ `cross-cloud-workload-identity reality` — MS-favorable: left.
- **e4-ax3** — *Which AI risk framework will your auditors and board hold you to — EU AI Act, NIST AI RMF, ISO 42001?* — `lightly-governed posture` ↔ `regulated / board-visible posture` — MS-favorable: right.

### Episode 5 — Audit & Ledger
- **e5-ax1** — *If an external auditor asked you to reproduce an agent decision from six weeks ago, could you?* — `unprovable decisions` ↔ `replayable, hash-chained decisions` — MS-favorable: right.
- **e5-ax2** — *Of your planned agent workloads, which touch regulated data, customer-facing decisions, or board-visible outputs?* — `non-regulated internal-use (~80%)` ↔ `regulated / customer-facing / board-visible (~20%)` — MS-favorable: right.
- **e5-ax3** — *Is your agent activity captured as structured audit rows, or as free-form log lines?* — `free-form log lines` ↔ `schema-validated audit rows` — MS-favorable: right.

### Episode 6 — FinOps
- **e6-ax1** — *Can you state the cost-per-decision for your top three agent use cases — and the outcome value of each?* — `aggregate AI spend` ↔ `per-use-case cost-per-outcome` — MS-favorable: right.
- **e6-ax2** — *Do your agents default to the most capable model, or is the model selected per task?* — `default-to-largest-model` ↔ `disciplined model-mix` — MS-favorable: right.
- **e6-ax3** — *What is your AI consumption cost trajectory quarter over quarter — and is the growth attributed to workloads?* — `unattributed consumption growth` ↔ `workload-attributed consumption` — MS-favorable: right.

### Episode 7 — Multi-Cloud & Portability
- **e7-ax1** — *When you say "multi-cloud," do you mean workloads on multiple clouds, or individual workloads spanning clouds?* — `enterprise-level multi-cloud (the norm)` ↔ `workload-level multi-cloud (the exception)` — MS-favorable: left.
- **e7-ax2** — *What is driving the multi-cloud requirement — regulatory residency, data gravity, M&A — or lock-in aversion and vendor leverage?* — `legitimate multi-cloud drivers` ↔ `multi-cloud theatre` — MS-favorable: right.
- **e7-ax3** — *If the model behind your agent were deprecated tomorrow, how long would it take to swap it?* — `model-locked agent design` ↔ `model-portable agent design` — MS-favorable: right.

### Episode 8 — The Seller's Playbook
- **e8-ax1** — *Where did the client show the most pain — and is that pain a contained, measurable Wave 1?* — `pain-aligned Wave 1 entry` ↔ `scope-creep / boil-the-ocean` — MS-favorable: left.
- **e8-ax2** — *Is the client's cloud reality a deliberate strategy, or an inherited history of acquisitions and defaults?* — `strategic cloud posture` ↔ `inherited cloud history` — MS-favorable: right.
- **e8-ax3** — *Does the client's architecture team know AWS and GCP well enough to catch an overclaim?* — `sophisticated, cross-cloud-fluent client` ↔ `trusting, single-cloud client` — MS-favorable: right.

## Client profile fields

- **industry** — the client's primary industry.
- **clouds** — current cloud footprint (e.g. "AWS primary, Azure for M365").
- **aiMaturity** — where they are with AI/agents (e.g. "POCs in progress, no production agents").
- **signals** — key signals: recent news, earnings notes, leadership/org changes, stated AI priorities.

## Output

Write `clients/<client-slug>.md` with these sections:

1. `# <Client Name> — Cross-Cloud Agentic client briefing` and the date.
2. `## Profile` — the four profile fields, each with a sentence.
3. `## Axis positions` — for each of the 24 axes: the axis id, the chosen 0–4 position with the pole names, the one-line rationale, and the confidence flag.
4. `## Research sources` — a bulleted list of the public sources used.
5. `## Import data` — a single fenced `json` code block, exactly this shape (fill every axis you could position; omit an axis only if you truly could not form a view):

```json
{
  "schema": 3,
  "client": {
    "id": "<client-slug>",
    "name": "<Client Name>",
    "profile": { "industry": "", "clouds": "", "aiMaturity": "", "signals": "" },
    "axes": {
      "e1": { "e1-ax1": 0, "e1-ax2": 0, "e1-ax3": 0 },
      "e2": { "e2-ax1": 0, "e2-ax2": 0, "e2-ax3": 0 },
      "e3": { "e3-ax1": 0, "e3-ax2": 0, "e3-ax3": 0 },
      "e4": { "e4-ax1": 0, "e4-ax2": 0, "e4-ax3": 0 },
      "e5": { "e5-ax1": 0, "e5-ax2": 0, "e5-ax3": 0 },
      "e6": { "e6-ax1": 0, "e6-ax2": 0, "e6-ax3": 0 },
      "e7": { "e7-ax1": 0, "e7-ax2": 0, "e7-ax3": 0 },
      "e8": { "e8-ax1": 0, "e8-ax2": 0, "e8-ax3": 0 }
    },
    "paq": {}, "actions": {}, "notes": []
  }
}
```

The seller then opens the study guide → Overview tab → Client profile → **Import**, and selects this `.md` file. The guide reads the `json` block, loads the client, and prepopulates the profile, all 24 axis selectors, the likelihood bars, and the seller-action emphasis.
````

**Step 2: Verify**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python -c "
import re
t=open('clients/_client-intake-template.md',encoding='utf-8').read()
ids=re.findall(r'e[1-8]-ax[1-3]',t)
assert len(set(ids))==24, f'expected 24 axis ids, found {len(set(ids))}'
assert '## Import data' in t and '\"schema\": 3' in t
print('template OK -', len(set(ids)), 'axes')
"
```

**Step 3: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/clients/_client-intake-template.md
git commit -m "feat: study guide v3.2 — client intake MD template"
```

---

## Task 2: Import pipeline — accept `.md`, prepopulate, set active

**Files:**
- Modify: `Cross-Cloud-Agentic-Study-Guide.html` — the `<script>` block + the `#cpImportFile` input

**Step 1: Widen the file input's accept attribute**

Find `<input type="file" id="cpImportFile" accept="application/json,.json" ...>` and change its `accept` to `accept=".md,.json,application/json,text/markdown"`.

**Step 2: Add the import parser/applier helpers**

In the `<script>` block, immediately after the `sg3Active` function definition, add:

```js
function sg3ParseImport(text){
  let payload=String(text||'');
  const m=payload.match(/```json\s*([\s\S]*?)```/i);
  if(m) payload=m[1];
  return JSON.parse(payload);
}
function sg3ApplyImport(data){
  let recs=[];
  if(data&&data.clients) recs=Object.keys(data.clients).map(k=>data.clients[k]);
  else if(data&&data.client) recs=[data.client];
  else if(data&&data.id&&data.name) recs=[data];
  let lastId=null;
  recs.forEach(rec=>{
    if(!rec||!rec.id) return;
    rec.profile=rec.profile||{industry:'',clouds:'',aiMaturity:'',signals:''};
    rec.axes=rec.axes||{}; rec.paq=rec.paq||{};
    rec.actions=rec.actions||{}; rec.notes=rec.notes||[];
    SG3.clients[rec.id]=rec; lastId=rec.id;
  });
  return lastId;
}
```

**Step 3: Replace the import file-change handler**

In `clientInit()`, the import wiring currently reads (the `impFile.addEventListener('change', …)` block). Replace the body of that change handler so the `r.onload` is:

```js
      r.onload=()=>{
        try{
          const data=sg3ParseImport(r.result);
          const id=sg3ApplyImport(data);
          if(id){
            SG3.activeClientId=id; sg3Save(); hydrateClient();
            alert('Imported client: '+SG3.clients[id].name);
          } else {
            alert('No client record found in that file.');
          }
        }catch(e){
          alert('Could not read that file — expected a study-guide .md or .json export.');
        }
        impFile.value='';
      };
```

Leave the rest of the import wiring (`imp.addEventListener('click',()=>impFile.click())`, `r.readAsText(f)`) unchanged.

**Step 4: Verify**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python -c "
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
for s in ['sg3ParseImport','sg3ApplyImport','SG3.activeClientId=id','.md,.json']:
    assert s in html, f'missing {s}'
js=html.split('<script>')[1].split('</script>')[0]
assert js.count('{')==js.count('}') and js.count('(')==js.count(')'), 'JS imbalance'
open('_sgcheck.js','w',encoding='utf-8').write(js); print('import pipeline present')
"
node --check _sgcheck.js && echo "JS OK" && rm _sgcheck.js
```

Also confirm the parser logic with a quick standalone check:

```bash
node -e "
function sg3ParseImport(text){let p=String(text||'');const m=p.match(/\`\`\`json\s*([\s\S]*?)\`\`\`/i);if(m)p=m[1];return JSON.parse(p);}
const md='# x\n\n## Import data\n\`\`\`json\n{\"schema\":3,\"client\":{\"id\":\"acme\",\"name\":\"Acme\"}}\n\`\`\`\n';
const d=sg3ParseImport(md);
if(d.client.id!=='acme') throw new Error('parse failed');
console.log('md json-block parse OK');
"
```

**Step 5: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/Cross-Cloud-Agentic-Study-Guide.html
git commit -m "feat: study guide v3.2 — import .md client file + prepopulate"
```

---

## Task 3: Player keyword UX — toggle fix, auto-expand, highlight

**Files:**
- Modify: `Cross-Cloud-Agentic-Study-Guide.html` — the `<style>` block + `keywordTreeInit()`

**Step 1: Update the CSS**

In the `<style>` block, the keyword-treeview rules currently include:
```
.np-item.has-kw::after{content:"\25B8";font-family:"JetBrains Mono",monospace;color:var(--amber);margin-left:auto;transition:transform .15s ease}
.np-item.has-kw.open::after{transform:rotate(90deg)}
```
Replace those two lines with:
```
.kw-toggle{display:inline-block;font-family:"JetBrains Mono",monospace;color:var(--amber);margin-left:auto;cursor:pointer;padding:0 6px;flex:none;transition:transform .15s ease}
.np-item.has-kw.open .kw-toggle{transform:rotate(90deg)}
```
And immediately after the `.kw-node:hover` rule add:
```
.kw-node.kw-now{border-left-color:var(--amber);background:var(--amber-bg);color:var(--ink);box-shadow:0 0 8px -2px var(--amber-dim)}
```

**Step 2: Replace `keywordTreeInit()`**

Replace the entire existing `function keywordTreeInit(){ … }` with:

```js
function keywordTreeInit(){
  document.querySelectorAll('.player').forEach(player=>{
    const ep=player.dataset.ep;
    const kw=EP_KEYWORDS[ep];
    const list=player.querySelector('.np-list');
    if(!kw||!list) return;
    const audio=player.querySelector('audio');
    const cues=EP_CUES[ep]||[];
    const rows=[].slice.call(list.querySelectorAll('.np-item'));
    const trees={};
    rows.forEach((row,i)=>{
      const kws=kw[String(i)];
      if(!kws||!kws.length) return;
      row.classList.add('has-kw');
      const tog=document.createElement('span');
      tog.className='kw-toggle'; tog.textContent='▸';
      const kids=document.createElement('div');
      kids.className='kw-children';
      kws.forEach(k=>{
        const node=document.createElement('div');
        node.className='kw-node';
        node.textContent=k.term;
        node.addEventListener('click',e=>{ e.stopPropagation(); openKeywordModal(ep,k); });
        kids.appendChild(node);
      });
      row.appendChild(tog);
      row.insertAdjacentElement('afterend',kids);
      tog.addEventListener('click',e=>{
        e.stopPropagation();
        row.classList.toggle('open');
        kids.classList.toggle('open');
      });
      trees[String(i)]={row:row,kids:kids};
    });
    if(audio&&cues.length){
      let lastIdx=-1;
      audio.addEventListener('timeupdate',()=>{
        const ct=audio.currentTime||0;
        let idx=0;
        for(let i=0;i<cues.length;i++){ if(cues[i].t<=ct+0.25) idx=i; else break; }
        if(idx===lastIdx) return;
        lastIdx=idx;
        Object.keys(trees).forEach(k=>{
          const t=trees[k], on=(k===String(idx));
          t.row.classList.toggle('open',on);
          t.kids.classList.toggle('open',on);
          t.kids.querySelectorAll('.kw-node').forEach(n=>n.classList.toggle('kw-now',on));
        });
      });
    }
  });
}
```

Key differences from the old version: the disclosure is a real `.kw-toggle` span (clicking it toggles and `stopPropagation`s — no audio seek); there is **no** click handler on the row itself for toggling (the v2 row-click seek is left untouched); a `timeupdate` listener auto-expands the section being played and adds `.kw-now` to its keywords, collapsing the others.

`keywordTreeInit()` is still called once at the end of the script after `playerInit()` — leave that call as-is.

**Step 3: Verify**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python -c "
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
assert '.kw-toggle{' in html and '.kw-node.kw-now{' in html
assert '.np-item.has-kw::after' not in html, 'old ::after triangle still present'
for s in ['kw-toggle','kw-now','timeupdate']:
    assert s in html, f'missing {s}'
js=html.split('<script>')[1].split('</script>')[0]
assert js.count('{')==js.count('}') and js.count('(')==js.count(')'), 'JS imbalance'
# the row no longer gets a toggle-on-click handler: keywordTreeInit must not add a row click that toggles
open('_sgcheck.js','w',encoding='utf-8').write(js); print('keyword UX changes present')
"
node --check _sgcheck.js && echo "JS OK" && rm _sgcheck.js
```

**Step 4: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/Cross-Cloud-Agentic-Study-Guide.html
git commit -m "feat: study guide v3.2 — keyword auto-expand/highlight + fix reseek"
```

---

## Task 4: Final verification

**Files:**
- Verify only.

**Step 1: Structural verification**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python -c "
import sys; sys.stdout.reconfigure(encoding='utf-8')
html=open('Cross-Cloud-Agentic-Study-Guide.html',encoding='utf-8').read()
print(f'size: {len(html.encode())//1024} KB')
assert html.count('<section class=\"panel')==10
assert html.count('<h3>Win the Deal</h3>')==8
for s in ['sg3ParseImport','sg3ApplyImport','keywordTreeInit','kw-toggle','kw-now']:
    assert s in html, f'missing {s}'
for tag in ['div','section','details','script','style']:
    assert html.count('<'+tag)==html.count('</'+tag+'>'), f'{tag} imbalance'
js=html.split('<script>')[1].split('</script>')[0]
assert js.count('{')==js.count('}') and js.count('(')==js.count(')'), 'JS imbalance'
open('_sgcheck.js','w',encoding='utf-8').write(js)
print('structure OK')
"
node --check _sgcheck.js && echo "JS SYNTAX OK" && rm _sgcheck.js
ls clients/_client-intake-template.md && echo "template present"
```

**Step 2: Browser smoke-test (controller, via preview)**

Load the file. (a) Build a tiny test client `.md` with a json block and Import it from the Overview tab — confirm the profile fields, axis selectors, and likelihood bars prepopulate and the client is active in the selector. (b) On an episode tab, press play — confirm the section being played auto-expands its keyword tree and its keywords get the `.kw-now` highlight. (c) Click a keyword — confirm the modal opens and the audio position does NOT jump. (d) Click the disclosure triangle — confirm it toggles without seeking.

**Step 3: Commit (if fixes were needed)**

```bash
git commit -am "fix: study guide v3.2 verification fixes" || echo "no fixes needed"
```

---

**End of plan.** 4 tasks. Estimated effort: ~1.5 hours.
