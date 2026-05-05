"""Root conftest for the APEX workspace.

Shared fixtures available to every package's test suite.
"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def repo_root() -> Path:
    """Absolute path to the APEX repository root."""
    return Path(__file__).parent


@pytest.fixture
def fixtures_dir(request: pytest.FixtureRequest) -> Path:
    """Return the per-package fixtures directory.

    Resolves to ``packages/<pkg>/tests/fixtures/`` relative to the test file
    that requested it.
    """
    return Path(request.path).parent / "fixtures"
