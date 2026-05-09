# APEX UC Harness Implementation Plan

> ⚠️ **DEPRECATED 2026-05-07** — superseded by `Merch/MVP/docs/plans/2026-05-07-mvp-test-harness-plan.md`.
> Wrong scope (13 cross-industry scenarios) and wrong location (`APEX/packages/`). Use the MVP-side plan that targets the 20 UCs from `mvp-scope-q1-usecases.xlsx` and lands at `Merch/MVP/TestHarness/`.

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a localhost web tool that lets a developer select any of 17 cataloged use cases and step through it phase-by-phase, with each step's inputs/outputs/assertions journaled to disk and visible in the UI.

**Architecture:** New Python package `apex-uc-harness` in the APEX workspace. A generic `StepEngine` executes phases declared in per-UC `steps.yaml` files; phases dispatch to typed executors (`agent_call`, `sor_seed`, `python_call`, `http_call`, `assert_only`). All state journaled to `.uc-runs/<run_id>/` so any step can be re-run from a prior step's saved state. FastAPI + Jinja + HTMX UI on `127.0.0.1`; same engine drives a `apex uc-harness run` CLI.

**Tech Stack:** Python 3.11, Pydantic v2, FastAPI, Uvicorn, Jinja2, HTMX 2, Tailwind (CDN), pytest, Testcontainers (via reused `apex-test-harness`), polyfactory (transitive).

**Source design doc:** `docs/plans/2026-05-07-apex-uc-harness-design.md`

**Estimated build:** 3-4 weeks across 4 phases, ~60 tasks. Each phase ends with a demo-able milestone.

---

## Pre-work — Worktree + repo orientation

### Task 0.1: Verify workspace state

**Goal:** Confirm APEX workspace is clean and `apex-test-harness` + `apex-agentic-merch` are buildable before starting.

**Step 1:** From `C:\Stage\Clients\Industries\APEX\`, run:
```bash
git status
uv sync --all-packages
uv run pytest packages/apex-test-harness -q --no-header
```

**Expected:** Clean working tree; sync succeeds; existing harness tests pass (or are explicitly skipped).

**Step 2:** Confirm package directories exist:
```bash
ls packages/apex-test-harness packages/apex-agentic-merch
```

**Expected:** Both directories present. If `apex-agentic-merch` is not yet built, that's fine — its `steps.yaml` files come in Phase 4 and the executor stubs out to mock callables until then.

**Step 3:** Use `superpowers:using-git-worktrees` to create an isolated worktree for this build:
```bash
git worktree add ../APEX-uc-harness -b feature/uc-harness
cd ../APEX-uc-harness
```

**Step 4:** Commit
```bash
git commit --allow-empty -m "chore: start uc-harness build in isolated worktree"
```

---

## Phase 1 — Foundation (Week 1)

**Milestone:** Empty package compiles, Pydantic spec models load a real `steps.yaml`, discovery walks both roots and produces a catalog. `apex uc-harness list` prints the catalog. CI green.

### Task 1.1: Scaffold the package

**Files:**
- Create: `packages/apex-uc-harness/pyproject.toml`
- Create: `packages/apex-uc-harness/README.md`
- Create: `packages/apex-uc-harness/src/apex_uc_harness/__init__.py`
- Create: `packages/apex-uc-harness/src/apex_uc_harness/_version.py`

**Step 1:** Write `pyproject.toml` with the dependency block from §1 of the design + `[tool.uv.sources]` pointing `apex-core`, `apex-test-harness`, `apex-agentic-merch` to workspace paths.

**Step 2:** Write `__init__.py`:
```python
from apex_uc_harness._version import __version__

__all__ = ["__version__"]
```

**Step 3:** Write `_version.py`: `__version__ = "0.1.0"`

**Step 4:** Sync and verify import:
```bash
uv sync --all-packages
uv run python -c "import apex_uc_harness; print(apex_uc_harness.__version__)"
```
Expected: `0.1.0`

**Step 5:** Commit
```bash
git add packages/apex-uc-harness/
git commit -m "feat(uc-harness): scaffold package"
```

### Task 1.2: Spec models — `ExpectSpec` (start with the leaf)

**Files:**
- Create: `packages/apex-uc-harness/src/apex_uc_harness/spec/__init__.py`
- Create: `packages/apex-uc-harness/src/apex_uc_harness/spec/schema.py`
- Create: `packages/apex-uc-harness/tests/__init__.py`
- Create: `packages/apex-uc-harness/tests/unit/__init__.py`
- Create: `packages/apex-uc-harness/tests/unit/spec/__init__.py`
- Create: `packages/apex-uc-harness/tests/unit/spec/test_schema.py`

**Step 1: Write the failing test**
```python
# tests/unit/spec/test_schema.py
from apex_uc_harness.spec.schema import ExpectSpec

def test_expect_spec_equals_kind():
    spec = ExpectSpec(assert_="equals", path="ranking[0].category", value="Apparel")
    assert spec.assert_ == "equals"
    assert spec.path == "ranking[0].category"
    assert spec.value == "Apparel"
```

**Step 2: Run, expect ImportError**
```bash
uv run pytest packages/apex-uc-harness/tests/unit/spec/test_schema.py::test_expect_spec_equals_kind -v
```
Expected: FAIL — `ModuleNotFoundError: No module named 'apex_uc_harness.spec.schema'`

**Step 3: Implement minimal**
```python
# src/apex_uc_harness/spec/schema.py
from typing import Any, Literal
from pydantic import BaseModel, Field

AssertKind = Literal[
    "equals", "range", "count", "contains",
    "schema_match", "ledger_row", "hash_chain_valid",
    "regex", "not_empty",
]

class ExpectSpec(BaseModel):
    model_config = {"populate_by_name": True, "extra": "forbid"}
    assert_: AssertKind = Field(alias="assert")
    path: str | None = None
    value: Any | None = None
    min: float | None = None
    max: float | None = None
    kind: str | None = None
```

**Step 4: Run, expect PASS**
```bash
uv run pytest packages/apex-uc-harness/tests/unit/spec/test_schema.py -v
```

**Step 5: Commit**
```bash
git add packages/apex-uc-harness/src/apex_uc_harness/spec packages/apex-uc-harness/tests
git commit -m "feat(uc-harness): ExpectSpec model"
```

### Task 1.3: Spec models — `StepSpec`

**Files:**
- Modify: `packages/apex-uc-harness/src/apex_uc_harness/spec/schema.py`
- Modify: `packages/apex-uc-harness/tests/unit/spec/test_schema.py`

**Step 1: Write the failing test**
```python
def test_step_spec_minimal():
    from apex_uc_harness.spec.schema import StepSpec, ExpectSpec
    spec = StepSpec(
        id="1-analyst",
        title="The Analyst ranks exceptions",
        kind="agent_call",
        using="apex_agentic_merch.runtime.analyst.run",
        expect=[ExpectSpec(assert_="equals", path="ranking[0].category", value="Apparel")],
    )
    assert spec.id == "1-analyst"
    assert spec.kind == "agent_call"
    assert len(spec.expect) == 1

def test_step_spec_rejects_unknown_kind():
    from apex_uc_harness.spec.schema import StepSpec
    import pytest
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        StepSpec(id="x", title="x", kind="not_a_real_kind", using="x")
```

**Step 2: Run — expect FAIL on import.**

**Step 3: Implement**
```python
# Append to spec/schema.py
StepKind = Literal["agent_call", "sor_seed", "python_call", "http_call", "assert_only", "drop_schema"]

class StepSpec(BaseModel):
    model_config = {"extra": "forbid"}
    id: str
    title: str
    kind: StepKind
    using: str | None = None
    inputs: dict[str, Any] | None = None
    inputs_from: str | None = None
    only_if: str | None = None
    fixtures: list[str] | None = None
    expect: list[ExpectSpec] = Field(default_factory=list)
```

**Step 4: Run — PASS.**

**Step 5: Commit**
```bash
git commit -am "feat(uc-harness): StepSpec model with kind validation"
```

### Task 1.4: Spec models — `UcSpec` (top-level)

**Files:**
- Modify: `packages/apex-uc-harness/src/apex_uc_harness/spec/schema.py`
- Modify: `packages/apex-uc-harness/tests/unit/spec/test_schema.py`

**Step 1: Write the failing test**
```python
def test_uc_spec_full():
    from apex_uc_harness.spec.schema import UcSpec
    spec = UcSpec(
        id="merch.fixture-2-demand",
        title="Apparel Wk-16 — Demand Branch",
        domain="agentic-merch",
        version=1,
        steps=[],
    )
    assert spec.id == "merch.fixture-2-demand"
    assert spec.version == 1

def test_uc_spec_rejects_unknown_version():
    from apex_uc_harness.spec.schema import UcSpec
    import pytest
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        UcSpec(id="x", title="x", domain="x", version=99, steps=[])
```

**Step 2-4: Implement, run.**
```python
class UcSpec(BaseModel):
    model_config = {"extra": "forbid"}
    id: str
    title: str
    domain: str
    version: Literal[1]
    description: str | None = None
    setup: list[StepSpec] = Field(default_factory=list)
    teardown: list[StepSpec] = Field(default_factory=list)
    steps: list[StepSpec]
```

**Step 5: Commit**
```bash
git commit -am "feat(uc-harness): UcSpec top-level model"
```

### Task 1.5: YAML loader with helpful errors

**Files:**
- Create: `packages/apex-uc-harness/src/apex_uc_harness/spec/loader.py`
- Create: `packages/apex-uc-harness/tests/unit/spec/test_loader.py`
- Create: `packages/apex-uc-harness/tests/fixtures/yaml/valid_minimal.yaml`
- Create: `packages/apex-uc-harness/tests/fixtures/yaml/invalid_kind.yaml`

**Step 1: Author test fixtures**

`valid_minimal.yaml`:
```yaml
id: test.minimal
title: Minimal valid UC
domain: test
version: 1
steps:
  - id: only-step
    title: do nothing
    kind: assert_only
    expect: []
```

`invalid_kind.yaml`:
```yaml
id: test.invalid
title: Bad kind
domain: test
version: 1
steps:
  - id: bad
    title: bad
    kind: fhir_call
    expect: []
```

**Step 2: Write the failing tests**
```python
# tests/unit/spec/test_loader.py
from pathlib import Path
import pytest
from apex_uc_harness.spec.loader import load_uc_spec, UcLoadError

FIX = Path(__file__).parent.parent.parent / "fixtures" / "yaml"

def test_load_valid_minimal():
    spec = load_uc_spec(FIX / "valid_minimal.yaml")
    assert spec.id == "test.minimal"
    assert spec.steps[0].kind == "assert_only"

def test_load_invalid_kind_raises():
    with pytest.raises(UcLoadError) as ei:
        load_uc_spec(FIX / "invalid_kind.yaml")
    assert "fhir_call" in str(ei.value)
    assert "line" in str(ei.value).lower() or "step" in str(ei.value).lower()
```

**Step 3: Implement**
```python
# spec/loader.py
from pathlib import Path
import yaml
from pydantic import ValidationError
from apex_uc_harness.spec.schema import UcSpec

class UcLoadError(Exception):
    def __init__(self, path: Path, message: str):
        super().__init__(f"{path}: {message}")
        self.path = path
        self.message = message

def load_uc_spec(path: Path) -> UcSpec:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        raise UcLoadError(path, f"YAML parse error: {e}") from e
    try:
        return UcSpec.model_validate(raw)
    except ValidationError as e:
        raise UcLoadError(path, f"schema validation: {e}") from e
```

**Step 4: Run, expect PASS.**

**Step 5: Commit**
```bash
git add packages/apex-uc-harness/src/apex_uc_harness/spec/loader.py packages/apex-uc-harness/tests/
git commit -m "feat(uc-harness): YAML loader with line-aware errors"
```

### Task 1.6: Discovery — `scan(roots)` → `[CatalogEntry]`

**Files:**
- Create: `packages/apex-uc-harness/src/apex_uc_harness/discovery.py`
- Create: `packages/apex-uc-harness/tests/unit/test_discovery.py`
- Create: `packages/apex-uc-harness/tests/fixtures/roots/root_a/uc1/steps.yaml`
- Create: `packages/apex-uc-harness/tests/fixtures/roots/root_b/sub/uc2/steps.yaml`
- Create: `packages/apex-uc-harness/tests/fixtures/roots/root_b/broken/steps.yaml`

**Step 1: Author 3 fixture UCs** (1 in root_a, 2 in root_b nested, one of which is broken).

**Step 2: Write failing test**
```python
# tests/unit/test_discovery.py
from pathlib import Path
from apex_uc_harness.discovery import scan, CatalogEntry

ROOTS = Path(__file__).parent.parent / "fixtures" / "roots"

def test_scan_finds_all_steps_yaml():
    entries = scan([ROOTS / "root_a", ROOTS / "root_b"])
    ids = sorted(e.uc_code for e in entries)
    assert "test.uc1" in ids
    assert "test.uc2" in ids
    # broken one shows up but with load_error set
    broken = [e for e in entries if e.spec is None]
    assert len(broken) == 1
    assert broken[0].load_error is not None

def test_scan_collision_raises():
    import pytest
    from apex_uc_harness.discovery import DuplicateUcCodeError
    # configure two roots that both contain a UC with the same id
    with pytest.raises(DuplicateUcCodeError):
        scan([ROOTS / "root_a", ROOTS / "root_a"])
```

**Step 3: Implement**
```python
# src/apex_uc_harness/discovery.py
from dataclasses import dataclass
from pathlib import Path
from apex_uc_harness.spec.loader import load_uc_spec, UcLoadError
from apex_uc_harness.spec.schema import UcSpec

@dataclass(frozen=True)
class CatalogEntry:
    spec: UcSpec | None
    source_path: Path
    domain: str
    uc_code: str
    title: str
    load_error: str | None

class DuplicateUcCodeError(Exception): ...

def scan(roots: list[Path]) -> list[CatalogEntry]:
    entries: list[CatalogEntry] = []
    seen: dict[str, Path] = {}
    for root in roots:
        for yaml_path in sorted(root.rglob("steps.yaml")):
            try:
                spec = load_uc_spec(yaml_path)
            except UcLoadError as e:
                entries.append(CatalogEntry(
                    spec=None, source_path=yaml_path,
                    domain="unknown", uc_code=yaml_path.parent.name,
                    title=yaml_path.parent.name,
                    load_error=str(e),
                ))
                continue
            if spec.id in seen:
                raise DuplicateUcCodeError(f"{spec.id} in both {seen[spec.id]} and {yaml_path}")
            seen[spec.id] = yaml_path
            entries.append(CatalogEntry(
                spec=spec, source_path=yaml_path,
                domain=spec.domain, uc_code=spec.id, title=spec.title,
                load_error=None,
            ))
    return entries
```

**Step 4: Run — PASS.**

**Step 5: Commit**
```bash
git commit -am "feat(uc-harness): catalog discovery across multiple roots"
```

### Task 1.7: `UcCatalog` aggregator

**Files:**
- Modify: `packages/apex-uc-harness/src/apex_uc_harness/discovery.py`
- Create: `packages/apex-uc-harness/tests/unit/test_catalog.py`

**Step 1: Write failing test**
```python
def test_catalog_groups_by_domain():
    from pathlib import Path
    from apex_uc_harness.discovery import scan, UcCatalog
    entries = scan([Path(__file__).parent.parent / "fixtures" / "roots" / "root_a"])
    catalog = UcCatalog(entries)
    grouped = catalog.by_domain()
    assert "test" in grouped
    assert any(e.uc_code == "test.uc1" for e in grouped["test"])

def test_catalog_get_returns_entry():
    from pathlib import Path
    from apex_uc_harness.discovery import scan, UcCatalog
    entries = scan([Path(__file__).parent.parent / "fixtures" / "roots" / "root_a"])
    catalog = UcCatalog(entries)
    entry = catalog.get("test.uc1")
    assert entry.uc_code == "test.uc1"
```

**Step 2-4: Implement on `UcCatalog`, run, PASS.**

**Step 5: Commit**
```bash
git commit -am "feat(uc-harness): UcCatalog aggregator (by_domain, get)"
```

### Task 1.8: CLI scaffold + `list` subcommand

**Files:**
- Create: `packages/apex-uc-harness/src/apex_uc_harness/_cli.py`
- Modify: `packages/apex-uc-harness/pyproject.toml` (add `[project.scripts]`)
- Create: `packages/apex-uc-harness/tests/unit/test_cli.py`

**Step 1: Write failing test using Typer's `CliRunner`**
```python
from typer.testing import CliRunner
from apex_uc_harness._cli import app
from pathlib import Path

def test_cli_list_prints_catalog(tmp_path, monkeypatch):
    # author one steps.yaml in tmp_path, configure roots via env var
    (tmp_path / "uc1").mkdir()
    (tmp_path / "uc1" / "steps.yaml").write_text(
        "id: t.cli\ntitle: cli test\ndomain: t\nversion: 1\nsteps:\n  - {id: a, title: a, kind: assert_only, expect: []}\n"
    )
    monkeypatch.setenv("APEX_UC_HARNESS_ROOTS", str(tmp_path))
    result = CliRunner().invoke(app, ["list"])
    assert result.exit_code == 0
    assert "t.cli" in result.stdout
```

**Step 2: Run — FAIL.**

**Step 3: Implement minimal Typer CLI:**
```python
# _cli.py
import os
from pathlib import Path
import typer
from apex_uc_harness.discovery import scan, UcCatalog

app = typer.Typer(help="APEX UC Harness")

def _roots() -> list[Path]:
    raw = os.environ.get("APEX_UC_HARNESS_ROOTS", "")
    return [Path(p).resolve() for p in raw.split(os.pathsep) if p]

@app.command()
def list() -> None:
    """List all UCs found across configured roots."""
    catalog = UcCatalog(scan(_roots()))
    for domain, entries in catalog.by_domain().items():
        typer.echo(f"=== {domain} ===")
        for e in entries:
            mark = "✓" if e.spec else "⚠"
            typer.echo(f"  {mark} {e.uc_code:40s} {e.title}")
```

Add to `pyproject.toml`:
```toml
[project.scripts]
"apex-uc-harness" = "apex_uc_harness._cli:app"
```

**Step 4: Run — PASS.**

**Step 5: Commit**
```bash
git commit -am "feat(uc-harness): CLI scaffold + list command"
```

### Task 1.9: Phase 1 milestone — wire it together end-to-end

**Step 1:** From repo root, run:
```bash
uv sync --all-packages
APEX_UC_HARNESS_ROOTS="docs/scenarios" uv run apex-uc-harness list
```
Expected: prints whatever `steps.yaml` files exist in `docs/scenarios` (likely zero this early; that's fine — tests prove the wiring).

**Step 2:** Run the full unit suite:
```bash
uv run pytest packages/apex-uc-harness/tests/unit -v
```
Expected: all green.

**Step 3:** Commit milestone tag (annotated):
```bash
git tag -a uc-harness-week-1 -m "Phase 1 complete: spec + loader + discovery + CLI list"
```

---

## Phase 2 — Engine + state journaling (Week 2)

**Milestone:** `apex uc-harness run <uc-id>` runs a real end-to-end UC headlessly using `assert_only` and `python_call` executors. Every step's I/O journaled under `.uc-runs/<run_id>/`. CLI prints a markdown report at the end.

### Task 2.1: `RunStore` — create + manifest

**Files:**
- Create: `packages/apex-uc-harness/src/apex_uc_harness/runtime/__init__.py`
- Create: `packages/apex-uc-harness/src/apex_uc_harness/runtime/state.py`
- Create: `packages/apex-uc-harness/tests/unit/runtime/__init__.py`
- Create: `packages/apex-uc-harness/tests/unit/runtime/test_state.py`

**Step 1: Write failing test**
```python
def test_create_run_writes_manifest(tmp_path):
    from apex_uc_harness.runtime.state import RunStore
    from apex_uc_harness.spec.schema import UcSpec
    spec = UcSpec(id="t.x", title="x", domain="t", version=1, steps=[])
    store = RunStore(root=tmp_path)
    run_id = store.create_run(spec)
    manifest = (tmp_path / run_id / "run.json")
    assert manifest.exists()
    data = manifest.read_text()
    assert "t.x" in data
    assert run_id in data
```

**Step 2: FAIL.**

**Step 3: Implement.** ID format `r-YYYYMMDD-HHMMSS-<rand4>`. Manifest has `uc_id`, `run_id`, `started_at`, `trace_id`.

**Step 4: PASS.**

**Step 5: Commit.**

### Task 2.2: `RunStore.write_step` + `read_step`

**Files:**
- Modify: `packages/apex-uc-harness/src/apex_uc_harness/runtime/state.py`
- Modify: `packages/apex-uc-harness/tests/unit/runtime/test_state.py`

**Step 1: Failing test** for `write_step` (creates `<step_idx>-<step_id>/{inputs,outputs,result}.json` + optional `step.log`, `ledger.jsonl`) and `read_step` round-trip.

**Step 2-4: Implement, run, PASS.**

**Step 5: Commit.**

### Task 2.3: `RunStore.state_at` (the rewind primitive)

**Step 1: Failing test** that creates a run with 3 written steps, then `state_at(run_id, before_step_idx=2)` returns a dict containing `steps.<id-0>.outputs` and `steps.<id-1>.outputs` but not step 2.

**Step 2-4: Implement, run, PASS.**

**Step 5: Commit.**

### Task 2.4: `RunStore.fork`

**Step 1: Failing test** that creates a run with 4 steps written, then `fork(run_id, from_step_idx=2)` returns new run_id whose directory contains steps 0,1 (copied verbatim) and 2,3 absent.

**Step 2-4: Implement (use `shutil.copytree` for individual step dirs), run, PASS.**

**Step 5: Commit.**

### Task 2.5: Per-run lock file

**Step 1: Failing test** — opening two `RunStore.lock(run_id)` context managers raises on the second.

**Step 2-4: Implement using `filelock`, run, PASS.**

**Step 5: Commit.**

### Task 2.6: Assertion kind — `equals`

**Files:**
- Create: `packages/apex-uc-harness/src/apex_uc_harness/assertions/__init__.py`
- Create: `packages/apex-uc-harness/src/apex_uc_harness/assertions/kinds.py`
- Create: `packages/apex-uc-harness/tests/unit/test_assertions.py`

**Step 1: Failing test**
```python
def test_equals_pass():
    from apex_uc_harness.assertions.kinds import run_assertion
    from apex_uc_harness.spec.schema import ExpectSpec
    result = run_assertion(
        ExpectSpec(assert_="equals", path="a.b", value=42),
        outputs={"a": {"b": 42}},
    )
    assert result.ok is True

def test_equals_fail_with_diff():
    from apex_uc_harness.assertions.kinds import run_assertion
    from apex_uc_harness.spec.schema import ExpectSpec
    result = run_assertion(
        ExpectSpec(assert_="equals", path="a.b", value=42),
        outputs={"a": {"b": 99}},
    )
    assert result.ok is False
    assert "99" in result.actual_repr
    assert "42" in result.expected_repr
```

**Step 2-4: Implement** (`AssertionResult` dataclass + dispatcher + `equals` impl using JSONPath via `jsonpath-ng`).

**Step 5: Commit.**

### Task 2.7: Assertion kinds — `range`, `count`, `contains`, `not_empty`, `regex`

One commit per kind, each with pass+fail tests. Five tasks of identical shape. Reuses the dispatcher from 2.6.

### Task 2.8: Assertion kinds — `schema_match`

**Step 1: Failing test** that asserts an output dict matches an importable Pydantic model (`schema_match: apex_agentic_merch.schemas.IntentDiagnosis`).

**Step 2-4: Implement** (importlib resolves the dotted path; `model_validate` is the check).

**Step 5: Commit.**

### Task 2.9: Assertion kinds — `ledger_row`, `hash_chain_valid`

**Step 1: Failing test** against a synthetic in-memory LEDGER stub (a list of dicts written by an executor).

**Step 2-4: Implement** (read `ledger.jsonl` from current step's dir; check at least one row matches; for `hash_chain_valid`, recompute SHA256 chain across the full run's `ledger.jsonl` files).

**Step 5: Commit.**

### Task 2.10: Templating — Jinja with `StrictUndefined`

**Files:**
- Create: `packages/apex-uc-harness/src/apex_uc_harness/runtime/templating.py`
- Create: `packages/apex-uc-harness/tests/unit/runtime/test_templating.py`

**Step 1: Failing test**
```python
def test_resolve_run_var():
    from apex_uc_harness.runtime.templating import resolve
    out = resolve("{{run.trace_id}}", {"run": {"trace_id": "trc-1"}})
    assert out == "trc-1"

def test_resolve_step_outputs():
    from apex_uc_harness.runtime.templating import resolve
    out = resolve(
        "{{steps.s1.outputs.a}}",
        {"steps": {"s1": {"outputs": {"a": 42}}}},
    )
    assert out == "42"   # Jinja stringifies; engine handles type coercion separately

def test_strict_undefined_typo_raises():
    from apex_uc_harness.runtime.templating import resolve
    import pytest
    from jinja2 import UndefinedError
    with pytest.raises(UndefinedError):
        resolve("{{run.tarce_id}}", {"run": {"trace_id": "x"}})

def test_resolve_dict_recursively():
    from apex_uc_harness.runtime.templating import resolve_dict
    out = resolve_dict(
        {"trace_id": "{{run.trace_id}}", "tenant": "appretl"},
        {"run": {"trace_id": "trc-1"}},
    )
    assert out == {"trace_id": "trc-1", "tenant": "appretl"}
```

**Step 2-4: Implement.**

**Step 5: Commit.**

### Task 2.11: Executor registry

**Files:**
- Create: `packages/apex-uc-harness/src/apex_uc_harness/runtime/registry.py`
- Create: `packages/apex-uc-harness/tests/unit/runtime/test_registry.py`

**Step 1: Failing test**
```python
def test_register_and_dispatch():
    from apex_uc_harness.runtime.registry import ExecutorRegistry, ExecutorContext
    reg = ExecutorRegistry()
    @reg.register("toy")
    def toy_executor(ctx: ExecutorContext) -> dict:
        return {"echoed": ctx.inputs}
    out = reg.dispatch("toy", ExecutorContext(inputs={"x": 1}, step=None, run=None))
    assert out == {"echoed": {"x": 1}}

def test_unknown_kind_raises():
    from apex_uc_harness.runtime.registry import ExecutorRegistry, ExecutorContext, UnknownExecutorError
    import pytest
    reg = ExecutorRegistry()
    with pytest.raises(UnknownExecutorError):
        reg.dispatch("nope", ExecutorContext(inputs={}, step=None, run=None))
```

**Step 2-4: Implement.**

**Step 5: Commit.**

### Task 2.12: Executor — `assert_only`

**Files:**
- Create: `packages/apex-uc-harness/src/apex_uc_harness/executors/__init__.py`
- Create: `packages/apex-uc-harness/src/apex_uc_harness/executors/assert_only.py`

**Step 1: Failing test** — registered as `"assert_only"`, returns the accumulated step state unchanged.

**Step 2-4: Implement (one-liner: returns `ctx.run.accumulated_state`).**

**Step 5: Commit.**

### Task 2.13: Executor — `python_call`

**Step 1: Failing test** — `using: "tests.fixtures.callables.echo"` with `inputs: {x: 1}` returns `{"echoed": {"x": 1}}`.

**Step 2-4: Implement** (`importlib.import_module` + `getattr` + call with `**inputs`).

**Step 5: Commit.**

### Task 2.14: `StepEngine.run_step` (the heart)

**Files:**
- Create: `packages/apex-uc-harness/src/apex_uc_harness/runtime/engine.py`
- Create: `packages/apex-uc-harness/tests/unit/runtime/test_engine.py`

**Step 1: Failing test** — `StepEngine.run_step(uc_spec, step_idx=0, run_id, store, registry)` resolves templating → runs executor → runs assertions → writes inputs.json/outputs.json/result.json → returns `StepResult`.

**Step 2-4: Implement.** Pseudocode:
```python
def run_step(self, uc, step_idx, run_id):
    step = (uc.setup + uc.steps + uc.teardown)[step_idx]
    state = self.store.state_at(run_id, before_step_idx=step_idx)
    if step.only_if and not eval_only_if(step.only_if, state):
        # write skipped result
        return StepResult(skipped=True, ...)
    inputs = resolve_inputs(step, state)
    with capture_logs() as logs:
        try:
            outputs = self.registry.dispatch(step.kind, ExecutorContext(...))
        except Exception as e:
            outputs = None
            error = e
    assertions = [run_assertion(e, outputs or {}) for e in step.expect]
    self.store.write_step(run_id, step_idx, StepPayload(inputs, outputs, assertions, logs, ...))
    return StepResult(...)
```

**Step 5: Commit.**

### Task 2.15: `StepEngine.run_uc` (run all steps headlessly)

**Step 1: Failing test** — runs a fixture UC with 3 `assert_only` steps + 1 `python_call`, end-to-end, returns a `RunResult` with all 4 step outcomes.

**Step 2-4: Implement.** Stops at first failed step unless `force=True`.

**Step 5: Commit.**

### Task 2.16: Markdown report writer

**Files:**
- Create: `packages/apex-uc-harness/src/apex_uc_harness/reporting/__init__.py`
- Create: `packages/apex-uc-harness/src/apex_uc_harness/reporting/markdown.py`
- Create: `packages/apex-uc-harness/tests/unit/test_reporting.py`

**Step 1: Failing test** — given a RunResult, `write_markdown_report(run_dir)` produces `report.md` matching the §6.2 design doc shape (header, table, totals).

**Step 2-4: Implement.**

**Step 5: Commit.**

### Task 2.17: JSON report writer

Identical shape to 2.16, machine-readable JSON.

### Task 2.18: CLI `run` subcommand

**Step 1: Failing test** using `CliRunner` against a fixture UC.

**Step 2-4: Implement** `apex uc-harness run <uc-id>`. Loads catalog, finds spec, creates run via `RunStore`, executes via `StepEngine.run_uc`, writes both reports, prints summary line.

**Step 5: Commit.**

### Task 2.19: Phase 2 milestone

Run a real end-to-end:
```bash
APEX_UC_HARNESS_ROOTS=packages/apex-uc-harness/tests/fixtures/roots \
  uv run apex-uc-harness run test.uc1
```
Expected: prints summary, writes `.uc-runs/<run_id>/report.md`. Tag:
```bash
git tag -a uc-harness-week-2 -m "Phase 2 complete: engine + state journal + CLI run"
```

---

## Phase 3 — Real executors + Web UI (Week 3)

**Milestone:** Open `http://127.0.0.1:8765`, see catalog, click a UC, click "Run next step" through the 6 Merch agent chain steps, see green/red on each. Re-run from any step works. Fork from any step works. `agent_call` and `sor_seed` executors functional.

### Task 3.1: Executor — `agent_chain`

**Files:**
- Create: `packages/apex-uc-harness/src/apex_uc_harness/executors/agent_chain.py`
- Create: `packages/apex-uc-harness/tests/unit/executors/test_agent_chain.py`

**Step 1: Failing test** — given `using: "apex_agentic_merch.runtime.analyst.run"` (mock the import), executor calls it with `**inputs`, captures any LEDGER rows the agent emits to the run's `ledger.jsonl`, returns the agent's structured output.

**Step 2-4: Implement.** Reuse `python_call` import logic; thin LEDGER capture wrapper around `apex_audit.LedgerWriter`.

**Step 5: Commit.**

### Task 3.2: Executor — `sor_seed` (reuses `apex-test-harness`)

**Files:**
- Create: `packages/apex-uc-harness/src/apex_uc_harness/executors/sor_seed.py`
- Create: `packages/apex-uc-harness/tests/integration/executors/test_sor_seed.py` (Testcontainers-backed)

**Step 1: Failing test** — pytest marker `@pytest.mark.integration`. Spins up `PostgresContainerFixture`, calls executor with `using: apex_test_harness.bronze_rc` and a fixture-callable returning 5 rows, asserts `SELECT COUNT(*) FROM bronze_rc` returns 5.

**Step 2-4: Implement.** Executor receives ctx with a `postgres_schema` already created by run setup; calls the named `using` callable to import a `SorSimulator` instance; calls `seed_rows`.

**Step 5: Commit.**

### Task 3.3: Executor — `http_call`

**Step 1: Failing test** using `respx` to mock `httpx.AsyncClient`. Step config: `kind: http_call, using: GET https://example.test/api, expect.value: {ok: true}`.

**Step 2-4: Implement** with `httpx`.

**Step 5: Commit.**

### Task 3.4: Executor — `drop_schema` (teardown)

Trivial — calls `PostgresContainerFixture.drop_schema(schema_name)`. One-task TDD cycle.

### Task 3.5: FastAPI app skeleton + `/healthz`

**Files:**
- Create: `packages/apex-uc-harness/src/apex_uc_harness/ui/__init__.py`
- Create: `packages/apex-uc-harness/src/apex_uc_harness/ui/server.py`
- Create: `packages/apex-uc-harness/src/apex_uc_harness/ui/routes.py`
- Create: `packages/apex-uc-harness/tests/integration/ui/test_server.py`

**Step 1: Failing test** using `httpx.AsyncClient` with FastAPI's lifespan:
```python
async def test_healthz_returns_200():
    from apex_uc_harness.ui.server import build_app
    app = build_app(catalog=..., store=...)
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/healthz")
    assert r.status_code == 200
```

**Step 2-4: Implement** `build_app(catalog, store, registry, templates_dir, static_dir)` factory and `/healthz`.

**Step 5: Commit.**

### Task 3.6: Templates infrastructure (Jinja + base.html + HTMX)

**Files:**
- Create: `packages/apex-uc-harness/src/apex_uc_harness/ui/templates/base.html`
- Create: `packages/apex-uc-harness/src/apex_uc_harness/ui/templates/_macros.html`
- Create: `packages/apex-uc-harness/src/apex_uc_harness/ui/static/styles.css`

**Step 1:** No test — just author the base template with HTMX 2 + Tailwind + Highlight.js CDN includes. Minimal CSS reset in `styles.css`.

**Step 2: Test the includes** with a `/healthz`-style template render assertion.

**Step 3: Commit.**

### Task 3.7: Catalog page (`GET /`)

**Files:**
- Create: `packages/apex-uc-harness/src/apex_uc_harness/ui/templates/catalog.html`
- Modify: `routes.py`

**Step 1: Failing test** — `GET /` returns 200 with HTML containing every UC in the catalog grouped by domain, status badges shown.

**Step 2-4: Implement.**

**Step 5: Commit.**

### Task 3.8: UC detail page (`GET /uc/{uc_code}`)

**Step 1: Failing test** — returns 200 with steps list, recent runs, "Start new run" button.

**Step 2-4: Implement.** "Recent runs" sourced from `RunStore.list_runs(uc_id=uc_code)`.

**Step 5: Commit.**

### Task 3.9: Run start endpoint (`POST /uc/{uc_code}/run`)

**Step 1: Failing test** — POST creates a new run dir + manifest, redirects (303) to `/runs/{run_id}`.

**Step 2-4: Implement.**

**Step 5: Commit.**

### Task 3.10: Stepper page (`GET /runs/{run_id}`)

**Step 1: Failing test** — renders two-column layout with step list (left) + initially-empty details panel (right).

**Step 2-4: Implement.**

**Step 5: Commit.**

### Task 3.11: Step execute endpoint (`POST /runs/{run_id}/step/{n}/execute`)

**Step 1: Failing test** — POST runs step n, writes journal, returns HTML fragment containing the updated details panel + updated step badge.

**Step 2-4: Implement.** Returns HTMX-friendly partial; the page swaps it into `#details-panel` and `#step-{n}-badge` via `hx-swap-oob`.

**Step 5: Commit.**

### Task 3.12: Step inspect endpoint (`GET /runs/{run_id}/step/{n}`)

Read-only view of journaled state. One-task TDD cycle.

### Task 3.13: Re-run from step (`POST /runs/{run_id}/step/{n}/rerun`)

**Step 1: Failing test** — given a 6-step run that's all green, POST rerun on step 4 → step 4 re-executes; steps 5, 6 marked stale (`~` badge) without re-running.

**Step 2-4: Implement.** Calls `state_at(run_id, n)` then runs step n. Marks subsequent steps stale by writing a `stale: true` field to their `result.json`.

**Step 5: Commit.**

### Task 3.14: Fork run (`POST /runs/{run_id}/fork?from=N`)

**Step 1: Failing test** — POST fork from step 3 → new run_id, new dir contains copies of steps 0..2, redirects to new run's stepper.

**Step 2-4: Implement** using `RunStore.fork`.

**Step 5: Commit.**

### Task 3.15: "Run all remaining" (`POST /runs/{run_id}/run-all`)

**Step 1: Failing test** — runs every pending step until completion or first failure.

**Step 2-4: Implement** as a loop over single-step execution. Returns the final run summary partial.

**Step 5: Commit.**

### Task 3.16: View `steps.yaml` source (`GET /uc/{uc_code}/source`)

Returns the raw YAML inside a `<pre>` for the modal. One task.

### Task 3.17: View final report (`GET /runs/{run_id}/report`)

Returns the markdown report rendered via `markdown-it-py`. One task.

### Task 3.18: CLI `serve` subcommand

**Step 1: Failing test** that imports `_cli.serve` and asserts it can be invoked without raising during config (use a port-finding helper to avoid binding).

**Step 2-4: Implement** — Uvicorn programmatic launch on `127.0.0.1:8765`.

**Step 5: Commit.**

### Task 3.19: Phase 3 milestone

Manual verification (UI is the deliverable):
```bash
uv run apex-uc-harness serve
# open http://127.0.0.1:8765 in browser
```
Walk through: catalog → pick a fixture UC → start run → run next step ×3 → re-run from step 1 → fork from step 2.

Tag:
```bash
git tag -a uc-harness-week-3 -m "Phase 3 complete: web UI + real executors"
```

---

## Phase 4 — UC inventory + reports + smoke (Week 4)

**Milestone:** All 17 production UCs have authored `steps.yaml`. `apex uc-harness report --all` runs every UC headlessly and produces a catalog-wide pass/fail summary. Smoke tests cover the two real Merch fixtures.

### Task 4.1: Author `merch.fixture-1-supply` `steps.yaml`

**Files:**
- Create: `packages/apex-agentic-merch/src/apex_agentic_merch/data/ucs/fixture-1-supply/steps.yaml`

**Step 1:** Read `2026-05-05-agentic-merch-q1-mvp-design.md` §3 to confirm the supply-branch chain.

**Step 2:** Author 7-step `steps.yaml` (setup → 5 agents → teardown; Pricer skipped via `only_if`).

**Step 3:** Run via CLI:
```bash
uv run apex-uc-harness run merch.fixture-1-supply
```
Expected: green if `apex-agentic-merch` runtime exists; otherwise the failing assertions tell you exactly which agent's contract isn't met yet.

**Step 4: Commit**
```bash
git commit -am "feat(uc-harness): merch.fixture-1-supply steps.yaml"
```

### Task 4.2-4.4: Author the other 3 Merch fixtures

Same shape as 4.1 — one task per fixture, each ending in a commit.

### Task 4.5-4.17: Author the 13 scenario `steps.yaml` files

**One task per scenario UC.** For each:

**Step 1:** Read the scenario's existing `README.md` (e.g., `docs/scenarios/RC/customer-experience/RC-CX-01-loyalty-churn-prediction-winback/README.md`) to extract the intended phases.

**Step 2:** Author `docs/scenarios/.../<UC>/steps.yaml`. For phases without real implementations, use `python_call` against `apex_uc_harness.stubs.<uc_code>.<phase>` (a stub module returning canned data — author the stub in the same task).

**Step 3:** Run the UC via CLI; iterate on assertions until green against the stub.

**Step 4:** Commit.

Per task: ~30 minutes (most of the time is reading the README and shaping plausible phases). Total: ~6 hours of authoring across the 13 scenarios.

### Task 4.18: Catalog-wide CLI `report --all`

**Step 1: Failing test** — runs all UCs in a fixture catalog headlessly, produces a summary file with per-UC status.

**Step 2-4: Implement** `apex uc-harness report --all` that loops over the catalog and writes `.uc-runs/catalog-report-<timestamp>.md`.

**Step 5: Commit.**

### Task 4.19: Smoke tests in pytest

**Files:**
- Create: `packages/apex-uc-harness/tests/integration/test_real_ucs.py`

**Step 1: Failing test** marked `@pytest.mark.smoke`:
```python
@pytest.mark.smoke
def test_merch_fixture_1_supply_runs_clean():
    from apex_uc_harness.discovery import scan, UcCatalog
    from apex_uc_harness.runtime.engine import StepEngine
    # ... catalog → spec → engine.run_uc → assert all green
```

**Step 2-4: Implement.**

**Step 5: Commit.**

### Task 4.20: README + runbook

**Files:**
- Modify: `packages/apex-uc-harness/README.md`
- Create: `docs/uc-harness-runbook.md`

**Step 1:** Author README covering install, CLI commands, web UI launch, where reports land.

**Step 2:** Author runbook covering how to add a new UC (`steps.yaml` template + assertion-kind cheatsheet).

**Step 3:** Commit.

### Task 4.21: Phase 4 milestone — catalog-wide green

```bash
uv run apex-uc-harness report --all
cat .uc-runs/catalog-report-*.md | tail -30
```
Expected: every one of the 17 UCs reports PASS.

```bash
uv run pytest packages/apex-uc-harness -m "smoke or not smoke" -v
```
Expected: full unit suite + smoke green.

Tag:
```bash
git tag -a uc-harness-v0.1.0 -m "v0.1.0: 17 UCs, web UI + CLI, full report green"
```

---

## Verification before declaring done

Use **superpowers:verification-before-completion** before claiming this plan is complete.

Required green signals:
- [ ] `uv run pytest packages/apex-uc-harness -v` — unit + integration green
- [ ] `uv run pytest packages/apex-uc-harness -m smoke -v` — smoke green
- [ ] `uv run apex-uc-harness list` — prints all 17 UCs without parse errors
- [ ] `uv run apex-uc-harness report --all` — every UC reports PASS
- [ ] Manual web UI verification: catalog renders → UC detail renders → run a UC step-by-step → re-run from step → fork from step → final report opens
- [ ] CI lane (if added): `harness-uc` workflow green on a PR

When all check, request review with **superpowers:requesting-code-review**, then finish via **superpowers:finishing-a-development-branch**.

---

## Notes on TDD discipline

Every implementation task follows the cycle:
1. Write the failing test FIRST.
2. Run it — confirm RED with the *expected* failure mode (not a typo'd import).
3. Write the minimal code to make it pass.
4. Run — confirm GREEN.
5. Commit.

If a task is too big to fit this cycle in 5 minutes, split it. Refer to **superpowers:test-driven-development** when in doubt.

## Notes on commits

Commit per task. Use Conventional Commits prefix: `feat(uc-harness):`, `test(uc-harness):`, `refactor(uc-harness):`, `docs(uc-harness):`. Co-author tag is automatic per Claude Code conventions.

## Notes on YAGNI

Things explicitly NOT to build in this plan, even if they feel close at hand:
- Pytest plugin that adapts `steps.yaml` to parametrized tests
- Conformance markers
- Diff view between two runs
- Real-time log streaming (websockets)
- Auto-rescan via `watchdog`
- Playwright UI tests
- Auth, CSRF, anything beyond `127.0.0.1` binding

These all belong to a hypothetical v0.2 — see §8 of the design doc.
