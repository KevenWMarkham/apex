# apex-tokenizer

APEX's deterministic + reversible token service — the runtime that ships from Sprint 5 to replace every `_tokenize_placeholder_*` function in the Practice packages.

## Design

- **Deterministic.** `tokenize(value, classification, tenant_id)` with the same inputs returns the same token — joins across Silver rows work naturally.
- **Reversible via vault.** Tokens are opaque strings (`tok_<base64url-16>`); cleartext is recovered by looking the token up in a vault. **Not** by reversing the hash.
- **Classification-scoped.** Two different classifications applied to the same value produce different tokens — so a PHI-view and a PII-view of the same string never collide.
- **Backend-pluggable.** `VaultBackend` is a protocol. `InMemoryVaultBackend` for dev + tests; `DeltaVaultBackend` for Fabric.

## Public surface

```python
from apex_tokenizer import (
    TokenService,          # wrap a backend + call tokenize / detokenize
    VaultBackend,           # protocol
    InMemoryVaultBackend,   # default for dev + tests
    VaultEntry,             # row structure
    tokenize,               # module-level convenience
    detokenize,
    tokenize_classified_fields,  # walk a Pydantic model → tokenise classified fields
    set_default_service,
    vault_ddl,              # Delta DDL for the vault table
)
```

## Authz gating

Sprint 5 ships **unconditional detokenise**. The visibility-lattice check (per `APEX_Design.md` §8.3) gates detokenise per requester identity — that wiring lands in Sprint 10 alongside `apex-identity`.

## Secret handling

- Dev / tests: a fixed placeholder secret is used. **Do not** ship this to production.
- Production: a tenant-scoped HMAC secret is expected via `APEX_TOKENIZER_SECRET` env var or Key Vault binding (Sprint 14).
