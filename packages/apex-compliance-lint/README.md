# apex-compliance-lint

**Sprint 29 Task 29.9.** Standalone APEX compliance linter — Independence-language
+ typography + brand rules across HTML / Markdown / DOCX / PPTX artifacts.

## Install

```bash
pip install -e packages/apex-compliance-lint              # core (HTML, MD)
pip install -e packages/apex-compliance-lint[docx]        # add DOCX support
pip install -e packages/apex-compliance-lint[pptx]        # add PPTX support
pip install -e packages/apex-compliance-lint[docx,pptx]   # all formats
```

## CLI

```bash
apex-compliance-lint path/to/artifact.html
apex-compliance-lint docs/  --severity warning
apex-compliance-lint a.md b.html  --pack deloitte_microsoft_independence
```

Exit codes:

- `0` — clean (no errors)
- `1` — at least one ERROR-severity violation
- `2` — config error (unknown pack, malformed input, no files matched)

## Rule packs (Sprint 29 §29.9.3)

| Pack id | Description | Severity |
|---------|-------------|----------|
| `deloitte_microsoft_independence` | Forbidden Independence-language: partner / alliance / partnership / endorsed / "Microsoft jointly" / Gold-Partner / etc. | ERROR |
| `apex_typography` | Prose mentions of fonts outside the design-token registry | WARNING |
| `apex_brand` | "black box" / "fully autonomous" / "guarantees" outcome language / etc. | mixed |

Rule packs are configurable. Tenants extending beyond Deloitte-Microsoft
import the `Rule` / `RulePack` types and ship their own packs without
touching the core engine.

## File adapters (Sprint 29 §29.9.2)

| Extension | Adapter | Dependency |
|-----------|---------|------------|
| `.html` `.htm` | `HTMLAdapter` | stdlib only |
| `.md` `.markdown` | `MarkdownAdapter` | stdlib only |
| `.docx` | `DOCXAdapter` | `python-docx` (optional) — falls back to stdlib zipfile + ElementTree |
| `.pptx` | `PPTXAdapter` | `python-pptx` (optional) — falls back to stdlib zipfile + ElementTree |

## Library API

```python
from apex_compliance_lint import (
    DEFAULT_PACKS, default_registry, lint_paths,
)
from pathlib import Path

report = lint_paths(
    [Path("docs/some-artifact.md"), Path("apex-workspace/CHARTER.md")],
    adapter_registry=default_registry(),
    packs=list(DEFAULT_PACKS),
)
print(f"errors: {len(report.errors)}, warnings: {len(report.warnings)}")
for v in report.errors:
    print(f"{v.file}:{v.line}:{v.column} [{v.rule_id}] {v.matched_text}")
```

## Cross-references

- `apex-workspace/APEX-CORE.md` §7 (hard limit #8 — Independence language)
- `apex-workspace/CHARTER.md` §6 (Independence language operationalized)
- Sprint 29 Task 29.10 — pre-publish CI lane wires this linter into the GitHub Actions workflow
- Appendix N (Sprint 29 Task 29.2) — design-system reference + Independence linguistic rules + approved-substitute table
