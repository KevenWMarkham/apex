# apex-translators — Error Semantics Runbook

**Sprint 23 exit criterion:** "Each translator has parser + emitter +
round-trip conformance tests + **error-semantics runbook**."

This document catalogs every documented failure mode across the six
translators and the disposition guidance for ingestion pipelines.

## Common pattern

```python
from apex_translators import ParseError, EmitError, TranslatorError

try:
    msg = parse_x12(raw)
except ParseError as exc:
    # Quarantine + alert; never silently swallow
    ...
except TranslatorError as exc:
    # Catch-all at the ingestion boundary
    ...
```

Both `ParseError` and `EmitError` inherit from `TranslatorError`. Catch
the most-specific exception when you want differentiated handling;
catch `TranslatorError` at the ingestion-pipeline boundary as the
backstop.

## EDI X12 (`edi_x12`)

| Condition | Exception | Disposition |
|-----------|-----------|-------------|
| Empty payload | `ParseError("EDI X12 payload is empty")` | Quarantine; likely upstream truncation |
| Missing `ISA` segment | `ParseError("EDI X12 payload must start with 'ISA'…")` | Quarantine; payload is not X12 |
| ISA segment too short (< 106 chars) | `ParseError("ISA header too short — need ≥ 106 characters")` | Quarantine; corrupted ISA envelope |
| ISA elements < 16 | `ParseError("ISA segment too short: expected 16 elements, got N")` | Quarantine; non-standard envelope |
| Missing `ISA` after split | `ParseError("EDI X12 payload missing ISA envelope segment")` | Quarantine |
| Unmatched `ST`/`SE` | `ParseError("ST segment without matching SE")` / `ParseError("SE segment without matching ST")` | Quarantine; inspect for partial transmission |
| Empty `ParsedMessage` to emit | `EmitError("Cannot emit X12 from a message with no segments")` | Programmer error; report upstream |
| Unparseable ISA timestamp (ISA-09 / ISA-10) | non-fatal — `sent_at` left `None` | Log; continue |

**Tolerances:** parser accepts trailing CR/LF and Windows line-endings.
Delimiters auto-detected from the ISA segment; pass an explicit
`EDIX12Delimiters` to override.

## HL7 v2 (`hl7v2`)

| Condition | Exception | Disposition |
|-----------|-----------|-------------|
| Empty / non-MSH-prefixed | `ParseError("HL7 v2 message must begin with MSH segment")` | Quarantine |
| MSH < 8 chars | `ParseError("MSH segment is too short")` | Quarantine |
| MSH-2 (encoding chars) < 4 chars | `ParseError("MSH-2 (encoding characters) is too short")` | Quarantine |
| Missing MSH after split | `ParseError("HL7 v2 message missing MSH after split")` | Quarantine; defensive |
| Malformed DTM in MSH-7 | non-fatal — `sent_at` left `None` | Log; continue |
| Empty `ParsedMessage` to emit | `EmitError("Cannot emit HL7 v2 from a message with no segments")` | Programmer error |
| MSH segment with no elements on emit | `EmitError("MSH segment has no elements")` | Programmer error |

**Tolerances:** segment delimiter is `\r` per the HL7 spec; parser
tolerates `\n` and `\r\n` for editor-mangled fixtures. MLLP framing is
optional — use `strip_mllp()` before `parse_hl7v2()` for wire-side
ingestion; `wrap_mllp()` produces the framed bytes for emission.

## HL7 CDA (`cda`)

| Condition | Exception | Disposition |
|-----------|-----------|-------------|
| Empty payload | `ParseError("CDA payload is empty")` | Quarantine |
| Payload > 10 MB | `ParseError("CDA payload exceeds 10485760 bytes — refusing to parse")` | Quarantine; defensive XML-bomb guard |
| XML parse failure | `ParseError("CDA XML parse error: …")` | Quarantine; log offending offset |
| Wrong root element | `ParseError("CDA root element should be ClinicalDocument…")` | Quarantine; not a CDA document |
| `structuredBody` missing | non-fatal — empty `segments` list | Log; CDA header-only is valid |

**One-way only.** No emitter. The 10 MB limit is defensive; raise via
custom parser config if a tenant needs more.

## EPCIS 2.0 (`epcis`)

| Condition | Exception | Disposition |
|-----------|-----------|-------------|
| Empty payload | `ParseError("EPCIS payload is empty")` | Quarantine |
| Non-JSON / non-XML start | `ParseError("EPCIS payload first non-whitespace character must be '{', '[', or '<'")` | Quarantine; payload is neither dialect |
| JSON parse failure | `ParseError("EPCIS JSON parse error: …")` | Quarantine |
| JSON root is not an object | `ParseError("EPCIS JSON root must be an object")` | Quarantine |
| `eventList` is not a list | `ParseError("EPCIS eventList must be an array")` | Quarantine |
| XML parse failure | `ParseError("EPCIS XML parse error: …")` | Quarantine |
| Format mismatch on emit | `EmitError("EPCIS emitter requires format='epcis', got …")` | Programmer error |

**Tolerances:** missing `creationDate` is non-fatal (empty string in
metadata). Missing `epcisBody` / `eventList` produces an empty segment
list.

## OAGIS BOD (`oagis`)

| Condition | Exception | Disposition |
|-----------|-----------|-------------|
| Empty payload | `ParseError("OAGIS payload is empty")` | Quarantine |
| XML parse failure | `ParseError("OAGIS XML parse error: …")` | Quarantine |
| Root tag with no recognized verb | `ParseError("OAGIS BOD root … does not start with a recognized OAGIS verb")` | Quarantine; non-OAGIS document |
| Missing `DataArea` | `ParseError("OAGIS BOD … missing DataArea")` | Quarantine; non-conformant BOD |
| Missing `message_type` on emit | `EmitError("OAGIS message_type is required …")` | Programmer error |
| Format mismatch on emit | `EmitError("OAGIS emitter requires format='oagis' …")` | Programmer error |

**Tolerances:** missing `ApplicationArea` is non-fatal (sender / control
number left blank). Verbs not in the canonical 10 will fail root-tag
recognition; extend `OAGIS_VERBS` if needed.

## IATA PADIS (`padis`)

| Condition | Exception | Disposition |
|-----------|-----------|-------------|
| Empty payload | `ParseError("PADIS payload is empty")` | Quarantine |
| All-blank lines | `ParseError("PADIS payload has no non-blank lines")` | Quarantine |
| Header not in supported set | `ParseError("PADIS message header … not in supported set …")` | Quarantine; unsupported message type |

**Tolerances:** flight-key second line is optional — when missing,
`metadata['flight']` is absent. Lines starting with `.` are attached as
continuations to the preceding `PAX` segment, or surfaced as
`SUPPLEMENTARY` segments when there's no preceding PAX. Lines that
match neither the flight-key nor the traveler-record regex are
surfaced as `UNSTRUCTURED` segments.

## At the ingestion boundary

```python
from apex_translators import (
    TranslatorError, ParseError,
    parse_x12, parse_hl7v2, parse_cda, parse_epcis, parse_oagis, parse_padis,
)

PARSERS = {
    "edi-x12": parse_x12,
    "hl7v2":   parse_hl7v2,
    "cda":     parse_cda,
    "epcis":   parse_epcis,
    "oagis":   parse_oagis,
    "padis":   parse_padis,
}

def ingest(raw: str, expected_format: str) -> "ParsedMessage | None":
    try:
        return PARSERS[expected_format](raw)
    except ParseError as exc:
        log.warning(
            "translator.parse_error",
            format=expected_format, error=str(exc),
        )
        quarantine(raw, exc)
        return None
    except TranslatorError as exc:
        log.error("translator.unknown_error", format=expected_format, error=str(exc))
        quarantine(raw, exc)
        return None
```
