"""One-time harvester: build registry YAML manifests from existing catalogs.

Run from package root after Sprint 16/17/18 catalogs are stable. Idempotent —
will overwrite existing harvest-generated YAMLs but skip files marked
``# harvest:hand-edited`` in their first line.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from apex_agents import scan_all_catalogs as scan_agents
from apex_services import scan_all_catalogs as scan_services
from apex_references import scan_all_references


REGISTRY_DIR = Path(__file__).parent / "src" / "apex_registries"


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")[:80]


def is_hand_edited(p: Path) -> bool:
    if not p.exists():
        return False
    try:
        first = p.read_text(encoding="utf-8").splitlines()[0]
        return "harvest:hand-edited" in first
    except (OSError, IndexError):
        return False


def write_yaml(path: Path, data: dict) -> None:
    if is_hand_edited(path):
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        fh.write("# harvest:auto-generated — apex_registries.harvest\n")
        yaml.safe_dump(
            data, fh, sort_keys=False, default_flow_style=False, allow_unicode=True
        )


def harvest_kpis() -> int:
    """Build KPI registry from agents + services."""
    out_dir = REGISTRY_DIR / "kpis"
    seen: dict[str, dict] = {}

    # From agents (Sprint 16) — KpiTarget on each spec
    for prac, entries in scan_agents().items():
        for entry in entries:
            for k in entry.spec.kpis:
                key = (prac, k.name)
                seen.setdefault(
                    key,
                    dict(
                        kind="kpi",
                        kpi_id=f"kpi.{prac}.{slugify(k.name)}",
                        name=k.name,
                        practice=prac,
                        direction=k.direction,
                        description=(
                            f"KPI tracked by APEX {prac.upper()} agents/services. "
                            "Wave-2 typical movement defined by source manifests."
                        ),
                        measurement_pattern="audit-row attribution against pre-engagement baseline",
                        typical_baseline="",
                        typical_wave2_target=k.target_band or "",
                        typical_wave3_target="",
                        units="",
                        cadence="monthly",
                        appendix_c_section=f"Appendix C — {prac.upper()} KPIs",
                    ),
                )

    # From services (Sprint 17) — KpiCommitment
    for prac, entries in scan_services().items():
        for entry in entries:
            for k in entry.spec.kpis:
                key = (prac, k.name)
                cur = seen.get(
                    key,
                    dict(
                        kind="kpi",
                        kpi_id=f"kpi.{prac}.{slugify(k.name)}",
                        name=k.name,
                        practice=prac,
                        direction=k.direction,
                        description=(
                            f"KPI tracked by APEX {prac.upper()} services. "
                            "Wave-2 typical movement defined by source manifests."
                        ),
                        measurement_pattern=k.measurement_pattern
                        or "audit-row attribution against pre-engagement baseline",
                        typical_baseline=k.baseline,
                        typical_wave2_target=k.wave2_target,
                        typical_wave3_target=k.wave3_target,
                        units="",
                        cadence="monthly",
                        appendix_c_section=f"Appendix C — {prac.upper()} KPIs",
                    ),
                )
                # Enrich with service-level baseline/targets if available
                if k.baseline and not cur.get("typical_baseline"):
                    cur["typical_baseline"] = k.baseline
                if k.wave2_target and not cur.get("typical_wave2_target"):
                    cur["typical_wave2_target"] = k.wave2_target
                if k.wave3_target and not cur.get("typical_wave3_target"):
                    cur["typical_wave3_target"] = k.wave3_target
                if k.measurement_pattern and not cur.get("measurement_pattern"):
                    cur["measurement_pattern"] = k.measurement_pattern
                seen[key] = cur

    count = 0
    for (prac, name), data in seen.items():
        fname = f"{prac}-{slugify(name)}.yaml"
        write_yaml(out_dir / fname, data)
        count += 1
    return count


def harvest_personas() -> int:
    """Build Persona catalog from agents + services + references."""
    out_dir = REGISTRY_DIR / "personas"
    seen: dict[tuple[str, str], dict] = {}

    def upsert(name: str, prac: str, source: str) -> None:
        key = (prac, name)
        if key in seen:
            return
        # Heuristic seniority
        nl = name.lower()
        if any(t in nl for t in ["chief ", "cmo", "ceo", "cfo", "ciso", "cio", "coo"]):
            seniority = "c-suite"
        elif "svp" in nl:
            seniority = "svp"
        elif "vp" in nl or "vice president" in nl:
            seniority = "vp"
        elif "director" in nl or "head of" in nl:
            seniority = "director"
        elif "manager" in nl or "supervisor" in nl or "lead" in nl:
            seniority = "manager"
        else:
            seniority = "individual-contributor"
        seen[key] = dict(
            kind="persona",
            persona_id=f"persona.{prac}.{slugify(name)}",
            name=name,
            practice=prac,
            seniority=seniority,
            function=source,
            description=(
                f"{name} ({prac.upper()}). Persona referenced by APEX "
                f"{source} manifests."
            ),
            typical_decisions=[],
            pains=[],
            metrics_owned=[],
            appendix_e_section=f"Appendix E — {prac.upper()} Personas",
        )

    for prac, entries in scan_agents().items():
        for entry in entries:
            upsert(entry.spec.persona, prac, "agent")
    for prac, entries in scan_services().items():
        for entry in entries:
            for p in entry.spec.personas:
                upsert(p.name, prac, "service")
    for entry in scan_all_references():
        for p in entry.spec.sponsor_personas:
            upsert(p, entry.spec.practice, "reference-deployment")

    count = 0
    for (prac, name), data in seen.items():
        fname = f"{prac}-{slugify(name)}.yaml"
        write_yaml(out_dir / fname, data)
        count += 1
    return count


def harvest_mcp_tools() -> int:
    """Build MCP tool catalog from agents."""
    out_dir = REGISTRY_DIR / "mcp_tools"
    seen: dict[str, dict] = {}

    for prac, entries in scan_agents().items():
        for entry in entries:
            for t in entry.spec.tools:
                if t.tool_id in seen:
                    if t.write and not seen[t.tool_id].get("write"):
                        seen[t.tool_id]["write"] = True
                    continue
                # Infer SOR / layer from tool id
                parts = t.tool_id.split(".")
                sor_or_layer = parts[3] if len(parts) >= 4 else "unknown"
                related = []
                if sor_or_layer.upper().endswith("ML"):
                    related = [sor_or_layer.upper()]
                seen[t.tool_id] = dict(
                    kind="mcp_tool",
                    tool_id=t.tool_id,
                    practice=prac,
                    sor_or_layer=sor_or_layer,
                    purpose=t.purpose,
                    write=t.write,
                    inputs_schema="",
                    outputs_schema="",
                    classification_required=[],
                    related_canonical_schemas=related,
                    appendix_f_section=f"Appendix F — {prac.upper()} MCP Tools",
                )

    count = 0
    for tool_id, data in seen.items():
        fname = f"{slugify(tool_id)}.yaml"
        write_yaml(out_dir / fname, data)
        count += 1
    return count


if __name__ == "__main__":
    n_kpi = harvest_kpis()
    n_per = harvest_personas()
    n_mcp = harvest_mcp_tools()
    print(f"KPIs harvested:        {n_kpi}")
    print(f"Personas harvested:    {n_per}")
    print(f"MCP tools harvested:   {n_mcp}")
