# apex-standards-j1939 — Third-Party Content Attribution

## SAE J1939

- **Authority:** SAE International
- **URL:** https://www.sae.org/standards/development/standards-committee-content/sae-j1939
- **License:** Commercial / membership-restricted
- **Redistribution:** **Not permitted.** APEX ships a curated seed of widely-referenced SPNs/PGNs (public-knowledge subset) plus empty hooks for tenant-supplied catalogs.
- **Compliance:** Tenants using APEX with full J1939 coverage must hold their own SAE J1939 licence.

## What this package contains

- Pydantic / dataclass shapes for J1939 concepts (APEX IP).
- A seed registry of ~20 well-known SPNs / PGNs chosen for reference-deployment coverage.
- `load_spn_catalog()` / `load_pgn_catalog()` hooks for tenant-supplied full catalogs.

## What this package does **not** contain

- The full SAE J1939 SPN / PGN catalog.
- Any SAE-copyrighted prose, decoder implementations, or protocol specifications beyond what is publicly documented.
