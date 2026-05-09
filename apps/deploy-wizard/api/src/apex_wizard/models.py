from typing import Literal

from pydantic import BaseModel, Field

Wave = Literal["w1", "w2", "w3"]


class Tenant(BaseModel):
    slug: str = Field(min_length=3, max_length=40, pattern=r"^[a-z0-9-]+$")
    azure_subscription_id: str
    resource_group: str
    region: str
    container_apps_env_id: str
    agent_identity_id: str


class ServiceSelection(BaseModel):
    service_code: str
    featured_scenarios: list[str] = []
    mcp_servers: list[dict] = []


class DeploymentRequest(BaseModel):
    tenant: str
    wave: Wave
    selections: list[ServiceSelection]
    operator: str
    note: str | None = None


class DeploymentRecord(BaseModel):
    id: str
    tenant: str
    wave: Wave
    selections: list[ServiceSelection]
    parameters_path: str
    blueprint_path: str
    bicep_what_if_summary: dict | None = None
    status: Literal["pending", "running", "succeeded", "failed", "rolled_back"]
    operator: str
    started_at: str
    completed_at: str | None = None
    audit_row_id: str | None = None


class HitlThreshold(BaseModel):
    tenant: str
    service_code: str
    scenario_id: str
    field: str
    operator_role: str
    threshold: float
