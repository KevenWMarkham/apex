"""W3 Fusion Mesh Catalog — Sprint 28 Task 28.3 (BL.P.174–176).

Sellers Guide §2.2 treats Wave-3 as "Sustain & Transform" — the moment
where multiple Wave-2 scenarios fuse into composed outcomes spanning
the Practice. The Fusion catalog names those meshes so SoWs can quote
Wave-3 commercial without re-deriving the composition each time.

Per Practice, 5–8 fusion meshes per build-instructions §28.3.1
(target: 35–56 total across all 7 Practices). Each mesh carries:

- ``mesh_id`` — stable identifier (e.g., ``mesh.rc.perishables-economics``)
- ``practice`` — RC / HLS / ER / AXLE / TMT / TH / ICE
- ``name`` — short display label
- ``description`` — what composed outcome this mesh delivers
- ``constituent_w2_service_codes`` — Wave-2 service codes feeding the mesh
- ``composed_outcomes`` — what fusion buys you that individual W2 does not
- ``orchestration_archetype`` — Sprint 19 archetype id powering the mesh
- ``target_tenant_profile`` — which tenant shape buys this mesh

The HTML tab placement (Task 28.3.4) is front-end work; this module
ships the Python data + lookup helpers. Cross-link from scenarios'
Wave-3 ribbon to mesh entries (Task 28.3.6) consumes
:func:`mesh_by_w2_service_code`.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FusionMesh:
    """One Wave-3 fusion mesh."""

    mesh_id: str
    practice: str
    name: str
    description: str
    constituent_w2_service_codes: tuple[str, ...]
    composed_outcomes: tuple[str, ...]
    orchestration_archetype: str
    target_tenant_profile: str = ""


# ---------------------------------------------------------------------------
# Catalog — 5-8 meshes per Practice
# ---------------------------------------------------------------------------


CATALOG: tuple[FusionMesh, ...] = (
    # ----- RC (5) -----
    FusionMesh(
        mesh_id="mesh.rc.perishables-economics",
        practice="rc",
        name="Perishables Economics Mesh",
        description="Cold-chain disposition + markdown cadence + loyalty-churn signal compose into perishables P&L recovery.",
        constituent_w2_service_codes=("RC-E2E-04", "RC-E2E-05", "RC-E2E-07"),
        composed_outcomes=(
            "Per-store perishables margin lift",
            "FSMA 204 audit posture sustained",
            "Loyalty-tier retention rate stabilized post-disposition events",
        ),
        orchestration_archetype="arch.recovery.001",
        target_tenant_profile="Big-box grocer with cold-chain estate ≥ 200 stores",
    ),
    FusionMesh(
        mesh_id="mesh.rc.assortment-velocity",
        practice="rc",
        name="Assortment Velocity Mesh",
        description="Demand sensing + inventory replenishment + substitution recommender fused for omnichannel velocity.",
        constituent_w2_service_codes=("RC-E2E-03", "RC-TTP-04", "RC-TTP-06"),
        composed_outcomes=(
            "Top-200-SKU OOS rate sustained reduction",
            "Substitution acceptance rate stable across channels",
            "Demand-shock response time compressed",
        ),
        orchestration_archetype="arch.optimize.004",
        target_tenant_profile="Multi-format grocer with omnichannel fulfillment",
    ),
    FusionMesh(
        mesh_id="mesh.rc.shrink-and-trust",
        practice="rc",
        name="Shrink-and-Trust Mesh",
        description="Shrink-detection + customer-identity + LP investigation chain composed into chain-wide trust uplift.",
        constituent_w2_service_codes=("RC-E2E-06", "RC-E2E-08"),
        composed_outcomes=(
            "Chain-wide shrink % of sales reduction sustained",
            "False-accusation rate near zero (customer-identity integration)",
            "LP team throughput +50% via auto-evidence packets",
        ),
        orchestration_archetype="arch.rca.002",
        target_tenant_profile="Mass / GM retailer with mature LP function",
    ),
    FusionMesh(
        mesh_id="mesh.rc.merchant-intel",
        practice="rc",
        name="Merchant Intelligence Mesh",
        description="Markdown cadence + assortment-pricing + competitive scan fused as the chief-merchant copilot surface.",
        constituent_w2_service_codes=("RC-E2E-05", "RC-E2E-09"),
        composed_outcomes=(
            "Sustained gross-margin uplift +200-400bps chain-wide",
            "Markdown cadence yield +10-15% sell-through",
            "Competitive-action approval cycle compressed to same-day",
        ),
        orchestration_archetype="arch.optimize.001",
        target_tenant_profile="Specialty retailer with seasonal velocity exposure",
    ),
    FusionMesh(
        mesh_id="mesh.rc.store-operating-model",
        practice="rc",
        name="Store Operating Model Mesh",
        description="Store-ops digest + cold-chain + replenishment + shrink fused as the store-manager unified surface.",
        constituent_w2_service_codes=("RC-E2E-04", "RC-E2E-07", "RC-TTP-04"),
        composed_outcomes=(
            "Store-manager intervention list reduced from 30+ to top-3 daily",
            "Cross-store consistency on disposition decisions",
            "Routine-decision autonomy in HOTL by Wave-3",
        ),
        orchestration_archetype="arch.summarize.001",
        target_tenant_profile="Chain operator transitioning store-manager role to coach",
    ),

    # ----- HLS (6) -----
    FusionMesh(
        mesh_id="mesh.hls.revenue-and-outcomes",
        practice="hls",
        name="Revenue-and-Outcomes Mesh",
        description="Denial prevention + prior-auth + care-gap closure compose into payer-aligned revenue + outcomes.",
        constituent_w2_service_codes=("HLS-PAY-01", "HLS-PAY-02", "HLS-LS-03"),
        composed_outcomes=(
            "First-pass denial rate sustained -35%",
            "Care-gap closure rate +25-40pp on instrumented HEDIS measures",
            "Value-based-care contract margin lift",
        ),
        orchestration_archetype="arch.score.001",
        target_tenant_profile="IDN with significant value-based contract exposure",
    ),
    FusionMesh(
        mesh_id="mesh.hls.acute-care-safety",
        practice="hls",
        name="Acute-Care Safety Mesh",
        description="Sepsis early warning + drug interaction + adverse-event detection fused for hospital-wide safety.",
        constituent_w2_service_codes=("HLS-E2E-01", "HLS-LS-03"),
        composed_outcomes=(
            "SEP-1 compliance > 90% sustained hospital-wide",
            "Adverse-event detection precision +25pp vs. prior baseline",
            "Pharmacovigilance signal-to-FDA cycle compressed",
        ),
        orchestration_archetype="arch.predict.003",
        target_tenant_profile="Acute-care hospital with mature CDS estate",
    ),
    FusionMesh(
        mesh_id="mesh.hls.utilization-and-throughput",
        practice="hls",
        name="Utilization & Throughput Mesh",
        description="LOS prediction + readmission risk + utilization management compose into bed-throughput optimization.",
        constituent_w2_service_codes=("HLS-E2E-02", "HLS-E2E-04"),
        composed_outcomes=(
            "Med-surg LOS -1.0 day hospital-wide",
            "30-day readmission -4pp sustained on CHF/pneumonia",
            "ED boarding hours -50% sustained",
        ),
        orchestration_archetype="arch.optimize.002",
        target_tenant_profile="Bed-constrained IDN with ED-boarding pain",
    ),
    FusionMesh(
        mesh_id="mesh.hls.population-health",
        practice="hls",
        name="Population Health Mesh",
        description="Risk stratification + care-gap + study-enrollment fused for population-health management.",
        constituent_w2_service_codes=("HLS-E2E-03", "HLS-LS-05"),
        composed_outcomes=(
            "Top-decile risk cohort intervention rate +40pp",
            "Clinical-trial enrollment rate +25pp on instrumented protocols",
            "HEDIS Stars metric uplift",
        ),
        orchestration_archetype="arch.score.001",
        target_tenant_profile="IDN running ACO + research mission",
    ),
    FusionMesh(
        mesh_id="mesh.hls.identity-and-consent",
        practice="hls",
        name="Identity & Consent Mesh",
        description="Patient identity + consent management + 42 CFR Part 2 segmentation compose into trust posture.",
        constituent_w2_service_codes=("HLS-E2E-03",),
        composed_outcomes=(
            "Duplicate-MRN rate near zero",
            "Consent-violation incidents zero (auditor-attested)",
            "42 CFR Part 2 segmentation regulator-confirmed",
        ),
        orchestration_archetype="arch.match.001",
        target_tenant_profile="IDN with behavioral-health + SUD service lines",
    ),
    FusionMesh(
        mesh_id="mesh.hls.supply-and-pharmacy",
        practice="hls",
        name="Supply & Pharmacy Mesh",
        description="Supply cold-chain + adverse-event + medication reconciliation fused for pharmacy safety + cost.",
        constituent_w2_service_codes=("HLS-LS-03",),
        composed_outcomes=(
            "Pharmacy waste from cold-chain incidents -60%",
            "Adverse-drug-event detection precision +30pp",
            "Medication reconciliation cycle time -50%",
        ),
        orchestration_archetype="arch.triage.005",
        target_tenant_profile="IDN with central pharmacy + 503B distribution",
    ),

    # ----- ER (5) -----
    FusionMesh(
        mesh_id="mesh.er.grid-reliability",
        practice="er",
        name="Grid Reliability Mesh",
        description="Outage triage + restoration sequencing + vegetation-risk fused for territory-wide reliability.",
        constituent_w2_service_codes=("ER-PU-02", "ER-PU-03"),
        composed_outcomes=(
            "SAIDI -15-20% sustained system-wide",
            "Vegetation defect-find rate +60% sustained",
            "Crew dispatch acceptance >90% (mature operations)",
        ),
        orchestration_archetype="arch.recovery.002",
        target_tenant_profile="Investor-owned electric utility with high vegetation exposure",
    ),
    FusionMesh(
        mesh_id="mesh.er.wildfire-risk",
        practice="er",
        name="Wildfire-Risk Mesh",
        description="PSPS decision + vegetation risk + asset health composed for regulator-grade wildfire risk posture.",
        constituent_w2_service_codes=("ER-PU-01", "ER-PU-03"),
        composed_outcomes=(
            "PSPS audit completeness 100% maintained + regulator-attested",
            "Wildfire-ignition events from utility-side equipment near zero",
            "PUC public-records compliance sustained",
        ),
        orchestration_archetype="arch.explain.002",
        target_tenant_profile="California / Pacific-Northwest IOU with HFTD exposure",
    ),
    FusionMesh(
        mesh_id="mesh.er.der-and-demand",
        practice="er",
        name="DER & Demand Mesh",
        description="DER orchestration + AMI billing + demand-response composed for grid-edge optimization.",
        constituent_w2_service_codes=("ER-PU-04", "ER-MN-01"),
        composed_outcomes=(
            "Peak shaving 5-10% sustained",
            "Demand-response participation rate +20pp",
            "Customer DER + EV integration scaled to 30%+ of load",
        ),
        orchestration_archetype="arch.optimize.003",
        target_tenant_profile="Utility with growing DER + EV penetration",
    ),
    FusionMesh(
        mesh_id="mesh.er.upstream-ops",
        practice="er",
        name="Upstream Ops Mesh",
        description="Well operations + drilling safety + HSE incident composed for upstream O&G safety+productivity.",
        constituent_w2_service_codes=("ER-OG-01", "ER-OG-02", "ER-OG-03"),
        composed_outcomes=(
            "TRIR sustained ≤ 0.5",
            "Non-productive time (NPT) -40% sustained",
            "Field-engineer cognitive-load reduction (measured via HSE near-miss reporting +30%)",
        ),
        orchestration_archetype="arch.predict.002",
        target_tenant_profile="Major upstream oil & gas operator",
    ),
    FusionMesh(
        mesh_id="mesh.er.mining-fleet",
        practice="er",
        name="Mining Fleet Mesh",
        description="Fleet-mining + autonomy + HSE composed for autonomous-haulage transition.",
        constituent_w2_service_codes=("ER-OG-03", "ER-MN-01"),
        composed_outcomes=(
            "Haul-cycle time -15% sustained",
            "Fuel-burn per ton -8% sustained",
            "Autonomy uptime > 95%",
        ),
        orchestration_archetype="arch.optimize.002",
        target_tenant_profile="Open-pit mining operator with autonomous-haul ambitions",
    ),

    # ----- AXLE (5) -----
    FusionMesh(
        mesh_id="mesh.axle.connected-factory",
        practice="axle",
        name="Connected Factory Mesh",
        description="OEE monitor + predictive maintenance + andon-RCA fused for plant-wide OEE compounding.",
        constituent_w2_service_codes=("AXLE-Connected-Factory-01", "AXLE-Connected-Factory-02"),
        composed_outcomes=(
            "OEE +10pp plant-wide sustained",
            "Unplanned downtime -40% sustained",
            "Andon-RCA cycle compressed to same-shift",
        ),
        orchestration_archetype="arch.monitor.001",
        target_tenant_profile="Multi-line discrete-manufacturing plant",
    ),
    FusionMesh(
        mesh_id="mesh.axle.quality-supply",
        practice="axle",
        name="Quality & Supply Mesh",
        description="Quality defect + supplier quality + warranty cost fused for end-to-end PPM reduction.",
        constituent_w2_service_codes=("AXLE-QMS-01", "AXLE-Aftermarket-01"),
        composed_outcomes=(
            "Field-defect PPM -50% sustained",
            "Warranty cost per vehicle -8-12% sustained",
            "Supplier 8D corrective-action throughput +2x",
        ),
        orchestration_archetype="arch.rca.002",
        target_tenant_profile="Tier-1 automotive supplier or industrial OEM with warranty exposure",
    ),
    FusionMesh(
        mesh_id="mesh.axle.production-scheduling",
        practice="axle",
        name="Production Scheduling Mesh",
        description="Production scheduling + supply chain + energy optimization composed for cost-aware throughput.",
        constituent_w2_service_codes=("AXLE-Ops-01", "AXLE-Ops-03", "AXLE-Supply-01"),
        composed_outcomes=(
            "Schedule-attainment > 95% sustained",
            "Energy cost per unit -15-20% sustained",
            "Material-buffer inventory -25% sustained",
        ),
        orchestration_archetype="arch.optimize.002",
        target_tenant_profile="Multi-plant manufacturer with central scheduling",
    ),
    FusionMesh(
        mesh_id="mesh.axle.connected-product",
        practice="axle",
        name="Connected-Product Mesh",
        description="Vehicle DTC + telematics + warranty cost composed for connected-product service economics.",
        constituent_w2_service_codes=("AXLE-Aftermarket-01", "AXLE-Aftermarket-02"),
        composed_outcomes=(
            "Service first-time-fix rate +15pp",
            "Pattern-based recall lead time compressed by months",
            "Telemetry-driven service revenue +30% sustained",
        ),
        orchestration_archetype="arch.predict.002",
        target_tenant_profile="Automotive OEM with connected-vehicle estate",
    ),
    FusionMesh(
        mesh_id="mesh.axle.engineering-loop",
        practice="axle",
        name="Engineering Loop Mesh",
        description="Generative engineering + warranty + quality fused for design-to-field feedback loop.",
        constituent_w2_service_codes=("AXLE-QMS-01", "AXLE-Aftermarket-01"),
        composed_outcomes=(
            "Design change cycle from field-claim to PLM revision compressed",
            "Predictive-quality at NPI design boundary integrated",
            "DfM analytics in mainline NPI workflow",
        ),
        orchestration_archetype="arch.compose.001",
        target_tenant_profile="Industrial OEM with mature PLM + warranty data",
    ),

    # ----- TMT (5) -----
    FusionMesh(
        mesh_id="mesh.tmt.customer-care-uplift",
        practice="tmt",
        name="Customer Care Uplift Mesh",
        description="Contact-center copilot + churn risk + traveler-360 equivalent for telco subscribers fused for retention.",
        constituent_w2_service_codes=(),
        composed_outcomes=(
            "AHT -25% sustained",
            "FCR ≥ 80% sustained",
            "Churn -2-3pp sustained on full base",
        ),
        orchestration_archetype="arch.summarize.001",
        target_tenant_profile="Tier-1 telco with mature contact-center estate",
    ),
    FusionMesh(
        mesh_id="mesh.tmt.network-health",
        practice="tmt",
        name="Network Health Mesh",
        description="Network ops + DORA-aware DevOps + incident MTTR composed for self-healing network.",
        constituent_w2_service_codes=(),
        composed_outcomes=(
            "Routine alarm self-resolution > 60%",
            "DORA top-quartile across all four metrics",
            "Customer-impacting incident MTTR -50%",
        ),
        orchestration_archetype="arch.monitor.002",
        target_tenant_profile="Telco / B2B SaaS with mature SRE function",
    ),
    FusionMesh(
        mesh_id="mesh.tmt.content-trust",
        practice="tmt",
        name="Content Trust Mesh",
        description="IVT detection + content safety + appeal-overturn composed for trust + monetization integrity.",
        constituent_w2_service_codes=(),
        composed_outcomes=(
            "IVT rate -50% sustained",
            "Trust-and-safety review backlog cleared (1-day SLA)",
            "Appeal-overturn rate stabilized (auditor-attested)",
        ),
        orchestration_archetype="arch.score.001",
        target_tenant_profile="Ad-tech / OTT platform with monetization integrity exposure",
    ),
    FusionMesh(
        mesh_id="mesh.tmt.devex",
        practice="tmt",
        name="DevEx Mesh",
        description="Developer-experience copilot + DORA + content-platform composed for platform DevEx uplift.",
        constituent_w2_service_codes=(),
        composed_outcomes=(
            "Lead-time-for-changes top-quartile",
            "Engineer NPS uplift",
            "Production incident-MTTR aligned with SaaS SLAs",
        ),
        orchestration_archetype="arch.summarize.001",
        target_tenant_profile="B2B SaaS with significant DevOps investment",
    ),
    FusionMesh(
        mesh_id="mesh.tmt.subscriber-360",
        practice="tmt",
        name="Subscriber 360 Mesh",
        description="Subscriber data platform + journey orchestration + offer-management composed for cross-channel uplift.",
        constituent_w2_service_codes=(),
        composed_outcomes=(
            "Cross-channel offer acceptance rate +20pp",
            "ARPU uplift on instrumented segments",
            "Cross-sell take-rate +30% sustained",
        ),
        orchestration_archetype="arch.personalize.001",
        target_tenant_profile="Carrier with mature CDP investment",
    ),

    # ----- TH (5) -----
    FusionMesh(
        mesh_id="mesh.th.network-recovery",
        practice="th",
        name="Network Recovery Mesh",
        description="IROPS recovery + crew scheduling + disruption-comms fused for integrated cross-domain recovery.",
        constituent_w2_service_codes=("TH-AIR-01",),
        composed_outcomes=(
            "IROPS recovery cycle median 20 minutes",
            "Crew-legality violation rate near zero",
            "Customer-rebook acceptance > 85%",
        ),
        orchestration_archetype="arch.recovery.001",
        target_tenant_profile="Network airline with hub-and-spoke exposure",
    ),
    FusionMesh(
        mesh_id="mesh.th.commercial-yield",
        practice="th",
        name="Commercial Yield Mesh",
        description="Yield management + demand disruption + competitive watch fused for revenue-region optimization.",
        constituent_w2_service_codes=("TH-AIR-02",),
        composed_outcomes=(
            "Yield per ASM +3-5% network",
            "Corporate-contract retention sustained",
            "Demand-shock revenue protection sustained",
        ),
        orchestration_archetype="arch.optimize.001",
        target_tenant_profile="Network airline with corporate-contract base",
    ),
    FusionMesh(
        mesh_id="mesh.th.traveler-experience",
        practice="th",
        name="Traveler Experience Mesh",
        description="Traveler-360 + loyalty personalization + guest experience fused for elite-tier retention.",
        constituent_w2_service_codes=("TH-AIR-03", "TH-AIR-05"),
        composed_outcomes=(
            "Top-tier loyalty retention +5pp sustained",
            "Service-recovery offer engagement >85%",
            "F&B / ancillary capture +5-10% sustained",
        ),
        orchestration_archetype="arch.personalize.001",
        target_tenant_profile="Network airline with mature loyalty program",
    ),
    FusionMesh(
        mesh_id="mesh.th.ground-ops",
        practice="th",
        name="Ground Ops Mesh",
        description="Ground ops + baggage + crew composed for hub-station turn-time optimization.",
        constituent_w2_service_codes=("TH-AIR-04", "TH-AIR-07"),
        composed_outcomes=(
            "D0 +5pp network-wide",
            "Baggage mishandle rate -30% sustained",
            "Late-arrival cascade events -50%",
        ),
        orchestration_archetype="arch.predict.002",
        target_tenant_profile="Network airline with hub-station turn-time exposure",
    ),
    FusionMesh(
        mesh_id="mesh.th.hotel-rm",
        practice="th",
        name="Hotel Revenue Management Mesh",
        description="Hotel RM + guest sentiment + loyalty composed for property-level RevPAR optimization.",
        constituent_w2_service_codes=("TH-HOT-01", "TH-HOT-02"),
        composed_outcomes=(
            "RevPAR uplift on instrumented properties",
            "Direct-booking share +15pp sustained",
            "Member-rate take-rate +25pp sustained",
        ),
        orchestration_archetype="arch.optimize.001",
        target_tenant_profile="Hotel chain with mature revenue-management discipline",
    ),

    # ----- ICE (5) -----
    FusionMesh(
        mesh_id="mesh.ice.connected-product-economics",
        practice="ice",
        name="Connected-Product Economics Mesh",
        description="Connected-product analytics + warranty + service-aftermarket fused for IoT product P&L.",
        constituent_w2_service_codes=(),
        composed_outcomes=(
            "Field-warranty PPM -50% sustained",
            "Service revenue from telemetry +30% sustained",
            "Asset MTBF +50% sustained",
        ),
        orchestration_archetype="arch.predict.002",
        target_tenant_profile="Industrial OEM with connected installed base",
    ),
    FusionMesh(
        mesh_id="mesh.ice.dealer-channel",
        practice="ice",
        name="Dealer Channel Mesh",
        description="Dealer management + parts replenishment + field dispatch fused for channel-CSAT uplift.",
        constituent_w2_service_codes=(),
        composed_outcomes=(
            "Parts-fill rate ≥ 95% sustained",
            "First-time-fix rate ≥ 85% sustained",
            "Dealer-CSAT top-quartile",
        ),
        orchestration_archetype="arch.optimize.004",
        target_tenant_profile="OEM with multi-region dealer network",
    ),
    FusionMesh(
        mesh_id="mesh.ice.service-aftermarket",
        practice="ice",
        name="Service Aftermarket Mesh",
        description="Field dispatch + parts allocation + warranty composed for service-business margin.",
        constituent_w2_service_codes=(),
        composed_outcomes=(
            "Service margin uplift on instrumented product families",
            "Truck-rolls per fix -25% sustained",
            "Warranty-cost-of-service alignment with revenue",
        ),
        orchestration_archetype="arch.schedule.002",
        target_tenant_profile="OEM with mature service operation",
    ),
    FusionMesh(
        mesh_id="mesh.ice.operator-coaching",
        practice="ice",
        name="Operator Coaching Mesh",
        description="Operator coaching + safety + telemetry composed for workforce-productivity uplift.",
        constituent_w2_service_codes=(),
        composed_outcomes=(
            "Operator productivity +15-25pp sustained",
            "Workforce-safety incident rate sustained reduction",
            "Time-to-competence for new operators -40%",
        ),
        orchestration_archetype="arch.summarize.001",
        target_tenant_profile="Industrial operator with workforce-development pressure",
    ),
    FusionMesh(
        mesh_id="mesh.ice.quality-program",
        practice="ice",
        name="Quality Program Mesh",
        description="Quality program + supplier quality + warranty composed for end-to-end PPM reduction.",
        constituent_w2_service_codes=(),
        composed_outcomes=(
            "Field-defect PPM -50% sustained",
            "Supplier corrective-action throughput +2x",
            "Predictive-quality at NPI design boundary",
        ),
        orchestration_archetype="arch.rca.002",
        target_tenant_profile="ICE OEM with multi-supplier estate",
    ),
)


# Sprint 28 §28.3.1 mandates 5-8 meshes per Practice (target 35-56 total).
assert 35 <= len(CATALOG) <= 56, (
    f"Sprint 28 §28.3.1 mandates 35-56 meshes total, got {len(CATALOG)}"
)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def all_meshes() -> tuple[FusionMesh, ...]:
    return CATALOG


def get_mesh(mesh_id: str) -> FusionMesh | None:
    for m in CATALOG:
        if m.mesh_id == mesh_id:
            return m
    return None


def meshes_by_practice(practice: str) -> tuple[FusionMesh, ...]:
    return tuple(m for m in CATALOG if m.practice == practice.lower())


def mesh_by_w2_service_code(service_code: str) -> tuple[FusionMesh, ...]:
    """Wave-3 fusion meshes that include the named Wave-2 scenario.

    Powers Sprint 28 §28.3.6 cross-link — every featured scenario's
    Wave-3 ribbon points to the meshes it participates in.
    """
    return tuple(
        m for m in CATALOG
        if service_code in m.constituent_w2_service_codes
    )


def per_practice_counts() -> dict[str, int]:
    """How many meshes per Practice — for governance reporting."""
    out: dict[str, int] = {}
    for m in CATALOG:
        out[m.practice] = out.get(m.practice, 0) + 1
    return out
