---
description: Run the pack acceptance test pack against the current pack.
---

You are validating the pack against its acceptance criteria.

## Steps
1. Detect the current pack from cwd.
2. Run pytest against `packs/<industry>/tests/`.
3. Report:
   - Total tests
   - Passing
   - Failing
   - Skipped
4. For each failure, surface the manifest line that caused it.

## Exit criteria
All 60+ acceptance tests must pass before the pack can advance to Deploy phase.
