# APEX · Store 100 — Facilitator Guide

**Document class:** Facilitator guide (Account Team enablement)
**Companion to:** `apex-rc-store-100-shift-walkthrough.html` (the narrative)
**Audience:** DMTSP Account Teams running client conversations with the Store 100 reference implementation
**Current as of:** APEX Core v1.2 (2026-04-17)
**Related:** `docs/APEX-solution-overview.docx` · `docs/APEX-RC-agent-catalog.docx`

---

## Part 0 — Compliance & Language Constraints (Inherited)

This guide inherits Part 0 of APEX Core unchanged. All Deloitte–Microsoft terminology rules apply. The HTML walkthrough and this guide use synthetic reference-implementation identifiers — Store 100, Marisol Reyes, DFW Metroplex, Apr 14 2026, the eight event timestamps. These are scenario data, not client data.

**Scenario-vs-engagement boundary.** This guide is *reusable* across engagements. Real client-engagement specifics — actual store numbers, real manager names, client-identifiable ROI figures, named vendors, named regulators — belong in engagement-specific deliverables, not in this document. When an Account Team uses this guide with a live client, the facilitator maps Store 100's synthetic scenarios to the client's actual operational equivalents verbally; the document itself stays synthetic.

**HITL gate types** follow Core Part 8.3 unchanged: `HITL` (decision required), `ACK_ONLY` (visibility only), `ZERO_TOUCH` (fully autonomous), `ESCALATION` (deferred to higher authority). Wave references (W1–W4) follow Core Part 12.

---

## Part 1 — How to Use This Guide

The HTML walkthrough tells the story. This guide tells you how to use the story in three specific meeting settings.

### 1.1 Discovery meeting (first client conversation)

- **Goal:** Establish that APEX has a concrete, credible answer to "what does agentic actually look like in a retail store."
- **How to use:** Walk 3 of the 8 events. Pick ones that match the pain the client has already named (stockouts → Event 04; recalls → Event 05; shrink → Event 07).
- **Time budget:** 25–30 minutes.
- **Leave-behind:** The HTML walkthrough and the solution overview.

### 1.2 Architecture review (technical audience, CIO/CTO or their delegates)

- **Goal:** Show that every scenario binds to concrete Microsoft-native infrastructure, a specific canonical schema, and a specific orchestration. No hand-waving.
- **How to use:** Walk all 8 events, but lean on the **APEX Cross-Walk** field in each event sheet. Name the ORCH, the agents by catalog ID, the schema entities, the HITL gate type. Use the RC Agent Catalog as a companion — hand it to them.
- **Time budget:** 60–75 minutes.
- **Leave-behind:** Overview + catalog + HTML walkthrough + solution stack (when available).

### 1.3 CMM assessment (positioning for wave commitment)

- **Goal:** Map each scenario to a wave, get the client to pick their starting wave.
- **How to use:** Lead with the aggregate ROI pitch (Part 12). Then walk 4 events from W1 (the ones they'll see in their first 90 days). Then name the wave-exit criteria. Close with the next-meeting checklist (Part 14).
- **Time budget:** 45 minutes.
- **Leave-behind:** This guide's Part 14 checklist — signed.

---

## Part 2 — Store 100 at a Glance

The HTML walkthrough compresses an imagined 9-hour shift into one document. Eight exception events between 5:58 AM and 2:32 PM. One store manager on duty — Marisol Reyes. One agentic fleet working the perimeter.

**The headline:** eight events, one hour of manager touch.

Every event follows the same APEX shape:

1. **Schema lights up** — canonical entities in the edition's Silver/Gold layers record the event.
2. **Agent responds autonomously** — the fleet classifies the situation, pulls history, pre-stages the decision.
3. **Human is engaged at the gate** — Marisol gets a decision-ready brief or an acknowledgment, not a raw alert.
4. **Outcome is recorded** — audit trail complete, metrics captured, state updated.

### 2.1 The 8-event grid

| # | Time | Severity | Event | ORCH |
|---|---|---|---|---|
| 01 | 5:58 AM | Critical | Reefer 14 cold-chain excursion | ORCH-03 Cold Chain & Disposition |
| 02 | 7:20 AM | High | DSD short-ship (beverage rep) | ORCH-01 DSD Reconciliation & Claims |
| 03 | 8:36 AM | High | 127 stale ESL tags on pet aisle | ORCH-02 Pricing Integrity |
| 04 | 10:15 AM | Medium | 18 empty shelves, backroom stock present | ORCH-04 Labor & Fulfillment |
| 05 | 11:43 AM | Critical | Infant formula recall | ORCH-05 Recall Impact |
| 06 | 12:32 PM | Low | BOPIS spinach out, substitution needed | ORCH-06 Fulfillment Exception |
| 07 | 1:47 PM | High | 4.2× void rate on spirits register | ORCH-07 Shrink & Loss Prevention |
| 08 | 2:32 PM | Critical | Plastic fragment in sealed muffin | ORCH-08 Customer Incident Response |

Each event binds to a different orchestration. In one shift, Store 100 exercises **8 of the 12 RC orchestrations** — which is why this walkthrough carries disproportionate weight in a client conversation. It is not a demo of one agent; it is a demo of the orchestrated fleet.

---

## Part 3 — Reader's Kit

Bring these to every meeting where you use the Store 100 walkthrough:

| Artifact | Path | When to reach for it |
|---|---|---|
| Store 100 HTML walkthrough | `.../Walmart/02_projects/apex-rc-store-100-shift-walkthrough.html` | Primary narrative — open on the screen. |
| APEX Solution Overview (Word) | `docs/APEX-solution-overview.docx` | When the client asks "what is APEX?" — point to Part 1–4. |
| RC Agent Catalog (Word) | `docs/APEX-RC-agent-catalog.docx` | When the client asks about a specific agent — look up the card live. |
| This facilitator guide | `docs/APEX-Store-100-facilitator-guide.docx` | Your own side-monitor. Not shown to the client. |
| RC build spec | `apex-rc-build-spec-v2.md` | If pushed on a definition or convention — the source of truth. |

**One rule:** never lead with the catalog or the build spec. Those are reference; the HTML is the story. Pull the reference forward only when the client asks a question the story doesn't answer.

---

## Part 4 — Event 01 · 5:58 AM · Reefer 14 Cold Chain

### Event summary
Critical severity. Between 02:15 and 06:27 the dairy endcap held at 48–52°F against a 41°F threshold. The compressor soft-start failed overnight. By the time Marisol swipes in, the case has been cooling back for twenty minutes and a disposition-ready brief is waiting on her phone.

### The hook
*"Marisol's phone lit up before her badge did. Here's why that matters."*

### APEX cross-walk

| Concept | Binding |
|---|---|
| ORCH | ORCH-03 · Cold Chain & Disposition |
| Primary agents | SCM-A04 Cold Chain Telemetry Monitor · SCM-A05 Disposition Classifier · SCM-A06 Write-Off Pre-Approver |
| Primary schema | SCML |
| Key entities | COLD_CHAIN_TELEMETRY · TEMPERATURE_EXCURSION · STORE_INVENTORY_POSITION |
| HITL gate | **HITL** — Marisol confirms save/destroy and approves the $534 targeted write-off after visual inspection |
| Wave | W2 (Expansion) |
| Microsoft services | IoT Hub + Event Hubs (L2) · OneLake/ADX for telemetry (L3) · Logic Apps (L6) · Teams notification (L7) |

### Talking points

- The agent didn't wait for Marisol to arrive. The entire save/destroy classification was done on telemetry the client was *already emitting* — we just added the controls plane.
- **Sub-category risk scoring** is what distinguishes "save the sealed cheese" from "destroy the ready-to-eat dairy." Three of your agents today would say "destroy it all." APEX doesn't.
- The write-off is *targeted*. Not a blanket 412-unit loss. The claim is linked to a specific telemetry case file — the audit trail exists before the adjuster asks for it.
- **Total manager touch: 90 seconds.** That is the number the client should anchor on.

### Common client questions

**Q: "What if the CV/telemetry gets it wrong and we destroy product we could have saved?"**
A: The disposition classifier reports a confidence band. Below threshold, the case flips from ACK_ONLY to HITL — the manager sees the split and can override. Above threshold, the manager sees the recommendation but still has the final approval tap. False-save errors are the regulated risk; false-destroy errors are the financial risk. We calibrate the threshold to the sub-category.

**Q: "Who owns the write-off policy decisions — us or you?"**
A: The client. The agent stages the write-off; the approval routing lives in the client's finance system. Deloitte never holds the approval handle. This is explicit in Core Part 6 Independence posture.

### The ROI point

Walmart's industry average write-off rate on cold-chain excursions hovers around 60–70% destroy (most operators can't distinguish risk by sub-category fast enough). Store 100's targeted write-off: **71% *saved*** — $1,313 avoided on a $1,847 exposure. Multiply by the number of cold-chain excursions per store per year, multiply by store count — this single scenario often justifies W1 on its own.

### Next step

This is the **flagship W2 scenario**. Use it to pin the client's W1 → W2 transition to cold-chain MVP. Frame: *"By the time you exit W1 you have the receiving and price-integrity foundation. W2 lights up cold chain."*

---

## Part 5 — Event 02 · 7:20 AM · DSD Short-Ship

### Event summary
High severity. RFID portal scan on the inbound dock clocks 44 cases against an invoice of 48. Before the beverage rep reaches the back office, the agent has built the dispute package and surfaced the vendor's 90-day pattern: three short-ships on this vendor in 90 days.

### The hook
*"The beverage rep was still walking to the back office when the claim was already drafted. With evidence."*

### APEX cross-walk

| Concept | Binding |
|---|---|
| ORCH | ORCH-01 · DSD Reconciliation & Claims |
| Primary agents | SCM-A01 DSD Reconciliation · SCM-A02 Vendor Pattern Detector · SCM-A03 Claim Assembly |
| Primary schema | SCML |
| Key entities | ASN · STORE_RECEIVING_EVENT · RECEIVING_DISCREPANCY · DSD_INVOICE |
| HITL gate | **HITL** — Marisol signs disputed receipt; Accounts Payable receives a pre-built claim |
| Wave | W1 (Foundation) |
| Microsoft services | Event Hubs (L2) · Lakehouse (L3) · Logic Apps (L6) · Vendor portal webhook (L1) |

### Talking points

- The value isn't in catching this *one* short-ship. The value is in the vendor pattern — three of four short-ships in 90 days is no longer noise; it's a conversation with the category manager.
- Historically this reconciliation happens a week later, post-invoice, with weak evidence. Now it happens at the dock. Your claims win rate changes.
- **The rep's iPad gets a "sign disputed" line pre-filled.** The agent isn't telling the rep what to do — it's giving the manager a one-tap way to formalize what the scan already said.
- This is a **W1 scenario** — cheap, fast, concrete. Perfect for anchoring a W1 pitch.

### Common client questions

**Q: "Vendors won't agree to RFID portals at the door — we've tried."**
A: Agreed — portal adoption is engagement-specific. The APEX pattern works with whatever capture mechanism the client already has — barcode scan at pallet receipt, weight-on-scale, handheld audit. RFID is the ideal case; the pattern generalizes.

**Q: "What if we file a dispute and the vendor disputes the dispute?"**
A: The dispute package carries timestamped evidence: portal logs, dock camera frame references, historical pattern. Contestable claims are materially fewer when evidence ships with the claim. We don't eliminate disputes; we shift the burden.

### The ROI point

**$142.56 claim, filed with strong evidence before the truck left the lot.** The per-claim dollar is small; the compound effect is large. Stores this size see 40–80 DSD discrepancies per week. Historical win rate on disputed claims without evidence: ~30%. With evidence: ~70%. Apply the delta across 52 weeks × store count.

### Next step

This is a **W1 anchor**. Put it on the wave-commitment worksheet as one of the first two ORCHs Store 100 lights up in the first 90 days.

---

## Part 6 — Event 03 · 8:36 AM · 127 Stale ESL Tags

### Event summary
High severity. Overnight ESL push silently failed on the pet aisle gateway. Shelf shows regular; POS rings promo. By the fourth customer transaction, the agent catches the gap, freezes the loss, stages customer refunds, and drafts the ESL bridge tag sheet.

### The hook
*"One hundred twenty-seven tags went stale overnight. Four customers rang through at the wrong price before the fleet caught it. The fifth didn't."*

### APEX cross-walk

| Concept | Binding |
|---|---|
| ORCH | ORCH-02 · Pricing Integrity |
| Primary agents | MER-A04 ESL Gateway Monitor · MER-A05 POS Mismatch Detector |
| Primary schema | MERML |
| Key entities | PRICE_RECORD · PRICE_TAG_STATUS · PROMOTION_ACTIVATION · POS_VOID |
| HITL gate | **ACK_ONLY** (on auto-refund) → **HITL** on refunds exceeding a threshold |
| Wave | W1 (Foundation) |
| Microsoft services | ESL gateway API (L1) · Event Hubs (L2) · Lakehouse (L3) · Logic Apps (L6) · SMS / receipt printer (L7) |

### Talking points

- Pricing integrity failures are **silent** by default. The ESL gateway doesn't tell you when it drops a push; you find out from the customer refund line.
- The **bridge tag** mechanism turns a 2-hour problem into a 90-second problem. Paper tags get printed at the service desk; an associate walks the aisle; the gateway gets restarted in parallel.
- Customer refunds are *staged automatically* for transactions that already happened — the customer doesn't have to come back.
- **This is a W1 scenario** because ESL monitoring is the simplest orchestration to stand up: one gateway API, one POS event stream, one MERML schema. No CV, no lot tracing, no regulatory feeds.

### Common client questions

**Q: "What if we don't have ESL today — only printed tags?"**
A: The price-integrity ORCH still applies; the gateway-monitor agent doesn't. The POS-mismatch detection works regardless of the display mechanism (it's a comparison between POS ring and the authoritative price record). ESL is an acceleration lever, not a prerequisite.

**Q: "How does the agent know to stage refunds automatically — is that not a legal/compliance exposure?"**
A: The threshold is policy-driven. Below X dollars per transaction, auto-refund and ACK_ONLY to the manager. Above X, HITL gate. Policy is client-owned, written into the ORCH configuration. Agents execute policy; they don't define it.

### The ROI point

**4 rings at wrong price before catch, 127 SKUs corrected in 14 minutes, loss frozen at ~$18.** Without APEX, this typically runs 2+ hours and $200–400 in loss per incident. Frequency is 1–3 incidents per store per week on average ESL fleets. Compound across the fleet.

### Next step

W1 anchor. Pair with Event 02 (DSD) to argue the **W1 "reconciliation pair"** — receiving and pricing are the two foundations. Everything else builds on knowing what's in the store and what it costs.

---

## Part 7 — Event 04 · 10:15 AM · Empty Shelves With Backroom Stock

### Event summary
Medium severity. Eighteen OSA (on-shelf availability) events cluster across two aisles. Perpetual inventory says "in stock" — but CV sees empty facings and POS velocity has flatlined for 40 minutes. All 18 items have backroom stock.

### The hook
*"Eighteen empty shelves. All of them had backroom stock. The perpetual said everything was fine."*

### APEX cross-walk

| Concept | Binding |
|---|---|
| ORCH | ORCH-04 · Labor & Fulfillment |
| Primary agents | MER-A06 Phantom OOS Detector · MER-A07 Pick List Optimizer · MER-A08 Associate Router |
| Primary schema | MERML |
| Key entities | STORE_INVENTORY_POSITION · OSA_EVENT |
| HITL gate | **ZERO_TOUCH** on detection + pick-list generation; **ACK_ONLY** to associate via handheld |
| Wave | W1 (Foundation) |
| Microsoft services | Shelf CV (L1 edge) · Event Hubs (L2) · Lakehouse (L3) · Agent Service (L6) · Associate mobile (L7) |

### Talking points

- **Phantom OOS is the canonical retail problem.** Perpetual says stock exists, shelf is empty, customer walks. The CV + POS + perpetual *fusion* is what detects it.
- The **pick list optimizer** doesn't just list 18 items — it orders them by walking route. That is 6–12 minutes saved per replenishment cycle.
- The **associate router** knows who is free, who is in zone, and whose radio is active. Tasks get dispatched to the right associate, not broadcast.
- **This is a ZERO_TOUCH orchestration** — the manager doesn't see any of this unless a task ages out past SLO. The human only enters on exception.

### Common client questions

**Q: "We don't have shelf CV everywhere. Does this still work?"**
A: Phantom OOS detection has a graceful degradation path. Without CV, we rely on POS velocity + perpetual inventory + shelf-capture handhelds. Detection rate is lower but the ORCH still fires. CV is the accelerator; it's not mandatory.

**Q: "Associates are going to push back on being routed by an algorithm."**
A: Agreed — and this is a change-management conversation, not a technical one. The system shows the associate what, not when. Prioritization is the associate's call; the system provides the ordered list. We've seen associate adoption accelerate once they realize the system saves them walking miles per shift.

### The ROI point

Phantom OOS costs retailers 3–8% of category sales on affected SKUs. For Store 100's size, this single 18-event cluster represents ~$440 in at-risk sales. Detection latency dropped from "customer complaint" (hours) to CV signal (minutes). Frequency: 10–25 phantom events per store per day.

### Next step

**W1 capstone scenario.** The client feels the labor benefit viscerally — associates stop walking blind routes. Put this on the wave-commitment worksheet as the W1 scenario that shows operational ROI most clearly.

---

## Part 8 — Event 05 · 11:43 AM · Infant Formula Recall

### Event summary
Critical severity. FDA posts a Class II recall at 11:43. Four minutes later the agent has resolved the affected lot upstream to the supplier, downstream to 9 transactions in the last 21 days, and identified the customers (where loyalty data permits). Marisol sees a customer notification queue ready to dispatch.

### The hook
*"The recall posted at 11:43. By 11:47 she knew exactly who bought it."*

### APEX cross-walk

| Concept | Binding |
|---|---|
| ORCH | ORCH-05 · Recall Impact |
| Primary agents | SCM-A07 FDA Feed Listener · SCM-A08 Lot Trace Resolver · (MER-A12 Markdown Cadence Agent for in-aisle pull) |
| Primary schema | SCML (plus CXML for customer resolution) |
| Key entities | RECALL_NOTICE · LOT_TRACE · LOYALTY_STATE · CUSTOMER_INCIDENT |
| HITL gate | **HITL** — recall coordinator (not Marisol) confirms customer-notification scope before dispatch |
| Wave | W2 (Expansion) |
| Microsoft services | FDA public feed (L1 external) · Event Hubs (L2) · Lakehouse (L3) · Agent Service (L6) · Teams + SMS dispatch (L7) |

### Talking points

- **Four minutes from FDA post to notification-ready.** The previous process took hours — sometimes days — to resolve which stores, which customers, which lots.
- **Lot trace is bidirectional:** upstream to identify which vendor/batch/supplier is implicated; downstream to identify which customers purchased the affected lot.
- The agent does **not** dispatch notifications autonomously. Recall communications are an HITL gate at the recall coordinator — this is both a legal requirement and a brand-trust requirement.
- This scenario **binds three schemas**: SCML (recall + lot trace), CXML (customer loyalty state), MERML (in-aisle product pull). It's a natural demo of the cross-schema event envelope.

### Common client questions

**Q: "Customer notification on a recall — how does this stay consent-compliant?"**
A: The agent respects the same consent flags the marketing stack honors (MKTL · SEGMENT_MEMBERSHIP suppression rules). A customer who has opted out of non-transactional contact doesn't receive a marketing nudge — but they do receive a safety notification per policy. The distinction is encoded in the ORCH configuration, not the agent logic.

**Q: "What's the false-match rate on downstream customer identification?"**
A: Lot-to-transaction match is high-confidence (lot codes are explicit on receiving). Transaction-to-customer match depends on loyalty penetration. For Store 100-style formats, 40–60% of transactions have customer ID; the remainder get in-store signage and POS-flagged notifications on next visit.

### The ROI point

**The ROI is not monetary — it's brand-and-regulatory.** A four-minute notification-ready window transforms recall posture from "we'll get back to you" to "here is our response playbook, executed." On Class I recalls that difference is material to regulatory relationships and can materially affect brand trust.

### Next step

This is a **W2 scenario** that the C-suite cares about disproportionately. Use it to pull the CFO or General Counsel into the conversation. It's the event that proves APEX is not just about stockouts.

---

## Part 9 — Event 06 · 12:32 PM · BOPIS Spinach Substitution

### Event summary
Low severity. Jennifer (online customer) ordered for 1:00 PM pickup. The associate picking for her hits an OOS on organic spinach. Before the associate even asks, the agent has ranked three substitution candidates, one-tap SMS'd Jennifer, and is tracking the SLA clock.

### The hook
*"Jennifer's spinach was out. Marisol never heard about it."*

### APEX cross-walk

| Concept | Binding |
|---|---|
| ORCH | ORCH-06 · Fulfillment Exception Handling |
| Primary agents | CXM-A01 Pick Exception Handler · CXM-A02 Substitution Ranker · CXM-A03 Customer Confirm Gateway |
| Primary schema | CXML |
| Key entities | FULFILLMENT_ORDER · PICK_EXCEPTION · SUBSTITUTION_EVENT |
| HITL gate | **HITL — the customer is the human.** Marisol never sees this unless the customer doesn't respond. |
| Wave | W2 (Expansion) |
| Microsoft services | BOPIS order source (L1) · Event Hubs (L2) · Lakehouse (L3) · Agent Service (L6) · SMS gateway (L7) |

### Talking points

- **Marisol doesn't see this event.** That is the point. Low-severity customer-facing exceptions never touch the manager.
- The **14-month substitution history** is what makes the ranker credible — it's not "closest-SKU fallback." It's "this customer has accepted 'baby spinach' as a substitute for 'organic spinach' 7 of 9 times."
- **SMS aging** means the clock is watched. If Jennifer doesn't tap within 4 minutes, the order state transitions; the agent doesn't stall the pickup.
- **This is the shopper-trust scenario.** Customers cite substitution handling as a top-3 BOPIS satisfaction driver. APEX turns it from a manager problem into a ranked shortlist with a one-tap confirm.

### Common client questions

**Q: "What if the customer doesn't respond at all — do we substitute or refund?"**
A: Policy-driven. Most clients configure: under 4 minutes no-response → default-substitute (if confidence is high); over 4 minutes → default-refund. The ORCH respects whichever policy the client configures.

**Q: "How does this handle multi-item exceptions — three OOS in one order?"**
A: The ranker processes them as a batch and sends a single consolidated SMS ("We have 3 substitutions to confirm"). The customer taps once per item; the whole batch is tracked under the same SLA clock.

### The ROI point

**Customer touch without manager touch.** The metric the client cares about is: what fraction of BOPIS exceptions are resolved without manager intervention? Store 100's target is >95%. Without APEX, 40–60% of exceptions escalate to the manager at some point.

### Next step

Pair this with Event 04 (Phantom OOS) to pitch the **W2 customer-experience bundle.** The argument: once you've nailed the in-store inventory accuracy (W1), the W2 wave lets you extend that accuracy to the omnichannel customer promise.

---

## Part 10 — Event 07 · 1:47 PM · 4.2× Void Rate on Spirits

### Event summary
High severity. The void pattern detector flags Register 7's void rate on the spirits category at 4.2× the 90-day sigma baseline. One employee. Pattern is corroborated by a returns-without-receipt cluster on the same category, same shift, same employee. The agent builds the evidence package and routes to Loss Prevention.

### The hook
*"Four-point-two times the void rate. Only on spirits. Only on this register. Only on this shift."*

### APEX cross-walk

| Concept | Binding |
|---|---|
| ORCH | ORCH-07 · Shrink & Loss Prevention |
| Primary agents | MER-A09 Void Pattern Detector · MER-A10 Variance Correlator · MER-A11 Evidence Package Builder |
| Primary schema | MERML |
| Key entities | POS_VOID · SHRINK_EVENT · CYCLE_COUNT_VARIANCE |
| HITL gate | **ESCALATION** — Loss Prevention takes ownership; the agent never acts on the employee directly |
| Wave | W2 (Expansion) |
| Microsoft services | POS stream (L1) · Event Hubs (L2) · Lakehouse (L3) · CCTV index (L1) · Agent Service (L6) |

### Talking points

- **ESCALATION is the critical gate here.** The agent does not fire anyone. The agent does not even flag the employee to Marisol. It routes the evidence package to Loss Prevention per client policy.
- The **sigma anomaly + category isolator + employee-register correlator** is the decomposition that makes this specific, not generic. "Void rate is high" is not actionable. "Void rate is 4.2σ above baseline, on spirits, on register 7, on shift 2" is actionable.
- The **returns-without-receipt correlation** is where the pattern becomes compelling. Two independent signals, same employee, same category — that's not noise.
- The CCTV timestamp index is referenced, not included. APEX doesn't store video; it points to it. Evidence-bundle contents respect client retention policies.

### Common client questions

**Q: "What are the civil-liberties implications of an AI flagging an employee?"**
A: Two things. First, the agent never takes action against an employee — it produces evidence for human reviewers who operate under HR and LP policies. Second, the signals are *statistical* (sigma anomalies on a specific category on a specific register), not profile-based. We do not use demographic features in the detection.

**Q: "What if the employee is innocent and the pattern is explained by something else — shift schedule, category mix, register assignment?"**
A: Loss Prevention reviews every case before action. The agent surfaces candidates; humans adjudicate. The whole point of the ESCALATION gate is that we never short-circuit the HR review process.

### The ROI point

**Shrink recovery in this category, for this client size, typically runs 0.3–0.7% of spirits revenue.** For a 3-store cluster the dollar number often exceeds the software + engagement cost for W2 by itself. This is the scenario that makes W2 self-funding.

### Next step

This is often the **scenario that unlocks the CFO.** Pair it with the W2 cold-chain scenario (Event 01) to frame W2 economics: shrink + cold chain pays for the agent fleet. If the client's CFO is in the room, lead with Event 07.

---

## Part 11 — Event 08 · 2:32 PM · Plastic Fragment in Muffin

### Event summary
Critical severity. A customer reports a plastic fragment in a sealed muffin at the service desk. The customer submits a photo. OCR extracts the lot code. The incident pattern detector correlates the lot against 4 other incidents in the last 14 days at two other stores. Pattern classification: **Tier 2 — systemic**, not isolated. Stakeholder Router dispatches to QA, Legal, and Comms in parallel.

### The hook
*"A plastic fragment in a sealed muffin. And a pattern emerging across three stores."*

### APEX cross-walk

| Concept | Binding |
|---|---|
| ORCH | ORCH-08 · Customer Incident Response |
| Primary agents | CXM-A04 OCR Lot Extractor · CXM-A05 Incident Pattern Detector · CXM-A06 Stakeholder Router |
| Primary schema | CXML |
| Key entities | CUSTOMER_INCIDENT · (cross-ref to SCML · LOT_TRACE) |
| HITL gate | **ESCALATION** — QA, Legal, Comms each own their response; the store does not |
| Wave | W3 (Platform) |
| Microsoft services | Customer mobile upload (L1) · Azure AI Foundry OCR (L5) · Lakehouse (L3) · Agent Service (L6) · Multi-channel dispatch (L7) |

### Talking points

- **OCR from customer photo is not the hard part.** The hard part is the **tier classification**: is this an isolated event (Tier 1, service recovery) or a systemic event (Tier 2, product recall)?
- **Three stores in 14 days** is what flips the tier. One store, three incidents — maybe handling damage. Three stores, three incidents — supply-side defect. The correlation is what triggers the escalation.
- **Parallel stakeholder dispatch** is what turns a 4-hour internal process into a 4-minute coordination. QA gets a ticket with lot trace attached. Legal gets a brief with jurisdictional flags. Comms gets a draft with brand-guardrail scoring.
- The store manager's role is **hand-off, not handling.** Marisol's job is to make the customer feel cared for at the service desk; the escalation owns everything else.

### Common client questions

**Q: "Tier-2 classifications can drive false escalations — what's the cost of getting it wrong?"**
A: False Tier-2 is expensive (unnecessary legal/comms cycles). False Tier-1 is catastrophic (a pattern gets missed). The classifier errs toward Tier-2 and Legal can downgrade it; we do not auto-downgrade. The asymmetry is the point.

**Q: "What does the customer experience of this look like?"**
A: The customer at the service desk sees Marisol acknowledge, apologize, and offer immediate recovery (refund + replacement). The customer doesn't see the escalation machinery — that's internal. The system makes it possible for Marisol to spend her time on the customer rather than on routing emails.

### The ROI point

**The ROI is brand and regulatory, not revenue.** The specific dollar case here is weak; the reputational case is the highest-magnitude scenario in the whole walkthrough. Clients who have lived through a product-safety incident internalize this scenario faster than any of the others.

### Next step

This is often the **closing scenario** in a C-suite presentation. It's the one that makes APEX feel like operational insurance, not just operational optimization. Use it to frame the move from W2 to W3 — **"W3 is where you stop firefighting Tier-2 incidents and start preventing them."**

---

## Part 12 — The Aggregate ROI Pitch

After walking the eight events, the summary sentence is:

> **Eight events. One manager. One hour of manager touch.**

That is the line to anchor the economics.

### The math in their language

| Dimension | Before APEX | With APEX |
|---|---|---|
| Cold-chain write-offs | Blanket destroys on excursion | Targeted: 71% saved on Event 01 — **$1,313 avoided** |
| DSD disputes | Filed days late with weak evidence; ~30% win rate | Filed at the dock with evidence; ~70% win rate |
| ESL / price-integrity | Caught by refund complaints hours later | Caught in 4 rings; **90-second bridge-tag fix** |
| Phantom OOS | Noticed by customer complaint | CV + POS fusion in minutes; pick-list ordered by route |
| Recall response | Hours to identify affected customers | **4 minutes to notification-ready** |
| BOPIS substitution | Escalates to manager 40–60% of the time | <5% manager touch; one-tap customer confirm |
| Shrink detection | Pattern-found-by-auditor weeks later | Sigma flagged same-day; evidence-package-ready |
| Tier-2 incident escalation | 4-hour internal coordination | 4-minute parallel dispatch |

Sum across a store's weekly event volume. Multiply by store count. The W1 + W2 ORCHs typically deliver **3–5× ROI on the engagement investment within 12 months** in the retail operator economics we've modeled. The client should run their own model with their own volumes — we give them the template.

### The line you want them to remember

*"The agent fleet handles the perimeter. The manager handles the decisions. The decisions that need a human are the only ones that reach her."*

---

## Part 13 — Common Objections and Prepared Responses

### 13.1 "This feels like a lot of AI. What if the models drift?"

**Response.** Every agent is backtested in isolation before orchestrator wiring (Core decomposition philosophy). Every ORCH declares its HITL gates explicitly (Core Part 8.3). Drift is monitored via Azure AI Foundry evals and the edition's eval harness. When confidence falls below threshold, the gate escalates — ACK_ONLY becomes HITL. The system degrades gracefully, it doesn't fail silently.

### 13.2 "What's the Deloitte Independence story here?"

**Response.** Core Part 6 is unambiguous. Client-tenant data planes. No Deloitte-side retention of client-identifiable data. Every schema and every agent runs on the client's Azure tenant. Deloitte's visibility ends at the engagement boundary; operational data stays in the client's OneLake. We formalized this further in Core v1.2 — only opaque account IDs, version numbers, and manifest hashes ever cross the boundary.

### 13.3 "How long until we see value?"

**Response.** W1 is designed to be self-funding in the 60–90 day horizon. The two W1 foundation plays (receiving reconciliation and price integrity) are the fastest to deploy because they bind to data streams the client already has. W2 (cold chain, phantom OOS extension, BOPIS) typically follows 90–120 days later. The wave model is explicit about exit criteria — we don't advance waves on schedule, we advance on measured outcomes.

### 13.4 "What if our IT team doesn't have the Fabric / Foundry skills?"

**Response.** That's scoping, not scope. The engagement includes Deloitte engineers who know Fabric, Foundry, and Agent Service. Knowledge transfer is part of the wave-exit criteria for W1 — by the time W1 closes, client-side engineers are operating the fleet, Deloitte is advisory. This is intentional; it's how we avoid creating a long-term dependency.

### 13.5 "Our data isn't clean enough for this."

**Response.** Candid answer: every client says this and every client is right. APEX's Bronze–Silver–Gold medallion architecture (Core Part 6) is explicitly designed for this. Bronze is ungoverned, Silver is where cleansing happens, Gold is where agents read. W1 includes data-conformance work scoped to the 2–3 ORCHs you're standing up; you don't have to clean the whole lake to start. Clean what you need, when you need it.

### 13.6 "What happens when an agent gets something wrong in front of a customer?"

**Response.** Two answers. First, the gate taxonomy means customer-visible actions (like SMS substitution confirmations) are always HITL — the customer is the final human. Agents don't act on customers autonomously. Second, every agent action is audit-logged with full context — what the agent saw, what it decided, what the confidence was. When something goes wrong, you can reconstruct exactly why. That's a lot better than what most retailers have today for human-driven decisions.

---

## Part 14 — Next-Meeting Checklist

After the Store 100 walkthrough conversation, the agreed next step should be one of three things. Leave the client with this page filled out.

### 14.1 Commitments to capture on the page

- [ ] **Which 2–3 ORCHs** will the client stand up in W1? (most common pair: ORCH-01 DSD + ORCH-02 Price Integrity)
- [ ] **Which store is the W1 pilot?** (identify real store; Store 100 is synthetic)
- [ ] **Which data streams** does the client already emit that feed these ORCHs? (receiving dock, POS, ESL gateway, etc.)
- [ ] **Who is the client-side sponsor?** (typically VP Operations or VP Store Systems)
- [ ] **Who is the client-side technical lead?** (typically a Fabric/Azure architect)
- [ ] **W1 success criteria** — measurable, time-boxed (e.g., "30% reduction in missed DSD claims over 90 days")
- [ ] **W1 timeline** — target start date, target exit date
- [ ] **What else needs to be true** for the client to commit to W1? (contracting, security review, legal, etc.)

### 14.2 Next-meeting artifacts to bring

- Wave 1 scope document (named ORCHs, named agents, named Microsoft services)
- Fleet-registry onboarding PR template
- Security / Independence review pack
- W1 timeline with milestones tied to wave-exit criteria

### 14.3 If the client asks for more time

- **"We need to think about it."** → Schedule a follow-up in 10 business days. Provide the HTML walkthrough and the solution overview as leave-behinds. Identify the specific open question blocking decision.
- **"We need our CFO in the room."** → Best possible outcome. Prepare an economics-first version of this walkthrough leading with Events 01, 07, and 12's aggregate ROI.
- **"We need our Legal team in the room."** → Prepare a compliance-first version leading with the Independence posture (Core Part 6), the event-envelope audit trail, and the HITL-gate taxonomy as the governance model.

---

**End of APEX · Store 100 Facilitator Guide — 2026-04-17**

*Reference implementation narrative: `apex-rc-store-100-shift-walkthrough.html`. Framework source: `apex-core-build-spec.md` · `apex-rc-build-spec-v2.md`. Companion artifacts: `docs/APEX-solution-overview.docx` · `docs/APEX-RC-agent-catalog.docx`.*
