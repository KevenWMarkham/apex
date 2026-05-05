# Sprint 3 Plan — Practice Schemas + Industry-Standard Integration

**Source:** `APEX_Design.md` §5 + §15 · `Industry-Standards-Incorporation-Plan.md` · `Orchestrator.md` Sprint 3
**Depends on:** Sprint 1 L1 contract ✅ · Sprint 2 RC anchor + `apex-schemas-common.standards` ✅
**Closes:** BL.P.11–P.19 (Practice schemas) · BL.P.139–P.146 (Pattern-B packages) · BL.P.148–P.153, P.162, P.165 (standards bindings/translators that fall out of Sprint 3 entity work)
**Date:** 2026-04-19

---

## 1. Purpose

Define concretely:

1. **Which canonical entities** each remaining Practice (HLS, ER, AXLE, TMT, TH, ICE) ships.
2. **Which industry standards** each entity binds to, using which of the four incorporation patterns (A/B/C/D — see `Industry-Standards-Incorporation-Plan.md` §4).
3. **Which `apex-standards-*` Pattern-B packages** must exist *before* the consuming Practice entity code can compile, and their minimum-viable scope.
4. **Cross-Practice sharing** of standards packages.
5. **Parallelisation plan** — who can work on what concurrently after the shared packages ship.
6. **Acceptance criteria** per Practice.

This plan is Sprint 3's contract. Every entity module shipped in Sprint 3 MUST reflect the pattern table assigned to it here; every deviation is a PR comment.

---

## 2. Sprint 3 Structure — Two Phases

Sprint 3 runs in two phases because Pattern-B packages block consuming Practice packages:

```
Phase 1 — Shared Pattern-B standards packages (weeks 1–3)
  ├── apex-standards-fhir    (R4 subset)            blocks: HLS
  ├── apex-standards-cim     (IEC 61970/61968)      blocks: ER
  ├── apex-standards-isa95   (hierarchy + common)   blocks: ER, AXLE, ICE
  ├── apex-standards-sid     (TM Forum SID subset)  blocks: TMT
  ├── apex-standards-opentravel (OTA subset)        blocks: TH
  ├── apex-standards-cdisc   (ODM/SDTM subset)      blocks: HLS (StudyML)
  ├── apex-standards-j1939   (SPN/PGN registry)     blocks: AXLE, ICE
  └── apex-standards-iso14224 (reliability model)   blocks: AXLE, ICE

Phase 2 — Practice packages (weeks 2–5, parallel by Practice lead)
  ├── apex-hlscml            ← depends on fhir + cdisc
  ├── apex-ercml             ← depends on cim + isa95
  ├── apex-axlecml           ← depends on isa95 + j1939 + iso14224
  ├── apex-telml             ← depends on sid
  ├── apex-thml (iropsml)    ← depends on opentravel
  └── apex-iceml (connectediceml) ← depends on j1939 + iso14224
```

**Total duration:** 4 weeks single-stream, 3 weeks with two streams, 2 weeks with three+ streams.

---

## 3. Per-Practice Plans

Each sub-section specifies:

- **Entities** — one row per canonical entity with the pattern used.
- **Pattern-A identifier types** — added to `apex-schemas-common.standards.types` or per-Practice types module.
- **Pattern-B mirrors needed** — in the dependent `apex-standards-*` package.
- **Pattern-D translators** — shipped in the Practice package's `translators/` subpackage.
- **Classifications** — per entity, which APEX classifications dominate.

### 3.1 HLS — Healthcare & Life Sciences

**Package:** `packages/apex-hlscml/`
**Depends on:** `apex-standards-fhir`, `apex-standards-cdisc`
**Classifications:** **PHI**-heavy — every identifier gets `_token` suffix and `Classification.PHI`.
**Design anchor:** APEX_Design §15 HLS row; `Industry-Standards-Incorporation-Plan.md` §6.2.

#### Canonical entities

| Entity | Pattern | Standard source | Notes |
|--------|---------|-----------------|-------|
| `Patient` | C (consume+extend) | FHIR R4 Patient | `from_fhir()`, `to_fhir()`, MRN tokenised |
| `Encounter` | C | FHIR R4 Encounter | Visit-level container; links to Patient |
| `Observation` | C | FHIR R4 Observation | Lab result / vital — LOINC code via Pattern A |
| `DiagnosticReport` | C | FHIR R4 DiagnosticReport | Report container for Observations |
| `MedicationRequest` | C | FHIR R4 MedicationRequest | Prescription — RxNorm + NDC via Pattern A |
| `Practitioner` | C | FHIR R4 Practitioner | Clinician identity, tokenised |
| `ClaimHeader` | C | FHIR R4 Claim (+ HIPAA X12 837) | Claim-level |
| `ClaimLine` | C | FHIR R4 ExplanationOfBenefit | Line-level |
| `Study` | C | CDISC ODM Study | Trial-level entity |
| `StudyEnrollment` | C | CDISC ODM Subject | Trial participant |
| `AdverseEvent` | C | CDISC SDTM AE | Trial safety event |

#### Pattern-A identifier types (in `apex-schemas-common.standards.types`)

Already shipped: `Icd10Code`, `NdcCode`, `LoincCode`.
Add in Sprint 3 Phase 1:

- `CptCode` — `^\d{5}$` → `StandardRef("cpt", "CPT", "2026")`
- `HcpcsCode` — `^[A-V][0-9]{4}$` → `StandardRef("hcpcs", "HCPCS-L2", "2026")`
- `RxNormConceptId` — `^\d{1,7}$` → `StandardRef("rxnorm", "RxCUI", "2026-01")`
- `SnomedCtConceptId` — `^\d{6,18}$` → `StandardRef("snomed-ct", "SCTID", "2026-01")`
- `FhirReference` — `^[A-Z][A-Za-z]+/[A-Za-z0-9\-\.]+$` → marker type

#### Pattern-B mirrors to ship in `apex-standards-fhir`

**R4 resource subset** (scope: fields used by HLS agents; exhaustive FHIR coverage is out of scope):

| Resource | Fields in scope |
|----------|-----------------|
| `FhirPatient` | id, identifier[], name[], telecom[], gender, birthDate, address[] |
| `FhirEncounter` | id, status, class, subject, period, reasonCode[] |
| `FhirObservation` | id, status, code, subject, effectiveDateTime, valueQuantity, valueCodeableConcept |
| `FhirDiagnosticReport` | id, status, category, code, subject, effectiveDateTime, result[] |
| `FhirMedicationRequest` | id, status, medicationCodeableConcept, subject, authoredOn, dosageInstruction[] |
| `FhirPractitioner` | id, identifier[], name[], qualification[] |
| `FhirClaim` | id, status, type, patient, provider, item[] |
| `FhirCoding`, `FhirCodeableConcept`, `FhirIdentifier`, `FhirHumanName`, `FhirAddress`, `FhirPeriod`, `FhirReference`, `FhirQuantity` | Shared primitives |

**Scope rule:** when a downstream agent in a later sprint needs an additional FHIR field, add it to the mirror *as that sprint's PR*, not speculatively in Sprint 3.

**R4 → R5 migration:** stub only in Sprint 3. Full migration defers until HLS clients need R5.

#### Pattern-D translators (in `apex-hlscml/translators/`)

- `fhir_to_hlscml.py` — `FhirPatient → Patient`, `FhirObservation → Observation`, etc. Tokenises PHI at the boundary.
- `hlscml_to_fhir.py` — inverse, re-hydrating cleartext only for authorised identities via the tokenizer-mcp.
- `hl7v2_to_fhir_stub.py` — stub + fixture of two ADT A01/A04 messages; full parser is BL.P.156 (later sprint).
- `cda_to_fhir_stub.py` — stub + one C-CDA fixture; full parser is BL.P.157.

#### Pattern-B mirrors to ship in `apex-standards-cdisc`

- `CdiscStudy`, `CdiscSubject`, `CdiscAdverseEvent`, `CdiscFormData` (ODM-aligned).
- SDTM domain skeletons: DM (Demographics), AE (Adverse Events), LB (Labs). Full SDTM is out of scope.

#### Acceptance criteria

- [ ] `apex-standards-fhir` installs and tests round-trip for at least one reference FHIR R4 fixture per resource.
- [ ] Every HLSCML entity has `from_fhir` / `to_fhir` with round-trip test.
- [ ] Tokenisation applied to: `mrn_token`, `name_family_token`, `name_given_token`, `address_token`, `phone_token`, `email_token`, `practitioner_npi_token`.
- [ ] `audit_model()` passes on every HLSCML entity.
- [ ] LOINC / ICD-10 / NDC / RxNorm / CPT / HCPCS bindings all register in `STANDARDS`.

---

### 3.2 ER — Energy & Resources

**Package:** `packages/apex-ercml/`
**Depends on:** `apex-standards-cim`, `apex-standards-isa95`
**Classifications:** Mix of **INTERNAL** + **EXPORT_CONTROLLED** (NERC CIP data) + **TRADE_SECRET** (operational parameters).

#### Canonical entities

| Entity | Pattern | Standard source | Notes |
|--------|---------|-----------------|-------|
| `Meter` | C | CIM `Meter` (IEC 61968) | AMI meter; identifier resolution on meter serial |
| `MeterReading` | C | CIM `Reading` | Time-series reading; classified INTERNAL |
| `GridEvent` | C | CIM `EnergyEvent` | Outage / voltage-sag / equipment fault |
| `Asset` | C | CIM `Asset` (IEC 61968-4) | Pole / transformer / substation |
| `WorkOrder` | C | CIM `WorkOrder` | Maintenance / inspection work |
| `Well` | C | WITSML `Well` | O&G: well head |
| `Production` | C | PRODML | O&G: production-well metrics |
| `IsoReliabilityRecord` | B | ISO 14224 (via `apex-standards-iso14224`) | Reliability data for trend analysis |
| `NercComplianceFlag` | A | NERC CIP identifier | Reference to regulated assets |

#### Pattern-A identifier types

- `CimMRID` — CIM master resource identifier (UUID-ish)
- `NercCipClassification` — Literal `{"LOW", "MEDIUM", "HIGH", "NON_BULK"}`
- `IsoReliabilityTaxonomy` — ISO 14224 taxonomy codes

#### Pattern-B mirrors to ship in `apex-standards-cim`

Focus: IEC 61970 + 61968 subset needed for utility-operations agents.

- Core classes: `CimAsset`, `CimLocation`, `CimCustomer`, `CimMeter`, `CimReading`, `CimEnergyEvent`, `CimWorkOrder`, `CimEquipment`.
- Common types: `MRID`, `DateTimeInterval`, `UnitSymbol` enum.

**Out of scope for Sprint 3:** IEC 61850 substation automation (Pattern T5, Sprint 15 adapter).

#### Pattern-B mirrors to ship in `apex-standards-isa95`

**SHARED: consumed by ER, AXLE, ICE.** (Design §15.)

- `Isa95Enterprise`, `Isa95Site`, `Isa95Area`, `Isa95WorkCenter`, `Isa95WorkUnit` — hierarchy.
- `Isa95Personnel`, `Isa95Equipment`, `Isa95Material`.
- `Isa95PhysicalAsset`, `Isa95ProcessSegment`.

#### Pattern-D translators (in `apex-ercml/translators/`)

- `cim_to_ercml.py` + inverse with round-trip.
- `cim_to_iso15926_stub.py` — stub (BL.P.164 full impl is later).

#### Acceptance criteria

- [ ] `apex-standards-cim` installs; CIM Asset round-trip works against CIM reference XML fixture.
- [ ] `apex-standards-isa95` installs; hierarchy tests in both ER and AXLE/ICE consumers.
- [ ] ERCML Meter + MeterReading entity for a utility's AMI meter reading can be constructed from CIM reference payload via `cim_to_ercml.meter_from_cim`.

---

### 3.3 AXLE — Automotive / Industrial Manufacturing

**Package:** `packages/apex-axlecml/`
**Depends on:** `apex-standards-isa95`, `apex-standards-j1939`, `apex-standards-iso14224`
**Classifications:** mostly **INTERNAL**, occasional **TRADE_SECRET** on process recipes.

#### Canonical entities

| Entity | Pattern | Standard source | Notes |
|--------|---------|-----------------|-------|
| `Equipment` | C | ISA-95 Equipment | Production-floor asset hierarchy |
| `WorkCenter` | C | ISA-95 WorkCenter | Grouping |
| `ProductionEvent` | C | ISA-95 ProductionEvent + ISA-88 | Batch start / end / transition |
| `QualityResult` | C | ISA-95 + IATF 16949 | Per-unit / per-batch quality |
| `Genealogy` | C | ISA-95 ProductDefinition + lineage edges | Lot / serial traceability |
| `BillOfMaterials` | C | STEP AP242 | Product structure |
| `J1939Signal` | A | SAE J1939 (PGN/SPN) | Vehicle-bus signal reference |
| `ReliabilityRecord` | B | ISO 14224 | Shared with ICE |
| `OpcUaNodeRef` | A | OPC UA NodeId | Reference only; adapter in Sprint 15 |

#### Pattern-A identifier types

- `J1939Spn` — integer 0-524287 + lookup to J1939 SPN catalog
- `J1939Pgn` — integer 0-131071
- `StepProductId` — STEP AP242 product id
- `OpcUaNodeId` — `ns=<int>;[s|i|g|b]=<value>` regex

#### Pattern-B mirrors in `apex-standards-j1939`

**SHARED: consumed by AXLE + ICE.**

- `J1939Spn` dataclass with fields (spn_id, parameter_name, units, resolution, offset, range, length_bits).
- Seed registry with ~50 most-referenced SPNs (engine RPM, coolant temp, fuel level, etc.).
- `J1939Pgn` dataclass + seed registry.
- Not redistributing the full SPN catalog (SAE licence — see §8 of standards plan).

#### Pattern-B mirrors in `apex-standards-iso14224`

**SHARED: consumed by AXLE + ICE.**

- `Iso14224Equipment` taxonomy.
- `Iso14224FailureMode` enum (leakage, vibration, structural, etc.).
- `ReliabilityRecord` canonical shape.

#### Pattern-D translators (in `apex-axlecml/translators/`)

- `isa95_to_axlecml.py` — parent-class hierarchy to Equipment tree.
- `step_to_axlecml_bom.py` — STEP AP242 BoM → AXLECML BillOfMaterials (stub with one fixture; full in later sprint).

#### Acceptance criteria

- [ ] Shared `apex-standards-isa95` consumed successfully by `apex-axlecml`, `apex-ercml`, and `apex-iceml` (integration test).
- [ ] J1939 signal lookup works against 50-SPN seed registry.
- [ ] Genealogy entity handles forward + reverse lineage queries.

---

### 3.4 TMT — Technology, Media, Telecom

**Package:** `packages/apex-telml/`
**Depends on:** `apex-standards-sid`
**Classifications:** **INTERNAL** on network/service data; **PII** on CRM data; **PCI** on billing.

#### Canonical entities

| Entity | Pattern | Standard source | Notes |
|--------|---------|-----------------|-------|
| `TelcoCustomer` | C | TM Forum SID Customer | Extends RC's Customer concept |
| `ProductOffering` | C | TM Forum SID ProductOffering | Sellable bundle |
| `Service` | C | TM Forum SID Service | Provisioned service instance |
| `NetworkResource` | C | TM Forum SID Resource | Physical or logical network element |
| `BillingAccount` | C | TM Forum SID BillingAccount | Customer billing binding |
| `ContentAsset` | C | SMPTE / EIDR | Media asset |
| `AdImpression` | C | IAB AdCOM | Ad-tech atom |

#### Pattern-A identifier types

Already in `apex-schemas-common.standards.types`: `Eidr`.
Add: `ImsiMsisdn`, `ImeiImeisv`, `E164PhoneNumber`, `TM_Forum_ID`.

#### Pattern-B mirrors in `apex-standards-sid`

**Scope:** SID domains most agents consume — Customer, Product, Service, Resource, Party. Skip heavy SID domains (Market / Sales / ResourceInventoryManagement) until a consuming agent exists.

- `SidCustomer`, `SidProductOffering`, `SidProduct`, `SidService`, `SidResource`, `SidParty`, `SidBillingAccount`.
- Shared primitives: `SidLifecycleStatus`, `SidRelatedParty`.

#### Pattern-D translators

- `sid_to_telml.py` — SID → TELML canonical.
- `eidr_resolver_stub.py` — EIDR identifier → Content Asset reference (full resolver is later).

#### Acceptance criteria

- [ ] SID Customer ↔ TelcoCustomer round-trip.
- [ ] EIDR regex passes against reference ID fixture.
- [ ] TelcoCustomer FK to CXML Customer resolves (cross-Practice federation check).

---

### 3.5 TH — Travel & Hospitality

**Package:** `packages/apex-thml/` (note: design calls it `IROPsML`; proposing `thml` as the module root with IROP / Reservation sub-packages inside)
**Depends on:** `apex-standards-opentravel`
**Classifications:** **PII**-heavy (traveler identity), **PCI** on payment, **MEMBER_ONLY** on loyalty.

#### Canonical entities

| Entity | Pattern | Standard source | Notes |
|--------|---------|-----------------|-------|
| `Traveler` | C | IATA NDC OrderPassenger + OpenTravel | PII tokenised |
| `Reservation` | C | IATA NDC Order + OpenTravel Reservation | Container |
| `Itinerary` | C | OpenTravel Air + Hotel + Car subsets | Per-trip journey |
| `Segment` | C | IATA NDC FlightSegment + OTA | Flight leg / hotel stay / car day |
| `LoyaltyAccount` | C | Program-specific + OTA LoyaltyInfo | Tier + balance |
| `Disruption` | C | IROPs event model | Cancellation / delay / equipment swap |
| `Booking` | C | IATA NDC ConfirmedBooking | Post-payment state |

#### Pattern-A identifier types

- `IataAirportCode` — `^[A-Z]{3}$`
- `IataAirlineCode` — `^[A-Z]{2,3}$`
- `PnrLocator` — `^[A-Z0-9]{6}$`

#### Pattern-B mirrors in `apex-standards-opentravel`

**OTA Air / Hotel / Car subsets** (agents consume thin slice, not the whole OTA schema corpus):

- `OtaAirReservation`, `OtaAirSegment`, `OtaTraveler`.
- `OtaHotelReservation`, `OtaHotelStay`.
- `OtaCarReservation`.

#### Pattern-D translators

- `iata_ndc_to_thml.py` — NDC Order → Reservation + Itinerary.
- `ota_to_thml.py` — OTA Reservation → Reservation.
- `padis_stub.py` — stub for IATA PADIS messages (full in Sprint 15 adapter).

#### Acceptance criteria

- [ ] Traveler + Reservation + Itinerary + Segment round-trip against one NDC reference fixture.
- [ ] OTA Hotel reservation round-trip.
- [ ] PII tokenisation covers: full_name, email, passport_number, loyalty_number, payment_method.

---

### 3.6 ICE — Industrial & Commercial Equipment

**Package:** `packages/apex-iceml/` (or `apex-connectediceml/`)
**Depends on:** `apex-standards-j1939`, `apex-standards-iso14224`
**Classifications:** mostly **INTERNAL** with occasional **TRADE_SECRET** on OEM-licensed telematics payloads.

#### Canonical entities

| Entity | Pattern | Standard source | Notes |
|--------|---------|-----------------|-------|
| `Equipment` | C | AEMP 2.0 / ISO 15143-3 Equipment | Unit / serial |
| `TelemetryReading` | C | AEMP 2.0 Snapshot + J1939 SPN lookup | Normalised telemetry |
| `ServiceEvent` | C | ISO 14224 Event + OEM service codes | Fault / anomaly |
| `MaintenanceRecord` | C | OEM service-record format | Completed / scheduled |
| `FleetMember` | C | AEMP 2.0 fleet association | Cross-unit grouping |
| `EsgMetric` | C | CDP / ESG reporting shape | Sustainability output |

#### Pattern-A identifier types

- `AempEquipmentId`, `Vin17` (vehicle identification number 17-char), `EsgMetricCode`.

#### Pattern-B mirrors

No dedicated ICE-specific Pattern-B package; all needed mirrors live in the **shared** `apex-standards-j1939` and `apex-standards-iso14224` packages.

#### Pattern-D translators

- `j1939_to_aemp.py` + inverse — round-trip tested.
- `aemp_to_iceml.py` — vendor AEMP feed → IceML Equipment + TelemetryReading.

#### Acceptance criteria

- [ ] AEMP 2.0 reference snapshot parses into Equipment + TelemetryReading.
- [ ] J1939 SPN resolution works against the seed-50 registry.
- [ ] Cross-Practice sharing verified: `apex-standards-j1939` used identically in AXLE tests and ICE tests.

---

## 4. Shared Pattern-B Packages in Detail

### 4.1 `apex-standards-fhir`

- `pyproject.toml` deps: pydantic + apex-core.
- `src/apex_standards_fhir/r4/` — one file per resource.
- `src/apex_standards_fhir/primitives/` — shared types (Identifier, HumanName, CodeableConcept, …).
- `src/apex_standards_fhir/r5/` — skeleton only in Sprint 3.
- `src/apex_standards_fhir/migrations/r4_to_r5.py` — stub.
- Tests: round-trip against HL7-published FHIR example JSONs for each in-scope resource.

### 4.2 `apex-standards-cim`

- `src/apex_standards_cim/iec_61970/` — power-system model subset.
- `src/apex_standards_cim/iec_61968/` — utility-operations subset.
- `src/apex_standards_cim/shared/` — MRID + common types.
- Tests: reference CIM XML fixture round-trips.

### 4.3 `apex-standards-isa95`

- `src/apex_standards_isa95/hierarchy.py` — Enterprise / Site / Area / WorkCenter / WorkUnit.
- `src/apex_standards_isa95/personnel.py`, `.../equipment.py`, `.../material.py`.
- Tests: verify hierarchy parent/child integrity; shared-usage tests imported by ER / AXLE / ICE test suites.

### 4.4 `apex-standards-sid`

- `src/apex_standards_sid/customer/`, `.../product/`, `.../service/`, `.../resource/`, `.../party/`.
- Kept intentionally thin — SID is huge; resist full-fidelity mirror.

### 4.5 `apex-standards-opentravel`

- `src/apex_standards_opentravel/air/`, `.../hotel/`, `.../car/`, `.../shared/`.
- Fixtures from OpenTravel sample XMLs.

### 4.6 `apex-standards-cdisc`

- `src/apex_standards_cdisc/odm/` — study / subject / form shapes.
- `src/apex_standards_cdisc/sdtm/` — DM / AE / LB domains.
- `define_xml/` — stub.

### 4.7 `apex-standards-j1939`

- `src/apex_standards_j1939/spn.py` — Signal Parameter Number + 50-seed registry.
- `src/apex_standards_j1939/pgn.py` — Parameter Group Number + seed registry.
- `src/apex_standards_j1939/frame.py` — CAN-frame shape (for decoding during adapter work in Sprint 15).
- **Licence:** do NOT redistribute full SAE SPN catalog. README documents "tenant supplies full catalog" hook.

### 4.8 `apex-standards-iso14224`

- `src/apex_standards_iso14224/taxonomy.py` — equipment taxonomy.
- `src/apex_standards_iso14224/failure_modes.py` — enum.
- `src/apex_standards_iso14224/reliability_record.py` — canonical shape.

---

## 5. Cross-Practice Sharing Map

| Shared package | ER | AXLE | ICE | HLS | TMT | TH |
|----------------|:--:|:----:|:---:|:---:|:---:|:--:|
| `apex-standards-isa95` | ✅ | ✅ | ✅ | | | |
| `apex-standards-j1939` | | ✅ | ✅ | | | |
| `apex-standards-iso14224` | | ✅ | ✅ | | | |
| `apex-standards-fhir` | | | | ✅ | | |
| `apex-standards-cim` | ✅ | | | | | |
| `apex-standards-cdisc` | | | | ✅ | | |
| `apex-standards-sid` | | | | | ✅ | |
| `apex-standards-opentravel` | | | | | | ✅ |

**Invariants to enforce in CI:**

- A Practice package MUST NOT import from another Practice package (`apex-hlscml` cannot import `apex-ercml`).
- A Practice package MAY import from `apex-core`, `apex-schemas-common`, and any `apex-standards-*`.
- An `apex-standards-*` package MUST NOT import from any Practice package.

---

## 6. Sprint 3 Parallelisation Plan

### Single-stream (one engineer)

Sequential by phase: Phase 1 → Phase 2. ~4 weeks total.

### Two-stream

- **Stream A (standards engineer):** Phase 1 all packages (FHIR first → ISA-95 → CIM → SID → OpenTravel → CDISC → J1939 → ISO 14224).
- **Stream B (practice engineer):** Once a given Phase-1 package merges, starts its dependent Practice package.

Estimate: 3 weeks.

### Three-plus-stream (recommended)

- **Stream A (FHIR + HLS lead):** `apex-standards-fhir` + `apex-standards-cdisc` + `apex-hlscml`. ~15 days.
- **Stream B (industrial lead):** `apex-standards-isa95` + `apex-standards-j1939` + `apex-standards-iso14224` + `apex-axlecml` + `apex-iceml`. ~15 days.
- **Stream C (utility + TMT + TH lead):** `apex-standards-cim` + `apex-standards-sid` + `apex-standards-opentravel` + `apex-ercml` + `apex-telml` + `apex-thml`. ~15 days.

Estimate: 2 weeks. Requires cross-stream coordination meeting (weekly) to keep shared ISA-95 package stable.

---

## 7. Acceptance Criteria (Sprint 3 as a whole)

Sprint 3 closes when:

1. All 8 `apex-standards-*` Pattern-B packages ship and pass `uv run pytest`.
2. All 6 Practice packages (`apex-hlscml`, `apex-ercml`, `apex-axlecml`, `apex-telml`, `apex-thml`, `apex-iceml`) ship and pass tests.
3. Each Practice package's entities have a round-trip test against at least one reference fixture from the standard authority.
4. `apex standards audit` reports zero `registered=False` or `version_matches=False` across all packages.
5. Cross-Practice sharing verified: `apex-standards-isa95` passes tests when imported by ER, AXLE, ICE simultaneously.
6. CI `conformance` lane green (depends on `BL.P.136`).
7. `Roadmap.md` ticks BL.P.11–P.19 + BL.P.139–P.146 + BL.P.148–P.153, P.162, P.165.

---

## 8. Dependencies on Other Sprints

- **Sprint 2 complete** ✅ — `apex-schemas-common.standards` module is the foundation for every Pattern-A binding in Sprint 3.
- **BL.P.135 (apex standards CLI)** — recommended to ship *before* Sprint 3 starts; gives us `apex standards audit` during Phase 1 development. Small item (~1 day).
- **BL.P.136 (conformance CI lane)** — recommended *before* Sprint 3 starts; CI green from day 1 is much cheaper than retrofitting.
- **Sprint 5 (tokeniser + Silver transform)** — not a Sprint 3 dependency, but HLSCML Patient's PHI tokenisation is the first production driver. Flag: HLSCML ships the classifications in Sprint 3; actual tokenisation runtime ships in Sprint 5.

---

## 9. Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|:----------:|------------|
| FHIR mirror scope creep — every HLS agent wants "just one more field" | High | Fix R4 mirror at the Sprint-3-planned-subset; additions require a new PR tied to a consuming agent |
| SNOMED CT / LOINC licence breach via accidental content redistribution | Medium | `apex-standards-*` licence attribution doc + CI check that flags any file >1 MB |
| ISA-95 hierarchy disagreements across ER / AXLE / ICE | Medium | Weekly sync during Phase 1; hierarchy.py PRs require approval from all three Practice leads |
| Standards-version drift (FHIR R4 → R5 announced mid-Sprint) | Low | `apex_pinned_version` in registry; version-bump is a deliberate later-sprint PR |
| CIM modelling depth underestimated | Medium | Scope cap: only IEC 61970 core + 61968 utility-ops subset in Sprint 3; 62325 market model deferred |
| OPC UA tried to be modelled as schema instead of adapter | Low | Locked down in `Industry-Standards-Incorporation-Plan.md` §6: OPC UA is Sprint 15 adapter only |

---

## 10. Open Questions

1. **Which HLS agents consume which FHIR resources?** — needed to finalise FHIR mirror scope. Default: the 8 resources listed in §3.1 cover the anchor 10 HLS agents from Implementation Plan §15.
2. **SID scope for TMT** — TMT has 45+ SID domains. Confirm which Practice leads consider essential Sprint-3 scope. Default: 7 domains listed in §3.4.
3. **Bring-your-own terminology service** — does Deloitte pilot have access to a SNOMED CT / LOINC terminology server, or do we ship a dev-only mock? Default: dev-only mock in `apex-standards-fhir/terminology/mock.py`, tenant swaps for real service.
4. **Package naming — `apex-thml` vs `apex-iropsml`** — design says IROPsML but TH covers more than IROPs. Proposing `apex-thml` with IROP as a sub-module. Confirm.
5. **Package naming — `apex-iceml` vs `apex-connectediceml`** — design says ConnectedICEML. Proposing `apex-iceml` as the Python module (shorter) with ConnectedICE used in docs. Confirm.

---

## 11. What Ships vs What Defers

| Item | Sprint 3 | Later |
|------|:--------:|:-----:|
| FHIR R4 Patient / Encounter / Observation / DiagnosticReport / MedicationRequest / Practitioner / Claim | ✅ | |
| FHIR R5 mirror | stub | Sprint after HLS reference deployment |
| FHIR full resource set | | Incremental per agent |
| CIM IEC 61970 + 61968 subset | ✅ | |
| CIM 62325 (market) | | Only if market-agent demand arises |
| SNOMED CT terminology *binding* (regex + hook) | ✅ | |
| SNOMED CT *content* | | Never (licence) |
| LOINC binding | ✅ | |
| ICD-10 / NDC / CPT / HCPCS / RxNorm bindings | ✅ | |
| ISA-95 hierarchy | ✅ | |
| ISA-88 batch model | stub | Consumed by AXLE batch-manufacturing reference deployment (Sprint 18) |
| STEP AP242 / PLCS | stub | Sprint when needed by consuming agent |
| OPC UA schema modelling | | NEVER — it's a Sprint 15 adapter |
| AEMP 2.0 mirror | ✅ | |
| J1939 SPN 50-seed registry | ✅ | |
| J1939 full SPN catalog | | Tenant-supplied |
| ISO 14224 taxonomy | ✅ | |
| TM Forum SID core domains (7) | ✅ | |
| TM Forum SID full (45+ domains) | | Incremental per agent |
| OpenTravel Air/Hotel/Car subsets | ✅ | |
| OpenTravel full corpus | | Incremental per agent |
| CDISC ODM + SDTM skeleton | ✅ | |
| CDISC full + Define-XML | | Sprint when needed |
| EIDR identifier binding | ✅ | |
| HL7 v2 → FHIR R4 full parser | stub | BL.P.156 later sprint |
| HL7 CDA → FHIR R4 full parser | stub | BL.P.157 later sprint |
| DICOM | | Sprint 15 adapter |
| EDI X12 / HIPAA X12 full parsers | | BL.P.155 later sprint |

---

## 12. Definition of Done

Sprint 3 is done when:

1. All 14 packages merged (8 standards + 6 practices).
2. Full suite green: `.venv/Scripts/python -m pytest packages -q` shows N+ passed where N is Sprint-2 baseline (118) plus additions.
3. `apex standards audit` green across every Practice package.
4. `Roadmap.md` reflects ticked BL items + updated progress snapshot.
5. Cross-Practice integration test runs: `apex-standards-isa95` consumed by ER + AXLE + ICE without conflict.
6. Open questions §10 answered.
7. This plan's risks §9 reviewed and mitigations held.
