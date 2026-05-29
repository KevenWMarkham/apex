"""Build a standalone APEX-M source bundle.

Includes only what's needed to run APEX-M against in-process mocks
without cloning the full APEX monorepo:

  apex-m/                          full tree
  packages/apex-core/              workspace dep
  docs/guides/APEX-M-Local-Setup/  this handoff package
  README.md                        top-level pointer at the handoff

Excludes: caches, virtualenvs, build artifacts, __pycache__, .pyc, .pyo.

Output: docs/guides/APEX-M-Standalone-Bundle.tar.gz
"""
from __future__ import annotations

import io
import tarfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
OUT = REPO_ROOT / "docs" / "guides" / "APEX-M-Standalone-Bundle.tar.gz"

INCLUDE_TREES = [
    "apex-m",
    "packages/apex-core",
    "docs/guides/APEX-M-Local-Setup",
]

EXCLUDE_DIRS = {"__pycache__", ".venv", "venv", ".pytest_cache",
                ".mypy_cache", ".ruff_cache", "node_modules", ".git",
                "dist", "build", ".tox"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo", ".pyd", ".log", ".tmp"}

TOP_README = """# APEX-M · Standalone Bundle

This tarball contains the minimum slice of the APEX monorepo needed to
run APEX-M against in-process mock implementations on a developer laptop.

## What's here

```
apex-m/                          # APEX-M source + Bicep IaC
packages/apex-core/              # APEX-Core protocol definitions (workspace dep)
docs/guides/APEX-M-Local-Setup/  # Quickstart README + requirements.txt + .env.example
```

## Quickstart

```bash
# 1) Extract
tar -xzf APEX-M-Standalone-Bundle.tar.gz
cd APEX-M-Standalone-Bundle

# 2) Read the full setup guide
cat docs/guides/APEX-M-Local-Setup/README.md

# 3) Run the bash quickstart (uv-or-pip + mock agent)
./docs/guides/APEX-M-Local-Setup/run-local-mock.sh

# Or on Windows
.\\docs\\guides\\APEX-M-Local-Setup\\run-local-mock.ps1
```

## What you can NOT do with this bundle alone

- Run sibling variants (APEX-G, APEX-A) — not included
- Run the wizard's render endpoint — apps/deploy-wizard not included
- Run any other practice's MCP tools (RC, HLS, ICE, TH, AXLE) — not included
- Deploy to a real Azure tenant — requires the full repo + Bicep blueprints

For any of the above, clone the full repo from
https://github.com/Deloitte-US-Consulting/APEX

## Independence posture

Laptop substrate with `APEX_FORCE_MOCK=true` touches **no client cloud
subscription** and bills **no Microsoft / Google / AWS API call**.
Independence-clean by construction per `docs/apex-core/Independence-Posture.md`
in the full repo.

---

**Bundle version:** 1.0 · **Generated:** 2026-05-29
"""


def should_skip(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIRS:
        return True
    if path.suffix in EXCLUDE_SUFFIXES:
        return True
    return False


def add_tree(tar: tarfile.TarFile, src_root: Path, arc_root: str) -> int:
    """Walk src_root and add files to tar under arc_root/. Returns count."""
    count = 0
    for f in src_root.rglob("*"):
        if not f.is_file():
            continue
        rel = f.relative_to(src_root)
        if should_skip(rel):
            continue
        arcname = f"APEX-M-Standalone-Bundle/{arc_root}/{rel.as_posix()}"
        tar.add(str(f), arcname=arcname)
        count += 1
    return count


def main() -> None:
    if OUT.exists():
        OUT.unlink()

    counts = {}
    with tarfile.open(OUT, "w:gz", compresslevel=9) as tar:
        # --- Source trees ---
        for tree in INCLUDE_TREES:
            src = REPO_ROOT / tree
            if not src.exists():
                print(f"WARN: {tree} not found, skipping")
                continue
            counts[tree] = add_tree(tar, src, tree)
            print(f"  {tree}: {counts[tree]} files")

        # --- Top-level README pointer ---
        readme_bytes = TOP_README.encode("utf-8")
        info = tarfile.TarInfo("APEX-M-Standalone-Bundle/README.md")
        info.size = len(readme_bytes)
        info.mode = 0o644
        tar.addfile(info, io.BytesIO(readme_bytes))
        print(f"  README.md: 1 file")

    print(f"\nWrote {OUT}")
    print(f"Size: {OUT.stat().st_size:,} bytes "
          f"({OUT.stat().st_size / 1024:.1f} KB)")
    print(f"Total files: {sum(counts.values()) + 1}")


if __name__ == "__main__":
    main()
