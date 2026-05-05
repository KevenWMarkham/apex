"""apex-purview Typer subcommands.

Attached to the top-level ``apex`` CLI via conditional import in
``apex_core.cli``.

Subcommands:

    apex purview emit-classifications <schema.yaml> [--include-all]
    apex purview emit-attachments     <schema.yaml>
    apex purview list-classifications
"""

from __future__ import annotations

import json
from pathlib import Path

import typer

from apex_purview.classifications import (
    APEX_CLASSIFICATIONS,
    emit_classification_typedefs,
    emit_entity_classifications,
    enumerate_classifications,
    load_schema_yaml,
)
from apex_purview.lineage import (
    emit_from_spec,
    emit_lineage_batch,
    emit_process_typedefs,
    load_lineage_spec,
)
from apex_purview.dlp import (
    DEFAULT_DLP_MATRIX,
    SURFACES,
    build_default_bundle,
    emit_dlp_payload,
    lookup_action,
)
from apex_purview.retention import (
    DEFAULT_RETENTION_MATRIX,
    build_default_retention_bundle,
    emit_retention_payload,
    lookup_retention,
)
from apex_purview.catalog import emit_catalog_bundle, emit_relationship_typedefs
from apex_purview.propagation import build_propagation_graph, validate_propagation
from apex_purview._register import print_report, register_all

purview_app = typer.Typer(
    name="purview",
    help="APEX Purview integration — classification / lineage / DLP / catalog emitters.",
    no_args_is_help=True,
)


@purview_app.command("emit-classifications")
def emit_classifications_cmd(
    schema: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        help="APEX canonical schema YAML.",
    ),
    include_all: bool = typer.Option(
        False,
        "--include-all",
        help=(
            "Emit every APEX classification (for Purview bootstrap). "
            "Default: only classifications referenced in the schema."
        ),
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Write JSON to this file. Default: stdout.",
    ),
) -> None:
    """Emit Purview classification type-def payload for a schema."""
    doc = load_schema_yaml(schema)
    payload = emit_classification_typedefs(doc, include_all=include_all)
    body = json.dumps(payload, indent=2, sort_keys=True)
    if output is None:
        typer.echo(body)
    else:
        output.write_text(body + "\n", encoding="utf-8")
        typer.echo(f"Wrote {output} ({len(payload['classificationDefs'])} classificationDefs)")


@purview_app.command("emit-attachments")
def emit_attachments_cmd(
    schema: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        help="APEX canonical schema YAML.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Write JSON to this file. Default: stdout.",
    ),
) -> None:
    """Emit per-entity / per-attribute classification attachment payload."""
    doc = load_schema_yaml(schema)
    attachments = emit_entity_classifications(doc)
    body = json.dumps(attachments, indent=2, sort_keys=True)
    if output is None:
        typer.echo(body)
    else:
        output.write_text(body + "\n", encoding="utf-8")
        typer.echo(f"Wrote {output} ({len(attachments)} attachments)")


@purview_app.command("register-all")
def register_all_cmd(
    root: Path = typer.Option(
        Path("."),
        "--root",
        help="Repository root to scan for schema YAMLs.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Directory where per-schema payloads are written. "
        "Omit for validate-only mode.",
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Non-zero exit if zero schemas were discovered.",
    ),
) -> None:
    """Discover every schema YAML and emit Purview payloads in one pass.

    Intended for CI: fails the build if any schema produces an emission
    error. With ``--output``, writes reviewable JSON artifacts for every
    schema to a structured directory.
    """
    report = register_all(root, output)
    print_report(report)

    if strict and not report.results:
        raise typer.Exit(code=2)
    raise typer.Exit(code=report.exit_code)


@purview_app.command("emit-lineage")
def emit_lineage_cmd(
    spec: Path = typer.Argument(
        ...,
        exists=True,
        readable=True,
        help="Lineage YAML spec (kind: lineage).",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Write Atlas bulk-body JSON to this file. Default: stdout.",
    ),
) -> None:
    """Emit Atlas v2 lineage bulk-body from a declarative lineage spec."""
    doc = load_lineage_spec(spec)
    processes = emit_from_spec(doc)
    payload = emit_lineage_batch(processes)
    body = json.dumps(payload, indent=2, sort_keys=True)
    if output is None:
        typer.echo(body)
    else:
        output.write_text(body + "\n", encoding="utf-8")
        typer.echo(f"Wrote {output} ({len(payload['entities'])} lineage processes)")


@purview_app.command("emit-process-typedefs")
def emit_process_typedefs_cmd(
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Write JSON to this file. Default: stdout.",
    ),
) -> None:
    """Emit the seven APEX lineage Process type-defs for Purview bootstrap."""
    payload = emit_process_typedefs()
    body = json.dumps(payload, indent=2, sort_keys=True)
    if output is None:
        typer.echo(body)
    else:
        output.write_text(body + "\n", encoding="utf-8")
        typer.echo(f"Wrote {output} ({len(payload['entityDefs'])} Process type-defs)")


@purview_app.command("emit-dlp")
def emit_dlp_cmd(
    output: Path | None = typer.Option(None, "--output", "-o"),
) -> None:
    """Emit the default APEX DLP policy bundle."""
    bundle = build_default_bundle()
    payload = emit_dlp_payload(bundle)
    body = json.dumps(payload, indent=2, sort_keys=True)
    if output is None:
        typer.echo(body)
    else:
        output.write_text(body + "\n", encoding="utf-8")
        typer.echo(f"Wrote {output} ({len(payload['rules'])} DLP rules)")


@purview_app.command("dlp-lookup")
def dlp_lookup_cmd(
    classification: str = typer.Argument(..., help="APEX classification key."),
    surface: str = typer.Argument(..., help=f"Surface, one of {SURFACES}."),
) -> None:
    """Look up the DLP action for a (classification, surface) pair."""
    typer.echo(lookup_action(classification, surface))


@purview_app.command("emit-retention")
def emit_retention_cmd(
    output: Path | None = typer.Option(None, "--output", "-o"),
) -> None:
    """Emit the default APEX retention policy bundle."""
    bundle = build_default_retention_bundle()
    payload = emit_retention_payload(bundle)
    body = json.dumps(payload, indent=2, sort_keys=True)
    if output is None:
        typer.echo(body)
    else:
        output.write_text(body + "\n", encoding="utf-8")
        typer.echo(f"Wrote {output} ({len(payload['rules'])} retention rules)")


@purview_app.command("retention-lookup")
def retention_lookup_cmd(
    classification: str = typer.Argument(..., help="APEX classification key."),
) -> None:
    """Look up the retention duration for a classification."""
    typer.echo(lookup_retention(classification))


@purview_app.command("emit-catalog")
def emit_catalog_cmd(
    schema: Path = typer.Argument(..., exists=True, readable=True),
    output: Path | None = typer.Option(None, "--output", "-o"),
) -> None:
    """Emit the Unified Catalog bundle (glossary terms + relationships) for a schema."""
    doc = load_schema_yaml(schema)
    bundle = emit_catalog_bundle(doc)
    body = json.dumps(bundle, indent=2, sort_keys=True)
    if output is None:
        typer.echo(body)
    else:
        output.write_text(body + "\n", encoding="utf-8")
        typer.echo(
            f"Wrote {output} ({len(bundle['terms'])} terms, "
            f"{len(bundle['relationships'])} relationships)"
        )


@purview_app.command("emit-relationship-typedefs")
def emit_relationship_typedefs_cmd(
    output: Path | None = typer.Option(None, "--output", "-o"),
) -> None:
    """Emit Atlas relationshipDef payload for apex_fk + apex_join."""
    payload = emit_relationship_typedefs()
    body = json.dumps(payload, indent=2, sort_keys=True)
    if output is None:
        typer.echo(body)
    else:
        output.write_text(body + "\n", encoding="utf-8")
        typer.echo(f"Wrote {output} ({len(payload['relationshipDefs'])} relationshipDefs)")


@purview_app.command("validate-propagation")
def validate_propagation_cmd(
    schemas: list[Path] = typer.Argument(..., exists=True, readable=True),
    lineage: Path | None = typer.Option(
        None, "--lineage", help="Optional lineage spec to wire Gold inputs."
    ),
) -> None:
    """Validate classification propagation across schemas (and optional lineage).

    Walks the Silver → Gold chain, computes most-restrictive inheritance,
    fails non-zero on any violation. Designed for CI.
    """
    schema_docs = [load_schema_yaml(s) for s in schemas]
    lineage_doc = load_lineage_spec(lineage) if lineage is not None else None
    nodes = build_propagation_graph(schema_docs, lineage_doc)
    report = validate_propagation(nodes)

    typer.echo(report.summary())
    for v in report.violations:
        typer.echo(
            f"  VIOLATION  {v.layer}  {v.node}  "
            f"declared={v.declared_classification}  required={v.required_classification}"
        )
        for input_name, input_class in v.triggering_inputs:
            typer.echo(f"    triggered by {input_name} ({input_class})")

    raise typer.Exit(code=report.exit_code)


@purview_app.command("list-classifications")
def list_classifications_cmd(
    schema: Path | None = typer.Argument(
        None,
        help="Optional schema YAML. If provided, lists only the "
        "classifications referenced by it; otherwise lists all APEX classifications.",
    ),
) -> None:
    """List APEX classification definitions."""
    if schema is None:
        keys = sorted(APEX_CLASSIFICATIONS.keys())
    else:
        doc = load_schema_yaml(schema)
        keys = sorted(enumerate_classifications(doc))

    for key in keys:
        spec = APEX_CLASSIFICATIONS.get(key)
        if spec is None:
            typer.echo(f"  {key}  [UNKNOWN — extend APEX_CLASSIFICATIONS]")
            continue
        typer.echo(f"  {key:22}  {spec['type_name']:24}  {spec['description'][:80]}")
