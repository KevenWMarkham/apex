// Generate APEX-Store-100-facilitator-guide.docx
// Run: node build-facilitator-guide.cjs

const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat, HeadingLevel, BorderStyle,
  WidthType, ShadingType, PageBreak, PageNumber
} = require('docx');

const PAGE_WIDTH = 12240;
const PAGE_MARGIN = 1080;
const CONTENT_WIDTH = PAGE_WIDTH - 2 * PAGE_MARGIN;

const border = { style: BorderStyle.SINGLE, size: 4, color: "B8B8B8" };
const cellBorders = { top: border, bottom: border, left: border, right: border };
const headerShading = { fill: "1A2339", type: ShadingType.CLEAR, color: "auto" };
const cardLabelShading = { fill: "F4EFE3", type: ShadingType.CLEAR, color: "auto" };
const cellMargins = { top: 100, bottom: 100, left: 140, right: 140 };

// --- Helpers --------------------------------------------------------------

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 200 },
    children: [new TextRun(text)]
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 160 },
    children: [new TextRun(text)]
  });
}
function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 220, after: 120 },
    children: [new TextRun(text)]
  });
}
function p(text, opts = {}) {
  const children = Array.isArray(text) ? text : [new TextRun({ text, ...opts })];
  return new Paragraph({
    spacing: { after: 140, line: 300 },
    alignment: opts.align ?? AlignmentType.LEFT,
    children
  });
}
function bullet(text) {
  const children = Array.isArray(text) ? text : [new TextRun(text)];
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 80, line: 280 },
    children
  });
}
function checkbox(text) {
  const children = Array.isArray(text) ? text : [new TextRun(text)];
  return new Paragraph({
    spacing: { after: 80, line: 280 },
    indent: { left: 280 },
    children: [new TextRun({ text: "\u2610 ", size: 24 }), ...children]
  });
}
function numbered(text, level = 0) {
  const children = Array.isArray(text) ? text : [new TextRun(text)];
  return new Paragraph({
    numbering: { reference: "numbers", level },
    spacing: { after: 80, line: 280 },
    children
  });
}
function bold(text) { return new TextRun({ text, bold: true }); }
function italic(text) { return new TextRun({ text, italics: true }); }
function plain(text) { return new TextRun(text); }
function mono(text) { return new TextRun({ text, font: "Consolas", size: 20 }); }
function pageBreak() { return new Paragraph({ children: [new PageBreak()] }); }

// --- Table helpers --------------------------------------------------------

function makeTable(columnWidths, headerCells, rows) {
  const totalWidth = columnWidths.reduce((a, b) => a + b, 0);
  const headerRow = new TableRow({
    tableHeader: true,
    children: headerCells.map((text, i) => new TableCell({
      borders: cellBorders,
      width: { size: columnWidths[i], type: WidthType.DXA },
      shading: headerShading,
      margins: cellMargins,
      children: [new Paragraph({
        spacing: { after: 0, line: 260 },
        children: [new TextRun({ text, bold: true, color: "FFFFFF", size: 20 })]
      })]
    }))
  });
  const bodyRows = rows.map(row => new TableRow({
    children: row.map((cell, i) => new TableCell({
      borders: cellBorders,
      width: { size: columnWidths[i], type: WidthType.DXA },
      margins: cellMargins,
      children: (Array.isArray(cell) ? cell : [cell]).map(line =>
        typeof line === 'string'
          ? new Paragraph({
              spacing: { after: 0, line: 260 },
              children: [new TextRun({ text: line, size: 20 })]
            })
          : line
      )
    }))
  }));
  return new Table({
    width: { size: totalWidth, type: WidthType.DXA },
    columnWidths,
    rows: [headerRow, ...bodyRows]
  });
}

// --- Event data -----------------------------------------------------------

const severityColor = {
  Critical: "EF4444",
  High: "F5A623",
  Medium: "D4A244",
  Low: "64748B"
};

const EVENTS = [
  {
    part: 4, num: "01", time: "5:58 AM", severity: "Critical",
    title: "Reefer 14 Cold Chain",
    summary: "Between 02:15 and 06:27 the dairy endcap held at 48–52°F against a 41°F threshold. The compressor soft-start failed overnight. By the time Marisol swipes in, the case has been cooling back for twenty minutes and a disposition-ready brief is waiting on her phone.",
    hook: "\"Marisol's phone lit up before her badge did. Here's why that matters.\"",
    crossWalk: [
      ["ORCH", "ORCH-03 · Cold Chain & Disposition"],
      ["Primary agents", "SCM-A04 Cold Chain Telemetry Monitor · SCM-A05 Disposition Classifier · SCM-A06 Write-Off Pre-Approver"],
      ["Primary schema", "SCML"],
      ["Key entities", "COLD_CHAIN_TELEMETRY · TEMPERATURE_EXCURSION · STORE_INVENTORY_POSITION"],
      ["HITL gate", "HITL — Marisol confirms save/destroy and approves the $534 targeted write-off after visual inspection"],
      ["Wave", "W2 (Expansion)"],
      ["Microsoft services", "IoT Hub + Event Hubs (L2) · OneLake/ADX for telemetry (L3) · Logic Apps (L6) · Teams notification (L7)"]
    ],
    talkingPoints: [
      "The agent didn't wait for Marisol to arrive. The entire save/destroy classification was done on telemetry the client was already emitting — we just added the controls plane.",
      "Sub-category risk scoring is what distinguishes \"save the sealed cheese\" from \"destroy the ready-to-eat dairy.\" Three of your agents today would say \"destroy it all.\" APEX doesn't.",
      "The write-off is targeted. Not a blanket 412-unit loss. The claim is linked to a specific telemetry case file — the audit trail exists before the adjuster asks for it.",
      "Total manager touch: 90 seconds. That is the number the client should anchor on."
    ],
    qa: [
      ["Q: What if the CV/telemetry gets it wrong and we destroy product we could have saved?",
       "A: The disposition classifier reports a confidence band. Below threshold, the case flips from ACK_ONLY to HITL — the manager sees the split and can override. Above threshold, the manager sees the recommendation but still has the final approval tap. False-save errors are the regulated risk; false-destroy errors are the financial risk. We calibrate the threshold to the sub-category."],
      ["Q: Who owns the write-off policy decisions — us or you?",
       "A: The client. The agent stages the write-off; the approval routing lives in the client's finance system. Deloitte never holds the approval handle. This is explicit in Core Part 6 Independence posture."]
    ],
    roi: "Walmart's industry average write-off rate on cold-chain excursions hovers around 60–70% destroy (most operators can't distinguish risk by sub-category fast enough). Store 100's targeted write-off: 71% saved — $1,313 avoided on a $1,847 exposure. Multiply by the number of cold-chain excursions per store per year, multiply by store count — this single scenario often justifies W1 on its own.",
    nextStep: "This is the flagship W2 scenario. Use it to pin the client's W1 → W2 transition to cold-chain MVP. Frame: \"By the time you exit W1 you have the receiving and price-integrity foundation. W2 lights up cold chain.\""
  },
  {
    part: 5, num: "02", time: "7:20 AM", severity: "High",
    title: "DSD Short-Ship",
    summary: "RFID portal scan on the inbound dock clocks 44 cases against an invoice of 48. Before the beverage rep reaches the back office, the agent has built the dispute package and surfaced the vendor's 90-day pattern: three short-ships on this vendor in 90 days.",
    hook: "\"The beverage rep was still walking to the back office when the claim was already drafted. With evidence.\"",
    crossWalk: [
      ["ORCH", "ORCH-01 · DSD Reconciliation & Claims"],
      ["Primary agents", "SCM-A01 DSD Reconciliation · SCM-A02 Vendor Pattern Detector · SCM-A03 Claim Assembly"],
      ["Primary schema", "SCML"],
      ["Key entities", "ASN · STORE_RECEIVING_EVENT · RECEIVING_DISCREPANCY · DSD_INVOICE"],
      ["HITL gate", "HITL — Marisol signs disputed receipt; Accounts Payable receives a pre-built claim"],
      ["Wave", "W1 (Foundation)"],
      ["Microsoft services", "Event Hubs (L2) · Lakehouse (L3) · Logic Apps (L6) · Vendor portal webhook (L1)"]
    ],
    talkingPoints: [
      "The value isn't in catching this one short-ship. The value is in the vendor pattern — three of four short-ships in 90 days is no longer noise; it's a conversation with the category manager.",
      "Historically this reconciliation happens a week later, post-invoice, with weak evidence. Now it happens at the dock. Your claims win rate changes.",
      "The rep's iPad gets a \"sign disputed\" line pre-filled. The agent isn't telling the rep what to do — it's giving the manager a one-tap way to formalize what the scan already said.",
      "This is a W1 scenario — cheap, fast, concrete. Perfect for anchoring a W1 pitch."
    ],
    qa: [
      ["Q: Vendors won't agree to RFID portals at the door — we've tried.",
       "A: Agreed — portal adoption is engagement-specific. The APEX pattern works with whatever capture mechanism the client already has — barcode scan at pallet receipt, weight-on-scale, handheld audit. RFID is the ideal case; the pattern generalizes."],
      ["Q: What if we file a dispute and the vendor disputes the dispute?",
       "A: The dispute package carries timestamped evidence: portal logs, dock camera frame references, historical pattern. Contestable claims are materially fewer when evidence ships with the claim. We don't eliminate disputes; we shift the burden."]
    ],
    roi: "$142.56 claim, filed with strong evidence before the truck left the lot. The per-claim dollar is small; the compound effect is large. Stores this size see 40–80 DSD discrepancies per week. Historical win rate on disputed claims without evidence: ~30%. With evidence: ~70%. Apply the delta across 52 weeks × store count.",
    nextStep: "This is a W1 anchor. Put it on the wave-commitment worksheet as one of the first two ORCHs Store 100 lights up in the first 90 days."
  },
  {
    part: 6, num: "03", time: "8:36 AM", severity: "High",
    title: "127 Stale ESL Tags",
    summary: "Overnight ESL push silently failed on the pet aisle gateway. Shelf shows regular; POS rings promo. By the fourth customer transaction, the agent catches the gap, freezes the loss, stages customer refunds, and drafts the ESL bridge tag sheet.",
    hook: "\"One hundred twenty-seven tags went stale overnight. Four customers rang through at the wrong price before the fleet caught it. The fifth didn't.\"",
    crossWalk: [
      ["ORCH", "ORCH-02 · Pricing Integrity"],
      ["Primary agents", "MER-A04 ESL Gateway Monitor · MER-A05 POS Mismatch Detector"],
      ["Primary schema", "MERML"],
      ["Key entities", "PRICE_RECORD · PRICE_TAG_STATUS · PROMOTION_ACTIVATION · POS_VOID"],
      ["HITL gate", "ACK_ONLY on auto-refund → HITL on refunds exceeding threshold"],
      ["Wave", "W1 (Foundation)"],
      ["Microsoft services", "ESL gateway API (L1) · Event Hubs (L2) · Lakehouse (L3) · Logic Apps (L6) · SMS / receipt printer (L7)"]
    ],
    talkingPoints: [
      "Pricing integrity failures are silent by default. The ESL gateway doesn't tell you when it drops a push; you find out from the customer refund line.",
      "The bridge tag mechanism turns a 2-hour problem into a 90-second problem. Paper tags get printed at the service desk; an associate walks the aisle; the gateway gets restarted in parallel.",
      "Customer refunds are staged automatically for transactions that already happened — the customer doesn't have to come back.",
      "This is a W1 scenario because ESL monitoring is the simplest orchestration to stand up: one gateway API, one POS event stream, one MERML schema. No CV, no lot tracing, no regulatory feeds."
    ],
    qa: [
      ["Q: What if we don't have ESL today — only printed tags?",
       "A: The price-integrity ORCH still applies; the gateway-monitor agent doesn't. The POS-mismatch detection works regardless of the display mechanism (it's a comparison between POS ring and the authoritative price record). ESL is an acceleration lever, not a prerequisite."],
      ["Q: How does the agent know to stage refunds automatically — is that not a legal/compliance exposure?",
       "A: The threshold is policy-driven. Below X dollars per transaction, auto-refund and ACK_ONLY to the manager. Above X, HITL gate. Policy is client-owned, written into the ORCH configuration. Agents execute policy; they don't define it."]
    ],
    roi: "4 rings at wrong price before catch, 127 SKUs corrected in 14 minutes, loss frozen at ~$18. Without APEX, this typically runs 2+ hours and $200–400 in loss per incident. Frequency is 1–3 incidents per store per week on average ESL fleets. Compound across the fleet.",
    nextStep: "W1 anchor. Pair with Event 02 (DSD) to argue the W1 \"reconciliation pair\" — receiving and pricing are the two foundations. Everything else builds on knowing what's in the store and what it costs."
  },
  {
    part: 7, num: "04", time: "10:15 AM", severity: "Medium",
    title: "Empty Shelves With Backroom Stock",
    summary: "Eighteen OSA (on-shelf availability) events cluster across two aisles. Perpetual inventory says \"in stock\" — but CV sees empty facings and POS velocity has flatlined for 40 minutes. All 18 items have backroom stock.",
    hook: "\"Eighteen empty shelves. All of them had backroom stock. The perpetual said everything was fine.\"",
    crossWalk: [
      ["ORCH", "ORCH-04 · Labor & Fulfillment"],
      ["Primary agents", "MER-A06 Phantom OOS Detector · MER-A07 Pick List Optimizer · MER-A08 Associate Router"],
      ["Primary schema", "MERML"],
      ["Key entities", "STORE_INVENTORY_POSITION · OSA_EVENT"],
      ["HITL gate", "ZERO_TOUCH on detection + pick-list generation; ACK_ONLY to associate via handheld"],
      ["Wave", "W1 (Foundation)"],
      ["Microsoft services", "Shelf CV (L1 edge) · Event Hubs (L2) · Lakehouse (L3) · Agent Service (L6) · Associate mobile (L7)"]
    ],
    talkingPoints: [
      "Phantom OOS is the canonical retail problem. Perpetual says stock exists, shelf is empty, customer walks. The CV + POS + perpetual fusion is what detects it.",
      "The pick list optimizer doesn't just list 18 items — it orders them by walking route. That is 6–12 minutes saved per replenishment cycle.",
      "The associate router knows who is free, who is in zone, and whose radio is active. Tasks get dispatched to the right associate, not broadcast.",
      "This is a ZERO_TOUCH orchestration — the manager doesn't see any of this unless a task ages out past SLO. The human only enters on exception."
    ],
    qa: [
      ["Q: We don't have shelf CV everywhere. Does this still work?",
       "A: Phantom OOS detection has a graceful degradation path. Without CV, we rely on POS velocity + perpetual inventory + shelf-capture handhelds. Detection rate is lower but the ORCH still fires. CV is the accelerator; it's not mandatory."],
      ["Q: Associates are going to push back on being routed by an algorithm.",
       "A: Agreed — and this is a change-management conversation, not a technical one. The system shows the associate what, not when. Prioritization is the associate's call; the system provides the ordered list. We've seen associate adoption accelerate once they realize the system saves them walking miles per shift."]
    ],
    roi: "Phantom OOS costs retailers 3–8% of category sales on affected SKUs. For Store 100's size, this single 18-event cluster represents ~$440 in at-risk sales. Detection latency dropped from \"customer complaint\" (hours) to CV signal (minutes). Frequency: 10–25 phantom events per store per day.",
    nextStep: "W1 capstone scenario. The client feels the labor benefit viscerally — associates stop walking blind routes. Put this on the wave-commitment worksheet as the W1 scenario that shows operational ROI most clearly."
  },
  {
    part: 8, num: "05", time: "11:43 AM", severity: "Critical",
    title: "Infant Formula Recall",
    summary: "FDA posts a Class II recall at 11:43. Four minutes later the agent has resolved the affected lot upstream to the supplier, downstream to 9 transactions in the last 21 days, and identified the customers (where loyalty data permits). Marisol sees a customer notification queue ready to dispatch.",
    hook: "\"The recall posted at 11:43. By 11:47 she knew exactly who bought it.\"",
    crossWalk: [
      ["ORCH", "ORCH-05 · Recall Impact"],
      ["Primary agents", "SCM-A07 FDA Feed Listener · SCM-A08 Lot Trace Resolver · (MER-A12 Markdown Cadence Agent for in-aisle pull)"],
      ["Primary schema", "SCML (plus CXML for customer resolution)"],
      ["Key entities", "RECALL_NOTICE · LOT_TRACE · LOYALTY_STATE · CUSTOMER_INCIDENT"],
      ["HITL gate", "HITL — recall coordinator (not Marisol) confirms customer-notification scope before dispatch"],
      ["Wave", "W2 (Expansion)"],
      ["Microsoft services", "FDA public feed (L1 external) · Event Hubs (L2) · Lakehouse (L3) · Agent Service (L6) · Teams + SMS dispatch (L7)"]
    ],
    talkingPoints: [
      "Four minutes from FDA post to notification-ready. The previous process took hours — sometimes days — to resolve which stores, which customers, which lots.",
      "Lot trace is bidirectional: upstream to identify which vendor/batch/supplier is implicated; downstream to identify which customers purchased the affected lot.",
      "The agent does not dispatch notifications autonomously. Recall communications are an HITL gate at the recall coordinator — this is both a legal requirement and a brand-trust requirement.",
      "This scenario binds three schemas: SCML (recall + lot trace), CXML (customer loyalty state), MERML (in-aisle product pull). It's a natural demo of the cross-schema event envelope."
    ],
    qa: [
      ["Q: Customer notification on a recall — how does this stay consent-compliant?",
       "A: The agent respects the same consent flags the marketing stack honors (MKTL · SEGMENT_MEMBERSHIP suppression rules). A customer who has opted out of non-transactional contact doesn't receive a marketing nudge — but they do receive a safety notification per policy. The distinction is encoded in the ORCH configuration, not the agent logic."],
      ["Q: What's the false-match rate on downstream customer identification?",
       "A: Lot-to-transaction match is high-confidence (lot codes are explicit on receiving). Transaction-to-customer match depends on loyalty penetration. For Store 100-style formats, 40–60% of transactions have customer ID; the remainder get in-store signage and POS-flagged notifications on next visit."]
    ],
    roi: "The ROI is not monetary — it's brand-and-regulatory. A four-minute notification-ready window transforms recall posture from \"we'll get back to you\" to \"here is our response playbook, executed.\" On Class I recalls that difference is material to regulatory relationships and can materially affect brand trust.",
    nextStep: "This is a W2 scenario that the C-suite cares about disproportionately. Use it to pull the CFO or General Counsel into the conversation. It's the event that proves APEX is not just about stockouts."
  },
  {
    part: 9, num: "06", time: "12:32 PM", severity: "Low",
    title: "BOPIS Spinach Substitution",
    summary: "Jennifer (online customer) ordered for 1:00 PM pickup. The associate picking for her hits an OOS on organic spinach. Before the associate even asks, the agent has ranked three substitution candidates, one-tap SMS'd Jennifer, and is tracking the SLA clock.",
    hook: "\"Jennifer's spinach was out. Marisol never heard about it.\"",
    crossWalk: [
      ["ORCH", "ORCH-06 · Fulfillment Exception Handling"],
      ["Primary agents", "CXM-A01 Pick Exception Handler · CXM-A02 Substitution Ranker · CXM-A03 Customer Confirm Gateway"],
      ["Primary schema", "CXML"],
      ["Key entities", "FULFILLMENT_ORDER · PICK_EXCEPTION · SUBSTITUTION_EVENT"],
      ["HITL gate", "HITL — the customer is the human. Marisol never sees this unless the customer doesn't respond."],
      ["Wave", "W2 (Expansion)"],
      ["Microsoft services", "BOPIS order source (L1) · Event Hubs (L2) · Lakehouse (L3) · Agent Service (L6) · SMS gateway (L7)"]
    ],
    talkingPoints: [
      "Marisol doesn't see this event. That is the point. Low-severity customer-facing exceptions never touch the manager.",
      "The 14-month substitution history is what makes the ranker credible — it's not \"closest-SKU fallback.\" It's \"this customer has accepted 'baby spinach' as a substitute for 'organic spinach' 7 of 9 times.\"",
      "SMS aging means the clock is watched. If Jennifer doesn't tap within 4 minutes, the order state transitions; the agent doesn't stall the pickup.",
      "This is the shopper-trust scenario. Customers cite substitution handling as a top-3 BOPIS satisfaction driver. APEX turns it from a manager problem into a ranked shortlist with a one-tap confirm."
    ],
    qa: [
      ["Q: What if the customer doesn't respond at all — do we substitute or refund?",
       "A: Policy-driven. Most clients configure: under 4 minutes no-response → default-substitute (if confidence is high); over 4 minutes → default-refund. The ORCH respects whichever policy the client configures."],
      ["Q: How does this handle multi-item exceptions — three OOS in one order?",
       "A: The ranker processes them as a batch and sends a single consolidated SMS (\"We have 3 substitutions to confirm\"). The customer taps once per item; the whole batch is tracked under the same SLA clock."]
    ],
    roi: "Customer touch without manager touch. The metric the client cares about is: what fraction of BOPIS exceptions are resolved without manager intervention? Store 100's target is >95%. Without APEX, 40–60% of exceptions escalate to the manager at some point.",
    nextStep: "Pair this with Event 04 (Phantom OOS) to pitch the W2 customer-experience bundle. The argument: once you've nailed the in-store inventory accuracy (W1), the W2 wave lets you extend that accuracy to the omnichannel customer promise."
  },
  {
    part: 10, num: "07", time: "1:47 PM", severity: "High",
    title: "4.2× Void Rate on Spirits",
    summary: "The void pattern detector flags Register 7's void rate on the spirits category at 4.2× the 90-day sigma baseline. One employee. Pattern is corroborated by a returns-without-receipt cluster on the same category, same shift, same employee. The agent builds the evidence package and routes to Loss Prevention.",
    hook: "\"Four-point-two times the void rate. Only on spirits. Only on this register. Only on this shift.\"",
    crossWalk: [
      ["ORCH", "ORCH-07 · Shrink & Loss Prevention"],
      ["Primary agents", "MER-A09 Void Pattern Detector · MER-A10 Variance Correlator · MER-A11 Evidence Package Builder"],
      ["Primary schema", "MERML"],
      ["Key entities", "POS_VOID · SHRINK_EVENT · CYCLE_COUNT_VARIANCE"],
      ["HITL gate", "ESCALATION — Loss Prevention takes ownership; the agent never acts on the employee directly"],
      ["Wave", "W2 (Expansion)"],
      ["Microsoft services", "POS stream (L1) · Event Hubs (L2) · Lakehouse (L3) · CCTV index (L1) · Agent Service (L6)"]
    ],
    talkingPoints: [
      "ESCALATION is the critical gate here. The agent does not fire anyone. The agent does not even flag the employee to Marisol. It routes the evidence package to Loss Prevention per client policy.",
      "The sigma anomaly + category isolator + employee-register correlator is the decomposition that makes this specific, not generic. \"Void rate is high\" is not actionable. \"Void rate is 4.2σ above baseline, on spirits, on register 7, on shift 2\" is actionable.",
      "The returns-without-receipt correlation is where the pattern becomes compelling. Two independent signals, same employee, same category — that's not noise.",
      "The CCTV timestamp index is referenced, not included. APEX doesn't store video; it points to it. Evidence-bundle contents respect client retention policies."
    ],
    qa: [
      ["Q: What are the civil-liberties implications of an AI flagging an employee?",
       "A: Two things. First, the agent never takes action against an employee — it produces evidence for human reviewers who operate under HR and LP policies. Second, the signals are statistical (sigma anomalies on a specific category on a specific register), not profile-based. We do not use demographic features in the detection."],
      ["Q: What if the employee is innocent and the pattern is explained by something else — shift schedule, category mix, register assignment?",
       "A: Loss Prevention reviews every case before action. The agent surfaces candidates; humans adjudicate. The whole point of the ESCALATION gate is that we never short-circuit the HR review process."]
    ],
    roi: "Shrink recovery in this category, for this client size, typically runs 0.3–0.7% of spirits revenue. For a 3-store cluster the dollar number often exceeds the software + engagement cost for W2 by itself. This is the scenario that makes W2 self-funding.",
    nextStep: "This is often the scenario that unlocks the CFO. Pair it with the W2 cold-chain scenario (Event 01) to frame W2 economics: shrink + cold chain pays for the agent fleet. If the client's CFO is in the room, lead with Event 07."
  },
  {
    part: 11, num: "08", time: "2:32 PM", severity: "Critical",
    title: "Plastic Fragment in Muffin",
    summary: "A customer reports a plastic fragment in a sealed muffin at the service desk. The customer submits a photo. OCR extracts the lot code. The incident pattern detector correlates the lot against 4 other incidents in the last 14 days at two other stores. Pattern classification: Tier 2 — systemic, not isolated. Stakeholder Router dispatches to QA, Legal, and Comms in parallel.",
    hook: "\"A plastic fragment in a sealed muffin. And a pattern emerging across three stores.\"",
    crossWalk: [
      ["ORCH", "ORCH-08 · Customer Incident Response"],
      ["Primary agents", "CXM-A04 OCR Lot Extractor · CXM-A05 Incident Pattern Detector · CXM-A06 Stakeholder Router"],
      ["Primary schema", "CXML"],
      ["Key entities", "CUSTOMER_INCIDENT · (cross-ref to SCML · LOT_TRACE)"],
      ["HITL gate", "ESCALATION — QA, Legal, Comms each own their response; the store does not"],
      ["Wave", "W3 (Platform)"],
      ["Microsoft services", "Customer mobile upload (L1) · Azure AI Foundry OCR (L5) · Lakehouse (L3) · Agent Service (L6) · Multi-channel dispatch (L7)"]
    ],
    talkingPoints: [
      "OCR from customer photo is not the hard part. The hard part is the tier classification: is this an isolated event (Tier 1, service recovery) or a systemic event (Tier 2, product recall)?",
      "Three stores in 14 days is what flips the tier. One store, three incidents — maybe handling damage. Three stores, three incidents — supply-side defect. The correlation is what triggers the escalation.",
      "Parallel stakeholder dispatch is what turns a 4-hour internal process into a 4-minute coordination. QA gets a ticket with lot trace attached. Legal gets a brief with jurisdictional flags. Comms gets a draft with brand-guardrail scoring.",
      "The store manager's role is hand-off, not handling. Marisol's job is to make the customer feel cared for at the service desk; the escalation owns everything else."
    ],
    qa: [
      ["Q: Tier-2 classifications can drive false escalations — what's the cost of getting it wrong?",
       "A: False Tier-2 is expensive (unnecessary legal/comms cycles). False Tier-1 is catastrophic (a pattern gets missed). The classifier errs toward Tier-2 and Legal can downgrade it; we do not auto-downgrade. The asymmetry is the point."],
      ["Q: What does the customer experience of this look like?",
       "A: The customer at the service desk sees Marisol acknowledge, apologize, and offer immediate recovery (refund + replacement). The customer doesn't see the escalation machinery — that's internal. The system makes it possible for Marisol to spend her time on the customer rather than on routing emails."]
    ],
    roi: "The ROI is brand and regulatory, not revenue. The specific dollar case here is weak; the reputational case is the highest-magnitude scenario in the whole walkthrough. Clients who have lived through a product-safety incident internalize this scenario faster than any of the others.",
    nextStep: "This is often the closing scenario in a C-suite presentation. It's the one that makes APEX feel like operational insurance, not just operational optimization. Use it to frame the move from W2 to W3 — \"W3 is where you stop firefighting Tier-2 incidents and start preventing them.\""
  }
];

// --- Event sheet renderer -------------------------------------------------

function eventTitleRow(e) {
  const sev = severityColor[e.severity] || "64748B";
  return new TableRow({
    tableHeader: true,
    children: [new TableCell({
      borders: cellBorders,
      columnSpan: 2,
      width: { size: CONTENT_WIDTH, type: WidthType.DXA },
      shading: headerShading,
      margins: cellMargins,
      children: [new Paragraph({
        spacing: { after: 0, line: 260 },
        children: [
          new TextRun({ text: `${e.num}  `, bold: true, color: "F5A623", size: 22, font: "Consolas" }),
          new TextRun({ text: `${e.time}  ·  `, color: "FFFFFF", size: 22 }),
          new TextRun({ text: e.severity.toUpperCase(), bold: true, color: sev, size: 18, font: "Consolas" }),
          new TextRun({ text: `  ·  ${e.title}`, bold: true, color: "FFFFFF", size: 24 })
        ]
      })]
    })]
  });
}

function labeledRow(label, value) {
  const labelWidth = 2400;
  const valueWidth = CONTENT_WIDTH - labelWidth;
  return new TableRow({
    cantSplit: true,
    children: [
      new TableCell({
        borders: cellBorders,
        width: { size: labelWidth, type: WidthType.DXA },
        shading: cardLabelShading,
        margins: cellMargins,
        children: [new Paragraph({
          spacing: { after: 0, line: 260 },
          children: [new TextRun({
            text: label.toUpperCase(),
            bold: true, size: 16, color: "56627C", font: "Consolas"
          })]
        })]
      }),
      new TableCell({
        borders: cellBorders,
        width: { size: valueWidth, type: WidthType.DXA },
        margins: cellMargins,
        children: Array.isArray(value) ? value : [new Paragraph({
          spacing: { after: 0, line: 260 },
          children: [new TextRun({ text: value, size: 20 })]
        })]
      })
    ]
  });
}

function crossWalkCell(rows) {
  // rows is [[label, value], ...]
  return rows.map(([label, value]) => new Paragraph({
    spacing: { after: 60, line: 260 },
    children: [
      new TextRun({ text: `${label}: `, bold: true, size: 18, color: "2F3F5F", font: "Consolas" }),
      new TextRun({ text: value, size: 18 })
    ]
  }));
}

function bulletedCell(items) {
  return items.map(item => new Paragraph({
    spacing: { after: 60, line: 260 },
    indent: { left: 180, hanging: 180 },
    children: [
      new TextRun({ text: "\u2022 ", size: 20, color: "2DD4BF" }),
      new TextRun({ text: item, size: 20 })
    ]
  }));
}

function qaCell(qaPairs) {
  const paragraphs = [];
  qaPairs.forEach(([q, a], idx) => {
    paragraphs.push(new Paragraph({
      spacing: { after: 30, line: 260 },
      children: [new TextRun({ text: q, italics: true, size: 20, color: "8F5A0C" })]
    }));
    paragraphs.push(new Paragraph({
      spacing: { after: idx < qaPairs.length - 1 ? 120 : 0, line: 260 },
      children: [new TextRun({ text: a, size: 20 })]
    }));
  });
  return paragraphs;
}

function eventSheet(e) {
  const rows = [
    eventTitleRow(e),
    labeledRow("Event summary", e.summary),
    labeledRow("The hook", [new Paragraph({
      spacing: { after: 0, line: 260 },
      children: [new TextRun({ text: e.hook, italics: true, size: 20, color: "0D7D70" })]
    })]),
    labeledRow("APEX cross-walk", crossWalkCell(e.crossWalk)),
    labeledRow("Talking points", bulletedCell(e.talkingPoints)),
    labeledRow("Q&A prep", qaCell(e.qa)),
    labeledRow("ROI point", e.roi),
    labeledRow("Next step", e.nextStep)
  ];
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [2400, CONTENT_WIDTH - 2400],
    rows
  });
}

// --- Document assembly ----------------------------------------------------

const children = [];

// Title page
children.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 3600, after: 200 },
    children: [new TextRun({ text: "APEX · Store 100", bold: true, size: 72, color: "1A2339" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [new TextRun({ text: "Facilitator Guide", size: 48, color: "2F3F5F" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 720 },
    children: [new TextRun({ text: "How Account Teams use the Store 100 walkthrough in client conversations", italics: true, size: 24, color: "8A97B2" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: [new TextRun({ text: "Companion to: apex-rc-store-100-shift-walkthrough.html", size: 22 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: [new TextRun({ text: "Current as of APEX Core v1.2", size: 22 })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: [new TextRun({ text: "2026-04-17", size: 22 })]
  }),
  pageBreak()
);

// Part 0
children.push(
  h1("Part 0 — Compliance & Language Constraints (Inherited)"),
  p("This guide inherits Part 0 of APEX Core unchanged. All Deloitte–Microsoft terminology rules apply. The HTML walkthrough and this guide use synthetic reference-implementation identifiers — Store 100, Marisol Reyes, DFW Metroplex, Apr 14 2026, the eight event timestamps. These are scenario data, not client data."),
  h2("Scenario-vs-engagement boundary"),
  p("This guide is reusable across engagements. Real client-engagement specifics — actual store numbers, real manager names, client-identifiable ROI figures, named vendors, named regulators — belong in engagement-specific deliverables, not in this document. When an Account Team uses this guide with a live client, the facilitator maps Store 100's synthetic scenarios to the client's actual operational equivalents verbally; the document itself stays synthetic."),
  p("HITL gate types follow Core Part 8.3 unchanged: HITL (decision required), ACK_ONLY (visibility only), ZERO_TOUCH (fully autonomous), ESCALATION (deferred to higher authority). Wave references (W1–W4) follow Core Part 12.")
);

// Part 1
children.push(
  h1("Part 1 — How to Use This Guide"),
  p("The HTML walkthrough tells the story. This guide tells you how to use the story in three specific meeting settings."),
  h2("1.1 Discovery meeting (first client conversation)"),
  bullet([bold("Goal: "), plain("Establish that APEX has a concrete, credible answer to \"what does agentic actually look like in a retail store.\"")]),
  bullet([bold("How to use: "), plain("Walk 3 of the 8 events. Pick ones that match the pain the client has already named (stockouts → Event 04; recalls → Event 05; shrink → Event 07).")]),
  bullet([bold("Time budget: "), plain("25–30 minutes.")]),
  bullet([bold("Leave-behind: "), plain("The HTML walkthrough and the solution overview.")]),
  h2("1.2 Architecture review (technical audience, CIO/CTO or their delegates)"),
  bullet([bold("Goal: "), plain("Show that every scenario binds to concrete Microsoft-native infrastructure, a specific canonical schema, and a specific orchestration. No hand-waving.")]),
  bullet([bold("How to use: "), plain("Walk all 8 events, but lean on the APEX Cross-Walk field in each event sheet. Name the ORCH, the agents by catalog ID, the schema entities, the HITL gate type. Use the RC Agent Catalog as a companion — hand it to them.")]),
  bullet([bold("Time budget: "), plain("60–75 minutes.")]),
  bullet([bold("Leave-behind: "), plain("Overview + catalog + HTML walkthrough + solution stack (when available).")]),
  h2("1.3 CMM assessment (positioning for wave commitment)"),
  bullet([bold("Goal: "), plain("Map each scenario to a wave, get the client to pick their starting wave.")]),
  bullet([bold("How to use: "), plain("Lead with the aggregate ROI pitch (Part 12). Then walk 4 events from W1 (the ones they'll see in their first 90 days). Then name the wave-exit criteria. Close with the next-meeting checklist (Part 14).")]),
  bullet([bold("Time budget: "), plain("45 minutes.")]),
  bullet([bold("Leave-behind: "), plain("This guide's Part 14 checklist — signed.")])
);

// Part 2
children.push(
  h1("Part 2 — Store 100 at a Glance"),
  p("The HTML walkthrough compresses an imagined 9-hour shift into one document. Eight exception events between 5:58 AM and 2:32 PM. One store manager on duty — Marisol Reyes. One agentic fleet working the perimeter."),
  p([bold("The headline: "), plain("eight events, one hour of manager touch.")]),
  p("Every event follows the same APEX shape:"),
  numbered([bold("Schema lights up"), plain(" — canonical entities in the edition's Silver/Gold layers record the event.")]),
  numbered([bold("Agent responds autonomously"), plain(" — the fleet classifies the situation, pulls history, pre-stages the decision.")]),
  numbered([bold("Human is engaged at the gate"), plain(" — Marisol gets a decision-ready brief or an acknowledgment, not a raw alert.")]),
  numbered([bold("Outcome is recorded"), plain(" — audit trail complete, metrics captured, state updated.")]),
  h2("2.1 The 8-event grid"),
  makeTable(
    [600, 1400, 1400, 3400, 3280],
    ["#", "Time", "Severity", "Event", "ORCH"],
    [
      ["01", "5:58 AM", "Critical", "Reefer 14 cold-chain excursion", "ORCH-03 Cold Chain & Disposition"],
      ["02", "7:20 AM", "High", "DSD short-ship (beverage rep)", "ORCH-01 DSD Reconciliation & Claims"],
      ["03", "8:36 AM", "High", "127 stale ESL tags on pet aisle", "ORCH-02 Pricing Integrity"],
      ["04", "10:15 AM", "Medium", "18 empty shelves, backroom stock present", "ORCH-04 Labor & Fulfillment"],
      ["05", "11:43 AM", "Critical", "Infant formula recall", "ORCH-05 Recall Impact"],
      ["06", "12:32 PM", "Low", "BOPIS spinach out, substitution needed", "ORCH-06 Fulfillment Exception"],
      ["07", "1:47 PM", "High", "4.2× void rate on spirits register", "ORCH-07 Shrink & Loss Prevention"],
      ["08", "2:32 PM", "Critical", "Plastic fragment in sealed muffin", "ORCH-08 Customer Incident Response"]
    ]
  ),
  p("Each event binds to a different orchestration. In one shift, Store 100 exercises 8 of the 12 RC orchestrations — which is why this walkthrough carries disproportionate weight in a client conversation. It is not a demo of one agent; it is a demo of the orchestrated fleet.")
);

// Part 3
children.push(
  h1("Part 3 — Reader's Kit"),
  p("Bring these to every meeting where you use the Store 100 walkthrough:"),
  makeTable(
    [3200, 4000, 2880],
    ["Artifact", "Path", "When to reach for it"],
    [
      ["Store 100 HTML walkthrough", "…/Walmart/02_projects/apex-rc-store-100-shift-walkthrough.html", "Primary narrative — open on the screen."],
      ["APEX Solution Overview (Word)", "docs/guides/APEX-solution-overview.docx", "When the client asks \"what is APEX?\" — point to Part 1–4."],
      ["RC Agent Catalog (Word)", "docs/reference/APEX-RC-agent-catalog.docx", "When the client asks about a specific agent — look up the card live."],
      ["This facilitator guide", "docs/guides/APEX-Store-100-facilitator-guide.docx", "Your own side-monitor. Not shown to the client."],
      ["RC build spec", "docs/build-specs/apex-rc-build-spec-v2.md", "If pushed on a definition or convention — the source of truth."]
    ]
  ),
  p([bold("One rule: "), plain("never lead with the catalog or the build spec. Those are reference; the HTML is the story. Pull the reference forward only when the client asks a question the story doesn't answer.")])
);

// Parts 4-11 - Event sheets
EVENTS.forEach(e => {
  children.push(h1(`Part ${e.part} — Event ${e.num} · ${e.time} · ${e.title}`));
  children.push(eventSheet(e));
  children.push(new Paragraph({ spacing: { after: 160 }, children: [] }));
});

// Part 12
children.push(
  h1("Part 12 — The Aggregate ROI Pitch"),
  p("After walking the eight events, the summary sentence is:"),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 200 },
    children: [new TextRun({ text: "Eight events. One manager. One hour of manager touch.", bold: true, size: 32, color: "0D7D70", italics: true })]
  }),
  p("That is the line to anchor the economics."),
  h2("The math in their language"),
  makeTable(
    [2400, 3800, 3880],
    ["Dimension", "Before APEX", "With APEX"],
    [
      ["Cold-chain write-offs", "Blanket destroys on excursion", "Targeted: 71% saved on Event 01 — $1,313 avoided"],
      ["DSD disputes", "Filed days late with weak evidence; ~30% win rate", "Filed at the dock with evidence; ~70% win rate"],
      ["ESL / price integrity", "Caught by refund complaints hours later", "Caught in 4 rings; 90-second bridge-tag fix"],
      ["Phantom OOS", "Noticed by customer complaint", "CV + POS fusion in minutes; pick-list ordered by route"],
      ["Recall response", "Hours to identify affected customers", "4 minutes to notification-ready"],
      ["BOPIS substitution", "Escalates to manager 40–60% of the time", "<5% manager touch; one-tap customer confirm"],
      ["Shrink detection", "Pattern-found-by-auditor weeks later", "Sigma flagged same-day; evidence-package-ready"],
      ["Tier-2 incident escalation", "4-hour internal coordination", "4-minute parallel dispatch"]
    ]
  ),
  p("Sum across a store's weekly event volume. Multiply by store count. The W1 + W2 ORCHs typically deliver 3–5× ROI on the engagement investment within 12 months in the retail operator economics we've modeled. The client should run their own model with their own volumes — we give them the template."),
  h2("The line you want them to remember"),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 200 },
    indent: { left: 560, right: 560 },
    children: [new TextRun({ text: "\"The agent fleet handles the perimeter. The manager handles the decisions. The decisions that need a human are the only ones that reach her.\"", italics: true, size: 22, color: "2F3F5F" })]
  })
);

// Part 13
const objections = [
  ["13.1  \"This feels like a lot of AI. What if the models drift?\"",
   "Every agent is backtested in isolation before orchestrator wiring (Core decomposition philosophy). Every ORCH declares its HITL gates explicitly (Core Part 8.3). Drift is monitored via Azure AI Foundry evals and the edition's eval harness. When confidence falls below threshold, the gate escalates — ACK_ONLY becomes HITL. The system degrades gracefully, it doesn't fail silently."],
  ["13.2  \"What's the Deloitte Independence story here?\"",
   "Core Part 6 is unambiguous. Client-tenant data planes. No Deloitte-side retention of client-identifiable data. Every schema and every agent runs on the client's Azure tenant. Deloitte's visibility ends at the engagement boundary; operational data stays in the client's OneLake. We formalized this further in Core v1.2 — only opaque account IDs, version numbers, and manifest hashes ever cross the boundary."],
  ["13.3  \"How long until we see value?\"",
   "W1 is designed to be self-funding in the 60–90 day horizon. The two W1 foundation plays (receiving reconciliation and price integrity) are the fastest to deploy because they bind to data streams the client already has. W2 (cold chain, phantom OOS extension, BOPIS) typically follows 90–120 days later. The wave model is explicit about exit criteria — we don't advance waves on schedule, we advance on measured outcomes."],
  ["13.4  \"What if our IT team doesn't have the Fabric / Foundry skills?\"",
   "That's scoping, not scope. The engagement includes Deloitte engineers who know Fabric, Foundry, and Agent Service. Knowledge transfer is part of the wave-exit criteria for W1 — by the time W1 closes, client-side engineers are operating the fleet, Deloitte is advisory. This is intentional; it's how we avoid creating a long-term dependency."],
  ["13.5  \"Our data isn't clean enough for this.\"",
   "Candid answer: every client says this and every client is right. APEX's Bronze–Silver–Gold medallion architecture (Core Part 6) is explicitly designed for this. Bronze is ungoverned, Silver is where cleansing happens, Gold is where agents read. W1 includes data-conformance work scoped to the 2–3 ORCHs you're standing up; you don't have to clean the whole lake to start. Clean what you need, when you need it."],
  ["13.6  \"What happens when an agent gets something wrong in front of a customer?\"",
   "Two answers. First, the gate taxonomy means customer-visible actions (like SMS substitution confirmations) are always HITL — the customer is the final human. Agents don't act on customers autonomously. Second, every agent action is audit-logged with full context — what the agent saw, what it decided, what the confidence was. When something goes wrong, you can reconstruct exactly why. That's a lot better than what most retailers have today for human-driven decisions."]
];

children.push(h1("Part 13 — Common Objections and Prepared Responses"));
objections.forEach(([q, a]) => {
  children.push(h2(q));
  children.push(p([bold("Response. "), plain(a)]));
});

// Part 14
children.push(
  h1("Part 14 — Next-Meeting Checklist"),
  p("After the Store 100 walkthrough conversation, the agreed next step should be one of three things. Leave the client with this page filled out."),
  h2("14.1 Commitments to capture on the page"),
  checkbox([bold("Which 2–3 ORCHs"), plain(" will the client stand up in W1? (most common pair: ORCH-01 DSD + ORCH-02 Price Integrity)")]),
  checkbox([bold("Which store is the W1 pilot?"), plain(" (identify real store; Store 100 is synthetic)")]),
  checkbox([bold("Which data streams"), plain(" does the client already emit that feed these ORCHs? (receiving dock, POS, ESL gateway, etc.)")]),
  checkbox([bold("Who is the client-side sponsor?"), plain(" (typically VP Operations or VP Store Systems)")]),
  checkbox([bold("Who is the client-side technical lead?"), plain(" (typically a Fabric/Azure architect)")]),
  checkbox([bold("W1 success criteria"), plain(" — measurable, time-boxed (e.g., \"30% reduction in missed DSD claims over 90 days\")")]),
  checkbox([bold("W1 timeline"), plain(" — target start date, target exit date")]),
  checkbox([bold("What else needs to be true"), plain(" for the client to commit to W1? (contracting, security review, legal, etc.)")]),
  h2("14.2 Next-meeting artifacts to bring"),
  bullet("Wave 1 scope document (named ORCHs, named agents, named Microsoft services)"),
  bullet("Fleet-registry onboarding PR template"),
  bullet("Security / Independence review pack"),
  bullet("W1 timeline with milestones tied to wave-exit criteria"),
  h2("14.3 If the client asks for more time"),
  bullet([bold("\"We need to think about it.\""), plain(" → Schedule a follow-up in 10 business days. Provide the HTML walkthrough and the solution overview as leave-behinds. Identify the specific open question blocking decision.")]),
  bullet([bold("\"We need our CFO in the room.\""), plain(" → Best possible outcome. Prepare an economics-first version of this walkthrough leading with Events 01, 07, and 12's aggregate ROI.")]),
  bullet([bold("\"We need our Legal team in the room.\""), plain(" → Prepare a compliance-first version leading with the Independence posture (Core Part 6), the event-envelope audit trail, and the HITL-gate taxonomy as the governance model.")])
);

// Closing
children.push(
  new Paragraph({ spacing: { before: 400 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [italic("End of APEX · Store 100 Facilitator Guide — 2026-04-17")]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 140 },
    children: [new TextRun({
      text: "Reference implementation narrative: apex-rc-store-100-shift-walkthrough.html. Framework source: docs/build-specs/apex-core-build-spec.md · docs/build-specs/apex-rc-build-spec-v2.md. Companion: docs/guides/APEX-solution-overview.docx · docs/reference/APEX-RC-agent-catalog.docx.",
      italics: true, size: 20, color: "56627C"
    })]
  })
);

// --- Document ------------------------------------------------------------

const doc = new Document({
  creator: "Deloitte Microsoft Practice",
  title: "APEX Store 100 Facilitator Guide",
  description: "Account Team facilitator guide for the Store 100 reference implementation",
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Arial", color: "1A2339" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: "2F3F5F" },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: "2F3F5F" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } }
    ]
  },
  numbering: {
    config: [
      { reference: "bullets",
        levels: [{ level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] },
      { reference: "numbers",
        levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: PAGE_WIDTH, height: 15840 },
        margin: { top: PAGE_MARGIN, right: PAGE_MARGIN, bottom: PAGE_MARGIN, left: PAGE_MARGIN }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({ text: "APEX · Store 100 Facilitator Guide · Core v1.2", size: 18, color: "56627C" })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "Page ", size: 18, color: "56627C" }),
            new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "56627C" }),
            new TextRun({ text: " of ", size: 18, color: "56627C" }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 18, color: "56627C" })
          ]
        })]
      })
    },
    children
  }]
});

Packer.toBuffer(doc).then(buffer => {
  const out = "docs/guides/APEX-Store-100-facilitator-guide.docx";
  fs.writeFileSync(out, buffer);
  console.log(`wrote ${out} (${buffer.length.toLocaleString()} bytes)`);
  console.log(`  events: ${EVENTS.length}`);
  console.log(`  objections: ${objections.length}`);
}).catch(err => {
  console.error("failed:", err);
  process.exit(1);
});
