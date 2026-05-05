"""Bronze landing template — Custom Endpoint (webhook) (APEX_Design §6.2.5).

The "custom endpoint" pattern is an Azure Function / Container App that
accepts webhook payloads, verifies their HMAC signature, and writes them
through to OneLake via the OneLake SDK. Because this runs as a FastAPI / ASGI
app rather than a Fabric notebook, the file below is the *reference app
structure*, not a PySpark script.

A Fabric-side companion notebook (`notebooks/bronze/custom_endpoint_compaction.py`
in a later sprint) reads the small Delta files produced by the endpoint and
compacts them into Bronze.

Error semantics (§6.2.5): Function logs via App Insights. Failed ingests
dead-letter to a Service Bus queue for manual reprocessing.

Schema evolution: endpoint code enforces the payload schema; additive drift
passes; breaking changes return HTTP 400 and alert.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from apex_core.types import Classification, Practice
from apex_medallion import (
    BronzeLandingConfig,
    DeadLetterRecord,
    RetentionPolicy,
    SourcePattern,
)

if TYPE_CHECKING:  # pragma: no cover
    from fastapi import FastAPI, Request


def landing_config() -> BronzeLandingConfig:
    """CUSTOMIZE per webhook source."""
    return BronzeLandingConfig(
        source_system=os.environ["APEX_SOURCE_SYSTEM"],
        source_pattern=SourcePattern.CUSTOM_ENDPOINT,
        source_connection_name=os.environ["APEX_FUNCTION_NAME"],
        workspace_id=os.environ["FABRIC_WORKSPACE_ID"],
        lakehouse_id=os.environ["FABRIC_LAKEHOUSE_ID"],
        target_table=os.environ["APEX_BRONZE_TARGET"],
        practice=Practice(os.environ["APEX_PRACTICE"]),
        classification=Classification(os.environ.get("APEX_CLASSIFICATION", "internal")),
        retention=RetentionPolicy(),
        pattern_detail={
            "function_name": os.environ["APEX_FUNCTION_NAME"],
            "signature_header": os.environ.get("APEX_SIGNATURE_HEADER", "X-Signature"),
            "hmac_secret_env": os.environ.get("APEX_HMAC_SECRET_ENV", "APEX_HMAC_SECRET"),
            "deadletter_queue": os.environ.get("APEX_DEADLETTER_QUEUE", "apex-bronze-dlq"),
        },
    )


def verify_signature(body: bytes, signature: str | None, secret: str) -> bool:
    """Verify an HMAC-SHA256 signature header."""
    if not signature:
        return False
    expected = hmac.new(
        secret.encode("utf-8"), body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


def build_bronze_row(
    config: BronzeLandingConfig,
    *,
    raw_body: bytes,
    entity_id: str,
    run_id: str,
) -> dict[str, object]:
    """Assemble the Bronze row dict that will be written to OneLake."""
    now = datetime.now(UTC)
    return {
        "event_id": str(uuid4()),
        "event_ts": now.isoformat(),
        "entity_id": entity_id,
        "source_system": config.source_system,
        "source_system_ts": now.isoformat(),
        "ingest_ts": now.isoformat(),
        "ingest_date": now.date().isoformat(),
        "run_id": run_id,
        "_raw_payload": raw_body.decode("utf-8", errors="replace"),
        "_classification": config.classification.value,
    }


def to_deadletter_record(
    config: BronzeLandingConfig,
    *,
    raw_body: bytes,
    error: Exception,
    run_id: str,
) -> DeadLetterRecord:
    """Assemble a ``DeadLetterRecord`` when the endpoint can't accept a payload."""
    return DeadLetterRecord(
        source_system=config.source_system,
        source_pattern=config.source_pattern.value,
        target_table=config.target_table,
        occurred_at=datetime.now(UTC),
        error_class=type(error).__name__,
        error_message=str(error),
        retry_count=0,
        payload_raw=raw_body.decode("utf-8", errors="replace"),
        run_id=run_id,
    )


def create_app(config: BronzeLandingConfig) -> "FastAPI":
    """Construct the webhook FastAPI app. Deploy to Azure Functions / Container Apps."""
    from fastapi import FastAPI, HTTPException, Request

    app = FastAPI(title=f"APEX Webhook — {config.source_system}")
    secret = os.environ[config.pattern_detail["hmac_secret_env"]]
    sig_header = config.pattern_detail["signature_header"]

    @app.post("/v1/ingest")
    async def ingest(request: Request) -> dict[str, str]:
        body = await request.body()
        signature = request.headers.get(sig_header)
        if not verify_signature(body, signature, secret):
            raise HTTPException(status_code=401, detail="signature invalid")
        try:
            payload = json.loads(body)
            entity_id = str(payload.get("id", uuid4()))
            run_id = request.headers.get("X-Run-Id", str(uuid4()))
            row = build_bronze_row(config, raw_body=body, entity_id=entity_id, run_id=run_id)
            _write_to_onelake(config, row)
            return {"status": "accepted", "run_id": run_id}
        except Exception as exc:  # noqa: BLE001 — anything unparseable → dead-letter
            _emit_deadletter(config, body, exc, run_id=str(uuid4()))
            raise HTTPException(status_code=400, detail=f"ingest-failed: {exc}") from exc

    return app


def _write_to_onelake(config: BronzeLandingConfig, row: dict[str, object]) -> None:
    """Write a single row via the OneLake SDK (deferred — stub in Sprint 4)."""
    # Real impl (Sprint 5): use `azure-storage-file-datalake` + Delta append.
    # For Sprint 4 we only ship the structure; the SDK call is provided by the
    # operator's deployment.
    _ = config, row


def _emit_deadletter(
    config: BronzeLandingConfig,
    body: bytes,
    error: Exception,
    *,
    run_id: str,
) -> None:
    """Send a failed payload to the Service Bus dead-letter queue (deferred)."""
    dlr = to_deadletter_record(config, raw_body=body, error=error, run_id=run_id)
    _ = dlr  # Sprint 5: write to Service Bus via azure-servicebus SDK
