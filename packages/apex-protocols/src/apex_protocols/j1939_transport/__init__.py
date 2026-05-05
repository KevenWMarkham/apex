"""SAE J1939 transport wrapper — Sprint 25 Task 25.3 (BL.P.168).

Wraps the CAN-bus capture path so APEX agents see normalized
SPN-addressed values rather than raw 8-byte CAN frames. Integrates with
the :mod:`apex_standards.j1939` SPN/PGN registry from Sprint 21 Task 21.8.

Submodules:

- :mod:`apex_protocols.j1939_transport.normalizer` — multi-ECU frame
  decoder + SPN-addressed value emission
- :mod:`apex_protocols.j1939_transport.throttle` — high-frequency-signal
  throttling + downsampling
"""

from apex_protocols.j1939_transport.normalizer import (
    CANFrame,
    DecodedSignal,
    J1939Normalizer,
    decode_frame,
)
from apex_protocols.j1939_transport.throttle import SignalThrottle

__all__ = [
    "CANFrame",
    "DecodedSignal",
    "J1939Normalizer",
    "SignalThrottle",
    "decode_frame",
]
