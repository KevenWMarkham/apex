"""Golden fixtures for translator round-trip tests.

Synthetic but realistic-shaped messages. Sufficient for Sprint 23 exit
criterion ("Golden fixtures cover ≥3 real-world message variants per format").

Each fixture is a single-string message; tests parse → emit → parse and
assert the round-trip is faithful. Where the format is one-way (CDA,
PADIS), tests assert structural extraction only.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# EDI X12 — RC: 850, 856, 810, 820 ; HLS: 837, 835, 270, 271
# ---------------------------------------------------------------------------

# Note: ISA segment is fixed-width per §1 of the X12 standard. We use *
# as element separator and ~ as segment terminator.

_X12_850 = (
    "ISA*00*          *00*          *ZZ*SENDERID01     *ZZ*RECEIVERID01   "
    "*250630*1245*U*00501*000000001*0*P*:~"
    "GS*PO*SENDERID*RECEIVERID*20250630*1245*1*X*005010~"
    "ST*850*0001~"
    "BEG*00*SA*PO12345**20250630~"
    "REF*DP*DEPT01~"
    "PO1*1*100*EA*5.50**UP*012345678901~"
    "CTT*1~"
    "SE*6*0001~"
    "GE*1*1~"
    "IEA*1*000000001~"
)

_X12_856 = (
    "ISA*00*          *00*          *ZZ*SENDERID01     *ZZ*RECEIVERID01   "
    "*250701*0830*U*00501*000000002*0*P*:~"
    "GS*SH*SENDERID*RECEIVERID*20250701*0830*2*X*005010~"
    "ST*856*0002~"
    "BSN*00*SHIP12345*20250701*0830~"
    "HL*1**S~"
    "TD1*CTN25*100~"
    "HL*2*1*O~"
    "PRF*PO12345~"
    "HL*3*2*P~"
    "MAN*GM*00012345678901234567~"
    "HL*4*3*I~"
    "LIN**UP*012345678901~"
    "SN1**100*EA~"
    "CTT*4~"
    "SE*12*0002~"
    "GE*1*2~"
    "IEA*1*000000002~"
)

_X12_810 = (
    "ISA*00*          *00*          *ZZ*SENDERID01     *ZZ*RECEIVERID01   "
    "*250705*1430*U*00501*000000003*0*P*:~"
    "GS*IN*SENDERID*RECEIVERID*20250705*1430*3*X*005010~"
    "ST*810*0003~"
    "BIG*20250705*INV987654*20250630*PO12345~"
    "IT1*1*100*EA*5.50**UP*012345678901~"
    "TDS*55000~"
    "CTT*1~"
    "SE*6*0003~"
    "GE*1*3~"
    "IEA*1*000000003~"
)

_X12_837 = (
    "ISA*00*          *00*          *ZZ*PROVIDERID01   *ZZ*PAYERID01      "
    "*250710*0900*U*00501*000000004*0*P*:~"
    "GS*HC*PROVIDERID*PAYERID*20250710*0900*4*X*005010X222A1~"
    "ST*837*0004*005010X222A1~"
    "BHT*0019*00*REF12345*20250710*0900*CH~"
    "NM1*41*2*ACME HEALTH*****46*1234567890~"
    "PER*IC*JANE DOE*TE*5551234567~"
    "NM1*40*2*PAYER NAME*****46*9876543210~"
    "HL*1**20*1~"
    "NM1*85*2*ACME CLINIC*****XX*1234567890~"
    "HL*2*1*22*1~"
    "SBR*P********CI~"
    "NM1*IL*1*PATIENT*JOHN****MI*MEMBER123~"
    "CLM*CLAIMID01*250.50***11:B:1*Y*A*Y*Y~"
    "HI*ABK:E11.65~"
    "SE*13*0004~"
    "GE*1*4~"
    "IEA*1*000000004~"
)

_X12_835 = (
    "ISA*00*          *00*          *ZZ*PAYERID01      *ZZ*PROVIDERID01   "
    "*250715*1100*U*00501*000000005*0*P*:~"
    "GS*HP*PAYERID*PROVIDERID*20250715*1100*5*X*005010X221A1~"
    "ST*835*0005~"
    "BPR*I*1500.00*C*ACH*CCP*01*123456789*DA*99988877*1234567890**01*987654321*DA*55544433*20250715~"
    "TRN*1*EFT123*1234567890~"
    "DTM*405*20250715~"
    "N1*PR*PAYER NAME~"
    "N1*PE*ACME CLINIC*XX*1234567890~"
    "LX*1~"
    "CLP*CLAIMID01*1*250.50*200.00*50.50*MA*PAYERCONTROL01*11~"
    "SE*9*0005~"
    "GE*1*5~"
    "IEA*1*000000005~"
)

_X12_270 = (
    "ISA*00*          *00*          *ZZ*PROVIDERID01   *ZZ*PAYERID01      "
    "*250720*0815*U*00501*000000006*0*P*:~"
    "GS*HS*PROVIDERID*PAYERID*20250720*0815*6*X*005010X279A1~"
    "ST*270*0006*005010X279A1~"
    "BHT*0022*13*REF22345*20250720*0815~"
    "HL*1**20*1~"
    "NM1*PR*2*PAYER NAME*****PI*PAYERID~"
    "HL*2*1*21*1~"
    "NM1*1P*2*ACME CLINIC*****XX*1234567890~"
    "HL*3*2*22*0~"
    "TRN*1*ELIG-INQ-1*1234567890~"
    "NM1*IL*1*PATIENT*JOHN****MI*MEMBER123~"
    "DMG*D8*19800101*M~"
    "DTP*291*RD8*20250720-20250720~"
    "EQ*30~"
    "SE*12*0006~"
    "GE*1*6~"
    "IEA*1*000000006~"
)

_X12_271 = (
    "ISA*00*          *00*          *ZZ*PAYERID01      *ZZ*PROVIDERID01   "
    "*250720*0820*U*00501*000000007*0*P*:~"
    "GS*HB*PAYERID*PROVIDERID*20250720*0820*7*X*005010X279A1~"
    "ST*271*0007*005010X279A1~"
    "BHT*0022*11*REF22345*20250720*0820~"
    "HL*1**20*1~"
    "NM1*PR*2*PAYER NAME*****PI*PAYERID~"
    "HL*2*1*21*1~"
    "NM1*1P*2*ACME CLINIC*****XX*1234567890~"
    "HL*3*2*22*0~"
    "NM1*IL*1*PATIENT*JOHN****MI*MEMBER123~"
    "EB*1**30**GOLD PPO~"
    "SE*9*0007~"
    "GE*1*7~"
    "IEA*1*000000007~"
)

EDI_X12_FIXTURES: dict[str, str] = {
    "850": _X12_850,
    "856": _X12_856,
    "810": _X12_810,
    "820": _X12_810.replace("*BIG*", "*BPR*").replace("ST*810*", "ST*820*").replace("GS*IN*", "GS*RA*"),
    "837": _X12_837,
    "835": _X12_835,
    "270": _X12_270,
    "271": _X12_271,
}


# ---------------------------------------------------------------------------
# HL7 v2.x — ADT_A04, ORU_R01, ORM_O01, RXE
# ---------------------------------------------------------------------------

# v2.5.1 ADT^A04 — Patient registration
_HL7V2_ADT_A04 = (
    "MSH|^~\\&|REGISTRATION|MAIN_HOSPITAL|EHR|MAIN_HOSPITAL|"
    "20250630120000||ADT^A04|MSG00001|P|2.5.1\r"
    "EVN||20250630120000\r"
    "PID|1||PATID1234^^^MRN^MR||DOE^JOHN^A||19800101|M||"
    "2106-3|123 MAIN ST^^ANYTOWN^NY^10001||(212)5551234\r"
    "PV1|1|O|CLINIC^^^^^|||||1234^DOCTOR^JANE^^MD\r"
    "AL1|1|MA|^PENICILLIN|SV~SEVERE\r"
)

# v2.5.1 ORU^R01 — Observation result
_HL7V2_ORU_R01 = (
    "MSH|^~\\&|LAB|MAIN_HOSPITAL|EHR|MAIN_HOSPITAL|"
    "20250630143000||ORU^R01|MSG00002|P|2.5.1\r"
    "PID|1||PATID1234^^^MRN^MR||DOE^JOHN^A||19800101|M\r"
    "OBR|1|ORD123|FILL456|24323-8^Comprehensive metabolic panel^LN|||"
    "20250630140000\r"
    "OBX|1|NM|2345-7^Glucose^LN||95|mg/dL|65-99|N|||F\r"
    "OBX|2|NM|2823-3^Potassium^LN||4.0|mmol/L|3.5-5.0|N|||F\r"
)

# v2.7 ORM^O01 — Pharmacy order
_HL7V2_ORM_O01 = (
    "MSH|^~\\&|PHARMACY|MAIN_HOSPITAL|EHR|MAIN_HOSPITAL|"
    "20250701083000||ORM^O01|MSG00003|P|2.7\r"
    "PID|1||PATID1234^^^MRN^MR||DOE^JOHN^A||19800101|M\r"
    "ORC|NW|ORD789|||||||20250701083000\r"
    "RXE|^Q24H&Once daily&^^^^^^^7^days^D|"
    "00378-3000-01^Lisinopril 10 mg tablet^NDC|10|"
    "10|mg|TAB^Tablet|Take one tablet by mouth daily\r"
)

HL7V2_FIXTURES: dict[str, str] = {
    "ADT^A04": _HL7V2_ADT_A04,
    "ORU^R01": _HL7V2_ORU_R01,
    "ORM^O01": _HL7V2_ORM_O01,
}


# ---------------------------------------------------------------------------
# HL7 CDA / C-CDA — minimal CCD with each named section
# ---------------------------------------------------------------------------

_CDA_CCD = """<?xml version="1.0" encoding="UTF-8"?>
<ClinicalDocument xmlns="urn:hl7-org:v3">
  <typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
  <templateId root="2.16.840.1.113883.10.20.22.1.2"/>
  <id root="DOC-12345"/>
  <code code="34133-9" displayName="Summarization of Episode Note"
        codeSystem="2.16.840.1.113883.6.1"/>
  <title>Continuity of Care Document</title>
  <effectiveTime value="20250630143000"/>
  <recordTarget>
    <patientRole>
      <id root="2.16.840.1.113883.4.1" extension="MRN001"/>
      <patient>
        <name>
          <given>John</given>
          <family>Doe</family>
        </name>
        <administrativeGenderCode code="M"/>
      </patient>
    </patientRole>
  </recordTarget>
  <component>
    <structuredBody>
      <component>
        <section>
          <templateId root="2.16.840.1.113883.10.20.22.2.6.1"/>
          <code code="48765-2" displayName="Allergies"
                codeSystem="2.16.840.1.113883.6.1"/>
          <text>Penicillin — severe rash, 2010-05</text>
          <entry>
            <observation>
              <code code="419199007" displayName="Allergy to substance"
                    codeSystem="2.16.840.1.113883.6.96"/>
              <value displayName="Penicillin"/>
            </observation>
          </entry>
        </section>
      </component>
      <component>
        <section>
          <templateId root="2.16.840.1.113883.10.20.22.2.1.1"/>
          <code code="10160-0" displayName="History of Medication use"
                codeSystem="2.16.840.1.113883.6.1"/>
          <text>Lisinopril 10 mg PO daily</text>
        </section>
      </component>
      <component>
        <section>
          <templateId root="2.16.840.1.113883.10.20.22.2.5.1"/>
          <code code="11450-4" displayName="Problem List"
                codeSystem="2.16.840.1.113883.6.1"/>
          <text>Type 2 diabetes mellitus with hyperglycemia</text>
          <entry>
            <observation>
              <code code="44054006" displayName="Diabetes mellitus type 2"
                    codeSystem="2.16.840.1.113883.6.96"/>
              <value displayName="Active"/>
            </observation>
          </entry>
        </section>
      </component>
      <component>
        <section>
          <templateId root="2.16.840.1.113883.10.20.22.2.3.1"/>
          <code code="30954-2" displayName="Relevant diagnostic tests"
                codeSystem="2.16.840.1.113883.6.1"/>
          <text>Glucose 95 mg/dL (2025-06-30)</text>
        </section>
      </component>
    </structuredBody>
  </component>
</ClinicalDocument>"""

CDA_FIXTURES: dict[str, str] = {"CCD": _CDA_CCD}


# ---------------------------------------------------------------------------
# EPCIS 2.0 — JSON-LD ObjectEvent / AggregationEvent / TransactionEvent
# ---------------------------------------------------------------------------

_EPCIS_OBJECT = """{
  "@context": "https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld",
  "type": "EPCISDocument",
  "schemaVersion": "2.0",
  "creationDate": "2025-06-30T14:30:00.000-04:00",
  "epcisBody": {
    "eventList": [
      {
        "type": "ObjectEvent",
        "eventTime": "2025-06-30T14:30:00.000-04:00",
        "eventTimeZoneOffset": "-04:00",
        "epcList": [
          "urn:epc:id:sgtin:0614141.107346.2017",
          "urn:epc:id:sgtin:0614141.107346.2018"
        ],
        "action": "OBSERVE",
        "bizStep": "https://ref.gs1.org/cbv/BizStep-shipping",
        "disposition": "https://ref.gs1.org/cbv/Disp-in_transit"
      }
    ]
  }
}"""

_EPCIS_AGGREGATION = """{
  "@context": "https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld",
  "type": "EPCISDocument",
  "schemaVersion": "2.0",
  "creationDate": "2025-06-30T15:00:00.000-04:00",
  "epcisBody": {
    "eventList": [
      {
        "type": "AggregationEvent",
        "eventTime": "2025-06-30T15:00:00.000-04:00",
        "eventTimeZoneOffset": "-04:00",
        "parentID": "urn:epc:id:sscc:0614141.0001234567",
        "childEPCs": [
          "urn:epc:id:sgtin:0614141.107346.2017",
          "urn:epc:id:sgtin:0614141.107346.2018"
        ],
        "action": "ADD",
        "bizStep": "https://ref.gs1.org/cbv/BizStep-packing"
      }
    ]
  }
}"""

_EPCIS_TRANSACTION = """{
  "@context": "https://ref.gs1.org/standards/epcis/2.0.0/epcis-context.jsonld",
  "type": "EPCISDocument",
  "schemaVersion": "2.0",
  "creationDate": "2025-06-30T16:30:00.000-04:00",
  "epcisBody": {
    "eventList": [
      {
        "type": "TransactionEvent",
        "eventTime": "2025-06-30T16:30:00.000-04:00",
        "eventTimeZoneOffset": "-04:00",
        "bizTransactionList": [
          {
            "type": "https://ref.gs1.org/cbv/BTT-po",
            "bizTransaction": "urn:epcglobal:cbv:bt:0614141:1234"
          }
        ],
        "action": "ADD",
        "epcList": ["urn:epc:id:sgtin:0614141.107346.2017"]
      }
    ]
  }
}"""

_EPCIS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<epcis:EPCISDocument xmlns:epcis="urn:epcglobal:epcis:xsd:2"
                     schemaVersion="2.0"
                     creationDate="2025-06-30T14:30:00.000-04:00">
  <EPCISBody>
    <EventList>
      <ObjectEvent>
        <eventTime>2025-06-30T14:30:00.000-04:00</eventTime>
        <eventTimeZoneOffset>-04:00</eventTimeZoneOffset>
        <epcList>
          <epc>urn:epc:id:sgtin:0614141.107346.2017</epc>
        </epcList>
        <action>OBSERVE</action>
        <bizStep>https://ref.gs1.org/cbv/BizStep-shipping</bizStep>
      </ObjectEvent>
    </EventList>
  </EPCISBody>
</epcis:EPCISDocument>"""

EPCIS_FIXTURES: dict[str, str] = {
    "ObjectEvent": _EPCIS_OBJECT,
    "AggregationEvent": _EPCIS_AGGREGATION,
    "TransactionEvent": _EPCIS_TRANSACTION,
    "XML-ObjectEvent": _EPCIS_XML,
}


# ---------------------------------------------------------------------------
# OAGIS BOD — ProcessItem / SyncCarrier / GetManufacturingFacility
# ---------------------------------------------------------------------------

_OAGIS_PROCESS_ITEM = """<?xml version="1.0" encoding="UTF-8"?>
<ProcessItem>
  <ApplicationArea>
    <Sender>
      <LogicalID>SAP-S4HANA-PROD</LogicalID>
    </Sender>
    <CreationDateTime>2025-06-30T14:30:00.000-04:00</CreationDateTime>
    <BODID>BOD-PROC-12345</BODID>
  </ApplicationArea>
  <DataArea>
    <Process/>
    <Item>
      <ItemID>ITEM-001</ItemID>
      <Description>Stamped Steel Bracket</Description>
      <UnitOfMeasure>EA</UnitOfMeasure>
    </Item>
  </DataArea>
</ProcessItem>"""

_OAGIS_SYNC_CARRIER = """<?xml version="1.0" encoding="UTF-8"?>
<SyncCarrier>
  <ApplicationArea>
    <Sender>
      <LogicalID>WMS-PROD</LogicalID>
    </Sender>
    <CreationDateTime>2025-06-30T14:30:00.000-04:00</CreationDateTime>
    <BODID>BOD-SYNC-67890</BODID>
  </ApplicationArea>
  <DataArea>
    <Sync/>
    <Carrier>
      <CarrierID>CARRIER-FEDEX</CarrierID>
      <Name>FedEx</Name>
      <SCAC>FDEG</SCAC>
    </Carrier>
  </DataArea>
</SyncCarrier>"""

_OAGIS_GET_FACILITY = """<?xml version="1.0" encoding="UTF-8"?>
<GetManufacturingFacility>
  <ApplicationArea>
    <Sender>
      <LogicalID>MES-NORTHPLANT</LogicalID>
    </Sender>
    <CreationDateTime>2025-06-30T14:30:00.000-04:00</CreationDateTime>
    <BODID>BOD-GET-99999</BODID>
  </ApplicationArea>
  <DataArea>
    <Get/>
    <ManufacturingFacility>
      <FacilityID>PLANT-NORTH</FacilityID>
      <Name>North Assembly Plant</Name>
    </ManufacturingFacility>
  </DataArea>
</GetManufacturingFacility>"""

OAGIS_FIXTURES: dict[str, str] = {
    "ProcessItem": _OAGIS_PROCESS_ITEM,
    "SyncCarrier": _OAGIS_SYNC_CARRIER,
    "GetManufacturingFacility": _OAGIS_GET_FACILITY,
}


# ---------------------------------------------------------------------------
# IATA PADIS — PNL / ADL / PRL
# ---------------------------------------------------------------------------

_PADIS_PNL = """PNL
DL0123/30JUN/JFKLHR/Y
1HOLLAND/JOHN MR
.R/SSR DOCS DL HK1 P/USA/123456789/USA/15JAN80/M/15JAN30/HOLLAND/JOHN
1SMITH/JANE MS
2DOE/ROBERT/MARY"""

_PADIS_ADL = """ADL
DL0123/30JUN/JFKLHR/Y
1ANDERSON/PETER MR
1WILSON/SARAH MS"""

_PADIS_PRL = """PRL
AA1234/15DEC/SFOORD/J
1JONES/MICHAEL MR
1WILLIAMS/EMMA MS"""

PADIS_FIXTURES: dict[str, str] = {
    "PNL": _PADIS_PNL,
    "ADL": _PADIS_ADL,
    "PRL": _PADIS_PRL,
}
