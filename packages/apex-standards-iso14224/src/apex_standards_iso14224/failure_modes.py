"""ISO 14224 failure modes and mechanisms (controlled vocabulary)."""

from __future__ import annotations

from enum import StrEnum


class Iso14224FailureMode(StrEnum):
    """High-level failure modes per ISO 14224 Table B.1."""

    LEAKAGE = "leakage"
    EXTERNAL_LEAKAGE = "external_leakage"
    INTERNAL_LEAKAGE = "internal_leakage"
    VIBRATION = "vibration"
    OVERHEATING = "overheating"
    STRUCTURAL_DEFICIENCY = "structural_deficiency"
    ELECTRICAL_FAULT = "electrical_fault"
    CONTROL_FAULT = "control_fault"
    INSTRUMENT_FAULT = "instrument_fault"
    FAIL_TO_START = "fail_to_start"
    FAIL_TO_STOP = "fail_to_stop"
    SPURIOUS_STOP = "spurious_stop"
    EXTERNAL_INFLUENCE = "external_influence"
    PARAMETER_DEVIATION = "parameter_deviation"
    OTHER = "other"
    UNKNOWN = "unknown"


class Iso14224FailureMechanism(StrEnum):
    """Root-cause mechanisms per ISO 14224 Table B.2."""

    CORROSION = "corrosion"
    EROSION_WEAR = "erosion_wear"
    FATIGUE = "fatigue"
    OVERLOAD = "overload"
    CONTAMINATION = "contamination"
    IMPROPER_ASSEMBLY = "improper_assembly"
    MATERIAL_DEFECT = "material_defect"
    DESIGN_DEFECT = "design_defect"
    MANUFACTURING_DEFECT = "manufacturing_defect"
    MISOPERATION = "misoperation"
    AGING = "aging"
    LOOSENING = "loosening"
    NOT_IDENTIFIED = "not_identified"
    OTHER = "other"
