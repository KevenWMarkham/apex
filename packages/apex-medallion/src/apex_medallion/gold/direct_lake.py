"""Direct Lake semantic-model descriptor + TMDL-ish renderer.

A full TMDL (Tabular Model Definition Language) writer is out of scope for
Sprint 6 — tenants use the Power BI / Fabric tooling for the final definition.
This module produces a readable, reviewable descriptor that captures APEX's
opinionated shape of a Direct Lake semantic model for a Practice, with
measures sourced from the :class:`MeasureRegistry`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from apex_medallion.gold.measure import MeasureDefinition, MeasureLanguage


@dataclass(frozen=True, slots=True)
class TableSpec:
    """One table inside a semantic model."""

    name: str
    silver_delta_path: str
    """OneLake path / qualified Delta table the semantic model reads via Direct Lake."""
    columns: tuple[str, ...]
    measures: tuple[MeasureDefinition, ...] = ()

    def dax_measures(self) -> list[MeasureDefinition]:
        return [m for m in self.measures if m.language is MeasureLanguage.DAX]


@dataclass(frozen=True, slots=True)
class SemanticModelSpec:
    """A Direct Lake semantic model spanning one or more Silver Delta tables."""

    model_name: str
    tables: tuple[TableSpec, ...]
    culture: str = "en-US"
    notes: str = ""

    def total_measures(self) -> int:
        return sum(len(t.dax_measures()) for t in self.tables)


def render_tmdl(spec: SemanticModelSpec) -> str:
    """Render a human-readable TMDL-flavoured body for ``spec``.

    This is not production TMDL — it's a readable descriptor suitable for a
    code review and for handing to a Power BI developer to codify into a real
    ``.tmdl`` file.
    """
    lines: list[str] = [f"model {spec.model_name}", f"    culture {spec.culture}", ""]
    for t in spec.tables:
        lines.append(f"    table {t.name}")
        lines.append(f"        source {t.silver_delta_path}  -- Direct Lake")
        for col in t.columns:
            lines.append(f"        column {col}")
        for m in t.dax_measures():
            lines.append(f"        measure {m.name}  -- owner: {m.owner}  v{m.version}")
            lines.append(f"            expression = {m.formula}")
        lines.append("")
    if spec.notes:
        lines.append(f"    -- {spec.notes}")
    return "\n".join(lines).rstrip() + "\n"
