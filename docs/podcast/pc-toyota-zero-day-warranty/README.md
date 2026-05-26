# The Zero Day Warranty Podcast — Toyota's Path from 8-12 Weeks to Minutes · `pc-toyota-zero-day-warranty`

A **five-episode** podcast on the Zero Day Warranty agentic scenario for **Toyota Motor North America** — built for the Deloitte Account Team and **client-shareable as a single artefact** when the moment calls for it. Builds on the APEX Trilogy and runs parallel to the DTNA Account Podcast.

> **Dual-audience artefact.** Unlike the DTNA podcast (internal-only) or the Trilogy (framework-only), the *spoken content* is safe for a Toyota listener. Internal codenames, Practice abbreviations, and scenario IDs are absent from the audio. The internal-language mapping lives in this README — not in the show bible, not in the episodes.

---

## Why this podcast exists

In May 2026 the Deloitte Account Team opened a Zero Day Warranty conversation with Chris Crotts at Toyota — joining connected-vehicle warranty claims back to factory build history per VIN, in minutes rather than the **8 to 12 weeks across six teams** the current process consumes. Reference scenario: **$4.2M in warranty cost identified, $2.8M in chargeback recovery, 340% improvement**.

The Account Team needs:

1. **A shared narrative arc** — the warranty-cluster moment, Toyota's TPS heritage, and why an audit-ready agent composes capabilities Toyota already licenses.
2. **The four data domains** — Build Record, Connected Vehicle, Quality Event, Assembly Asset — joined per VIN on Microsoft Fabric medallion.
3. **A platform picture** — Microsoft Fabric + Agent Framework + Purview as the agentic platform; NVIDIA composable for Day-0 prevention and the Omniverse / Drive estate Toyota already runs.
4. **A 90-day path** — one-plant pilot and Account Team handoff.

---

## The hosts

**Keven** *(the practitioner)* — `en-US-AndrewNeural` · Trilogy continuity host. 22+ years on the Microsoft platform. Warm, confident, practitioner register. Lives in Allen, TX — fifteen minutes from TMNA HQ in Plano.

**Mia** *(the automotive engineering partner)* — `en-US-MichelleNeural` · Senior Deloitte specialist with 18 years on automotive accounts. Manufacturing-IT and quality-leadership background — has sat in plant quality reviews, read andon-cord data, watched warranty clusters triaged across six teams in real time. Speaks fluent TPS — Jidoka, Andon, Kaizen, Genchi Genbutsu, Hansei — accurately, never as decoration. The *shop-floor reality and operator-dignity* lens.

Mia is the **seventh distinct voice pairing** in the APEX podcast family.

---

## The five episodes

| # | Title | Centered on |
|---|---|---|
| 01 | **The Zero Day Warranty Idea** | The warranty-cluster moment · 8-12-weeks-across-six-teams baseline · Toyota's TPS and Jidoka heritage · the audit-ready-agent hypothesis |
| 02 | **Four Data Domains** | Vehicle build record · connected vehicle warranty data · quality events on the line · assembly line telemetry · Microsoft Fabric medallion · per-VIN joinable Gold views |
| 03 | **The 24-Step Agent and the Microsoft Platform** | Microsoft Fabric + Agent Framework + Purview · the 24-step agent end to end · LEDGER hash chain and audit echo · the $4.2M / $2.8M / 340% calculation walked one step at a time |
| 04 | **NVIDIA at the Station (Day-0 Prevention)** | Metropolis · DeepStream · Jetson · RAPIDS · the two-fabric architecture · why inline vision at the station is Day-0 prevention and composes with the Microsoft data fabric |
| 05 | **Omniverse, Toyota's NVIDIA Estate, and the 90-Day Path** | Woven City and Omniverse · Toyota Drive · NeMo, Triton, NVIDIA AI Enterprise · the 90-day one-plant pilot · Account Team handoff |

Run time: ~2.5 hours · 28-32 minutes per episode.

---

## Independence from Microsoft · the two-contract model

This podcast operates inside Deloitte's Independence posture. The audio reflects it precisely:

- **Deloitte recommends.** When the hosts say Microsoft Fabric or Agent Framework or Purview is the right platform, that recommendation is on the technical and economic merits — not on partner-channel compensation.
- **Toyota contracts directly with Microsoft.** Microsoft licensing flows on Microsoft paper between Microsoft and Toyota. Deloitte does not resell, mark up, or take margin on Microsoft licensing.
- **Toyota contracts directly with Deloitte.** A separate Deloitte SOW governs the services scope.
- **Two contracts. No co-sell. No alliance. No strategic-partnership construct.** Those words are absent from this podcast on purpose.
- **No compensation flows from Microsoft to Deloitte** for influencing Toyota's platform choice. The recommendation stands on its own.

Episode 5 names this posture explicitly so a client listener hears the model stated, not implied.

---

## Internal-language mapping · client-safe term → internal nomenclature

For Account Team reference only. **This table lives in the README, not in the audio.** Episodes use the left-hand column; the right-hand column is for internal coordination.

| Client-safe term (spoken in audio) | Internal nomenclature |
|---|---|
| "Zero Day Warranty agentic scenario" | ORCH-01 Warranty Root-Cause (AXLE) · SB06 Warranty Traceability & Cost Avoidance (BRML) |
| "the vehicle build record domain" | BRML — Build Record ML schema family |
| "connected vehicle warranty data domain" | CVML — Connected Vehicle ML schema family |
| "quality events on the line domain" | QEML — Quality Event ML schema family |
| "assembly line telemetry domain" | AAML — Assembly Asset ML schema family |
| "Microsoft Fabric for the unified data layer" | Bronze / Silver / Gold medallion on OneLake · per-VIN joinable Gold views |
| "Agent Framework for the agent reasoning" | Microsoft Agent Framework SDK + Azure AI Foundry Agent Service |
| "Microsoft Purview for governance and audit" | LEDGER hash chain + Purview audit echo + DSPM for AI |
| "audit-ready agent" | LEDGER hash chain + Microsoft Purview audit echo |
| "24-step manual investigation across teams and systems" | 24-step Foundry agent chain per Toyota AgenticAI scenario S1 (now automated) |
| "$4.2M / $2.8M / 340%" reference scenario | SB06 demo scenario value statement |
| "8 to 12 weeks across six teams" | Toyota AgenticAI scenario S1 current-state baseline |

Internal nomenclature on tape = re-record. The discipline is intentional.

---

## Music sting

A single industrial **G-major chord** in the automotive-brand-family register — royalty-free via ffmpeg, top and tail of every episode. No copyrighted or Toyota-branded music.

---

## Related podcasts

- **Sellers Podcast Ep 4** — *The Seven Industries* — defines AXLE as the automotive Practice.
- **Services Podcast Eps 3-4** — the medallion + agent foundation under Episodes 2 and 3 here.
- **Services Podcast Ep 6** — the warranty cost-spiral deep dive — conceptual ancestor of Zero Day Warranty.
- **DTNA Account Podcast Ep 2** — the same warranty pattern in a Class 8 truck context.

---

## Files in this folder

```
pc-toyota-zero-day-warranty/
├── README.md                              ← you are here
├── 00-show-bible-and-format.md            ← format + Toyota style notes
├── 01-the-zero-day-warranty-idea.md       ← Episode 1 (forthcoming)
├── 02-four-data-domains.md                ← Episode 2 (forthcoming)
├── 03-the-24-step-agent-and-the-microsoft-platform.md  ← Episode 3 (forthcoming)
├── 04-nvidia-at-the-station.md            ← Episode 4 (forthcoming)
├── 05-omniverse-and-the-90-day-path.md    ← Episode 5 (forthcoming)
└── _build_audio.py                        ← TTS pipeline (forthcoming)
```

`audio/` appears after generation.


---

*The implied listener: a Deloitte Account Team member preparing for the next Crotts conversation — or, when the moment is right, a Toyota Quality, Toyota Connected, or Manufacturing IT leader walked through Zero Day Warranty on their own terms.*
