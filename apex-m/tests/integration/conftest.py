"""pytest configuration for apex-m integration tests.

Sprint 41 — Phase I.1.
"""
from __future__ import annotations

import pytest


def pytest_configure(config):
    """Register the `integration` marker so unmarked runs skip these tests."""
    config.addinivalue_line(
        "markers",
        "integration: tests that hit a real Microsoft tenant. "
        "Requires APEX_TEST_TENANT_ID + APEX_TEST_CLIENT_ID env vars or "
        "Workload Identity Federation. Skipped by default.",
    )


def pytest_collection_modifyitems(config, items):
    """Skip integration tests unless explicitly requested via -m integration."""
    if config.getoption("-m") and "integration" in config.getoption("-m"):
        return
    skip_marker = pytest.mark.skip(reason="run with -m integration to execute")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_marker)
