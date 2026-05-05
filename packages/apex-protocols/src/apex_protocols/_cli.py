"""apex-protocols Typer subcommands."""

from __future__ import annotations

from pathlib import Path

import typer

from apex_protocols import (
    SUPPORTED_PROTOCOLS,
    parse_nodeset,
    parse_scd,
)
from apex_protocols.datasets import (
    IEC61850_SCD_XML,
    J1939_FRAME_CAPTURE,
    OPCUA_NODESET_XML,
)
from apex_protocols.j1939_transport.normalizer import SPN_LAYOUTS


protocols_app = typer.Typer(
    name="protocols",
    help="APEX OT protocol adapters — OPC UA, IEC 61850, SAE J1939.",
    no_args_is_help=True,
)


@protocols_app.command("list")
def list_cmd() -> None:
    """List supported OT protocols + smoke-test dataset sizes."""
    typer.echo("Supported OT protocols:")
    typer.echo(f"  opcua       NodeSet entries: {len(parse_nodeset(OPCUA_NODESET_XML))}")
    typer.echo(f"  iec61850    IEDs in smoke SCD: {len(parse_scd(IEC61850_SCD_XML).ieds)}")
    typer.echo(f"  j1939       PGNs decoded: {len(SPN_LAYOUTS)}, fixture frames: {len(J1939_FRAME_CAPTURE)}")
    assert set(SUPPORTED_PROTOCOLS)  # silence unused import in some lint configs


@protocols_app.command("nodeset")
def nodeset_cmd(
    path: Path = typer.Argument(..., exists=True, help="Path to a NodeSet2 XML."),
) -> None:
    """Parse an OPC UA NodeSet2 XML and list its variables."""
    raw = path.read_text(encoding="utf-8")
    entries = parse_nodeset(raw)
    typer.echo(f"Parsed {len(entries)} entries from {path}")
    for e in entries:
        typer.echo(f"  [{e.node_class:11}] {e.node_id:50} {e.display_name}")


@protocols_app.command("scd")
def scd_cmd(
    path: Path = typer.Argument(..., exists=True, help="Path to an IEC 61850 SCD XML."),
) -> None:
    """Parse an IEC 61850 SCD and list IEDs / Logical Devices / control blocks."""
    raw = path.read_text(encoding="utf-8")
    doc = parse_scd(raw)
    for ied in doc.ieds:
        typer.echo(f"IED {ied.name} ({ied.manufacturer})")
        for ld in ied.logical_devices:
            typer.echo(f"  LD {ld.inst} — {len(ld.logical_nodes)} LNs, {len(ld.goose_blocks)} GOOSE, {len(ld.sv_blocks)} SV")


@protocols_app.command("runbooks")
def runbooks_cmd() -> None:
    """List shipped per-protocol runbooks."""
    from apex_protocols.base import SUPPORTED_PROTOCOLS

    runbooks_dir = Path(__file__).resolve().parent / "runbooks"
    for proto in SUPPORTED_PROTOCOLS:
        suffix = "" if proto != "j1939" else ""
        candidates = list(runbooks_dir.glob(f"{proto}*"))
        for c in candidates:
            typer.echo(f"  {proto:12} {c.relative_to(runbooks_dir.parent.parent)}")
