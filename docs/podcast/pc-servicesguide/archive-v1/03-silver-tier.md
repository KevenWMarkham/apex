# Episode 03 · Silver Tier — Where Canonical Lives

**Source:** *Professional APEX-M Services Guide* — Part III (Chapters 8, 9, 10, 11, 12)
**Run time:** ≈ 30 minutes target
**Last updated:** 2026-05-12

---

## Cold Open

[Sound: rapid typing, then it stops]

**KEVEN:** Two months into a recent engagement, the engagement lead came to me and said, *"Keven, we have a problem. The agent is correct nine times out of ten. But the tenth answer — and we can't predict which tenth — is completely wrong. And we cannot ship to production with one-in-ten wrong."*

[pause]

**MORGAN:** And the problem turned out to be —

**KEVEN:** The problem turned out to be that the Silver canonical for "customer" had been built by *two different team members* in *two different sprints*, using *two different reconciliation rules.* One reconciled on email-as-primary. The other reconciled on customer-ID-as-primary. So when the same physical customer appeared with a slightly different email, sometimes they were one customer in Silver and sometimes they were two. And the agent's answer depended on which path the data took through Silver that day.

**MORGAN:** That is the Silver story.

**KEVEN:** That is the Silver story. The Silver tier is the place where, if you do it right, every downstream Service inherits stable meaning. If you do it wrong, every downstream Service inherits the same instability. There is no third option. Today's episode is the architecture of that.

**MORGAN:** I'm Morgan.

**KEVEN:** I'm Keven Markham. APEX Services Podcast, Episode Three. *Silver Tier — Where Canonical Lives.*

---

## Theme Statement

**MORGAN:** Part Three. Five chapters. Walk me through them.

**KEVEN:** Chapter Eight — *From Raw to Silver — the conformance layer.* Chapter Nine — *Schema Library deep dive.* This one is enormous — fourteen schema families across seven Practices. Chapter Ten — *Industry Schemas deep dive — how the fourteen families are used.* Chapter Eleven — *Quality, Lineage, Microsoft Purview.* Chapter Twelve — *Microsoft Entra ID and Purview — security and governance deep dive.*

**MORGAN:** And the through-line.

**KEVEN:** The through-line — *Silver is the anchor of stable meaning across the entire APEX framework.* Get Silver right, every Service is easy. Get Silver wrong, every Service inherits the wrongness.

---

## The Story

### From raw to Silver (Chapter 8)

**KEVEN:** Chapter Eight. *From Raw to Silver — the conformance layer.*

The conformance layer is where Bronze tokens are mapped into canonical entities. It's a transformation pipeline — typically a Fabric notebook or a Spark job, sometimes a dataflow Gen2 — that reads Bronze, applies the conformance rules, and writes to Silver.

**MORGAN:** Section eight point — the four conformance dimensions. Quickly.

**KEVEN:** Four.

**Schema conformance.** Bronze fields are mapped to canonical-schema fields. Names normalised. Types coerced. Nullability declared.

**Identity conformance.** Same-entity instances across sources are reconciled. This is the matching problem — the one that bit my engagement.

**Code-value conformance.** Lookups normalised. "MA" / "Massachusetts" / "Mass." → the canonical state code. "Walk-in" / "WI" / "In-person" → the canonical channel code.

**Temporal conformance.** Time zones normalised. Effective-dated fields properly bounded. Late-arriving facts handled.

**MORGAN:** And the engineering pattern.

**KEVEN:** Section eight point — *the conformance notebook pattern.* The pattern is — *one conformance pipeline per source-to-canonical entity mapping.* Not per source. Not per canonical. *Per mapping.* You'll have multiple Bronze tables feeding one Silver canonical. You'll have one Bronze table feeding multiple Silver canonicals. Each is a separate, versioned, governed pipeline.

**MORGAN:** Identity reconciliation. The problem from the cold open.

**KEVEN:** Section eight point — *identity-reconciliation discipline.* Three rules.

Rule one — *every canonical has exactly one primary-identity expression.* Customer is reconciled on customer-ID. Product is reconciled on SKU. VIN is reconciled on, well, VIN. The primary identity is declared in the canonical schema, not chosen at the source.

Rule two — *secondary-identity matches generate match scores, not collapses.* If a record matches the canonical on email but not customer-ID, it gets a match-score row. A separate process — typically a survivorship rule — decides whether to merge.

Rule three — *survivorship rules are explicit and versioned.* They live in code, in the Silver workspace, with PR review. They are not hand-tuned in a notebook by whoever happens to be in the sprint.

**MORGAN:** And the way to know you've got this right —

**KEVEN:** Section eight point — *the conformance audit.* Every Silver row carries its Bronze-source row ID and the conformance pipeline version. You can walk from any Silver record back to the Bronze inputs that built it, with the rule version that did the matching. Purview lineage makes this queryable.

### Schema library deep dive (Chapter 9)

**MORGAN:** Chapter Nine. *Schema Library deep dive.* Largest chapter in the Services Guide. Fourteen schema families.

**KEVEN:** Yes. Let me name them again — we hit them in Episode One, but the audience needs them on hand.

**RC family.** Order. Customer-and-Loyalty. Supply-and-Inventory.

**HLS family.** ClinicalEncounter. ClaimsAndUtilization. PharmaTrial.

**ER family.** UtilityNetwork. UpstreamEnergy. ChemicalsProcess.

**AXLE family.** BuildRecord. ConnectedVehicle. AssemblyAsset. QualityEvent.

**TH family.** TravellerProfile.

That's fourteen. Note ICE — Industrial Construction and Equipment — *re-uses* canonical schemas from RC for the consumer-aftermarket side and AXLE for the asset-and-service side. Section nine point — *cross-Practice canonical re-use.* ICE doesn't get its own family. It composes from the two existing ones.

**MORGAN:** Let me push. Each family — what's *in* it?

**KEVEN:** Take RC Order, for example. Section nine point — has the full layout. The Order family contains — *Order-Header, Order-Line, Order-Status-History, Order-Fulfillment, Order-Returns, Order-Payment, Order-Promotion-Applied.* Seven tables. Joined on order-ID. Each table has its own schema with declared primary key, declared foreign keys, declared sensitivity classifications, declared retention.

**MORGAN:** Naming. Section nine point — naming and layout conventions.

**KEVEN:** Practice prefix, family root, sub-entity suffix. Hyphen-separated. Lower-case for engineering, title-case for documentation. Example — `rc-order-header` is the engineering name; *RC Order Header* in docs.

**MORGAN:** And the deeper structure — how the fourteen relate to industry standards. The Sellers Guide section one point six A mentions this.

**KEVEN:** Yes. Each family declares its standards lineage in metadata. RC Order's standards lineage is GS1 plus Schema.org Commerce. HLS ClinicalEncounter's standards lineage is FHIR R4. AXLE BuildRecord's standards lineage is AIAG plus SAE J-standards. ER UtilityNetwork's standards lineage is CIM. The Silver schema is *not* the standard verbatim — but it composes with the standard. That's what makes Silver portable across clients in the same Practice.

### Industry schemas — how they're used (Chapter 10)

**MORGAN:** Chapter Ten. *Industry Schemas deep dive — how the fourteen families are used.* This is the chapter that connects schema to Service.

**KEVEN:** Right. Section ten point — *per-Service schema usage.* Every Service in the APEX catalog declares which canonical families it consumes. The declaration is in the Service manifest — a YAML file in the Service's repo.

**MORGAN:** Example.

**KEVEN:** RC-CX-01 — the loyalty churn prediction and winback Service. Its manifest declares — *consumes RC-Customer-and-Loyalty family. Consumes RC-Order family — specifically Order-Header, Order-Line, Order-Returns. Consumes RC-Channel-Interaction family.* Three families, ten tables. The Service's Gold mart pulls from those Silver canonical tables.

**MORGAN:** And the discipline?

**KEVEN:** The discipline is — *a Service never consumes Bronze directly, and a Service never invents its own canonical.* If your Service needs a field that isn't in the canonical, you don't add it to your Gold mart from Bronze. You file a *canonical-extension request* against the schema family. The extension goes through schema review. If approved, the field lands in Silver canonical. *Then* the Gold mart consumes it.

**MORGAN:** That's the friction point — section ten point — *canonical extensions.*

**KEVEN:** Yes. And the friction is on purpose. Without that gate, every Service customises Silver. Silver decays. Multi-Service composition breaks. The gate keeps Silver canonical.

**MORGAN:** Section ten point — *cross-family compositions.* The places where Services span families.

**KEVEN:** Several. AXLE Warranty Traceability — the Zero Day Warranty scenario — composes four AXLE families. RC Loyalty Churn composes the Customer-and-Loyalty family with the Order family. HLS Prior Authorisation composes ClinicalEncounter with ClaimsAndUtilization. The compositions are *first-class declarations*, not ad-hoc joins.

### Quality, lineage, Purview (Chapter 11)

**MORGAN:** Chapter Eleven. *Quality, Lineage, Microsoft Purview.* This is the chapter that connects Silver to governance.

**KEVEN:** Right. Three dimensions.

**Section eleven point — quality framework.** Every Silver canonical has declared quality rules. Completeness, validity, uniqueness, consistency, timeliness. The rules run as part of the conformance pipeline. Failures land in a *quality-incident* table — also in Silver — that Purview surfaces in DSPM-for-AI dashboards.

**Section eleven point — lineage in Purview.** Native. Fabric automatically registers every notebook, pipeline, lakehouse table, and semantic-model artefact with Purview. The lineage diagram shows source-to-Silver-to-Gold-to-agent flows for any selected dataset. This is the diagram the auditor wants.

**Section eleven point — DLP and labels.** Sensitivity labels applied at Bronze propagate through Silver to Gold to agent output. A Silver canonical that consumes PII-labelled Bronze inherits the label automatically.

**MORGAN:** And the engineering implication?

**KEVEN:** Two things. One — *quality rules are part of the canonical definition, not separate.* When you define a canonical, you define its quality contract. Two — *the lineage you get is the lineage Fabric and Purview produce.* You don't build it. You don't maintain it. The platform does. Don't reinvent.

### Entra ID and Purview governance (Chapter 12)

**MORGAN:** Chapter Twelve. *Microsoft Entra ID and Purview — Security and Governance deep dive.* The chapter that operationalises governance.

**KEVEN:** Yes. And let me just hit the practitioner takeaways — this chapter is long and dense.

**Section twelve point — the identity model.** Three classes of identities in APEX. *User identities* — bound to Entra ID users. *Service identities* — managed identities for pipelines and tools. *Privileged identities* — pii-unlock, schema-admin, audit-reader. Each has its own access patterns.

**Section twelve point — user-identity-mode security in OneLake.** Already covered in Episode One. Worth emphasising — this is where row-level security per invoking user actually gets enforced.

**Section twelve point — Purview policy templates for APEX.** APEX ships *policy templates* — pre-built Purview rule sets — for each Practice. The templates cover sensitivity-label catalogues, DLP rules, audit-retention policies, the pii-unlock policy structure. Deploying APEX includes deploying these templates.

**Section twelve point — auditor access pattern.** The client's auditor — internal or external — gets a *read-only* Entra identity bound to Purview's audit-reader role. They query Purview directly with their own credentials. APEX doesn't construct a special interface for the auditor. *Purview is the audit interface.*

**MORGAN:** And the failure mode if you skip this chapter.

**KEVEN:** Sprint twelve you realise you've been emitting audit events to a custom log store. The CCO asks why the auditor can't read them. You say *"we'll build an export."* Six months later you ship. Don't. Use Purview's audit-reader role on day one. The templates exist. Deploy them.

### Pulling Part III together

**MORGAN:** Synthesis. The architectural beats of Silver.

**KEVEN:** Five beats.

One — *Silver is the anchor of stable meaning.* If you can't enforce that, you can't ship a multi-Service engagement.

Two — *the conformance layer has four dimensions* — schema, identity, code-value, temporal. Each is a discipline.

Three — *fourteen canonical schema families.* Practice-aligned. Standards-rooted. Pre-built.

Four — *canonical extensions are a governed gate.* Don't bypass. Silver decay is the enemy.

Five — *Purview is the audit interface.* Use the templates. Give the auditor a read-role. Done.

---

## APEX Facts

**MORGAN:** APEX Facts. Eight rapid.

**KEVEN:** Fact One — four dimensions of conformance?

**MORGAN:** Schema, identity, code-value, temporal.

**KEVEN:** Fact Two — number of canonical schema families?

**MORGAN:** Fourteen.

**KEVEN:** Fact Three — Practice that re-uses other Practices' canonicals?

**MORGAN:** ICE — Industrial Construction Equipment. Re-uses RC and AXLE.

**KEVEN:** Fact Four — primary-identity discipline?

**MORGAN:** One primary-identity expression per canonical. Declared, not chosen at source.

**KEVEN:** Fact Five — how Services declare canonical usage?

**MORGAN:** In the Service manifest. YAML in the Service's repo.

**KEVEN:** Fact Six — what's a canonical-extension request?

**MORGAN:** The governed gate by which a Service adds a field to Silver canonical. Goes through schema review.

**KEVEN:** Fact Seven — how does the auditor access APEX audit data?

**MORGAN:** Through Purview's audit-reader role, with their own Entra credentials. No special interface.

**KEVEN:** Fact Eight — three identity classes?

**MORGAN:** User identities, service identities, privileged identities.

**KEVEN:** Time.

---

## Adopt / Hold

**MORGAN:** Adopt versus Hold on Silver patterns. Keven, Adopt.

**KEVEN:** Adopt — *the canonical-extension gate as the discipline of Silver.* No exceptions. Every Service that needs a new field files an extension request. The schema review approves or rejects. The canonical evolves slowly and intentionally. The Silver decay problem is the single biggest threat to a multi-Service engagement; this gate is the answer.

**MORGAN:** Hold. When does the extension gate become engineering friction that hurts the engagement?

Two cases.

Case one — *very early in an engagement, when you're still discovering the canonical shape.* For the first three or four sprints, the gate is lighter — the schema is moving, the team is converging. After sprint five or so, the gate gets sticky.

Case two — *for Service-specific computed fields that aren't actually canonical.* If your Service needs a derived "customer-tenure-days" field, that doesn't belong in Silver canonical. It belongs in the Service's Gold mart, computed from canonical inputs. Don't extend Silver for Service-specific derivations.

**KEVEN:** Synthesis?

**MORGAN:** Extension gate exists. It gets stricter as the engagement matures. Service-specific computations live in Gold, not Silver. Canonical is for *shared meaning*.

---

## Lessons

**KEVEN:** Monday-morning lessons for the Silver work.

One — **on sprint one of the Silver build, write the identity reconciliation policy for each canonical.** Primary identity. Survivorship rules. Tie-breaker logic. Even if it's three sentences per canonical. Get it on paper.

Two — **set up the Purview policy templates in the workspace before any Silver pipeline runs.** Sensitivity labels, DLP, retention. Then the pipelines inherit governance from day one.

Three — **for every canonical, write a *quality contract* alongside the schema definition.** Completeness, validity, uniqueness, consistency, timeliness — even if some are TBD. The contract evolves but it exists.

Four — **review the canonical-extension queue at sprint planning every sprint.** Not at the start of each Service build. Continuously. The queue is the heartbeat of canonical evolution.

Five — **give the client's auditor a Purview audit-reader role in week one.** Not week thirty. Don't build a custom audit interface. Purview is the audit interface.

---

## Carve Outs

**MORGAN:** Carve outs. Mine — Chapter Eleven, the *quality framework* section. Read it twice. Most engineering teams under-invest in declaring quality contracts because they think it's busywork. Then they spend six weeks chasing data-quality firefighters in late sprints. The quality contract section is the single best ROI hour you'll spend on the engagement.

**KEVEN:** Mine — read Chapter Twelve, the section on the Purview policy templates for APEX. Then go to the Deployment Guide and read the parallel section on *deploying* the templates. Services Guide tells you what they are. Deployment Guide tells you how they land in a client tenant. The two together are how you go from architecture to running governance.

---

## Sign-off

**KEVEN:** That's it for Episode Three. Next episode — *Gold Tier — Decision-Ready Data.* Part Four of the Services Guide. Lakehouse patterns. Per-Service Gold marts. The agent MCP tool surface. The episode that closes the medallion loop.

**MORGAN:** See you there.

[outro]

---

**End of Episode 03 · Silver Tier — Where Canonical Lives**
*≈ 5,100 words*
