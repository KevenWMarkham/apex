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

module.exports = { all: chapters, appendices };
