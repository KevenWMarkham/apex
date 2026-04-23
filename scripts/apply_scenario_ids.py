"""Rename every scenario folder to include a globally unique ID prefix.

New pattern: <PRACTICE>/<domain-slug>/<PRACTICE>-<DOMCODE>-<NN>-<slug>/
Example:     RC/supply-chain/RC-SUPCHN-01-cold-chain-excursion-store-cooler/

The triplet PRACTICE-DOMCODE-NN is a globally unique ID. Searching for
"RC-SUPCHN-01" in the file tree jumps straight to the one folder.

After rename: rebuilds indexes via rebuild_scenario_indexes.py logic.
Safe to run repeatedly (idempotent — skips folders already prefixed).
"""

from __future__ import annotations

import io
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path("docs/scenarios")

PRACTICES = ["RC", "HLS", "ER", "AXLE", "TMT", "TH", "ICE"]
DOMAIN_CODES = {
    "clinical-care":          "CLIN",
    "network-infrastructure": "NET",
    "engineering-rd":         "ENG",
    "supply-chain":           "SUPCHN",
    "asset-maintenance":      "ASSET",
    "quality-compliance":     "QUAL",
    "risk-fraud-security":    "RISK",
    "pricing-revenue":        "PRICE",
    "customer-experience":    "CX",
    "marketing-growth":       "MKTG",
    "operations-workforce":   "OPS",
    "channel-partner-dealer": "CHAN",
    "other":                  "OTHER",
}

renamed = 0
already_prefixed = 0
skipped = 0

for p in PRACTICES:
    prac_dir = ROOT / p
    if not prac_dir.exists():
        continue
    for domain_dir in prac_dir.iterdir():
        if not domain_dir.is_dir() or domain_dir.name.startswith("_"):
            continue
        if domain_dir.name not in DOMAIN_CODES:
            continue
        code = DOMAIN_CODES[domain_dir.name]
        for scenario in sorted(domain_dir.iterdir()):
            if not scenario.is_dir():
                continue
            name = scenario.name
            # Already prefixed?
            if name.startswith(f"{p}-{code}-"):
                already_prefixed += 1
                continue
            # Expected legacy pattern: NN-slug
            m = re.match(r"^(\d{2,3})-(.+)$", name)
            if not m:
                skipped += 1
                print(f"  ! Skipping (unexpected name): {scenario}")
                continue
            idx = int(m.group(1))
            slug = m.group(2)
            new_name = f"{p}-{code}-{idx:02d}-{slug}"
            new_path = domain_dir / new_name
            if new_path.exists():
                skipped += 1
                print(f"  ! Collision: {new_path} already exists")
                continue
            shutil.move(str(scenario), str(new_path))
            renamed += 1

print(f"\nRenamed:          {renamed}")
print(f"Already prefixed: {already_prefixed}")
print(f"Skipped:          {skipped}")
print(f"\nRebuilding indexes ...")

# Run the index rebuilder so paths reflect new names
subprocess.run(
    [sys.executable, "scripts/rebuild_scenario_indexes.py"],
    check=True,
)
