"""ISO 14224 equipment taxonomy (top-level classes + common subclasses)."""

from __future__ import annotations

from enum import StrEnum


class Iso14224EquipmentClass(StrEnum):
    """Top-level equipment classes per ISO 14224 Annex A."""

    PUMP = "pump"
    COMPRESSOR = "compressor"
    HEAT_EXCHANGER = "heat_exchanger"
    VESSEL = "vessel"
    VALVE = "valve"
    ELECTRIC_MOTOR = "electric_motor"
    GENERATOR = "generator"
    TURBINE = "turbine"
    GEARBOX = "gearbox"
    PIPING = "piping"
    INSTRUMENTATION = "instrumentation"
    CONTROL_SYSTEM = "control_system"
    SAFETY_SYSTEM = "safety_system"
    BATTERY = "battery"
    TRANSFORMER = "transformer"


class Iso14224EquipmentSubclass(StrEnum):
    """Common subclasses useful to reference deployments.

    Non-exhaustive; tenants extend per Annex A chapter relevant to their asset.
    """

    # Pumps
    CENTRIFUGAL_PUMP = "centrifugal_pump"
    POSITIVE_DISPLACEMENT_PUMP = "positive_displacement_pump"
    # Compressors
    CENTRIFUGAL_COMPRESSOR = "centrifugal_compressor"
    RECIPROCATING_COMPRESSOR = "reciprocating_compressor"
    # Valves
    CONTROL_VALVE = "control_valve"
    SAFETY_VALVE = "safety_valve"
    SHUT_OFF_VALVE = "shut_off_valve"
    # Motors / generators
    INDUCTION_MOTOR = "induction_motor"
    SYNCHRONOUS_MOTOR = "synchronous_motor"
    # Turbines
    STEAM_TURBINE = "steam_turbine"
    GAS_TURBINE = "gas_turbine"
    WIND_TURBINE = "wind_turbine"
    # Heat exchangers
    SHELL_AND_TUBE = "shell_and_tube"
    PLATE_AND_FRAME = "plate_and_frame"
    # Instrumentation
    TEMPERATURE_SENSOR = "temperature_sensor"
    PRESSURE_SENSOR = "pressure_sensor"
    FLOW_METER = "flow_meter"
    VIBRATION_SENSOR = "vibration_sensor"
