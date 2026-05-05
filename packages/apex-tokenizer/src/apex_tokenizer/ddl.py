"""Vault Delta table DDL."""

from __future__ import annotations

VAULT_TABLE = "silver_vault_tokens"


def vault_ddl(database: str | None = None) -> str:
    """Return the ``CREATE TABLE`` DDL for the tokeniser vault.

    PIM-gated: direct read access is restricted to the detokeniser service
    principal + audit-review identities. Applications read via MCP only.
    """
    qualified = f"{database}.{VAULT_TABLE}" if database else VAULT_TABLE
    return f"""CREATE TABLE {qualified} (
  token                    STRING NOT NULL,
  cleartext                STRING NOT NULL,
  classification           STRING NOT NULL,
  tenant_id                STRING NOT NULL,
  source_system            STRING,
  created_ts               TIMESTAMP NOT NULL,
  created_by               STRING NOT NULL
)
USING DELTA
PARTITIONED BY (tenant_id, classification)
TBLPROPERTIES (
  'delta.enableChangeDataFeed' = 'true',
  'apex.medallion.layer' = 'silver_vault',
  'apex.access_policy' = 'pim_gated_detokenise_only'
);"""
