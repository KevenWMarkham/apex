# APEX Test Harness — Schema Validation Pre-Fabric

**Date:** 2026-04-21
**Status:** Design approved. Implementation plan to follow.
**Scope:** A self-contained Python package that validates APEX Practice schemas against synthetic data served from a PostgreSQL container, before any Fabric investment.

---

## Purpose

Build confidence that the Pydantic entities shipped across APEX Practice packages will correctly parse, classify, and tokenise the data shapes real source systems will hand us — using a laptop-local PostgreSQL container as a stand-in for a downstream SOR. The harness must be runnable on a developer laptop and in CI, with zero Fabric dependency.

**Success criterion:** when the harness passes cleanly against `apex-rc` (and, in wave 2, the other Practices), we have empirical evidence that the schema layer is solid, and we can commit to multi-week Fabric setup work knowing the entity contracts hold.

---

## Constraints locked during brainstorm

| # | Decision point | Choice |
|---|---|---|
| 1 | Validation depth | **B** — shape + classifications + tokenisation (no SCD2 / drift / translators in MVP) |
| 2 | Practice scope for pilot | **A** — `apex-rc` only (SCML + MERML + CXML composed) |
| 3 | Postgres table shape | **C** — JSONB payload + 5-field envelope columns (matches Bronze in Fabric) |
| 4 | Data generation | **C** — hybrid: YAML fixtures for happy path + edge cases; polyfactory-derived generators for volume |
| 5 | Runtime | **A** — pytest + Testcontainers (throwaway Postgres per session) |
| 6 | Package location | **A** — new workspace package `apex-test-harness` |
| arch | Internal architecture | **Layered** — reusable library half + per-Practice test suites |

---

## Section 1 — Architecture at a glance

### Package layout

```
packages/apex-test-harness/
  pyproject.toml
  README.md
  src/apex_test_harness/
    __init__.py
    containers.py        PostgresContainerFixture — session-scoped Testcontainers wrapper
    bronze.py            BronzeRow model + DDL emitter for JSONB + envelope table
    sor_sim.py           SorSimulator ABC — seeds Postgres from fixtures or generators
    generators.py        PolyfactoryBuilder — derives generator from any Pydantic entity
    validators/
      __init__.py
      shape.py           validate_shape(row, entity_cls)
      classification.py  validate_classifications(entity_cls)
      tokenisation.py    validate_tokenisation(entity, token_service)
    report.py            HarnessReport — coverage matrix per entity × field
  tests/
    conftest.py          Postgres container fixture (session-scoped)
    rc/
      conftest.py        RC-specific seed + validator setup
      fixtures/
        customer.yaml
        order.yaml
        sku.yaml
        markdown.yaml
      test_customer.py
      test_order.py
      test_sku.py
      test_markdown.py
      test_composed_rc_flow.py
```

### Dependencies

```toml
[project]
dependencies = [
  "apex-core",
  "apex-schemas-common",
  "apex-tokenizer",
  "apex-rc",                      # pulls SCML + MERML + CXML transitively via PracticeBundle
  "psycopg[binary]>=3.2",
  "testcontainers[postgres]>=4.8",
  "polyfactory>=2.19",
  "pyyaml>=6.0",
]
```

### End-to-end data flow

```
  YAML fixture  OR  polyfactory generator
                |
                v  (seed step)
  +---------------------------------+
  |  Postgres (Testcontainer)       |
  |  table: bronze_rc               |
  |    event_id UUID                |   <-- envelope columns (5)
  |    event_ts TIMESTAMPTZ         |
  |    entity_id TEXT               |
  |    source_system TEXT           |
  |    source_system_ts TIMESTAMPTZ |
  |    payload JSONB                |   <-- SOR-native payload
  +----------------+----------------+
                   | SELECT
                   v
  +---------------------------------+
  | SorSimulator.read_rows()        |
  +----------------+----------------+
                   | dict per row
                   v
  +---------------------------------+
  | EntityValidator                 |
  |  1. validate_shape              |   Pydantic parse into apex-rc entity
  |  2. validate_classifications    |   every PHI/PII/PCI/TRADE field Annotated
  |  3. validate_tokenisation       |   tokenise + detokenise round-trip
  +----------------+----------------+
                   |
                   v
             HarnessReport
       (pass/fail + coverage matrix)
```

### Session lifecycle

| Phase | Trigger | Action | Cost |
|---|---|---|---|
| Session start | pytest boot | Testcontainers pulls + starts one Postgres instance | ~4-6 s (cached image); one-time per run |
| Per-Practice setup | first test in `tests/rc/` | `CREATE TABLE bronze_rc` + indexes via `bronze.emit_ddl()` | ~30 ms |
| Per-test setup | each test fn | Seed rows for this test's fixture set into a fresh schema | ~10-50 ms per test |
| Per-test run | test body | `SorSimulator.read_rows()` + `EntityValidator.run()` + assertions | ~5-20 ms |
| Per-test teardown | test exit | `DROP SCHEMA ... CASCADE` | ~5 ms |
| Session end | pytest exit | Container stops; volume discarded | ~1 s |

**Why one container per session + schema per test:** per-test containers cost 20+ minutes across the suite; shared state across tests creates coupling bugs. Per-session container + per-test schema runs the full RC suite in under 90 seconds with proper isolation.

---

## Section 2 — Library primitives

Eight types in `src/apex_test_harness/`. Each is small, focused, composable.

### 2.1 `PostgresContainerFixture` (`containers.py`)

```python
class PostgresContainerFixture:
    def connection_url(self) -> str: ...              # postgresql+psycopg://...
    def create_schema(self, name: str) -> None: ...   # CREATE SCHEMA name
    def drop_schema(self, name: str) -> None: ...     # DROP SCHEMA name CASCADE
```

Session-scoped via `@pytest.fixture(scope="session")`. Tests get a fresh schema via a function-scoped companion fixture.

### 2.2 `BronzeRow` + DDL emitter (`bronze.py`)

```python
class BronzeRow(BaseModel):
    model_config = ConfigDict(frozen=True, strict=True)
    event_id: UUID
    event_ts: datetime         # UTC; enforced
    entity_id: str
    source_system: str
    source_system_ts: datetime
    payload: dict[str, Any]    # JSONB in Postgres
```

`emit_ddl(table_name, schema)` returns the `CREATE TABLE` statement with an `(source_system, date_trunc('day', event_ts))` index pair — partitioning fidelity matches Fabric Bronze.

### 2.3 `SorSimulator` ABC (`sor_sim.py`)

```python
class SorSimulator(ABC):
    @abstractmethod
    def seed_rows(self, conn, schema: str, rows: Iterable[BronzeRow]) -> None: ...
    @abstractmethod
    def read_rows(self, conn, schema: str, *, where: str | None = None) -> list[dict]: ...
```

Default concrete `PayloadJsonbSorSimulator` covers 90% of cases. Practice suites subclass only for SOR-specific quirks.

### 2.4 `PolyfactoryBuilder` (`generators.py`)

```python
class PolyfactoryBuilder:
    @staticmethod
    def for_entity(
        entity_cls: type[BaseModel],
        *,
        seed: int = 0,
        overrides: dict[str, Any] | None = None,
    ) -> type[ModelFactory]: ...

    @staticmethod
    def build_bronze_rows(
        entity_cls: type[BaseModel],
        *,
        count: int,
        tenant_id: str,
        source_system: str,
        seed: int = 0,
    ) -> list[BronzeRow]: ...
```

### 2.5 Three validators (`validators/`)

Pure functions returning dataclass results. No exceptions on validation failure — results aggregate.

```python
# shape.py
@dataclass(frozen=True)
class ShapeResult:
    entity_cls_name: str
    row_id: str
    ok: bool
    parsed: BaseModel | None
    errors: tuple[str, ...]

def validate_shape(row: dict, entity_cls: type[BaseModel]) -> ShapeResult: ...

# classification.py — STATIC check, runs once per entity class
@dataclass(frozen=True)
class ClassificationResult:
    entity_cls_name: str
    ok: bool
    classified_fields: dict[str, Classification]
    unclassified_sensitive: tuple[str, ...]

def validate_classifications(entity_cls: type[BaseModel]) -> ClassificationResult: ...

# tokenisation.py — DYNAMIC check, per parsed entity
@dataclass(frozen=True)
class TokenisationResult:
    entity_cls_name: str
    row_id: str
    ok: bool
    tokenised_fields: tuple[str, ...]
    failures: tuple[str, ...]

def validate_tokenisation(
    entity: BaseModel,
    token_service: TokenService,
    tenant_id: str,
) -> TokenisationResult: ...
```

**Tokenisation exercises the four §6.3 invariants:** determinism, classification separation, tenant separation, vault round-trip.

**Classification heuristic** for `unclassified_sensitive`: fields matching `/(_token$|email|phone|ssn|mrn|dob|address|account_num|card)/i` without a `Classification` annotation are flagged. **Reported as warnings, not failures** — the heuristic will false-positive.

### 2.6 `HarnessReport` (`report.py`)

```python
@dataclass(frozen=True)
class HarnessReport:
    practice: str
    tenant_id: str
    shape_results: tuple[ShapeResult, ...]
    classification_results: tuple[ClassificationResult, ...]
    tokenisation_results: tuple[TokenisationResult, ...]

    @property
    def passed(self) -> bool: ...
    def coverage_matrix(self) -> dict[str, dict[str, str]]: ...
    def summary(self) -> str: ...
    def fields_never_exercised(self) -> dict[str, tuple[str, ...]]: ...
```

### Embedded design decisions

- Warnings, not failures, for `unclassified_sensitive`. False positives on names like `contact_description` shouldn't block CI.
- Fresh `InMemoryVaultBackend` per test — determinism + isolation.
- Polyfactory over `hypothesis.strategies.from_type` — Pydantic-native, more predictable for v2 models.

---

## Section 3 — Synthetic data strategy

### 3.1 Fixture file shape — one YAML per entity, array of scenarios

```yaml
# tests/rc/fixtures/customer.yaml
- id: happy_minimal
  kind: happy_path
  description: Required fields only; no PII set
  overrides:
    status: ACTIVE
    consent_marketing: false
    consent_analytics: false
  expect:
    shape: pass
    classification: pass
    tokenisation: skip

- id: happy_pii_heavy
  kind: happy_path
  description: Every PII token field populated
  overrides:
    status: ACTIVE
    full_name_token: "{{polyfactory}}"
    email_token: "{{polyfactory}}"
    phone_token: "{{polyfactory}}"
    address_token: "{{polyfactory}}"
    birth_year: 1985
  expect:
    shape: pass
    classification: pass
    tokenisation: pass

- id: edge_opted_out
  kind: edge_case
  description: Customer after opt-out
  overrides:
    status: OPTED_OUT
    opted_out_date: 2025-03-15
  expect: { shape: pass, classification: pass, tokenisation: pass }

- id: malformed_missing_status
  kind: malformed
  description: Required field missing
  overrides_raw: { customer_natural: "cust-001" }
  expect:
    shape: fail
    shape_error_contains: ["status"]

- id: malformed_wrong_type
  kind: malformed
  description: birth_year as string; Pydantic strict rejects
  overrides_raw:
    customer_natural: "cust-002"
    status: "ACTIVE"
    birth_year: "nineteen-eighty-five"
  expect:
    shape: fail
    shape_error_contains: ["birth_year", "int"]
```

The loader fills unpinned fields from `PolyfactoryBuilder.for_entity(cls, seed=hash(scenario.id))`. Same scenario produces the same filler every run.

### 3.2 Scenario-kind taxonomy

| Kind | Filler generator | Validators that run | Expected outcome |
|---|---|---|---|
| `happy_path` | Fills unpinned via polyfactory | shape + classification + tokenisation | All pass |
| `edge_case` | Fills unpinned via polyfactory | shape + classification + tokenisation | All pass (unusual but valid) |
| `malformed` | Uses `overrides_raw` verbatim | shape only | Shape fails with specific error match |
| `classification_drift` | Fills unpinned via polyfactory | shape + classification + tokenisation | classification warns; `unclassified_sensitive` populated |

### 3.3 Edge-case matrix per RC entity (minimum-complete bar)

| # | Scenario | SKU | Markdown | Customer | Order |
|---|---|---|---|---|---|
| 1 | `happy_minimal` (required only) | ✓ | ✓ | ✓ | ✓ |
| 2 | `happy_maximal` (every optional set) | ✓ | ✓ | ✓ | ✓ |
| 3 | `enum_boundary` (one per enum value) | ACTIVE / INACTIVE / DISCONTINUED | 6 MarkdownReason values | ACTIVE / INACTIVE / OPTED_OUT / SUPPRESSED | — |
| 4 | sensitive-heavy | `unit_cost_token` (TRADE) | — | all 4 PII tokens | `payment_token` (PCI) |
| 5 | `malformed_missing_required` | no `sku_status` | no `reason` | no `status` | no `customer_key` |
| 6 | `malformed_wrong_type` | `case_pack` as string | `marked_down_price` as string | `birth_year` as string | `total_amount` as string |
| 7 | `fk_mismatch` | `category_key` unknown | `sku_key` unknown | — | `customer_key` unknown |
| 8 | `tenant_separation` | ✓ | ✓ | ✓ | ✓ |

Total: ~35 scenarios across 4 entities → ~140 validation runs.

### 3.4 Volume test (opt-in, nightly)

Separate `test_volume_*.py` files, gated by `--volume` pytest flag.

```python
@pytest.mark.volume
@pytest.mark.parametrize("seed", list(range(10)))
def test_volume_customer(bronze_schema, seed):
    rows = PolyfactoryBuilder.build_bronze_rows(
        Customer, count=10_000, tenant_id="t-vol",
        source_system="vol-sim", seed=seed,
    )
    # seed + validate; assert 100% shape pass, 100% classification pass
```

100 000 rows per entity across 10 seeds. Catches distribution bugs the fixture matrix can't — e.g. a Pydantic validator that falls over on a particular Unicode codepoint.

### 3.5 Out of scope for MVP

- FK referential integrity across entities (FKs are opaque strings; resolver runs downstream)
- Time-travel / SCD2 scenarios (Depth C; locked on B)
- Translator round-trips (Depth D)
- Multi-row aggregation assertions (belongs to Gold measure tests)

---

## Section 4 — Test suite wiring for RC

### 4.1 Shared fixtures (`tests/conftest.py`)

```python
@pytest.fixture(scope="session")
def postgres() -> Iterator[PostgresContainerFixture]:
    with PostgresContainerFixture.start() as pg:
        yield pg

@pytest.fixture
def bronze_schema(postgres, request) -> Iterator[BronzeSchema]:
    schema = f"rc_{hashlib.sha1(request.node.nodeid.encode()).hexdigest()[:10]}"
    postgres.create_schema(schema)
    bronze = BronzeSchema(postgres.connection_url(), schema)
    bronze.apply_ddl("bronze_rc")
    yield bronze
    postgres.drop_schema(schema)
```

### 4.2 RC-specific fixtures (`tests/rc/conftest.py`)

```python
@pytest.fixture
def rc_token_service() -> TokenService:
    return TokenService(key=b"harness-test-key", vault=InMemoryVaultBackend())

@pytest.fixture
def rc_sim() -> PayloadJsonbSorSimulator:
    return PayloadJsonbSorSimulator(table="bronze_rc")

@pytest.fixture
def rc_validator(rc_token_service) -> EntityValidator:
    return EntityValidator(token_service=rc_token_service)

_ENTITIES = {
    "customer": (Customer, "customer.yaml"),
    "order":    (Order,    "order.yaml"),
    "sku":      (SKU,      "sku.yaml"),
    "markdown": (Markdown, "markdown.yaml"),
}

def pytest_generate_tests(metafunc):
    if "scenario" not in metafunc.fixturenames:
        return
    entity_name = metafunc.module.__name__.rsplit("_", 1)[-1]
    entity_cls, yaml_file = _ENTITIES[entity_name]
    scenarios = load_scenarios(Path(__file__).parent / "fixtures" / yaml_file)
    metafunc.parametrize("scenario", scenarios, ids=[s.id for s in scenarios])
```

### 4.3 Single-entity test shape (~10 lines)

```python
# tests/rc/test_customer.py
from apex_rc.cxml.entities import Customer
from apex_test_harness import run_scenario

def test_scenario(scenario, bronze_schema, rc_sim, rc_validator):
    row = build_bronze_row_from_scenario(scenario, Customer)
    rc_sim.seed_rows(bronze_schema.conn, bronze_schema.schema, [row])

    read_back = rc_sim.read_rows(bronze_schema.conn, bronze_schema.schema,
                                 where=f"entity_id = '{row.entity_id}'")
    assert len(read_back) == 1

    result = run_scenario(
        scenario, read_back[0], Customer,
        validator=rc_validator, tenant_id="t-harness",
    )
    assert result.matches(scenario.expect)
```

### 4.4 Composed RC flow

One test exercises SKU → Markdown → Customer → Order together; also asserts `fields_never_exercised() == {}` — the coverage-matrix guarantee.

### 4.5 Expected output

~38 tests, ~50-70 s wall clock (container boot ~5 s, per-test ~1.5 s).

---

## Section 5 — Runtime + CI integration

### 5.1 Testcontainers config

```python
class PostgresContainerFixture:
    _IMAGE = "postgres:16-alpine"   # pinned; 16 matches Fabric Warehouse JSONB parity
    _PORT = 5432

    @classmethod
    @contextmanager
    def start(cls) -> Iterator[Self]:
        container = PostgresContainer(cls._IMAGE, port=cls._PORT)
        container.with_env("POSTGRES_DB", "apex_harness")
        container.with_env("POSTGRES_USER", "apex")
        container.with_env("POSTGRES_PASSWORD", "harness")
        container.with_kwargs(tmpfs={"/var/lib/postgresql/data": "rw,size=512m"})
        with container:
            _wait_for_ready(container, timeout_s=30)
            yield cls(container)
```

- Pinned image tag (`postgres:16-alpine`) — matches Fabric Warehouse's JSONB operator behaviour.
- `tmpfs` data dir — Postgres runs in RAM, cuts boot + teardown by ~40%.
- Docker is the only runtime dependency.

### 5.2 pytest configuration additions

```toml
[tool.pytest.ini_options]
markers = [
  "volume: opt-in generator-driven volume tests (use --volume to enable)",
]
addopts = "-ra --strict-markers --strict-config --import-mode=importlib -m 'not volume'"
```

### 5.3 GitHub Actions (`.github/workflows/harness.yml`)

```yaml
name: Schema Harness
on:
  push: { branches: [main] }
  pull_request:

jobs:
  harness-rc:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install uv
      - run: uv sync --all-packages
      - run: uv run pytest packages/apex-test-harness -v
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: harness-report
          path: packages/apex-test-harness/.harness-report/

  harness-volume-nightly:
    runs-on: ubuntu-latest
    if: github.event_name == 'schedule'
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install uv
      - run: uv sync --all-packages
      - run: uv run pytest packages/apex-test-harness -m volume --volume -v
```

GitHub's `ubuntu-latest` runners have Docker pre-installed — no DinD gymnastics.

### 5.4 SLA targets

| Run profile | Target wall-clock | Pass bar |
|---|---|---|
| Every commit / PR (`harness-rc`) | < 90 seconds | 100% of non-volume scenarios pass |
| Nightly (`harness-volume-nightly`) | < 15 minutes | 100% of volume scenarios pass over 10 seeds × 4 entities × 10 000 rows |
| Developer laptop full suite | < 90 seconds | Same as CI |
| Fast debug iteration (one entity) | < 10 seconds | Same as CI |

If PR wall-clock blows past 90 s, first suspect is per-test schema-create cost. Fallback: widen `bronze_schema` scope from `function` to `module` with table-level tenant-prefix isolation.

### 5.5 Pre-Fabric gate criteria — when we call it done

1. 100% of the ~35 fixture scenarios pass across Customer, Order, SKU, Markdown.
2. Composed RC flow test passes, including `fields_never_exercised() == {}`.
3. Volume test (nightly) runs clean — 10 seeds × 4 entities × 10 000 rows, zero shape failures.
4. Coverage matrix shows every field of every RC entity exercised by at least one scenario with correct classification handling.
5. Classification heuristic false-positive rate on fixtures < 5%.

When all five hold, we have empirical evidence the schema layer is solid. Commit to Fabric.

### 5.6 Debugging workflow

Two custom pytest flags worth building: `--keep-schema` (skip teardown drop) and `--print-conn-url`.

```bash
# Reproduce a specific failing scenario
pytest packages/apex-test-harness/tests/rc/test_customer.py::test_scenario \
       -k "malformed_wrong_type" -v --pdb

# Inspect the coverage matrix
pytest packages/apex-test-harness/tests/rc/test_composed_rc_flow.py -v
cat packages/apex-test-harness/.harness-report/coverage.json | jq

# Inspect the rows that went into Postgres for a given test
pytest ... --keep-schema
psql "$(pytest packages/apex-test-harness --print-conn-url)" -c \
     "SELECT event_id, entity_id, payload FROM rc_<hash>.bronze_rc LIMIT 5;"
```

---

## Wave 2 expansion (not in scope for this design)

When `apex-test-harness` is green for RC, adding a second Practice looks like:

1. `tests/hlscml/fixtures/` — 8+ scenarios per HLS entity (Patient, Observation, Encounter, …).
2. `tests/hlscml/conftest.py` — declares the entity-to-YAML map; reuses the root `postgres` fixture and the library `EntityValidator`.
3. One per-entity test file per entity (`test_patient.py`, `test_observation.py`, …).
4. One composed HLS flow test.

Zero library changes. This is the core payoff of the layered architecture.

---

## Decision log — summary

| Decision | Choice | Why |
|---|---|---|
| Validation depth | B | Shape + classifications + tokenisation covers the hardest invariants; C/D come later |
| Pilot Practice | `apex-rc` | Canonical demo; exercises PII tokenisation; shortest path to a working pattern |
| Postgres shape | JSONB payload + envelope | Mirrors Bronze in Fabric; same validator wiring works for both |
| Data generation | Hybrid (YAML + polyfactory) | Deterministic CI + soak coverage without double-writing fixtures |
| Runtime | pytest + Testcontainers | Self-contained; CI-native; zero manual setup |
| Location | New workspace package | Reusable for wave 2 without retrofit |
| Architecture | Layered library + per-Practice tests | Matches existing monorepo convention; scales to all 10 Practices with zero library churn |
| Unclassified-sensitive outcome | Warning, not failure | Regex heuristic will false-positive |
| Fixture YAML shape | Per-entity, array-of-scenarios | Terse; easy to diff a whole entity's matrix |
| Volume tests | `--volume` opt-in, nightly | 4M validations per commit is the wrong default |
| Minimum scenarios per entity | 8 | Covers required/optional, enum boundary, sensitive-heavy, two malformation classes, FK edge, tenant separation |
| Postgres image | `postgres:16-alpine`, pinned, tmpfs | Fabric Warehouse JSONB parity; RAM-speed boot |
| Pre-Fabric gate | 5 criteria | Empirical evidence the schema layer holds |

---

## Next step

Invoke `writing-plans` skill to produce the detailed implementation plan (phases, tasks, test-driven increments) keyed off this design.
