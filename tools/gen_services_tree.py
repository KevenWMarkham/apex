"""
Generate the services/ tree from APEX-Scenario-Chains.xlsx.

Layout:
  services/
    _registry.json                         # all 724 scenarios indexed
    README.md                              # taxonomy, how-to-add
    {industry}/                            # rc, axle, er, hls, ice, th, tmt
      README.md
      {SERVICE-CODE}/                      # e.g., RC-E2E-03
        service.yaml                       # service contract + persona + KPI
        bicep/
          main.bicep                       # service-level deployment
          agents.bicep                     # agent fleet stamping
        scenarios/
          {scenario-id}/                   # only featured fully scaffolded
            scenario.yaml                  # 24-step chain + scenario metadata
            agents/                        # 6-agent fleet (featured only)
              assess/agent.yaml
              classify/agent.yaml
              quantify/agent.yaml
              decide/agent.yaml
              act/agent.yaml
              learn/agent.yaml
            bicep/
              scenario.bicep
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

import pandas as pd
import yaml

REPO_ROOT = Path(r"C:\Stage\Clients\Industries\APEX\.claude\worktrees\sweet-williams-159583")
XLSX = Path(r"C:\Stage\Clients\Industries\APEX\docs\reference\APEX-Scenario-Chains.xlsx")
SERVICES_ROOT = REPO_ROOT / "services"

INDUSTRY_PREFIX = {
    "RC": ("rc", "Retail & Consumer Products"),
    "AXLE": ("axle", "Automotive · Aftermarket · Mobility"),
    "ER": ("er", "Energy & Resources"),
    "HLS": ("hls", "Health Care & Life Sciences"),
    "ICE": ("ice", "Industrial Connected Equipment"),
    "TH": ("th", "Travel & Hospitality"),
    "TMT": ("tmt", "Technology · Media · Telecom"),
}

AGENT_ROLES = ["assess", "classify", "quantify", "decide", "act", "learn"]


def industry_of(service_code: str) -> tuple[str, str]:
    prefix = service_code.split("-")[0]
    return INDUSTRY_PREFIX[prefix]


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")
    return s or "untitled"


def yaml_dump(data: dict) -> str:
    return yaml.safe_dump(data, sort_keys=False, default_flow_style=False, allow_unicode=True)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    SERVICES_ROOT.mkdir(parents=True, exist_ok=True)

    lib = pd.read_excel(XLSX, sheet_name="Scenario Library")
    featured = pd.read_excel(XLSX, sheet_name="Featured Chains")
    chain_kpi = pd.read_excel(XLSX, sheet_name="Scenario→KPI Chain")
    chain_24 = pd.read_excel(XLSX, sheet_name="24-Step Chain")

    featured_ids = set(featured["Scenario ID"].astype(str))
    featured_by_id = {row["Scenario ID"]: row for _, row in featured.iterrows()}
    chain_kpi_by_id = {row["Scenario ID"]: row for _, row in chain_kpi.iterrows()}
    chain_24_by_id: dict[str, list[dict]] = defaultdict(list)
    for _, row in chain_24.iterrows():
        chain_24_by_id[row["Scenario ID"]].append({
            "step": int(row["Step #"]),
            "key": row["Step Key"],
            "title": row["Step Title"],
            "layer": row["Layer"],
            "kind": row["Kind"],
            "purpose": row["Purpose"],
            "what_apex_does": row["What APEX Does"],
        })

    services_index: dict[str, dict] = {}
    registry_scenarios: list[dict] = []

    for _, row in lib.iterrows():
        sid = str(row["Scenario ID"]).strip()
        scode = str(row["Service Code"]).strip()
        title = str(row["Title"]).strip()
        domain = str(row["Domain"]).strip()
        brief = str(row["Brief (the moment)"]).strip()
        kpi = str(row["KPI / Outcome"]).strip()
        is_featured = sid in featured_ids

        ind_slug, ind_label = industry_of(scode)

        if scode not in services_index:
            services_index[scode] = {
                "service_code": scode,
                "industry_slug": ind_slug,
                "industry_label": ind_label,
                "domains": set(),
                "scenarios": [],
                "featured_count": 0,
                "catalog_count": 0,
            }
        svc = services_index[scode]
        svc["domains"].add(domain)
        svc["scenarios"].append({
            "scenario_id": sid,
            "title": title,
            "domain": domain,
            "brief": brief,
            "kpi": kpi,
            "featured": is_featured,
        })
        if is_featured:
            svc["featured_count"] += 1
        else:
            svc["catalog_count"] += 1

        registry_scenarios.append({
            "scenario_id": sid,
            "title": title,
            "service_code": scode,
            "industry_slug": ind_slug,
            "domain": domain,
            "brief": brief,
            "kpi": kpi,
            "featured": is_featured,
        })

    # ---- Top-level _registry.json ----
    registry = {
        "generated_from": "docs/reference/APEX-Scenario-Chains.xlsx",
        "totals": {
            "scenarios": len(registry_scenarios),
            "service_codes": len(services_index),
            "industries": len({s["industry_slug"] for s in services_index.values()}),
            "featured": sum(1 for s in registry_scenarios if s["featured"]),
            "catalog": sum(1 for s in registry_scenarios if not s["featured"]),
        },
        "industries": [
            {"slug": slug, "label": label} for slug, label in sorted(INDUSTRY_PREFIX.values())
        ],
        "service_codes": sorted([
            {
                "code": svc["service_code"],
                "industry": svc["industry_slug"],
                "domains": sorted(svc["domains"]),
                "featured_count": svc["featured_count"],
                "catalog_count": svc["catalog_count"],
                "total": svc["featured_count"] + svc["catalog_count"],
            }
            for svc in services_index.values()
        ], key=lambda x: x["code"]),
        "scenarios": sorted(registry_scenarios, key=lambda x: x["scenario_id"]),
    }
    write(SERVICES_ROOT / "_registry.json", json.dumps(registry, indent=2, ensure_ascii=False))

    # ---- Industry READMEs (will be rewritten with prose later) ----
    by_industry: dict[str, list[dict]] = defaultdict(list)
    for svc in services_index.values():
        by_industry[svc["industry_slug"]].append(svc)

    for ind_slug, label in INDUSTRY_PREFIX.values():
        ind_dir = SERVICES_ROOT / ind_slug
        ind_dir.mkdir(parents=True, exist_ok=True)
        svcs = sorted(by_industry.get(ind_slug, []), key=lambda x: x["service_code"])
        rows = "\n".join(
            f"| `{s['service_code']}` | {', '.join(sorted(s['domains']))} | "
            f"{s['featured_count']} | {s['catalog_count']} |"
            for s in svcs
        )
        readme = f"""# {label} (`{ind_slug}/`)

Service codes mapped to this industry prefix.

| Service code | Domains | Featured | Catalog |
|---|---|---:|---:|
{rows}

Featured scenarios are fully scaffolded with a 6-agent fleet under
`{{service-code}}/scenarios/{{scenario-id}}/agents/`. Catalog scenarios
appear only in `services/_registry.json` (zero scaffolding) until promoted.
"""
        write(ind_dir / "README.md", readme)

    # ---- Per-service-code scaffolds ----
    for scode, svc in services_index.items():
        ind_slug = svc["industry_slug"]
        svc_dir = SERVICES_ROOT / ind_slug / scode
        svc_dir.mkdir(parents=True, exist_ok=True)

        service_yaml = {
            "service_code": scode,
            "industry": ind_slug,
            "industry_label": svc["industry_label"],
            "domains": sorted(svc["domains"]),
            "scenarios": {
                "featured": svc["featured_count"],
                "catalog": svc["catalog_count"],
                "total": svc["featured_count"] + svc["catalog_count"],
            },
            "deployment": {
                "wave_strategy": "three-wave",
                "iac": "bicep",
                "module": f"infra/bicep/modules/service.bicep",
                "service_module": f"services/{ind_slug}/{scode}/bicep/main.bicep",
            },
            "agent_archetype": {
                "name": "hierarchical-root + sequential-with-hitl-gate",
                "fleet_size": 6,
                "roles": AGENT_ROLES,
            },
            "schemas_consumed": [],
            "personas": {
                "operator": "TBD — see scenarios/*/scenario.yaml",
                "hitl_approver": "TBD — Teams Adaptive Card gate",
            },
        }
        write(svc_dir / "service.yaml", yaml_dump(service_yaml))

        # Service-level Bicep
        write(svc_dir / "bicep" / "main.bicep", f"""// services/{ind_slug}/{scode}/bicep/main.bicep
// Service-level deployment for {scode}. Composes the canonical agent-fleet
// module with service-specific schemas, personas, and HITL policy.

targetScope = 'resourceGroup'

@description('APEX tenant slug (e.g., contoso-prod).')
param tenant string

@description('Wave being deployed: w1 | w2 | w3.')
@allowed([ 'w1', 'w2', 'w3' ])
param wave string

@description('Featured scenario IDs to deploy in this wave.')
param featuredScenarios array = []

@description('Container Apps environment resource ID.')
param containerAppsEnvId string

@description('Managed identity resource ID for agent runtime.')
param agentIdentityId string

var serviceCode = '{scode}'

module fleet '../../../../infra/bicep/modules/agent-fleet.bicep' = [
  for sid in featuredScenarios: {{
    name: 'fleet-${{sid}}'
    params: {{
      tenant: tenant
      serviceCode: serviceCode
      scenarioId: sid
      wave: wave
      containerAppsEnvId: containerAppsEnvId
      agentIdentityId: agentIdentityId
    }}
  }}
]

output serviceCode string = serviceCode
output deployedScenarios array = featuredScenarios
""")

        write(svc_dir / "bicep" / "agents.bicep", f"""// services/{ind_slug}/{scode}/bicep/agents.bicep
// Override hook for service-specific agent configuration.
// Default agent-fleet behavior is in infra/bicep/modules/agent-fleet.bicep.
// Add only the deltas (custom tools, custom prompts, custom HITL gates) here.

targetScope = 'resourceGroup'

@description('Tenant slug.')
param tenant string

@description('Scenario id this override applies to.')
param scenarioId string

// Add scenario-specific overrides below. Empty by default.
""")

    # ---- Featured-scenario full scaffolds ----
    for _, frow in featured.iterrows():
        sid = str(frow["Scenario ID"]).strip()
        scode = str(frow["Service"]).strip()
        title = str(frow["Title"]).strip()
        ind_slug, _ = industry_of(scode)
        scen_dir = SERVICES_ROOT / ind_slug / scode / "scenarios" / sid

        steps = chain_24_by_id.get(sid, [])
        scenario_yaml = {
            "scenario_id": sid,
            "title": title,
            "service_code": scode,
            "domain": str(frow["Domain"]).strip(),
            "featured": True,
            "moment": str(frow["Scenario (the moment)"]).strip(),
            "solution": str(frow["Solution (architectural approach)"]).strip(),
            "use_case": str(frow["Use Cases (decomposed)"]).strip() if "Use Cases (decomposed)" in frow else str(frow.get("Use Case (Wave 2 delivery)", "")).strip(),
            "service_productized": str(frow.get("Service (productized)", "")).strip(),
            "personas": str(frow.get("Persona (operator · HITL approver)", "")).strip(),
            "kpi": str(frow.get("KPI / Outcome", "")).strip(),
            "waves": {
                "w1_foundation": str(frow.get("W1 Foundation", "")).strip(),
                "w2_pilot": str(frow.get("W2 Pilot (you are here)", "")).strip(),
                "w3_scale_fuse": str(frow.get("W3 Scale & Fuse", "")).strip(),
            },
            "chain_24": [
                {
                    "step": s["step"],
                    "key": s["key"],
                    "title": s["title"],
                    "layer": s["layer"],
                    "kind": s["kind"],
                    "purpose": s["purpose"],
                }
                for s in sorted(steps, key=lambda x: x["step"])
            ],
            "agents": [
                {"role": role, "config": f"agents/{role}/agent.yaml"}
                for role in AGENT_ROLES
            ],
        }
        write(scen_dir / "scenario.yaml", yaml_dump(scenario_yaml))

        # 6 agent stubs
        for role in AGENT_ROLES:
            agent = {
                "role": role,
                "scenario_id": sid,
                "service_code": scode,
                "archetype": "hierarchical-root + sequential-with-hitl-gate",
                "model": "TBD",
                "tools": [],
                "schemas_read": [],
                "schemas_write": [],
                "hitl_gate": role in ("decide", "act"),
                "audit_row_emit": True,
                "prompt_ref": f"prompts/{role}.md",
            }
            write(scen_dir / "agents" / role / "agent.yaml", yaml_dump(agent))
            write(
                scen_dir / "agents" / role / "prompts" / f"{role}.md",
                f"# {role.title()} agent prompt — {sid}\n\nTBD\n",
            )

        # Scenario-level Bicep overlay (mostly empty; service-level handles core)
        write(scen_dir / "bicep" / "scenario.bicep", f"""// services/{ind_slug}/{scode}/scenarios/{sid}/bicep/scenario.bicep
// Scenario-level overlay — only define if the scenario needs more than the
// service-default agent fleet (e.g., custom MCP server, custom data fusion).

targetScope = 'resourceGroup'

@description('Tenant slug.')
param tenant string

// Scenario-specific resources go here. Empty by default.
""")

    # ---- Top-level services/README.md ----
    total_industries = len(INDUSTRY_PREFIX)
    total_services = len(services_index)
    total_scenarios = len(registry_scenarios)
    total_featured = sum(1 for s in registry_scenarios if s["featured"])

    readme = f"""# APEX Service Catalog

Source-of-truth folder structure for all APEX services and scenarios. Generated
from [`docs/reference/APEX-Scenario-Chains.xlsx`](../docs/reference/APEX-Scenario-Chains.xlsx)
via [`tools/gen_services_tree.py`](../tools/gen_services_tree.py). Re-run that
script after the spreadsheet changes.

## Counts

| | Count |
|---|---:|
| Industries | {total_industries} |
| Service codes | {total_services} |
| Total scenarios | {total_scenarios} |
| Featured (fully scaffolded) | {total_featured} |
| Catalog (registry stub only) | {total_scenarios - total_featured} |

## Layout

```
services/
  _registry.json                       # full index of every scenario
  rc/   axle/   er/   hls/   ice/   th/   tmt/
    {{SERVICE-CODE}}/                    # e.g. RC-E2E-03
      service.yaml                     # service contract
      bicep/
        main.bicep                     # deploys the service for a wave
        agents.bicep                   # service-level agent overrides
      scenarios/
        {{scenario-id}}/                 # featured only
          scenario.yaml                # 24-step chain
          agents/{{role}}/agent.yaml      # 6-agent fleet (assess→learn)
          agents/{{role}}/prompts/*.md
          bicep/scenario.bicep         # scenario overlay
```

Featured scenarios are fully scaffolded with a 6-agent fleet
(`assess`, `classify`, `quantify`, `decide`, `act`, `learn`). Catalog scenarios
live only in `_registry.json` until they are promoted to featured (which means
adding their scenario folder + agent fleet here).

## Industries

| Slug | Label | Service codes |
|---|---|---:|
""" + "\n".join(
        f"| `{slug}/` | {label} | {sum(1 for s in services_index.values() if s['industry_slug'] == slug)} |"
        for slug, label in sorted(INDUSTRY_PREFIX.values())
    ) + """

## Adding a service

1. Add the new `Service Code` row to the spreadsheet's *Scenario Library* sheet.
2. Re-run `python tools/gen_services_tree.py`.
3. Fill in the generated `service.yaml` (personas, schemas).
4. If the service should be deployable: edit `bicep/main.bicep` to compose the
   relevant `infra/bicep/modules/*` and add the service to the wizard registry
   at `apps/deploy-wizard/api/services_catalog.py`.

## Promoting a catalog scenario to featured

1. Mark `Featured?` = `⭐ Featured` in the spreadsheet.
2. Re-run the generator — agent fleet and `scenario.yaml` are scaffolded.
3. Replace the `TBD` placeholders in `agents/*/agent.yaml` with real config.

## Bicep ↔ Terraform

This tree generates **Bicep** modules. Existing Terraform modules under
`infra/terraform/` remain canonical for Fabric capacity, Key Vault, Container
App environments, and Purview (per the architecture book §10). The Bicep modules
under `infra/bicep/` and the per-service Bicep here layer on top — they deploy
*services and agent fleets* into resource groups already provisioned by
Terraform. The `apps/deploy-wizard/` control plane orchestrates both.
"""
    write(SERVICES_ROOT / "README.md", readme)

    print(f"OK  industries={total_industries}  services={total_services}  scenarios={total_scenarios}  featured={total_featured}")


if __name__ == "__main__":
    main()
