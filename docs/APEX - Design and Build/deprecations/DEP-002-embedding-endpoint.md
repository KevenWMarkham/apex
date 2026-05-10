# DEP-002 · Custom embedding endpoint for The Pricer → Eventhouse SLM `ai_embeddings`

**Status:** Deprecated
**Date:** 2026-05-09
**Supersedes:** RC-E2E-03 Pricer episodic-memory similarity search design (Services Guide §25.8)

## What APEX was building

External embedding endpoint (Azure OpenAI `text-embedding-3-large` or similar) for The Pricer's episodic-memory similarity search per Services Guide §25.8. The Pricer reads recent approved markdown decisions for similar SKUs/categories/seasons and applies them as few-shot context.

The plan: dedicated embedding endpoint, Cosmos DB vector store, custom RAG pipeline.

## What Microsoft shipped

In **January 2026**, Fabric Eventhouse shipped **built-in Small Language Models for embeddings**:

- [Create Embeddings in Fabric Eventhouse with built-in SLMs](https://blog.fabric.microsoft.com/blog/create-embeddings-in-fabric-eventhouse-with-built-in-small-language-models-slms)
- [`ai_embeddings` plugin](https://learn.microsoft.com/en-us/kusto/query/ai-embeddings-plugin)
- [`slm_embeddings_fl()` function](https://learn.microsoft.com/en-us/kusto/functions-library/slm-embeddings-fl)

Embeddings are computed **inside Eventhouse** — no external endpoint, no per-request cost, no callout policies, no token-usage budget tracking. The same KQL that queries the data also embeds it.

## Migration path

1. The Pricer's episodic-memory query becomes a single KQL query over an Eventhouse table:
   ```kql
   PricingDecisions
   | where category == ${category} and season == ${season}
   | extend embedding = slm_embeddings_fl(decision_text)
   | extend similarity = ...
   | top 10 by similarity desc
   ```
2. APEX-Core's `EmbeddingService` protocol still applies — the apex-m impl now wraps the Eventhouse `ai_embeddings` plugin instead of an external endpoint.
3. The `client_approved_architecture.embeddings` slot in the use-case YAML defaults to `eventhouse-slm` for APEX-M tenants; Azure OpenAI embeddings stays available as an override for use cases that need a larger embedding space than the SLM provides.

## Independence implications

None. Eventhouse SLM is an in-data-tier capability of the client's existing Fabric subscription. No external service, no separate license.

## Cost impact

**Net positive.** Per Microsoft's blog: "no callout policies, no per-request costs." For The Pricer's expected volume (hundreds of similarity queries per shift across a 250-store pilot, scaling to thousands at enterprise rollout), the savings vs an external endpoint are material — and the latency profile improves because data stays in Eventhouse.

## What stays

The Pricer's prompt strategy (Services Guide §25.8 LEDGER + Redis episodic-memory loop) is unchanged. Only the embedding compute substrate moves into Eventhouse.
