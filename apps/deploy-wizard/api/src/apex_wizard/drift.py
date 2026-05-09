from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/{tenant}")
def drift_report(tenant: str) -> dict:
    """Run Bicep `what-if` against the pinned release manifest and return
    divergence as a structured diff. Per Professional-APEX §3792 a daily cron
    job calls this and writes any divergence to apex_drift_log + Teams alert.
    """
    raise HTTPException(status_code=501, detail="Not implemented — scaffold only")
