# 09 — Portability & Open-Home Commitments

> _Draft — the design choices that make "your data, our network" credible. Open-by-construction is **not** a concession; it is the moat. Closed gardens are how Big Tech wins; open standards are how the Telco wins._

## 1. The portability bargain

The pack makes three public commitments to the household. Each is **enforced at the protocol layer**, not promised in a marketing page:

| Commitment | What it means in practice | Enforcement mechanism |
|---|---|---|
| **Your data, your vault** | The household's data lives in an object store the customer owns. The Telco operates the runtime; it never holds the encryption key in clear. | Customer-held KMS key. Vault bucket-policy denies the Telco's runtime read access except via signed, ephemeral, per-agent-run tokens that the customer can revoke. |
| **One-click export** | The customer can export the entire vault — telemetry, entity history, agent runs, embeddings, actions — to any S3-compatible bucket they nominate. | Standard export format (Parquet for tabular, JSONL for events, Markdown for agent transcripts). See §3. |
| **Switch the orchestrator, keep the data** | The customer can disconnect the Telco's orchestrator and connect a 3rd-party orchestrator while retaining every byte of history and every consent grant. | Open MCP interface contract — see §4. |

These commitments are publishable in plain language and verifiable by the customer. They are the foundation of the trust-asymmetry argument in [`08-consumer-business-case.md`](./08-consumer-business-case.md).

## 2. The Matter-first device strategy

Closed device ecosystems (HomeKit-only, Google Home-only, single-OEM clouds) are structurally disqualified as anchor sources. The pack commits to **Matter / Thread as the lingua franca** with three consequences:

1. **Device coverage scales linearly with the Matter device library** — there is no "we waited for the OEM to sign a deal" bottleneck. CSA membership is the gate.
2. **The customer keeps the device when they switch orchestrator** — a Matter-bound Hue bulb is still a Matter-bound Hue bulb if the orchestration layer changes. No platform-specific re-pairing.
3. **OEMs see the Telco platform as a multiplier, not a competitor** — every OEM gets distribution; no OEM gets locked out. The "Works with [Telco] Home" badge is additive to the OEM's existing channel mix, not an alternative to it.

Where Matter does not yet cover a device class (CGMs, certain vehicle telematics, certain medical devices), the pack uses **vendor-native APIs with a forward-commitment** — the moment Matter publishes that device class, the integration migrates.

## 3. The vault export format

The export is **lossless** by construction. A receiving system can rebuild the household's full agentic state from the export alone, without any Telco-specific tooling.

```
vault-export-<household_id>-<timestamp>/
├── manifest.json                              # schema version, contents, integrity hashes
├── consent/                                   # per-grant JSON, including history of revokes
├── entities/
│   ├── household.parquet
│   ├── person.parquet
│   ├── device.parquet
│   └── ...
├── events/
│   ├── telemetry-YYYY-MM.parquet              # one file per month
│   ├── energy-readings-YYYY-MM.parquet
│   ├── inventory-readings-YYYY-MM.parquet
│   └── ...
├── agent-runs/
│   ├── run-<uuid>.jsonl                       # one file per agent run, ndjson
│   └── ...
├── embeddings/
│   └── context-embeddings.parquet             # pgvector dump
└── audit/
    └── view-definition-shas.jsonl             # which Gold view produced each result
```

Two concrete consequences:

- A customer leaving the Telco can take this archive to a competitor or a self-hosted Home Assistant + custom orchestrator and rehydrate it. Their agent history travels with them.
- A regulator auditing the household's claim ("the Telco's agent did X without consent") can replay the export against the audit log without needing Telco-side access.

## 4. The open MCP interface

The orchestrator and sub-agents communicate with downstream tools (vendor APIs, vault, partner integrations) over **MCP**, the open Anthropic protocol. The Telco does not invent a private RPC contract.

Two consequences:

- **Third-party agents can list** against the household vault on the same protocol the Telco's own sub-agents use. The marketplace is genuinely open — a startup that builds the world's best `LawnCareAgent` can plug into the Telco platform without bilateral integration work.
- **The customer can replace the orchestrator** with any MCP client that respects the consent grants. The Telco's lock-in is the **quality of the orchestrator and the partner-deal flow** behind it, not data hostage-taking.

## 5. Why "open" is the moat, not the concession

The intuition many Telco strategy teams start from is "open means we lose the customer to a competitor; close it down to protect the install base." This pack rejects that framing.

| Closed garden play | Open-by-construction play |
|---|---|
| Customer trusts the platform less | Customer trusts the platform **more** — they can leave any time, so they choose to stay |
| OEM partnerships are zero-sum (one OEM wins, others lose) | OEM partnerships are additive (every OEM benefits from distribution) |
| Regulator views the platform as a lock-in target | Regulator views the platform as the **reference design** for consumer data |
| Big Tech can replicate the closed garden, with more resources | Big Tech **cannot** credibly run an open garden — their core business depends on closed data |

The competitive moat is **the fact of openness itself**, combined with the Telco's structural advantages (the router, the billing relationship, the regulatory posture). Big Tech cannot copy "openness" without breaking their own business model. That is the durable defence.

## 6. What is **not** open

Two surfaces are deliberately not open and the pack should be clear about why:

1. **The Telco's commercial partnership terms.** The take rates, exclusivity clauses, and outcome-share methodology with grocers / utilities / payers are the Telco's negotiated value — they are not published in the open MCP catalog.
2. **The orchestrator's proprietary routing logic.** The orchestrator's prompt + reasoning approach is the differentiator at the marketplace layer. The interface is open; the brain is not.

Everything else — schemas, device interfaces, consent grants, audit logs, export formats — is open by design.

## 7. Public commitments document

The pack ships a one-page consumer-facing commitments document. Draft outline:

> **Your home. Your data. Our network.**
> 1. Your data lives in your vault. We operate it. You own the key.
> 2. You can export everything, anytime, in standard formats. One click. No phone call.
> 3. You can switch the orchestrator and keep your data. The MCP protocol is open.
> 4. We use Matter for every device class Matter supports. We do not require you to buy specific brands.
> 5. We tell you which agent did what, when, and what it cost. Every action is auditable.
> 6. We never sell your data. We never train on your data without your explicit, revocable consent.

These six lines are the **brand promise**. Everything else in this pack is the engineering that makes them true.
