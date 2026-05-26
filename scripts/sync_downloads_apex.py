"""Upload the latest version of each APEX-related artifact from
C:\\Users\\kmarkham\\Downloads to the apex-docs blob container under the
`downloads/` prefix.

Curation logic: explicit allow-list (below) of the LATEST version of each
artifact family. Skipped: older versions (e.g. v3/v4 when v5 exists),
duplicates with parenthetical or trailing-underscore-number suffixes,
Office lock files (~$), large media (webm/zip), and folder snapshots.

Idempotent: each upload is content-md5-compared against the existing blob
and skipped when unchanged.
"""
from __future__ import annotations

import base64
import hashlib
import os
import sys
from pathlib import Path

from azure.storage.blob import BlobServiceClient, ContentSettings

DOWNLOADS = Path(r"C:\Users\kmarkham\Downloads")
CONTAINER = "apex-docs"
PREFIX = "downloads/"

# ---------------------------------------------------------------------------
# Curated allow-list — LATEST version of each APEX-related artifact family.
# Organized by category. Update by adding to the relevant section.
# ---------------------------------------------------------------------------
FILES = [
    # === APEX Architecture (latest = v5) ===
    "APEX-Architecture-v5.docx",
    "APEX-Architecture-v5.pdf",

    # === APEX Design (latest = v3) ===
    "APEX-Design-v3.pptx",
    "APEX-Design-v3.pdf",
    "APEX-Design.md",
    "_apex_design_v3.md",   # markitdown extract of the v3 pptx

    # === APEX conceptual / design extensions ===
    "APEX-Agent-Intelligence-Design.md",
    "APEX-Conceptual-Gaps.md",
    "APEX-Live-Translation-Design.md",
    "APEX-Multimodal-Archival-Design.md",
    "APEX-Operating-Profiles-Design.md",
    "APEX-Vector-Cache-Integration.md",
    "APEX-VV-Temporal-Snapshot-Design.md",

    # === APEX marketing / positioning ===
    "APEX-Marketing-Playbook-Offshore-v1.docx",
    "APEX-Stacked-Architecture-Narrated.html",
    "APEX_ConCon_Architecture_Conformance_Email.md",
    "APEX_ConCon_Positioning.pptx",
    "APEX_Family_Positioning_9.pptx",     # latest positioning deck
    "APEX_Family_Positioning_7.pdf",      # latest PDF positioning export
    "APEX_Design_v1_Tool_Slides_18-21.pptx",

    # === APEX practice walkthroughs / one-pagers ===
    "APEX-RC-E2E-03-MVP-Walkthrough.docx",
    "APEX-TMT-MED-01-OnePager.html",
    "APEX-TMT-TEL-RAA-04-MVP-Walkthrough.docx",
    "APEX-TMT-TEL-RAA-04-OnePager.html",
    "APEX-M-Merchandising-Walkthrough.docx",
    "APEX-M-Merchandising-Walkthrough.pdf",

    # === APEX-M GSSC Lab ===
    "APEX-M-GSSC-Lab-Backlog.md",
    "APEX-M-GSSC-Lab-Infrastructure-Deployment.docx",
    "APEX-M-GSSC-Lab-Infrastructure-Deployment.pdf",

    # === APEX Agentic Merch cost / BOM ===
    "APEX-Agentic-Merch-Azure-Calculator-Estimate-Deloitte.xlsx",
    "APEX-Agentic-Merch-Azure-Calculator-Estimate.md",
    "APEX-Agentic-Merch-Azure-Calculator-Estimate.xlsx",
    "APEX-Agentic-Merch-Azure-Cost-Deloitte-Discounted.md",
    "APEX-Agentic-Merch-BOM.md",
    "APEX-Agentic-Merch-BOM.xlsx",
    "APEX-Agentic-Merch-MVP-Azure-Cost.md",
    "APEX-Agentic-Merch-MVP-Azure-Cost.xlsx",

    # === APEX other / inventory ===
    "apex_package.html",
    "apex-build-inventory-v2.html",

    # === APEX-adjacent Agentic Merch artifacts (latest of each) ===
    "Agentic Merchandising_vDRAFT.pptx",
    "Agentic Merchandising_vDRAFT.xlsx",
    "Agentic_Merch_ConCon_Response_to_Tom.md",
    "data_dictionary_Retail_AgenticMerch.xlsx",
]


def content_type(p: Path) -> str:
    ext = p.suffix.lower().lstrip(".")
    return {
        "md":   "text/markdown; charset=utf-8",
        "html": "text/html; charset=utf-8",
        "htm":  "text/html; charset=utf-8",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "pdf":  "application/pdf",
        "txt":  "text/plain; charset=utf-8",
    }.get(ext, "application/octet-stream")


def file_md5(p: Path) -> bytes:
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.digest()


def main() -> int:
    conn = os.environ.get("DEMO_STORAGE_CONN") or os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if not conn:
        print("ERROR: set DEMO_STORAGE_CONN and retry", file=sys.stderr)
        return 2
    svc = BlobServiceClient.from_connection_string(conn)
    cc = svc.get_container_client(CONTAINER)

    uploaded = 0
    skipped = 0
    missing = 0
    errored = 0
    total_bytes = 0
    for name in FILES:
        src = DOWNLOADS / name
        if not src.exists():
            print(f"  MISSING (skipped): {name}")
            missing += 1
            continue
        blob_name = PREFIX + name  # preserve original filename (spaces ok in blob name)
        bc = cc.get_blob_client(blob_name)
        local_md5 = file_md5(src)
        # Skip if unchanged
        try:
            props = bc.get_blob_properties()
            if props.content_settings.content_md5 == local_md5:
                skipped += 1
                continue
        except Exception:
            pass
        # Upload
        try:
            sz = src.stat().st_size
            with open(src, "rb") as f:
                bc.upload_blob(
                    f,
                    overwrite=True,
                    content_settings=ContentSettings(
                        content_type=content_type(src),
                        content_md5=local_md5,
                    ),
                )
            uploaded += 1
            total_bytes += sz
            print(f"  uploaded  {blob_name}  ({sz:,} bytes)")
        except Exception as exc:
            errored += 1
            print(f"  FAILED {name}: {exc}", file=sys.stderr)

    print(
        f"\nDone. uploaded={uploaded} skipped={skipped} missing={missing} errored={errored}  "
        f"total_uploaded={total_bytes / 1e6:.1f} MB"
    )
    return 0 if errored == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
