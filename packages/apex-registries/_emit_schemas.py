"""Emit Appendix A schema registry — 48 canonical schema families."""
import yaml
from pathlib import Path

OUT = Path(__file__).parent / "src" / "apex_registries" / "schemas"
OUT.mkdir(parents=True, exist_ok=True)

SCHEMAS = [
    # RC
    ("SCML",  "Supply Chain Management Lineage",         ["rc"],            ["Lot","Movement","Trace","Allocation"],         ["GS1","FSMA 204","EDI X12"],          "operations",        "apex-scml"),
    ("CXML",  "Customer Experience Management Lineage",  ["rc"],            ["Customer","Identity","Journey","Consent"],     ["UCDM","GDPR"],                       "pii",                "apex-cxml"),
    ("MERML", "Merchandising Lineage",                   ["rc","axle"],     ["Assortment","Markdown","Pricing","ProductMaster"], ["GS1"],                          "operations",        "apex-merml"),
    # HLS
    ("PatientML",  "Patient Management Lineage",         ["hls"],           ["Patient","Encounter","Observation","Order"],   ["HL7 FHIR R4","HIPAA"],               "phi",                "apex-patientml"),
    ("ClaimML",    "Claim Management Lineage",           ["hls"],           ["Claim","Adjudication","Denial","Remittance"],  ["HIPAA 837","835","270/271"],         "phi",                "apex-claimml"),
    ("EncounterML","Clinical Encounter Lineage",         ["hls"],           ["Encounter","Diagnosis","Procedure","CarePlan"], ["HL7 FHIR R4"],                      "phi",                "apex-encounterml"),
    ("StudyML",    "Clinical Study Lineage",             ["hls"],           ["Study","Subject","Visit","AdverseEvent"],      ["CDISC SDTM","CDASH"],                "phi",                "apex-studyml"),
    ("MEDML",     "Medication Lineage",                  ["hls"],           ["Medication","Order","Administration","Reconciliation"], ["HL7 FHIR R4","NDC"],         "phi",                "apex-medml"),
    ("PopHealthML","Population Health Lineage",          ["hls"],           ["Cohort","RiskScore","CareGap","Attribution"],  ["HEDIS","CMS Stars"],                 "phi",                "apex-pophealthml"),
    ("ProvML",    "Provider Lineage",                    ["hls"],           ["Provider","Affiliation","Privilege","Credential"], ["NPPES","DEA"],                  "phi",                "apex-provml"),
    # ER
    ("GridML",   "Grid Operations Lineage",              ["er"],            ["Substation","Feeder","Section","Asset"],       ["IEC CIM","MultiSpeak"],              "critical-infrastructure","apex-gridml"),
    ("OutageML", "Outage Lineage",                       ["er"],            ["Outage","Affected","Restoration","Cause"],     ["IEC CIM"],                           "critical-infrastructure","apex-outageml"),
    ("MeterML",  "Metering Lineage",                     ["er"],            ["Meter","Reading","Tariff","Bill"],             ["MultiSpeak","IEC 62056"],            "pii",                "apex-meterml"),
    ("DERMML",  "Distributed Energy Resource Mgmt Lineage", ["er"],         ["DER","Aggregation","Dispatch","Constraint"],   ["IEEE 1547","IEC 61850"],             "critical-infrastructure","apex-dermml"),
    ("UOGML",    "Upstream Oil and Gas Lineage",         ["er"],            ["Well","DrillingOp","Production","HSEEvent"],   ["WITSML","PRODML"],                   "operations",        "apex-uogml"),
    ("DrillingML","Drilling Operations Lineage",         ["er"],            ["Rig","Bore","SafetyEvent"],                    ["WITSML","IADC"],                     "operations",        "apex-drillingml"),
    ("MiningML", "Mining Operations Lineage",            ["er"],            ["Pit","Haul","Asset","ShiftPlan"],              ["IREDES","ISA-95"],                   "operations",        "apex-miningml"),
    ("HSEML",    "HSE Event Lineage",                    ["er","axle"],     ["Incident","NearMiss","Investigation","CorrectiveAction"], ["OSHA","ISO 45001"],      "operations",        "apex-hseml"),
    ("PUML",     "Power and Utilities Cross Lineage",    ["er"],            ["TariffBook","RegulatoryFiling","StormEvent"],  ["FERC","NERC"],                       "critical-infrastructure","apex-puml"),
    # AXLE
    ("QMSML",   "Quality Mgmt System Lineage",           ["axle"],          ["NonConformance","CorrectiveAction","SupplierLot","Audit"], ["ISO 9001","IATF 16949"], "operations",        "apex-qmsml"),
    ("AAML",    "Aftermarket Aftersales Lineage",        ["axle"],          ["WarrantyClaim","DTC","ServiceCampaign","Telematics"], ["SAE J1939","UDS","ASAM"], "operations",        "apex-aaml"),
    ("MSCML",   "Manufacturing Supply Chain Lineage",    ["axle"],          ["WorkOrder","Operation","BOM","Routing"],       ["ISA-95","B2MML"],                    "operations",        "apex-mscml"),
    ("EngML",   "Engineering PLM Lineage",               ["axle"],          ["Part","Revision","ChangeNotice","BOM"],        ["ISO 10303 STEP"],                    "intellectual-property","apex-engml"),
    ("EquipML", "Equipment Health Lineage",              ["axle"],          ["Asset","Sensor","HealthScore","Failure"],      ["ISO 13374","ISO 14224"],             "operations",        "apex-equipml"),
    ("AftermarketML","Vehicle Aftermarket Lineage",      ["axle"],          ["Vehicle","Owner","ServiceHistory"],            ["VIN ISO 3779","SAE J2735"],          "pii",                "apex-aftermarketml"),
    # TMT
    ("BSSML",   "Business Support System Lineage",       ["tmt"],           ["Subscriber","Plan","Bill","Payment"],          ["TM Forum SID","3GPP"],               "pii",                "apex-bssml"),
    ("SubscriberML","Subscriber Lineage",                ["tmt"],           ["Subscriber","Account","Service","Usage"],      ["TM Forum SID"],                      "pii",                "apex-subscriberml"),
    ("ContentSafetyML","Content Safety IVT Lineage",     ["tmt"],           ["Asset","Decision","ReviewQueue","Appeal"],     ["IFTA","C2PA"],                       "operations",  "apex-contentsafetyml"),
    ("NetworkML","Network Operations Lineage",           ["tmt"],           ["Element","Alarm","Ticket","ChangeWindow"],     ["TM Forum eTOM"],                     "operations",        "apex-networkml"),
    ("RightsML","Rights Management Lineage",             ["tmt"],           ["Title","Right","Window","Territory"],          ["EIDR","UMG"],                        "intellectual-property","apex-rightsml"),
    # TH
    ("OpsML-TH","Travel Hospitality Ops Lineage",        ["th"],            ["FlightLeg","CrewPairing","Aircraft","Gate"],   ["IATA SSIM","A-CDM"],                 "operations",        "apex-opsml-th"),
    ("OpsML",   "Travel Hospitality Ops Lineage Alias",  ["th"],            ["FlightLeg","CrewPairing","Aircraft","Gate"],   ["IATA SSIM","A-CDM"],                 "operations",        "apex-opsml-th"),
    ("TravelerML","Traveler 360 Lineage",                ["th"],            ["Traveler","PNR","LoyaltyMember","Preference"], ["IATA NDC","OpenTravel"],             "pii",                "apex-travelerml"),
    ("RevML-TH","Travel Revenue Mgmt Lineage",           ["th"],            ["OandD","Fare","Inventory","Booking"],          ["IATA NDC","ATPCO"],                  "payment-card",       "apex-revml-th"),
    ("InvML-TH","Travel Inventory Lineage",              ["th"],            ["Inventory","SeatMap","HoldRule"],              ["IATA NDC"],                          "operations",        "apex-invml-th"),
    ("LoyaltyML","Loyalty Program Lineage",              ["th","rc"],       ["Member","Earn","Burn","Tier"],                 ["OpenTravel"],                        "pii",                "apex-loyaltyml"),
    ("IROPsML","Irregular Operations Lineage",           ["th"],            ["Disruption","RecoveryPlan","CustomerImpact","CrewImpact"], ["IATA NDC"],             "operations",        "apex-iropsml"),
    ("GroundML","Ground Operations Lineage",             ["th"],            ["Turn","Resource","BaggageEvent","FuelEvent"],  ["IATA SGHA"],                         "operations",        "apex-groundml"),
    # ICE
    ("AMML-ICE","Asset Mgmt for ICE Lineage",            ["ice"],           ["Asset","WorkOrder","Spare","Telemetry"],       ["ISO 14224","ISO 55000"],             "operations",        "apex-amml-ice"),
    ("AMML",   "Asset Mgmt Lineage Alias",               ["ice"],           ["Asset","WorkOrder","Spare","Telemetry"],       ["ISO 14224","ISO 55000"],             "operations",        "apex-amml-ice"),
    ("ConnectedICEML","Connected ICE Lineage",           ["ice"],           ["Device","Telemetry","FirmwareImage","Ticket"], ["MQTT","OPC UA"],                     "operations",        "apex-connectedice"),
    ("ConnectedProductML","Connected Product Lineage",   ["ice","axle"],    ["Product","Owner","Telemetry","UsageEvent"],    ["MQTT","OPC UA"],                     "operations",        "apex-connectedproduct"),
    ("DealerML","Dealer Channel Mgmt Lineage",           ["ice","axle"],    ["Dealer","Allocation","SalesEvent","Service"],  ["AAIA","RAPID"],                      "operations",        "apex-dealerml"),
    ("SupplyML-A","Aftermarket Supply Chain Lineage",    ["ice","axle"],    ["PartLot","DistributionMove","ReturnMaterial"], ["AIAG"],                              "operations",        "apex-supplyml-a"),
    ("SupplyML-ICE","ICE Supply Chain Lineage",          ["ice"],           ["PartLot","DistributionMove","ReturnMaterial"], ["AIAG"],                              "operations",        "apex-supplyml-ice"),
    ("QMSML-ICE","ICE Quality Mgmt Lineage",             ["ice"],           ["NonConformance","CorrectiveAction","Audit"],   ["ISO 9001"],                          "operations",        "apex-qmsml-ice"),
    ("TECML",   "Telematics Edge Compute Lineage",       ["axle","ice"],    ["EdgeDevice","Function","DataChunk"],           ["AUTOSAR","SAE J3016"],               "operations",        "apex-tecml"),
    ("TELML",   "Telematics Lineage",                    ["axle","ice","er"], ["VehicleEvent","Position","DTC","Trip"],      ["SAE J1939","SAE J2735"],             "operations",        "apex-telml"),
    ("CCML",    "Customer Care Lineage",                 ["tmt","th","rc","ice"], ["Case","Interaction","Resolution","SLA"], ["TM Forum SID","ITIL"],                "pii",                "apex-ccml"),
]

count = 0
for code, name, practices, entities, standards, classification, pkg in SCHEMAS:
    data = dict(
        kind="schema",
        schema_code=code,
        name=name,
        description=f"{name} canonical schema family. Bronze to Silver to Gold pipeline scope; consumed by APEX agents/services across {', '.join(p.upper() for p in practices)}.",
        practices=practices,
        primary_entities=entities,
        standards_alignment=standards,
        governance_classification=classification,
        appendix_a_section=f"Appendix A — Schema family {code}",
        package_implementation=pkg,
    )
    fname = f"{code.lower().replace('-', '_')}.yaml"
    path = OUT / fname
    with path.open("w", encoding="utf-8") as fh:
        fh.write("# harvest:auto-generated — apex_registries.harvest\n")
        yaml.safe_dump(data, fh, sort_keys=False, default_flow_style=False, allow_unicode=True)
    count += 1
print(f"Schemas written: {count}")
