# 06 — Strategic Partnership Map

> Partnerships fall into **five archetypes** by what is being exchanged. Once a candidate is classified, the deal structure (rev-share % vs fixed integration fee vs data-for-distribution swap) almost writes itself.

## 1. The five partnership archetypes

| Archetype | What flows to Telco | What flows to partner | Typical deal shape |
|---|---|---|---|
| **A — Data-In** | Telemetry / catalog data to make the agent smart | Customer reach + a clean signal back (consumption, NPS) | Reciprocal data-sharing + revenue share on actions |
| **B — Action-Out (Fulfillment)** | Transaction completion the customer wants | Order volume, basket lift, lower CAC | Per-order rev-share, ~3–8% take rate |
| **C — Distribution / Bundle** | Bundled subscriber growth | Discounted CAC vs paid acquisition | Wholesale licensing or co-branded SKU |
| **D — Co-Insurance / Risk-Share** | Partner that monetizes the agent's outcome | Reduced loss ratio / better cohort risk | Outcome-based fees, shared savings |
| **E — Platform / Standards** | Interoperability with the device universe | Reference-implementation status | Strategic, usually free-as-in-beer |

## 2. Per-service partnership plays

### `TMT-TEL-HOM-01` — Grocery replenishment

| Partner type | Candidates | Archetype | Value exchange |
|---|---|---|---|
| Grocery retailers | Kroger, Walmart, Albertsons, H-E-B, Instacart, Amazon Fresh | B | Telco delivers high-intent baskets; retailer pays 4–7% rev-share + waives delivery fees on Telco-orchestrated orders |
| CPG brands | P&G, Unilever, Nestlé, PepsiCo | A + B | Replenishment data → demand-sensing; CPG funds promoted-SKU placement inside agent suggestions (disclosed as "sponsored") |
| Loyalty / rewards | Fetch, Ibotta, retailer-own loyalty | A + C | Loyalty points auto-applied → stickier subscription |
| Appliance OEMs (fridge cameras) | Samsung Family Hub, LG ThinQ, Whirlpool 6th Sense | A + E | Vision / inventory data; co-branded "Works with [Telco] Home" badge |

### `TMT-TEL-HOM-02` — Energy optimizer

| Partner type | Candidates | Archetype | Value exchange |
|---|---|---|---|
| Utilities | Duke, ConEd, Pacific Gas, NextEra, EDF | A + D | Tariff / ToU feeds + DR participation; Telco shares utility's avoided peak-MW capex |
| DR aggregators | OhmConnect, Voltus, AutoGrid, Leap | D | Telco enrolls households into DR programs; rev-share on capacity payments |
| Solar / storage | Tesla Energy, Enphase, Sunrun, SunPower | A + B | Powerwall / inverter telemetry; agent triggers grid-export or self-consume |
| EV charging | ChargePoint, Wallbox, Tesla Supercharger | A + B | Smart-charge scheduling; potential roaming-network fee share |
| Smart thermostats | Google Nest, ecobee, Resideo | A + E | Bidirectional control APIs |

> **Strategic note.** Utilities are the most underrated partner here — they pay $200–600 / kW-year for verified demand response. A Telco that aggregates 100K homes at 2 kW each is selling 200 MW of virtual capacity worth **$40–120M / yr**.

### `TMT-TEL-HOM-03` — Eldercare monitor

| Partner type | Candidates | Archetype | Value exchange |
|---|---|---|---|
| Medicare Advantage plans | UnitedHealth, Humana, Aetna, Elevance, CVS / Aetna | D | MA plans pay PMPM for fall-risk reduction; D-SNP and chronic SNP cohorts highest value |
| Hospital systems / ACOs | HCA, Ascension, Kaiser, regional ACOs | D | Readmission avoidance fee per qualifying patient |
| Pharmacy / med-adherence | CVS, Walgreens, Hero, MedMinder | A + B | Adherence data + auto-refill order action |
| PERS / alert vendors | Lifeline (Philips), Lively (Best Buy), Bay Alarm Medical | C | Co-branded device bundle into Telco plan |
| Senior-focused MA brokers | eHealth, GoHealth, SelectQuote | C | Bundled lead-gen during AEP |

> **Strategic note.** This is the **highest LTV service per subscriber by 5–10×**, because the payer (an MA plan) values 1 prevented fall ≈ $14K avoided ER visit. The Telco doesn't even need to charge the consumer directly — it can be sponsored by the health plan.

### `TMT-TEL-HOM-04` — Maintenance orchestrator

| Partner type | Candidates | Archetype | Value exchange |
|---|---|---|---|
| Appliance OEMs | Whirlpool, GE, Samsung, LG, Bosch | A + E | Diagnostic codes + firmware status; co-branded "extended warranty smart-monitored" SKU |
| Warranty providers | Asurion, Cinch, American Home Shield | D | Asurion already sells through Telcos for handsets — natural extension; loss-ratio reduction sharing |
| HVAC service networks | Carrier, Trane, Lennox dealer networks | B | Filter / maintenance dispatch with rev-share |
| Plumbing / leak detection | Moen Flo, Phyn (Roper) | A + B | Leak event triggers plumber dispatch; insurance discount |
| Recall feeds | CPSC, NHTSA recall API, SaferProducts.gov | A (free) | Cross-reference recall to household devices → safety alert |

### `TMT-TEL-HOM-05` — Security & presence

| Partner type | Candidates | Archetype | Value exchange |
|---|---|---|---|
| Security incumbents | ADT, Vivint, Brinks, SimpliSafe | C or competitive | Either bundle (ADT-Telco co-sell) or displacement play |
| Camera / doorbell OEMs | Ring (Amazon), Nest (Google), Eufy, Arlo | A + E | Event data; agent improves package-theft response, etc. |
| P&C insurance carriers | State Farm, Progressive, Allstate, Travelers, Lemonade | D | Insurance-premium discount funded by reduced claim frequency — Telco shares the premium savings |
| 911 / PSAP integrators | RapidSOS, Noonlight | E | Verified-presence data flows to first responders |
| Locksmith / access control | August (ASSA Abloy), Schlage Encode, Yale | A + B | Visitor verification + grant / revoke access |

### `TMT-TEL-HOM-06` — Wellness coach

| Partner type | Candidates | Archetype | Value exchange |
|---|---|---|---|
| Wearable OEMs | Apple Health, Garmin, Fitbit (Google), Oura, Whoop | A + E | Read-side health data |
| CGM / device makers | Dexcom, Abbott (Libre), Medtronic | A + D | Glucose data → diabetes program enrollment funded by payer |
| Employer wellness | Virgin Pulse, Limeade, Wellable, Vitality | C | B2B2C distribution through employers |
| Health plans | Same MA / commercial payers as HOM-03 | D | PMPM for chronic-condition cohort engagement |
| Pharma | Novo Nordisk, Eli Lilly (GLP-1 adherence) | D | Adherence-as-a-service for high-cost specialty drugs |
| Telehealth | Teladoc, Amwell, Included Health | B | Escalation from agent to clinician visit |

### `TMT-TEL-HOM-07` — Vehicle readiness

| Partner type | Candidates | Archetype | Value exchange |
|---|---|---|---|
| Automakers (telematics) | GM OnStar, Ford SYNC, Stellantis Uconnect, Tesla, Toyota Connected | A + E | Vehicle event data; embedded SIM = natural Telco fit |
| Charging networks | ChargePoint, EVgo, Electrify America, Tesla | A + B | Plan + schedule charges |
| Auto insurance (UBI) | Progressive Snapshot, State Farm Drive Safe, Root | D | Telematics-based premium discount, shared with Telco |
| Service networks | Jiffy Lube, Firestone, Pep Boys, dealer networks | B | Scheduled-maintenance booking + rev-share |
| Tire / parts | Bridgestone, Goodyear, Michelin, AutoZone | A + B | TPMS triggers reorder |

### `TMT-TEL-HOM-08` — Entertainment concierge

| Partner type | Candidates | Archetype | Value exchange |
|---|---|---|---|
| Streamers | Netflix, Disney+, Max, Paramount+, Peacock | C | Bundled SKUs (already standard Telco play; agent makes it personalized) |
| Music / podcast | Spotify, Apple Music, Audible | C + A | Bundle + listening data |
| CTV ad platforms | Roku, Samsung Ads, LG Ads, FreeWheel, The Trade Desk | A + B | Privacy-safe audience inference from agent context; ad rev-share |
| Live sports | DAZN, ESPN+, NFL Sunday Ticket, regional sports networks | C | Personalized highlight delivery |
| Gaming | Xbox Cloud, GeForce NOW, PlayStation Plus | C | Bandwidth / latency value-add |

## 3. Cross-cutting / foundational partners

These don't sit under any one service — they make the whole platform possible.

| Layer | Candidates | Why |
|---|---|---|
| Hyperscaler (vault + AI) | Microsoft Azure (natural fit given APEX is MS-native), AWS, GCP | Per-household vault infra, Fabric / medallion runtime, Foundry agent runtime |
| Identity & consent | Microsoft Entra, Okta, Auth0, Trinsic (verifiable credentials) | Per-person granular consent ledger |
| Payments | Stripe, Visa Direct, Adyen, Telco bill-on-invoice | Push payments for agent-initiated transactions |
| Device interoperability | CSA Matter, Thread Group, Home Assistant (OSS), SmartThings (Samsung), Apple HomeKit, Google Home | Without Matter membership the device coverage stays narrow |
| Financial data | Plaid, MX, Finicity (Mastercard) | Budget-aware agents need bank feeds |
| Loyalty / rewards rails | Fetch, Drop, Bilt | Stitch every transaction into a reward |
| System integrators | Deloitte (Microsoft-aligned per APEX compliance lint), Accenture, Capgemini | Channel into Telco enterprise procurement |
| MCP server marketplace | Anthropic MCP ecosystem, Smithery, Composio | Agent ↔ partner tool plumbing |
| Privacy / data trust | Skyflow, Privacera, OneTrust | Defensible "your data, our network" positioning |

## 4. The three platform-defining partnerships

If we had to pick the three partnerships that decide whether this platform wins or loses, they are:

1. **Microsoft Azure** (or equivalent hyperscaler) as the vault / runtime backbone. Without a credible "we don't read your data, the hyperscaler enforces it" story, the consumer-trust differentiator vs. Big Tech evaporates. **Foundational.**
2. **At least one top-3 Medicare Advantage payer.** `TMT-TEL-HOM-03` (eldercare) is the wedge that turns this from a $15 / mo consumer add-on into a **$50–80 PMPM B2B2C revenue line**. It also gives the Telco an unassailable narrative: "the only home platform reimbursed by your health plan." Humana, UHG (Optum), and CVS / Aetna are the three to target.
3. **CSA Matter + a top home-appliance OEM (Samsung or LG).** Without first-class device coverage at the appliance layer, the agent can't see the world. A flagship OEM partnership ("Works with [Telco] Home" — the FIOS-of-AI seal) creates a flywheel that pulls every other OEM in.

The other partnerships are important but substitutable — if Kroger says no, Walmart says yes; if Ring says no, Eufy says yes. The three above don't have substitutes that are equally good.

## 5. Suggested phasing

| Phase | Quarter | Partnerships to close |
|---|---|---|
| Phase 0 — Foundation | Q1–Q2 | Hyperscaler + Matter membership + identity provider |
| Phase 1 — Anchor consumer pull | Q3 | One grocer (HOM-01) + one utility-DR aggregator (HOM-02) — demoable economic value |
| Phase 2 — B2B2C unlock | Q4 | One MA payer (HOM-03) + one P&C insurer (HOM-05) — outcome-based revenue |
| Phase 3 — Coverage breadth | Year 2 | Appliance OEMs, automakers, streamers — turn the bundle into a "store" |
| Phase 4 — Marketplace | Year 2+ | Open MCP marketplace so 3rd-party agents / partners list against the household vault |

## 6. Deal-structure heuristics

| Archetype | Heuristic |
|---|---|
| A (Data-In) | Don't pay cash for data; pay in attribution (signed events back to source) and referral volume. Data has no scarcity value once you have scale. |
| B (Action-Out) | Take rate 3–8% is market for orchestrated commerce; demand price-match guarantees so the agent isn't perceived as marking-up. |
| C (Distribution) | Wholesale to the Telco at 40–60% off retail, brand co-presented; never let the partner control the retention surface. |
| D (Risk-share) | Insist on outcome measurement methodology up front (control cohort, attribution window). This is where partnerships die. |
| E (Standards) | Trade speed of integration for reference-design status; commit to publish the spec. |
