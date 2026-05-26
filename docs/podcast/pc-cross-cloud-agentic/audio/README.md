# The Cross-Cloud Agentic Podcast · Audio Files

Eight MP3 episodes — an Independence-minded guide for Microsoft Target Platform Sellers on positioning agentic AI across Microsoft, AWS, and Google Cloud. Each episode is wrapped with a royalty-free opening and closing music sting in a C-major boardroom register (see *Music* section below).

Voices via **Microsoft Edge Neural TTS** (`edge-tts`). Concatenated with **ffmpeg**.

## Episodes

| # | File | Duration | Size | Source script |
|---|---|---|---|---|
| 01 | `01-the-agentic-stack-and-five-principles.mp3` | **34:08** | 11.7 MB | `01-the-agentic-stack-and-five-principles.md` |
| 02 | `02-data-foundation-and-no-replication.mp3` | **39:14** | 13.5 MB | `02-data-foundation-and-no-replication.md` |
| 03 | `03-agent-runtime-talking-to-gold.mp3` | **37:20** | 12.8 MB | `03-agent-runtime-talking-to-gold.md` |
| 04 | `04-governance-identity-and-safety.mp3` | **45:36** | 15.7 MB | `04-governance-identity-and-safety.md` |
| 05 | `05-audit-ledger-and-replay.mp3` | **42:17** | 14.5 MB | `05-audit-ledger-and-replay.md` |
| 06 | `06-finops-for-agentic-ai.mp3` | **38:02** | 13.1 MB | `06-finops-for-agentic-ai.md` |
| 07 | `07-multi-cloud-and-portability.mp3` | **41:37** | 14.3 MB | `07-multi-cloud-and-portability.md` |
| 08 | `08-the-sellers-playbook.mp3` | **37:02** | 12.7 MB | `08-the-sellers-playbook.md` |
| | **SERIES TOTAL** | **5 h 15 min** | **108.3 MB** | |

Each episode runtime above includes the 5-second opening sting + the 6-second closing sting + 0.6s of silence between stings and voice. Spoken-content runtime is approximately 11.6 seconds shorter per episode.

The runtime came in longer than the original 28-32-minute design target because the episode scripts ran ~6,100 words each (the cross-cloud comparison content is dense) and edge-tts reads slightly slower than the conversational-pace estimate. The content is complete and intact; the longer runtime is a function of voice cadence and content density, not bloat. Episode 4 (Governance, Identity, Safety) is the longest at 45:36 because it weaves three substantial topics.

## Voice cast

| Host | Voice (edge-tts) | Personality cue |
|---|---|---|
| **Keven** *(the Microsoft platform practitioner)* | `en-US-AndrewNeural` | Warm · Confident · Trilogy continuity host · 22+ years on the Microsoft platform |
| **Reid** *(the cross-cloud principal architect)* | `en-US-AndrewMultilingualNeural` | Technical · architectural · has built production agentic stacks on Microsoft Azure, AWS Bedrock, AND GCP Vertex AI · the cross-cloud honesty enforcer |

This is the **eighth distinct voice pairing** in the APEX podcast family:

| Podcast | Pairing |
|---|---|
| Sellers | Andrew + Brian (boardroom) |
| Services v2 | Andrew + Emma (delivery team) |
| Deployment | Andrew + Ava (war room) |
| Disney Account | Andrew + Emma Multilingual (account team) |
| Disney Studios | Andrew + Ava Multilingual (Studios account team) |
| DTNA | Andrew + Brian Multilingual (industrial account) |
| Toyota Zero Day Warranty | Andrew + Michelle (agentic scenario) |
| **Cross-Cloud Agentic (this)** | **Andrew + Andrew Multilingual** (Microsoft sellers) |

### Note on the two-Andrew pairing

Both voices are Andrew variants — `AndrewNeural` for Keven and `AndrewMultilingualNeural` for Reid. The edge-tts en-US male voice catalog is small, and the Multilingual tier (the natural-quality generation matching Andrew) has only four voices, three of which were already used in prior podcasts. Andrew Multilingual was selected after a three-candidate audition (Andrew Multilingual, Brian Multilingual, Steffan).

The two voices are differentiated three ways:
1. **Rate/pitch tuning** — Reid runs at `-3%` rate and `-2Hz` pitch (the principal-architect-deliberate register) vs Keven's `+0%` / `+0Hz`.
2. **Vocabulary** — Keven references Microsoft platform tenure; Reid references "I have built this on Bedrock and Vertex AI."
3. **Sentence shape** — Keven uses framing prompts ("Set up X"); Reid uses direct architectural pushback ("I want to push back on that").

## Music — royalty-free, C-major boardroom register

Each episode begins with a **5-second opening sting** and ends with a **6-second closing sting** synthesised entirely from scratch via ffmpeg additive synthesis. The Cross-Cloud Agentic stings are in a **C-major boardroom register** — clean, professional, executive-briefing-room feel. Distinct from the DTNA/Toyota industrial G-major register and the Disney bell-tree register.

- **Opening sting** — ascending C3-G3-C4-E4 fanfare · major-third warmth · warm horn-like timbre · slight echo
- **Closing sting** — sustained C-major chord with low fundamental and high-fifth (G5) sparkle · gradual resolution

### Explicit disclosure

- The stings are **not** derived from, and do not quote, any copyrighted composition — Microsoft-related, AWS-related, GCP-related, or otherwise.
- They were generated programmatically by `_build_music.py` using only ffmpeg's `sine` lavfi source and standard filters (`afade`, `aecho`, `amix`, `volume`). No sample libraries, no external audio assets.
- Each podcast in the APEX family has its own sting key and register so a listener can identify the podcast from the sting alone.

## Format

- **Codec:** MP3 (LAME, libmp3lame)
- **Bitrate:** 48 kbps
- **Sample rate:** 24 kHz
- **Channels:** mono
- **Inter-turn pause:** 350 ms
- **Sting-to-voice silence:** 300 ms

Standard podcast-grade encoding. Identical format to the seven prior APEX podcasts for tooling consistency.

## How to regenerate

If episode scripts change:

```bash
cd C:\Stage\Clients\Industries\APEX\docs\podcast\pc-cross-cloud-agentic

# Regenerate voice audio for one episode
python _build_audio.py 04-governance-identity-and-safety.md

# Or all eight
python _build_audio.py --all

# Then re-wrap with music stings
python _apply_music.py
```

If a different music sting is preferred:

```bash
# Replace opening_sting.mp3 and/or closing_sting.mp3 with the preferred files
# (24kHz mono MP3 recommended)

# Then re-wrap all episodes from the unstinged originals
python _apply_music.py
```

The `_apply_music.py` script keeps stingless backups in `audio/_originals/` so the wrap operation is reversible and idempotent.

## Structure of the audio folder

```
audio/
├── 01-the-agentic-stack-and-five-principles.mp3   ← episode with stings applied
├── 02-data-foundation-and-no-replication.mp3
├── 03-agent-runtime-talking-to-gold.mp3
├── 04-governance-identity-and-safety.mp3
├── 05-audit-ledger-and-replay.mp3
├── 06-finops-for-agentic-ai.mp3
├── 07-multi-cloud-and-portability.mp3
├── 08-the-sellers-playbook.mp3
├── _originals/                                    ← stingless backups (do not edit)
│   └── (8 stingless episode MP3s)
├── _auditions/                                    ← voice audition samples (Reid candidates)
└── README.md
```

## Series content overview

Eight episodes for Microsoft Target Platform Sellers — how to win agentic AI work across Microsoft, AWS, and GCP without overclaiming:

- **Ep 1 — The Agentic Stack + The Five Principles** · wrong-way / right-way · the four-layer stack + identity · the Five Architectural Principles named · the 2024-2026 inflection
- **Ep 2 — Data Foundation + The No-Replication Principle** · medallion · Silver canonical, Gold composed · Fabric Mirroring / BigQuery Omni / Athena Federated Query · streaming · vector stores
- **Ep 3 — Agent Runtime: Talking to Gold, Not SORs** · the MCP boundary discipline · Foundry / Bedrock / Vertex AI · model availability · HITL patterns · RAG vs fine-tuning vs distillation
- **Ep 4 — Governance, Identity, and Safety for Agentic AI** · Purview / Lake Formation+Macie / Dataplex · DSPM for AI · Entra / IAM federation / Workload Identity Federation · EU AI Act / NIST AI RMF / ISO 42001 · cloud guardrails
- **Ep 5 — Audit, Ledger, and Replay: The Trust Substrate** · audit-row-not-log-line · hash-chained ledger · replay-token validation · HITL gates as audit events · the ledger pattern productized on Microsoft, assembled on AWS and GCP · operational observability
- **Ep 6 — FinOps for Agentic AI** · the +20-40% QoQ cost growth · tokens / Copilot seats / agent runtime / vector store / audit-ledger storage / federation-query compute · model-mix optimisation · the CFO conversation
- **Ep 7 — Multi-Cloud Reality + Cloud + Model Portability** · the Acceleration Framework's cloud portability · what "primary cloud" actually means · cross-cloud egress economics · the 18-month model-generation refresh · when multi-cloud is legitimate vs theatre
- **Ep 8 — The Seller's Playbook** · five honest claims · four overclaims to avoid · six pushback-handling talking points · when to recommend NOT Microsoft · the six discovery openers · Wave sizing · funding programs

## The Five Architectural Principles

The series teaches a vendor-neutral architectural framework — referred to on tape as *the Acceleration Framework*:

1. **Gold-Tier-First** — agents talk to a purpose-built Gold Tier shaped for reasoning, never directly to SORs or data warehouses
2. **Governance + Audit + Ledger as Trust Substrate** — DSPM-for-AI policy + hash-chained audit-row-per-step + replay-token validation
3. **Identity Continuity** — agent / operator / source / auditor identity all distinct but interlinked
4. **No Replication — Sources Stay Untouched** — virtualization / mirroring / shortcuts / federation; SORs serve OLTP, DWs serve BI, streams stay live
5. **Model Portability** — agent design portable across GPT / Claude / Gemini / Llama generations

## Notes

- **Audience.** Microsoft Target Platform Sellers (DMTSP). Safe for Deloitte AI team listeners — the series honestly identifies where AWS and GCP have parity or advantage. **Generic — no specific client is named on tape.** Reference clients are archetypes only ("a global retailer," "a regulated bank," "a hyperscale media company").
- **Independence from Microsoft.** The series operates under Independence: recommend on technical and economic merits; two-contract model (three contracts when NVIDIA is in scope); no co-sell; no compensation flows from platform vendors to Deloitte for influencing client cloud choices. The forbidden vocabulary of vendor-aligned selling never appears on tape.
- **The Acceleration Framework is taught generically.** Internal codenames are never spoken — the framework name on tape is descriptive, not branded.
- **Cross-cloud honesty.** Reid (the co-host) is the cross-cloud honesty enforcer. When Microsoft genuinely is not differentiated — agent runtime parity, model availability where AWS Bedrock leads, NVIDIA platform-neutrality — the series says so. This is the structural seller-discipline lesson.
- **No fabricated metrics.** Cost-growth patterns, market percentages, and model pricing are referenced in industry-analyst spirit (Gartner / Forrester / IDC) or as approximate public pricing — never as fabricated client-specific figures.
- **Companion podcasts in this folder family** — `../pc-sellersguide/` (10 episodes · framework-wide selling) · `../pc-servicesguide/` (12 episodes · framework-wide architecture) · `../pc-deploymentguide/` (6 episodes · framework-wide operations) · `../pc-disney-account/` (6 episodes) · `../pc-disney-studios/` (5 episodes) · `../pc-dtna-account/` (5 episodes) · `../pc-toyota-zero-day-warranty/` (5 episodes + summary).
