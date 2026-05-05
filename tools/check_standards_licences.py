"""Per-package licence-file presence check — Sprint 20 Task 20.5.3.

Every ``packages/apex-standards-*/`` package must ship a
``LICENSE-ATTRIBUTION.md`` file. CI runs this scanner; exit 1 if any
package is missing the file.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REQUIRED_FILES: tuple[str, ...] = ("LICENSE-ATTRIBUTION.md",)


def find_standards_packages(root: Path) -> list[Path]:
    packages_dir = root / "packages"
    if not packages_dir.is_dir():
        return []
    return sorted(
        d for d in packages_dir.iterdir()
        if d.is_dir() and d.name.startswith("apex-standards-")
    )


def check_package(package_dir: Path) -> list[str]:
    issues: list[str] = []
    for required in REQUIRED_FILES:
        if not (package_dir / required).exists():
            issues.append(
                f"{package_dir.name}: missing required file {required!r}"
            )
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify every apex-standards-* package has its licence files."
    )
    parser.add_argument(
        "root", nargs="?", default=".",
        help="Workspace root (default: current directory).",
    )
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    packages = find_standards_packages(root)
    if not packages:
        print(f"warn: no apex-standards-* packages found under {root}")
        return 0

    all_issues: list[str] = []
    for pkg in packages:
        all_issues.extend(check_package(pkg))

    if not all_issues:
        print(f"OK — all {len(packages)} apex-standards-* packages have licence files")
        return 0

    for issue in all_issues:
        print(issue, file=sys.stderr)
    print(
        f"FAIL — {len(all_issues)} licence-file issue(s) across "
        f"{len(packages)} apex-standards-* package(s)",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
