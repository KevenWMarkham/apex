# apex-standards-opentravel — Third-Party Content Attribution

This package mirrors structural definitions from OpenTravel Alliance (OTA).

## OpenTravel Alliance (OTA)

- **Authority:** OpenTravel Alliance
- **URL:** https://opentravel.org/
- **Pinned version:** 2025A
- **License:** Open — OpenTravel publishes message specifications and XSDs under an open licence permitting redistribution with attribution
- **Pattern:** B (data model mirror) per `Industry-Standards-Incorporation-Plan.md` §3
- **Redistribution:** Structural definitions may be freely redistributed with attribution.

## What this package ships

- Pydantic models named after OpenTravel message types
  (`OTA_AirAvailRQ/RS`, `OTA_HotelAvailRQ/RS`, `OTA_HotelResRQ/RS`,
  `OTA_ReadRQ`, etc.) capturing the request/response data shape
- OpenTravel XML namespace constants
- IATA/ICAO airline-code, airport-code, and city-code validators (cross-link
  to IATA NDC where applicable)

## Cross-references

- IATA NDC (apex-schemas-common.standards) — modern airline-distribution complement to OTA
- IATA SSIM, A-CDM (referenced in canonical `OpsML-TH` schema)

## Restricted content guardrail

OpenTravel content is open and may be redistributed; nonetheless this package
ships **mirror models, not raw OpenTravel XSDs**. Tenants requiring direct
schema validation should obtain XSDs from openttravel.org and run XML-schema
validation alongside APEX Pydantic validation.
