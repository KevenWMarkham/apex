"""Tests for apex_wizard.drift (Sprint 46.4)."""

from __future__ import annotations

import pytest

from apex_wizard.bicep_runner import MockBicepRunner, WhatIfChange
from apex_wizard.drift import (
    DriftDetector,
    DriftFinding,
    DriftReport,
    _reset_drift_log_for_test,
    get_drift_history,
    run_drift_cron,
)


@pytest.fixture(autouse=True)
def _clear_log() -> None:
    _reset_drift_log_for_test()


# ---------------------------------------------------------------------------
# Detector — interpretation of what-if results as drift
# ---------------------------------------------------------------------------


def test_no_drift_when_what_if_returns_only_no_change() -> None:
    """A clean tenant — what-if shows NoChange only → no drift."""
    runner = MockBicepRunner(preset_changes=(
        WhatIfChange(change_kind="NoChange", resource_id="r1", resource_type="t"),
        WhatIfChange(change_kind="NoChange", resource_id="r2", resource_type="t"),
    ))
    detector = DriftDetector(runner=runner)
    report = detector.detect(
        tenant="bigbox",
        blueprint_path="/tmp/blueprint.bicep",
        parameters_path="/tmp/params.json",
        pinned_release="v1.0.0",
    )
    assert report.has_drift is False
    assert report.drift_count == 0
    assert report.severity == "none"


def test_drift_detected_when_what_if_shows_modifications() -> None:
    """A modified tenant — drift findings reflect the changes."""
    runner = MockBicepRunner(preset_changes=(
        WhatIfChange(change_kind="Modify", resource_id="r-mod", resource_type="t"),
        WhatIfChange(change_kind="NoChange", resource_id="r-nochange", resource_type="t"),
    ))
    detector = DriftDetector(runner=runner)
    report = detector.detect(
        tenant="bigbox",
        blueprint_path="/tmp/blueprint.bicep",
        parameters_path="/tmp/params.json",
        pinned_release="v1.0.0",
    )
    assert report.has_drift is True
    assert report.drift_count == 1
    assert report.findings[0].drift_kind == "modified"
    assert report.severity == "low"


def test_drift_severity_high_on_deletion() -> None:
    """Any deletion = high severity (incident-grade)."""
    runner = MockBicepRunner(preset_changes=(
        WhatIfChange(change_kind="Delete", resource_id="r-deleted", resource_type="t"),
    ))
    detector = DriftDetector(runner=runner)
    report = detector.detect(
        tenant="bigbox",
        blueprint_path="/tmp/blueprint.bicep",
        parameters_path="/tmp/params.json",
        pinned_release="v1.0.0",
    )
    assert report.severity == "high"


def test_drift_severity_medium_for_3_to_10_modifications() -> None:
    runner = MockBicepRunner(preset_changes=tuple(
        WhatIfChange(change_kind="Modify", resource_id=f"r-{i}", resource_type="t")
        for i in range(5)
    ))
    detector = DriftDetector(runner=runner)
    report = detector.detect(
        tenant="bigbox",
        blueprint_path="/tmp/blueprint.bicep",
        parameters_path="/tmp/params.json",
        pinned_release="v1.0.0",
    )
    assert report.drift_count == 5
    assert report.severity == "medium"


def test_drift_severity_high_for_more_than_10_modifications() -> None:
    runner = MockBicepRunner(preset_changes=tuple(
        WhatIfChange(change_kind="Modify", resource_id=f"r-{i}", resource_type="t")
        for i in range(11)
    ))
    detector = DriftDetector(runner=runner)
    report = detector.detect(
        tenant="bigbox",
        blueprint_path="/tmp/blueprint.bicep",
        parameters_path="/tmp/params.json",
        pinned_release="v1.0.0",
    )
    assert report.severity == "high"


def test_detector_preset_findings_override_what_if() -> None:
    """Test mode — feed canned findings instead of computing from what-if."""
    preset = (
        DriftFinding(
            resource_id="canned-r",
            resource_type="canned-t",
            drift_kind="modified",
        ),
    )
    runner = MockBicepRunner()
    detector = DriftDetector(runner=runner, preset_findings=preset)
    report = detector.detect(
        tenant="bigbox",
        blueprint_path="/tmp/blueprint.bicep",
        parameters_path="/tmp/params.json",
        pinned_release="v1.0.0",
    )
    assert report.findings == preset


def test_report_as_dict_serialises_findings() -> None:
    import json
    runner = MockBicepRunner(preset_changes=(
        WhatIfChange(change_kind="Modify", resource_id="r", resource_type="t"),
    ))
    detector = DriftDetector(runner=runner)
    report = detector.detect(
        tenant="bigbox",
        blueprint_path="/tmp/blueprint.bicep",
        parameters_path="/tmp/params.json",
        pinned_release="v1.0.0",
    )
    body = json.dumps(report.as_dict())
    assert "drift_count" in body
    assert "modified" in body


# ---------------------------------------------------------------------------
# Cron entrypoint — iterates across tenants + persists to log
# ---------------------------------------------------------------------------


def test_run_drift_cron_iterates_all_tenants() -> None:
    runner = MockBicepRunner(preset_changes=(
        WhatIfChange(change_kind="NoChange", resource_id="r", resource_type="t"),
    ))
    detector = DriftDetector(runner=runner)
    reports = run_drift_cron(
        tenants=["bigbox-prod", "smallchain-prod", "labtenant"],
        detector=detector,
    )
    assert len(reports) == 3
    tenants_seen = {r.tenant for r in reports}
    assert tenants_seen == {"bigbox-prod", "smallchain-prod", "labtenant"}


def test_run_drift_cron_persists_to_history() -> None:
    runner = MockBicepRunner(preset_changes=(
        WhatIfChange(change_kind="Modify", resource_id="r", resource_type="t"),
    ))
    detector = DriftDetector(runner=runner)
    run_drift_cron(tenants=["bigbox-prod"], detector=detector)
    history = get_drift_history("bigbox-prod")
    assert len(history) == 1
    assert history[0].drift_count == 1
    assert history[0].severity == "low"


def test_run_drift_cron_persists_history_across_runs() -> None:
    runner = MockBicepRunner(preset_changes=(
        WhatIfChange(change_kind="Modify", resource_id="r", resource_type="t"),
    ))
    detector = DriftDetector(runner=runner)
    run_drift_cron(tenants=["bigbox-prod"], detector=detector)
    run_drift_cron(tenants=["bigbox-prod"], detector=detector)
    history = get_drift_history("bigbox-prod")
    assert len(history) == 2
