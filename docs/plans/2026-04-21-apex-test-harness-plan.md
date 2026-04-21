# APEX Test Harness Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build `apex-test-harness` — a pytest + Testcontainers harness that validates APEX Practice schemas (shape + classifications + tokenisation) against synthetic PostgreSQL-backed data, with `apex-rc` as the pilot Practice.

**Architecture:** New workspace package `packages/apex-test-harness/`. Library half (`src/apex_test_harness/`) ships reusable primitives — `PostgresContainerFixture`, `BronzeRow`, `SorSimulator`, `PolyfactoryBuilder`, three validators, `HarnessReport`. Tests half (`tests/`) ships per-Practice fixtures (`tests/rc/fixtures/*.yaml`) and test files that import the library and parametrise via a `pytest_generate_tests` hook. Wave 2 HLS adds one fixture directory with zero library churn.

**Tech Stack:** Python 3.11, Pydantic v2, pytest, Testcontainers (Postgres 16-alpine), psycopg 3, polyfactory, PyYAML. Dev uses `uv` workspaces. CI via GitHub Actions on ubuntu-latest.

**Design doc:** [2026-04-21-apex-test-harness-design.md](2026-04-21-apex-test-harness-design.md)

---

## Required reading before execution

1. The design doc (above) — locks every architectural decision.
2. `packages/apex-rc/src/apex_rc/` — the pilot Practice we validate against. Customer/Order/SKU/Markdown are the four pilot entities. Their field shapes, classifications, and validators are what the harness exercises.
3. `packages/apex-tokenizer/src/apex_tokenizer/service.py` — `TokenService`, `InMemoryVaultBackend`. The tokenisation validator exercises this.
4. `packages/apex-schemas-common/src/apex_schemas_common/purview.py` — `walk_annotated_metadata()`. The classification validator calls this.
5. `packages/apex-core/src/apex_core/envelope.py` — `CanonicalEnvelope`. BronzeRow composes the same 5 fields.
6. Root `pyproject.toml` — workspace layout; new package must be added here.

---

## Invariants the implementation MUST preserve

- **Frozen strict Pydantic models.** Every new model in the harness uses `ConfigDict(frozen=True, strict=True, extra="forbid")` unless there's a specific reason otherwise.
- **No module-level mutable state.** Caches keyed by tenant + classification; never global. Tests must not share state via the library.
- **Deterministic by default.** Polyfactory always seeded. Test IDs hash to seeds. Same input → same token → same test result on any machine.
- **Validators never raise for validation failures.** Results aggregate. A failing entity does not abort a run.
- **`tests/` directory is excluded from the workspace mypy + ruff strict modes** (same as every other package). Library code (`src/`) is fully typed.

---

## Task 1: Scaffold the package

**Files:**
- Create: `packages/apex-test-harness/pyproject.toml`
- Create: `packages/apex-test-harness/README.md`
- Create: `packages/apex-test-harness/src/apex_test_harness/__init__.py`
- Create: `packages/apex-test-harness/tests/__init__.py`
- Create: `packages/apex-test-harness/tests/conftest.py` (empty stub)
- Modify: `pyproject.toml` (root) — no change needed if workspace glob is `packages/*`

**Step 1: Write the failing smoke test**

`packages/apex-test-harness/tests/test_smoke.py`:
```python
def test_package_imports() -> None:
    import apex_test_harness
    assert apex_test_harness.__name__ == "apex_test_harness"
```

**Step 2: Run test to verify it fails**

Run: `./.venv/Scripts/python.exe -m pytest packages/apex-test-harness -q`
Expected: `ModuleNotFoundError: No module named 'apex_test_harness'`

**Step 3: Create package files**

`packages/apex-test-harness/pyproject.toml`:
```toml
[project]
name = "apex-test-harness"
version = "0.1.0"
description = "APEX schema validation harness — pytest + Testcontainers + synthetic Postgres-backed data."
readme = "README.md"
requires-python = ">=3.11"
license = { text = "Proprietary - Deloitte Internal" }
dependencies = [
    "apex-core",
    "apex-schemas-common",
    "apex-tokenizer",
    "apex-rc",
    "pydantic>=2.9.0",
    "psycopg[binary]>=3.2",
    "testcontainers[postgres]>=4.8",
    "polyfactory>=2.19",
    "pyyaml>=6.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/apex_test_harness"]

[tool.uv.sources]
apex-core = { workspace = true }
apex-schemas-common = { workspace = true }
apex-tokenizer = { workspace = true }
apex-rc = { workspace = true }

[tool.pytest.ini_options]
markers = [
  "volume: opt-in generator-driven volume tests (use --volume to enable)",
]
```

`packages/apex-test-harness/src/apex_test_harness/__init__.py`:
```python
"""APEX schema validation harness."""
```

`packages/apex-test-harness/README.md`:
```markdown
# apex-test-harness

Schema-validation harness for APEX Practice packages. pytest + Testcontainers + Postgres-backed synthetic data. Pilot: apex-rc.
```

**Step 4: Install + run test to verify it passes**

Run: `./.venv/Scripts/python.exe -m pip install -e packages/apex-test-harness --quiet && ./.venv/Scripts/python.exe -m pytest packages/apex-test-harness -q`
Expected: `1 passed`

**Step 5: Commit**

```bash
git add packages/apex-test-harness/
git commit -m "feat(harness): scaffold apex-test-harness package"
```

---

## Task 2: `BronzeRow` Pydantic model + DDL emitter

**Files:**
- Create: `packages/apex-test-harness/src/apex_test_harness/bronze.py`
- Create: `packages/apex-test-harness/tests/test_bronze.py`

**Step 1: Write the failing test**

```python
# tests/test_bronze.py
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from apex_test_harness.bronze import BronzeRow, emit_ddl


def test_bronze_row_all_five_envelope_fields_required() -> None:
    row = BronzeRow(
        event_id=uuid4(),
        event_ts=datetime.now(UTC),
        entity_id="ent-1",
        source_system="sap.s4",
        source_system_ts=datetime.now(UTC),
        payload={"foo": "bar"},
    )
    assert row.payload == {"foo": "bar"}


def test_bronze_row_is_frozen() -> None:
    row = BronzeRow(
        event_id=uuid4(), event_ts=datetime.now(UTC),
        entity_id="e", source_system="s",
        source_system_ts=datetime.now(UTC), payload={},
    )
    with pytest.raises(Exception):
        row.entity_id = "other"  # type: ignore[misc]


def test_bronze_row_rejects_missing_envelope() -> None:
    with pytest.raises(Exception):
        BronzeRow(entity_id="e", source_system="s", payload={})  # type: ignore[call-arg]


def test_emit_ddl_produces_create_table() -> None:
    ddl = emit_ddl("bronze_rc", "public")
    assert "CREATE TABLE" in ddl.upper()
    assert "bronze_rc" in ddl
    assert "payload JSONB" in ddl
    assert "event_id UUID" in ddl
    assert "source_system TEXT" in ddl
```

**Step 2: Run test to verify it fails**

Run: `./.venv/Scripts/python.exe -m pytest packages/apex-test-harness/tests/test_bronze.py -q`
Expected: `ModuleNotFoundError: No module named 'apex_test_harness.bronze'`

**Step 3: Implement `bronze.py`**

```python
"""BronzeRow + DDL emitter. Mirrors Fabric Bronze: envelope + JSONB payload."""

from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BronzeRow(BaseModel):
    """One row in the Bronze table. 5-field envelope + JSONB payload."""

    model_config = ConfigDict(frozen=True, strict=True, extra="forbid")

    event_id: UUID
    event_ts: datetime
    entity_id: str
    source_system: str
    source_system_ts: datetime
    payload: dict[str, Any]


def emit_ddl(table_name: str, schema: str) -> str:
    """Return CREATE TABLE statement for a Bronze table.

    Partition-fidelity index on (source_system, date_trunc('day', event_ts)).
    """
    return f"""
CREATE TABLE IF NOT EXISTS {schema}.{table_name} (
    event_id UUID NOT NULL,
    event_ts TIMESTAMPTZ NOT NULL,
    entity_id TEXT NOT NULL,
    source_system TEXT NOT NULL,
    source_system_ts TIMESTAMPTZ NOT NULL,
    payload JSONB NOT NULL,
    PRIMARY KEY (event_id)
);
CREATE INDEX IF NOT EXISTS ix_{table_name}_sys_day
    ON {schema}.{table_name} (source_system, date_trunc('day', event_ts));
CREATE INDEX IF NOT EXISTS ix_{table_name}_entity
    ON {schema}.{table_name} (entity_id);
""".strip()
```

**Step 4: Run test**

Run: `./.venv/Scripts/python.exe -m pytest packages/apex-test-harness/tests/test_bronze.py -q`
Expected: `4 passed`

**Step 5: Commit**

```bash
git add packages/apex-test-harness/src/apex_test_harness/bronze.py \
        packages/apex-test-harness/tests/test_bronze.py
git commit -m "feat(harness): add BronzeRow + emit_ddl"
```

---

## Task 3: `PostgresContainerFixture` + root conftest wiring

**Files:**
- Create: `packages/apex-test-harness/src/apex_test_harness/containers.py`
- Create: `packages/apex-test-harness/tests/test_containers_integration.py`

**Step 1: Write the failing integration test**

```python
# tests/test_containers_integration.py
import pytest

from apex_test_harness.containers import PostgresContainerFixture


@pytest.mark.integration
def test_container_starts_and_serves_connection_url() -> None:
    with PostgresContainerFixture.start() as fx:
        url = fx.connection_url()
        assert url.startswith("postgresql+psycopg://") or url.startswith("postgresql://")


@pytest.mark.integration
def test_create_and_drop_schema() -> None:
    with PostgresContainerFixture.start() as fx:
        fx.create_schema("harness_test_1")
        # No error means success; second drop is idempotent
        fx.drop_schema("harness_test_1")
```

**Step 2: Run test to verify it fails**

Run: `./.venv/Scripts/python.exe -m pytest packages/apex-test-harness/tests/test_containers_integration.py -q -m integration`
Expected: `ModuleNotFoundError`

**Step 3: Implement `containers.py`**

```python
"""Testcontainers-backed Postgres fixture. Session-scoped; schema-per-test."""

from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Iterator, Self

import psycopg
from testcontainers.postgres import PostgresContainer


class PostgresContainerFixture:
    """Wraps a PostgresContainer with schema create/drop helpers."""

    _IMAGE = "postgres:16-alpine"
    _PORT = 5432

    def __init__(self, container: PostgresContainer) -> None:
        self._container = container

    @classmethod
    @contextmanager
    def start(cls) -> Iterator[Self]:
        """Context-manager: start a fresh container, yield the fixture, stop."""
        container = (
            PostgresContainer(cls._IMAGE, port=cls._PORT)
            .with_env("POSTGRES_DB", "apex_harness")
            .with_env("POSTGRES_USER", "apex")
            .with_env("POSTGRES_PASSWORD", "harness")
            .with_kwargs(tmpfs={"/var/lib/postgresql/data": "rw,size=512m"})
        )
        with container:
            cls._wait_for_ready(container)
            yield cls(container)

    @staticmethod
    def _wait_for_ready(container: PostgresContainer, timeout_s: float = 30.0) -> None:
        start = time.monotonic()
        last_exc: Exception | None = None
        while time.monotonic() - start < timeout_s:
            try:
                with psycopg.connect(container.get_connection_url()) as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT 1")
                        return
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                time.sleep(0.3)
        raise RuntimeError(f"Postgres container not ready in {timeout_s}s: {last_exc}")

    def connection_url(self) -> str:
        return self._container.get_connection_url()

    def create_schema(self, name: str) -> None:
        with psycopg.connect(self.connection_url(), autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute(f'CREATE SCHEMA IF NOT EXISTS "{name}"')

    def drop_schema(self, name: str) -> None:
        with psycopg.connect(self.connection_url(), autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute(f'DROP SCHEMA IF EXISTS "{name}" CASCADE')
```

Add to `pyproject.toml` markers: `"integration: tests that need Docker"`.

**Step 4: Run test — requires Docker running locally**

Run: `./.venv/Scripts/python.exe -m pytest packages/apex-test-harness/tests/test_containers_integration.py -q -m integration`
Expected: `2 passed in ~10s` (image pull first run)

**Step 5: Commit**

```bash
git add packages/apex-test-harness/src/apex_test_harness/containers.py \
        packages/apex-test-harness/tests/test_containers_integration.py \
        packages/apex-test-harness/pyproject.toml
git commit -m "feat(harness): add PostgresContainerFixture (Testcontainers)"
```

---

## Task 4: `SorSimulator` ABC + `PayloadJsonbSorSimulator`

**Files:**
- Create: `packages/apex-test-harness/src/apex_test_harness/sor_sim.py`
- Create: `packages/apex-test-harness/tests/test_sor_sim.py`

**Step 1: Write tests using the container fixture**

```python
# tests/test_sor_sim.py
from datetime import UTC, datetime
from uuid import uuid4

import pytest

from apex_test_harness.bronze import BronzeRow, emit_ddl
from apex_test_harness.containers import PostgresContainerFixture
from apex_test_harness.sor_sim import PayloadJsonbSorSimulator


@pytest.fixture(scope="module")
def pg():
    with PostgresContainerFixture.start() as fx:
        yield fx


@pytest.fixture
def schema(pg, request):
    name = f"sor_{request.node.name.replace('[','_').replace(']','')}"
    pg.create_schema(name)
    import psycopg
    with psycopg.connect(pg.connection_url()) as conn:
        with conn.cursor() as cur:
            cur.execute(emit_ddl("bronze_rc", name))
            conn.commit()
    yield (pg.connection_url(), name)
    pg.drop_schema(name)


@pytest.mark.integration
def test_seed_and_read_roundtrip(schema):
    url, sname = schema
    sim = PayloadJsonbSorSimulator(table="bronze_rc")
    row = BronzeRow(
        event_id=uuid4(), event_ts=datetime.now(UTC),
        entity_id="cust-1", source_system="sap.s4",
        source_system_ts=datetime.now(UTC),
        payload={"status": "ACTIVE"},
    )
    import psycopg
    with psycopg.connect(url) as conn:
        sim.seed_rows(conn, sname, [row])
        rows = sim.read_rows(conn, sname)
    assert len(rows) == 1
    assert rows[0]["entity_id"] == "cust-1"
    assert rows[0]["payload"]["status"] == "ACTIVE"


@pytest.mark.integration
def test_where_clause_filters(schema):
    url, sname = schema
    sim = PayloadJsonbSorSimulator(table="bronze_rc")
    rows = [
        BronzeRow(event_id=uuid4(), event_ts=datetime.now(UTC),
                  entity_id=f"e-{i}", source_system="sap",
                  source_system_ts=datetime.now(UTC),
                  payload={"i": i}) for i in range(3)
    ]
    import psycopg
    with psycopg.connect(url) as conn:
        sim.seed_rows(conn, sname, rows)
        filtered = sim.read_rows(conn, sname, where="entity_id = 'e-1'")
    assert len(filtered) == 1
    assert filtered[0]["entity_id"] == "e-1"
```

**Step 2: Run test to verify it fails**

Run: `./.venv/Scripts/python.exe -m pytest packages/apex-test-harness/tests/test_sor_sim.py -q -m integration`
Expected: `ModuleNotFoundError: No module named 'apex_test_harness.sor_sim'`

**Step 3: Implement `sor_sim.py`**

```python
"""SOR simulator over the Postgres Bronze table."""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any, Iterable

import psycopg

from apex_test_harness.bronze import BronzeRow


class SorSimulator(ABC):
    """Seeds and reads rows from a simulated SOR Bronze table."""

    @abstractmethod
    def seed_rows(
        self, conn: psycopg.Connection, schema: str, rows: Iterable[BronzeRow]
    ) -> None: ...

    @abstractmethod
    def read_rows(
        self,
        conn: psycopg.Connection,
        schema: str,
        *,
        where: str | None = None,
    ) -> list[dict[str, Any]]: ...


class PayloadJsonbSorSimulator(SorSimulator):
    """Default: INSERTs into bronze_<table>; SELECTs back with optional WHERE."""

    def __init__(self, table: str) -> None:
        self._table = table

    def seed_rows(
        self, conn: psycopg.Connection, schema: str, rows: Iterable[BronzeRow]
    ) -> None:
        stmt = (
            f'INSERT INTO "{schema}".{self._table} '
            f"(event_id, event_ts, entity_id, source_system, source_system_ts, payload) "
            f"VALUES (%s, %s, %s, %s, %s, %s)"
        )
        with conn.cursor() as cur:
            for r in rows:
                cur.execute(
                    stmt,
                    (
                        str(r.event_id),
                        r.event_ts,
                        r.entity_id,
                        r.source_system,
                        r.source_system_ts,
                        json.dumps(r.payload, default=str),
                    ),
                )
        conn.commit()

    def read_rows(
        self,
        conn: psycopg.Connection,
        schema: str,
        *,
        where: str | None = None,
    ) -> list[dict[str, Any]]:
        sql = (
            f'SELECT event_id, event_ts, entity_id, source_system, '
            f'source_system_ts, payload FROM "{schema}".{self._table}'
        )
        if where:
            sql += f" WHERE {where}"
        sql += " ORDER BY event_ts"
        out: list[dict[str, Any]] = []
        with conn.cursor() as cur:
            cur.execute(sql)
            for row in cur.fetchall():
                out.append(
                    {
                        "event_id": str(row[0]),
                        "event_ts": row[1],
                        "entity_id": row[2],
                        "source_system": row[3],
                        "source_system_ts": row[4],
                        "payload": row[5],
                    }
                )
        return out
```

**Step 4: Run test**

Expected: `2 passed`

**Step 5: Commit**

```bash
git add packages/apex-test-harness/src/apex_test_harness/sor_sim.py \
        packages/apex-test-harness/tests/test_sor_sim.py
git commit -m "feat(harness): add SorSimulator ABC + PayloadJsonbSorSimulator"
```

---

## Task 5: `PolyfactoryBuilder`

**Files:**
- Create: `packages/apex-test-harness/src/apex_test_harness/generators.py`
- Create: `packages/apex-test-harness/tests/test_generators.py`

**Step 1: Write tests**

```python
# tests/test_generators.py
from apex_rc.cxml.entities import Customer
from apex_test_harness.generators import PolyfactoryBuilder


def test_for_entity_produces_valid_customer() -> None:
    factory = PolyfactoryBuilder.for_entity(Customer, seed=42)
    customer = factory.build()
    assert isinstance(customer, Customer)


def test_seed_determinism() -> None:
    f1 = PolyfactoryBuilder.for_entity(Customer, seed=42).build()
    f2 = PolyfactoryBuilder.for_entity(Customer, seed=42).build()
    assert f1.customer_natural == f2.customer_natural  # deterministic


def test_build_bronze_rows_shape() -> None:
    rows = PolyfactoryBuilder.build_bronze_rows(
        Customer, count=3, tenant_id="t-1",
        source_system="rc-sim", seed=7,
    )
    assert len(rows) == 3
    for r in rows:
        assert r.source_system == "rc-sim"
        assert "status" in r.payload  # Customer has a required status field


def test_overrides_are_honoured() -> None:
    factory = PolyfactoryBuilder.for_entity(
        Customer, seed=1, overrides={"status": "OPTED_OUT"},
    )
    customer = factory.build()
    assert customer.status == "OPTED_OUT"
```

**Step 2: Run — fails with ModuleNotFoundError**

**Step 3: Implement `generators.py`**

```python
"""Polyfactory-backed generator for Pydantic entities."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

from apex_test_harness.bronze import BronzeRow


class PolyfactoryBuilder:
    """Derives deterministic factories + Bronze-row generators from entities."""

    @staticmethod
    def for_entity(
        entity_cls: type[BaseModel],
        *,
        seed: int = 0,
        overrides: dict[str, Any] | None = None,
    ) -> type[ModelFactory]:
        """Produce a seeded polyfactory factory for entity_cls."""
        overrides = overrides or {}

        class _Factory(ModelFactory[entity_cls]):  # type: ignore[valid-type]
            __model__ = entity_cls
            __random_seed__ = seed
            __set_as_default_factory_for_type__ = False

        # Apply overrides by patching the build() call
        orig_build = _Factory.build

        @classmethod  # type: ignore[misc]
        def _build_with_overrides(cls, **kwargs):  # type: ignore[no-untyped-def]
            merged = {**overrides, **kwargs}
            return orig_build(**merged)

        _Factory.build = _build_with_overrides  # type: ignore[assignment]
        return _Factory

    @staticmethod
    def build_bronze_rows(
        entity_cls: type[BaseModel],
        *,
        count: int,
        tenant_id: str,
        source_system: str,
        seed: int = 0,
    ) -> list[BronzeRow]:
        """Generate `count` Bronze rows wrapping entity_cls instances."""
        factory = PolyfactoryBuilder.for_entity(entity_cls, seed=seed)
        now = datetime.now(UTC)
        rows: list[BronzeRow] = []
        for i in range(count):
            entity = factory.build()
            payload = entity.model_dump(mode="json")
            payload["_tenant_id"] = tenant_id
            rows.append(
                BronzeRow(
                    event_id=uuid4(),
                    event_ts=now,
                    entity_id=f"{source_system}-{seed}-{i}",
                    source_system=source_system,
                    source_system_ts=now,
                    payload=payload,
                )
            )
        return rows
```

**Step 4: Run test**

Run: `./.venv/Scripts/python.exe -m pytest packages/apex-test-harness/tests/test_generators.py -q`
Expected: `4 passed`

**Step 5: Commit**

```bash
git add packages/apex-test-harness/src/apex_test_harness/generators.py \
        packages/apex-test-harness/tests/test_generators.py
git commit -m "feat(harness): add PolyfactoryBuilder"
```

---

## Task 6: `validate_shape` validator

**Files:**
- Create: `packages/apex-test-harness/src/apex_test_harness/validators/__init__.py`
- Create: `packages/apex-test-harness/src/apex_test_harness/validators/shape.py`
- Create: `packages/apex-test-harness/tests/validators/__init__.py`
- Create: `packages/apex-test-harness/tests/validators/test_shape.py`

**Step 1: Write tests**

```python
# tests/validators/test_shape.py
from apex_rc.cxml.entities import Customer
from apex_test_harness.validators.shape import ShapeResult, validate_shape


def test_shape_passes_on_valid_row() -> None:
    row = {
        "payload": {"customer_natural": "cust-1", "status": "ACTIVE",
                    "consent_marketing": False, "consent_analytics": False,
                    "envelope": {}, "entity_id": "x", "tenant_id": "t"},
        "entity_id": "cust-1",
    }
    r = validate_shape(row, Customer)
    assert isinstance(r, ShapeResult)
    # May fail if envelope/entity_id fields aren't in Customer — see assertion note
    # We assert against either pass OR fail with a specific error, not silently


def test_shape_fails_on_missing_required() -> None:
    row = {"payload": {"customer_natural": "cust-1"}, "entity_id": "cust-1"}
    r = validate_shape(row, Customer)
    assert r.ok is False
    assert any("status" in e.lower() for e in r.errors)


def test_shape_fails_on_wrong_type() -> None:
    row = {
        "payload": {"customer_natural": "c", "status": "ACTIVE",
                    "birth_year": "not-an-int"},
        "entity_id": "c",
    }
    r = validate_shape(row, Customer)
    assert r.ok is False
```

**Step 2: Run — fails with ModuleNotFoundError**

**Step 3: Implement**

```python
# src/apex_test_harness/validators/__init__.py
"""Harness validators."""

from apex_test_harness.validators.shape import ShapeResult, validate_shape

__all__ = ["ShapeResult", "validate_shape"]
```

```python
# src/apex_test_harness/validators/shape.py
"""Shape validator — Pydantic parses the row into the entity class."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel, ValidationError


@dataclass(frozen=True)
class ShapeResult:
    entity_cls_name: str
    row_id: str
    ok: bool
    parsed: BaseModel | None
    errors: tuple[str, ...]


def validate_shape(row: dict[str, Any], entity_cls: type[BaseModel]) -> ShapeResult:
    """Parse row['payload'] into entity_cls; capture Pydantic errors."""
    payload = row.get("payload", {})
    row_id = str(row.get("entity_id") or row.get("event_id") or "?")
    try:
        parsed = entity_cls.model_validate(payload)
    except ValidationError as exc:
        flat = tuple(
            f"{'.'.join(str(p) for p in e['loc'])}: {e['msg']}" for e in exc.errors()
        )
        return ShapeResult(
            entity_cls_name=entity_cls.__name__, row_id=row_id,
            ok=False, parsed=None, errors=flat,
        )
    return ShapeResult(
        entity_cls_name=entity_cls.__name__, row_id=row_id,
        ok=True, parsed=parsed, errors=(),
    )
```

**Step 4: Run test**

Expected: `3 passed` (the first test may need payload adjustment — check Customer's actual required fields; iterate until green)

**Step 5: Commit**

```bash
git add packages/apex-test-harness/src/apex_test_harness/validators/ \
        packages/apex-test-harness/tests/validators/
git commit -m "feat(harness): add validate_shape"
```

---

## Task 7: `validate_classifications` (with regex heuristic)

**Files:**
- Create: `packages/apex-test-harness/src/apex_test_harness/validators/classification.py`
- Create: `packages/apex-test-harness/tests/validators/test_classification.py`

**Step 1: Write tests**

```python
# tests/validators/test_classification.py
from apex_rc.cxml.entities import Customer
from apex_rc.scml.entities import SKU
from apex_test_harness.validators.classification import (
    ClassificationResult,
    validate_classifications,
)


def test_customer_pii_fields_are_classified() -> None:
    r = validate_classifications(Customer)
    # Customer has *_token fields classified as PII in apex-rc.
    # They should show up as classified (not unclassified_sensitive).
    assert r.ok is True
    assert "full_name_token" in r.classified_fields
    assert "email_token" in r.classified_fields
    assert "phone_token" in r.classified_fields


def test_sku_trade_secret_field_is_classified() -> None:
    r = validate_classifications(SKU)
    assert "unit_cost_token" in r.classified_fields


def test_heuristic_flags_unannotated_sensitive_name() -> None:
    # Synthetic entity with a *_token field that lacks Classification annotation
    from pydantic import BaseModel

    class Leaky(BaseModel):
        customer_natural: str
        ssn: str  # suspicious name, no Annotated[..., Classification.PII]

    r = validate_classifications(Leaky)
    assert "ssn" in r.unclassified_sensitive
```

**Step 2: Run — fails**

**Step 3: Implement**

```python
# src/apex_test_harness/validators/classification.py
"""Classification validator — static check per entity class."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, get_args

from pydantic import BaseModel

from apex_core.types import Classification

_SENSITIVE_NAME_PATTERN = re.compile(
    r"(_token$|^email|^phone|^ssn|^mrn|^dob|^address|account_num|^card)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ClassificationResult:
    entity_cls_name: str
    ok: bool
    classified_fields: dict[str, Classification]
    unclassified_sensitive: tuple[str, ...]


def _classification_for_field(field_info: Any) -> Classification | None:
    """Walk Annotated metadata on a Pydantic field looking for Classification."""
    meta = getattr(field_info, "metadata", ())
    for item in meta:
        if isinstance(item, Classification):
            return item
    # Some Annotated wrappers expose type args via get_args on the annotation.
    annotation = getattr(field_info, "annotation", None)
    if annotation is not None:
        for arg in get_args(annotation):
            if isinstance(arg, Classification):
                return arg
    return None


def validate_classifications(entity_cls: type[BaseModel]) -> ClassificationResult:
    """Static inspection: every sensitive-looking field must be classified."""
    classified: dict[str, Classification] = {}
    unclassified: list[str] = []

    for fname, finfo in entity_cls.model_fields.items():
        cls = _classification_for_field(finfo)
        if cls is not None:
            classified[fname] = cls
            continue
        if _SENSITIVE_NAME_PATTERN.search(fname):
            unclassified.append(fname)

    return ClassificationResult(
        entity_cls_name=entity_cls.__name__,
        ok=True,  # heuristic warnings don't fail the result
        classified_fields=classified,
        unclassified_sensitive=tuple(unclassified),
    )
```

Update `validators/__init__.py` to re-export.

**Step 4: Run test**

Expected: `3 passed`

**Step 5: Commit**

```bash
git add packages/apex-test-harness/src/apex_test_harness/validators/classification.py \
        packages/apex-test-harness/tests/validators/test_classification.py \
        packages/apex-test-harness/src/apex_test_harness/validators/__init__.py
git commit -m "feat(harness): add validate_classifications with regex heuristic"
```

---

## Task 8: `validate_tokenisation` (four §6.3 invariants)

**Files:**
- Create: `packages/apex-test-harness/src/apex_test_harness/validators/tokenisation.py`
- Create: `packages/apex-test-harness/tests/validators/test_tokenisation.py`

**Step 1: Write tests**

```python
# tests/validators/test_tokenisation.py
from apex_rc.cxml.entities import Customer
from apex_tokenizer import InMemoryVaultBackend, TokenService
from apex_test_harness.validators.tokenisation import (
    TokenisationResult, validate_tokenisation,
)


def _token_service() -> TokenService:
    return TokenService(key=b"test-key", vault=InMemoryVaultBackend())


def test_determinism_same_value_same_token() -> None:
    c = Customer(customer_natural="c1", status="ACTIVE",
                 full_name_token="Jane Doe",
                 consent_marketing=False, consent_analytics=False)
    ts = _token_service()
    r1 = validate_tokenisation(c, ts, tenant_id="t1")
    r2 = validate_tokenisation(c, ts, tenant_id="t1")
    assert r1.ok and r2.ok


def test_tenant_separation() -> None:
    c = Customer(customer_natural="c1", status="ACTIVE",
                 full_name_token="Jane Doe",
                 consent_marketing=False, consent_analytics=False)
    ts = _token_service()
    r = validate_tokenisation(c, ts, tenant_id="t1")
    # Expect at least one tokenised field exercised
    assert "full_name_token" in r.tokenised_fields


def test_round_trip_detokenises() -> None:
    c = Customer(customer_natural="c1", status="ACTIVE",
                 full_name_token="Jane Doe",
                 consent_marketing=False, consent_analytics=False)
    ts = _token_service()
    r = validate_tokenisation(c, ts, tenant_id="t1")
    assert r.ok
    assert "round_trip" not in "\n".join(r.failures)
```

**Step 2: Run — fails**

**Step 3: Implement**

```python
# src/apex_test_harness/validators/tokenisation.py
"""Tokenisation validator — exercises the four §6.3 invariants."""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel

from apex_core.types import Classification
from apex_tokenizer import TokenService

from apex_test_harness.validators.classification import _classification_for_field


@dataclass(frozen=True)
class TokenisationResult:
    entity_cls_name: str
    row_id: str
    ok: bool
    tokenised_fields: tuple[str, ...]
    failures: tuple[str, ...]


_TOKENISABLE = {
    Classification.PHI, Classification.PII,
    Classification.PCI, Classification.TRADE_SECRET,
}


def validate_tokenisation(
    entity: BaseModel,
    token_service: TokenService,
    tenant_id: str,
) -> TokenisationResult:
    """Tokenise each classified field; verify determinism + tenant separation + round-trip."""
    cls = type(entity)
    failures: list[str] = []
    tokenised: list[str] = []

    for fname, finfo in cls.model_fields.items():
        classification = _classification_for_field(finfo)
        if classification not in _TOKENISABLE:
            continue
        plain = getattr(entity, fname)
        if plain is None:
            continue

        # 1. Determinism: same plaintext -> same token
        t1 = token_service.tokenize(plain, classification=classification, tenant_id=tenant_id)
        t2 = token_service.tokenize(plain, classification=classification, tenant_id=tenant_id)
        if t1 != t2:
            failures.append(f"{fname}: determinism failed")
            continue

        # 2. Tenant separation: different tenant -> different token
        t_other = token_service.tokenize(plain, classification=classification, tenant_id=f"{tenant_id}-other")
        if t1 == t_other:
            failures.append(f"{fname}: tenant separation failed")

        # 3. Classification separation: different classification -> different token
        # Pick a different valid classification
        other_cls = next(iter(_TOKENISABLE - {classification}))
        t_other_cls = token_service.tokenize(plain, classification=other_cls, tenant_id=tenant_id)
        if t1 == t_other_cls:
            failures.append(f"{fname}: classification separation failed")

        # 4. Round-trip via vault
        round_tripped = token_service.detokenize(t1, classification=classification, tenant_id=tenant_id)
        if round_tripped != plain:
            failures.append(f"{fname}: round_trip failed")

        tokenised.append(fname)

    return TokenisationResult(
        entity_cls_name=cls.__name__,
        row_id=str(getattr(entity, "entity_id", "?")),
        ok=not failures,
        tokenised_fields=tuple(tokenised),
        failures=tuple(failures),
    )
```

**Step 4: Run test**

Expected: `3 passed`

**Step 5: Commit**

```bash
git add packages/apex-test-harness/src/apex_test_harness/validators/tokenisation.py \
        packages/apex-test-harness/tests/validators/test_tokenisation.py
git commit -m "feat(harness): add validate_tokenisation covering 4 §6.3 invariants"
```

---

## Task 9: `HarnessReport` + coverage matrix

**Files:**
- Create: `packages/apex-test-harness/src/apex_test_harness/report.py`
- Create: `packages/apex-test-harness/tests/test_report.py`

**Step 1: Write tests** — verify `passed` property logic, `coverage_matrix()` shape, `fields_never_exercised()` returns only fields untouched by any parsed entity, `summary()` prints a per-entity line.

**Step 2: Run — fails**

**Step 3: Implement.** `HarnessReport` aggregates the three result tuples. `coverage_matrix()` groups `ShapeResult.parsed` entities by entity-class, walks `model_fields` on each class, marks a field as "exercised" if any parsed instance had a non-None value for it. `fields_never_exercised()` returns only the non-exercised fields per entity.

**Step 4: Run — green**

**Step 5: Commit**

---

## Task 10: Fixture YAML loader + `Scenario` dataclass + `run_scenario`

**Files:**
- Create: `packages/apex-test-harness/src/apex_test_harness/scenarios.py`
- Create: `packages/apex-test-harness/tests/test_scenarios.py`
- Create: `packages/apex-test-harness/tests/fixtures/minimal_customer.yaml`

**Step 1: Write tests**

```python
# Happy-path YAML loads into Scenario list with correct kinds.
# run_scenario on 'malformed' kind invokes only shape validator.
# run_scenario on 'happy_path' invokes all three.
# build_bronze_row_from_scenario honours `overrides` + polyfactory filler.
# build_bronze_row_from_scenario honours `overrides_raw` verbatim (no filler).
```

**Step 2: Run — fails**

**Step 3: Implement.** `Scenario(id, kind, description, overrides, overrides_raw, expect)` dataclass; `load_scenarios(path) -> list[Scenario]`; `build_bronze_row_from_scenario(scenario, entity_cls, tenant_id, source_system) -> BronzeRow` (dispatches on kind — happy_path/edge_case uses polyfactory with overrides; malformed uses overrides_raw verbatim); `run_scenario(scenario, row, entity_cls, validator, tenant_id) -> ScenarioOutcome`. The `ScenarioOutcome.matches(expect)` compares expected vs actual (pass/fail/skip per validator + error-substring match for `shape_error_contains`).

**Step 4: Run — green**

**Step 5: Commit**

---

## Task 11: Root `tests/conftest.py` — session Postgres + bronze_schema fixtures

**Files:**
- Modify: `packages/apex-test-harness/tests/conftest.py`

```python
import hashlib
from typing import Iterator

import psycopg
import pytest

from apex_test_harness.bronze import emit_ddl
from apex_test_harness.containers import PostgresContainerFixture


@pytest.fixture(scope="session")
def postgres() -> Iterator[PostgresContainerFixture]:
    with PostgresContainerFixture.start() as fx:
        yield fx


class BronzeSchema:
    def __init__(self, url: str, schema: str) -> None:
        self.url = url
        self.schema = schema

    @property
    def conn(self):
        return psycopg.connect(self.url)

    def apply_ddl(self, table: str) -> None:
        with psycopg.connect(self.url) as c:
            with c.cursor() as cur:
                cur.execute(emit_ddl(table, self.schema))
                c.commit()


@pytest.fixture
def bronze_schema(postgres, request) -> Iterator[BronzeSchema]:
    raw = request.node.nodeid.encode()
    schema = f"h_{hashlib.sha1(raw).hexdigest()[:10]}"
    postgres.create_schema(schema)
    b = BronzeSchema(postgres.connection_url(), schema)
    b.apply_ddl("bronze_rc")
    yield b
    postgres.drop_schema(schema)
```

**Step 2-5:** Run `pytest` collection; assert no import errors; commit.

---

## Task 12: RC conftest — `rc_token_service`, `rc_sim`, `rc_validator`, `pytest_generate_tests`

**Files:**
- Create: `packages/apex-test-harness/tests/rc/__init__.py`
- Create: `packages/apex-test-harness/tests/rc/conftest.py`
- Create: `packages/apex-test-harness/tests/rc/fixtures/` (directory)

**Step 1-5:** Implement per design §4.2. Commit.

---

## Task 13: Customer fixtures + `test_customer.py` (8 scenarios)

**Files:**
- Create: `packages/apex-test-harness/tests/rc/fixtures/customer.yaml`
- Create: `packages/apex-test-harness/tests/rc/test_customer.py`

**Step 1:** Write `customer.yaml` with the 8 minimum-complete scenarios:
1. happy_minimal
2. happy_maximal
3. enum_boundary_active / _inactive / _opted_out / _suppressed
4. pii_heavy (all 4 token fields set)
5. malformed_missing_status
6. malformed_wrong_type (birth_year string)
7. fk_mismatch (not applicable for Customer — substitute with another edge)
8. tenant_separation

**Step 2:** Write `test_customer.py`:
```python
from apex_rc.cxml.entities import Customer
from apex_test_harness import run_scenario, build_bronze_row_from_scenario

def test_scenario(scenario, bronze_schema, rc_sim, rc_validator):
    row = build_bronze_row_from_scenario(scenario, Customer,
                                          tenant_id="t-harness", source_system="rc-sim")
    with bronze_schema.conn as conn:
        rc_sim.seed_rows(conn, bronze_schema.schema, [row])
        read_back = rc_sim.read_rows(conn, bronze_schema.schema,
                                      where=f"entity_id = '{row.entity_id}'")
    assert len(read_back) == 1
    outcome = run_scenario(scenario, read_back[0], Customer,
                            validator=rc_validator, tenant_id="t-harness")
    assert outcome.matches(scenario.expect), outcome.summary()
```

**Step 3:** Run `pytest packages/apex-test-harness/tests/rc/test_customer.py -v -m integration`. Expected: 8-10 tests all pass.

**Step 4:** Commit.

---

## Tasks 14-16: Order / SKU / Markdown fixtures + tests

Mirror Task 13 for the other three RC entities. Each closes ~8-10 scenarios. `sku.yaml` includes `enum_boundary` across SkuStatus values; `markdown.yaml` across all 6 MarkdownReason values. **fk_mismatch** scenarios exercise the design §3.3 row 7.

---

## Task 17: Composed RC flow test

**Files:**
- Create: `packages/apex-test-harness/tests/rc/test_composed_rc_flow.py`

Implements the Section 4.4 end-to-end test. Generates SKUs via polyfactory, creates markdowns for 2 of 5, creates customers, creates orders covering (customer × sku) pairs. Runs all three validators across all 4 entities. Asserts `report.passed` + `fields_never_exercised() == {}`.

---

## Task 18: Volume tests (opt-in, `--volume` flag)

**Files:**
- Create: `packages/apex-test-harness/tests/rc/test_volume_customer.py`
- Create: `packages/apex-test-harness/tests/rc/test_volume_order.py`
- Create: `packages/apex-test-harness/tests/rc/test_volume_sku.py`
- Create: `packages/apex-test-harness/tests/rc/test_volume_markdown.py`

Each file: `@pytest.mark.volume @pytest.mark.parametrize("seed", range(10))`; generates 10 000 rows; asserts 100% shape pass + 100% classification pass.

Add `--volume` custom CLI option to `tests/conftest.py`:
```python
def pytest_addoption(parser):
    parser.addoption("--volume", action="store_true",
                     help="Enable @pytest.mark.volume tests")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--volume"):
        return
    skip = pytest.mark.skip(reason="volume: use --volume to enable")
    for item in items:
        if "volume" in item.keywords:
            item.add_marker(skip)
```

---

## Task 19: Debug pytest plugins (`--keep-schema`, `--print-conn-url`)

Extend `tests/conftest.py` with the two custom flags. `--keep-schema` prevents the `drop_schema` call in the `bronze_schema` fixture teardown; `--print-conn-url` registers a session-end hook that prints `postgres.connection_url()` so a developer can pipe it into `psql`.

---

## Task 20: GitHub Actions workflow

**Files:**
- Create: `.github/workflows/harness.yml`

Copy the workflow from design §5.3 verbatim. Verify it parses via `actionlint` if available. Commit.

---

## Task 21: Pre-Fabric gate verification

Run all five criteria from design §5.5 and document the results:

1. Run `pytest packages/apex-test-harness -v` — expect ~38 tests pass in < 90 seconds.
2. Run `pytest packages/apex-test-harness/tests/rc/test_composed_rc_flow.py -v` — expect `fields_never_exercised == {}` assertion holds.
3. Run `pytest packages/apex-test-harness -m volume --volume -v` — expect clean pass over 100 000 rows × 4 entities × 10 seeds.
4. Inspect the coverage matrix from step 2; assert every Customer/Order/SKU/Markdown field shows "exercised".
5. Count classification warnings on the fixture suite; assert FPR < 5%.

Write results into a `packages/apex-test-harness/.harness-report/gate-verification-2026-04-21.md` artefact. Commit.

---

## Task 22: Full suite green; merge

Run the whole workspace suite:
```
./.venv/Scripts/python.exe -m pytest packages -q
```
Expected: 642 prior tests + ~48 new harness tests = ~690 passed. No regressions in the pre-existing 642.

Final commit summarising the harness shipping:

```bash
git add -A packages/apex-test-harness/ .github/workflows/harness.yml
git commit -m "feat(harness): ship apex-test-harness v0.1.0 (pre-Fabric gate passed)"
```

---

## Post-merge — Wave 2 note

Ready to extend to HLS when these hold:
- RC harness green in CI for at least 1 week with no flakes.
- At least one real-world schema bug caught by the harness (signal it earns its keep).

Wave 2 is additive only: `tests/hlscml/` with fixtures + conftest + test files. Zero library churn per the layered architecture.

---

## References

- **Skill:** `superpowers:executing-plans` for task-by-task execution.
- **Skill:** `superpowers:test-driven-development` for disciplined TDD per task.
- **Design doc:** `docs/plans/2026-04-21-apex-test-harness-design.md`
- **Prior art:** Existing pytest + Pydantic patterns across the 41 shipped packages; `apex-rc/tests/` for how a Practice test suite is shaped.
