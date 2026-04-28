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

chapters.push({
  num: 2, part: 1, title: 'Where Margin Moves at Kroger',
  objectives: [
    'Name the five margin levers that matter most in modern grocery',
    'Explain how agentic AI moves each lever in concrete terms',
    'Identify the two levers APEX is most differentiated on at Kroger',
    'Recognize when a basis-point margin claim is credible vs over-promised',
  ],
  body: `
> **Independence Reminder**
> Margin commentary in this chapter is calibrated to publicly-disclosed grocery industry ranges and Kroger's own public filings as of 2026 Q1. No internal Kroger figures are referenced. Every basis-point claim is illustrative and to be replaced with discovery-validated numbers before any client commitment.

Margin is the dominant lens for any Kroger conversation in 2026. The post-Albertsons capital-discipline window, the persistent gap between US grocery operating margins and broader retail, and the open investor question of how Kroger sustains organic growth without M&A optionality all converge on one CFO-level concern: where do the next 100-200 basis points of operating margin come from, and which of them are defensible in audit. A pursuit that does not start with margin is a pursuit that will not survive the second meeting.

## 2.1 The five margin levers in modern grocery

Five levers move margin in modern grocery. Sellers should be able to name them in order, describe each in two sentences, and quote a publicly-disclosed industry impact range for each.

### Assortment & Pricing

Assortment and pricing is the lever closest to gross margin. It covers SKU-level rationalization (what to stock and discontinue), private-label penetration, everyday and promotional price-point setting, vendor-funded promotion participation, and the price-elasticity-aware response to competitor moves. Industry public commentary places category-level uplift from disciplined assortment-and-pricing programs in the **80-200 bps** range over a multi-year horizon, with the top end coming from private-label-heavy categories.

### Shrink (especially fresh)

Shrink — inventory loss to spoilage, theft, and process breakdown — is the largest controllable cost line in fresh categories. Public US grocery disclosures put total shrink in the **1.5-3.5%** of revenue range, with fresh categories (produce, meat, deli, bakery) running materially higher. Reducing fresh shrink by even 50-100 bps of category revenue moves the whole-store margin meaningfully.

### Labor productivity

Labor is the largest single operating expense in a supermarket P&L. The lever covers both labor scheduling (FreshFlex-style flexible models) and the substitution of routine knowledge work with agent-assisted decisioning (planogram updates, replenishment recommendations, exception handling). Public productivity-program disclosures across the industry suggest **3-7% labor cost reductions** are achievable when the lever is pulled with discipline.

### Supplier-funded retail media

Retail media is the highest-margin revenue line in modern grocery. Kroger Precision Marketing through 84.51° is the public face of this lever for Kroger. Industry analysts publicly estimate retail-media gross margins in the **70-90%** range, materially above any other revenue stream, and growth rates that compound at 20-30% annually for the leading networks.

### Fresh-defect rate

Fresh-defect rate — the percentage of fresh items sold that fail a freshness or condition standard — sits at the intersection of customer trust and shrink. Reducing the defect rate moves both customer satisfaction (loyalty trips, basket size) and shrink (markdowns, write-offs). Public commentary places fresh-defect impact in the **30-80 bps** category-margin range when addressed systematically.

| Lever | What it is | Typical impact range (bps) | Where it shows up financially |
|---|---|---|---|
| Assortment & Pricing | SKU rationalization, private-label, price elasticity, promo participation | 80-200 bps category margin | Gross margin line; private-label penetration % |
| Shrink (fresh) | Spoilage, theft, process loss in produce / meat / deli / bakery | 50-150 bps category margin | Cost of goods; inventory adjustment line |
| Labor productivity | Scheduling, agent-assisted decisioning, exception handling | 3-7% labor expense | SG&A; labor hours per $K revenue |
| Supplier-funded retail media | CPG-funded promo and on-site media monetized by the grocer | 70-90% margin on incremental revenue | Other revenue; media income line |
| Fresh-defect rate | % of fresh items sold below freshness/condition standard | 30-80 bps category margin | Markdowns, customer-experience metrics |

## 2.2 How agentic AI moves each lever

The five levers map to five agent-classes. The shorthand for sellers is: **decision class → agent class → audit row.**

### Assortment & Pricing — the merchant-decision agents

The agent-class is a **multi-agent merchant-decision pod** built on Foundry, with HITL gates at every recommendation boundary and audit-row attribution that ties each assortment or pricing change back to the model output, the merchant decision, and the realized P&L delta. RC-E2E-03 Assortment & Pricing Intelligence is exactly this class. The mechanism is straightforward: the agents narrow the merchant's decision space from "review 12,000 SKUs across 40 categories" to "approve, modify, or reject 200 priority recommendations this week," with the rationale and counterfactual surfaced inline in Copilot.

### Shrink (fresh) — the perishable-flow agents

The agent-class is a **perishable-flow agent** that consumes POS streams, receiving events, temperature telemetry where available, and waste-bin scans, then issues markdown-timing, cross-store-rebalance, and donation-routing recommendations. The Fabric-resident SOR carries the lot-level data; the agent runs in Foundry; the recommendation surfaces to a store manager in Teams Copilot with a one-tap accept. Audit attribution is at the lot level: a 30% markdown applied at 14:00 on lot LX-2207 is captured against the agent that recommended it.

### Labor productivity — the schedule-and-assignment agents

The agent-class is a **schedule-and-assignment optimizer** that aligns labor to demand at the department-half-hour grain. The substantive productivity gain is not in the schedule itself — it is in the substitution of routine merchandising knowledge work (planogram updates, replenishment, exception triage) with agent-assisted decisioning, freeing in-store associates for customer-facing time. The HITL gate sits at the manager approval of the schedule and at the associate accept of any agent-suggested task reassignment.

### Supplier-funded retail media — the CPG-collaboration agents

The agent-class is a **CPG-collaboration agent** that helps category managers respond to supplier-funded promotion proposals with elasticity-aware counter-offers, traceable participation history, and audit-row attribution from media spend through to incremental basket impact. This lever sits adjacent to 84.51° rather than inside it: 84.51° owns the segment and elasticity science; the agent layer owns the merchant-facing decision orchestration.

### Fresh-defect rate — the freshness-signal agents

The agent-class is a **freshness-signal agent** that fuses receiving condition, dwell time, temperature excursions (where instrumented), and customer return signals into a per-lot freshness score. The recommendation is rotation, repositioning, markdown, or pull. The Fabric Eventhouse carries the lot-level lineage; the agent issues recommendations; the HITL gate is the produce or meat manager's accept. This agent overlaps significantly with the FSMA 204 traceability service (RC-E2E-09) — the same lot-level lineage that satisfies the regulatory audit also feeds the freshness-signal agent.

## 2.3 Where APEX is most differentiated

Of the five levers, APEX is most differentiated on two for Kroger specifically: **Assortment & Pricing (RC-E2E-03)** and **Traceability (RC-E2E-09)**. The reasoning is not generic; it is Kroger-shaped.

**Assortment & Pricing differentiation.** Kroger's merchant decision cadence is weekly at the category level and daily at the price-point level. The decision volume is enormous — tens of thousands of SKU-store combinations per cycle. The 84.51° feature surface is mature but not decision-orchestrated; it produces segments, elasticities, and propensity scores, not approve-or-reject merchant queues. APEX's wedge is exactly the orchestration layer: a multi-agent pod that turns 84.51° science into a HITL-gated merchant queue, with every approval captured in an audit row that survives both internal finance challenge and external auditor review. No internal Kroger team is publicly known to have built that orchestration layer at production scale.

**Traceability differentiation.** FSMA 204 enforcement for the Food Traceability List takes effect January 2026; grocers have a hard regulatory wall against which to validate their lot-level supplier-to-store lineage. The wall is not optional and the timing is not negotiable. Most grocer programs are publicly described as in-flight rather than complete. APEX's wedge here is two-fold: a Fabric Eventhouse SOR that ingests supplier and receiving events at the lot grain with audit-row provenance, and a recall agent that turns the regulatory data into a 24-hour recall execution capability. Both are defensible in audit because the lineage is captured at the source, not reconstructed.

These two services share infrastructure — the same Bronze→Silver SOR, the same Purview classification, the same Entra identity boundary, the same Copilot HITL surface. That shared infrastructure is the structural reason Kroger gets a lower marginal cost on the second service than they would buying two separate programs.

## 2.4 The credibility test — what gets a CFO to take the meeting

A basis-point claim earns a CFO meeting only if it passes four tests. Sellers should run the test before the pitch, not in front of the CFO.

1. **Within published industry range.** A 150 bps assortment-and-pricing uplift on private-label dairy in 12 months is within the publicly-disclosed industry range (80-200 bps). A 600 bps uplift in the same window is laughable on its face.
2. **Attributable to a specific decision class.** "150 bps on private-label dairy from elasticity-aware promo participation across the top 200 dairy SKUs" is attributable. "150 bps from AI" is not.
3. **Defensible in audit.** Every claimed bp must be traceable through a recorded merchant decision, the agent recommendation behind it, the model version at the time, and the realized P&L delta. If the audit chain is broken, the claim is not defensible.
4. **Costed against a credible Wave-1 envelope.** A 150 bps uplift that requires a $50M build and 18 months of integration is not a credible Wave-1 claim. The envelope must match the claim's time horizon and the grocer's capital posture.

A worked example: **"150 bps margin uplift on private-label dairy in 12 months."** Credible if it is sourced to (a) the elasticity-aware promo participation decision class, (b) a Wave-1 envelope under $5M of build and discovery, (c) a HITL-gated merchant approval workflow whose audit rows survive finance review, and (d) a counterfactual (this-many-points-without-the-program) the grocer's own analytics team can replicate. Not credible if it is sourced to "AI optimization" with no attribution chain — that pitch dies inside the CFO office before reaching the merchant sponsor.

## 2.5 What Kroger's published numbers reveal

Kroger's publicly-disclosed gross margin and operating margin sit in the low end of their historical band, with persistent commentary in earnings calls about price-investment pressure, fresh shrink, and labor cost. The post-Albertsons window has added explicit investor pressure on organic margin: with the M&A path closed for the medium term, Kroger's CFO must produce margin progress through operations, technology, and category management — the three places where the five levers above live.

The implication is direct. **Assortment & Pricing** addresses the gross-margin line that earnings commentary returns to. **Shrink** addresses the cost-of-goods adjustment line that has visibly grown across the industry post-pandemic. **Labor productivity** addresses the SG&A line under FreshFlex pressure. **Retail media** is the high-margin revenue stream the investor community most rewards. **Fresh-defect rate** sits at the intersection of customer experience and shrink. All five are CFO-relevant; the first two are where APEX is most differentiated; the CFO is the gating stakeholder for any program at this scale, with the merchant and operations sponsors as the build-side counterparts.

> **Companion Artifacts**
> - [ROI Case](Services/RC-E2E-03_Assortment-and-Pricing/Tier1-Executive/APEX-RC-E2E-03-Kroger-ROI-Case.html) — interactive sensitivity that makes the basis-point claims tangible
> - [Cross-Grocer Comparison](Services/RC-E2E-03_Assortment-and-Pricing/Tier4-Strategic/APEX-RC-E2E-03-Cross-Grocer-Comparison.xlsx) — margin posture comparison across Kroger, Albertsons, Publix, HEB, Ahold
`,
  summary: [
    'Five margin levers; agentic AI moves each through different agent-classes',
    'Assortment & Pricing and Traceability are the two most-differentiated levers for APEX at Kroger',
    'Basis-point credibility is the gate — within range, attributable, defensible, costed',
    'CFO is the gating stakeholder; the post-Albertsons margin pressure is the open door',
  ],
  actions: [
    'Pre-build basis-point claims for your prospect category — within published range, attributable, defensible',
    'Rehearse the five-lever framing for the next CFO conversation',
    'Identify which of the five levers your sponsor cares about most before pitching',
  ],
});

chapters.push({
  num: 3, part: 1, title: 'APEX Wedge into the Kroger Estate',
  objectives: [
    'Describe the four-pillar Microsoft footprint at Kroger as it is publicly inferable',
    'Explain the coexistence pattern with 84.51° and Ocado in plain architectural terms',
    'Name the three integration seams APEX engages, with the data flow at each',
    'Recognize the two anti-patterns that have killed agentic-AI pitches at Kroger',
  ],
  body: `
> **Independence Reminder**
> The Kroger estate description in this chapter is reconstructed from publicly-available signals — earnings calls, public job postings, vendor press releases, and conference talks — as of 2026 Q1. Treat every architectural claim as a hypothesis to validate in discovery. The estate is mature in places (84.51° on GCP) and locked in others (Ocado-powered CFCs); APEX at Kroger is a wedge, not a re-platform, and the wedge has to thread the seams.

## 3.1 The four Microsoft pillars at Kroger today

Microsoft is one of multiple platforms in play at Kroger. Sellers should not overstate the Microsoft footprint; they should know it precisely and speak to it precisely. There are four pillars.

### Azure — the compute footprint

Kroger has a substantial publicly-inferable Azure footprint, visible in job postings, vendor announcements, and conference talks across the past three years. The footprint includes core enterprise workloads and a growing share of data-and-analytics consumption that does not sit inside the 84.51° GCP estate. **Discovery territory:** the specific Azure landing zones, the hybrid posture against on-premises Cincinnati workloads, and the share of data-and-analytics consumption that has migrated off legacy Hadoop into Azure-native services.

### Microsoft 365 — the broad enterprise

M365 is broadly deployed across the Kroger enterprise, including Teams as the collaboration backbone and Exchange Online for mail. This is the surface against which Copilot adoption decisions get made; it is also the surface against which Teams-embedded agent experiences land. **Discovery territory:** the specific Copilot-for-M365 license footprint, the Teams app-deployment governance posture, and which lines of business are pilot vs production.

### Foundry — the growing footprint

Azure AI Foundry adoption at Kroger is publicly inferable from job postings that periodically reference Foundry, agent orchestration, and model deployment on Azure. The footprint is growing rather than mature; the public signals suggest pilot and early-production posture rather than enterprise-wide deployment. **Discovery territory:** the specific Foundry workspaces in production, the model-governance posture, and the responsibility split between central AI platform and line-of-business teams.

### Fabric and Copilot — early-stage indicators

Microsoft Fabric and the broader Copilot family (Copilot Studio, Copilot for M365, Sales Copilot, Service Copilot) appear in public Kroger job postings and vendor commentary as growing but not yet enterprise-scale workloads. The signals point to early adoption with significant headroom. **Discovery territory:** which Fabric capacities are in production vs proof-of-concept, the OneLake adoption posture against the existing data estate, and whether Copilot Studio is the chosen agent-builder surface or whether Foundry is doing the orchestration work directly.

The aggregate read: Microsoft has air cover at Kroger but does not own the customer-data plane (84.51° on GCP does) and does not own the fulfillment-center plane (Ocado does). The wedge for APEX runs through the Microsoft pillars, but the architecture must coexist with the non-Microsoft surfaces.

## 3.2 Coexisting with 84.51°

84.51° is a wholly-owned Kroger subsidiary headquartered in Cincinnati, with internal political weight, a CPG-analytics revenue line, and a publicly-disclosed posture on Google Cloud Platform. Customer features — household segments, lifetime value, propensity scores, basket-affinity signals — are curated inside 84.51° and reach the broader enterprise as features and segments rather than as raw events. The MLOps practice is mature; the data stewardship is rigorous.

The architectural and political reality is the same: APEX must coexist with 84.51° rather than displace it. Pitches that sound like displacement get blocked at the data-stewardship gate before they reach the merchant or CFO sponsor. The wedge runs through three patterns: agent orchestration on top of 84.51°-curated features, HITL discipline that 84.51° has not built (because it is not their charter), and Microsoft-native business-application surfaces (Copilot, Teams) sitting on top of the science.

The boundary contract reads cleanly. **84.51° owns the customer features, segments, elasticities, and propensity scores.** Those flow to the agent layer via secure API or Fabric shortcut, with Purview classification mediating access. **The agent layer owns the decision orchestration, the HITL surface, the audit-row attribution, and the merchant-facing experience.** Each side does what it does best; neither side displaces the other; the contract is API-mediated and governed by Purview. That is the picture a 84.51° data steward can sign off on.

## 3.3 Coexisting with Ocado

The Ocado-powered customer fulfillment centers are a closed envelope. Ocado supplies its own software, warehouse-management system, and picking robotics; the contract is closed; the integration surface is narrow. Pitches that imply integration into the Ocado stack lose architectural credibility at the CIO level immediately, because the closed-envelope posture is well known.

The wedge is at the seam between CFC fulfillment and store-fulfilled BOPIS. CFCs serve Kroger Delivery; stores serve BOPIS pickup and last-mile substitution. On the store-fulfilled side, Kroger's own software — not Ocado's — handles substitution decisions, customer notifications, and exception management. **This is where the agent fleet attaches.** RC-E2E-03 (assortment and pricing decisions that ripple into store-fulfillment availability), the substitution agent, and the customer-notification orchestration all live on the store side of the seam. Inside the Ocado envelope, APEX has no business; outside it, the merchandising and fulfillment decisions are Kroger's own — and that is where agentic AI delivers value.

## 3.4 The three integration seams APEX engages

APEX engages the Kroger estate at exactly three seams. Each has a specific data flow and an RC service that lives on it.

### Seam 1 — Loyalty and customer features → Foundry

84.51°-curated features (household segments, propensity scores, basket-affinity, elasticity coefficients) reach merchant-facing agents in Foundry via a secure API surface, with Purview classification controlling field-level access by agent identity. The agent treats the features as inputs to the merchant-decision orchestration; it does not re-derive them and does not displace 84.51°. The relevant RC service is **RC-E2E-03 Assortment & Pricing Intelligence**.

### Seam 2 — FSMA 204 traceability → Fabric Eventhouse

Lot-level supplier data and store receiving events ingest directly into a Fabric Eventhouse, with the SOR carrying lineage from supplier shipment through receiving, store transfer, and POS scan. The Fabric Eventhouse is the system of record for the FSMA 204 audit obligation; the recall agent runs against it; the freshness-signal agent overlaps. The relevant RC service is **RC-E2E-09 Product Tracking & FSMA 204 Traceability**.

### Seam 3 — Merchant decisions → Copilot HITL

Agent recommendations surface to the merchant or store manager via Teams Copilot or Copilot Studio cards. The HITL gate captures approval, modification, or rejection along with reasoning; the audit row attaches the decision to the model version and the input features at the time. This is the experience surface; it is also the audit-defensibility surface. The relevant RC services are both anchors plus the Grocery Merchandising portfolio attaches.

## 3.5 Anti-pattern #1 — pitching a re-platform of 84.51°

The most common way to lose the Kroger conversation early is to pitch anything that sounds like displacement of 84.51°. The political weight is real: 84.51° is wholly-owned, headquartered in Cincinnati, has a CPG-analytics revenue line of its own, and carries internal sponsorship at the CEO level. Any pitch that implies the Microsoft platform should host the customer-data science, or that 84.51°'s feature store should migrate to Fabric, or that the GCP estate should be retired, gets blocked at the data-stewardship review before reaching the merchant or CFO sponsor.

The discipline is to lead with coexistence, name 84.51° explicitly as the upstream feature owner in the architecture, and frame the agent layer as the decision-orchestration tier that 84.51° was never chartered to build. Pitches that pass this test sustain the conversation; pitches that fail it stall in week two.

## 3.6 Anti-pattern #2 — pitching CFC integration through Ocado

The second most common way to lose is to pitch agent integration into the Ocado stack at the customer fulfillment centers. The CFC envelope is closed by contract and by architecture; Ocado supplies the software and the robotics; the integration surface is narrow and is governed by Ocado's own roadmap, not Kroger's. Pitches that propose substitution agents inside CFCs, or robotics-orchestration agents on the picking line, or warehouse-management agents at the CFC tier, lose architectural credibility immediately.

The discipline is to confine the agent fleet to the store side of the CFC-vs-store seam: store-fulfilled BOPIS, store-side substitution, store-side customer notification, and store-side exception management. Inside the Ocado envelope, the right answer is "Ocado's stack runs that"; outside it, the agent fleet has full play.

## 3.7 The architecture slide a CIO will accept

The one-slide picture a Kroger CIO will sign off on is straightforward in prose. **84.51° on GCP** holds the customer features and feeds them to the agent layer via secure API, with the API surface Purview-classified. **Foundry agents on Azure** orchestrate the merchant decisions, consuming both 84.51° features and the Fabric-resident operational SOR. **Fabric Eventhouse** holds the FSMA 204 traceability lineage, the POS streams, and the operational events the agents reason over; OneLake shortcuts and the Bronze→Silver pipeline stitch the data planes together without copying. **Copilot surfaces** — Teams cards, Copilot Studio experiences, Copilot for M365 — sit on top of both the agent layer and the Fabric semantic model, providing the HITL approval surface and the merchant-facing experience. **Purview** classifies everything and mediates field-level access; **Entra** is the identity plane that ties agents, users, and data classifications together.

The picture has Kroger's existing investments in their proper place (84.51° upstream, Ocado in its envelope, Microsoft as the decision-orchestration and experience plane), it has a single SOR for the operational data the agents need, and it has the governance plane explicit rather than implied. That is the slide a CIO can defend internally; it is also the slide that does not trigger either of the two anti-patterns.

> **Companion Artifacts**
> - [Solution Architecture Document](Services/Shared-Both-Services/Tier0-Foundation/APEX-RC-E2E-03-09-Solution-Architecture-Document.docx) — the full architecture treatment behind this chapter
> - [SOR ERD](Services/Shared-Both-Services/Tier0-Foundation/APEX-RC-E2E-03-09-SOR-ERD.html) — the entity-relationship picture for the operational SOR
> - [Service Roadmap](Services/Shared-Both-Services/Tier4-Strategic/APEX-RC-E2E-03-09-Service-Roadmap.html) — the multi-wave sequence that lives on these seams
`,
  summary: [
    'Four Microsoft pillars at Kroger — Azure, M365, growing Foundry, early Fabric/Copilot',
    'Coexist with 84.51° (customer features) and Ocado (CFC envelope) — never displace',
    'Three seams: 84.51° features → Foundry; FSMA 204 → Fabric Eventhouse; merchant decisions → Copilot HITL',
    'Two anti-patterns kill the pitch — re-platforming 84.51° or implying Ocado integration',
  ],
  actions: [
    'For your Kroger sub-org, map the four MS pillars and identify which is the strongest air cover',
    'Pre-validate your coexistence story with the Microsoft account team before pitching',
    'Stress-test your pitch deck against the two anti-patterns; remove anything that sounds like displacement',
  ],
});

module.exports = { all: chapters, appendices };
