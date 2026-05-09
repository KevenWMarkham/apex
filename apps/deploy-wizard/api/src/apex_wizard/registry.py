"""Loader for services/_registry.json — the wizard's view of the catalog."""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

# repo root: services/_registry.json sits at <root>/services/_registry.json
# this file: <root>/apps/deploy-wizard/api/src/apex_wizard/registry.py
# parents[5] walks up: apex_wizard → src → api → deploy-wizard → apps → <root>
REPO_ROOT = Path(__file__).resolve().parents[5]
REGISTRY_PATH = REPO_ROOT / "services" / "_registry.json"
SERVICES_ROOT = REPO_ROOT / "services"

# Per-practice build-status files. Glob keyed (services/{practice}/_build-status.yaml).
# The wizard /api/catalog/build-status endpoint aggregates across all practices
# that have a file present.
BUILD_STATUS_GLOB = "*/_build-status.yaml"

# Use-case YAMLs live at services/{ind}/{code}/use-cases/{slug}/use-case.yaml
USE_CASE_GLOB = "*/*/use-cases/*/use-case.yaml"

# Adapter root — wizard validates use-case adapter refs resolve here.
ADAPTERS_ROOT = REPO_ROOT / "packages" / "apex-adapters" / "src" / "apex_adapters" / "protocol_adapters"

# Canonical agent set per Professional-APEX-Deployment-Guide §7.2.
# Most services compose this 5-persona set; some scenarios add a 6th.
CANONICAL_AGENTS = [
    {"role": "the-analyst", "label": "The Analyst", "description": "Reads telemetry + canonical schemas, produces a situation read."},
    {"role": "the-demand-checker", "label": "The Demand Checker", "description": "Cross-references demand signals — POS velocity, elasticity, weather, calendar."},
    {"role": "the-finance-lead", "label": "The Finance Lead", "description": "Quantifies P&L impact and applies commercial-envelope guardrails."},
    {"role": "the-operations-lead", "label": "The Operations Lead", "description": "Translates the decision into work — task lists, routing, store action."},
    {"role": "the-briefer", "label": "The Briefer", "description": "Produces the HITL Adaptive Card and the audit-row trace."},
]


@lru_cache(maxsize=1)
def load_registry() -> dict[str, Any]:
    with REGISTRY_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def industries() -> list[dict[str, str]]:
    return load_registry()["industries"]


def service_codes(industry: str | None = None) -> list[dict[str, Any]]:
    codes = load_registry()["service_codes"]
    if industry:
        codes = [c for c in codes if c["industry"] == industry]
    return codes


def scenarios(
    *,
    industry: str | None = None,
    service_code: str | None = None,
    domain: str | None = None,
    featured_only: bool = False,
) -> list[dict[str, Any]]:
    items = load_registry()["scenarios"]
    if industry:
        items = [s for s in items if s["industry_slug"] == industry]
    if service_code:
        items = [s for s in items if s["service_code"] == service_code]
    if domain:
        items = [s for s in items if s["domain"] == domain]
    if featured_only:
        items = [s for s in items if s["featured"]]
    return items


def _scenario_agents(industry: str, service_code: str, scenario_id: str) -> list[dict[str, str]]:
    """Read agents from `services/{industry}/{code}/scenarios/{id}/agents/` if scaffolded.

    Featured scenarios have agent dirs on disk; catalog scenarios fall back to
    the canonical 5-persona set per the deployment guide.
    """
    agents_dir = SERVICES_ROOT / industry / service_code / "scenarios" / scenario_id / "agents"
    if not agents_dir.is_dir():
        return CANONICAL_AGENTS
    found: list[dict[str, str]] = []
    for child in sorted(agents_dir.iterdir()):
        if not child.is_dir():
            continue
        agent_yaml = child / "agent.yaml"
        meta = {"role": child.name, "label": child.name.replace("-", " ").title(), "description": ""}
        if agent_yaml.is_file():
            try:
                with agent_yaml.open("r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                if isinstance(data, dict):
                    meta["label"] = str(data.get("label") or meta["label"])
                    meta["description"] = str(data.get("description") or "")
                    meta["hitl_gate"] = bool(data.get("hitl_gate", False))
            except Exception:
                pass
        found.append(meta)
    return found or CANONICAL_AGENTS


def load_use_cases(*, service_code: str | None = None) -> list[dict]:
    """Load every services/{ind}/{code}/use-cases/{slug}/use-case.yaml.

    Each returned dict carries the full YAML content plus injected fields:
    - `slug` (the directory name)
    - `path` (relative path from repo root)
    """
    out: list[dict] = []
    for path in SERVICES_ROOT.glob(USE_CASE_GLOB):
        try:
            with path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            if not isinstance(data, dict):
                continue
        except Exception:
            continue
        # path: services/{ind}/{code}/use-cases/{slug}/use-case.yaml
        slug = path.parent.name
        code = path.parent.parent.parent.name
        if service_code and code != service_code:
            continue
        data.setdefault("service_code", code)
        data["slug"] = slug
        data["path"] = str(path.relative_to(REPO_ROOT)).replace("\\", "/")
        out.append(data)
    return out


def list_known_adapters() -> list[str]:
    """Return dotted adapter names found under packages/apex-adapters/.../protocol_adapters/.

    Used by the validator when a use-case references an adapter — must
    resolve to a real protocols.py declaring SATISFIES.
    """
    if not ADAPTERS_ROOT.is_dir():
        return []
    out: list[str] = []
    # Walk: protocol_adapters/{category}/[{cloud_subdir}/]{provider}/
    for category in sorted(p for p in ADAPTERS_ROOT.iterdir() if p.is_dir()):
        for entry in sorted(category.iterdir()):
            if not entry.is_dir():
                continue
            # cloud has aws/gcp/azure subdirs; saas/siem/identity have providers directly
            has_grandkids = any(
                (sub / "protocols.py").exists()
                for sub in entry.iterdir()
                if sub.is_dir()
            )
            if has_grandkids:
                for sub in sorted(entry.iterdir()):
                    if (sub / "protocols.py").exists():
                        out.append(f"{category.name}.{entry.name}.{sub.name}")
            elif (entry / "protocols.py").exists():
                out.append(f"{category.name}.{entry.name}")
    return out


def load_build_status() -> dict[str, dict]:
    """Load every per-practice _build-status.yaml. Returns a dict keyed by
    practice slug. Missing files are silently skipped — practices without a
    plan just don't appear in the wizard's Roadmap page.
    """
    out: dict[str, dict] = {}
    for path in SERVICES_ROOT.glob(BUILD_STATUS_GLOB):
        practice = path.parent.name
        try:
            with path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            if not isinstance(data, dict):
                continue
            out[practice] = data
        except Exception:
            # Bad YAML is non-fatal — surface in the API as missing-practice
            # rather than 500 the whole catalog endpoint.
            continue
    return out


def _status_for_service(plan: dict, service_code: str) -> str | None:
    svc = (plan.get("services") or {}).get(service_code)
    if isinstance(svc, dict):
        return svc.get("status")
    return None


def _status_for_scenario(plan: dict, service_code: str, scenario_id: str) -> str | None:
    svc = (plan.get("services") or {}).get(service_code) or {}
    scn = (svc.get("scenarios") or {}).get(scenario_id)
    if isinstance(scn, dict):
        return scn.get("status")
    return None


def _status_for_agent(plan: dict, service_code: str, scenario_id: str, role: str) -> str | None:
    svc = (plan.get("services") or {}).get(service_code) or {}
    scn = (svc.get("scenarios") or {}).get(scenario_id) or {}
    agent = (scn.get("agents") or {}).get(role)
    if isinstance(agent, dict):
        return agent.get("status")
    return None


def tree(featured_only: bool = True) -> list[dict[str, Any]]:
    """Practice → Service → Scenario → Agent hierarchy for the wizard treeview.

    `featured_only=True` returns only the 36 featured scenarios — these are the
    deployable ones. Set False to see catalog stubs too (read-only in the UI).
    """
    reg = load_registry()
    plans = load_build_status()
    scns = scenarios(featured_only=featured_only)
    by_industry: dict[str, list[dict]] = {}
    for sc in scns:
        by_industry.setdefault(sc["industry_slug"], []).append(sc)

    by_service: dict[tuple[str, str], list[dict]] = {}
    for sc in scns:
        by_service.setdefault((sc["industry_slug"], sc["service_code"]), []).append(sc)

    nodes: list[dict[str, Any]] = []
    for ind in reg["industries"]:
        ind_slug = ind["slug"]
        ind_scenarios = by_industry.get(ind_slug, [])
        if featured_only and not ind_scenarios:
            continue
        plan = plans.get(ind_slug, {})
        service_nodes: list[dict[str, Any]] = []
        svc_codes_for_ind = sorted({sc["service_code"] for sc in ind_scenarios})
        for code in svc_codes_for_ind:
            svc_scenarios = by_service.get((ind_slug, code), [])
            scenario_nodes = []
            for sc in sorted(svc_scenarios, key=lambda x: x["scenario_id"]):
                scenario_nodes.append({
                    "id": f"scenario:{sc['scenario_id']}",
                    "kind": "scenario",
                    "label": sc["title"],
                    "scenario_id": sc["scenario_id"],
                    "service_code": code,
                    "industry": ind_slug,
                    "domain": sc["domain"],
                    "kpi": sc["kpi"],
                    "featured": sc["featured"],
                    "status": _status_for_scenario(plan, code, sc["scenario_id"]) or "planned",
                    "children": [
                        {
                            "id": f"agent:{sc['scenario_id']}:{a['role']}",
                            "kind": "agent",
                            "label": a["label"],
                            "role": a["role"],
                            "scenario_id": sc["scenario_id"],
                            "service_code": code,
                            "industry": ind_slug,
                            "description": a.get("description", ""),
                            "hitl_gate": a.get("hitl_gate", False),
                            "status": _status_for_agent(plan, code, sc["scenario_id"], a["role"]) or "planned",
                            "children": [],
                        }
                        for a in _scenario_agents(ind_slug, code, sc["scenario_id"])
                    ],
                })
            service_nodes.append({
                "id": f"service:{code}",
                "kind": "service",
                "label": code,
                "service_code": code,
                "industry": ind_slug,
                "domains": sorted({sc["domain"] for sc in svc_scenarios}),
                "scenario_count": len(svc_scenarios),
                "status": _status_for_service(plan, code) or "planned",
                "children": scenario_nodes,
            })
        nodes.append({
            "id": f"practice:{ind_slug}",
            "kind": "practice",
            "label": ind["label"],
            "industry": ind_slug,
            "service_count": len(service_nodes),
            "has_plan": ind_slug in plans,
            "children": service_nodes,
        })
    return nodes
