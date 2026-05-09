from collections import defaultdict
from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .models import DeploymentRecord, DeploymentRequest

router = APIRouter()


class TreeSelection(BaseModel):
    """Selected node ids from the wizard treeview.

    Each id has a kind prefix:
      practice:{slug} · service:{code} · scenario:{id} · agent:{scenario}:{role}

    The render endpoint roll-up rule: a service is deployed if either the
    service node is selected, OR any of its scenarios/agents are selected.
    Scenarios and agents are deployed only if explicitly selected (or
    inherited from a selected parent).
    """
    selected_ids: list[str]
    tenant: str
    wave: Literal["w1", "w2", "w3"] = "w2"


class RenderedParameters(BaseModel):
    blueprint: str
    parameters: dict
    summary: dict


@router.post("/render", response_model=RenderedParameters)
def render_parameters(sel: TreeSelection) -> RenderedParameters:
    """Translate a treeview selection into a Bicep parameter file for the
    blueprint matching the chosen wave. The wizard previews this before the
    operator confirms `az deployment group create`.
    """
    practices: set[str] = set()
    services: set[str] = set()
    scenarios: set[str] = set()
    agents: dict[str, set[str]] = defaultdict(set)  # scenario_id -> {role}

    for raw in sel.selected_ids:
        if not raw or ":" not in raw:
            continue
        kind, _, rest = raw.partition(":")
        if kind == "practice":
            practices.add(rest)
        elif kind == "service":
            services.add(rest)
        elif kind == "scenario":
            scenarios.add(rest)
        elif kind == "agent":
            scenario_id, _, role = rest.partition(":")
            if scenario_id and role:
                agents[scenario_id].add(role)
                scenarios.add(scenario_id)

    if not (practices or services or scenarios or agents):
        raise HTTPException(status_code=400, detail="No selections provided")

    # Group scenarios by service code via the registry.
    # Only featured scenarios are deployable (they have an agent-fleet
    # scaffold on disk). Catalog stubs are filtered out unless explicitly
    # selected by scenario id.
    from . import registry
    reg = registry.load_registry()
    by_service: dict[str, list[str]] = defaultdict(list)
    for sc in reg["scenarios"]:
        sid = sc["scenario_id"]
        explicit = sid in scenarios
        inherited = sc["service_code"] in services or sc["industry_slug"] in practices
        if not (explicit or inherited):
            continue
        if not sc["featured"] and not explicit:
            # When inherited from a parent, filter to featured only.
            continue
        by_service[sc["service_code"]].append(sid)

    selections_param = [
        {
            "serviceCode": code,
            "featuredScenarios": sorted(set(sids)),
            "agentRoleOverrides": {
                sid: sorted(agents[sid]) for sid in sids if sid in agents and agents[sid]
            },
            "mcpServers": [],
        }
        for code, sids in sorted(by_service.items())
    ]

    # APEX-M Bicep blueprints. APEX-G and APEX-A would substitute Terraform
    # / CloudFormation modules at the same logical step.
    blueprint = {
        "w1": "apex-m/infra/bicep/blueprints/w1-foundation.bicep",
        "w2": "apex-m/infra/bicep/blueprints/w2-pilot.bicep",
        "w3": "apex-m/infra/bicep/blueprints/w3-scale-fuse.bicep",
    }[sel.wave]

    parameters = {
        "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
        "contentVersion": "1.0.0.0",
        "parameters": {
            "tenant": {"value": sel.tenant},
            "containerAppsEnvId": {"value": "REPLACE_WITH_LAYER1_OUTPUT"},
            "agentIdentityId": {"value": "REPLACE_WITH_LAYER1_OUTPUT"},
            "selections": {"value": selections_param},
        },
    }

    summary = {
        "wave": sel.wave,
        "tenant": sel.tenant,
        "practices_selected": sorted(practices),
        "service_count": len(by_service),
        "scenario_count": sum(len(v) for v in by_service.values()),
        "agent_role_filters": sum(len(v) for v in agents.values()),
    }

    return RenderedParameters(blueprint=blueprint, parameters=parameters, summary=summary)


@router.post("", response_model=DeploymentRecord)
def create_deployment(req: DeploymentRequest) -> DeploymentRecord:
    """Render Bicep parameters and kick off `az deployment group create`.

    TBD — see `bicep_runner.py`. Implementation will:
    1. Call /render to materialize the parameter file.
    2. Persist a DeploymentRecord (status=pending) to Cosmos.
    3. Run `az deployment group what-if`; attach diff to the record.
    4. Run `az deployment group create`; stream output; update record.
    5. After success, register agents with Agent Service per book §10.
    """
    raise HTTPException(status_code=501, detail="Not implemented — scaffold only")


@router.get("", response_model=list[DeploymentRecord])
def list_deployments(tenant: str | None = None) -> list[DeploymentRecord]:
    raise HTTPException(status_code=501, detail="Not implemented — scaffold only")


@router.get("/{deployment_id}", response_model=DeploymentRecord)
def get_deployment(deployment_id: str) -> DeploymentRecord:
    raise HTTPException(status_code=501, detail="Not implemented — scaffold only")
