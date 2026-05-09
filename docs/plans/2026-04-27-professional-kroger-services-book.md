# Professional Kroger Services Book — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build `Professional-Kroger-Services.html` — a single-file Wrox-style book that wraps the 17 Kroger pursuit artifacts in a 5-part, 22-chapter engagement narrative.

**Architecture:** Mirror the Sellers Guide build pattern. Two new files in the APEX repo root: `kroger-services-content.cjs` (chapter content) and `build-kroger-services.cjs` (renderer copied from `build-sellers-guide.cjs` and re-pointed). Output sits in the Kroger deliverables folder so relative artifact links work without rewriting paths.

**Tech Stack:** Node.js (CommonJS), `@mermaid-js/mermaid-cli` for diagram pre-rendering, embedded CSS/JS — same stack the Sellers Guide already uses.

**Reference design doc:** `docs/plans/2026-04-27-professional-kroger-services-book-design.md`

**Reference output:** `docs/book/Professional-APEX-M-Sellers-Guide.html` (look-and-feel target)

---

## Conventions for this plan

- All file paths are absolute or relative to the APEX repo root: `C:/Stage/Clients/Industries/APEX/`
- The output HTML path is referenced as `$OUT` below; its absolute value is:
  `C:/Stage/Clients/Industries/Consumer/Retail/Kroger/02_projects/FY27_Pipeline/assortment-pricing-agentic/deliverables/Professional-Kroger-Services.html`
- "Verify chapter renders" means: run the build, open `$OUT` in a browser, scroll to the chapter, confirm the title, objectives box, body, summary, and Seller Actions blocks all appear with no raw markdown leaking through.
- "Verify companion-artifact links resolve" means: from the rendered Companion Artifacts callout, click each link and confirm it opens the underlying file with no 404.
- Commit cadence: one commit per task. Commit messages use conventional-commit prefixes (`feat`, `chore`, `docs`).
- TDD adaptation: this is content production, not a code project. The "failing test" for each scaffolding task is the build error (missing import, missing field). The "failing test" for each chapter is the missing chapter in the rendered TOC. Both surface immediately when the build runs.

---

## Task 1: Scaffold the content module

**Files:**
- Create: `C:/Stage/Clients/Industries/APEX/kroger-services-content.cjs`

**Step 1: Write the file with a single placeholder chapter so the renderer has something to consume**

```javascript
// kroger-services-content.cjs — Professional Kroger Services book content.
//
// Wraps the 17 deliverables under
// Consumer/Retail/Kroger/02_projects/FY27_Pipeline/assortment-pricing-agentic/deliverables/
// into the 5-part engagement-arc book described in
// docs/plans/2026-04-27-professional-kroger-services-book-design.md.
//
// Independence note: The book is internal Deloitte sellers' material. APEX is
// the internal accelerator name; client-facing narrative blocks (Ch 19) frame
// the work as "Deloitte-delivered agents on Kroger's Microsoft platform" and
// do not name APEX.

const chapters = [];
const appendices = [];

chapters.push({
  num: 1, part: 1, title: 'Placeholder — replaced in Task 4',
  objectives: ['Placeholder objective'],
  body: '## Placeholder\n\nReplaced in Task 4.\n',
  summary: ['Placeholder takeaway'],
  actions: ['Placeholder action'],
});

module.exports = { all: chapters, appendices };
```

**Step 2: Commit**

```bash
cd "C:/Stage/Clients/Industries/APEX"
git add kroger-services-content.cjs
git commit -m "chore(kroger-book): scaffold content module with placeholder chapter"
```

---

## Task 2: Scaffold the builder

**Files:**
- Create: `C:/Stage/Clients/Industries/APEX/build-kroger-services.cjs` (copy of `build-sellers-guide.cjs` with three changes)
- Reference: `C:/Stage/Clients/Industries/APEX/build-sellers-guide.cjs` (read for the source-of-truth machinery)

**Step 1: Copy the Sellers Guide builder verbatim**

```bash
cd "C:/Stage/Clients/Industries/APEX"
cp build-sellers-guide.cjs build-kroger-services.cjs
```

**Step 2: Edit `build-kroger-services.cjs` — three changes**

Change A — header comment (top of file, lines 1-7):

Replace:
```
// build-sellers-guide.cjs
//
// Builds Professional APEX: The Sellers Guide as a single-file Wrox-style
// HTML book. Targets Deloitte Microsoft-practice sellers and GPLs pursuing
// APEX revenue in named industry accounts.
//
// Output: docs/book/Professional-APEX-M-Sellers-Guide.html
// Run:   node build-sellers-guide.cjs
```

With:
```
// build-kroger-services.cjs
//
// Builds Professional Kroger Services as a single-file Wrox-style HTML book.
// Wraps the 17 Kroger deliverables into a 5-part engagement-arc narrative.
// Sits in the Kroger deliverables folder so relative artifact links resolve
// without path rewriting.
//
// Output: <deliverables>/Professional-Kroger-Services.html (absolute path below)
// Run:    node build-kroger-services.cjs
```

Change B — output path (line ~17):

Replace:
```
const OUTPUT_HTML = path.join(ROOT, 'docs', 'book', 'Professional-APEX-M-Sellers-Guide.html');
```

With:
```
const OUTPUT_HTML = 'C:/Stage/Clients/Industries/Consumer/Retail/Kroger/02_projects/FY27_Pipeline/assortment-pricing-agentic/deliverables/Professional-Kroger-Services.html';
```

Change C — content require (line ~178):

Replace:
```
const chapters = require('./sellers-guide-content.cjs');
```

With:
```
const chapters = require('./kroger-services-content.cjs');
```

**Step 3: Run the build to verify the scaffolding works end-to-end**

```bash
cd "C:/Stage/Clients/Industries/APEX"
node build-kroger-services.cjs
```

Expected output (approximate):
```
Building Professional APEX: The Sellers Guide...

  Chapter 1: Placeholder — replaced in Task 4
  ✓ ../Consumer/Retail/Kroger/02_projects/FY27_Pipeline/assortment-pricing-agentic/deliverables/Professional-Kroger-Services.html
    NN KB  ·  1 chapters  ·  0 appendices
```

Note: the "Building Professional APEX: The Sellers Guide..." line still shows the old title — fine for now; we replace it in Task 3 as part of the brand pass. We are verifying the build runs and writes to the new path.

**Step 4: Confirm the file exists**

```bash
ls -la "C:/Stage/Clients/Industries/Consumer/Retail/Kroger/02_projects/FY27_Pipeline/assortment-pricing-agentic/deliverables/Professional-Kroger-Services.html"
```

Expected: file exists, size > 50 KB (CSS + JS overhead).

**Step 5: Commit**

```bash
cd "C:/Stage/Clients/Industries/APEX"
git add build-kroger-services.cjs
git commit -m "chore(kroger-book): scaffold builder script (copy of sellers-guide builder)"
```

---

## Task 3: Re-brand the builder (cover, parts, sidebar, console banner)

**Files:**
- Modify: `C:/Stage/Clients/Industries/APEX/build-kroger-services.cjs`

**Step 1: Edit the parts metadata**

Find the `const parts = { ... }` block (around line 542). Replace the entire object with:

```javascript
const parts = {
  1: { title: 'Why Kroger, Why APEX', intro: 'The strategic context for the Kroger pursuit, where margin moves in modern grocery, and how APEX wedges into the Kroger estate alongside 84.51°, Ocado, and Boost.' },
  2: { title: 'The Service Portfolio', intro: 'The two anchor services (RC-E2E-03 Assortment & Pricing and RC-E2E-09 Product Tracking), the high-attach catalog, and how Kroger differentiates from Albertsons, Publix, HEB, and Ahold.' },
  3: { title: 'The Architecture', intro: 'System of record, the Fabric plane, the Foundry agent plane, the MCP layer, and Purview governance — the five technology planes Deloitte assembles for Kroger.' },
  4: { title: 'The Pursuit', intro: 'Executive engagement, the pitch, risk and stakeholder management, the demo, and the client-presentable Kroger Store 412 day-in-the-shift narrative.' },
  5: { title: 'At Scale', intro: 'Operations and test strategy, the multi-wave service roadmap, cross-grocer expansion, and the closing seller compact.' },
};
```

**Step 2: Edit the cover / front matter**

Find the `const FRONT_MATTER = ...` block (around line 603). Replace it with:

```javascript
const FRONT_MATTER = `
<section class="cover" id="cover">
  <div class="brand">Professional</div>
  <h1 class="title"><span class="accent">Kroger</span> Services</h1>
  <div class="subtitle">The Anchor-Account Companion to APEX RC-E2E-03 + RC-E2E-09</div>
  <div class="edition">FY27 Pipeline · Assortment, Pricing & Product Tracking at The Kroger Co.</div>
  <p class="tagline">A field guide for Deloitte sellers and delivery leads pursuing the Kroger agentic-AI program. Wraps the seventeen pursuit deliverables into one read — strategy, services, architecture, pursuit motion, and at-scale playbook.</p>
  <div class="wrox-label">WROX-STYLE EDITION · KROGER VOLUME</div>
  <div class="byline">
    by the APEX RC team · Deloitte Microsoft Technology &amp; Services Practice<br>
    April 2026 · Version 1.0 · CONFIDENTIAL — internal use only
  </div>
</section>
<section class="front-toc" id="front-matter">
  <h1>How to Use This Book</h1>
  <p><em>Professional Kroger Services</em> is the read-front-to-back companion to the seventeen artifacts that make up the FY27 Kroger pursuit deliverables set. It is not a replacement for those artifacts — it is the narrative that ties them together. A seller can read it cold to get smart on the pursuit; a delivery lead can use it to brief a new team member; a GPL can hand it to an account partner walking into a meeting.</p>
  <p>The book is organised around five questions:</p>
  <ul>
    <li><strong>"Why Kroger, why now, and why does APEX fit?"</strong> → Part I.</li>
    <li><strong>"What are we actually selling?"</strong> → Part II.</li>
    <li><strong>"How does it get built?"</strong> → Part III.</li>
    <li><strong>"How do we close it?"</strong> → Part IV. Chapter 19 (Kroger Store 412) is client-presentable as-is.</li>
    <li><strong>"How do we run it and grow it?"</strong> → Part V.</li>
  </ul>
  <p>Each chapter ends with a <strong>Companion Artifacts</strong> callout listing the underlying deliverable files. Click through whenever you need the full document.</p>
  <aside class="callout independence">
    <div class="callout-label">Independence Reminder</div>
    <p>This book contains publicly-observable strategic signals on The Kroger Co. It does not represent that Deloitte is currently engaged with Kroger, nor does it disclose confidential client information. All account narratives are framed as hypotheses to validate in discovery. The Kroger Store 412 narrative in Chapter 19 is illustrative — it is not a description of any actual Kroger store deployment.</p>
  </aside>
</section>
`;
```

**Step 3: Edit the HTML `<title>`, topbar brand, and topbar tagline**

Find the `<title>` line (around line 637) and the `<header class="topbar">` block (around line 642).

Replace:
```html
<title>Professional APEX — The Sellers Guide</title>
```

With:
```html
<title>Professional Kroger Services</title>
```

Replace:
```html
<a href="#cover" class="book-brand">Professional <span class="accent">APEX</span> · Sellers Guide</a>
<div class="current-chapter" id="current-chapter">Pursuing Microsoft Revenue in Industry Accounts</div>
```

With:
```html
<a href="#cover" class="book-brand">Professional <span class="accent">Kroger</span> Services</a>
<div class="current-chapter" id="current-chapter">FY27 Pipeline · RC-E2E-03 + RC-E2E-09 at The Kroger Co.</div>
```

**Step 4: Edit the console banner**

Find:
```javascript
console.log('Building Professional APEX: The Sellers Guide...\n');
```

Replace with:
```javascript
console.log('Building Professional Kroger Services...\n');
```

**Step 5: Run the build and verify the new branding**

```bash
cd "C:/Stage/Clients/Industries/APEX"
node build-kroger-services.cjs
```

Expected console output:
```
Building Professional Kroger Services...

  Chapter 1: Placeholder — replaced in Task 4
  ✓ ../Consumer/Retail/Kroger/.../Professional-Kroger-Services.html
    NN KB  ·  1 chapters  ·  0 appendices
```

Open the file in a browser and confirm:
- Browser tab title is "Professional Kroger Services"
- Topbar reads "Professional Kroger Services"
- Cover page shows "Professional Kroger Services" with the FY27 subtitle
- Sidebar shows the 5 new part titles (Why Kroger / Service Portfolio / Architecture / Pursuit / At Scale)
- Front matter "How to Use This Book" reads correctly with Kroger framing

**Step 6: Commit**

```bash
cd "C:/Stage/Clients/Industries/APEX"
git add build-kroger-services.cjs
git commit -m "feat(kroger-book): re-brand cover, parts, sidebar, and front matter"
```

---

## Task 4: Add the Companion Artifacts callout type

**Files:**
- Modify: `C:/Stage/Clients/Industries/APEX/build-kroger-services.cjs`

The Sellers Guide supports note / warning / bestpractice / tryitout / keyplay / objection / independence callouts. We add a new `companion` type for "Companion Artifacts" boxes.

**Step 1: Add the new callout matcher**

In `build-kroger-services.cjs`, find the blockquote-callout `if (/^>\s?/.test(line))` block (around line 122). Inside the type-detection chain, add a new branch BEFORE the final `else` / fall-through:

Find:
```javascript
else if (/^\*\*Independence/i.test(firstLine))  { cls = 'independence'; label = 'Independence Reminder'; }
const cleaned = bqText.replace(/^\*\*(Note|Warning|Best Practice|Try It Out|Key Play|Objection|Independence)\*\*[.\s:—-]*/i, '');
```

Replace with:
```javascript
else if (/^\*\*Independence/i.test(firstLine))  { cls = 'independence'; label = 'Independence Reminder'; }
else if (/^\*\*Companion/i.test(firstLine))     { cls = 'companion'; label = 'Companion Artifacts'; }
const cleaned = bqText.replace(/^\*\*(Note|Warning|Best Practice|Try It Out|Key Play|Objection|Independence|Companion Artifacts|Companion)\*\*[.\s:—-]*/i, '');
```

**Step 2: Add the CSS rule for the new callout class**

In `build-kroger-services.cjs`, find the existing callout CSS — search for `.callout.independence` (around line 360-380 in CSS section). Below the independence rule, add:

```css
.callout.companion {
  border-color: var(--gold);
  background: linear-gradient(to right, rgba(200,157,58,0.08), transparent 60%);
}
.callout.companion .callout-label { color: var(--gold); }
.callout.companion ul { margin: 6px 0 0 0; padding-left: 22px; }
.callout.companion li { margin: 3px 0; font-size: 14px; }
.callout.companion a { color: var(--navy); text-decoration: underline; text-decoration-color: var(--gold); }
.callout.companion a:hover { color: var(--gold); }
```

**Step 3: Test the new callout end-to-end**

Edit `kroger-services-content.cjs`. Replace the placeholder body with:

```javascript
chapters.push({
  num: 1, part: 1, title: 'Smoke test',
  objectives: ['Verify the Companion Artifacts callout renders'],
  body: `
## Smoke

This chapter is a temporary smoke test for the Companion Artifacts callout. It is replaced in Task 5.

> **Companion Artifacts**
> - [Walkthrough](Services/RC-E2E-03_Assortment-and-Pricing/Tier0-Foundation/APEX-RC-E2E-03-Walkthrough.docx) — narrative walkthrough of the service
> - [One-pager](Services/RC-E2E-03_Assortment-and-Pricing/Tier1-Executive/APEX-RC-E2E-03-Kroger-OnePager.html) — 5-minute summary
`,
  summary: ['Smoke takeaway'],
  actions: ['Smoke action'],
});
```

(Replace the existing `chapters.push({ ... })` block, keeping `const chapters = [];` and the trailing `module.exports = ...`.)

**Step 4: Build and verify**

```bash
cd "C:/Stage/Clients/Industries/APEX"
node build-kroger-services.cjs
```

Open the output. Scroll to Chapter 1. Confirm:
- A gold-bordered "Companion Artifacts" box appears
- Both bullets render as links (with the gold underline)
- Clicking the One-pager link opens the existing Kroger one-pager file in the browser

**Step 5: Commit**

```bash
cd "C:/Stage/Clients/Industries/APEX"
git add build-kroger-services.cjs kroger-services-content.cjs
git commit -m "feat(kroger-book): add Companion Artifacts callout type and verify with smoke chapter"
```

---

## Task 5: Replace the smoke chapter with Foreword + Chapter 1 (Strategic Context)

**Files:**
- Modify: `C:/Stage/Clients/Industries/APEX/kroger-services-content.cjs`

**Step 1: Remove the smoke chapter and add the Foreword (chapter 0)**

Replace the entire `chapters.push({ ... })` block with two pushes:

```javascript
// ---- PART I — WHY KROGER, WHY APEX ----

chapters.push({
  num: 0, part: 1, title: 'Foreword — How to Read This Book',
  objectives: [
    'Understand the dual audience (sellers and delivery leads) and how the book serves both',
    'Identify the seventeen Kroger deliverables this book wraps',
    'Recognize where the client-presentable narrative blocks live',
    'Know when to read straight through versus jump to a single chapter',
  ],
  body: `
## The book in one paragraph

This book is the read-front-to-back companion to the FY27 Kroger pursuit. The seventeen deliverables under the engagement folder are the substance; this book is the narrative that ties them together. Read it cold and you will know what to sell, what to build, what to govern, and how to scale. Hand the book to a delivery lead joining the team and you will save them two weeks of asking around.

## What's in scope

The book covers the FY27 Kroger pipeline scope as it stands at the design date: RC-E2E-03 Assortment & Pricing Intelligence as the lead service, RC-E2E-09 Product Tracking & FSMA 204 Traceability as the co-anchor, and the Grocery Merchandising service portfolio (six high-attach services) sitting around the two anchors. Architecture coverage runs from the system-of-record Bronze→Silver layer through the Fabric semantic model, the Foundry six-agent fleet, the MCP server tier, and Purview governance.

## How the chapters are organised

The book has five parts. Part I is the *why* — Kroger's strategic posture, where margin moves in grocery, and how APEX wedges into an estate that already has 84.51° and Ocado in it. Part II is the *what* — the two anchor services in depth, the high-attach catalog, and the cross-grocer differentiation table. Part III is the *how* — five technology planes Deloitte assembles. Part IV is the *pursuit* — executive engagement, the pitch, risk and stakeholder management, the demo, and the Kroger Store 412 day-in-the-shift narrative. Part V is the *at-scale* — operations, roadmap, cross-grocer expansion, and the closing seller compact.

## The Kroger Store 412 narrative

Chapter 19 is different from the rest of the book. It is written to be lifted unchanged into a client conversation. APEX is not named in it. The voice is that of a Kroger Marketplace store operations lead living through one shift with a fleet of agents quietly handling the operational friction of the day. Sellers can present Chapter 19 to a Kroger executive and say "this is what your store looks like with the program in production." The book frames Chapter 19 with internal Deloitte context before and after; the chapter body itself stays client-clean.

## The seventeen deliverables this book wraps

> **Companion Artifacts**
> - [Deliverables Index](INDEX.html) — the master index page covering all 17 artifacts
> - [Walkthrough](Services/RC-E2E-03_Assortment-and-Pricing/Tier0-Foundation/APEX-RC-E2E-03-Walkthrough.docx) — the foundational service walkthrough
> - [Grocery Merchandising Portfolio](Services/Shared-Both-Services/Tier0-Foundation/APEX-RC-Grocery-Merchandising-Service-Portfolio.docx) — the eight-service portfolio framing
> - [SOR Bronze→Silver](Services/Shared-Both-Services/Tier0-Foundation/APEX-RC-E2E-03-09-SOR-Bronze-to-Silver.docx) and [SOR ERD](Services/Shared-Both-Services/Tier0-Foundation/APEX-RC-E2E-03-09-SOR-ERD.html)
> - [One-pager](Services/RC-E2E-03_Assortment-and-Pricing/Tier1-Executive/APEX-RC-E2E-03-Kroger-OnePager.html), [ROI Case](Services/RC-E2E-03_Assortment-and-Pricing/Tier1-Executive/APEX-RC-E2E-03-Kroger-ROI-Case.html), [Personas](Services/RC-E2E-03_Assortment-and-Pricing/Tier1-Executive/APEX-RC-E2E-03-Kroger-Personas.html), [FSMA 204 Checklist](Services/RC-E2E-09_Product-Tracking/Tier1-Executive/APEX-FSMA-204-Compliance-Checklist.docx)
> - [Fabric Runbook](Services/Shared-Both-Services/Tier2-Build/APEX-RC-E2E-03-09-Fabric-Runbook.docx), [MCP Deep Dive](Services/RC-E2E-03_Assortment-and-Pricing/Tier2-Build/APEX-RC-E2E-03-MCP-Server-Deep-Dive.docx), [Sequence Diagram](Services/RC-E2E-03_Assortment-and-Pricing/Tier2-Build/APEX-RC-E2E-03-Service-Sequence-Diagram.html), [Six Agents Deep Dive](Services/RC-E2E-03_Assortment-and-Pricing/Tier2-Build/APEX-RC-E2E-03-Six-Agents-Deep-Dive-and-Maturation.docx), [Use Case Catalog](Services/RC-E2E-03_Assortment-and-Pricing/Tier2-Build/APEX-RC-E2E-03-Use-Case-Catalog.xlsx)
> - [Demo Script](Services/RC-E2E-03_Assortment-and-Pricing/Tier3-Governance/APEX-RC-E2E-03-Demo-Script-and-Walkthrough-Guide.docx), [Pitch Deck](Services/RC-E2E-03_Assortment-and-Pricing/Tier3-Governance/APEX-RC-E2E-03-Kroger-Pitch-Deck.html), [Risk Register](Services/RC-E2E-03_Assortment-and-Pricing/Tier3-Governance/APEX-RC-E2E-03-Kroger-Risk-Register.xlsx), [Stakeholder Map](Services/RC-E2E-03_Assortment-and-Pricing/Tier3-Governance/APEX-RC-E2E-03-Kroger-Stakeholder-Map.xlsx)
> - [Cross-Grocer Comparison](Services/RC-E2E-03_Assortment-and-Pricing/Tier4-Strategic/APEX-RC-E2E-03-Cross-Grocer-Comparison.xlsx), [Service Roadmap](Services/Shared-Both-Services/Tier4-Strategic/APEX-RC-E2E-03-09-Service-Roadmap.html), [Privacy & Governance Spec](Services/Shared-Both-Services/Tier4-Strategic/APEX-RC-E2E-03-09-Privacy-Data-Governance-Spec.docx), [AI/ML Model Spec](Services/Shared-Both-Services/Tier4-Strategic/APEX-RC-E2E-03-09-AI-ML-Model-Spec.docx)
> - [Solution Architecture Document](Services/Shared-Both-Services/Tier0-Foundation/APEX-RC-E2E-03-09-Solution-Architecture-Document.docx), [Service Operations Playbook](Services/Shared-Both-Services/Tier2-Build/APEX-RC-E2E-03-09-Service-Operations-Playbook.docx), [Test Strategy](Services/Shared-Both-Services/Tier2-Build/APEX-RC-E2E-03-09-Test-Strategy-and-Test-Plan.docx)

## Independence posture

Every public claim about Kroger in this book is sourced from publicly-available signals and is to be treated as a hypothesis to validate in discovery. Deloitte's audit relationship with Kroger (if any) governs the pursuit; sellers must confirm pre-clearance before any outbound activity. The Independence Reminder callouts in this book mark passages where this discipline is most exposed.
`,
  summary: [
    'Five parts: why → what → how → pursuit → at scale',
    'Seventeen deliverables wrapped, each linked from its chapter',
    'Chapter 19 (Kroger Store 412) is client-presentable as-is',
    'Independence pre-clearance gates every Kroger outbound action',
  ],
  actions: [
    'Read the front matter and the Foreword cold; then jump to the chapter for your role',
    'Open the Deliverables Index in a second tab so you can flip to artifacts as you read',
    'Confirm Independence pre-clearance for Kroger before any client outreach',
  ],
});

chapters.push({
  num: 1, part: 1, title: 'Kroger Strategic Context',
  objectives: [
    'Articulate Kroger\'s post-Albertsons strategic posture in one minute',
    'Name the four publicly-known data and AI investments at Kroger',
    'Identify the three boards / programs an APEX pursuit must respect',
    'Distinguish what is public knowledge from what requires discovery',
  ],
  body: `
> **Independence Reminder**
> All claims in this chapter derive from publicly-available signals as of 2026 Q1. Treat every strategic assertion as a hypothesis to validate in discovery — not as a commitment of fact about The Kroger Co.

## 1.1 The Kroger of 2026 in one paragraph

The Kroger Co. is the second-largest US grocer by revenue and the largest by traditional supermarket footprint. After the Albertsons merger collapsed in late 2024, Kroger entered 2025 as a stand-alone scale grocer with three programmatic priorities its public communications return to: digital and ecommerce growth (Boost membership, Kroger Delivery via Ocado-powered customer fulfillment centers), media and data monetization (Kroger Precision Marketing through 84.51°), and operational productivity (Restock Kroger continuation, FreshFlex labor model, store-network optimization).

## 1.2 The four publicly-known data and AI investments

Sellers walking into a Kroger conversation should have these four investments at the front of their mind. Each is publicly disclosed and each shapes where APEX fits.

### 84.51° — the data and analytics subsidiary

84.51° is Kroger's wholly-owned customer-data and analytics subsidiary headquartered in Cincinnati. It runs Kroger's 60M+ household loyalty data, supports CPG supplier analytics, and powers Kroger Precision Marketing. Public statements describe heavy use of Google Cloud Platform, in-house data-science capacity, and a maturing MLOps practice. **Implication for APEX:** any agentic AI program at Kroger must coexist with 84.51° rather than displace it. The wedge is agent orchestration and HITL discipline on top of 84.51°-curated features and segments — not a re-platform.

### Ocado — the customer fulfillment center technology

Kroger licenses Ocado Smart Platform for its automated customer fulfillment centers (CFCs). The CFCs operate as in-network warehouses serving Kroger Delivery; they carry their own software stack, their own warehouse management, and their own picking robotics. **Implication for APEX:** the CFC envelope is largely closed to outside agentic AI integration; the wedge is at the seam between CFCs and store-fulfilled BOPIS, where Kroger's own software handles substitution, customer notification, and exception management.

### Restock Kroger and FreshFlex — operational discipline programs

Restock Kroger is the multi-year operational productivity program; FreshFlex is the more recent labor-model evolution responding to associate-availability pressure. Both programs have CFO and COO sponsorship; both are productivity-instrumented. **Implication for APEX:** any operational-AI conversation at Kroger must speak the language of these programs — productivity per labor hour, shrink avoidance, freshness-defect rate. Pitches that ignore the existing program rhythm get filtered out.

### Microsoft footprint — Azure, M365, growing AI

Kroger's Microsoft footprint includes substantial Azure consumption, M365 across the enterprise, and a growing Copilot pilot footprint. Public job postings periodically reference Azure AI Foundry, Fabric, and Copilot Studio. **Implication for APEX:** the Microsoft platform conversation has air cover; the question is which boundary inside Kroger owns the conversation, and which Microsoft account team is the sales-side counterpart.

## 1.3 The three boards / programs an APEX pursuit must respect

A Kroger pursuit that does not navigate these three structures will stall.

1. **84.51° governance.** Any agent that uses customer data must pass through 84.51° data-stewardship review. Sellers should sequence 84.51° engagement early, not as an afterthought.
2. **Restock / FreshFlex program offices.** Operational-AI proposals route through these program offices for productivity-impact measurement. Get the productivity-claim formulation right before pitching.
3. **The CFO office.** Kroger is a margin-tight grocer; every program is measured on basis-point impact. Pitches without basis-point math get deferred indefinitely.

## 1.4 What is public knowledge vs what requires discovery

This is the hard line for sellers.

| Public knowledge | Requires discovery |
|---|---|
| 84.51° exists and runs on GCP | Specific feature-store schemas and model-deployment cadence |
| Ocado powers CFCs | CFC-to-store handoff data flows and exception SLAs |
| Restock Kroger is the operational productivity program | Specific 2026 productivity targets by category |
| Azure footprint exists and is growing | Specific AI-platform commitments and Copilot expansion plans |
| FSMA 204 is a regulatory constraint on grocers | Kroger's specific FSMA 204 program timeline and gap posture |
| Cincinnati HQ; CEO and CFO publicly identified | Internal program sponsors for any specific service |

Sellers must be precise about which side of the line a given claim sits on; pretending discovery information is public knowledge will be caught immediately by Kroger's procurement team.

## 1.5 The post-Albertsons window

The Albertsons merger collapsed in late 2024 after the FTC and Washington-state actions. Kroger paid Albertsons a $600M breakup fee. The strategic implication: Kroger entered 2025 with reduced M&A optionality and elevated investor pressure on organic margin and ecommerce growth. **For APEX, this is the window.** Kroger's CFO conversation in 2025-2026 is acutely about basis points of margin and capital discipline. A program that produces credible basis-point impact with a clear capital envelope is a programmatic fit.

> **Companion Artifacts**
> - [One-pager](Services/RC-E2E-03_Assortment-and-Pricing/Tier1-Executive/APEX-RC-E2E-03-Kroger-OnePager.html) — the executive summary that traces back to this strategic context
> - [Cross-Grocer Comparison](Services/RC-E2E-03_Assortment-and-Pricing/Tier4-Strategic/APEX-RC-E2E-03-Cross-Grocer-Comparison.xlsx) — Kroger's posture vs Albertsons, Publix, HEB, Ahold
> - [Stakeholder Map](Services/RC-E2E-03_Assortment-and-Pricing/Tier3-Governance/APEX-RC-E2E-03-Kroger-Stakeholder-Map.xlsx) — the named decision-makers behind these programs
`,
  summary: [
    'Kroger is the #2 US grocer by revenue, post-Albertsons stand-alone, three priorities: digital, media/data, operations',
    '84.51°, Ocado, Restock/FreshFlex, and Microsoft footprint are the four public investments that shape any APEX pursuit',
    '84.51° governance, Restock/FreshFlex program offices, and the CFO office are the three structures the pursuit must navigate',
    'The post-Albertsons window opens a CFO conversation acutely about basis-point margin impact',
  ],
  actions: [
    'Memorize the four public investments and the implication for APEX of each',
    'Confirm Independence pre-clearance status before any outbound on Kroger',
    'Pull the Stakeholder Map and identify your single-threaded executive sponsor hypothesis',
  ],
});
```

**Step 2: Build and verify**

```bash
cd "C:/Stage/Clients/Industries/APEX"
node build-kroger-services.cjs
```

Open `$OUT`. Confirm:
- Sidebar lists "Foreword — How to Read This Book" (Chapter 0) and "Kroger Strategic Context" (Chapter 1) under Part I
- Both chapters render cleanly with objectives, body, summary, Seller Actions
- The Companion Artifacts callouts in both chapters render gold-bordered with working links
- Click the One-pager link in Ch 1's Companion Artifacts box; the existing one-pager opens

**Step 3: Commit**

```bash
cd "C:/Stage/Clients/Industries/APEX"
git add kroger-services-content.cjs
git commit -m "feat(kroger-book): add Foreword and Ch 1 Strategic Context"
```

---

## Tasks 6–25: Author the remaining 21 chapters

Each of the remaining chapters follows the **same task pattern as Task 5**, repeated. Rather than enumerate twenty more identical tasks, this section gives you the per-chapter spec. Treat each chapter as one task; commit after each.

### Per-chapter task pattern

For each chapter:

1. Open `kroger-services-content.cjs` and append a new `chapters.push({ ... })` block with the spec below
2. Run `node build-kroger-services.cjs`
3. Open `$OUT`, scroll to the new chapter, verify it renders and the Companion Artifacts links resolve
4. Commit with message `feat(kroger-book): add Ch <N> <Title>`

### Chapter content briefs

Each brief gives: chapter number, part, title, the 3-5 objectives bullets, the 4-8 body sections to cover, the companion artifacts to link, and the summary/actions framing.

---

#### Task 6 — Chapter 2: Where Margin Moves at Kroger

- **Part:** 1
- **Title:** Where Margin Moves at Kroger
- **Objectives:** name the five margin levers in modern grocery; explain how agentic AI moves each lever; identify which two levers APEX is most differentiated on; recognize when the margin claim is credible vs over-promised
- **Body sections (use `## 2.1`, `## 2.2`, etc.):**
  - 2.1 The five margin levers (assortment & pricing, shrink, labor productivity, supplier-funded media, fresh-defect rate)
  - 2.2 How agentic AI moves each lever (table)
  - 2.3 Where APEX is most differentiated (assortment & pricing + traceability) — and why
  - 2.4 The credibility test — what gets a CFO to take the meeting
  - 2.5 The numbers Kroger publishes (operating margin, gross margin trend) — what they reveal about which levers matter most
- **Companion Artifacts:** ROI Case, Cross-Grocer Comparison
- **Summary:** five levers; two APEX-differentiated levers; basis-point credibility is the gate; CFO conversation goes through margin math
- **Actions:** prepare basis-point claims for your prospect category; rehearse the CFO five-lever framing; identify which lever the merchant sponsor cares about most

---

#### Task 7 — Chapter 3: APEX Wedge into the Kroger Estate

- **Part:** 1
- **Title:** APEX Wedge into the Kroger Estate
- **Objectives:** describe the four-pillar Microsoft footprint at Kroger; explain the coexistence pattern with 84.51° and Ocado; identify the three integration seams APEX engages; recognize the two anti-patterns that kill a Kroger pitch
- **Body sections:**
  - 3.1 The four Microsoft pillars at Kroger today (Azure, M365, growing Foundry/Fabric/Copilot)
  - 3.2 Coexisting with 84.51° (GCP-resident features, MLOps maturity, governance gates)
  - 3.3 Coexisting with Ocado (CFC envelope, the BOPIS seam)
  - 3.4 The three integration seams (loyalty/customer features → Foundry; FSMA 204 traceability → Fabric Eventhouse; merchant decisions → Copilot HITL)
  - 3.5 Anti-pattern #1: pitching a re-platform of 84.51°
  - 3.6 Anti-pattern #2: pitching CFC integration through Ocado
  - 3.7 The architectural slide a CIO will accept (one diagram)
- **Companion Artifacts:** Solution Architecture Document, SOR ERD, Service Roadmap
- **Summary:** four MS pillars; coexist with 84.51° / Ocado; three seams; two anti-patterns to avoid
- **Actions:** map the four MS pillars at your specific Kroger sub-org; identify the seam your pitch lives at; pre-validate the coexistence story with the Microsoft account team

---

#### Task 8 — Chapter 4: The Two Anchors at a Glance

- **Part:** 2
- **Title:** The Two Anchors at a Glance
- **Objectives:** describe RC-E2E-03 and RC-E2E-09 in one sentence each; explain why they are co-anchored; identify the shared infrastructure both rely on; know when to lead with one vs the other
- **Body sections:**
  - 4.1 RC-E2E-03 in one sentence (assortment + pricing + margin alerts to merchants with HITL)
  - 4.2 RC-E2E-09 in one sentence (FSMA 204 traceability + product-level provenance)
  - 4.3 Why they are co-anchored (shared SOR, shared Fabric semantic model, shared agent fleet, complementary stakeholder coverage)
  - 4.4 When to lead with RC-E2E-03 (margin-pressured merchant conversation)
  - 4.5 When to lead with RC-E2E-09 (food-safety-pressured QA / regulatory conversation)
  - 4.6 Common infrastructure both rely on (preview of Part III)
- **Companion Artifacts:** Solution Architecture Document, Walkthrough, FSMA 204 Checklist
- **Summary:** two anchors, one foundation; co-anchoring is by design, not coincidence; lead-service decision turns on the most-pressured executive at the prospect
- **Actions:** identify the most-pressured executive in your Kroger sub-org and pick the lead service accordingly; rehearse the one-sentence framings; map the cross-anchor narrative for stakeholders who span both worlds

---

#### Task 9 — Chapter 5: RC-E2E-03 Assortment & Pricing Intelligence

- **Part:** 2
- **Title:** RC-E2E-03 Assortment & Pricing Intelligence
- **Objectives:** describe the six agents and their handoffs; explain the HITL gates and where they sit; identify the three Kroger personas that consume this service; know the wave-1 / wave-2 / wave-3 commercial envelope
- **Body sections:**
  - 5.1 What the service does (one-paragraph framing)
  - 5.2 The six agents (table: name, input, output, owns-decision)
  - 5.3 The handoff sequence (mermaid diagram)
  - 5.4 The HITL gates (where merchants approve, what gets logged)
  - 5.5 The three personas (Category Manager, Pricing Director, Private-Brand Lead — short journey for each)
  - 5.6 Commercial envelope (Wave 1 $/timeframe, Wave 2, Wave 3)
  - 5.7 Three illustrative use cases (one per persona, abbreviated)
  - 5.8 What the underlying artifacts give you (pointer to Six Agents Deep Dive, Use Case Catalog)
- **Companion Artifacts:** Walkthrough, OnePager, Personas, Six Agents Deep Dive, Use Case Catalog, Sequence Diagram, ROI Case
- **Summary:** six agents, HITL throughout, three personas, three-wave commercial envelope
- **Actions:** memorize the six-agent narrative; rehearse the HITL story for each persona; pre-tune the wave envelopes for your specific Kroger conversation

---

#### Task 10 — Chapter 6: RC-E2E-09 Product Tracking & FSMA 204 Traceability

- **Part:** 2
- **Title:** RC-E2E-09 Product Tracking & FSMA 204 Traceability
- **Objectives:** describe FSMA 204 in regulatory plain English; identify the five Critical Tracking Events (CTEs) and Key Data Elements (KDEs); explain how RC-E2E-09 closes Kroger's most exposed gaps; know the regulatory and litigation context
- **Body sections:**
  - 6.1 FSMA 204 in one paragraph (FDA final rule, January 2026 compliance date, food-traceability list)
  - 6.2 The five CTEs (growing/raising, transformation, creation, shipping, receiving)
  - 6.3 The KDE checklist (what data each CTE must carry)
  - 6.4 TLC discipline — Traceability Lot Code as the spine
  - 6.5 24-month retention — the compliance constraint
  - 6.6 Where Kroger has gaps (publicly inferable: produce + dairy + seafood + soft cheeses)
  - 6.7 How RC-E2E-09 closes the gaps (Fabric Eventhouse + Foundry recall agent + Purview lineage)
  - 6.8 The litigation upside (foreign-object pattern detection, recall response)
- **Companion Artifacts:** FSMA 204 Compliance Checklist, Solution Architecture Document, Fabric Runbook
- **Summary:** FSMA 204 is the regulatory wedge; five CTEs + KDEs are the traceability spine; RC-E2E-09 plus Purview closes Kroger's exposed gaps; litigation defensibility is the second-order value
- **Actions:** memorize the five CTEs; learn one specific Kroger food category gap; rehearse the FSMA 204 → litigation-defensibility pitch for QA leadership

---

#### Task 11 — Chapter 7: The High-Attach Catalog

- **Part:** 2
- **Title:** The High-Attach Catalog
- **Objectives:** name the six high-attach RC services; tier-rank them for Grocery Merchandising; identify which attach to RC-E2E-03 vs RC-E2E-09 vs both; know the typical wave-2 / wave-3 sequence
- **Body sections:**
  - 7.1 The eight-service Grocery Merchandising portfolio (table from APEX-RC-Grocery-Merchandising-Service-Portfolio.docx)
  - 7.2 Tier 1 anchors (E2E-03 + E2E-09)
  - 7.3 Tier 2 high-attach (which services, what each does, attaches to which anchor)
  - 7.4 Tier 3 peripheral (which services, when to consider)
  - 7.5 The wave-2 sequence (typical: which Tier 2 services come first)
  - 7.6 The wave-3 sequence (extension to additional banners / categories)
  - 7.7 What NOT to bundle (services that look related but degrade the pitch)
- **Companion Artifacts:** Grocery Merchandising Portfolio (.docx), Service Roadmap (.html)
- **Summary:** eight services tiered; Tier-2 attach drives Wave-2 expansion; wave-3 is banner/category extension; not all bundling helps
- **Actions:** for your specific prospect, identify the most-likely Tier-2 attach; rehearse the wave-2 sequencing story; pre-clear bundling decisions with the lead partner

---

#### Task 12 — Chapter 8: Cross-Grocer Differentiation

- **Part:** 2
- **Title:** Cross-Grocer Differentiation — Kroger vs Albertsons / Publix / HEB / Ahold
- **Objectives:** describe how the five major US grocers differ on data and AI posture; identify which Kroger characteristics shape the pitch; recognize the cross-grocer claims that translate vs the ones that don't
- **Body sections:**
  - 8.1 The five-grocer comparison (table from Cross-Grocer-Comparison.xlsx)
  - 8.2 Kroger's distinguishing characteristics (84.51°, Ocado, FreshFlex)
  - 8.3 Albertsons' distinguishing characteristics (post-merger-collapse posture, inferred AI maturity)
  - 8.4 Publix, HEB, Ahold — short profiles
  - 8.5 What translates from Kroger to other grocers (the platform pattern, the agent library)
  - 8.6 What does NOT translate (84.51°-specific integration, Ocado-specific seams)
- **Companion Artifacts:** Cross-Grocer Comparison
- **Summary:** five grocers, distinct postures; Kroger's three distinguishing characteristics shape every pitch; the platform pattern translates, the integrations don't
- **Actions:** memorize the five-grocer comparison; rehearse the Kroger-distinct pitch; identify your second-grocer expansion target

---

#### Task 13 — Chapter 9: System of Record (SOR)

- **Part:** 3
- **Title:** System of Record — Bronze→Silver
- **Objectives:** describe the Bronze and Silver layer scopes; identify the source systems feeding Bronze; name the Silver entities; understand why this layering is non-negotiable for downstream agents
- **Body sections:**
  - 9.1 Why SOR matters (no data, no agents)
  - 9.2 The Bronze layer (raw ingest from source systems)
  - 9.3 The source systems (POS, loyalty, supplier portal, FSMA 204 feed, etc.)
  - 9.4 The Silver layer (conformed business entities)
  - 9.5 The Silver entity model (ERD walkthrough)
  - 9.6 Why the Silver model is the spine of every agent
  - 9.7 The Bronze→Silver transformation contract
- **Companion Artifacts:** SOR Bronze→Silver (.docx), SOR ERD (.html)
- **Summary:** Bronze raw, Silver conformed; ten-ish source systems feed Bronze; Silver is the spine; the transformation contract is the QA gate
- **Actions:** walk the ERD with your lead architect; identify which source systems are missing in your prospect's estate; pre-clear the transformation contract owner

---

#### Task 14 — Chapter 10: The Fabric Plane

- **Part:** 3
- **Title:** The Fabric Plane
- **Objectives:** describe the Fabric components in the architecture; name the semantic-model layer; identify the Eventhouse / Eventstream usage; know the capacity-sizing rule of thumb
- **Body sections:**
  - 10.1 What Fabric does for this program
  - 10.2 OneLake as the unified storage tier
  - 10.3 The Fabric semantic model (Direct Lake, what the agents query)
  - 10.4 Eventhouse for time-series telemetry (FSMA 204, cold chain, POS streams)
  - 10.5 Eventstream for ingest pipelines
  - 10.6 Mirroring / shortcuts to 84.51° / Azure data
  - 10.7 Capacity sizing rule of thumb (F-SKU starting envelope, scale path)
- **Companion Artifacts:** Fabric Runbook, Solution Architecture Document
- **Summary:** OneLake + semantic model + Eventhouse/Eventstream; mirroring keeps coexistence clean; capacity sizing has a starting heuristic
- **Actions:** rehearse the Fabric architecture story for a CIO; pre-validate the capacity envelope with the Microsoft account team; identify the F-SKU starting tier for your prospect

---

#### Task 15 — Chapter 11: The Foundry Plane

- **Part:** 3
- **Title:** The Foundry Plane — Six Agents and Maturation
- **Objectives:** name the six agents and their purpose; describe the model-routing strategy (which agent uses which model class); explain the maturation path (prompt → fine-tune → distill); know the cost-per-decision target band
- **Body sections:**
  - 11.1 The six-agent fleet (recap from Ch 5; deeper here)
  - 11.2 Model routing — which agent uses which model class and why
  - 11.3 Tool calling / MCP integration (preview Ch 12)
  - 11.4 The maturation path (start with prompt + RAG; mature to fine-tune; distill where economics demand)
  - 11.5 The cost-per-decision target band (illustrative)
  - 11.6 Evaluation harness (how Foundry agents get measured)
  - 11.7 The HITL contract (how agents surface decisions; how humans respond)
- **Companion Artifacts:** Six Agents Deep Dive, Sequence Diagram, AI/ML Model Spec
- **Summary:** six agents, model-class-aware routing, prompt → fine-tune → distill maturation; cost-per-decision targets and eval harness anchor the economics
- **Actions:** memorize the six-agent / model-class table; rehearse the maturation story for a Chief Data & Analytics Officer; pre-validate the cost band with the Foundry product team

---

#### Task 16 — Chapter 12: The MCP Layer

- **Part:** 3
- **Title:** The MCP Layer
- **Objectives:** describe what MCP is in this architecture; identify the MCP servers in the deployment; explain the contract MCP gives the Foundry agents; understand where MCP intersects with Purview
- **Body sections:**
  - 12.1 MCP in one paragraph (Model Context Protocol, the tool-calling standard)
  - 12.2 The MCP servers in the Kroger deployment (list with purpose for each)
  - 12.3 Server-to-tool contract (what the agents see)
  - 12.4 MCP hosting in Azure (App Service / Container Apps pattern)
  - 12.5 MCP intersection with Purview (classification, lineage, audit)
  - 12.6 MCP intersection with Entra (identity, scopes, on-behalf-of)
  - 12.7 The MCP-as-product story (where MCP becomes the integration spine for Kroger long-term)
- **Companion Artifacts:** MCP Server Deep Dive, Sequence Diagram
- **Summary:** MCP is the agent-to-tool spine; multiple servers, one contract; Azure-hosted; Purview + Entra wrap it; long-term MCP becomes Kroger's integration product
- **Actions:** memorize the MCP server list; rehearse the MCP-as-product narrative for an enterprise architect; pre-clear the MCP hosting choice with the Microsoft account team

---

#### Task 17 — Chapter 13: Purview & Governance

- **Part:** 3
- **Title:** Purview & Governance
- **Objectives:** describe Purview's role in the agentic stack; identify the four Purview capabilities the program uses; explain the data-classification posture; know the audit-row discipline
- **Body sections:**
  - 13.1 Why Purview is non-negotiable in agentic AI
  - 13.2 Data Map / classification (what gets classified and how)
  - 13.3 Data Loss Prevention (DLP) for agent outputs
  - 13.4 Data lineage (Bronze → Silver → semantic model → agent → decision)
  - 13.5 Communication compliance for HITL conversations
  - 13.6 Audit-row discipline (every decision attributed to inputs, model version, human approval)
  - 13.7 The privacy / governance specification walkthrough
- **Companion Artifacts:** Privacy & Data Governance Spec, AI/ML Model Spec
- **Summary:** Purview is non-negotiable; four capabilities (classification, DLP, lineage, comms compliance); audit-row discipline is the regulator-ready spine
- **Actions:** memorize the four Purview capabilities; rehearse the audit-row pitch for Compliance/Legal; pre-clear classification posture with 84.51° governance

---

#### Task 18 — Chapter 14: Executive Engagement

- **Part:** 4
- **Title:** Executive Engagement
- **Objectives:** know what each Tier-1 Executive artifact does and when to use it; sequence executive engagements through these artifacts; rehearse the persona journey for the three target personas
- **Body sections:**
  - 14.1 The Tier-1 Executive set in one frame
  - 14.2 The One-pager — when, to whom, what to expect back
  - 14.3 The ROI Case — the interactive sensitivity story
  - 14.4 The Persona journey artifact — Food Safety Lead day-in-the-life
  - 14.5 The FSMA 204 Compliance Checklist — when QA leadership is in the room
  - 14.6 The sequencing playbook (one-pager → ROI → personas → checklist)
  - 14.7 What to do when the meeting goes sideways (the recovery patterns)
- **Companion Artifacts:** OnePager, ROI Case, Personas, FSMA 204 Checklist
- **Summary:** four Tier-1 artifacts, one sequencing playbook; recovery patterns matter when the room shifts
- **Actions:** memorize the four artifacts and their sequencing; rehearse one persona day-in-the-life cold; have the recovery patterns at hand for your next meeting

---

#### Task 19 — Chapter 15: The Pitch

- **Part:** 4
- **Title:** The Pitch — Walking the 16-Slide Deck
- **Objectives:** know the 16-slide structure of the Kroger pitch; identify the three slides that close the meeting; rehearse the transitions between slides; understand which slides to skip with which audience
- **Body sections:**
  - 15.1 The 16-slide structure overview
  - 15.2 Slides 1-3: setting the strategic context
  - 15.3 Slides 4-7: the two anchor services
  - 15.4 Slides 8-10: the architecture
  - 15.5 Slides 11-13: the commercial envelope and risk
  - 15.6 Slides 14-16: the close (asks, next steps, sponsorship)
  - 15.7 The three closing slides — what each must accomplish
  - 15.8 Audience-specific skip patterns
- **Companion Artifacts:** Pitch Deck (.html), Demo Script & Walkthrough Guide
- **Summary:** 16 slides; three closing slides do the closing work; skip patterns matter
- **Actions:** memorize the 16-slide flow; rehearse the three closers; pre-build your audience-specific skip pattern for the next pitch

---

#### Task 20 — Chapter 16: Risk & Stakeholders

- **Part:** 4
- **Title:** Risk & Stakeholders
- **Objectives:** identify the top-five pursuit risks; map them to mitigation owners; identify the stakeholder tiers; sequence stakeholder engagement
- **Body sections:**
  - 16.1 The risk register at a glance (top categories)
  - 16.2 The top-five pursuit risks (Independence, 84.51° governance, CFO basis-point credibility, Ocado-seam confusion, Microsoft-account-team alignment)
  - 16.3 Mitigation ownership (who owns what)
  - 16.4 The stakeholder tiering (Tier 1 sponsors, Tier 2 influencers, Tier 3 informed)
  - 16.5 Engagement sequencing (Tier 1 first; Tier 2 in workshops; Tier 3 communicated)
  - 16.6 The risk-mitigation rhythm (weekly, by phase)
- **Companion Artifacts:** Risk Register (.xlsx), Stakeholder Map (.xlsx)
- **Summary:** top-five risks; mitigation owners assigned; three stakeholder tiers; engagement sequencing matters
- **Actions:** read the Risk Register cold; identify your top three risks for this specific pursuit; pre-build your stakeholder engagement calendar

---

#### Task 21 — Chapter 17: The Demo

- **Part:** 4
- **Title:** The Demo — Walking RC-E2E-03 Live
- **Objectives:** walk the demo storyline; know the three branch points where the demo can pivot; identify the safety nets for things going wrong; rehearse the recovery patterns
- **Body sections:**
  - 17.1 Demo storyline at a glance (one merchant, one decision, one HITL gate)
  - 17.2 The three branch points where pivot is possible
  - 17.3 The safety nets (offline screenshots, recorded video fallback)
  - 17.4 What can go wrong (network, model latency, data, persona credibility)
  - 17.5 The recovery patterns
  - 17.6 The post-demo question set
- **Companion Artifacts:** Demo Script & Walkthrough Guide, Sequence Diagram
- **Summary:** one merchant, one decision, one HITL; three branch points; safety nets ready; recovery patterns rehearsed
- **Actions:** rehearse the demo cold three times; pre-stage the safety nets; build your post-demo question set

---

#### Task 22 — Chapter 18: Kroger Store 412 — A Day in the Shift

This is the **client-presentable** chapter. APEX is not named; the voice is operational and Kroger-grounded.

- **Part:** 4
- **Title:** Kroger Store 412 — A Day in the Shift
- **Objectives:** experience what an agentic-AI program looks like in production at a Kroger Marketplace store; understand the eight events that anchor the narrative; recognize how HITL gates surface; see the audit-row discipline in operational language
- **Body framing:**
  - Open with an Independence Reminder explicitly framing this as illustrative
  - Open with an internal Deloitte note: "Lift this chapter unchanged into client-facing materials. APEX is not named below by design."
  - Story format mirrors the Sellers Guide's "Big Box Store Store 100" narrative: Marisol-equivalent persona at a Cincinnati Marketplace store, 8 events across one shift, financial impact and time savings table at the end
  - Body sections: 18.1 The shift at a glance (timeline + table); 18.2-18.9 one section per event; 18.10 Shift summary (metrics table); 18.11 Why this narrative matters; 18.12 How to use this narrative in client conversations
- **Eight events (use grocery-flavored events; differentiate from Big Box Store's events to avoid duplication):**
  1. **05:50 — Cold-chain excursion in the dairy walk-in** (Critical, Cold Chain)
  2. **07:15 — Fresh-produce shrink anomaly on bagged salads** (High, Shrink/Fresh)
  3. **08:42 — ESL-shelf-tag desync on private-brand center-store** (High, Price Integrity)
  4. **10:08 — Phantom OOS on 22 high-velocity SKUs in baby aisle** (Medium, OSA)
  5. **11:30 — FDA Class II infant-formula recall** (Critical, Recall — same recall scenario as Big Box Store but resolved through Kroger's FSMA 204 lens)
  6. **12:15 — BOPIS substitution on organic milk** (Low, Customer Experience)
  7. **13:50 — Shrink pattern on register 12 — spirits** (High, Shrink Signal)
  8. **14:45 — Customer incident — foreign object in bakery muffin** (Critical, Customer Incident)
- **Close with both an Independence Reminder and an internal positioning note** matching the Big Box Store chapter pattern
- **Companion Artifacts:** Pitch Deck, Demo Script & Walkthrough Guide, ROI Case
- **Summary:** one shift, eight events, ~5.2 manager hours returned, ~$18-25K decision-attributable financial impact; client-presentable as-is
- **Actions:** read this chapter end-to-end before any client conversation that touches store operations; lift the relevant 1-2 events for the specific stakeholder you're meeting; never name APEX while presenting this

---

#### Task 23 — Chapter 19: Operations & Test Strategy

- **Part:** 5
- **Title:** Operations & Test Strategy
- **Objectives:** know the operating model post-Wave-1; identify the test layers (unit, integration, eval, production); understand the SLOs and the eval harness; know the run-book rhythm
- **Body sections:**
  - 19.1 The operating model post-Wave-1
  - 19.2 The four test layers (unit, integration, eval, production)
  - 19.3 Eval harness for agents (golden sets, regression, drift detection)
  - 19.4 SLOs (latency, accuracy, HITL approval throughput)
  - 19.5 The run-book rhythm (daily, weekly, monthly)
  - 19.6 Incident response (when an agent surfaces something it shouldn't)
- **Companion Artifacts:** Service Operations Playbook, Test Strategy and Test Plan, AI/ML Model Spec
- **Summary:** operating model + four test layers + eval harness + SLOs + run-book + incident response
- **Actions:** memorize the four test layers; rehearse the SLO story for an SRE audience; pre-build the run-book for Wave-1 close

---

#### Task 24 — Chapter 20: The Service Roadmap

- **Part:** 5
- **Title:** The Service Roadmap
- **Objectives:** describe the multi-wave roadmap; identify the wave-2 expansion candidates; know the wave-3 banner-extension story; understand how the roadmap drives commercial framing
- **Body sections:**
  - 20.1 The roadmap at a glance (Wave 1, 2, 3 with timeframes)
  - 20.2 Wave 1 scope and exit criteria
  - 20.3 Wave 2 expansion candidates (high-attach services from Ch 7)
  - 20.4 Wave 3 banner extension (Marketplace, Mariano's, Harris Teeter, Fred Meyer)
  - 20.5 The commercial framing through each wave
  - 20.6 Roadmap risks and mitigation
- **Companion Artifacts:** Service Roadmap (.html), Pitch Deck
- **Summary:** three waves, expansion candidates, banner extension, commercial framing
- **Actions:** memorize the wave envelopes; pre-stage the wave-2 candidate set for your prospect; rehearse the wave-3 banner extension story

---

#### Task 25 — Chapter 21: Cross-Grocer Expansion Pattern

- **Part:** 5
- **Title:** Cross-Grocer Expansion Pattern
- **Objectives:** explain how the Kroger pattern extends to other US grocers; identify which assets transfer vs which need rebuilding; know the order of grocer pursuit after Kroger lands
- **Body sections:**
  - 21.1 The pattern in one paragraph
  - 21.2 What transfers (semantic model, agent library, MCP servers, governance posture)
  - 21.3 What needs rebuilding (grocer-specific source-system integrations, persona tuning, regulatory variants)
  - 21.4 The pursuit order after Kroger (Albertsons, Publix, HEB, Ahold — sequencing rationale)
  - 21.5 The cross-grocer commercial leverage (selling Kroger as the proof point)
- **Companion Artifacts:** Cross-Grocer Comparison, Service Roadmap
- **Summary:** semantic model + agent library + MCP transfer; grocer-specific integrations rebuild; the pursuit order matters; Kroger-as-proof is the leverage
- **Actions:** identify your second-grocer target; pre-stage the Kroger-as-proof story; align with practice leadership on pursuit-order priorities

---

#### Task 26 — Chapter 22: The Kroger Compact

- **Part:** 5
- **Title:** The Kroger Compact
- **Objectives:** internalize the seller compact for the Kroger pursuit; understand the post-close hand-off discipline; know the success criteria for the program
- **Body sections:**
  - 22.1 The seller compact in five sentences
  - 22.2 Independence as the non-negotiable
  - 22.3 Coexistence (84.51°, Ocado) as the architectural commitment
  - 22.4 Basis-point credibility as the CFO commitment
  - 22.5 Audit-row discipline as the regulatory commitment
  - 22.6 The post-close hand-off (sales → delivery)
  - 22.7 Success criteria for the program (Wave-1 close, Wave-2 expansion, Wave-3 banner extension, cross-grocer leverage)
- **Companion Artifacts:** all 17 artifacts (link the INDEX)
- **Summary:** the compact in five sentences; four commitments; the hand-off discipline; the success criteria
- **Actions:** sign the compact in your own head before the next Kroger conversation; review the Independence checklist; pre-stage the hand-off in your pursuit plan

---

## Task 27: Final validation pass

**Files:**
- Verify: `$OUT` (the rendered HTML)

**Step 1: Run the build clean**

```bash
cd "C:/Stage/Clients/Industries/APEX"
node build-kroger-services.cjs
```

Expected:
```
Building Professional Kroger Services...

  Chapter 0: Foreword — How to Read This Book
  Chapter 1: Kroger Strategic Context
  Chapter 2: Where Margin Moves at Kroger
  ...
  Chapter 22: The Kroger Compact
  ✓ ../Consumer/Retail/Kroger/.../Professional-Kroger-Services.html
    NN KB  ·  23 chapters  ·  0 appendices
```

(23 chapters because Foreword is num=0 plus Ch 1–22.)

**Step 2: Open the output in a browser and walk the book end-to-end**

Verify:
- Cover renders correctly with Kroger branding
- Sidebar shows all 5 parts and all 23 chapters
- Search box works (type "FSMA" → narrows TOC)
- Dark-mode toggle works
- Each chapter has objectives box, body, summary, Seller Actions
- Companion Artifacts callouts are gold-bordered with working links
- Mermaid diagrams render to PNG (not raw mermaid text)
- Chapter 19 (Kroger Store 412) does NOT mention APEX in its body (it does in the framing notes around it)
- Chapter numbers in the sidebar match the chapter headings

**Step 3: Link integrity check**

Open every Companion Artifacts callout and click each link. Each should resolve to an existing file. If any 404s, fix the path in the corresponding `chapters.push({ ... })` block and rebuild.

**Step 4: Spot-check Independence callouts**

The Independence Reminder should appear at:
- Front matter (How to Use This Book)
- Top of Chapter 1
- Top and bottom of Chapter 19 (Kroger Store 412)

If any is missing, add it.

**Step 5: Final commit**

```bash
cd "C:/Stage/Clients/Industries/APEX"
git add -A
git commit -m "feat(kroger-book): final validation — full book builds cleanly with all 23 chapters and link integrity verified"
```

---

## Definition of done (matches the design doc)

- `build-kroger-services.cjs` and `kroger-services-content.cjs` exist in the APEX repo root
- Running `node build-kroger-services.cjs` from the APEX repo root produces `Professional-Kroger-Services.html` at the deliverables folder path with no errors
- Output HTML opens in a browser, sidebar navigates, all 23 chapters render, all Companion Artifacts links resolve to existing files
- Mermaid diagrams render
- Search, dark mode, font-size controls work
- File size in the same order of magnitude as the Sellers Guide (~3-4 MB)
