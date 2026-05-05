"""Emit Appendices G (products), H (partners), K (competitive), J (exercises)."""
import yaml
from pathlib import Path

ROOT = Path(__file__).parent / "src" / "apex_registries"


def write(folder: str, fname: str, data: dict) -> None:
    p = ROOT / folder / fname
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as fh:
        fh.write("# harvest:auto-generated — apex_registries.harvest\n")
        yaml.safe_dump(data, fh, sort_keys=False, default_flow_style=False, allow_unicode=True)


# Appendix G — Microsoft products & SKUs
PRODUCTS = [
    # Fabric
    ("ms.fabric.f64",     "fabric",         "Microsoft Fabric F64 Capacity",  "F64",  "Reserved Fabric capacity (~32 vcores). Entry-level production deployments and small-Practice anchors.", "reserved-capacity-monthly", "Single-Practice prod tenant", "Sprint 14 single-capacity-tenant default"),
    ("ms.fabric.f128",    "fabric",         "Microsoft Fabric F128 Capacity", "F128", "Reserved Fabric capacity (~64 vcores). Standard for reference-deployment Wave-1.", "reserved-capacity-monthly", "Reference deployments + medium prod", "Sprint 18 reference-deployment default"),
    ("ms.fabric.f256",    "fabric",         "Microsoft Fabric F256 Capacity", "F256", "Reserved Fabric capacity for large multi-Practice tenants.", "reserved-capacity-monthly", "Multi-Practice prod", "Sprint 14 per-workload-isolation"),
    ("ms.fabric.f512",    "fabric",         "Microsoft Fabric F512 Capacity", "F512", "Top-tier Fabric reserved capacity.", "reserved-capacity-monthly", "Enterprise multi-tenant prod", "Sprint 14 large-enterprise"),
    ("ms.fabric.mirroring","fabric",        "Microsoft Fabric Mirroring",     "feature","Real-time CDC ingest from supported SOR databases.", "no-additional-cost-with-fabric", "Bronze ingestion", "Sprint 15 adapter primary path"),
    ("ms.fabric.realtime","fabric",         "Microsoft Fabric Real-Time Intelligence", "RTI", "Streaming-first ingestion + KQL-based analysis.", "consumption", "Telemetry pipelines", "Sprint 15 streaming adapters"),
    # Foundry
    ("ms.foundry.gpt4o",         "foundry", "Azure AI Foundry — GPT-4o",      "gpt-4o-2024-11-20", "Standard-tier reasoning + multimodal model.", "consumption-tokens", "Most agent reasoning", "Sprint 16 ModelTier.STANDARD default pin"),
    ("ms.foundry.gpt4o-mini",    "foundry", "Azure AI Foundry — GPT-4o-mini", "gpt-4o-mini-2024-07-18", "Lightweight model for classification + simple summarization.", "consumption-tokens", "High-volume routine tasks", "Sprint 16 ModelTier.LIGHTWEIGHT default pin"),
    ("ms.foundry.o1",            "foundry", "Azure AI Foundry — o1",          "o1-2024-12-17", "Reasoning-tier model for multi-step planning + elasticity.", "consumption-tokens", "PSPS, IROPS, complex orchestration", "Sprint 16 ModelTier.REASONING default pin"),
    ("ms.foundry.embeddings",    "foundry", "Azure AI Foundry — text-embedding-3-large", "text-embedding-3-large", "Embeddings for retrieval + clustering.", "consumption-tokens", "RAG + semantic search", "Sprint 16 retrieval pipelines"),
    # Copilot Studio
    ("ms.copilot-studio.std",  "copilot-studio", "Copilot Studio — Standard", "messages-pack", "Low-code copilot authoring + Teams surface.", "messages-bundle", "HITL surface for agents", "Sprint 16 default surface for Teams cards"),
    ("ms.copilot-studio.kit",  "copilot-studio", "Copilot Studio — Agent Builder Kit", "feature", "Programmatic agent builder + tool bindings.", "messages-bundle", "Custom agent surfaces", "Sprint 16 advanced surfaces"),
    # Purview
    ("ms.purview.std",        "purview", "Microsoft Purview — Data Map + Catalog", "standard", "Discovery, classification, lineage across Fabric.", "consumption", "Governance baseline", "Sprint 13 governance foundation"),
    ("ms.purview.compliance", "purview", "Microsoft Purview — Compliance Manager","add-on",   "Policy assessment + DLP authoring.", "per-user/month", "Compliance teams", "Sprint 13 DLP authoring"),
    ("ms.purview.audit",      "purview", "Microsoft Purview — Audit Premium",      "premium",  "Long-retention audit log with crypto-preservation.", "per-user/month", "Regulator-grade audit", "Sprint 18 PSPS / SEP-1 audit retention"),
    # Defender
    ("ms.defender.cloud",        "defender", "Microsoft Defender for Cloud",  "P2",       "CSPM + CWPP across Azure resources.", "per-resource/month", "Posture mgmt for Fabric/Foundry", "Sprint 13 posture telemetry"),
    ("ms.defender.endpoint",     "defender", "Microsoft Defender for Endpoint","P2",      "EDR for engagement laptops.", "per-user/month", "Workforce endpoint protection", "Engagement perimeter"),
    # Entra
    ("ms.entra.id-p2",           "entra",    "Microsoft Entra ID — P2",       "P2",       "Conditional Access + PIM + Identity Protection.", "per-user/month", "Engagement IAM baseline", "Sprint 13 IAM baseline"),
    ("ms.entra.workload-id",     "entra",    "Microsoft Entra Workload Identities", "feature", "Service-principal / managed-identity governance.", "per-identity/month", "Agent workload identity", "Sprint 16 agent identity"),
    # Intune
    ("ms.intune.suite",          "intune",   "Microsoft Intune Suite",        "suite",    "MDM/MAM + endpoint privilege management.", "per-user/month", "Workforce device mgmt", "Engagement perimeter"),
    # Teams
    ("ms.teams.premium",         "teams",    "Microsoft Teams Premium",       "premium",  "Advanced meeting + intelligent recap + watermarking.", "per-user/month", "HITL Teams-card surfaces with rich approval flows", "Sprint 16 HITL surfaces"),
    # Power Platform
    ("ms.power.platform.std",    "power-platform", "Power Platform — Standard","standard", "Power Apps + Power Automate.", "per-user/month", "Edge automations + custom HITL UIs", "Sprint 16 custom surfaces"),
    # Azure OpenAI (legacy alongside Foundry; some clients still on direct AOAI)
    ("ms.azure-openai.gpt4o",    "azure-openai", "Azure OpenAI Service — GPT-4o", "gpt-4o", "Direct Azure OpenAI deployment for clients not on Foundry.", "consumption-tokens", "Legacy / non-Foundry deployments", "Fallback to Sprint 16 reasoning"),
    # Azure ML
    ("ms.azure-ml.workspace",    "azure-ml", "Azure ML — Workspace",          "workspace","ML model training + registry + deployment.", "consumption", "Model lifecycle for tabular models", "Sprint 16 supplemental model registry"),
    # GitHub Copilot
    ("ms.gh.copilot.business",   "github-copilot", "GitHub Copilot Business", "business", "Engineer productivity for build+adapter+package work.", "per-user/month", "Engagement engineering team", "Sprint 14/15 build velocity"),
    # Azure Storage / Network
    ("ms.azure.storage.adls",    "azure-storage", "Azure Data Lake Storage Gen2", "ADLS Gen2", "Underlying storage for Fabric workspaces.", "consumption", "Bronze/Silver/Gold storage", "Sprint 14 capacity backbone"),
    ("ms.azure.network.private", "azure-network","Azure Private Endpoints + Private Link", "feature", "Network isolation for Fabric / Foundry / Purview.", "per-endpoint/month", "Regulated workload network isolation", "Sprint 14 isolation pattern"),
]
for pid, family, display, sku, desc, basis, use, role in PRODUCTS:
    data = dict(
        kind="product", product_id=pid, family=family,
        display_name=display, sku_or_tier=sku, description=desc,
        list_price_basis=basis, typical_use=use, apex_role=role,
        appendix_g_section=f"Appendix G — {family}",
    )
    write("products", f"{pid.replace('.', '-')}.yaml", data)

# Appendix H — Partners
PARTNERS = [
    ("ptr.sap",         "SAP",                "sor-vendor",     ["rc","axle","er","ice"], "ERP backbone for finance, supply chain, manufacturing.", "mirrored-db-via-Sprint15-adapter", ["Master agreement"]),
    ("ptr.oracle",      "Oracle",             "sor-vendor",     ["rc","hls","er"],         "ERP / HCM / database.",                                  "mirrored-db-via-Sprint15-adapter", []),
    ("ptr.salesforce",  "Salesforce",         "sor-vendor",     ["rc","hls","tmt","th","ice"], "CRM + Marketing Cloud + Service Cloud.",            "API-via-Sprint15-adapter",         ["Co-sell"]),
    ("ptr.epic",        "Epic",               "sor-vendor",     ["hls"],                   "EHR / health-system core SOR.",                          "Clarity-mirroring-via-Sprint15",   ["Pre-cleared deployment posture"]),
    ("ptr.workday",     "Workday",            "sor-vendor",     ["hls","th","tmt","rc","axle"], "HCM / Financials.",                                "Mirroring-via-Sprint15",           []),
    ("ptr.servicenow",  "ServiceNow",         "sor-vendor",     ["hls","er","tmt","th","rc","axle","ice"], "ITSM / workflow.",                          "API-via-Sprint15-adapter",         []),
    ("ptr.sabre",       "Sabre",              "sor-vendor",     ["th"],                    "GDS + airline DCS / PSS.",                                "API-via-Sprint15-adapter",         []),
    ("ptr.amadeus",     "Amadeus",            "sor-vendor",     ["th"],                    "GDS + airline DCS / PSS.",                                "API-via-Sprint15-adapter",         []),
    ("ptr.ge-digital",  "GE Digital (Proficy)","sor-vendor",    ["axle","er"],             "Industrial historian / MES.",                             "Mirroring-via-Sprint15",           []),
    ("ptr.osisoft",     "OSIsoft / AVEVA (PI)","sor-vendor",    ["axle","er","ice"],       "Industrial historian.",                                   "PI-API-via-Sprint15-adapter",      []),
    ("ptr.manhattan",   "Manhattan Associates","sor-vendor",    ["rc"],                    "WMS.",                                                    "Mirroring-via-Sprint15",           []),
    ("ptr.snowflake",   "Snowflake",          "sor-vendor",     ["rc","hls","th","tmt","ice"], "Cloud warehouse (read-mirror to Fabric).",          "Mirroring-via-Sprint15",           []),
    ("ptr.databricks",  "Databricks",         "sor-vendor",     ["rc","axle","er","th","tmt","ice","hls"], "Lakehouse (read-mirror to Fabric).",     "Mirroring-via-Sprint15",           []),
    ("ptr.openai",      "OpenAI",             "model-provider", ["cross"],                 "Reasoning-tier and standard models via Azure AI Foundry.",  "Foundry-pinned-deployment",        []),
    ("ptr.anthropic",   "Anthropic",          "model-provider", ["cross"],                 "Claude family models for reasoning + standard agents.",     "Foundry-pinned-deployment-or-AWS-Bedrock-via-bridge", []),
    ("ptr.dunhumby",    "dunnhumby",          "data-provider",  ["rc"],                    "Customer-data-science + retail loyalty insights.",          "Co-delivery-on-pilot",             []),
    ("ptr.veeva",       "Veeva",              "isv",            ["hls"],                   "Life-sciences CRM / clinical / regulatory.",                "API-via-Sprint15-adapter",         []),
    ("ptr.aws",         "Amazon Web Services","infrastructure", ["cross"],                 "Some clients dual-clouded; bridges supported but not encouraged.", "Bridge-only", []),
    ("ptr.gcp",         "Google Cloud",       "infrastructure", ["cross"],                 "Same posture as AWS.",                                       "Bridge-only",                      []),
    ("ptr.deloitte-iv",  "Deloitte In-Vehicle Practice", "delivery-partner", ["axle","ice"], "Sister Deloitte practice for vehicle / aftermarket plays.", "Co-staffing", ["Practice MoU"]),
]
for pid, name, category, practices, desc, pattern, contracts in PARTNERS:
    data = dict(
        kind="partner", partner_id=pid, name=name, category=category,
        practices=practices, description=desc,
        apex_integration_pattern=pattern,
        contracts_in_place=contracts,
        appendix_h_section=f"Appendix H — {category}",
    )
    write("partners", f"{pid.replace('.', '-')}.yaml", data)

# Appendix K — Competitive posture
COMPETITIVE = [
    ("comp.accenture-cfc", "Accenture", "Centre for Advanced AI + Industry-X stack",
        ["APEX is contract-shippable in 4-12 weeks vs. multi-quarter Centre engagements", "Independence-clean for Big-4-eligible clients", "Sprint 16 catalog + Sprint 18 references give pre-engagement evidence"],
        ["AICPA / SEC independence rules limit which client populations APEX can serve where Deloitte audits"],
        ["Faster time-to-value", "Compliance-grade audit posture out of the box", "Pre-built reference deployments per Practice"]),
    ("comp.ibm-watsonx", "IBM", "watsonx + Industry packs",
        ["APEX is Microsoft-native (Fabric / Foundry / Copilot Studio) vs. watsonx-on-OpenShift", "Pre-engagement Sprint 18 reference deployments are shippable",
         "Sprint 16 anchor agent catalog larger than watsonx out-of-the-box"],
        ["Clients with significant IBM mainframe estate may benefit from watsonx's CICS connectors"],
        ["Microsoft licensing leverage", "Faster Wave-1 commercial path"]),
    ("comp.capgemini-genai", "Capgemini", "AI Insights + sector-specific accelerators",
        ["APEX has named anchor agents per Practice with HITL gates baked in",
         "Sprint 17 service catalog provides commercially-priced productized services"],
        ["Capgemini is independence-clean for clients where Deloitte cannot serve"],
        ["Catalog depth", "Auditable HITL posture", "Microsoft strategic alignment"]),
    ("comp.bcg-x", "BCG", "BCG X / Gen-AI offerings",
        ["BCG plays consulting-led; APEX is package-led (shippable Python + Fabric infra + agents)",
         "APEX Sprint 18 references collapse 6-month BCG engagements into 8-12 week Wave-1 fixed-fee"],
        ["BCG independence-clean for Deloitte-audit clients"],
        ["Time-to-value", "Fixed-fee predictability", "Audit-grade artifacts"]),
    ("comp.mckinsey-quantumblack", "McKinsey", "QuantumBlack",
        ["McKinsey/QB plays bespoke; APEX is repeatable-blueprint",
         "APEX cross-Practice catalog covers more sector breadth than QB sector-by-sector consult"],
        ["McKinsey independence-clean for Deloitte-audit clients"],
        ["Repeatability", "Catalog breadth", "Microsoft licensing alignment"]),
    ("comp.pwc", "PwC", "PwC AI Factory",
        ["PwC is direct competitor (Big-4); APEX wins on Microsoft-native + Sprint 16/17/18 catalog depth"],
        ["Equivalent independence posture; competition is on capability, speed, price"],
        ["Pre-built catalogs", "Faster ramp", "Stronger Microsoft alignment"]),
    ("comp.kpmg", "KPMG", "KPMG Trusted AI",
        ["Similar Big-4 dynamics to PwC", "APEX Sprint 13 governance + Sprint 18 audit posture differentiates on regulator defensibility"],
        ["Equivalent independence posture"],
        ["Audit-grade traceability", "Regulator-defensible artifacts"]),
    ("comp.ey", "EY", "EY.ai platform",
        ["Similar Big-4 dynamics", "APEX Sprint 16 anchor agent count > EY.ai out-of-the-box library"],
        ["Equivalent independence posture"],
        ["Catalog depth", "Faster Wave-1 commercial path"]),
    ("comp.databricks-mosaic", "Databricks (Mosaic AI)", "Mosaic AI Agent Framework",
        ["APEX is Microsoft-native; Databricks Mosaic is Databricks-native", "APEX HITL/HOTL governance is more mature for regulated clients"],
        ["Clients deeply Databricks-invested may prefer Mosaic-native"],
        ["Microsoft alignment", "HITL governance maturity"]),
    ("comp.snowflake-cortex", "Snowflake (Cortex AI)", "Snowflake Cortex Agents",
        ["APEX is Microsoft-native; Cortex is Snowflake-native", "APEX cross-Practice catalog >> Cortex"],
        ["Snowflake-deep clients may have lock-in pull"],
        ["Microsoft alignment", "Catalog breadth", "HITL governance"]),
]
for cid, competitor, offering, diffs, indep, themes in COMPETITIVE:
    data = dict(
        kind="competitive", entry_id=cid,
        competitor=competitor, competitor_offering=offering,
        apex_differentiators=diffs,
        independence_concerns=indep,
        win_themes=themes,
        appendix_k_section="Appendix K — Independence and Competitive Posture",
    )
    write("competitive", f"{cid.replace('.', '-')}.yaml", data)

# Appendix J — Exercise solutions (10 exemplars)
EXERCISES = [
    ("ex.10.3.a",  "§10.3", "10. Healthcare Practice",
        "Identify the three highest-value HITL gates in a Wave-1 hospital deployment.",
        "Sepsis early warning escalation (charge nurse), claim-triage rework (revenue cycle specialist), patient-identity duplicate-MRN (HIM steward). Each emits an audit row with PHI redaction.",
        ["HITL placement is at consequential decisions, not all writes", "Audit row is mandatory at every HITL gate"],
        ["kpi.hls.sep-1-bundle-compliance"], ["arch.recovery.001","arch.match.001"]),
    ("ex.10.5.b", "§10.5", "10. Healthcare Practice",
        "Explain why HLS-PAY-01 is value-share-eligible but HLS-E2E-01 is fixed-fee.",
        "HLS-PAY-01 attaches money-direction KPIs (recovered AR) where attribution is clean (837/835 cycle). HLS-E2E-01 sepsis early warning is fixed-fee because clinical attribution is multi-causal and not contractually attributable.",
        ["Value-share requires clean money attribution", "Clinical-outcome attribution is multi-causal"],
        ["kpi.hls.first-pass-denial-rate"], ["arch.score.001"]),
    ("ex.11.4.a", "§11.4", "11. Energy & Resources Practice",
        "Walk through a PSPS decision audit row.",
        "Audit row pins: model version, weather-data provenance + timestamp, fuel-moisture provider + reading time, vegetation-risk last-cycle data, decision-maker UPN, decision timestamp, segments included, segments excluded, justification narrative, customer-notification window.",
        ["Regulator-defensible audit requires every input timestamp + provenance", "Decision and decision-maker are both in-row"],
        ["kpi.er.psps-decision-audit-completeness"], ["arch.explain.002"]),
    ("ex.12.2.a", "§12.2", "12. Industrial / Manufacturing Practice",
        "Decompose an OEE shortfall using the Sprint 16 OEE monitor agent.",
        "Decompose into Availability × Performance × Quality. Drivers below target each get a confidence-scored hypothesis (e.g., changeover #4 SMED candidate). Andon-RCA agent correlates with prior incidents.",
        ["OEE = A × P × Q", "Decomposition surfaces confidence-scored levers"],
        ["kpi.axle.oee"], ["arch.monitor.001","arch.rca.001"]),
    ("ex.13.6.a", "§13.6", "13. Telecom / Media / Tech Practice",
        "Map IVT (invalid-traffic) detection to its commercial model.",
        "IVT detection is value-share-eligible: cleanly attributable to recovered ad-spend / refund avoidance. ContentSafetyML schema family + apex.tmt.agents — IVT detection writes audit row tied to settlement.",
        ["IVT money-attribution is clean", "ContentSafetyML schema captures the decision evidence"],
        ["kpi.tmt.ivt-rate"], ["arch.score.001"]),
    ("ex.14.4.a", "§14.4", "14. Travel / Hospitality Practice",
        "Sequence an IROPS recovery plan composition.",
        "1. Reasoning-tier IROPS agent fuses flight legs, crew legality, aircraft, gate, customer rebook. 2. Crew-scheduling agent layered for legality-aware swaps. 3. Disruption-comms cascades messages. HITL is duty-manager approve.",
        ["Reasoning-tier model justifies cost via recovery-time savings", "Three sub-agents compose; one HITL"],
        ["kpi.th.irops-recovery-cycle-time"], ["arch.recovery.001","arch.cascade.001"]),
    ("ex.15.3.a", "§15.3", "15. Industrial Connected Electronics Practice",
        "Why does ICE Wave-1 typically run F128 single-tenant rather than per-workload-isolation?",
        "ICE Wave-1 telemetry estate is typically homogeneous (single OEM device family), so the OT/IT isolation overhead of per-workload doesn't pay off. Multi-OEM Wave-2 may justify isolation.",
        ["Capacity choice follows estate complexity, not always max-isolation"],
        [], []),
    ("ex.16.7.a", "§16.7", "16. Retail / Consumer Practice",
        "Map cold-chain agent decision to FSMA 204 audit obligations.",
        "Cold-chain response writes the disposition decision + lot trace to the audit row. SCML schema links the lot to inbound supplier movements. The audit row is FSMA 204 traceability-event compatible.",
        ["SCML schema designed against FSMA 204 traceability-event vocabulary","Audit row is the traceability event"],
        ["kpi.rc.cold-chain-disposition-decision-latency"], ["arch.triage.005"]),
    ("ex.2.6.a", "§2.6", "2. APEX Foundations",
        "When does a service ship as value-share vs. fixed-fee?",
        "Value-share when (a) the KPI is money-direction, (b) attribution is contractually clean, (c) Deloitte-independence rules permit. Fixed-fee otherwise.",
        ["Three conditions must all hold for value-share","Independence is gate, not preference"],
        [], []),
    ("ex.6.10.a", "§6.10", "6. Agent runtime",
        "What goes in an audit row?",
        "agent_name, agent_version, prompt_sha, model_pin, decision, decision_actor (HITL only), inputs_provenance, outputs_persisted_to, classification_at_emit, timestamp, replay_token.",
        ["Audit row is the contract artifact","Replay token enables forensic replay"],
        [], []),
]
for eid, section, chapter, prompt, solution, points, kpis, archs in EXERCISES:
    data = dict(
        kind="exercise", exercise_id=eid,
        sellers_guide_section=section, chapter=chapter,
        prompt=prompt, canonical_solution=solution,
        teaching_points=points,
        related_kpi_ids=kpis,
        related_archetype_ids=archs,
    )
    write("exercises", f"{eid.replace('.', '-')}.yaml", data)

print("Products:", len(PRODUCTS))
print("Partners:", len(PARTNERS))
print("Competitive:", len(COMPETITIVE))
print("Exercises:", len(EXERCISES))
