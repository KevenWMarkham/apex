"""hlscml-mcp tool implementations — PHI-scoped clinical reads."""

from __future__ import annotations

from apex_core.types import Classification
from fabric_mcp import get_entity_by_key as _fabric_get_entity
from fabric_mcp import query_gold_view as _fabric_query_view
from mcp_common import ToolContract, traced_call

SERVER_NAME = "hlscml-mcp"
TOOL_VERSION = "1.0.0"
_REQUIRED_SCOPES = ["practice:hls"]


def get_patient_by_key(
    patient_key: str,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> dict:
    """Return the tokenised Patient canonical row."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.get_patient_by_key",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"patient_key": patient_key},
        classification_applied=[Classification.PHI],
    ) as ctx:
        row = _fabric_get_entity(
            "patient", patient_key,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = row
        return row


def list_observations_for_patient(
    patient_key: str,
    loinc_code: str | None = None,
    limit: int = 100,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """List observations for a patient; optionally filter by LOINC code."""
    filters: dict[str, object] = {"patient_key": patient_key}
    if loinc_code is not None:
        filters["loinc_code"] = loinc_code
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_observations_for_patient",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"patient_key": patient_key, "loinc_code": loinc_code, "limit": limit},
        classification_applied=[Classification.PHI],
    ) as ctx:
        rows = _fabric_query_view(
            "gold_hlscml.observation", filters, limit,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = rows
        return rows


def list_medications_for_patient(
    patient_key: str,
    limit: int = 50,
    *,
    agent_id: str = "unknown",
    caller_identity: str = "unknown",
) -> list[dict]:
    """List medication requests for a patient."""
    with traced_call(
        tool_name=f"{SERVER_NAME}.list_medications_for_patient",
        tool_version=TOOL_VERSION,
        agent_id=agent_id, caller_identity=caller_identity,
        parameters={"patient_key": patient_key, "limit": limit},
        classification_applied=[Classification.PHI],
    ) as ctx:
        rows = _fabric_query_view(
            "gold_hlscml.medication_request", {"patient_key": patient_key}, limit,
            agent_id=agent_id, caller_identity=caller_identity,
        )
        ctx["result"] = rows
        return rows


CONTRACTS: list[ToolContract] = [
    ToolContract(
        name=f"{SERVER_NAME}.get_patient_by_key", version=TOOL_VERSION,
        description="Return a tokenised HLSCML Patient by key.",
        classification_propagation=[Classification.PHI],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.list_observations_for_patient", version=TOOL_VERSION,
        description="List observations for a patient (optionally filtered by LOINC).",
        classification_propagation=[Classification.PHI],
        required_scopes=_REQUIRED_SCOPES,
    ),
    ToolContract(
        name=f"{SERVER_NAME}.list_medications_for_patient", version=TOOL_VERSION,
        description="List medication requests for a patient.",
        classification_propagation=[Classification.PHI],
        required_scopes=_REQUIRED_SCOPES,
    ),
]
