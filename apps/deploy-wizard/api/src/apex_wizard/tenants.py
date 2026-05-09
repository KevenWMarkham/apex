from fastapi import APIRouter, HTTPException

from .models import Tenant

router = APIRouter()


@router.get("", response_model=list[Tenant])
def list_tenants() -> list[Tenant]:
    raise HTTPException(status_code=501, detail="Not implemented — scaffold only")


@router.post("", response_model=Tenant)
def create_tenant(t: Tenant) -> Tenant:
    raise HTTPException(status_code=501, detail="Not implemented — scaffold only")


@router.get("/{slug}", response_model=Tenant)
def get_tenant(slug: str) -> Tenant:
    raise HTTPException(status_code=501, detail="Not implemented — scaffold only")
