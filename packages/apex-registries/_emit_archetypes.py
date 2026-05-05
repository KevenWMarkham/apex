"""Emit Appendix D — 47 orchestration archetypes."""
import yaml
from pathlib import Path

OUT = Path(__file__).parent / "src" / "apex_registries" / "archetypes"
OUT.mkdir(parents=True, exist_ok=True)

# (id_suffix, family, name, description, inputs, outputs, hitl_gate, oversight, model_tier, example_agents)
ARCHETYPES = [
    # Triage family (5)
    ("triage.001", "triage", "Event-Cluster Triage", "Group inbound events into similarity clusters and rank by impact.", ["EventStream","SeverityRubric"], ["RankedClusters"], "Cluster acceptance > N events", "HITL", "standard", ["apex.er.agents.outage-triage"]),
    ("triage.002", "triage", "Document Triage", "Classify inbound documents (claims, denials, support tickets) by recoverable value × probability of resolution.", ["DocumentBatch","RoutingPolicy"], ["TriageList"], "Top-of-queue dispatch", "HOTL", "standard", ["apex.hls.agents.claim-triage"]),
    ("triage.003", "triage", "Alert Triage", "Reduce alert volume via signal-quality scoring and drop low-precision alerts.", ["AlertStream","HistoricalNoiseModel"], ["FilteredAlerts"], "False-positive review", "HOTL", "lightweight", []),
    ("triage.004", "triage", "Severity-Cascade Triage", "Cascade severity: route routine to automation, escalate complex to specialist queues.", ["EventStream"], ["RoutingDecisions"], "Specialist queue handoff", "HITL", "standard", []),
    ("triage.005", "triage", "Disposition Triage", "Recommend disposition action (sell/markdown/donate/destroy etc.) per item.", ["ItemBatch","ShelfLifeModel","PolicyRules"], ["DispositionPlan"], "Manager approves disposition", "HITL", "standard", ["apex.rc.agents.cold-chain-response"]),
    # Cascade family (3)
    ("cascade.001", "cascade", "Notification Cascade", "Fan out notifications across channels with channel-aware formatting and acknowledgment tracking.", ["Event","RecipientList"], ["DeliveryReceipts"], "Send to broad audience > N", "HOTL", "lightweight", ["apex.th.agents.disruption-comms"]),
    ("cascade.002", "cascade", "Workflow Cascade", "Trigger downstream workflows in dependency order with retry / compensate.", ["WorkflowGraph","TriggerEvent"], ["ExecutionTrace"], "Compensation flow fires", "HITL", "standard", []),
    ("cascade.003", "cascade", "Approval Cascade", "Multi-step approval routing with parallel and sequential gates per policy.", ["ApprovalRequest","Policy"], ["ApprovalDecision"], "Final approver", "HITL", "lightweight", []),
    # RCA family (4)
    ("rca.001", "rca", "Anomaly Root-Cause", "Hypothesize root cause from telemetry signature + change correlation.", ["TelemetryWindow","ChangeLog"], ["RootCauseHypotheses"], "Engineer reviews hypotheses", "HITL", "reasoning", ["apex.axle.agents.andon-rca"]),
    ("rca.002", "rca", "Defect-Cluster Root-Cause", "Cluster defects + correlate with supplier lots / process windows / shift boundaries.", ["DefectStream","GenealogyData"], ["RCAReport"], "Quality engineer", "HITL", "standard", ["apex.axle.agents.quality-defect"]),
    ("rca.003", "rca", "Incident Post-Mortem", "Generate structured post-mortem from incident timeline + remediation candidates.", ["IncidentTimeline"], ["PostMortemDraft"], "SRE / IM lead review", "HITL", "reasoning", []),
    ("rca.004", "rca", "Billing Anomaly RCA", "Find root cause of customer-billing anomalies and propose remediation playbook.", ["BillExceptions","CIShistory"], ["RCAReport","Playbook"], "Customer-care HITL", "HITL", "standard", ["apex.er.agents.ami-billing-anomaly"]),
    # Recovery family (3)
    ("recovery.001", "recovery", "IROPS Recovery", "Generate integrated recovery plan across operations, crew, customer simultaneously.", ["DisruptionEvent","NetworkState"], ["RecoveryPlan"], "Duty manager approves plan", "HITL", "reasoning", ["apex.th.agents.irops-recovery"]),
    ("recovery.002", "recovery", "Outage Restoration", "Sequence restoration crews against critical-load + safety + crew-fatigue constraints.", ["OutageMap","CrewState","CriticalLoadMap"], ["DispatchPlan"], "Dispatcher approves blocks", "HITL", "reasoning", ["apex.er.agents.restoration-sequencing"]),
    ("recovery.003", "recovery", "Service Recovery", "Compose customer service-recovery offers from prior preferences + tier value.", ["ServiceEvent","TravelerProfile"], ["RecoveryOfferSet"], "CSR approves offer", "HITL", "standard", ["apex.th.agents.loyalty-personalization"]),
    # Personalize family (3)
    ("personalize.001", "personalize", "Next-Best-Offer", "Score next-best offer from history + propensity + inventory.", ["CustomerProfile","OfferCatalog"], ["RankedOffers"], "Margin / brand guardrail", "HOTL", "standard", ["apex.rc.agents.substitution-recommendation"]),
    ("personalize.002", "personalize", "Content Personalization", "Tailor content surface (web/app/email) per traveler/customer profile.", ["CustomerProfile","ContentLibrary"], ["PersonalizedSurface"], "Brand review on creative", "HOTL", "lightweight", []),
    ("personalize.003", "personalize", "Substitution Recommendation", "Pre-stage alternates for at-risk SKUs / inventory gaps.", ["DemandSignal","InventoryState"], ["SubstitutionPlan"], "Category manager", "HOTL", "standard", ["apex.rc.agents.substitution-recommendation"]),
    # Optimize family (4)
    ("optimize.001", "optimize", "Price Optimization", "Compute elastic-demand price given competitive + capacity + objective.", ["PriceCurves","Constraints"], ["PriceAction"], "Magnitude > threshold", "HITL", "standard", ["apex.th.agents.yield-management"]),
    ("optimize.002", "optimize", "Schedule Optimization", "Re-sequence production / crew / aircraft against constraint events.", ["Schedule","ConstraintEvent"], ["RevisedSchedule"], "Planner approves", "HITL", "reasoning", ["apex.axle.agents.production-scheduling"]),
    ("optimize.003", "optimize", "Energy Load-Shift", "Shift load to lower-cost windows under stability constraints.", ["TariffFeed","LoadProfile"], ["LoadShiftPlan"], "Operator approves aggregate", "HITL", "standard", ["apex.axle.agents.energy-optimization"]),
    ("optimize.004", "optimize", "Replenishment Optimization", "Replenish against demand signal + DC capacity + safety stock.", ["DemandForecast","InventoryState"], ["ReplenishmentOrders"], "Planner approves", "HITL", "standard", ["apex.rc.agents.inventory-replenishment"]),
    # Monitor family (3)
    ("monitor.001", "monitor", "OEE / KPI Monitor", "Decompose KPI into drivers + flag attribution.", ["TelemetryStream","KPIMap"], ["DriverDecomposition"], "Plant manager digest", "HOTL", "lightweight", ["apex.axle.agents.oee-monitor"]),
    ("monitor.002", "monitor", "Threshold Monitor", "Continuous threshold check with hysteresis + suppression.", ["MetricStream","Thresholds"], ["AlertEvents"], "Threshold breach", "HOTL", "lightweight", []),
    ("monitor.003", "monitor", "Compliance Monitor", "Verify ongoing compliance against policy bundle, surface drift.", ["PolicyBundle","ActivityLog"], ["DriftReport"], "Compliance officer", "HITL", "lightweight", []),
    # Predict family (3)
    ("predict.001", "predict", "Demand Sensing", "Multi-horizon demand forecast with weather/event overrides.", ["HistoricalSales","ExogenousFactors"], ["DemandForecast"], "Planner accepts forecast", "HOTL", "standard", ["apex.rc.agents.demand-sensing"]),
    ("predict.002", "predict", "Predictive Maintenance", "Equipment-failure score + recommended action.", ["VibrationSpectrum","ThermalProfile","CurrentDraw"], ["FailureScore","Action"], "Maintenance planner", "HITL", "standard", ["apex.axle.agents.predictive-maintenance"]),
    ("predict.003", "predict", "Risk Prediction", "Patient / customer / outage risk model with explanation.", ["FeatureSet"], ["RiskScore","Explanation"], "Clinician / case manager", "HITL", "standard", ["apex.hls.agents.readmission-risk","apex.hls.agents.sepsis-early-warning"]),
    # Schedule family (2)
    ("schedule.001", "schedule", "Crew Scheduling", "Crew-legality-aware rebooking under disruption.", ["CrewPool","Disruption"], ["RebookPlan"], "Crew Ops approves", "HITL", "reasoning", ["apex.th.agents.crew-scheduling"]),
    ("schedule.002", "schedule", "Workforce Scheduling", "Forecast-driven shift planning with skill-mix constraints.", ["DemandForecast","SkillMatrix"], ["Schedule"], "WFM manager", "HITL", "standard", []),
    # Match family (3)
    ("match.001", "match", "Identity Resolution", "Cross-system identity resolution with HITL gate on conflicts.", ["RecordSet","MatchRules"], ["IdentityMap"], "HIM / data-steward", "HITL", "standard", ["apex.hls.agents.patient-identity","apex.rc.agents.customer-identity"]),
    ("match.002", "match", "Lot / Trace Match", "Match lot genealogy across upstream-downstream movements.", ["LotMovements"], ["TraceGraph"], "QA traceability sign-off", "HITL", "standard", []),
    ("match.003", "match", "Adverse-Event Match", "Match adverse-event signals against drug / device cohorts.", ["AESignals","ProductCohort"], ["MatchedEvents"], "Pharmacovigilance review", "HITL", "standard", ["apex.hls.agents.adverse-event"]),
    # Translate family (3)
    ("translate.001", "translate", "Format Translator", "Translate between message formats (HL7v2 to FHIR, EDI to JSON, etc.).", ["SourceMessage","TargetFormat"], ["TargetMessage"], "Sample-quality review", "HOTL", "lightweight", []),
    ("translate.002", "translate", "Standard Translator", "Map cross-standard equivalents (ICD-10 to SNOMED, NDC to RxNorm).", ["SourceCode","Mapping"], ["TargetCode"], "Coding compliance", "HOTL", "lightweight", []),
    ("translate.003", "translate", "Protocol Adapter", "Adapt protocol layers (REST to gRPC, MQTT to AMQP).", ["SourcePayload"], ["TargetPayload"], "API gateway gate", "HOTL", "lightweight", []),
    # Summarize family (2)
    ("summarize.001", "summarize", "Operational Digest", "Daily/shift digest with prioritized actions.", ["MultiSourceSignals"], ["DigestNarrative"], "Recipient acknowledges", "HOTL", "standard", ["apex.rc.agents.store-ops-intelligence"]),
    ("summarize.002", "summarize", "Investigation Summary", "Summarize incident or audit investigation evidence.", ["EvidenceBundle"], ["SummaryDoc"], "Auditor / counsel review", "HITL", "reasoning", []),
    # Explain family (2)
    ("explain.001", "explain", "Decision Explanation", "Generate plain-language explanation of agent decision with feature attribution.", ["Decision","FeatureSet"], ["Explanation"], "User requests rationale", "HOTL", "standard", []),
    ("explain.002", "explain", "Regulatory Explanation", "Produce regulator-defensible reasoning trace for high-stakes decision.", ["Decision","ReasoningChain"], ["RegulatoryNarrative"], "Counsel review", "HITL", "reasoning", ["apex.er.agents.psps-decision"]),
    # Score family (2)
    ("score.001", "score", "Risk Score", "Compute composite risk score with band-based action.", ["FeatureSet","ScoringModel"], ["Score","Band"], "Action band crossed", "HITL", "standard", []),
    ("score.002", "score", "Quality Score", "Quality / yield / health score with attribution.", ["MeasurementSet"], ["Score","Drivers"], "Score-out-of-spec", "HOTL", "standard", []),
    # Negotiate family (2)
    ("negotiate.001", "negotiate", "Contract Negotiation Support", "Support negotiation with comparables + concession analysis.", ["DealContext","Comparables"], ["NegotiationGuide"], "Deal team review", "HITL", "reasoning", []),
    ("negotiate.002", "negotiate", "Supplier Negotiation Support", "Support supplier negotiation on pricing / SLAs / corrective action.", ["SupplierHistory","BenchmarkData"], ["NegotiationPosition"], "Procurement HITL", "HITL", "standard", ["apex.axle.agents.supplier-quality"]),
    # Compose family (2)
    ("compose.001", "compose", "Plan Composition", "Compose multi-step plan from sub-agent capabilities.", ["Goal","CapabilityCatalog"], ["Plan"], "Plan complexity > threshold", "HITL", "reasoning", []),
    ("compose.002", "compose", "Document Composition", "Compose proposal / report / brief from canonical components.", ["ContentBlocks","Template"], ["Document"], "Sign-off authority", "HITL", "standard", []),
    # Catch-all to round out 47
    ("monitor.004", "monitor", "Drift Monitor", "Detect data / model drift across deployed agents.", ["EvalStream","ReferenceDistribution"], ["DriftSignal"], "Drift exceeds tolerance", "HITL", "standard", []),
]

assert len(ARCHETYPES) == 47, f"Expected 47, got {len(ARCHETYPES)}"

count = 0
for arch_id, family, name, description, inputs, outputs, gate, oversight, tier, examples in ARCHETYPES:
    data = dict(
        kind="archetype",
        archetype_id=f"arch.{arch_id}",
        family=family,
        name=name,
        description=description,
        canonical_inputs=inputs,
        canonical_outputs=outputs,
        typical_hitl_gate=gate,
        typical_oversight=oversight,
        typical_model_tier=tier,
        example_agents=examples,
        appendix_d_section=f"Appendix D — Archetype family {family}",
    )
    fname = f"{arch_id.replace('.', '-')}.yaml"
    path = OUT / fname
    with path.open("w", encoding="utf-8") as fh:
        fh.write("# harvest:auto-generated — apex_registries.harvest\n")
        yaml.safe_dump(data, fh, sort_keys=False, default_flow_style=False, allow_unicode=True)
    count += 1
print(f"Archetypes written: {count}")
