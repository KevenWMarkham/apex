# The Cross-Cloud Agentic Podcast — A Microsoft Seller's Honest Guide · `pc-cross-cloud-agentic`

An **eight-episode** podcast for Microsoft Target Platform Sellers (DMTSP) on how to win agentic AI work — across Microsoft, AWS, and Google Cloud — without overclaiming, without dismissing the other two clouds, and without drifting into partner-channel language that Independence prohibits. Safe for Deloitte AI team listeners. **Generic — no specific client is named on tape.** Reference clients are always archetypes: *a global retailer · a large auto manufacturer · a regulated bank · a hyperscale media company.*

> **First podcast in the family written specifically for Microsoft sellers.** The Trilogy speaks to the framework. The account podcasts speak to a single client. This series speaks to the seller carrying a Microsoft quota who is being asked the cross-cloud question by every CIO they meet.

---

## Why this podcast exists

Every Microsoft seller in 2026 is walking into the same conversation. The CIO has Azure. They also have AWS and a Vertex AI proof-of-concept. They have heard the Microsoft pitch on Fabric, Foundry, Agent Framework, and Purview. They have heard the AWS pitch on Bedrock and Athena Federated Query. They have heard the Google pitch on Vertex AI, BigQuery Omni, and Dataplex.

The seller's job is not to pretend the other two clouds do not exist. The seller's job is to know — at architectural depth — where Microsoft is genuinely the right answer, where it is a tie, and where the honest recommendation is to lead with someone else and let Microsoft compose. That is the only conversation a serious CIO respects.

This series is that conversation. Keven and Reid walk the agentic stack end to end — data foundation, runtime, governance, audit, FinOps, multi-cloud, the seller's playbook — and at every layer they compare what Microsoft, AWS, and GCP actually deliver. Reid is the cross-cloud honesty enforcer. When Keven overclaims for Microsoft, Reid pushes back. The disagreement is real, never performative.

---

## The hosts

**Keven** *(the practitioner)* — `en-US-AndrewNeural` · Trilogy continuity host. 22+ years on the Microsoft platform. Warm, confident, plain-spoken. Has been in the room when the CIO asked the hard cross-cloud question and has had to answer it on the spot.

**Reid** *(the cross-cloud principal architect)* — `en-US-AndrewMultilingualNeural` · Senior principal architect with buildout experience on all three clouds. Has shipped Bedrock-backed agents; has stood up Vertex AI Search; has run Fabric Mirroring and Foundry Agent Service in production. The cross-cloud honesty enforcer.

**A note on the voice pairing.** Both Keven and Reid use Andrew-family voices — `AndrewNeural` and `AndrewMultilingualNeural` respectively — the two highest-naturalness male voices in the edge-tts inventory. The personas are differentiated by **rate and pitch tuning** at synthesis: Keven at +0% rate, +0 Hz pitch (reference register); Reid at -3% rate, -2 Hz pitch (slower, slightly lower — the architect-thinking-through-it register). Vocabulary and sentence shape carry the rest. This is the **eighth distinct voice pairing** in the family.

---

## The Five Architectural Principles

The framework the series teaches is referred to on tape as *the Acceleration Framework* — descriptive, not branded. It rests on five principles. Every episode reinforces at least one. Episode 1 names them explicitly.

| # | Principle | One-line definition |
|---|---|---|
| 1 | **Gold-Tier-First** | Agents talk to a purpose-built Gold Tier shaped for reasoning — never directly to systems of record or data warehouses. |
| 2 | **Governance + Audit + Ledger as Trust Substrate** | DSPM-for-AI policy, hash-chained audit-row-per-step, and replay-token validation — the substrate that lets a regulated enterprise adopt an agent in a real decision flow. |
| 3 | **Identity Continuity** | Agent, operator, source-system, and auditor identities are all distinct and all interlinked. No translation gaps. |
| 4 | **No Replication — Sources Stay Untouched** | Virtualization, mirroring, shortcuts, federation. SORs continue serving OLTP; DWs continue serving BI; streams stay live. Gold is composed from sources that are never copied wholesale. |
| 5 | **Model Portability** | The agent design is portable across model generations — GPT, Claude, Gemini, Llama — and across the providers that host them. |

These five principles are platform-agnostic — they hold whether the buildout lands primarily on Azure, primarily on AWS, primarily on GCP, or genuinely multi-cloud.

---

## The eight episodes

| # | Title | Centered on |
|---|---|---|
| 01 | **The Agentic Stack + The Five Principles** | Wrong-way / right-way · the four-layer stack + identity · the five principles named · why now |
| 02 | **Data Foundation + The No-Replication Principle** | Medallion · Silver canonical · Gold composed · Fabric Mirroring · BigQuery Omni · Athena Federated Query · streaming · vector stores |
| 03 | **Agent Runtime: Talking to Gold, Not SORs** | MCP boundary · Foundry · Bedrock · Vertex AI · model availability · HITL patterns · RAG vs fine-tuning |
| 04 | **Governance, Identity, and Safety for Agentic AI** | Purview · Lake Formation + Macie · Dataplex · DSPM for AI · Entra · IAM federation · Workload Identity Federation · EU AI Act · NIST AI RMF · ISO 42001 · Bedrock Guardrails · AI Content Safety · Vertex Safety |
| 05 | **Audit, Ledger, and Replay: The Trust Substrate** | Audit row, not log line · hash chain · replay-token validation · the ledger pattern productized on Microsoft, assembled on AWS and GCP · operational observability |
| 06 | **FinOps for Agentic AI** | +20-40% QoQ cost growth · tokens · Copilot seats · agent runtime · vector store · audit-ledger storage · federation-query compute · model-mix optimisation · the CFO conversation |
| 07 | **Multi-Cloud Reality + Cloud + Model Portability** | Cloud-portable Acceleration Framework · model portability deep dive · what "primary cloud" actually means · cross-cloud egress · when multi-cloud is legitimate and when it is theatre |
| 08 | **The Seller's Playbook** | Five honest claims · four overclaims to avoid · six pushback-handling talking points · when to recommend NOT Microsoft · the six discovery openers · Wave sizing · funding programs (Independence-clean) |

Run time: approximately **246 minutes** across the series · 28-32 minutes per episode · 5,500-6,200 words per episode · ~48,000 words total.

---

## Independence from Microsoft · the two-contract model

This podcast is produced under Deloitte's Independence posture. The audio reflects it precisely:

- **Deloitte recommends.** When Keven and Reid recommend Microsoft Fabric, Agent Framework, Foundry, or Purview, that recommendation rests on the technical and economic merits — never on partner-channel compensation.
- **The client contracts directly with Microsoft.** Microsoft licensing flows on Microsoft paper. Deloitte does not resell, mark up, or take margin on Microsoft licensing.
- **The client contracts directly with Deloitte.** A separate Deloitte SOW governs the services scope.
- **Two contracts.** Clean separation. No compensation flows from Microsoft to Deloitte for influencing the client's cloud choice.
- **Three contracts when NVIDIA is in scope.** The client contracts directly with NVIDIA, with Microsoft, and with Deloitte — three separate paper paths, no margin stacking.

Episode 1 names this model explicitly. Episode 8 closes with it again as a discipline the seller carries into every meeting.

### Vocabulary absent from this podcast on purpose

The following words never appear on tape as endorsements. They are listed here so the discipline is visible: *co-sell* · *alliance* · *strategic partnership* · *channel partner* · *our partnership with Microsoft*. If a take drifts into partner-channel language, it is a re-record.

---

## Music sting

A new royalty-free **C-major chord in the boardroom register**, synthesised via ffmpeg additive synthesis. Same sting top and tail every episode. Distinct from the seven prior podcasts in the family — each podcast in the family has its own sting key and register.

---

## Files in this folder

```
pc-cross-cloud-agentic/
├── README.md
├── 00-show-bible-and-format.md
├── 01-the-agentic-stack-and-five-principles.md
├── 02-data-foundation-no-replication.md
├── 03-agent-runtime-talking-to-gold.md
├── 04-governance-identity-safety.md
├── 05-audit-ledger-replay.md
├── 06-finops-for-agentic-ai.md
├── 07-multi-cloud-and-portability.md
├── 08-the-sellers-playbook.md
├── _voice_audition.py
└── audio/_auditions/
```

---

*The implied listener: a Microsoft Target Platform Seller two weeks from a cross-cloud CIO conversation, looking for an honest, defensible architectural posture that holds up when the CIO pushes back. The seller who walks out of that meeting having said exactly what they meant — and nothing they didn't.*
