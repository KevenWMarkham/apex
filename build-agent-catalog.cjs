// Generate APEX-RC-agent-catalog.docx — deep-dive on all 34 RC agents.
// Run: node build-agent-catalog.cjs

const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat, HeadingLevel, BorderStyle,
  WidthType, ShadingType, PageBreak, PageNumber
} = require('docx');

// --- Styling constants ----------------------------------------------------

const PAGE_WIDTH = 12240;
const PAGE_MARGIN = 1080;
const CONTENT_WIDTH = PAGE_WIDTH - 2 * PAGE_MARGIN;

const border = { style: BorderStyle.SINGLE, size: 4, color: "B8B8B8" };
const cellBorders = { top: border, bottom: border, left: border, right: border };
const cardLabelShading = { fill: "F4EFE3", type: ShadingType.CLEAR, color: "auto" };
const cardValueShading = { fill: "FFFFFF", type: ShadingType.CLEAR, color: "auto" };
const headerShading = { fill: "1A2339", type: ShadingType.CLEAR, color: "auto" };
const matrixDotShading = { fill: "E6F7F4", type: ShadingType.CLEAR, color: "auto" };
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

function bullet(text, level = 0) {
  const children = Array.isArray(text) ? text : [new TextRun(text)];
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { after: 80, line: 280 },
    children
  });
}

function bold(text) { return new TextRun({ text, bold: true }); }
function italic(text) { return new TextRun({ text, italics: true }); }
function plain(text) { return new TextRun(text); }

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

// --- Agent card helper ----------------------------------------------------

const FIELD_ORDER = [
  'purpose',
  'primary_orch',
  'primary_schema',
  'inputs',
  'outputs',
  'decomposition',
  'hitl_gate',
  'wave'
];

const FIELD_LABELS = {
  purpose: 'Purpose',
  primary_orch: 'Primary ORCH',
  primary_schema: 'Primary schema',
  inputs: 'Inputs',
  outputs: 'Outputs',
  decomposition: 'Decomposition',
  hitl_gate: 'HITL gate',
  wave: 'Wave availability'
};

function agentCard(agent) {
  const labelWidth = 2400;
  const valueWidth = CONTENT_WIDTH - labelWidth;

  const titleRow = new TableRow({
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
          new TextRun({ text: `${agent.id}  `, bold: true, color: "F5A623", size: 22, font: "Consolas" }),
          new TextRun({ text: agent.name, bold: true, color: "FFFFFF", size: 24 })
        ]
      })]
    })]
  });

  const fieldRows = FIELD_ORDER.map(field => new TableRow({
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
            text: FIELD_LABELS[field].toUpperCase(),
            bold: true,
            size: 16,
            color: "56627C",
            font: "Consolas"
          })]
        })]
      }),
      new TableCell({
        borders: cellBorders,
        width: { size: valueWidth, type: WidthType.DXA },
        shading: cardValueShading,
        margins: cellMargins,
        children: [new Paragraph({
          spacing: { after: 0, line: 260 },
          children: [new TextRun({ text: agent[field] ?? '—', size: 20 })]
        })]
      })
    ]
  }));

  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [labelWidth, valueWidth],
    rows: [titleRow, ...fieldRows]
  });
}

function spacer() {
  return new Paragraph({ spacing: { after: 160 }, children: [] });
}

// --- Agent data (34 agents) ----------------------------------------------

const merchandising = [
  {
    id: "MER-A01", name: "Dynamic Pricing Agent",
    purpose: "Set and maintain store-level prices that balance demand elasticity against competitive signal and margin guardrails.",
    primary_orch: "(platform)",
    primary_schema: "MERML · PRICE_RECORD, STORE_INVENTORY_POSITION",
    inputs: "GV_STORE_PRICE_TODAY, competitive feeds, elasticity curves, margin policy.",
    outputs: "PRICE_RECORD updates, ESL push events, margin variance alerts.",
    decomposition: "elasticity learner, competitive signal, margin guardrail",
    hitl_gate: "ACK_ONLY — category manager receives a summary of price moves; HITL only on moves that breach margin policy.",
    wave: "W2 (Expansion)"
  },
  {
    id: "MER-A02", name: "Assortment Optimizer",
    purpose: "Identify under-performing SKUs, white-space candidates, and assortment rationalization opportunities per store cluster.",
    primary_orch: "ORCH-09 Assortment Optimization",
    primary_schema: "MERML · STORE_INVENTORY_POSITION, SHELF_FACING",
    inputs: "GV_STORE_VELOCITY_90D, planogram assignments, category benchmarks.",
    outputs: "Assortment change proposals; planogram update requests.",
    decomposition: "velocity analyzer, white-space detector, rationalization scorer",
    hitl_gate: "HITL — Category Manager approves planogram reshuffles before execution.",
    wave: "W3 (Platform)"
  },
  {
    id: "MER-A03", name: "Planogram Compliance Agent",
    purpose: "Detect shelf-facing deviations from planned planograms via computer vision and generate correction tasks.",
    primary_orch: "(platform)",
    primary_schema: "MERML · SHELF_FACING, PLANOGRAM_COMPLIANCE_EVENT",
    inputs: "Shelf CV feed, PLANOGRAM_ASSIGNMENT, associate roster.",
    outputs: "PLANOGRAM_COMPLIANCE_EVENT records; associate tasking messages.",
    decomposition: "shelf CV classifier, diff calculator, task router",
    hitl_gate: "ZERO_TOUCH — autonomous diff + task routing; ACK_ONLY summary to store manager daily.",
    wave: "W2 (Expansion)"
  },
  {
    id: "MER-A04", name: "ESL Gateway Monitor",
    purpose: "Ensure electronic shelf label pushes complete successfully; detect stale tags and generate bridge-tag events.",
    primary_orch: "ORCH-02 Pricing Integrity",
    primary_schema: "MERML · PRICE_RECORD",
    inputs: "ESL gateway telemetry, PRICE_RECORD changes, tag-battery state.",
    outputs: "Stale-tag alerts; bridge-tag events; gateway-health signals.",
    decomposition: "push verifier, stale-tag detector, bridge-tag generator",
    hitl_gate: "ZERO_TOUCH — automated remediation; HITL only on gateway failure exceeding SLO.",
    wave: "W1 (Foundation)"
  },
  {
    id: "MER-A05", name: "POS Mismatch Detector",
    purpose: "Reconcile shelf-displayed prices against POS ring prices and stage customer refunds when mismatched.",
    primary_orch: "ORCH-02 Pricing Integrity",
    primary_schema: "MERML · PRICE_RECORD, POS_VOID",
    inputs: "POS transaction stream, GV_STORE_PRICE_TODAY, shelf CV (where available).",
    outputs: "Mismatch alerts; customer refund records; training signals for pricing agents.",
    decomposition: "price-ring comparator, customer refund stager",
    hitl_gate: "ACK_ONLY — store manager confirms refunds above a threshold.",
    wave: "W1 (Foundation)"
  },
  {
    id: "MER-A06", name: "Phantom OOS Detector",
    purpose: "Identify on-shelf availability failures where perpetual inventory says stock exists but CV+POS evidence contradicts.",
    primary_orch: "ORCH-04 Labor & Fulfillment",
    primary_schema: "MERML · STORE_INVENTORY_POSITION, OSA_EVENT",
    inputs: "Shelf CV, POS velocity, perpetual inventory, GV_STORE_VELOCITY_90D.",
    outputs: "OSA_EVENT records; replenishment task triggers; variance signals.",
    decomposition: "CV-POS-perpetual fusion, confidence scorer",
    hitl_gate: "ACK_ONLY — associate receives picklist replenishment task.",
    wave: "W1 (Foundation)"
  },
  {
    id: "MER-A07", name: "Pick List Optimizer",
    purpose: "Build efficient pick-walk sequences for associate replenishment based on velocity and physical layout.",
    primary_orch: "ORCH-04 Labor & Fulfillment",
    primary_schema: "MERML · STORE_INVENTORY_POSITION",
    inputs: "Active OSA events, store map, associate location, shift schedule.",
    outputs: "Ordered pick lists; walk-time estimates; task completion telemetry.",
    decomposition: "velocity ranker, walking-order solver",
    hitl_gate: "ZERO_TOUCH — embedded in associate mobile app.",
    wave: "W1 (Foundation)"
  },
  {
    id: "MER-A08", name: "Associate Router",
    purpose: "Match store associates to tasks (replenishment, planogram fix, customer assist) based on zone, skill, and radio status.",
    primary_orch: "ORCH-04 Labor & Fulfillment",
    primary_schema: "MERML · (task queue; no canonical entity today)",
    inputs: "Associate zone/radio state, task queue, shift schedule, SLO policy.",
    outputs: "Task-to-associate assignments; dispatch notifications.",
    decomposition: "zone tracker, task-match scorer, radio-status listener",
    hitl_gate: "ZERO_TOUCH — autonomous routing; store manager sees daily rollup.",
    wave: "W2 (Expansion)"
  },
  {
    id: "MER-A09", name: "Void Pattern Detector",
    purpose: "Detect statistically-anomalous POS void patterns by employee and category for loss-prevention investigation.",
    primary_orch: "ORCH-07 Shrink & Loss Prevention",
    primary_schema: "MERML · POS_VOID, SHRINK_EVENT",
    inputs: "GV_EMPLOYEE_VOID_90D, category sigma baselines, register telemetry.",
    outputs: "Anomaly alerts; candidate investigation cases.",
    decomposition: "sigma anomaly, category isolator, employee-register correlator",
    hitl_gate: "ESCALATION — Loss Prevention team takes ownership; agent never acts on employees directly.",
    wave: "W2 (Expansion)"
  },
  {
    id: "MER-A10", name: "Variance Correlator",
    purpose: "Correlate cycle-count variance against recent return receipts and voids to distinguish shrink from recordkeeping drift.",
    primary_orch: "ORCH-07 Shrink & Loss Prevention",
    primary_schema: "MERML · CYCLE_COUNT_VARIANCE, SHRINK_EVENT",
    inputs: "Cycle count snapshots, return records, void records, receiving discrepancies.",
    outputs: "Classified variance reasons; shrink/recordkeeping split.",
    decomposition: "cycle-count matcher, return-receipt cross-checker",
    hitl_gate: "ACK_ONLY — store manager reviews classification weekly.",
    wave: "W2 (Expansion)"
  },
  {
    id: "MER-A11", name: "Evidence Package Builder",
    purpose: "Assemble timeline + artifact bundles (POS records, CCTV frames, receipts) for Loss Prevention investigations.",
    primary_orch: "ORCH-07 Shrink & Loss Prevention",
    primary_schema: "MERML · POS_VOID, SHRINK_EVENT (and CCTV index)",
    inputs: "All relevant transaction records, CCTV timestamp index, employee roster.",
    outputs: "Evidence bundle artifacts for LP/HR/legal review.",
    decomposition: "timeline assembler, CCTV-frame referencer",
    hitl_gate: "ESCALATION — bundle handed to Loss Prevention; agent does not adjudicate.",
    wave: "W3 (Platform)"
  },
  {
    id: "MER-A12", name: "Markdown Cadence Agent",
    purpose: "Classify expiring / near-expiring product and time markdown recommendations to minimize waste.",
    primary_orch: "(platform)",
    primary_schema: "MERML · LOT_EXPIRATION_STATE, MARKDOWN_EVENT, WASTE_EVENT",
    inputs: "LOT_EXPIRATION_STATE, sell-through velocity, markdown policy.",
    outputs: "MARKDOWN_EVENT records; disposition recommendations.",
    decomposition: "expiration tracker, disposition classifier",
    hitl_gate: "ACK_ONLY — category manager reviews markdown cadence summary.",
    wave: "W2 (Expansion)"
  }
];

const supplyChain = [
  {
    id: "SCM-A01", name: "DSD Reconciliation Agent",
    purpose: "Match direct-store-delivery invoices against advance shipment notices and flag line-level variances.",
    primary_orch: "ORCH-01 DSD Reconciliation & Claims",
    primary_schema: "SCML · ASN, STORE_RECEIVING_EVENT",
    inputs: "Vendor portal ASN feed, DSD invoices, receiving dock scans.",
    outputs: "Reconciled line items; variance records; dispute candidates.",
    decomposition: "portal-ASN matcher, line-level variance",
    hitl_gate: "ACK_ONLY — receiving manager acknowledges matched line items.",
    wave: "W1 (Foundation)"
  },
  {
    id: "SCM-A02", name: "Vendor Pattern Detector",
    purpose: "Classify recurring vendor shortfall patterns across a 90-day rolling window to distinguish noise from policy violations.",
    primary_orch: "ORCH-01 DSD Reconciliation & Claims",
    primary_schema: "SCML · ASN, STORE_RECEIVING_EVENT",
    inputs: "90-day reconciled DSD history per vendor, vendor SLA policy.",
    outputs: "Vendor-pattern classifications; escalation candidates.",
    decomposition: "90d window scorer, recurrence classifier",
    hitl_gate: "ACK_ONLY — merchandising reviews vendor scorecards weekly.",
    wave: "W2 (Expansion)"
  },
  {
    id: "SCM-A03", name: "Claim Assembly Agent",
    purpose: "Draft vendor-dispute claims with attached evidence (ASN diffs, receiving photos, invoice lines).",
    primary_orch: "ORCH-01 DSD Reconciliation & Claims",
    primary_schema: "SCML · ASN, STORE_RECEIVING_EVENT",
    inputs: "Matched variance records, evidence artifacts, vendor dispute templates.",
    outputs: "Draft claim packages ready for accounts-payable submission.",
    decomposition: "evidence attacher, dispute drafter",
    hitl_gate: "HITL — Accounts Payable reviews and submits claims.",
    wave: "W2 (Expansion)"
  },
  {
    id: "SCM-A04", name: "Cold Chain Telemetry Monitor",
    purpose: "Watch per-lot temperature sensors continuously and classify excursions against product-class thresholds.",
    primary_orch: "ORCH-03 Cold Chain & Disposition",
    primary_schema: "SCML · COLD_CHAIN_TELEMETRY",
    inputs: "IoT sensor feed (Event Hubs), product-class thresholds, transit manifests.",
    outputs: "Excursion events; severity classifications; downstream triggers.",
    decomposition: "threshold watcher, excursion classifier",
    hitl_gate: "ZERO_TOUCH on detection; ACK_ONLY to DC manager for minor excursions.",
    wave: "W2 (Expansion)"
  },
  {
    id: "SCM-A05", name: "Disposition Classifier",
    purpose: "Decide save-vs-destroy for product lots after cold-chain excursions based on sub-category risk profile.",
    primary_orch: "ORCH-03 Cold Chain & Disposition",
    primary_schema: "SCML · COLD_CHAIN_TELEMETRY, LOT_TRACE",
    inputs: "Excursion records, regulatory limits, product-class risk tables.",
    outputs: "Save/destroy disposition; financial impact estimate.",
    decomposition: "sub-category risk scorer, save/destroy splitter",
    hitl_gate: "HITL for destroy-recommendations above a dollar threshold; ACK_ONLY for save.",
    wave: "W2 (Expansion)"
  },
  {
    id: "SCM-A06", name: "Write-Off Pre-Approver",
    purpose: "Stage write-off proposals in the loss ledger with pre-populated approval routing and supporting evidence.",
    primary_orch: "ORCH-03 Cold Chain & Disposition",
    primary_schema: "SCML · COLD_CHAIN_TELEMETRY (and finance ledger)",
    inputs: "Destroy dispositions, write-off policy, approval routing rules.",
    outputs: "Staged write-off records; approval-route notifications.",
    decomposition: "loss-ledger stager, approval-route primer",
    hitl_gate: "HITL — Finance approver signs off via approval workflow.",
    wave: "W3 (Platform)"
  },
  {
    id: "SCM-A07", name: "FDA Feed Listener",
    purpose: "Continuously parse FDA and state regulatory recall feeds and resolve matches to active store inventory.",
    primary_orch: "ORCH-05 Recall Impact",
    primary_schema: "SCML · RECALL_NOTICE, LOT_TRACE",
    inputs: "FDA public feed, state regulatory feeds, vendor advisories.",
    outputs: "RECALL_NOTICE records; lot-match triggers for traceability.",
    decomposition: "recall parser, lot resolver",
    hitl_gate: "ZERO_TOUCH — autonomous ingestion; ESCALATION triggers downstream if match found.",
    wave: "W2 (Expansion)"
  },
  {
    id: "SCM-A08", name: "Lot Trace Resolver",
    purpose: "Trace affected lots upstream to suppliers and downstream to stores and customers for recall impact assessment.",
    primary_orch: "ORCH-05 Recall Impact",
    primary_schema: "SCML · LOT_TRACE, RECALL_NOTICE",
    inputs: "RECALL_NOTICE, LOT_TRACE records, CXML · LOYALTY_STATE for customer resolution.",
    outputs: "Impacted-lot manifest; affected-store list; customer notification queue.",
    decomposition: "upstream tracer, downstream tracer, customer identifier",
    hitl_gate: "HITL — recall coordinator confirms customer-notification scope before dispatch.",
    wave: "W2 (Expansion)"
  }
];

const customerExperience = [
  {
    id: "CXM-A01", name: "Pick Exception Handler",
    purpose: "Classify fulfillment pick exceptions and surface alternative-finding opportunities in real time.",
    primary_orch: "ORCH-06 Fulfillment Exception Handling",
    primary_schema: "CXML · FULFILLMENT_ORDER, PICK_EXCEPTION",
    inputs: "Live pick events, inventory snapshot, substitution history.",
    outputs: "Classified exception records; alternative-candidate shortlist.",
    decomposition: "OOS classifier, alternative finder",
    hitl_gate: "ZERO_TOUCH classification; downstream HITL via Customer Confirm.",
    wave: "W2 (Expansion)"
  },
  {
    id: "CXM-A02", name: "Substitution Ranker",
    purpose: "Rank substitution candidates by 14-month customer-history signals, margin, and inventory position.",
    primary_orch: "ORCH-06 Fulfillment Exception Handling",
    primary_schema: "CXML · SUBSTITUTION_EVENT, FULFILLMENT_ORDER",
    inputs: "14mo customer purchase history, inventory position, margin policy.",
    outputs: "Ranked substitution shortlist; confidence scores.",
    decomposition: "14mo history scorer, rank composer",
    hitl_gate: "ZERO_TOUCH — feeds Customer Confirm Gateway for the final human step.",
    wave: "W2 (Expansion)"
  },
  {
    id: "CXM-A03", name: "Customer Confirm Gateway",
    purpose: "Send one-tap SMS confirmations for substitutions and age-out unanswered requests within SLO.",
    primary_orch: "ORCH-06 Fulfillment Exception Handling",
    primary_schema: "CXML · SUBSTITUTION_EVENT",
    inputs: "Substitution shortlist, customer contact preferences, order SLA timer.",
    outputs: "Confirmation events; timeout events; substitution decisions.",
    decomposition: "one-tap SMS, aging monitor",
    hitl_gate: "HITL — the customer is the human in the loop.",
    wave: "W2 (Expansion)"
  },
  {
    id: "CXM-A04", name: "OCR Lot Extractor",
    purpose: "Extract lot codes from customer-submitted product photos during incident reports for recall correlation.",
    primary_orch: "ORCH-08 Customer Incident Response",
    primary_schema: "CXML · CUSTOMER_INCIDENT",
    inputs: "Customer-submitted images, product-class OCR templates.",
    outputs: "Parsed lot codes; confidence scores; incident-image index.",
    decomposition: "image normalizer, code parser",
    hitl_gate: "ZERO_TOUCH — low-confidence extractions are flagged for human review.",
    wave: "W3 (Platform)"
  },
  {
    id: "CXM-A05", name: "Incident Pattern Detector",
    purpose: "Correlate incidents across stores to identify tier-1 (isolated) vs tier-2 (systemic) product issues.",
    primary_orch: "ORCH-08 Customer Incident Response",
    primary_schema: "CXML · CUSTOMER_INCIDENT",
    inputs: "All active incidents, lot trace, store roster, historical incident patterns.",
    outputs: "Tier classifications; cross-store correlation bundles.",
    decomposition: "cross-store correlator, tier classifier",
    hitl_gate: "ESCALATION — tier-2 classifications trigger stakeholder routing.",
    wave: "W3 (Platform)"
  },
  {
    id: "CXM-A06", name: "Stakeholder Router",
    purpose: "Dispatch tier-2 incidents in parallel to QA, Legal, and Communications teams with tailored briefs.",
    primary_orch: "ORCH-08 Customer Incident Response",
    primary_schema: "CXML · CUSTOMER_INCIDENT",
    inputs: "Tier-2 incident bundle, stakeholder contact roster, brief templates.",
    outputs: "QA ticket, Legal brief, Comms draft — dispatched in parallel.",
    decomposition: "QA/Legal/Comms parallel dispatcher",
    hitl_gate: "ESCALATION — each stakeholder is a separate human-in-loop recipient.",
    wave: "W3 (Platform)"
  },
  {
    id: "CXM-A07", name: "Returns Disposition Agent",
    purpose: "Decide resell / regrade / RTV / destroy for each returned item and draft the RTV claim where applicable.",
    primary_orch: "ORCH-12 Customer Lifecycle",
    primary_schema: "CXML · RETURN_TRANSACTION",
    inputs: "Return record, product condition tag, vendor RTV policy, resale-floor eligibility.",
    outputs: "Disposition decisions; draft RTV claim packages.",
    decomposition: "disposition selector, RTV claim drafter",
    hitl_gate: "ACK_ONLY — returns desk acknowledges routine; HITL for high-value or fraud-flagged returns.",
    wave: "W3 (Platform)"
  },
  {
    id: "CXM-A08", name: "Lifecycle Signal Agent",
    purpose: "Predict customer churn and identify winback opportunities from lifecycle state transitions.",
    primary_orch: "ORCH-12 Customer Lifecycle",
    primary_schema: "CXML · LOYALTY_STATE",
    inputs: "LOYALTY_STATE, purchase recency/frequency/monetary, MKTL journey state.",
    outputs: "Churn-risk scores; winback opportunity records; campaign triggers.",
    decomposition: "churn predictor, winback opportunity scorer",
    hitl_gate: "ACK_ONLY — marketing reviews weekly campaign triggers.",
    wave: "W4 (Adaptive)"
  }
];

const marketing = [
  {
    id: "MKT-A01", name: "Audience Builder",
    purpose: "Resolve audience segment definitions against the customer base and apply suppression filters for compliance.",
    primary_orch: "ORCH-11 Campaign Orchestration",
    primary_schema: "MKTL · AUDIENCE, SEGMENT_MEMBERSHIP",
    inputs: "Segment definitions, customer profile data, consent records, suppression rules.",
    outputs: "Materialized audiences; membership deltas; suppression-filtered counts.",
    decomposition: "segment resolver, suppression filter",
    hitl_gate: "ACK_ONLY — marketing confirms segment counts before campaign launch.",
    wave: "W3 (Platform)"
  },
  {
    id: "MKT-A02", name: "Creative Variant Generator",
    purpose: "Generate campaign creative variants (copy + image briefs) under brand guardrails.",
    primary_orch: "ORCH-11 Campaign Orchestration",
    primary_schema: "MKTL · CAMPAIGN, CREATIVE_ASSET",
    inputs: "Campaign brief, brand guardrail rules, audience profile, historical performance.",
    outputs: "Creative variant set; brand-compliance scores.",
    decomposition: "copy generator, image brief builder, brand guardrail checker",
    hitl_gate: "HITL — creative director approves or edits variants before activation.",
    wave: "W3 (Platform)"
  },
  {
    id: "MKT-A03", name: "Campaign Orchestrator",
    purpose: "Sequence channel activations and pace spend across the campaign lifecycle.",
    primary_orch: "ORCH-11 Campaign Orchestration",
    primary_schema: "MKTL · CAMPAIGN",
    inputs: "Approved creative, channel inventory, pacing policy, real-time engagement signals.",
    outputs: "Channel activation schedule; pacing adjustments; launch events.",
    decomposition: "channel sequencer, pacing controller",
    hitl_gate: "ACK_ONLY — marketing reviews daily pacing reports; HITL on budget variance.",
    wave: "W3 (Platform)"
  },
  {
    id: "MKT-A04", name: "Attribution Agent",
    purpose: "Run multi-touch attribution and incrementality tests continuously to credit touchpoints with revenue.",
    primary_orch: "(platform)",
    primary_schema: "MKTL · ATTRIBUTION_EVENT",
    inputs: "Full touchpoint stream, conversion events, holdout definitions.",
    outputs: "Attribution credits per touchpoint; incrementality estimates with CIs.",
    decomposition: "MTA model runner, incrementality tester",
    hitl_gate: "ZERO_TOUCH — reports surface in BI; no direct action on customers.",
    wave: "W4 (Adaptive)"
  },
  {
    id: "MKT-A05", name: "LTV Forecaster",
    purpose: "Forecast customer lifetime value at the individual level and simulate the impact of proposed interventions.",
    primary_orch: "ORCH-12 Customer Lifecycle",
    primary_schema: "MKTL · JOURNEY_STATE, SEGMENT_MEMBERSHIP",
    inputs: "Historical purchase stream, demographic signals, active loyalty state, proposed intervention set.",
    outputs: "LTV forecasts; intervention-lift estimates.",
    decomposition: "cohort modeler, intervention simulator",
    hitl_gate: "ACK_ONLY — marketing reviews intervention recommendations monthly.",
    wave: "W4 (Adaptive)"
  },
  {
    id: "MKT-A06", name: "Journey State Agent",
    purpose: "Classify each customer's current journey state and rank next-best-actions against personalized goals.",
    primary_orch: "ORCH-12 Customer Lifecycle",
    primary_schema: "MKTL · JOURNEY_STATE, SEGMENT_MEMBERSHIP",
    inputs: "Live event stream, journey definitions, NBA action catalog.",
    outputs: "JOURNEY_STATE transitions; next-best-action rankings; experience triggers.",
    decomposition: "state transition classifier, next-best-action ranker",
    hitl_gate: "ZERO_TOUCH — embedded in personalization surfaces; ACK_ONLY for weekly rollups.",
    wave: "W4 (Adaptive)"
  }
];

const DOMAINS = [
  {
    name: "Merchandising Domain",
    count: 12,
    primary: "MERML",
    consumed: "CXML, MKTL",
    cadence: "Minute–hour operational; daily planning; weekly assortment.",
    agents: merchandising
  },
  {
    name: "Supply Chain Domain",
    count: 8,
    primary: "SCML",
    consumed: "MERML",
    cadence: "Second–minute for cold chain and recall; hour–day for planning.",
    agents: supplyChain
  },
  {
    name: "Customer Experience Domain",
    count: 8,
    primary: "CXML",
    consumed: "MERML, MKTL",
    cadence: "Second for omnichannel; minute–hour for incidents; session-based for personalization.",
    agents: customerExperience
  },
  {
    name: "Marketing Domain",
    count: 6,
    primary: "MKTL",
    consumed: "CXML, MERML",
    cadence: "Hour–day for activation; week for planning; campaign-lifecycle for optimization.",
    agents: marketing
  }
];

const ALL_AGENTS = [...merchandising, ...supplyChain, ...customerExperience, ...marketing];

// --- Cross-reference matrix (Part 6) -------------------------------------

function buildOrchMatrix() {
  const orchs = ["ORCH-01","ORCH-02","ORCH-03","ORCH-04","ORCH-05","ORCH-06","ORCH-07","ORCH-08","ORCH-09","ORCH-10","ORCH-11","ORCH-12","(platform)"];
  const colWidth = Math.floor((CONTENT_WIDTH - 1800) / orchs.length);
  const firstCol = 1800;

  const headerRow = new TableRow({
    tableHeader: true,
    children: [
      new TableCell({
        borders: cellBorders, width: { size: firstCol, type: WidthType.DXA },
        shading: headerShading, margins: cellMargins,
        children: [new Paragraph({ children: [new TextRun({ text: "Agent", bold: true, color: "FFFFFF", size: 16 })] })]
      }),
      ...orchs.map(o => new TableCell({
        borders: cellBorders, width: { size: colWidth, type: WidthType.DXA },
        shading: headerShading, margins: { top: 80, bottom: 80, left: 40, right: 40 },
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: o.replace("ORCH-",""), bold: true, color: "FFFFFF", size: 14, font: "Consolas" })]
        })]
      }))
    ]
  });

  const dataRows = ALL_AGENTS.map(a => {
    const orchKey = a.primary_orch.startsWith("ORCH-") ? a.primary_orch.split(" ")[0] : "(platform)";
    return new TableRow({
      cantSplit: true,
      children: [
        new TableCell({
          borders: cellBorders, width: { size: firstCol, type: WidthType.DXA },
          shading: cardLabelShading, margins: cellMargins,
          children: [new Paragraph({
            children: [new TextRun({ text: a.id, bold: true, size: 16, font: "Consolas", color: "2F3F5F" })]
          })]
        }),
        ...orchs.map(o => {
          const hit = o === orchKey;
          return new TableCell({
            borders: cellBorders, width: { size: colWidth, type: WidthType.DXA },
            shading: hit ? matrixDotShading : cardValueShading,
            margins: { top: 60, bottom: 60, left: 20, right: 20 },
            children: [new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [new TextRun({ text: hit ? "\u25CF" : "\u00B7", color: hit ? "0D7D70" : "B8B8B8", size: 18 })]
            })]
          });
        })
      ]
    });
  });

  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [firstCol, ...orchs.map(() => colWidth)],
    rows: [headerRow, ...dataRows]
  });
}

// --- Cadence summary (Part 7) --------------------------------------------

function buildCadenceTable() {
  const bands = [
    { label: "Second (real-time)", members: ["SCM-A04","CXM-A01","CXM-A02","CXM-A03","MKT-A06"] },
    { label: "Minute (near-real-time)", members: ["MER-A04","MER-A05","MER-A06","MER-A07","SCM-A05","CXM-A04"] },
    { label: "Hour (operational)", members: ["MER-A01","MER-A03","MER-A08","MER-A12","SCM-A01","SCM-A06","SCM-A07","SCM-A08","CXM-A05","CXM-A06","CXM-A07","MKT-A03"] },
    { label: "Day (planning)", members: ["MER-A09","MER-A10","MER-A11","SCM-A02","SCM-A03","CXM-A08","MKT-A01","MKT-A02"] },
    { label: "Weekly / campaign-cycle", members: ["MER-A02","MKT-A04","MKT-A05"] }
  ];

  const rows = bands.map(b => [
    b.label,
    `${b.members.length} agent${b.members.length === 1 ? '' : 's'}`,
    b.members.join(", ")
  ]);

  const col0 = 2800, col1 = 1400, col2 = CONTENT_WIDTH - col0 - col1;
  const header = new TableRow({
    tableHeader: true,
    children: ["Cadence band","Count","Agents"].map((h, i) => new TableCell({
      borders: cellBorders, width: { size: [col0,col1,col2][i], type: WidthType.DXA },
      shading: headerShading, margins: cellMargins,
      children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, color: "FFFFFF", size: 20 })] })]
    }))
  });
  const body = rows.map(r => new TableRow({
    children: r.map((cell, i) => new TableCell({
      borders: cellBorders, width: { size: [col0,col1,col2][i], type: WidthType.DXA },
      margins: cellMargins,
      children: [new Paragraph({ children: [new TextRun({ text: cell, size: 20, font: i === 2 ? "Consolas" : "Arial" })] })]
    }))
  }));
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: [col0, col1, col2],
    rows: [header, ...body]
  });
}

// --- Document assembly ----------------------------------------------------

const children = [];

// Title page
children.push(
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 3600, after: 200 },
    children: [new TextRun({ text: "APEX · RC", bold: true, size: 80, color: "1A2339" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [new TextRun({ text: "Agent Catalog", size: 48, color: "2F3F5F" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 720 },
    children: [new TextRun({ text: "Deep-dive on all 34 agents in the Retail & Consumer edition", italics: true, size: 26, color: "8A97B2" })]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER, spacing: { after: 100 },
    children: [new TextRun({ text: "Companion to: APEX Solution Overview", size: 22 })]
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
  p("This document inherits Part 0 of APEX Core unchanged. All Deloitte–Microsoft terminology rules apply. All agent references are synthetic, consistent with the RC edition's published roster. No client-identifiable names appear."),
  p("Gate-type references use the Core Part 8.3 taxonomy unchanged: HITL, ACK_ONLY, ZERO_TOUCH, ESCALATION. Wave references use the Core Part 12 convention: W1 Foundation, W2 Expansion, W3 Platform, W4 Adaptive.")
);

// Part 1 - How to read
children.push(
  h1("Part 1 — How to Read This Catalog"),
  p("Each of the 34 RC agents is documented on its own card using eight consistent fields. Reading the fields in order gives you the full picture: the problem the agent solves, where it plugs into the orchestration grid, which canonical schema it reads and writes, and how a human stays in control."),
  h2("The eight fields"),
  bullet([bold("Purpose"), plain(" — one-sentence problem statement. What decision or enablement does this agent provide?")]),
  bullet([bold("Primary ORCH"), plain(" — the orchestration this agent is the main participant in. (platform) means the agent is a cross-cutting capability used by many ORCHs rather than bound to one.")]),
  bullet([bold("Primary schema + key entities"), plain(" — the canonical schema the agent authoritatively reads/writes, with the entities it touches most.")]),
  bullet([bold("Inputs"), plain(" — the Gold views, schema entities, or external feeds the agent consumes.")]),
  bullet([bold("Outputs"), plain(" — the records, events, artifacts, or state changes the agent produces.")]),
  bullet([bold("Decomposition"), plain(" — the named sub-agent contracts verbatim from the RC build spec Part 5. Each sub-agent is backtested in isolation before being wired into the parent.")]),
  bullet([bold("HITL gate"), plain(" — the Core Part 8.3 gate type that applies. Many agents have mixed gates (e.g., ACK_ONLY for routine cases, HITL above a threshold); the card names the dominant gate and notes the threshold if applicable.")]),
  bullet([bold("Wave availability"), plain(" — the deployment wave in which this agent becomes generally available for production use.")]),
  h2("Domain intros"),
  p("Each domain part opens with a brief preamble listing the primary schema the domain's agents own, the schemas they consume, and the decision cadence band the domain operates in. This context is lifted verbatim from the RC build spec so the catalog stays consistent with the authoritative specification."),
  h2("Cross-references"),
  p("Two cross-reference artifacts close out the catalog: Part 6 is the Agent × ORCH matrix (at-a-glance view of which agents participate in which orchestrations) and Part 7 is the decision-cadence summary (which agents live in which temporal band).")
);

// Parts 2-5 - One per domain
DOMAINS.forEach((d, idx) => {
  children.push(
    h1(`Part ${idx + 2} — ${d.name} (${d.count} agents)`),
    p([
      bold("Primary schema: "), plain(`${d.primary}.  `),
      bold("Consumed schemas: "), plain(`${d.consumed}.  `),
      bold("Decision cadence: "), plain(d.cadence)
    ])
  );
  d.agents.forEach(a => {
    children.push(agentCard(a));
    children.push(spacer());
  });
});

// Part 6 - Cross-reference matrix
children.push(
  h1("Part 6 — Agent × ORCH Cross-Reference Matrix"),
  p("At-a-glance view of which agents participate in which orchestrations. Each filled dot indicates the agent's primary ORCH binding. The right-most column marks cross-cutting platform agents that are not bound to a single ORCH."),
  buildOrchMatrix(),
  p(""),
  p([italic("ORCH numbering (Core Part 8.1) is a positional slot, not a semantic guarantee. ORCH-05 in APEX-RC is Recall Impact; the same slot in other editions names different orchestrations. The number identifies the position across the 12-slot grid, not a shared meaning.")])
);

// Part 7 - Cadence summary
children.push(
  h1("Part 7 — Decision-Cadence Summary"),
  p("RC agents operate across five temporal bands. The band an agent lives in shapes everything downstream: eval cadence, telemetry SLOs, observability dashboards, and the choice of platform service (Event Hubs for second-band, Logic Apps for hour-band, Fabric Data Factory for day-band, etc.)."),
  buildCadenceTable(),
  p(""),
  p([italic("Some agents span bands (e.g., Dynamic Pricing is minute-band for ESL push verification but hour-band for elasticity re-estimation). Each agent is placed in its dominant band; secondary bands are noted in the agent card's Inputs/Outputs fields.")])
);

// Closing
children.push(
  new Paragraph({ spacing: { before: 400 }, children: [] }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [italic("End of APEX · RC Agent Catalog — 2026-04-17")]
  }),
  new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 140 },
    children: [new TextRun({
      text: "For the full RC edition specification, read docs/build-specs/apex-rc-build-spec-v2.md. For the APEX framework overview, read docs/guides/APEX-solution-overview.docx.",
      italics: true, size: 20, color: "56627C"
    })]
  })
);

// --- Assemble document ----------------------------------------------------

const doc = new Document({
  creator: "Deloitte Microsoft Practice",
  title: "APEX RC Agent Catalog",
  description: "Deep-dive reference for all 34 RC-edition agents",
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
          children: [new TextRun({ text: "APEX · RC Agent Catalog · Core v1.2", size: 18, color: "56627C" })]
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
  const out = "docs/reference/APEX-RC-agent-catalog.docx";
  fs.writeFileSync(out, buffer);
  console.log(`wrote ${out} (${buffer.length.toLocaleString()} bytes)`);
  console.log(`  agents: ${ALL_AGENTS.length}`);
  console.log(`  domains: ${DOMAINS.length}`);
}).catch(err => {
  console.error("failed:", err);
  process.exit(1);
});
