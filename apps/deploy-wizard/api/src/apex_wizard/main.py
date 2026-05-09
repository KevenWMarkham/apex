from fastapi import FastAPI

from . import catalog, deployments, drift, hitl, tenants

app = FastAPI(title="APEX Deploy Wizard", version="0.1.0")
app.include_router(catalog.router, prefix="/api/catalog", tags=["catalog"])
app.include_router(tenants.router, prefix="/api/tenants", tags=["tenants"])
app.include_router(deployments.router, prefix="/api/deployments", tags=["deployments"])
app.include_router(drift.router, prefix="/api/drift", tags=["drift"])
app.include_router(hitl.router, prefix="/api/hitl", tags=["hitl"])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
