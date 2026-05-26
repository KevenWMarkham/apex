# Episode 06 · FinOps for Agentic AI

**Builds on:** Episodes 1-5 (the architecture) · Trilogy — Sellers Ep 2 (commercial discipline)
**Run time:** ≈ 28 minutes target
**Last updated:** 2026-05-14

---

## Cold Open

[Sound: a CFO's office. Quarter-end. Friday, late. The blinds half-drawn against the long afternoon light. A printed dashboard on the desk — landscape, single-sheet — with one chart climbing diagonally across the page. A coffee mug pushed to the edge. The Finance Director's tablet open beside the printout. The CFO has been in this chair for nineteen years.]

**KEVEN:** I want to start tonight in a CFO's office. Quarter-end. Friday afternoon. The printout in front of him is one chart on a single sheet. The chart shows total AI consumption spend across the enterprise — tokens, Copilot seats, agent-runtime managed services, vector stores, embedding APIs, the rest of it — climbing diagonally for the last three quarters in a row. Plus thirty-one percent quarter over quarter, then plus twenty-eight, then plus thirty-five. The dashboard's title is *Q3 AI Consumption Trend.* The CFO has had this dashboard on his desk for ninety minutes. He has not put it down.

**REID:** And the meeting on his calendar.

**KEVEN:** And the meeting on his calendar is at four o'clock with the Chief AI Officer, the CIO, and the seller who has been carrying the agentic program for the last eighteen months. The seller is the one walking in to explain the chart. The CFO opens with one sentence. *Explain to me why our AI bill is up thirty-five percent quarter over quarter.* That is the entire opening. No preamble. No softening. The chart is the question.

**REID:** And the seller has, conservatively, ninety seconds to land an answer before the room decides whether the program is a credible investment or an undisciplined cost line.

**KEVEN:** Ninety seconds. The seller without a FinOps story for agentic AI loses the room in those ninety seconds. The seller who walks in with aggregate spend numbers and a list of services consumed loses faster, because the CFO has had three quarters of *services consumed* already and the chart is still climbing. The seller who walks in with per-use-case cost-per-outcome — *this greenlight-decision agent costs X dollars per decision and produces Y dollars of cycle-time saving per decision; this warranty-investigation agent costs X per cluster and produces Y of chargeback recovery per cluster* — that seller has a chance to hold the room. The chart is the same chart. The framing is what changes.

**REID:** And that is the substance of the next twenty-eight minutes.

**KEVEN:** That is the substance of the next twenty-eight minutes. *FinOps for Agentic AI.* The twenty-to-forty-percent QoQ growth pattern the analysts are citing. The cost sources — tokens, seats, runtime, vector, embedding, federation, audit-ledger. The productization gap across all three clouds — no cloud has a clean *AI Cost Management* product today. Model-mix optimization as the single largest cost lever in agentic AI. Copilot seat reclamation as the productivity-license-specific lever. Audit-ledger retention discipline — yes, the substrate from Episode Five costs real money to retain. And the CFO conversation framing — per-use-case cost-per-outcome, every time. Let's go.

---

## The conversation

### The plus-twenty-to-forty-percent QoQ pattern — what the analysts are seeing

**KEVEN:** Let's start where the CFO is starting. The cost-growth pattern. *Gartner, Forrester, and IDC are each citing AI consumption growth in the twenty-to-forty-percent quarter-over-quarter range across mid-to-large enterprise AI deployments through twenty-twenty-five and into twenty-twenty-six.* Paraphrased. Not a verbatim quote from any one of them. The shape of the published research is converging.

**REID:** And the shape of the growth.

**KEVEN:** The shape is — tokens from foundation models climbing as agent populations expand. Copilot seat licensing climbing as enterprise rollouts move from pilot to broad deployment. Agent-runtime managed-service compute climbing as Wave One workloads move into production and Wave Two scenarios spin up. Vector-store storage and query climbing as retrieval-grounded agents accumulate corpora. Embedding API spend climbing as new content gets indexed. *And the new cost lines* — federation-query compute, the cost of Principle Four pay-per-query rather than pay-once-for-bulk-copy. And audit-ledger storage, append-only, growing forever, the substrate from Episode Five.

**REID:** And the consequence for the CFO.

**KEVEN:** Every CFO with more than three agentic workloads in production is starting to ask the question on the dashboard. The seller who can't answer loses the conversation. Not because the spend is unjustifiable — most of the time it is amply justifiable when framed against outcome value — but because the CFO has been asked to defend the line in front of an audit committee, a board risk committee, or an external auditor reviewing budget discipline. The seller's answer has to be specific, has to be per-use-case, has to be tied to outcome. Aggregate spend with an aggregate justification does not survive that conversation.

**REID:** Let me push gently. The twenty-to-forty range is the analyst-cited pattern across the enterprises the firms surveyed. Specific enterprises sit higher or lower. The pattern is a pattern. The seller should be careful not to walk into a CFO conversation with *the industry is at thirty percent and we are at thirty-five so we are normal.* Normal-against-the-pattern is not the answer. The answer is *here is what is driving our specific growth, here is the per-use-case outcome value, here is whether we are spending efficiently against that value.*

**KEVEN:** Conceded cleanly. The pattern is a context-setter for the conversation, not an exoneration of the spend. The seller's job is to break the aggregate down into the cost sources, attribute each source to a workload or class of workloads, and tie each workload to its outcome. The pattern tells you the conversation is universal. It does not tell you whether your specific enterprise is spending well.

### Why traditional FinOps doesn't cover this cleanly

**REID:** The framework question. Most enterprises already have FinOps practice. Most have for years. Walk why agentic doesn't drop into the existing practice cleanly.

**KEVEN:** Walking it. Three cost dynamics traditional cloud FinOps was not designed for. *One — per-token pricing.* Foundation model APIs charge per million tokens, input and output priced separately, varying by model family, varying by generation. GPT-4o is one price. GPT-4o-mini is materially cheaper. Claude Opus is one price; Claude Sonnet is cheaper; Claude Haiku cheaper again. Gemini Pro versus Flash. Multimodal calls — vision, audio — priced differently from text. The pricing model is fundamentally per-call, per-modality, per-model. *Two — per-seat productivity licensing.* The Copilot family — Microsoft 365 Copilot, GitHub Copilot, Power Platform AI Builder, Sales Copilot, Service Copilot — licensed per user per month. The cost is fixed regardless of usage. The value varies dramatically with utilization. *Three — model-mix economics.* The right model for the right task changes the per-call cost by ten times easily, sometimes a hundred times. The same task on Opus versus Haiku is a hundred-x difference. The same task on GPT-4o versus GPT-4o-mini is roughly ten-x. The choice of which model handles which task is, today, the largest single cost lever in the agentic stack.

**REID:** And the framework consequence.

**KEVEN:** Traditional cloud FinOps — the FinOps Foundation principles, the FOCUS specification, the practice maturity model — were built for compute, storage, network, database, with the dominant cost-line being VM hours, storage TB-months, and network egress. Those are still real. They are still tracked. The mature FinOps practice handles them well. The AI consumption layer adds three new cost-line classes that the existing tooling, the existing dashboards, and the existing allocation models do not handle natively.

**REID:** Let me push back gently. *The FinOps principles are right.* Visibility, accountability, optimization. Cost-as-a-shared-responsibility. The principles themselves don't change. The cost levers are new. The framework adapts. The seller should not walk into a CFO conversation saying *traditional FinOps doesn't work for AI.* That sounds like *we need a whole new practice and a whole new budget for that practice.* The CFO will not be persuaded. The correct framing is — *the FinOps practice you have is the right practice. The cost dynamics of AI consumption are new, so the levers your practice pulls are different. The framework's the same; the levers are different.*

**KEVEN:** Conceded cleanly. The framework's the same; the levers are different. That is the line to carry. Visibility, accountability, optimization — those principles apply directly. The vocabulary of AI-specific levers — per-token pricing variability, per-seat utilization variance, model-mix economics — is the new piece the seller has to be fluent in. The framework adapts. The products lag.

### Cost sources covered — the full picture

**REID:** Now the inventory. Eight cost sources every seller should be able to walk. Go.

**KEVEN:** Walking the eight. *One — per-token foundation model costs.* The most visible cost line. Pricing varies by model. Approximate ranges current as of mid-twenty-twenty-six — GPT-4o input on the order of two-to-three dollars per million tokens, output materially higher; Claude Opus input on the order of fifteen dollars per million tokens, output higher again; Claude Sonnet and Haiku materially cheaper; Gemini Pro and Flash priced in the same competitive range; self-hosted Llama or Mistral where the cost is compute time rather than per-token. Pricing changes continuously. The seller should reference vendor pricing pages, not memorize numbers. *Two — Copilot seat licensing.* M365 Copilot, GitHub Copilot, Power Platform AI Builder, Sales Copilot, Service Copilot. Per user per month. Fixed cost. Utilization-dependent value. This is the productivity-AI line on the enterprise's bill.

**REID:** Three and four.

**KEVEN:** *Three — agent-runtime managed-service compute.* Foundry Agent Service on Microsoft, Bedrock Agents and Bedrock AgentCore on AWS, Vertex AI Agent Engine on GCP. Each charges for runtime invocation, orchestration, tool-call execution, memory persistence. Priced per invocation or per resource-hour depending on the service tier. *Four — vector-store storage and query.* Azure AI Search on Microsoft, OpenSearch Vector and Bedrock Knowledge Bases on AWS, Vertex AI Vector Search on GCP. Storage cost for the indexed corpus. Per-query cost for retrieval. Both lines grow with the corpus and with the agent population querying it.

**REID:** Five and six.

**KEVEN:** *Five — embedding API spend.* Generating the vectors that go into the vector store. Text-embedding-three-large versus text-embedding-three-small on OpenAI differs roughly ten-x on cost. Similar ranges across the other providers. Many enterprises use the larger embedding model for every workload by default, because it is the safest quality choice. The cost difference at scale is real, and the quality difference for many workloads is small. *Six — custom-model hosting.* When models are not on managed APIs — self-hosted Llama on AWS, custom containers on Vertex, Azure ML endpoints — the cost shifts from per-token to compute time, GPU-hour or accelerator-hour. Different cost model. Different optimization levers.

**REID:** Seven and eight.

**KEVEN:** *Seven — federation-query compute.* The cost of Principle Four from Episode One. Pay-per-query rather than pay-once-for-bulk-copy. Athena Federated Query on AWS, BigQuery Omni on GCP, Fabric Mirroring on Microsoft. Each federation query consumes compute on the federating service plus the source. The trade-off is real — federation avoids the bulk-copy storage cost and avoids the data-staleness problem, but pays per-query at scale. At low query volumes, federation is the right cost answer. At very high query volumes against the same source, the bulk-copy economics flip back. The seller has to know which side of the curve the workload sits on. *Eight — audit-ledger storage.* From Episode Five. The substrate is append-only. It grows forever if nothing prunes it. Hot-tier storage cost compounds. Cold-tier archival with retention policy is essential. The audit-ledger cost line is real, often missed in early Wave One budgets, and is structurally non-negotiable for regulated workloads.

**REID:** And the implicit ninth.

**KEVEN:** Implicit ninth is *the storage tier discipline across Bronze, Silver, Gold.* Hot storage, cool storage, archive storage — the data foundation from Episode Two has tiering decisions that materially affect the bill. Bronze is the largest by volume and usually the coolest by access pattern; Gold is the smallest but the hottest. Tiering policy applied correctly is a meaningful FinOps lever on the data layer. Most enterprises leave Bronze on hot storage by default and pay for it. The seller should know to look for that.

### Cost management products across the three clouds

**REID:** Three clouds. What does each give you, productized, for managing AI consumption cost specifically. Walk Microsoft first.

**KEVEN:** Microsoft. *Azure Cost Management* — the generic cloud cost analytics. Cost views by subscription, resource group, tag. The same surface every Azure customer has used for years. It works for AI consumption as far as the resources emit cost lines. *Azure Cost Management views for Azure OpenAI and Foundry* — per-model, per-deployment cost visibility, attribution by deployment name and model version. Better than nothing. Not a productized *AI Cost Management.* It is generic Cost Management with the AI-specific resources surfaced. *Microsoft 365 Copilot Admin Center* — seat utilization analytics. Which users are active, which are not, on which Copilot SKUs. Reasonably mature today. The piece that informs seat reclamation discipline, which we walk in a minute. *Power BI for cost analytics* — when the off-the-shelf views are not enough, enterprises typically build their own dashboards on top of the billing-export data. Standard pattern.

**REID:** And AWS.

**KEVEN:** AWS. *AWS Cost Explorer* — the generic cost analytics surface. Mature, capable, well-understood. *AWS Cost and Usage Reports* — the detailed line-item billing data. Every charge, every dimension, exported to S3 or queryable through Athena. The substrate every serious AWS FinOps practice runs on. *Bedrock cost reporting* — per-model invocation costs attributable through the standard cost dimensions. *AWS Budgets* — alerting on cost thresholds. *AWS Cost Anomaly Detection* — surfacing anomalous cost shifts, increasingly with AI-relevant pattern detection. Honest summary on AWS — capable generic FinOps tooling, AI-specific resources surfaced, no productized *AI Cost Management* layer that does per-use-case cost-per-outcome cleanly.

**REID:** And GCP.

**KEVEN:** GCP. *Cloud Billing* — cost analytics. *Vertex AI cost reporting* — per-model invocation visibility through the standard Cloud Billing dimensions. *BigQuery for cost analytics* — Cloud Billing exports to BigQuery. Most GCP FinOps practices run their analysis layer there. The query surface is strong. *Recommendations Hub* — cost optimization recommendations, increasingly with AI-relevant suggestions through twenty-twenty-five and twenty-twenty-six.

**REID:** And the honest cross-cloud claim.

**KEVEN:** *None of the three clouds has a productized "AI Cost Management" surface that gives a CFO per-use-case cost-per-outcome cleanly.* All three give per-resource and per-service cost views. None give per-agent or per-scenario cost-per-decision views productized. Every enterprise that wants the CFO-grade view builds it themselves, on top of the billing-export data, by tagging discipline at the resource layer and joining the cost data to outcome-value data from the business side. *That is the productization gap.* Real today. Expected to close through twenty-twenty-six and twenty-twenty-seven as the cloud vendors recognize the gap and ship surfaces that fill it.

**REID:** Let me push here. The productization gap is genuinely cross-cloud. Microsoft does not have the answer either. The seller who walks into a CFO conversation claiming Microsoft has the productized AI Cost Management answer and AWS and GCP do not — overclaims and gets caught. The honest claim is *none of the three has it productized yet; every enterprise is building it themselves; the build is achievable and the FinOps team your client already has can do it.*

**KEVEN:** Conceded cleanly. The productization gap is universal. The seller's honest posture is — *here is what each cloud gives you generically; here is the gap; here is what your FinOps team builds on top to close the gap; here is what we expect to be productized over the next twenty-four months.* That posture is credible across all three clouds. It doesn't depend on a Microsoft differentiation that isn't there.

### Model-mix optimization — the single largest cost lever

**REID:** Now the biggest lever. The thing the seller should leave the CFO conversation with as the headline. Model-mix.

**KEVEN:** Model-mix optimization. *The single largest FinOps lever in agentic AI today.* Said plainly. Bigger than seat reclamation. Bigger than embedding-tier discipline. Bigger than storage tiering. Bigger than ledger retention. Model-mix is the lever where the wrong choice costs ten-x to a hundred-x on the same workload.

**REID:** Walk it.

**KEVEN:** The discipline. *Use the cheapest model that produces an acceptable answer for the task.* Said exactly that way. Not the most capable model that produces the best possible answer. The cheapest model that clears the quality threshold the workload requires. For routine classification, lightweight summarization, simple extraction, low-stakes drafting — the small-model family is sufficient. GPT-4o-mini, Claude Haiku, Gemini Flash, smaller open-weights. For complex multi-step reasoning, high-stakes drafting, regulated-content review, decision support on material outcomes — the large-model family earns the cost. GPT-4o, Claude Opus or Sonnet, Gemini Pro. The mistake most enterprises make is defaulting to the most-capable model across every workload because it is the safest single quality choice.

**REID:** And the cost shape of the mistake.

**KEVEN:** On many enterprise workloads, the cost difference between the right small model and the default large model is ten-x to a hundred-x on the same task. Across a workload population, the aggregate impact is large. Industry analysts cite savings on the order of thirty-to-sixty percent on covered workloads when model-mix is optimized rigorously. Paraphrased — that range is consistent with what Gartner, Forrester, and IDC are reporting through twenty-twenty-five and into twenty-twenty-six.

**REID:** And the operational discipline.

**KEVEN:** Two pieces. *Per-task model selection* — the agent's orchestration logic chooses the model based on the task class, not on a single default. Routine reads on the small-model family. Complex reasoning on the large-model family. The orchestration code makes the choice. *Per-task cost-per-outcome tracking* — for each task class, track cost and quality. If a workload is currently on Opus, test it on Sonnet. If it clears the quality bar, downshift. If it doesn't, hold. The discipline is empirical, not theological. *Test the cheap model. If it works, use it. If it doesn't, use the expensive one and document why.*

**REID:** And the seller's framing for the CFO.

**KEVEN:** *Model-mix discipline is the single largest cost lever in the agentic stack today. The wrong-model-for-the-task pattern is the most common single FinOps failure. Enterprise pilot teams default to the most capable model because it is the safest quality choice. The cost difference at scale is ten-x to a hundred-x on the same task. Per-task model selection — driven by the orchestration logic — combined with empirical per-task quality testing recovers thirty-to-sixty percent of consumption cost on the covered workloads. Said to a CFO, that is the single highest-leverage architectural commitment the program can make.*

**REID:** And the architectural pre-requisite.

**KEVEN:** The pre-requisite is — *the orchestration runtime has to support per-task model selection cleanly.* Foundry Agent Service does. Bedrock Agents and AgentCore do. Vertex AI Agent Engine does. The capability is universal across the three managed-runtime stories. What varies is how readily the orchestration code expresses the policy. The seller should be specific — the model-mix lever exists on all three clouds. The discipline to use it is the operational practice. The architecture supports it. Nothing here is a single-cloud feature.

### Idle Copilot seat reclamation — the productivity-license lever

**KEVEN:** Now the Copilot-specific lever. M365 Copilot. GitHub Copilot. Power Platform AI Builder. Sales Copilot. Service Copilot. All licensed per seat per month. Fixed cost regardless of utilization.

**REID:** And the utilization pattern.

**KEVEN:** The utilization pattern is the FinOps issue. In a typical enterprise rollout of Copilot at scale, *twenty-to-forty percent of provisioned seats are under-utilized.* Below the engagement threshold that justifies the license. Paraphrased from the industry analysts and from what Microsoft itself publishes through the Copilot Admin Center analytics. The pattern is well-documented.

**REID:** And the recovery discipline.

**KEVEN:** Quarterly seat reclamation. *Every quarter, review the utilization analytics. Identify the seats below threshold. Reach out to the user. Either re-engage them with training and use-case discovery, or reclaim the seat and reallocate it to a user on the waitlist.* The discipline is operational. The tooling exists today — the Copilot Admin Center surfaces the utilization data; the enterprise's IT-asset-management practice plugs into the data and runs the reclamation cycle. Recovery in industry-cited enterprise deployments is on the order of fifteen-to-twenty-five percent of Copilot license spend. And the political shape of the lever is real — *Copilot is a productivity license. Taking it away from a user feels like a downgrade.* The cleanest framing is — *we have a waitlist. We have users who would use it more. We are reallocating, not reclaiming.* The discipline is easier when there is genuine demand. When the demand isn't there, the lever is harder. The seller should know the political shape and not pitch reclamation as a frictionless cost-saving. It is real money. It is also a real change-management conversation.

**REID:** And the cross-cloud honesty.

**KEVEN:** *Copilot reclamation is a Microsoft-specific lever* — because the Copilot family is a Microsoft commercial surface. GitHub Copilot is licensed per seat too, included. The equivalent levers on AWS and GCP are different shapes — AWS does not have a comparable per-seat productivity-AI license at the same scale; GCP's Duet AI and Gemini for Workspace have their own equivalents with their own utilization patterns. The lever is real on Microsoft. The equivalent levers on the other clouds are smaller in dollar terms today because the seat populations are smaller. That is not a permanent state. As Duet and Gemini for Workspace populations grow, the equivalent reclamation discipline will become a comparable lever.

### Audit-ledger retention discipline

**REID:** Audit-ledger storage. From Episode Five. Walk the cost discipline.

**KEVEN:** The ledger substrate from Episode Five is append-only by architecture. It grows forever if nothing prunes it. The cost discipline is two-tier retention. *Hot-tier retention* — the rows accessed for active query, by compliance team, by SRE team, by FinOps team. Typical range thirty to ninety days. Storage class is hot, query cost is low, retention is short. *Cold-tier archival* — the rows held for the audit retention requirement. Typical range one to seven years for non-regulated. Per-regulation for regulated. Storage class is cold or archive, query cost is higher, retention is long.

**REID:** And the regulated versus non-regulated shapes.

**KEVEN:** Per-regulation on the regulated side. Some regulated industries require seven-to-ten-year retention on auditable records. Pharmaceutical, financial-reporting-adjacent, certain public-sector workloads. The ledger has to retain at the longest applicable retention period. That is a real cost line. It is structurally non-negotiable. The discipline is — *put it in archive storage; design the queries to be acceptable on archive-tier latency for the rare regulator-driven query; do not pay hot-tier rates for rows nobody is querying.* And for non-regulated workloads, the FinOps lever is sampling. *Keep every row for regulated workloads. Sample non-regulated workloads at a rate that supports debugging and incident-response use without storing every row forever.* Standard pattern. Ten-percent sampling, or one-row-in-twenty, or full retention for a representative time window with sampling outside it. The discipline depends on what the SRE team and the FinOps team need the rows for. The compliance team's requirement is non-regulated equals less stringent retention by definition.

**REID:** And the budget line.

**KEVEN:** *Audit-ledger storage is often missed in Wave One budgets.* The build is funded; the runtime is funded; the substrate is funded; nobody funds the storage growth out into year three. The seller should put the line in the budget conversation at Wave One. Hot-tier for the first ninety days, archival for the retention period, sampling for the non-regulated, regulator-specified retention for the regulated. Modelled out for three years, not just for Wave One. The CFO does not love being surprised by a structural cost line in year two that wasn't in the original plan.

### The CFO conversation — per-use-case cost-per-outcome

**REID:** Now the seller's framing. The CFO opening from the cold open. Walk the answer.

**KEVEN:** Walking it. The CFO asks *why is our AI bill up thirty-five percent quarter over quarter.* The wrong answer is *because we are using more tokens, more seats, more runtime, more storage.* That answer is true. It does not help the CFO. The CFO is being asked to defend the spend to the audit committee. *More tokens* is not a defence.

**REID:** And the right answer.

**KEVEN:** The right answer is *per-use-case cost-per-outcome.* For each material workload, the seller has the cost-per-decision and the outcome-value-per-decision. *Workload one — the greenlight decision-support agent. Costs X dollars per decision. Produces Y dollars of cycle-time savings per decision. Margin is the difference. Volume in the quarter was V. Total contribution to the quarter's outcome value was V times margin. Cost of that contribution was X times V. Net is positive.* Same template per workload. Aggregated up, the total quarterly AI consumption sits against the total quarterly outcome value the agent population produced. Both numbers in the same row.

**REID:** And the failure mode.

**KEVEN:** The failure mode is — *workloads that have cost but not measurable outcome value.* They are the ones that lose the CFO conversation, because they are the ones that look like undisciplined cost. The discipline is — every workload in production has to have a cost line, an outcome metric, and a value attribution. If a workload cannot articulate its outcome value, it is a candidate for sunsetting. The CFO will support that discipline. The CFO will not support a flat plus-thirty-five-percent that cannot be broken down by workload and attributed to outcome.

**REID:** And the seller's posture.

**KEVEN:** *The seller who shows up to the CFO with aggregate AI spend numbers loses. The seller who shows up with per-use-case cost-per-outcome — workload by workload, cost per decision, value per decision, ROI per agent — wins.* That is the FinOps story for agentic AI. The architecture supports it. The discipline at the workload layer is what produces the numbers. The seller's job is to make sure the discipline is in place before the CFO asks the question. Because the CFO is going to ask the question, increasingly, every quarter, through twenty-twenty-six and beyond.

**REID:** And the architecture connection.

**KEVEN:** The architecture connection is the audit-ledger substrate from Episode Five. The substrate that captures every agent decision as a structured row, with model version, tools invoked, data accessed — that same substrate captures the cost of every decision. The same rows that serve compliance audit and operational observability serve FinOps cost attribution. *One substrate, multiple consumers.* Compliance asks for the chain; SRE asks for the latency distribution; FinOps asks for the cost per decision broken down by workload. Same rows. Different filters. Different aggregations. The FinOps story for agentic AI rides on the same architectural commitment as the audit story. Build the substrate. Tag at the resource layer. Join cost data to outcome data. The CFO conversation lands.

### A reading I want to do

**KEVEN:** I want to read briefly — paraphrased — from a composite of what Gartner, Forrester, and IDC have published through twenty-twenty-five and into twenty-twenty-six on AI consumption cost growth and the productization gap in AI cost management. The shape of the published research is converging.

**REID:** Go.

**KEVEN:** [reading, paraphrased — composite of Gartner AI cost management research, Forrester AI ROI research, and IDC enterprise AI consumption forecasts through 2025-2026]

*"Enterprise AI consumption costs are growing in the twenty-to-forty-percent quarter-over-quarter range across mid-to-large deployments, driven principally by token-priced foundation-model invocation, per-seat productivity-AI licensing, managed agent-runtime compute, vector-store and embedding services, and emerging cost lines including federation-query compute and audit-substrate retention. None of the three major cloud platforms — Microsoft Azure, AWS, or Google Cloud — currently provides a productized AI Cost Management surface that delivers per-use-case cost-per-outcome attribution natively. Enterprises seeking that view build it on top of generic cloud-billing analytics, augmented by workload tagging, model-mix telemetry, and outcome-value data drawn from business systems. The productization gap is expected to close through twenty-twenty-six and twenty-twenty-seven as the cloud vendors and FinOps tool providers ship AI-aware cost-management surfaces. In the current window, the FinOps-Foundation framework principles — visibility, accountability, and optimization — apply directly to AI consumption; the cost levers the framework pulls are AI-specific and emergent."*

[pause]

**REID:** *The productization gap is what makes this seller's playbook deliverable today.* The cloud vendors will productize. By twenty-twenty-seven we will likely have AI-aware Cost Management surfaces from at least one and probably all three of the hyperscalers. Today, the FinOps story for agentic AI is custom engineering on top of generic billing analytics, plus the discipline of per-use-case cost-per-outcome at the workload layer. The architecture supports it. The substrate enables it. The discipline produces it. The seller carries it into the CFO conversation. The differentiation today is the discipline, not the tooling.

**KEVEN:** Said exactly that way.

### One disagreement

**REID:** Pushback. The structural one. Because this is where I have to push back if I am doing my job.

**KEVEN:** Go.

**REID:** *FinOps for AI is the same as FinOps for cloud.* Said plainly. The FinOps Foundation principles are right. Visibility, accountability, optimization. Cost-as-a-shared-responsibility. The maturity model — crawl, walk, run. The team operating model. All of it is the same framework. The seller who tells a CFO *agentic AI needs a whole new FinOps practice* loses the room, because the CFO has invested in the existing practice and the practice is the right practice. The cost levers are different. The framework is the framework.

**KEVEN:** Conceded on the framework. Pushed back on the levers.

**REID:** Walk the push-back.

**KEVEN:** Walking it. The framework is the framework. The principles apply. The practice is the practice. *And the cost dynamics are different in three structural ways the existing practice was not designed to handle.* One — per-token pricing variability across model families, generations, and modalities, which the existing cost-allocation tooling does not natively dimension. Two — per-seat productivity licensing with utilization variance, which is a new commercial surface most enterprises did not have at scale before the Copilot rollout. Three — model-mix economics where the wrong-model-for-the-task choice costs ten-x to a hundred-x on the same workload, which is a lever the existing FinOps practice did not have to pull because traditional compute, storage, and network do not have hundred-x intra-class cost variability of that shape.

**REID:** And the convergence.

**KEVEN:** *Framework same, levers different. Both true. Sellers need both.* The framework gives the CFO continuity — the FinOps practice they have funded is the right practice. The levers give the program specificity — the AI-specific cost dynamics require AI-specific vocabulary, AI-specific tagging, AI-specific allocation models. The seller who walks in with framework-only loses the per-use-case conversation. The seller who walks in with levers-only loses the framework-continuity conversation. Both at once is the right answer.

**REID:** Convergence. Named cleanly.

**KEVEN:** Named cleanly. Framework continuity at the practice layer. Lever specificity at the workload layer. The CFO gets a story that respects the practice they have funded and respects the new cost dynamics the agentic workload introduces. That is the FinOps story.

### What to carry forward

**KEVEN:** Three things.

**REID:** Go.

**KEVEN:** *One — AI consumption costs are growing twenty-to-forty percent quarter over quarter at scale, per Gartner, Forrester, and IDC. The CFO conversation is here. The seller without a FinOps story for agentic AI loses it. The seller with per-use-case cost-per-outcome, workload by workload, with model-version attribution and outcome-value attribution, holds the room. The substrate from Episode Five is what makes that view possible. Build the substrate; tag at the resource layer; join cost to outcome.*

*Two — the productized "AI Cost Management" gap is real across all three clouds. Microsoft does not have it productized; AWS does not have it productized; GCP does not have it productized. Every enterprise builds the per-use-case view themselves, on top of generic billing analytics, augmented by workload tagging and outcome-value data. That productization gap is expected to close over twenty-twenty-six and twenty-twenty-seven. In the current window, the discipline is the differentiator. The seller's claim is honest across all three clouds and does not depend on a Microsoft advantage that is not there.*

*Three — model-mix optimization is the single largest cost lever in agentic AI today. Wrong-model-for-the-task is the most common single FinOps failure. Per-task model selection driven by orchestration logic, plus empirical per-task quality testing, recovers thirty-to-sixty percent of consumption cost on covered workloads on industry-cited patterns. Copilot seat reclamation recovers another fifteen-to-twenty-five percent of seat spend in typical enterprise rollouts. Audit-ledger retention discipline keeps the substrate cost in check. The framework is the FinOps framework you already have. The levers are agentic-AI-specific. Both at once.*

**REID:** And the seller's posture from the disagreement — framework continuity at the practice layer; lever specificity at the workload layer. The CFO conversation lands when the framework is respected and the levers are precise. Per-use-case cost-per-outcome is the framing every time. ROI per agent is the metric the seller defends.

**KEVEN:** Per-use-case cost-per-outcome, every time. ROI per agent, every time.

**REID:** Next episode — *Multi-Cloud Reality, Cloud Portability, and Model Portability.* The Acceleration Framework's cloud-portability commitment. The eighteen-month model-generation refresh cycle. What *primary cloud* actually means in a multi-cloud enterprise. When multi-cloud is legitimate strategy and when it is theatre. The Bedrock-versus-Foundry-versus-Vertex composition the seller has to be honest about when the CIO has already committed strategically to a non-Microsoft primary cloud.

**KEVEN:** See you there.

[outro]

---

## Further reading

### Industry analyses
- **FinOps Foundation** — [finops.org](https://www.finops.org/) — framework, principles, FOCUS specification, maturity model
- **Gartner** — AI cost management market analyses and AI consumption forecasts
- **Forrester** — AI ROI research and Total Economic Impact methodology
- **IDC** — enterprise AI consumption and budget forecasts

### Microsoft Learn
- **Azure Cost Management** — overview, views, and exports
- **Microsoft Cost Management for Azure OpenAI** — per-model, per-deployment cost visibility
- **Microsoft 365 Copilot Admin Center** — seat utilization analytics
- **Foundry Agent Service** — runtime cost emission and tagging guidance

### AWS documentation
- **AWS Cost Explorer** — generic cost analytics
- **AWS Cost and Usage Reports** — detailed line-item billing data
- **Amazon Bedrock** — invocation cost reporting and pricing
- **AWS Budgets and AWS Cost Anomaly Detection** — alerting and anomaly surfacing

### Google Cloud documentation
- **Cloud Billing** — cost analytics and BigQuery export
- **Vertex AI cost reporting** — per-model invocation costs
- **Recommendations Hub** — cost-optimization recommendations including AI-relevant suggestions

### Foundation model pricing references
- **OpenAI** — model pricing page (current pricing for GPT-4o, GPT-4o-mini, embedding tiers)
- **Anthropic** — Claude model pricing (Opus, Sonnet, Haiku)
- **Google** — Gemini pricing (Pro, Flash, embedding tiers)
- **Meta** — Llama (self-hosted compute cost basis)

### From the Acceleration Framework
- **Episode 1** — Five Principles (Principle 4 federation pay-per-query trade-off)
- **Episode 2** — Data Foundation (Bronze-Silver-Gold tiering and storage class discipline)
- **Episode 5** — Audit, Ledger, Replay (audit-ledger storage retention is a FinOps line)
- **Episode 7** (next) — Multi-Cloud Reality, Cloud Portability, and Model Portability

---

**End of Episode 06 · FinOps for Agentic AI**
*≈ 5,500 words · target 28 minutes at conversational pace*
