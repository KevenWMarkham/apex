from fastapi import APIRouter, HTTPException

from .models import DeploymentRecord, DeploymentRequest

router = APIRouter()


@router.post("", response_model=DeploymentRecord)
def create_deployment(req: DeploymentRequest) -> DeploymentRecord:
    """Render Bicep parameters and kick off `az deployment group create`.

    TBD — see `bicep_runner.py`. The endpoint contract is settled:
    - Validate tenant exists.
    - For each selection, validate service code + scenario ids against
      services/_registry.json.
    - Render parameter file under `apps/deploy-wizard/parameters/`.
    - Run blueprint matching the wave: w1-foundation | w2-pilot | w3-scale-fuse.
    - Persist DeploymentRecord to Cosmos.
    """
    raise HTTPException(status_code=501, detail="Not implemented — scaffold only")


@router.get("", response_model=list[DeploymentRecord])
def list_deployments(tenant: str | None = None) -> list[DeploymentRecord]:
    raise HTTPException(status_code=501, detail="Not implemented — scaffold only")


@router.get("/{deployment_id}", response_model=DeploymentRecord)
def get_deployment(deployment_id: str) -> DeploymentRecord:
    raise HTTPException(status_code=501, detail="Not implemented — scaffold only")
