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

Chapter 18 is different from the rest of the book. It is written to be lifted unchanged into a client conversation. APEX is not named in it. The voice is that of a Kroger Marketplace store operations lead living through one shift with a fleet of agents quietly handling the operational friction of the day. Sellers can present Chapter 18 to a Kroger executive and say "this is what your store looks like with the program in production." The book frames Chapter 18 with internal Deloitte context before and after; the chapter body itself stays client-clean.

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
    'Chapter 18 (Kroger Store 412) is client-presentable as-is',
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

module.exports = { all: chapters, appendices };
