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

// ---- PART II — THE SERVICE PORTFOLIO ----

chapters.push({
  num: 4, part: 2, title: 'The Two Anchors at a Glance',
  objectives: [
    'Describe RC-E2E-03 in one sentence',
    'Describe RC-E2E-09 in one sentence',
    'Explain why the two are co-anchored, not sold standalone',
    'Know when to lead with one vs the other based on the prospect\'s most-pressured executive',
  ],
  body: `
The two anchors share a substrate. RC-E2E-03 Assortment & Pricing Intelligence and RC-E2E-09 Product Tracking & FSMA 204 Traceability look like two different services on the surface — one is about merchant decisions, the other is about regulatory compliance — but underneath they sit on the same Bronze→Silver SOR, the same Fabric semantic model, the same Foundry agent fleet, and the same Purview governance plane. Together they define the Kroger entry: a Wave-1 envelope that earns the right to expand, an architecture story that survives CIO review, and a stakeholder coverage pattern that puts a Deloitte signature in front of every margin-relevant executive at Kroger inside the first nine months.

## 4.1 RC-E2E-03 in one sentence

**RC-E2E-03 turns 84.51° features and operational data into a HITL-gated stream of approve-or-reject merchant recommendations — assortment, pricing, promotion participation — surfaced to category managers in Copilot, with audit-row attribution at every recommendation that ties model version, agent rationale, merchant decision, and realized P&L delta into a single defensible chain.**

That one sentence carries a lot of weight. It says assortment, pricing, and promotion participation are inside the service, not adjacent to it. It says the recommendation surface is Copilot, which means the conversation about user adoption is a Microsoft conversation, not a custom-app conversation. It says HITL gates are at every recommendation, which means the program survives both internal finance challenge and external auditor review. And it says the audit row is the program's spine — every dollar of claimed margin must be traceable back through a recorded merchant decision, the model that informed it, and the features that fed the model. The merchant agents are the headline; the audit row is what makes the headline survive.

## 4.2 RC-E2E-09 in one sentence

**RC-E2E-09 ingests supplier, receiving, and store-event data into a Fabric Eventhouse at the lot grain, satisfies FSMA 204 traceability obligations across the five Critical Tracking Events, and runs a Foundry recall agent that turns the regulatory data into a 24-hour recall execution capability — with Purview lineage stamping every record so the audit chain is automatically defensible.**

The lot grain is the spine. FSMA 204 enforcement begins January 2026, which means by the time most pursuits land in front of a Kroger QA, Legal, or Operations executive in 2026, the regulatory clock is already counting down. The Eventhouse is the system of record; the recall agent is the workflow on top of it; the Purview lineage is what turns "we have the data" into "we can produce the data to the FDA in audit form within 24 hours of request." That last clause is the difference between a check-the-box compliance program and a defensible one — and for an industry that has watched class-action litigation follow every recent recall, the defensibility is the part the General Counsel cares most about.

## 4.3 Why the two are co-anchored

The two services are not sold standalone. They are co-anchored by design, and the design is structural rather than commercial. There are four shared infrastructure pieces.

**Shared SOR (Bronze→Silver).** Both services consume from the same operational system of record. Supplier data, receiving events, store-transfer records, POS streams, and lot-level lineage all land once in the Bronze layer, get conformed once in Silver, and serve both the merchant-decision agents (RC-E2E-03) and the recall and freshness agents (RC-E2E-09). Building the Bronze→Silver pipeline twice would be wasteful; building it once and serving both services is the architecture that survives CIO review.

**Shared semantic model in Fabric.** The Fabric semantic model — the lakehouse tables, the Direct Lake datasets, the OneLake shortcuts to 84.51°-curated features — is a single asset. Merchant agents and recall agents query against the same conformed dimensions (item, store, supplier, lot) and the same fact tables (sales, receiving, transfer). Maintaining one semantic model is materially cheaper than maintaining two; more importantly, it eliminates the cross-service data-divergence risk that destroys credibility in audit.

**Shared agent fleet (six core agents serve both).** The six core agents that ship with the program are not service-specific. The same Foundry workspace, the same agent registry, the same MCP server tier, and the same observability stack serve both anchor services. Adding a recall agent or a freshness agent to a workspace that already has the merchant-decision agents is a marginal-cost addition, not a separate build.

**Complementary stakeholder coverage.** RC-E2E-03 lands with the Chief Merchant and the CFO — the gross-margin conversation, the assortment and pricing program rhythm, the basis-point math. RC-E2E-09 lands with the Head of QA, the General Counsel, and the COO — the regulatory clock, the recall-execution defensibility, the litigation exposure. Selling both anchors covers every margin-relevant executive at Kroger; selling one covers half. The CEO conversation is materially easier with both anchors framed than with either one alone.

The economic argument for the co-anchor is direct. **The second anchor's marginal Wave-1 cost is 30-50% lower than a standalone build because the substrate is shared.** A grocer that buys RC-E2E-03 and then later decides to buy RC-E2E-09 separately will pay roughly two full Wave-1 envelopes. A grocer that buys the two as co-anchors pays Wave-1 plus an incremental delta — the delta covering the recall-agent build, the FSMA 204 lineage extension, and the Purview classification expansion, but not a duplicate Bronze→Silver pipeline, a duplicate semantic model, or a duplicate Foundry workspace. The discount is not a sales tactic; it is a structural artifact of the shared substrate, and it is the right way to frame the second anchor in a CFO conversation.

## 4.4 When to lead with RC-E2E-03

Lead with RC-E2E-03 when the most-pressured executive in the prospect's sub-org is the **Chief Merchant or the CFO**. The pitch language is the gross-margin language: assortment rationalization, private-label penetration, elasticity-aware promo participation, basis-point uplift on a named category. The wedge category is private label — the highest gross-margin category, the one Kroger publicly invests in most aggressively, and the one where elasticity-aware promo participation has the cleanest measurement. Open with private-label dairy, work outward from there.

The post-Albertsons margin pressure conversation is the door. The CFO needs basis-point progress; the Chief Merchant needs decision-velocity progress; the agents serve both. RC-E2E-03 puts a credible Wave-1 number in front of both ($500K–$1.2M envisioning + foundation, with the Wave-2 production envelope visible behind it), and lets the executive say yes to a small commitment that earns the right to a larger one.

## 4.5 When to lead with RC-E2E-09

Lead with RC-E2E-09 when the most-pressured executive is the **Head of QA, the General Counsel, or the COO**. The pitch language is the regulatory language: FSMA 204, the Food Traceability List, the five Critical Tracking Events, the 24-month retention obligation, the 24-hour FDA-response obligation. The wedge is the timing: FSMA 204 enforcement begins January 2026, which means by mid-2026 every grocer is either compliant, scrambling to be compliant, or exposed. There is no fourth posture.

The General Counsel conversation is qualitatively different from the CFO conversation. The GC cares about defensibility and litigation exposure, not basis points. The recall-execution scenario — "FDA Class II recall, lot-level scope, customer notification, end-to-end inside 24 hours" — is the demo that closes the GC. The COO conversation overlaps: recall execution at 24 hours is an operational capability, not just a regulatory one, and the COO who has to coordinate the recall is the same COO who has to defend the response time on the next earnings call.

## 4.6 Common infrastructure both rely on (preview of Part III)

Part III treats the architecture in depth across five chapters. As a preview, the five planes both anchor services rely on are:

- **System of Record (Bronze→Silver).** The conformed operational data layer. Supplier feeds, receiving events, transfer records, POS streams. Lot grain throughout. One system, two services.
- **Fabric.** The semantic model, the lakehouse, OneLake shortcuts to 84.51° features, Direct Lake datasets for sub-second query. The data plane both agent fleets reason over.
- **Foundry.** The agent runtime. Six core agents, MCP-mediated tool calls, prompt and model versioning, observability. The decision-orchestration tier.
- **MCP.** The tool-server tier that exposes Fabric data, 84.51° features, ServiceNow tickets, and Copilot surfaces to the agents through a single typed contract. The integration plane.
- **Purview.** The classification, lineage, and access-control plane. Field-level data governance, row-level filters by agent identity, automated lineage capture for FSMA 204 audit. The governance plane.

Each plane gets its own chapter in Part III, with the architecture, the runbook references, and the decisions Deloitte makes on Kroger's behalf at each layer. For now, the headline is that the same five planes serve both anchors — which is exactly what makes the co-anchor model work.

> **Companion Artifacts**
> - [Solution Architecture Document](Services/Shared-Both-Services/Tier0-Foundation/APEX-RC-E2E-03-09-Solution-Architecture-Document.docx) — the full architecture treatment for both anchors, end-to-end
> - [RC-E2E-03 Walkthrough](Services/RC-E2E-03_Assortment-and-Pricing/Tier0-Foundation/APEX-RC-E2E-03-Walkthrough.docx) — the foundational walkthrough for the Assortment & Pricing anchor
> - [FSMA 204 Compliance Checklist](Services/RC-E2E-09_Product-Tracking/Tier1-Executive/APEX-FSMA-204-Compliance-Checklist.docx) — the regulatory checklist that frames the RC-E2E-09 anchor
`,
  summary: [
    'Two anchors, one shared substrate; co-anchored by design',
    'RC-E2E-03 lands with Merchant/CFO; RC-E2E-09 lands with QA/Legal/Operations',
    'Lead-service decision turns on the most-pressured executive',
    'The second anchor is 30-50% cheaper at Wave-1 because the substrate is shared',
  ],
  actions: [
    'Identify the most-pressured executive in your sub-org and pick the lead service accordingly',
    'Rehearse the one-sentence framings until they land in 8-10 seconds each',
    'Map the cross-anchor narrative for stakeholders who span both worlds (the COO especially)',
  ],
});

chapters.push({
  num: 5, part: 2, title: 'RC-E2E-03 Assortment & Pricing Intelligence',
  objectives: [
    'Describe the six agents and the data each consumes/produces',
    'Walk the handoff sequence between the agents',
    'Identify the HITL gates and what each captures',
    'Quote a credible Wave-1 / Wave-2 / Wave-3 commercial envelope range',
  ],
  body: `
RC-E2E-03 is the assortment-and-pricing service in operational terms: it turns the merchant's "review 12,000 SKUs across 40 categories this week" problem into "approve, modify, or reject 200 priority recommendations this week, with the rationale and counterfactual surfaced inline." It is a multi-agent service running on Foundry, mediated by MCP, governed by Purview, and surfaced through Copilot. It is the service that, more than any other in the portfolio, gives a Kroger CFO a basis-point story they can defend in audit.

## 5.1 What the service does

In one paragraph: RC-E2E-03 ingests POS streams from the operational SOR, competitor pricing from licensed third-party feeds, supplier cost from the buyer-and-cost master, and 84.51° features (household segments, propensity scores, price-elasticity coefficients) from the customer-data subsidiary's API surface; reasons across them through a six-agent pod that scores margin exposure, models price-move impact, and composes ranked recommendations; surfaces the recommendations to category managers in Copilot with full rationale and counterfactual; captures HITL approval, modification, or rejection along with merchant reasoning; and measures the realized P&L delta against the recommendation in an audit row that ties model version, agent rationale, merchant decision, and realized outcome into a single chain. Every dollar of claimed margin is attributable through that chain, end to end.

## 5.2 The six agents

The six agents are not arbitrary. Each owns a decision boundary that a generalist single-model approach would either skip or get wrong. The decomposition is the architecture.

| Agent | Inputs | Outputs | Owns decision boundary |
|---|---|---|---|
| **Margin-Exposure Agent** | POS, supplier cost, current shelf price, category margin targets | Ranked list of SKU-store pairs by margin exposure (current vs target) | Where is gross margin at risk this cycle? |
| **Elasticity Agent** | 84.51° elasticity coefficients, historical price-test data, basket-affinity signals | Per-SKU price-move impact curves with confidence bands | What happens if we move this price 1%, 3%, 5%? |
| **Counter-Move Agent** | Competitor pricing feeds, banner positioning rules, KVI (Known Value Item) flags | Recommended response to a competitor move (match, ignore, undercut, repress) | How do we respond to a competitor's move on a watched SKU? |
| **Promo-Participation Agent** | Vendor-funded promotion proposals, supplier-spend history, elasticity outputs | Counter-offer structures and participation recommendations | Do we accept, modify, or decline this VFP proposal? |
| **Substitution-Pattern Agent** | Basket data, BOPIS substitution history, out-of-stock signals | Substitution acceptance rates per SKU pair, assortment-rationalization candidates | Which SKUs can we discontinue without losing the basket? |
| **Recommendation-Composer Agent** | All upstream agent outputs, merchant calendar, HITL acceptance history | Ranked merchant queue: top-N approve-or-reject items with rationale | Which 200 recommendations does the merchant see this week? |

The naming logic is decision-class-first; each agent name describes the decision it owns. The naming verifies against the canonical artifact (\`APEX-RC-E2E-03-Six-Agents-Deep-Dive-and-Maturation.docx\`), which carries the production names used in delivery. Sellers should treat these names as illustrative for narrative purposes; the deep-dive artifact is the source of truth for the production naming.

## 5.3 The handoff sequence

The agents run in a roughly sequential pipeline within a typical merchant cycle, with feedback loops where the composer asks earlier agents for refinement.

A normal weekly cycle looks like this. The **Margin-Exposure Agent** runs first against the freshest POS and cost data, producing a ranked list of where margin is most at risk against category targets. The **Elasticity Agent** consumes the at-risk list and overlays per-SKU price-move impact curves, narrowing the actionable subset. The **Counter-Move Agent** runs in parallel against competitor-pricing feeds, producing a list of competitor-driven response candidates. The **Promo-Participation Agent** runs against any open VFP proposals on the merchant's desk, scoring each against the elasticity outputs. The **Substitution-Pattern Agent** runs against the assortment side, flagging SKUs whose basket-substitutability allows discontinuation candidates. Finally, the **Recommendation-Composer Agent** consumes all five upstream outputs, deduplicates and prioritizes them against the merchant's calendar (e.g., this week's category review meeting), and produces the ranked queue of 100-300 recommendations the merchant sees in Copilot. The composer is the only agent whose output the merchant directly sees; the upstream five are visible to the merchant only as the rationale behind a specific recommendation.

The cycle is not strictly one-pass. The composer can call back to the elasticity agent or the counter-move agent for a what-if (e.g., "what does the recommendation look like if we drop the price by 2% instead of 4%?"), and the merchant's HITL decisions feed back into the composer's prioritization model for the next cycle. The cadence is weekly at the category level and daily at the price-point level, which means the agents run at different frequencies; the orchestration is in Foundry, the schedule is in the agent runtime, and the visibility is in Copilot.

## 5.4 The HITL gates

Every recommendation that reaches a merchant passes through a HITL gate. The gate is not a rubber stamp; it is the audit-row capture point. Four pieces of data are captured at every gate.

1. **Model version.** The exact version of each upstream agent that contributed to the recommendation, recorded as a hash. This is what makes the recommendation reproducible six months later when finance challenges the claimed P&L delta.
2. **Recommendation.** The full recommendation as presented to the merchant: the SKU, the proposed action (price move, promo response, assortment change), the predicted impact, the confidence band, and the counterfactual.
3. **Merchant decision.** Approve, modify (with the modification captured), or reject. Decisions are timestamped and attributed to the merchant's Entra identity.
4. **Override reason if any.** When a merchant modifies or rejects, a structured reason capture is required — not free text, but a small taxonomy of override classes (e.g., *upcoming-vendor-meeting*, *known-stock-issue*, *competitive-intelligence-not-in-feed*). The override taxonomy is a compounding asset; over time it tells the program where the agents are systematically blind.

The audit-row discipline is the spine. Every dollar of claimed margin must be attributable through the audit chain — model version, recommendation, decision, override (if any), and realized P&L delta. Without that chain, the basis-point claims do not survive the first finance challenge; with that chain, the program survives both internal challenge and external auditor review. This is the part of the program that distinguishes it from a generic "AI for pricing" pitch and the part that earns CFO sponsorship.

## 5.5 The three personas

Three personas use the Copilot surface day in and day out. Each gets a tuned experience.

**Category Manager.** A category manager (say, the dairy category manager) opens Copilot at 7:30 AM on Monday and sees a ranked queue of roughly 40-80 recommendations for the week — a mix of price moves, promo participation responses, and assortment-rationalization candidates, ordered by predicted P&L impact and tagged by upstream agent. They work through the queue across Monday and Tuesday, approving the obvious ones in bulk, modifying a handful where they have intelligence the agents do not have (e.g., an upcoming vendor meeting that changes the negotiation calculus), and rejecting a small number with a structured reason. By Tuesday afternoon the queue is cleared; by Wednesday the approved decisions are flowing into the pricing system; by the following Monday the realized impact is back in their dashboard, attributed by recommendation. They get back time and a defensible decision history; they give up the illusion of reviewing every SKU manually, which they were not actually doing anyway.

**Pricing Director.** The pricing director sees a different Copilot view — not individual SKU recommendations but a portfolio-level view across categories: which categories had the highest accept rates, which had the highest override rates and why, which competitor-driven responses were strongest, and what the realized vs predicted impact gap looks like. They use it for two things: weekly check-ins with the category managers (a more substantive conversation than the old "did you review the report" check-in), and quarterly model-tuning conversations with the delivery team. They get the portfolio visibility they have never had before; they give up the false comfort of a single price-strategy document that nobody followed.

**Private-Brand Lead.** The private-brand lead — owning Kroger's own-label portfolio across multiple categories — gets a third Copilot view focused on private-label-specific decisions: penetration trends, where private-label substitution is succeeding against national brands, which private-label SKUs are at margin risk, and which national-brand price moves create private-label opportunity. The private-brand lead's decisions feed back into the assortment-rationalization recommendations that other category managers see, creating a coordination loop the program makes explicit. They get a portfolio view of own-label margin levers; they give up running private-label as a parallel track separate from the broader category cycle.

Each persona's Copilot surface is tuned to their decision boundary. Each accepts or rejects different things. Each gets back different information. The single agent fleet underneath serves all three.

## 5.6 Commercial envelope

The commercial envelope is illustrative — three waves, sized to publicly-defensible ranges, calibrated to a Kroger-scale grocer. Replace with discovery-validated numbers before any client commitment.

**Wave 1 — $500K to $1.2M, 6-8 weeks.** Envisioning and foundation. Discovery sessions with the merchant, CFO, and IT sponsors; a one-category proof-of-concept (typically private-label dairy) running against historical data; a Fabric Eventhouse stand-up; a Foundry workspace with two of the six agents in narrow scope; the Purview classification baseline; and a pitch-grade ROI Case sized to the prospect's actual category footprint. The Wave-1 deliverable is the right to Wave 2 — a credible projected impact, a costed Wave-2 envelope, and an executive-sponsored go-no-go decision.

**Wave 2 — $4M to $8M, 6-9 months.** Full RC-E2E-03 production deployment plus one or two high-attach services from the catalog in Chapter 7 (most commonly Markdown Optimization and Demand Forecasting, both of which feed naturally into the merchant-decision pipeline). All six agents in production, the full Bronze→Silver SOR, the Fabric semantic model, the MCP server tier, Purview lineage and classification across the data plane, and the Copilot surfaces tuned for all three personas. Wave 2 is where the basis-point claims become realized basis points.

**Wave 3 — $10M to $25M, 12-24 months.** Banner extension and cross-anchor expansion. RC-E2E-03 extends to additional banners (Marketplace, Fred Meyer, Mariano's, Harris Teeter); RC-E2E-09 lands as the second anchor; additional high-attach services come on; and the program enters the at-scale operating cadence covered in Part V. Wave 3 is the program in steady state — the largest envelope, but also the lowest unit cost of incremental capability because the substrate is now mature.

These ranges are illustrative. The actual envelope for any prospect depends on the number of banners, the number of categories in scope, the existing data-platform maturity, and the Microsoft licensing posture. Pre-tune the envelope to the specific Kroger conversation before pitching.

## 5.7 Three illustrative use cases

Three quick scenarios, one per persona, in Sellers Guide format.

**Cassidy, dairy category manager — private-label whole milk pricing response.** *Pain:* Competitor moved private-label whole-milk gallon down 5% in three banners over the weekend. Cassidy historically would not see this until Wednesday's competitive-pricing report. *Agent action:* The Counter-Move Agent picked up the move from the Sunday-morning pricing feed; the Elasticity Agent modeled three response scenarios (match, undercut by 2%, hold); the Composer surfaced the recommendation to Cassidy at 7:30 AM Monday with a recommended hold (the elasticity model says volume risk is low because basket affinity is high) and a fallback match-on-Day-3 if the competitor sustains the move. *HITL decision:* Cassidy approved the hold-with-fallback. *Outcome:* Margin protected through the week; the realized basket data on the following Monday matched the elasticity-model prediction within the confidence band.

**Devon, pricing director — quarterly model-tuning conversation.** *Pain:* Devon historically had no portfolio-level visibility into where category managers were overriding the pricing models, which made model improvement guesswork. *Agent action:* The Composer Agent's override-reason taxonomy surfaced a pattern across deli categories — a specific override class ("upcoming-vendor-meeting") spiked in the trailing six weeks, suggesting the supplier-cost feed was running stale relative to vendor-negotiation cadence. *HITL decision:* Devon scheduled a working session with the deli managers and the data team to refresh the supplier-cost feed cadence. *Outcome:* Override rate in deli dropped 40% in the following four weeks; recommendation accept rates improved correspondingly.

**Pat, private-brand lead — assortment rationalization.** *Pain:* Pat had a list of 60 private-label SKUs in slow-moving categories that finance wanted rationalized, but no clean way to predict basket impact of discontinuation. *Agent action:* The Substitution-Pattern Agent scored each SKU's basket-substitutability against neighboring private-label and national-brand SKUs; the Composer surfaced the top 20 candidates with predicted basket-loss percentages. *HITL decision:* Pat approved 14 discontinuations and held back 6 where the substitution model was below confidence threshold for further discovery. *Outcome:* SKU count down 14, basket impact below 0.3% in the following quarter (within model prediction), shelf space reallocated to higher-velocity own-label items.

## 5.8 What the underlying artifacts give you

Seven artifacts cover the service from narrative through commercial through technical. Each gives the seller a different angle.

- **Walkthrough** gives narrative depth — the long-form story of what the service does, in voice that a non-technical executive can read in an evening.
- **Six Agents Deep Dive and Maturation** gives technical depth — the agent-by-agent specification, the maturation roadmap from pilot to production, and the governance posture for each.
- **Use Case Catalog** gives breadth — a structured catalog of the use cases the service addresses across categories and personas, with measurable outcomes for each.
- **Service Sequence Diagram** gives the architecture view — the request-and-response flow from POS event through agent reasoning through Copilot HITL through pricing-system commit.
- **ROI Case** gives the commercial frame — interactive sensitivity on the basis-point math, sized to the prospect's actual category footprint.
- **Personas** gives the executive-engagement frame — a per-persona profile that the seller can use to prepare for a specific stakeholder conversation.
- **One-Pager** gives the leave-behind — the single-page executive summary that walks out of the meeting in the executive's hand.

> **Companion Artifacts**
> - [Walkthrough](Services/RC-E2E-03_Assortment-and-Pricing/Tier0-Foundation/APEX-RC-E2E-03-Walkthrough.docx) — the foundational service walkthrough
> - [One-Pager](Services/RC-E2E-03_Assortment-and-Pricing/Tier1-Executive/APEX-RC-E2E-03-Kroger-OnePager.html) — executive summary for leave-behind
> - [Personas](Services/RC-E2E-03_Assortment-and-Pricing/Tier1-Executive/APEX-RC-E2E-03-Kroger-Personas.html) — Category Manager, Pricing Director, Private-Brand Lead profiles
> - [Six Agents Deep Dive and Maturation](Services/RC-E2E-03_Assortment-and-Pricing/Tier2-Build/APEX-RC-E2E-03-Six-Agents-Deep-Dive-and-Maturation.docx) — agent-by-agent technical specification
> - [Use Case Catalog](Services/RC-E2E-03_Assortment-and-Pricing/Tier2-Build/APEX-RC-E2E-03-Use-Case-Catalog.xlsx) — structured catalog across categories and personas
> - [Service Sequence Diagram](Services/RC-E2E-03_Assortment-and-Pricing/Tier2-Build/APEX-RC-E2E-03-Service-Sequence-Diagram.html) — request-and-response flow architecture
> - [ROI Case](Services/RC-E2E-03_Assortment-and-Pricing/Tier1-Executive/APEX-RC-E2E-03-Kroger-ROI-Case.html) — interactive commercial sensitivity
`,
  summary: [
    'Six agents; HITL throughout; audit-row discipline at every gate',
    'Three personas; each gets a Copilot surface tuned to their decisions',
    'Wave 1 / 2 / 3 envelopes give the commercial frame, in illustrative ranges',
    'Seven companion artifacts cover narrative through commercial through technical',
  ],
  actions: [
    'Memorize the six-agent narrative end-to-end',
    'Rehearse the persona day-in-the-life for whichever persona is in your next meeting',
    'Pre-tune the wave envelopes for your specific Kroger conversation',
  ],
});

chapters.push({
  num: 6, part: 2, title: 'RC-E2E-09 Product Tracking & FSMA 204 Traceability',
  objectives: [
    'Describe FSMA 204 in regulatory plain English',
    'Identify the five Critical Tracking Events (CTEs) and the Key Data Elements (KDEs) for each',
    'Explain how RC-E2E-09 closes the four most-exposed grocer gaps',
    'Recognize the litigation and customer-trust upside that sits on top of regulatory compliance',
  ],
  body: `
FSMA 204 is the regulatory wedge that opens the QA, Legal, and Operations door at any US grocer in 2026. It is timing-pressured (enforcement begins January 2026), it is non-discretionary (the FDA does not negotiate the rule), and it is operationally exposing — most US grocers' supplier-to-store traceability chains have publicly-inferable gaps that FSMA 204 will surface the moment the first request-for-records lands. RC-E2E-09 Product Tracking & FSMA 204 Traceability is the service that closes those gaps with a Fabric Eventhouse SOR, a Foundry recall agent, and Purview lineage that makes the audit chain automatically defensible.

## 6.1 FSMA 204 in one paragraph

FSMA 204 is Section 204 of the FDA Food Safety Modernization Act, codified in the final rule under 21 CFR Part 1, Subpart S. It applies to every entity in the supply chain that manufactures, processes, packs, or holds a food on the **Food Traceability List (FTL)** — a defined list that includes leafy greens, fresh herbs, melons, peppers, sprouts, tomatoes, tropical tree fruits, several cheeses, deli salads, nut butters, certain seafood, and other high-risk categories. Compliance enforcement begins **January 2026**, after a two-year extension from the original 2024 date. Covered entities must capture defined Key Data Elements at each Critical Tracking Event, retain the records for a minimum of 24 months, and produce an electronically-sortable spreadsheet of the records to the FDA within 24 hours of request. The rule is operational, not advisory; the timing is binding; and the format requirement (electronically-sortable spreadsheet) is exactly the kind of obligation that exposes any grocer whose lot-level data lives in disconnected systems.

## 6.2 The five Critical Tracking Events (CTEs)

The rule defines five Critical Tracking Events. At each CTE, the covered entity must capture the defined KDEs and retain them for the minimum 24 months.

1. **Growing/Harvesting.** The source CTE for fresh produce, seafood (capture/landing for wild-caught, harvest for aquaculture), and other primary commodities. KDEs identify the source farm, harvest date, and grower.
2. **Transformation.** The CTE for any change to a food on the FTL — cutting, chopping, slicing, repackaging, combining with other foods. Each transformation creates a new lot with its own Traceability Lot Code (TLC) and links back to the input lot(s).
3. **Creation.** The CTE for the first making of an FTL food that is not the result of growing or harvesting (e.g., cheese aged from milk, salads built from washed greens). Like transformation, creation generates a new TLC and links back to inputs.
4. **Shipping.** The CTE for any shipment of an FTL food from a covered location. KDEs identify the immediate receiver, the shipping date, the TLC, and the quantity.
5. **Receiving.** The CTE for any receipt of an FTL food at a covered location. KDEs identify the immediate previous source, the receiving date, the TLC, and the quantity.

Sellers should be able to recite these in order. The CTE order is the spine of any FSMA 204 conversation; getting the order wrong loses credibility with a QA executive immediately.

## 6.3 The KDE checklist (what data each CTE must carry)

The Key Data Elements vary by CTE, but the categories are consistent. Sellers should know the table.

| CTE | Required KDEs | Retention | Format |
|---|---|---|---|
| Growing/Harvesting | TLC, source location identifier, harvest date, grower business name | 24 months minimum | Electronically-sortable spreadsheet on FDA request |
| Transformation | New TLC, input TLC(s), transformation date, new product description, location | 24 months minimum | Electronically-sortable spreadsheet on FDA request |
| Creation | New TLC, input source(s), creation date, new product description, location | 24 months minimum | Electronically-sortable spreadsheet on FDA request |
| Shipping | TLC, ship date, ship-from location, ship-to location, quantity, product description | 24 months minimum | Electronically-sortable spreadsheet on FDA request |
| Receiving | TLC, receive date, receive-from location, receive-at location, quantity, product description | 24 months minimum | Electronically-sortable spreadsheet on FDA request |

The 24-hour FDA-request response time is the part that exposes most grocers. Having the data is necessary but not sufficient — the data has to be retrievable, queryable, and producible in the required format inside one business day. That is a Fabric query, not a paper-records hunt.

## 6.4 TLC discipline — the Traceability Lot Code as the spine

The **Traceability Lot Code** is the unique identifier that threads every CTE. A new TLC is generated at growing/harvesting, at transformation, and at creation; the same TLC carries through shipping and receiving until the next transformation or creation event. The lot is the smallest unit of recall execution: when the FDA orders a recall, the scope is defined by TLC, and the grocer's job is to identify every store, every customer transaction, and every remaining inventory unit associated with the recalled TLC inside the 24-hour clock.

If TLC discipline breaks, the regulatory chain breaks. The most common gap is at the receiving CTE: a supplier sends a TLC on the bill of lading, but the receiving system captures only the supplier name and date, not the TLC. When the recall lands two months later, the grocer cannot tie the recalled lot back to the specific receipt and therefore cannot scope the impact. The fix is operational and architectural — the Fabric Eventhouse must ingest the TLC from the receiving event, not reconstruct it after the fact. RC-E2E-09 builds the TLC capture at receiving as a non-negotiable design constraint.

## 6.5 24-month retention — the compliance constraint

The FDA's 24-month minimum retention is straightforward to satisfy in storage cost; the operational constraint is the audit posture. The data must be:

- **Retrievable within 24 hours of FDA request.** No "we have it on backup tape" answers. The data has to be queryable in production systems, not archived offline.
- **Queryable by TLC.** A request will name a TLC; the system must be able to pull every CTE record associated with that TLC across the full 24-month window in a single query.
- **Producible in electronically-sortable spreadsheet format.** The FDA defines the format. The grocer's responsibility is to be able to generate the file on demand — not to ask for an extension while the data team builds an export.
- **Defensible in audit.** The records must carry lineage that proves they were captured at the source, not reconstructed after the request. Reconstructed records will not survive an FDA inspection.

Fabric Eventhouse is the storage and query plane that meets all four constraints by design. Purview lineage is what proves the records were captured at the source. The combination is the architectural answer to the 24-month-retention obligation, and it is what RC-E2E-09 ships.

## 6.6 Where US grocers have publicly-inferable gaps

US grocer FSMA 204 readiness is uneven across the industry. The four publicly-inferable gap categories are well known to anyone tracking the regulatory commentary; where Kroger specifically sits within these categories is discovery territory.

- **Produce, especially leafy greens and bagged salads.** Ready-to-eat, short shelf life, and recurring source of FDA recall activity. The supplier-to-store TLC chain for bagged-salad converters is publicly described as inconsistent across the industry, and the receiving-CTE capture is the most-exposed point.
- **Dairy, especially soft cheeses and infant formula by lot.** Soft cheeses are on the FTL; infant formula carries lot-level recall sensitivity even where not directly on the FTL. The transformation CTE (cheese aging, repackaging) is where lineage commonly breaks.
- **Seafood, especially shellfish and tuna.** Shellfish carry harvest-tag chain-of-custody requirements; tuna carries species-substitution risk. The growing/harvesting CTE for wild-caught seafood is exposing because the source data lives outside the grocer's systems and must be ingested faithfully.
- **Ready-to-eat prepared foods.** Deli salads, prepared sandwiches, and other in-store-prepared foods involve creation and transformation CTEs at the store level — the grocer is the covered entity, not just a downstream receiver, and the in-store data capture is publicly described as inconsistent.

Where Kroger sits across these four is discovery territory; the seller's job is to ask the QA executive directly, not to assume.

## 6.7 How RC-E2E-09 closes the gaps

RC-E2E-09 closes the gaps with three architectural moves.

**Fabric Eventhouse ingests at lot grain.** Supplier feeds (advance shipping notices, bills of lading), receiving events (DC and store), transformation events (in-store kitchen, deli prep), and POS scans land directly into the Fabric Eventhouse with the TLC captured at the source. The Eventhouse is the single source of record for FSMA 204 lineage; downstream services (recall agent, freshness-signal agent) query against it. No reconstruction, no after-the-fact joining, no "we'll figure it out when the recall lands."

**Foundry recall agent queries the Eventhouse for impact scoping in seconds.** When a recall is initiated, the recall agent takes a TLC (or a supplier-name + date-range) as input and produces three outputs in seconds: every store that received the lot, every customer transaction that touched the lot (loyalty-attributed where possible, anonymous otherwise), and every remaining inventory unit. The agent then orchestrates the downstream actions: store-level pull notifications via Teams, customer notifications via the loyalty channel, and the FDA-format export of the lineage records.

**Purview lineage stamps every record so the audit chain is automatically defensible.** Every record in the Eventhouse carries Purview lineage from source ingestion through every transformation. When the FDA inspector asks "how do you know this record reflects the actual receiving event," the answer is in the Purview lineage — captured automatically, not constructed manually. This is what turns "we have the data" into "we can defend the data."

A short recall scenario makes the architecture concrete. **Class II FDA recall on infant formula, lot LX-IF-2207, initiated Tuesday 09:00.** The recall agent receives the lot identifier at 09:02. By 09:08 the agent has identified 412 stores that received the lot, 11,847 loyalty-attributed customer transactions, and 2,304 remaining inventory units across the network. By 09:30 store-pull notifications have hit every receiving store via Teams and have been acknowledged by 380 of 412. By 11:00 the loyalty notifications have been queued through the customer-communications channel. By 14:00 the FDA-format lineage export is ready for submission. End-to-end inside the same business day; all steps timestamped, attributed, and Purview-lineage-defensible.

## 6.8 The litigation and customer-trust upside

The regulatory compliance is the floor, not the ceiling. The second-order value of RC-E2E-09 is what closes the General Counsel.

**Foreign-object pattern detection.** A single customer report of a foreign object in a deli salad at one store is not by itself meaningful. The same report on the same SKU at three sister stores within 48 hours is a pattern — and the agent fleet built on the lot-level Eventhouse can identify the pattern automatically, scope the affected lots, and prompt a proactive pull at all stores receiving the implicated lots before the fourth report lands. The legal calculus is direct: every customer who never received an exposed product is a customer the grocer never has to defend against in litigation, and every store that pulls the product proactively is a store the regulator never has to investigate. The General Counsel quantifies this in expected-value terms, and it lands.

**Recall response defensibility.** When a recall is contested in litigation — and meaningful recalls usually are — the question the plaintiff's counsel asks is "what did you know, when did you know it, and what did you do about it." A grocer who answers from a Fabric Eventhouse with Purview lineage produces a defensible evidence package. A grocer who answers from reconstructed spreadsheets produces a target. The General Counsel's risk model on the recall-defense exposure is large — large enough that even a modest reduction in time-to-defense changes the legal-quantified risk number meaningfully. Sellers who carry the recall-defense scenario into the GC conversation close the GC.

> **Companion Artifacts**
> - [FSMA 204 Compliance Checklist](Services/RC-E2E-09_Product-Tracking/Tier1-Executive/APEX-FSMA-204-Compliance-Checklist.docx) — the regulatory checklist for the QA and Legal stakeholder
> - [Solution Architecture Document](Services/Shared-Both-Services/Tier0-Foundation/APEX-RC-E2E-03-09-Solution-Architecture-Document.docx) — the full architecture treatment, both anchors
> - [Fabric Runbook](Services/Shared-Both-Services/Tier2-Build/APEX-RC-E2E-03-09-Fabric-Runbook.docx) — Fabric Eventhouse build guide for the FSMA 204 SOR
`,
  summary: [
    'FSMA 204 is the regulatory wedge; January 2026 enforcement makes it timing-pressured',
    'Five CTEs + KDEs + TLC + 24-month retention is the compliance shape',
    'RC-E2E-09 closes the gaps with Fabric Eventhouse + Foundry recall agent + Purview lineage',
    'Litigation defensibility and customer trust are the second-order values that close the General Counsel',
  ],
  actions: [
    'Memorize the five CTEs in order',
    'Pre-build the recall scenario for the QA/Legal stakeholder you\'re meeting next',
    'Map your prospect\'s gap categories to the four publicly-inferable gap patterns',
  ],
});

chapters.push({
  num: 7, part: 2, title: 'The High-Attach Catalog — Six Services that Attach to the Two Anchors',
  objectives: [
    'Name the six high-attach RC services in the Grocery Merchandising portfolio',
    'Tier-rank the eight-service portfolio (two anchors + six attach + zero peripheral)',
    'Identify which attach to RC-E2E-03 vs RC-E2E-09 vs both',
    'Sequence wave-2 and wave-3 attach decisions',
  ],
  body: `
The two anchors are the front door. They earn the executive sponsorship, they prove the architecture, and they put basis-point progress on the CFO's scorecard inside Wave 2. The high-attach catalog is what scales the program after Wave 1 closes — six additional services that share the substrate, attach to the anchors at well-understood seams, and turn an anchor pursuit into a multi-year platform program. The canonical source for the portfolio is \`APEX-RC-Grocery-Merchandising-Service-Portfolio.docx\`, which carries the production naming and tier-ranking; this chapter tells the seller-side story of how the portfolio sequences in front of a Kroger CFO.

## 7.1 The Grocery Merchandising portfolio at a glance

The Grocery Merchandising portfolio is intentionally tight. Eight services total — two anchors, six high-attach, and (deliberately) zero peripheral services. The portfolio is shaped this way because every service in it shares the substrate; anything that does not share the substrate lives in an adjacent practice (Supply Chain, Stores, Customer) and gets sold separately.

| Service code | Service name | Tier | Attaches to | Typical Wave introduction |
|---|---|---|---|---|
| RC-E2E-03 | Assortment & Pricing Intelligence | 1 (anchor) | n/a | Wave 1 |
| RC-E2E-09 | Product Tracking & FSMA 204 Traceability | 1 (anchor) | n/a | Wave 1 (co-anchor) |
| RC-TTP-11 | Markdown Optimization | 2 (high-attach) | RC-E2E-03 + RC-E2E-09 | Wave 2 |
| RC-TTP-12 | Promotion Effectiveness | 2 (high-attach) | RC-E2E-03 | Wave 2 |
| RC-TTP-13 | Vendor Funded Promotion (VFP) Management | 2 (high-attach) | RC-E2E-03 | Wave 2 |
| RC-TTP-14 | Demand Forecasting | 2 (high-attach) | RC-E2E-03 (primarily) | Wave 2 |
| RC-TTP-15 | Replenishment Optimization | 2 (high-attach) | RC-E2E-03 + RC-E2E-09 | Wave 3 |
| RC-TTP-16 | Substitution Intelligence | 2 (high-attach) | RC-E2E-03 (and the BOPIS seam) | Wave 3 |

*Service codes and names verify against the Grocery Merchandising Service Portfolio artifact in the Companion Artifacts section.* The TTP suffix denotes "tools, techniques, processes" — services that ride on top of the E2E anchors rather than standing as full end-to-end services on their own. This is exactly the property that makes them high-attach: each TTP service consumes data, agents, and governance from the anchors and adds a focused decision class on top.

## 7.2 Tier 1 — the anchors (RC-E2E-03 + RC-E2E-09)

Recap from Chapters 5 and 6. RC-E2E-03 is the merchant-decision orchestration on top of 84.51° features and operational data, surfaced through Copilot, governed by audit-row discipline. RC-E2E-09 is the lot-level traceability and recall-execution capability built on the Fabric Eventhouse, satisfying FSMA 204 and turning the regulatory data into a litigation-defensibility asset. The two are non-substitutable in the portfolio because they are the two services that earn the executive sponsorship — the CFO/Merchant on one side, the QA/Legal/COO on the other. Without one or both anchors, the high-attach catalog has no executive attachment point.

## 7.3 Tier 2 — high-attach (six services)

Each high-attach service is defined by its decision class, the anchor it attaches to, and the reason it makes a Wave-2 candidate.

**RC-TTP-11 Markdown Optimization.** Decision class: when, where, and how deeply to mark down perishables to clear inventory before spoilage. Attaches to both anchors — the merchant-decision substrate from RC-E2E-03 supplies elasticity and basket-affinity; the lot-grain Fabric Eventhouse from RC-E2E-09 supplies the receiving-date and remaining-shelf-life signal. Wave-2 candidacy is the strongest in the catalog because markdown optimization has the highest measurable margin impact at the lowest integration risk; the agent runs in a closed loop with the merchant queue and the perishable inventory data already in scope.

**RC-TTP-12 Promotion Effectiveness.** Decision class: post-event measurement and learning loop on every promotion run, with attribution back to elasticity coefficients and competitor-response data. Attaches to RC-E2E-03 — the same six-agent fleet, with an additional measurement-and-learning agent that closes the loop between predicted and realized promotion impact. Wave-2 candidacy is strong because it tunes the existing agents (the elasticity model improves with every promotion-effectiveness cycle) and produces a CFO-ready dashboard of which promotions paid off.

**RC-TTP-13 Vendor Funded Promotion (VFP) Management.** Decision class: which vendor-funded promotion proposals to accept, modify, or decline, and how to structure counter-offers. Attaches to RC-E2E-03 — the Promo-Participation Agent in the six-agent fleet is the foundation; VFP Management adds the supplier-facing workflow, the contract-management surface, and the audit trail of supplier interactions. Wave-2 candidacy is strong because the supplier-funded media line is the highest-margin revenue stream in modern grocery (see Chapter 2), and the agents move it materially.

**RC-TTP-14 Demand Forecasting.** Decision class: SKU-store-day demand prediction at the granularity needed for both replenishment and merchant decisioning. Attaches to RC-E2E-03 primarily — the elasticity and basket-affinity agents need credible demand signal as input; bringing demand forecasting in-portfolio means the upstream signal is owned by the same team that owns the downstream decision. Wave-2 candidacy is strong because it feeds the merchant agents from the inside; without disciplined demand forecasting, the merchant agents are reasoning over noisier inputs than they could be.

**RC-TTP-15 Replenishment Optimization.** Decision class: when and how much to reorder at each store and DC, balancing service level, working capital, and shrink risk. Attaches to both anchors — RC-E2E-03 supplies the merchant-decision substrate, RC-E2E-09 supplies the lot-grain receiving and shelf-life data. Wave-3 candidacy because the integration with the supplier and DC systems is heavier than the other Tier-2 services, and the operational change-management is more substantial; the value is real but the build is longer.

**RC-TTP-16 Substitution Intelligence.** Decision class: which substitutions to offer in BOPIS and Kroger Delivery store-fulfilled orders when the requested item is out of stock. Attaches to RC-E2E-03 (the Substitution-Pattern Agent in the six-agent fleet is the foundation) and to the BOPIS seam (Chapter 3, Seam 3). Wave-3 candidacy because the customer-experience seam involves the loyalty and customer-communication systems — surfaces that need cross-team coordination beyond the merchant org. High value (closes the customer-experience seam) but more cross-functional than Wave-2 services.

## 7.4 Tier 3 — peripheral (none in the publicly-known catalog)

The Grocery Merchandising portfolio is intentionally tight. There is no Tier-3 peripheral category — services that look related but do not share the substrate live in adjacent practices and get sold separately. **Customer-experience services** (loyalty analytics, personalization, marketing automation) are 84.51°-owned territory and pursued through a different motion. **Supply-chain services** (DC operations, transportation, inbound logistics) imply Ocado-stack adjacency for CFC-related work and live in the Supply Chain practice for non-CFC work. **Store-operations services** (workforce management, planogram execution, in-store marketing) live in the Stores practice. The discipline is to keep the Grocery Merchandising portfolio focused on merchant and category-management decisions; bundling outside that boundary degrades the pitch.

## 7.5 The wave-2 attach sequence (typical)

The typical Wave-2 attach sequence puts three of the six high-attach services on the table.

**First attach: RC-TTP-11 Markdown Optimization.** Highest measurable margin impact, lowest integration risk, fastest time to realized basis points. Markdown is a closed-loop decision class with a tight feedback cycle (mark down today, observe the sell-through this week), which means the model learns fast and the realized vs predicted gap closes quickly. This is the attach that proves the Wave-2 expansion is paying off.

**Second attach: RC-TTP-14 Demand Forecasting.** Feeds the merchant agents from the inside. The elasticity and basket-affinity models have been running on existing demand inputs through Wave 1 and early Wave 2; bringing demand forecasting in-portfolio means the merchant agents reason over a cleaner signal. The realized impact shows up as improved accept rates and tighter realized-vs-predicted gaps on the merchant agents — a credibility multiplier on RC-E2E-03 itself.

**Third attach (sometimes Wave 2, sometimes early Wave 3): RC-TTP-12 Promotion Effectiveness or RC-TTP-13 VFP Management.** Both attach to the Promo-Participation Agent. Promotion Effectiveness is the measurement-and-learning loop; VFP Management is the supplier-facing workflow on top. Sequence depends on prospect priorities — a supplier-revenue-pressured CFO will lead with VFP; a merchant-team-pressured Chief Merchant will lead with Promotion Effectiveness.

The sequencing rationale is not arbitrary: it is decision-impact ordered, integration-risk ordered, and credibility-multiplier ordered. The first two attaches (Markdown, Demand Forecasting) build credibility for the third, and the third builds the case for Wave 3.

## 7.6 The wave-3 attach sequence (typical)

Wave 3 is extension. The remaining high-attach services come on (Replenishment Optimization, Substitution Intelligence), the program extends to additional banners (Marketplace, Fred Meyer, Mariano's, Harris Teeter), and additional categories come into scope (general merchandise, pharmacy where appropriate). The substrate carries the marginal cost down; the operating cadence (Part V) is in steady state by mid-Wave-3.

The banner-extension argument is straightforward. The Bronze→Silver SOR, the Fabric semantic model, the Foundry agent fleet, and the Purview governance all operate at the enterprise scale by design; extending to a new banner is configuration and tuning, not re-platform. The Cross-Grocer Comparison logic (Chapter 8) eventually applies inside Kroger as much as it applies across grocers — different banners have different category mixes and different customer behaviors, and the agents tune to each.

## 7.7 What NOT to bundle

There are services that look related but degrade the pitch when bundled. Sellers should know the rule.

**Customer-experience services that cross the 84.51° boundary.** Loyalty analytics, personalization, customer-segment marketing — all 84.51°-owned. Bundling these into the Grocery Merchandising pitch triggers the displacement anti-pattern from Chapter 3 and gets blocked at the data-stewardship gate. The right pattern is coexistence: 84.51° owns the customer plane; the agents consume curated features from it; the pitch respects the boundary.

**Supply-chain services that imply Ocado-stack integration.** Customer Fulfillment Center optimization, picking-line orchestration, robotics-orchestration agents — all inside the Ocado envelope. Bundling these triggers the CFC-integration anti-pattern from Chapter 3 and loses architectural credibility immediately. The right pattern is store-side scope: the agents work on the store side of the CFC-vs-store seam, not inside the CFC envelope.

**The naming rule.** *Anything that crosses the 84.51° or Ocado boundary needs a separate pursuit motion, not an attach.* This is the seller's discipline; pre-clear bundling decisions with the lead partner before pitching anything that approaches either boundary.

> **Companion Artifacts**
> - [Grocery Merchandising Service Portfolio](Services/Shared-Both-Services/Tier0-Foundation/APEX-RC-Grocery-Merchandising-Service-Portfolio.docx) — the canonical eight-service portfolio document
> - [Service Roadmap](Services/Shared-Both-Services/Tier4-Strategic/APEX-RC-E2E-03-09-Service-Roadmap.html) — the wave-by-wave sequence across the portfolio
`,
  summary: [
    'Eight services tiered: two anchors + six high-attach',
    'Tier-2 attach drives Wave-2 expansion at lower marginal cost',
    'Wave-3 is banner and category extension',
    'Don\'t bundle services that cross 84.51° or Ocado boundaries',
  ],
  actions: [
    'For your specific prospect, identify the most-likely Tier-2 attach',
    'Rehearse the wave-2 sequencing rationale',
    'Pre-clear bundling decisions with the lead partner before pitching',
  ],
});

chapters.push({
  num: 8, part: 2, title: 'Cross-Grocer Differentiation — Kroger vs Albertsons / Publix / HEB / Ahold',
  objectives: [
    'Describe how the five major US grocers differ on data and AI posture',
    'Identify the three Kroger characteristics that most shape the pitch',
    'Recognize which cross-grocer claims translate from Kroger to others, and which don\'t',
    'Sequence the cross-grocer pursuit order intelligently',
  ],
  body: `
> **Independence Reminder**
> This chapter compares publicly-disclosed postures of multiple US grocers — Kroger, Albertsons, Publix, HEB, and Ahold Delhaize USA. All assertions derive from publicly-available signals (earnings calls, public job postings, vendor announcements, press coverage) as of 2026 Q1. Where a posture is not publicly inferable, the table reads "discovery territory." Sellers must not infer specifics from internal Deloitte engagement information into client-facing comparisons; the cross-grocer narrative is positioning, not intelligence-sharing, and the discipline is mandatory.

The cross-grocer comparison is two tools in one. As a Kroger pitch tool it is positioning differentiation — what only Kroger gets, why Kroger's posture makes APEX a programmatic fit. As an expansion-strategy tool it is sequencing — which grocer comes after Kroger, where the platform pattern translates, and where the pursuit motion has to adapt. Sellers should know both uses; the chapter is structured to support both.

## 8.1 The five-grocer comparison at a glance

Five US grocers carry the scale and the strategic profile that match the program. The comparison covers the dimensions most relevant to an agentic-AI conversation.

| Grocer | Loyalty / customer-data subsidiary | Cloud / data platform posture | Operational productivity program | Public AI signal | Most-pressured margin lever (publicly inferable) |
|---|---|---|---|---|---|
| **Kroger** | 84.51° wholly-owned, Cincinnati, public CPG-revenue line | GCP-heavy via 84.51°; growing Azure footprint enterprise-wide | Restock Kroger + FreshFlex labor model | Public job postings reference Foundry, Fabric, Copilot Studio | Gross margin (post-Albertsons window); fresh shrink |
| **Albertsons** | Smaller proprietary footprint; loyalty data less subsidiary-shaped than Kroger | Multi-cloud; less-public data-platform commentary | Productivity programs publicly disclosed but lower public profile than Restock Kroger | Limited public AI signal; some announced initiatives | Post-merger-collapse margin pressure; private-equity ownership history shapes capital posture |
| **Publix** | Employee-owned; smaller customer-data subsidiary footprint; conservative tech adoption | Conservative cloud posture; less public commentary on AI platform commitments | Strong fresh-execution operational program; less publicly named than Restock Kroger | Limited public AI signal | Fresh-margin discipline; employee-ownership posture shapes investment cadence |
| **HEB** | Private company; proprietary loyalty and customer-data investment with limited public disclosure | Discovery territory for cloud/platform specifics; publicly known to invest heavily in proprietary tech | Fiercely innovative private operator; productivity programs not publicly named | Limited public AI signal; HEB tech investment is heavy but publicly opaque | Private-label leadership; regional dominance defends margin |
| **Ahold Delhaize USA** | Multi-banner US (Stop & Shop, Food Lion, Giant, Hannaford) plus EU portfolio; has its own customer-data investments | Multi-cloud, including Azure footprint; data platform spans US/EU operating companies | Operational programs vary by banner | Some public AI initiatives at the parent level; banner-level investments vary | Multi-banner integration cost; EU/US capital-allocation balance |

Several rows read "discovery territory" by design — public posture for a private company like HEB or for a multi-banner operator like Ahold is genuinely thinner than the Kroger public posture. Sellers should not over-fill these cells; "discovery territory" is the honest answer when the answer is not public.

## 8.2 Kroger's distinguishing characteristics

Three Kroger characteristics most shape the pitch. Each was introduced in Chapter 1; this chapter takes them one layer deeper for cross-grocer contrast.

**84.51° as a wholly-owned customer-data subsidiary with a public CPG-revenue line.** No other US grocer has the same shape of customer-data subsidiary. Albertsons has loyalty data but no comparable subsidiary; Publix has employee-ownership-mediated loyalty without subsidiary structure; HEB has proprietary investment without public disclosure; Ahold has multi-banner customer-data investments but not a single subsidiary with the public CPG-revenue posture 84.51° has. The pitch implication: Kroger is uniquely a coexistence-with-subsidiary conversation. The agent layer respects 84.51° as an upstream feature owner; the boundary contract is API-mediated; the architecture slide names 84.51° explicitly. None of the other four grocers requires this exact pattern in this exact form.

**Ocado-powered CFC strategy.** Kroger's CFC strategy with Ocado is unique in the US — no other major US grocer has licensed the Ocado Smart Platform for automated CFCs at scale. Albertsons has CFC investments but on a different stack; Publix and HEB have not pursued the same CFC posture; Ahold has automated fulfillment investments that vary by banner. The pitch implication: Kroger is a closed-CFC-envelope conversation, with the agents living on the store side of the seam. None of the other four grocers requires this exact pattern; the CFC anti-pattern from Chapter 3 is Kroger-specific.

**FreshFlex labor model.** Kroger's FreshFlex labor model is publicly disclosed and named; no other major US grocer has named the same program in the same shape. Other grocers have flexible-labor programs and labor-cost discipline, but the Kroger-specific FreshFlex framing is a piece of vocabulary that lands in a Kroger conversation and would not land in an Albertsons or Publix conversation. The pitch implication: any operational-AI conversation at Kroger should reference FreshFlex by name, not by generic "flexible labor" framing.

## 8.3 Albertsons' distinguishing characteristics

Albertsons' strategic posture is shaped by the post-merger-collapse aftermath. The Kroger merger was blocked in late 2024; Albertsons paid no breakup fee but absorbed the strategic disruption of an 18-month M&A process that ended with no transaction. Public commentary suggests the company has reset to a stand-alone strategic posture with continued investor pressure on margin and growth.

Albertsons' AI investment is less publicly visible than Kroger's. The customer-data subsidiary footprint is smaller; the loyalty program (Just for U) is integrated more tightly with the operating company than 84.51° is with Kroger. Private-equity ownership history (Cerberus Capital and consortium) shapes the capital posture — Albertsons has historically operated under tighter capital discipline than Kroger, which influences the wave-envelope conversation. The pitch implication: Albertsons is a similar-but-tighter conversation to Kroger; the basis-point math has to be even more disciplined; the Wave-1 envelope has to size smaller for similar architectural ambition.

## 8.4 Publix, HEB, and Ahold — short profiles

**Publix.** Employee-owned, conservative tech-adoption posture, strong fresh-execution culture. The employee-ownership structure shapes the investment cadence — capital decisions move on a different rhythm than at investor-owned grocers, and the bias is toward proven-rather-than-leading-edge technology. The pitch language has to lean into the operational discipline angle (which Publix has in spades) rather than the leading-edge AI angle. Fresh-execution and shrink-discipline conversations land; speculative margin-uplift pitches do not.

**HEB.** Private, fiercely innovative, regional dominance in Texas and Mexico, unique private-label posture (HEB private-label penetration is publicly described as among the highest in US grocery). HEB is privately known to invest heavily in proprietary technology, but the public disclosure is thin by design. The pitch language has to respect the private-company posture (less appetite for vendor-led narratives, more appetite for partnership) and the regional-dominance angle (the agents tune to Texas-specific category mix and customer behavior). The discovery cycle is longer because the private-company decision motion is slower.

**Ahold Delhaize USA.** Multi-banner US operations (Stop & Shop, Food Lion, Giant Food, Hannaford) plus EU portfolio under the parent. Multi-cloud platform posture including Azure. Customer-data investments at both parent and operating-company level. The pitch language has to handle the multi-banner reality — what works at Stop & Shop is not automatically the right pattern at Food Lion, and the program design has to account for banner-level variation from the start. The advantage: when Ahold lands, the program scales across multiple banners with shared substrate, which is a larger expansion footprint than any single-banner operator offers.

## 8.5 What translates from Kroger to other grocers

Most of the platform pattern translates cleanly across the five grocers. The translatable pieces:

- **The five-plane platform pattern.** Bronze→Silver SOR, Fabric semantic model, Foundry agent fleet, MCP server tier, Purview governance plane. The architecture is grocer-agnostic; the planes apply at any grocer with the Microsoft footprint to support them.
- **The agent library.** The six-agent merchant-decision pod (Margin-Exposure, Elasticity, Counter-Move, Promo-Participation, Substitution-Pattern, Composer) is decision-class-shaped, not Kroger-shaped. The agents work for any grocer with the same merchant-decision boundaries; the inputs change, the agents do not.
- **The audit-row discipline.** The HITL-and-audit-row spine works at any grocer. CFOs at every major US grocer want the same defensibility posture; the discipline travels.
- **The Wave 1 / 2 / 3 commercial framing.** The illustrative envelope ranges scale roughly with grocer size; the framing of "small Wave 1 earns the right to large Wave 2" works everywhere.
- **The FSMA 204 traceability shape.** The regulatory environment is identical across all five grocers — same CTEs, same KDEs, same TLC, same retention obligation. The RC-E2E-09 service translates directly; only the gap-pattern specifics change.

## 8.6 What does NOT translate

Three patterns are Kroger-specific and the pitch language must adapt at every other grocer.

- **84.51°-specific integration.** The wholly-owned-subsidiary coexistence pattern is unique to Kroger. At other grocers the customer-data plane has different shape — internal team rather than subsidiary, multi-banner rather than centralized, employee-owned-loyalty rather than CPG-monetized. The pitch language has to map to the local shape.
- **Ocado-seam integration.** The closed-CFC-envelope pattern is Kroger-specific. At other grocers the CFC posture differs (no CFCs, different vendor stack, in-house automation). The seam analysis from Chapter 3 has to be redone for each grocer.
- **FreshFlex-specific labor framing.** The named-program reference is Kroger-only. At other grocers the operational-productivity language has to adapt — Albertsons' equivalent program, Publix's fresh-execution discipline, HEB's regional operational pattern, Ahold's banner-by-banner programs. Generic "flexible labor" framing is too thin everywhere; the pitch has to find each grocer's named-program equivalent.

## 8.7 Cross-grocer pursuit order

The intelligent pursuit sequence orders the five grocers by similarity-to-Kroger and decision-cycle-velocity.

**Kroger first.** The anchor proof point. The RC-E2E-03 + RC-E2E-09 anchor combination, the architecture pattern, the audit-row discipline, the wave envelopes. Kroger landed is the case study that opens the next four conversations.

**Albertsons second.** The closest similar conversation. Same scale tier, same margin-pressure shape, same regulatory environment, similar Microsoft posture. The pitch language adapts (no 84.51°-specific coexistence; different CFC posture; different productivity-program naming) but the core narrative is the same. The decision cycle is comparable to Kroger's.

**Ahold third.** Multi-banner gives wider expansion footprint at lower per-banner cost once landed. The platform pattern translates well; the multi-banner program design adds complexity but also amortizes the substrate across more banners. The decision cycle involves both US and parent-level engagement, which is slower than a single-OpCo grocer.

**HEB and Publix later.** Both are slower-cycle pursuits because of proprietary postures (HEB's private-company decision motion, Publix's employee-ownership investment cadence). Both are valuable when they land — HEB's private-label leadership and Publix's fresh-execution discipline make each a reference account in a different way — but the pursuit motion has to be patient. Lead with relationship and operational-discipline framing, not with leading-edge AI framing.

> **Companion Artifacts**
> - [Cross-Grocer Comparison](Services/RC-E2E-03_Assortment-and-Pricing/Tier4-Strategic/APEX-RC-E2E-03-Cross-Grocer-Comparison.xlsx) — the structured comparison across Kroger, Albertsons, Publix, HEB, and Ahold
`,
  summary: [
    'Five US grocers; distinct postures across data, cloud, productivity, AI signal',
    'Kroger\'s three distinguishing characteristics (84.51°, Ocado, FreshFlex) shape every pitch',
    'The platform pattern translates; the integrations don\'t',
    'Pursuit order: Kroger → Albertsons → Ahold → (HEB / Publix later)',
  ],
  actions: [
    'Memorize the five-grocer comparison rows',
    'Rehearse the Kroger-distinct pitch (what only Kroger gets)',
    'Identify your second-grocer expansion target and align with practice leadership',
  ],
});

// ---- PART III — THE ARCHITECTURE ----

chapters.push({
  num: 9, part: 3, title: 'System of Record — Bronze→Silver',
  objectives: [
    'Describe what the Bronze and Silver layer scopes are for this program',
    'Identify the source systems feeding the Bronze layer',
    'Name the Silver entities that form the spine of the agent fleet',
    'Understand why the Bronze→Silver contract is the QA gate for everything downstream',
  ],
  body: `
No data, no agents. Every chapter that follows assumes the Bronze→Silver layer is in place; without it, there is nothing for the agents to reason over, nothing for Purview to govern, nothing for the audit row to attribute. The system of record is foundational, and a Wave-1 envelope that under-invests in the SOR produces a Wave-2 program that cannot scale. The discipline starts here.

## 9.1 Why SOR matters for agentic AI

Agents that reason on bad data produce bad recommendations, and bad recommendations destroy CFO credibility faster than missing recommendations. A merchant who accepts an agent recommendation that turns out to have been built on a stale supplier-cost feed, or on a receiving event that never landed in the data plane, will reject the next twenty recommendations on principle. Worse, the audit row that ties the recommendation back to the realized P&L delta becomes indefensible the moment the inputs are challenged — the chain breaks at the source, and the program loses its CFO sponsorship in the next quarterly review.

The Silver layer is what makes the agent fleet defensible. It is the conformed, schema-validated, freshness-instrumented business-entity layer that sits between raw operational source systems and the agent runtime. Every agent in the fleet queries Silver; no agent queries a source system directly; every Silver record carries the provenance back to the Bronze record (and from there to the source-system event) that produced it. This is the architectural posture that lets a CFO defend the basis-point claims, that lets a General Counsel defend the recall-execution evidence chain, and that lets a CIO defend the data plane in front of the audit committee. Without it, the program is a demo; with it, the program is a system of record.

## 9.2 The Bronze layer — raw ingest from source systems

The Bronze layer is the as-is landing zone. Data lands at native cadence, in native shape, with original timestamps preserved and source identifiers untouched. There is no transformation in Bronze, no schema enforcement, no deduplication, no normalization — Bronze is a lossless capture of what the source system produced, when it produced it, with the metadata that tells the data engineering team where it came from. If the supplier portal sends a JSON payload with seventeen fields and three of them are misspelled, all seventeen land in Bronze with the misspellings intact. If the POS system sends a transaction record with a future-dated timestamp because of a clock-sync issue at the store, the future-dated timestamp lands in Bronze alongside the system-time of ingest.

The discipline matters for two reasons. First, the Bronze layer is the replay surface — when a downstream Silver transformation has a bug and produces wrong outputs for two weeks, the fix is to correct the transformation and replay from Bronze. If Bronze had been transformed at ingest, the source data would be lost and the replay would not be possible. Second, the Bronze layer is the audit baseline — when a regulator or auditor asks "what did the source system actually send you on July 17," the answer is in Bronze, not reconstructed from Silver. The integrity of the answer depends on the lossless capture.

In Fabric terms, Bronze lives in OneLake delta tables organized by source system, with partition keys that match the source system's natural cadence (date for batch sources, hour or minute for event streams). Eventstream pipelines handle the streaming sources; batch ingest jobs handle the file-and-API sources. Schema-on-read at Bronze, schema-on-write at Silver — that is the line.

## 9.3 The source systems (typical Kroger pattern)

The source systems feeding Bronze are illustrative for the Kroger pattern. Specifics — vendor, version, integration mechanism, refresh cadence — are discovery territory and should be confirmed in Wave-1 envisioning rather than assumed. The shape below is the publicly-inferable typical pattern for a Kroger-scale grocer.

| Source system | Domain | Data shape | Cadence | Refresh latency |
|---|---|---|---|---|
| POS / transaction system | Sales, basket, store-level revenue | Event stream (transaction, line item, tender) | Continuous | Sub-minute via Eventstream |
| Loyalty / customer master (84.51° feed) | Household segments, propensity scores, elasticity coefficients | Curated feature tables via API or Fabric shortcut | Daily refresh, near-real-time for select features | Hours, with feature-specific SLOs |
| Item master | PLU + UPC + GTIN + TLC, item attributes, category hierarchy | Reference dataset with daily delta | Daily batch | Same-day |
| Supplier portal / EDI receiving | Advance shipping notices, bills of lading, receiving confirmations | EDI 856/810/856-style messages plus portal events | Per-shipment | Minutes from supplier transmission |
| Cold-chain telemetry | Temperature, humidity, GPS for refrigerated transport and store cases | Time-series telemetry stream | Continuous | Seconds via Eventhouse |
| Planogram master | Shelf layouts, facings, category placement | Reference dataset with weekly batch | Weekly with mid-week updates | Same-day |
| Pricing / promo system | Effective shelf price, promo windows, KVI flags | Reference + event hybrid (price changes are events) | Daily batch + intraday events | Hours for batch, minutes for events |
| ESL gateway | Electronic shelf label state, sync confirmations | Event stream | Continuous | Sub-minute |
| Labor scheduling | Department schedules, FreshFlex assignments, time-clock events | Reference + event hybrid | Daily batch + intraday events | Same-day |

These integrations are illustrative; the specific Kroger systems, vendors, and versions are discovery territory. The shape of the table — *how many sources, what cadence each runs at, what latency the agents can rely on* — is what the lead architect should walk through with the Kroger data-platform team in the first week of Wave 1.

## 9.4 The Silver layer — conformed business entities

Silver is the harmonized, schema-validated, business-entity layer that the agent fleet queries. Each Silver record is the result of a Bronze→Silver transformation that maps one or more Bronze records (potentially across multiple source systems) into a canonical business entity with a defined schema, a canonical key, a versioned schema definition, and a freshness service-level objective. Silver is the contract the agent fleet depends on; Bronze is the lossless capture that makes the contract recoverable.

The conformance pattern is straightforward in shape and demanding in execution. Each Bronze record is mapped to one or more Silver entities; the mapping is a code artifact (not a stored procedure, not a notebook left in an analyst's workspace) under version control with explicit ownership. Each Silver entity has a primary key that is canonical across the data plane — an item is identified by GTIN or by an internal item number that resolves consistently across categories; a store is identified by the canonical store number that the operations org uses; a lot is identified by the TLC. Where source systems disagree on identifiers, the conformance layer resolves the disagreement once and writes the canonical identifier to Silver; the disagreement does not propagate to the agent fleet.

Schema validation at Silver is enforced. A Bronze→Silver transformation that produces a Silver record violating its schema fails the transformation and surfaces an alert to data engineering before the bad record reaches the agent fleet. This is the gate that protects the agent fleet from upstream data-quality drift. Freshness is also instrumented — each Silver entity has a freshness SLO (e.g., POS-derived sales facts current within 5 minutes; item-master attributes current within 24 hours; cold-chain telemetry current within 30 seconds), and the data plane reports freshness against SLO continuously. When freshness drifts, the agents are notified and downgrade their confidence accordingly.

## 9.5 The Silver entity model

The core Silver entities are decision-class-shaped, not source-system-shaped. Each is described below with its one-line purpose, primary key, and freshness SLO target. The full visual entity-relationship model lives in the SOR ERD artifact.

- **Item.** The canonical product entity carrying GTIN, UPC, PLU, internal item number, category hierarchy, and attribute set. Primary key: item number (canonical). Freshness SLO: 24 hours for attribute updates, sub-hour for new-item additions.
- **Lot.** The traceability lot carrying TLC, source identifier, harvest or production date, and lineage links to upstream lots (for transformations and creations). Primary key: TLC. Freshness SLO: minutes from supplier transmission (FSMA-driven).
- **Customer (anonymized for the agent layer).** The household identifier shape, anonymized at the Silver boundary so that agents reason over segment and propensity rather than raw customer identifiers. Primary key: anonymized household identifier. Freshness SLO: daily for segment updates, near-real-time for in-trip signals where available.
- **Transaction.** The basket-level event combining tender, line items, store, register, and timestamp. Primary key: transaction identifier. Freshness SLO: sub-minute via Eventstream.
- **Receipt.** The receiving-event entity for inbound supplier shipments, carrying TLC, supplier, store or DC, quantity, and lineage links. Primary key: receipt identifier. Freshness SLO: minutes from receiving-system transmission.
- **Promotion.** The promotion-instance entity carrying promo identifier, scope (item/category/store), effective window, and funding source (vendor-funded or grocer-funded). Primary key: promotion identifier. Freshness SLO: same-day.
- **Price-Point.** The effective shelf-price entity at the item-store-time grain, carrying everyday price, promotional price (where active), and effective window. Primary key: composite of item, store, and effective time. Freshness SLO: minutes for price changes, sub-minute for ESL-confirmed updates.
- **Supplier.** The supplier-master entity carrying supplier identifier, business name, location, and qualification status. Primary key: supplier identifier (canonical). Freshness SLO: daily.
- **Store.** The store-master entity carrying canonical store number, banner, format, geography, and operational metadata. Primary key: store number. Freshness SLO: daily, with intraday updates for open/closed status.
- **Staff-Assignment.** The labor-assignment entity at the associate-shift-department grain, supporting the FreshFlex labor model and the schedule-and-assignment agents. Primary key: composite of associate, shift, and department. Freshness SLO: hourly for schedule, sub-minute for time-clock events.

The full ERD — entities, relationships, foreign keys, cardinality — lives in the SOR ERD artifact and should be walked end-to-end with the lead architect before Wave-1 envisioning workshops begin. The ERD is also the artifact that 84.51° data stewards will review during the data-stewardship gate; it should be presentable cold.

## 9.6 Why Silver is the spine

Every agent in the fleet queries Silver, never Bronze. This is not an implementation convenience; it is the architectural gate that defines what the agent fleet is and is not. Three structural reasons.

**Source-system independence.** When a source system is replaced — a new POS vendor, a new pricing system, a refreshed item master — the impact is confined to the Bronze→Silver transformations for that system. The Silver entities and their schemas do not change; the agents continue querying Silver as before; the swap is invisible to the agent fleet. Without this discipline, every source-system change is an agent-fleet change, and the program loses the agility that makes it valuable.

**Audit defensibility.** Every agent decision traces through schema-validated Silver records, each of which traces back through a versioned Bronze→Silver transformation to a Bronze record, which traces back to a source-system event with timestamp and identifier. This is the chain that makes the audit row defensible: the chain is automatic, captured in lineage metadata, and reproducible six months later when a finance challenge or regulatory inquiry lands.

**Data-quality isolation.** Bad data in a source system does not silently corrupt the agent fleet. The Bronze→Silver schema validation catches malformed records at the conformance boundary; the freshness SLO catches stale records as their staleness exceeds threshold; the agents are notified and adjust. Without Silver as the gate, source-system data-quality drift propagates directly into agent reasoning, and the program loses the integrity that makes it survive scrutiny.

## 9.7 The Bronze→Silver transformation contract

Each Bronze→Silver transformation is a code artifact with explicit ownership, versioning, and a test suite. Not a notebook in someone's workspace, not a stored procedure with no test coverage, not a hand-written script that runs on an analyst's laptop. The discipline is software-engineering-grade: each transformation has a named owner on the data engineering team, lives in a code repository with pull-request review, has unit tests for the transformation logic and integration tests against a frozen Bronze sample, and is deployed through the same CI/CD pipeline that other data-platform code uses.

When a transformation fails — a schema violation in Silver, a freshness SLO miss, an upstream source-system change that breaks the parsing logic — the failure surfaces to data engineering before it surfaces to the agent fleet. Alerting is on the freshness SLO and on the schema-validation failure rate; runbooks define the response; ownership is named. This is the contract that makes the data plane operable rather than fragile.

The Wave-1 envelope budget for SOR work is typically **30-40% of total Wave-1 effort**, sometimes higher when the source-system landscape is messier than expected. Sellers who shave the SOR budget to make the Wave-1 number look smaller are setting up the program to fail in Wave 2; the substrate is the foundation everything downstream depends on, and under-investing here produces an agent fleet that cannot be defended and a CFO conversation that does not survive the second quarter.

> **Companion Artifacts**
> - [SOR Bronze→Silver](Services/Shared-Both-Services/Tier0-Foundation/APEX-RC-E2E-03-09-SOR-Bronze-to-Silver.docx) — the foundational SOR design document
> - [SOR ERD](Services/Shared-Both-Services/Tier0-Foundation/APEX-RC-E2E-03-09-SOR-ERD.html) — the full entity-relationship picture
`,
  summary: [
    'Bronze raw, Silver conformed; ten-ish source systems feed Bronze; Silver is the agent spine',
    'Each Bronze→Silver transformation is a versioned, owned, tested code artifact',
    'Silver freshness SLOs gate downstream agent reliability',
    'SOR is 30-40% of Wave-1 effort because everything downstream depends on it',
  ],
  actions: [
    'Walk the ERD with your lead architect before envisioning workshops begin',
    'Identify which source systems are missing or weak in your prospect\'s estate',
    'Pre-clear the Bronze→Silver transformation owner before Wave-1 SOW',
  ],
});

chapters.push({
  num: 10, part: 3, title: 'The Fabric Plane',
  objectives: [
    'Describe the Fabric components in the architecture',
    'Name the semantic-model layer and what it serves',
    'Identify the Eventhouse / Eventstream usage pattern',
    'Quote a capacity-sizing rule of thumb for the F-SKU starting envelope',
  ],
  body: `
Fabric is the data-plane substrate. OneLake holds everything; the semantic model is the consumption surface; Eventhouse and Eventstream handle the time-series flows; mirroring keeps the coexistence story clean. For this program at Kroger, Fabric is not just a data warehouse — it is the operational data plane that the agent fleet reasons over, the regulatory data plane that the recall agent queries, and the integration plane that bridges the Kroger estate (POS, supplier, store) to the 84.51° estate without copying customer features into Microsoft territory.

## 10.1 What Fabric does for this program

Fabric provides storage, compute, semantic model, and event ingest in one capacity-priced envelope. For a Kroger-scale workload, the appeal is consolidation: one F-SKU envelope replaces the OpEx complexity of a multi-vendor data stack — separate warehouse licensing, separate streaming-platform licensing, separate semantic-layer licensing, separate ETL-tool licensing — with a single capacity reservation that the data-platform team manages against a single set of SLAs. The accounting story is simpler; the operational story is simpler; the upgrade story is simpler.

The architectural story is also tighter. The Bronze and Silver layers from Chapter 9 live in OneLake delta tables; the semantic model that the agents query is **Direct Lake** over those same delta tables, with no separate import or refresh cycle; the time-series streams (POS, cold-chain, FSMA 204 receiving events) land in Eventhouse with KQL-queryable indexes; the streaming pipelines that move source data into Bronze run as Eventstreams. Everything addressable through one workspace, one capacity, one identity boundary. The agent fleet does not have to reason about which platform a particular dataset lives on — it lives in Fabric, the rest is detail.

## 10.2 OneLake as the unified storage tier

Every Bronze and Silver record lives in OneLake — the unified storage tier under Fabric. The format is delta/parquet; the layout is workspace-scoped lakehouses with partition strategies tuned to each entity's query patterns; the access is governed through Entra and classified through Purview. This gives the agent fleet a single addressable storage namespace: when an MCP server (Chapter 12) needs to read a Silver entity, it reads from OneLake; when the recall agent needs to scan a year of receiving events, it scans Eventhouse-indexed OneLake data; when the demand-forecasting model needs a year of POS history, it reads from OneLake.

The storage-tier consolidation has a structural consequence for cost. Compute and storage are decoupled at the OneLake layer — capacity buys compute, OneLake billing covers storage independently — which means the program scales storage and compute against actual workload rather than against a coupled SKU. For the Kroger pattern (large historical retention for FSMA 204, intensive query on recent data for the agent fleet), the decoupling lets the program right-size each dimension separately.

OneLake shortcuts are the structural mechanism that keeps the coexistence story clean — the **shortcut** lets the Fabric workspace read a dataset from another estate (84.51° on GCP, an Azure SQL database, an external Synapse workspace) as if it were native OneLake, without copying the data. Section 10.6 covers the implications.

## 10.3 The Fabric semantic model (Direct Lake)

**Direct Lake** is the semantic layer the agents query. It is the deterministic, business-entity-aware view that the Foundry agents call when they need a Silver record — not a SQL surface, not a raw delta-table read, but a semantic-model query that resolves through the same conformed entity model the data-engineering team published. The agent does not write SQL; it calls a tool exposed by an MCP server (Chapter 12) that resolves through the semantic model and returns a typed business entity.

The decoupling matters. A semantic-model layer between the agents and the storage tier means the storage layout can change — partition strategies refined, table physical structures evolved, even underlying delta tables refactored — without the agent code changing. The agent calls a tool with semantic intent (*"give me the price-point history for item X at store Y over the last 90 days"*); the tool resolves through the semantic model; the semantic model resolves through Direct Lake to the underlying delta tables. Three layers of decoupling, each protecting the layer above from the churn of the layer below.

Direct Lake also gives the program a single conformed view that BI consumers can use. The same semantic model that serves the agent fleet serves Power BI dashboards, Copilot for M365 query surfaces, and any other BI client. There is one definition of *item*, one definition of *store*, one definition of *transaction* — and that one definition is what the merchant sees in their dashboard, what the agents reason over, and what the audit row attributes against. The cross-consumer consistency is itself a defensibility property.

## 10.4 Eventhouse for time-series telemetry

The FSMA 204 traceability records, the cold-chain telemetry, the POS streams, the ESL state events, the time-clock events — all the high-volume, time-series, low-latency data lives in **Eventhouse**. KQL-queryable, time-series-optimized, designed for the workload pattern where queries are bounded by time windows and the cardinality of the events is high.

The recall agent in RC-E2E-09 is the canonical Eventhouse query workload. When a recall is initiated and the agent receives a TLC at 09:02, the query that returns every store that received the lot, every customer transaction that touched the lot, and every remaining inventory unit is an Eventhouse query against a time-bounded slice of the receiving and transaction streams. Sub-minute for the impact-scoping result; minutes for the full lineage export. The performance is not incidental — it is what makes the 24-hour FSMA 204 obligation operationally feasible.

Eventhouse also serves the freshness-signal agent (Chapter 2's fresh-defect-rate decision class), the cold-chain-excursion analytics, and any other workload where the natural shape of the data is time-series with high cardinality. The Eventhouse and OneLake delta layers are not separate stores — Eventhouse data is queryable through the Fabric semantic model alongside OneLake delta data, which means the agents reason over a unified view that hides the storage-tier distinction.

## 10.5 Eventstream for ingest pipelines

**Eventstream** sits between source systems and OneLake, handling the streaming ingest from POS, supplier, and telemetry sources. This is the Bronze-layer landing pipeline for the streaming sources — the batch sources land through scheduled batch jobs, but the streaming sources land through Eventstream, with the ingest pipeline preserving source order, source timestamps, and source identifiers as required by the Bronze-layer discipline from Chapter 9.

The Eventstream pipelines are versioned alongside the Bronze→Silver transformation code; ownership is named on the data engineering team; the ingest pipeline failure modes (back-pressure, schema-drift, source-system outage) are runbook-documented. When a source system pushes a malformed event, the Eventstream pipeline routes it to a dead-letter queue rather than dropping it silently; data engineering investigates; the agent fleet is shielded.

## 10.6 Mirroring and shortcuts to other estates

Fabric **mirroring** and **shortcuts** are the architectural mechanisms that keep the coexistence story with 84.51° clean. The 84.51° estate runs on Google Cloud Platform; copying customer features into Fabric would trigger the displacement anti-pattern from Chapter 3, the data-stewardship gate would block the program, and the cost of duplicated storage would compound monthly. Instead, the Fabric workspace reads the 84.51°-curated feature tables in place via shortcut — the data does not move, the ownership does not change, the governance posture does not shift, but the agent fleet can query the features through the same semantic model that serves Silver.

The same pattern applies to Azure SQL, to existing Synapse workspaces, and to any other estate that the Kroger data-platform team has invested in. Mirroring keeps a continuously-refreshed copy in OneLake for workloads that need ultra-low-latency reads; shortcuts read in place for workloads that tolerate a network hop. The decision is workload-specific and discovery-driven; the architectural pattern is consistent.

For the Kroger pattern specifically, the mirroring story is what lets the architecture slide from Chapter 3 hold up in front of a CIO. **84.51° features stay on GCP, are read via shortcut, are governed by 84.51° upstream and Purview at the consumption boundary.** The Fabric workspace consolidates the operational data plane (POS, supplier, store) but does not absorb the customer-data plane. That is the boundary that makes the coexistence defensible.

## 10.7 Capacity sizing rule of thumb

Capacity sizing is illustrative; the actual envelope depends on data volume, query concurrency, semantic-model complexity, Eventhouse retention, and a half-dozen other factors that only Microsoft and the joint architecture team can size definitively. The rule-of-thumb starting envelope below is publicly-defensible heuristic, not commitment.

| Workload phase | Typical F-SKU starting tier | Notes |
|---|---|---|
| Wave-1 envisioning + foundational deployment | F64, or F128 if heavy Eventhouse from the start (FSMA 204 receiving stream) | Sized for one-category proof-of-concept and the foundational SOR build |
| Wave-2 production | F128–F256 depending on category breadth | Six-agent fleet in production, full Bronze→Silver, semantic model, FSMA 204 lineage live |
| Wave-3 production at Kroger scale | F256–F512 | All anchors plus high-attach catalog, multi-banner, enterprise scale |

The framing is illustrative. Final pricing is set by Microsoft and the Microsoft account team should validate the starting envelope against the specific Kroger licensing posture before any commitment is documented. The rule-of-thumb tier scales via reservation discounts as the program grows; the program rarely sees a step-change cost increase, more often a gradual climb as workload grows and Microsoft's reservation pricing absorbs the growth.

A note on co-tenancy: Fabric capacity is not exclusively a single-workload reservation, and the Kroger data platform team may already have an enterprise F-SKU footprint that the program rides on top of. Discovery should establish whether the program needs its own dedicated capacity (typical for the regulatory FSMA 204 workload, where SLO isolation matters) or whether it can share an existing enterprise capacity (often acceptable for the agent-decision workload where queries are bursty and small). The decision changes both the cost story and the ownership story; surface it early in Wave 1.

> **Companion Artifacts**
> - [Fabric Runbook](Services/Shared-Both-Services/Tier2-Build/APEX-RC-E2E-03-09-Fabric-Runbook.docx) — the build-side runbook for the Fabric plane
> - [Solution Architecture Document](Services/Shared-Both-Services/Tier0-Foundation/APEX-RC-E2E-03-09-Solution-Architecture-Document.docx) — the full architecture treatment, both anchors
`,
  summary: [
    'OneLake + semantic model + Eventhouse + Eventstream is the Fabric stack for this program',
    'Mirroring keeps coexistence with 84.51° clean — read in place, don\'t copy',
    'Direct Lake is the semantic surface the agents call through MCP',
    'Capacity sizing has a starting heuristic; Microsoft validates final pricing',
  ],
  actions: [
    'Rehearse the Fabric architecture story for a CIO audience',
    'Pre-validate the F-SKU starting envelope with the Microsoft account team',
    'Identify the F-SKU starting tier for your prospect\'s expected workload',
  ],
});

chapters.push({
  num: 11, part: 3, title: 'The Foundry Plane — Six Agents and Maturation',
  objectives: [
    'Recap the six-agent fleet and the model-routing logic for each',
    'Describe the maturation path (prompt → fine-tune → distill) and when each step is worthwhile',
    'Quote a cost-per-decision target band for the agent fleet',
    'Understand the evaluation harness and the HITL contract that anchor the fleet\'s economics',
  ],
  body: `
Foundry is the reasoning runtime. The six agents from Chapter 5 live here; the model-routing decisions live here; the evaluation harness lives here; the HITL contract is enforced here. For this program, Foundry is what turns the data plane into a decision plane — and **model routing** is what keeps the cost-per-decision in defensible bounds as the fleet scales from one-category proof-of-concept to multi-banner production.

## 11.1 The six-agent fleet recap

The six agents introduced in Chapter 5 are the working fleet for RC-E2E-03. Each owns a decision boundary; each is named for its decision class; each runs on a model class chosen for that boundary. The names below are the canonical fleet:

- **Margin-Exposure Agent** — where is gross margin at risk this cycle?
- **Elasticity Agent** — what happens if we move this price 1%, 3%, 5%?
- **Counter-Move Agent** — how do we respond to a competitor's move on a watched SKU?
- **Promo-Participation Agent** — do we accept, modify, or decline this VFP proposal?
- **Substitution-Pattern Agent** — which SKUs can we discontinue without losing the basket?
- **Recommendation-Composer Agent** — which 200 recommendations does the merchant see this week?

The fleet is co-resident in a single Foundry workspace with a shared agent registry, a shared MCP server tier, a shared observability stack, and a shared evaluation harness. RC-E2E-09's recall and freshness-signal agents add into the same workspace as the program expands; the workspace is the unit of operational scale, not the individual agent.

## 11.2 Model routing — which agent uses which class and why

Model routing is the discipline of matching each agent's decision class to a model whose reasoning capability is necessary and sufficient for the boundary. Putting a top-tier reasoning model behind every decision is uneconomic; using a small fast model where deep reasoning is required produces unreliable recommendations that destroy merchant trust. The right answer is per-agent, and it changes as the agents mature.

The illustrative routing table below uses publicly-known model classes. Final selection is a joint decision with the Microsoft Foundry product team and depends on availability, cost, latency, and license posture at the time of deployment. Treat this as the starting heuristic, not the commitment.

| Agent | Model class | Why this class | Typical token shape |
|---|---|---|---|
| **Margin-Exposure Agent** | Top-tier reasoning (e.g., Claude Sonnet, GPT-4o) | Multi-factor reasoning across margin targets, supplier cost, KVI flags, category strategy; first-pass agent that anchors the entire week | 4-12K input, 1-3K output per cycle |
| **Elasticity Agent** | Top-tier reasoning (e.g., Claude Sonnet, GPT-4o) | Probabilistic reasoning over elasticity coefficients, basket-affinity, confidence bands; output drives downstream pricing decisions | 6-15K input, 2-4K output per SKU |
| **Counter-Move Agent** | Top-tier reasoning (e.g., Claude Sonnet, GPT-4o) | Game-theoretic reasoning over competitor postures, banner positioning, KVI implications; latency-sensitive (must respond inside the merchant's review window) | 4-10K input, 1-2K output per move |
| **Promo-Participation Agent** | Mid-tier reasoning (e.g., GPT-4o-mini, Claude Haiku) | Bounded decision class; structured input (VFP proposal), structured output (accept/modify/decline + counter-offer); benefits from fine-tuning over time | 2-6K input, 1-2K output per proposal |
| **Substitution-Pattern Agent** | Mid-tier reasoning (e.g., GPT-4o-mini, Claude Haiku) | Pattern-recognition over basket data; not a reasoning-intensive decision but a high-volume one; ideal candidate for fine-tuning | 3-8K input, 1K output per candidate SKU |
| **Recommendation-Composer Agent** | Smaller model with strong tool-calling (e.g., Claude Haiku, fine-tuned smaller) | Orchestration and ranking, not deep reasoning; consumes upstream agent outputs and merchant calendar; tool-calling dominates over reasoning | 8-20K input, 2-5K output per merchant queue |

The routing logic — *Margin-Exposure, Elasticity, Counter-Move at the top tier; Promo-Participation, Substitution-Pattern at mid tier; Composer at small with strong tool-calling* — is the starting posture. It changes as agents mature down the path described in Section 11.4.

## 11.3 Tool calling and MCP integration (preview Ch 12)

Agents do not query data sources directly; they call tools exposed by MCP servers. This decoupling is what lets us swap models without rebuilding the agent code, and it is what lets the same agent code serve multiple banners with different backend integrations. The Margin-Exposure Agent does not know whether the price-point data lives in Fabric Direct Lake, in an Eventhouse query, or in a mirrored Azure SQL instance — it calls a tool named *get-current-price-points-for-category* with typed input, and the MCP server resolves the call against whatever backend currently serves the data.

When the model class behind the Margin-Exposure Agent changes (an upgrade from one top-tier model to another, a fine-tuning step, a distillation step), the tool-calling contract does not change. The agent code adapts to the new model's tool-calling syntax (which is itself converging across model providers), but the tools themselves stay stable. This is the structural property that makes the model-routing table above changeable rather than brittle. Chapter 12 covers the MCP layer in depth.

## 11.4 The maturation path

The fleet matures along a three-stage path. Each stage has explicit prerequisites; sellers and delivery leads should not skip stages or invert the order.

**Stage 1 — Prompt + RAG.** The starting posture for Wave-1 and early Wave-2. Agents run on a top-tier reasoning model with carefully-engineered prompts and retrieval-augmented context from the Silver layer. This stage is the cheapest to iterate (prompt changes deploy in hours, not weeks) but the most expensive per decision (top-tier model tokens dominate the cost line). The right stage for proving the agent boundaries, refining the input/output contracts, and accumulating the labeled examples that make Stage 2 worthwhile.

**Stage 2 — Fine-tune.** The right step when a recurring decision class has accumulated **enough labeled examples** — typically 1000 or more high-quality examples with clear ground-truth labels (the merchant's HITL decision plus the realized P&L delta). Fine-tuning a smaller model on the decision class reduces both tokens (the prompt is shorter because the model has internalized the decision pattern) and latency (smaller model, fewer parameters). The Promo-Participation Agent and the Substitution-Pattern Agent are the natural Stage-2 candidates; both have bounded decision classes and both accumulate labeled examples quickly under HITL.

**Stage 3 — Distill.** The right step when a fine-tuned agent is hot enough — running thousands of decisions per day on a regular cadence — to justify a small dedicated model whose only job is that decision class. Distillation cuts token cost 10-50x for the highest-volume agents and shrinks latency to sub-second. The Recommendation-Composer Agent is a natural Stage-3 candidate eventually, because it runs every merchant cycle on every category and the orchestration logic is bounded enough to distill cleanly.

The maturation cost-benefit math is the program's compounding economics. **A Stage-1 fleet operates on token-rich top-tier models; a Stage-3 fleet operates on token-lean distilled models with surgical use of top-tier where reasoning depth is genuinely required.** The cost gap between the two is the multi-year economic story for the CFO.

## 11.5 Cost-per-decision target band

The cost-per-decision target band is illustrative and highly workload-dependent. The framing below is the publicly-defensible heuristic for the Kroger pattern; actual cost depends on token shape, model selection, fine-tuning investment, and the maturation stage of each agent.

- **Wave-1 prompt-only fleet:** $0.05–$0.20 per decision. Top-tier model, prompt + RAG, no fine-tuning yet. The Wave-1 cost is high per decision but absolute volume is low — one-category proof-of-concept produces hundreds of decisions per cycle, not thousands.
- **Mature mixed fleet (Wave 2 to mid Wave 3):** $0.005–$0.02 per decision. Mix of top-tier on the reasoning-heavy agents, fine-tuned mid-tier on the Promo-Participation and Substitution-Pattern agents. Volume has scaled to thousands of decisions per cycle across multiple categories.
- **Distilled production fleet (mid Wave 3 onward):** sub-cent per decision. Top-tier reserved for the highest-stakes reasoning calls (Counter-Move under competitive pressure, Margin-Exposure for at-risk categories); distilled small models for the high-volume orchestration and pattern-recognition work. Volume at full Kroger scale is tens of thousands of decisions per day.

The illustrative ranges are the right shape for a CFO conversation about scaling economics. Sellers should frame the cost-per-decision band as a multi-year trajectory rather than a Wave-1 commitment; the program earns the right to move down the band by completing the maturation prerequisites at each stage.

## 11.6 Evaluation harness — how Foundry agents get measured

Every agent has a **golden set** — a frozen, labeled set of representative decision examples curated by the data-science team in collaboration with the merchant org. The harness runs the golden set against every model swap, every prompt change, every fine-tuning iteration, and every deployment to a new banner; regressions surface as failed harness runs and block deployment until investigated.

In production, **drift detection** runs against a rolling sample of live decisions. The harness compares the agent's recommendations on the rolling sample against the golden-set baseline; if the agent's distribution of recommendations shifts beyond a calibrated threshold (e.g., recommending price increases at a materially higher rate than the golden set suggests is appropriate for the current input distribution), an alert surfaces to the data-science team. Drift can be benign (the world has changed, the agent is responding correctly), or it can indicate a problem (a source-system change has shifted the input distribution and the agent has not been retrained for the new distribution). Either way, the alert triggers investigation.

The **eval report** is surfaced to the operations team weekly. Cadence-routine: golden-set pass rate per agent, drift-detection signal summary, accept-rate trends from the merchant HITL surface, realized-vs-predicted impact gap per agent. This is the operational dashboard that the program runs on; it is also the artifact that the data-science team and the merchant team review jointly to prioritize the next round of agent tuning. The full eval design lives in the AI/ML Model Spec artifact.

## 11.7 The HITL contract

Every agent surfaces a recommendation with a **confidence score** and a **rationale**. The merchant accepts, modifies, or rejects; if they modify or reject, a structured **override reason** is captured. The audit row captures all of it — model version, inputs (with classification labels), prompt fingerprint, recommendation, confidence, rationale, merchant decision, override reason if any, timestamp, identity. This is the contract.

The HITL gate is what makes the audit trail defensible AND what produces the labeled examples that feed the maturation path. Both properties matter equally. The defensibility property is what the CFO and General Counsel rely on when challenges land — every recommendation traces, every decision attributes, every dollar of claimed margin connects back through the chain. The labeled-example property is what compounds the program's economics — every HITL decision is a labeled example for the agent that produced the recommendation, and 1000 high-quality labeled examples is the threshold for Stage-2 fine-tuning. The merchant org is, structurally, the labeling team for the agent fleet; the program does not have to fund a separate labeling effort because the labeling falls out of the operational HITL workflow.

The contract is also where the program's economics tighten over time. A Wave-1 fleet runs every recommendation through HITL; a Wave-2 fleet runs the high-stakes recommendations through HITL and the routine recommendations on a sampled-HITL basis (the merchant reviews every fifth recommendation, not every one, with the full audit row still captured); a Wave-3 fleet retains HITL on the high-stakes decisions and operates the routine ones on supervisory oversight (the merchant reviews exception reports rather than individual recommendations). The throughput climbs; the audit defensibility holds; the cost-per-decision falls; the merchant time freed is the substantive productivity gain.

> **Companion Artifacts**
> - [Six Agents Deep Dive and Maturation](Services/RC-E2E-03_Assortment-and-Pricing/Tier2-Build/APEX-RC-E2E-03-Six-Agents-Deep-Dive-and-Maturation.docx) — the agent-by-agent specification and maturation roadmap
> - [Service Sequence Diagram](Services/RC-E2E-03_Assortment-and-Pricing/Tier2-Build/APEX-RC-E2E-03-Service-Sequence-Diagram.html) — the agent-to-agent and agent-to-tool flow
> - [AI/ML Model Spec](Services/Shared-Both-Services/Tier4-Strategic/APEX-RC-E2E-03-09-AI-ML-Model-Spec.docx) — the full eval, model-governance, and maturation design
`,
  summary: [
    'Six agents; model class is matched to decision complexity, not bolted on uniformly',
    'Prompt + RAG → fine-tune → distill is the maturation path; each step has explicit prerequisites',
    'Cost-per-decision target band drops 10-50x as agents mature',
    'Evaluation harness + HITL contract anchor both defensibility and economics',
  ],
  actions: [
    'Memorize the six-agent / model-class table for your next architecture conversation',
    'Rehearse the maturation story for a Chief Data & Analytics Officer',
    'Pre-validate the illustrative cost band with the Foundry product specialist on the Microsoft team',
  ],
});

chapters.push({
  num: 12, part: 3, title: 'The MCP Layer',
  objectives: [
    'Describe MCP in the context of this architecture',
    'Identify the MCP servers in the deployment and what each exposes',
    'Explain the tool contract MCP gives the Foundry agents',
    'Recognize where MCP intersects with Purview and Entra',
  ],
  body: `
MCP is the agent-to-tool spine. It is what lets the same agent code work against different backends — and what lets governance wrap every tool call. For this program at Kroger, MCP is the architectural layer that makes the rest of the platform composable: the agents call tools, the tools resolve through MCP servers, the MCP servers wrap the underlying systems (Fabric semantic model, Eventhouse, 84.51° API, pricing system, audit store), and the whole stack is uniformly governed by Purview classification and Entra identity.

## 12.1 MCP in one paragraph

**Model Context Protocol (MCP)** is an open contract for tool calling that decouples the agent (which reasons) from the tool surface (which acts). Each tool is exposed via an MCP server with a typed input/output contract, an explicit auth scope, and a well-defined error model. The agent calls a tool by name with typed arguments; the MCP server resolves the call against its backend system; the response returns to the agent as a typed object. The contract is open — published, versioned, and supported by every major model and agent framework — which means the investment in MCP servers compounds across model upgrades, agent-framework changes, and even multi-vendor agent estates. For a Kroger-scale program, MCP is the structural piece that makes the platform durable across multiple Wave-3 years.

## 12.2 The MCP servers in the Kroger deployment

The deployment carries a focused set of MCP servers, each wrapping one backend system or one decision-tier of the platform. The table below is the working set; the full list and each server's tool catalog lives in the MCP Deep Dive artifact.

| Server | Purpose | Tools exposed (sample) | Backend system |
|---|---|---|---|
| **Semantic-Model server** | Read access to the Fabric Direct Lake semantic model | *get-item-attributes*, *get-price-points-for-category*, *get-promotion-history*, *get-substitution-patterns* | Fabric Direct Lake / OneLake delta |
| **Eventhouse server** | KQL queries against time-series streams | *scope-recall-by-tlc*, *get-cold-chain-excursions*, *get-pos-stream-window*, *get-receiving-events-for-supplier* | Fabric Eventhouse |
| **Customer-Features server** | Curated 84.51° feature reads via API | *get-segment-membership* (anonymized), *get-elasticity-coefficients*, *get-basket-affinity*, *get-propensity-scores* | 84.51° feature API (read via shortcut where possible) |
| **Pricing/Promo server** | Write-back to the pricing and promotion systems through approved channels | *propose-price-change*, *commit-approved-promotion*, *cancel-pending-price-change* | Pricing system + promotion system |
| **Notification server** | Teams Copilot card delivery and customer-channel notifications | *push-merchant-recommendation-card*, *push-store-pull-notification*, *queue-customer-recall-notification* | Teams + customer-communication channel |
| **Audit-Row server** | Writes the canonical audit record for every agent decision | *write-audit-row*, *attach-realized-impact*, *amend-audit-row-with-merchant-decision* | Audit store (typically OneLake-resident with append-only semantics) |

Each server is small, focused, and replaceable. When the underlying pricing system is upgraded, only the Pricing/Promo server changes; the agent code and every other server are untouched. When 84.51° refines its feature API, only the Customer-Features server adapts. The blast radius of a backend change is bounded to one MCP server. The full server-by-server tool catalog and contract is in the MCP Deep Dive artifact, which the lead architect should walk through during Wave-1 architecture review.

## 12.3 Server-to-tool contract — what the agents see

Each tool is a function with **typed inputs**, **typed outputs**, and an **explicit auth scope**. The agent does not see the backend; it sees a callable tool with a JSON-schema-defined input shape, a JSON-schema-defined output shape, and a well-documented error model. Calling *get-price-points-for-category* requires an auth scope that includes pricing-read; calling *propose-price-change* requires the pricing-write scope plus a merchant identity context; calling *get-segment-membership* requires the customer-feature-read scope and the call returns anonymized segment data, not raw customer identifiers.

The typed contract is what makes the agents reliable. A Stage-1 prompt-engineered agent and a Stage-3 distilled agent call the same tool with the same input shape and consume the same output shape — the model behind the agent has changed, but the tool surface is stable. This is also what makes the program multi-banner-ready: the same Margin-Exposure Agent code that serves the Kroger banner serves the Marketplace banner, the Fred Meyer banner, and the Mariano's banner because the tool surface is uniform across them. Banner-specific behavior is captured in tool implementations (the Pricing/Promo server resolves the right downstream pricing system per banner), not in agent code.

## 12.4 MCP hosting in Azure

The production hosting pattern is straightforward and Azure-native. **App Service** or **Container Apps** hosts the bulk of the MCP servers; **Azure Functions** is the right shape for the lightest-weight servers (e.g., simple notification dispatchers with no persistent state). All servers sit behind **Azure API Management** for rate limiting, throttling, monitoring, and external-facing identity boundaries.

The hosting choice between App Service and Container Apps is a discovery-driven decision; for the Kroger pattern with multiple language runtimes (the Customer-Features server may be Python, the Pricing/Promo server may be .NET, the Eventhouse server may use the official KQL SDK in either), Container Apps is often the cleaner shape for operational consistency. App Service is the right shape when the team is heavily Microsoft-stack-aligned and wants the simpler deployment model. Either pattern works; the decision is operational rather than architectural and should be pre-cleared with the Microsoft account team.

API Management at the front gives the program a clean throttling and observability layer. Every tool call is logged through API Management's standard surface; rate limits are enforced per-tool to protect downstream backends; external identities (where the surface is exposed beyond the tenant) authenticate through API Management's gateway. For internal-only servers, API Management still adds value as the uniform observability boundary.

## 12.5 MCP intersection with Purview

Every tool call is observable to Purview through the standard Azure logging surface. **Classification labels** assigned by Purview to underlying data (e.g., a customer-segment table classified as customer-PII) propagate through tool calls so that customer-PII data carries its label end-to-end — when the Customer-Features server returns segment data to an agent, the response carries the classification label, and the agent's downstream actions (writing the segment data into a recommendation, surfacing it to a merchant) inherit the label.

**DLP applies at the tool boundary.** A tool refuses to return classified data to an unauthorized agent context. If an agent operating with a merchant-decision auth scope attempts to call a tool that returns raw customer identifiers (which require a higher classification scope), the call is rejected at the MCP server before any data leaves the backend. This is the structural protection against agent-driven data exfiltration; it sits at the tool boundary because that is the only consistent gate where every agent action passes.

The intersection with Purview is also what gives the program lineage through the agent layer. Without MCP-mediated tool calls, agent reasoning is a black box from a lineage perspective — you can see what data the agent received and what recommendation it produced, but the chain of tool calls inside the reasoning is opaque. With MCP, every tool call is logged, every classification label propagates, and the lineage chain runs end-to-end from source through tool through agent through recommendation through audit row. Chapter 13 covers Purview in depth.

## 12.6 MCP intersection with Entra

Agents call tools **on-behalf-of** a human user (or a service principal for unattended scenarios). **Entra** issues the scoped tokens; the audit row captures the user identity. The Margin-Exposure Agent invoked from Cassidy's Copilot session calls tools with Cassidy's identity in the token; the audit row attributes the recommendation chain back to Cassidy; if Cassidy lacks the auth scope for a particular tool, the tool call fails with an authorization error.

This is the structural pattern that makes the agent's actions attributable to a human. Without it, agent actions are ambiguous from an audit perspective — they were taken by the system, not by anyone in particular. With on-behalf-of identity, every action attributes; the audit row is defensible; the security and compliance posture survives review. For unattended scenarios (e.g., an overnight Margin-Exposure batch run with no merchant in the loop), the agent runs as a service principal with explicit auth scopes, and the audit row attributes the recommendation chain back to the service principal — which is itself owned by a named team and bounded by explicit scope.

## 12.7 The MCP-as-product story

Long-term, the MCP servers become the integration product Kroger owns and extends. Future internal Kroger teams add tools; future LLMs and agent frameworks consume them; the investment compounds because the contract is open. The Pricing/Promo server that today serves the six-agent merchant fleet may tomorrow serve a customer-service-side agent that needs to read price-point history for a customer inquiry, a finance-side agent that needs to verify pricing decisions against a budget, or a third-party developer's agent that Kroger has chosen to grant scoped access.

This is the structural argument for why the MCP layer is **not a transient implementation detail.** The Bronze→Silver SOR is the data product; the Fabric semantic model is the consumption product; the MCP server tier is the integration product. Each compounds as the program scales; each survives model-vendor changes and agent-framework changes; each is an asset that Kroger's data and platform team owns and extends. Sellers who frame MCP as a transient layer (*"the agents will get to the data however they get to it"*) miss the strategic shape; sellers who frame MCP as a long-term product investment (*"this is your integration tier for every agent estate you build over the next decade"*) land the architecture conversation with a Chief Data Officer or Chief Architect.

> **Companion Artifacts**
> - [MCP Server Deep Dive](Services/RC-E2E-03_Assortment-and-Pricing/Tier2-Build/APEX-RC-E2E-03-MCP-Server-Deep-Dive.docx) — the server-by-server contract, tool catalog, and hosting design
> - [Service Sequence Diagram](Services/RC-E2E-03_Assortment-and-Pricing/Tier2-Build/APEX-RC-E2E-03-Service-Sequence-Diagram.html) — the request/response flow including MCP tool calls
`,
  summary: [
    'MCP is the agent-to-tool spine; multiple servers, one open contract',
    'Azure-hosted via App Service / Container Apps behind API Management',
    'Purview classification + Entra identity wrap every tool call for governance',
    'Long-term, the MCP layer is Kroger\'s integration product, not a transient detail',
  ],
  actions: [
    'Memorize the MCP server list and what each exposes',
    'Rehearse the MCP-as-product narrative for an enterprise architect',
    'Pre-clear the MCP hosting choice (App Service vs Container Apps) with the Microsoft account team',
  ],
});

chapters.push({
  num: 13, part: 3, title: 'Purview & Governance',
  objectives: [
    'Describe Purview\'s role in an agentic AI program',
    'Identify the four Purview capabilities the program uses',
    'Explain the data-classification posture from Bronze through agent decision',
    'Recognize the audit-row discipline as the regulator-ready evidence chain',
  ],
  body: `
Purview is non-negotiable. An agentic AI program without Purview is a program that cannot survive a regulatory audit, a CISO review, or a compliance-driven incident. For this program at Kroger, Purview is the governance plane that wraps every other plane — the SOR, the Fabric data plane, the Foundry agent runtime, the MCP integration tier — and turns the platform from a collection of capable components into a defensible system of record. The defensibility is the part the General Counsel and the Chief Compliance Officer care most about, and it is the part that makes the difference between a pilot and a production program.

## 13.1 Why Purview is non-negotiable in agentic AI

Three structural reasons make Purview a hard requirement, not a nice-to-have.

**Regulator pressure.** The FTC's posture on AI-driven consumer decisions, the FDA's posture on FSMA 204 evidence chains, and the patchwork of state privacy laws (CCPA, CPRA, the emerging state-level AI laws) all converge on the same operational requirement: the program must produce, on demand, a defensible record of which data informed which decision and which classification controls were applied. Without Purview, the records are reconstructed manually under deadline pressure, and reconstructed records do not survive scrutiny.

**Customer trust.** The largest headline-risk event in retail in the past decade has been the customer-data exfiltration incident — at Target, at Home Depot, at multiple grocers. The lesson is that the headline does not turn on whether the exfiltration was sophisticated; it turns on whether the grocer can credibly demonstrate that the controls were in place and working. Purview is the evidence that the controls were in place and working, and it is what lets a CISO defend the program in front of the audit committee after an incident.

**Legal defensibility.** The audit chain must be **producible** — not merely existing in some logging system, but producible in a form that opposing counsel cannot challenge as reconstructed. Purview lineage is captured automatically at the moment of data movement; it is not assembled after the fact. That is the property that makes it defensible. The General Counsel quantifies the defensibility differential in expected-value terms against the program's litigation exposure, and the math underwrites the Purview investment.

## 13.2 Data Map and classification

**Purview Data Map** scans Bronze and Silver and applies classification labels — *PII*, *PHI* (where applicable, e.g., for pharmacy operations), *financial-confidential* (for supplier-cost and margin data), *supplier-confidential* (for vendor-funded promotion contracts), and the standard public/internal/confidential tiers for everything else. The scan runs on a defined cadence (typically daily for Silver, less frequent for Bronze) and surfaces classification drift — new datasets that arrive without classification, existing datasets whose contents have shifted classification, and policy violations where classified data has landed in an unclassified zone.

Classification **propagates** through the semantic model into tool outputs. When the Customer-Features MCP server returns segment data to an agent, the response carries the classification label that was applied at the underlying feature table. When the agent writes a recommendation that incorporates segment data into the audit row, the audit row inherits the label. The classification chain runs end-to-end; the agent does not have to know what classification rules apply because the rules ride along with the data.

The classification matrix — which data class lives where, what label applies, what controls follow — is co-authored with Kroger's data-governance and 84.51° data-stewardship teams during Wave 1. The matrix is also the artifact the program presents at the data-stewardship gate; getting the matrix right early is what unblocks the rest of the program.

## 13.3 Data Loss Prevention (DLP) for agent outputs

**DLP policies** apply at the tool boundary (Chapter 12). An agent operating outside its authorized scope cannot retrieve classified data; an agent producing a recommendation with classified data attached cannot deliver the recommendation to an unauthorized surface. Both gates are enforced at the MCP server, not at the agent — which means the gates are uniform across model-vendor changes, prompt revisions, and fine-tuning iterations. The agent's behavior may evolve; the DLP enforcement does not.

The DLP posture covers two failure modes. **Data over-disclosure** — the agent retrieving more sensitive data than its decision boundary requires — is gated at the tool input by auth scope. **Data over-exposure** — the agent producing a recommendation that surfaces sensitive data into a less-controlled channel (e.g., a Teams card visible to unauthorized recipients, an export to an unmanaged endpoint) — is gated at the tool output by classification-aware delivery rules. Both gates fail closed: an unauthorized request is denied, an unauthorized delivery is blocked, and both events surface to the security team for investigation.

DLP enforcement is also what makes the program safe to scale to additional banners and additional categories without per-banner re-engineering. The DLP rules are policy-defined, not code-defined; adding a banner extends the policy scope, not the codebase.

## 13.4 Data lineage end-to-end

The lineage chain is the evidence backbone. **Source system → Bronze record → Silver entity → semantic-model exposure → tool call → agent reasoning → recommendation → HITL decision → audit row.** Every link in the chain is captured automatically — at ingestion, at conformance, at semantic-model query, at tool call, at agent recommendation, at HITL gate, at audit-row write. The capture is not a separate process the team has to remember to run; it is a property of the platform.

When a regulator or auditor asks *"how do you know this recommendation was based on accurate data,"* the answer runs the chain backward. The audit row identifies the recommendation; the recommendation identifies the agent and the model version; the model version identifies the prompt and the tool calls; the tool calls identify the semantic-model queries; the semantic-model queries identify the underlying Silver entities; the Silver entities identify the Bronze records and the conformance transformations; the Bronze records identify the source-system events with original timestamps. **End-to-end, automatic, reproducible.** This is the architectural property that makes the program survive regulatory scrutiny.

The lineage chain is also what makes incident response operable. When a data-quality issue is detected at Silver — say, a price-point entity with a wrong effective time — the lineage chain identifies every recommendation that consumed the bad data, every merchant decision that followed the recommendation, and every realized P&L delta that attributes back to the chain. The remediation is bounded; the affected decisions are identified; the merchant and finance teams can review the affected outcomes specifically rather than treating the whole program as suspect.

## 13.5 Communication compliance for HITL conversations

The HITL surface (Teams Copilot, Copilot Studio) is **communications-compliance-monitored** where required. Sensitive communications can be flagged, retained, and reviewed. For the merchant-decision flow, this typically applies to the structured override-reason capture, the margin-exposure-driven escalation conversations between category managers and the pricing director, and the supplier-funded promotion negotiations that touch the VFP Management workflow.

The communications-compliance posture is more delicate at Kroger than at many grocers because of the 84.51° boundary. Communications that touch customer segment data, propensity scores, or basket-affinity outputs need the classification-aware retention and review posture; communications that stay inside the merchant-and-margin conversation need the standard retention. The policy work is co-authored with Kroger's communications-compliance and legal teams during Wave 1 and is part of the Privacy and Data Governance Specification.

## 13.6 Audit-row discipline

The **audit row** is the canonical record of every agent decision. Each row captures:

- **Model version** — the exact hash of each upstream agent's model artifact at decision time.
- **Inputs (with classification labels)** — every input the agent received, with the classification label that applied at retrieval.
- **Prompt fingerprint** — a hash of the prompt template and any retrieval-augmented context, allowing reproducibility without storing the full prompt text.
- **Recommendation** — the full recommendation as presented, including SKU, action, predicted impact, confidence band, counterfactual.
- **Confidence** — the agent's confidence score for the recommendation.
- **Human decision** — accept, modify (with the modification captured), or reject; timestamped and identity-attributed.
- **Override reasoning if any** — the structured override-class capture from the merchant.
- **Downstream financial impact (when measurable)** — the realized P&L delta attached to the recommendation as it becomes measurable, typically days to weeks after the decision.

This is the artifact the GRC team produces in a regulatory audit. It is also the artifact finance produces when challenging a basis-point claim. It is the artifact the General Counsel produces when defending a recall response. The audit row is not an internal logging convenience; it is the regulator-ready evidence chain, and the discipline of writing it correctly at every decision is what makes the chain trustworthy.

The audit-row store itself is OneLake-resident with append-only semantics, classified at the highest tier the row's content requires (typically financial-confidential at minimum, customer-PII when the recommendation involved customer-segment inputs), and Purview-lineaged like any other Silver entity. Retention is policy-driven and typically multi-year — the FSMA 204 24-month minimum applies for the recall-related rows, and finance and legal retention requirements typically push the merchant-decision rows to similar or longer windows.

## 13.7 The Privacy and Data Governance Specification walkthrough

The Privacy and Data Governance Specification artifact lays out the controls in operational detail. Five sections anchor it.

- **Classification matrix** — the full enumeration of data classes, the labels that apply, the storage zones each is permitted in, and the retention obligation for each.
- **Retention by classification** — the policy-defined retention windows tied to each classification; FSMA-driven 24-month minimums for traceability data, multi-year retention for financial-confidential decisions, the exceptional handling for customer data that crosses the 84.51° boundary.
- **Access scopes by role** — which roles (merchant, pricing director, private-brand lead, recall responder, GRC analyst, security responder) can access which classifications, in which contexts, with which audit obligations.
- **Exit obligations** — what happens to data, audit rows, and lineage records when the program ends or when a banner is divested; the obligations that survive any commercial change.
- **Incident-response playbooks** — the structured response to a classification breach, a DLP failure, a lineage-chain gap, or an audit-row write failure.

The spec is **co-authored with Kroger's GRC team during Wave 1** — not delivered by Deloitte and reviewed by Kroger, but co-authored with shared accountability. This is the discipline that makes the spec land; specs delivered for review get edited by GRC and become political artifacts; specs co-authored from the start carry shared ownership and survive the operating cadence.

> **Companion Artifacts**
> - [Privacy & Data Governance Spec](Services/Shared-Both-Services/Tier4-Strategic/APEX-RC-E2E-03-09-Privacy-Data-Governance-Spec.docx) — the full controls document
> - [AI/ML Model Spec](Services/Shared-Both-Services/Tier4-Strategic/APEX-RC-E2E-03-09-AI-ML-Model-Spec.docx) — model-governance design that pairs with the privacy controls
`,
  summary: [
    'Purview is non-negotiable; agentic AI without Purview cannot survive an audit',
    'Four capabilities used: classification, DLP, lineage, communications compliance',
    'Lineage runs end-to-end from source system through audit row',
    'Audit-row discipline is the regulator-ready evidence chain',
  ],
  actions: [
    'Memorize the four Purview capabilities and where each applies',
    'Rehearse the audit-row pitch for the General Counsel and Chief Compliance Officer',
    'Pre-clear classification posture with 84.51° governance early in Wave 1',
  ],
});

// ---- PART IV — THE PURSUIT ----

chapters.push({
  num: 14, part: 4, title: 'Executive Engagement',
  objectives: [
    'Know what each Tier-1 Executive artifact does and when to use it',
    'Sequence executive engagements through these artifacts',
    'Rehearse the persona journey for the three target personas',
    'Recognize the recovery patterns when an executive meeting goes sideways',
  ],
  body: `
Executive engagement is the moment the program becomes real or stays a deck. Everything in Parts I through III — the strategic context, the service framing, the architectural depth — exists to support this moment. The four Tier-1 Executive artifacts are the working tools the seller carries into the room; each is engineered for a specific executive surface, a specific objection class, and a specific kind of commitment. A seller who walks in without these artifacts is improvising; a seller who walks in with them and does not know which one to reach for at which moment is just as exposed.

## 14.1 The Tier-1 Executive set in one frame

Four artifacts make up the Tier-1 Executive set. Sellers should be able to name them, describe what each does in one sentence, and recall which executive room each is built for.

The **One-pager** (RC-E2E-03 Kroger One-pager) is the five-minute artifact. It leads with the basis-point margin claim, anchors on the five margin levers from Chapter 2, sketches the Wave-1 envelope, and lands on a single executive ask. It is the artifact you hand the executive before the meeting and expect them to bring up first. It travels well — folded into a leave-behind, pasted into an email, dropped into a board pre-read packet. Its job is to make the program fit on one page without losing the substance.

The **ROI Case** (RC-E2E-03 Kroger ROI Case) is the interactive Chart.js sensitivity built for live use in the room. It lets the CFO or finance lead toggle the basis-point assumption, the Wave-1 envelope, the time-to-impact horizon, and the category footprint, then watch the resulting NPV and payback recompute in real time. It is the artifact you reach for when the conversation turns to "what does the math actually look like." Slides cannot do what this artifact does; the live interactivity is what converts skepticism faster than any static deck.

The **Personas** (RC-E2E-03 Kroger Personas) are the day-in-the-life artifacts that ground the abstract program in a single named role's reality. Three personas ship in the artifact — the Category Manager, the Pricing Director, the Private-Brand Lead — and each walks the executive through one operational day with and without the program. Use Personas with QA, Operations, or Stores leadership; use them with any executive who has not lived the merchant cycle and needs to see the human texture of what changes.

The **FSMA 204 Compliance Checklist** (RC-E2E-09 FSMA 204 Compliance Checklist) maps the FDA final rule line-by-line to the RC-E2E-09 implementation. Use it when QA, Legal, or Compliance leadership is in the room and the conversation has turned to regulatory gaps. It is the artifact that transforms a vague regulatory anxiety into a defensible, costed, sequenced plan. With the checklist on the table, the conversation moves from "are we exposed" to "what is the closure plan."

## 14.2 The One-pager — when, to whom, what to expect back

The One-pager is the artifact that runs ahead of the meeting. Hand it to the CFO, the Chief Merchant, or the CIO at least 48 hours before the meeting if you can. It is calibrated for a five-minute read in the back of a car — single page, basis-point claim above the fold, the five margin levers as the structural spine, the Wave-1 envelope and the single ask in the bottom third. It is the artifact you expect them to have read before they walk in, and the one you expect them to bring up first.

The substantive content runs along three beats. **Beat one** is the basis-point claim — sized to the prospect's specific category footprint, calibrated to a publicly-defensible industry range, and explicitly attributable to a named decision class (not "AI in general"). Beat two is the five-margin-lever framing from Chapter 2, which positions the claim against the industry-recognized lever set rather than as a vendor-invented framework. Beat three is the Wave-1 envelope (typically $500K to $1.2M for envisioning and foundation, sized to the prospect) and the single executive ask — a Wave-1 go-ahead and a named sponsor.

The expected outcome is signal, not commitment. A CFO who reads the One-pager and brings it up first in the meeting has signaled the basis-point claim has cleared the credibility gate; a CFO who reads it and does not bring it up has signaled either skepticism (in which case the ROI Case is the next artifact) or that the claim did not land (in which case the meeting is at risk and the seller needs to rebuild credibility before pitching anything more). Both signals are useful; the One-pager's diagnostic value is real.

The One-pager is also the artifact most likely to circulate beyond the room. A Chief Merchant who is intrigued may forward it to their CFO or COO peer; a CIO who is bought-in may forward it to their architecture team for technical pre-read. The artifact is built to survive that forwarding intact — the basis-point claim is sourced, the architecture is not implied, the Wave-1 envelope is illustrative, and the single ask is unambiguous. None of that is accidental.

## 14.3 The ROI Case — the interactive sensitivity

The ROI Case is the artifact built for live use in the room. It is a Chart.js-powered interactive that lets a finance lead manipulate the inputs — basis-point uplift, Wave-1 envelope, time-to-impact, category footprint, the discount rate to apply — and watch the NPV and payback recompute as the toggles move. The interactivity is the point. A static ROI table generates the question "what if the inputs change"; the interactive ROI Case answers the question by handing the CFO the toggle and inviting them to ask their own version of the question.

The right moment to bring it up is the moment the CFO challenges the basis-point claim. The challenge will come — it always does — and the response should not be to argue the number but to invite the challenger to test the math themselves. *"Let's drop the basis-point assumption to half what we've claimed and see what the case still looks like."* The Chart.js sensitivity recomputes; the NPV is still positive; the payback is still defensible; the conversation has just been reframed from "is your number right" to "even at half your number, the case clears." That is the move the artifact is built to enable.

Pre-stage the ROI Case before the meeting. Open it on the laptop you bring; pre-tune the inputs to the prospect's actual category footprint; rehearse the toggles you expect to demonstrate. The worst version of this is the seller who fumbles for the artifact mid-meeting and cannot find the right page; the best version is the seller who turns the laptop, scrolls to the sensitivity section, and hands control to the finance lead with a single sentence — *"toggle the assumptions and see where the case breaks."*

The ROI Case also serves as the asynchronous follow-up artifact. After the meeting, the link goes out with the recap email; the CFO's finance team works through it on their own schedule; the next meeting opens with the toggles they ran. The interactivity compounds across the engagement — the more the finance team interrogates the case, the more they internalize the structure, and the more the conversation moves from "do we believe the math" to "how do we sequence the wave."

## 14.4 The Persona journey artifact — Food Safety Lead day-in-the-life

The Personas artifact takes a single Kroger persona and walks them through one operational day, with and without the program. Three personas ship — Category Manager, Pricing Director, Private-Brand Lead — and the Food Safety Lead is a strong default for the FSMA 204 conversation when QA leadership is in the room. The artifact does what slides cannot: it grounds the abstract program in the concrete texture of one named role's reality, decision by decision, hour by hour.

The Food Safety Lead day-in-the-life walks the QA executive through a recall scenario from the perspective of a single operations professional whose job depends on getting it right. The morning starts with an FDA Class II recall notification; without the program, the Food Safety Lead spends the next four hours coordinating across stores, suppliers, and corporate teams to scope the impact, with the regulatory clock ticking. With the program, the recall agent has scoped the exposure inside ten minutes, queued the customer notifications, posted the regulatory hold, and drafted the FDA evidence package — the Food Safety Lead's role shifts from manual coordination to oversight and judgment, which is what their training and experience were actually meant for.

Use the Personas artifact in three contexts. **First**, with operators who have lived the work and need to see the program in operator language; the abstract architecture lands when grounded in a named role's decisions. **Second**, with executives who have not lived the work and need to see the human texture of what changes; the day-in-the-life format is more legible to a CEO or board member than an architecture diagram. **Third**, as a recovery artifact when an operator pushes back on practicality — the Personas day-in-the-life is the answer to "this won't work on the floor."

The artifact also sets up Chapter 18. The Kroger Store 412 narrative is the longer, more elaborated version of the same operator-grounded approach, scaled to a full shift with eight events. The Personas artifact prepares the room for that conversation; the Store 412 narrative closes it.

## 14.5 The FSMA 204 Compliance Checklist — when QA leadership is in the room

The FSMA 204 Compliance Checklist is the artifact for the QA, Legal, or Compliance executive. It maps the FDA final rule — every Critical Tracking Event, every Key Data Element, every retention obligation, every format requirement — line by line to the RC-E2E-09 implementation, with a status column showing where each line is closed by design, closed by configuration, closed by integration, or open and requiring discovery.

The checklist works because it inverts the typical conversation. Most regulatory pitches start with the vendor's capabilities and ask the QA team to map them back to the rule; the checklist starts with the rule and shows how the implementation maps forward to it. The QA executive does not have to translate vendor language into regulator language; the translation is already done. The conversation moves immediately to "where are the gaps in our specific posture" — which is the conversation the QA team has been wanting to have with someone who can actually close the gaps.

Bring it up the moment the conversation turns to compliance. The right opening is not a pitch but a pause: *"Here's the FDA rule, line by line, against what the implementation closes. Walk through the open lines with us — those are the discovery items."* The discipline is to let the checklist do the work; the seller's job is to listen for which lines the QA team is most concerned about, which lines they have already started addressing internally, and which lines they have not yet realized are exposing them.

The checklist also lands hard with the General Counsel because it converts a vague regulatory anxiety into a defensible, costed, line-item closure plan. A General Counsel who can hand the audit committee a document showing every FSMA 204 line and its closure status has a different conversation than a General Counsel who can only say "we're working on it." The checklist is the artifact that produces that document.

## 14.6 The sequencing playbook (one-pager → ROI → personas → checklist)

The natural sequence of executive engagement runs through the four artifacts in a predictable order. Knowing the order is what lets the seller flex it.

**Pre-read the One-pager** before the meeting. Send it 48 hours ahead if you can; carry physical copies into the meeting in case the executive has not seen it. **Walk through the One-pager in the meeting** as the opening five minutes — basis-point claim, five-lever framing, Wave-1 envelope, single ask. The One-pager sets the frame.

**Pivot to the ROI Case** the moment the CFO or finance lead challenges the math. This pivot is the most predictable transition in the playbook; the challenge will come, and the artifact is engineered to absorb it. Hand the toggle to the challenger; let the math tell the story.

**Ground in the Persona journey** the moment the operator pushes back on practicality. The pushback usually sounds like *"this won't work in stores"* or *"merchants don't have time for another tool"* — both of which are answered by walking the named-role day-in-the-life and showing where the program returns time rather than consuming it.

**Close with the FSMA 204 Checklist** if compliance is in the air or in the room. The checklist is the artifact that lets QA, Legal, or Compliance leadership leave the meeting with a costed, line-item closure plan rather than another vague regulatory anxiety.

The sequence is not rigid. A meeting with the Chief Compliance Officer alone may run the checklist first and the One-pager last; a meeting with the CFO alone may never need the Persona artifact at all. But the natural order — frame, math, ground, defend — is the order most executive conversations want to take, and a seller who knows the order can flex it intentionally rather than improvise their way through.

## 14.7 What to do when the meeting goes sideways

Every executive meeting has a moment where it could go sideways. The recovery patterns below are the moves that turn the wobble into the next artifact rather than the end of the conversation.

1. **The CFO challenges the bps claim.** The challenge usually arrives in the form *"I don't believe a 150 bps uplift is achievable in 12 months."* Drop to the ROI Case immediately. Open the laptop, scroll to the sensitivity, hand the toggle to the CFO. *"Let's see what the case looks like at 80 bps. At 50 bps. Where does it break?"* The math tells the story; the seller does not have to argue.

2. **The operator says "this won't work in stores."** The pushback is rarely about the technology; it is about the operator's lived experience of failed past programs that promised time savings and produced extra clicks. Pivot to the Persona journey. *"Let me walk you through one day for a Category Manager — same role, same week, with and without the program."* The named-role day-in-the-life lands because it grounds the abstract in concrete decisions an operator can recognize.

3. **The compliance officer raises a regulatory concern.** The concern usually arrives as *"I am not sure we are ready for FSMA 204."* Pull the FSMA 204 Compliance Checklist. *"Let me show you the rule, line by line, against what the implementation closes."* The checklist converts the anxiety into a costed closure plan; the CCO's posture shifts from defensive to action-oriented.

The worst recovery move is to argue. Arguing the basis-point claim cedes the conversational ground to the CFO's skepticism; arguing the practicality concern reinforces the operator's prior; arguing the regulatory concern signals the program does not have a defensible answer. The discipline is to pivot to the artifact that addresses the objection — and the artifact is always available because the Tier-1 Executive set is engineered for exactly these moments.

The other lesson is that the recovery patterns are predictable. The CFO will challenge the math; the operator will challenge the practicality; the CCO will challenge the regulatory readiness. None of these challenges are surprising; all of them are anticipated; all of them have an artifact engineered to absorb them. A seller who has rehearsed the recovery patterns walks into every meeting with the moves pre-staged and the artifacts ready.

> **Companion Artifacts**
> - [One-pager](Services/RC-E2E-03_Assortment-and-Pricing/Tier1-Executive/APEX-RC-E2E-03-Kroger-OnePager.html) — the five-minute executive summary
> - [ROI Case](Services/RC-E2E-03_Assortment-and-Pricing/Tier1-Executive/APEX-RC-E2E-03-Kroger-ROI-Case.html) — the interactive Chart.js sensitivity for live CFO use
> - [Personas](Services/RC-E2E-03_Assortment-and-Pricing/Tier1-Executive/APEX-RC-E2E-03-Kroger-Personas.html) — Category Manager, Pricing Director, Private-Brand Lead day-in-the-life
> - [FSMA 204 Compliance Checklist](Services/RC-E2E-09_Product-Tracking/Tier1-Executive/APEX-FSMA-204-Compliance-Checklist.docx) — line-by-line FDA-rule-to-implementation map
`,
  summary: [
    'Four Tier-1 artifacts, each engineered for a specific executive room',
    'Sequencing playbook is one-pager → ROI → personas → checklist',
    'Recovery patterns turn objections into the next artifact',
    'The worst move is to argue — pivot to an artifact instead',
  ],
  actions: [
    'Memorize which artifact addresses which objection class',
    'Rehearse one Persona day-in-the-life cold for your next meeting',
    'Pre-stage the ROI Case for live use; rehearse the toggles you will demonstrate',
  ],
});

chapters.push({
  num: 15, part: 4, title: 'The Pitch — Walking the 16-Slide Deck',
  objectives: [
    'Know the 16-slide structure of the Kroger pitch end-to-end',
    'Identify the three slides that close the meeting',
    'Rehearse the transitions between slides so the flow lands',
    'Apply audience-specific skip patterns',
  ],
  body: `
The pitch deck is the artifact that turns an executive meeting into a Wave-1 commitment. Sixteen slides, thirty minutes, three closing slides that do most of the closing work. The deck is engineered as a flow, not a slide collection — every transition is rehearsed, every closing slide does a specific job, and the audience-specific skip patterns let the seller flex the deck without losing structure. A seller who walks the deck cold misses the design; a seller who walks it well lands a Wave-1 commitment in thirty minutes.

## 15.1 The 16-slide structure overview

The deck splits into five movements: strategic context (slides 1-3), the two anchor services (slides 4-7), the architecture (slides 8-10), the commercial envelope and risk (slides 11-13), and the close (slides 14-16). The pacing is designed for thirty minutes of facilitated walk plus fifteen minutes of executive conversation; sellers who try to walk all sixteen slides in fifteen minutes end up reading slides instead of having a conversation.

| # | Title | Purpose | Time on slide |
|---|---|---|---|
| 1 | Cover + the question | Open with the question the program answers; set the executive frame | 1 min |
| 2 | The strategic context | The post-Albertsons window, the margin pressure, the open door for the program | 2 min |
| 3 | The five margin levers | The industry-recognized lever set; positions the claim against the framework | 2 min |
| 4 | RC-E2E-03 framing | What the assortment & pricing service is, in one sentence and one diagram | 2 min |
| 5 | The six agents | The decision-class-shaped agent fleet; one slide for the table | 2 min |
| 6 | RC-E2E-09 + FSMA 204 timing | The traceability anchor and the regulatory clock | 2 min |
| 7 | Why co-anchored | The shared substrate, the lower marginal cost, the combined stakeholder coverage | 2 min |
| 8 | Five-plane architecture | SOR, Fabric, Foundry, MCP, Purview — the architectural backbone | 3 min |
| 9 | Coexistence with 84.51° and Ocado | The boundary-respecting story that survives CIO review | 2 min |
| 10 | The audit-row spine | The defensibility property that closes the General Counsel | 2 min |
| 11 | Wave 1 / 2 / 3 envelopes | The commercial framing that lets the executive say yes to a small commitment | 2 min |
| 12 | Top-five risks | The risks named, the mitigations costed, the owners identified | 2 min |
| 13 | Independence and procurement | The two-contract structure (Microsoft for platform, Deloitte for services) | 1 min |
| 14 | The ask | Wave-1 envisioning go-ahead and a named sponsor | 2 min |
| 15 | Next-step calendar | Discovery sessions, workshops, SOW timeline | 2 min |
| 16 | Sponsor-ladder | Named decision-makers across CFO/CIO/CMO/QA — the coverage map | 1 min |

Total: ~30 minutes of walk. The remaining fifteen minutes of the typical executive slot is conversation, recovery, and the close. The pacing is not arbitrary; it is what fits a forty-five-minute executive meeting without compressing the closing slides.

## 15.2 Slides 1-3: setting the strategic context

**Slide 1 — Cover + the question.** The cover is not just branding; it is the question the program answers, written above the brand mark. *"Where do the next 200 basis points of operating margin come from at Kroger?"* That question, positioned where the executive sees it before any other content, frames the entire meeting as an answer to a question they are already asking. Spend one minute. Read the question aloud; pause; let it land; move on.

**Slide 2 — The strategic context.** The post-Albertsons window, the elevated investor pressure on organic margin, the constrained M&A optionality. Two minutes. The seller's job is to ground the meeting in Kroger-specific strategic reality, not generic retail commentary. The executive should hear the slide and recognize their own boardroom conversations in it.

**Slide 3 — The five margin levers.** Assortment & pricing, shrink, labor productivity, retail media, fresh-defect rate. Two minutes. Position the program against the industry-recognized framework rather than a vendor-invented one; this is what gives the basis-point claim credibility before the claim itself lands. Expect the executive to nod through this slide; they have lived these levers for years.

The transition out of slide 3 is the structural one of the deck. *"Of these five levers, the program is most differentiated on two — assortment and pricing, and traceability. Let me walk you through both."* That transition opens the second movement.

## 15.3 Slides 4-7: the two anchor services

**Slide 4 — RC-E2E-03 framing.** The one-sentence framing from Chapter 4: assortment & pricing intelligence as the merchant-decision orchestration layer on top of 84.51° features and operational data, surfaced through Copilot, governed by audit-row discipline. Two minutes. Pair the sentence with one architecture diagram showing the data flow; do not deep-dive the architecture yet, that comes in slides 8-10.

**Slide 5 — The six agents.** The agent table from Chapter 5: Margin-Exposure, Elasticity, Counter-Move, Promo-Participation, Substitution-Pattern, Composer. Two minutes. The decision-class-first naming is what makes this slide land; the executive sees that the agents are organized around their merchant team's actual decision boundaries, not around vendor-defined product categories.

**Slide 6 — RC-E2E-09 + FSMA 204 timing.** The traceability anchor and the January 2026 enforcement clock. Two minutes. Pair the service description with the regulatory timeline; the timing pressure is the door-opener for the QA, Legal, and Operations conversation, and the slide should make the timing concrete.

**Slide 7 — Why co-anchored.** The shared substrate (Bronze→Silver SOR, Fabric semantic model, Foundry agent fleet, Purview governance) and the structural reason the second anchor is 30-50% cheaper at Wave-1 than a standalone build. Two minutes. This slide is also where the combined stakeholder coverage story lands — RC-E2E-03 covers Merchant/CFO, RC-E2E-09 covers QA/Legal/COO, together they cover every margin-relevant executive at Kroger.

## 15.4 Slides 8-10: the architecture

**Slide 8 — The five-plane architecture.** The architectural backbone — SOR, Fabric, Foundry, MCP, Purview — with one diagram showing all five planes and the data flow between them. Three minutes. This is the slide a CIO will scrutinize hardest; it is also the slide that makes the rest of the deck defensible. Do not skim it; walk each plane briefly and let the CIO's attention focus where it focuses.

**Slide 9 — Coexistence with 84.51° and Ocado.** The boundary-respecting architecture story from Chapter 3. 84.51° as the upstream feature owner on GCP, read via shortcut; Ocado as the closed CFC envelope, agents on the store side of the seam; Microsoft as the decision-orchestration and experience plane. Two minutes. This slide is what takes the displacement anti-pattern off the table before it becomes an objection.

**Slide 10 — The audit-row spine.** The defensibility property that closes the General Counsel — every recommendation traceable through model version, inputs, prompt fingerprint, decision, override, and realized financial impact. Two minutes. This slide is the bridge from the architecture to the commercial conversation; the audit-row discipline is what makes the basis-point claims defensible in audit, which is what makes the Wave-1 envelope worth funding.

## 15.5 Slides 11-13: the commercial envelope and risk

**Slide 11 — Wave 1 / 2 / 3 envelopes.** The illustrative envelopes from Chapter 5 — Wave 1 at $500K-$1.2M for envisioning and foundation, Wave 2 at $4M-$8M for production deployment, Wave 3 at $10M-$25M for banner extension and cross-anchor expansion. Two minutes. The Wave-1 envelope is the focus; the larger waves are visible behind it but are not the commitment being asked for in the meeting.

**Slide 12 — Top-five risks.** The risk table from Chapter 16 — Independence pre-clearance, 84.51° governance gate, CFO basis-point credibility, Ocado-seam confusion, Microsoft account-team alignment. Each named, each costed for mitigation, each with a named owner. Two minutes. Naming the risks before the executive does is itself a credibility move; sellers who duck the risks lose the meeting at slide 12.

**Slide 13 — Independence and procurement.** The two-contract structure: Kroger's contract with Microsoft for the platform, Kroger's separate contract with Deloitte for the services. One minute. This is the slide that aligns the procurement conversation upfront and prevents the late-stage surprise where procurement asks "wait, is this a single vendor commitment" and the deal slips into a longer sourcing cycle.

## 15.6 Slides 14-16: the close (asks, next steps, sponsorship)

**Slide 14 — The ask.** The explicit Wave-1 envisioning go-ahead and a named sponsor. Two minutes. The ask is unambiguous: *"We are asking for a Wave-1 envisioning commitment in the $500K-$1.2M range, sized to the specific category footprint we identify in discovery, with a named executive sponsor who can clear the Independence pre-clearance gate this quarter."* The seller's job on this slide is to read the ask aloud and then stop talking.

**Slide 15 — Next-step calendar.** The discovery-to-SOW calendar with concrete dates. Discovery sessions in week 1-2; architecture and stakeholder workshops in week 3-4; SOW draft in week 5; signed SOW in week 6-8. Two minutes. The calendar makes the ask concrete; an executive who agrees to the ask is also agreeing to a sequence of meetings on a defined timeline.

**Slide 16 — Sponsor-ladder.** The named decision-makers across the executive surface — CFO office, CIO office, Chief Merchant office, COO/Stores office, QA leadership for FSMA 204, 84.51° leadership for governance, Microsoft account team for co-sell. One minute. The ladder is the coverage map; it shows the executive that the program has thought through who needs to know, who can block, and who can sponsor.

## 15.7 The three closing slides — what each must accomplish

The three closing slides are the slides that do most of the closing work. Each has a specific job; missing the job on any of the three weakens the close.

**Slide 14 lands the ask.** A Wave-1 envisioning commitment in a defensible envelope, with a named sponsor. The close does not happen until the executive agrees to this slide, even informally — a head-nod is sufficient, a verbal "let's do this" is ideal. If the executive sidesteps the ask on slide 14, the close has not landed yet, and slides 15 and 16 will not save it.

**Slide 15 lands the calendar.** Concrete dates for discovery, workshops, and SOW. The calendar converts the verbal commitment into a scheduled commitment; an executive who agrees to slide 14 but pushes back on the calendar in slide 15 has not actually committed, and the seller's job is to surface that gap immediately.

**Slide 16 lands the sponsorship map.** The coverage of executive decision-makers across the program's surface. This slide closes the meeting because it shows the executive that the program is not asking for their commitment alone; it is asking for their commitment as one node in a coordinated sponsorship structure that makes their Yes a defensible Yes.

The meeting closes when all three are accepted, even informally. A nodded Yes on slide 14, an agreed calendar on slide 15, and a confirmed sponsorship map on slide 16 is a closed meeting, regardless of whether a contract is in hand. The contract follows the meeting if the close lands; it does not follow if the close does not land, regardless of how good the rest of the deck was.

## 15.8 Audience-specific skip patterns

The deck flexes for the audience. The skip patterns below are the standard adaptations.

| Audience | Skip slides | Deepen slides | Why |
|---|---|---|---|
| **CFO-only audience** | 6 (FSMA 204), 8 (architecture), 9 (coexistence) | 11 (envelopes), 14 (ask) | CFO cares about the math and the commitment; deep architecture is for the CIO meeting |
| **CIO-only audience** | 11 (envelopes), 12 (risks), 14 (ask) | 8 (architecture), 9 (coexistence), 10 (audit-row) | CIO cares about the architecture and the coexistence story; commercial close happens in a separate meeting |
| **QA / Compliance audience** | 11 (envelopes), 14 (ask) | 6 (FSMA 204), 13 (procurement and Independence) | QA cares about regulatory readiness and procurement defensibility; commercial close runs through the CFO |

The skip patterns are not about cutting the deck; they are about reallocating time. A CFO meeting that skips slides 6, 8, and 9 has six minutes back to spend on the envelopes, the ROI Case sensitivity, and the sponsor-ladder conversation. A CIO meeting that skips slides 11, 12, and 14 has six minutes back to spend on the architecture deep-dive and the coexistence story. The total time stays at thirty minutes; the depth shifts.

A composite audience (CFO plus CIO, or Chief Merchant plus QA leadership) runs the full deck without skipping. The composite meeting is harder to pace because the depth has to stretch across more domains; sellers should rehearse the composite version explicitly rather than improvise the audience-specific version on the fly.

> **Companion Artifacts**
> - [Pitch Deck](Services/RC-E2E-03_Assortment-and-Pricing/Tier3-Governance/APEX-RC-E2E-03-Kroger-Pitch-Deck.html) — the canonical 16-slide deck for executive use
> - [Demo Script & Walkthrough Guide](Services/RC-E2E-03_Assortment-and-Pricing/Tier3-Governance/APEX-RC-E2E-03-Demo-Script-and-Walkthrough-Guide.docx) — the live-walk script that pairs with the deck
`,
  summary: [
    '16 slides, 30 minutes, three closing slides',
    'Slides 1-3 set the strategic frame; slides 14-16 close the meeting',
    'The three closes: ask, calendar, sponsorship',
    'Audience-specific skip patterns let the deck flex without losing structure',
  ],
  actions: [
    'Rehearse the 16-slide flow until each transition lands',
    'Pre-build your audience-specific skip pattern for the next pitch',
    'Practice the three closing slides — they do most of the closing work',
  ],
});

chapters.push({
  num: 16, part: 4, title: 'Risk & Stakeholders',
  objectives: [
    'Identify the top-five pursuit risks and the mitigation owner for each',
    'Map the stakeholder tiers (Tier-1 sponsors, Tier-2 influencers, Tier-3 informed)',
    'Sequence stakeholder engagement through the pursuit',
    'Establish the risk-mitigation rhythm (weekly cadence, by phase)',
  ],
  body: `
Every Kroger pursuit lives or dies on two things — the risks you anticipate and the stakeholders you sequence. Both are tracked in artifacts, and both decay if not refreshed. This chapter teaches the seller to read the Risk Register and the Stakeholder Map, to recognize the top-five pursuit risks and their mitigation owners, to map the three stakeholder tiers, and to establish the cadence that keeps both artifacts current as the pursuit moves through Wave 1.

## 16.1 The risk register at a glance

The Risk Register artifact enumerates the active risks across six categories — Independence, Architecture, Commercial, Stakeholder, Regulatory, and Delivery — with severity, probability, mitigation owner, and a tracker of mitigation actions and outcomes. The register is a working artifact, not a one-time deliverable; it is updated weekly at the engagement-lead level, reviewed bi-weekly with the Tier-1 sponsor, and refreshed monthly with the Lead Partner. Risks that have been closed move to a closed-risk archive; new risks are added as discovery surfaces them; severity and probability are recalibrated as the pursuit progresses.

The register's structure makes it usable as both a working tool and a leadership artifact. Sellers can read the working tool and see what they should be doing this week to mitigate the highest-severity active risks; partners can read the leadership artifact and see whether the pursuit is operating with discipline. The same document serves both audiences because the structure is consistent. Get familiar with the register early in any pursuit; the register is the artifact that distinguishes a disciplined pursuit from an improvised one.

## 16.2 The top-five pursuit risks

Five risks deserve permanent residency at the top of the register for any Kroger pursuit. Each is high-impact for Kroger specifically, each has a named mitigation owner, and each is the kind of risk that, un-mitigated, kills the pursuit before Wave 1 closes.

1. **Independence pre-clearance.** Deloitte's audit relationship with Kroger (where applicable, and where relevant audit independence rules apply) gates outbound activity. Any conversation that touches Kroger before pre-clearance is a violation of Deloitte's Independence policy and creates serious downstream exposure. Mitigation owner: **Independence Office**. The mitigation pattern is mandatory and procedural — pre-clearance request, status confirmation, documented approval before any outbound communication. The risk is permanent because Independence status can change with audit-engagement transitions.

2. **84.51° governance gate.** Any agent that uses customer data must pass 84.51° data-stewardship review before production deployment. The review is rigorous and the cycle time is non-trivial; pursuits that under-budget the 84.51° engagement timeline lose Wave 1 to Wave 2 slip. Mitigation owner: **Lead Partner with the 84.51° relationship**. The mitigation pattern is early engagement — surface the data-stewardship gate in week 2 of Wave 1, not in month 4 of Wave 2 when production deployment is being planned.

3. **CFO basis-point credibility.** An over-promised basis-point claim kills the program. The CFO's finance team will challenge the math; if the math does not survive challenge, the program loses CFO sponsorship and the rest of the executive surface follows. Mitigation owner: **Engagement Lead + Finance Lead**. The mitigation pattern is rigorous claim discipline — every basis-point claim within published industry range, attributable to a specific decision class, defensible in audit, costed against a credible Wave-1 envelope. Run the credibility test from Chapter 2 before the pitch, not in front of the CFO.

4. **Ocado-seam confusion.** Proposals that imply Ocado integration lose architectural credibility immediately at the CIO level, because the closed-CFC-envelope posture is well known. A single slide that places agents inside the Ocado stack is enough to lose the architecture conversation. Mitigation owner: **Lead Architect**. The mitigation pattern is architectural discipline — every architecture artifact (slide, diagram, runbook) reviewed for CFC-envelope clarity before circulation. The agent fleet lives on the store side of the seam; nothing in the materials should suggest otherwise.

5. **Microsoft account-team alignment.** Pursuits that bypass the Microsoft account team lose air cover. The account team holds the platform-licensing relationship, the Foundry-product relationship, and the co-sell motion that funds executive engagements; bypassing them creates internal Microsoft friction that lands on the program in Wave 2. Mitigation owner: **Co-Sell Lead**. The mitigation pattern is early and continuous coordination — joint account planning, joint executive engagement, joint pursuit reviews. The Microsoft account team is a partner in the pursuit, not an audience for it.

## 16.3 Mitigation ownership

Every risk has a named owner. This is not a documentation convenience; it is the discipline that distinguishes a pursued risk from a noted one. Un-owned risks fester because nobody is responsible for moving them; named-owner risks get worked because the owner is accountable for the mitigation tracker.

The Risk Register's ownership column is the artifact that enforces this discipline. When a risk is added to the register without an owner, the register fails its review and the engagement lead has to resolve the ownership before the next cadence meeting. When an owner leaves the engagement (rotation, role change, departure), the ownership transfers explicitly and the register is updated; the risk does not float without an owner during the transition.

The Lead Partner and the Engagement Lead jointly own the meta-discipline of risk ownership. They review the register weekly to ensure every risk has an owner, the owners are working their mitigations, and the owners are escalating where they are stuck. The discipline holds when leadership takes the meta-discipline seriously; it fails when leadership treats the register as a status report rather than a working tool.

## 16.4 The stakeholder tiering

The Stakeholder Map artifact organizes the prospect's executive surface into three tiers. Each tier has a different role in the pursuit, a different engagement cadence, and a different artifact set.

**Tier-1 sponsors** are the named decision-makers who can fund Wave 1. For a Kroger pursuit, the Tier-1 surface typically includes the CFO office (margin pressure, capital discipline), the Chief Merchant office (assortment and pricing decision velocity), the CIO office (architecture and platform commitment), the Chief Operating Officer for stores (operational productivity), and QA leadership for the FSMA 204 conversation. These are the executives whose Yes funds the program; their engagement is the gating activity for Wave 1.

**Tier-2 influencers** are the leaders who can block or accelerate the program even though they do not directly fund Wave 1. The Tier-2 surface includes 84.51° leadership (data-stewardship gate), the Microsoft account team (platform and co-sell air cover), the Restock and FreshFlex program offices (operational productivity alignment), Legal and Compliance leadership (regulatory and contractual review), and the internal architecture organization (technical due diligence). Tier-2 engagement happens through workshops and architecture reviews; the influencers' input shapes the program design and their endorsement clears the path for Tier-1 commitment.

**Tier-3 informed** are the people who need to know but do not gate the program. Delivery teams, internal IT operations, change management, and communications are the Tier-3 surface. Tier-3 engagement is communication-driven — delivery cadence updates, status reports, change-management briefings — not workshop-driven. The Tier-3 stakeholders are not less important; they are differently engaged because their role is different.

The tiering is not a hierarchy of importance; it is a hierarchy of function. A Tier-3 stakeholder whose role intersects with the program will surface as a Tier-2 influencer in a specific phase; a Tier-2 influencer whose endorsement carries Tier-1 weight in a specific room will engage as a Tier-1 sponsor for that conversation. The tiering is the working pattern, not the static assignment.

## 16.5 Engagement sequencing

The sequence is Tier-1 first. This is the discipline; pursuits that engage Tier-2 before Tier-1 has bought in are the most common cause of pursuit failure.

**Tier-1 sponsor-led discovery** opens the pursuit. The Lead Partner or Engagement Lead engages the Tier-1 sponsor through the Tier-1 Executive artifacts (Chapter 14); the sponsor's commitment to Wave-1 envisioning is the gate that opens Tier-2 engagement. Without sponsor commitment, the Tier-2 workshops are speculative — they consume influencer time without a funded vehicle to act on the inputs, and the influencers learn quickly to deprioritize the conversation.

**Tier-2 workshops** follow the sponsor commitment. Architecture workshops with the internal architecture organization; governance workshops with 84.51° data-stewardship; commercial workshops with the Microsoft account team. Each workshop has a specific output (architecture decisions, data-stewardship pre-clearance, commercial-structure alignment) that feeds the Wave-1 SOW. The workshops are facilitated, not improvised; the engagement lead carries an agenda, a desired output, and a pre-read.

**Tier-3 communication** runs continuously through the program. Delivery cadence updates, status reports, change-management briefings — all on a defined cadence, all attributable to a named communicator, all archived in the program's communications repository. Tier-3 communication is not optional; it is what prevents the surprises that destroy program credibility in Wave 2.

The sequencing failure mode is to pitch at Tier-2 before Tier-1 has committed. The architecture team is intrigued by the technology; the Microsoft account team is excited about the co-sell; the 84.51° team is willing to engage on data stewardship — and none of them can fund Wave 1, so the engagement cycles through Tier-2 conversations indefinitely without converting to a commitment. The discipline is to hold Tier-2 engagement until Tier-1 has committed, even when Tier-2 conversations are easier to schedule.

## 16.6 The risk-mitigation rhythm

Risks decay if not refreshed. The cadence below is the working rhythm that keeps the Risk Register current and the mitigations moving.

**Weekly engagement-lead review.** Every week, the engagement lead reviews the Risk Register with the named mitigation owners. Active risks get a status update; closed risks move to the archive; new risks are surfaced and added; severity and probability are recalibrated against the week's events. The review takes thirty to sixty minutes depending on the active register size; it is non-negotiable. A weekly review that is skipped becomes a monthly review that catches stale information.

**Bi-weekly Tier-1 sponsor review.** Every two weeks, the engagement lead reviews the top risks with the Tier-1 sponsor. This review is shorter (fifteen to thirty minutes) and focused on the top-three to top-five active risks. The sponsor's role is to clear blocks, escalate where escalation is required, and provide the air cover for mitigation actions that need executive sponsorship. The bi-weekly cadence is what keeps the sponsor engaged in the working pursuit rather than only the executive moments.

**Monthly Lead Partner review.** Every month, the engagement lead reviews the full register with the Lead Partner. This review is the quality gate — is the discipline holding, are the owners working their mitigations, are new risks being surfaced as discovery progresses, is the pursuit on track. The monthly cadence is also where the Lead Partner sees the cross-pursuit pattern and can apply lessons from other engagements to this one.

The rhythm is the discipline. A pursuit that runs the weekly, bi-weekly, and monthly reviews on cadence has a Risk Register that reflects reality; a pursuit that skips the cadence has a Risk Register that is theater. The Tier-1 sponsor and the Lead Partner can tell the difference quickly, and the difference shows up in pursuit outcomes.

> **Companion Artifacts**
> - [Risk Register](Services/RC-E2E-03_Assortment-and-Pricing/Tier3-Governance/APEX-RC-E2E-03-Kroger-Risk-Register.xlsx) — the active risk tracker, weekly cadence
> - [Stakeholder Map](Services/RC-E2E-03_Assortment-and-Pricing/Tier3-Governance/APEX-RC-E2E-03-Kroger-Stakeholder-Map.xlsx) — the Tier-1/Tier-2/Tier-3 surface and engagement plan
`,
  summary: [
    'Top-five risks: Independence, 84.51° governance, CFO bps credibility, Ocado-seam confusion, MS account-team alignment',
    'Every risk has a named mitigation owner',
    'Three stakeholder tiers; sponsor-first sequencing',
    'Weekly risk-review cadence at engagement-lead level',
  ],
  actions: [
    'Read the Risk Register cold; identify your top three risks for this specific pursuit',
    'Map your prospect\'s stakeholders into the three tiers before any outbound',
    'Pre-build your Tier-1 engagement calendar — sponsor first',
  ],
});

chapters.push({
  num: 17, part: 4, title: 'The Demo — Walking RC-E2E-03 Live',
  objectives: [
    'Walk the demo storyline end-to-end',
    'Know the three branch points where the demo can pivot',
    'Identify the safety nets for technical failures',
    'Rehearse the recovery patterns',
  ],
  body: `
A great demo lands the program. A bad demo costs the next meeting. The structure here is engineered to maximize the chance of the former — one merchant, one decision, one HITL gate, three branch points where the demo can pivot to the audience's interest, three safety nets in case the technology stumbles, and three post-demo questions that move the conversation from interest to commitment. The discipline is rehearsal; the artifact is a script; the worst version is the demo run cold.

## 17.1 Demo storyline at a glance

The demo is structured around one merchant making one decision through one HITL gate. The merchant is the Category Manager from Chapter 5 — Cassidy, the dairy category manager. The decision is a margin-defense recommendation in private-label dairy; a competitor has moved private-label whole milk down 5% over the weekend, and the Counter-Move Agent has surfaced a recommended response with the Elasticity Agent's impact modeling and the Composer's prioritized merchant queue framing. The HITL gate is the Copilot card where Cassidy approves, modifies, or rejects with reasoning.

The flow runs about twelve minutes when walked cleanly. Two minutes setting the merchant context (who Cassidy is, what her week looks like, what queue she opens on Monday morning). Three minutes walking the agent reasoning chain (the Counter-Move Agent picked up the move from the Sunday-morning pricing feed, the Elasticity Agent modeled three response scenarios, the Composer prioritized the recommendation with confidence band and counterfactual). Three minutes on the Copilot HITL surface (the recommendation card, the rationale expansion, the override-reason taxonomy). Two minutes on the audit-row capture (model version, recommendation, decision, override if any, attribution to Cassidy's identity). Two minutes on the realized-impact loop (how the recommendation's outcome flows back into the model-tuning cycle).

Twelve minutes is the clean walk. The realistic walk is fifteen to twenty minutes because the audience interrupts with questions, and the questions are usually the most valuable part of the demo. The seller's job is to handle the interruptions without losing the storyline; the script is the spine, the questions are the conversation.

## 17.2 The three branch points where pivot is possible

Three moments in the demo allow the seller to pivot the conversation to the audience's specific interest. Knowing the branch points is what lets the seller flex the demo without abandoning the structure.

**Branch 1 — at the data-grounding moment.** The first branch is at the moment the agents reach back into the data plane to ground the recommendation. If the audience is data-curious — a Chief Data Officer, a data-platform leader, an analytics-org executive — the seller can pivot here into the SOR conversation: how the Bronze→Silver layer carries the source data, how the Fabric semantic model exposes it through MCP tools, how the agents query the semantic model through typed contracts rather than raw SQL. The branch ends with the recommendation grounded; the storyline resumes.

**Branch 2 — at the agent-recommendation moment.** The second branch is at the moment the Composer surfaces the prioritized recommendation. If the audience is technically curious — a CTO, an enterprise architect, an AI/ML platform lead — the seller can pivot here into the agent-architecture conversation: the six-agent fleet, the model-routing logic, the maturation path from prompt-engineered through fine-tuned through distilled, the cost-per-decision economics. The branch ends with the recommendation surfaced to Copilot; the storyline resumes.

**Branch 3 — at the HITL-approval moment.** The third branch is at the moment Cassidy makes her HITL decision in Copilot. If the audience is operator-curious — a COO, a Chief Merchant, an operations leadership team — the seller can pivot here into the persona conversation: how the merchant's day changes, how the override-reason taxonomy compounds into the labeled-example asset that feeds Stage-2 fine-tuning, how the audit row attributes the decision to Cassidy's identity in a way that survives finance challenge. The branch ends with the decision captured; the storyline resumes.

The branches do not extend the demo by twelve more minutes each; they extend it by two to four minutes when handled with discipline. The seller's job is to recognize the audience cue, take the branch, hit the branch's substantive point, and return to the storyline. Sellers who take a branch and do not return lose the storyline; sellers who recognize the cue and do not take the branch leave the audience's interest unaddressed. The discipline is in the recognition and the return.

## 17.3 The safety nets

Live demos fail. Network drops, models go slow, Foundry endpoints cold-start, data freshness gaps surface mid-walk. The discipline is to pre-stage the safety nets in order of preference; the seller's job is to know which net to reach for at which failure mode.

1. **Live demo working as expected.** The goal. Connectivity is solid, the model responds in single-digit seconds, the Foundry endpoint is warm, the Copilot card renders cleanly, the audit row writes correctly. When this is the state, the demo carries itself; the seller's job is to narrate and field questions.

2. **Pre-rendered screenshots ready.** The first net. Every step of the demo has a pre-rendered screenshot capturing the expected state — the Counter-Move Agent's pricing-feed input, the Elasticity Agent's impact curves, the Composer's prioritized queue, the Copilot card, the audit-row write. When the live system is sluggish or a tool times out, the seller pivots to the screenshot for that step without breaking the narrative — *"while we're waiting for the system to respond, this is what the agent's output looks like in the production environment."* The screenshot carries the story; the demo continues.

3. **Recorded video fallback.** The second net. A 90-second recorded walkthrough of the full demo flow, captured from a previous clean run, available on the seller's local machine and on a cloud share for redundancy. When the demo environment is fully unavailable — connectivity dropped, the Foundry workspace is down, the Copilot integration is broken — the seller pivots to the video, narrates over it, and preserves the storyline. The video is not the preferred outcome but it is materially better than abandoning the demo; the audience sees the flow even if they do not see it live.

The order matters. Sellers who reach for the video at the first sign of latency over-rotate; the screenshot is the right intermediate step. Sellers who try to recover a fully-failed demo with screenshots over-rotate the other way; if the environment is down, the video is the right call. The discipline is to recognize the failure mode and pick the right net.

## 17.4 What can go wrong

Five common failure modes show up in demos at this level of complexity. Each has a known recovery; the recovery patterns are in the next section.

| Failure mode | Likelihood | Recovery |
|---|---|---|
| Network drop | Medium | Pivot to pre-rendered screenshots for the affected steps; if recovery is sustained, pivot to recorded video |
| Model latency (10+ second response time) | High | Tell the story over the spinner — "the system is reasoning, not stalled" — and continue narrating |
| Foundry endpoint cold start | Medium | Pre-warm the endpoint 15 minutes before the demo; if cold-start surfaces anyway, narrate what is happening and pivot to screenshots if recovery exceeds 30 seconds |
| Data freshness gap (recommendation built on stale data) | Low-Medium | Acknowledge the gap explicitly and pivot to the agent-architecture branch — "in production this would be flagged automatically by the freshness SLO" |
| Persona credibility challenge from the audience | Medium | Invite the challenger into the demo as the persona — "what would you decide here?" — and let them walk the HITL decision |

The likelihood column is illustrative — actual likelihood depends on the demo environment's operational maturity, the audience's technical sophistication, and the network conditions at the venue. Sellers should expect at least one of these failure modes per demo and rehearse the recovery for each.

## 17.5 The recovery patterns

For each failure mode, the recovery is a single move and a single sentence. The discipline is to have the move and the sentence pre-rehearsed, not improvised.

**Network drop.** The move is to pivot to screenshots. The sentence is *"while the connection is recovering, let me show you the same flow from a recent production capture."* The screenshot covers the next step; the seller narrates from the screenshot until connectivity returns.

**Model latency (the model is slow).** The move is to tell the story over the spinner. The sentence is *"the system is reasoning, not stalled — it is composing the recommendation across the upstream agent outputs and the merchant calendar; in production this typically takes 8-12 seconds."* The narration fills the dead air and turns the latency into demonstrable depth rather than a stall.

**Foundry endpoint cold start.** The move is the same as model latency for short delays; for longer delays, pivot to screenshots. The sentence is *"this is a cold-start latency you would not see in production — production endpoints are warm and respond inside 2 seconds — but it gives me a chance to walk through what the agent is composing."*

**Data freshness gap.** The move is to acknowledge it explicitly and pivot to the agent-architecture branch. The sentence is *"the recommendation looks built on slightly stale data — in production the freshness SLO would have flagged this and the agent would have downgraded its confidence accordingly. Let me walk through how the freshness SLO works."* The acknowledgment turns a credibility hit into a credibility win; the seller is showing they understand the failure mode.

**Persona credibility challenge.** The move is to invite the challenger into the demo as the persona. The sentence is *"you have lived this decision more than I have — what would you do here? Let me hand you the HITL surface and let you walk the decision."* The invitation flips the dynamic from defensive to participatory; the challenger becomes a co-narrator rather than an adversary.

The recovery patterns work because they are pre-rehearsed. A seller who is improvising the recovery in front of the audience signals discomfort; a seller who delivers the recovery sentence in a calm, prepared tone signals depth. The audience cannot tell the difference between a planned move and a recovered move when the move is well-rehearsed.

## 17.6 The post-demo question set

The demo is not the close; the post-demo questions are. Three pre-prepared questions move the conversation from interest to commitment. The seller asks them; the audience's answers reveal whether the demo landed and whether the pursuit is moving.

**Question 1: "What would you change about the recommendation?"** The question invites the audience to engage with the agent's reasoning. An audience that engages — *"I would weight the basket-affinity higher"* or *"the counterfactual should account for the upcoming vendor meeting"* — has internalized the agent's role and is positioning themselves as a future user. An audience that demurs — *"hard to say without more context"* — is still in observer mode, and the seller needs another conversation to convert them. Either answer is useful diagnostic information.

**Question 2: "Where in your current process would this gate sit?"** The question grounds the abstract program in the audience's operational reality. A merchant audience will name the specific step in their merchandising review cycle; a CIO audience will name the specific integration point in their existing platform; a CFO audience will name the specific point in the budget-review cadence. The answers reveal both the audience's operational understanding and their seriousness about adoption.

**Question 3: "What would your CFO want to see in the audit row?"** The question moves the conversation to the defensibility property. A merchant audience will reference the model version and the override reasoning; a CIO audience will reference the lineage chain and the classification labels; a CFO audience will reference the realized impact and the model-version reproducibility. The answers tell the seller which executive surface is most engaged and which artifact (the audit-row spec, the lineage walkthrough, the realized-impact dashboard) to bring up in the next conversation.

The three questions are sequenced from most-tactical to most-strategic. Sellers should ask all three; the answers compound. A demo that ends with the audience having answered all three questions is a demo that has converted from presentation to dialogue, which is the prerequisite for the next-meeting commitment.

> **Companion Artifacts**
> - [Demo Script & Walkthrough Guide](Services/RC-E2E-03_Assortment-and-Pricing/Tier3-Governance/APEX-RC-E2E-03-Demo-Script-and-Walkthrough-Guide.docx) — the canonical demo script and live-walk guide
> - [Sequence Diagram](Services/RC-E2E-03_Assortment-and-Pricing/Tier2-Build/APEX-RC-E2E-03-Service-Sequence-Diagram.html) — the request-and-response architecture for the agent flow
`,
  summary: [
    'One merchant, one decision, one HITL gate — the demo storyline',
    'Three branch points let the demo pivot to audience interest',
    'Three safety nets in order: live, screenshots, video',
    'Three post-demo questions move the conversation to commitment',
  ],
  actions: [
    'Rehearse the demo cold three times before the first client run',
    'Pre-stage the safety nets for every demo',
    'Internalize the three post-demo questions',
  ],
});

chapters.push({
  num: 18, part: 4, title: 'Kroger Store 412 — A Day in the Shift',
  objectives: [
    'Experience what an agentic-AI program looks like in production at a Kroger Marketplace store',
    'Understand the eight events that anchor the narrative',
    'Recognize how HITL gates surface in operator-grounded language',
    'See the audit-row discipline expressed in operational terms',
  ],
  body: `
> **Independence Reminder**
> Store 412, the named operations lead persona, every event in this narrative, and every dollar figure cited are illustrative. This chapter is not a description of any actual Kroger store deployment. The operational events, the financial-impact figures, and the timing details are constructed to illustrate what an agentic-AI program looks like in production at a Kroger Marketplace store; they are not claims about The Kroger Co. Any resemblance to specific actual incidents at specific actual stores is coincidental.

> **Note**
> Lift this chapter unchanged into client-facing materials. APEX is not named below by design. When presenting this narrative to Kroger executives, frame the work as "Deloitte-delivered agents on Kroger's Microsoft platform." The accelerator name stays internal to Deloitte teams; the chapter body is engineered to be client-clean as written.

## 18.1 The shift at a glance

Marisol Reyes is the Operations Lead at Kroger Marketplace Store 412 in suburban Cincinnati. She has been with Kroger for eleven years — four as a front-end supervisor at a Westside store, three as an assistant manager at a smaller banner format, and the past four leading operations at Store 412 through the Marketplace conversion. She knows the dairy walk-in's compressor by sound, the bakery's lot-code system by memory, and the names of every associate on her shift. The narrative below traces one Tuesday in April, from her 5:50 AM swipe-in through the early afternoon, across eight operational events that show what a fleet of production agents on Kroger's Microsoft platform looks like in the day-to-day reality of a single store.

\`\`\`mermaid
timeline
    title Kroger Store 412 — One Shift, Eight Events
    05:50 : Event 01 Critical<br/>Cold-chain excursion<br/>Dairy walk-in 4 hours
    07:15 : Event 02 High<br/>Fresh-produce shrink<br/>Bagged salad anomaly
    08:42 : Event 03 High<br/>ESL desync<br/>Private-brand center-store
    10:08 : Event 04 Medium<br/>Phantom OOS<br/>22 baby-aisle SKUs
    11:30 : Event 05 Critical<br/>FDA Class II recall<br/>Infant formula lot
    12:15 : Event 06 Low<br/>BOPIS substitution<br/>Organic milk
    13:50 : Event 07 High<br/>Shrink pattern<br/>Register 12 spirits
    14:45 : Event 08 Critical<br/>Customer incident<br/>Foreign object in muffin
\`\`\`

One shift. Eight events. Roughly one hour of total manager touch across the eight events. About 5.5 hours of manager time returned against the pre-program baseline. About $22,000 in financial impact protected across cold-chain savings, shrink avoidance, sales protection, recall execution, and customer-incident management.

| Event # | Time | Severity | Orchestration | Domain |
|---|---|---|---|---|
| 01 | 5:50 AM | Critical | Cold Chain | Supply Chain / Food Safety |
| 02 | 7:15 AM | High | Shrink / Fresh | Merchandising / Fresh |
| 03 | 8:42 AM | High | Price Integrity | Merchandising |
| 04 | 10:08 AM | Medium | OSA Triage | Merchandising |
| 05 | 11:30 AM | Critical | Recall | Food Safety / Compliance |
| 06 | 12:15 PM | Low | Substitution | Customer Experience |
| 07 | 1:50 PM | High | Shrink Signal | Loss Prevention |
| 08 | 2:45 PM | Critical | Customer Incident | Quality / Legal |

## 18.2 Event 01 — Cold-chain excursion in the dairy walk-in (5:50 AM, Cold Chain)

**Situation.** Between 1:42 AM and 5:38 AM the dairy walk-in cooler held at 46-49 °F against a 38 °F threshold for refrigerated dairy. The compressor's soft-start contactor failed in the early-morning window when the store was closed and no associate was on the floor; the unit cooled back into compliance about twelve minutes before Marisol's swipe-in. By the time she walked into the office at 5:50 AM, her phone already held a disposition-ready brief on the affected inventory across 34 SKUs and 287 units.

**Agents at work.** A cold-chain telemetry agent had been monitoring the walk-in's temperature stream into the operational data plane continuously through the night. A correlation agent joined the four-hour temperature excursion to the lot-level inventory in the walk-in — gallon and half-gallon milk across three brands, yogurt cups across the private-brand and national-brand portfolio, soft cheese, and prepared dairy desserts. Kroger's published food-safety thresholds by sub-category split the affected inventory into save-viable (sealed, low-pathogen-risk packaging that briefly held above threshold but stayed below the public-health bright line) versus mandatory-destroy (ready-to-consume dairy that crossed the bright line). A quarantine task was queued for the 6:00 AM dairy clerk; case labels were pre-printed at the service desk. A write-off pre-approval with the telemetry chart attached was routed to Marisol's Teams card for a single-tap decision.

**Marisol's HITL decision (6:02 AM).** *"Approve $1,840 targeted write-off on the ready-to-consume items. Save the sealed gallon milk and the unopened yogurt cases — pull them for visual inspection by the dairy clerk before they go back on the shelf. Get the refrigeration vendor on the phone for the compressor service."*

**Outcome.** 73% of the affected inventory saved through the targeted disposition. $4,180 in write-off avoided against a $6,020 total exposure. Doors opened at 6:30 AM with the dairy walk-in re-stocked from the save-viable pool. Time-from-temperature-recovery to disposition-brief: 14 minutes. Manager touch on the decision: 90 seconds. Audit trail: complete, with the four-hour temperature curve, the lot-level inventory at exposure, the per-SKU disposition decision, and Marisol's approval all attributed to a single audit row defensible to the FDA inspector and to the Kroger food-safety team.

**How Deloitte delivered this.** Microsoft Fabric Eventstream and Eventhouse ingested the cold-chain telemetry continuously through the night; agents running on Azure AI Foundry performed the correlation between the temperature excursion and the lot-level inventory, applied the food-safety threshold logic, and composed the disposition brief; Microsoft Teams Copilot rendered the HITL approval card with the telemetry chart in-card; Microsoft Purview classified the inventory-loss evidence chain and stamped the lineage; the audit row attributes the $4,180 saved write-off to this specific decision at this specific store on this specific morning.

## 18.3 Event 02 — Fresh-produce shrink anomaly on bagged salads (7:15 AM, Shrink/Fresh)

**Situation.** At 7:15 AM the agent surfaced an anomaly on the bagged-salad endcap. POS velocity for two specific SKUs (organic spring-mix triple-pack and chopped-romaine kits) had been running 60% below the four-week trailing average for the prior three days. Receiving condition on the most recent two truck deliveries had been logged as marginal — leaf integrity acceptable but warmer-than-spec at the dock. Shelf-life math against the receive date said the affected lots had 48 hours remaining; absent intervention, the projected write-off was about $1,200 across the two SKUs.

**Agents at work.** A fresh-shrink agent had been correlating POS velocity, receiving-condition logs, and lot-level shelf-life math continuously across the produce department. The agent surfaced the bagged-salad anomaly with two recommended response paths — a targeted 25% markdown on the aging lots to clear them at a margin loss but above the destruction-cost threshold, or an immediate pull and donation routing to the food-bank partner that Kroger maintains a standing relationship with. The agent included the per-path math: markdown projected $720 in margin recovered against the $1,200 write-off baseline; donation projected $0 in margin but a tax-treatment offset of about $180 plus the avoided-destruction cost of about $90.

**Marisol's HITL decision (7:21 AM).** *"Markdown twenty-five percent. Print the shelf-talkers, walk the produce manager through it, run the markdown through end-of-day Thursday. If they don't move by 2 PM Thursday, pull and donate."*

**Outcome.** Markdown applied at 7:35 AM; both SKUs cleared by Wednesday afternoon at the markdown price. Realized margin recovery: $680 against the $720 projected, within the agent's confidence band. Write-off avoided. Manager touch: 2 minutes including the produce-manager handoff. Audit trail: complete, with the velocity anomaly, the receiving-condition data, the lot-level shelf-life math, the markdown decision, the realized clearance, and the financial-impact attribution all in a single row.

## 18.4 Event 03 — ESL desync on private-brand center-store (8:42 AM, Price Integrity)

**Situation.** The ESL gateway dropped the overnight pricing push for a slice of center-store private-brand items — the regular price stayed on the shelf labels, but the POS rang a Tuesday-Wednesday promotional price that was lower by 8-15% across the affected items. By the third transaction at 8:38 AM the agent had caught the gap, frozen the further loss at the register, and staged the remediation. Marisol got the alert in her Teams card at 8:42 AM with the loss already contained.

**Agents at work.** A price-integrity agent monitored the POS transaction stream against the active promotional schedule and the ESL gateway state. At 8:36:22 the agent detected a divergence between the rung price and the shelf-displayed price across three transactions on different items in the affected slice; by 8:38:14 the third transaction had triggered the agent's confidence threshold, and the agent suspended the stale shelf-price override at the registers — POS now rang the regular shelf price on those items, eliminating the further margin erosion. A paper-tag print job for the 64 affected SKUs was queued at the service-desk printer to bridge until the ESL gateway recovered. The ESL vendor was ticketed automatically with the gateway log; root cause was traced to a firmware handshake issue after the prior evening's vendor software push.

**Marisol's HITL decision (8:46 AM).** *"Print the tags, walk the center-store aisle with whichever associate is on it, get the ESL vendor on the line. If they can't restore by 11 AM, escalate to the district manager."*

**Outcome.** Loss frozen at three transactions; the further 4-6 hours of margin erosion that would have run before the next manual price audit was prevented. 64 SKUs remediated with paper tags within 35 minutes. ESL gateway restored at 10:50 AM; paper tags pulled and ESL labels re-synced by 11:30 AM. Total margin erosion contained to about $24 across the three transactions. Manager touch: 90 seconds for the decision, plus the standing supervision of the paper-tag walk. Audit trail: complete, including the ESL gateway log, the divergence detection, the agent's automatic suspension of the stale override, and Marisol's remediation decision.

## 18.5 Event 04 — Phantom OOS on 22 high-velocity baby-aisle SKUs (10:08 AM, OSA)

**Situation.** Computer vision from the shelf-edge cameras, four-hour rolling POS velocity, and the perpetual inventory system all agreed: 22 high-velocity SKUs across the baby aisle were showing zero on the shelf while the perpetual-inventory system said 387 units were in the backroom across those SKUs. This is the classic phantom-OOS pattern — backroom stock present, shelf empty, no manager involved in identifying the gap, customers turning away or substituting. The agent caught it on the morning sweep, sorted the pull-list by velocity, and assigned the pick task to the most-available associate without a manager debate.

**Agents at work.** An on-shelf-availability agent fused shelf-camera computer vision (latest sweep at 10:04 AM), POS velocity (four-hour rolling), and perpetual inventory position. Across the baby aisle, the agent confirmed 22 empty facings against 387 backroom units. A planogram lookup generated aisle-by-aisle pick locations sorted by velocity. The pick task was assigned to associate Diego R. — the most-available associate by his current handheld zone, his radio status, and his last-task completion time. Diego's handheld received the prioritized pick list at 10:09 AM.

**Marisol's decision (10:08 AM).** *"Acknowledged."* (No HITL approval required for this routine remediation; the agent's automatic assignment is the operational pattern, the manager sees the alert for awareness only.)

**Outcome.** All 22 facings restocked in 41 minutes. No manager walk; no category-team escalation. Sales protected: about $2,840 across the rest of the day at average baby-aisle velocity. Historically, this class of phantom-OOS event was caught either by store walk (which Marisol does once or twice per shift, at random) or by customer complaint to a clerk (which then escalates to the manager and consumes 20-30 minutes of investigation per event). Manager touch on this event: 5 seconds for the acknowledgment.

## 18.6 Event 05 — FDA Class II infant-formula recall (11:30 AM, Recall)

**Situation.** At 11:28 AM the FDA posted a Class II recall on a specific lot of infant formula across multiple distribution channels nationally. By 11:30 AM the recall agent had resolved the entire FSMA 204 Critical Tracking Event chain for the affected lot at Store 412 — receiving event, transfer event, current shelf and backroom inventory, and 14-day customer-purchase exposure — and Marisol's phone alert finished playing while the disposition-ready brief was already on her screen.

**Agents at work.** Within four minutes of the FDA post, the recall agent ran the lot identifier through the Fabric Eventhouse FSMA 204 traceability records. The agent resolved the upstream lineage — supplier shipment, DC receipt, transfer to Store 412, store receiving event — and the downstream exposure. Exposure quantified: 41 units on shelf at Store 412, 88 units in the backroom, 27 units sold in the prior 14 days (24 attributed to loyalty-customer transactions, 3 to anonymous tender). A pull-from-shelf task was generated for two associates; quarantine bay QB-02 was designated. A bilingual customer notification (English and Spanish, email plus SMS) with prepaid return label and full refund was drafted for the 24 loyalty-attributed customers — held for manager release. A regulatory hold was posted to the POS so any remaining units that scanned at register would block the sale and prompt the cashier to direct the customer to service. The full FSMA 204 evidence package — five Critical Tracking Events with all required Key Data Elements, Traceability Lot Code chain, retention metadata — was assembled and ready for FDA submission within ten minutes of the recall post.

**Marisol's HITL decision (11:38 AM).** *"Release the customer notifications — I'll oversee the floor pull personally. Get me Corporate Communications on the line before the SMS goes; they'll want to coordinate the customer-service script. Tell the QA lead I want a confirmation when the lineage package is in the FDA portal."*

**Outcome.** 129 units pulled from shelf and backroom and quarantined in 18 minutes. 24 loyalty customers reached via the bilingual notification within 45 minutes of the FDA post; 21 of the 24 acknowledged the notification within the same hour. Full FSMA 204 lineage submitted to the FDA portal at 12:45 PM, well inside the 24-hour regulatory window. Benchmark equivalent recall-execution events at a single store historically consumed 4-6 hours of manager and supervisor time just to scope the impact; Marisol's total touch on this event was about 12 minutes including the phone calls. The 27 customer transactions were defensibly traced back to the lot through the loyalty data and the POS basket records; the 3 anonymous-tender transactions were unrecoverable, which the FSMA 204 framework anticipates and accepts.

## 18.7 Event 06 — BOPIS substitution on organic milk (12:15 PM, Customer Experience)

**Situation.** A BOPIS picker hit an empty shelf on a half-gallon organic whole milk SKU for a customer named Rachel whose order pickup was scheduled for 1:00 PM. Thirty-eight seconds later, Rachel had tapped accept on a proposed substitute through the Kroger app. The event illustrates what the autonomous customer-experience class looks like when the agents handle the full loop without surfacing to a manager.

**Agents at work.** The pick exception triggered the substitution agent at 12:15 PM. The agent retrieved Rachel's 18-month substitution acceptance history — she accepts conventional whole milk when organic is unavailable, rejects size upsizes, accepts the in-house Kroger brand when name-brand is unavailable. Three candidate substitutes were ranked by predicted acceptance: the agent's top pick was the Kroger-brand conventional half-gallon whole milk at a $1.20 lower price point, with an SMS notification offering one-tap accept or one-tap reject. Rachel tapped accept at 12:15:38; the picker's handheld received the substitution confirmation; the order line moved to picked status; the price adjustment flowed to the order total automatically.

**No HITL required.** Fully autonomous. The substitution surfaces to the manager only if the customer rejects all proposed candidates, if the substitution exceeds an aging threshold without customer response, or if the substitution involves a class of product where store policy requires human review (alcohol, regulated pharmacy items, certain prepared foods).

**Outcome.** Order fulfilled on the original 1:00 PM pickup slot. Customer experience preserved through the personalized substitution. Manager shield intact — this is the class of event that silently consumes the majority of the floor lead's day in the pre-program operational pattern. Resolution: 38 seconds end-to-end. Manager touch: 0.

## 18.8 Event 07 — Shrink pattern on register 12 — spirits (1:50 PM, Shrink Signal)

**Situation.** A 72-hour pattern tripped the shrink-signal agent's confidence threshold at 1:48 PM. The pattern: register 12, one specific cashier on consecutive shifts (Monday day, Monday evening, Tuesday day), an anomalous void cadence on high-value spirits (4.6× the normal void rate per spirit transaction), no matching return receipts on the voided items, and a downstream inventory variance in spirits that aligned with the void volume. Not an accusation — a structured evidence package with statistical confidence and a recommended escalation path.

**Agents at work.** The shrink-signal agent correlated POS void patterns by register and cashier (4.6× normal rate on spirits transactions), inventory variance for the affected SKU set (spirit inventory short by an amount that closely matched the voided dollar value), associate schedule (3 of 3 consecutive days on register 12), and the absence of matching customer return receipts across the 72-hour window. The agent's confidence band was computed; surfacing to the manager surface was suppressed until the pattern crossed the 3σ threshold (it did at 1:48 PM). The evidence timeline was assembled, including CCTV-frame timestamps that the loss-prevention team would need to pull (the agent does not move CCTV footage; it surfaces the timestamp references). The case was held behind a loss-prevention-only surface; the cashier and the front-end supervisor were not notified directly.

**Marisol's HITL decision (1:54 PM).** *"Escalate to loss prevention with the package. No conversation with the cashier from me — handle this through proper procedure. Confirm to me when LP has acknowledged."*

**Outcome.** Loss-prevention investigation opened with a clean, statistically-grounded evidence package. The associate's due-process protections preserved through the LP-only surface; Marisol stays out of the direct line of inquiry, which protects both the investigation integrity and the associate's right to a properly-conducted process. Pattern statistical confidence: 3.2σ. Evidence rows: 48 (POS void timestamps, inventory variance records, schedule confirmations, CCTV-frame references). Manager touch: 90 seconds for the decision and the LP handoff confirmation.

## 18.9 Event 08 — Customer incident — foreign object in bakery muffin (2:45 PM, Customer Incident)

**Situation.** A customer named Mr. Patel came to the customer-service desk at 2:42 PM with a sealed package of muffins from the in-store bakery, a clear photograph showing a small piece of clear plastic visible inside one of the muffins through the window of the package, and the receipt from his purchase the prior afternoon. The customer-service associate paged Marisol; the agent was already pulling the lot code from the photo by the time Marisol got to the desk.

**Agents at work.** An OCR agent extracted the lot code (B-2451-0421) from Mr. Patel's phone photo and confirmed the lot against the bakery product master. The lot was resolved to a specific overnight bakery production run on April 21 — the affected baking line, the time window, the specific batch of muffin batter. A cross-match against open customer-incident cases at other Kroger Marketplace stores in the central-Ohio region surfaced two prior low-severity complaints on the same lot at two different stores within the prior 36 hours — both had been treated as one-store incidents. With the third complaint, the pattern crossed the agent's threshold for cross-store escalation. A Tier-2 case was opened automatically; QA leadership at the regional level, Legal, and Corporate Communications were notified in parallel at 2:45 PM. The agent recommended a proactive pull of the affected lot at the 12 other stores in the region that received product from the same overnight run, before additional customer complaints landed.

**Marisol's HITL decision (2:51 PM).** *"Full refund to Mr. Patel plus a $50 gift card and a written apology. Preserve his package and the photo as evidence — bag it, label it, log it, give him a receipt for the bag. Get me the regional QA lead on the line — we have to coordinate the cross-store pull tonight before the 12 other stores' overnight bake runs go out."*

**Outcome.** Mr. Patel left the store at 3:05 PM with refund, gift card, written apology, and the receipt for his preserved package. Full case file assembled in 7 minutes — the manual lot-trace and cross-store correlation that this event would have required pre-program would have consumed 45-60 minutes of Marisol's time and would not have caught the cross-store pattern at all (the prior two complaints would have remained one-store incidents). More substantively: pattern detection enabled the proactive pull at 12 other stores starting at 4:00 PM that afternoon, before any of those stores had logged additional customer complaints. What presented as a single-store customer incident converted into a regional-scale quality signal with proactive containment. Legal posture: evidence preserved with chain-of-custody documentation; coordinated regional response on the record.

**How Deloitte delivered this.** The OCR extraction, the lot-master resolution, the cross-store complaint correlation, the proactive-pull recommendation, and the multi-stakeholder notification orchestration all run on the agent fleet that Deloitte delivered onto Kroger's Microsoft platform. The cross-store pattern detection compounds across the network — every store's customer-incident events feed back into the regional pattern recognition, and every recognized pattern triggers proactive containment before customer complaints scale.

## 18.10 Shift summary

| Metric | Value |
|---|---|
| Events handled across the shift | 8 |
| Agent-resolved or decision-prepped | 6 of 8 (2 events fully autonomous, 4 events decision-ready with HITL) |
| HITL decisions Marisol made | 6 (avg ~95 seconds per decision) |
| Financial impact protected | ~$22,000 (write-off avoidance, shrink prevention, sales protection, recall containment, customer-incident mitigation) |
| Manager time returned vs pre-program baseline | ~5.5 hours across the shift |
| Total manager touch across all 8 events | ~1 hour |
| Audit-defensible decision rows produced | 8 (one per event, with full lineage) |
| Regulatory submissions assembled | 1 FSMA 204 lineage package, submitted within 75 minutes of FDA post |
| Customer-experience events resolved without manager touch | 1 (BOPIS substitution, fully autonomous) |
| Cross-store quality patterns detected | 1 (bakery foreign-object lot, 12-store proactive pull initiated) |

## 18.11 Why this narrative matters

Marisol's shift is not a pitch deck. It is a concrete illustration of what an agentic-AI program looks like when it is running in production at a Kroger Marketplace store, with the ordinary operational friction of a Tuesday in April handled by a fleet of agents that surface decisions to the operations lead in operator-grounded language, attribute every decision to a defensible audit row, and return the operator's day to the work that only an operator can do.

When a Kroger executive asks what the program actually does at the store level, the answer is in this shift. Eight events of the kind that consume an operations lead's day in the current operational pattern; six of them resolved either fully autonomously or with a single HITL decision averaging 95 seconds; financial impact of about $22,000 protected through a single shift at a single store; about 5.5 hours of manager time returned. Scaled across the Kroger store network and across operating days, the headline labor-capacity recovery and the headline financial-impact protection are both substantial — and both are auditable, attributable, and defensible to the FDA inspector, the corporate finance team, the regional QA lead, and the regional loss-prevention team.

The narrative also shows what changes operationally. Marisol does not lose her judgment, her relationships with the associates, or her standing on the floor; she gets all of those back, because the agents are handling the routine decision triage that previously consumed her morning. The agents do not replace her judgment — they prepare it, ground it in data, and let her exercise it in seconds rather than spending hours assembling the inputs. The audit row makes her decisions defensible in a way the pre-program operational pattern could not: every decision attributed, every input traced, every outcome measurable. That is the substantive shift the program produces.

## 18.12 How to use this narrative in client conversations

The narrative flexes for the audience. Use it whole when the conversation has the room (45+ minutes of executive time and an audience that engages with operational texture); use selected events when the conversation is shorter or when a specific stakeholder cares about a specific event class.

- **With operations executives (COO, VP Stores, VP Operations).** Walk the eight-event day to show real operational texture. The pattern language — cold-chain excursion, ESL desync, phantom OOS, FSMA 204 recall execution, shrink signal, customer incident — resonates with operators who have lived these events through the current operational pattern and recognize the texture immediately.

- **With CFOs.** Anchor the $22,000 single-shift financial-impact protection scaled to the Kroger store count and operating days. The arithmetic is illustrative, but the structure is the point: per-store, per-shift, decision-attributable, audit-defensible. Pair the shift summary table with the ROI Case (Chapter 14) and let the CFO's finance team work through the sensitivity.

- **With CIOs and Chief Digital Officers.** Walk the architecture inside the events — the Microsoft Fabric Eventstream and Eventhouse carrying the cold-chain telemetry, the Foundry agents handling the correlation and disposition, the Teams Copilot rendering the HITL surface, the Purview classification stamping the evidence chain. The five-plane architecture is visible in every event; the architectural conversation lands harder when grounded in the operational moment than when presented as an abstraction.

- **With Chief Compliance Officers and General Counsels.** The FSMA 204 recall execution in Event 05, the loss-prevention due-process preservation in Event 07, and the cross-store pattern detection on the bakery lot in Event 08 all demonstrate regulator-ready and litigation-defensible decision attribution. The audit row is the spine; the General Counsel sees what the litigation-defense posture looks like in the operational moment.

- **With procurement.** The services that produced these outcomes are the services on offer. The commercial structure is two contracts: Kroger's contract with Microsoft for the platform (Fabric, Foundry, Copilot, Purview, identity, networking) and Kroger's separate contract with Deloitte for the services that delivered the agents onto the platform. The two-contract structure is what makes the procurement conversation clean.

- **With QA leadership.** Events 01 (cold-chain), 05 (FSMA 204 recall), and 08 (cross-store quality pattern) are the QA-relevant trio. Walk all three; the operational texture makes the regulatory story more concrete than a checklist walk-through, and the FSMA 204 evidence package in Event 05 demonstrates the 24-hour-FDA-response capability in operational form.

> **Independence Reminder**
> Store 412, Marisol Reyes, the eight events, the financial figures, the timing details, and every operational specific in this chapter are illustrative. This chapter is not a description of any actual Kroger store deployment, of any actual Kroger Marketplace store, of any actual Kroger associate, or of any actual customer. The narrative is constructed to illustrate what an agentic-AI program looks like in production at a Kroger Marketplace store; it is not a claim about The Kroger Co. Sellers must not represent this chapter as a description of an actual deployment in any client conversation.

> **Note**
> When presenting this narrative to Kroger executives, describe the work as "Deloitte-delivered agents on Kroger's Microsoft platform." Never name the internal accelerator in front of the client. The accelerator name stays internal to Deloitte teams; the chapter body has been engineered to be client-clean so it can be lifted into client-facing materials unchanged. The framing — "Deloitte-delivered agents on Kroger's Microsoft platform" — is the consistent positioning across every executive surface, every artifact, and every conversation.

> **Companion Artifacts**
> - [Pitch Deck](Services/RC-E2E-03_Assortment-and-Pricing/Tier3-Governance/APEX-RC-E2E-03-Kroger-Pitch-Deck.html) — the 16-slide deck this narrative supports
> - [Demo Script & Walkthrough Guide](Services/RC-E2E-03_Assortment-and-Pricing/Tier3-Governance/APEX-RC-E2E-03-Demo-Script-and-Walkthrough-Guide.docx) — the live-walk demo that complements this narrative
> - [ROI Case](Services/RC-E2E-03_Assortment-and-Pricing/Tier1-Executive/APEX-RC-E2E-03-Kroger-ROI-Case.html) — the financial-impact sensitivity that scales the per-shift figures to the network
`,
  summary: [
    'One shift, eight events, ~5.5 manager hours returned, ~$22K decision-attributable financial impact',
    'Six HITL decisions averaging 95 seconds each',
    'Two events fully autonomous (no manager touch)',
    'Client-presentable as-is — accelerator name never appears in body',
  ],
  actions: [
    'Read this chapter end-to-end before any client conversation that touches store operations',
    'Lift the relevant 1-2 events for the specific stakeholder you are meeting',
    'Never name the internal accelerator while presenting this narrative — the accelerator name stays internal',
  ],
});

module.exports = { all: chapters, appendices };
