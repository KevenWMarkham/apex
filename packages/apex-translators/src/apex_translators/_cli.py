"""apex-translators Typer subcommands."""

from __future__ import annotations

from pathlib import Path

import typer

from apex_translators import (
    SUPPORTED_FORMATS,
    parse_cda,
    parse_epcis,
    parse_hl7v2,
    parse_oagis,
    parse_padis,
    parse_x12,
)
from apex_translators.fixtures import (
    CDA_FIXTURES,
    EDI_X12_FIXTURES,
    EPCIS_FIXTURES,
    HL7V2_FIXTURES,
    OAGIS_FIXTURES,
    PADIS_FIXTURES,
)


translators_app = typer.Typer(
    name="translators",
    help="APEX message-format translators — EDI X12, HL7 v2, CDA, EPCIS, OAGIS, PADIS.",
    no_args_is_help=True,
)


_PARSERS = {
    "edi-x12": parse_x12,
    "hl7v2": parse_hl7v2,
    "cda": parse_cda,
    "epcis": parse_epcis,
    "oagis": parse_oagis,
    "padis": parse_padis,
}

_FIXTURE_BUNDLES = {
    "edi-x12": EDI_X12_FIXTURES,
    "hl7v2": HL7V2_FIXTURES,
    "cda": CDA_FIXTURES,
    "epcis": EPCIS_FIXTURES,
    "oagis": OAGIS_FIXTURES,
    "padis": PADIS_FIXTURES,
}


@translators_app.command("formats")
def formats_cmd() -> None:
    """List supported translator formats."""
    typer.echo("Supported formats:")
    for fmt in SUPPORTED_FORMATS:
        bundle = _FIXTURE_BUNDLES.get(fmt, {})
        typer.echo(f"  {fmt:12} ({len(bundle)} fixture(s))")


@translators_app.command("fixtures")
def fixtures_cmd(
    format: str = typer.Argument(..., help="Format key (edi-x12, hl7v2, cda, epcis, oagis, padis)."),
) -> None:
    """List fixture names for a format."""
    if format not in _FIXTURE_BUNDLES:
        typer.echo(f"Unknown format {format!r}", err=True)
        raise typer.Exit(code=1)
    for name in sorted(_FIXTURE_BUNDLES[format]):
        typer.echo(f"  {name}")


@translators_app.command("parse")
def parse_cmd(
    format: str = typer.Argument(..., help="Format key."),
    path: Path = typer.Argument(..., exists=True, help="Path to a message file."),
) -> None:
    """Parse a file and print summary."""
    if format not in _PARSERS:
        typer.echo(f"Unknown format {format!r}", err=True)
        raise typer.Exit(code=1)
    raw = path.read_text(encoding="utf-8")
    msg = _PARSERS[format](raw)
    typer.echo(f"format:         {msg.format}")
    typer.echo(f"message_type:   {msg.message_type}")
    if msg.sender:
        typer.echo(f"sender:         {msg.sender}")
    if msg.receiver:
        typer.echo(f"receiver:       {msg.receiver}")
    if msg.control_number:
        typer.echo(f"control_number: {msg.control_number}")
    if msg.version:
        typer.echo(f"version:        {msg.version}")
    if msg.sent_at:
        typer.echo(f"sent_at:        {msg.sent_at.isoformat()}")
    typer.echo(f"segments:       {len(msg.segments)}")
    by_name: dict[str, int] = {}
    for seg in msg.segments:
        by_name[seg.name] = by_name.get(seg.name, 0) + 1
    for name, count in sorted(by_name.items(), key=lambda kv: (-kv[1], kv[0])):
        typer.echo(f"  {name:20} {count}")
