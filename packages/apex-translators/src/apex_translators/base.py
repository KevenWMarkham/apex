"""Common base types for APEX message-format translators — Sprint 23.

Each translator submodule (``edi_x12``, ``hl7v2``, ``cda``, ``epcis``,
``oagis``, ``padis``) defines:

- A :class:`Parser` implementation that consumes raw bytes/text and emits
  :class:`ParsedMessage` instances
- An :class:`Emitter` implementation (where the format is bidirectional)
  that takes a :class:`ParsedMessage` and renders to bytes/text
- A round-trip conformance suite that asserts ``encode(parse(x)) == x``
  modulo whitespace / control-char normalization

The :class:`ParsedMessage` is the format-neutral intermediate representation:
a typed envelope (sender / receiver / timestamps / control numbers) plus a
list of :class:`Segment` rows whose interpretation depends on the format.
The shape is **not** the canonical Silver schema — Bronze→Silver loaders
are responsible for the final canonical mapping. This intermediate exists
purely to give each translator a uniform API surface.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Protocol


@dataclass
class Segment:
    """One named segment / element of a parsed message.

    For EDI X12: name is the segment id (ISA, GS, ST, BEG, ...) and
    ``elements`` holds the *-delimited values.

    For HL7 v2: name is the segment id (MSH, PID, ...) and ``elements``
    holds the |-delimited fields (with sub-component handling
    flattened into ``raw`` for now).

    For EPCIS / OAGIS: name is the event-type / noun, ``elements`` is
    empty, and ``data`` holds the deserialized JSON / XML structure.
    """

    name: str
    elements: list[str] = field(default_factory=list)
    """Positional elements/fields (EDI / HL7v2 use this; XML/JSON formats use ``data``)."""

    data: dict[str, Any] = field(default_factory=dict)
    """Deserialized structured payload (XML / JSON formats use this)."""

    raw: str = ""
    """Original raw segment text — useful for debugging + emit fidelity."""


@dataclass
class ParsedMessage:
    """Format-neutral parsed-message envelope.

    Translator output. Bronze→Silver loaders consume this, map fields onto
    canonical schemas (SCML, PatientML, ClaimML, etc.), and emit the
    canonical Silver row with its :class:`apex_core.envelope.CanonicalEnvelope`.
    """

    format: str
    """Translator format key, e.g., ``"edi-x12"``, ``"hl7v2"``, ``"cda"``,
    ``"epcis"``, ``"oagis"``, ``"padis"``."""

    message_type: str = ""
    """Specific message id within the format, e.g., ``"850"``, ``"ADT^A04"``."""

    sender: str = ""
    receiver: str = ""
    sent_at: datetime | None = None
    control_number: str = ""
    """ICN / control number for the envelope (when format defines one)."""

    version: str = ""
    """Format/transaction version, e.g., ``"00501"`` (EDI release 5010)."""

    segments: list[Segment] = field(default_factory=list)
    raw: str = ""
    """Original raw input — kept for debug + emit fidelity. Set by parsers."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Extra format-specific metadata (delimiters, character sets, etc.)."""

    def find(self, name: str) -> list[Segment]:
        """Return every segment with ``segment.name == name``."""
        return [s for s in self.segments if s.name == name]

    def first(self, name: str) -> Segment | None:
        """Return the first segment with ``segment.name == name`` or None."""
        for s in self.segments:
            if s.name == name:
                return s
        return None


class Parser(Protocol):
    """Format-specific parser protocol."""

    def parse(self, raw: str) -> ParsedMessage:
        ...


class Emitter(Protocol):
    """Format-specific emitter protocol."""

    def emit(self, message: ParsedMessage) -> str:
        ...


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


class TranslatorError(Exception):
    """Base for translator parse / emit failures."""


class ParseError(TranslatorError):
    """Raised when a parser cannot interpret its input."""


class EmitError(TranslatorError):
    """Raised when an emitter cannot serialize a message."""


# ---------------------------------------------------------------------------
# Format keys
# ---------------------------------------------------------------------------


FORMAT_EDI_X12 = "edi-x12"
FORMAT_HL7V2 = "hl7v2"
FORMAT_CDA = "cda"
FORMAT_EPCIS = "epcis"
FORMAT_OAGIS = "oagis"
FORMAT_PADIS = "padis"


SUPPORTED_FORMATS: tuple[str, ...] = (
    FORMAT_EDI_X12,
    FORMAT_HL7V2,
    FORMAT_CDA,
    FORMAT_EPCIS,
    FORMAT_OAGIS,
    FORMAT_PADIS,
)
