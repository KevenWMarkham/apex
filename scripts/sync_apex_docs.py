"""Sync local APEX docs to the `apex-docs` blob container.

Idempotent: each blob upload is compared against the file's md5 via the
blob's Content-MD5 metadata; unchanged files are skipped.

Usage:
  $env:DEMO_STORAGE_CONN = "<storage account connection string>"
  python scripts/sync_apex_docs.py

Source root: C:\\Stage\\Clients\\Industries\\APEX
Blob prefix: relative path under that root (e.g. docs/packs/CFMP-v0.2.md)
"""
from __future__ import annotations

import base64
import hashlib
import os
import sys
from pathlib import Path

from azure.storage.blob import BlobServiceClient, ContentSettings

ROOT = Path(r"C:\Stage\Clients\Industries\APEX")
CONTAINER = "apex-docs"
INCLUDE_EXTS = {".md", ".html", ".htm", ".docx", ".xlsx", ".pptx", ".pdf", ".yaml", ".yml", ".txt", ".json"}
# Don't recurse into noise — session transcripts, dependency caches, build
# artifacts, archive folders. These were polluting the APEX Library landing
# page (~1,734 .claude/ entries alone).
SKIP_DIR_PREFIXES = {
    ".git", ".venv", "node_modules", "__pycache__", "_archive",
    ".claude",            # Claude Code session history (transcripts, JSONL)
    ".next",              # Next.js build cache
    "dist", "build", "out",
    ".pytest_cache",
}
SKIP_FILE_PREFIXES = {"~$"}


def _content_type(path: Path) -> str:
    ext = path.suffix.lower().lstrip(".")
    return {
        "md":   "text/markdown; charset=utf-8",
        "html": "text/html; charset=utf-8",
        "htm":  "text/html; charset=utf-8",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "pdf":  "application/pdf",
        "yaml": "text/yaml; charset=utf-8",
        "yml":  "text/yaml; charset=utf-8",
        "txt":  "text/plain; charset=utf-8",
    }.get(ext, "application/octet-stream")


def _file_md5(path: Path) -> bytes:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.digest()


def _should_skip_dir(name: str) -> bool:
    n = name.lower()
    return any(n.startswith(p) for p in SKIP_DIR_PREFIXES)


def _should_skip_file(name: str) -> bool:
    return any(name.startswith(p) for p in SKIP_FILE_PREFIXES)


def walk_targets():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # in-place prune of skip dirs
        dirnames[:] = [d for d in dirnames if not _should_skip_dir(d)]
        for fname in filenames:
            if _should_skip_file(fname):
                continue
            p = Path(dirpath) / fname
            if p.suffix.lower() not in INCLUDE_EXTS:
                continue
            yield p


def main():
    conn = os.environ.get("DEMO_STORAGE_CONN") or os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    if not conn:
        print("ERROR: set DEMO_STORAGE_CONN (or AZURE_STORAGE_CONNECTION_STRING) and retry", file=sys.stderr)
        return 2
    svc = BlobServiceClient.from_connection_string(conn)
    cc = svc.get_container_client(CONTAINER)
    try:
        cc.create_container()
        print(f"created container: {CONTAINER}")
    except Exception:
        pass  # already exists

    uploaded = 0
    skipped = 0
    errored = 0
    for src in walk_targets():
        try:
            rel = src.relative_to(ROOT).as_posix()
        except ValueError:
            continue
        bc = cc.get_blob_client(rel)
        local_md5 = _file_md5(src)
        local_md5_b64 = base64.b64encode(local_md5).decode()

        # check existing
        try:
            props = bc.get_blob_properties()
            remote_md5 = props.content_settings.content_md5
            if remote_md5 == local_md5:
                skipped += 1
                continue
        except Exception:
            pass  # blob does not exist yet

        try:
            with open(src, "rb") as f:
                bc.upload_blob(
                    f,
                    overwrite=True,
                    content_settings=ContentSettings(
                        content_type=_content_type(src),
                        content_md5=local_md5,
                    ),
                )
            uploaded += 1
            if uploaded % 25 == 0:
                print(f"  ... uploaded {uploaded} files so far")
        except Exception as exc:
            errored += 1
            print(f"  FAILED {rel}: {exc}", file=sys.stderr)

    print(f"\nDone. uploaded={uploaded} skipped={skipped} errored={errored}")
    return 0 if errored == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
