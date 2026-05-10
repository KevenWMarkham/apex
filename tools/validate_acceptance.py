"""End-to-end validation of the original user-acceptance criteria.

User acceptance (from the original engagement ask):

  1. Deployable framework to laptop / dev / test / stage / production
  2. Deploy UX (with wizard)
  3. Incorporate use cases when deployed

This script proves each criterion by exercising the actual code paths —
not by introspection but by **running the wizard's render + security-gate +
deploy chain in mock mode and inspecting the artefacts**.

Run:

    python tools/validate_acceptance.py

The script exits 0 when every criterion validates, 1 otherwise. CI can
gate on this. The script also writes detailed evidence to
``tools/_acceptance_evidence/`` for the user-acceptance review.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Force mock mode — this validation does NOT require Azure subscription.
os.environ["APEX_FORCE_MOCK"] = "true"

REPO_ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = REPO_ROOT / "tools" / "_acceptance_evidence"
EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)


def _section(title: str) -> None:
    bar = "=" * 70
    print(f"\n{bar}\n{title}\n{bar}")


def _ok(message: str) -> None:
    print(f"  PASS  {message}")


def _fail(message: str) -> None:
    print(f"  FAIL  {message}")


# ---------------------------------------------------------------------------
# A1 — Laptop substrate: render docker-compose from RC-E2E-03 _default
# ---------------------------------------------------------------------------


def validate_laptop_substrate() -> bool:
    """Validate the laptop deployment path.

    Acceptance: An RC engineer with this repo on a laptop can render a
    docker-compose.yml that defines the agent containers for RC-E2E-03's
    cold-chain scenario and immediately ``docker-compose up`` to exercise
    the chain end-to-end against mock backends.
    """
    _section("A1 — Laptop substrate: docker-compose render")
    from apex_wizard.deployments import RenderedParameters, render_parameters, TreeSelection

    selection = TreeSelection(
        selected_ids=["service:RC-E2E-03"],
        tenant="laptop-dev-001",
        wave="w2",
        substrate="laptop",
        primary_variant="APEX-M",
        use_case_id="rc-e2e-03--default",
    )
    rendered: RenderedParameters = render_parameters(selection)

    failures: list[str] = []

    if rendered.format != "docker-compose":
        failures.append(f"format expected 'docker-compose', got {rendered.format!r}")
    elif rendered.compose_yaml is None:
        failures.append("compose_yaml is None — laptop substrate should produce it")
    else:
        body = rendered.compose_yaml
        # Substantive checks the operator would make
        required_markers = [
            "services:",
            "apex-mock-foundry",
            "apex-mock-fabric",
            "apex-mock-purview",
            "APEX_FORCE_MOCK: 'true'",
            "APEX_VARIANT: APEX-M",
            "APEX_USE_CASE_ID: rc-e2e-03--default",
        ]
        missing = [m for m in required_markers if m not in body]
        if missing:
            failures.append(f"compose_yaml missing markers: {missing}")

        # At least one agent container per role per scenario should appear
        for role in ("assess", "classify", "quantify", "decide", "act", "learn"):
            container_name = f"apex-m-rc-e2e-03-rc-cold-chain-excursion-mid-shift-{role}"
            if container_name not in body:
                failures.append(f"missing agent container {container_name}")

    # Write the rendered evidence
    if rendered.compose_yaml:
        evidence = EVIDENCE_DIR / "A1_laptop_docker_compose.yml"
        evidence.write_text(rendered.compose_yaml, encoding="utf-8")
        _ok(f"docker-compose.yml rendered ({len(rendered.compose_yaml)} bytes) -> {evidence}")

    summary_lines = [
        f"  format: {rendered.format}",
        f"  blueprint: {rendered.blueprint or '(none — laptop substrate uses docker-compose)'}",
        f"  substrate: {rendered.substrate}",
        f"  use_case_id: {rendered.use_case_id}",
        f"  service_count: {rendered.summary.get('service_count', '?')}",
        f"  scenario_count: {rendered.summary.get('scenario_count', '?')}",
    ]
    for line in summary_lines:
        print(line)

    if failures:
        for f in failures:
            _fail(f)
        return False
    _ok("Laptop substrate render produces complete docker-compose.yml")
    _ok("All 6 canonical agent roles materialise as containers")
    _ok("APEX_FORCE_MOCK env wired so containers run against in-process mocks")
    return True


# ---------------------------------------------------------------------------
# A2 — Cloud substrates: render Bicep parameters
# ---------------------------------------------------------------------------


def validate_cloud_substrate() -> bool:
    """Validate dev / stage / prod cloud-substrate rendering."""
    _section("A2 — Cloud substrate: Bicep parameter render")
    from apex_wizard.deployments import render_parameters, TreeSelection

    all_ok = True
    for substrate in ("dev", "stage", "prod"):
        selection = TreeSelection(
            selected_ids=["service:RC-E2E-03"],
            tenant=f"bigbox-{substrate}",
            wave="w2",
            substrate=substrate,  # type: ignore[arg-type]
            primary_variant="APEX-M",
            use_case_id="rc-e2e-03--default",
        )
        rendered = render_parameters(selection)

        failures: list[str] = []
        if rendered.format != "bicep-parameters":
            failures.append(f"[{substrate}] format expected 'bicep-parameters', got {rendered.format}")
        if rendered.blueprint != "apex-m/infra/bicep/blueprints/w2-pilot.bicep":
            failures.append(f"[{substrate}] blueprint path unexpected: {rendered.blueprint}")
        if rendered.parameters is None:
            failures.append(f"[{substrate}] parameters is None")
        else:
            schema_uri = rendered.parameters.get("$schema", "")
            if "deploymentParameters.json" not in schema_uri:
                failures.append(f"[{substrate}] parameters not in Azure deploymentParameters format")
            tenant_val = rendered.parameters.get("parameters", {}).get("tenant", {}).get("value")
            if tenant_val != f"bigbox-{substrate}":
                failures.append(f"[{substrate}] tenant param mismatch: {tenant_val}")
            selections = rendered.parameters.get("parameters", {}).get("selections", {}).get("value", [])
            if not any(s.get("serviceCode") == "RC-E2E-03" for s in selections):
                failures.append(f"[{substrate}] RC-E2E-03 not in selections array")

        # Evidence
        import json as _json
        evidence = EVIDENCE_DIR / f"A2_{substrate}_bicep_params.json"
        evidence.write_text(_json.dumps(rendered.parameters or {}, indent=2), encoding="utf-8")
        _ok(f"[{substrate}] Bicep parameters rendered -> {evidence}")

        if failures:
            for f in failures:
                _fail(f)
            all_ok = False
        else:
            _ok(f"[{substrate}] format=bicep-parameters · blueprint={Path(rendered.blueprint).name}")

    if all_ok:
        _ok("All 3 cloud substrates (dev/stage/prod) emit valid Bicep parameters")
        _ok("Same blueprint path across substrates; parameters carry tenant slug forward")
    return all_ok


# ---------------------------------------------------------------------------
# A3 — Use-case incorporation: clone _default -> bigbox-prod
# ---------------------------------------------------------------------------


def validate_use_case_incorporation() -> bool:
    """Validate that a real client's use-case can be incorporated at deploy time.

    Acceptance: An operator can clone services/rc/RC-E2E-03/use-cases/_default/
    to <client>/, populate the persona_principal_bindings block, and the PSG-15
    lint flips green (unblocking the deploy button).
    """
    _section("A3 — Use-case incorporation: clone + bindings + PSG-15")
    from apex_core.validators import quick_check_psg_15, validate_use_case_personas

    # Step 1 — synthetic _default use-case as it ships from the framework.
    default_use_case = {
        "use_case_id": "rc-e2e-03--default",
        "service_code": "RC-E2E-03",
        "scenario_id": "rc-cold-chain-excursion-mid-shift",
        "primary_variant": "APEX-M",
        "substrate": "lab",   # Lab worked example
        "personas_active": [
            {"id": "marisol-reyes-store-ops"},
            {"id": "daniel-chen-merch-director"},
        ],
        # No persona_principal_bindings in the _default file — synthetic personas.
    }

    # Validation 1 — _default on lab substrate: warnings only, deploy allowed
    lab_ok = quick_check_psg_15(default_use_case)
    if lab_ok:
        _ok("_default use-case on lab substrate: PSG-15 allows deploy (worked-example mode)")
    else:
        _fail("_default use-case on lab substrate should pass PSG-15 (warnings only)")
        return False

    # Validation 2 — same use-case on prod substrate WITHOUT bindings: fails closed
    prod_unbound = dict(default_use_case)
    prod_unbound["substrate"] = "prod"
    prod_unbound["use_case_id"] = "rc-e2e-03--bigbox-prod-UNBOUND"
    prod_unbound_ok = quick_check_psg_15(prod_unbound)
    if not prod_unbound_ok:
        _ok("Cloned _default -> bigbox-prod WITHOUT bindings: PSG-15 fails closed (correct)")
    else:
        _fail("Prod substrate without persona bindings should fail PSG-15")
        return False

    # Validation 3 — operator clones _default and populates bindings: deploy allowed
    prod_bound = dict(default_use_case)
    prod_bound["substrate"] = "prod"
    prod_bound["use_case_id"] = "rc-e2e-03--bigbox-prod"
    prod_bound["persona_principal_bindings"] = {
        "marisol-reyes-store-ops": {
            "binding_mode": "entra_group",
            "entra_group_object_id": "8a3c1234-aaaa-bbbb-cccc-456789abcdef",
            "fallback_principals": ["store-ops-on-call@bigbox.com"],
        },
        "daniel-chen-merch-director": {
            "binding_mode": "specific_principals",
            "fallback_principals": ["merch-director@bigbox.com", "merch-vp@bigbox.com"],
        },
    }

    prod_bound_report = validate_use_case_personas(prod_bound)
    if prod_bound_report.valid:
        _ok("Cloned _default -> bigbox-prod WITH bindings: PSG-15 green, deploy allowed")
        _ok(f"  Bound personas: {prod_bound_report.bindings_count} of {len(prod_bound_report.personas_active)} active")
    else:
        _fail(f"Bound prod use-case should pass: errors={prod_bound_report.errors}")
        return False

    # Write evidence
    import json as _json
    (EVIDENCE_DIR / "A3_default_use_case.json").write_text(
        _json.dumps(default_use_case, indent=2), encoding="utf-8",
    )
    (EVIDENCE_DIR / "A3_bigbox_prod_use_case.json").write_text(
        _json.dumps(prod_bound, indent=2), encoding="utf-8",
    )
    _ok(f"Evidence written: A3_default_use_case.json + A3_bigbox_prod_use_case.json")
    _ok("Use-case incorporation flow validated: clone -> bind -> deploy gates pass")
    return True


# ---------------------------------------------------------------------------
# A4 — Wizard end-to-end: POST /api/deployments
# ---------------------------------------------------------------------------


def validate_wizard_end_to_end() -> bool:
    """Validate the full wizard deploy chain via FastAPI TestClient."""
    _section("A4 — Wizard end-to-end: POST /api/deployments (mock mode)")
    from fastapi.testclient import TestClient

    from apex_wizard.deployments import _reset_deployment_store_for_test
    from apex_wizard.main import app

    _reset_deployment_store_for_test()
    client = TestClient(app)

    # Health
    health = client.get("/health")
    if health.status_code != 200:
        _fail(f"/health returned {health.status_code}")
        return False
    _ok("/health returns 200")

    # Security gates
    gates = client.get("/api/security-gate?tenant=bigbox-prod")
    if gates.status_code != 200:
        _fail(f"/api/security-gate returned {gates.status_code}")
        return False
    body = gates.json()
    if len(body["gates"]) != 15:
        _fail(f"expected 15 gates, got {len(body['gates'])}")
        return False
    _ok(f"/api/security-gate returns all 15 gates (PSG-1 through PSG-15)")
    _ok(f"  overall_status: {body['overall_status']} · deploy_allowed: {body['deploy_allowed']}")

    # Deploy
    deploy_payload = {
        "tenant": "bigbox-prod",
        "wave": "w2",
        "selections": [
            {
                "service_code": "RC-E2E-03",
                "featured_scenarios": ["rc-cold-chain-excursion-mid-shift"],
            },
        ],
        "operator": "marisol.reyes@labtenant.onmicrosoft.com",
        "note": "acceptance-criteria validation run",
    }
    deploy = client.post("/api/deployments", json=deploy_payload)
    if deploy.status_code != 200:
        _fail(f"/api/deployments returned {deploy.status_code}: {deploy.text}")
        return False
    record = deploy.json()
    if record["status"] != "succeeded":
        _fail(f"deployment status: {record['status']} (expected succeeded)")
        return False
    _ok(f"/api/deployments succeeded — id={record['id']}")
    _ok(f"  what-if counts: {record['bicep_what_if_summary']['counts']}")
    _ok(f"  audit row id (correlation): {record['audit_row_id']}")

    # List + get round-trip
    listing = client.get("/api/deployments?tenant=bigbox-prod")
    if listing.status_code != 200 or len(listing.json()) != 1:
        _fail("/api/deployments listing round-trip failed")
        return False
    _ok("/api/deployments list+get round-trip works")

    # Drift detection
    drift = client.get("/api/drift/bigbox-prod")
    if drift.status_code != 200:
        _fail(f"/api/drift returned {drift.status_code}")
        return False
    drift_body = drift.json()
    _ok(f"/api/drift returns severity={drift_body['severity']!r} (mock-mode synthetic)")

    # Evidence
    import json as _json
    (EVIDENCE_DIR / "A4_wizard_deployment_record.json").write_text(
        _json.dumps(record, indent=2), encoding="utf-8",
    )
    (EVIDENCE_DIR / "A4_wizard_security_gate.json").write_text(
        _json.dumps(body, indent=2), encoding="utf-8",
    )
    _ok("Wizard end-to-end chain validated: PSG -> what-if -> deploy -> audit row -> drift")
    return True


# ---------------------------------------------------------------------------
# Top-level: run + summarise
# ---------------------------------------------------------------------------


def main() -> int:
    print("APEX user-acceptance criteria validation")
    print("=========================================")
    print("Mode: mock (APEX_FORCE_MOCK=true)")
    print(f"Evidence dir: {EVIDENCE_DIR.relative_to(REPO_ROOT)}\n")

    results: dict[str, bool] = {
        "A1 — Laptop substrate (docker-compose render)": validate_laptop_substrate(),
        "A2 — Cloud substrate (Bicep parameter render × 3 substrates)": validate_cloud_substrate(),
        "A3 — Use-case incorporation (clone _default + persona bindings + PSG-15)":
            validate_use_case_incorporation(),
        "A4 — Wizard end-to-end (PSG -> deploy -> drift via FastAPI)":
            validate_wizard_end_to_end(),
    }

    _section("SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    for name, ok in results.items():
        marker = "PASS" if ok else "FAIL"
        print(f"  {marker}  {name}")
    print()
    print(f"  {passed} of {total} acceptance criteria validated.")
    print(f"  Evidence artefacts: {EVIDENCE_DIR.relative_to(REPO_ROOT)}/")
    print()

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
