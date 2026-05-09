from fastapi import APIRouter, HTTPException

from .models import HitlThreshold

router = APIRouter()


@router.get("", response_model=list[HitlThreshold])
def list_thresholds(tenant: str | None = None) -> list[HitlThreshold]:
    raise HTTPException(status_code=501, detail="Not implemented — scaffold only")


@router.put("", response_model=HitlThreshold)
def upsert_threshold(t: HitlThreshold) -> HitlThreshold:
    """Persist threshold to Cosmos and write the secret to Key Vault under
    `apex-hitl-{tenant}-{service}-{scenario}-{field}`. Agents read from Key
    Vault at decision time, so updates take effect on next decision."""
    raise HTTPException(status_code=501, detail="Not implemented — scaffold only")
