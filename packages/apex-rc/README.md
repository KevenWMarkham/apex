# apex-rc

**APEX L3 Practice bundle — Retail & Consumer.**

This package binds the RC Practice's schemas (SCML, MERML, CXML), and will (in
later sprints) bind its agent catalogue and service catalogue.

- Sprint 2 (current): schema binding + `PracticeBundle` model + declarative manifest.
- Sprint 16: agent catalogue added.
- Sprint 17: service catalogue added.

## Usage

```python
from apex_rc import rc_bundle

bundle = rc_bundle()
print(bundle.practice)           # Practice.RC
print(bundle.entities["scml"])   # ['SKU', 'Location', 'Lot', ...]
print(bundle.standards)          # ['gs1-gtin', 'gs1-sscc', 'gs1-gln', ...]
```
