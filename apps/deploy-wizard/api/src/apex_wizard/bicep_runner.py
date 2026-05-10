"""Sprint 46.1 — subprocess wrapper around `az deployment group what-if` / `create`.

Dual-mode by design:

- **Mock mode** (default; activated by env var ``APEX_FORCE_MOCK=true`` or by
  passing ``runner=MockBicepRunner()``): returns deterministic synthetic
  what-if diffs + correlation IDs. Used in unit tests + laptop substrate.

- **Real mode** (activated by setting ``APEX_FORCE_MOCK=false`` AND having
  ``az`` on PATH): shells out to the Azure CLI; streams stdout to a logger
  callback; parses JSON output into structured types.

The wizard's deploy button calls ``BicepRunner.what_if`` first and renders
the diff to the operator; on confirm, ``BicepRunner.deploy`` runs the
apply. Both calls update a :class:`BicepRunResult` audit-friendly record.

References
----------

- Sprint 46 build-status — `services/rc/_build-status.yaml` sprint-46.items[0]
- Pre-deployment Security Gate — `Pre-deployment-Security-Gate.md`
- AZ CLI reference: ``az deployment group what-if`` / ``az deployment group create``
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess  # noqa: S404 — wrapped + sanitised below
import time
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Callable, Literal, Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Structured result types
# ---------------------------------------------------------------------------


WhatIfChangeKind = Literal[
    "Create", "Delete", "Deploy", "Modify", "NoChange", "Ignore", "Unsupported",
]


@dataclass(frozen=True)
class WhatIfChange:
    """One resource-level change from ``az deployment group what-if``.

    Mirrors the shape of the AZ CLI's JSON output ``changes[]`` array,
    distilled to the fields the wizard's audit row + UI care about.
    """

    change_kind: WhatIfChangeKind
    resource_id: str
    resource_type: str
    before: dict | None = None
    after: dict | None = None


@dataclass(frozen=True)
class WhatIfResult:
    """Aggregated result of a ``what-if`` run."""

    blueprint_path: str
    parameters_path: str
    resource_group: str
    tenant: str
    ran_at: datetime
    duration_ms: int
    changes: tuple[WhatIfChange, ...]
    mode: Literal["mock", "real"]

    @property
    def counts(self) -> dict[str, int]:
        """Summary counts by change_kind — what the wizard UI renders."""
        out: dict[str, int] = {}
        for c in self.changes:
            out[c.change_kind] = out.get(c.change_kind, 0) + 1
        return out

    @property
    def has_destructive(self) -> bool:
        """True if any Delete changes are present.

        The wizard requires a second operator confirmation on what-if
        results that include destructive changes.
        """
        return any(c.change_kind == "Delete" for c in self.changes)


@dataclass(frozen=True)
class DeployResult:
    """Result of ``az deployment group create``.

    correlation_id is the Azure deployment id the operator can look up
    in the portal or follow via ``az deployment group show``.
    """

    correlation_id: str
    blueprint_path: str
    parameters_path: str
    resource_group: str
    tenant: str
    started_at: datetime
    completed_at: datetime
    duration_ms: int
    succeeded: bool
    outputs: dict
    error: str | None
    mode: Literal["mock", "real"]


# ---------------------------------------------------------------------------
# Protocol — the contract Mock + Real satisfy
# ---------------------------------------------------------------------------


@runtime_checkable
class BicepRunner(Protocol):
    """Run Bicep deployments. Implementations: :class:`MockBicepRunner`, :class:`RealBicepRunner`."""

    def what_if(
        self,
        *,
        tenant: str,
        resource_group: str,
        blueprint_path: str,
        parameters_path: str,
    ) -> WhatIfResult:
        ...

    def deploy(
        self,
        *,
        tenant: str,
        resource_group: str,
        blueprint_path: str,
        parameters_path: str,
    ) -> DeployResult:
        ...


# ---------------------------------------------------------------------------
# Real-mode runner — calls `az` via subprocess
# ---------------------------------------------------------------------------


class AzCliNotFoundError(RuntimeError):
    """Raised when ``az`` isn't on PATH and real mode is requested."""


class AzCliError(RuntimeError):
    """Raised when ``az`` returns non-zero or unparseable output."""

    def __init__(self, message: str, *, stderr: str = "", return_code: int = -1):
        super().__init__(message)
        self.stderr = stderr
        self.return_code = return_code


@dataclass
class RealBicepRunner:
    """Production runner — shells out to ``az deployment group ...``.

    The runner does NOT pass parameters as command-line args; it always
    uses the ``--parameters @<file>`` form to avoid shell-injection and
    keep the audit trail clean (the file is content-addressed via SHA256
    in the wizard's audit row).
    """

    az_path: str = "az"   # Override for testing with a custom binary path
    log: Callable[[str], None] | None = None
    timeout_seconds: int = 1800   # 30-minute hard ceiling per deploy

    def __post_init__(self) -> None:
        # Verify az is on PATH at construction so failures surface early.
        if shutil.which(self.az_path) is None:
            raise AzCliNotFoundError(
                f"Azure CLI binary {self.az_path!r} not on PATH. "
                "Install via https://learn.microsoft.com/cli/azure/install-azure-cli "
                "or use MockBicepRunner for offline tests."
            )

    def what_if(
        self,
        *,
        tenant: str,
        resource_group: str,
        blueprint_path: str,
        parameters_path: str,
    ) -> WhatIfResult:
        self._validate_paths(blueprint_path, parameters_path)
        started = datetime.now(UTC)
        t0 = time.monotonic()
        argv = [
            self.az_path, "deployment", "group", "what-if",
            "--resource-group", resource_group,
            "--template-file", blueprint_path,
            "--parameters", f"@{parameters_path}",
            "--output", "json",
            "--no-pretty-print",
        ]
        proc = self._run(argv)
        duration_ms = int((time.monotonic() - t0) * 1000)
        try:
            data = json.loads(proc.stdout) if proc.stdout else {}
        except json.JSONDecodeError as exc:
            raise AzCliError(
                f"az deployment group what-if returned unparseable JSON: {exc}",
                stderr=proc.stderr,
                return_code=proc.returncode,
            ) from None

        raw_changes = data.get("changes", []) if isinstance(data, dict) else []
        changes = tuple(_parse_change(c) for c in raw_changes)
        return WhatIfResult(
            blueprint_path=blueprint_path,
            parameters_path=parameters_path,
            resource_group=resource_group,
            tenant=tenant,
            ran_at=started,
            duration_ms=duration_ms,
            changes=changes,
            mode="real",
        )

    def deploy(
        self,
        *,
        tenant: str,
        resource_group: str,
        blueprint_path: str,
        parameters_path: str,
    ) -> DeployResult:
        self._validate_paths(blueprint_path, parameters_path)
        started = datetime.now(UTC)
        t0 = time.monotonic()
        argv = [
            self.az_path, "deployment", "group", "create",
            "--resource-group", resource_group,
            "--template-file", blueprint_path,
            "--parameters", f"@{parameters_path}",
            "--name", f"apex-{tenant}-{int(started.timestamp())}",
            "--output", "json",
            "--no-pretty-print",
        ]
        proc = self._run(argv)
        duration_ms = int((time.monotonic() - t0) * 1000)
        completed = datetime.now(UTC)

        succeeded = proc.returncode == 0
        error = proc.stderr.strip() if not succeeded else None
        try:
            data = json.loads(proc.stdout) if proc.stdout else {}
        except json.JSONDecodeError:
            data = {}

        outputs = data.get("properties", {}).get("outputs", {}) if isinstance(data, dict) else {}
        correlation_id = (
            data.get("properties", {}).get("correlationId") if isinstance(data, dict) else None
        ) or str(uuid.uuid4())

        return DeployResult(
            correlation_id=correlation_id,
            blueprint_path=blueprint_path,
            parameters_path=parameters_path,
            resource_group=resource_group,
            tenant=tenant,
            started_at=started,
            completed_at=completed,
            duration_ms=duration_ms,
            succeeded=succeeded,
            outputs=outputs,
            error=error,
            mode="real",
        )

    # --- internals ----------------------------------------------------

    def _validate_paths(self, blueprint_path: str, parameters_path: str) -> None:
        for p in (blueprint_path, parameters_path):
            if not Path(p).exists():
                raise FileNotFoundError(f"{p!r} does not exist; cannot run az")

    def _run(self, argv: list[str]) -> subprocess.CompletedProcess:
        if self.log:
            self.log(f"$ {' '.join(argv)}")
        try:
            return subprocess.run(   # noqa: S603 — argv list, no shell
                argv,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            raise AzCliError(
                f"az command exceeded {self.timeout_seconds}s timeout",
                stderr=str(exc),
            ) from None


def _parse_change(raw: dict) -> WhatIfChange:
    return WhatIfChange(
        change_kind=raw.get("changeType") or "NoChange",
        resource_id=raw.get("resourceId") or "",
        resource_type=raw.get("resourceType") or "",
        before=raw.get("before"),
        after=raw.get("after"),
    )


# ---------------------------------------------------------------------------
# Mock-mode runner — deterministic synthetic results
# ---------------------------------------------------------------------------


@dataclass
class MockBicepRunner:
    """Test / laptop substrate runner. Returns synthetic results.

    Configurable via class attributes for test scenarios:

    - ``preset_changes``: tuple of changes ``what_if`` returns
    - ``deploy_should_succeed``: bool — flip to test failure-path code
    - ``deploy_error_message``: optional error string when failing
    """

    preset_changes: tuple[WhatIfChange, ...] = field(default_factory=tuple)
    deploy_should_succeed: bool = True
    deploy_error_message: str | None = None
    log: Callable[[str], None] | None = None

    def what_if(
        self,
        *,
        tenant: str,
        resource_group: str,
        blueprint_path: str,
        parameters_path: str,
    ) -> WhatIfResult:
        if self.log:
            self.log(f"[mock] what-if tenant={tenant} blueprint={blueprint_path}")
        started = datetime.now(UTC)
        # If no preset_changes provided, synthesise a small deterministic
        # diff (matches the shape the operator would see in real mode).
        changes = self.preset_changes or _default_mock_changes(tenant)
        return WhatIfResult(
            blueprint_path=blueprint_path,
            parameters_path=parameters_path,
            resource_group=resource_group,
            tenant=tenant,
            ran_at=started,
            duration_ms=42,
            changes=changes,
            mode="mock",
        )

    def deploy(
        self,
        *,
        tenant: str,
        resource_group: str,
        blueprint_path: str,
        parameters_path: str,
    ) -> DeployResult:
        if self.log:
            self.log(f"[mock] deploy tenant={tenant} blueprint={blueprint_path}")
        started = datetime.now(UTC)
        time.sleep(0.001)
        completed = datetime.now(UTC)
        return DeployResult(
            correlation_id=f"mock-{uuid.uuid4()}",
            blueprint_path=blueprint_path,
            parameters_path=parameters_path,
            resource_group=resource_group,
            tenant=tenant,
            started_at=started,
            completed_at=completed,
            duration_ms=1,
            succeeded=self.deploy_should_succeed,
            outputs={"mockOutput": "ok"} if self.deploy_should_succeed else {},
            error=self.deploy_error_message if not self.deploy_should_succeed else None,
            mode="mock",
        )


def _default_mock_changes(tenant: str) -> tuple[WhatIfChange, ...]:
    """Synthesise a representative diff for a fresh tenant deploy."""
    return (
        WhatIfChange(
            change_kind="Create",
            resource_id=f"/subscriptions/MOCK/resourceGroups/rg-{tenant}/providers/Microsoft.App/managedEnvironments/cae-{tenant}",
            resource_type="Microsoft.App/managedEnvironments",
            after={"location": "eastus", "sku": {"name": "Consumption"}},
        ),
        WhatIfChange(
            change_kind="Create",
            resource_id=f"/subscriptions/MOCK/resourceGroups/rg-{tenant}/providers/Microsoft.KeyVault/vaults/kv-{tenant}",
            resource_type="Microsoft.KeyVault/vaults",
            after={"properties": {"enableRbacAuthorization": True}},
        ),
        WhatIfChange(
            change_kind="NoChange",
            resource_id=f"/subscriptions/MOCK/resourceGroups/rg-{tenant}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/uami-{tenant}",
            resource_type="Microsoft.ManagedIdentity/userAssignedIdentities",
        ),
    )


# ---------------------------------------------------------------------------
# Default runner factory — used by the deployments + drift endpoints
# ---------------------------------------------------------------------------


def get_default_runner(*, log: Callable[[str], None] | None = None) -> BicepRunner:
    """Return the right BicepRunner for the current environment.

    Selection rule:

    - If env var ``APEX_FORCE_MOCK == "true"`` → MockBicepRunner (laptop).
    - Else if ``az`` is on PATH → RealBicepRunner (lab/dev/stage/prod).
    - Else → MockBicepRunner with a warning logged (lets the test suite
      and CI work without az installed).
    """
    force_mock = os.environ.get("APEX_FORCE_MOCK", "").strip().lower() == "true"
    if force_mock:
        return MockBicepRunner(log=log)
    if shutil.which("az") is None:
        if log:
            log("[warn] az CLI not found; falling back to MockBicepRunner")
        return MockBicepRunner(log=log)
    return RealBicepRunner(log=log)


# ---------------------------------------------------------------------------
# Legacy free-function shim — kept for backward compat with deployments.py
# ---------------------------------------------------------------------------


def run_what_if(tenant: str, blueprint_path: str, parameters_path: str) -> dict:
    """Legacy free-function — wraps the default runner.

    Returns a structured dict the legacy code expected
    (``{added, modified, deleted, summary}``).
    """
    runner = get_default_runner()
    result = runner.what_if(
        tenant=tenant,
        resource_group=f"rg-{tenant}",
        blueprint_path=blueprint_path,
        parameters_path=parameters_path,
    )
    return {
        "added": [c.resource_id for c in result.changes if c.change_kind == "Create"],
        "modified": [c.resource_id for c in result.changes if c.change_kind in ("Modify", "Deploy")],
        "deleted": [c.resource_id for c in result.changes if c.change_kind == "Delete"],
        "no_change": [c.resource_id for c in result.changes if c.change_kind == "NoChange"],
        "summary": result.counts,
        "mode": result.mode,
        "duration_ms": result.duration_ms,
    }


def run_deploy(tenant: str, blueprint_path: str, parameters_path: str) -> str:
    """Legacy free-function — wraps the default runner, returns correlation id."""
    runner = get_default_runner()
    result = runner.deploy(
        tenant=tenant,
        resource_group=f"rg-{tenant}",
        blueprint_path=blueprint_path,
        parameters_path=parameters_path,
    )
    if not result.succeeded:
        raise AzCliError(f"deploy failed: {result.error or 'unknown error'}")
    return result.correlation_id
