"""IATA PADIS parser — Sprint 23 Task 23.6 (BL.P.160).

PADIS = Passenger and Airport Data Interchange Standards. Teletype-style
record-oriented format. We support the named subset:

- PNL  Passenger Name List
- ADL  Add/Delete List
- PRL  Passenger Reconfirmation List

One-way (PADIS → canonical) per Sprint 23 spec.
"""

from apex_translators.padis.parser import (
    PADIS_MESSAGE_TYPES,
    PADISParser,
    parse_padis,
)

__all__ = [
    "PADIS_MESSAGE_TYPES",
    "PADISParser",
    "parse_padis",
]
