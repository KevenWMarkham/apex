"""EPCIS 2.0 JSON-LD emitter — Sprint 23 Task 23.4."""

from __future__ import annotations

import json
from dataclasses import dataclass

from apex_translators.base import EmitError, ParsedMessage


@dataclass
class EPCISEmitter:
    """Render a :class:`ParsedMessage` back to EPCIS 2.0 JSON-LD."""

    indent: int | None = None

    def emit(self, message: ParsedMessage) -> str:
        if message.format != "epcis":
            raise EmitError(
                f"EPCIS emitter requires format='epcis', got {message.format!r}"
            )
        events = []
        for seg in message.segments:
            event = dict(seg.data)
            event.setdefault("type", seg.name)
            events.append(event)

        doc = {
            "@context": message.metadata.get(
                "context", "https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld"
            ),
            "type": message.message_type or "EPCISDocument",
            "schemaVersion": message.version or "2.0",
            "creationDate": message.metadata.get("creation_date", ""),
            "epcisBody": {"eventList": events},
        }
        return json.dumps(doc, indent=self.indent, ensure_ascii=False)


def emit_epcis_json(message: ParsedMessage, indent: int | None = None) -> str:
    """Convenience: emit an EPCIS 2.0 JSON-LD document."""
    return EPCISEmitter(indent=indent).emit(message)
