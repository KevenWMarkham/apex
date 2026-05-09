from fastapi import APIRouter, Query

from . import registry

router = APIRouter()


@router.get("/industries")
def list_industries() -> list[dict[str, str]]:
    """Practices = industries — 7 of them per Deployment Guide §7.3."""
    return registry.industries()


@router.get("/practices")
def list_practices() -> list[dict[str, str]]:
    """Alias for /industries — the deployment guide calls them Practices."""
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


@router.get("/tree")
def get_tree(featured_only: bool = Query(default=True)) -> list[dict]:
    """Practice → Service → Scenario → Agent hierarchy for the wizard treeview.

    `featured_only=true` (default) returns only the 36 deployable scenarios.
    Each node carries a `status` field (planned / scaffolded / implemented /
    deployed / pilot / ga) sourced from the per-practice _build-status.yaml.
    """
    return registry.tree(featured_only=featured_only)


@router.get("/use-cases")
def list_use_cases(service: str | None = Query(default=None)) -> list[dict]:
    """List use cases under a service (or all services if `service` omitted).

    Each entry is the full use-case.yaml content plus `slug` and `path`.
    Phase 0.9: variant-aware via `primary_variant` field; per-tenant
    `client_approved_architecture` block declares adapter bindings.
    """
    return registry.load_use_cases(service_code=service)


@router.get("/adapters")
def list_adapters() -> list[str]:
    """Inventory of available APEX protocol adapters under
    packages/apex-adapters/.../protocol_adapters/. Wizard's render endpoint
    validates use-case adapter refs against this list."""
    return registry.list_known_adapters()


@router.get("/build-status")
def get_build_status(practice: str | None = Query(default=None)) -> dict:
    """Per-practice build plan with sprint orchestration. Read by the
    wizard's Roadmap page. Returns the raw YAML structure as JSON; pass
    `practice=rc` to fetch a single one.

    Each practice has a file at `services/<practice>/_build-status.yaml`.
    """
    plans = registry.load_build_status()
    if practice:
        if practice not in plans:
            return {"practices": [], "missing": practice}
        return {"practices": [plans[practice]]}
    return {"practices": list(plans.values())}
