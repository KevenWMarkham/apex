# Episode 07 · Multi-Cloud Reality, Cloud Portability, and Model Portability

**Builds on:** Episodes 1-6 (architecture + FinOps) · Trilogy — Sellers Ep 2 (Independence)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-14

---

## Cold Open

[Sound: a CTO's architecture-review room. A multi-national enterprise headquarters — the kind with a long polished table, glass walls onto a corridor, and a wall-mounted screen at the far end. Three cloud logos on that screen — Microsoft, AWS, Google Cloud — arrayed across a single slide. Three subsidiaries listed beneath the logos, each inherited at acquisition, each running on a different primary cloud. The CTO has been in the chair for six months. The deck on the table was prepared by an outside advisor. The first agenda item is one line — *Agentic AI architecture across the three subsidiaries.*]

**KEVEN:** I want to start tonight in a CTO's architecture review room. A multi-national enterprise. Headquarters in one country, subsidiaries in three others, each acquired over the last seven years. One subsidiary runs primarily on Microsoft Azure. One on AWS. One on Google Cloud. None of those choices were made by this CTO. Each was inherited, intact, at acquisition. The cloud reality on the screen is not a strategy. It is a history.

**REID:** And the agenda item.

**KEVEN:** The agenda item is one line. *Agentic AI architecture across the three subsidiaries.* The CTO is not choosing a primary cloud. The CTO is asking a different question — *given that I am multi-cloud by inheritance, how do I architect agentic AI across the three so that the enterprise behaves like one enterprise, and so that I don't end up with three incompatible agent stacks I have to operate separately for the next decade?* The cloud choice was made before this CTO took the chair.

**REID:** And the seller's mistake in that room.

**KEVEN:** The seller's mistake is to walk in and pitch *let's standardize on Microsoft.* That answer ignores the inherited reality, the migration cost, and the political shape of three subsidiaries that each have a CIO who chose their own cloud and is not going to be told to unwind that choice by a new corporate CTO. The seller who walks in with *standardize on one cloud* loses inside the first ten minutes.

**REID:** And the right move.

**KEVEN:** The right move is to recognize what *multi-cloud* means at the enterprise level versus what it means at the agentic-workload level. The enterprise is multi-cloud. The individual agentic workloads will almost always pick a primary cloud per scenario — the cloud where the bulk of the workload's data lives. The architectural job is to make sure the Acceleration Framework's principles apply portably across the three, so an agent on the Microsoft side can interoperate with the audit substrate on the AWS side, and an agent on the GCP side can federate identity back to Entra when the corporate function needs to. Multi-cloud at the enterprise level. Primary cloud per workload at the agentic stack level. Both true at once.

**REID:** That distinction is the substance of the next thirty minutes. The Acceleration Framework's vendor-neutral design and what *cloud-portable by design* actually means. The 90-percent reality that most agentic workloads land on one primary cloud. The cross-cloud egress economics. The identity-federation patterns from Episode Four, deepened. The model-portability discipline. And the legitimate-versus-theatre framing the seller has to be precise about.

**KEVEN:** *Multi-Cloud Reality, Cloud Portability, and Model Portability.* Let's go.

---

## The conversation

### The Acceleration Framework's cloud portability — by design

**KEVEN:** Let me start with the claim I want to defend across the whole episode. *The Acceleration Framework is architecturally cloud-portable by design.* The Five Principles are vendor-neutral. Said in Episode One, said again every episode since. Tonight is where we test that claim against the multi-cloud reality.

**REID:** Walk the principles one more time. With portability in mind this round.

**KEVEN:** Walking them. *Principle One — Gold-Tier-First.* The agent talks to a purpose-built Gold Tier composed from systems of record and data warehouses. Bronze lands raw on OneLake, on S3, on Cloud Storage. The medallion pattern doesn't change across the three. Silver canonical schemas travel — the definitions live in code, not in any single cloud's metadata service. Gold per-scenario views travel — the composition logic is portable across query engines. The principle is the principle on every cloud.

**REID:** And Principle Two.

**KEVEN:** *Principle Two — Governance, audit, and the ledger pattern.* From Episode Five. The ledger pattern is productized most densely on Microsoft today — Purview plus DSPM for AI plus the audit-row infrastructure. On AWS the same pattern is assembled — CloudTrail plus Macie plus a DynamoDB or QLDB ledger with hash-chained rows. On GCP the same pattern is assembled — Cloud Audit Logs plus Dataplex plus a BigQuery-backed ledger. The productized density varies. *The pattern itself is portable.* The audit-row schema, the hash-chain logic, the replay token — all defined in code. The engineering effort varies; the architecture does not.

**REID:** Principle Three.

**KEVEN:** *Principle Three — Identity Continuity.* From Episode Four. The federation primitives differ. Microsoft Entra. AWS IAM Identity Center plus federation. GCP Cloud IAM with Workload Identity Federation. The architectural goal is the same on all three — agent, operator, source, auditor identities all distinct, all chained end-to-end through the audit substrate. *Identity continuity is achievable on all three clouds.* The continuity principle holds across all three; the shape of the federation depends on which cloud is the home of which identity.

**REID:** Principle Four.

**KEVEN:** *Principle Four — No Replication. Sources stay untouched.* From Episode Two. Mirroring and Shortcuts on Microsoft, Athena Federated Query on AWS, BigQuery Omni on GCP. *All three clouds have credible no-replication patterns.* The productization variance is real — Fabric Mirroring is operationally turnkey for the SQL-source case, BigQuery Omni is strongest for cross-cloud federated query against S3 and ADLS, Athena Federated Query is broadest in source-connector coverage. The seller does not have to compromise the principle to recommend any cloud.

**REID:** And Principle Five — the deep dive of this episode.

**KEVEN:** *Principle Five — Model Portability.* We come back to this in detail in a few minutes. The architectural commitment — the agent design is portable across model generations and across model providers. The disciplines that produce that portability are themselves cloud-portable. Versioned prompts. Tool abstractions. Model-agnostic SDKs. Evaluation harnesses. Every one of those disciplines can be expressed on any of the three clouds.

**REID:** And the headline claim.

**KEVEN:** *The Acceleration Framework is architecturally cloud-portable by design. Microsoft earns the recommendation on productized-capability density across the principles — said in Episode One, said in Episode Five, said again now. The architecture itself is not Microsoft-locked.* That distinction is what protects the seller in a multi-cloud CIO conversation. The architectural commitments do not depend on the cloud. The cloud choice is downstream of the architectural commitments, not upstream.

**REID:** And that is the line the seller has to be able to hold in front of a CTO who has three clouds inherited and is not in a position to consolidate. The framework travels. The recommendation is a productization-density argument, not an architecture-lock argument.

### What "primary cloud" actually means in practice

**REID:** Now the framing question. *What does primary cloud actually mean?* Because the seller hears multi-cloud and the CIO hears multi-cloud and they are not always saying the same thing.

**KEVEN:** Walking it. The ninety-percent reality. *Most agentic workloads land on one cloud per scenario.* That cloud is the workload's primary cloud. The primary cloud is typically — almost without exception — the cloud where the bulk of the workload's data already lives. The data gravity drives the cloud selection at the workload layer. The architectural choice is not made in the abstract.

**REID:** And the enterprise layer.

**KEVEN:** The enterprise layer is different. At the enterprise level, *most enterprises above a certain size are multi-cloud.* The Gartner and Forrester research on enterprise cloud adoption — paraphrased from the published surveys through twenty-twenty-five — puts the multi-cloud-at-enterprise-level rate at somewhere between seventy and ninety percent for enterprises above a thousand employees. M&A activity, vendor diversification, regulatory residency, business-unit autonomy, historical inertia — every one of these produces multi-cloud at the enterprise scale. So the enterprise is multi-cloud. *That does not mean every workload is multi-cloud.*

**REID:** And the conflation that costs sellers.

**KEVEN:** The conflation is — a CIO says *we are multi-cloud* and the seller hears *every workload spans clouds.* That is almost never what the CIO is saying. Almost always what the CIO is saying is *we have workloads on multiple clouds.* The distinction matters because cross-cloud composition at the individual-workload level is genuinely the edge case. It is not the default. The default — even at multi-cloud enterprises — is *each agentic workload picks its primary cloud based on the data gravity for that scenario, runs there, and composes with the rest of the enterprise's stack through identity and audit federation patterns.*

**REID:** Let me sharpen that. *Sellers should be precise.* A client saying *we are multi-cloud* usually means *we have workloads on multiple clouds.* It does not usually mean *this one agent workload spans multiple clouds.* Confusing the two leads to over-architected solutions. The seller who walks in with a cross-cloud composition pattern for a workload whose data is ninety-nine percent on one cloud is selling complexity that the workload does not require. The right move is — *which cloud holds the data for this scenario? That is the primary cloud for this workload. The architecture commits there. Cross-cloud composition is the exception, and the exception is justified case by case.*

**KEVEN:** Said exactly that way. The architectural default is *primary cloud per workload.* The architectural exception is cross-cloud composition, justified per scenario.

**REID:** And the consequence for the framework.

**KEVEN:** The consequence is — the Acceleration Framework applies to each workload on its primary cloud. The Five Principles guide the architecture there. The multi-cloud reality of the enterprise shows up at the seams — identity federation between primary clouds, audit-substrate composition across primary clouds, the occasional cross-cloud query when the scenario justifies the egress cost. The framework is not invalidated by multi-cloud. The framework is *applied per workload on the workload's primary cloud, with the seams between primary clouds engineered explicitly when the enterprise needs them.*

**REID:** That is the architectural posture. Single-cloud-by-default at the workload level, multi-cloud-aware at the enterprise level, seams engineered explicitly where the seams matter.

### Cross-cloud egress economics — the real reason multi-cloud is rare at the agentic stack

**KEVEN:** Now the economics that drive the architectural pattern. Because the *primary cloud per workload* default isn't just an architectural preference. It is an economic constraint. Data egress between clouds is expensive.

**REID:** Walk the numbers — directionally.

**KEVEN:** Directionally. Data egress charges out of any of the three major clouds run typically in the range of five to ten cents per gigabyte, depending on destination, volume tier, and pricing program. Vendor pricing pages are authoritative and they change. The directional shape is — moving data out of one cloud and into another is materially more expensive than moving the same data within a cloud, by an order of magnitude or more in many cases. Intra-cloud movement is often free or near-free; cross-cloud movement is metered and adds up fast at agentic-workload data volumes.

**REID:** And the agentic-workload pattern.

**KEVEN:** The pattern compounds the egress problem. Agents that need real-time data access — retrieval-augmented generation against a corpus, federated query against a transactional system, audit-row writes back to the substrate — generate many small data movements over the course of every decision. If those movements cross clouds, every movement is a metered egress event. A single agentic workload making thousands of decisions per day, each touching modestly-sized data, can accumulate cross-cloud egress charges that materially change the workload's economics over a quarter.

**REID:** And the federation patterns from Episode Two.

**KEVEN:** Federation patterns reduce the egress cost compared to the bulk-copy alternative. Mirroring, Shortcuts, and Federation are designed to avoid moving the data once-for-bulk-copy. BigQuery Omni in particular is engineered to push the query down to where the data lives — query S3 from BigQuery, query ADLS from BigQuery — without bulk-copying the underlying object data across the cloud boundary. The compute moves; the data stays. But federation reduces egress, it does not eliminate it. Query results still cross the boundary. *Federation does not make cross-cloud queries free.* It makes them dramatically cheaper than bulk-copy.

**REID:** Let me push there. The architectural question is whether cross-cloud query is worth the recurring cost for the specific workload. For a low-volume workload where the data has to stay where it is for regulatory or data-gravity reasons, federation is the clean answer. For a high-volume workload where the cross-cloud query frequency compounds, the bulk-copy economics flip back to being cheaper despite the data-staleness penalty. The seller has to know which side of that curve the workload sits on.

**KEVEN:** And the architectural pattern that emerges — the economics push toward *primary cloud per workload.* The cloud where the data lives is the cloud where the agent runs. Cross-cloud federation is reserved for scenarios where the data cannot move and the access pattern is bounded. The default is single-cloud per workload; the exception is justified case by case against the egress and federation cost.

### Identity federation patterns across clouds

**REID:** Now the identity layer. From Episode Four. Recap and deepen with the multi-cloud frame.

**KEVEN:** Walking it. The three federation primitives. *Microsoft Entra B2B* — federation into Entra from external identity providers including AWS IAM, Google Cloud Identity, Okta, Ping, and the SAML and OIDC providers more broadly. Entra B2B is the inbound pattern. *AWS IAM federation* — SAML 2.0 support for federating external identity providers into AWS, plus OIDC for workload identity, plus cross-account roles for AWS-to-AWS federation. AWS IAM Identity Center sits on top of that to provide the single-sign-on surface. *GCP Workload Identity Federation* — said in Episode Four, said again now — the strongest cross-cloud federation primitive of the three. Workload Identity Federation lets an external workload — running on AWS, on Azure, on-premises, in a CI/CD environment — assume a GCP service identity without long-lived credentials. The federation is short-lived, scoped, and rotated. The pattern is operationally clean.

**REID:** And the agentic-workload application.

**KEVEN:** Federation patterns enable *agent-identity portability across clouds.* An agent running on AWS Bedrock with an IAM role can federate into Entra to read corporate identity claims about the operator who invoked it. An agent running on GCP Vertex AI with a service account can federate into AWS IAM to read from a permitted S3 bucket. An agent running on Azure Foundry with a managed identity can federate into Google Cloud IAM via Workload Identity Federation to call a Vertex AI endpoint. *All three directions are achievable with current productized primitives.* The architectural commitment is to design for federation from the start, not to bolt federation on later.

**REID:** Let me push there. *If you architect for identity federation from Wave One, multi-cloud composition is achievable.* The federation patterns work. The primitives are mature. *If you bolt federation on later, every cross-cloud scenario becomes an integration project.* The audit substrate has to be retrofitted to handle the federated principal. The replay token has to be retrofitted to carry the federation chain. The privilege grants have to be re-mapped. The retrofit is expensive and it tends to be uneven — the cleanly-architected workloads federate easily; the bolted-on workloads cost more to federate than they cost to build originally. The architectural discipline pays for itself many times over when the second cloud lands. *Design for federation early.*

**KEVEN:** Said exactly that way. The federation primitives are universal across the three clouds. The discipline is universal. The retrofit cost is the penalty for skipping the discipline.

### Multi-cloud audit chain patterns

**REID:** And the audit substrate from Episode Five. How does the ledger compose across clouds?

**KEVEN:** Walking it. The audit substrate composition across clouds is buildable. *The audit-row schema can be portable across clouds.* The seller defines the schema in code, not in any single cloud's audit-service configuration. The same row shape — agent identity, operator identity, source identity, tool invoked, inputs, outputs, hash of the previous row, replay token, timestamp — is written by an agent on Azure to an audit table backed by Fabric, by an agent on AWS to an audit table backed by DynamoDB or QLDB, and by an agent on GCP to an audit table backed by BigQuery or Spanner. *Same schema. Different physical storage.* The portability is at the schema layer.

**REID:** And the cross-cloud query layer.

**KEVEN:** The cross-cloud query layer rides on the same federation primitives we just walked. *Audit query across clouds is achievable through federation.* BigQuery Omni can query the AWS-side audit storage if the audit data lands in S3 in a queryable format. Athena Federated Query can reach across to other sources. Fabric Mirroring can pull AWS-resident audit data into OneLake when the auditor wants a unified view. The pattern is — store the audit rows in the cloud where the agent runs, federate the query out when an enterprise-level audit view is needed. *Federation at the audit layer is the same pattern as federation at the workload data layer.*

**REID:** And cross-cloud replay.

**KEVEN:** Cross-cloud replay is the harder problem. Replay requires the model version, the prompt version, the tool definitions, the inputs, and the deterministic state at the time of the original invocation. If all of those are captured by the audit row — as they should be, if the substrate from Episode Five was built properly — then replay is achievable on any cloud that can host the same model version. *The replay token has to be portable across the model-hosting endpoints.* The discipline is — capture the model version explicitly, hold the model version available across the clouds where replay might happen, and design prompts and tool definitions to be model-agnostic enough that minor substitution does not invalidate the replay.

**REID:** Which connects directly into Principle Five.

**KEVEN:** The replay-across-clouds problem is a model-portability problem in disguise. If the agent's design is locked to a single model version on a single cloud, cross-cloud replay is impossible. If the design is model-portable in the way Principle Five requires, replay is achievable. The audit substrate composition and the model portability discipline are the same architectural commitment expressed two different ways. *The pattern is buildable; the engineering is real; the discipline pays off when the enterprise needs unified audit across clouds.* No cloud productizes cross-cloud audit composition end-to-end today. All three productize the within-cloud audit substrate. The cross-cloud composition sits naturally on top of the federation patterns the enterprise has already built for data and identity.

### Model Portability — Principle Five deep dive

**REID:** Now the deep dive. Principle Five. Model Portability. This is the section that has the most independent architectural content for this episode.

**KEVEN:** Walking it. The cadence question first. *Model generations are refreshing faster every cycle.* The pattern across the major model families through twenty-twenty-four, twenty-twenty-five, and into twenty-twenty-six — GPT-4 to GPT-4o to GPT-4.1 to the o-series, roughly an eighteen-month arc with multiple generations inside it. Claude 3.5 Sonnet to 3.7 Sonnet to the four-series, roughly twelve months across the recent generations. Gemini 1.5 to 2.0 inside a window closer to nine months. The cadence is accelerating, not slowing. An agent built tightly to a specific model generation today is an agent that is going to be re-architected inside the next twelve to eighteen months. That is unsustainable as an operating practice for an enterprise running tens or hundreds of agents in production.

**REID:** And the architectural discipline that produces model portability.

**KEVEN:** Four disciplines. Said cleanly. *One — versioned prompts.* The prompts the agent uses live in source control. Every version is captured. The prompt is treated as code. When the model changes and the prompt has to adapt, the adaptation is a code change that runs through review, testing, and deployment like any other code change. The prompt is not embedded in the orchestration code as a string literal; the prompt is a versioned artifact with its own deployment lifecycle. *Two — tool-call abstractions.* The tools the agent uses are defined model-independently. The tool schema — name, description, parameters, return type — is the contract. The model-specific format the agent runtime uses to invoke the tool — whether that is OpenAI's function-calling format, Anthropic's tool-use format, Google's tool-call format — is below the abstraction. The orchestration code expresses the tool call in the model-independent form. The runtime translates.

**REID:** Three and four.

**KEVEN:** *Three — model-agnostic SDKs.* The Microsoft Agent Framework SDK supports multiple model backends — OpenAI on Azure, Anthropic Claude through partner integrations, the Foundry model catalog. AWS Bedrock Agents accept multiple models per agent and let the orchestration code choose the model per invocation. GCP Vertex AI Agent Builder supports model selection across Gemini, Claude via the Anthropic partnership, and the open-weights catalog. The SDKs let the orchestration code express the agent independently of the model. The discipline is to *use the model-selection feature, not to hardcode the model.* *Four — evaluation harnesses.* The same scenarios run against multiple model versions periodically. When a new generation lands, the harness compares the outputs to the previous-model baseline and flags regression. *Test the new model on the agent's actual workload. If it passes, swap in. If it regresses, hold.* Empirical, not theological.

**REID:** And where each cloud lands on model portability.

**KEVEN:** Three clouds. Walked honestly. *AWS Bedrock* — strongest multi-vendor model story today. Claude family is native; AWS and Anthropic have a deep alignment and the latest Claude models land on Bedrock often at or near launch. Beyond Claude, Bedrock catalogs Llama, Mistral, Cohere, Stability for image, and Amazon's own Titan family. The catalog breadth plus the Claude-native posture make Bedrock the cleanest multi-vendor runtime today. *GCP Vertex AI Model Garden* — Gemini is native and lands first on Vertex; the Anthropic partnership puts Claude on Vertex too, often at or near Bedrock's availability; Llama and Mistral are catalogued; Codey for code-generation tasks. The Model Garden surface is mature and the Gemini-native plus Claude-via-partnership story is strong. *Microsoft Foundry* — OpenAI is native; the OpenAI partnership and investment relationship mean the latest OpenAI models — GPT-4o, GPT-4.1, the o-series — land on Foundry first. Anthropic is available through partner integrations and an expanding multi-vendor catalog through twenty-twenty-five and twenty-twenty-six. The Foundry multi-vendor catalog is broadening; the OpenAI-native story is the strongest single-vendor story on any cloud.

**REID:** Let me push there. The honest claim is — *Bedrock has the multi-vendor lead today.* It has the cleanest single-runtime story for *I want to run multiple model families through the same agent infrastructure and pick the right model per task without leaving the runtime.* That is genuinely a Bedrock strength. Foundry has the OpenAI lead. Vertex has the Gemini lead and the Claude-via-Anthropic-partnership availability. *The cleanest model-portability story right now is to design the agent's tooling against an abstraction layer.* The architectural commitment is to express the agent above the model layer. Model versions are deployable artifacts; the agent is the durable asset.

**KEVEN:** Conceded cleanly. The multi-vendor lead is Bedrock's today. The architectural posture I recommend to sellers is — *Foundry on Microsoft-primary workloads gives the OpenAI-native depth. Bedrock on AWS-primary workloads gives the multi-vendor depth. Vertex on GCP-primary workloads gives the Gemini-native plus Claude-via-partnership depth.* In all three, the agent design is model-portable at the abstraction layer the runtime exposes. The seller does not have to compromise the principle to recommend any cloud. *Models are deployable artifacts. Agents are durable assets.* Said exactly that way. Models will refresh every nine to eighteen months. The agent should not refresh that fast. The agent's design — its prompts, its tools, its orchestration logic, its evaluation harness — is the durable part. Treat models like deployable artifacts and agents like durable assets, and the refresh cycle stops being existential for the portfolio.

### When multi-cloud is legitimate vs theatre

**REID:** And now the framing the seller needs in the room. *When is multi-cloud legitimate, and when is it theatre?* Be specific.

**KEVEN:** Walking it. The legitimate cases first. *Regulatory data residency.* Some data — by regulation, by sovereign-cloud requirement, by jurisdiction-specific privacy law — has to live in a specific cloud or geography that one cloud serves better than another. EU AI Act provisions on regulated AI workloads. GDPR data-locality. Emerging US state regulations on AI accountability. Industry-specific frameworks — pharmaceutical record-keeping, financial-reporting-adjacent retention, public-sector accreditations. When the regulation says *this data lives here*, the cloud choice is not optional. Multi-cloud is legitimate because compliance is non-negotiable.

**REID:** And the source-data gravity case.

**KEVEN:** *Source-data gravity.* When the client's authoritative data of record already lives in one cloud at scale — the petabyte S3 estate that has been the system of record for fifteen years, the BigQuery warehouse that holds the entire commercial transaction history, the ADLS lake that contains every manufacturing telemetry record — moving that data is prohibitive in both egress cost and operational risk. The honest architectural answer is to put the agentic workload on the cloud where the data already lives. *Data gravity wins over cloud preference.*

**REID:** And the model-family case.

**KEVEN:** *Model-family preference.* When the client has a strong preference for a specific model family — Claude-native for a regulated-content review workflow, Gemini-native for a multimodal grounding scenario, OpenAI-native for a specific tool-use pattern — and the preferred model lands first and most natively on one cloud, the workload goes where the model lives. Bedrock if the workload is Claude-native. Vertex if Gemini-native. Foundry if OpenAI-native. *Model availability is a legitimate input to the cloud choice.*

**REID:** And M&A inheritance.

**KEVEN:** *Enterprise-architecture inheritance.* From the cold open. Subsidiaries acquired over years, each on a different primary cloud, each with operational practices built around that cloud. Forcing consolidation is expensive, politically charged, and rarely produces the projected savings on the promised timeline. Living with the inheritance and engineering the seams is usually the better economic answer. *M&A inheritance is a legitimate multi-cloud condition.*

**REID:** Now the theatre cases.

**KEVEN:** Theatre cases. *We don't want vendor lock-in.* When a CIO says that without an accompanying architectural commitment to portability discipline — without versioned prompts, tool abstractions, model-agnostic SDKs, evaluation harnesses — the lock-in framing is theatre. The architecture is not portable; it is just split. Splitting workloads across two clouds without portability discipline produces two locked-in stacks, not one portable stack. *The architectural commitment to portability is what avoids lock-in. The cloud split does not.*

**REID:** And *cloud-agnostic on principle.*

**KEVEN:** *Cloud-agnostic on principle.* When the aspiration is *everything must run identically on every cloud,* the result is usually a least-common-denominator architecture that doesn't use any cloud's productized capabilities well. Foundry, Bedrock, and Vertex each have productized capabilities that genuinely accelerate agentic builds. A least-common-denominator architecture that refuses to use any of them leaves the program slower and less feature-complete than the engineering team could have shipped. *Cloud-agnostic on principle* is usually an architectural-elegance preference dressed up as a strategic posture.

**REID:** And the procurement framing.

**KEVEN:** *We need to negotiate with cloud vendors.* Said sometimes as a justification for multi-cloud at the architectural level. It is usually a procurement strategy, not an architecture strategy. Nothing wrong with multiple cloud commitments for procurement leverage — that is a finance function. It is not an architectural justification for forcing individual workloads to span clouds. The procurement leverage exists at the enterprise contract level, not at the workload architecture level.

**REID:** Let me push there. *Sellers need to be precise about which one the client is doing.* When the client articulates a multi-cloud rationale that is actually theatre — anti-lock-in rhetoric without portability discipline, cloud-agnostic on principle without a workload justification, procurement leverage masquerading as architectural strategy — the seller's job is to engage honestly and surface the precision. Theatre multi-cloud leads to over-architected solutions and stalled pilots. *Legitimate multi-cloud justifies the architectural discipline.* The seller who can distinguish them earns the architectural credibility. The seller who can't loses the room to one who can.

**KEVEN:** Said exactly that way. Be specific about legitimate versus theatre. Engage with the legitimate cases on their own architectural terms. Surface the theatre cases respectfully and redirect to the architectural commitment that actually addresses the underlying concern.

### A reading I want to do

**KEVEN:** I want to read briefly — paraphrased — from the kind of register Gartner, Forrester, and 451 Research have been publishing through twenty-twenty-five on multi-cloud adoption and the distinction between enterprise-level and workload-level multi-cloud.

**REID:** Go.

**KEVEN:** [reading, paraphrased — composite of Gartner cloud adoption research, Forrester multi-cloud strategy analyses, and 451 Research / S&P Global Market Intelligence multi-cloud surveys through 2024-2026]

*"Enterprise-level multi-cloud adoption remains the dominant pattern among large organizations, with most enterprises above a certain scale running material workloads on two or more major cloud providers. Workload-level multi-cloud — individual applications or workloads that span multiple cloud providers in active runtime composition — remains the exception rather than the rule. The dominant architectural pattern is workload assignment to a primary cloud based on data gravity, capability fit, and regulatory requirements, with cross-cloud composition reserved for specific integration scenarios. The economic asymmetry between intra-cloud and inter-cloud data movement is a persistent driver of this pattern. Productized cross-cloud federation capabilities — query federation, identity federation, and audit substrate composition — are maturing but do not eliminate the economic asymmetry; they reduce its impact for bounded scenarios. Enterprises planning for the twenty-twenty-six through twenty-twenty-eight window should anticipate increased regulatory and data-residency pressure expanding the legitimate workload-level multi-cloud surface, while procurement-driven and rhetoric-driven multi-cloud aspirations remain a source of over-architected solutions."*

[pause]

**REID:** *Enterprise-level multi-cloud is the norm at scale. Per-workload multi-cloud is the exception.* That distinction is what sellers conflate when they over-architect. The reading captures the architectural conversation the field is actually having, not the one the marketing teams are pitching. The framing matters. The seller who walks into a CIO conversation with the enterprise-versus-workload distinction held cleanly in mind is the seller who proposes the right architecture for the workload at hand, instead of proposing cross-cloud composition for every workload because the enterprise is multi-cloud.

**KEVEN:** Said exactly that way.

### One disagreement

**REID:** Pushback. Because this is where I have to push back if I am doing my job.

**KEVEN:** Go.

**KEVEN:** Let me state my position first, so you have something to push on. *Multi-cloud at the agentic stack level is rare. Most agentic workloads will pick a primary cloud per scenario based on data gravity, and cross-cloud composition will remain the exception through the twenty-twenty-six to twenty-twenty-eight window.* That is the architectural pattern I see today and that I expect to hold for the near term.

**REID:** I am going to push there. *Increasingly less rare.* The pattern you are describing is the twenty-twenty-four pattern. The pattern through twenty-twenty-six and beyond is going to shift, and it is going to shift in one specific direction. *Data-residency mandates.* The EU AI Act provisions phase in through twenty-twenty-five and twenty-twenty-six on regulated AI categories. GDPR is in continuous evolution on cross-border data flows. Emerging US state regulations — California, New York, Colorado, Texas — on AI accountability and consumer data are landing through twenty-twenty-six. Sector-specific frameworks in healthcare, financial services, and public-sector are tightening. *Each of these creates a class of agentic workload where the data must live in a specific cloud or region, and where the agentic workload that reasons over that data has to either run in the same cloud or compose with the data via tightly-bounded cross-cloud federation.* Sellers planning for twenty-twenty-six through twenty-twenty-eight need to design for it more rigorously than twenty-twenty-four architects did.

**KEVEN:** Make the counter-claim sharper.

**REID:** The counter-claim is — *workload-level multi-cloud is going to become less exceptional inside the next two to three years, driven by regulatory data residency and by data-sovereignty pressure.* Not the majority pattern. Not by a long way. But less exceptional than it is now. The seller who designs only for *primary cloud per workload* and treats cross-cloud composition as an edge case will get caught in the regulatory-driven scenarios. The architectural discipline you described — federation patterns, identity continuity, audit-substrate composition, model portability — is exactly the discipline that makes the regulatory scenarios buildable. *The architecture you're describing is right. The frequency you're predicting is too low.*

**KEVEN:** Let me concede part and hold part. Concede — the regulatory pressure is real. The data-residency surface is expanding. The frequency of legitimate workload-level multi-cloud will increase through twenty-twenty-six to twenty-twenty-eight. Hold — the dominant pattern remains primary-cloud-per-workload, and the exception is justified per scenario. Convergence — both are right at different timescales. The architectural discipline serves both. *The right design discipline is portable-by-default, single-cloud-by-default-execution.* Build the architecture so multi-cloud is achievable when justified. Default to single-cloud execution per workload to keep things operationally simple. When the regulatory scenario lands, the architecture is ready. When the regulatory scenario does not apply, the operational simplicity holds.

**REID:** That is the convergence. *Portable-by-default, single-cloud-by-default-execution.* The phrase carries the discipline. The seller carries the phrase.

**KEVEN:** Said exactly that way.

### What to carry forward

**KEVEN:** Three things.

**REID:** Go.

**KEVEN:** *One — the Acceleration Framework is architecturally cloud-portable by design. The Five Principles are vendor-neutral. Gold-Tier-First, Governance-and-Ledger, Identity Continuity, No Replication, Model Portability — every one of them is achievable on Microsoft, on AWS, and on GCP. The productized-capability density varies. The architecture does not. Microsoft earns the recommendation on productization density across the principles, particularly on the governance and ledger substrate. The architecture itself is not Microsoft-locked. The seller defends Microsoft on productization. The seller defends the framework on architecture. Both honest; both holdable in front of a CIO who knows the substance.*

*Two — primary cloud means primary cloud per workload. Enterprise multi-cloud is the norm at scale. Per-workload multi-cloud is the exception that requires explicit justification. The legitimate cases are regulatory residency, source-data gravity, model-family preference, and M&A inheritance. The theatre cases are anti-lock-in rhetoric without portability discipline, cloud-agnostic on principle, and procurement strategy masquerading as architecture. The seller must be precise about which one the client is doing. The architectural posture — portable-by-default, single-cloud-by-default-execution. Build for portability. Default to operational simplicity. When the legitimate case lands, the architecture is ready.*

*Three — model portability is its own architectural discipline. Not a slogan. Four pieces. Versioned prompts in source control. Tool-call abstractions expressed model-independently. Model-agnostic SDKs — Agent Framework, Bedrock Agents, Vertex AI Agent Builder — used in their multi-model mode. Evaluation harnesses that run the same scenarios across model versions to detect regression. Models will refresh every nine to eighteen months across the major families. Agents should not refresh that fast. Models are deployable artifacts; agents are durable assets. Bedrock has the multi-vendor model lead today; Foundry has the OpenAI-native lead; Vertex has the Gemini-native plus Claude-via-partnership lead. The architectural commitment to model portability rides on top of any of the three runtimes.*

**REID:** And the seller's framing from the disagreement — *portable-by-default, single-cloud-by-default-execution.* Held in tension on purpose. The discipline absorbs the regulatory pressure when it arrives. The simplicity holds when it does not. The seller carries both.

**KEVEN:** Portable-by-default, single-cloud-by-default-execution. Said exactly that way.

**REID:** Next episode — *The Seller's Playbook.* The Acceleration Framework as the architectural pitch. Five honest claims the seller can defend. Four overclaims to avoid. Six pushback-handling talking points. The six discovery openers. When to recommend NOT Microsoft. The honest sales motion that holds up across the cross-cloud conversation we've spent seven episodes building toward.

**KEVEN:** See you there.

[outro]

---

## Further reading

### Industry analyses
- **Gartner** — multi-cloud market research, cloud adoption surveys, AI infrastructure trend reports
- **Forrester** — cloud strategy and portability research, multi-cloud architecture analyses
- **451 Research / S&P Global Market Intelligence** — multi-cloud adoption data and enterprise cloud surveys
- **IDC** — multi-cloud forecasts and enterprise cloud-strategy research

### Microsoft Learn
- **Microsoft Entra B2B** — federation IN to Entra from external identity providers
- **Azure Arc** — multi-cloud and hybrid management surface
- **Microsoft Fabric** — cross-cloud Shortcuts and Mirroring patterns
- **Microsoft Agent Framework SDK** — model-agnostic agent authoring patterns

### AWS documentation
- **AWS IAM federation patterns** — SAML 2.0, OIDC, cross-account roles
- **AWS Bedrock Model availability** — Claude, Llama, Mistral, Cohere, Stability, Titan
- **Cross-account IAM roles** — workload identity across AWS accounts and external providers

### Google Cloud documentation
- **Workload Identity Federation** — short-lived credential federation from external workloads
- **Vertex AI Model Garden** — Gemini, Claude via Anthropic partnership, Llama, Mistral, Codey
- **BigQuery Omni** — cross-cloud federated query against S3 and ADLS

### Model availability (cross-cloud)
- **OpenAI** — model availability across clouds; Azure OpenAI as the primary enterprise surface
- **Anthropic** — Claude availability on Bedrock, Vertex AI via partnership, and Microsoft partner integrations
- **Google DeepMind** — Gemini availability across Vertex AI and partner integrations
- **Meta Llama** — open-model availability across Bedrock, Vertex AI Model Garden, and self-hosted patterns

### From the Acceleration Framework
- **Episodes 1-6** — the architecture this episode tests under multi-cloud reality
- **Episode 8** (next) — The Seller's Playbook

---

**End of Episode 07 · Multi-Cloud Reality, Cloud Portability, and Model Portability**
*≈ 5,800 words · target 30 minutes at conversational pace*
