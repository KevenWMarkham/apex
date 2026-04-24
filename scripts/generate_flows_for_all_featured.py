"""Generate APEX_FLOW_DATA entries for all 35 featured scenarios.

The existing narrated HTML has flow data for ONE scenario
(rc-cold-chain-excursion). This script generates flow graphs for the
remaining 34 featured chains, using a templated 24-node pattern
(10 W1 Foundation · 8 W2 Pilot · 6 W3 Scale & Fuse) and pulling text
from each chain's authored Scenario / Solution / Use Case / Service /
Persona / KPI fields.

For each of the 35 featured scenarios:
  1. Derive flow-key: <practice-lower>-<slug>
  2. Emit 24 nodes with scenario-specific:
     - SOR choice + telemetry description (by domain)
     - Silver canonical entities (by domain)
     - W2 event / agent / HITL / outcome descriptions (from chain text)
     - W3 fusion partners + enterprise KPI (from chain + siblings)
  3. Inject into APEX_FLOW_DATA
  4. Update ID_TO_FLOW_KEY to map all 35 scenario IDs

Idempotent: keeps the original rc-cold-chain-excursion entry; for the
other 34, overwrites any prior auto-generated entry.
"""

from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HTML = Path("docs/reference/APEX-Stacked-Architecture-Narrated.html")
CHAINS = Path("docs/scenarios/_catalog/featured-chains.json")

html = HTML.read_text(encoding="utf-8")
chains = json.load(open(CHAINS, encoding="utf-8"))

# ---- 1. Build scenario-ID lookup (same logic used elsewhere) ---------------

PRACTICES = ["RC", "HLS", "ER", "AXLE", "TMT", "TH", "ICE"]
DOMAIN_CODES = {
    "clinical-care": "CLIN", "network-infrastructure": "NET", "engineering-rd": "ENG",
    "supply-chain": "SUPCHN", "asset-maintenance": "ASSET", "quality-compliance": "QUAL",
    "risk-fraud-security": "RISK", "pricing-revenue": "PRICE", "customer-experience": "CX",
    "marketing-growth": "MKTG", "operations-workforce": "OPS", "channel-partner-dealer": "CHAN",
    "other": "OTHER",
}

SCEN_ROOT = Path("docs/scenarios")
title_to_id: dict[tuple[str, str], str] = {}
for p in PRACTICES:
    pdir = SCEN_ROOT / p
    if not pdir.exists():
        continue
    for dom in pdir.iterdir():
        if not dom.is_dir() or dom.name not in DOMAIN_CODES:
            continue
        code = DOMAIN_CODES[dom.name]
        for scen in dom.iterdir():
            if not scen.is_dir():
                continue
            readme = scen / "README.md"
            if not readme.exists():
                continue
            first = readme.read_text(encoding="utf-8").split("\n", 1)[0].strip()
            if not first.startswith("# "):
                continue
            title = first[2:].strip()
            m = re.match(r"^[A-Z]+-[A-Z]+-(\d{2,3})-", scen.name)
            if not m:
                continue
            sid = f"{p}-{code}-{int(m.group(1)):02d}"
            title_to_id[(p, title.lower().strip())] = sid


def scenario_id_for(chain: dict) -> str | None:
    key = (chain["practice"], chain["title"].lower().strip())
    if key in title_to_id:
        return title_to_id[key]
    for (kp, kt), v in title_to_id.items():
        if kp == chain["practice"] and (kt in chain["title"].lower() or chain["title"].lower() in kt):
            return v
    return None


def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[\u2014\u2013\u2212]", "-", s)
    s = re.sub(r"[^a-z0-9\- ]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)


def flow_key_for(chain: dict) -> str:
    return f"{chain['practice'].lower()}-{slugify(chain['title'])}"


# ---- 2. Practice-specific SOR / entity templates ---------------------------

PRACTICE_SORS: dict[str, dict[str, str]] = {
    "RC": {
        "default": "POS + ERP + Loyalty",
        "supply-chain": "WMS + IoT telemetry + ERP",
        "customer-experience": "CRM + Loyalty + Web analytics",
        "marketing-growth": "Marketing Cloud + Adtech + CDP",
        "pricing-revenue": "ERP + Competitive pricing feeds",
        "operations-workforce": "Store ops + Workforce mgmt",
        "other": "POS + ERP",
    },
    "HLS": {
        "default": "EMR + Claims + HL7 feeds",
        "clinical-care": "EMR + Lab + HL7/FHIR streams",
        "quality-compliance": "Registry + HEDIS + Purview lineage",
        "engineering-rd": "ELN + CDISC + trial-operations stack",
        "other": "EMR + Claims",
    },
    "ER": {
        "default": "SCADA + OSS + Maximo",
        "network-infrastructure": "SCADA + AMI + DMS/OMS",
        "asset-maintenance": "Maximo + IoT + Historian",
        "quality-compliance": "Env-monitoring + regulatory feeds",
        "operations-workforce": "WFM + Dispatch + Historian",
        "other": "SCADA + OSS",
    },
    "AXLE": {
        "default": "MES + PLM + QMS",
        "quality-compliance": "QMS + SPC + CAPA workflow",
        "engineering-rd": "PLM + CAD + simulation stack",
        "supply-chain": "ERP + TMS + Supplier portal",
        "operations-workforce": "MES + Scheduling + HR",
        "asset-maintenance": "CMMS + IoT + Historian",
        "other": "MES + PLM",
    },
    "TMT": {
        "default": "BSS/OSS + Billing + CRM",
        "network-infrastructure": "OSS/BSS + Probe + Alarm mgmt",
        "customer-experience": "CRM + Contact Center + Loyalty",
        "marketing-growth": "CDP + Adtech + Content mgmt",
        "risk-fraud-security": "Fraud platform + Billing",
        "other": "BSS/OSS + CRM",
    },
    "TH": {
        "default": "PSS + PMS + Loyalty",
        "pricing-revenue": "RMS + PSS + Competitive shop",
        "customer-experience": "CRM + Loyalty + PMS",
        "operations-workforce": "Crew systems + Rostering",
        "other": "PSS + PMS",
    },
    "ICE": {
        "default": "ERP + Dealer portal + Telematics",
        "asset-maintenance": "Telematics + Dealer portal + CMMS",
        "channel-partner-dealer": "Dealer portal + CRM + Incentive mgmt",
        "supply-chain": "ERP + TMS + Parts portal",
        "other": "ERP + Dealer portal",
    },
}

PRACTICE_ENTITIES: dict[str, dict[str, str]] = {
    "RC": {
        "default": "SCML.SKU + SCML.Lot + CXML.Customer",
        "supply-chain": "SCML.Lot + SCML.Shipment + SCML.Inventory",
        "customer-experience": "CXML.Customer + CXML.Order + CXML.Loyalty",
        "marketing-growth": "CXML.Campaign + CXML.Customer + MERML.Promotion",
        "pricing-revenue": "MERML.Price + MERML.Elasticity + SCML.SKU",
        "operations-workforce": "SCML.Location + WorkforceML.Shift + CXML.Order",
    },
    "HLS": {
        "default": "Patient + Observation + MedicationRequest",
        "clinical-care": "Patient + Encounter + Observation + MedicationRequest",
        "quality-compliance": "Patient + QualityMeasure + AuditTrail",
        "engineering-rd": "Study + Subject + ProtocolDeviation",
    },
    "ER": {
        "default": "GridML.Asset + GridML.Reading + GridML.Event",
        "network-infrastructure": "GridML.Asset + GridML.Outage + GridML.Customer",
        "asset-maintenance": "AssetML.Equipment + AssetML.Reading + WorkOrder",
        "quality-compliance": "EnvML.Emission + EnvML.Permit + AuditTrail",
    },
    "AXLE": {
        "default": "MfgML.WorkOrder + MfgML.Defect + MfgML.Part",
        "quality-compliance": "MfgML.Defect + MfgML.CAPA + MfgML.SPCReading",
        "engineering-rd": "EngML.Part + EngML.BOM + EngML.Simulation",
        "supply-chain": "MfgML.Supplier + MfgML.Shipment + MfgML.PO",
    },
    "TMT": {
        "default": "NetML.Subscriber + NetML.Service + NetML.Element",
        "network-infrastructure": "NetML.Element + NetML.Fault + NetML.KPI",
        "customer-experience": "NetML.Subscriber + NetML.Interaction + NetML.Ticket",
        "marketing-growth": "NetML.Subscriber + NetML.Campaign + NetML.Content",
    },
    "TH": {
        "default": "THML.Guest + THML.Booking + THML.Flight",
        "pricing-revenue": "THML.Booking + THML.Rate + THML.Inventory",
        "customer-experience": "THML.Guest + THML.Interaction + THML.Loyalty",
        "operations-workforce": "THML.Crew + THML.Schedule + THML.Flight",
    },
    "ICE": {
        "default": "ICEML.Asset + ICEML.Dealer + ICEML.Telemetry",
        "asset-maintenance": "ICEML.Asset + ICEML.Telemetry + ICEML.WorkOrder",
        "channel-partner-dealer": "ICEML.Dealer + ICEML.Deal + ICEML.Incentive",
        "supply-chain": "ICEML.Parts + ICEML.Shipment + ICEML.Dealer",
    },
}


def lookup(d: dict, prim: str, fallback_key: str = "default") -> str:
    return d.get(prim, d.get(fallback_key, ""))


def domain_from_id(sid: str) -> str:
    """Reverse-lookup domain slug from the domain code in a scenario ID."""
    parts = sid.split("-")
    if len(parts) < 3:
        return "other"
    code = parts[1]
    inv = {v: k for k, v in DOMAIN_CODES.items()}
    return inv.get(code, "other")


# ---- 3. Flow template generator --------------------------------------------

def build_flow(chain: dict, scenario_id: str) -> dict:
    practice = chain["practice"]
    title = chain["title"]
    scenario_txt = chain.get("Scenario", "")
    solution_txt = chain.get("Solution", "")
    use_case_txt = chain.get("Use Case", "")
    service_txt = chain.get("Service", "")
    persona_txt = chain.get("Persona", "")
    kpi_txt = chain.get("KPI", "")

    domain = domain_from_id(scenario_id)
    sor_label = lookup(PRACTICE_SORS.get(practice, {}), domain)
    entities_label = lookup(PRACTICE_ENTITIES.get(practice, {}), domain)

    # --- W1 Foundation layer (10 nodes, template) ---
    w1 = {
        "w1-sor": {
            "wave": "W1", "title": f"SOR: {sor_label}", "subtitle": "Source of record",
            "layer": "data", "kind": "source",
            "details": {
                "eyebrow": "W1 · Foundation · System of Record",
                "layer_name": "Integration Plane · SOR",
                "purpose": f"The system-of-record stack for {practice} — {sor_label} — is where the raw events enter APEX. Latency and completeness here set the ceiling for the scenario.",
                "what_apex_does": "APEX mirrors into Bronze via OneLake shortcuts, CDC mirroring, or Fabric Real-Time Hub streaming. The SOR stays authoritative for operational systems.",
                "products": [["Systems of Record", sor_label], ["Fabric Mirroring / CDC", "OneLake shortcut"], ["Real-Time Hub", "for streams"]],
                "scenario_note": scenario_txt[:220] if scenario_txt else f"{title} starts here — every downstream step assumes clean SOR fidelity.",
                "sections": ["§7 MCP Topology", "§13 SOR Integration Playbook"],
            },
        },
        "w1-rth": {
            "wave": "W1", "title": "Real-Time Hub", "subtitle": "Streaming ingestion",
            "layer": "integration", "kind": "process",
            "details": {
                "eyebrow": "W1 · Foundation · Integration",
                "layer_name": "Integration Plane · Fabric Real-Time Hub",
                "purpose": "Bridges SOR streams into Bronze Eventhouse with minimal transformation — event-time indexing, schema-on-read, dead-letter handling.",
                "what_apex_does": "Eventstream configured per SOR feed; Bronze Eventhouse indexes on event-time. No business logic runs here — pure ingest.",
                "products": [["Microsoft Fabric", "Real-Time Hub"], ["Eventstream", "Stream router"], ["Eventhouse", "KQL store"]],
                "scenario_note": f"Events for this scenario land with sub-second fidelity to Bronze, ready for Silver conformance.",
                "sections": ["§12 Fabric Data Plane", "§13.2 Eventstream"],
            },
        },
        "w1-bronze": {
            "wave": "W1", "title": "Bronze · Raw Landing", "subtitle": "Medallion L0",
            "layer": "data", "kind": "store",
            "details": {
                "eyebrow": "W1 · Foundation · Data",
                "layer_name": "Data Plane · Bronze (Medallion L0)",
                "purpose": "Immutable, schema-on-read raw landing zone. Every event arrives here untransformed.",
                "what_apex_does": "Bronze tables partitioned by event-date + source; no PII scrub yet (that is Silver's job). Retention per domain policy.",
                "products": [["OneLake", "Bronze lakehouse"], ["Delta Lake", "ACID storage"], ["Purview", "Bronze classification"]],
                "scenario_note": f"Bronze is the forensic record — every event that contributed to this scenario's decisions is preserved here.",
                "sections": ["§12.1 Medallion Pattern", "§14 Purview Trust"],
            },
        },
        "w1-tokenizer": {
            "wave": "W1", "title": "Tokenizer", "subtitle": "PII/PHI boundary",
            "layer": "governance", "kind": "process",
            "details": {
                "eyebrow": "W1 · Foundation · Governance",
                "layer_name": "Trust Plane · Tokenizer",
                "purpose": "Format-preserving tokenization at the Bronze→Silver boundary. PII/PHI never crosses into Silver in raw form.",
                "what_apex_does": "Entity-aware tokenizer produces stable surrogate keys so agents join + reason without ever touching raw identifiers.",
                "products": [["APEX Tokenizer", "Azure Function"], ["Purview", "classification propagation"], ["Key Vault", "token key mgmt"]],
                "scenario_note": f"Any PII/PHI in {practice} data is tokenized before agents can read it.",
                "sections": ["§11 Decision Audit Row", "§14.3 Classification"],
            },
        },
        "w1-silver": {
            "wave": "W1", "title": "Silver · Canonical", "subtitle": f"{practice} canonical schemas",
            "layer": "data", "kind": "store",
            "details": {
                "eyebrow": "W1 · Foundation · Data",
                "layer_name": "Data Plane · Silver (Medallion L1)",
                "purpose": f"{practice} canonical schemas land here — tokenized, deduplicated, typed, joinable.",
                "what_apex_does": f"Conforms Bronze raw to {practice} canonical entities: {entities_label}. Agents never read Bronze — they read Silver.",
                "products": [["OneLake", "Silver lakehouse"], [f"{practice} Canonical", entities_label], ["dbt / Fabric Notebooks", "conformance jobs"]],
                "scenario_note": f"This scenario's agents read {entities_label} — the canonical schema for {practice}.",
                "sections": ["§5 Canonical Schema", "§12.1 Medallion"],
            },
        },
        "w1-gold": {
            "wave": "W1", "title": "Gold · Agent-Safe Views", "subtitle": "Medallion L2 · Direct Lake",
            "layer": "schema", "kind": "store",
            "details": {
                "eyebrow": "W1 · Foundation · Schema",
                "layer_name": "Data Plane · Gold (Medallion L2)",
                "purpose": "Agent-safe, classification-aware, identity-scoped, output-signed Direct Lake views. This is the layer agents actually read.",
                "what_apex_does": "Gold views are pre-joined, filtered by classification, and served sub-second via Direct Lake. Agents authenticate as themselves — row-level security enforces scope.",
                "products": [["OneLake", "Gold lakehouse"], ["Direct Lake", "sub-second serving"], ["Power BI", "semantic model"]],
                "scenario_note": f"Gold views for this scenario merge {entities_label} into the agent-safe shape defined by §{'16' if practice=='RC' else '10'} Service Catalog.",
                "sections": ["§12.3 Direct Lake", "§16 Service Catalog"],
            },
        },
        "w1-mcp": {
            "wave": "W1", "title": "MCP Servers", "subtitle": "Typed agent tools",
            "layer": "agent", "kind": "tool",
            "details": {
                "eyebrow": "W1 · Foundation · Agent",
                "layer_name": "Reasoning Plane · MCP Servers",
                "purpose": "MCP (Model Context Protocol) servers expose Gold views as typed, identity-scoped, classification-aware tools for agents to call.",
                "what_apex_does": f"For this scenario, MCP tools include {practice}-canonical query tools + write-back tools gated by HITL. Every tool call logs to LEDGER.",
                "products": [["Azure Container Apps", "MCP hosting"], ["Azure AI Agent Service", "tool invocation"], ["APEX MCP SDK", "typed contracts"]],
                "scenario_note": f"The agents in this flow call MCP tools — not raw SQL. Every call is audited.",
                "sections": ["§7 MCP Topology", "§6 Agent Runtime"],
            },
        },
        "w1-identity": {
            "wave": "W1", "title": "Entra · Managed Identity", "subtitle": "Agent identity + scope",
            "layer": "identity", "kind": "process",
            "details": {
                "eyebrow": "W1 · Foundation · Identity",
                "layer_name": "Identity Plane · Entra ID P2",
                "purpose": "Every agent runs under a managed Entra identity. The agent cannot reach any data that identity is not authorized to see.",
                "what_apex_does": "Entra groups + conditional access enforce scope. Token binding propagates identity from MCP → Gold → Bronze for lineage.",
                "products": [["Entra ID P2", "managed identity"], ["Conditional Access", "scope enforcement"], ["Purview", "identity lineage"]],
                "scenario_note": f"Agents in this scenario authenticate as scoped identities — not shared service principals.",
                "sections": ["§8 Entra + Conditional Access", "§14 Purview Trust"],
            },
        },
        "w1-ledger": {
            "wave": "W1", "title": "LEDGER · Audit Row Store", "subtitle": "Decision evidence",
            "layer": "governance", "kind": "store",
            "details": {
                "eyebrow": "W1 · Foundation · Governance",
                "layer_name": "Trust Plane · Decision Audit Row",
                "purpose": "Every agent decision writes a 14-field audit row. LEDGER is the append-only store; it is the forensic record a regulator walks.",
                "what_apex_does": "Audit rows carry decision_id, trace_id, manifest SHAs, policy SHAs, input/output hashes, cost/safety verdict, HITL status.",
                "products": [["Delta Lake", "append-only store"], ["Purview", "lineage integration"], ["Log Analytics", "query surface"]],
                "scenario_note": f"Every decision in this {title} flow writes a row here, tied by trace_id.",
                "sections": ["§11 Audit Row", "§8.8 Audit Architecture"],
            },
        },
        "w1-hitl-surface": {
            "wave": "W1", "title": "HITL Surface · Teams", "subtitle": "Human-in-the-loop UX",
            "layer": "experience", "kind": "process",
            "details": {
                "eyebrow": "W1 · Foundation · Experience",
                "layer_name": "Experience Plane · Teams Adaptive Card",
                "purpose": "When a gate fires, the approver gets a Teams Adaptive Card with the decision summary, the evidence, and one-click Approve/Modify/Reject.",
                "what_apex_does": "The card writes back to LEDGER with the approver's Entra identity, timestamp, and rationale. Policy verdict + safety verdict are visible inline.",
                "products": [["Microsoft Teams", "Adaptive Card"], ["Copilot Studio", "card flow"], ["Power Automate", "orchestration"]],
                "scenario_note": f"For {title}, the HITL gate's primary approver is: {persona_txt[:140] if persona_txt else 'the operational lead on shift'}.",
                "sections": ["§9.1 Gate Kinds", "§9.3 Teams Card"],
            },
        },
    }

    # --- W2 Pilot layer (8 nodes, scenario-specific) ---
    w2 = {
        "w2-event": {
            "wave": "W2", "title": f"{title} · Event Fires", "subtitle": "Scenario trigger",
            "layer": "integration", "kind": "event",
            "details": {
                "eyebrow": "W2 · Pilot · Scenario Trigger",
                "layer_name": "Integration Plane · Trigger",
                "purpose": f"This is the business event that kicks off the {title} flow.",
                "what_apex_does": "Eventstream pattern matches the trigger condition and forwards to the DAG orchestrator.",
                "products": [["Eventstream", "trigger match"], ["Azure Functions", "orchestration trigger"], ["Service Bus", "queue"]],
                "scenario_note": scenario_txt[:280] if scenario_txt else f"The {title} event fires when the scenario conditions are met.",
                "sections": ["§10 Orchestration", "§13.2 Events"],
            },
        },
        "w2-orchestrator": {
            "wave": "W2", "title": "DAG Orchestrator", "subtitle": "Azure AI Agent Service",
            "layer": "agent", "kind": "process",
            "details": {
                "eyebrow": "W2 · Pilot · Orchestration",
                "layer_name": "Reasoning Plane · Orchestrator",
                "purpose": "Composes the agent DAG — sequential + parallel + HITL + feedback patterns from APEX §10.2.",
                "what_apex_does": "Reads the orchestration manifest; dispatches child agents; enforces trace-ID discipline; writes parent audit row.",
                "products": [["Azure AI Agent Service", "runtime"], ["Semantic Kernel", "DAG"], ["APEX Orchestration SDK", "manifest → execution"]],
                "scenario_note": f"For {title}, the orchestrator composes the agent DAG described in the Solution: {solution_txt[:150] if solution_txt else 'a multi-agent decision flow'}.",
                "sections": ["§10.2 Four Primitives", "§6.11 Orchestrator Types"],
            },
        },
        "w2-agent-assess": {
            "wave": "W2", "title": "Agent 1: Assess", "subtitle": "Situation understanding",
            "layer": "agent", "kind": "agent",
            "details": {
                "eyebrow": "W2 · Pilot · Agent #1",
                "layer_name": "Reasoning Plane · Agent (Assess)",
                "purpose": "First agent reads the event + relevant Gold views to establish situational ground truth.",
                "what_apex_does": f"Reads {entities_label.split('+')[0].strip()} views; produces a structured assessment; hands off to the classification agent.",
                "products": [["MCP tools", "Gold view read"], ["Semantic Kernel agent", "assessment prompt"], ["LEDGER", "writes audit row"]],
                "scenario_note": f"Assess stage: {use_case_txt[:200] if use_case_txt else 'pulls the relevant canonical entities and structures the situation.'}",
                "sections": ["§10.3 Archetypes"],
            },
        },
        "w2-agent-classify": {
            "wave": "W2", "title": "Agent 2: Classify", "subtitle": "Rule + policy match",
            "layer": "agent", "kind": "agent",
            "details": {
                "eyebrow": "W2 · Pilot · Agent #2",
                "layer_name": "Reasoning Plane · Agent (Classify)",
                "purpose": "Matches assessment against policy + regulation + business rules to categorise the situation.",
                "what_apex_does": "Reads the applicable policy bundle (classification, HITL thresholds, commercial envelope); emits a typed classification.",
                "products": [["Azure AI Agent Service", "reasoning"], ["Policy manifest", "rule evaluation"], ["Purview", "classification context"]],
                "scenario_note": f"Classification stage applies {practice} domain rules to the assessment.",
                "sections": ["§9 HITL Gates", "§14.3 Classification"],
            },
        },
        "w2-agent-quantify": {
            "wave": "W2", "title": "Agent 3: Quantify", "subtitle": "Value + risk model",
            "layer": "agent", "kind": "agent",
            "details": {
                "eyebrow": "W2 · Pilot · Agent #3",
                "layer_name": "Reasoning Plane · Agent (Quantify)",
                "purpose": "Quantifies the commercial + risk impact. Produces the decision candidate with confidence + expected value.",
                "what_apex_does": "ML model + rules evaluate the classified situation; produces a quantified recommendation + confidence bounds.",
                "products": [["Azure ML", "model scoring"], ["Fabric DS notebooks", "decision features"], ["APEX signals", "risk context"]],
                "scenario_note": f"Quantify stage produces the decision input — what the HITL approver will see on their Teams card.",
                "sections": ["§10.3 Feedback Loop", "§16 Service Catalog"],
            },
        },
        "w2-hitl": {
            "wave": "W2", "title": "HITL Gate", "subtitle": "Human approval",
            "layer": "experience", "kind": "gate",
            "details": {
                "eyebrow": "W2 · Pilot · HITL Gate",
                "layer_name": "Experience Plane · HITL",
                "purpose": "A human with the right role + training reviews the agent's recommendation and commits Approve / Modify / Reject.",
                "what_apex_does": f"Gate presents to: {persona_txt[:200] if persona_txt else 'the designated approver for this scenario'}. Writes approver decision + rationale to LEDGER.",
                "products": [["Teams Adaptive Card", "UX"], ["Entra ID", "approver identity"], ["LEDGER", "decision capture"]],
                "scenario_note": f"Without HITL, the agent cannot commit irreversible outcomes. This gate is the governance floor.",
                "sections": ["§9.1 Gate Kinds", "§11 Audit Row"],
            },
        },
        "w2-agent-act": {
            "wave": "W2", "title": "Agent 4: Act", "subtitle": "Downstream effect",
            "layer": "agent", "kind": "agent",
            "details": {
                "eyebrow": "W2 · Pilot · Agent #4",
                "layer_name": "Reasoning Plane · Agent (Act)",
                "purpose": "After HITL approval, the action agent executes the downstream effect — write-back, notification, workflow kickoff.",
                "what_apex_does": "Calls action MCP tools (SOR write-back, ticket creation, notification); references parent audit row via trace_id.",
                "products": [["MCP Action tools", "SOR write-back"], ["Power Automate", "workflow"], ["Service Bus", "async queue"]],
                "scenario_note": f"For {title}, the act agent performs the approved decision and emits its own audit row linked back via downstream_effect_ref.",
                "sections": ["§11.3 Downstream Effect"],
            },
        },
        "w2-kpi": {
            "wave": "W2", "title": "KPI Attribution", "subtitle": "Outcome measured",
            "layer": "outcome", "kind": "outcome",
            "details": {
                "eyebrow": "W2 · Pilot · KPI",
                "layer_name": "Outcome Plane · KPI Attribution",
                "purpose": "The business KPI is attributed back to this specific decision via trace_id — not estimated, not sampled.",
                "what_apex_does": "KPI measurement pipeline joins downstream SOR data back to the decision trace for causal attribution.",
                "products": [["Power BI", "KPI dashboard"], ["Fabric Warehouse", "attribution model"], ["LEDGER", "decision lookup"]],
                "scenario_note": kpi_txt[:220] if kpi_txt else f"KPI attributed: the measurable outcome of this decision.",
                "sections": ["§16 Service Catalog", "§11.5 Composite Row"],
            },
        },
    }

    # --- W3 Scale & Fuse layer (6 nodes) ---
    # Pick 2 sibling scenarios from the same practice for the fusion nodes
    siblings = [c for c in chains if c["practice"] == practice and c["title"] != title][:2]
    fuse_a = siblings[0] if len(siblings) > 0 else None
    fuse_b = siblings[1] if len(siblings) > 1 else None

    w3 = {
        "w3-scale": {
            "wave": "W3", "title": "Enterprise Scale", "subtitle": "N-fold deployment",
            "layer": "outcome", "kind": "process",
            "details": {
                "eyebrow": "W3 · Scale · Rollout",
                "layer_name": "Outcome Plane · Scale",
                "purpose": "W2 Pilot proved the pattern on one business unit. W3 scales it across the enterprise footprint.",
                "what_apex_does": "Template deployment kit: Fabric workspace clone, Entra group set, MCP tool registration, LEDGER routing — all idempotent.",
                "products": [["Fabric Workspace templates", "per-unit clone"], ["Terraform / Bicep", "infra repeatability"], ["APEX Deployment CLI", "per-unit config"]],
                "scenario_note": f"Scale for {title}: deploy to every unit where {service_txt[:80] if service_txt else 'the service catalog applies'}.",
                "sections": ["§15 Service Catalog", "§18 Reference Deployments"],
            },
        },
        "w3-fuse-a": {
            "wave": "W3", "title": f"Fuse: {fuse_a['title'][:30] if fuse_a else 'Sibling Scenario A'}", "subtitle": "Cross-scenario context",
            "layer": "outcome", "kind": "process",
            "details": {
                "eyebrow": "W3 · Fuse · Cross-Scenario",
                "layer_name": "Outcome Plane · Fusion",
                "purpose": "Audit rows + Silver canonical data from this scenario flow into a sibling scenario as context — the same LEDGER, the same Gold views.",
                "what_apex_does": f"Links this scenario's outputs into the upstream context for: {fuse_a['title'] if fuse_a else 'other practice scenarios'}.",
                "products": [["LEDGER cross-trace", "shared audit rows"], ["Gold view reuse", "same canonical entities"], ["Fabric lineage", "Purview tracking"]],
                "scenario_note": f"Fusion demonstrates the {practice} flywheel: one scenario's decisions enrich the next.",
                "sections": ["§11.5 Composite Row", "§6.12.7 LEDGER Feedback"],
            },
        },
        "w3-fuse-b": {
            "wave": "W3", "title": f"Fuse: {fuse_b['title'][:30] if fuse_b else 'Sibling Scenario B'}", "subtitle": "Cross-scenario context",
            "layer": "outcome", "kind": "process",
            "details": {
                "eyebrow": "W3 · Fuse · Cross-Scenario",
                "layer_name": "Outcome Plane · Fusion",
                "purpose": "Second fusion link — same LEDGER, same Gold, different decision context.",
                "what_apex_does": f"Links this scenario's outputs into: {fuse_b['title'] if fuse_b else 'another practice scenario'}.",
                "products": [["LEDGER cross-trace", "shared audit rows"], ["Gold view reuse", "same canonical entities"]],
                "scenario_note": f"Pattern reuse across {practice} scenarios is the value compounding mechanism.",
                "sections": ["§18 Reference Deployments"],
            },
        },
        "w3-purview": {
            "wave": "W3", "title": "Purview Trust", "subtitle": "Enterprise lineage + DLP",
            "layer": "governance", "kind": "store",
            "details": {
                "eyebrow": "W3 · Scale · Trust",
                "layer_name": "Trust Plane · Purview",
                "purpose": "At scale, Purview is where regulators walk. Lineage from SOR to decision, DLP policies enforced, WORM retention applied.",
                "what_apex_does": "Purview graph visualizes cross-scenario lineage; DLP rules gate agent-facing views; audit query APIs for regulators.",
                "products": [["Microsoft Purview", "Trust Plane"], ["Unified Catalog", "business glossary"], ["WORM retention", "7-year default"]],
                "scenario_note": f"Enterprise-scale trust for {practice} anchors in Purview — every decision in this flow is walk-able.",
                "sections": ["§14 Purview Trust", "§8.8 Audit Architecture"],
            },
        },
        "w3-ledger-feedback": {
            "wave": "W3", "title": "Feedback Loop", "subtitle": "LEDGER → eval",
            "layer": "governance", "kind": "process",
            "details": {
                "eyebrow": "W3 · Scale · Feedback",
                "layer_name": "Trust Plane · LEDGER Feedback",
                "purpose": "LEDGER is not a log — it is how the agent learns. Sampled rows become eval cases; eval cases shape next-version prompts.",
                "what_apex_does": "Audit rows → SME review → golden dataset → regression tests → shadow mode → canary rollout. Year one instincts, year three superagent.",
                "products": [["Azure AI Evaluation", "golden sets"], ["Promptflow", "regression"], ["LEDGER", "decision corpus"]],
                "scenario_note": f"Every approved + rejected decision in this {title} flow becomes a training signal for the next version.",
                "sections": ["§6.12.7 LEDGER Feedback", "§5A.4 Evaluation Plane"],
            },
        },
        "w3-kpi-enterprise": {
            "wave": "W3", "title": "Enterprise KPI", "subtitle": "Portfolio outcome",
            "layer": "outcome", "kind": "outcome",
            "details": {
                "eyebrow": "W3 · Scale · KPI",
                "layer_name": "Outcome Plane · Enterprise KPI",
                "purpose": "At enterprise scale the KPI is no longer 'this decision' but 'the rate-of-sound-decisions across the portfolio'.",
                "what_apex_does": "Aggregate Power BI semantic model joins audit rows to SOR outcomes across every instance of this scenario.",
                "products": [["Power BI Premium", "semantic model"], ["Fabric Warehouse", "portfolio math"], ["Teams dashboards", "executive view"]],
                "scenario_note": f"Enterprise KPI for {title}: {kpi_txt[:200] if kpi_txt else 'measured across every deployment unit'}.",
                "sections": ["§16 Service Catalog", "§18 Reference Deployments"],
            },
        },
    }

    return {**w1, **w2, **w3}


# ---- 4. Build flows for all 35 scenarios -----------------------------------

generated_flows: dict[str, dict] = {}
id_to_flow_key: dict[str, str] = {}

# Preserve the original cold-chain entry by keying off its original flow-key
ORIG_COLD_CHAIN_KEY = "rc-cold-chain-excursion"

for c in chains:
    sid = scenario_id_for(c)
    if not sid:
        continue
    # Special-case: RC-SUPCHN-01 keeps its hand-authored flow-key
    if sid == "RC-SUPCHN-01":
        fk = ORIG_COLD_CHAIN_KEY
    else:
        fk = flow_key_for(c)
    id_to_flow_key[sid] = fk
    # Only generate flows for non-cold-chain (cold-chain stays authored)
    if sid != "RC-SUPCHN-01":
        generated_flows[fk] = build_flow(c, sid)

print(f"Generated {len(generated_flows)} new flow entries")
print(f"ID→flow-key map: {len(id_to_flow_key)}")

# ---- 5. Inject into APEX_FLOW_DATA ----------------------------------------

m = re.search(r"(const APEX_FLOW_DATA\s*=\s*)(\{.*?\});", html, re.DOTALL)
if not m:
    print("ERROR: APEX_FLOW_DATA not found")
    sys.exit(1)

flow_data = json.loads(m.group(2))
# Merge generated flows
for k, v in generated_flows.items():
    flow_data[k] = v

new_flow_data_js = json.dumps(flow_data, ensure_ascii=False, separators=(",", ":"))
html = html[:m.start(2)] + new_flow_data_js + html[m.end(2):]
print(f"APEX_FLOW_DATA now has {len(flow_data)} scenarios")

# ---- 6. Update ID_TO_FLOW_KEY in the flow-picker v2 init ------------------

id_map_js = json.dumps(id_to_flow_key, ensure_ascii=False, separators=(",", ":"))
m2 = re.search(r"(const ID_TO_FLOW_KEY\s*=\s*)(\{[^}]*?\});", html)
if m2:
    html = html[:m2.start(2)] + id_map_js + html[m2.end(2):]
    print(f"ID_TO_FLOW_KEY now has {len(id_to_flow_key)} mappings")
else:
    print("WARN: ID_TO_FLOW_KEY not found — skipping")

HTML.write_text(html, encoding="utf-8")
print(f"\nWrote {HTML}")
