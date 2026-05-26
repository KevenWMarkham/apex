# Episode 08 · The Seller's Playbook

**Builds on:** Episodes 1-7 (the architecture and FinOps and multi-cloud) · Trilogy — Sellers Eps 2 + 8 (Independence and pursuit discipline) · Disney Account Podbook Ep 5 (account-team playbook pattern)
**Run time:** ≈ 32 minutes target
**Last updated:** 2026-05-14

---

## Cold Open

[Sound: a Microsoft seller's home office. Friday afternoon. The light is long and amber through a single window. A laptop closed on one corner of the desk. A coffee cup. Three pieces of paper laid out side by side across the working surface — printed, annotated by hand, slightly creased at the corners from being carried in a portfolio for a week. The faint hum of an HVAC fan in the background and the quiet of a house at the end of a working week.]

**KEVEN:** I want to start tonight in a Microsoft seller's home office. Friday afternoon. Late. The seller has a meeting Monday morning with a new prospect — a global enterprise the seller has never sat with before. The CIO will be in the room. Two direct reports. An outside advisor the CIO trusts. Forty-five minutes on the calendar. The agenda is one line — *agentic AI architecture, cloud strategy, and Deloitte's point of view.*

**REID:** And what's on the desk.

**KEVEN:** Three pieces of paper. *The first one is the Acceleration Framework's Five Principles* — printed, principle names down the left, productization notes on Microsoft, AWS, and GCP across the right. *The second one is the six discovery openers* — six questions, one per principle plus FinOps, that surface the architectural pain without cloud-vendor framing. *The third one is the Independence-from-Microsoft cheat sheet* — the two-contract operating model, the no-reseller-margin discipline, the verbatim talking points for when the prospect asks whether Microsoft compensation is influencing the recommendation. Three pages. The seller's working substrate.

**REID:** Three pages. After eighteen years working with Microsoft sellers, that is the cleanest preparation artefact I have heard described.

**KEVEN:** It is the spine of the whole series. Seven episodes of architecture, FinOps, governance, multi-cloud honesty — all of it compresses into those three pages by Friday afternoon. Tonight is where we walk what is on each page. The practitioner closer. The Acceleration Framework as the architectural pitch. Five honest claims. Four overclaims. Six pushback-handling talking points. The six discovery openers. When to recommend NOT Microsoft. Wave sizing and the 90-day path. Funding programs handled Independence-clean. And the closing posture that wins both the deal and the long-term relationship.

**REID:** Episode Eight. *The Seller's Playbook.* The series finale.

**KEVEN:** Let's go.

---

## The conversation

### The Acceleration Framework as the architectural pitch

**KEVEN:** The headline. *The seller's pitch is not Microsoft is better.* Wrong opener. Every CIO in 2026 has heard it from every Microsoft seller they have met. The pitch that wins is different — *there's a right way to build agentic AI. The Acceleration Framework is that right way. Cloud-neutral. Five vendor-neutral principles. The architecture is the architecture. The cloud recommendation follows on merits.*

**REID:** Why that opener works where the other does not.

**KEVEN:** Three reasons. *One — it leads with architecture, not with vendor.* The CIO is paid to make architectural decisions, not to hand a vendor a quota retirement. *Two — it is cloud-neutral in substance.* The Five Principles are vendor-neutral by design. Said in Episode One; said every episode since. *Three — it earns the right to make a cloud recommendation later.* Once the architectural commitments are agreed, the cloud choice becomes a productization-density comparison across the principles. That is a conversation Microsoft can win honestly on most of them.

**REID:** And the contrast with the partner-channel motion.

**KEVEN:** Sharp. The partner-channel motion is *Microsoft is the right answer because Microsoft is the right answer.* Circular. Works in rooms where the CIO has already decided. Fails in rooms where the CIO is genuinely choosing. The architectural motion survives a sophisticated architect's scrutiny — and the Deloitte AI team architect who has shipped on Bedrock and Vertex respects it. The partner-channel motion is the one the AI team quietly routes around.

**REID:** Said exactly that way. The framework is the spine. Microsoft earns the recommendation on top of the framework, not in place of it.

### Microsoft's productization advantage — per principle

**REID:** Walk it. Principle by principle. Honest comparison. No theatre.

**KEVEN:** *Principle One — Gold-Tier-First.* *Microsoft Fabric is the broadest productized story today.* Bronze on OneLake, Silver canonical, Gold per-scenario — all in one SaaS surface. *AWS Lake Formation plus Glue plus Athena plus Iceberg* — mature services, four to compose. *GCP BigQuery plus BigLake plus Dataplex* — the closest competitor on naturalness. Microsoft is *broadest productized;* GCP is close; AWS is most assembly-required.

**REID:** And the seller's defensible claim on Principle One.

**KEVEN:** *Microsoft Fabric is the broadest productized medallion-pattern story; GCP BigQuery plus BigLake plus Dataplex is the closest competitor; AWS is most assembly-required.* *Principle Two — Governance, Audit, and the Ledger Pattern.* This is where Microsoft is most differentiated today. *Purview is one product that covers catalog plus lineage plus access plus sensitivity plus DSPM-for-AI.* AWS requires four to six services composed — Lake Formation, Macie, CloudTrail, IAM, Glue Catalog. GCP Dataplex covers most of the surface; closer to productized than AWS. *And the ledger pattern itself exists as productized reference architecture on Foundry today. AWS and GCP can build it; Microsoft has it productized.*

**REID:** And the twelve-month-window framing.

**KEVEN:** *Microsoft's productization lead on governance and ledger is real today. The lead is not permanent.* AWS is investing; the assembly gap narrows through twenty-twenty-six. GCP is investing too. *The twelve-month window is when the lead is most defensible.* After that, re-evaluate against the actual product landscape.

**REID:** Principle Three.

**KEVEN:** *Principle Three — Identity Continuity.* This one splits cleanly. *Microsoft Entra has the broadest enterprise SaaS federation surface* — M365 plus SAP plus Salesforce plus Workday plus ServiceNow plus thousands more. *GCP Workload Identity Federation has the cleanest cross-cloud agent-identity primitive* — short-lived, scoped, rotated. *AWS IAM plus Identity Center plus Cognito requires the most assembly.* Microsoft wins on enterprise SaaS federation; GCP wins on cross-cloud agent identity. Both honest.

**REID:** Principle Four.

**KEVEN:** *Principle Four — No Replication. Sources Stay Untouched.* *Microsoft Fabric Mirroring plus Shortcuts plus Eventstreams is the broadest productized source-mirroring story* — Snowflake, Databricks, Cosmos DB, Azure SQL, Postgres, Oracle. *GCP BigQuery Omni is the strongest cross-cloud federation primitive.* *AWS Athena Federated Query has the broadest source-connector catalog with most assembly.* Microsoft broadest productized; GCP strongest cross-cloud; all three credible.

**REID:** And the deep one. Principle Five.

**KEVEN:** *Principle Five — Model Portability.* Microsoft does not win on multi-vendor model selection. *AWS Bedrock has the multi-vendor lead* — Claude family native, Llama, Mistral, Cohere, Stability, Titan. *GCP Vertex AI Model Garden* — Gemini-native plus Claude via Anthropic partnership. *Microsoft Foundry* — OpenAI-native lead; multi-vendor catalog broadening but not at Bedrock's breadth today. *Bedrock wins on multi-vendor model selection.*

**REID:** The honest comparison matrix.

**KEVEN:** *Sellers can defend Microsoft on Principles One, Two, and Four productization density. Sellers split honestly with GCP on Principle Three. Sellers concede Principle Five to AWS Bedrock on multi-vendor model selection while defending Foundry's OpenAI-native lead.* That matrix survives a sophisticated architect's scrutiny. The AI team respects it. The CIO trusts it.

### Independence-minded framing — the operating model

**REID:** The commercial layer. The architecture is the architecture, but the seller operates under a specific commercial discipline that protects the architecture from drifting into vendor-loyalty pitching.

**KEVEN:** The operating model. *Deloitte recommends on technical and economic merits.* *The two-contract model — three contracts when NVIDIA is in scope.* Client contracts with the platform vendor on platform paper. Client contracts with Deloitte on Deloitte paper. Separate contracts. No reseller margin. No partner-channel motion. No compensation flows from platform vendors to Deloitte for influencing client choices.

**REID:** And the verbatim cheat-sheet language.

**KEVEN:** Five lines. *One — the recommendation is on merits, not on compensation.* *Two — the client contracts with the platform vendor on platform paper.* Microsoft on Microsoft paper. AWS on AWS paper. GCP on GCP paper. NVIDIA on NVIDIA paper. *Three — the client contracts with Deloitte on Deloitte paper.* Separately. *Four — no reseller margin.* Deloitte does not mark up Microsoft licensing. *Five — no partner-channel motion.* The seller operates as an independent advisor — no commercial constructs that tie Deloitte's recommendation to platform-vendor compensation. The seller's language reflects that discipline; the vocabulary of vendor-aligned selling is absent. Five lines. The seller memorizes them.

**REID:** Let me push there. *This is the discipline that earns long-term client trust — short-term it can lose deals against sellers who don't operate this way; long-term it wins the relationship.* The short-term picture is uncomfortable. A seller competing against partner-channel sellers who can underprice through reseller economics is at a price disadvantage on the line item. *Short term, Independence is a competitive disadvantage on price.* The seller has to know it going in.

**KEVEN:** And the long-term picture.

**REID:** *Long term, Independence is the discipline that wins the relationship.* The CIO who buys from the partner-channel seller learns over time that the recommendation was conflated with the compensation. *At the relationship-renewal moment — the second engagement, the third — the Independence-minded seller's win rate is higher.* The patience required is real. The compounding is real. Independence is the long game.

**KEVEN:** Short-term can lose deals. Long-term wins the relationship. The seller carries both into the room.

### Five honest claims sellers can defend

**KEVEN:** Five claims. The credibility substrate. Each defendable in front of a sophisticated client architect and the Deloitte AI team listening in the back.

**REID:** Walk them.

**KEVEN:** *Claim One — Microsoft has the most productized DSPM-for-AI capability on the market today.* Purview DSPM for AI covers AI-content discovery, sensitivity classification on AI inputs and outputs, policy enforcement, integration with the broader Purview substrate. AWS Macie composed with Lake Formation plus Bedrock Guardrails approximates the coverage as engineering work. GCP Sensitive Data Protection plus Dataplex AI governance covers most of the surface, less integrated. *True today; the twelve-month window applies; defendable.*

**REID:** Claim Two, three, four, and five — run them.

**KEVEN:** *Claim Two — Microsoft has the most productized hash-chained ledger pattern reference architecture for agent audit chains.* The pattern from Episode Five — audit-row-per-step with hash chain, replay token, append-only retention — is productized as reference architecture on Foundry. AWS and GCP can build it. CloudTrail plus QLDB plus assembly. Cloud Audit Logs plus BigQuery-backed ledger plus assembly. *Microsoft has the productized reference; the others require engineering.* Defendable.

*Claim Three — Microsoft Entra ID has the broadest enterprise SaaS federation surface.* The Entra application gallery is the broadest catalog of any cloud — M365, SAP, Salesforce, Workday, ServiceNow, thousands more pre-built connectors with mature B2B and B2C surfaces. AWS IAM Identity Center and GCP Cloud Identity have growing SaaS federation; not at Entra's catalog scale. *True for the enterprise-SaaS-federation surface; defendable.*

*Claim Four — Microsoft Fabric Mirroring is the broadest productized source-mirroring story for the No-Replication pattern.* Snowflake, Databricks, Cosmos DB, Azure SQL, Postgres, Oracle — the catalog covers the dominant operational and analytical source types and is broadening on a quarterly cadence. AWS Athena Federated Query has more federated-query connectors — that is federated query, not mirroring. GCP BigQuery Omni is cross-cloud federation, not source mirroring. *Across source types for the mirroring use case specifically, Microsoft is broadest.* Defendable.

*Claim Five — Deloitte operates Independence-clean.* Microsoft licensing and Deloitte services are separate contracts on separate paper, no margin stacking, no reseller motion, no compensation flowing from Microsoft to Deloitte for influencing the client's cloud choice. *The claim is verifiable.* The client can request the contract structure. The client can verify that Deloitte's revenue from the engagement comes from the client's contract with Deloitte, not from Microsoft's contract with the client. Operating discipline; verifiable; defensible.

**REID:** Five claims. All defendable. All honest. All survive scrutiny.

### Four overclaims to avoid

**REID:** The four overclaims. The ones a seller might say naively and not understand what they cost.

**KEVEN:** *Overclaim One — Microsoft's agent runtime is better.* FALSE on capability parity. *Foundry, Bedrock, and Vertex AI are all production-grade agent runtimes today.* Different feature mixes; all three credible for serious agentic workloads. *Don't pitch this.*

**REID:** Two through four.

**KEVEN:** *Overclaim Two — Microsoft has more available models.* FALSE. *AWS Bedrock has the multi-vendor lead today.* Claude family native, Llama, Mistral, Cohere, Stability, Titan. Microsoft Foundry has the OpenAI-native depth; the catalog is broadening but does not match Bedrock's breadth today. *Don't pitch this.*

*Overclaim Three — Microsoft is more NVIDIA-aligned.* FALSE. *NVIDIA runs equally on all three clouds.* NVIDIA AI Enterprise, Triton, NIM, NeMo, Omniverse — every part of the NVIDIA stack is supported on Azure, AWS, and GCP. NVIDIA is platform-neutral by NVIDIA's own design and commercial structure. *Don't pitch this.*

*Overclaim Four — Microsoft is the only one with audit trails.* FALSE. *All three clouds can build the ledger pattern.* AWS has CloudTrail plus QLDB or DynamoDB. GCP has Cloud Audit Logs plus BigQuery-backed ledger. Microsoft has the pattern productized as reference architecture; AWS and GCP require engineering. *The pattern is buildable on all three. Don't pitch this.*

**REID:** *Pitching any of these four loses credibility with the Deloitte AI team AND with sophisticated client architects.* The seller who says any of them in front of a Deloitte AI architect earns a polite redirect at best and a quiet routing-around at worst. The seller who says any of them in front of a client architect who has built on AWS or GCP loses architectural credibility for the rest of the engagement. *Sellers who learn to NOT say these four lines protect the long-term relationship.*

**KEVEN:** The four overclaims are the four shortest paths to losing the room. The discipline is to not say them. The discipline pays off every time the seller does not say them.

### Six pushback-handling talking points

**REID:** The talking points. Every cross-cloud CIO conversation in 2026 produces at least one of these six pushbacks. The seller has to have the verbatim language ready.

**KEVEN:** *Pushback One — we're AWS-primary.* The response.

*"Understood. The Acceleration Framework is architecturally portable — the Five Principles work on AWS. We can architect on AWS. The honest comparison is on productization density per principle: AWS is most assembly-required on governance, broadest on multi-vendor model selection, strong on data foundation if your data is already on S3. Where's your team's preferred starting point?"*

**REID:** Pushback Two.

**KEVEN:** *Pushback Two — we're GCP-primary.* The response.

*"Understood. GCP is the closest competitor to Microsoft on productized governance via Dataplex. BigQuery Omni is the strongest cross-cloud federation. Workload Identity Federation is the strongest cross-cloud identity. The honest gap is in productized DSPM-for-AI and the ledger reference architecture today. The architecture is the architecture; cloud choice is on merits."*

**REID:** Pushback Three.

**KEVEN:** *Pushback Three — Deloitte should be cloud-agnostic.* The response.

*"At the architecture layer, we are. The Acceleration Framework is vendor-neutral by design. At the implementation layer, we recommend on technical and economic merits per client per workload. We're agnostic about which cloud you should use; we're not agnostic about which architecture works."*

**REID:** Pushback Four. The hardest one.

**KEVEN:** *Pushback Four — Microsoft compensation is influencing the recommendation.* The response.

*"Our Independence model is the two-contract operating model. Client contracts with Microsoft directly on Microsoft paper. Client contracts with Deloitte directly on Deloitte paper. No reseller margin. No partner-channel compensation flowing to Deloitte for influencing your choice. The recommendation is on merits; you can verify by checking that Deloitte's revenue from this engagement comes from your contract with us, not from Microsoft's contract with you."*

**REID:** And the seller has to be able to say that without flinching, because the question is asked by every serious CIO who has been in the chair more than a few years.

**KEVEN:** Without flinching. The two-contract framing is verifiable. *Pushback Five — we want portability later.* The response.

*"That's the right discipline. The Acceleration Framework's Five Principles are vendor-neutral by design. Wave 1 lands on a primary cloud per workload because cross-cloud egress economics and identity federation make per-workload portability the wrong default. The architecture stays portable; the execution starts primary-cloud."*

**REID:** Pushback Six.

**KEVEN:** *Pushback Six — we don't want our data replicated into a new lake.* The response.

*"Right answer. Principle 4 is 'No Replication — Sources Stay Untouched.' Virtualization, mirroring, shortcuts, federation. Fabric Mirroring, BigQuery Omni, Athena Federated Query. Your SORs stay where they are. Your DWs stay where they are. Streams stay live. The Acceleration Framework doesn't fight that — it depends on it."*

**REID:** Six pushbacks. Six verbatim responses. The seller carries the six like the seller carries the five claims and the four overclaims.

### When to recommend NOT Microsoft

**REID:** The section every Microsoft seller has to be able to walk. *When does the honest recommendation point away from Microsoft.* The Independence-minded seller says this out loud. The partner-channel seller does not.

**KEVEN:** Four cases. *Case One — AWS-resident data gravity at scale.* If the client's data is overwhelmingly on AWS — petabyte S3 estate, decade of operational telemetry, the warehouse on Redshift — *building the Gold Tier on AWS is the right call.* Egress economics push that way. The honest first move is Athena Federated Query, Lake Formation, and a Gold Tier composed inside AWS. Microsoft composes at the seams. Say so.

**REID:** Case Two.

**KEVEN:** *Case Two — GCP-strategic posture at the enterprise architecture office.* If the EA office has committed to GCP — standardization decision was made, operational practices are GCP-native, the data engineering team has invested in BigQuery and Dataplex — *fighting that commitment is the wrong battle.* Compose, do not displace. Say so.

**REID:** Case Three.

**KEVEN:** *Case Three — multi-cloud regulatory mandate.* When regulations require multi-cloud — EU AI Act provisions, sovereign cloud requirements, sector-specific frameworks — *design for multi-cloud honestly.* The discipline from Episode Seven applies. Portable-by-default, single-cloud-by-default-execution.

**REID:** Case Four.

**KEVEN:** *Case Four — Anthropic-on-Bedrock or Gemini-on-Vertex model preference.* If the client's preferred model is native on AWS or GCP — Claude for regulated-content review on Bedrock, Gemini for multimodal grounding on Vertex — *that cloud often wins for that workload.* Model availability is a legitimate input to the cloud choice.

**REID:** *The sellers who say in some cases Microsoft is not the right answer earn more credibility than sellers who never say it.* The CIO who hears the seller acknowledge the four cases trusts the seller's Microsoft recommendation in every case where Microsoft genuinely is the right answer. *The credibility compounds.* The seller who never says it is the seller the CIO assumes is selling Microsoft regardless of the architecture.

**KEVEN:** The sellers who name the four cases honestly earn the right to be trusted on every recommendation that follows. The CIO does not need the seller to be Microsoft-only. The CIO needs the seller to be architecturally honest about where Microsoft fits and where it does not. *Independence-minded selling is the long game.*

### The six discovery openers — one per principle plus FinOps

**REID:** The discovery substrate. The questions that surface the architectural pain without cloud-vendor framing. Six openers. One per principle plus FinOps.

**KEVEN:** *Opener One — Are your agents currently pointing at SORs or your data warehouse directly?* Surfaces the Gold-Tier-First conversation. Principle One. *Yes, our agent points at our warehouse* — Wave 1 foundation problem. *We don't have agents yet* — greenfield. *We have a Gold Tier on Snowflake* — federation conversation. One question; three architectural conversations.

**REID:** Opener Two.

**KEVEN:** *Opener Two — How are you handling AI governance and audit for agent decisions today?* Surfaces the Trust Substrate conversation. Principle Two. *We haven't gotten there yet* — governance-gap entry point. *CloudTrail and we figure that's enough* — the difference between an audit log and an audit row. *We have a hash-chained ledger* — sophisticated architect who respects the productized reference. The substrate is the conversation.

**REID:** Opener Three.

**KEVEN:** *Opener Three — What identity does your agent run as, and how does that identity propagate to source access?* Surfaces the Identity Continuity conversation. Principle Three. *The agent runs as a service principal with read access to everything* — translation-gap problem. *We federate operator identity through to source* — sophisticated identity architect. *We haven't thought about that* — Wave 1 cross-cutting design point. Identity is the conversation.

**REID:** Opener Four.

**KEVEN:** *Opener Four — Are you replicating data into a new lake to make AI work, or are your operational sources staying untouched?* Surfaces the No-Replication conversation. Principle Four. *We're standing up a new lake* — replication-cost conversation. *Our SORs stay where they are* — aligned architect. The sources answer the conversation.

**REID:** Opener Five.

**KEVEN:** *Opener Five — How model-portable is your agent design — could you swap GPT for Claude tomorrow if you needed to?* Surfaces the Model Portability conversation. Principle Five. *We'd have to rewrite the agent* — four-discipline conversation. *We have a model abstraction layer and we routinely swap* — sophisticated architect. The portability discipline is the conversation.

**REID:** Opener Six.

**KEVEN:** *Opener Six — What's your AI consumption cost trajectory looking like quarter-over-quarter?* Surfaces the FinOps conversation. Episode Six. *Up thirty-five percent QoQ* — the CFO conversation from Episode Six's cold open. *We haven't measured it* — visibility-and-accountability entry point. *Under control via model-mix optimization* — mature FinOps-for-AI practice. The cost lever is the conversation.

**REID:** Six openers. Together they surface the architectural pain without cloud-vendor framing. The seller's discovery substrate.

**KEVEN:** Six architectural questions. No vendor framing. No partner-channel motion. No Microsoft-loyalty pitch. The seller walks in with the six in their head and surfaces the architectural pain inside the first twenty minutes of any agentic-AI discovery conversation. The framework does the rest.

### Wave sizing and the 90-day pilot path

**REID:** The execution layer. The architectural conversation has to land in a deliverable Wave 1.

**KEVEN:** *Good Wave 1 has four properties.* *Operational* — real decision flow with a current owner. Not a research project. *Contained* — one clear use case with one clear ROI metric. The scope discipline protects the timeline. *Measurable* — success metric defined before the build, baseline captured. *Aligned to existing data assets* — Wave 1 does not also rebuild the data foundation.

**REID:** And what kills agentic projects.

**KEVEN:** Four killers. *Scope creep — Wave 1 becomes boil the ocean.* The ninety-day pilot becomes a nine-month rebuild. *Ungoverned model proliferation* — fifteen agents on twelve models with no abstraction layer. *Cost shock* — no FinOps story, CFO sees thirty-five percent QoQ growth and pulls funding. *Audit posture afterthought* — the ledger pattern is bolted on, the auditor asks for replay evidence, the substrate is not there. Four killers. Each one fatal. Wave 1 design addresses each.

**REID:** And the 90-day cadence.

**KEVEN:** *Thirty-thirty-thirty.* Thirty days discovery — confirm the use case, validate data access, scope the agent's reasoning surface, scope the audit substrate, validate Independence framing with client legal. Thirty days build — agent, Gold Tier slice, audit row, HITL design, evaluation harness. Thirty days HITL validation — humans in the loop at decision points, side-by-side with current process, metric capture, audit-row inspection, replay validation. *Day ninety is the pilot decision.* Continue to Wave 2 or hold and refactor. The decision is data-grounded and the audit substrate supports the decision either way.

### Funding programs — Independence-clean handling

**REID:** And the funding programs. Cloud-vendor funding is a real input to pilot economics and the seller has to handle it Independence-clean.

**KEVEN:** Three programs. *Microsoft BVA plus ECIF plus Azure Credits* — Microsoft funds discovery and POC. *AWS ProServe credits plus MAP* — AWS funds equivalent. *GCP Cloud Innovation Credits plus Customer Success Manager engagement* — GCP equivalent.

**REID:** And the Independence-clean framing.

**KEVEN:** *Cloud-vendor funding flows to the client.* Funding subsidizes the client's discovery, POC, early production. *Funding does not flow to Deloitte for influencing the cloud choice.* The client may apply for funding from whichever cloud vendor the client is considering — that is the client's commercial relationship, not the seller's commercial motion. Deloitte's services are still billed to the client on Deloitte paper. *The two-contract model holds.* The funding sits inside the client-vendor contract, not inside the client-Deloitte contract.

**REID:** And the seller's role.

**KEVEN:** *The seller informs the client that funding programs exist on all three clouds.* The seller connects the client to the cloud-vendor account team. The seller does not negotiate the funding terms; that is between the client and the cloud vendor directly. *Awareness and connection, not commercial intermediation.* The discipline keeps the recommendation on merits.

### Closing posture — the series finale closer

**REID:** The closing. The series-finale closing. Bring it home.

**KEVEN:** *The Acceleration Framework is the architectural pitch.* *The Five Principles are the architectural commitments.* Gold-Tier-First. Governance plus Audit plus Ledger. Identity Continuity. No Replication. Model Portability. *The Six Discovery Openers are the practitioner substrate.* Six questions that surface the architectural pain without cloud-vendor framing.

**REID:** And the cloud recommendation.

**KEVEN:** *Microsoft earns the recommendation on productized-capability density across the principles.* Defendable claims on governance density, ledger productization, enterprise SaaS federation, source mirroring, OpenAI-native depth. Honest concessions where they're due — Bedrock on multi-vendor model selection, GCP on cross-cloud agent identity. *Independence is the operating model.* Two contracts. Three when NVIDIA. No reseller margin. No partner-channel motion. Recommend on merits.

**REID:** And the practitioner closer.

**KEVEN:** *The Microsoft seller who carries this into client conversations doesn't pitch Microsoft. They pitch the right way to build agentic AI.* The cloud recommendation follows on merits. The architectural pitch earns the room. The honest comparison matrix survives the architect's scrutiny. The Independence framing earns the long-term relationship. *That is the operating model that wins both the deal and the long-term relationship.*

**REID:** Let me close with the long-game framing. *The sellers who get this right are the ones the Deloitte AI team will defend. The sellers who don't are the ones the AI team will quietly route around.* The AI architect who has built on Bedrock and Vertex respects the seller who acknowledges Bedrock's multi-vendor lead and Vertex's cross-cloud federation strength. The architect routes around the seller who pitches *Microsoft is better* without architectural substance. *Independence-minded selling is the long game.*

**KEVEN:** Eight episodes. The Acceleration Framework. The Five Principles. The Six Discovery Openers. The five honest claims. The four overclaims to avoid. The six pushback-handling talking points. The Independence operating model. The wave-sizing discipline. The funding programs handled Independence-clean. *This is the seller's working substrate.* Three pages on the desk by Friday afternoon. Monday morning, the seller walks into the room and the framework holds. See you in the field.

### A reading I want to do

**KEVEN:** I want to read briefly — paraphrased — from the register the Trilogy Sellers Episode 2 carries on the commercial arc. The line about Independence-minded selling being the long game.

**REID:** Go.

**KEVEN:** [reading, paraphrased — composite of Trilogy Sellers Episode 2 *The Commercial Arc* register and the Sellers Handbook closing on long-term advisory selling]

*"The architectural pitch earns the room. The productization comparison earns the recommendation. The Independence framing earns the trust. The trust is what survives the renewal moment. Sellers who optimize for the trust win at the renewal. Sellers who optimize for the deal win the deal and lose the next two. The compounding lives in the renewals. The renewals live in the trust. The trust lives in the discipline. Independence-minded selling is the long game. The patience required is real. The compounding is real. The relationship is the asset that justifies the seller's place across multiple engagements, multiple budget cycles, and multiple architecture refresh waves."*

[pause]

**REID:** *The patience required is real. The compounding is real.* The seller who walks into Monday's meeting with the three pages on the desk and the framework in mind has the patience artefact ready. The patience is the work. The compounding does the rest.

**KEVEN:** Said exactly that way. The reading lands.

### One disagreement — the final disagreement of the series

**REID:** The pushback. The finale; the disagreement has to be real one more time. *Sellers WILL be tempted to skip the cross-cloud honest comparison and just pitch Microsoft.* Every quarter. Every deal. The seller has a quota; the quota retires faster on a Microsoft-loyalty pitch in some rooms than on an architectural-honesty pitch. *Short term, the partner-channel motion wins more deals than the Independence-minded motion. The discipline is hard to maintain.* The architectural-honesty motion is a different muscle and it atrophies fast if it is not exercised. The temptation does not go away.

**KEVEN:** Concede part and counter part. *Concede the temptation.* The Microsoft-loyalty pitch retires quota in some rooms faster than the architectural pitch. The discipline is harder in year two of a quota than year one. *Counter — short-term skipping wins one deal; loses the relationship.* The CIO who hears the Microsoft-loyalty pitch in year one and discovers in year three that the architecture was wrong because the seller skipped the honest comparison is the CIO who fires the seller and finds an Independence-minded advisor for year four onward. *The Independence-minded seller's long-term win rate is higher than the partner-channel seller's, but the patience required is real.*

**REID:** And the other constituency.

**KEVEN:** *The Deloitte AI team.* The AI architect who has shipped on Bedrock and Vertex listens to the Microsoft seller's pitch and decides — *do I bring this seller into my client conversations or do I route around them.* The Microsoft-loyalty pitch fails the architect's scrutiny in the first sentence. The architectural-honesty pitch passes and earns the AI architect's defense in the room. *The partner-channel motion loses the AI team. The Independence-minded motion wins the AI team.*

**REID:** Convergence. *The discipline is hard but compounding.* The sellers who maintain it win disproportionately at the relationship-renewal moments — which is where Microsoft Account Team economics actually live. *The Independence-minded seller plays to the renewal. The partner-channel seller plays to the close.* The Independence-minded motion retires more quota over five years than the partner-channel motion does.

**KEVEN:** *The discipline is hard but compounding. The sellers who maintain it win disproportionately at the relationship-renewal moments.* The relationship is the asset. The renewals are the compounding. *Play the long game.*

### What to carry forward — series finale

**KEVEN:** Five things — series finale.

**REID:** Go.

**KEVEN:** *One — there's a right way to build agentic AI. The Acceleration Framework. Five vendor-neutral principles. Lead with architecture; cloud recommendation follows on merits.*

*Two — Microsoft earns the recommendation on productized-capability density across the principles. Defendable claims; overclaims to avoid; honest concessions where they're due.*

*Three — six discovery openers, one per principle plus FinOps. Surface the architectural pain without cloud-vendor framing.*

*Four — Independence-minded selling is the operating model. Two contracts. Three when NVIDIA. No reseller margin. No partner-channel motion. Recommend on merits.*

*Five — the discipline is hard and compounding. Short-term it can lose deals; long-term it builds the relationships that justify Account Team economics. Play the long game.*

### Sign-off

**KEVEN:** Thanks for listening to *The Cross-Cloud Agentic Podcast*. Eight episodes. About four hours total. The Acceleration Framework, the Five Principles, the Six Discovery Openers. This is the seller's substrate.

**REID:** I'm Reid. Cross-cloud principal architect. Twenty years across Microsoft, AWS, and GCP buildouts. *The honest comparison is the long-term seller's edge.*

**KEVEN:** I'm Keven. Vice President, Deloitte's Microsoft Technology and Services Practice. See you in the field.

[outro music · long]

---

## Further reading

### From the Acceleration Framework
- **Episode 01 — *The Agentic Stack and the Five Principles***
- **Episode 02 — *Data Foundation and No-Replication***
- **Episode 03 — *Agent Runtime: Talking to Gold, Not SORs***
- **Episode 04 — *Governance, Identity, and Safety for Agentic AI***
- **Episode 05 — *Audit, Ledger, and Replay***
- **Episode 06 — *FinOps for Agentic AI***
- **Episode 07 — *Multi-Cloud Reality, Cloud Portability, and Model Portability***

### Independence and commercial discipline
- **APEX Trilogy · Sellers Podcast Ep 2 — *The Commercial Arc*** — two-contract model (generalized to three-contract when NVIDIA is in scope)
- **APEX Trilogy · Sellers Podcast Ep 7 — *The Pursuit Motion*** — pursuit discipline and pursuit qualification
- **APEX Trilogy · Sellers Podcast Ep 8 — *The Sellers Dream*** — four-level ladder
- **APEX Trilogy · Sellers Podcast Ep 9 — *Functional-Area Discovery*** — the 30-Min Framework
- **APEX Trilogy · Services Podcast Ep 4 — *The MCP Boundary*** — agent runtime and tool-call abstraction

### Industry analyses
- **Gartner** — agent and AI platform market research, Magic Quadrant analyses
- **Forrester** — agentic AI Wave research, cloud strategy analyses
- **IDC** — AI platforms forecast, enterprise cloud-strategy research

### Microsoft Learn
- **Microsoft Fabric** — Mirroring, Shortcuts, OneLake, medallion architecture
- **Microsoft Foundry (Azure AI Foundry)** — agent runtime, model catalog, OpenAI-native depth
- **Microsoft Agent Framework SDK** — model-agnostic agent authoring
- **Microsoft Purview** — catalog, lineage, access, sensitivity, DSPM for AI
- **Microsoft Entra ID** — B2B federation, enterprise SaaS application gallery
- **Microsoft Power Platform** — Copilot Studio, Power Automate AI Builder

### AWS documentation
- **AWS Bedrock** — multi-vendor model catalog, Bedrock Agents, Bedrock Guardrails
- **AWS Lake Formation** — data lake permissions, fine-grained access control
- **AWS Macie** — sensitive data discovery and classification
- **AWS IAM and IAM Identity Center** — federation, SSO, cross-account roles
- **AWS CloudTrail** — audit logging and event history

### Google Cloud documentation
- **Vertex AI** — Gemini-native, Claude via Anthropic partnership, Model Garden
- **Google Cloud Dataplex** — catalog, governance, sensitive data protection
- **BigQuery Omni** — cross-cloud federated query against S3 and ADLS
- **Workload Identity Federation** — short-lived credential federation
- **Cloud Sensitive Data Protection** — DLP-style data discovery and classification

### Standards
- **EU AI Act** — regulated AI categories, governance provisions
- **NIST AI Risk Management Framework (AI RMF)** — Govern, Map, Measure, Manage
- **ISO/IEC 42001** — AI management system standard
- **OWASP Top 10 for LLM Applications** — LLM and agentic-AI vulnerabilities

### Cloud-vendor funding programs (Independence-clean)
- **Microsoft BVA / ECIF / Azure Credits** — Microsoft customer investment funds (client-facing; not a Deloitte revenue stream)
- **AWS ProServe credits / MAP (Migration Acceleration Program)** — AWS equivalent
- **GCP Cloud Innovation Credits** — GCP equivalent

### From the Cross-Cloud Agentic Podcast family
- **README.md** — series overview, the eight episodes, the Five Principles
- **00 — Show Bible and Format** — voice cast, Independence rules, forbidden vocabulary, production rules

---

**End of Episode 08 · The Seller's Playbook**
**End of *The Cross-Cloud Agentic Podcast* — series complete**
*≈ 6,200 words · target 32 minutes at conversational pace · series total ≈ 48,000 words across 8 episodes*
