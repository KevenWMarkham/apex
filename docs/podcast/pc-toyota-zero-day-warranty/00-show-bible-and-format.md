# Show Bible · The Zero Day Warranty Podcast

Content rules for the Toyota Zero Day Warranty podcast. Adds to (does not replace) the Trilogy, Disney, and DTNA show bibles. The defining constraint: **the audio is dual-audience**. Account Team members listen to prepare; a Toyota listener may also hear it cold. The rules hold that distinction in every line.

---

## 1. What makes this podcast different

| Dimension | Trilogy | Disney / DTNA / Studios | Toyota Zero Day Warranty |
|---|---|---|---|
| **Audience** | Framework-wide | Account Team only | **Account Team AND Toyota-shareable** |
| **Industry** | All seven Practices | TMT-MED · AXLE · TMT-MED | AXLE — Toyota Motor North America specifically |
| **Voice cast** | Various | Various | Keven (Andrew) + Mia (Michelle) — seventh distinct pairing |
| **Distinctive content** | Framework | Account-specific plays | The single Zero Day Warranty scenario, five episodes deep |
| **Internal-language guard** | Standard | Standard | **Hard line — internal codenames never on tape** |

---

## 2. The conversational design rules

All rules from prior show bibles apply:

- **No chapter or section number citations in dialogue.** Hosts know the framework.
- **Stair-step pedagogy.** Foundation laid before built upon. No concept used in episode N+1 that was not introduced in episode N.
- **Cold-open scenes** open every episode — 3-5 minutes of lived experience (a warranty cluster on a Monday morning, a quality engineer pulling spreadsheets, a connected-vehicle dashboard lighting up). Not abstract framing.
- **One concept developed fully (4-6 min) before transitioning.** No topic-switching.
- **Real disagreement between hosts** every episode — Keven and Mia have different priors. Mia has stood on the line; Keven has stood at the platform whiteboard. The disagreement is real, never performative.
- **Quote-and-react moments from primary sources** — Toyota public statements, TPS canon (Ohno, Liker), Microsoft and NVIDIA technical documentation. Always with attribution.
- **What-to-carry-forward closers.** 1-2 minutes naming what the listener should take into their next conversation.
- **Further Reading section** in each `.md` — primary sources only.
- **No announced segments.** Structure is felt, not narrated.

---

## 3. Toyota-specific style additions

### Rule 1 · TPS terminology accurately and respectfully

Toyota invented modern manufacturing discipline. Hosts use TPS vocabulary because it is the right vocabulary — not because it is fashionable.

- **Jidoka** — autonomation; the line stops when a quality problem is detected so the problem is fixed at source. Explained inline first time, used precisely thereafter.
- **Andon** — the cord, the light, the signal. A worker pulling the andon is doing what the system asks. The Zero Day Warranty agent is conceptually an andon for the field — a signal raised in minutes not weeks.
- **Kaizen** — continuous improvement, owned by the operator and the team closest to the work.
- **Genchi Genbutsu** — go and see. The opposite of analysing from a desk.
- **Hansei** — reflection. After a defect, after a recall — what do we learn.

If a host can't explain a TPS term in a sentence to a non-Toyota listener, the term doesn't go in. **Never decorative.**

### Rule 2 · Operator dignity is non-negotiable

Toyota's TPS culture treats the operator as the heart of quality. The Zero Day Warranty agent **augments** that — it does not replace it:

- The agent takes the **manual reconciliation toil** off six teams, returning their time to higher-judgement work — root-cause hypothesis testing, supplier conversations, design feedback.
- The agent **never makes a chargeback decision on its own.** It produces an evidence package; a human signs.
- Operator-cohort patterns in the data surface *training, tooling, and station ergonomics* questions — never blame.

Any line that diminishes the operator gets cut.

### Rule 3 · Audit-ready framing is non-negotiable

Every decision the agent makes is an audit row. The hash chain is real, the replay token is real, the Microsoft Purview audit echo is real. Not a slogan — the architectural reason Toyota Quality and Toyota Legal can adopt an agent in the warranty path at all. Episodes 3 and 5 walk it explicitly; Episodes 1, 2, and 4 reference it without belabouring.

### Rule 4 · Independence from Microsoft, stated explicitly

The rule that protects everything. Spoken on tape:

- **Deloitte recommends.** Microsoft is the platform. Toyota contracts with Microsoft directly.
- **Two contracts. Microsoft licensing on Microsoft paper. Deloitte services on Deloitte paper.** Said exactly that way in Episode 1 and again in Episode 5.
- **Words that never appear on tape: "co-sell" · "alliance" · "strategic partnership" · "partner channel" · "channel partner".**
- **No compensation flows from Microsoft to Deloitte** for influencing Toyota's platform decisions. Said at least once.

If a take drifts into partner-channel language, it's a re-record.

### Rule 5 · NVIDIA is composable, not a replacement

Episodes 4 and 5 introduce NVIDIA — Metropolis, DeepStream, Jetson, RAPIDS, Triton, NeMo, NVIDIA AI Enterprise, Omniverse, Toyota Drive. The framing:

- NVIDIA is **composable with** the Microsoft platform, not a substitute.
- The Microsoft data fabric remains the system of record for the warranty agent. NVIDIA inline at the station is **Day-0 prevention** — catching the defect before it becomes a warranty claim.
- Toyota already runs an NVIDIA estate (Woven City on Omniverse; AV development on Drive). The conversation acknowledges what exists.
- NVIDIA is named accurately as a capability in the same architecture, not pitched as Deloitte's recommendation the way Microsoft is.

### Rule 6 · The numbers anchor — said the same way every time

Across all five episodes, the reference scenario value statement is spoken consistently:

- **$4.2M** in warranty cost identified
- **$2.8M** in chargeback recovery evidence
- **340%** improvement over the manual chargeback process
- **8 to 12 weeks across six teams → minutes** for the same investigation

No host invents Toyota-specific numbers. The $4.2M / $2.8M / 340% is the **reference scenario** — clearly labelled as such — not a Toyota result.

### Rule 7 · The four domains, named consistently

Always named the same client-safe way on tape: "the vehicle build record" · "connected vehicle warranty data" · "quality events on the line" · "assembly line telemetry". Never BRML / CVML / QEML / AAML on tape — those live in the README mapping table for Account Team reference.

---

## 4. What NOT to do

- **Do not** use "co-sell" / "alliance" / "strategic partnership" / "channel partner" anywhere.
- **Do not** trivialise TPS or use Jidoka, Andon, Kaizen, Genchi Genbutsu, or Hansei as decoration.
- **Do not** pitch L4 (transformation) when the conversation is L2 (one-plant Wave 1 pilot). The 90-day path in Episode 5 is L2. L4 is named in passing as a horizon, not pushed.
- **Do not** fabricate Toyota-specific numbers beyond the labelled $4.2M / $2.8M / 340% reference scenario.
- **Do not** quote copyrighted Toyota music or marketing slogans.
- **Do not** use internal codenames on tape — BRML, CVML, QEML, AAML, ORCH-01, SB06, AXLE, APEX-M all live in documents, never in audio.
- **Do not** characterise operators as sources of defects. Cohort patterns surface training / tooling / ergonomics questions, never blame.
- **Do not** pitch NVIDIA as a replacement for the Microsoft fabric. Composable, named accurately.
- **Do not** use emojis in the markdown files.

---

## 5. Voice cast

| Host | Voice (edge-tts) | Persona |
|---|---|---|
| **Keven** | `en-US-AndrewNeural` | Trilogy continuity host; the practitioner. 22+ years on the Microsoft platform. Warm, confident, plain-spoken. |
| **Mia** | `en-US-MichelleNeural` | Automotive engineering partner. 18 years on automotive accounts. Manufacturing-IT and quality-leadership background. TPS-fluent. Comfortable with shop-floor reality. |

Seventh distinct voice pairing in the APEX podcast family. Michelle chosen for its newer-generation naturalness — matches Andrew's Multilingual-tier register in conversational quality. Replaced an earlier audition of Aria, which read as too synthetic / news-anchor for the conversational format.

---

## 6. Recurring rhythms

Each episode has these rhythms, not announced:

| Rhythm | Length |
|---|---|
| **Cold-open scene** — a lived warranty / quality / connected-vehicle moment | 3-5 min |
| **Context** — TPS, Toyota, or Microsoft / NVIDIA platform context for the episode | 3-5 min |
| **The development** — the concept walked: pain → architecture → mechanism → outcome | 14-18 min |
| **Disagreement** — a specific point Keven and Mia diverge on | 3-4 min |
| **What to carry forward** — the listener's takeaway | 1-2 min |

Total: 28-32 minutes per episode.

---

## 7. Length targets

| Episode | Target |
|---|---|
| 01 (The Idea) | 5,500-6,000 words |
| 02 (Four Domains) | 5,500-6,000 words |
| 03 (The Agent & Platform) | 6,000-6,500 words |
| 04 (NVIDIA at the Station) | 5,500-6,000 words |
| 05 (Omniverse & 90-Day Path) | 5,500-6,000 words |
| **Total** | **~28,000-30,000 words · ~2.5 hours audio** |

---

## 8. Music sting

A single industrial **G-major chord** in the automotive-brand-family register, synthesised royalty-free via ffmpeg. Same sting top and tail every episode. No copyrighted or Toyota-branded music.
