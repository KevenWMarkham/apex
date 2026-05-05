"""Adapter catalog — discovers and loads every shipped manifest.

The 15 reference manifests live under
``packages/apex-adapters/src/apex_adapters/manifests/`` and are
shipped as part of the package. Engagement-specific overrides land in
client repos and are loaded explicitly.
"""

from __future__ import annotations

from pathlib import Path

from apex_adapters.framework import AdapterSpec, load_adapter_spec


#: Canonical filename → declared subtask mapping. Keyed by
#: ``adapter_name`` (matches the ``name`` field in each YAML).
ADAPTER_REGISTRY: dict[str, dict[str, str]] = {
    "epic-clarity":              {"subtask": "15.1.1", "track": "HLS"},
    "hl7-fhir":                  {"subtask": "15.1.2", "track": "HLS"},
    "sap-s4hana":                {"subtask": "15.2.1", "track": "ERP"},
    "oracle-ebs-fusion":         {"subtask": "15.2.2", "track": "ERP"},
    "salesforce":                {"subtask": "15.3.1", "track": "CRM"},
    "workday-hcm":               {"subtask": "15.3.2", "track": "HCM"},
    "servicenow":                {"subtask": "15.3.3", "track": "ITSM"},
    "salesforce-marketing-cloud": {"subtask": "15.3.4", "track": "MarTech"},
    "manhattan-wms":             {"subtask": "15.4.1", "track": "Supply"},
    "sap-ariba-coupa":           {"subtask": "15.4.2", "track": "Supply"},
    "osi-pi":                    {"subtask": "15.5.1", "track": "Historian"},
    "ge-proficy":                {"subtask": "15.5.2", "track": "Historian"},
    "as400-db2":                 {"subtask": "15.6.1", "track": "Legacy"},
    "analytics-platforms":       {"subtask": "15.6.2", "track": "Analytics"},
    "snowflake-databricks":      {"subtask": "15.6.3", "track": "Interop"},
}


def manifests_dir() -> Path:
    """Return the directory holding the shipped reference manifests."""
    return Path(__file__).parent / "manifests"


def list_shipped_manifests() -> list[str]:
    """Return the adapter names of every shipped reference manifest."""
    yamls = sorted(p.stem for p in manifests_dir().glob("*.yaml"))
    return yamls


def load_shipped_manifest(adapter_name: str) -> AdapterSpec:
    """Load a shipped reference manifest by adapter name."""
    path = manifests_dir() / f"{adapter_name}.yaml"
    if not path.exists():
        raise FileNotFoundError(
            f"No shipped manifest for adapter {adapter_name!r}. "
            f"Available: {list_shipped_manifests()}"
        )
    return load_adapter_spec(path)


def load_all_shipped_manifests() -> dict[str, AdapterSpec]:
    """Load every shipped manifest. Useful for CI conformance checks."""
    return {name: load_shipped_manifest(name) for name in list_shipped_manifests()}
