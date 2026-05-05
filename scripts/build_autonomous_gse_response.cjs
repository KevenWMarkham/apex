// Build: Autonomous GSE — APEX Services Positioning
// For: Nagataka Asa (Deloitte Japan) proposal
// Author: Keven Markham, DMTSP

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
  BorderStyle, WidthType, ShadingType, PageNumber, PageBreak,
  TabStopType, TabStopPosition,
} = require('docx');

const AZURE = "0078D4";
const TEAL = "008272";
const SLATE_BG = "F1F5F9";
const HEAD_BG = "0F172A";
const BORDER = "CCCCCC";

const cellBorder = { style: BorderStyle.SINGLE, size: 4, color: BORDER };
const cellBorders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };

function p(text, opts = {}) {
  return new Paragraph({
    spacing: { after: 120, ...opts.spacing },
    alignment: opts.align,
    children: [new TextRun({ text, bold: opts.bold, italics: opts.italics, size: opts.size || 22, color: opts.color })],
  });
}

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 360, after: 200 },
    children: [new TextRun({ text, bold: true, size: 32, color: HEAD_BG })],
    border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: AZURE, space: 4 } },
  });
}
function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 140 },
    children: [new TextRun({ text, bold: true, size: 26, color: AZURE })],
  });
}
function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 200, after: 100 },
    children: [new TextRun({ text, bold: true, size: 22, color: TEAL })],
  });
}

function bullet(text, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { after: 80 },
    children: [new TextRun({ text, size: 22 })],
  });
}

function bulletRich(runs, level = 0) {
  return new Paragraph({
    numbering: { reference: "bullets", level },
    spacing: { after: 80 },
    children: runs,
  });
}

function headerCell(text, width) {
  return new TableCell({
    borders: cellBorders,
    width: { size: width, type: WidthType.DXA },
    shading: { fill: HEAD_BG, type: ShadingType.CLEAR },
    margins: { top: 100, bottom: 100, left: 140, right: 140 },
    children: [new Paragraph({ children: [new TextRun({ text, bold: true, color: "FFFFFF", size: 20 })] })],
  });
}

function dataCell(text, width, opts = {}) {
  return new TableCell({
    borders: cellBorders,
    width: { size: width, type: WidthType.DXA },
    shading: opts.shaded ? { fill: SLATE_BG, type: ShadingType.CLEAR } : undefined,
    margins: { top: 80, bottom: 80, left: 140, right: 140 },
    children: [new Paragraph({ children: [new TextRun({ text, bold: opts.bold, size: 20 })] })],
  });
}

// =====================================================================
// CONTENT
// =====================================================================

const cover = [
  new Paragraph({
    spacing: { before: 0, after: 200 },
    children: [new TextRun({ text: "DELOITTE  ·  DMTSP  ·  CONSUMER INDUSTRY", bold: true, size: 18, color: AZURE })],
  }),
  new Paragraph({
    spacing: { before: 0, after: 120 },
    children: [new TextRun({ text: "Autonomous Ground Support Equipment (GSE)", bold: true, size: 44, color: HEAD_BG })],
  }),
  new Paragraph({
    spacing: { before: 0, after: 80 },
    children: [new TextRun({ text: "APEX-Aligned Services & Capability Positioning", bold: true, size: 28, color: TEAL })],
  }),
  new Paragraph({
    spacing: { before: 0, after: 360 },
    children: [new TextRun({ text: "Prepared for the Deloitte Japan Autonomous GSE Market Research engagement", italics: true, size: 22, color: "475569" })],
  }),
  p("Author: Keven Markham, Specialist Master, Deloitte Microsoft Technology & Services Practice (DMTSP)", { size: 20 }),
  p("Recipient: Nagataka Asa, Deloitte Japan", { size: 20 }),
  p("Date: 1 May 2026", { size: 20 }),
  p("Classification: Internal — Deloitte Global", { size: 20, italics: true }),
  new Paragraph({ children: [new PageBreak()] }),
];

const execSummary = [
  h1("1. Executive Summary"),
  p("Autonomous Ground Support Equipment (GSE) — autonomous tugs, baggage tractors, belt loaders, pushback tractors, GPUs, lavatory and water service vehicles — sits at the convergence of three forces that Deloitte's APEX framework was purpose-built to address: industrial fleet telemetry at scale, time-pressured airline turn operations, and a regulatory environment that is hardening around safety cases for autonomous airside operations."),
  p("APEX (Agentic Platform for Enterprise eXecution) is DMTSP's domain-canonical reference framework for deploying agentic AI on Microsoft-native infrastructure. It is not a product; it is a framework-of-frameworks that gives every industry a shared grammar (Core) and an industry dialect (Edition). For autonomous GSE, three APEX Practices apply directly:"),
  bulletRich([
    new TextRun({ text: "ICE — Industrial & Commercial Equipment", bold: true, size: 22 }),
    new TextRun({ text: " — fleet asset health, utilization optimisation, spare-parts triage, compliance inspection. The natural home for the GSE asset itself.", size: 22 }),
  ]),
  bulletRich([
    new TextRun({ text: "TH — Travel & Hospitality (airline sub-variant)", bold: true, size: 22 }),
    new TextRun({ text: " — turn operations, disruption recovery, ramp dispatch. The natural home for how autonomous GSE participates in the airline operating model.", size: 22 }),
  ]),
  bulletRich([
    new TextRun({ text: "AXLE — Automotive depth programme", bold: true, size: 22 }),
    new TextRun({ text: " — autonomous-vehicle engineering depth that GSE OEMs need for safety case construction, V&V harnesses, and ODD (Operational Design Domain) discipline.", size: 22 }),
  ]),
  p("Combined, these Practices give the engagement team a structured lens on (a) what airport operators need from autonomous GSE, and (b) what success factors separate the winning GSE OEMs from the rest. Sections 4 and 5 of this document address each."),
];

const aboutAPEX = [
  h1("2. APEX in One Page"),
  p("APEX is a manifest-driven, agentic platform that turns enterprise events into resolved, auditable decisions. It runs on Microsoft Fabric (data plane) and Azure AI services (intelligence plane), bound by a versioned contract that specifies every schema, agent, tool, orchestration, and human-in-the-loop (HITL) gate."),
  h3("Seven-Layer Reference Architecture"),
  p("Every Practice inherits the same seven layers — L1 Edge & Source, L2 Ingest & Integration, L3 Storage, L4 Semantic, L5 Intelligence, L6 Orchestration, L7 Experience — each mapped to specific Microsoft services. For autonomous GSE, L1 is the vehicle bus, ramp telemetry, and CDM/A-CDM feeds; L7 is the OCC dispatcher, the ramp coordinator, and the maintenance lead."),
  h3("Catalog Today"),
  p("45 catalogued services across seven Practices: 25 GA (RC, HLS, ER, AXLE) and 20 in active build (TMT, TH, ICE) with 2026 GA targets. Each service is a subscribable SKU: scenario + personas + KPIs + SLOs + artifact bundle + prerequisites + commercial terms."),
  h3("Why this matters for autonomous GSE"),
  p("Autonomous GSE is a quintessential APEX problem: high-frequency event streams from heterogeneous sources, time-critical decisions with safety implications, regulated audit trails, and a need to compose decisions across operator, OEM, ANSP, and regulator boundaries. APEX provides the manifest discipline (schemas, gates, evidence) without forcing the client onto a shared runtime."),
];

// Service mapping table
const serviceTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [1400, 2400, 2200, 3360],
  rows: [
    new TableRow({ tableHeader: true, children: [
      headerCell("Service ID", 1400),
      headerCell("Service", 2400),
      headerCell("APEX Practice", 2200),
      headerCell("Autonomous GSE Application", 3360),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-ICE-FAF-01", 1400, { bold: true }),
      dataCell("Field Asset Failure Response", 2400),
      dataCell("ICE — Industrial & Commercial Equipment", 2200),
      dataCell("Predict and triage GSE failures (battery, drive, sensor stack) before they cause a missed turn. Anchors fleet-wide health telemetry to the airline operating clock.", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-ICE-SPA-02", 1400, { bold: true }),
      dataCell("Spare-Parts Availability Triage", 2400),
      dataCell("ICE", 2200),
      dataCell("Critical for autonomous platforms: lidar, IMU, compute modules and traction batteries are long-lead. Pre-positions parts to hub airports against forecasted MTBF and turn density.", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-ICE-WCP-03", 1400, { bold: true }),
      dataCell("Warranty Claim Pattern Analysis", 2400),
      dataCell("ICE", 2200),
      dataCell("For OEMs: detect failure-mode patterns across the deployed autonomous GSE fleet earlier than manual claim review; closes the field-to-engineering loop.", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-ICE-CRP-04", 1400, { bold: true }),
      dataCell("Contract-Renewal Revenue Protection", 2400),
      dataCell("ICE", 2200),
      dataCell("Detects degradation signals (uptime drift, dispatch reliability) in autonomous-GSE service contracts before renewal — protects recurring revenue for OEM and lessor.", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-ICE-AaS-05", 1400, { bold: true }),
      dataCell("As-a-Service Utilization Optimization", 2400),
      dataCell("ICE", 2200),
      dataCell("The flagship service for GSE-as-a-Service commercial models. Tracks per-asset utilisation, SLA conformance, and pay-per-use telemetry. Enables OEMs to move from sale to subscription.", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-ICE-CIR-06", 1400, { bold: true }),
      dataCell("Compliance Inspection Response", 2400),
      dataCell("ICE", 2200),
      dataCell("Direct fit for FAA Part 139, EASA / CAA, and JCAB inspection regimes plus SAE J3016-style autonomy levels and ICAO Annex 14 airside safety. Maintains audit-grade evidence per inspection.", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-TH-DRO-02", 1400, { bold: true }),
      dataCell("Disruption Recovery Orchestration", 2400),
      dataCell("TH — Travel & Hospitality (airline)", 2200),
      dataCell("When weather, IRROPS, or a stand closure cascades, autonomous-GSE allocation becomes a constraint variable. DRO re-optimises GSE deployment alongside crew, gate, and aircraft.", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-TH-HER-06", 1400, { bold: true }),
      dataCell("Exception Routing (ramp variant)", 2400),
      dataCell("TH (airline-adapted)", 2200),
      dataCell("Originally housekeeping; the same exception-routing pattern adapts to ramp exceptions: stuck tug, missed pushback window, GPU offline.", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-ER-FWO-04", 1400, { bold: true }),
      dataCell("Field Work-Order Optimisation", 2400),
      dataCell("ER — Energy & Resources", 2200),
      dataCell("The crew-skills + route-optimiser pair (ER-A07/A08) transfers cleanly to autonomous-GSE maintenance dispatch across a hub footprint with 1st-time-fix targets.", 3360, { shaded: true }),
    ]}),
    new TableRow({ children: [
      dataCell("APEX-AXLE", 1400, { bold: true }),
      dataCell("Autonomous-Vehicle Depth Programme", 2400),
      dataCell("AXLE — Automotive", 2200),
      dataCell("For GSE OEMs: ODD definition, V&V harness, safety-case scaffolding, OTA update discipline. The automotive-depth complement to ICE's commercial framing.", 3360, { shaded: true }),
    ]}),
  ],
});

const serviceMapping = [
  h1("3. APEX Service Mapping for Autonomous GSE"),
  p("The table below maps APEX catalogued services to the autonomous GSE problem domain. Each row is a subscribable SKU with a defined scenario, KPIs, HITL gates, and an artifact bundle. A typical Wave 1 engagement subscribes to two or three services; the portfolio grows from there."),
  serviceTable,
  p(""),
  h3("Cross-Practice Capabilities Always Included"),
  bullet("Manifest model — every schema (vehicle telemetry, work orders, inspection events) version-pinned with bump classification and migration discipline."),
  bullet("HITL gate taxonomy — every decision declares HITL, ACK_ONLY, ZERO_TOUCH, or ESCALATION. Critical for autonomous-airside safety cases."),
  bullet("Independence posture — client-tenant data planes; Deloitte retains zero client-identifiable telemetry. Important for airport operator data-sovereignty conversations."),
  bullet("Observability — Application Insights, Fabric monitoring, custom agent telemetry; supports regulator-readable audit trails."),
];

const airportNeeds = [
  h1("4. Airport-Related Issues & Needs Driving Autonomous GSE"),
  p("Drawn from the APEX TH-airline and ICE Practice frames; corroborated against ACI, IATA AHM, and JCAB / FAA airside posture as of 2026."),
  h2("4.1 Operational Drivers"),
  bullet("Turn-time compression — narrow-body turns trending below 30 minutes at hub airports; ground service variability is now the dominant residual delay contributor after weather and ATC."),
  bullet("Ramp labour scarcity — post-pandemic ramp-agent attrition is structural in North America, EU, and Japan; recruiting cycles outpace fleet growth at major hubs."),
  bullet("Stand congestion & A-CDM tightening — CDM/A-CDM milestones (TOBT, TSAT, ATOT) are tightening; ad-hoc GSE allocation no longer meets the milestone window."),
  bullet("Heterogeneous fleet age — most hubs operate three generations of GSE concurrently; autonomous platforms must coexist with manual equipment for at least a decade."),
  h2("4.2 Safety & Regulatory Drivers"),
  bullet("Airside safety cases — autonomous GSE must demonstrate ODD-bounded safe operation under Annex 14 / Part 139 inspection regimes; safety-case construction is the long-pole engineering effort."),
  bullet("Foreign Object Debris (FOD) and ramp-incident reduction — autonomous GSE telemetry creates first-time visibility into near-miss events; airport authorities increasingly expect this evidence."),
  bullet("ICAO / IATA AHM alignment — equipment-independent vehicle data standards (AHM 950 / 956) are gaining traction; autonomous platforms must emit conformant telemetry."),
  bullet("Cybersecurity for airside autonomy — ENISA, TSA, and JCAB are sharpening guidance for autonomous airside; OT/IT segmentation and OTA update control are now procurement criteria."),
  h2("4.3 Commercial & Sustainability Drivers"),
  bullet("GSE-as-a-Service commercial models — airports and ground handlers prefer pay-per-turn or pay-per-utilisation over capex; this requires telemetry, SLA discipline, and metered billing infrastructure."),
  bullet("Electrification overlap — autonomy is arriving at the same time as eGSE; charging-window scheduling is a new constraint that changes optimisation models."),
  bullet("Net-zero airport commitments — most major hubs have 2030 / 2035 net-zero airside targets; autonomous + electric GSE is the credible compliance pathway."),
  bullet("Insurance & risk transfer — carriers are still pricing autonomous-GSE risk; structured operating data accelerates underwriter confidence and reduces premiums."),
  h2("4.4 Integration & Data Drivers"),
  bullet("Airport Operational Database (AODB) integration — autonomous GSE must read TOBT/TSAT and emit position/status to be useful at the gate-level."),
  bullet("Multi-stakeholder data contracts — operator, OEM, ground handler, and ANSP each require different views of the same telemetry; consent and data-sharing frameworks are immature."),
  bullet("Legacy radio dispatch — many ramp operations still run on voice radio; autonomous platforms force a re-architecture of dispatch tooling that benefits the whole operation."),
];

const successFactors = [
  h1("5. Key Success Factors for Autonomous GSE Developers"),
  p("Synthesised from APEX's AXLE (automotive autonomy depth) and ICE (industrial fleet) practice patterns, plus DMTSP fieldwork on adjacent autonomous-mobility programmes."),
  h2("5.1 Engineering & Product Success Factors"),
  bullet("ODD discipline — winning OEMs publish a tight, evidenced Operational Design Domain and grow it with measured V&V, rather than over-claiming Level-4 capability across all weather and surface conditions."),
  bullet("Sensor redundancy with airside-credible failure modes — multi-modal sensor stacks (lidar + radar + camera + IMU) with independent failure paths; demonstrable safe-stop behaviour under FOD, low sun, and standing water."),
  bullet("Vehicle bus + telemetry fluency — first-class CAN, J1939, and OEM-specific bus integration with lossless cloud telemetry; autonomy without telemetry has no safety case."),
  bullet("OTA update discipline — staged rollouts, signed updates, deterministic rollback; aligned with TSA/ENISA / JCAB cyber expectations for airside."),
  bullet("Twin-track HMI — one HMI for autonomous operation, one for tele-operated fallback; both must coexist on the platform from day one."),
  h2("5.2 Operational & Commercial Success Factors"),
  bullet("Day-one integration with A-CDM / AODB — winning entrants ship with TOBT/TSAT consumption and event publishing; losing entrants treat integration as a phase-2 problem."),
  bullet("GSE-as-a-Service commercial model — utilisation-priced contracts (per turn, per kWh, per uptime hour) align OEM economics with operator outcomes; a flat sale pre-empts the recurring relationship."),
  bullet("Spare-parts pre-positioning at hubs — autonomy components (compute modules, lidars, traction batteries) are long-lead; OEMs that stage parts at hub airports earn higher dispatch reliability."),
  bullet("Service-network density — autonomy MTBF is improving but still demands dense field-service coverage; the OEMs that win hub deals are the ones who can field a same-shift technician."),
  bullet("Fleet-mixed orchestration — autonomous platforms must dispatch alongside manual equipment for a decade; OEMs that publish open APIs into ramp dispatch tools earn faster pilot conversion."),
  h2("5.3 Safety, Regulatory & Trust Success Factors"),
  bullet("Pre-built safety-case artifacts — STPA, FMEA, hazard logs, and ODD-traceable test evidence shipped with the product, not produced ad-hoc per airport."),
  bullet("Independent V&V harness — third-party-audited verification builds regulator trust faster than internal claims, especially in JCAB and EASA jurisdictions."),
  bullet("Airside cyber posture — segmented OT/IT, signed firmware, secure-boot evidence, and an SBOM are increasingly mandatory in 2026 procurement."),
  bullet("Transparent incident telemetry — winning OEMs publish near-miss and intervention data to the operator under a clear data-sharing contract; trust compounds, opacity erodes."),
  h2("5.4 Ecosystem & Partnership Success Factors"),
  bullet("Airline-grade SLAs as a forcing function — designing to a published OTP-relevant SLA (e.g., 99.5% pushback dispatch reliability) drives the right architecture upstream."),
  bullet("Microsoft / hyperscaler alignment for telemetry & intelligence — Fabric / Azure AI Foundry / Azure AI Agent Service is the most regulator-credible stack for airside in 2026; OEMs that build on it pre-empt operator IT objections."),
  bullet("Co-development with ground handlers — Swissport, dnata, Menzies, and similar are the primary day-to-day operators of GSE; OEM partnerships here accelerate fleet conversion."),
  bullet("Standards engagement — active participation in IATA AHM working groups, ISO TC 20/SC 9, and SAE G-31 (autonomy in aviation) signals long-term seriousness to airport authorities."),
];

const deloitteFit = [
  h1("6. Deloitte Capability Hooks (DMTSP × APEX)"),
  p("Deloitte's Microsoft practice (DMTSP) brings APEX as the framework, plus the engagement engineering to land it. The autonomous-GSE engagement model has four predictable workstreams:"),
  h3("Workstream A — Operator-Side Implementation"),
  bullet("Foundation wave: Fabric workspace topology, ICE schema deployment, first 2–3 ICE services live (typical FAF-01 + AaS-05 + CIR-06)."),
  bullet("Intelligence wave: TH-airline disruption-recovery integration with ramp dispatch; cross-Practice observability."),
  bullet("Optimisation wave: cross-hub roll-out; multi-handler tenancy; net-zero KPI integration."),
  h3("Workstream B — OEM-Side Product & Telemetry"),
  bullet("AXLE depth: ODD definition, V&V harness scaffolding, safety-case content discipline."),
  bullet("ICE-AaS-05: As-a-Service utilisation telemetry build-out; metered billing integration."),
  bullet("ICE-WCP-03: warranty pattern analysis on deployed-fleet telemetry; closes field-to-engineering loop."),
  h3("Workstream C — Regulatory & Safety Case"),
  bullet("ICE-CIR-06 implementation: audit-grade evidence pipeline aligned to FAA Part 139, EASA, and JCAB regimes."),
  bullet("HITL taxonomy: explicit gate declarations on every autonomous decision surface, suitable for regulator review."),
  h3("Workstream D — Commercial Model"),
  bullet("Subscription pricing and SLA design for GSE-as-a-Service contracts."),
  bullet("Insurance / risk-transfer structuring with telemetry-backed underwriting."),
  bullet("Investment envelope per Practice: $3–8M Wave 1, $5–12M Wave 2, $3–6M Wave 3. Expected 2–4× cumulative ROI on Wave 1 services by month 18."),
];

const closingCV = [
  h1("7. Author Background — Keven Markham"),
  p("Specialist Master, Deloitte Microsoft Technology & Services Practice (DMTSP). 22+ years across Microsoft platforms (Azure, Fabric, Power Platform, Copilot, Foundry, Security). Lead architect on APEX framework. Transportation- and airport-adjacent work spans cross-airport asset health programmes, ramp-operations data architectures, and autonomous-mobility pattern adaptation from automotive (AXLE) to industrial fleets (ICE)."),
  h3("Relevant APEX Authorship for this Engagement"),
  bullet("APEX Core (manifest model, HITL taxonomy, seven-layer reference architecture)."),
  bullet("APEX-ICE Practice (Field Asset Failure Response, As-a-Service Utilization Optimization, Compliance Inspection Response)."),
  bullet("APEX-TH airline sub-variant (Disruption Recovery Orchestration, ramp exception routing patterns)."),
  bullet("APEX-AXLE complementary programme (autonomous-vehicle depth scaffolding)."),
  h3("CV Inclusion in Proposal"),
  p("Latest CV will be shared separately by 4 May 2026 EOD EST per request. Please confirm preferred format (Deloitte Global standard CV vs. proposal-specific one-pager) on receipt."),
  new Paragraph({ children: [new PageBreak()] }),
  h1("Appendix A — Reference Documents"),
  bullet("APEX Solution Overview (DMTSP, current as of APEX Core v1.2, 2026-04-17)."),
  bullet("APEX Comprehensive Solutions Reference (catalogue of 45 services across seven Practices)."),
  bullet("Transportation AHM · APEX & AXLE for Fleet Asset Management deck (DMTSP)."),
  bullet("AXLE-3D Factory KPIs reference (DMTSP)."),
  bullet("APEX-Stacked-Architecture-Narrated reference (DMTSP)."),
  p("All reference documents available on request via DMTSP SharePoint."),
];

// =====================================================================
// DOCUMENT
// =====================================================================

const doc = new Document({
  creator: "Keven Markham, DMTSP",
  title: "Autonomous GSE — APEX Services Positioning",
  description: "APEX-aligned services positioning for Deloitte Japan autonomous GSE proposal",
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial", color: HEAD_BG },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: AZURE },
        paragraph: { spacing: { before: 280, after: 140 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, font: "Arial", color: TEAL },
        paragraph: { spacing: { before: 200, after: 100 }, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets",
        levels: [
          { level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
          { level: 1, format: LevelFormat.BULLET, text: "\u25E6", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 1440, hanging: 360 } } } },
        ] },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    headers: {
      default: new Header({ children: [
        new Paragraph({
          tabStops: [{ type: TabStopType.RIGHT, position: 9360 }],
          children: [
            new TextRun({ text: "Deloitte  ·  DMTSP", color: AZURE, bold: true, size: 18 }),
            new TextRun({ text: "\tAutonomous GSE — APEX Services Positioning", color: "475569", size: 18 }),
          ],
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: AZURE, space: 4 } },
        }),
      ]}),
    },
    footers: {
      default: new Footer({ children: [
        new Paragraph({
          tabStops: [{ type: TabStopType.RIGHT, position: 9360 }],
          children: [
            new TextRun({ text: "Internal — Deloitte Global  ·  1 May 2026", color: "94A3B8", size: 16 }),
            new TextRun({ text: "\tPage ", color: "94A3B8", size: 16 }),
            new TextRun({ children: [PageNumber.CURRENT], color: "94A3B8", size: 16 }),
            new TextRun({ text: " of ", color: "94A3B8", size: 16 }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], color: "94A3B8", size: 16 }),
          ],
        }),
      ]}),
    },
    children: [
      ...cover,
      ...execSummary,
      ...aboutAPEX,
      ...serviceMapping,
      ...airportNeeds,
      ...successFactors,
      ...deloitteFit,
      ...closingCV,
    ],
  }],
});

const outDir = path.resolve(__dirname, "..", "docs", "APEX - Design and Build");
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
const outPath = path.join(outDir, "Autonomous-GSE-APEX-Services-Positioning.docx");

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outPath, buffer);
  console.log("Wrote:", outPath);
});
