# apex-standards-j1939

**Pattern-A + Pattern-B** binding for SAE J1939 — heavy-duty vehicle and commercial-equipment serial network.

**Shared by:** `apex-axlecml`, `apex-iceml`.

## Scope

- `J1939SPN` — Signal Parameter Number metadata (spn, name, units, resolution, offset, range, length_bits)
- `J1939PGN` — Parameter Group Number metadata
- `CanFrame` — decoded CAN 2.0B extended frame shape (used by the OPC UA / telematics adapters in Sprint 15)
- **Seed registry** — ~20 most-referenced SPNs and PGNs used in APEX reference deployments

## Licence

SAE J1939 full SPN / PGN catalogs are **commercially licensed**. APEX ships:

- Data structures and decoder skeletons (APEX IP)
- A small curated **seed** of widely-referenced SPNs / PGNs (public-knowledge subset)

Tenants needing the full catalog supply it themselves via `load_spn_catalog(path)` and `load_pgn_catalog(path)` hooks.

See `LICENSE-ATTRIBUTION.md`.
