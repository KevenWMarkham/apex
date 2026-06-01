# Episode 03 · The default channel · Home goes live in shadow (M2)

**Builds on:** Eps 01 + 02. The M1 gate items have closed: AT&T Wave-1 charter signed, LA28 sponsorship scope confirmed, NBCU scope-boundary conversation opened, Microsoft Azure CAF capacity reservation confirmed, pursuit team named, Microsoft platform engagement framework set with Independence-clean language.

## Cold Open

[soft room-tone, the low hum of a NOC server aisle, an HVAC unit cycling, a single keyboard tap]

Late autumn 2026. Eleven forty-seven on a Wednesday night, Eastern time. The AT&T NOC engineer is at her workstation, second monitor angled slightly toward her, the just-launched Default Home Channel telemetry stream lit across the right two-thirds of the screen. The channel went live in shadow ten minutes ago. The first agent has just composed a recommendation for a real AT&T household — a billing-cycle optimisation, the kind a customer would skim past in three months when shadow flips to live and a card lands on their phone. Low-stakes. Exactly the kind of recommendation the operations playbook wants to see first.

She watches the trace_id propagate through the A2A Swarm runtime. HOM-02 hands to HOM-04. HOM-04 hands to HOM-99 for the household-policy check. The vault seals the audit row at the edge — the customer-held KMS signs, the per-household key wraps the payload, the LEDGER substrate writes the row. The Adaptive Card renders on the operator console next to her, a clean rectangle of summary text and a recommended action. And then it stays there. No customer-facing delivery. The card sits on the operator console and does nothing else. The household never sees it. The household does not know the recommendation exists.

But everything below that surface is real. The composition is real. The trace is real. The vault sealed a real audit row against a real customer-held key. The latency budget held — she checks the dashboard, two hundred and forty-three milliseconds end to end, well inside the envelope. CAF capacity is reading nominal. Foundry throughput is steady. The Microsoft Azure platform underneath is carrying actual load against a real AT&T household for the first time.

She types a single line into the shift log. *2347 ET. HOM channel shadow live. First trace clean. No delivery. Holding.* She hits enter. The trace count on the dashboard ticks from one to two as the next household enters the run.

The Microsoft platform engagement from M1 just became operationally true at 11:47pm Eastern on a Wednesday.

[beat. then studio]

**RASHMI:** I want to start with that NOC engineer at her desk at 11:47pm, because the part of M2 that does not get photographed — and the part that I think pursuit teams in this kind of build under-rate — is what shadow mode actually feels like when it goes live for the first time. It is not a launch. There is no announcement. There is no customer who knows anything happened. There is one engineer in a NOC, typing a one-line entry into a shift log, and a trace count ticking from one to two on a dashboard. That is the M2 moment. And the reason that moment matters — the reason it carries the whole milestone — is that everything below the operator console is real. The composition is real. The vault is real. The audit is real. The Microsoft Azure platform is carrying real load against a real household. The delivery is the only thing that's suppressed. Everything else is the production system. And that is what makes shadow mode the contract between the platform and the anchor.

**KEVEN:** And the part I want listeners to hold — because we will come back to it — is that everything underneath that operator console at 11:47pm is the Microsoft platform engagement actually working. Foundry is running the agent fleet. The A2A Swarm is moving the trace through HOM-02 and HOM-04 and HOM-99. The CAF capacity reservation that the Microsoft AE walked through with the DMTSP Microsoft Platform Lead at M1 is now carrying nominal load on real traces. The reference patterns from the architecture center that the AT&T CTO's team validated at M1 are operationally true. The platform engagement framework we set at M1 — recommended on the merits, Independence-clean, the canonical phrase carried into Schedule B of the Wave-1 charter — has just become a live runtime against a real anchor. The platform either holds at M2 or it doesn't. And at 11:47pm on a Wednesday in late autumn 2026, it holds. That is the milestone in one sentence.

## The conversation

### Shadow mode — what it means and why

**RASHMI:** Picture the Risk Advisory Partner the morning after. Eight-fifteen Pacific. She is at her kitchen counter with a coffee, the laptop open to the shadow-launch readiness checklist she signed off on the previous Friday. The NOC engineer's shift-log entry is in her inbox, forwarded by the TMT Delivery Architect with a one-line subject — *HOM shadow live. Clean first trace.* The Partner reads the shift-log entry twice. She does not reply to the email. She opens the gate-status tracker for M2 instead, finds the line for *shadow-launch confirmed,* and changes it from amber to a paused green. Paused because the shadow window is only ten minutes old. Green because the contract that made the launch possible held. That coffee, that kitchen counter, that paused green on the tracker — that is what shadow mode means to the seller side of the house. It means the Partner can pause on green, not amber, before the second cup is cold.

**KEVEN:** And the reason shadow mode is the load-bearing pattern for M2 — and Rashmi, the reason the Risk Advisory Partner could move the line at all — is that shadow lets the channel run end-to-end against real telemetry without exposing the customer to a recommendation we have not yet validated at scale. The agents compose. The vault seals. The audit writes. The Adaptive Card renders on the operator console. The operator sees what the customer would see. But the customer-facing delivery — the push notification, the in-app card, the bill insert — is suppressed at the delivery edge. The platform carries production load. The customer experiences nothing. That is the contract.

**RASHMI:** Walk why it has to be shadow. Why not a small live cohort from the start.

**KEVEN:** Because the risk surface at M2 is the platform itself, not the recommendation quality. We do not yet know how the A2A Swarm coordination behaves under sustained load against four quarters of AT&T-anonymised IoT data. We do not yet know the steady-state Foundry throughput against a real household-distribution. We do not yet know whether the customer-held KMS sealing pattern survives a sustained burst of vault writes. Those are platform-engineering questions and the right way to ask them is to run the system end-to-end against real data with the delivery surface dark. The recommendation quality conversation — *is the recommendation the household actually wants* — is the M3 conversation. M2 is the *does the platform hold* conversation. Two different questions. Two different cohorts.

**RASHMI:** And the AT&T side of the contract. What does AT&T get out of shadow mode that AT&T could not get out of a small live launch?

**KEVEN:** AT&T gets the ability to read its own NOC dashboards for ninety days against the Default Home Channel before any customer in their footprint has seen a recommendation. AT&T's Security office can audit the vault behaviour without a customer being at risk during the audit. AT&T's Privacy office can confirm that the per-household vault residency holds through a real load before there is a real-world surface to defend. The AT&T CTO can walk into a board update and say — *the platform has been running against real households for ninety days, the audit row is clean, the vault has held, the latency is inside envelope, and no customer has seen a recommendation we have not gated.* That is what shadow buys AT&T. It is the institutional permission slip to flip the switch at M3.

**RASHMI:** And the seller frame. What does this mean for a TMT seller talking to a Wave-2 LCSP next quarter?

**KEVEN:** It means the seller can say — *we ran AT&T's Default Home Channel in shadow for ninety days with vault, audit, and customer-held KMS production-cut. The platform held. The architecture is reference-pattern-fidelity. The Microsoft platform engagement held under real load.* That is a sentence the TMT seller can put in a Wave-2 LCSP brief and it lands. Without the shadow window, the same sentence is a hope. With the shadow window, it is a record.

**RASHMI:** Monday morning. What does the seller do?

**KEVEN:** Monday morning the TMT Account SE for the AT&T anchor is in a stand-up with the NOC engineering lead, reading the prior week's shadow-telemetry summary. The TMT Delivery Architect is in a separate stand-up with the platform team walking the trace-volume curves. The Risk Advisory Partner has the gate-status checklist on her screen. Three stand-ups. One channel. One platform. One gate.

### The Default Home Channel architecture

**KEVEN:** Picture the TMT Delivery Architect at a whiteboard in the Atlanta delivery centre, mid-afternoon, two weeks before the shadow launch. The whiteboard has nine boxes on it. HOM-01 through HOM-08 across the top in a row, then HOM-99 sitting underneath the row in the centre, drawn slightly larger, because HOM-99 is the household-policy guardrail and it sits across all eight. Arrows between the boxes show the A2A Swarm routing — HOM-02 to HOM-04 when an energy-optimisation recommendation needs a billing context check, HOM-05 to HOM-01 when a device-coordination action needs identity confirmation, HOM-99 sitting as a check-in node for every transition. To the right of the whiteboard, on a second whiteboard, the CAF substrate is sketched — Foundry instances, the vault edge with the customer-held KMS, the Adaptive Card surface, the LEDGER substrate underneath. The Architect is walking a TMT Senior Manager and a Microsoft CSA through the diagram for the third time that week. The CSA is asking the question that matters — *what happens to a trace when HOM-99 fails closed.* That whiteboard, that afternoon, that question — that is the architecture sub-section.

**RASHMI:** Walk the nine agents. What does each one do.

**KEVEN:** Eight functional agents and one guardrail. HOM-01 is identity and household composition — who lives at this address, what devices are in this household, what consent surfaces apply. HOM-02 is energy and utility optimisation — billing-cycle recommendations, plan-fit, time-of-use guidance. HOM-03 is connectivity orchestration — Wi-Fi, mobile, the boundary between AT&T's services and adjacent connected-home services. HOM-04 is billing-context awareness — the AT&T Bill as the trust anchor, line-item rendering, plan-change reasoning. HOM-05 is device coordination — the connected-home action surface. HOM-06 is media and entertainment routing — watch-party suggestions, content discovery within scope. HOM-07 is the safety and security agent — door, camera, alarm-adjacent guidance. HOM-08 is the household calendar and rhythm agent — when the household is home, when the household is travelling, when to defer recommendations. And HOM-99 is the household-policy guardrail — the agent that holds the *we will not surface this recommendation to this household at this time* veto across all eight.

**RASHMI:** And the A2A Swarm runtime. What is the listener supposed to hear about it.

**KEVEN:** A2A Swarm is the multi-agent coordination layer that runs on Foundry. Agents compose by passing structured messages with a propagating trace_id; the Swarm runtime arbitrates priority, manages back-pressure, and surfaces traces to LangFuse for observability. Each agent is a Foundry agent with its own prompt, tool set, and model-routing policy. The HOM-99 guardrail is wired into every transition. When HOM-99 fails closed — and to the Microsoft CSA's question on the whiteboard, this is the load-bearing case — the trace terminates, the Adaptive Card surface receives a *suppressed* signal, the audit row writes with the suppression reason, and the operator console shows the suppression. No customer-facing delivery is even contemplated. HOM-99 has veto power on every trace.

**RASHMI:** And the vault. The customer-held KMS piece is the one the AT&T Security office is going to ask about hardest.

**KEVEN:** Right. The vault sits at the trust edge — between the agent fleet and the LEDGER substrate. Each AT&T household has its own per-household vault tenant. The encryption key is held by AT&T as the household's trust anchor — a customer-held KMS model, not a platform-held model. When an audit row writes, the platform composes the row, the vault wraps it with the per-household key signed by AT&T's KMS, and the row lands in LEDGER with the customer-held signature on it. The platform never holds the cleartext key. The model survives an audit because the cleartext is never in platform custody. That is the property AT&T's Security office is validating in M2.

**RASHMI:** And the Adaptive Card surface. The thing the operator sees on the console at 11:47pm.

**KEVEN:** Adaptive Cards are the rendering layer. Standard schema, structured payload, rendered by a host — in shadow, the host is the operator console; in live, the hosts are the AT&T mobile app and the bill insert. The card the NOC engineer saw at 11:47pm was the operator-host render of exactly the payload the customer-app host would have rendered, with the delivery edge dark. Same payload. Different host. That is what makes shadow mode an honest dress rehearsal — the only thing the customer would see differently is the delivery surface itself.

**RASHMI:** Monday morning. What does the seller do?

**KEVEN:** Monday morning the TMT Delivery Architect's architecture readout is in the document-management system, version two, scoped to the AT&T CTO's architecture team for review. The Microsoft CSA and the DMTSP Microsoft Platform Lead have their next joint architectural readout on the calendar — CAF substrate validation, A2A Swarm pattern walk, LangFuse trace-volume review.

### What "Default" means and why it matters

**RASHMI:** Picture the TMT VP four weeks after the shadow launch, in a Travel-Channel onboarding workshop. The room is the TH Travel anchor lead, the TMT Delivery Architect, an American Airlines product manager, and a Marriott loyalty-platform architect. The TMT Delivery Architect has just walked the Default Home Channel architecture diagram — the nine agents, the A2A Swarm, the vault edge, the Adaptive Card surface. The Marriott architect has been quiet through the walk. He puts down his coffee. He says one sentence. *"So Travel plugs into this. We do not rebuild this."* The TMT Delivery Architect says *correct.* The Marriott architect says *"Then we are not talking about a Travel Channel build. We are talking about a Travel agent set inside the Home Channel substrate."* The room goes still for about three seconds. That moment — when an anchor architect on a Wave-1 plug-in channel realises the Home substrate is the substrate — is what "Default" means. It is the first time the pattern lands outside the Wave-1 anchor. And it lands clean because the Default got built right.

**KEVEN:** Walk why Default has to be the pattern. What happens if Home is just another channel among eleven.

**RASHMI:** Then every plug-in channel rebuilds the substrate. Travel rebuilds the vault. Retail rebuilds the LEDGER. Mobility rebuilds the A2A Swarm topology for its own agent set. Eleven different teams reinvent the platform. The Microsoft platform engagement loses fidelity. The reference patterns drift. The Risk Advisory overlay has to clear eleven different architectures instead of one. By M5 we have a runtime per channel and an integration debt that swallows the runway. That is what happens when Default is not actually the Default.

**KEVEN:** And the alternative — when Home is Default.

**RASHMI:** Travel ships HOM-99-equivalent guardrails as a configuration over the same household-policy substrate. Retail ships a Retail agent set — basket coordination, loyalty-context awareness, store-pickup orchestration — that hangs off the same Adaptive Card surface and the same vault edge. Mobility ships agent personas that route through the same A2A Swarm with their own model-routing policies. The vault is the same. The LEDGER is the same. The Foundry capacity envelope is shared. The Microsoft platform engagement is one engagement, validated once at M2, leveraged across the eleven channels. That is the Wave-1 design.

**KEVEN:** And the M2 work that secures the pattern. Specifically.

**RASHMI:** Three pieces. First, the marketplace meta-pack tables — Channel, ChannelSubscription, partner_directory — get stood up at M2, not at M3, because the plug-in channels need a registry to subscribe into. The TMT Delivery Architect lands those tables at the same time he lands the Home pack TMTML entities, in the same shadow window. Second, the Home pack itself is built as a reference pack — every entity, every event, every agent contract is documented as the template for plug-ins. When Travel onboards in M3, the Travel team is reading the Home pack as a template, not as a one-off. Third, the configuration surfaces — what a plug-in channel changes about Home versus what it inherits — are documented in M2. The Marriott architect at the workshop could ask *what do I configure* and get a one-page answer. Without that document, the pattern is not portable.

**KEVEN:** And the platform side. What does Default mean for the Microsoft platform engagement.

**RASHMI:** It means the CAF capacity envelope is sized for the *substrate* — not for Home. The Foundry agent fleet is provisioned with headroom for plug-in agent sets to land. The vault and LEDGER throughput targets are calibrated for the full eleven-channel load profile, not the Home-only load profile. The Microsoft AE's CAF reservation form from M1 is shaped against the eleven-channel forecast. That is why the M0-to-M1 work paid for itself — when M3 plug-ins land, there is no scramble to revise the platform engagement. The platform was sized for the pattern, not for the pilot.

**RASHMI:** Monday morning. What does the seller do?

**KEVEN:** Monday morning the TH Travel anchor lead's M3 plug-in workshop calendar is being built off the Home reference pack documentation. The RC Retail anchor lead has the same documentation in hand for the Walmart pre-warm conversation. The TMT Delivery Architect's pack-template version is in the document-management system, scoped to the Wave-1 plug-in leads as required reading.

### The first observations

**KEVEN:** Picture the Monday morning shadow-telemetry review meeting, six weeks into shadow. The TMT Delivery Architect is on screen-share with three dashboards open — trace volume, latency distribution, suppression rate. The AT&T NOC engineering lead is on the call. The Microsoft CSA is on the call. The DMTSP Microsoft Platform Lead is on the call. The TMT Account SE for AT&T is on the call. The Architect pulls up the suppression-rate dashboard. The number on the screen — the percentage of traces where HOM-99 has failed closed and suppressed delivery — is higher than the platform team forecast. Not catastrophically. Higher. The Architect circles the number with his cursor. He says *"We need to walk this."* That circled number on a Monday-morning screen-share — that is the first observations sub-section.

**RASHMI:** Walk the kinds of observations shadow surfaces. What is the telemetry telling us.

**KEVEN:** Four families of observations. First, *platform behaviour at load* — latency distributions, throughput against forecast, Foundry response-time curves, CAF capacity utilisation, vault-write latency, LEDGER-write latency. Are we inside the envelope. Second, *coordination behaviour* — how often the A2A Swarm routes a trace through more than two agents before composing a recommendation, how often a trace deadlocks and is recovered, how often the back-pressure system has to throttle. Are the patterns clean. Third, *household-policy behaviour* — how often HOM-99 fails closed, on what kinds of recommendations, for what kinds of households. Is the guardrail too tight, too loose, or right. Fourth, *recommendation-quality signal* — when a recommendation is composed and suppressed, would a human operator have agreed with the composition. That signal is qualitative and comes from the NOC operator-console review.

**RASHMI:** And the suppression-rate observation. The one the Architect circled. Walk that.

**KEVEN:** The forecast was a low-single-digit suppression rate in steady state. The observed rate at six weeks is meaningfully higher. The Architect's working theory — and it is a theory at this point — is that HOM-99 is failing closed on traces where the household-policy substrate does not have enough recent signal to make a confident decision, and HOM-99's default in the absence of signal is to suppress. That is the right default. But it means we are leaving cleanly-composable recommendations on the table because the policy substrate is still warming. The fix is partly a M3 fix — more signal accumulates as shadow runs longer — and partly a HOM-99 calibration question we open with the AT&T Privacy office.

**RASHMI:** And the AT&T Privacy office. What is that conversation.

**KEVEN:** It is the conversation about how much signal the household-policy substrate is permitted to retain before HOM-99 will allow a recommendation to compose. The Privacy office is going to ask — *what is the minimum signal you need, retained for what duration, with what audit trail.* The TMT Delivery Architect has a one-page answer ready. The vault residency report shows where the signal lives. The LEDGER audit row shows how it is referenced. The conversation is honest and it is short.

**RASHMI:** And the latency. What is the platform showing.

**KEVEN:** Inside envelope. The p50 trace is comfortably within target. The p95 is inside envelope. The p99 has occasional outliers tied to Foundry cold-starts on agents that have not been routed through in a while. The platform team's mitigation is keep-warm for the long-tail agents during the Games window, which the CAF reservation has headroom for. The Microsoft CSA has walked the keep-warm pattern with the DMTSP Microsoft Platform Lead. Inside envelope, with a known mitigation for the long tail. The platform is behaving.

**RASHMI:** And the vault. Has it held.

**KEVEN:** It has. Vault-write latency is steady. No write-conflict patterns. The customer-held KMS signing is steady. AT&T Security has run an audit pass at four weeks and the audit row sample they pulled was clean. The vault has held against six weeks of sustained shadow load. That is the answer the M2 gate wants to hear.

**RASHMI:** Monday morning. What does the seller do?

**KEVEN:** Monday morning the TMT Account SE has the AT&T CTO's monthly architectural review on the calendar with the suppression-rate observation, the latency report, and the vault audit attached. The TMT Delivery Architect has the HOM-99 calibration conversation with the AT&T Privacy office on the calendar. The Risk Advisory Partner has the gate-status checklist updated with the shadow-telemetry summary.

### The Microsoft platform engagement holds

**KEVEN:** Picture the Microsoft CSA and the DMTSP Microsoft Platform Lead on a Tuesday morning at the CAF capacity dashboard, the live read of the AT&T Wave-1 shadow workload pulled up in one window, the reference architecture-center pattern open in another. It is peak-shadow-load hour — the part of the diurnal cycle where the agent fleet is most active because households are in their morning routine. CAF utilisation is steady. Foundry throughput is steady. Vault throughput is steady. The two of them are not looking for a problem. They are confirming the absence of one. The CSA says one line — *"this is the pattern."* The Platform Lead nods. That dashboard, that nod — that is the Microsoft platform engagement holding at M2. The M1 commitment, made on paper in a CAF capacity-reservation form, just became operationally true on a Tuesday morning.

**RASHMI:** Walk what holding means at M2. Specifically.

**KEVEN:** Three things hold. First, the CAF capacity envelope holds. The reservation the Microsoft AE walked with the DMTSP Microsoft Platform Lead at M1 — sized against the eleven-channel forecast with headroom for the Super Bowl LXII window and the Games window — is reading nominal against actual shadow load. The forecast was right. Second, Foundry throughput holds. The agent fleet is composing within the throughput envelope, with the keep-warm mitigation for long-tail agents queued and ready. Third, the vault throughput holds. The customer-held KMS signing is sustaining without write-conflict. Three platform-engagement properties. All three holding at six weeks of shadow.

**RASHMI:** And the architecture-center reference patterns. The ones the AT&T CTO's architecture team validated at M1.

**KEVEN:** They are operationally fidelity-clean. The A2A Swarm pattern as we built it maps to the reference pattern on the architecture center. The Foundry deployment topology maps to the reference. The vault edge maps to the reference. The LEDGER substrate maps to the reference. When the Microsoft CSA walked the AT&T CTO's architecture team through a fidelity review at five weeks, the review confirmed the Wave-1 build is reference-pattern-true. That fidelity is what makes the Microsoft platform engagement defensible. We did not improvise on Microsoft's platform. We built against Microsoft's published patterns. The Wave-1 build is the architecture center reference, instantiated.

**RASHMI:** And the Independence-language hygiene. The Wave-1 charter Schedule B is in production now. How is the language holding.

**KEVEN:** Same way it was set at M0. *Microsoft platform engagement* every time. The Schedule B addendum to the Wave-1 charter uses the canonical phrase. The quarterly architecture review document with AT&T uses the canonical phrase. The TMT Delivery Architect's architecture readout uses the canonical phrase. The DMTSP Microsoft Platform Lead's coordination notes with the Microsoft CSA use the canonical phrase. The Risk Advisory Partner reviews the documents every fortnight for drift. There has been no drift. The platform is recommended on the merits — capacity, latency, throughput, fidelity. The conversation Microsoft has with AT&T about Microsoft's own commercial relationship sits on Microsoft's paper, in a room Deloitte is not in. The Deloitte page describes the Microsoft platform engagement and nothing else. That posture has held through six weeks of shadow.

**RASHMI:** And the Microsoft CSA's role in M2. What is it concretely.

**KEVEN:** The Microsoft CSA sits beside the DMTSP Microsoft Platform Lead at the joint architectural readouts with AT&T's CTO organisation. The CSA owns the reference-pattern fidelity conversation from the Microsoft platform side — *here is the architecture-center pattern, here is how we have implemented it, here are the observed metrics against the reference targets.* The Platform Lead owns the engagement-language posture from the Deloitte side — *here is how we describe what we are doing, here is how we keep the Independence-clean frame.* They sit beside each other. They coordinate. The conversations they have with AT&T are technical platform-engagement conversations. Whatever Microsoft is doing commercially with AT&T is happening through the Microsoft AE's own channel into AT&T's CTO organisation, on Microsoft's paper. The CSA and the Platform Lead are in the architecture conversation, not the commercial one.

**RASHMI:** And the M2 readout to AT&T at the end of the milestone. What does that document carry.

**KEVEN:** The CAF utilisation curves. The Foundry throughput curves. The vault throughput curves. The latency distributions. The HOM-99 suppression analysis. The reference-pattern fidelity confirmation. The Schedule B Independence-language section, reaffirmed. One document. Clean. The AT&T CTO reads it. The Microsoft platform engagement holds at M2 because the platform actually held — under real load, against real telemetry, with reference-pattern fidelity, with Independence-clean language. The M1 commitment is now an M2 record.

**RASHMI:** Monday morning. What does the seller do?

**KEVEN:** Monday morning the DMTSP Microsoft Platform Lead has the next joint architectural readout with the Microsoft CSA on the calendar. The Risk Advisory Partner has the Schedule B language-hygiene review for the quarter scheduled. The TMT Delivery Architect has the M2 readout document in version one, draft circulating internally before it goes to the AT&T CTO.

### The validation gate

**RASHMI:** Picture the Risk Advisory Partner on a Friday afternoon, four months after the shadow launch, the M2 gate-status file open in front of her. The office is quiet — late Pacific afternoon, the after-five lull. Five items on the gate. Each one has a small green check, a date stamp, an artifact reference. The AT&T NOC engineering lead's shadow-window summary sits attached to item one. The AT&T Security office's vault-and-KMS sign-off sits attached to item two. The AT&T mobile-app beta build with "My Channels" UX live sits attached to item three. The AT&T Billing team's bill-insert approval sits attached to item four. The TMT Delivery Architect's LEDGER substrate operational confirmation sits attached to item five. The Partner is composing the M2 gate-close note to the TMT VP and the M&P Leader. Two paragraphs. The first paragraph names the five items and the date each one closed. The second paragraph says — *M2 is closed. M3 unlocks Monday.* She sends. M2 is done.

**KEVEN:** Walk the five gate items. Specifically.

**RASHMI:** Five items. One — HOM-01 through HOM-08 plus HOM-99 deployed in the AT&T shadow environment, running against four quarters of AT&T-anonymised IoT data, telemetry-clean for the full shadow window. Two — the per-household vault and the customer-held KMS in production, validated by the AT&T Security office and the AT&T Privacy office, with vault-residency report on file. Three — *My Channels* UX live in the AT&T mobile app beta tier, with the bill insert and line-item rendering validated against the existing AT&T streaming-bundle UX precedent and approved by AT&T Billing. Four — the bill insert and line-item rendering approved by AT&T Billing — same artifact as part of three but called out separately because the Billing approval is its own gate. Five — the audit row and LEDGER substrate operating end-to-end, with the joint architectural readout from the Microsoft CSA and the DMTSP Microsoft Platform Lead delivered at AT&T confirming CAF substrate validation, A2A Swarm pattern fidelity, and LangFuse trace-volume readouts.

**KEVEN:** And the gate failure modes. Pick one and walk it.

**RASHMI:** Item two. The vault and customer-held KMS validation. The failure mode is — AT&T Security finds an audit pattern they cannot reconcile, the vault-residency report comes back amber because the customer-held key model has an edge case the Security office wants closed before sign-off. The mitigation is — the TMT Delivery Architect and the AT&T Security architect have been in fortnightly stand-ups through the entire shadow window. The edge cases get surfaced early. The sign-off at gate is a confirmation of what has already been worked through, not a first encounter with the model.

**KEVEN:** Item three. The *My Channels* UX in the mobile app beta. The failure mode is — the AT&T mobile-app product team has a release-train cadence and the *My Channels* surface misses the window the M2 gate requires. The mitigation is — the TMT Account SE wired the *My Channels* surface into the existing streaming-bundle UX framework, so the release-train acceptance was already pre-conditioned. The work plugs into a known cadence. The beta tier ships in the regularly-scheduled release.

**RASHMI:** Item five. The audit row and LEDGER substrate. The failure mode is — the LEDGER substrate is operational but the joint architectural readout cannot land because the Microsoft CSA and the DMTSP Microsoft Platform Lead cannot get the AT&T CTO's architecture team on a single calendar before gate. The mitigation is — that readout was scheduled at M1, six months in advance. It happens. The calendar is the discipline.

**KEVEN:** And the seller-team risk on the gate. The pursuit team has been running the weekly Practice-leads sync the entire shadow window. The cadence has held. When the gate-close note goes, it is not heroic. It is the consequence of the cadence.

**RASHMI:** Monday morning. What does the seller do?

**KEVEN:** Monday morning of the week after the gate closes, the M3 sub-section of the tracker opens. The first plug-in channels — Travel, Retail, Media — start their commercial conversations in earnest. The Home reference pack is published as the template. The Microsoft platform engagement is the operational ground truth. M2 is done. M3 is the next chapter.

### A reading I want to do

**RASHMI:** I want to recommend a primary source — the AT&T NOC public engineering posts and the AT&T Connected Home product-team blog content from the eighteen months prior to the shadow launch. Not the marketing pages. The engineering posts. The ones where AT&T's own engineers describe how they think about reliability, the bill experience, the connected-home device coordination, the privacy posture they expect their platforms to carry. The reason I want listeners to read those is that the Default Home Channel architecture is operating against an institutional set of expectations that AT&T's engineering culture has written down in public, post by post, over the eighteen months before our shadow launch. If you have read those posts, the choices we made on the architecture — the customer-held KMS model, the operator-console mediation in shadow, the bill-anchored trust frame — feel like the obvious choices. If you have not read those posts, the choices feel arbitrary. Make them obvious for yourself before the next pursuit conversation, because the AT&T CTO's team is reading those posts as their own canon. You should be too.

**KEVEN:** And I will add — read alongside that the Microsoft Azure architecture-center reference patterns for multi-agent runtime composition on Foundry with vault integration. The reference patterns describe the same A2A Swarm topology, the same Foundry deployment model, the same vault edge pattern we instantiated for the AT&T shadow build. Read them at M2 because the platform-engagement readout we are about to deliver to the AT&T CTO is structured against those patterns. The reference is the canon. The implementation is the instantiation. If you read the reference, the readout reads as confirmation. If you do not read the reference, the readout reads as a list of metrics. Make it confirmation. The Microsoft platform engagement reads cleaner when you have read the architecture-center material.

### One disagreement

**KEVEN:** The disagreement is about whether M2 should end with a small live cohort. I argued — and I will name it — that M2 should close with a fifty-household live cohort, real customers consented in, real recommendations delivered in a tightly bounded way, so that we have real customer-facing experience data before M3 plug-in channels start their commercial conversations. The argument is that shadow is honest about the platform but silent about the customer experience, and that going from zero customers to a Wave-1 plug-in motion in M3 with no live-customer feedback at all is asking the M3 anchors to commit on a forecast rather than evidence.

**RASHMI:** And I argued — and I will name it — that M2 should be shadow-only. The Wave-1 charter with AT&T is built around the shadow-window proof point. The AT&T Security office sign-off is built around the shadow-window evidence. The AT&T Privacy office sign-off is the same. The institutional permission slip AT&T's CTO is going to walk to his CEO is the shadow-window record — *ninety days of clean shadow against real households, no customer exposure, audit-clean, vault-clean.* That is a clean story. The moment we put fifty live households into M2, we have introduced a customer-exposure surface that the AT&T Privacy office has not yet pre-cleared. The institutional clearance for live customer exposure is M3 work, after the Wave-1 plug-in channels are signed and the customer-facing posture is agreed across the anchor set. M2 live cohort exposure breaks the M2 gate frame.

**KEVEN:** And we converged. Shadow-only at M2 for the gate frame, but with a pre-staged small cohort selection. Five thousand AT&T households identified, consented in advance under the M2 shadow-window consent posture, opted into the *My Channels* beta tier, sitting ready in a cohort-management table waiting for an M3 flip-switch. The moment M3 plug-in anchors sign and the customer-facing posture is agreed, the cohort flips from shadow-eligible to live-eligible. No selection scramble in M3. No fresh consent motion. The cohort is pre-staged. The flip is a configuration change, not a recruitment exercise.

**RASHMI:** I can live with that. The discipline is that the pre-staged cohort sits in shadow until the M3 institutional clearances close. The cohort is not a sneak-live. It is a ready-list. The line is hard and it is named — the customer-facing flip happens at M3, not at M2, even though the cohort is ready at M2.

**KEVEN:** And the way the pre-staged cohort gets sold to AT&T's Privacy office is exactly that — a ready-list under shadow-window consent, eligible to flip when the M3 clearances close. The Privacy office signs off on the ready-list at M2 because it is shadow-compliant. The Privacy office signs off on the flip at M3 because the M3 clearances close. Two signatures. Two gates. Honest sequencing.

**RASHMI:** Pre-staged-cohort-at-M2 plus institutional-flip-at-M3. That is the converge. The fifty-live-cohort-at-M2 frame is off the table. The ready-list frame replaces it.

### The quote-and-react

**KEVEN:** I want to read a line from the Microsoft Azure architecture center, from the reference pattern on multi-agent runtime composition with vault-integrated audit. The line, as the architecture center material states it: *"The reference pattern places the vault at the trust boundary between the agent fleet and the audit substrate, with the encryption key held outside the platform's custody, so that audit integrity is independent of platform compromise."*

**RASHMI:** And the react. That sentence — *"the encryption key held outside the platform's custody, so that audit integrity is independent of platform compromise"* — is exactly the property the AT&T Security office is validating at the M2 gate. The customer-held KMS model is not a Deloitte invention. It is the Microsoft Azure reference pattern for multi-agent runtime composition with vault-integrated audit, instantiated for the AT&T anchor with AT&T as the key-holder. When the AT&T CTO walks into a board update and says *the audit integrity is independent of platform compromise,* he is reading the architecture center back to his board. He is reading published canon. The architecture we built rides on a reference pattern that exists outside our build. That is what makes the Microsoft platform engagement defensible at M2. We did not invent the property. We instantiated the reference. The AT&T Security office can validate against the canon because the canon is public. That is the quote, and that is why it is the quote for M2.

### What to carry forward

1. Default is the pattern. The Home Channel substrate is what every plug-in channel rides on, and getting it right at M2 — the meta-pack tables, the reference pack documentation, the configuration surfaces, the shared vault and LEDGER and Foundry envelope — is what makes M3, M4, and the wave-2 plug-ins land cleanly. Build the Default at the substrate level. Do not build a single-channel pilot.
2. Shadow mode is the platform's contract with the anchor. Real load, real telemetry, suppressed delivery — that contract is what makes the AT&T CTO comfortable enough at M2 to flip to live at M3. Hold the line: shadow-only at M2 for the institutional clearance, with a pre-staged ready-list cohort waiting for the M3 flip. Do not let a live-cohort temptation break the M2 gate frame.
3. The Microsoft platform engagement either holds at M2 or it does not. CAF capacity, Foundry throughput, vault throughput, reference-pattern fidelity, Independence-clean language — every property has to hold on real load against real telemetry. The M1 commitment is paper. The M2 reading is the record. Walk into the AT&T CTO's M2 readout with the record, not the paper.

## Further reading

- The `APEX-Agentic-Telco-Olympics-Tracker` HTML, M2 section — the milestone-arc artifact that drives the M2 deliverables and the gate items.
- AT&T NOC public engineering posts and AT&T Connected Home product-team engineering content — the institutional engineering culture the Default Home Channel architecture is operating against.
- The Microsoft Azure architecture-center reference patterns for multi-agent runtime composition with Foundry and vault-integrated audit substrate — the published canon the Wave-1 build instantiates.
- AT&T Security and Privacy public posture statements — the institutional frames the customer-held KMS model and the per-household vault residency report are pre-cleared against.
- The marketplace meta-pack reference documentation — Channel, ChannelSubscription, partner_directory — the tables stood up at M2 that the M3 plug-in channels subscribe into.
- The Risk Advisory Schedule B Independence-language template — the firm's reference for the *Microsoft platform engagement* phrasing carried into the Wave-1 charter and reaffirmed at the M2 readout.
