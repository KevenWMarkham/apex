# Episode 04 · Governance, Identity, and Safety for Agentic AI

**Builds on:** Episodes 1-3 (principles, data foundation, agent runtime) · Trilogy — Sellers Ep 2 (Independence) · Services Ep 6 (Purview)
**Run time:** ≈ 32 minutes target
**Last updated:** 2026-05-14

---

## Cold Open

[Sound: a CISO's office. Friday afternoon. The light through the blinds is the kind of late-week amber that means everyone wants to be anywhere but here. A printout on the desk — three pages, stapled, red ink in the margins of two of them. The CISO's hand on the top page. A laptop open beside it, with a third-party penetration-test report on screen. The hum of a building HVAC settling for the weekend.]

**KEVEN:** I want to start tonight in a CISO's office. Friday afternoon, three forty-five. A printout in front of her. Red pen in two of the margins. The printout is the executive summary of a third-party penetration test that landed Wednesday. The pen-test team has identified — through a relatively unremarkable lateral-movement exercise on a non-production network — that an agentic pilot the AI team launched three months ago has been quietly accessing the customer-PII tables in production. Not just metadata. Row-level access. With a service principal that has read-customer-PII permission on the source database directly. The access has been going on the whole time the pilot has been running.

**REID:** And the audit row.

**KEVEN:** The audit row is the part that is making her hand tremble a little, in the way that a CISO's hand trembles when she is composed enough that you wouldn't notice unless you'd seen it before. The audit row shows the service principal accessed the table. It does not show the human who configured the service principal. It does not show who authorised the access. It does not show whether the data crossed any sensitivity boundary on the way out. The DLP policy didn't flag it, because the DLP policy was written for human users on workstation endpoints, not for service principals on agent runtimes. There is no identity continuity gap visible in any tool the CISO owns, because the gap is the *absence* of a tool — the absence of the AI-aware data-security posture management layer that would have caught this on the day the pilot went live.

**REID:** And the question she has for the AI team.

**KEVEN:** The question she has for the AI team is the question that defines this episode. *How does this not happen at scale?* Because the pilot is a pilot. Six operators. One workload. One source. And it slipped past every governance control she owns. The plan is to scale this to two hundred operators, twelve workloads, and fourteen sources over the next eighteen months. At that scale, this same failure mode shows up in places nobody is going to find with a third-party pen test. It shows up in regulatory disclosure six months later.

**REID:** And the answer is not — *we'll write better playbooks.* The answer is architectural. Because the gap she just found is not a discipline gap. It is a control-plane gap.

**KEVEN:** Control-plane gap. Said exactly that way. And that's the episode. *Governance, Identity, and Safety for Agentic AI.* Principles Two and Three and the safety thread that ties them together. Purview. DSPM for AI. Entra. AWS IAM. Workload Identity Federation. EU AI Act. NIST AI RMF. ISO forty-two thousand and one. Bedrock Guardrails. Vertex AI Safety. Azure AI Content Safety. The control plane the CISO needed. Let's go.

---

## The conversation

### Why governing an agent is different from governing a human or a traditional ML pipeline

**KEVEN:** Let's start with the why. Because every governance conversation I've been in on the agentic side starts with somebody — usually a thoughtful enterprise architect who's been doing this for twenty years — saying *we have governance. We have DLP. We have RBAC. We have an approval workflow. Why is the agent different?* And the honest answer is — the agent breaks three assumptions traditional governance was built on.

**REID:** Walk the three.

**KEVEN:** *One — data access is dynamic.* Traditional governance was built on the assumption that data access is statically permissioned. The human user has a role. The role has permissions. The permissions are reviewed quarterly. The access pattern is — log in, do the thing you're permissioned for, log out. The agent breaks that. The agent's data access is decided at reasoning time. The agent looks at the question, reasons about which sources it needs, decides which Gold views to query, and reaches for them. Across a session, the agent might touch eight different Gold views composed from twenty different source-system origins. The set of data the agent touches is not knowable in advance. It is emergent from the reasoning.

**REID:** And the traditional access-review process — *here are the permissions this principal has, do they still need them* — collapses on that, because the principal has read access to everything the agent might ever need, which by design is everything composable from the data foundation.

**KEVEN:** Exactly. *Two — tool calls are high-velocity.* Traditional approval workflows assume a human is in the loop on each meaningful action. A human submits a request, an approver reviews it, the action happens. Even high-volume processes — say expense approvals — top out at maybe a few hundred actions per approver per day. The agent doesn't have that constraint. A single agentic session, as we said in Episode Three, makes seven to twenty tool calls. Times the active operator population. Times the concurrency. The action volume on the agent runtime is two or three orders of magnitude above what traditional approval workflows were designed for.

**REID:** And if you try to put a human approver in front of every tool call, you've broken the agent. You've turned an autonomous reasoning loop back into a wizard with prompts. The HITL gate we walked in Episode Three — that's the right answer for irreversible actions. It is not the right answer for every read.

**KEVEN:** Right. *Three — reasoning is cross-domain.* Traditional governance scopes data access by domain. Finance data is governed by the finance team. HR data is governed by the HR team. Operational data is governed by the operations team. Each domain has its own access model, its own steward, its own audit posture. The agent's per-scenario Gold views — by design, the way we built them in Episode Two — span multiple source-of-record origins from multiple domains. A demand-shaping scenario reads from sales, returns, marketing, supply chain. A workforce-planning scenario reads from HR, finance, operations. The agent's data access is *cross-domain by construction*. Which means the governance model has to compose across the domains the data came from. Not enforce each domain in isolation.

**REID:** And that composition is hard. Because the steward of the finance source doesn't naturally have visibility into how the data is used after it crosses into the Gold view. The agent reads from the Gold view. The finance steward sees nothing in his audit log. The lineage has to propagate back. The sensitivity label has to ride along. The access decision has to inherit from the most-restrictive source contribution. None of that is automatic on traditional governance stacks.

**KEVEN:** Dynamic access. High-velocity tool calls. Cross-domain reasoning. Three properties of the agent that traditional DLP, traditional RBAC, traditional approval workflows don't handle cleanly. And that is why the Acceleration Framework names Principle Two — *governance, audit, ledger* — as its own first-class principle. The governance posture has to be re-architected for the agentic shape of the workload. Not bolted onto the legacy posture.

**REID:** Principle Two is not *do governance better.* Principle Two is *do governance at the shape of the agent.*

**KEVEN:** Said exactly that way. Now — three clouds. Three productized stories. Let's start where Microsoft has the freshest differentiation, name it honestly, and walk to AWS and GCP from there.

### Microsoft Purview — productized: catalog + lineage + access + sensitivity + DSPM for AI in one product

**KEVEN:** Microsoft first. Because on this axis — governance for agentic AI — Microsoft has the densest productized story today, and the seller has to be able to claim it honestly while it's true.

**REID:** State the claim plainly. Don't soften it. Don't oversell it. State it.

**KEVEN:** Stated plainly. *Microsoft Purview is the only product on the market today that combines, in a single product, with a single billing line and a single console — data catalog, data lineage, access policy, sensitivity classification, and DSPM for AI.* Five capabilities that elsewhere are five products. In Purview, they are one product.

**REID:** Walk the five.

**KEVEN:** *Data catalog.* The metadata layer. Every data asset in the estate — tables, files, semantic models, reports, Power BI workspaces, Fabric items — registered, classified, discoverable. *Data lineage.* The propagation traceability. When a Gold view is composed from three Silver canonical models composed from seven Bronze landings — the lineage graph traces that, end to end. *Access policy.* The row, column, and scope discipline. Who can read what, expressed as policy that propagates into the data plane. *Sensitivity classification.* Labels — PII, PHI, financial, regulated-data, customer-confidential — applied to assets, propagating through the lineage. *DSPM for AI.* Data Security Posture Management, productized for AI workloads, generally available in 2025. The piece that knows the difference between a human BI query and an agentic tool call, and applies posture policy accordingly.

**REID:** And the one console claim.

**KEVEN:** One console. One identity model — Microsoft Entra. One billing line — part of the broader Microsoft 365 and Azure commercial surface. One audit substrate that all five capabilities emit into. The architectural density is real.

**REID:** Now let me push back, because this is where I have to push back if I'm doing my job. *Purview has been around for years.* The catalog piece dates back to Azure Purview pre-rebrand. The sensitivity-label piece dates back to Microsoft Information Protection before that. Lineage has been incrementally maturing for years. None of those are the differentiation we're talking about tonight. *The DSPM for AI piece is the differentiation.* That's the productized capability that hit GA in 2025 and that AWS and GCP do not have a like-for-like productized equivalent for today. The seller who pitches Purview-the-catalog as the Microsoft differentiation is pitching a five-year-old story. The seller who pitches Purview-DSPM-for-AI as the Microsoft differentiation is pitching the freshest single productized advantage Microsoft has on the agentic control plane today.

**KEVEN:** Conceded. The freshness is in the AI-aware layer specifically. The rest of Purview is mature and assembled cleanly. The DSPM-for-AI piece is the freshly productized capability that creates the current differentiation window. And that's the piece the seller has to be able to walk in detail.

**REID:** Walk it.

### DSPM for AI — the new productized capability

**KEVEN:** Walking DSPM for AI specifically. Four properties that make it different from traditional DSPM.

**REID:** Go.

**KEVEN:** *One — posture-aware to AI workload data access patterns.* DSPM for AI knows the difference between a human running a BI query and an agent runtime making a tool call against a Fabric SQL endpoint. The traffic shape is different. The risk surface is different. The posture rules apply differently. Traditional DSPM treated all reads as comparable. DSPM for AI treats agent reads as a distinct class with their own posture model. The operational consequence — an agent can read in seconds what a human reads in days. Same policy across both either over-restricts the agent or under-restricts the human. DSPM for AI lets you set policy that's aware of which class of consumer is reading and respond accordingly.

**REID:** Two.

**KEVEN:** *Two — model-version-aware.* DSPM for AI tracks which specific model version accessed which data class. When you upgrade — GPT-4 to GPT-4o, or Claude 3.5 to Claude 4 — the posture telemetry knows the upgrade happened, knows which workloads now run on the new version, and tracks whether the new version is accessing the same data classes as before, more, or fewer. In a regulated industry every model-version change is a model-risk-management event. Banks, insurers, pharma — their MRM committees need evidence that the new version has been assessed against the data it now touches. DSPM for AI is the productized substrate for that evidence.

**REID:** Three and four.

**KEVEN:** *Three — consent-aware.* DSPM for AI knows which data classes have AI-consent labels applied. The data the owner has affirmatively labelled as eligible for AI workload consumption is treated differently from data with no consent label or a human-eyes-only label. The agent's tool call is checked against the consent state at runtime, not just against the role permission of the service principal. Two layers of governance — static role permission plus dynamic consent posture. Both apply. *Four — surfaces prompt-injection signal in agent telemetry.* Started shipping more aggressively through 2025. The telemetry includes signals that look like prompt-injection attempts — instructions buried in retrieved documents that try to redirect the agent, tool calls that look anomalous against the reasoning trace, output patterns that suggest the agent has been redirected. Not a complete prevention layer. A posture-management telemetry stream that surfaces likely incidents for the security team to investigate.

**REID:** And the honest seller posture on the maturity.

**KEVEN:** *Purview DSPM for AI hit general availability in 2025.* The capabilities I just walked are productized today. It is the strongest single productized differentiation Microsoft has on the agentic control plane in this current window.

**REID:** And the honest gap.

**KEVEN:** And the honest gap is — the differentiation window is approximately twelve months. AWS and GCP have credible roadmap commitments to productize AI-aware DSPM equivalents. The capability gap will narrow. The seller's posture is — claim it honestly while it's true, prepare for the gap to narrow, and ensure the architectural decisions the client makes today don't depend on the gap remaining permanent. The Purview-versus-assembled comparison is real today. In twenty-six or twenty-seven, the comparison will be Purview versus more-productized-AWS-and-GCP-equivalents, and the differentiation will be on density and integration density rather than productized-versus-assembled.

**REID:** Twelve-month window. Claim while true. Prepare for narrowing. That's the seller's honest posture.

**KEVEN:** Said exactly that way.

### AWS — Lake Formation + Macie + Audit Manager + GuardDuty (multi-service assembly)

**REID:** Let me take AWS. Because I've built this. The assembled-AWS version of what Purview productizes — I've shipped it in production for a client whose data foundation was AWS-resident at scale, where the integration was worth the engineering.

**KEVEN:** Walk what you assembled.

**REID:** Six services. Six consoles. Six billing lines. The seller has to know all six because the client's architects know them. *AWS Lake Formation.* The fine-grained access surface. Row-level, column-level, cell-level access policies, expressed declaratively, propagated into the query plane — Athena, Redshift Spectrum, EMR. Lake Formation is the AWS analog of the Purview access-policy capability for data-lake assets. Mature. Well-engineered. *Amazon Macie.* The sensitive-data discovery and classification service. Scans S3 buckets for sensitive content, applies classifications, integrates with downstream policy. The AWS analog of the Purview sensitivity-classification capability.

**KEVEN:** Three.

**REID:** *AWS Audit Manager.* The compliance-evidence collection service. Continuously collects evidence against a defined control framework — SOC 2, HIPAA, PCI, the major ones — and produces audit-ready reports. The AWS analog of the audit-substrate emission Purview produces, with the framework-mapping layer on top. *Amazon GuardDuty.* The threat-detection service. Continuously analyses CloudTrail, VPC Flow Logs, DNS logs for anomalous patterns that suggest compromise. The behavioural-detection layer.

**KEVEN:** Five and six.

**REID:** *AWS CloudTrail.* The API audit logging substrate. Every AWS API call, captured. The raw audit row. *AWS Config.* The resource compliance service. Tracks resource configuration state, flags drift from policy, alerts on non-compliant resources. The configuration-management governance layer. Six services. The capabilities can be assembled to match Purview's scope. Lake Formation plus Macie plus Audit Manager plus GuardDuty plus CloudTrail plus AWS Config — when you wire them together correctly — give you a comparable governance posture for an AWS-resident agentic workload.

**KEVEN:** And the assembly cost.

**REID:** The assembly is real engineering. In a Wave One engagement at a client of meaningful scale, integrating those six services into a coherent governance posture is typically three to six months of work for a competent platform team. That's not a knock on AWS. The capabilities are there. The capabilities are mature. The seller's argument is not that AWS can't do it. The seller's argument is that the productized integration on Microsoft compresses three-to-six months of integration work into a configuration exercise. That compression is real economic value for the client. It's also not infinite — once a team has done the AWS integration once, the second engagement is faster.

**KEVEN:** And the AI-aware DSPM gap on AWS.

**REID:** Today, AWS does not have a productized AI-aware DSPM layer comparable to Purview DSPM for AI. The classification, threat-detection, and audit pieces are mature for general workloads. The agent-specific posture-management story — model-version-aware tracking, consent-label awareness, prompt-injection signal — is the productized gap on AWS today. AWS has roadmap commitments. The twelve-month window applies. Today, the gap is real.

**KEVEN:** And the honest cross-cloud posture.

**REID:** Honest cross-cloud posture. If a client is AWS-resident at scale, with petabytes of data of record in S3, with mature Lake Formation and Macie deployments already operating — the integration is worth the engineering. The assembled-AWS governance posture is solid. The agentic-AI-aware piece is the freshest gap; for a Wave One workload, that gap is bridgeable with policy and process while the productization closes in. If a client could go either way — has data on both clouds, hasn't committed yet — the productized integration on Microsoft is the seller's commercial leverage. Both can be the right answer. The constraint determines which.

### GCP — Dataplex + Sensitive Data Protection + Security Command Center (closer to Purview)

**REID:** GCP. The shape is different from AWS — more productized, fewer parts.

**KEVEN:** Walk it.

**REID:** *Google Cloud Dataplex.* The unified data governance surface. Catalog, lineage, access management, data quality, lifecycle policy — all in Dataplex. Of the three clouds, Dataplex is structurally the closest to Purview in scope. A single Google Cloud product that covers the catalog plus lineage plus access plus quality piece. *Sensitive Data Protection* — the rebrand of what used to be Cloud DLP. The sensitive-data classification service. Scans data assets, applies classifications, supports redaction and de-identification workflows. Separate product from Dataplex but integrates cleanly. The GCP analog of Macie on AWS or the sensitivity layer of Purview. *Security Command Center.* The security posture management product. Threat detection, vulnerability management, asset inventory, compliance status. Across the broader GCP estate, including AI workloads.

**KEVEN:** And the productization comparison to Purview.

**REID:** Dataplex covers most of Purview's data-governance scope in a single product, which is structurally tighter than the six-service AWS assembly. Sensitive Data Protection is a separate but well-integrated product. Security Command Center covers the threat-detection and posture-management substrate. The integration work to compose them is meaningfully less than the AWS assembly. Closer to Purview-style productization. But the AI-aware DSPM piece — the agent-specific data security posture management layer — is the remaining gap on GCP today. Same as AWS. Same twelve-month productization timeline expected.

**KEVEN:** And model-card-level transparency.

**REID:** GCP also has Model Cards as a productized artifact pattern, which contributes to the broader AI-governance story without being a DSPM-for-AI replacement. Useful adjacent productization. Not the same axis.

**KEVEN:** Honest comparison summary.

**REID:** Honest comparison. *Purview is the only product today with productized DSPM for AI bundled into the broader data-governance surface.* AWS assembles equivalent base capabilities from six services and lacks the AI-aware DSPM productized layer. GCP composes most of the data-governance surface in Dataplex plus Sensitive Data Protection plus Security Command Center, and also lacks the AI-aware DSPM productized layer. Three different architectural shapes. One productized differentiation window. Twelve months, approximately.

**KEVEN:** Twelve months. Claim while true. Prepare for the narrowing.

### Identity Continuity — Principle 3 in detail

**KEVEN:** Now the second thread. Identity. Because governance assumes you know whose action you're governing — and the agentic stack has *four* identities that have to connect, and most enterprises walk into this with one or two of them properly modelled and the other two improvised.

**REID:** Walk the four.

**KEVEN:** Four identities. *Agent identity.* The principal the agent runtime authenticates as when it makes tool calls. On Microsoft, that's an Entra service principal. On AWS, that's an IAM role. On GCP, that's a service account. *Operator identity.* The human who's interacting with the agent — the end user, the analyst, the operator of the agentic workflow. On Microsoft, an Entra user. On AWS, an IAM user or, more typically at enterprise scale, a workforce identity through IAM Identity Center. On GCP, a Cloud Identity user. *Source identity.* The identity used when the agent reaches into an underlying system of record — federated identity into SAP, Salesforce, Workday, Snowflake, the source-system identity space. *Auditor identity.* A separate principal — read-only, scoped to audit-row access only — that the security and compliance team uses to inspect the trail.

**REID:** And the discipline.

**KEVEN:** The discipline is — *all four must connect.* Identity propagation has to flow through every tool call. The agent identity is the principal that authenticates. The operator identity is the on-behalf-of context that the agent inherits. The source identity is the federated identity that propagates into the source-system call. The auditor identity is the principal that reads the audit row afterward and can trace it back through all three. End-to-end traceability. Every tool call. Every reasoning step. Every audit row.

**REID:** That's the discipline. The productized story varies by cloud. Walk Microsoft.

**KEVEN:** *Microsoft Entra ID is the single plane.* All four identities in one identity surface. Entra service principal for the agent. Entra user for the operator. Entra federation into the source systems — and this is the part that matters for enterprise SaaS — *Entra has the broadest enterprise SaaS federation depth in the productized identity market.* Native federation into Microsoft 365 — that's table stakes. But also SAP, Salesforce, Workday, ServiceNow, Adobe, Atlassian, GitHub, and dozens more. Pre-integrated. Pre-tested. Plus the auditor principal scoped through Entra access reviews and conditional access. Single identity plane. Productized for enterprise scale.

**REID:** And the differentiation claim.

**KEVEN:** The differentiation claim — narrowly stated — is *enterprise SaaS federation depth.* For a typical large enterprise where the data of record lives in a constellation of SaaS systems (Microsoft 365 for productivity, SAP for ERP, Salesforce for CRM, Workday for HR, ServiceNow for IT), Entra is the productized identity surface with the broadest pre-integrated federation across that constellation. The seller can claim that honestly.

**REID:** Now AWS.

**KEVEN:** AWS has three identity primitives that don't unify the way Entra does. *AWS IAM* is mature for AWS-resource identity — service roles, instance profiles, federated principals. Best in class for governing access to AWS resources themselves. *AWS IAM Identity Center* — formerly AWS SSO — handles workforce identity, including federation from external identity providers like Entra or Okta. *Amazon Cognito* handles customer identity for consumer-facing applications. Three products. Each does its thing well. They don't compose into a single identity plane the way Entra does. The architecturally interesting consequence — for an AWS-resident agentic workload at an enterprise where the workforce identity is upstream from Entra or Okta, you typically end up federating *through* AWS Identity Center *from* Entra, which is operationally fine but means the productized identity story is *Entra plus AWS Identity Center*, not AWS Identity Center standalone.

**REID:** And the AWS strength.

**KEVEN:** The AWS strength is AWS IAM for AWS-resource governance. Mature. Granular. Powerful. For the agent's *resource-access* governance specifically — the IAM role the agent runs as, the policies attached to it, the resource-level permissions — IAM is best in class on AWS. The piece that doesn't unify is the workforce-and-customer-and-resource cross-context unification.

**REID:** Now GCP.

**KEVEN:** GCP has Cloud IAM and Workload Identity Federation. *Cloud IAM* is the GCP-resource access governance — similar shape to AWS IAM, similar maturity. Then *Workload Identity Federation* — and this is the part where I have to concede cleanly to Reid before he has to push, because Reid's going to push.

**REID:** I'm going to push. Concede.

**KEVEN:** Conceded. *Workload Identity Federation on GCP is the strongest cross-cloud agent-identity federation primitive in the productized market today.* A workload running on GCP — a Vertex AI agent, a Cloud Run service, a GKE workload — can assume a federated identity into AWS or into Azure, without static credentials. Short-lived federated tokens. No long-lived secrets. The federation is set up once; the runtime exchange happens at every call. Cross-cloud agent identity is genuinely well-engineered on GCP.

**REID:** And I want to push on this one because it's the place I have personal production hours and I can defend it cleanly. *If a client's reality is cross-cloud — meaningfully cross-cloud, not "primary Azure and one workload on AWS" but actually distributed agent workloads across two or three clouds — Workload Identity Federation on GCP gives you the cleanest agent-identity bridge across clouds.* I've shipped this. The workload runs on GCP, calls into AWS via federated identity, reads from an S3 source, returns a result. No static credentials anywhere. The audit row on both sides shows the federated principal. The seller who pitches Entra as universally the right cross-cloud identity answer is missing the axis Workload Identity Federation wins on.

**KEVEN:** And I'm not going to push back on that. I'm going to converge. *Reid is right on that axis.* Cross-cloud workload identity federation is the axis Workload Identity Federation wins. For enterprise SaaS workforce-and-source federation — Microsoft 365 plus SAP plus Salesforce plus Workday plus ServiceNow with native pre-integrated federation depth — Entra is the dominant productized identity surface. Two different axes. Both honestly differentiated. The seller's discipline is to be precise about *which axis the client's reality requires.*

**REID:** And most enterprise reality is mixed. Some workloads cross clouds; most workloads federate to SaaS. Both axes show up in the same engagement. The productized answer is — Entra is the enterprise identity plane for the workforce-and-SaaS axis, Workload Identity Federation is the productized cross-cloud bridge for the workload-identity axis. They compose. They're not mutually exclusive.

**KEVEN:** They compose. The seller's discipline is naming both axes and being honest about which one is differentiating in the specific client conversation.

### Safety, Red-Teaming, and AI Risk Frameworks

**KEVEN:** Now the third thread. Safety. The piece that ties governance and identity to the regulated reality the CISO actually operates in.

**REID:** Walk the standards landscape first. The seller who can't name these is going to lose the conversation with the regulated-industry CISO and the Chief AI Officer.

**KEVEN:** Four pieces of vocabulary every seller has to use fluently. *EU AI Act.* In force August 2024. Major obligations phasing in through 2025 to 2027. Risk-tiered — unacceptable-risk prohibitions, high-risk obligations on certain categories, limited-risk transparency obligations, minimal-risk mostly unregulated. Applies to AI systems placed on the EU market regardless of where the provider is based. The seller has to know which tier the client's workload falls into and what obligations attach. *NIST AI Risk Management Framework — NIST AI RMF.* Published 2023, in active enterprise adoption. Four core functions — Govern, Map, Measure, Manage. Voluntary framework, but increasingly cited in US regulatory expectations and federal procurement. The major insurers and banks have built their internal AI-risk programs around it. When the client's risk team speaks, they tend to speak NIST AI RMF. *ISO/IEC 42001.* The AI management systems standard. International, published 2023. Certifiable — third-party auditable, similar to ISO 27001. For a multinational client operating across regulatory regimes, the increasingly common common-denominator certification. Large enterprises are starting to require ISO 42001 certification from AI-system suppliers in procurement. *OWASP Top 10 for LLM Applications.* The application-security frame. Specific threat categories — prompt injection direct and indirect, insecure output handling, training data poisoning, denial of service, supply-chain vulnerabilities, sensitive information disclosure, insecure plugin design, excessive agency, overreliance, model theft. The penetration-test team in the cold open works from this checklist.

**REID:** And the threat surfaces for the agent specifically.

**KEVEN:** Four to name. *Prompt injection — direct and indirect.* Direct, the operator types a malicious instruction. Indirect, the agent retrieves a document that contains an embedded instruction that redirects its behaviour. The indirect form scales scariest because it can be planted into legitimate sources by anyone who can write to a source the agent's RAG layer might reach. *Data exfiltration via agent tool calls.* The agent is a privileged user by design — read access to the Gold tier composed from multiple sources. If it's compromised, the blast radius is the entire data foundation it can compose from. *Model misuse and jailbreaks.* Adversaries attempting to bypass the agent's safety training to produce harmful output. *Hallucination harm.* The agent confidently producing wrong information the operator relies on — not malicious, emergent from probabilistic generation. The harm shows up downstream in a regulatory filing, a customer communication, a clinical recommendation.

**REID:** And the productized guardrails on each cloud.

**KEVEN:** Three clouds, three productized stories. Reasonably comparable maturity on this axis, narrow differentiation. *Azure AI Content Safety plus Microsoft Defender for Cloud AI.* Content Safety is the content-filtering surface — text and image safety, jailbreak-attempt detection, protected-material detection, groundedness checking. Defender for Cloud AI is the security-posture-management layer for AI workloads, integrated with the broader Defender estate. Combined with the DSPM-for-AI signal we already walked, the Microsoft posture is content-filter plus posture-management plus AI-aware DSPM in the same productized integration. *AWS Bedrock Guardrails.* Content filters, denied-topic enforcement, sensitive-information redaction. Configurable per agent — the strongest per-agent customization story of the three, applied at the model-invocation boundary. *Vertex AI Safety filters plus the broader Responsible AI suite.* Safety filters at the model-serving layer with configurable thresholds. Plus Model Cards, evaluations, bias detection, Explainable AI. The most opinionated of the three by default — Google's filters lean conservative out of the box.

**REID:** Honest comparison. All three clouds have productized content safety. Bedrock Guardrails has the strongest per-agent configurability. Microsoft has the broadest posture-management integration through Defender for Cloud AI plus DSPM for AI. GCP is the most opinionated by default. Sellers should not pretend a major productized gap exists on basic content safety. The differentiation is in adjacent layers — DSPM for AI on Microsoft, agent-specific configurability on AWS, the broader Responsible AI suite on GCP.

**KEVEN:** Pick on adjacent strengths, not on the safety layer itself.

### A reading I want to do

**KEVEN:** I want to read briefly — paraphrased — from the register Microsoft Learn, NIST AI RMF publications, and the EU AI Act overview literature have been using through 2025 on what agentic AI specifically requires of the governance posture.

**REID:** Go.

**KEVEN:** [reading, paraphrased — composite of the Microsoft Learn Purview DSPM for AI guidance, the NIST AI RMF Govern function, and the EU AI Act high-risk obligations register]

*"Agentic AI systems require a governance posture qualitatively different from the posture suitable for traditional machine learning workloads or for general data estates. The reasoning loop's runtime data access decisions, the high-velocity tool invocation pattern, and the cross-domain composition of agent context together break the assumptions on which traditional access review, traditional data loss prevention, and traditional approval workflows were built. The substrate that responds — the audit-row-per-step pattern, the AI-aware data security posture management dimension, the identity continuity across operator, agent, source, and auditor — is itself an architectural commitment, not an operational refinement. Organisations that treat agentic governance as an extension of traditional governance discover the gap when a third-party assessment surfaces an access pattern that no existing control flagged. Organisations that treat agentic governance as its own architectural layer prevent the same finding by construction."*

[pause]

**REID:** *Agentic governance as its own architectural layer, not an extension of traditional governance.* That sentence is exactly the discipline. And the regulatory landscape is moving fast enough that the seller who can't speak fluently about EU AI Act, NIST AI RMF, and ISO 42001 is going to lose conversations with regulated-industry CISOs and Chief AI Officers in 2026. This is table-stakes vocabulary. Not aspirational. Table-stakes.

**KEVEN:** Table-stakes vocabulary.

**REID:** And the productized substrate — Purview DSPM for AI on Microsoft, the assembled-AWS equivalent, the Dataplex-plus-adjacent on GCP — that's what the framework names. Principle Two is governance, audit, ledger. The reading just gave the *why* of why Principle Two had to be named separately from the data foundation and the runtime.

**KEVEN:** Said cleanly.

### One disagreement

**REID:** Pushback. The structural one. Because this episode has two axes that are honestly contested and the seller has to know which axis they're losing on.

**KEVEN:** Go.

**REID:** *Workload Identity Federation on GCP makes cross-cloud agent identity portable in a way Entra cannot match today.* I want to defend that cleanly. Short-lived federated tokens, no static credentials, audit row on both sides reflecting the federated principal. I've shipped this in production. For genuinely multi-cloud clients — meaning workloads that meaningfully traverse two or three clouds — GCP has the better cross-cloud agent identity story. Not Entra. Not AWS IAM Identity Center. GCP Workload Identity Federation. The Microsoft seller has to be able to say that without flinching.

**KEVEN:** Conceded cleanly. *On the cross-cloud workload identity axis specifically, Workload Identity Federation is the productized answer.* I'm not going to fight that. Entra Workload Identity has improved through 2025 and federation patterns exist on Microsoft for some cross-cloud cases, but the like-for-like productization is on GCP.

**REID:** And the pivot.

**KEVEN:** Here's the pivot — and it's a legitimate pivot, not a deflection. *Most enterprise identity reality is not "genuinely multi-cloud."* Most enterprise identity reality is *one primary cloud plus a federated SaaS workforce.* The primary cloud holds the workload identities. The workforce identities live in Entra, are federated into Microsoft 365 natively, into SAP and Salesforce and Workday and ServiceNow via Entra's pre-integrated federation, and into the primary cloud through Entra-to-cloud federation patterns. For that reality — which is the majority enterprise reality I see — Entra's enterprise SaaS federation depth is the dominant productized identity surface.

**REID:** So you're not contesting the cross-cloud point.

**KEVEN:** I'm not contesting the cross-cloud point. I'm naming the axis it sits on. The cross-cloud workload identity axis is one axis. The enterprise-SaaS-workforce federation axis is a different axis. Both are real. Both have productized differentiation. They differentiate on different things. The seller's discipline is to know which axis the client's reality is on.

**REID:** And the convergence.

**KEVEN:** Convergence. *Both Entra and Workload Identity Federation are honestly differentiated, on different axes.* Workload Identity Federation wins on cross-cloud workload identity. Entra wins on enterprise SaaS workforce federation depth. For a client whose reality is primary-cloud-plus-federated-SaaS, Entra is the dominant productized identity surface. For a client whose reality is genuinely-multi-cloud-workloads, Workload Identity Federation is the cleanest cross-cloud agent identity bridge. Sellers should be precise about which axis the client's reality requires. Not pick the universal answer that doesn't exist.

**REID:** Convergence. Named cleanly.

**KEVEN:** Named cleanly.

### What to carry forward

**KEVEN:** Three things.

**REID:** Go.

**KEVEN:** *One — governing an agent is different from governing a human or a traditional ML pipeline. Three properties break the traditional posture. Data access is dynamic, decided at reasoning time. Tool calls are high-velocity, two orders of magnitude above traditional approval-workflow scale. Reasoning is cross-domain by construction, composing Gold views from multiple source-system origins. The Acceleration Framework's Principle Two — governance, audit, ledger — is the architectural response. Not better governance. Governance at the shape of the agent.*

*Two — Microsoft Purview is the only product today that combines, in a single product with a single billing line and a single console, data catalog, lineage, access policy, sensitivity classification, and DSPM for AI. The DSPM for AI piece — productized in 2025 — is the freshest single productized differentiation Microsoft has on the agentic control plane today. AWS requires four-to-six services — Lake Formation plus Macie plus Audit Manager plus GuardDuty plus CloudTrail plus AWS Config — to assemble the equivalent base capability, with the AI-aware DSPM piece as the freshest gap. GCP Dataplex plus Sensitive Data Protection plus Security Command Center covers most of the data-governance scope in a tighter productization, with the same AI-aware DSPM gap. The differentiation window is approximately twelve months. Claim it honestly while true. Prepare for the narrowing.*

*Three — identity continuity is its own first-class principle, and it has two axes that are honestly differentiated on different clouds. Microsoft Entra has the broadest productized enterprise SaaS federation depth — Microsoft 365, SAP, Salesforce, Workday, ServiceNow and dozens more, pre-integrated. Workload Identity Federation on GCP is the cleanest productized cross-cloud workload-identity bridge. Both are real. Both are differentiated. Sellers should be precise about which axis the client's reality requires. And on safety — content filtering and posture management are reasonably comparable across the three productized stories. EU AI Act, NIST AI RMF, and ISO 42001 are table-stakes vocabulary for any regulated-industry conversation in 2026.*

**REID:** And the seller's posture from the disagreement — name the axis. Cross-cloud workload identity is Workload Identity Federation's axis. Enterprise SaaS workforce federation is Entra's axis. AI-aware data security posture management is Purview's axis, on a twelve-month window. Be precise. The architectural honesty is the commercial leverage.

**KEVEN:** Architectural honesty as commercial leverage. The discipline.

**REID:** Next episode — *Audit, Ledger, and Replay: The Trust Substrate.* The audit-row-per-step pattern walked in detail. The hash-chained ledger discipline. Replay-token validation. Human-in-the-loop gates as audit events. The ledger productized on Microsoft via Purview audit echo and Foundry runtime emission, assembled on AWS via CloudTrail plus Audit Manager plus custom ledger composition, assembled on GCP via Dataplex plus Security Command Center plus custom ledger composition. The substrate that lets the CISO from the cold open answer her own question.

**KEVEN:** See you there.

[outro]

---

## Further reading

### Standards and frameworks
- **EU AI Act** — [eur-lex.europa.eu](https://eur-lex.europa.eu/) — in force August 2024; major obligations phasing 2025-2027
- **NIST AI Risk Management Framework (NIST AI RMF)** — [nist.gov](https://www.nist.gov/itl/ai-risk-management-framework) — Govern, Map, Measure, Manage
- **ISO/IEC 42001** — AI management systems standard; certifiable
- **OWASP Top 10 for LLM Applications** — [owasp.org](https://owasp.org/) — application-security threat categories

### Microsoft Learn
- **Microsoft Purview** — unified data governance overview
- **Microsoft Purview DSPM for AI** — data security posture management for AI workloads; generally available 2025
- **Microsoft Purview Data Catalog** — metadata and discovery
- **Microsoft Purview Data Lineage** — propagation traceability
- **Microsoft Purview Information Protection** — sensitivity labels and classification
- **Microsoft Entra ID** — identity platform; enterprise SaaS federation depth
- **Microsoft Entra Conditional Access** — access policy
- **Microsoft Entra access reviews** — auditor and reviewer principal scoping
- **Azure AI Content Safety** — content filtering, jailbreak detection, groundedness checking
- **Microsoft Defender for Cloud AI** — security posture management for AI workloads

### AWS documentation
- **AWS Lake Formation** — fine-grained access for data lake assets
- **Amazon Macie** — sensitive-data discovery and classification
- **AWS Audit Manager** — compliance-evidence collection
- **Amazon GuardDuty** — threat detection
- **AWS CloudTrail** — API audit logging substrate
- **AWS Config** — resource configuration compliance
- **AWS IAM** — resource-access identity
- **AWS IAM Identity Center** — workforce identity and external IdP federation
- **Amazon Cognito** — customer identity
- **AWS Bedrock Guardrails** — content filters, denied topics, sensitive-info redaction

### Google Cloud documentation
- **Google Cloud Dataplex** — unified data governance; catalog, lineage, access, quality, lifecycle
- **Sensitive Data Protection** (formerly Cloud DLP) — sensitive-data classification and redaction
- **Security Command Center** — security posture management
- **Google Cloud IAM** — GCP-resource identity and access
- **Workload Identity Federation** — cross-cloud short-lived federated tokens
- **Vertex AI Safety filters** — model-serving content safety
- **Vertex AI Responsible AI suite** — Model Cards, evaluations, bias detection, Explainable AI

### Industry research
- **Gartner** — AI governance, AI TRiSM, and trust market analyses
- **Forrester** — AI risk management research
- **IDC** — AI safety and compliance forecasts

### From the Acceleration Framework
- **Episode 1** — Five Principles overview, including Principle 2 (governance, audit, ledger) and Principle 3 (identity continuity)
- **Episode 2** — Data Foundation and the No-Replication Principle (the substrate the governance posture sits on)
- **Episode 3** — Agent Runtime — Talking to Gold, Not SORs (the MCP boundary the governance posture surrounds)
- **Episode 5** (next) — Audit, Ledger, Replay: The Trust Substrate

---

**End of Episode 04 · Governance, Identity, and Safety for Agentic AI**
*≈ 6,200 words · target 32 minutes at conversational pace*
