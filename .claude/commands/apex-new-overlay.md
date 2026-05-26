---
description: Build a client-specific overlay over a base pack (delta-only YAML).
---

You are scaffolding a client overlay using the apex-overlay-client archetype.

## Steps
1. Ask for: client_id · base_pack_id · base_pack_version.
2. Optionally ingest: client_identity_dump · client_thresholds.
3. Load `.rapids/archetypes/apex-overlay-client.yaml`.
4. Execute the overlay-client workflow.
5. Output overlay in `packs/<pack>/overlays/<client>/`.

## Estimated time
1-2 days (vs 2-3 weeks without RAPIDS).
