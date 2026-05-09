from fastapi import APIRouter, Query

from . import registry

router = APIRouter()


@router.get("/industries")
def list_industries() -> list[dict[str, str]]:
    return registry.industries()


@router.get("/services")
def list_services(industry: str | None = Query(default=None)) -> list[dict]:
    return registry.service_codes(industry=industry)


@router.get("/scenarios")
def list_scenarios(
    industry: str | None = Query(default=None),
    service_code: str | None = Query(default=None),
    domain: str | None = Query(default=None),
    featured_only: bool = Query(default=False),
) -> list[dict]:
    return registry.scenarios(
        industry=industry,
        service_code=service_code,
        domain=domain,
        featured_only=featured_only,
    )
