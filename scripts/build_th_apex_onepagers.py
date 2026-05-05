"""Build APEX Agentic AI OnePager HTML for every Travel-Hospitality client.

For each of the 15 T&H clients (Airlines / Hospitality-Leisure / Logistics-Mobility),
emit `<Client>_APEX_OnePager.html` into `01_account/one_pager/`.

Each one-pager:
  - Models on Nike_OnePager.html visual structure (1440px landscape, 3-col grid,
    Chart.js, modals, Deloitte branding)
  - Replaces the Microsoft Platform pipeline with APEX Agentic AI Services pipeline:
    scenarios from the APEX scenario catalog mapped to the client's functional area
    (back-office · operations · frontline)
  - Charts focus on: Scenario value by functional area, Agent fleet distribution,
    KPI uplift chain, Maturation timeline (W1->W4+)
  - WEDGE/NEW/EXPANSION strategy tags retained
  - Modal popups for top scenarios + key contacts

Output: <client>/01_account/one_pager/<Client>_APEX_OnePager.html
"""
from __future__ import annotations
import io, sys, html
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

TH_ROOT = Path(r"C:\Stage\Clients\Industries\Travel-Hospitality")

# ---------------------------------------------------------------------------
# Service catalog (from APEX-Scenario-Chains.xlsx)
# ---------------------------------------------------------------------------
SERVICE_NAMES = {
    "TH-AIR-02": "Airline Operations & Customer",
    "TH-AIR-04": "Baggage Operations",
    "TH-AIR-06": "Fleet & Crew Operations",
    "TH-HOT-03": "Hotel Revenue & Operations",
    "TH-HOT-05": "Guest Experience & Sentiment",
    "RC-E2E-03": "Assortment & Pricing",
    "RC-E2E-04": "Customer Loyalty & Marketing",
    "RC-E2E-05": "Store / Front-of-House Ops",
    "RC-E2E-06": "Supply Chain & Logistics",
    "RC-E2E-07": "Loss Prevention & Fraud",
    "RC-E2E-08": "Workforce Intelligence",
    "RC-E2E-09": "Perishables & Waste",
    "AXLE-Connected-Factory-01": "Connected Asset · Predictive Maintenance",
    "AXLE-Supply-04": "Supply Chain Resilience",
    "ICE-Aftermarket-01": "Distribution & Service Operations",
    "ICE-Connected-06": "Connected Products · Fleet Telematics",
}

# Functional area buckets that map to service codes (T&H tilt)
FUNCTIONAL_AREA = {
    "TH-AIR-02": "Operations · Airline Network",
    "TH-AIR-04": "Frontline · Baggage",
    "TH-AIR-06": "Operations · Fleet & Crew",
    "TH-HOT-03": "Operations · Revenue & Property",
    "TH-HOT-05": "Frontline · Guest Experience",
    "RC-E2E-03": "Back-Office · Pricing & Yield",
    "RC-E2E-04": "Frontline · Customer & Loyalty",
    "RC-E2E-05": "Frontline · FOH / Drive-Thru",
    "RC-E2E-06": "Operations · Supply Chain",
    "RC-E2E-07": "Operations · Risk & Fraud",
    "RC-E2E-08": "Back-Office · Workforce",
    "RC-E2E-09": "Operations · Food & Waste",
    "AXLE-Connected-Factory-01": "Operations · Asset Reliability",
    "AXLE-Supply-04": "Operations · Supply Resilience",
    "ICE-Aftermarket-01": "Operations · Distribution & Service",
    "ICE-Connected-06": "Operations · Telematics & Fleet",
}

# ---------------------------------------------------------------------------
# Client catalog · 15 Travel-Hospitality clients with APEX scenario alignment
# Public-domain facts (revenue, employees, HQ) from FY24/FY25 annual reports.
# ---------------------------------------------------------------------------

CLIENTS = []

# ===== AIRLINES (4) =====

CLIENTS.append({
    "ticker":"AAL","name_short":"American Airlines","name_long":"American Airlines Group, Inc.",
    "segment":"Airlines","sub_path":"Airlines","folder":"American_Airlines",
    "hq":"Fort Worth, TX · NASDAQ: AAL","revenue":"$54.2B","employees":"~133,000",
    "metric3":"~6,800","metric3_lbl":"Daily Flights","metric4":"~960",
    "metric4_lbl":"Aircraft","metric5":"$10B","metric5_lbl":"Market Cap",
    "metric6":"~120M","metric6_lbl":"AAdvantage Members",
    "primary_cloud":"Azure (IBM partnership)","erp":"SAP S/4HANA · Sabre PSS","brand_color":"#0078D2",
    "priorities":[
        ("Reliability & On-Time","Operational integrity recovery · IROPS containment"),
        ("AAdvantage Loyalty","#1 program · partner cards · co-brand expansion"),
        ("Fleet Modernization","787s · Airbus narrowbody renewal · cargo"),
        ("Premium Cabin Mix","Flagship · revenue per ASM · upgrade monetization"),
    ],
    "contacts":[
        ("Robert Isom","CEO"),
        ("Devon May","EVP & CFO"),
        ("Ganesh Jayaram","SVP & Chief Digital & Information Officer"),
        ("David Seymour","COO"),
        ("Heather Garboden","Chief Customer Officer"),
    ],
    "scenarios":[
        ("TH-AIR-02","Irregular-ops recovery & rebooking agent","-22% IROPS cost",2.5,5.0,"Q1–Q2",30,"wedge"),
        ("TH-AIR-06","Crew rostering & fatigue-risk management","-14% reserve usage",2.0,4.0,"Q2",20,"new"),
        ("RC-E2E-04","AAdvantage personalization at 120M scale","+18% LTV",1.5,3.0,"Q2–Q3",20,"new"),
        ("AXLE-Connected-Factory-01","Engine MRO predictive maintenance","-18% AOG hours",1.2,2.5,"Q3",15,"new"),
        ("TH-AIR-04","Baggage mishandling reduction","-28% mishandle/1K",0.8,1.6,"Q3",10,"new"),
        ("RC-E2E-08","Pilot / cabin-crew workforce analytics","-12% overtime",0.6,1.4,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"DAL","name_short":"Delta Air Lines","name_long":"Delta Air Lines, Inc.",
    "segment":"Airlines","sub_path":"Airlines","folder":"Delta_Air_Lines",
    "hq":"Atlanta, GA · NYSE: DAL","revenue":"$61.6B","employees":"~100,000",
    "metric3":"~5,400","metric3_lbl":"Daily Flights","metric4":"~970",
    "metric4_lbl":"Aircraft","metric5":"$36B","metric5_lbl":"Market Cap",
    "metric6":"~120M","metric6_lbl":"SkyMiles Members",
    "primary_cloud":"AWS (strategic) + Azure","erp":"Oracle EBS · Deltamatic ops · SAP HCM","brand_color":"#003366",
    "priorities":[
        ("Premium Strategy","Premium revenue >57% · Delta One · Comfort+"),
        ("Loyalty Economics","SkyMiles · Amex co-brand $7B+ remuneration"),
        ("Operational Integrity","#1 on-time · A350/A330neo widebody renewal"),
        ("Sustainable Aviation","SAF · fleet renewal · carbon roadmap"),
    ],
    "contacts":[
        ("Ed Bastian","CEO"),
        ("Dan Janki","EVP & CFO"),
        ("Rahul Samant","EVP & Chief Information Officer"),
        ("Allison Ausband","EVP & Chief Customer Experience Officer"),
        ("Glen Hauenstein","President"),
    ],
    "scenarios":[
        ("TH-AIR-02","Network-disruption recovery (weather + ATC)","-24% IROPS cost",3.0,6.0,"Q1–Q2",30,"wedge"),
        ("RC-E2E-04","SkyMiles personalization · premium upsell","+22% upsell",2.0,4.0,"Q2",25,"new"),
        ("TH-AIR-06","Crew tracking · trip-pairing optimization","-12% pairing cost",1.5,3.0,"Q2–Q3",20,"new"),
        ("AXLE-Connected-Factory-01","Delta TechOps · engine predictive maintenance","-20% AOG hours",1.5,3.0,"Q3",15,"new"),
        ("TH-AIR-04","Baggage tracking & mishandling reduction","-32% mishandle/1K",0.8,1.6,"Q3",10,"new"),
        ("RC-E2E-08","Workforce analytics · ground & maintenance","-14% overtime",0.6,1.4,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"LUV","name_short":"Southwest Airlines","name_long":"Southwest Airlines Co.",
    "segment":"Airlines","sub_path":"Airlines","folder":"Southwest_Airlines",
    "hq":"Dallas, TX · NYSE: LUV","revenue":"$27.5B","employees":"~75,000",
    "metric3":"~4,000","metric3_lbl":"Daily Flights","metric4":"~820",
    "metric4_lbl":"Aircraft (737 fleet)","metric5":"$20B","metric5_lbl":"Market Cap",
    "metric6":"~38M","metric6_lbl":"Rapid Rewards Members",
    "primary_cloud":"Azure (Microsoft partnership)","erp":"SAP S/4HANA migration · GE Digital ops","brand_color":"#304CB2",
    "priorities":[
        ("Operational Resilience","Post-Dec 2022 IT modernization · crew-tracking lift"),
        ("Network Transformation","Assigned seating · premium · red-eye capacity"),
        ("Cost Discipline","Elliott pressure · CASM-X reduction · efficiency"),
        ("Loyalty & Bag Fees","First checked-bag policy change · ancillary uplift"),
    ],
    "contacts":[
        ("Bob Jordan","President & CEO"),
        ("Tammy Romo","EVP & CFO"),
        ("Lauren Woods","EVP & Chief Information Officer"),
        ("Andrew Watterson","COO"),
        ("Ryan Green","EVP Commercial Transformation"),
    ],
    "scenarios":[
        ("TH-AIR-02","Point-to-point operations recovery","-26% IROPS cost",2.0,4.0,"Q1–Q2",30,"wedge"),
        ("TH-AIR-06","Crew-tracking & compliance (post-2022)","-18% reserve usage",1.8,3.5,"Q2",25,"new"),
        ("RC-E2E-04","Rapid Rewards personalization & bag-policy mix","+14% ancillary",1.5,3.0,"Q2–Q3",20,"new"),
        ("RC-E2E-08","Ground-ops workforce analytics","-12% overtime",1.0,2.0,"Q3",15,"new"),
        ("TH-AIR-04","Baggage handling for new bag-fee economics","-22% mishandle/1K",0.7,1.4,"Q3",10,"new"),
        ("AXLE-Supply-04","737 supplier-disruption mitigation (Boeing risk)","-16% disruption",0.6,1.2,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"UAL","name_short":"United Airlines","name_long":"United Airlines Holdings, Inc.",
    "segment":"Airlines","sub_path":"Airlines","folder":"United_Airlines",
    "hq":"Chicago, IL · NASDAQ: UAL","revenue":"$57.0B","employees":"~110,000",
    "metric3":"~4,800","metric3_lbl":"Daily Flights","metric4":"~1,000",
    "metric4_lbl":"Aircraft","metric5":"$32B","metric5_lbl":"Market Cap",
    "metric6":"~115M","metric6_lbl":"MileagePlus Members",
    "primary_cloud":"AWS + Azure (hybrid)","erp":"SAP S/4HANA · Sabre PSS","brand_color":"#002244",
    "priorities":[
        ("United Next","Largest fleet plan in US aviation history"),
        ("Premium Cabin Growth","Polaris · Premium Plus · domestic premium"),
        ("Hub Reinforcement","Newark · ORD · DEN · IAH · SFO · IAD"),
        ("Loyalty Monetization","MileagePlus · Chase co-brand · partner expansion"),
    ],
    "contacts":[
        ("Scott Kirby","CEO"),
        ("Mike Leskinen","EVP & CFO"),
        ("Jason Birnbaum","EVP & Chief Information Officer"),
        ("Toby Enqvist","COO"),
        ("Linda Jojo","EVP & Chief Customer Officer"),
    ],
    "scenarios":[
        ("TH-AIR-02","Hub-recovery orchestration · weather IROPS","-22% IROPS cost",2.5,5.0,"Q1–Q2",30,"wedge"),
        ("RC-E2E-04","MileagePlus personalization · premium upsell","+18% upsell",2.0,4.0,"Q2",25,"new"),
        ("TH-AIR-06","Crew tracking · Boeing/Airbus mixed fleet","-14% pairing cost",1.5,3.0,"Q2–Q3",20,"new"),
        ("AXLE-Connected-Factory-01","737 MAX / 787 predictive maintenance","-18% AOG hours",1.2,2.5,"Q3",15,"new"),
        ("TH-AIR-04","Baggage operations across 8 hubs","-28% mishandle/1K",0.8,1.6,"Q3",10,"new"),
        ("RC-E2E-08","Pilot/CA workforce analytics","-12% overtime",0.6,1.4,"Q3–Q4",10,"expansion"),
    ],
})

# ===== HOSPITALITY-LEISURE (6) =====

CLIENTS.append({
    "ticker":"EXPE","name_short":"Expedia","name_long":"Expedia Group, Inc.",
    "segment":"Hospitality","sub_path":"Hospitality-Leisure","folder":"Expedia",
    "hq":"Seattle, WA · NASDAQ: EXPE","revenue":"$13.7B","employees":"~16,500",
    "metric3":"~3M","metric3_lbl":"Properties","metric4":"~600M",
    "metric4_lbl":"Monthly Visits","metric5":"$23B","metric5_lbl":"Market Cap",
    "metric6":"~30M","metric6_lbl":"One Key Members",
    "primary_cloud":"AWS","erp":"Oracle · Workday · custom OTA platform","brand_color":"#191E3B",
    "priorities":[
        ("One Key Loyalty","Multi-brand (Expedia · Hotels.com · Vrbo) loyalty merger"),
        ("B2B Travel","Expedia Group B2B · TAAP · platform-as-a-service"),
        ("AI-Powered Trip Planning","Romie · ChatGPT plug-in · travel agent GenAI"),
        ("Vrbo Recovery","Vacation rental supply · post-rebrand growth"),
    ],
    "contacts":[
        ("Ariane Gorin","CEO"),
        ("Scott Schenkel","CFO"),
        ("Rathi Murthy","CTO & President, Product & Technology"),
        ("Jon Gieselman","President, Expedia Brands"),
    ],
    "scenarios":[
        ("RC-E2E-04","One Key cross-brand personalization","+22% LTV",2.0,4.0,"Q1–Q2",30,"wedge"),
        ("TH-HOT-03","Lodging revenue & dynamic pricing for hotelier partners","+1.6pp take-rate",1.8,3.5,"Q2",25,"new"),
        ("TH-HOT-05","Trip-sentiment intervention agent","+12pp NPS",1.2,2.5,"Q2–Q3",20,"new"),
        ("RC-E2E-07","Marketplace fraud / chargeback detection","+$18M/yr",1.0,2.0,"Q3",15,"new"),
        ("RC-E2E-06","Lodging supplier-network optimization","+14% conv",0.7,1.4,"Q3",10,"new"),
        ("RC-E2E-08","Customer-service agent assist (deflection)","-22% AHT",0.5,1.2,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"MAR","name_short":"Marriott","name_long":"Marriott International, Inc.",
    "segment":"Hospitality","sub_path":"Hospitality-Leisure","folder":"Marriott_International",
    "hq":"Bethesda, MD · NASDAQ: MAR","revenue":"$25.1B","employees":"~411,000 (system)",
    "metric3":"~9,400","metric3_lbl":"Properties","metric4":"30+",
    "metric4_lbl":"Brands","metric5":"$78B","metric5_lbl":"Market Cap",
    "metric6":"~228M","metric6_lbl":"Bonvoy Members",
    "primary_cloud":"Azure (strategic Microsoft partnership)","erp":"Oracle Hospitality · Workday · MGS migration","brand_color":"#A41E22",
    "priorities":[
        ("Bonvoy Personalization","228M+ members · GenAI concierge · partner ecosystem"),
        ("Asset-Light Growth","Net-rooms growth · luxury · midscale (City Express)"),
        ("Direct Channel Mix","Bonvoy direct · OTA dependency reduction"),
        ("Tech Modernization","Distribution platform · Marriott Global System (MGS)"),
    ],
    "contacts":[
        ("Anthony Capuano","President & CEO"),
        ("Leeny Oberg","CFO & EVP Development"),
        ("Naveen Manga","CTO"),
        ("Drew Pinto","Chief Revenue & Technology Officer"),
        ("Peggy Roe","Chief Customer Officer"),
    ],
    "scenarios":[
        ("RC-E2E-04","Bonvoy personalization at 228M scale","+24% LTV",3.0,6.0,"Q1–Q2",35,"wedge"),
        ("TH-HOT-03","Property-level revenue management at 9,400 hotels","+1.7pp RevPAR",2.5,5.0,"Q2",25,"new"),
        ("TH-HOT-05","Guest-sentiment intervention & service recovery","+14pp NPS",1.5,3.0,"Q2–Q3",20,"new"),
        ("RC-E2E-06","Group/transient demand optimization","+12% group conv",1.2,2.5,"Q3",15,"new"),
        ("RC-E2E-08","Property workforce optimization (housekeeping)","-14% labor",0.8,1.6,"Q3",10,"new"),
        ("RC-E2E-07","Loyalty / payments fraud detection","+$22M/yr",0.6,1.4,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"VAC","name_short":"Marriott Vacations","name_long":"Marriott Vacations Worldwide",
    "segment":"Hospitality","sub_path":"Hospitality-Leisure","folder":"Marriott_Vacations",
    "hq":"Orlando, FL · NYSE: VAC","revenue":"$4.9B","employees":"~22,000",
    "metric3":"~120","metric3_lbl":"Resorts","metric4":"~700K",
    "metric4_lbl":"Owner Families","metric5":"$2.3B","metric5_lbl":"Market Cap",
    "metric6":"3","metric6_lbl":"Brand Portfolios",
    "primary_cloud":"Azure (Marriott alignment)","erp":"Oracle · Workday · custom timeshare platform","brand_color":"#86754C",
    "priorities":[
        ("Owner Lifecycle","Tour conversion · upgrades · used-week resale"),
        ("Bonvoy Integration","Marriott Vacation Club + Bonvoy member economics"),
        ("Capital Discipline","Vistana acquisition synergies · cost-out program"),
        ("Resort Operations","Property-level NPS · service-recovery uplift"),
    ],
    "contacts":[
        ("John Geller","President & CEO"),
        ("Jason Marino","CFO"),
        ("Lori Gustafson","EVP & Chief Brand & Digital Officer"),
        ("David Babich","EVP, MVCV - North America"),
    ],
    "scenarios":[
        ("RC-E2E-04","Owner lifetime-value & tour-conversion agent","+20% LTV",1.5,3.0,"Q1–Q2",25,"wedge"),
        ("TH-HOT-03","Resort yield management · 120 resorts","+1.7pp RevPAR",1.2,2.5,"Q2",20,"new"),
        ("TH-HOT-05","Owner & guest sentiment intervention","+12pp NPS",1.0,2.0,"Q2–Q3",15,"new"),
        ("RC-E2E-08","Resort-property workforce optimization","-12% labor",0.7,1.4,"Q3",10,"new"),
        ("RC-E2E-06","Procurement & resort-supply optimization","-10% spend",0.6,1.2,"Q3",10,"new"),
        ("RC-E2E-07","Timeshare contract / payment fraud detection","+$5M/yr",0.4,1.0,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"MCD","name_short":"McDonald's","name_long":"McDonald's Corporation",
    "segment":"Hospitality","sub_path":"Hospitality-Leisure","folder":"McDonalds",
    "hq":"Chicago, IL · NYSE: MCD","revenue":"$25.5B","employees":"~150,000 (corp)",
    "metric3":"~43,000","metric3_lbl":"Restaurants","metric4":"~150M",
    "metric4_lbl":"MyMcD Members","metric5":"$220B","metric5_lbl":"Market Cap",
    "metric6":"100+","metric6_lbl":"Countries",
    "primary_cloud":"GCP (strategic) + Azure","erp":"SAP S/4HANA · Salesforce · custom POS","brand_color":"#FFC72C",
    "priorities":[
        ("Accelerating the Arches","Marketing · McDelivery · McCafe · Core menu"),
        ("MyMcDonald's Rewards","150M+ members · digital revenue >40%"),
        ("AI Drive-Thru","IBM partnership reset · GCP voice · OpenAI menu personalization"),
        ("Restaurant Productivity","Crew labor · food cost · DSP integration"),
    ],
    "contacts":[
        ("Chris Kempczinski","CEO"),
        ("Ian Borden","CFO"),
        ("Brian Rice","EVP & Global Chief Information Officer"),
        ("Manu Steijaert","EVP & Global Chief Customer Officer"),
        ("Joe Erlinger","President, McDonald's USA"),
    ],
    "scenarios":[
        ("RC-E2E-04","MyMcD Rewards personalization at 150M scale","+20% LTV",3.0,6.0,"Q1–Q2",35,"wedge"),
        ("RC-E2E-09","Food-cost & crew-waste reduction","-26% waste",2.0,4.0,"Q2",25,"new"),
        ("RC-E2E-08","Restaurant labor scheduling at 43K stores","-14% overtime",1.5,3.0,"Q2–Q3",20,"new"),
        ("RC-E2E-03","Menu-engineering & price-architecture optimization","+1.4pp GM",1.2,2.5,"Q3",15,"new"),
        ("RC-E2E-05","Drive-thru order accuracy / FOH copilot","+10pp accuracy",1.0,2.0,"Q3",15,"new"),
        ("AXLE-Supply-04","Beef / chicken supplier-disruption mitigation","-14% disruption",0.7,1.4,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"RCL","name_short":"Royal Caribbean","name_long":"Royal Caribbean Group",
    "segment":"Hospitality","sub_path":"Hospitality-Leisure","folder":"Royal_Caribbean",
    "hq":"Miami, FL · NYSE: RCL","revenue":"$16.5B","employees":"~107,000 (incl. shipboard)",
    "metric3":"~70","metric3_lbl":"Ships","metric4":"~9M",
    "metric4_lbl":"Guests/Year","metric5":"$70B","metric5_lbl":"Market Cap",
    "metric6":"~500","metric6_lbl":"Destinations",
    "primary_cloud":"AWS","erp":"SAP S/4HANA · Workday · custom Vantage platform","brand_color":"#003F7F",
    "priorities":[
        ("Trifecta Program","2025 financial targets · ROIC · EBITDA per APCD"),
        ("Sea Beyond Personalization","On-ship experience · pre-cruise upsell"),
        ("Fleet Expansion","Icon Class · Star · Quantum · Celebrity · Silversea"),
        ("Private Destinations","Perfect Day at CocoCay · Nassau · Bahamas"),
    ],
    "contacts":[
        ("Jason Liberty","President & CEO"),
        ("Naftali Holtz","CFO"),
        ("Mike Schneider","SVP & CIO"),
        ("Mark Tamis","SVP, Hotel Operations"),
        ("Pat Volker","SVP, Revenue Management & Loyalty"),
    ],
    "scenarios":[
        ("RC-E2E-04","Crown & Anchor / Captain's Club cross-loyalty","+18% LTV",1.8,3.5,"Q1–Q2",30,"wedge"),
        ("TH-HOT-03","Cabin yield management · 70 ships","+1.8pp net yield",1.5,3.0,"Q2",25,"new"),
        ("TH-HOT-05","On-ship guest-sentiment & service recovery","+14pp NPS",1.2,2.5,"Q2–Q3",20,"new"),
        ("AXLE-Connected-Factory-01","Vessel predictive maintenance · IoT","-18% downtime",1.0,2.0,"Q3",15,"new"),
        ("RC-E2E-06","Provisioning & port-supply optimization","-12% spend",0.8,1.6,"Q3",10,"new"),
        ("RC-E2E-08","Shipboard crew workforce optimization","-12% overtime",0.5,1.2,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"YUM","name_short":"Yum! Brands","name_long":"Yum! Brands, Inc.",
    "segment":"Hospitality","sub_path":"Hospitality-Leisure","folder":"Yum_Brands",
    "hq":"Louisville, KY · NYSE: YUM","revenue":"$7.3B","employees":"~36,000 (corp)",
    "metric3":"~61,000","metric3_lbl":"Restaurants","metric4":"~155",
    "metric4_lbl":"Countries","metric5":"$38B","metric5_lbl":"Market Cap",
    "metric6":"4","metric6_lbl":"Brands (KFC/PH/TB/Habit)",
    "primary_cloud":"Azure (Microsoft strategic partnership)","erp":"SAP S/4HANA · Byte digital platform · Workday","brand_color":"#FFFFFF",
    "priorities":[
        ("Byte by Yum! Platform","Proprietary digital platform · 95K+ users (franchisees)"),
        ("Drive-Thru / Voice AI","Voice-AI rollout (Taco Bell · KFC) · order accuracy"),
        ("Loyalty Across Brands","Taco Bell Rewards · KFC · Pizza Hut · Habit"),
        ("Franchisee Productivity","Labor · food cost · supply-chain visibility"),
    ],
    "contacts":[
        ("David Gibbs","CEO"),
        ("Chris Turner","CFO & Co-COO"),
        ("Joe Park","Chief Digital & Technology Officer"),
        ("Sean Tresvant","CEO, Taco Bell"),
        ("Sabir Sami","CEO, KFC"),
    ],
    "scenarios":[
        ("RC-E2E-04","Cross-brand loyalty (Taco Bell/KFC/PH/Habit)","+18% LTV",2.0,4.0,"Q1–Q2",30,"wedge"),
        ("RC-E2E-09","Food-cost & crew-waste reduction","-22% waste",1.5,3.0,"Q2",20,"new"),
        ("RC-E2E-08","Labor scheduling at 61K restaurants","-12% overtime",1.2,2.5,"Q2–Q3",20,"new"),
        ("RC-E2E-03","Menu-engineering & franchisee pricing intelligence","+1.5pp GM",1.0,2.0,"Q3",15,"new"),
        ("AXLE-Supply-04","Chicken / cheese / produce supplier-risk","-16% disruption",0.8,1.6,"Q3",10,"new"),
        ("RC-E2E-05","Drive-thru / voice AI accuracy uplift","+10pp accuracy",0.6,1.4,"Q3–Q4",10,"expansion"),
    ],
})

# ===== LOGISTICS-MOBILITY (5) =====

CLIENTS.append({
    "ticker":"BGM","name_short":"Bristol Global","name_long":"Bristol Global Mobility",
    "segment":"Logistics","sub_path":"Logistics-Mobility","folder":"Bristol_Global_Mobility",
    "hq":"Phoenix, AZ · Privately held","revenue":"~$200M (est.)","employees":"~400",
    "metric3":"160+","metric3_lbl":"Countries Served","metric4":"~50K",
    "metric4_lbl":"Annual Relocations","metric5":"Family-led","metric5_lbl":"Status",
    "metric6":"3","metric6_lbl":"Decades in Mobility",
    "primary_cloud":"Azure (Microsoft partner)","erp":"Microsoft Dynamics 365 · custom MoveTrack","brand_color":"#0F4C81",
    "priorities":[
        ("Independent Differentiation","Wholly-owned · client-aligned · no-channel-conflict"),
        ("Technology Platform","MoveTrack · supplier marketplace · client portals"),
        ("Service-Excellence","Consultant model · 5-star NPS targets"),
        ("Global Expansion","Asia-Pacific · Latin America growth"),
    ],
    "contacts":[
        ("Diane Lewis","Founder & CEO"),
        ("(Operations Lead)","COO"),
        ("(Technology Lead)","CTO / Head of MoveTrack"),
        ("(Account Mgmt Lead)","Head of Global Account Management"),
    ],
    "scenarios":[
        ("RC-E2E-04","Assignee experience & sentiment-driven service","+18% NPS",0.6,1.2,"Q1–Q2",25,"wedge"),
        ("RC-E2E-08","Mobility-consultant case-load optimization","+22% case throughput",0.5,1.0,"Q2",20,"new"),
        ("ICE-Aftermarket-01","Supplier-marketplace optimization","-12% spend",0.4,0.9,"Q2–Q3",15,"new"),
        ("RC-E2E-06","End-to-end relocation orchestration","-10% lead time",0.3,0.7,"Q3",15,"new"),
        ("RC-E2E-07","Expense / vendor-fraud detection","+$2M/yr",0.2,0.5,"Q3",10,"new"),
        ("TH-HOT-05","Assignee in-flight sentiment intervention","+10pp NPS",0.2,0.4,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"FDX","name_short":"FedEx","name_long":"FedEx Corporation",
    "segment":"Logistics","sub_path":"Logistics-Mobility","folder":"FedEx_Corporation",
    "hq":"Memphis, TN · NYSE: FDX","revenue":"$87.7B","employees":"~500,000",
    "metric3":"~700","metric3_lbl":"Aircraft","metric4":"~220K",
    "metric4_lbl":"Vehicles","metric5":"$67B","metric5_lbl":"Market Cap",
    "metric6":"~16M","metric6_lbl":"Daily Shipments",
    "primary_cloud":"AWS (FedEx Dataworks) + Azure","erp":"Oracle EBS · custom routing · SAP","brand_color":"#4D148C",
    "priorities":[
        ("Network 2.0","Express + Ground network convergence"),
        ("DRIVE Cost Program","$4B+ permanent cost-out · operational efficiency"),
        ("FedEx Dataworks","Data-monetization · supply-chain insight platform"),
        ("Surround / fdx Platform","Customer-facing digital · supplier orchestration"),
    ],
    "contacts":[
        ("Raj Subramaniam","President & CEO"),
        ("John Dietrich","EVP & CFO"),
        ("Sriram Krishnasamy","CEO, FedEx Dataworks · CDIO"),
        ("Brie Carere","EVP & Chief Customer Officer"),
        ("Scott Harkins","SVP, Network Operations Planning"),
    ],
    "scenarios":[
        ("RC-E2E-06","Network 2.0 routing & load-plan optimization","+$200M run-rate",4.0,8.0,"Q1–Q2",35,"wedge"),
        ("AXLE-Supply-04","Shipper supplier-disruption visibility (Dataworks)","-16% disruption",2.5,5.0,"Q2",25,"new"),
        ("ICE-Connected-06","Fleet telematics · 220K vehicles","-12% fuel/idle",2.0,4.0,"Q2–Q3",20,"new"),
        ("AXLE-Connected-Factory-01","Sortation / hub predictive maintenance","-18% downtime",1.5,3.0,"Q3",15,"new"),
        ("RC-E2E-08","Hub & courier workforce optimization","-12% overtime",1.0,2.0,"Q3",10,"new"),
        ("RC-E2E-04","fdx / Surround customer-experience personalization","+14% LTV",0.8,1.6,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"HTZ","name_short":"Hertz","name_long":"Hertz Global Holdings, Inc.",
    "segment":"Logistics","sub_path":"Logistics-Mobility","folder":"Hertz",
    "hq":"Estero, FL · NASDAQ: HTZ","revenue":"$9.4B","employees":"~24,000",
    "metric3":"~10,400","metric3_lbl":"Locations","metric4":"~500K",
    "metric4_lbl":"Vehicles (peak)","metric5":"$1.2B","metric5_lbl":"Market Cap",
    "metric6":"3","metric6_lbl":"Brands (Hertz/Dollar/Thrifty)",
    "primary_cloud":"AWS","erp":"Oracle · custom rental management · SAP HCM","brand_color":"#FFD100",
    "priorities":[
        ("Fleet Reset","Post-EV writedown · ICE/EV mix rebalance · residual recovery"),
        ("Profitability Recovery","Pricing discipline · vehicle utilization · cost-out"),
        ("Hertz Gold Plus Rewards","Loyalty growth · digital booking · upsell"),
        ("Operational Modernization","Counter automation · fleet maintenance · damage detection"),
    ],
    "contacts":[
        ("Gil West","CEO"),
        ("Scott Haralson","CFO"),
        ("Tim Langley-Hawthorne","EVP & CIO"),
        ("Eileen Drury","SVP, Customer Experience"),
        ("Darren Arrington","EVP, Revenue Management"),
    ],
    "scenarios":[
        ("TH-HOT-03","Fleet revenue management & dynamic pricing","+1.8pp RPD",1.8,3.5,"Q1–Q2",30,"wedge"),
        ("AXLE-Connected-Factory-01","Vehicle telematics predictive maintenance","-18% downtime",1.5,3.0,"Q2",25,"new"),
        ("RC-E2E-04","Gold Plus Rewards personalization & upsell","+18% LTV",1.2,2.5,"Q2–Q3",20,"new"),
        ("RC-E2E-07","Damage / unreturned-vehicle / fraud detection","+$25M/yr",1.0,2.0,"Q3",15,"new"),
        ("RC-E2E-08","Counter & fleet workforce optimization","-12% overtime",0.7,1.4,"Q3",10,"new"),
        ("ICE-Aftermarket-01","Used-car remarketing & disposition","+$15M/yr",0.5,1.2,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"LYFT","name_short":"Lyft","name_long":"Lyft, Inc.",
    "segment":"Logistics","sub_path":"Logistics-Mobility","folder":"Lyft",
    "hq":"San Francisco, CA · NASDAQ: LYFT","revenue":"$5.8B","employees":"~3,000",
    "metric3":"~24M","metric3_lbl":"Active Riders","metric4":"~750K",
    "metric4_lbl":"Active Drivers","metric5":"$5.5B","metric5_lbl":"Market Cap",
    "metric6":"~830M","metric6_lbl":"Quarterly Rides",
    "primary_cloud":"AWS","erp":"Workday · Coupa · custom marketplace platform","brand_color":"#FF00BF",
    "priorities":[
        ("Profitability Inflection","First GAAP-profit year · capital-efficient growth"),
        ("Driver Supply","Earner experience · upfront fares · earnings transparency"),
        ("Rider Experience","Price Lock · Women+ Connect · Wait & Save"),
        ("Autonomous Partnerships","Mobileye · May Mobility · Marubeni · AV roadmap"),
    ],
    "contacts":[
        ("David Risher","CEO"),
        ("Erin Brewer","CFO"),
        ("Jason Vogel","Chief Product Officer"),
        ("Audrey Liu","EVP, Engineering"),
        ("Kristin Sverchek","President"),
    ],
    "scenarios":[
        ("RC-E2E-04","Rider personalization · Wait & Save · Price Lock","+16% retention",1.5,3.0,"Q1–Q2",30,"wedge"),
        ("RC-E2E-08","Driver-supply matching & incentive optimization","+12% utilization",1.2,2.5,"Q2",25,"new"),
        ("RC-E2E-07","Driver / rider fraud & abuse detection","+$15M/yr",1.0,2.0,"Q2–Q3",20,"new"),
        ("TH-HOT-05","Rider/driver sentiment & service recovery","+10pp NPS",0.8,1.6,"Q3",15,"new"),
        ("RC-E2E-03","Surge / dynamic-pricing intelligence","+1.4pp take-rate",0.7,1.4,"Q3",10,"new"),
        ("RC-E2E-06","Lyft Media · advertising load-balancing","+18% ad ROI",0.5,1.2,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"UBER","name_short":"Uber","name_long":"Uber Technologies, Inc.",
    "segment":"Logistics","sub_path":"Logistics-Mobility","folder":"Uber",
    "hq":"San Francisco, CA · NYSE: UBER","revenue":"$43.9B","employees":"~31,000",
    "metric3":"~161M","metric3_lbl":"Monthly Users","metric4":"~7.4M",
    "metric4_lbl":"Drivers/Couriers","metric5":"$152B","metric5_lbl":"Market Cap",
    "metric6":"3","metric6_lbl":"Segments (Mobility/Delivery/Freight)",
    "primary_cloud":"GCP + Oracle (multi-cloud)","erp":"Workday · Oracle Fusion · custom marketplace","brand_color":"#000000",
    "priorities":[
        ("Profitability & Free Cash Flow","First GAAP-profitable year · S&P 500 inclusion"),
        ("Uber One Cross-Vertical","Membership unifying Mobility + Delivery"),
        ("Autonomous Roadmap","Waymo · Wayve · Aurora · 14+ AV partners"),
        ("Advertising Business","Uber Ads · sponsored placements · CPG partners"),
    ],
    "contacts":[
        ("Dara Khosrowshahi","CEO"),
        ("Prashanth Mahendra-Rajah","CFO"),
        ("Sundeep Jain","Chief Product Officer"),
        ("Jill Hazelbaker","SVP, Marketing & Public Affairs"),
        ("Andrew Macdonald","SVP, Mobility & Business Operations"),
    ],
    "scenarios":[
        ("RC-E2E-04","Uber One cross-vertical loyalty (Mobility+Eats)","+22% LTV",3.5,7.0,"Q1–Q2",35,"wedge"),
        ("RC-E2E-03","Surge / dynamic-pricing intelligence","+1.6pp take-rate",2.5,5.0,"Q2",25,"new"),
        ("TH-HOT-05","Rider / courier / driver sentiment intervention","+14pp NPS",1.5,3.0,"Q2–Q3",20,"new"),
        ("RC-E2E-07","Account-takeover / fraud detection at scale","+$45M/yr",1.5,3.0,"Q3",15,"new"),
        ("RC-E2E-08","Driver / courier supply-side optimization","+10% utilization",1.0,2.0,"Q3",10,"new"),
        ("RC-E2E-06","Eats logistics · last-mile routing optimization","+12% courier eff",0.8,1.6,"Q3–Q4",10,"expansion"),
    ],
})


# ---------------------------------------------------------------------------
# HTML template (identical to Consumer build)
# ---------------------------------------------------------------------------

CSS = """
:root{--deloitte-green:#86BC25;--deloitte-dark:#0D2818;--accent-teal:#00A3A1;--accent-blue:#0076A8;--accent-navy:#012169;--bg-light:#F7F9FA;--text-primary:#1A1A2E;--text-secondary:#4A5568;--border:#E2E8F0;--white:#FFFFFF;--red-flag:#C53030;--amber:#D69E2E;--green-ok:#38A169;--apex-violet:#6648B0;--apex-gold:#E3B657;--apex-teal:#3DD9C4}
*{margin:0;padding:0;box-sizing:border-box}
@page{size:A4 landscape;margin:0}
body{font-family:'DM Sans',sans-serif;background:var(--white);color:var(--text-primary);width:1440px;margin:0 auto;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.header{display:flex;justify-content:space-between;align-items:center;padding:20px 36px 16px;border-bottom:3px solid var(--deloitte-green);background:linear-gradient(135deg,var(--deloitte-dark) 0%,#0a3620 50%,#0d4428 100%);color:var(--white)}
.header-left{display:flex;align-items:center;gap:20px}
.header-logo{font-family:'Outfit',sans-serif;font-weight:800;font-size:15px;letter-spacing:3px;text-transform:uppercase;color:var(--deloitte-green);border-right:2px solid rgba(134,188,37,.4);padding-right:20px}
.header-title h1{font-family:'Outfit',sans-serif;font-size:22px;font-weight:700;letter-spacing:-0.3px}
.header-title p{font-size:11px;opacity:0.7;margin-top:2px;letter-spacing:0.5px}
.header-right{text-align:right;display:flex;gap:16px;align-items:center}
.revenue-badge{background:linear-gradient(135deg,var(--deloitte-green),#6fa31e);color:var(--deloitte-dark);padding:10px 18px;border-radius:8px;text-align:center;line-height:1.2}
.revenue-badge .amount{font-family:'Outfit',sans-serif;font-size:22px;font-weight:800}
.revenue-badge .label{font-size:9px;font-weight:600;text-transform:uppercase;letter-spacing:1.5px}
.phase-badge{background:rgba(255,255,255,.08);border:1px solid rgba(134,188,37,.3);padding:8px 14px;border-radius:8px;text-align:center}
.phase-badge .label{font-size:8px;text-transform:uppercase;letter-spacing:1.5px;opacity:0.6;display:block}
.phase-badge .value{font-family:'Outfit',sans-serif;font-size:13px;font-weight:600;color:var(--deloitte-green)}
.apex-chip{background:linear-gradient(135deg,var(--apex-violet),#8466CC);color:#fff;padding:6px 12px;border-radius:6px;font-family:'Outfit',sans-serif;font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase}
.main{display:grid;grid-template-columns:310px 1fr 310px;gap:0;min-height:calc(100% - 130px)}
.col-left{padding:18px 20px;border-right:1px solid var(--border);background:var(--bg-light)}
.company-header{display:flex;align-items:center;gap:10px;margin-bottom:14px}
.company-icon{width:42px;height:42px;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#fff;font-family:'Outfit';font-weight:800;font-size:13px}
.company-header .info h3{font-family:'Outfit',sans-serif;font-size:15px;font-weight:700}
.company-header .info p{font-size:9px;color:var(--text-secondary);text-transform:uppercase;letter-spacing:0.8px}
.metrics-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:16px}
.metric-card{background:var(--white);border:1px solid var(--border);border-radius:8px;padding:9px 10px;text-align:center}
.metric-card .num{font-family:'Outfit',sans-serif;font-size:15px;font-weight:700;color:var(--accent-navy)}
.metric-card .lbl{font-size:8px;text-transform:uppercase;letter-spacing:0.8px;color:var(--text-secondary);margin-top:1px}
.metric-card.highlight{background:linear-gradient(135deg,#012169,#0050a0);color:white;border:none}
.metric-card.highlight .num{color:white}
.metric-card.highlight .lbl{color:rgba(255,255,255,.7)}
.metric-card.apex{background:linear-gradient(135deg,var(--apex-violet),#8466CC);color:white;border:none}
.metric-card.apex .num{color:white;font-size:13px}
.metric-card.apex .lbl{color:rgba(255,255,255,.85)}
.section-label{font-family:'Outfit',sans-serif;font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:2px;color:var(--deloitte-green);margin-bottom:8px;padding-bottom:4px;border-bottom:1px solid var(--border)}
.priorities-block{margin-bottom:16px}
.priority-item{display:flex;align-items:flex-start;gap:8px;margin-bottom:7px;font-size:10.5px;line-height:1.4}
.priority-num{width:18px;height:18px;min-width:18px;border-radius:50%;background:var(--accent-navy);color:white;font-size:9px;font-weight:700;display:flex;align-items:center;justify-content:center;margin-top:1px}
.priority-item strong{color:var(--accent-navy)}
.team-list{margin-bottom:0}
.team-item{display:flex;justify-content:space-between;align-items:center;padding:5px 0;border-bottom:1px solid rgba(0,0,0,.05);font-size:10px}
.team-item:last-child{border-bottom:none}
.team-item .name{font-weight:600;color:var(--text-primary)}
.team-item .role{color:var(--text-secondary);font-size:9px}
.col-center{padding:18px 22px;display:flex;flex-direction:column;gap:14px}
.chart-row{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.chart-box{background:var(--white);border:1px solid var(--border);border-radius:10px;padding:12px 14px;position:relative}
.chart-box h4{font-family:'Outfit',sans-serif;font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--text-secondary);margin-bottom:8px}
.chart-container{position:relative;width:100%;height:155px}
.opp-pipeline{background:var(--white);border:1px solid var(--border);border-radius:10px;padding:12px 14px}
.opp-pipeline h4{font-family:'Outfit',sans-serif;font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--text-secondary);margin-bottom:8px}
.pipeline-table{width:100%;border-collapse:collapse;font-size:9.5px}
.pipeline-table th{text-align:left;font-size:8px;text-transform:uppercase;letter-spacing:1px;color:var(--text-secondary);padding:4px 6px;border-bottom:2px solid var(--border);font-weight:600}
.pipeline-table td{padding:5px 6px;border-bottom:1px solid var(--border);vertical-align:middle}
.pipeline-table tr:last-child td{border-bottom:none}
.pipeline-table .opp-name{font-weight:600;color:var(--text-primary)}
.svc-code{font-family:'Outfit',sans-serif;font-size:9px;font-weight:700;color:var(--apex-violet);background:rgba(102,72,176,.08);padding:2px 6px;border-radius:4px;margin-right:5px}
.tag{display:inline-block;padding:2px 6px;border-radius:3px;font-size:8px;font-weight:700;text-transform:uppercase;letter-spacing:0.5px}
.tag-new{background:#EBF8FF;color:#2B6CB0}.tag-expansion{background:#F0FFF4;color:#276749}.tag-wedge{background:#FFFBEB;color:#975A16}.tag-displace{background:#FFF5F5;color:#C53030}
.bar-container{width:80px;height:8px;background:#EDF2F7;border-radius:4px;overflow:hidden}
.bar-fill{height:100%;border-radius:4px;background:linear-gradient(90deg,var(--apex-violet),#8466CC)}
.col-right{padding:18px 20px;border-left:1px solid var(--border);background:var(--bg-light);display:flex;flex-direction:column;gap:14px}
.approach-steps{margin-bottom:0}
.step-item{display:flex;gap:10px;margin-bottom:10px;position:relative}
.step-item:not(:last-child)::after{content:'';position:absolute;left:11px;top:24px;bottom:-6px;width:2px;background:linear-gradient(to bottom,var(--apex-violet),transparent)}
.step-dot{width:24px;height:24px;min-width:24px;border-radius:50%;background:var(--apex-violet);color:#fff;font-size:10px;font-weight:800;display:flex;align-items:center;justify-content:center}
.step-content h5{font-family:'Outfit',sans-serif;font-size:11px;font-weight:700;margin-bottom:2px}
.step-content p{font-size:9.5px;color:var(--text-secondary);line-height:1.35}
.step-tag{font-size:8px;font-weight:700;color:var(--apex-violet);text-transform:uppercase;letter-spacing:0.5px}
.risk-item{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid rgba(0,0,0,.05);font-size:10px;line-height:1.3}
.risk-item:last-child{border-bottom:none}
.risk-dot{width:8px;height:8px;min-width:8px;border-radius:50%}
.risk-dot.high{background:var(--red-flag)}.risk-dot.medium{background:var(--amber)}.risk-dot.low{background:var(--green-ok)}
.next-steps-list{font-size:10px}
.ns-item{display:flex;align-items:flex-start;gap:6px;margin-bottom:6px;line-height:1.35}
.ns-arrow{color:var(--apex-violet);font-weight:800;min-width:10px;margin-top:1px}
.ns-item .timeline{font-size:8px;font-weight:600;color:var(--accent-teal);text-transform:uppercase}
.footer{display:flex;justify-content:space-between;align-items:center;padding:8px 36px;background:var(--deloitte-dark);color:rgba(255,255,255,.5);font-size:8px;letter-spacing:0.5px}
.footer strong{color:var(--deloitte-green)}
@media print{body{width:100%}.main{min-height:auto}}
.modal-overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,.65);z-index:9999;justify-content:center;align-items:center;backdrop-filter:blur(4px);animation:mfadeIn .2s ease}
.modal-overlay.open{display:flex}
@keyframes mfadeIn{from{opacity:0}to{opacity:1}}
.modal-box{background:#fff;border-radius:14px;width:90%;max-width:720px;max-height:85vh;overflow-y:auto;box-shadow:0 24px 80px rgba(0,0,0,.35);animation:mslideUp .25s ease;position:relative}
@keyframes mslideUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:none}}
.mh{padding:18px 24px 14px;border-bottom:1px solid #E2E8F0;display:flex;justify-content:space-between;align-items:flex-start}
.mh-title{font-family:'Outfit',sans-serif;font-size:16px;font-weight:700}
.mh-sub{font-size:10px;color:#4A5568;margin-top:2px;text-transform:uppercase;letter-spacing:.5px}
.mclose{width:32px;height:32px;border:none;background:none;font-size:18px;cursor:pointer;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#4A5568;transition:.2s}
.mclose:hover{background:#F7F9FA;color:#1A1A2E}
.mb{padding:18px 24px 24px;font-size:13px;line-height:1.7;color:#4A5568}
.mb h4{font-family:'Outfit',sans-serif;font-size:13px;font-weight:700;color:var(--apex-violet);margin:14px 0 6px;text-transform:uppercase;letter-spacing:.5px}
.mb h4:first-child{margin-top:0}
.mb strong{color:#1A1A2E}
.mb ul{margin:4px 0 8px 16px;font-size:12px}
.mb li{margin-bottom:3px}
.mtag{display:inline-block;font-size:10px;font-weight:600;padding:2px 8px;border-radius:4px;background:rgba(102,72,176,.08);color:var(--apex-violet);border:1px solid rgba(102,72,176,.15);margin-right:4px;margin-bottom:4px}
.clickable{cursor:pointer;transition:.15s;position:relative}
.clickable:hover{opacity:.85}
.agent-row{display:flex;flex-wrap:wrap;gap:5px;margin-top:6px}
.agent-pill{display:inline-block;padding:2px 6px;border-radius:4px;font-size:8.5px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;background:rgba(102,72,176,.10);color:var(--apex-violet)}
"""


# ---------------------------------------------------------------------------
# Per-client section builders
# ---------------------------------------------------------------------------

def _esc(s):
    return html.escape(s) if s else ""


def total_value(scenarios):
    lo = sum(s[3] for s in scenarios)
    hi = sum(s[4] for s in scenarios)
    if lo < 1:
        return f"${lo*1000:.0f}K-${hi*1000:.0f}K"
    return f"${lo:.1f}-{hi:.1f}M"


def build_priorities_html(client):
    out = ['<div class="section-label">CEO / C-Suite Strategic Priorities</div>',
           '<div class="priorities-block">']
    for i, (title, body) in enumerate(client["priorities"], start=1):
        out.append(f'<div class="priority-item"><div class="priority-num">{i}</div>'
                   f'<div><strong>{_esc(title)}</strong> &mdash; {_esc(body)}</div></div>')
    out.append('</div>')
    return "\n".join(out)


def build_contacts_html(client):
    out = ['<div class="section-label">Account / Client Contacts</div>',
           '<div class="team-list">']
    for name, role in client["contacts"]:
        out.append(f'<div class="team-item"><span class="name">{_esc(name)}</span>'
                   f'<span class="role">{_esc(role)}</span></div>')
    out.append('</div>')
    return "\n".join(out)


def build_pipeline_html(client):
    out = ['<div class="opp-pipeline">',
           '<h4>FY27 APEX Agentic AI Services Pipeline &mdash; Functional-Area Aligned</h4>',
           '<table class="pipeline-table">',
           '<thead><tr><th style="width:36%">Scenario (Service ID)</th>'
           '<th>Functional Area</th><th>Tag</th><th>Value</th><th>Quarter</th>'
           '<th style="width:80px">Confidence</th></tr></thead><tbody>']
    for code, title, kpi, lo, hi, qtr, prog, tag in client["scenarios"]:
        svc_name = SERVICE_NAMES.get(code, code)
        fa = FUNCTIONAL_AREA.get(code, "Operations")
        if lo < 1:
            value_str = f"${int(lo*1000)}K-${int(hi*1000)}K"
        else:
            value_str = f"${lo:.1f}-{hi:.1f}M"
        out.append(
            f'<tr><td><span class="svc-code">{code}</span>'
            f'<span class="opp-name">{_esc(title)}</span><br>'
            f'<span style="font-size:8px;color:#6648B0;font-weight:600">{_esc(svc_name)} &middot; KPI: {_esc(kpi)}</span></td>'
            f'<td style="font-size:9px">{_esc(fa)}</td>'
            f'<td><span class="tag tag-{tag}">{tag.title()}</span></td>'
            f'<td>{value_str}</td><td>{_esc(qtr)}</td>'
            f'<td><div class="bar-container"><div class="bar-fill" style="width:{prog}%"></div></div></td></tr>'
        )
    out.append('</tbody></table></div>')
    return "\n".join(out)


def build_approach_html(client):
    """W1/W2/W3 wave approach."""
    waves = [
        ("Wave 1 · Foundation", "W1 · Q1–Q2 FY27",
         f"Establish APEX substrate on {client['primary_cloud']}: SOR connectors -> Bronze landing -> Silver canonical "
         f"(MERML / SCML schemas) -> LEDGER 14-field audit row store. Wire MCP server, Entra identities, "
         f"Adaptive-Card HITL surface in Teams. BVA-funded discovery + first-scenario assessment."),
        ("Wave 2 · Pilot (you are here)", "W2 · Q2–Q3 FY27",
         f"Stand up the marquee scenario for the highest-value functional area &mdash; "
         f"<strong>{SERVICE_NAMES.get(client['scenarios'][0][0], client['scenarios'][0][0])}</strong>. "
         f"6-agent fleet: Assess &middot; Classify &middot; Quantify &middot; Approve &middot; Act &middot; Evidence-Write. "
         f"Sequential-with-HITL-gate orchestration. KPI: <strong>{client['scenarios'][0][2]}</strong>."),
        ("Wave 3 · Scale & Fuse", "W3 · Q3–Q4 FY27",
         "Expand to adjacent scenarios across the same functional area &middot; multi-region / multi-property rollout &middot; "
         "fuse with adjacent functional areas via A2A swarm. Purview lineage at enterprise scale &middot; "
         "LEDGER feedback loop drives model retraining."),
    ]
    out = ['<div><div class="section-label">APEX Wave Roadmap (W1 &rarr; W3)</div>',
           '<div class="approach-steps">']
    for i, (title, tag, body) in enumerate(waves, start=1):
        out.append(f'<div class="step-item"><div class="step-dot">{i}</div>'
                   f'<div class="step-content"><div class="step-tag">{_esc(tag)}</div>'
                   f'<h5>{title}</h5><p>{body}</p></div></div>')
    out.append('</div></div>')
    return "\n".join(out)


def build_funding_html(client):
    return f"""
<div>
  <div class="section-label">Funding Strategy (Independence-Safe)</div>
  <div class="next-steps-list">
    <div class="ns-item"><span class="ns-arrow">&rsaquo;</span><div><strong>BVA:</strong> $100&ndash;200K &mdash; APEX Discovery + functional-area scenario assessment</div></div>
    <div class="ns-item"><span class="ns-arrow">&rsaquo;</span><div><strong>DCIF:</strong> $250&ndash;500K &mdash; Wave-2 pilot co-investment for marquee scenario</div></div>
    <div class="ns-item"><span class="ns-arrow">&rsaquo;</span><div><strong>ISV Marketplace:</strong> $300&ndash;750K &mdash; Foundry / Fabric capability burndown via MACC ISVs</div></div>
    <div class="ns-item"><span class="ns-arrow">&rsaquo;</span><div><strong>Client Direct:</strong> Wave-3 scale-out funded from W2 KPI run-rate</div></div>
  </div>
</div>"""


def build_risks_html(client):
    primary = client["primary_cloud"].upper()
    risks = []
    if "AWS" in primary and "AZURE" not in primary:
        risks.append(("high", "AWS-primary cloud", "APEX Decision/Runtime planes are Microsoft-native; position as workload-specific COEXIST + Foundry agentic on AWS data-lake feeds"))
    elif "GCP" in primary and "AZURE" not in primary:
        risks.append(("high", "GCP-primary cloud", "APEX Decision/Runtime planes are Microsoft-native; position as agentic workload on existing data foundation"))
    elif "AWS" in primary or "GCP" in primary:
        risks.append(("medium", "Multi-cloud posture", "Hybrid AWS/GCP+Azure stance &mdash; APEX runs on the Azure portion; coexistence plan for SOR feeds"))
    else:
        risks.append(("low", "Azure-aligned", "Primary cloud is Azure &mdash; APEX runs natively on Microsoft platform"))
    risks.append(("medium", "Operational integrity in flight", f"{client['erp']} &mdash; sequence APEX behind operational/ERP cutovers; never on the IROPS critical path"))
    risks.append(("medium", "Independence posture", "Manifests, policies, LEDGER are client artifacts; Deloitte authors and operates &mdash; no Microsoft ECIF flows direct to Deloitte"))
    risks.append(("medium", "Competitive SI presence", "Accenture / Big-4 likely active; differentiate on APEX 6-agent fleet + LEDGER provability vs generic Foundry"))
    out = ['<div><div class="section-label">Key Risks</div><div>']
    for sev, title, body in risks:
        out.append(f'<div class="risk-item"><div class="risk-dot {sev}"></div>'
                   f'<div><strong>{_esc(title)}</strong> &mdash; {body}</div></div>')
    out.append('</div></div>')
    return "\n".join(out)


def build_next_steps_html(client):
    return f"""
<div>
  <div class="section-label">Next Steps</div>
  <div class="next-steps-list">
    <div class="ns-item"><span class="ns-arrow">&rsaquo;</span><div><span class="timeline">Week 1</span> &mdash; Account-team meeting: review APEX scenario fit + funding</div></div>
    <div class="ns-item"><span class="ns-arrow">&rsaquo;</span><div><span class="timeline">30 Days</span> &mdash; Functional-area workshop with {client['contacts'][0][0].split(',')[0]} / direct reports</div></div>
    <div class="ns-item"><span class="ns-arrow">&rsaquo;</span><div><span class="timeline">45 Days</span> &mdash; APEX Discovery BVA proposal + scenario shortlist</div></div>
    <div class="ns-item"><span class="ns-arrow">&rsaquo;</span><div><span class="timeline">60 Days</span> &mdash; Wave-1 Foundation delivery kickoff (SOR &rarr; Bronze &rarr; Silver)</div></div>
    <div class="ns-item"><span class="ns-arrow">&rsaquo;</span><div><span class="timeline">Q2 FY27</span> &mdash; First Wave-2 marquee scenario in production with LEDGER audit</div></div>
  </div>
</div>"""


def build_modals_html(client):
    """Build modals for the top 3 scenarios."""
    out = []
    for i, sc in enumerate(client["scenarios"][:3]):
        code, title, kpi, lo, hi, qtr, prog, tag = sc
        svc_name = SERVICE_NAMES.get(code, code)
        fa = FUNCTIONAL_AREA.get(code, "Operations")
        modal_id = f"m-sc-{i}"
        agents = "Assess · Classify · Quantify · Approve · Act · Evidence-Write".split(" · ")
        agent_pills = "".join(f'<span class="agent-pill">{a}</span>' for a in agents)
        if lo < 1:
            value_str = f"${int(lo*1000)}K-${int(hi*1000)}K"
        else:
            value_str = f"${lo:.1f}M-${hi:.1f}M"
        out.append(f"""
<div class="modal-overlay" id="{modal_id}">
  <div class="modal-box">
    <div class="mh"><div><div class="mh-title">{_esc(title)}</div>
      <div class="mh-sub">{code} &middot; {_esc(svc_name)} &middot; {value_str} &middot; {tag.upper()}</div></div>
      <button class="mclose" onclick="closeModal('{modal_id}')">&#10005;</button></div>
    <div class="mb">
      <h4>Functional Area &amp; Business Moment</h4>
      <p><strong>{_esc(fa)}</strong> &mdash; This scenario fires when the operational signal arrives at the SOR (PSS, PMS, telematics, CRM, IROPS, OTA depending on functional area). APEX agents take it from event &rarr; bounded mutation with full LEDGER audit. Target KPI uplift: <strong>{_esc(kpi)}</strong>.</p>

      <h4>APEX 6-Agent Fleet</h4>
      <div class="agent-row">{agent_pills}</div>
      <p style="margin-top:8px">Sequential orchestration with a Teams Adaptive-Card HITL gate before any material mutation. Every action emits a 14-field audit row to the LEDGER plane &mdash; drillable from KPI &rarr; trace_id &rarr; reasoning trace.</p>

      <h4>KPI Uplift Chain</h4>
      <ul>
        <li><strong>Wave 1 ({client['primary_cloud']} foundation):</strong> SOR &rarr; Bronze &rarr; Silver canonical. KPI baseline established.</li>
        <li><strong>Wave 2 (pilot):</strong> {_esc(kpi)} on the first cohort &middot; sequential agents with HITL gate &middot; Teams notification.</li>
        <li><strong>Wave 3 (scale &amp; fuse):</strong> Multi-region / multi-property run-rate &middot; A2A fusion with adjacent scenarios &middot; LEDGER-fed retraining.</li>
      </ul>

      <h4>Microsoft-Native Stack</h4>
      <div>
        <span class="mtag">Microsoft Fabric</span>
        <span class="mtag">Azure OpenAI / Foundry</span>
        <span class="mtag">CAF Dynamic</span>
        <span class="mtag">Teams Adaptive Cards</span>
        <span class="mtag">Entra ID</span>
        <span class="mtag">Purview</span>
        <span class="mtag">Power BI Direct Lake</span>
      </div>

      <h4>Estimated Value</h4>
      <p><strong>{value_str}</strong> revenue influence over the FY27 horizon &middot; tag: <strong>{tag.upper()}</strong> &middot; quarter: {qtr}.</p>
    </div>
  </div>
</div>""")
    return "\n".join(out)


def build_html(client):
    total_lo = sum(s[3] for s in client["scenarios"])
    total_hi = sum(s[4] for s in client["scenarios"])
    if total_lo < 1:
        total_str = f"${int(total_lo*1000)}K-${int(total_hi*1000)}K"
    else:
        total_str = f"${total_lo:.1f}-{total_hi:.1f}M"

    fa_map = {}
    for code, _, _, lo, hi, *_ in client["scenarios"]:
        fa = FUNCTIONAL_AREA.get(code, "Other").split(" · ")[-1]
        fa_map.setdefault(fa, [0,0])
        fa_map[fa][0] += lo; fa_map[fa][1] += hi
    fa_labels = list(fa_map.keys())

    sc_labels = [s[1][:24] for s in client["scenarios"]]
    sc_lows = [s[3] for s in client["scenarios"]]
    sc_ups = [s[4]-s[3] for s in client["scenarios"]]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{_esc(client['name_long'])} &mdash; APEX Agentic AI Services One-Pager</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>

<div style="background:#0D2818;border-bottom:2px solid #86BC25;padding:0 24px;display:flex;align-items:center;justify-content:space-between;position:relative;z-index:200;">
  <div style="display:flex;gap:0;">
    <a href="{client['folder']}_OnePager.html" style="padding:6px 14px;font-size:11px;font-weight:600;text-decoration:none;color:rgba(134,188,37,.65);font-family:'DM Sans',sans-serif;display:inline-block;">Microsoft Platform Snapshot</a>
    <a href="{client['name_short'].replace(' ','').replace('!','').replace(chr(39),'')}_APEX_OnePager.html" style="padding:6px 14px;font-size:11px;font-weight:600;text-decoration:none;color:#86BC25;border-bottom:2px solid #86BC25;background:rgba(134,188,37,.1);font-family:'DM Sans',sans-serif;display:inline-block;">APEX Agentic AI Services</a>
  </div>
  <div style="font-size:9px;color:rgba(255,255,255,.6);font-family:'DM Sans';letter-spacing:1px;text-transform:uppercase;">{_esc(client['name_short'])} Document Suite &middot; APEX Agentic Edition</div>
</div>

<div class="header">
  <div class="header-left">
    <div class="header-logo">Deloitte</div>
    <div class="header-title">
      <h1>{_esc(client['name_long'])} &mdash; APEX Agentic AI Services Strategy</h1>
      <p>FY27 Revenue Influence Pipeline &nbsp;|&nbsp; APEX Scenario Catalog Mapping &nbsp;|&nbsp; Prepared by Keven Markham, VP DMTSP</p>
    </div>
  </div>
  <div class="header-right">
    <div class="apex-chip">APEX &middot; AGENTIC</div>
    <div class="phase-badge"><span class="label">Strategy</span><span class="value">WEDGE / NEW</span></div>
    <div class="phase-badge"><span class="label">Phase</span><span class="value">Discovery / Pilot</span></div>
    <div class="revenue-badge"><div class="amount">{total_str}</div><div class="label">FY27 APEX Pipeline</div></div>
  </div>
</div>

<div class="main">
  <!-- LEFT COLUMN -->
  <div class="col-left">
    <div class="company-header">
      <div class="company-icon" style="background:linear-gradient(135deg,{client['brand_color']},#444)">{client['ticker'][:4]}</div>
      <div class="info">
        <h3>{_esc(client['name_short'])}</h3>
        <p>{_esc(client['hq'])}</p>
      </div>
    </div>

    <div class="metrics-grid">
      <div class="metric-card highlight"><div class="num">{client['revenue']}</div><div class="lbl">Revenue</div></div>
      <div class="metric-card highlight"><div class="num">{client['employees']}</div><div class="lbl">Employees</div></div>
      <div class="metric-card"><div class="num">{client['metric3']}</div><div class="lbl">{client['metric3_lbl']}</div></div>
      <div class="metric-card"><div class="num">{client['metric4']}</div><div class="lbl">{client['metric4_lbl']}</div></div>
      <div class="metric-card"><div class="num">{client['metric5']}</div><div class="lbl">{client['metric5_lbl']}</div></div>
      <div class="metric-card"><div class="num">{client['metric6']}</div><div class="lbl">{client['metric6_lbl']}</div></div>
      <div class="metric-card apex" style="grid-column:span 2"><div class="num">{client['primary_cloud']}</div><div class="lbl">Primary Cloud &middot; ERP: {_esc(client['erp'])}</div></div>
    </div>

    {build_priorities_html(client)}
    {build_contacts_html(client)}
  </div>

  <!-- CENTER COLUMN -->
  <div class="col-center">
    <div class="chart-row">
      <div class="chart-box"><h4>APEX Scenario Value ($M, Range)</h4><div class="chart-container"><canvas id="scenarioChart"></canvas></div></div>
      <div class="chart-box"><h4>Value by Functional Area ($M)</h4><div class="chart-container"><canvas id="faChart"></canvas></div></div>
    </div>

    {build_pipeline_html(client)}

    <div class="chart-row">
      <div class="chart-box"><h4>APEX 6-Agent Fleet (Effort Mix)</h4><div class="chart-container"><canvas id="agentChart"></canvas></div></div>
      <div class="chart-box"><h4>KPI Uplift Trajectory (W1 &rarr; W3)</h4><div class="chart-container"><canvas id="kpiChart"></canvas></div></div>
    </div>
  </div>

  <!-- RIGHT COLUMN -->
  <div class="col-right">
    {build_approach_html(client)}
    {build_funding_html(client)}
    {build_risks_html(client)}
    {build_next_steps_html(client)}
  </div>
</div>

<div class="footer">
  <div><strong>CONFIDENTIAL</strong> &mdash; Deloitte Internal Use Only &nbsp;|&nbsp; {_esc(client['sub_path'])} / {_esc(client['name_short'])} / APEX Agentic AI Services</div>
  <div>Keven Markham &nbsp;|&nbsp; VP, DMTSP &nbsp;|&nbsp; APEX Reference: <strong>APEX-Scenario-Chains.xlsx</strong> &nbsp;|&nbsp; v1.0 &middot; FY27</div>
</div>

{build_modals_html(client)}

<script>
Chart.defaults.font.family="'DM Sans',sans-serif";Chart.defaults.font.size=10;Chart.defaults.color='#4A5568';

new Chart(document.getElementById('scenarioChart'),{{
  type:'bar',
  data:{{
    labels:{sc_labels!r},
    datasets:[
      {{label:'Low ($M)',data:{sc_lows},backgroundColor:'#6648B0',borderRadius:3}},
      {{label:'Upside ($M)',data:{sc_ups},backgroundColor:'rgba(102,72,176,0.35)',borderRadius:3}}
    ]
  }},
  options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,
    scales:{{x:{{stacked:true,grid:{{color:'rgba(0,0,0,.05)'}},ticks:{{callback:v=>'$'+v+'M',font:{{size:8}}}}}},
            y:{{stacked:true,grid:{{display:false}},ticks:{{font:{{size:7.5,weight:'600'}}}}}}}},
    plugins:{{legend:{{display:true,position:'bottom',labels:{{boxWidth:10,font:{{size:8}},padding:6}}}},
              tooltip:{{callbacks:{{label:ctx=>ctx.dataset.label+': $'+ctx.raw+'M'}}}}}}
  }}
}});

new Chart(document.getElementById('faChart'),{{
  type:'doughnut',
  data:{{
    labels:{fa_labels!r},
    datasets:[{{data:{[round(v[0]+(v[1]-v[0])/2,2) for v in fa_map.values()]},backgroundColor:['#6648B0','#3DD9C4','#E3B657','#0076A8','#86BC25','#012169','#E87B3C'],borderWidth:2,borderColor:'#fff'}}]
  }},
  options:{{responsive:true,maintainAspectRatio:false,cutout:'52%',
    plugins:{{legend:{{position:'right',labels:{{boxWidth:8,font:{{size:8.5}},padding:5}}}},
              tooltip:{{callbacks:{{label:ctx=>ctx.label+': ~$'+ctx.raw+'M'}}}}}}
  }}
}});

new Chart(document.getElementById('agentChart'),{{
  type:'bar',
  data:{{
    labels:['Assess','Classify','Quantify','Approve','Act','Evidence-Write'],
    datasets:[{{data:[18,16,22,12,20,12],backgroundColor:['#6648B0','#7B5DC2','#9075D4','#3DD9C4','#0076A8','#012169'],borderRadius:4}}]
  }},
  options:{{responsive:true,maintainAspectRatio:false,
    scales:{{y:{{grid:{{color:'rgba(0,0,0,.05)'}},ticks:{{callback:v=>v+'%',font:{{size:9}}}},max:30}},
            x:{{grid:{{display:false}},ticks:{{font:{{size:8.5,weight:'600'}}}}}}}},
    plugins:{{legend:{{display:false}},
              tooltip:{{callbacks:{{label:ctx=>'~'+ctx.raw+'% of fleet effort'}}}}}}
  }}
}});

new Chart(document.getElementById('kpiChart'),{{
  type:'line',
  data:{{
    labels:['W1 Foundation','W2 Pilot','W3 Scale','W3+ Fuse','W4+ Run-Rate'],
    datasets:[
      {{label:'Cumulative KPI Lift (%)',data:[0,28,62,85,100],borderColor:'#6648B0',backgroundColor:'rgba(102,72,176,0.10)',fill:true,tension:0.4,pointRadius:3,pointBackgroundColor:'#6648B0',borderWidth:2.5}},
      {{label:'Run-Rate Target',data:[100,100,100,100,100],borderColor:'#86BC25',borderDash:[6,4],borderWidth:1.5,pointRadius:0,fill:false}}
    ]
  }},
  options:{{responsive:true,maintainAspectRatio:false,
    scales:{{y:{{min:0,max:115,grid:{{color:'rgba(0,0,0,.05)'}},ticks:{{callback:v=>v+'%',font:{{size:9}}}}}},
            x:{{grid:{{display:false}},ticks:{{font:{{size:8.5}}}}}}}},
    plugins:{{legend:{{position:'bottom',labels:{{boxWidth:12,font:{{size:8}},padding:6}}}},
              tooltip:{{callbacks:{{label:ctx=>ctx.dataset.label+': '+ctx.raw+'%'}}}}}}
  }}
}});
</script>

<script>
function openModal(id){{document.getElementById(id).classList.add('open');document.body.style.overflow='hidden';}}
function closeModal(id){{document.getElementById(id).classList.remove('open');document.body.style.overflow='';}}
document.addEventListener('keydown',e=>{{if(e.key==='Escape'){{document.querySelectorAll('.modal-overlay.open').forEach(m=>{{m.classList.remove('open');document.body.style.overflow='';}})}}}});
document.querySelectorAll('.modal-overlay').forEach(m=>{{m.addEventListener('click',e=>{{if(e.target===m){{m.classList.remove('open');document.body.style.overflow='';}}}})}});

// Wire pipeline rows to modals
document.querySelectorAll('.pipeline-table tbody tr').forEach((row,i)=>{{
  if(i<3){{
    row.style.cursor='pointer';
    row.querySelector('.opp-name').style.color='#6648B0';
    row.addEventListener('click',()=>openModal('m-sc-'+i));
  }}
}});
</script>

</body>
</html>
"""


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main():
    print(f"Building APEX Agentic AI OnePagers for {len(CLIENTS)} Travel-Hospitality clients...\n")
    written = 0
    import unicodedata
    for client in CLIENTS:
        out_dir = TH_ROOT / client["sub_path"] / client["folder"] / "01_account" / "one_pager"
        out_dir.mkdir(parents=True, exist_ok=True)
        # ASCII-safe file name
        nfkd = unicodedata.normalize("NFKD", client["name_short"])
        ascii_name = "".join(c for c in nfkd if not unicodedata.combining(c))
        fname = ascii_name.replace(" ", "").replace(".", "").replace("'", "").replace("!", "")
        out_path = out_dir / f"{fname}_APEX_OnePager.html"
        try:
            html_text = build_html(client)
            out_path.write_text(html_text, encoding="utf-8")
            print(f"  [{client['segment']}] {client['name_short']:22s} -> {out_path.name}  ({len(html_text):,} chars)")
            written += 1
        except Exception as e:
            print(f"  [{client['segment']}] {client['name_short']:22s} -> ERROR: {e}")
    print(f"\nDone. {written}/{len(CLIENTS)} OnePagers written.")


if __name__ == "__main__":
    main()
