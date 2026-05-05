# apex-translators

**Sprint 23 — Message-format translators.** Bidirectional parsers and emitters
for enterprise message formats so SORs speaking EDI X12, HL7 v2, EPCIS 2.0,
and OAGIS BOD — plus one-way ingest from HL7 CDA and IATA PADIS — integrate
to APEX canonical Silver without bespoke per-engagement parsing.

## Coverage

| Format | Direction | Submodule | Task | Coverage |
|--------|-----------|-----------|------|----------|
| EDI X12 (RC: 850, 856, 810, 820 + HLS: 837, 835, 270, 271) | ↔ | `edi_x12` | 23.1 | 8 transactions, ISA/GS/ST envelope auto-detect of delimiters |
| HL7 v2.x (MSH, PID, PV1, OBX, OBR, ORC, RXE, AL1) | ↔ | `hl7v2` | 23.2 | v2.5.1 + v2.7, MLLP framing helpers (`wrap_mllp` / `strip_mllp`) |
| HL7 CDA / C-CDA | → | `cda` | 23.3 | 4 named C-CDA sections (Allergies, Medications, Problems, Results) + 7 supplementary template OIDs; XML-bomb safe (10 MB limit) |
| EPCIS 2.0 (Object/Aggregation/Transaction/Transformation/Association events) | ↔ | `epcis` | 23.4 | JSON-LD + XML parse, JSON-LD emit |
| OAGIS BOD | ↔ | `oagis` | 23.5 | 10 verbs (Get/Show/Process/Acknowledge/Sync/Confirm/Notify/Cancel/Update/Change), ApplicationArea + DataArea envelope |
| IATA PADIS | → | `padis` | 23.6 | 5 message types (PNL/ADL/PRL/PFS/PSM), flight-key + traveler record extraction |

## API

```python
from apex_translators import (
    parse_x12, emit_x12,
    parse_hl7v2, emit_hl7v2, wrap_mllp, strip_mllp,
    parse_cda,
    parse_epcis, emit_epcis_json,
    parse_oagis, emit_oagis,
    parse_padis,
    ParsedMessage, ParseError, EmitError,
)

msg = parse_x12(raw_x12_text)
print(msg.message_type)          # "850"
print(msg.first("BEG").elements) # ["00", "SA", "PO12345", "", "20250630"]

re_rendered = emit_x12(msg)
assert msg.segments == parse_x12(re_rendered).segments
```

## Round-trip semantics

For bidirectional formats (X12, HL7 v2, EPCIS, OAGIS): `emit(parse(x))`
re-parses to a structurally identical `ParsedMessage`. Bytewise identity is
NOT guaranteed (delimiter choice, optional whitespace, namespace prefixes
all may normalize) but segment names, field counts, and field values do.

For one-way formats (CDA, PADIS): structural extraction only — `emit()` is
not exposed.

## Error semantics

See `ERROR_SEMANTICS.md` for the runbook. Quick reference:

- `ParseError` raised on: missing envelope, unsupported message type,
  malformed delimiters, XML parse failure, empty payload, non-recognized
  PADIS/OAGIS root tag.
- `EmitError` raised on: empty `ParsedMessage`, format mismatch (e.g.,
  passing a `format='hl7v2'` message to `emit_x12()`), missing required
  metadata.

Both inherit from `TranslatorError` for catch-all handling at the
ingestion-pipeline boundary.

## Cross-references

- Sprint 9 — `edi-mcp` package (legacy stub parsers, superseded by this package)
- Sprint 22 Task 22.6 — ISO 8000 quality dimensions (translators set
  `provenance` and `conformance` scores when emitting `ParsedMessage` →
  `CanonicalEnvelope`)
- Sprint 21 — per-standard packages (FHIR, CDISC, etc.) — translators bridge
  legacy formats to those canonical schemas
- `Industry-Standards-Incorporation-Plan.md` §4 Pattern D
