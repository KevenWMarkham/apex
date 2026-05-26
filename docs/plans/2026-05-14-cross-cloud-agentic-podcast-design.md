# The Cross-Cloud Agentic Podcast — Design

**Date:** 2026-05-14
**Author:** Keven Markham (kmarkham@deloitte.com) · Deloitte's Microsoft Technology & Services Practice
**Status:** Design approved · ready for writing-plans handoff
**Folder target:** `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic\`

---

## Goal

Build an 8-episode podcast that teaches **Microsoft Target Platform Sellers** how to credibly position the Microsoft platform for agentic AI in clients running **any of the three major clouds** (Azure, AWS, GCP) — including genuine multi-cloud realities. The series operates under **Independence-minded** discipline: recommendations on technical and economic merits, two-contract model, no co-sell / alliance / partner language. Generic — no specific client referenced.

The series teaches sellers an **architectural framework** (five principles) that is **vendor-neutral by design** — the Microsoft case is that Microsoft's **productized capability density** across the five principles reduces engineering scope to deliver the framework's value. AWS and GCP can reach the same architectural endpoint; the productization difference is the seller's honest pitch.

## Audience

**Primary:** Microsoft Target Platform Sellers (DMTSP — Deloitte's Microsoft Technology & Services Practice). They sell Microsoft Fabric, Foundry, Agent Framework, Purview, Entra, Power Platform. They face clients with mixed cloud realities and a Deloitte AI team that is properly cloud-agnostic.

**Secondary (safe-to-listen):** Deloitte AI team members. The series does not pretend Microsoft is universally superior; it honestly identifies where AWS / GCP have parity or advantage. A Deloitte AI team listener should find the analysis defensible.

**Not the audience:** Clients. The seller's-playbook framing is internal Deloitte preparation, not client-facing content. Generic enough to be safe if shared externally, but not designed for client consumption.

## Architecture — The Five Principles

The Acceleration Framework's architectural commitments. Each principle is cloud-neutral; Microsoft / AWS / GCP differ in productized capability density per principle.

| # | Principle | One-line definition |
|---|---|---|
| 1 | **Gold-Tier-First** | Agents talk to a purpose-built Gold Tier shaped for reasoning — never directly to SORs or data warehouses. |
| 2 | **Governance + Audit + Ledger as Trust Substrate** | DSPM-for-AI policy + hash-chained audit-row-per-step + replay-token validation. |
| 3 | **Identity Continuity** | Agent / operator / source / auditor identity all distinct but interlinked. No translation gaps. |
| 4 | **No Replication — Sources Stay Untouched** | Virtualization / mirroring / shortcuts / federation. SORs continue serving OLTP. DWs continue serving BI. Streams stay live. |
| 5 | **Model Portability** | Agent design portable across GPT / Claude / Gemini / Llama generations. Not locked to one model. |

These five principles are named explicitly in Episode 1 and threaded through every subsequent episode.

## Tech Stack

| Component | Tool |
|---|---|
| Script format | Markdown · `**KEVEN:**` / `**REID:**` dialog markers |
| TTS | `edge-tts` (Microsoft Edge Neural TTS) |
| Audio concatenation | `ffmpeg` |
| Music sting synthesis | `ffmpeg` lavfi `sine` + filter chains (additive synthesis) — new C-major boardroom register |
| Output format | MP3 · 24kHz mono · 48 kbps · podcast-standard |
| Excel companion | None (this is a content-only podcast) |

## Voice cast

| Host | Voice (edge-tts) | Persona |
|---|---|---|
| **Keven** | `en-US-AndrewNeural` | Trilogy continuity host. 22+ years on the Microsoft platform. The practitioner. Microsoft-lens by tenure, but Independence-rigorous. |
| **Reid** | `en-US-DavisNeural` *(audition first; alternate if synthetic-sounding)* | Senior principal architect. Has built production-grade agentic stacks on Microsoft Azure, AWS Bedrock, AND GCP Vertex AI. The cross-cloud honesty enforcer. Pushes back when Keven overclaims. |

**8th distinct voice pairing** in the APEX podcast family:
1. Sellers: Andrew + Brian
2. Services v2: Andrew + Emma
3. Deployment: Andrew + Ava
4. Disney Account: Andrew + Emma Multilingual
5. Disney Studios: Andrew + Ava Multilingual
6. DTNA: Andrew + Brian Multilingual
7. Toyota Zero Day Warranty: Andrew + Michelle
8. **Cross-Cloud Agentic (this): Andrew + Davis**

The Keven-vs-Reid disagreement is **structural**, not performative. Reid pushes back when Microsoft really isn't differentiated, so sellers don't get caught overclaiming in front of a Deloitte AI-team member or client architecture office. Every episode has at least one substantive disagreement-and-convergence moment.

## Episode breakdown

| Ep | Title | Length | Words |
|---|---|---|---|
| 1 | The Agentic Stack + The Five Principles | ~30 min | ~5,800 |
| 2 | Data Foundation + The No-Replication Principle | ~32 min | ~6,200 |
| 3 | Agent Runtime: Talking to Gold, Not SORs | ~30 min | ~5,800 |
| 4 | Governance, Identity, and Safety for Agentic AI | ~32 min | ~6,200 |
| 5 | Audit, Ledger, and Replay: The Trust Substrate | ~32 min | ~6,200 |
| 6 | FinOps for Agentic AI | ~28 min | ~5,500 |
| 7 | Multi-Cloud Reality + Cloud + Model Portability | ~30 min | ~5,800 |
| 8 | The Seller's Playbook | ~32 min | ~6,200 |
| | **TOTAL** | **~246 min** | **~47,700** |

### Episode 1 — The Agentic Stack + The Five Principles

Wrong-way / right-way opening: don't point agents at SORs or DWs directly. The four-layer agentic stack (data foundation, agent runtime, control plane, model serving) plus identity as a fifth cross-cutting concern. The Five Principles named explicitly as the Acceleration Framework's commitments. Why now (2024-2026 inflection — Foundry GA, Bedrock Agents GA, Vertex AI Agent Builder GA all within 18 months). The Microsoft seller's Independence-minded lens. What we'll cover across 8 episodes. Real disagreement: Reid argues "agent" is overloaded — most things called agents are pipelines. Keven defines the term where Gold-Tier-MCP-boundary + reasoning + audit-row-per-step are all present.

### Episode 2 — Data Foundation + The No-Replication Principle

Medallion architecture as the Acceleration Framework substrate. Silver = canonical layer (per the show-bible rule, NOT Gold). Gold = composed per-scenario, per-entity-joinable, shaped for agent reasoning. **The No-Replication Principle explicit:** virtualization / mirroring / shortcuts / federation — not bulk copy. SORs continue serving OLTP, DWs continue serving BI, streams stay live. Microsoft Fabric Mirroring (productized, broadest source coverage) + Shortcuts + Eventstreams. GCP BigQuery Omni + BigLake (strongest cross-cloud federation). AWS Athena Federated Query + Lake Formation (most assembly required on this axis). Vector store strategy across the three. Streaming-source architecture (Kafka / EventHub / Kinesis / Pub/Sub windowing). Real disagreement: Reid argues BigQuery Omni is the strongest cross-cloud federation story on the market today; Keven concedes the point but counters with Fabric's tighter governance integration on mirrored sources.

### Episode 3 — Agent Runtime: Talking to Gold, Not SORs

The MCP boundary discipline. Agent tool calls land on Gold views — never on SORs directly. Microsoft Agent Framework + Foundry, AWS Bedrock Agents, GCP Vertex AI Agent Builder + Agent Engine. Model availability per runtime (GPT, Claude, Gemini, Llama families). Orchestration patterns (sequential, parallel, hierarchical). HITL design patterns deeper: gate placement (before-irreversible-action), interface design, escalation paths, feedback loops. RAG vs fine-tuning vs distillation — the domain-adaptation spectrum. Real disagreement: Reid argues Anthropic Claude is materially better on Bedrock than on Foundry today; Keven counters with the OpenAI velocity on Foundry and the partner-model availability roadmap.

### Episode 4 — Governance, Identity, and Safety for Agentic AI

The policy layer (Principle 2 — governance side) + Identity Continuity (Principle 3) + Safety/Risk frameworks (NEW addition).

**Governance:** Microsoft Purview (catalog + lineage + access + sensitivity + DSPM-for-AI in one product). AWS Lake Formation + Macie + Audit Manager + GuardDuty (multi-service assembly). GCP Dataplex + Sensitive Data Protection + Security Command Center. DSPM for AI as the newest productized capability — Microsoft's strongest single differentiation today.

**Identity:** The agent has an identity (Entra service principal / IAM role / GCP service account). The operator has identity. The auditor has identity. The source systems have identity. Identity propagates through every tool call and lands in every audit row. Microsoft Entra ID as single plane (broadest enterprise SaaS federation: Microsoft 365 + SAP + Salesforce + Workday). AWS IAM + IAM Identity Center + Cognito (multi-service identity). GCP Cloud IAM + Workload Identity Federation (strongest cross-cloud federation primitive).

**Safety:** EU AI Act, NIST AI RMF, ISO 42001. Prompt injection. Data exfiltration via tool calls. Microsoft Azure AI Content Safety + Defender for Cloud AI. AWS Bedrock Guardrails. GCP Vertex AI Safety filters. Model-risk-management posture.

Real disagreement: Reid argues GCP Workload Identity Federation makes cross-cloud agent identity portable in a way Entra can't match; Keven counters with the enterprise-SaaS federation reach.

### Episode 5 — Audit, Ledger, and Replay: The Trust Substrate

The evidence layer (Principle 2 — audit/ledger side). Why agentic AI requires a different audit pattern than traditional ML: the reasoning chain is the artifact, not just the final output. **"Audit row, not log line"** as the discipline. The hash-chained audit row pattern — every agent decision lands as a structured row with decision context, agent identity, model version, tool calls invoked, data accessed, parent-row hash, and output hash. Cryptographic tamper evidence. Replay-token validation — External Audit Reviewer reproduces reasoning offline against the audit chain. HITL gates as audit events. Identity propagation INTO each audit row. Lineage thread from audit row → Gold view → Silver canonical → Bronze reference → source system (and source identity).

The ledger pattern productized vs assembled:
- **Microsoft**: Foundry + Purview audit echo = productized reference architecture
- **AWS**: DynamoDB hash-chain table OR Amazon QLDB (note honestly: in maintenance mode) OR OpenSearch append-only — custom build
- **GCP**: BigQuery append-only audit tables with content-hash columns — custom build

Why this matters: regulated industries (HLS, FinServ, regulated Mfg), EU AI Act compliance, NIST AI RMF, board-level AI governance, External Audit Reviewer offline replay.

**Operational observability** (NEW addition): the SRE side alongside the compliance side. Prompt failure rates, tool-call latency, model-version drift detection, source-schema-drift surfacing. Distinct from audit but uses the same substrate.

Real disagreement: Reid argues the ledger pattern is overengineered for most enterprise AI; Keven argues regulated-industry and board-level governance make it table stakes.

### Episode 6 — FinOps for Agentic AI (NEW)

The cost explosion: +20-40% QoQ AI consumption growth across the enterprise. No cloud has productized "AI Cost Management" yet — Azure Cost Management, AWS Cost Explorer, GCP Cloud Billing all handle compute and storage well but AI-consumption-specific cost analytics is custom-built at most enterprises.

Cost sources covered:
- Per-token model costs (GPT, Claude, Gemini, Llama priced differently)
- Copilot seat utilisation (M365 Copilot, GitHub Copilot, Power Platform AI Builder)
- Agent runtime compute
- Vector store storage and query cost
- Embedding API spend
- Custom-model hosting
- Federation-query compute (the cost of the No-Replication Principle — pay-per-query rather than pay-once-for-copy)
- Audit-ledger storage (append-only = grows forever; cold-tier archival discipline required)
- Bronze / Silver / Gold storage tier economics

**Cost management across clouds:**
- Microsoft: Azure Cost Management for OpenAI/Foundry + M365 Copilot Admin Center (seat tracking) + Microsoft Cost Management for Azure OpenAI + Power BI for analytics
- AWS: AWS Cost Explorer + Bedrock cost reporting + per-model pricing transparency + Cost & Usage Reports
- GCP: Cloud Billing + Vertex AI cost reporting + per-model pricing

**Model-mix optimization:** the discipline of using cheap small models (GPT-4o-mini, Claude Haiku, Gemini Flash) where they suffice, expensive large models where they earn the cost. Per-use-case cost-per-outcome.

**Idle Copilot seat reclamation.** **Audit-ledger storage cost discipline.** The CFO conversation: per-use-case cost-per-outcome, ROI per agent, cost-vs-value composition.

Real disagreement: Reid argues "FinOps for AI is the same as FinOps for cloud"; Keven counters that AI consumption has different cost dynamics (per-token, per-seat, model-mix) that traditional cloud FinOps doesn't address.

### Episode 7 — Multi-Cloud Reality + Cloud + Model Portability

The Acceleration Framework is architecturally cloud-portable because all five principles are cloud-neutral. Bronze can land anywhere. Silver canonical schemas travel. Gold per-scenario views travel. Identity federates. The audit ledger composes. **Multi-cloud is the natural endpoint of "no replication" when source systems span clouds.**

**Model Portability (Principle 5) deep dive:** Agent design portable across model generations. Versioned prompts. Tool-call abstractions. Model-agnostic SDKs. Why this matters: GPT-4 → 4o → 4.1 happened in 18 months; Claude 3.5 → 3.7 → 4.x in 12 months; Gemini 1.5 → 2.0 in 9 months. An agent locked to a specific model is a wave-1-only asset. AWS Bedrock has the strongest multi-vendor model story (Claude native, Llama, Mistral, Cohere, Stability). GCP Vertex AI Model Garden (Gemini, Claude, Llama). Microsoft Foundry (OpenAI primary, Anthropic via partner integrations).

What "primary cloud" actually means in practice (90%+ of agentic workloads land on one cloud per scenario). Cross-cloud egress economics — the real reason multi-cloud is rare. Identity federation patterns. Multi-cloud audit chain composition. When cross-cloud composition is legitimate (regulatory data residency, source-resident gravity) vs theatre (architectural-elegance-for-its-own-sake).

Real disagreement: Keven argues multi-cloud at agentic stack is rare; Reid argues data-residency-mandated multi-cloud is increasingly real.

### Episode 8 — The Seller's Playbook

The Acceleration Framework + the Five Principles as the architectural pitch — cloud-neutral. Microsoft's productization advantage on each principle. Independence-minded framing: recommend on technical and economic merits; no co-sell; two-contract model.

**Five honest claims** Microsoft sellers can defend.
**Four overclaims** to avoid (named explicitly).
**Six pushback-handling talking points**:
1. "We're AWS-primary"
2. "We're GCP-primary"
3. "Deloitte should be cloud-agnostic"
4. "Microsoft compensation is influencing the recommendation"
5. "We want portability later" (model and cloud)
6. "We don't want our data replicated into a new lake" (the No-Replication objection — now answerable on the merits)

**When to recommend NOT Microsoft:** AWS-resident data gravity, GCP-strategic posture, multi-cloud regulatory mandate, specific Anthropic-on-Bedrock or Gemini-on-Vertex preferences.

**The seller's six discovery openers** (one per principle + FinOps):
1. *"Are your agents pointing at SORs or your data warehouse directly?"* (Principle 1)
2. *"How are you handling AI governance and audit for agent decisions today?"* (Principle 2)
3. *"What identity does your agent run as, and how does that identity propagate to source access?"* (Principle 3)
4. *"Are you replicating data into a new lake to make AI work, or are your sources staying untouched?"* (Principle 4)
5. *"How model-portable is your agent design — could you swap GPT for Claude tomorrow if you needed to?"* (Principle 5)
6. *"What's your AI consumption cost trajectory looking like quarter-over-quarter?"* (FinOps thread)

**Wave sizing / 90-day pilot path:** what makes a good Wave 1 (operational, contained, measurable). What kills agentic projects.

**Funding programs** (Independence-clean handling): Microsoft BVA / ECIF / Azure Credits; AWS ProServe credits / MAP; GCP Cloud Innovation Credits. Frame as discovery-funding for the client's benefit — never as compensation flowing to Deloitte for influencing client cloud choice.

**Closing posture:** the Microsoft platform earns the recommendation on merits. The Acceleration Framework + the Five Principles is what makes that recommendation defensible across any cloud reality.

## Production scope (what gets built)

| Deliverable | Path |
|---|---|
| Series README | `pc-cross-cloud-agentic/README.md` |
| Show bible | `pc-cross-cloud-agentic/00-show-bible-and-format.md` |
| 8 episode scripts | `01-the-agentic-stack-and-five-principles.md` through `08-the-sellers-playbook.md` |
| Voice audition script | `_voice_audition.py` (Davis sample; alternates if synthetic) |
| Audio build script | `_build_audio.py` (Andrew + Davis, edge-tts) |
| Music sting builder | `_build_music.py` (C-major boardroom register) |
| Music sting applier | `_apply_music.py` (idempotent wrap) |
| 8 episode MP3s | `audio/01-*.mp3` through `audio/08-*.mp3` |
| Audio README | `audio/README.md` |

## Data flow

**Writing phase:** Author each episode markdown using the established APEX podcast family style — cold open, stair-step exposition, real disagreement moment, quote-and-react from primary sources, what-to-carry-forward closer, Further Reading per episode. Each episode ~5,500-6,200 words.

**Audio generation phase:**
1. `_voice_audition.py` → generates 1-2 sample MP3s of Davis (and alternates) reading a representative passage; user confirms voice fit before production run
2. `_build_music.py` → generates `opening_sting.mp3` (5s) + `closing_sting.mp3` (6s) in C-major boardroom register
3. `_build_audio.py --all` → parses each episode .md, generates per-segment MP3s via edge-tts (Andrew for KEVEN, Davis for REID, 350ms inter-turn pauses), concatenates via ffmpeg, outputs `audio/0X-*.mp3`
4. `_apply_music.py` → wraps each episode with opening + 300ms silence + episode + 300ms silence + closing, backs up unstinged originals in `audio/_originals/`

## Error handling

- **edge-tts 503 rate limits:** retry with exponential backoff (5 attempts, 8 → 128 sec)
- **ffmpeg errors:** explicit cwd setting on concat operations
- **Idempotence:** `_apply_music.py` keeps stingless backups; re-running is safe
- **Voice rejection path:** if Davis sounds synthetic in audition (Aria lesson), re-audition with alternates (JasonNeural, BrandonNeural, GuyNeural) before committing to production run

## Testing

- **Per-episode parse test:** confirm `DIALOGUE_RE` matches every KEVEN/MIA turn — wait, **REID** turn here — segment count matches manual review
- **Forbidden-term scan:** no "co-sell" / "alliance" / "strategic partnership" / "channel partner" in any dialog body
- **Principle threading scan:** each episode contains references to its relevant Principle(s)
- **Cloud-balance scan:** each capability-comparison episode names Microsoft, AWS, AND GCP at least N times (target balance)
- **Audio sanity check:** ffprobe duration on each generated MP3 within ±10% of target
- **Sting integrity:** opening sting 5s±0.3s, closing sting 6s±0.3s
- **Idempotence check:** `_apply_music.py` twice produces identical output

## Out of scope

- Talent / change management (operators working with agents) — future series
- Industry-vertical-specific deep dives (HLS / FinServ / Mfg / Retail / Gov) — sellers learn these through anchor accounts
- Specific funding-program operational mechanics — should be a one-pager, not podcast content
- 24-Step Chain rows in APEX-Scenario-Chains.xlsx — this podcast does not require new scenarios; it teaches the framework, not specific scenarios
- Excel companion play-book — N/A (this is content-only, not a play catalog)
- Translation to other languages — out of scope for v1
- Interactive / branching episodes — out of scope

## Open questions deferred to writing-plans

- Exact voice character of Davis — audition needed before commit; alternates ready if synthetic-sounding
- Music sting precise musical progression (C major specific notes / harmonics) — `_build_music.py` author's call at implementation time
- Whether to include a brief "audition outcome" note in Ep 1 if Davis required substitution — likely yes, in show bible

---

**Next step:** invoke `superpowers:writing-plans` to produce the bite-sized implementation plan with TDD-style task breakdown for the 8-episode production.
