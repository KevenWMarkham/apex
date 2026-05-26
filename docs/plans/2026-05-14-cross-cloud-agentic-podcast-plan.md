# Cross-Cloud Agentic Podcast Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build an 8-episode internal-Microsoft-seller podcast teaching the Five Architectural Principles for agentic AI across Microsoft, AWS, and GCP — Independence-minded, generic, with full audio production.

**Architecture:** Markdown scripts (KEVEN / REID dialog) parsed by `edge-tts` for voice synthesis, concatenated by `ffmpeg`, wrapped with C-major boardroom-register music stings synthesised by ffmpeg additive synthesis. Mirrors the proven APEX-podcast-family pattern across 7 prior podcasts (Trilogy + 4 account podcasts).

**Tech Stack:** Python 3.x · `edge-tts` (Microsoft Neural TTS) · `ffmpeg` (concat demuxer + lavfi sine source for music) · Markdown for scripts · MP3 24kHz mono 48 kbps output.

**Design doc:** `docs/plans/2026-05-14-cross-cloud-agentic-podcast-design.md` — refer to this for the Five Principles, episode focus details, and source-coverage rules.

**Reference podcast (closest pattern):** `C:\Stage\Clients\Industries\APEX\docs\podcast\pc-toyota-zero-day-warranty\` — most recent production; same Andrew + female-second-voice pattern; same audio scripts as the copy-template. The audio/music build scripts copy almost verbatim from there.

---

## Pre-Task — Voice audition before episode writing begins

Davis (`en-US-DavisNeural`) is the planned co-host voice for REID. The Aria experience from Toyota taught us that some edge-tts voices read as synthetic. Audition Davis (and one or two alternates) BEFORE writing 48,000 words of dialog that may need re-recording.

### Task 0: Voice audition for Davis (+ alternates)

**Files:**
- Create: `pc-cross-cloud-agentic/_voice_audition.py`

**Step 1: Scaffold the folder**

```bash
mkdir -p "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
```

**Step 2: Write the audition script**

Model on `pc-toyota-zero-day-warranty/_voice_audition.py`. Three candidates:

```python
CANDIDATES = [
    ("reid-davis.mp3",    "en-US-DavisNeural"),
    ("reid-brandon.mp3",  "en-US-BrandonNeural"),  # newer Neural; alt 1
    ("reid-jason.mp3",    "en-US-JasonNeural"),    # newer Neural; alt 2
]
```

Use a representative passage in Reid's register — technical/architectural, ~30 seconds:

```python
PASSAGE = (
    "I want to push back on something. The phrase 'agent' is overloaded. "
    "Most of what gets called agentic AI in production today is a pipeline — "
    "a deterministic sequence of model calls and tool invocations. That's "
    "useful, but it's not what we mean when we talk about the agentic stack. "
    "The agentic stack requires reasoning, tool use, state, and an audit "
    "substrate that an external reviewer can replay. If those four aren't "
    "all present, you're shipping a pipeline. And pipelines are fine — "
    "but they don't earn the governance posture the agentic stack does."
)
```

**Step 3: Run the audition**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python _voice_audition.py
```

Expected: 3 MP3s in `audio/_auditions/`, ~30s each.

**Step 4: User picks the winner**

The controller (Claude) presents the 3 audition files to the user with an `AskUserQuestion` prompt:
- Davis (default recommendation)
- Brandon (newer Neural; warmer)
- Jason (newer Neural; more clipped)
- Other (re-audition with different voice)

**Step 5: Lock the voice choice in the rest of the plan**

Update Task 7 (`_build_audio.py`) with the chosen voice. If the user rejects all three, escalate to a 4-candidate re-audition (Roger, Eric, Tony, Andrew Multilingual) before proceeding.

**Step 6: Commit (optional)**

```bash
git add docs/podcast/pc-cross-cloud-agentic/_voice_audition.py
git commit -m "feat: voice audition script for Cross-Cloud Agentic podcast"
```

---

## Task 1: Folder + Series README + Show Bible

**Files:**
- Create: `pc-cross-cloud-agentic/README.md`
- Create: `pc-cross-cloud-agentic/00-show-bible-and-format.md`

**Step 1: Write `README.md`**

Match the structure of `pc-toyota-zero-day-warranty/README.md` and `pc-dtna-account/README.md`. Sections:
1. Series title — *"The Cross-Cloud Agentic Podcast — A Microsoft Seller's Honest Guide"*
2. One-line description + audience disclosure (Microsoft Target Platform Sellers; safe for Deloitte AI team listeners; generic, no client specified)
3. The hosts — Keven (Andrew) + Reid (audited voice). 8th distinct pairing.
4. The Five Architectural Principles named with one-line definitions
5. The eight episodes — table with titles and one-line "centered on" descriptions
6. Independence framing — Deloitte recommends on technical and economic merits; no co-sell; two-contract model; no compensation flows from Microsoft to Deloitte for influencing client cloud choices
7. Forbidden vocabulary list — "co-sell," "alliance," "partner," "strategic partnership," "channel partner" — explicit "absent from this podcast on purpose"
8. Music sting disclosure — royalty-free C-major boardroom register, ffmpeg-synthesised
9. Companion podcasts — Sellers / Services / Deployment Trilogy + 4 account podcasts
10. Files in folder

Target: ~1,100-1,300 words.

**Step 2: Write `00-show-bible-and-format.md`**

Match the structure of `pc-toyota-zero-day-warranty/00-show-bible-and-format.md`. Sections:
1. The series at a glance — comparison table (Trilogy / Account podcasts / **this**)
2. Voice rules — Keven's register, Reid's register, the structural disagreement dynamic
3. The Five Principles — referenced (not redefined; that's the README's job)
4. Cross-cloud-honesty discipline — explicit "Reid is the cross-cloud honesty enforcer; Keven defers when Reid pushes correctly"
5. Independence rules — locked posture, forbidden vocabulary, two-contract framing
6. Production rules — cold-open scenes, stair-step pedagogy, real disagreement per episode, quote-and-react, what-to-carry-forward closer, Further Reading per episode
7. What NOT to do — name specific clients, name internal codenames (APEX, ORCH-01, BRML, AAML, etc. — they NEVER appear on tape; the podcast teaches the Acceleration Framework generically), use forbidden vocabulary, overclaim Microsoft, dismiss AWS/GCP capabilities, dismiss Deloitte AI team pushback
8. Numbers discipline — no fabricated metrics; reference industry sources (Gartner, IDC, Forrester) without fabricating specific dollar figures

Target: ~1,300-1,500 words.

**Step 3: Verify**

```bash
ls "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic/"
# Expected: README.md + 00-show-bible-and-format.md + _voice_audition.py
wc -w "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic/"*.md
# Expected: README.md 1100-1300 words, show bible 1300-1500 words
```

Spot check: README contains the Five Principles section and the Independence disclosure. Show bible contains the forbidden-vocabulary list and "Reid is the cross-cloud honesty enforcer" framing.

**Step 4: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/README.md docs/podcast/pc-cross-cloud-agentic/00-show-bible-and-format.md
git commit -m "feat: scaffold Cross-Cloud Agentic podcast (README + show bible)"
```

---

## Task 2: Episode 1 — The Agentic Stack + The Five Principles

**Files:**
- Create: `pc-cross-cloud-agentic/01-the-agentic-stack-and-five-principles.md`

**Step 1: Write the script** (target ~5,800 words, ~30 min)

**Required template structure (in order):**

```markdown
# Episode 01 · The Agentic Stack and the Five Principles

**Builds on:** Trilogy — Sellers Ep 2 (Commercial Arc / Independence) · Sellers Ep 4 (Practices) · Services Ep 4 (MCP boundary)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-14

---

## Cold Open

[Sound: an architectural review room ambient. A whiteboard. The end of a Friday.]

[Open with the wrong-way / right-way contrast viscerally. A Microsoft seller has been asked "can you build an agent on top of our Snowflake data warehouse?" The right answer is "I can — but you'll wish I hadn't." Set the architectural premise of the series.]

---

## The conversation

### Why "agentic" needs a definition before we start

[6-8 turns. Reid pushes back on the term "agent" being overloaded. Keven defines: reasoning + tool use + state + audit substrate = agent. Pipelines are useful but they're not agents. The four-criterion definition becomes the show's working definition.]

### The four-layer agentic stack — plus identity as a fifth cross-cutting concern

[8-10 turns. Layer 1: data foundation (where the Gold Tier lives). Layer 2: agent runtime (Foundry / Bedrock / Vertex AI). Layer 3: control plane (governance + audit + ledger). Layer 4: model serving (NIM / Triton / cloud-native serving). Identity sits across all four. Stair-step build.]

### The Five Architectural Principles — named explicitly

[12-15 turns. Walk each principle with one-paragraph framing. Don't go deep — that's Eps 2-7's job.

**Principle 1 — Gold-Tier-First:** agents talk to a purpose-built Gold Tier composed from SORs and DWs; never directly to SORs or DWs. Why: brittleness, governance scope, audit complexity.

**Principle 2 — Governance + Audit + Ledger as Trust Substrate:** DSPM-for-AI policy + hash-chained audit-row-per-step + replay-token validation. Why: regulated industries require it; board-level AI governance requires it.

**Principle 3 — Identity Continuity:** agent / operator / source / auditor identities all distinct but interlinked. Why: identity translation gaps are audit gaps and security gaps.

**Principle 4 — No Replication — Sources Stay Untouched:** virtualization / mirroring / shortcuts / federation. SORs continue serving OLTP; DWs continue serving BI; streams stay live. Why: operational performance, governance scope, lineage accuracy.

**Principle 5 — Model Portability:** agent design portable across GPT / Claude / Gemini / Llama generations. Why: 18-month model-generation refresh cycles; vendor lock-in risk.

The Five Principles are the architectural framework this series teaches.]

### Why now — 2024-2026 inflection

[6-8 turns. Foundry GA, Bedrock Agents GA, Vertex AI Agent Builder GA all within 18 months. DSPM for AI productized 2025. Audit-ledger reference architectures emerging. Industry standards landing (EU AI Act in force 2025; NIST AI RMF 2024). The architectural conversation is settle-able now in a way it wasn't 24 months ago.]

### The Microsoft seller's lens — Independence-minded

[6-8 turns. The series operating model. Recommend on technical and economic merits. The Five Principles are vendor-neutral architecture. Microsoft earns the recommendation on productized-capability density — which sellers can defend honestly across all five principles. Two-contract model. No co-sell. The honest sales motion.]

### What we'll cover across eight episodes

[4-6 turns. Brief roadmap. Don't repeat content from those episodes.]

### A reading I want to do

**KEVEN:** [reading, paraphrased — Gartner or Forrester or McKinsey AI agent market analysis register. Paraphrase, don't fabricate a specific quote.]

**REID:** [reacts — the productization wave is real but the architectural discipline is what makes it deliverable, not the productization itself.]

### One disagreement

**REID:** [pushes — "agent" is overloaded; most things called agents are pipelines.]

**KEVEN:** [counter — agrees on overload but defends the four-criterion definition; pipelines are useful and the series will be precise about when "agent" applies vs when it doesn't.]

[Convergence: precise vocabulary discipline through the series.]

### What to carry forward

**KEVEN:** Three things.

**REID:** Go.

**KEVEN:** *One — the four-layer agentic stack plus identity as the fifth cross-cutting concern.*

*Two — the Five Architectural Principles as the Acceleration Framework's commitments. Vendor-neutral architecture.*

*Three — Microsoft earns the recommendation on productized-capability density across the five principles, not on partner-channel motion.*

**REID:** Next episode — *Data Foundation and the No-Replication Principle.* The Gold Tier across Fabric, Lake Formation, and Dataplex. Mirroring, Shortcuts, BigQuery Omni, Athena Federated Query. Sources stay untouched.

**KEVEN:** See you there.

[outro]

---

## Further reading

### Industry analyses
- **Gartner Hype Cycle for AI** — generative and agentic categories
- **Forrester** — agentic AI market and platform analyses
- **McKinsey & Company** — *The State of AI in [year]* annual report
- **IDC** — AI platforms market forecast

### Standards and frameworks
- **EU AI Act** — published in EU Official Journal
- **NIST AI Risk Management Framework (NIST AI RMF)**
- **ISO/IEC 42001** — AI management systems

### Microsoft Learn
- **Microsoft Fabric** — overview
- **Microsoft Agent Framework SDK** — agent runtime
- **Azure AI Foundry** — agent hosting
- **Microsoft Purview** — governance

### AWS documentation
- **AWS Bedrock Agents**
- **AWS Lake Formation**
- **Amazon Macie**

### Google Cloud documentation
- **Vertex AI Agent Builder**
- **Google Cloud Dataplex**
- **BigQuery Omni**

---

**End of Episode 01 · The Agentic Stack and the Five Principles**
*≈ 5,800 words · target 30 minutes at conversational pace*
```

**Style rules (CRITICAL — applies to all 8 episodes):**

1. **Generic.** No client names. Reference clients only as "a global retailer," "a large auto manufacturer," "a regulated bank," etc.
2. **Forbidden vocabulary** — `co-sell`, `alliance`, `strategic partnership`, `channel partner`, `our partnership with Microsoft` — never on tape.
3. **No internal codenames on tape** — APEX, ORCH-01, BRML, CVML, QEML, AAML, AXLE Practice, SB06, LEDGER (all-caps brand). On tape: "the Acceleration Framework," "the ledger pattern" (lowercase), "the audit row chain." Internal terms permitted in front-matter "Builds on:" and Further Reading sections only.
4. **Real disagreement** between Keven and Reid every episode. Reid is the cross-cloud honesty enforcer.
5. **No fabricated metrics.** Reference Gartner / Forrester / McKinsey / IDC in spirit without inventing specific dollar figures or percentages.
6. **NVIDIA composability acknowledged.** All three clouds run NVIDIA stack; this is platform-neutral.
7. **No emojis.**

**Step 2: Verify**

```bash
python -c "
import re
text = open('C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic/01-the-agentic-stack-and-five-principles.md', encoding='utf-8').read()
words = len(text.split())
segments = len(re.findall(r'^\*\*(KEVEN|REID):\*\*', text, re.MULTILINE))
print(f'words: {words} | segments: {segments}')
assert 5400 < words < 6300
assert 50 < segments < 110

# Body
body = text.split('## Further reading')[0]
parts = body.split('---', 2)
dialog = parts[2] if len(parts) > 2 else body

# Forbidden terms
for t in ['co-sell', 'alliance', 'strategic partnership', 'channel partner']:
    assert t.lower() not in dialog.lower(), f'forbidden: {t}'

# Internal codenames not on tape
for c in ['APEX', 'ORCH-01', 'BRML', 'CVML', 'QEML', 'AAML', 'AXLE Practice', 'SB06']:
    assert c not in dialog, f'codename on tape: {c}'

# All Five Principles named
for p in ['Gold-Tier-First', 'Governance', 'Audit', 'Ledger', 'Identity', 'No Replication', 'Model Portability']:
    assert p in dialog, f'missing principle reference: {p}'

print('OK')
"
```

Expected: `OK`.

**Step 3: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/01-the-agentic-stack-and-five-principles.md
git commit -m "feat: Ep 1 — The Agentic Stack and the Five Principles"
```

---

## Task 3: Episode 2 — Data Foundation + The No-Replication Principle

**Files:**
- Create: `pc-cross-cloud-agentic/02-data-foundation-and-no-replication.md`

**Step 1: Write the script** (target ~6,200 words, ~32 min)

**Required content beats:**

- Cold open: a data architect's recurring nightmare — every new agentic project demanding "yet another copy of the data into yet another lake." The No-Replication principle is the antidote.
- The medallion architecture (Bronze landing / Silver canonical / Gold composed) — Silver as canonical layer (NOT Gold; per show-bible rule)
- Why agentic AI specifically needs Gold-Tier-shaped views, not BI-shaped DW views
- **Microsoft Fabric Mirroring** — Snowflake, Databricks, Cosmos DB, Azure SQL, Postgres mirrored into OneLake without copy. **Fabric Shortcuts** — point at S3, ADLS, Dataverse without copy. **Fabric Eventstreams** — streaming sources (Kafka, EventHub, IoT Hub) without copy. Productized broadest.
- **GCP BigQuery Omni** — federated queries against S3 and Azure Blob Storage directly from BigQuery. Strongest cross-cloud federation story. **BigLake** for unified access to data in Cloud Storage.
- **AWS Athena Federated Query + Lake Formation** — per-source connectors (Snowflake, MongoDB, Postgres, etc.). Capable but multi-service assembly required. **AWS Glue** for the catalog layer.
- Per-entity joinability at Gold (per-customer, per-VIN, per-policyholder, per-product) — the unlock that makes agent reasoning credible
- Vector store strategy (RAG adjacent): Azure AI Search integrated vector / AWS OpenSearch + Bedrock Knowledge Bases + Aurora pgvector / GCP Vertex AI Vector Search + AlloyDB pgvector. Cost and quality vary.
- Streaming-source architecture: Kafka / EventHub / Kinesis / Pub/Sub windowing, watermarking, late-arrival handling
- The honest comparison: Microsoft Fabric Mirroring is productized broadest for the most source types; GCP BigQuery Omni is the strongest cross-cloud reach; AWS Athena Federated Query is most assembly-required on this specific axis
- One disagreement: Reid argues BigQuery Omni is the strongest cross-cloud federation story on the market; Keven concedes the point but counters with Fabric's tighter governance integration on mirrored sources

**Step 2: Verify**

```bash
python -c "
import re
text = open('.../02-data-foundation-and-no-replication.md', encoding='utf-8').read()
words = len(text.split())
segments = len(re.findall(r'^\*\*(KEVEN|REID):\*\*', text, re.MULTILINE))
print(f'words: {words} | segments: {segments}')
assert 5800 < words < 6800
assert 60 < segments < 130

body = text.split('## Further reading')[0]
parts = body.split('---', 2)
dialog = parts[2] if len(parts) > 2 else body

# Forbidden / codenames same as Ep 1

# Specific products named
for p in ['Fabric', 'Mirroring', 'Shortcuts', 'OneLake', 'BigQuery Omni', 'BigLake', 'Lake Formation', 'Athena', 'Iceberg']:
    assert p in dialog, f'missing product mention: {p}'

# Principle 4 explicit
assert 'No Replication' in dialog or 'no replication' in dialog
print('OK')
"
```

**Step 3: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/02-data-foundation-and-no-replication.md
git commit -m "feat: Ep 2 — Data Foundation and the No-Replication Principle"
```

---

## Task 4: Episode 3 — Agent Runtime: Talking to Gold, Not SORs

**Files:**
- Create: `pc-cross-cloud-agentic/03-agent-runtime-talking-to-gold.md`

**Step 1: Write the script** (target ~5,800 words, ~30 min)

**Required content beats:**

- Cold open: an engineer mid-implementation realizing his agent is hitting SAP rate limits at peak hour because the agent is hammering the OLTP system directly. The MCP boundary discipline matters.
- The Gold-Tier-MCP-boundary principle in action: every agent tool call lands on Gold, never on a source system
- **Microsoft Agent Framework SDK + Azure AI Foundry Agent Service** — the SDK + the hosting plane. Tool registration. Reasoning loop. State persistence.
- **AWS Bedrock Agents** — action groups, knowledge bases, prompt engineering, model selection. Anthropic Claude family native on Bedrock.
- **GCP Vertex AI Agent Builder + Agent Engine** — Gemini-primary but multi-model. Agent Garden patterns.
- Model availability per runtime: GPT-4o / GPT-4.1 on Foundry primary; Claude 3.5/3.7/4.x on Bedrock primary, partner integration on Foundry/Vertex; Gemini on Vertex primary; Llama on all three; Mistral / Cohere on AWS/GCP primary
- Orchestration patterns: sequential chains, parallel decompositions, hierarchical sub-agents
- HITL design patterns deeper: gate placement (before-irreversible-action vs after-reasoning), interface design (operator sees what?), escalation paths (when does the agent ask?), feedback loops
- RAG vs fine-tuning vs distillation — the domain adaptation spectrum. Cheapest to most committed.
- MCP (Model Context Protocol) — the emerging standard for tool definitions. Tool catalog versioning. Scope per agent role.
- One disagreement: Reid argues Anthropic Claude is materially better on Bedrock than on Foundry today; Keven counters with OpenAI velocity on Foundry and the partner-model roadmap.

**Step 2: Verify**

```bash
python -c "
import re
text = open('.../03-agent-runtime-talking-to-gold.md', encoding='utf-8').read()
words = len(text.split())
segments = len(re.findall(r'^\*\*(KEVEN|REID):\*\*', text, re.MULTILINE))
print(f'words: {words} | segments: {segments}')
assert 5400 < words < 6300
assert 50 < segments < 110

body = text.split('## Further reading')[0]
parts = body.split('---', 2)
dialog = parts[2] if len(parts) > 2 else body

for p in ['Foundry', 'Bedrock', 'Vertex', 'Agent Framework', 'MCP', 'HITL']:
    assert p in dialog, f'missing: {p}'

print('OK')
"
```

**Step 3: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/03-agent-runtime-talking-to-gold.md
git commit -m "feat: Ep 3 — Agent Runtime: Talking to Gold, Not SORs"
```

---

## Task 5: Episode 4 — Governance, Identity, and Safety for Agentic AI

**Files:**
- Create: `pc-cross-cloud-agentic/04-governance-identity-and-safety.md`

**Step 1: Write the script** (target ~6,200 words, ~32 min)

**Required content beats:**

This is one of the longest episodes — three concepts woven together (governance, identity, safety). Walk each in sequence.

**Governance:**
- What's different about governing an agent vs governing a human or traditional ML pipeline
- Dynamic data access at reasoning time; high-velocity tool calls; cross-domain per-scenario Gold views
- **Microsoft Purview** — productized: catalog + lineage + access + sensitivity + DSPM-for-AI in one product
- **AWS Lake Formation + Macie + Audit Manager + GuardDuty** — multi-service assembly
- **GCP Dataplex + Sensitive Data Protection + Security Command Center** — closer to Purview than AWS, but Sensitive Data Protection is a separate product
- DSPM for AI specifically — the new productized capability; Microsoft is differentiated here

**Identity Continuity (Principle 3):**
- Agent identity (service principal / IAM role / GCP service account)
- Operator identity (human user)
- Source identity (the SAP / Salesforce / Snowflake principal the federation uses)
- Auditor identity (separate read-only audit principal)
- Identity propagation: through every tool call, into every audit row
- **Microsoft Entra ID** — single plane, broadest enterprise SaaS federation (M365 + SAP + Salesforce + Workday)
- **AWS IAM + IAM Identity Center + Cognito** — multi-service identity; assembly required
- **GCP Cloud IAM + Workload Identity Federation** — strongest cross-cloud federation primitive
- Honest assessment: Entra has broadest SaaS reach; GCP has cleanest cross-cloud federation

**Safety / Risk frameworks:**
- EU AI Act (in force 2025)
- NIST AI Risk Management Framework
- ISO/IEC 42001 — AI management systems
- Prompt injection attacks
- Data exfiltration via agent tool calls
- **Microsoft Azure AI Content Safety + Defender for Cloud AI** — content safety and posture management
- **AWS Bedrock Guardrails** — content filtering and topic restrictions
- **GCP Vertex AI Safety filters** — Responsible AI suite

**One disagreement:** Reid argues Workload Identity Federation makes cross-cloud agent identity portable in a way Entra can't match; Keven counters with the enterprise-SaaS federation reach.

**Step 2: Verify**

```bash
python -c "
import re
text = open('.../04-governance-identity-and-safety.md', encoding='utf-8').read()
words = len(text.split())
segments = len(re.findall(r'^\*\*(KEVEN|REID):\*\*', text, re.MULTILINE))
print(f'words: {words} | segments: {segments}')
assert 5800 < words < 6800
assert 60 < segments < 130

body = text.split('## Further reading')[0]
parts = body.split('---', 2)
dialog = parts[2] if len(parts) > 2 else body

# Key products across the three governance/identity/safety dimensions
for p in ['Purview', 'Lake Formation', 'Dataplex', 'Entra', 'Workload Identity Federation',
          'EU AI Act', 'NIST', 'ISO', 'Bedrock Guardrails', 'AI Content Safety']:
    assert p in dialog, f'missing: {p}'

# Three threads present
for thread in ['governance', 'identity', 'safety']:
    assert thread in dialog.lower(), f'missing thread: {thread}'

print('OK')
"
```

**Step 3: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/04-governance-identity-and-safety.md
git commit -m "feat: Ep 4 — Governance, Identity, and Safety for Agentic AI"
```

---

## Task 6: Episode 5 — Audit, Ledger, and Replay: The Trust Substrate

**Files:**
- Create: `pc-cross-cloud-agentic/05-audit-ledger-and-replay.md`

**Step 1: Write the script** (target ~6,200 words, ~32 min)

**Required content beats:**

- Cold open: an External Audit Reviewer at 7 AM opening the agent's overnight reasoning chain. The audit row is the product, not the by-product.
- Why agentic AI requires a different audit pattern than traditional ML: the reasoning chain is the artifact
- **"Audit row, not log line"** as the discipline
- The hash-chained audit row pattern — every agent decision = a structured row with decision context, agent identity, model version, tool calls invoked, data accessed, parent-row hash, output hash
- Cryptographic tamper evidence — modifying any row invalidates downstream rows
- **Replay-token validation** — External Audit Reviewer reproduces reasoning offline
- HITL gates as audit events — every approve/modify/reject is its own audit row
- Identity propagation INTO audit rows — every row carries agent, operator, source identities
- Lineage thread: audit row → Gold view → Silver canonical → Bronze reference → source system
- **Microsoft**: Foundry + Purview audit echo = productized reference architecture for the ledger pattern
- **AWS**: custom build — DynamoDB hash-chain table OR Amazon QLDB (note honestly: in maintenance mode, not the future path) OR OpenSearch append-only — bespoke
- **GCP**: custom build — BigQuery append-only audit tables with content-hash columns — bespoke
- Why this matters: regulated industries (HLS, FinServ, regulated Mfg), EU AI Act compliance, NIST AI RMF, board-level AI governance, External Audit Reviewer offline replay
- **Operational observability** (alongside compliance audit): prompt failure rates, tool-call latency, model-version drift detection, source-schema-drift surfacing — uses the same substrate
- One disagreement: Reid argues the ledger pattern is overengineered for most enterprise AI; Keven argues regulated-industry and board-level governance make it table stakes.

**Step 2: Verify**

```bash
python -c "
import re
text = open('.../05-audit-ledger-and-replay.md', encoding='utf-8').read()
words = len(text.split())
segments = len(re.findall(r'^\*\*(KEVEN|REID):\*\*', text, re.MULTILINE))
print(f'words: {words} | segments: {segments}')
assert 5800 < words < 6800
assert 60 < segments < 130

body = text.split('## Further reading')[0]
parts = body.split('---', 2)
dialog = parts[2] if len(parts) > 2 else body

for p in ['ledger', 'audit row', 'replay', 'hash chain', 'External Audit', 'HITL']:
    assert p in dialog or p.lower() in dialog.lower(), f'missing: {p}'

# Internal LEDGER all-caps should NOT appear
assert 'LEDGER' not in dialog, 'LEDGER all-caps on tape'

print('OK')
"
```

**Step 3: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/05-audit-ledger-and-replay.md
git commit -m "feat: Ep 5 — Audit, Ledger, and Replay: The Trust Substrate"
```

---

## Task 7: Episode 6 — FinOps for Agentic AI

**Files:**
- Create: `pc-cross-cloud-agentic/06-finops-for-agentic-ai.md`

**Step 1: Write the script** (target ~5,500 words, ~28 min — shorter, focused)

**Required content beats:**

- Cold open: a CFO meeting at quarter-end. The CFO opens with "explain to me why our AI bill is up 35% quarter-over-quarter." The seller without a FinOps story loses the conversation.
- The +20-40% QoQ AI consumption cost growth pattern across enterprises
- No cloud has productized "AI Cost Management" yet — Azure / AWS / GCP all handle compute and storage well but AI-consumption-specific cost analytics is custom-built at most enterprises today
- Cost sources covered:
  - Per-token model costs (GPT, Claude, Gemini, Llama priced differently per million tokens)
  - Copilot seat utilisation (M365 Copilot, GitHub Copilot, Power Platform AI Builder)
  - Agent runtime compute (Foundry / Bedrock / Vertex AI managed-service costs)
  - Vector store storage and query cost
  - Embedding API spend
  - Custom-model hosting (when models aren't on a managed API)
  - Federation-query compute (the cost of Principle #4 — pay-per-query vs pay-once-for-copy)
  - Audit-ledger storage (append-only = grows forever; cold-tier archival discipline required)
  - Bronze / Silver / Gold storage tier economics
- Cost management across clouds:
  - **Microsoft**: Azure Cost Management for OpenAI/Foundry + M365 Copilot Admin Center (seat utilisation) + Microsoft Cost Management for Azure OpenAI + Power BI for analytics
  - **AWS**: AWS Cost Explorer + Bedrock cost reporting + per-model pricing transparency + Cost & Usage Reports
  - **GCP**: Cloud Billing + Vertex AI cost reporting + per-model pricing
- **Model-mix optimization** — using cheap small models (GPT-4o-mini, Claude Haiku, Gemini Flash) where they suffice; expensive large models where they earn the cost. Per-use-case cost-per-outcome modeling.
- Idle Copilot seat reclamation
- Audit-ledger storage cost discipline — retention policies, sampling strategies for non-regulated rows, cold-tier archival
- The CFO conversation: per-use-case cost-per-outcome, ROI per agent
- One disagreement: Reid argues "FinOps for AI is the same as FinOps for cloud"; Keven counters that AI consumption has different cost dynamics (per-token, per-seat, model-mix) that traditional cloud FinOps doesn't address.

**Step 2: Verify**

```bash
python -c "
import re
text = open('.../06-finops-for-agentic-ai.md', encoding='utf-8').read()
words = len(text.split())
segments = len(re.findall(r'^\*\*(KEVEN|REID):\*\*', text, re.MULTILINE))
print(f'words: {words} | segments: {segments}')
assert 5100 < words < 6000
assert 45 < segments < 100

body = text.split('## Further reading')[0]
parts = body.split('---', 2)
dialog = parts[2] if len(parts) > 2 else body

for p in ['Copilot', 'token', 'Cost Management', 'FinOps', 'CFO']:
    assert p in dialog, f'missing: {p}'

# QoQ growth thesis
assert 'QoQ' in dialog or 'quarter-over-quarter' in dialog.lower()

print('OK')
"
```

**Step 3: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/06-finops-for-agentic-ai.md
git commit -m "feat: Ep 6 — FinOps for Agentic AI"
```

---

## Task 8: Episode 7 — Multi-Cloud Reality + Cloud + Model Portability

**Files:**
- Create: `pc-cross-cloud-agentic/07-multi-cloud-and-portability.md`

**Step 1: Write the script** (target ~5,800 words, ~30 min)

**Required content beats:**

- Cold open: a CTO architecture review meeting at a multi-national. Three clouds in play because three subsidiaries inherited different cloud commitments. Multi-cloud is the architectural reality, not the architectural choice.
- The Acceleration Framework is architecturally cloud-portable because all Five Principles are cloud-neutral
- Bronze lands anywhere. Silver canonical schemas travel. Gold per-scenario views travel. Agent runtime portable. Identity federates. Audit ledger composes. Models portable.
- **Multi-cloud is the natural endpoint of "no replication" when source systems span clouds** — the Acceleration Framework doesn't fight multi-cloud; it composes with it
- **Model Portability (Principle 5) deep dive:**
  - 18-month model-generation refresh cycles (GPT-4 → 4o → 4.1; Claude 3.5 → 3.7 → 4.x; Gemini 1.5 → 2.0)
  - Versioned prompts. Tool-call abstractions. Model-agnostic SDKs.
  - AWS Bedrock has the strongest multi-vendor model story (Claude native, Llama, Mistral, Cohere, Stability)
  - GCP Vertex AI Model Garden (Gemini, Claude, Llama)
  - Microsoft Foundry (OpenAI primary, Anthropic via partner integrations)
  - Why "locked to GPT-4" is a wave-1-only-asset risk
- What "primary cloud" actually means in practice (90%+ of agentic workloads land on one cloud per scenario)
- Cross-cloud egress economics — the real reason multi-cloud is rare at the agentic stack level
- Identity federation patterns: Entra B2B + Workload Identity Federation + AWS IAM federation
- Multi-cloud audit chain composition
- When cross-cloud composition is legitimate (regulatory data residency, source-resident gravity, multi-vendor model preference) vs theatre (architectural-elegance-for-its-own-sake)
- One disagreement: Keven argues multi-cloud at the agentic stack is rare; Reid argues data-residency-mandated multi-cloud is increasingly real.

**Step 2: Verify**

```bash
python -c "
import re
text = open('.../07-multi-cloud-and-portability.md', encoding='utf-8').read()
words = len(text.split())
segments = len(re.findall(r'^\*\*(KEVEN|REID):\*\*', text, re.MULTILINE))
print(f'words: {words} | segments: {segments}')
assert 5400 < words < 6300
assert 50 < segments < 110

body = text.split('## Further reading')[0]
parts = body.split('---', 2)
dialog = parts[2] if len(parts) > 2 else body

for p in ['Model Portability', 'multi-cloud', 'Model Garden', 'federation', 'Foundry', 'Bedrock', 'Vertex']:
    assert p in dialog or p.lower() in dialog.lower(), f'missing: {p}'

print('OK')
"
```

**Step 3: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/07-multi-cloud-and-portability.md
git commit -m "feat: Ep 7 — Multi-Cloud Reality + Cloud + Model Portability"
```

---

## Task 9: Episode 8 — The Seller's Playbook

**Files:**
- Create: `pc-cross-cloud-agentic/08-the-sellers-playbook.md`

**Step 1: Write the script** (target ~6,200 words, ~32 min)

**Required content beats:**

This is the practitioner closer. Every prior episode points here.

- Cold open: a Microsoft seller's Friday-afternoon prep for a Monday meeting with a new prospect. Three pieces of paper on the desk: the Acceleration Framework's Five Principles, the seller's six discovery openers, and the Independence cheat sheet. This is the working artefact.
- **The Acceleration Framework + the Five Principles as the architectural pitch** — cloud-neutral
- **Microsoft's productization advantage on each principle:**
  - Principle 1 (Gold-Tier-First): Fabric medallion native
  - Principle 2 (Governance/Audit/Ledger): Purview + DSPM-for-AI + ledger reference architecture productized
  - Principle 3 (Identity): Entra single plane + broadest SaaS federation
  - Principle 4 (No Replication): Fabric Mirroring + Shortcuts broadest productized
  - Principle 5 (Model Portability): Foundry model availability + Agent Framework SDK abstraction
- **Independence-minded framing** — recommend on technical and economic merits; no co-sell; two-contract model; no compensation flows from Microsoft to Deloitte for influencing client cloud choices
- **Five honest claims** Microsoft sellers can defend:
  1. Most productized DSPM-for-AI capability (Principle 2)
  2. Most productized hash-chained ledger pattern reference architecture (Principle 2)
  3. Broadest enterprise-SaaS identity federation surface (Principle 3)
  4. Broadest source-mirroring productization (Principle 4)
  5. Operating on technical merits, not partner motion (Independence)
- **Four overclaims to avoid:**
  1. "Microsoft's agent runtime is better" (parity — they're all production-grade)
  2. "Microsoft has more models" (false — Bedrock has the multi-vendor lead)
  3. "Microsoft is more NVIDIA-aligned" (parity — NVIDIA runs equally on all three)
  4. "Microsoft is the only one with audit trails" (false — all three can build the pattern; Microsoft has it productized)
- **Six pushback-handling talking points** — verbatim-quotable:
  1. "We're AWS-primary"
  2. "We're GCP-primary"
  3. "Deloitte should be cloud-agnostic"
  4. "Microsoft compensation is influencing the recommendation"
  5. "We want portability later" (model and cloud)
  6. "We don't want our data replicated into a new lake"
- **When to recommend NOT Microsoft** (legitimate scenarios):
  - AWS-resident data gravity at scale
  - GCP-strategic posture at the enterprise architecture office
  - Multi-cloud regulatory mandate
  - Anthropic-on-Bedrock or Gemini-on-Vertex model-family preferences
- **The seller's six discovery openers** (one per principle + FinOps):
  1. *"Are your agents pointing at SORs or your data warehouse directly?"* (Principle 1)
  2. *"How are you handling AI governance and audit for agent decisions today?"* (Principle 2)
  3. *"What identity does your agent run as, and how does that identity propagate to source access?"* (Principle 3)
  4. *"Are you replicating data into a new lake to make AI work, or are your sources staying untouched?"* (Principle 4)
  5. *"How model-portable is your agent design — could you swap GPT for Claude tomorrow if you needed to?"* (Principle 5)
  6. *"What's your AI consumption cost trajectory looking like quarter-over-quarter?"* (FinOps)
- **Wave sizing / 90-day pilot path:** what makes a good Wave 1 (operational, contained, measurable); what kills agentic projects (scope creep, ungoverned model proliferation, cost shock)
- **Funding programs** (Independence-clean handling): Microsoft BVA / ECIF / Azure Credits; AWS ProServe credits / MAP; GCP Cloud Innovation Credits. Frame as discovery-funding for the client's benefit — never as compensation flowing to Deloitte for influencing cloud choice.
- **Closing posture:** the Microsoft platform earns the recommendation on merits. The Acceleration Framework + the Five Principles makes that recommendation defensible across any cloud reality.
- One disagreement: Reid argues sellers will be tempted to skip the cross-cloud honest comparison and just pitch Microsoft; Keven argues short-term skipping wins one deal but loses the relationship with the Deloitte AI team and with sophisticated client architects.

**Step 2: Verify**

```bash
python -c "
import re
text = open('.../08-the-sellers-playbook.md', encoding='utf-8').read()
words = len(text.split())
segments = len(re.findall(r'^\*\*(KEVEN|REID):\*\*', text, re.MULTILINE))
print(f'words: {words} | segments: {segments}')
assert 5800 < words < 6800
assert 60 < segments < 130

body = text.split('## Further reading')[0]
parts = body.split('---', 2)
dialog = parts[2] if len(parts) > 2 else body

# Six discovery openers
for opener_keyword in ['pointing at SORs', 'governance and audit', 'identity does your agent',
                       'replicating data', 'model-portable', 'consumption cost']:
    assert opener_keyword in dialog, f'missing discovery opener keyword: {opener_keyword}'

# Independence framing
assert 'Independence' in dialog or 'two-contract' in dialog or 'two contract' in dialog

print('OK')
"
```

**Step 3: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/08-the-sellers-playbook.md
git commit -m "feat: Ep 8 — The Seller's Playbook"
```

---

## Task 10: Build audio synthesis script

**Files:**
- Create: `pc-cross-cloud-agentic/_build_audio.py`

**Step 1: Copy `pc-toyota-zero-day-warranty/_build_audio.py` as template**

```bash
cp "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty/_build_audio.py" \
   "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic/_build_audio.py"
```

**Step 2: Apply edits**

Edit 1 — voice constants (use the audition winner; default DAVIS):

```python
VOICE_KEVEN = "en-US-AndrewNeural"   # Trilogy continuity host
VOICE_REID  = "en-US-DavisNeural"    # Cross-cloud principal architect — Reid
```

Edit 2 — `DIALOGUE_RE`:

```python
DIALOGUE_RE = re.compile(
    r"^\*\*(KEVEN|REID):\*\*\s*([\s\S]*?)"
    r"(?=^\*\*(?:KEVEN|REID):\*\*|^##|^---|\Z)",
    re.MULTILINE,
)
```

Edit 3 — `EPISODES` list (8 entries):

```python
EPISODES = [
    "01-the-agentic-stack-and-five-principles.md",
    "02-data-foundation-and-no-replication.md",
    "03-agent-runtime-talking-to-gold.md",
    "04-governance-identity-and-safety.md",
    "05-audit-ledger-and-replay.md",
    "06-finops-for-agentic-ai.md",
    "07-multi-cloud-and-portability.md",
    "08-the-sellers-playbook.md",
]
```

Edit 4 — speaker-to-voice dispatch in `synth_episode()`:

```python
if speaker == "KEVEN":
    voice, rate, pitch = VOICE_KEVEN, RATE_KEVEN, PITCH_KEVEN
else:
    voice, rate, pitch = VOICE_REID, RATE_REID, PITCH_REID
```

Add the rate/pitch constants (`RATE_REID = "-2%"`, `PITCH_REID = "+0Hz"`).

Edit 5 — docstring header updated for this podcast (8th pairing; Andrew + Davis; cross-cloud focus).

**Step 3: Smoke test — parse Ep 1, do NOT synthesize**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python -c "
from _build_audio import parse_script, EPISODES
for ep in EPISODES:
    txt = open(ep, encoding='utf-8').read()
    segs = parse_script(txt)
    speakers = set(s[0] for s in segs)
    print(f'  {ep}: {len(segs)} segments, speakers={speakers}')
    assert speakers == {'KEVEN', 'REID'}, f'unexpected speakers in {ep}: {speakers}'
print('OK')
"
```

Expected: `OK` with both `KEVEN` and `REID` for each episode.

**Step 4: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/_build_audio.py
git commit -m "feat: audio build script (Andrew + Davis voice pair)"
```

---

## Task 11: Build music sting builder + generate stings

**Files:**
- Create: `pc-cross-cloud-agentic/_build_music.py`

**Step 1: Copy `pc-toyota-zero-day-warranty/_build_music.py` as starting point**

```bash
cp "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty/_build_music.py" \
   "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic/_build_music.py"
```

**Step 2: Edit to use C-major boardroom register**

Replace the docstring header. Replace the musical notes section with a C-major-based progression (different from DTNA's G-major and Disney's bell-tree):

```python
# Musical notes — C major / G major register (boardroom feel)
C3 = 130.81
G3 = 196.00
C4 = 261.63
E4 = 329.63
G4 = 392.00
C5 = 523.25
E5 = 659.25
G5 = 783.99
```

Update opening sting notes to ascending C-G-C arpeggio (boardroom-clean):

```python
notes = [
    (C3, 0.00, 4.5),   # low root — grounded
    (G3, 0.40, 4.0),   # fifth above
    (C4, 0.80, 4.0),   # octave
    (E4, 1.30, 3.5),   # major third — adds warmth (C major chord)
]
```

Update closing sting to sustained C-major chord:

```python
notes = [
    (C3, 0.00, 5.5),
    (G3, 0.10, 5.5),
    (C4, 0.20, 5.5),
    (E4, 0.50, 5.3),
    (G4, 1.20, 4.5),
]
```

The horn-like timbre envelope from DTNA can stay — it gives the boardroom warmth.

**Step 3: Run the build**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python _build_music.py
```

Expected:
```
Building opening_sting.mp3 ...
  -> opening_sting.mp3 (xx KB)
Building closing_sting.mp3 ...
  -> closing_sting.mp3 (xx KB)
Done.
```

**Step 4: Verify durations**

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 opening_sting.mp3
# Expected: 4.9 - 5.1
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 closing_sting.mp3
# Expected: 5.9 - 6.1
```

**Step 5: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/_build_music.py docs/podcast/pc-cross-cloud-agentic/opening_sting.mp3 docs/podcast/pc-cross-cloud-agentic/closing_sting.mp3
git commit -m "feat: C-major boardroom music stings for Cross-Cloud Agentic podcast"
```

---

## Task 12: Build music sting applier

**Files:**
- Create: `pc-cross-cloud-agentic/_apply_music.py`

**Step 1: Copy `pc-toyota-zero-day-warranty/_apply_music.py`**

```bash
cp "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-toyota-zero-day-warranty/_apply_music.py" \
   "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic/_apply_music.py"
```

**Step 2: Edit `EPISODES` list (8 entries)**

```python
EPISODES = [
    "01-the-agentic-stack-and-five-principles.mp3",
    "02-data-foundation-and-no-replication.mp3",
    "03-agent-runtime-talking-to-gold.mp3",
    "04-governance-identity-and-safety.mp3",
    "05-audit-ledger-and-replay.mp3",
    "06-finops-for-agentic-ai.mp3",
    "07-multi-cloud-and-portability.mp3",
    "08-the-sellers-playbook.mp3",
]
```

Update the module docstring.

**Step 3: Lint check (no audio dir yet)**

```bash
python -c "from _apply_music import EPISODES; print('parsed OK:', len(EPISODES), 'episodes')"
# Expected: parsed OK: 8 episodes
```

**Step 4: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/_apply_music.py
git commit -m "feat: music sting applier for Cross-Cloud Agentic podcast"
```

---

## Task 13: Generate all 8 episode MP3s

**Files:**
- Create: `pc-cross-cloud-agentic/audio/01-*.mp3` through `audio/08-*.mp3`

**Step 1: Run the audio build in background**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python _build_audio.py --all
```

Estimated 45-90 minutes wall-clock for 8 episodes via edge-tts (depends on segment count and rate limits). Use background execution and wait for notification.

**Step 2: Verify all 8 MP3s exist and are in target duration band**

```bash
cd audio
for ep in 01-the-agentic-stack-and-five-principles \
          02-data-foundation-and-no-replication \
          03-agent-runtime-talking-to-gold \
          04-governance-identity-and-safety \
          05-audit-ledger-and-replay \
          06-finops-for-agentic-ai \
          07-multi-cloud-and-portability \
          08-the-sellers-playbook; do
  dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "${ep}.mp3" 2>/dev/null)
  printf "  %s: %ss\n" "$ep" "$dur"
done
```

Expected: each duration between 1500-2400 seconds (25-40 min depending on episode length).

**Step 3: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/audio/
git commit -m "feat: generate Cross-Cloud Agentic Eps 1-8 audio (edge-tts Andrew + Davis)"
```

---

## Task 14: Apply music stings to all 8 episodes

**Files:**
- Modify in place: `audio/01-*.mp3` through `audio/08-*.mp3`
- Create backups: `audio/_originals/01-*.mp3` through `audio/_originals/08-*.mp3`

**Step 1: Run the applier**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python _apply_music.py
```

Expected output: 8 lines, one per episode, showing duration after stings applied.

**Step 2: Verify idempotence**

```bash
python _apply_music.py
# Expected: same durations as step 1; no errors
```

**Step 3: Verify backups created**

```bash
ls audio/_originals/
# Expected: 8 backed-up MP3 files (stingless versions)
```

**Step 4: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/audio/
git commit -m "feat: apply music stings to all 8 Cross-Cloud Agentic episodes"
```

---

## Task 15: Audio README

**Files:**
- Create: `pc-cross-cloud-agentic/audio/README.md`

**Step 1: Write audio README** matching the structure of `pc-toyota-zero-day-warranty/audio/README.md`.

**Required sections:**
1. Title + one-line description
2. Episode table with actual durations and sizes (filled from ffprobe output)
3. Voice cast table — Keven (Andrew) + Reid (audition winner); 8th distinct pairing in the family
4. Music disclosure — royalty-free C-major boardroom register, ffmpeg-synthesised
5. Format spec (24kHz mono, 48kbps, 350ms inter-turn pause, 300ms sting-to-voice silence)
6. Regeneration instructions (`_build_audio.py` / `_build_music.py` / `_apply_music.py` order)
7. Folder structure diagram
8. Series content overview — 8 episodes with one-line summaries each
9. Notes:
   - Audience disclosure (Microsoft Target Platform Sellers; safe for Deloitte AI team)
   - Independence framing (no co-sell, two-contract model)
   - The Five Architectural Principles named
   - Generic positioning (no client specified)
   - Companion podcasts (7 prior podcasts in the family)

**Step 2: Verify**

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic/audio"
wc -w README.md
# Expected: 800-1300 words
```

**Step 3: Commit**

```bash
git add docs/podcast/pc-cross-cloud-agentic/audio/README.md
git commit -m "docs: audio README for Cross-Cloud Agentic podcast"
```

---

## Final verification

After Task 15:

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
ls -la
# Expected:
#   README.md, 00-show-bible-and-format.md
#   01..08 .md scripts
#   _voice_audition.py, _build_audio.py, _build_music.py, _apply_music.py
#   opening_sting.mp3, closing_sting.mp3
#   audio/ (folder with 8 final MP3s + _originals/ + README.md + _auditions/)
```

```bash
wc -w 0*.md
# Expected: each episode in 5,400-6,800 word range
# Total ~47,000-48,000 words
```

```bash
git log --oneline | head -20
# Expected: 15+ commits matching the task names above
```

---

## Cross-task verification — series-level checks

Run these once after Task 9 (all scripts written), before audio generation.

### Forbidden vocabulary scan

```bash
cd "C:/Stage/Clients/Industries/APEX/docs/podcast/pc-cross-cloud-agentic"
python -c "
import re
forbidden = ['co-sell', 'alliance', 'strategic partnership', 'channel partner', 'our partnership with Microsoft']
for i, ep in enumerate(['01-the-agentic-stack-and-five-principles', '02-data-foundation-and-no-replication',
                        '03-agent-runtime-talking-to-gold', '04-governance-identity-and-safety',
                        '05-audit-ledger-and-replay', '06-finops-for-agentic-ai',
                        '07-multi-cloud-and-portability', '08-the-sellers-playbook'], 1):
    text = open(f'{ep}.md', encoding='utf-8').read()
    body = text.split('## Further reading')[0]
    parts = body.split('---', 2)
    dialog = parts[2] if len(parts) > 2 else body
    for t in forbidden:
        assert t.lower() not in dialog.lower(), f'Ep {i}: forbidden term in dialog: {t}'
print('Forbidden-vocab scan: OK across all 8 episodes')
"
```

### Internal-codename scan (should be absent from dialog)

```bash
python -c "
codes = ['APEX', 'ORCH-01', 'BRML', 'CVML', 'QEML', 'AAML', 'SB06', 'AXLE Practice']
for i, ep in enumerate(['01-the-agentic-stack-and-five-principles', '02-data-foundation-and-no-replication',
                        '03-agent-runtime-talking-to-gold', '04-governance-identity-and-safety',
                        '05-audit-ledger-and-replay', '06-finops-for-agentic-ai',
                        '07-multi-cloud-and-portability', '08-the-sellers-playbook'], 1):
    text = open(f'{ep}.md', encoding='utf-8').read()
    body = text.split('## Further reading')[0]
    parts = body.split('---', 2)
    dialog = parts[2] if len(parts) > 2 else body
    for c in codes:
        assert c not in dialog, f'Ep {i}: internal codename on tape: {c}'
print('Internal-codename scan: OK across all 8 episodes')
"
```

### Cloud-balance scan (each comparison episode names all three)

```bash
python -c "
clouds = {'Microsoft': ['Microsoft', 'Azure', 'Fabric', 'Foundry', 'Purview', 'Entra'],
          'AWS': ['AWS', 'Amazon', 'Bedrock', 'Lake Formation'],
          'GCP': ['GCP', 'Google Cloud', 'Vertex', 'BigQuery', 'Dataplex']}
# Episodes 2, 3, 4, 5, 6, 7 are comparison episodes; should mention each cloud
for ep_id in ['02-data-foundation-and-no-replication', '03-agent-runtime-talking-to-gold',
              '04-governance-identity-and-safety', '05-audit-ledger-and-replay',
              '06-finops-for-agentic-ai', '07-multi-cloud-and-portability']:
    text = open(f'{ep_id}.md', encoding='utf-8').read()
    body = text.split('## Further reading')[0]
    parts = body.split('---', 2)
    dialog = parts[2] if len(parts) > 2 else body
    for cloud, keywords in clouds.items():
        found = any(k in dialog for k in keywords)
        assert found, f'{ep_id}: missing all keywords for {cloud}'
print('Cloud-balance scan: OK across the 6 comparison episodes')
"
```

---

## Notes for the executor

- **Order matters.** Task 0 (audition) BEFORE Tasks 2-9 (episode scripts). Tasks 2-9 BEFORE Task 10 (audio script). Task 10 before Task 13 (audio gen). Task 13 before Task 14 (sting application). Task 14 before Task 15 (audio README — needs real durations).
- **Tasks 2-9 are 8 independent content-writing tasks.** Per the subagent-driven-development skill's "no parallel implementation subagents" rule, dispatch them sequentially. If running solo (no subagent), each ~5,500-6,200 word script will take 10-20 min of focused writing.
- **Task 13 is long-running** (45-90 min via edge-tts). Use background execution; do not poll.
- **Idempotence:** Tasks 11, 13, 14 are idempotent — re-running them is safe.
- **No external network needed** for music sting build (Task 11) — pure ffmpeg synthesis.
- **edge-tts (Task 13) does need network** to call Microsoft Edge Neural TTS endpoints.
- **Reference the design doc** `docs/plans/2026-05-14-cross-cloud-agentic-podcast-design.md` for any content question.
- **Reference prior podcast** `pc-toyota-zero-day-warranty/` for the audio/music script copy pattern.
- **Reference the Toyota Internal Cloud Comparison doc** (`Automotive/Toyota/01_account/Internal_Cloud_Comparison_ControlPlane_ZeroDayWarranty.md`) for the technical substrate on the cross-cloud comparison — strip out Toyota specifics; keep the architectural analysis.
- **DRY rule:** the audio/music scripts copy from `pc-toyota-zero-day-warranty/` — do not reinvent.
- **YAGNI rule:** no Excel companion needed; no APEX-Scenario-Chains.xlsx update needed (this podcast teaches the framework, not specific scenarios).
- **Audition rejection path:** if Davis sounds synthetic, retry with Brandon → Jason → re-audition with 4 more candidates before commit.

---

**End of plan.** Total tasks: 15 (Task 0 = audition, Tasks 1-9 = content, Tasks 10-12 = audio infrastructure, Tasks 13-15 = audio generation + README). Estimated effort: 16-24 hours for scripts (Tasks 2-9) + 45-90 min audio gen (Task 13) + ~30 min everything else.
