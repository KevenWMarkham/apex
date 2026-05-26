# Episode 03 · The 24-Step Agent and the Microsoft Platform

**Builds on:** Toyota Eps 1-2 (the idea + four data domains) · Services Podcast Ep 4 (the MCP boundary and agent runtime) · Services Podcast Ep 6 (Purview + LEDGER hash chain) · AXLE Practice (ORCH-01 24-step orchestrator)
**Run time:** ≈ 32 minutes target
**Last updated:** 2026-05-14

---

## Cold Open

[Sound: a quiet office. Early morning. A faint HVAC hum. The soft chirp of a monitor waking up. The clack of a coffee cup set down on a desk.]

**MIA:** I want to start at seven o'clock on a Wednesday morning. Not eleven o'clock on a Tuesday night, like we opened Episode 1. *Wednesday morning. Plant Quality office at Toyota Motor Manufacturing Kentucky. Daylight just starting through the blinds.*

The same quality engineer from Episode 1 has come in early. She has not been here all night. She had dinner, she slept, she came in with coffee. *That itself is the story.* She opens her workstation. There is one tab waiting for her — the run log of the warranty agent that has been working on her warranty cluster since yesterday afternoon.

[pause]

**KEVEN:** And what she sees in the run log.

**MIA:** What she sees is twenty-four rows. *Twenty-four audit rows.* Each row is one step the agent took yesterday on her cluster — the sensor harness intermittent from Episode 1. Each row is hash-chained to the row before it. Each row has a replay token. Each row says, in plain language, *what the agent did, what data it touched, what it concluded, and what evidence supports the conclusion.*

She is not opening a black box. *She is opening an audit trail.* The agent's output is not just an answer. The agent's output IS the audit trail. The answer is one row in it.

[pause]

**KEVEN:** That's the whole episode.

**MIA:** That's the whole episode. *The audit trail is the product.* Not the by-product of the agent doing its work — the actual deliverable. Because without it, no Quality VP at Toyota signs off on an agent that touches a chargeback case. *With it*, the agent moves from interesting-demo to a tool that Quality and Legal and Finance can actually put their names next to.

**KEVEN:** And she reads the rows.

**MIA:** She reads them. *In order.* Row one — the agent picked up the cluster signal at three-twelve PM yesterday. Row four — the cohort was identified. Row eight — the cohort by station by tool lattice was composed. Row twelve — the statistical-significance tests on supplier lot landed. Row sixteen — the validation pass against control populations. Row twenty — the chargeback evidence package was drafted. *Row twenty-four — the package was written to the audit ledger and is sitting in her queue for review.*

Each row took seconds. The chain of twenty-four took about twelve minutes wall-clock yesterday afternoon. *She slept through the work.* Now she comes in and reads it the way she would have read a colleague's investigation notes — except the notes are forensically tight, every join is explicit, and every conclusion is traceable to its evidence.

**KEVEN:** *The Zero Day Warranty Podcast. Episode Three. The 24-Step Agent and the Microsoft Platform.* I'm Keven Markham.

**MIA:** I'm Mia. Let's walk what's inside those twenty-four rows.

---

## The conversation

### What the Microsoft platform contributes here

**KEVEN:** Before we open the chain, I want to name the platform pieces explicitly. *Three Microsoft components do the load-bearing work in this scenario.* We have referenced all three across Episodes 1 and 2. Now they get named with their roles.

**MIA:** Go.

**KEVEN:** *Microsoft Fabric — the unified data layer.* The four-domain canonical foundation we built in Episode 2 lives here. OneLake underneath, medallion on top. Bronze for raw landing, Silver for the canonical schemas across the four domains, Gold for the per-VIN joinable composite views the agent reaches into. *Fabric is the substrate.* When the agent asks "what does the world look like for this VIN?" Fabric is the layer that answers in seconds because the join has already been pre-composed at Gold.

**MIA:** And the second.

**KEVEN:** *Microsoft Agent Framework — the agent runtime.* Agent Framework is the SDK — the authoring layer where the agent's reasoning chain is built. The runtime hosts on *Azure AI Foundry Agent Service.* So when you hear "Agent Framework" and "Foundry" in the same paragraph, that's not two different things. *Agent Framework is the how. Foundry is the where it runs.* The 24-step chain is composed in Agent Framework. The execution is on Foundry.

**MIA:** And the third.

**KEVEN:** *Microsoft Purview — governance and audit.* Purview sits over the entire data and agent estate. Lineage, classification, access policy, audit. *The LEDGER hash chain — what the agent writes for every decision — rides on Purview.* The Purview audit echo mirrors every row into Purview's data-estate catalog. And *DSPM for AI* — Data Security Posture Management for AI — is Purview's continuous posture view over the agent workload itself.

**MIA:** Three components. *Fabric for the data. Agent Framework on Foundry for the agent. Purview for the audit.* And the framing matters.

**KEVEN:** *The framing matters.* These are the right components on the technical merits — Fabric is the right data fabric for a per-VIN four-domain join, Agent Framework is the right runtime for a long-chain audit-ready agent, Purview is the right governance plane because the audit chain has to live somewhere that Quality and Legal and Finance already trust. *Deloitte recommends these specifically because they fit the problem.* Toyota licenses Microsoft directly. We'll come back to that posture explicitly in a few minutes.

**MIA:** And one more thing about the platform piece — *nothing in this stack is bespoke to Toyota.* The data foundation aligns to the Common Data Model for Manufacturing inside Microsoft Industry Cloud for Manufacturing. The agent runtime is the same Agent Framework Microsoft ships to every Foundry tenant. The audit chain rides on Purview the same way it does for every Purview-governed estate. *Toyota benefits from being inside the platform pattern, not from a custom build.* That matters for adoption — and it matters for lifecycle.

**KEVEN:** Lifecycle is the point I want to expand for a second. *When Toyota signs up for this stack, Toyota inherits the upgrade path Microsoft is investing in.* Agent Framework's reasoning capabilities improve. Fabric's Gold-view performance improves. Purview's classification taxonomy improves. *Toyota does not have to fund any of those improvements.* They arrive on the platform release cadence. The agent the Toyota team is operating in year three is meaningfully more capable than the agent operating in year one — at the platform's expense, not Toyota's.

**MIA:** That compounds. The first deployment is the hard one — the data foundation, the canonical Silver, the first Gold views, the first agent chain. *Once that scaffolding stands up, the second agent is materially cheaper. The third is cheaper still.* Predictive maintenance, production planning, supplier-quality coordination — every one of them rides on the same Silver foundation, reuses the same audit chain, reuses the same Purview classification. *The first agent pays for the scaffolding. The next ten ride on it.*

### The 24-step agent chain — six phases, four steps each

**KEVEN:** Now the chain itself. *Twenty-four steps.* I want to walk them in groups — six phases, four steps each. Not because the chain is rigidly structured that way internally, but because the phases are how the work is conceptually organized, and that's how I think the listener should hold it.

**MIA:** Six phases of four. Walk them.

**KEVEN:** *Phase one — Detect.* Steps one through four. The agent picks up the warranty cluster signal. The signal comes off the connected-vehicle warranty data domain — the domain we walked in Episode 2 — when the failure-mode volume crosses a threshold. *Step one is the signal pickup.* Step two scopes the cohort — which part, which failure mode, which severity. Step three pulls the VIN list for the affected cohort. *Step four captures the cluster fingerprint* — a hashable summary of the cluster's shape, which becomes the first row of the audit chain. From this point forward, every later step in the chain references that fingerprint. *The cluster has been registered.*

**MIA:** Phase two.

**KEVEN:** *Phase two — Trace.* Steps five through eight. The agent walks back to the vehicle build record domain per VIN. *Step five extracts the build-week distribution of the affected VINs.* If the cluster is concentrated in specific build weeks, that's a strong signal. Step six identifies the over-represented build weeks against the baseline. Step seven, within those hot build weeks, extracts the per-station, per-tool, per-shift distribution. *Step eight composes the cohort by station by tool by supplier-lot lattice* — the four-dimensional grid the agent is going to reason against. *The candidate causal dimensions are now named.*

**MIA:** Phase three.

**KEVEN:** *Phase three — Compose.* Steps nine through twelve. The agent joins in the quality-events-on-the-line domain and the assembly-line-telemetry domain. *Step nine joins quality event records — the inspections and measurements during the build.* Step ten identifies the SPC anomalies that preceded the hot build weeks — the statistical-process-control signals that were drifting but had not yet crossed alarm thresholds. *Step eleven joins assembly telemetry — the tool traces, the equipment state.* Step twelve correlates tool calibration drift against the hot-station defects. *Statistical-significance scoring against each candidate causal dimension. Confidence intervals. The agent now has a ranked hypothesis space.*

**MIA:** Phase four.

**KEVEN:** *Phase four — Validate.* Steps thirteen through sixteen. The agent cross-checks against control populations. *Step thirteen extracts the supplier lot codes installed across the hot VIN population.* Step fourteen computes the supplier-lot warranty rate against baseline lots. *Step fifteen runs the statistical test on supplier-lot attribution significance* — is this lot demonstrably worse than its peer lots in the same window, or is it within normal variance. Step sixteen ranks the cohort by station by supplier-lot interactions by significance. *Selection-bias checks happen here too — the agent is checking that the cohort itself isn't a sampling artifact. And the operator-cohort dimension is handled with the safeguards we built in Episode 2 — surfaced at cohort level, never as individual blame.*

**MIA:** Phase five.

**KEVEN:** *Phase five — Recommend.* Steps seventeen through twenty. The agent drafts the chargeback evidence package. *Step seventeen generates the root-cause hypothesis with confidence intervals.* Step eighteen builds the full evidence package — cohort definition, statistical tests, supporting raw data, audit chain references. *Step nineteen computes the chargeback dollar exposure per supplier lot* — this is where the dollar number comes from. Step twenty generates the supplier chargeback documentation in the shape Supplier Quality and Finance need it. *The cohort by station by tool interaction the quality engineer reviews is now surfaced.*

**MIA:** And phase six.

**KEVEN:** *Phase six — Attest.* Steps twenty-one through twenty-four. *Step twenty-one triggers the NHTSA Early Warning Reporting check if applicable* — the regulatory submission posture. Step twenty-two routes the package to the Quality leader for human review. *Step twenty-three writes the final decision and rationale to the audit ledger as a hash-chained row.* Step twenty-four notifies downstream owners — corrective-action teams, dealer advisory channels. *Microsoft Purview audit echo. Ready for offline replay by an External Audit Reviewer.*

**MIA:** Six phases. Four steps each. *And — the rhythm I want the listener to hold — every step writes an audit row.* Not a log line. *An audit row.* Log lines are diagnostic; audit rows are evidence. *Every decision the agent makes is replayable.* That replayability is what we're going to build on for the rest of this episode.

**KEVEN:** *Every decision the agent makes is replayable.* Hold that. The chain length — twenty-four — is going to come up again when we get to the disagreement. There is a reason the chain is twenty-four and not eight.

### HITL — the quality engineer reviews, the agent surfaces

**MIA:** Now the human-in-the-loop piece. *Where does the human enter the chain.*

**KEVEN:** Right between phase five and phase six. *The HITL gate sits at the boundary.* Phase five produces a draft chargeback evidence package and surfaces the cohort by station by tool interaction. *Phase six does not start until the human signs.* The quality engineer — or in the bigger cases, the Quality Director — reviews the package. She accepts, modifies, or rejects.

**MIA:** Walk what each of those looks like.

**KEVEN:** *Accepts* — she reads the agent's reasoning, agrees with the cohort definition, agrees with the statistical conclusions, signs the package as written. The chain moves to phase six. *Modifies* — she reads the reasoning and disagrees with a specific element. Maybe the agent ranked the wrong dimension as most causal; maybe the supplier-lot attribution needs to be tightened; maybe the cohort window should be expanded by one build week. *She amends the package. The amendment itself becomes an audit row.* The chain moves to phase six with the amendment. *Rejects* — she reads the reasoning and concludes the cluster needs more investigation, or that the agent missed a dimension. *She kicks it back.* The agent doesn't argue; the agent re-runs phases three through five with whatever new constraint she's given. The rejection itself is an audit row.

**MIA:** And the cultural posture.

**KEVEN:** *The cultural posture is the operator-dignity rule from Episode 1, applied to the quality engineer.* The agent never autonomously initiates an external chargeback. *Never.* The chargeback package is only finalized after the human's sign-off. The agent's role is to remove the reconciliation toil and surface the evidence; *the judgement remains with the human.* TPS culture is preserved. The senior quality leader is still the protagonist of the warranty narrative — exactly as she was at her desk at eleven o'clock at night in Episode 1. The agent just gives her her hours back.

**MIA:** And the practical mechanism — how does the package get to her.

**KEVEN:** *Microsoft Teams plus Power Automate.* When phase five completes, the package gets surfaced in Teams as an actionable Adaptive Card. *Approve, amend, or deny in-line.* No new tool to learn. No new login. The Quality Director's daily workflow already includes Teams; the agent meets her where she works. The Adaptive Card includes the cohort summary, the dollar exposure, the top three causal dimensions ranked, and a link into the full audit chain if she wants to drill in. *She often does.*

**MIA:** And the identity piece. The agent acts on behalf of a person; it isn't anonymous.

**KEVEN:** *Microsoft Entra ID — Agent ID plus Workforce identity.* Every agent has its own managed identity. Every action the agent takes is recorded against that identity *and* against the person on whose behalf the agent is acting — *on-behalf-of, in the identity vocabulary.* When the Quality Director reviews a package, the audit row shows the agent did the reasoning, and shows the Director signed the conclusion. *Both signatures are present.* Conditional access policies on the supplier-data scope mean the agent only sees what its principal is authorized to see. *No backdoor scope. No service-account workaround.* The agent is an identity in Toyota's directory like any other principal — with the access it is supposed to have, audited the same way.

**MIA:** And one detail I want to make sure is on tape — *the agent surfaces the package; the agent does not push it through.* The package sits in her queue until she acts. *The human's clock controls.* If she needs three hours, three hours. If she needs three days for a particularly complex cluster, three days. *The agent has compressed the eight-to-twelve-weeks of toil into minutes; the human's judgement-time is preserved.* That's the right division of labour.

### The $4.2M / $2.8M / 340% calculation walked

**KEVEN:** Now the math. I have been pointing at the reference numbers since Episode 1 — *$4.2M, $2.8M, 340%.* Let me walk where each number comes from. *And same disclaimer every time* — these are reference-scenario numbers. They come from a representative plant model. They are not Toyota-specific results.

**MIA:** State the reference scenario.

**KEVEN:** *Reference plant — five thousand vehicles produced per week.* That's representative of a high-volume North American auto plant; Toyota Motor Manufacturing Kentucky runs higher than that, Toyota Motor Manufacturing Indiana runs in that range, Mazda Toyota Manufacturing in Huntsville is closer to that. *Five thousand a week is a reasonable midpoint.*

The affected window is three build weeks — weeks 12 through 14. *Three weeks times five thousand vehicles equals fifteen thousand vehicles in the window.* Of those, the suspect supplier lot has a penetration of about forty percent — six thousand vehicles got parts from the lot. *Six thousand is the affected population.*

**MIA:** And the per-vehicle warranty cost.

**KEVEN:** *Industry-average warranty cost per vehicle, mid-range US non-luxury — about three hundred dollars.* That's the baseline cost the average vehicle generates in warranty claims over its warranty life. *The suspect lot produces vehicles that experience claims at roughly two-point-three times the baseline rate.* The lot has a defect; the defect drives extra claims; the extra claims drive extra cost.

**MIA:** Walk to the $4.2M.

**KEVEN:** *Six thousand affected vehicles times the incremental warranty cost per affected vehicle.* The incremental cost is the difference between the bad-lot rate and the baseline — three hundred dollars times two-point-three, minus three hundred. *That's three hundred ninety dollars of extra cost per affected vehicle.* Six thousand times three-ninety equals two-point-three-four million dollars.

But that's not the full $4.2M number. *That's the base impact.* On top of it, you have the *extended-period failure tail* — vehicles that haven't yet experienced the failure mode but will, across the three-year warranty curve. That tail adds roughly an eighty-percent multiplier. *Two-point-three-four million times one-point-eight equals about four-point-two million.* That's the $4.2M attributable warranty cost.

**MIA:** And the $2.8M.

**KEVEN:** *Of that $4.2M, how much can be recovered from the supplier as a chargeback.* The reference assumption is *sixty-seven percent recovery rate* — given a forensic-quality evidence package the agent produced. Four-point-two million times sixty-seven percent equals two-point-eight-one-four million. *Round to $2.8M.* That's the recovered chargeback.

**MIA:** And the 340%.

**KEVEN:** *Now the comparison.* The manual-investigation baseline — given the slower investigation timeline and the weaker evidence package the manual process produces — typically recovers around *fifteen percent.* Four-point-two million times fifteen percent equals six hundred thirty thousand dollars. *The agentic version recovers two-point-eight million.* The improvement, computed as the percentage gain over the baseline — *two-point-eight-one-four minus six-thirty divided by six-thirty* — is about three hundred forty-seven percent. *Rounded to 340%.* That's where the 340% headline comes from.

**MIA:** And the two reasons the recovery rate is materially higher under the agent.

**KEVEN:** *Two reasons. First — evidence quality.* The manual process produces a chargeback case that is roughly defensible — the cohort, the dollar exposure, an attribution argument. *The agentic process produces a chargeback case that is forensically defensible* — every join is hash-chained, every conclusion is replay-validated, every statistical assumption is explicit. Suppliers contest weak evidence; they contest forensic evidence very differently. *Second — speed.* Cases recovered inside ninety days of the failure carry materially higher recovery rates than cases recovered nine months later, when invoices are paid and quarters have closed and the supplier's leverage shifts. *The agentic timeline closes inside the ninety-day window. The manual timeline rarely does.*

**MIA:** And the Account Team posture on these numbers.

**KEVEN:** *Reference scenario. Every time.* The $4.2M is not a Toyota-specific projection. The $2.8M is not a committed recovery. The 340% is not a guaranteed improvement. *These are the framework's reference figures from a representative plant model.* Toyota will compute its own numbers if and when a Business Value Assessment moves forward. That assessment would take four to six weeks of joint discovery to baseline against actual TMNA current-state metrics. The reference numbers are the conversation starter. *The Toyota-specific numbers come later.*

**MIA:** Said the same way every time. *The discipline matters.* The moment somebody on the Account Team quotes a Toyota-specific number off the reference scenario, two bad things happen. First — it stops being a discovery conversation and starts being a sales conversation. Second — it puts a number on Toyota's CFO desk that wasn't computed against Toyota's actual data, which is the wrong way to start a Business Value Assessment. *The reference numbers open the door. Toyota's numbers walk through it.*

### LEDGER hash chain and Purview audit echo

**KEVEN:** Now the audit chain. We've been pointing at it since Episode 1; let's walk it properly.

**MIA:** Walk it.

**KEVEN:** *Every step the agent takes writes one audit row.* Twenty-four steps, twenty-four rows. Each row contains fourteen fields — and I'm not going to enumerate the fourteen because the listener doesn't need that level of detail on tape; the important thing is the row is *structured.* It captures what the agent did, what data it touched, what conclusion it drew, what evidence supported the conclusion, who the agent was acting on behalf of, when it happened, and a cryptographic hash that links it to the previous row.

**MIA:** That hash link is the critical piece.

**KEVEN:** *That's the critical piece.* Each row's hash is computed from the row's contents plus the previous row's hash. *Which means the order of decisions is cryptographically preserved.* You cannot silently edit row twelve after the fact without breaking the hash on rows thirteen through twenty-four. *The chain is tamper-evident by construction.* If someone tries to alter the evidence chain after the agent has finished its work, the alteration is visible in the next hash computation.

**MIA:** And the replay token.

**KEVEN:** *Replay-token validated means an External Audit Reviewer can run the same reasoning offline and get the same answer.* The replay token captures the inputs the agent saw — the Gold-view contents at the moment the agent read them, the cohort definition, the statistical parameters. An auditor can take the token, re-run the same agent against the same inputs, and confirm the answer matches. *If the answer doesn't match, the chain didn't hold.* That replay capability is what makes the audit chain useful, not just decorative.

**MIA:** And the Purview piece.

**KEVEN:** *Microsoft Purview provides the audit echo.* The same row is mirrored into Purview's data-estate catalog for governance — alongside the lineage records, the access logs, the data-classification metadata. *Purview is the system of record for governance.* When a compliance reviewer asks "what data did this agent touch and under what authority" — Purview answers, with the audit row referenced. *The LEDGER chain and the Purview echo together are the audit-ready posture.* Episode 1 named it the load-bearing wall; this is the wall up close.

**MIA:** And why this matters specifically for Toyota.

**KEVEN:** *Toyota Quality, Toyota Legal, and Toyota Finance all need to sign off on a chargeback case before it leaves the building.* Each of those three signatures rests on the evidence package being defensible. *Without the audit chain, the agent is interesting but unsignable.* With it, the agent is a tool those three functions can actually adopt. *That's not a tagline. That's the architectural reason this scenario can land in the warranty path at all.*

### DSPM for AI — data security posture for AI workloads

**KEVEN:** And the CISO conversation. DSPM for AI.

**MIA:** Walk it briefly.

**KEVEN:** *Data Security Posture Management for AI — DSPM for AI — is the continuous posture view over the agent workload.* It's a capability inside Microsoft Purview. It answers — *what data is the agent seeing right now, where is the agent running, with what consent, against what sensitivity classifications.* Continuously. Not at a point in time. *Continuously.*

**MIA:** And why that matters at Toyota specifically.

**KEVEN:** *Because both the connected-vehicle data and the warranty-claim data have PII implications.* Connected-vehicle data can tie to a specific customer's driving behaviour. Warranty data can tie to a specific customer's repair history. *Toyota's CISO is responsible for those data classes meeting privacy and security obligations across jurisdictions.* The CISO needs not a point-in-time attestation that says "as of last quarter, the agent was compliant." She needs the continuous view — *as of right now, the agent is seeing this data, in this region, with this access policy, and here's the posture.*

**MIA:** And the integration.

**KEVEN:** *DSPM for AI integrates with the same Purview audit echo we just walked.* The audit rows the agent writes are visible to DSPM. The data classifications the agent's Gold views inherit from Silver are visible to DSPM. *The CISO gets one console.* That's the operational value — not another tool to monitor, the same tool extended to cover the AI workload. *That matters for adoption inside a security organization that already has too many consoles.*

**MIA:** Brief on DSPM. *Continuous posture, one console, ties into the same audit chain.* That's the CISO frame.

### Independence-from-Microsoft posture — explicit

**KEVEN:** And now the posture I want stated more cleanly than anywhere else in the series. *Independence from Microsoft.*

**MIA:** Said cleanly.

**KEVEN:** *Deloitte recommends.* When we say Microsoft Fabric is the right data foundation, that recommendation is on the technical merits — Fabric is the right fabric for the per-VIN four-domain join, and Toyota Connected already runs on Azure so the architectural fit is natural. *That recommendation is not influenced by any commercial relationship between Deloitte and Microsoft.* No compensation flows from Microsoft to Deloitte for influencing Toyota's platform choice.

**MIA:** And the contracts.

**KEVEN:** *Two contracts. Always.* When Toyota licenses Microsoft Fabric, Microsoft Agent Framework, Microsoft Purview — *Toyota contracts with Microsoft directly.* Microsoft licensing flows on Microsoft paper between Microsoft and Toyota. *Deloitte does not resell Microsoft licenses. Deloitte does not mark up Microsoft licenses. Deloitte does not take margin on Microsoft licensing flowing to Toyota.*

When Toyota engages Deloitte for the services — the architecture work, the implementation, the change management, the Account Team continuity — *Toyota contracts with Deloitte directly.* Deloitte paper, Deloitte and Toyota. *Two separate agreements.*

**MIA:** And the words we don't use.

**KEVEN:** *We don't use the language of commercial coupling between Deloitte and Microsoft for this work* — because there isn't any. The recommendation, the licensing relationship, and the services relationship are three separate things. *The recommendation is Deloitte's, on the merits.* The licensing relationship is between Microsoft and Toyota, on Microsoft paper. The services relationship is between Deloitte and Toyota, on Deloitte paper. *Three things. Three actors. Two contracts. Clean separation.*

**MIA:** And the reason to state it this cleanly on tape.

**KEVEN:** *Because a Toyota listener should hear the model stated, not infer it.* The Sellers Podcast Episode Two — *The Commercial Arc* — walked the broader framework for this posture across all of Deloitte's Microsoft Practice work. *This podcast adopts that frame and names it specifically for Toyota.* If a Quality VP at Toyota listens to this episode, she should be able to repeat the model back accurately to her own colleagues. *Deloitte recommends. Toyota contracts with Microsoft directly. Toyota contracts with Deloitte directly. Two contracts. No compensation flows from Microsoft to Deloitte for the platform recommendation.* The Account Team should be fluent in stating it. So should the Toyota listener.

**MIA:** Said. *And said the same way in Episode 1, again here, and once more in Episode 5.* The repetition is intentional.

### A reading I want to do

**KEVEN:** I want to read briefly from Microsoft Learn — the governance documentation on agentic AI in production environments. Paraphrased.

**MIA:** Read it.

**KEVEN:** [reading, paraphrased from Microsoft Learn governance documentation, cross-referenced with Automotive News and Reuters Automotive coverage of agentic AI adoption in production manufacturing]

*"In production manufacturing environments, the audit trail is not the by-product of the AI agent's work — the audit trail is the product. The reasoning is delivered as a hash-chained sequence of decisions, each replayable, each governed. Without that posture, AI agents do not cross the threshold into production processes where Quality, Legal, and Finance must sign. With it, the same agents become tools those functions adopt because they can defend the agent's work to their boards, their regulators, and their suppliers."*

[pause]

**MIA:** *The audit trail IS the product.* That sentence is the whole point. The agent's answer — the chargeback recommendation, the cohort definition, the dollar exposure — is *one row of evidence inside a chain of evidence.* Strip the chain off and the answer doesn't survive the first supplier contest. Keep the chain — *forensically, replayably, continuously governed* — and the answer is something Toyota Quality leadership can put their name next to.

That is *exactly* why the architectural decisions matter as much as the agent decisions. *The Quality VP does not sign because she trusts the agent. She signs because she trusts the audit chain that surrounds the agent.* The chain is the trust unit. The agent is just a reasoning engine that produces rows for the chain.

### One disagreement

**MIA:** Pushback. *The 24-step chain feels long to me.*

**KEVEN:** Make the case.

**MIA:** Twenty-four steps is a lot. *Each step adds latency, adds complexity, adds an opportunity for the chain to break or for the listener to lose the thread.* I have been in operational meetings where elegant chains of eight steps get more buy-in than dense chains of twenty-four. *Why not compress?* The agent does the same conceptual work. The reasoning could be packaged as four big moves instead of six phases of four — detect, trace, conclude, attest. *Eight steps. Cleaner story.*

If the work fits in eight, fit it in eight. The audit posture doesn't depend on the chain length; the audit posture depends on the chain being hash-chained and replayable. *Eight chained rows are just as auditable as twenty-four.* And eight steps tells a cleaner story to a Toyota executive. *Why are we leaving twenty-four on the table when eight would land easier?*

**KEVEN:** Counter.

**MIA:** Counter.

**KEVEN:** *Because the chain length is the audit-posture's price tag, and we cannot afford to underpay.* Let me walk why. Eight steps means each step contains, on average, three of the things that today are happening as twenty-four separate decisions. *That bundling breaks replayability at the granularity an External Audit Reviewer needs.*

Take phase three — the compose phase. Steps nine through twelve do four distinct things — join quality events, identify SPC anomalies, join assembly telemetry, correlate tool calibration drift. *Four distinct decisions. Four audit rows.* If I compress those into one step — call it "join the operational signals" — the audit row contains four decisions bundled together. *If an auditor wants to replay the SPC-anomaly detection without re-running the telemetry join, she can't.* The replay token has to be re-issued at the granularity of the decision.

**MIA:** So the audit posture pushes the chain length up.

**KEVEN:** *The audit posture defines the chain length.* The unit of replayability is one row. The decisions inside the row have to be small enough that the row can be re-run independently. *Twenty-four is not gratuitous. Twenty-four is what the audit posture buys you.* Compress to eight and the chain looks elegant — but the External Audit Reviewer can't do her job at the resolution she needs. Twenty-four is the resolution that survives a Toyota Legal review, an NHTSA submission, a supplier contest.

**MIA:** And the latency.

**KEVEN:** *Latency is not the constraint.* The whole twenty-four-step chain runs in eight to twenty minutes wall-clock. Compressing to eight steps might save a couple of minutes. *Two minutes of savings against eight to twelve weeks of manual baseline is not the trade we should make.* The trade we should make is *every single decision the agent makes is independently replayable.* That's worth the chain length.

**MIA:** Reluctantly accepted. *Long chain is intentional, not gratuitous.* The chain length is the audit-posture's price tag. Pay it.

**KEVEN:** Pay it. *And when you walk a Toyota executive through the chain, you walk the six phases, not all twenty-four steps. The audit auditor walks the twenty-four. The executive walks the six.* Different audiences, same chain.

**MIA:** And there's a related point I want on tape. *The chain length is also what survives the regulatory submission.* When phase six writes to the audit ledger, the rows are formatted in a way that an NHTSA Early Warning Reporting submission can reference directly. The agent's twenty-four rows become the evidentiary substrate for the regulatory filing. *If the chain were eight rows long, the submission would have to bundle decisions, and bundled decisions are exactly what regulatory submissions cannot do.* The granularity is the regulatory posture.

**KEVEN:** *The granularity is the regulatory posture.* That's the other reason twenty-four is the right number. The chain has to satisfy three audiences at three resolutions — the Quality Director at six phases, the Toyota Legal reviewer at twenty-four rows, the NHTSA examiner at fourteen-field rows with hash links. *All three resolutions live in the same chain.* You don't replay it three different ways. You replay it once, and each audience reads at the resolution they need.

### What to carry forward

**KEVEN:** Three things.

**MIA:** Go.

**KEVEN:** *One — the Microsoft platform stack is named and tight.* Microsoft Fabric for the unified data layer. Microsoft Agent Framework on Azure AI Foundry for the agent runtime. Microsoft Purview for governance and audit, with the LEDGER hash chain as the unit of evidence and DSPM for AI as the continuous CISO posture. *Three components, one stack. Toyota already runs on Azure through Toyota Connected; this composes natively.*

*Two — the 24-step chain is six phases of four. Detect. Trace. Compose. Validate. Recommend. Attest.* The chain length is intentional — twenty-four is the audit-posture's price tag, and the price tag is the reason Toyota Quality leadership can adopt the agent in the warranty path at all. *The audit trail is the product, not the by-product.*

*Three — the human-in-the-loop is the quality engineer.* The agent surfaces the cohort by station by tool interaction; the human approves, modifies, or rejects. *The agent never autonomously initiates a chargeback.* TPS dignity is preserved. The senior quality leader from Episode 1 is still the protagonist; the agent has just given her her hours back.

**MIA:** And the Independence frame. *Said exactly the way it is meant to be said.* Deloitte recommends. Toyota contracts with Microsoft directly for the platform. Toyota contracts with Deloitte directly for the services. *Two contracts. No compensation flows from Microsoft to Deloitte for influencing Toyota's platform choice.* The Account Team should be fluent in this. A Toyota listener should be able to repeat it back.

**KEVEN:** Said exactly that way.

**MIA:** Next episode — *NVIDIA at the Station. Day-0 Prevention.* The inversion of Zero Day Warranty. Inline vision AI at the inspection station — Metropolis, DeepStream, Jetson, RAPIDS — and the two-fabric architecture that composes inline prevention at the station with the Microsoft data fabric upstream. *Day-Zero prevention catching the defect before it ever becomes a warranty claim.*

**KEVEN:** See you there.

[outro]

---

## Further reading

### Microsoft Learn

- **Microsoft Fabric** · [learn.microsoft.com/fabric](https://learn.microsoft.com/fabric/) — unified data layer, OneLake, medallion architecture
- **Microsoft Agent Framework SDK** · [learn.microsoft.com](https://learn.microsoft.com/) — agent authoring and orchestration
- **Azure AI Foundry Agent Service** · [learn.microsoft.com/azure/ai-foundry](https://learn.microsoft.com/azure/ai-foundry/) — managed agent hosting and runtime
- **Microsoft Purview** · [learn.microsoft.com/purview](https://learn.microsoft.com/purview/) — governance, lineage, audit, classification
- **DSPM for AI** · Microsoft Purview Data Security Posture Management for AI — continuous posture management for AI workloads
- **Microsoft Industry Cloud for Manufacturing** — manufacturing-aligned platform context
- **Microsoft Entra ID — Agent ID and Workforce** — per-agent managed identity and conditional access

### Industry coverage

- **Reuters Automotive** · agentic-AI adoption in production manufacturing
- **Automotive News** · [autonews.com](https://www.autonews.com/) — warranty-cost and supplier-quality coverage
- **SAE International** — production data governance and quality engineering standards
- **MIT Industrial Performance Center** — academic research on manufacturing AI deployment patterns
- **AIAG** (Automotive Industry Action Group) — supplier-quality and chargeback evidence-package conventions

### Agentic-AI and audit literature

- **Microsoft Learn — Agent governance with Purview** — hash-chained audit rows, replay tokens, DSPM
- **DSPM patterns** for production AI — continuous posture management across AI workloads
- **NHTSA Early Warning Reporting · 49 CFR Part 579** — regulatory submission context referenced in phase six

### From the APEX framework (internal coordination only — not on-mic)

- **AXLE Practice — ORCH-01 Warranty Root-Cause** — the internal 24-step orchestrator pattern that the spoken chain translates
- **SB06 — Warranty Traceability & Cost Avoidance** — the demo scenario that produced the $4.2M / $2.8M / 340% reference figures
- **LEDGER hash chain specification** — the fourteen-field audit row and its replay-token construction
- **Companion HTML pack** — `ZeroDayWarranty_Calculations_and_References.html` for the calculation walkthrough and step-by-step chain breakdown · `ZeroDayWarranty_Architecture_Diagrams.html` for the component flow diagrams
- **Services Podcast Ep 4** — the MCP boundary and agent runtime conventions under this episode
- **Services Podcast Ep 6** — Purview plus LEDGER hash chain deep dive
- **Sellers Podcast Ep 2** — *The Commercial Arc* — the Independence-from-Microsoft posture framework referenced in the dialog

---

**End of Episode 03 · The 24-Step Agent and the Microsoft Platform**
*≈ 6,200 words · target 32 minutes at conversational pace*
