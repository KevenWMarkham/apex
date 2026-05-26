# The Daimler Trucks North America Account Podcast · `pc-dtna-account`

A **five-episode** internal Account Team podcast for the Deloitte team working **Daimler Trucks North America (DTNA).** Built on top of the APEX Trilogy podcasts (`pc-sellersguide/` · `pc-servicesguide/` · `pc-deploymentguide/`) — assumes the listener has at least skim-heard the Sellers Podcast and is familiar with the AXLE Practice.

> **Internal use.** This podcast names the client directly because it's internal Account Team preparation. The Trilogy podcasts reference DTNA-shaped scenarios anonymously through the AXLE Practice; this podcast names the company and its brands explicitly.

---

## Why this podcast exists

Daimler Trucks North America — DTNA — is the largest Class 8 heavy-duty truck manufacturer in North America by market share, the North American subsidiary of Daimler Truck Holding AG (spun off from Daimler AG in 2021). The 2026 opportunity at DTNA spans **AXLE Practice manufacturing and warranty scenarios**, **connected-vehicle and dealer-network plays**, and **the strategic conversations around electrification and autonomy** that are reshaping the trucking industry.

The Account Team needs:

1. **A shared strategic picture of DTNA** — four brands, three operating themes, the AXLE Practice mapping.
2. **A working knowledge of the AXLE scenarios** that map directly to DTNA's pressure points — Zero Day Warranty, predictive maintenance, connected diagnostics, dealer performance.
3. **A coherent ladder strategy** — L1 wedge through L4 fleet-customer transformation.
4. **An operational playbook** — who to call, what to say, Independence specifics for a German-parent audit-adjacent account, the 90-day calendar.

These five episodes deliver all four.

---

## The hosts

**Keven** *(the practitioner)* — `en-US-AndrewNeural` · Same Trilogy continuity host across all four account-and-framework podcasts.

**Marcus** *(the senior account partner)* — `en-US-BrianMultilingualNeural` · A senior Deloitte account partner with 10+ years on Class 8 truck OEM accounts. Has walked the Mt. Holly and Cleveland and Portland plants. Knows the dealer network, the major fleet customer relationships, the engineering and manufacturing leadership. Plays the role of *"OK but what the VP of Manufacturing will actually say to that is…"* Marcus keeps the conversation grounded in *who at DTNA decides what.*

The Trilogy podcasts had Jordan (strategist), Morgan (delivery architect), Sam (platform engineer); the Disney podcast had Riley (media account partner). Marcus is the *industrial-automotive account-relationship* lens — different from all four.

---

## The five episodes

| # | Title | Centered on |
|---|---|---|
| 01 | **The DTNA Account** | Strategic context · four brands (Freightliner, Western Star, Thomas Built, Detroit) · three pressure themes (electrification, autonomy, freight cycle) · why APEX *now* |
| 02 | **The Manufacturing & Quality Plays** | Zero Day Warranty · predictive maintenance · quality escape detection · plant-floor agent assist · supplier traceability · production planning |
| 03 | **The Connected Vehicle & Aftermarket Plays** | Detroit Connect diagnostic acceleration · dealer network performance · parts demand forecasting · service-bay agent assist · fleet customer experience · driver-facing in-cab assistance |
| 04 | **The Ladder for DTNA** | L1 wedge heatmap · L2 Wave 1 · L3 AXLE Practice CoE inside DTNA · L4 fleet-customer transformation (Detroit Connect + agentic services) · GSSC Lab for AXLE demos · the electrification and autonomy strategic frames |
| 05 | **The Account Team Playbook** | Relationship map across DTNA's executive org · 30-Min Framework tuned for truck-OEM leaders · Independence specifics (German-parent audit context) · Microsoft coordination · the 90-day calendar |

Total run time target: ~2.5 hours.

---

## How this podcast relates to the Trilogy and to the Disney podcast

This podcast is a *parallel artefact* to the Disney Account Podcast — same shape (5-episode account-specific deep dive), different industry. Both build on the Trilogy.

```
Sellers Podcast (general framework)  ────┐
                                          ├──> Disney Account Podcast (TMT-MED · pc-disney-account/)
Services Podcast (delivery architecture)──┤
                                          ├──> DTNA Account Podcast (AXLE · this folder)
Deployment Podcast (operations)         ──┘
```

Specific references this podcast makes back to the Trilogy:

- **Sellers Podcast Ep 4** — *The Seven Industries* — defines AXLE as the automotive Practice; this podcast is the account-specific application.
- **Sellers Podcast Ep 5** — *Anchor Accounts, Part 1* — covers a global automotive OEM anonymously; this podcast names DTNA.
- **Sellers Podcast Ep 6** — *The Warranty Cost Spiral* (Services v2 podcast) — the Zero Day Warranty story is *exactly* the DTNA pitch.
- **Services Podcast Eps 3-4** — the medallion + agent foundation the AXLE Service architecture rests on.
- **Services Podcast Ep 6** — the warranty cost-spiral deep dive — referenced extensively in Ep 2 of this podcast.
- **Deployment Podcast Ep 4** — Service and agent layers — the operational discipline for AXLE deployment.

---

## DTNA at a glance

| Dimension | DTNA |
|---|---|
| Parent | Daimler Truck Holding AG (spun off from Daimler AG in 2021) |
| Brands | Freightliner (flagship Class 8) · Western Star (premium / vocational) · Thomas Built Buses · Detroit (engines, axles, eAxle) |
| HQ | Portland, Oregon (Freightliner) · Stuttgart (Daimler Truck Holding parent) |
| Major NA plants | Mt. Holly, NC · Cleveland, NC · Saltillo, Mexico (engines) · Redford, MI (engines) · Gastonia, NC (Thomas Built) · Portland (HQ, engineering) |
| Market share | Largest Class 8 NA market share (typically ~40%) |
| Typical NA Class 8 market | ~250-280K units in a normal cycle year (highly cyclical) |
| Connected vehicle platform | Detroit Connect — telematics across the fleet |
| Autonomous-trucks partner | Torc Robotics (Daimler Truck Holding subsidiary based in Blacksburg, VA — Level 4 development) |
| Electric portfolio | eCascadia, eM2 (medium duty), eEconic, with planned Class 8 e-truck expansion |
| Regulatory pressure | CARB Advanced Clean Trucks · EPA 2027 NOx · NHTSA safety |

---

## Files in this folder

```
pc-dtna-account/
├── README.md                              ← you are here
├── 00-show-bible-and-format.md            ← format + DTNA-specific style notes
├── 01-the-dtna-account.md                 ← Episode 1
├── 02-manufacturing-and-quality.md        ← Episode 2
├── 03-connected-vehicle-and-aftermarket.md← Episode 3
├── 04-the-ladder-for-dtna.md              ← Episode 4
├── 05-the-account-team-playbook.md        ← Episode 5
└── _build_audio.py                        ← TTS pipeline (Keven=Andrew, Marcus=Brian Multilingual)
```

After audio generation, an `audio/` subfolder appears with the five MP3s and a folder-level README.

---

*The implied listener: a member of the Deloitte Account Team for DTNA — partner, senior manager, manager, senior consultant — who is preparing for an upcoming DTNA conversation and wants the* account-specific *application of APEX and the AXLE Practice without re-listening to the entire Trilogy.*
