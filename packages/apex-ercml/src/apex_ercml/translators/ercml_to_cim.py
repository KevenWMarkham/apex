"""ERCML → CIM translators (Pattern D inverse)."""

from __future__ import annotations

from apex_standards_cim import CimAsset, CimMeter, CimMeterKind

from apex_ercml.entities import Asset, Meter


def meter_to_cim(meter: Meter) -> CimMeter:
    """Translate an ERCML Meter back into a CIM Meter."""
    return CimMeter(
        m_rid=meter.cim_mrid,
        serial_number=meter.serial_number,
        kind=CimMeterKind(meter.kind.value),
        customer_mrid=meter.customer_key,
        location_mrid=meter.location_key,
        install_date=meter.install_date,
        remove_date=meter.remove_date,
    )


def asset_to_cim(asset: Asset) -> CimAsset:
    """Translate an ERCML Asset back into a CIM Asset."""
    return CimAsset(
        m_rid=asset.cim_mrid,
        name=asset.name,
        asset_type=asset.asset_type,
        location_mrid=asset.location_key,
        in_service_date=asset.in_service_date,
        lifecycle_state=asset.lifecycle_state.value,
    )
