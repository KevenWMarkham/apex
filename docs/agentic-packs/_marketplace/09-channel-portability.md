# 09 — Channel Portability & The Open MCP Spec

> _Draft — extends the open-home commitments from [`../telco/09-portability-open-home.md`](../telco/09-portability-open-home.md) to the marketplace level. Every Channel implements the same partner protocol; every Channel can be exported; every Channel can be switched off without losing the rest._

## 1. The five marketplace-level commitments

| # | Commitment | Enforced by |
|---|---|---|
| 1 | Your data lives in your vault, not in any Channel's silo. | Customer-held KMS key; vault export includes all Channel data. |
| 2 | You can export everything from any Channel, any time. | Lossless export format §3. |
| 3 | You can drop any Channel without losing the rest. | Per-Channel subscription model; no cross-Channel dependency lock-in. |
| 4 | Channel partners cannot lock you into one Telco. | Open `apex.tmt.mcp.partner.v1` protocol; partner-side multi-Telco listing is encouraged. |
| 5 | The marketplace tells you which Channel made which decision. | Audit log in `agent_run` + `agent_action`; visible in vault export. |

## 2. The open MCP partner spec — `apex.tmt.mcp.partner.v1`

Every Channel implements the same protocol surface. The spec is published in `docs/build-specs/` and licensed openly for any orchestrator (Telco, third-party, OSS).

### Required tools (every Channel)

```
- search(query: string, context: dict) → results[]
  Find items matching the customer's intent within this Channel.

- detail(item_id: string) → item_detail
  Return full information about one item.

- propose(item_id: string, traveler_or_household_info: dict) → proposal
  Generate a proposal (booking draft, order, action) without committing.

- commit(proposal_id: string, payment_method: PaymentMethod) → confirmation
  Execute the proposal. May require HITL approval per orchestrator policy.

- status(commit_id: string) → status
  Read current state of a committed action.

- modify(commit_id: string, change_request: dict) → new_confirmation
  Modify an existing commitment (e.g., rebook, change order).

- cancel(commit_id: string, reason: string) → cancellation_confirmation
  Cancel an existing commitment.

- preferences_read() → customer_preferences
  Read the customer's stored preferences within this Channel.

- preferences_write(preferences: dict) → ack
  Update the customer's stored preferences.
```

### Required webhooks

```
- state_change(commit_id, from_state, to_state, payload)
- disruption_event(commit_id, type, severity, recommended_action)
- loyalty_balance_update(member_token, new_balance, tier_change)
- proactive_offer(customer_token, offer_type, details, validity_window)
- compliance_event(customer_token, event_type, payload)
```

### Channel-specific extensions

Each Channel may extend the spec with vertical-specific tools — e.g., `apex.tmt.mcp.travel.v1` adds `irops_rebook`, `mobile_key_request`. Extensions are namespaced and additive; they do not override the base.

## 3. Vault export — marketplace additions

The marketplace adds three top-level folders to the vault export described in [`../telco/09-portability-open-home.md`](../telco/09-portability-open-home.md) §3:

```
vault-export-<household_id>-<timestamp>/
├── ...                                            # existing home + travel content
├── channel-subscriptions/
│   └── subscriptions-history.parquet              # which Channels active when
├── channel-actions/
│   └── actions-<channel-code>-YYYY.parquet        # all actions per Channel per year
└── marketplace-billing/
    └── invoices-YYYY-MM.json                      # which line items billed when
```

The customer can replay their entire marketplace history without Telco-side access.

## 4. Switching Telcos

If a customer switches Telcos, the agentic marketplace experience travels with them:

1. Customer exports their vault from old Telco (one tap)
2. New Telco imports the vault (one tap; ingest validates manifest hashes)
3. Channel subscriptions are re-established with each partner via the **portable partner-identity layer** (the partner sees "this is the same customer who was at old Telco with consent X, Y, Z; same vault root; same loyalty balances")
4. The Home Orchestrator on the new Telco picks up where the old one left off

The customer does **not** lose their loyalty balances, their preferences, their consent history, or their action audit trail. They lose only the old Telco's specific bundle pricing.

This is the **structural difference** between this marketplace and any vendor-cloud-locked agentic platform. Big Tech equivalents lose ~6 months of accumulated agent context when the customer switches; the marketplace loses none of it.

## 5. Open vs proprietary — the line

What is open:

- Partner MCP protocol
- Vault export format
- Schema definitions (Bronze envelope, Silver entity contracts, Gold view conventions)
- Consent grant vocabulary
- Compliance attestation framework
- Channel registry data model

What is proprietary:

- Each Telco's bundle pricing and commercial terms with partners
- Each Telco's orchestrator-routing logic (prompt + reasoning approach)
- Each Telco's customer-engagement instrumentation
- Each Telco's brand surfaces (UI, voice persona, design system)

This is the same line the streaming-bundle business draws today. It is well-understood by both partners and regulators. The Telco's value is in the operating-model differentiation, not in data hostage-taking.

## 6. What partner brands gain by participating

Brands that publish a Channel under this openness gain:

- **Multi-Telco distribution** from one MCP implementation
- **No bilateral integration tax** — every Telco accepts the same partner code
- **Verified customer identity** that travels with the customer across Telcos
- **No vendor lock-in risk** — the brand can pull the Channel from any one Telco without breaking the others
- **Regulatory cover** — the openness commitment is documented and audited; the brand inherits the trust posture

The openness is **mutual** — Telcos don't lock partners in, partners don't lock Telcos in, customers don't get locked into anyone.
