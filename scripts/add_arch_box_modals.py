"""Make every box in the Overview architecture diagram clickable.

Maps each <rect> in the Overview SVG to a slug by its (x,y) coordinates,
injects `data-arch-box="slug"` attributes + a .clickable-rect class,
adds two invisible overlay rects on the foundation band for the Entra
and Purview zones, and ships a modal + click handler + authored detail
content for all 19 boxes.

Idempotent via /* arch-box-modal-v1 */ marker.
"""

from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

HTML = Path("docs/reference/APEX-Stacked-Architecture-Narrated.html")
html = HTML.read_text(encoding="utf-8")

MARKER = "/* arch-box-modal-v1 */"
if MARKER in html:
    print("Arch box modal already present — no-op.")
    sys.exit(0)

# -----------------------------------------------------------------------------
# (x, y) -> slug   (matches the 18 rects found in the SVG)
# -----------------------------------------------------------------------------
COORD_TO_SLUG: dict[tuple[str, str], str] = {
    ("80",   "28"):  "ingress-event",
    ("80",   "96"):  "fabric-connectors",
    ("240",  "106"): "bronze",
    ("440",  "106"): "silver",
    ("640",  "106"): "gold",
    ("440",  "172"): "canonical-schema",
    ("240",  "236"): "orchestration",
    ("640",  "236"): "mcp-tool",
    ("1110", "236"): "redis",
    ("1110", "296"): "ledger",
    ("870",  "170"): "audit-row",
    ("540",  "304"): "foundry-agent",
    ("380",  "380"): "child-a",
    ("900",  "380"): "child-b",
    ("240",  "476"): "service-catalog",
    ("620",  "476"): "experience-plane",
    ("920",  "476"): "persona-hitl",
}

# -----------------------------------------------------------------------------
# Authored content for each box
# -----------------------------------------------------------------------------
BOX_DETAILS: dict[str, dict] = {
    "ingress-event": {
        "title": "Event · Trigger",
        "eyebrow": "Ingress Plane · §13 SOR Integration",
        "accent": "event",
        "purpose": "Every APEX decision starts as a change-event in a System of Record: a CDC row in SAP, a SCADA telemetry tick, an EMR update, a Kafka message. This box is the <strong>trigger</strong> — the precipitating signal that a scenario's agent flow must respond to.",
        "what_apex_does": "APEX does not own the SORs. It listens. Triggers are captured through Fabric Mirroring (for structured CDC), Event Hubs (for streams), OPC UA (for OT data), or custom iPaaS connectors. No business logic runs at this layer — pure capture.",
        "products": [["SAP", "ERP / S4HANA"], ["SCADA", "OT telemetry"], ["EMR", "Epic / Cerner / Meditech"], ["Salesforce", "CRM"], ["Kafka", "streams"]],
        "sections": ["§13 SOR Integration Playbook", "§7 MCP Topology"],
    },
    "fabric-connectors": {
        "title": "Fabric Connectors",
        "eyebrow": "Integration Plane · §12 Fabric Data",
        "accent": "data",
        "purpose": "The bridge between SORs and Bronze. Five canonical integration patterns cover the full SOR landscape: <strong>Mirroring</strong>, <strong>ADF pipelines</strong>, <strong>Event Hubs</strong>, <strong>OPC UA</strong>, <strong>iPaaS / self-hosted runtime</strong>.",
        "what_apex_does": "Selects the right pattern per SOR based on latency, fidelity, and compliance requirements. Mirroring for structured CDC (SAP, Salesforce); Event Hubs for high-throughput streams; OPC UA for OT; iPaaS for SaaS APIs.",
        "products": [["Fabric Mirroring", "CDC"], ["Azure Data Factory", "batch + orchestration"], ["Event Hubs", "streaming"], ["OPC UA Publisher", "OT"], ["Logic Apps / Boomi", "iPaaS"]],
        "sections": ["§12.2 Five Integration Patterns", "§13 SOR Playbook"],
    },
    "bronze": {
        "title": "Bronze · Raw Landing",
        "eyebrow": "Data Plane · Medallion L0",
        "accent": "data",
        "purpose": "Immutable, schema-on-read, SOR-fidelity raw landing zone. Every event arrives here untransformed. This is the forensic record.",
        "what_apex_does": "OneLake-backed Delta lakehouse tables partitioned by event-date + source. No PII scrub yet (that is Silver's job). Retention per domain policy — 7y default, 10y HLS, permanent for legal hold.",
        "products": [["OneLake", "Bronze lakehouse"], ["Delta Lake", "ACID storage"], ["Purview", "Bronze classification"]],
        "sections": ["§12.1 Medallion Pattern", "§14 Purview Trust"],
    },
    "silver": {
        "title": "Silver · Canonical",
        "eyebrow": "Data Plane · Medallion L1",
        "accent": "data",
        "purpose": "Conformed, tokenized, typed, joinable. The canonical schema layer lives here — SCML, PatientML, AXLEML, CXML, MERML — each a semantic contract.",
        "what_apex_does": "Tokenization happens at the Bronze→Silver boundary. PII/PHI never crosses into Silver in raw form. Surrogate keys let agents join and reason without touching identifiers.",
        "products": [["OneLake", "Silver lakehouse"], ["APEX Tokenizer", "format-preserving"], ["Canonical Schemas", "SCML / PatientML / etc."]],
        "sections": ["§5 Canonical Schema", "§11.6 Tokenization"],
    },
    "gold": {
        "title": "Gold · Agent-Safe Views",
        "eyebrow": "Data Plane · Medallion L2",
        "accent": "data",
        "purpose": "Agent-safe, classification-aware, identity-scoped, output-signed Direct Lake views. <strong>This is the layer agents actually read.</strong>",
        "what_apex_does": "Gold views are pre-joined, filtered by classification, served sub-second via Direct Lake. Agents authenticate as themselves — row-level security enforces scope. No agent ever touches Bronze or Silver directly.",
        "products": [["OneLake", "Gold lakehouse"], ["Direct Lake", "sub-second serving"], ["Power BI", "semantic model"]],
        "sections": ["§12.3 Direct Lake", "§16 Service Catalog"],
    },
    "canonical-schema": {
        "title": "Canonical Schema Layer",
        "eyebrow": "Schema Plane · §5 Canonical Schema",
        "accent": "schema",
        "purpose": "The semantic contract that makes every scenario <em>implementable</em>. SCML for supply chain, PatientML for clinical, AXLEML for manufacturing, and more — each a typed, classification-aware specification of the entities that matter in that industry.",
        "what_apex_does": "Every canonical schema carries: typed entities, relationships, classifications (propagated to Purview), business-term bindings (Unified Catalog), and pre-/post-measure derivations. Contracts are enforced in code (Fabric artifacts), in governance (Purview labels), and in agent behavior (MCP tool bindings).",
        "products": [["SCML", "Supply Chain"], ["PatientML", "Clinical"], ["AXLEML", "Manufacturing"], ["MERML", "Merchandising"], ["CXML", "Customer"]],
        "sections": ["§5 Canonical Schema", "§1.6 Why Canonical", "§1.6A Industry Standards"],
    },
    "orchestration": {
        "title": "Orchestration · 47 Archetypes",
        "eyebrow": "Contract Plane · §10 Orchestration",
        "accent": "orch",
        "purpose": "The <strong>multi-agent pattern library</strong>. Four primitive patterns (sequential, parallel, hierarchical, feedback) compose into 47 APEX orchestration archetypes spanning every scenario pattern across the 7 Practices.",
        "what_apex_does": "Each orchestration is a manifest-declared DAG. Parent Foundry Agent reads the manifest; dispatches child agents; enforces trace-ID discipline; composes the audit row. Semantic Kernel or Copilot Studio underneath.",
        "products": [["Azure AI Agent Service", "runtime"], ["Semantic Kernel", "DAG"], ["APEX Orchestration Manifests", "declarative"], ["Copilot Studio", "low-code"]],
        "sections": ["§10.2 Four Primitives", "§10.3 47 Archetypes", "§6.11 Orchestrator Types"],
    },
    "mcp-tool": {
        "title": "MCP Tool",
        "eyebrow": "Contract Plane · §7 MCP Topology",
        "accent": "mcp",
        "purpose": "Model Context Protocol servers expose Gold views as <strong>typed, identity-scoped, classification-aware</strong> tools for agents to call. The contract between agents and data.",
        "what_apex_does": "Each MCP tool is a typed Python function registered via the APEX MCP SDK. Every call is audited. Scope is bound to the calling agent's Entra identity. Classification rules gate what the tool can return.",
        "products": [["Azure Container Apps", "MCP hosting"], ["Azure AI Agent Service", "tool invocation"], ["APEX MCP SDK", "typed contracts"]],
        "sections": ["§7 MCP Topology", "Appendix I MCP Tool Catalog"],
    },
    "redis": {
        "title": "Redis · Session / P-C State",
        "eyebrow": "Control Plane · §6.13 Parent-Child",
        "accent": "control",
        "purpose": "The <strong>control-plane cache</strong> for multi-agent orchestrations. Holds ephemeral session state, parent-child coordination, and kill-switch signals.",
        "what_apex_does": "Redis is <em>control plane only</em> — never the data plane. It stores: agent session context, parent-child state handoffs, cancellation tokens, rate-limit counters. No business data lands here.",
        "products": [["Azure Cache for Redis", "Premium tier"], ["APEX Control Plane SDK", "typed operations"]],
        "sections": ["§6.13 Parent-Child Orchestration", "§6.13.3 Three Control Primitives"],
    },
    "ledger": {
        "title": "LEDGER · Document Lineage",
        "eyebrow": "Governance Plane · §6.12 File-First Context",
        "accent": "control",
        "purpose": "The file-first context architecture — <strong>beyond knowledge graphs and vectors</strong>. LEDGER holds signed manifests, memory files, identity files (SOUL.md), and the accumulating record of agent competence.",
        "what_apex_does": "Every file in LEDGER carries: Purview classification, Entra-gated reads, version pinning, immutability during run. Hardened against ClawHavoc-class attacks on file-first systems.",
        "products": [["OneLake", "signed manifest store"], ["Purview", "classification"], ["Entra", "read gates"]],
        "sections": ["§6.12 File-First Context", "§6.12.6 OpenClaw Lineage", "§6.12.7 LEDGER Feedback Loop"],
    },
    "audit-row": {
        "title": "Audit Row",
        "eyebrow": "Governance Plane · §11 Decision Audit Row",
        "accent": "gold",
        "purpose": "The 14-field typed audit row — <strong>the unit of regulator-answerable evidence</strong>. Every agent decision writes one. decision_id, trace_id, manifest SHAs, policy SHAs, input/output hashes, cost, safety verdict, HITL status.",
        "what_apex_does": "Audit rows land in an append-only store. They bind every decision to: the rules that governed it (three-version rule: manifest + policy + prompt SHAs), the data that fed it (input hash), the outcome (output hash), the human (HITL record).",
        "products": [["Delta Lake", "append-only store"], ["Purview", "lineage integration"], ["Log Analytics", "query surface"]],
        "sections": ["§11 Audit Row", "§11.6 Trace-ID Discipline", "§11.7 Three-Version Rule", "§8.8 Audit Architecture"],
    },
    "foundry-agent": {
        "title": "Foundry Agent · Parent",
        "eyebrow": "Reasoning Plane · §6 Azure AI Foundry",
        "accent": "reasoning",
        "purpose": "The reasoning core. <strong>Every APEX agent runs here.</strong> Azure AI Agent Service composes: LLM + tools + prompts + manifest. The parent orchestrates child agents and writes the parent audit row.",
        "what_apex_does": "Parent agent reads the orchestration manifest; decomposes work to child specialists; enforces trace-ID discipline; writes the audit row referencing every child decision. Writes audit row is non-optional — missing audit row = quarantined invocation.",
        "products": [["Azure AI Foundry", "agent platform"], ["Azure AI Agent Service", "runtime"], ["Foundation models", "GPT-4o / Claude / Llama"], ["APEX Agent SDK", "manifest-driven"]],
        "sections": ["§6 Foundry", "§6.3 Foundry-Native", "§6.10 Audit Row Emission"],
    },
    "child-a": {
        "title": "Child Agent A · Specialist",
        "eyebrow": "Reasoning Plane · §6.13 Parent-Child",
        "accent": "reasoning",
        "purpose": "A specialist sub-agent dispatched by the parent. Narrow tool surface, focused reasoning, writes its own audit row linked back to the parent via trace_id.",
        "what_apex_does": "Child agents are manifest-declared specialists — e.g. assess, classify, quantify, extract. Each has its own prompt, tool list, and evaluation harness. Parent composes their outputs into the final decision.",
        "products": [["Semantic Kernel Agent", "child runtime"], ["MCP tools", "narrow surface"], ["LEDGER", "audit trail"]],
        "sections": ["§6.13 Parent-Child", "§10.3 Hierarchical Archetype"],
    },
    "child-b": {
        "title": "Child Agent B · Specialist",
        "eyebrow": "Reasoning Plane · §6.13 Parent-Child",
        "accent": "reasoning",
        "purpose": "Second specialist child. Same shape as Child A but different specialty — decomposition is scenario-specific.",
        "what_apex_does": "Parent fans out to multiple children in parallel or sequentially. Each child's output becomes input to the parent's composite decision. All audit-rowed via shared trace_id.",
        "products": [["Semantic Kernel Agent", "child runtime"], ["MCP tools", "narrow surface"]],
        "sections": ["§6.13 Parent-Child", "§10.3 Hierarchical Archetype"],
    },
    "service-catalog": {
        "title": "Service Catalog",
        "eyebrow": "Experience Plane · §16 Service Catalog",
        "accent": "service",
        "purpose": "The <strong>productized + priced</strong> bundling of agents, orchestrations, and outcomes into sellable services. E.g. RC-E2E-03 (Assortment & Pricing), HLS-E2E-02 (Clinical Decision Support), AXLE-CF-01 (Connected Factory).",
        "what_apex_does": "Each service is a named bundle with a commercial envelope, KPI attribution, delivery team composition, and a pricing model. Services are how clients consume APEX — not individual agents.",
        "products": [["Service manifests", "declarative"], ["Commercial envelope contracts", "Wave-sized"], ["KPI attribution pipeline", "outcome-linked"]],
        "sections": ["§16 Service Catalog", "§15 Per-Practice Services", "§22B Value-Delivery Chain"],
    },
    "experience-plane": {
        "title": "Experience Plane",
        "eyebrow": "Experience Plane · §7 Copilot + Teams",
        "accent": "experience",
        "purpose": "Where humans meet agents. Copilot (M365 + custom), Copilot Studio (low-code flows), Power BI (dashboards + Q&A), Teams (notifications + HITL cards).",
        "what_apex_does": "Each experience surface is a thin client over the reasoning plane. Copilot reads agent responses; Copilot Studio orchestrates flows; Power BI visualizes KPIs from the audit row; Teams carries Adaptive Cards for approvals.",
        "products": [["Microsoft Copilot", "M365 + custom"], ["Copilot Studio", "low-code flows"], ["Power BI", "dashboards"], ["Microsoft Teams", "Adaptive Cards"]],
        "sections": ["§7 Copilot", "§7.5 Copilot Studio", "§9.3 Teams Card Integration"],
    },
    "persona-hitl": {
        "title": "Persona · HITL",
        "eyebrow": "Experience Plane · §9 HITL Gates",
        "accent": "experience",
        "purpose": "The <strong>human-in-the-loop gate</strong>. Approve / Modify / Deny. Every irreversible decision flows through a typed persona with the right role, training, and accountability.",
        "what_apex_does": "The Teams Adaptive Card presents: decision candidate, full evidence chain, policy verdict, safety verdict. The approver commits one of {approve, modify, reject, override} with rationale. That commit is appended to the audit row.",
        "products": [["Teams Adaptive Card", "UX"], ["Entra ID", "approver identity"], ["LEDGER", "decision capture"]],
        "sections": ["§9 HITL Runtime", "§9.1 Four Gate Kinds", "§2.2C Oversight Spectrum"],
    },
    "foundation-entra": {
        "title": "Entra · Identity",
        "eyebrow": "Foundation · §8 Entra ID P2",
        "accent": "entra",
        "purpose": "The identity backbone. <strong>Every agent runs under a managed Entra identity.</strong> Agents cannot reach data their identity is not authorized to see. No shared service principals, no API keys.",
        "what_apex_does": "Managed Identity for every agent + OBO (On-Behalf-Of) token flow for user context + Conditional Access policies gating tool invocation + Entra groups for scope assignment.",
        "products": [["Entra ID P2", "managed identities"], ["OBO flow", "user-context propagation"], ["Conditional Access", "scope enforcement"]],
        "sections": ["§8 Entra + Conditional Access", "§3.1 Identity Plane"],
    },
    "foundation-purview": {
        "title": "Purview · Trust",
        "eyebrow": "Foundation · §14 Purview Trust",
        "accent": "purview",
        "purpose": "The governance spine. Sensitivity labels, DLP policies, and end-to-end lineage from Bronze through Audit Row. <strong>Regulators walk Purview, not spreadsheets.</strong>",
        "what_apex_does": "Classifications declared in canonical schemas propagate automatically — through Fabric, through MCP tools, through agent outputs, into the audit row. DLP applies across every surface. Unified Catalog binds business terms to every field.",
        "products": [["Microsoft Purview", "Trust Plane"], ["Sensitivity Labels", "classification"], ["DLP policies", "enforcement"], ["Unified Catalog", "business glossary"]],
        "sections": ["§14 Purview Trust", "§14.3 Classification Propagation", "§8.8 Audit Architecture"],
    },
}


def make_modal_html() -> str:
    # Pre-render all box details as hidden sections; click handler swaps which is shown
    sections = []
    for slug, d in BOX_DETAILS.items():
        products = "".join(f'<span class="abm-pill">{p[0]} <em>{p[1]}</em></span>' for p in d["products"])
        refs = "".join(f'<span class="abm-ref">{s}</span>' for s in d["sections"])
        sections.append(
            f'<section data-arch-panel="{slug}" class="abm-panel">'
            f'  <div class="abm-eyebrow">{d["eyebrow"]}</div>'
            f'  <h3 class="abm-title">{d["title"]}</h3>'
            f'  <div class="abm-label">What this is</div>'
            f'  <p class="abm-body">{d["purpose"]}</p>'
            f'  <div class="abm-label">What APEX does here</div>'
            f'  <p class="abm-body">{d["what_apex_does"]}</p>'
            f'  <div class="abm-label">Key products</div>'
            f'  <div class="abm-pills">{products}</div>'
            f'  <div class="abm-label">Cross-references</div>'
            f'  <div class="abm-refs">{refs}</div>'
            f'</section>'
        )
    return '\n'.join(sections)


MODAL_HTML = (
    '<!-- arch-box-modal-v1 -->\n'
    '<div id="archBoxModalBackdrop" class="abm-backdrop" onclick="closeArchBoxModal()"></div>\n'
    '<div id="archBoxModal" class="abm-modal" role="dialog" aria-modal="true" aria-hidden="true" aria-labelledby="abmTitle">\n'
    '  <button class="abm-close" type="button" onclick="closeArchBoxModal()" aria-label="Close">&times;</button>\n'
    '  <div class="abm-body-wrap">\n'
    + make_modal_html() +
    '\n  </div>\n'
    '</div>\n'
)


CSS = (
    MARKER + "\n"
    "/* Make every rect in the overview SVG visibly clickable. */\n"
    "svg.flow-svg rect[data-arch-box] { cursor: pointer; transition: filter .15s ease, stroke-width .15s ease; }\n"
    "svg.flow-svg rect[data-arch-box]:hover { filter: brightness(1.25); stroke-width: 2.5; }\n"
    "svg.flow-svg .abm-hit { cursor: pointer; fill: transparent; pointer-events: all; }\n"
    "svg.flow-svg .abm-hit:hover { fill: rgba(255,255,255,0.03); }\n"
    "\n"
    "/* Arch-box modal */\n"
    ".abm-backdrop {\n"
    "  position: fixed; inset: 0;\n"
    "  background: rgba(0,0,0,.6);\n"
    "  opacity: 0; pointer-events: none;\n"
    "  transition: opacity .2s ease;\n"
    "  z-index: 9998;\n"
    "}\n"
    ".abm-backdrop.open { opacity: 1; pointer-events: auto; }\n"
    ".abm-modal {\n"
    "  position: fixed;\n"
    "  top: 50%; left: 50%;\n"
    "  transform: translate(-50%, -48%) scale(.96);\n"
    "  width: min(620px, 92vw);\n"
    "  max-height: 82vh;\n"
    "  background: var(--bg-1, #0b0b0b);\n"
    "  border: 1px solid var(--line, #2a2a2a);\n"
    "  border-radius: 10px;\n"
    "  box-shadow: 0 24px 80px rgba(0,0,0,.6);\n"
    "  opacity: 0; pointer-events: none;\n"
    "  transition: transform .22s cubic-bezier(.4,0,.2,1), opacity .2s ease;\n"
    "  z-index: 9999;\n"
    "  overflow: hidden;\n"
    "  display: flex; flex-direction: column;\n"
    "}\n"
    ".abm-modal.open {\n"
    "  transform: translate(-50%, -50%) scale(1);\n"
    "  opacity: 1; pointer-events: auto;\n"
    "}\n"
    ".abm-close {\n"
    "  position: absolute; top: 14px; right: 16px;\n"
    "  width: 32px; height: 32px;\n"
    "  border: 1px solid color-mix(in srgb, var(--ink-3, #8a8a8a) 30%, transparent);\n"
    "  background: transparent;\n"
    "  color: var(--ink-2, #b4b4b4);\n"
    "  border-radius: 50%;\n"
    "  font-size: 18px; line-height: 1;\n"
    "  cursor: pointer;\n"
    "  z-index: 2;\n"
    "  transition: background .15s, color .15s;\n"
    "}\n"
    ".abm-close:hover { background: color-mix(in srgb, var(--crimson, #D34848) 30%, transparent); color: #fff; }\n"
    ".abm-body-wrap { overflow-y: auto; padding: 28px 32px 32px; flex: 1; }\n"
    ".abm-panel { display: none; }\n"
    ".abm-panel.active { display: block; }\n"
    ".abm-eyebrow {\n"
    "  font-family: 'JetBrains Mono', monospace;\n"
    "  font-size: 10.5px;\n"
    "  font-weight: 700;\n"
    "  letter-spacing: 0.14em;\n"
    "  text-transform: uppercase;\n"
    "  color: var(--gold, #E3B657);\n"
    "  margin-bottom: 8px;\n"
    "}\n"
    ".abm-title {\n"
    "  font-family: 'Fraunces', Georgia, serif;\n"
    "  font-size: 24px; font-weight: 600;\n"
    "  color: var(--ink-0, #fff);\n"
    "  margin: 0 42px 18px 0;\n"
    "  line-height: 1.2;\n"
    "}\n"
    ".abm-label {\n"
    "  font-family: 'JetBrains Mono', monospace;\n"
    "  font-size: 10px; font-weight: 700;\n"
    "  letter-spacing: 0.14em;\n"
    "  text-transform: uppercase;\n"
    "  color: var(--sky, #6FB9E8);\n"
    "  margin: 18px 0 6px;\n"
    "}\n"
    ".abm-body {\n"
    "  font-size: 13.5px;\n"
    "  line-height: 1.65;\n"
    "  color: var(--ink-1, #e6edf3);\n"
    "  margin: 0 0 4px;\n"
    "}\n"
    ".abm-body strong { color: var(--gold, #E3B657); }\n"
    ".abm-body em { color: var(--teal, #44B8A8); font-style: normal; }\n"
    ".abm-pills { display: flex; flex-wrap: wrap; gap: 6px 8px; }\n"
    ".abm-pill {\n"
    "  display: inline-flex; align-items: center; gap: 6px;\n"
    "  padding: 3px 9px;\n"
    "  font-size: 11.5px;\n"
    "  border-radius: 14px;\n"
    "  background: color-mix(in srgb, var(--bg-3, #1a1a1a) 60%, transparent);\n"
    "  border: 1px solid color-mix(in srgb, var(--line, #2a2a2a) 80%, transparent);\n"
    "  color: var(--ink-1, #e6edf3);\n"
    "}\n"
    ".abm-pill em {\n"
    "  font-style: normal; color: var(--ink-3, #8a8a8a); font-size: 10.5px;\n"
    "}\n"
    ".abm-refs { display: flex; flex-wrap: wrap; gap: 4px 8px; }\n"
    ".abm-ref {\n"
    "  display: inline-block;\n"
    "  font-family: 'JetBrains Mono', monospace;\n"
    "  font-size: 10.5px;\n"
    "  color: var(--sky, #6FB9E8);\n"
    "  padding: 2px 6px;\n"
    "  background: color-mix(in srgb, var(--sky, #6FB9E8) 10%, transparent);\n"
    "  border-radius: 3px;\n"
    "}\n"
)


CLICK_JS = r"""
<script>
/* arch-box-modal-v1 */
(function() {
  'use strict';

  function openArchBoxModal(slug) {
    const modal = document.getElementById('archBoxModal');
    const back = document.getElementById('archBoxModalBackdrop');
    if (!modal) return;
    // Activate the right panel
    modal.querySelectorAll('.abm-panel').forEach(function(p) {
      p.classList.toggle('active', p.getAttribute('data-arch-panel') === slug);
    });
    modal.classList.add('open');
    back.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    // Scroll panel to top
    const wrap = modal.querySelector('.abm-body-wrap');
    if (wrap) wrap.scrollTop = 0;
  }

  function closeArchBoxModal() {
    const modal = document.getElementById('archBoxModal');
    const back = document.getElementById('archBoxModalBackdrop');
    if (!modal) return;
    modal.classList.remove('open');
    back.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  window.openArchBoxModal = openArchBoxModal;
  window.closeArchBoxModal = closeArchBoxModal;

  // Wire clicks on any SVG element with data-arch-box
  document.addEventListener('click', function(e) {
    const el = e.target.closest('[data-arch-box]');
    if (!el) return;
    const slug = el.getAttribute('data-arch-box');
    if (slug) openArchBoxModal(slug);
  });

  // ESC closes
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeArchBoxModal();
  });
})();
</script>
"""


# -----------------------------------------------------------------------------
# 1. Inject data-arch-box on each known rect
# -----------------------------------------------------------------------------
svg_start = html.find('<svg class="flow-svg" viewBox="0 0 1320 640"')
svg_end = html.find('</svg>', svg_start) + len('</svg>')
svg_block = html[svg_start:svg_end]
orig_svg = svg_block

injected = 0
for (x, y), slug in COORD_TO_SLUG.items():
    # Find <rect ... x="X" y="Y" ... /> and inject data-arch-box
    pattern = re.compile(
        rf'(<rect[^/>]*?\sx="{re.escape(x)}"\s+y="{re.escape(y)}"[^/>]*?)(/>)'
    )
    new_svg = pattern.sub(rf'\1 data-arch-box="{slug}"\2', svg_block, count=1)
    if new_svg != svg_block:
        svg_block = new_svg
        injected += 1
    else:
        print(f"  WARN: rect at ({x},{y}) for {slug} not found")

# Add two overlay rects on the foundation band for Entra + Purview zones
# Foundation band: x=80 y=558 w=1210 h=58 — split into two halves
overlay_rects = (
    '<rect class="abm-hit" data-arch-box="foundation-entra" '
    'x="80" y="558" width="605" height="58" rx="10"/>\n'
    '<rect class="abm-hit" data-arch-box="foundation-purview" '
    'x="685" y="558" width="605" height="58" rx="10"/>\n'
)
# Insert the overlays right before </svg>
closing_svg = svg_block.rfind('</svg>')
svg_block = svg_block[:closing_svg] + overlay_rects + svg_block[closing_svg:]

# Stitch back
html = html[:svg_start] + svg_block + html[svg_end:]
print(f"Injected data-arch-box on {injected} rects + 2 foundation overlay rects")

# -----------------------------------------------------------------------------
# 2. Inject CSS
# -----------------------------------------------------------------------------
close_style = html.find("</style>")
if close_style != -1:
    html = html[:close_style] + CSS + html[close_style:]
    print("Injected CSS")

# -----------------------------------------------------------------------------
# 3. Inject modal HTML + click JS right before </body>
# -----------------------------------------------------------------------------
close_body = html.rfind("</body>")
if close_body != -1:
    html = html[:close_body] + MODAL_HTML + CLICK_JS + html[close_body:]
    print("Injected modal + click handler")

HTML.write_text(html, encoding="utf-8")
print(f"\nWrote {HTML}")
