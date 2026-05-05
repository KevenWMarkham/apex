"""Build APEX Agentic AI OnePager HTML for every Consumer client.

For each of the 33 Consumer clients (Brands-Lifestyle / Food-Beverage / Retail),
emit `<Client>_APEX_OnePager.html` into `01_account/one_pager/`.

Each one-pager:
  - Models on Nike_OnePager.html visual structure (1440px landscape, 3-col grid,
    Chart.js, modals, Deloitte branding)
  - Replaces the Microsoft Platform pipeline with APEX Agentic AI Services pipeline:
    scenarios from the APEX scenario catalog mapped to the client's functional area
    (back-office · operations · frontline)
  - Charts focus on: Scenario value by functional area, Agent fleet distribution,
    KPI uplift chain, Maturation timeline (W1→W4+)
  - WEDGE/NEW/EXPANSION strategy tags retained
  - Modal popups for top scenarios + key contacts

Output: <client>/01_account/one_pager/<Client>_APEX_OnePager.html
"""
from __future__ import annotations
import io, sys, html
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

CONSUMER_ROOT = Path(r"C:\Stage\Clients\Industries\Consumer")

# ---------------------------------------------------------------------------
# Service catalog (from APEX-Scenario-Chains.xlsx)
# ---------------------------------------------------------------------------
SERVICE_NAMES = {
    "RC-E2E-03": "Assortment & Pricing",
    "RC-E2E-04": "Customer Loyalty & Marketing",
    "RC-E2E-05": "Store Operations",
    "RC-E2E-06": "Supply Chain & Logistics",
    "RC-E2E-07": "Loss Prevention & Fraud",
    "RC-E2E-08": "Workforce Intelligence",
    "RC-E2E-09": "Perishables & Waste",
    "AXLE-Connected-Factory-01": "Connected Factory · Predictive Maintenance",
    "AXLE-Ops-03": "Manufacturing Operations Excellence",
    "AXLE-QMS-02": "Quality Management & Root-Cause",
    "AXLE-Supply-04": "Supply Chain Resilience",
    "ICE-Aftermarket-01": "Distribution Operations",
    "ER-OG-03": "Field & Asset Operations",
}

# Functional area buckets that map to service codes
FUNCTIONAL_AREA = {
    "RC-E2E-03": "Back-Office · Pricing & Margin",
    "RC-E2E-04": "Frontline · Customer & Loyalty",
    "RC-E2E-05": "Frontline · In-Store Operations",
    "RC-E2E-06": "Operations · Supply Chain",
    "RC-E2E-07": "Operations · Risk & Loss",
    "RC-E2E-08": "Back-Office · Workforce",
    "RC-E2E-09": "Operations · Perishables",
    "AXLE-Connected-Factory-01": "Operations · Plant Floor",
    "AXLE-Ops-03": "Operations · Manufacturing",
    "AXLE-QMS-02": "Operations · Quality",
    "AXLE-Supply-04": "Operations · Supply Chain",
    "ICE-Aftermarket-01": "Operations · Distribution",
    "ER-OG-03": "Operations · Field",
}

# ---------------------------------------------------------------------------
# Client catalog · 33 Consumer clients with APEX scenario alignment
# Public-domain facts (revenue, employees, HQ) from FY24/FY25 annual reports.
# ---------------------------------------------------------------------------
# Each client dict:
#   ticker, name_short, name_long, segment ("Brands"|"Food"|"Retail"),
#   sub_path ("Brands-Lifestyle"|"Food-Beverage"|"Retail"),
#   folder (the actual folder name on disk),
#   hq, revenue (string), employees (string), retail_locations or note,
#   market_cap_or_note, gross_margin_or_note,
#   primary_cloud, erp,
#   priorities [4 items: title + body],
#   contacts [4-6 items: name, role],
#   scenarios [6 items: service_code, scenario_title, kpi, value_low, value_high,
#              quarter, progress_pct, tag (wedge|new|expansion|displace)],
#   risks [4 items: severity (high|medium|low), title + body],
#   approach_steps [3 items: tag, title, body],
#   funding [3 items: source + body],
#   next_steps [5 items: timeline + action]

def _r(prac):
    return [
        ("RC-E2E-03","Dynamic markdown optimization","+1.4pp GM",1.5,3.0,"Q1–Q2",30,"wedge"),
        ("RC-E2E-04","Loyalty-churn prediction","−6pp churn",1.0,2.5,"Q2–Q3",20,"new"),
        ("RC-E2E-05","On-shelf availability / OSA",">98% OSA",1.0,2.0,"Q2–Q3",15,"new"),
        ("RC-E2E-06","Last-mile slot optimization","+22% slot util",0.8,1.8,"Q3",15,"new"),
        ("RC-E2E-07","Returns-fraud detection","+$8.6M recovery",0.6,1.4,"Q1",25,"wedge"),
        ("RC-E2E-09","Perishable waste reduction","−28% loss",0.5,1.2,"Q3–Q4",10,"expansion"),
    ]

# ---- Client profiles ----
CLIENTS = []

# ===== BRANDS-LIFESTYLE (10) =====

CLIENTS.append({
    "ticker":"NKE","name_short":"Nike","name_long":"Nike, Inc.",
    "segment":"Brands","sub_path":"Brands-Lifestyle","folder":"Nike",
    "hq":"Beaverton, OR · NYSE: NKE","revenue":"$46.3B","employees":"77,800",
    "metric3":"1,045+","metric3_lbl":"Retail Stores","metric4":"160M+",
    "metric4_lbl":"Nike Members","metric5":"~$93B","metric5_lbl":"Market Cap",
    "metric6":"45.4%","metric6_lbl":"Gross Margin",
    "primary_cloud":"AWS","erp":"SAP S/4HANA","brand_color":"#111111",
    "priorities":[
        ("Return to Sport","Athlete-centric product, 2026 World Cup activation"),
        ("Wholesale Realignment","DTC + wholesale balance · Amazon return · Dick's"),
        ("Operational Excellence","CTO eliminated · COO expanded · 1,000+ cobots"),
        ("Digital Transformation","Tech under COO · CIO from Microsoft"),
    ],
    "contacts":[
        ("Elliott Hill","President & CEO"),
        ("Cheryan Jacob","CIO (ex-Microsoft)"),
        ("Venkatesh Alagirisamy","EVP, COO"),
        ("Matthew Friend","EVP, CFO"),
        ("Paul Silverglate","LCSP"),
    ],
    "scenarios":[
        ("RC-E2E-04","Member-360 lifetime-value uplift","+18% LTV",2.0,4.0,"Q1–Q2",30,"wedge"),
        ("RC-E2E-03","Markdown optimization · DTC + wholesale","+1.7pp GM",1.5,3.0,"Q2",20,"new"),
        ("RC-E2E-06","DC-to-store replenishment fusion","−12% safety stock",1.2,2.5,"Q2–Q3",15,"new"),
        ("RC-E2E-04","Cart-abandonment recovery (Nike app)","+18% recovery",0.8,1.6,"Q1–Q2",25,"wedge"),
        ("RC-E2E-05","Store associate clienteling agent","+8pp NPS",0.7,1.4,"Q3",10,"new"),
        ("RC-E2E-07","Returns-fraud detection","+$8.6M/yr",0.5,1.2,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"NWL","name_short":"Newell","name_long":"Newell Brands",
    "segment":"Brands","sub_path":"Brands-Lifestyle","folder":"Newell_Brands",
    "hq":"Atlanta, GA · NASDAQ: NWL","revenue":"$7.6B","employees":"24,000",
    "metric3":"100+","metric3_lbl":"Brands","metric4":"~25",
    "metric4_lbl":"Mfg Plants","metric5":"$3.2B","metric5_lbl":"Market Cap",
    "metric6":"31.8%","metric6_lbl":"Gross Margin",
    "primary_cloud":"Azure","erp":"SAP ECC → S/4HANA migration","brand_color":"#D71921",
    "priorities":[
        ("Project Phoenix","Multi-year operational restructuring · cost-out program"),
        ("Brand Portfolio","Sharpie · Coleman · Rubbermaid · Yankee Candle · Graco"),
        ("Supply Chain Modernization","Plant consolidation · network redesign"),
        ("Digital Marketing","Brand-led DTC + retailer partnership growth"),
    ],
    "contacts":[
        ("Chris Peterson","President & CEO"),
        ("Mark Erceg","CFO"),
        ("Joe Alkire","SVP & CIO"),
        ("Bradford Turner","CHRO & Chief Legal Officer"),
    ],
    "scenarios":[
        ("AXLE-Ops-03","Plant OEE & schedule adherence","+9pp OEE",1.6,3.2,"Q1–Q2",25,"wedge"),
        ("AXLE-Supply-04","Supplier risk & dual-sourcing","−18% disruption",1.2,2.5,"Q2",20,"new"),
        ("RC-E2E-03","Brand-portfolio price elasticity","+1.8pp GM",1.0,2.0,"Q2–Q3",15,"new"),
        ("RC-E2E-06","Network-flow rebalancing post-consolidation","−14% logistics",1.0,2.0,"Q3",10,"new"),
        ("AXLE-QMS-02","Quality-escape root-cause","−42% escape rate",0.7,1.4,"Q2",15,"new"),
        ("RC-E2E-04","Trade-promotion ROI optimization","+22% promo ROI",0.6,1.2,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"VFC","name_short":"VF Corp","name_long":"VF Corporation",
    "segment":"Brands","sub_path":"Brands-Lifestyle","folder":"VF_Corporation",
    "hq":"Denver, CO · NYSE: VFC","revenue":"$10.5B","employees":"28,000",
    "metric3":"1,300+","metric3_lbl":"Retail Stores","metric4":"7+",
    "metric4_lbl":"Power Brands","metric5":"$5.6B","metric5_lbl":"Market Cap",
    "metric6":"52.1%","metric6_lbl":"Gross Margin",
    "primary_cloud":"AWS + Azure (hybrid)","erp":"SAP S/4HANA","brand_color":"#003087",
    "priorities":[
        ("Reinvent Program","$300M cost-savings + brand-portfolio refocus"),
        ("Vans Turnaround","Brand-health recovery · global pricing reset"),
        ("North Face Growth","Outdoor category lead · DTC investment"),
        ("Operating Model","Single supply chain · regional commercial teams"),
    ],
    "contacts":[
        ("Bracken Darrell","President & CEO"),
        ("Paul Vogel","EVP, CFO"),
        ("Yon Nuta","Chief Digital & Tech Officer"),
        ("Caroline Brown","COO"),
    ],
    "scenarios":[
        ("RC-E2E-03","Vans markdown depth & cadence","+1.5pp GM",1.5,3.0,"Q1–Q2",25,"wedge"),
        ("RC-E2E-04","Multi-brand member identity & loyalty","+14% LTV",1.5,3.0,"Q2",20,"new"),
        ("RC-E2E-06","Single-supply-chain network optimization","−10% safety stock",1.2,2.5,"Q2–Q3",15,"new"),
        ("AXLE-Supply-04","Supplier disruption response (Asia tariff)","−18% disruption",1.0,2.0,"Q2",15,"new"),
        ("RC-E2E-05","Outlet-store conversion uplift","+9% conv",0.7,1.4,"Q3",10,"new"),
        ("RC-E2E-07","Returns-fraud (DTC focus)","+$5M/yr",0.5,1.0,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"PVH","name_short":"PVH","name_long":"PVH Corp.",
    "segment":"Brands","sub_path":"Brands-Lifestyle","folder":"PVH",
    "hq":"New York, NY · NYSE: PVH","revenue":"$8.9B","employees":"30,000",
    "metric3":"~1,800","metric3_lbl":"Retail Stores","metric4":"2",
    "metric4_lbl":"Power Brands (TH/CK)","metric5":"$4.6B","metric5_lbl":"Market Cap",
    "metric6":"58.7%","metric6_lbl":"Gross Margin",
    "primary_cloud":"AWS","erp":"SAP S/4HANA","brand_color":"#001F3F",
    "priorities":[
        ("PVH+ Plan","Brand-led · DTC-first · digital-first transformation"),
        ("Tommy Hilfiger Growth","Lifestyle category expansion globally"),
        ("Calvin Klein Reset","Brand reinvigoration · pricing architecture"),
        ("Supply Chain Agility","Speed-to-market · platform-led product development"),
    ],
    "contacts":[
        ("Stefan Larsson","CEO"),
        ("Zac Coughlin","CFO"),
        ("Eva Serrano","Chief Brand Officer, CK"),
        ("Lea Rytz Goldman","CEO, Tommy Hilfiger"),
    ],
    "scenarios":[
        ("RC-E2E-04","Wholesale + DTC member identity","+12% LTV",1.5,3.0,"Q1–Q2",25,"wedge"),
        ("RC-E2E-03","Brand-architecture pricing alignment","+1.6pp GM",1.2,2.5,"Q2",20,"new"),
        ("RC-E2E-06","Speed-to-market replenishment","−14% lead time",1.0,2.0,"Q2–Q3",15,"new"),
        ("AXLE-Supply-04","Tier-2/3 supplier visibility","−16% disruption",0.8,1.8,"Q3",10,"new"),
        ("RC-E2E-05","Flagship-store clienteling agent","+10pp NPS",0.7,1.4,"Q3",10,"new"),
        ("RC-E2E-07","Wholesale chargebacks dispute automation","+$4.2M/yr",0.5,1.0,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"RL","name_short":"Ralph Lauren","name_long":"Ralph Lauren Corporation",
    "segment":"Brands","sub_path":"Brands-Lifestyle","folder":"Ralph_Lauren",
    "hq":"New York, NY · NYSE: RL","revenue":"$6.6B","employees":"25,500",
    "metric3":"~530","metric3_lbl":"Owned Stores","metric4":"~720",
    "metric4_lbl":"Concession Shops","metric5":"$13.0B","metric5_lbl":"Market Cap",
    "metric6":"66.6%","metric6_lbl":"Gross Margin",
    "primary_cloud":"Azure","erp":"SAP S/4HANA","brand_color":"#012169",
    "priorities":[
        ("Next Great Chapter","Elevate brand · expand for growth · win key cities"),
        ("Direct-to-Consumer","65%+ DTC mix · digital + brick scaled"),
        ("Average Unit Retail (AUR)","Continued AUR uplift through brand elevation"),
        ("Sustainability","Design for Circularity · climate goals"),
    ],
    "contacts":[
        ("Patrice Louvet","President & CEO"),
        ("Justin Picicci","CFO"),
        ("Janet Sherlock","Chief Digital & Tech Officer"),
        ("Halide Alagöz","Chief Product & Sustainability Officer"),
    ],
    "scenarios":[
        ("RC-E2E-03","AUR-protective markdown discipline","+1.8pp GM",1.5,3.0,"Q1–Q2",25,"wedge"),
        ("RC-E2E-04","Luxury-tier clientele segmentation","+18% repeat",1.5,3.0,"Q2",20,"new"),
        ("RC-E2E-05","Concession-shop conversion lift","+11% conv",1.0,2.0,"Q2–Q3",15,"new"),
        ("RC-E2E-06","Speed-to-market for capsule drops","−18% lead time",0.8,1.8,"Q3",10,"new"),
        ("AXLE-Supply-04","Premium-fabric supplier risk","−14% disruption",0.7,1.4,"Q3",10,"new"),
        ("RC-E2E-07","Counterfeit & gray-market detection","+$6M/yr",0.5,1.2,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"EL","name_short":"Estée Lauder","name_long":"The Estée Lauder Companies",
    "segment":"Brands","sub_path":"Brands-Lifestyle","folder":"Estee_Lauder",
    "hq":"New York, NY · NYSE: EL","revenue":"$15.6B","employees":"62,000",
    "metric3":"25+","metric3_lbl":"Brands","metric4":"~150",
    "metric4_lbl":"Countries","metric5":"$26B","metric5_lbl":"Market Cap",
    "metric6":"71.4%","metric6_lbl":"Gross Margin",
    "primary_cloud":"AWS","erp":"SAP S/4HANA","brand_color":"#0A0A0A",
    "priorities":[
        ("Profit Recovery & Growth","Multi-year cost discipline + revenue rebuild"),
        ("China Recovery","Travel retail + mainland normalization"),
        ("Innovation Engine","Faster cycle times · breakthrough innovation"),
        ("Consumer-First","Personalization at scale across 25+ brands"),
    ],
    "contacts":[
        ("Stéphane de La Faverie","President & CEO"),
        ("Akhil Shrivastava","CFO"),
        ("Shana Randhava","SVP, Enterprise Innovation"),
        ("Michael Bowes","CIO"),
    ],
    "scenarios":[
        ("RC-E2E-04","Personalization across 25+ brands","+22% LTV",2.0,4.0,"Q1–Q2",25,"wedge"),
        ("RC-E2E-03","Travel-retail price-architecture optimization","+1.6pp GM",1.5,3.0,"Q2",20,"new"),
        ("RC-E2E-06","Travel-retail demand-shift fulfillment","−12% safety stock",1.2,2.5,"Q2–Q3",15,"new"),
        ("AXLE-Ops-03","Innovation-cycle plant capacity","+11pp OEE",1.0,2.0,"Q3",10,"new"),
        ("AXLE-QMS-02","Beauty-product quality escape detection","−38% escapes",0.8,1.6,"Q3",10,"new"),
        ("RC-E2E-07","Counterfeit luxury-beauty detection","+$8M/yr",0.6,1.2,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"ENR","name_short":"Energizer","name_long":"Energizer Holdings",
    "segment":"Brands","sub_path":"Brands-Lifestyle","folder":"Energizer",
    "hq":"St. Louis, MO · NYSE: ENR","revenue":"$2.9B","employees":"5,400",
    "metric3":"5","metric3_lbl":"Mfg Plants","metric4":"160+",
    "metric4_lbl":"Countries","metric5":"$2.4B","metric5_lbl":"Market Cap",
    "metric6":"40.9%","metric6_lbl":"Gross Margin",
    "primary_cloud":"Azure","erp":"SAP ECC → S/4HANA","brand_color":"#E60028",
    "priorities":[
        ("Project Momentum","Cost-savings program · operating-model redesign"),
        ("Auto-Care Growth","Armor All / STP / A/C Pro brand growth"),
        ("Battery Innovation","Premium product mix · sustainability"),
        ("Supply Chain","Plant footprint optimization"),
    ],
    "contacts":[
        ("Mark LaVigne","CEO"),
        ("John Drabik","CFO"),
        ("Hannah Kain","SVP, Supply Chain"),
        ("Mike Ladd","SVP, IT"),
    ],
    "scenarios":[
        ("AXLE-Ops-03","Battery-line OEE & changeover","+8pp OEE",1.2,2.5,"Q1–Q2",25,"wedge"),
        ("RC-E2E-03","Retailer trade-spend optimization","+1.5pp GM",1.0,2.0,"Q2",20,"new"),
        ("AXLE-Supply-04","Lithium / cobalt supplier risk","−16% disruption",0.8,1.8,"Q2–Q3",15,"new"),
        ("AXLE-QMS-02","Battery-pack defect root-cause","−40% escapes",0.7,1.4,"Q3",10,"new"),
        ("RC-E2E-06","Distributor-network replenishment","−10% safety stock",0.6,1.2,"Q3",10,"new"),
        ("RC-E2E-04","Auto-care category trade marketing","+18% promo ROI",0.4,1.0,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"WHR","name_short":"Whirlpool","name_long":"Whirlpool Corporation",
    "segment":"Brands","sub_path":"Brands-Lifestyle","folder":"Whirlpool",
    "hq":"Benton Harbor, MI · NYSE: WHR","revenue":"$16.6B","employees":"54,000",
    "metric3":"~30","metric3_lbl":"Mfg Plants","metric4":"170+",
    "metric4_lbl":"Countries","metric5":"$5.0B","metric5_lbl":"Market Cap",
    "metric6":"15.4%","metric6_lbl":"Gross Margin",
    "primary_cloud":"Azure","erp":"SAP S/4HANA","brand_color":"#005A9E",
    "priorities":[
        ("Margin Recovery","Pricing + cost actions · 9–10% EBIT target"),
        ("North America Focus","Post-Europe-exit, NA portfolio strength"),
        ("Smart Appliance / IoT","Connected-home category leadership"),
        ("Cost Restructuring","Plant footprint · global operating model"),
    ],
    "contacts":[
        ("Marc Bitzer","Chairman & CEO"),
        ("Jim Peters","CFO"),
        ("Ron Voglewede","Global Director, Connected Strategy"),
        ("Gilles Morel","President, Whirlpool EMEA (transition)"),
    ],
    "scenarios":[
        ("AXLE-Connected-Factory-01","Predictive maintenance · stamping & assembly","−22% downtime",2.0,4.0,"Q1–Q2",25,"wedge"),
        ("AXLE-Ops-03","Plant OEE digital twin","+10pp OEE",1.5,3.0,"Q2",20,"new"),
        ("AXLE-QMS-02","Warranty-claim root-cause from IoT data","−28% claims",1.2,2.5,"Q2–Q3",15,"new"),
        ("AXLE-Supply-04","Tier-2 component supplier risk","−18% disruption",1.0,2.0,"Q3",10,"new"),
        ("RC-E2E-03","Builder-channel pricing intelligence","+1.4pp GM",0.8,1.6,"Q3",10,"new"),
        ("ICE-Aftermarket-01","Connected-appliance service-call automation","−18% truck rolls",0.6,1.4,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"GIA","name_short":"GIA","name_long":"Gemological Institute of America",
    "segment":"Brands","sub_path":"Brands-Lifestyle","folder":"GIA",
    "hq":"Carlsbad, CA · Non-profit","revenue":"$430M (est.)","employees":"3,400",
    "metric3":"11","metric3_lbl":"Global Labs","metric4":"40+",
    "metric4_lbl":"Countries","metric5":"~2.5M","metric5_lbl":"Reports/Year",
    "metric6":"100%","metric6_lbl":"Gem Authentication",
    "primary_cloud":"Azure","erp":"Microsoft Dynamics 365","brand_color":"#003E7E",
    "priorities":[
        ("Lab-Grown Diamond Authentication","Disclosure & integrity in the supply chain"),
        ("Digital Reports","Mobile-first GIA report verification"),
        ("Education Growth","Online + on-campus expansion · 200K alumni"),
        ("Provenance & Traceability","Origin attestation · responsible sourcing"),
    ],
    "contacts":[
        ("Susan Jacques","President & CEO"),
        ("Mathilde Cathiard","SVP, Operations"),
        ("Tom Moses","EVP, Chief Lab & Research Officer"),
        ("Pritesh Patel","SVP, IT"),
    ],
    "scenarios":[
        ("AXLE-QMS-02","Lab-grown vs natural diamond classification agent","+3pp accuracy",1.2,2.5,"Q1–Q2",25,"wedge"),
        ("AXLE-Ops-03","Lab throughput & SLA optimization","+18% throughput",1.0,2.0,"Q2",20,"new"),
        ("RC-E2E-04","Education funnel personalization","+22% completion",0.8,1.6,"Q2–Q3",15,"new"),
        ("RC-E2E-07","Counterfeit-report detection","+$2M/yr",0.7,1.4,"Q3",10,"new"),
        ("AXLE-Supply-04","Provenance · KP-process integrity","100% chain",0.6,1.2,"Q3",10,"new"),
        ("RC-E2E-08","Gemologist hiring & certification analytics","+12% hire rate",0.4,0.9,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"SON","name_short":"Sonepar","name_long":"Sonepar SAS",
    "segment":"Brands","sub_path":"Brands-Lifestyle","folder":"Sonepar",
    "hq":"Paris, France · Privately held","revenue":"~$32B","employees":"~45,000",
    "metric3":"~3,000","metric3_lbl":"Branches","metric4":"100K+",
    "metric4_lbl":"Customers","metric5":"40","metric5_lbl":"Countries",
    "metric6":"#1","metric6_lbl":"Global Electrical Distributor",
    "primary_cloud":"Azure","erp":"SAP S/4HANA · Spark migration","brand_color":"#003087",
    "priorities":[
        ("Spark Digital Platform","Single global ERP & customer experience"),
        ("Sustainable Electrification","EV-charging · solar · grid distributors"),
        ("Branch & Service Excellence","B2B contractor experience modernization"),
        ("Acquisitive Growth","Continued bolt-on M&A globally"),
    ],
    "contacts":[
        ("Philippe Delpech","President & CEO"),
        ("Steven Reinhart","CFO"),
        ("Frédéric Vincent","Chairman"),
        ("Frédéric Dulot","Group CIO"),
    ],
    "scenarios":[
        ("RC-E2E-03","Project-quote pricing optimization","+1.7pp GM",1.8,3.5,"Q1–Q2",25,"wedge"),
        ("ICE-Aftermarket-01","Branch inventory rebalancing across 3K branches","−14% safety stock",1.5,3.0,"Q2",20,"new"),
        ("RC-E2E-04","Contractor-loyalty growth","+18% repeat",1.2,2.5,"Q2–Q3",15,"new"),
        ("RC-E2E-06","Same-day delivery routing","+22% slot util",1.0,2.0,"Q3",10,"new"),
        ("AXLE-Supply-04","Solar / EV-charger supply-chain risk","−18% disruption",0.8,1.6,"Q3",10,"new"),
        ("RC-E2E-07","Procurement-fraud detection · branch","+$5M/yr",0.5,1.2,"Q3–Q4",10,"expansion"),
    ],
})

# ===== FOOD-BEVERAGE (13) =====

CLIENTS.append({
    "ticker":"PEP","name_short":"PepsiCo","name_long":"PepsiCo, Inc.",
    "segment":"Food","sub_path":"Food-Beverage","folder":"PepsiCo",
    "hq":"Purchase, NY · NASDAQ: PEP","revenue":"$91.9B","employees":"318,000",
    "metric3":"~250","metric3_lbl":"Mfg Plants","metric4":"200+",
    "metric4_lbl":"Countries","metric5":"$219B","metric5_lbl":"Market Cap",
    "metric6":"54.5%","metric6_lbl":"Gross Margin",
    "primary_cloud":"Azure","erp":"SAP S/4HANA","brand_color":"#004B93",
    "priorities":[
        ("pep+ Strategy","End-to-end strategic transformation · sustainability"),
        ("North America Beverages","Volume + price-mix recovery · gut-health portfolio"),
        ("Frito-Lay Productivity","Plant automation · digital DSD"),
        ("Healthy Snacking","Permissible-snack innovation · expansion"),
    ],
    "contacts":[
        ("Ramon Laguarta","Chairman & CEO"),
        ("Jamie Caulfield","CFO"),
        ("Athina Kanioura","EVP, Chief Strategy & Transformation Officer"),
        ("David Schwartz","SVP & CIO, PepsiCo Foods NA"),
    ],
    "scenarios":[
        ("AXLE-Ops-03","Frito-Lay line OEE / changeover","+10pp OEE",2.5,5.0,"Q1–Q2",30,"wedge"),
        ("RC-E2E-03","DSD · trade-spend optimization","+1.6pp GM",2.0,4.0,"Q2",20,"new"),
        ("AXLE-Supply-04","Crop-supply risk (potato / corn)","−16% disruption",1.5,3.0,"Q2–Q3",15,"new"),
        ("RC-E2E-06","DSD truck-load optimization","+12% utilization",1.2,2.5,"Q3",10,"new"),
        ("AXLE-QMS-02","Beverage-bottle quality root-cause","−38% escapes",1.0,2.0,"Q3",10,"new"),
        ("RC-E2E-04","Direct-to-consumer (Gatorade / SodaStream)","+18% LTV",0.8,1.6,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"NSRGY","name_short":"Nestlé","name_long":"Nestlé S.A.",
    "segment":"Food","sub_path":"Food-Beverage","folder":"Nestle",
    "hq":"Vevey, Switzerland · OTC: NSRGY","revenue":"$103B (CHF 91B)","employees":"275,000",
    "metric3":"~340","metric3_lbl":"Mfg Plants","metric4":"188",
    "metric4_lbl":"Countries","metric5":"$220B","metric5_lbl":"Market Cap",
    "metric6":"46.9%","metric6_lbl":"Gross Margin",
    "primary_cloud":"Azure","erp":"SAP S/4HANA · GLOBE program","brand_color":"#0066B3",
    "priorities":[
        ("Real Internal Growth","Volume-led growth recovery · pricing normalized"),
        ("Premiumization","Coffee · pet-food · health-science verticals"),
        ("Operational Excellence","Procurement + manufacturing productivity"),
        ("Sustainability","Net-zero by 2050 · regenerative agriculture"),
    ],
    "contacts":[
        ("Laurent Freixe","CEO"),
        ("Anna Manz","CFO"),
        ("Aude Gandon","Global CMO"),
        ("Filippo Catalano","Group CIDO"),
    ],
    "scenarios":[
        ("AXLE-Ops-03","Multi-plant OEE via GLOBE","+9pp OEE",3.0,6.0,"Q1–Q2",30,"wedge"),
        ("AXLE-Supply-04","Coffee / cocoa supplier risk","−16% disruption",2.0,4.0,"Q2",25,"new"),
        ("RC-E2E-03","Premium-coffee category pricing","+1.7pp GM",1.5,3.0,"Q2–Q3",20,"new"),
        ("RC-E2E-09","Perishable / fresh-food waste reduction","−28% loss",1.2,2.5,"Q3",15,"new"),
        ("AXLE-QMS-02","Infant-formula quality assurance","−45% escapes",1.0,2.0,"Q3",15,"new"),
        ("RC-E2E-04","Pet-food DTC personalization","+22% LTV",0.8,1.6,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"KO","name_short":"Coca-Cola","name_long":"The Coca-Cola Company",
    "segment":"Food","sub_path":"Food-Beverage","folder":"Coca-Cola",
    "hq":"Atlanta, GA · NYSE: KO","revenue":"$47.1B","employees":"79,100",
    "metric3":"200+","metric3_lbl":"Brands","metric4":"200+",
    "metric4_lbl":"Countries","metric5":"$285B","metric5_lbl":"Market Cap",
    "metric6":"60.0%","metric6_lbl":"Gross Margin",
    "primary_cloud":"Azure (OpenAI partnership)","erp":"SAP S/4HANA + bottler-partner systems","brand_color":"#F40009",
    "priorities":[
        ("Total Beverage Company","Beyond CSDs · coffee · tea · juice · energy"),
        ("Bottler Partnership","Asset-light system · 200+ bottling partners"),
        ("Generative AI","$1.1B Microsoft partnership · OpenAI applications"),
        ("Marketing Effectiveness","Studio X · creator economy · personalization"),
    ],
    "contacts":[
        ("James Quincey","Chairman & CEO"),
        ("John Murphy","President & CFO"),
        ("Manuel Arroyo","Global CMO"),
        ("Neeraj Tolmare","SVP & Global CIO"),
    ],
    "scenarios":[
        ("RC-E2E-04","Studio X · personalized creative at scale","+24% creative ROI",2.5,5.0,"Q1–Q2",35,"wedge"),
        ("AXLE-Ops-03","Bottler-network OEE benchmarking","+8pp OEE",2.0,4.0,"Q2",25,"new"),
        ("RC-E2E-03","Trade-spend & retail-execution intelligence","+1.5pp GM",1.5,3.0,"Q2–Q3",20,"new"),
        ("AXLE-Supply-04","Sweetener / aluminum supplier risk","−14% disruption",1.2,2.5,"Q3",15,"new"),
        ("RC-E2E-06","Bottler-fleet route optimization","+12% utilization",1.0,2.0,"Q3",15,"new"),
        ("RC-E2E-09","Vending-machine demand forecasting","−24% stockout",0.8,1.6,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"MARS","name_short":"Mars","name_long":"Mars, Incorporated",
    "segment":"Food","sub_path":"Food-Beverage","folder":"Mars",
    "hq":"McLean, VA · Privately held","revenue":"$50B+ (est.)","employees":"150,000",
    "metric3":"~140","metric3_lbl":"Mfg Plants","metric4":"80+",
    "metric4_lbl":"Countries","metric5":"3","metric5_lbl":"Segments",
    "metric6":"#3","metric6_lbl":"Global Confectionery",
    "primary_cloud":"Azure","erp":"SAP S/4HANA","brand_color":"#000000",
    "priorities":[
        ("Mars Pet Nutrition","Royal Canin · IAMS · Pedigree · vet ecosystem"),
        ("Snickers / M&Ms / Skittles","Confectionery brand rejuvenation"),
        ("Sustainable Sourcing","Cocoa / palm oil / dairy commitments"),
        ("Family-Owned Discipline","Long-horizon investment · principles"),
    ],
    "contacts":[
        ("Poul Weihrauch","CEO, Mars"),
        ("Claus Aagaard","Chief Procurement Officer"),
        ("Sandeep Dadlani","Chief Digital & Information Officer"),
        ("Loïc Moutault","President, Mars Snacking"),
    ],
    "scenarios":[
        ("AXLE-Ops-03","Confectionery line OEE","+9pp OEE",2.5,5.0,"Q1–Q2",30,"wedge"),
        ("AXLE-Supply-04","Cocoa / palm-oil sustainable sourcing","−18% disruption",2.0,4.0,"Q2",25,"new"),
        ("RC-E2E-04","Pet-food vet-ecosystem personalization","+22% LTV",1.5,3.0,"Q2–Q3",20,"new"),
        ("RC-E2E-03","Confectionery-category pricing","+1.5pp GM",1.2,2.5,"Q3",15,"new"),
        ("AXLE-QMS-02","Pet-food quality / recall prevention","−42% escapes",1.0,2.0,"Q3",15,"new"),
        ("RC-E2E-06","DSD route & store-execution","+12% utilization",0.8,1.6,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"TSN","name_short":"Tyson","name_long":"Tyson Foods, Inc.",
    "segment":"Food","sub_path":"Food-Beverage","folder":"Tyson_Foods",
    "hq":"Springdale, AR · NYSE: TSN","revenue":"$53.3B","employees":"139,000",
    "metric3":"~140","metric3_lbl":"Plants & Facilities","metric4":"4",
    "metric4_lbl":"Protein Segments","metric5":"$22B","metric5_lbl":"Market Cap",
    "metric6":"5.7%","metric6_lbl":"Gross Margin",
    "primary_cloud":"Azure (announced)","erp":"SAP S/4HANA migration","brand_color":"#D71921",
    "priorities":[
        ("Productivity Program","$1B+ savings · plant network restructure"),
        ("Beef Margin Recovery","Multi-year cattle-cycle response"),
        ("Branded / Prepared Foods","Margin-mix shift · Jimmy Dean / Hillshire / Ball Park"),
        ("AI & Automation","Plant AI · video analytics · workforce safety"),
    ],
    "contacts":[
        ("Donnie King","President & CEO"),
        ("Curt Calaway","CFO"),
        ("Scott Spradley","EVP & CTO"),
        ("Amy Tu","Chief Legal Officer"),
    ],
    "scenarios":[
        ("AXLE-Ops-03","Protein-line yield & first-pass optimization","+8pp yield",2.5,5.0,"Q1–Q2",30,"wedge"),
        ("AXLE-Connected-Factory-01","Predictive maintenance · slaughter & processing","−22% downtime",2.0,4.0,"Q2",25,"new"),
        ("RC-E2E-09","Cold-chain shrink reduction","−18% shrink",1.5,3.0,"Q2–Q3",20,"new"),
        ("AXLE-QMS-02","Food-safety / FSIS audit automation","100% audit trail",1.2,2.5,"Q3",15,"new"),
        ("RC-E2E-03","Branded-foods retail pricing","+1.4pp GM",1.0,2.0,"Q3",10,"new"),
        ("AXLE-Supply-04","Live-animal / feed-supply forecasting","−14% disruption",0.8,1.6,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"ADM","name_short":"ADM","name_long":"Archer-Daniels-Midland",
    "segment":"Food","sub_path":"Food-Beverage","folder":"ADM",
    "hq":"Chicago, IL · NYSE: ADM","revenue":"$85.5B","employees":"42,000",
    "metric3":"~270","metric3_lbl":"Plants & Facilities","metric4":"200+",
    "metric4_lbl":"Countries","metric5":"$26B","metric5_lbl":"Market Cap",
    "metric6":"7.0%","metric6_lbl":"Gross Margin",
    "primary_cloud":"Azure","erp":"SAP S/4HANA","brand_color":"#FFC72C",
    "priorities":[
        ("Nutrition Growth","Animal Nutrition + Human Nutrition specialty growth"),
        ("Ag Services & Oilseeds","Core trading + processing scale"),
        ("Restoring Trust","Post-2024 accounting issues · governance + controls"),
        ("Productivity","$500M cost-savings · plant footprint optimization"),
    ],
    "contacts":[
        ("Juan Luciano","Chairman & CEO"),
        ("Monish Patolawala","CFO"),
        ("Ian Pinner","SVP, Strategy & Chief Commercial Officer"),
        ("Kristy Folkwein","SVP & CIO"),
    ],
    "scenarios":[
        ("AXLE-Ops-03","Soybean / corn processing OEE","+8pp OEE",2.5,5.0,"Q1–Q2",25,"wedge"),
        ("AXLE-Supply-04","Grain-supply / weather risk","−18% disruption",2.0,4.0,"Q2",20,"new"),
        ("RC-E2E-03","Specialty-nutrition pricing","+1.6pp GM",1.5,3.0,"Q2–Q3",15,"new"),
        ("AXLE-QMS-02","Food-ingredient quality assurance","−38% escapes",1.2,2.5,"Q3",15,"new"),
        ("RC-E2E-06","Logistics-optimization · barge/rail/truck","+11% utilization",1.0,2.0,"Q3",10,"new"),
        ("RC-E2E-07","Trading-controls / governance automation","+$10M/yr",0.8,1.6,"Q3–Q4",15,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"CARG","name_short":"Cargill","name_long":"Cargill, Incorporated",
    "segment":"Food","sub_path":"Food-Beverage","folder":"Cargill",
    "hq":"Minneapolis, MN · Privately held","revenue":"$160B (est.)","employees":"160,000",
    "metric3":"~70","metric3_lbl":"Countries","metric4":"~1,100",
    "metric4_lbl":"Locations","metric5":"6","metric5_lbl":"Business Units",
    "metric6":"#1","metric6_lbl":"US Private Co. (Forbes)",
    "primary_cloud":"Azure (Microsoft strategic partnership)","erp":"SAP S/4HANA · multi-instance","brand_color":"#00833F",
    "priorities":[
        ("Margin Optimization","Across volatile commodity cycles · grain · meat · feed"),
        ("Sustainable Food","Regenerative agriculture · Scope-3 commitments"),
        ("Animal Nutrition","Growth in feed-additive specialty segments"),
        ("Operational Excellence","Plant automation · logistics modernization"),
    ],
    "contacts":[
        ("Brian Sikes","President & CEO"),
        ("Joanne Knight","EVP, CFO & Strategy"),
        ("Jennifer Hartsock","CIO & Chief Digital Officer"),
        ("Florian Schattenmann","Chief Technology Officer"),
    ],
    "scenarios":[
        ("AXLE-Supply-04","Global commodity / weather / geo-risk","−18% disruption",3.0,6.0,"Q1–Q2",30,"wedge"),
        ("AXLE-Ops-03","Multi-plant OEE benchmarking","+9pp OEE",2.5,5.0,"Q2",25,"new"),
        ("RC-E2E-03","Animal-nutrition specialty pricing","+1.7pp GM",2.0,4.0,"Q2–Q3",20,"new"),
        ("RC-E2E-09","Cold-chain / spoilage reduction","−24% loss",1.5,3.0,"Q3",15,"new"),
        ("AXLE-QMS-02","Food-grade quality / regulatory","−40% escapes",1.2,2.5,"Q3",15,"new"),
        ("RC-E2E-06","Multi-modal logistics optimization","+12% utilization",1.0,2.0,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"SYY","name_short":"Sysco","name_long":"Sysco Corporation",
    "segment":"Food","sub_path":"Food-Beverage","folder":"Sysco",
    "hq":"Houston, TX · NYSE: SYY","revenue":"$78.8B","employees":"76,000",
    "metric3":"~340","metric3_lbl":"Distribution Sites","metric4":"700K+",
    "metric4_lbl":"Customer Locations","metric5":"$37B","metric5_lbl":"Market Cap",
    "metric6":"18.7%","metric6_lbl":"Gross Margin",
    "primary_cloud":"Azure","erp":"SAP S/4HANA · in-flight migration","brand_color":"#2D6CB4",
    "priorities":[
        ("Recipe for Growth","Outperform foodservice market 1.5x"),
        ("Customer Experience","Sysco Shop · digital ordering · personalization"),
        ("Specialty Growth","Asian · Italian · Mexican specialty acquisition strategy"),
        ("Sales-Force Productivity","CRM modernization · AI-assisted sales"),
    ],
    "contacts":[
        ("Kevin Hourican","Chairman & CEO"),
        ("Kenny Cheung","CFO"),
        ("Tom Bené (Board)","Strategic Advisor"),
        ("Tom Peck","EVP, Chief Information & Digital Officer"),
    ],
    "scenarios":[
        ("RC-E2E-06","Last-mile / delivery-route optimization","+22% slot util",2.5,5.0,"Q1–Q2",30,"wedge"),
        ("RC-E2E-04","Customer-365 cross-sell / next-best-product","+18% LTV",2.0,4.0,"Q2",25,"new"),
        ("RC-E2E-03","Center-of-the-plate margin optimization","+1.6pp GM",1.5,3.0,"Q2–Q3",20,"new"),
        ("RC-E2E-09","Perishable-DC waste reduction","−24% loss",1.2,2.5,"Q3",15,"new"),
        ("AXLE-Supply-04","Specialty supplier performance","−16% disruption",1.0,2.0,"Q3",15,"new"),
        ("RC-E2E-07","Foodservice fraud / chargeback","+$8M/yr",0.8,1.6,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"USFD","name_short":"GFS","name_long":"Gordon Food Service",
    "segment":"Food","sub_path":"Food-Beverage","folder":"Gordon_Food_Service",
    "hq":"Wyoming, MI · Privately held","revenue":"$22B (est.)","employees":"22,000",
    "metric3":"~60","metric3_lbl":"Distribution Centers","metric4":"170+",
    "metric4_lbl":"GFS Stores","metric5":"125+","metric5_lbl":"Years in Business",
    "metric6":"#4","metric6_lbl":"US Foodservice Distributor",
    "primary_cloud":"Azure","erp":"Custom + SAP","brand_color":"#0066B3",
    "priorities":[
        ("Family-Owned Discipline","Long-horizon investment · multi-generational"),
        ("Customer Service","High-touch, family-style customer relationship"),
        ("Geographic Growth","US + Canada expansion · GFS Store retail"),
        ("Operational Excellence","DC automation · last-mile optimization"),
    ],
    "contacts":[
        ("Rich Wolowski","President & CEO"),
        ("Andrew Gordon","Chairman"),
        ("Jeff Corradini","CFO"),
        ("Jen Krippner","Chief Information Officer"),
    ],
    "scenarios":[
        ("RC-E2E-06","Last-mile route optimization","+22% slot util",1.5,3.0,"Q1–Q2",25,"wedge"),
        ("RC-E2E-04","Customer-segment cross-sell","+16% LTV",1.2,2.5,"Q2",20,"new"),
        ("RC-E2E-03","Foodservice category pricing","+1.5pp GM",1.0,2.0,"Q2–Q3",15,"new"),
        ("RC-E2E-09","Perishable-DC waste reduction","−26% loss",0.8,1.6,"Q3",15,"new"),
        ("AXLE-Supply-04","Local-supplier / specialty risk","−14% disruption",0.6,1.4,"Q3",10,"new"),
        ("RC-E2E-05","GFS-Store retail conversion","+10% conv",0.5,1.0,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"BFA","name_short":"Sazerac","name_long":"Sazerac Company",
    "segment":"Food","sub_path":"Food-Beverage","folder":"Sazerac",
    "hq":"New Orleans, LA · Privately held","revenue":"$8B+ (est.)","employees":"8,000+",
    "metric3":"450+","metric3_lbl":"Brands","metric4":"9",
    "metric4_lbl":"Distilleries","metric5":"160+","metric5_lbl":"Countries",
    "metric6":"#2","metric6_lbl":"US Distilled Spirits Co.",
    "primary_cloud":"Azure","erp":"SAP S/4HANA","brand_color":"#A6192E",
    "priorities":[
        ("Premium Bourbon Allocation","Buffalo Trace · Eagle Rare · Pappy · capacity expansion"),
        ("Brand Acquisitions","Continued bolt-on M&A · integration excellence"),
        ("Supply Chain & Aging","Long-cycle inventory management · barrel allocation"),
        ("Distribution Excellence","Three-tier distributor relationship modernization"),
    ],
    "contacts":[
        ("Mark Brown","President & CEO"),
        ("Jake Wenz","COO"),
        ("Andrew Ortmeyer","CFO"),
        ("(Ed. Kirby)","Director, Information Technology"),
    ],
    "scenarios":[
        ("AXLE-Supply-04","Barrel-allocation / aging-inventory forecasting","−18% stockout",1.5,3.0,"Q1–Q2",25,"wedge"),
        ("AXLE-Ops-03","Distillery / bottling-line OEE","+9pp OEE",1.2,2.5,"Q2",20,"new"),
        ("RC-E2E-03","Three-tier distributor pricing intelligence","+1.6pp GM",1.0,2.0,"Q2–Q3",15,"new"),
        ("RC-E2E-04","DTC / consumer-direct (regulatory permitting)","+22% LTV",0.8,1.6,"Q3",10,"new"),
        ("AXLE-QMS-02","Quality control · bottling line","−35% defects",0.7,1.4,"Q3",10,"new"),
        ("RC-E2E-07","Counterfeit-bourbon detection","+$5M/yr",0.5,1.2,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"SGWS","name_short":"Southern Glazer's","name_long":"Southern Glazer's Wine & Spirits",
    "segment":"Food","sub_path":"Food-Beverage","folder":"Southern_Glazers",
    "hq":"Miramar, FL · Privately held","revenue":"$26B+ (est.)","employees":"23,000",
    "metric3":"#1","metric3_lbl":"US Wine & Spirits Distributor","metric4":"45",
    "metric4_lbl":"States","metric5":"450K+","metric5_lbl":"Customer Accounts",
    "metric6":"7,000+","metric6_lbl":"Brand Suppliers",
    "primary_cloud":"Azure","erp":"SAP S/4HANA + Databricks","brand_color":"#A6192E",
    "priorities":[
        ("SGWS-Plus Digital","Ordering · marketplace · customer experience"),
        ("Supplier Partnership","Brand-supplier portal modernization"),
        ("Sales Force Effectiveness","Field-sales AI assistance · route optimization"),
        ("Data & Analytics","Single-source-of-truth · supplier-shareable insights"),
    ],
    "contacts":[
        ("Wayne Chaplin","CEO"),
        ("Kathy Aragon","CFO"),
        ("Christophe Couturier","CIO"),
        ("Jacqueline Gonzalez","Chief HR Officer"),
    ],
    "scenarios":[
        ("RC-E2E-06","On-premise / off-premise route optimization","+22% slot util",2.0,4.0,"Q1–Q2",30,"wedge"),
        ("RC-E2E-04","SGWS-Plus customer cross-sell","+18% repeat",1.5,3.0,"Q2",25,"new"),
        ("RC-E2E-03","Three-tier pricing intelligence","+1.6pp GM",1.2,2.5,"Q2–Q3",20,"new"),
        ("AXLE-Supply-04","Brand-supplier allocation forecasting","−16% stockout",1.0,2.0,"Q3",15,"new"),
        ("RC-E2E-07","Order-fraud / chargeback automation","+$6M/yr",0.8,1.6,"Q3",10,"new"),
        ("RC-E2E-08","Field-sales rep productivity","+12% rep yield",0.5,1.2,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"CFI","name_short":"Christensen Farms","name_long":"Christensen Farms",
    "segment":"Food","sub_path":"Food-Beverage","folder":"Christensen_Farms",
    "hq":"Sleepy Eye, MN · Privately held","revenue":"~$1.5B (est.)","employees":"1,500",
    "metric3":"#5","metric3_lbl":"US Pork Producer","metric4":"~3M",
    "metric4_lbl":"Pigs Marketed/Year","metric5":"7","metric5_lbl":"States",
    "metric6":"~140","metric6_lbl":"Sow Farms",
    "primary_cloud":"Azure","erp":"Microsoft Dynamics 365","brand_color":"#7A2E18",
    "priorities":[
        ("Animal Welfare","Industry-leading welfare standards · audits"),
        ("Operational Excellence","Sow productivity · feed conversion · health"),
        ("Sustainability","Manure-management · methane reduction · regenerative ag"),
        ("Workforce","Rural-labor sourcing · automation"),
    ],
    "contacts":[
        ("Glenn Stolt","CEO"),
        ("Robert Christensen","Chairman"),
        ("(Jeff Spronk)","CFO"),
        ("(Vacant)","CIO / Director IT"),
    ],
    "scenarios":[
        ("ER-OG-03","Sow-farm IoT predictive health agent","+11% productivity",1.0,2.0,"Q1–Q2",25,"wedge"),
        ("AXLE-Connected-Factory-01","Predictive maintenance · feed mill","−22% downtime",0.8,1.6,"Q2",20,"new"),
        ("AXLE-Supply-04","Feed-corn / soy commodity hedging","−14% disruption",0.7,1.4,"Q2–Q3",15,"new"),
        ("AXLE-QMS-02","Welfare-audit & compliance automation","100% audit trail",0.6,1.2,"Q3",15,"new"),
        ("RC-E2E-09","Pork-yield optimization (loss reduction)","−18% shrink",0.5,1.0,"Q3",10,"new"),
        ("RC-E2E-08","Rural-workforce hiring & retention","+12% retention",0.4,0.8,"Q3–Q4",10,"expansion"),
    ],
})

# ===== RETAIL (10) =====

CLIENTS.append({
    "ticker":"WMT","name_short":"Walmart","name_long":"Walmart Inc.",
    "segment":"Retail","sub_path":"Retail","folder":"Walmart",
    "hq":"Bentonville, AR · NYSE: WMT","revenue":"$680.9B","employees":"2,100,000",
    "metric3":"~10,500","metric3_lbl":"Stores Worldwide","metric4":"~255M",
    "metric4_lbl":"Customers Weekly","metric5":"$760B","metric5_lbl":"Market Cap",
    "metric6":"24.4%","metric6_lbl":"Gross Margin",
    "primary_cloud":"Azure + GCP (multi-cloud)","erp":"Custom (built on Azure)","brand_color":"#0071CE",
    "priorities":[
        ("Adaptive Retail","Personalization · seamless DTC + brick"),
        ("Walmart Connect","Advertising business · $4B+ run-rate"),
        ("Marketplace + Fulfillment","3P seller acceleration · WFS"),
        ("Generative AI","Sparky · associate copilots · supplier copilots"),
    ],
    "contacts":[
        ("Doug McMillon","President & CEO"),
        ("John David Rainey","CFO"),
        ("Suresh Kumar","Global Chief Tech / Dev Officer"),
        ("Hari Vasudev","Chief Tech Officer · US"),
    ],
    "scenarios":[
        ("RC-E2E-04","Sparky · personalized shopping copilot","+20% AOV",3.0,6.0,"Q1–Q2",35,"wedge"),
        ("RC-E2E-03","Markdown & promotion optimization","+1.6pp GM",2.5,5.0,"Q2",25,"new"),
        ("RC-E2E-06","Marketplace + WFS routing fusion","+22% slot util",2.0,4.0,"Q2–Q3",20,"new"),
        ("RC-E2E-05","Associate-copilot in-store productivity","+14% task complete",1.5,3.0,"Q3",15,"new"),
        ("RC-E2E-09","Perishable / fresh waste reduction","−28% loss",1.2,2.5,"Q3",15,"new"),
        ("RC-E2E-07","Returns / SCO shrink-detection scale","+$50M/yr",1.0,2.0,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"KR","name_short":"Kroger","name_long":"The Kroger Co.",
    "segment":"Retail","sub_path":"Retail","folder":"Kroger",
    "hq":"Cincinnati, OH · NYSE: KR","revenue":"$147.1B","employees":"414,000",
    "metric3":"~2,720","metric3_lbl":"Supermarkets","metric4":"~62M",
    "metric4_lbl":"Households","metric5":"$48B","metric5_lbl":"Market Cap",
    "metric6":"22.0%","metric6_lbl":"Gross Margin",
    "primary_cloud":"Azure (Microsoft strategic partnership)","erp":"SAP S/4HANA · Databricks","brand_color":"#0F4D92",
    "priorities":[
        ("Customer-First Strategy","84.51° insights · personalization · fresh leadership"),
        ("Boost Membership","Grow loyalty · second-largest after Amazon Prime"),
        ("Alt-Profit Streams","Kroger Precision Marketing · Kroger Personal Finance"),
        ("Generative AI","Microsoft + 84.51° co-development"),
    ],
    "contacts":[
        ("Ron Sargent","Interim CEO (post-McMullen)"),
        ("Todd Foley","CFO"),
        ("Yael Cosset","Chief Information Officer"),
        ("Stuart Aitken","SVP & Chief Merchant & Marketing Officer"),
    ],
    "scenarios":[
        ("RC-E2E-03","Assortment & pricing · localized","+2.4pp GM",3.0,6.0,"Q1–Q2",40,"wedge"),
        ("RC-E2E-04","84.51° loyalty / personalization scale","+18% LTV",2.5,5.0,"Q2",30,"new"),
        ("RC-E2E-09","Perishable waste reduction · grocery","−28% loss",2.0,4.0,"Q2–Q3",25,"new"),
        ("RC-E2E-05","On-shelf availability · fresh / center-store",">98% OSA",1.5,3.0,"Q3",20,"new"),
        ("RC-E2E-06","Boost / pickup slot optimization","+22% slot util",1.2,2.5,"Q3",15,"new"),
        ("RC-E2E-07","SCO + returns shrink detection","+$30M/yr",0.8,1.6,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"COST","name_short":"Costco","name_long":"Costco Wholesale",
    "segment":"Retail","sub_path":"Retail","folder":"Costco",
    "hq":"Issaquah, WA · NASDAQ: COST","revenue":"$254.4B","employees":"333,000",
    "metric3":"~890","metric3_lbl":"Warehouses","metric4":"~136M",
    "metric4_lbl":"Cardholders","metric5":"$430B","metric5_lbl":"Market Cap",
    "metric6":"12.6%","metric6_lbl":"Gross Margin",
    "primary_cloud":"Azure","erp":"Custom mainframe migration","brand_color":"#005DAA",
    "priorities":[
        ("Membership Engine","93%+ renewal · low churn · scale member base"),
        ("Supplier Negotiation","Treasure-hunt assortment · low SKU count"),
        ("E-commerce + Logistics","Costco Logistics · Last-mile · Returns"),
        ("Kirkland Signature","Private-brand growth · ~30% of sales"),
    ],
    "contacts":[
        ("Ron Vachris","President & CEO"),
        ("Gary Millerchip","CFO"),
        ("(Vacant after Vachris)","COO"),
        ("Boris Metodiev","SVP & CIO"),
    ],
    "scenarios":[
        ("RC-E2E-04","Member-renewal predictive uplift","+1pp renewal",2.5,5.0,"Q1–Q2",30,"wedge"),
        ("RC-E2E-03","Treasure-hunt assortment optimization","+1.4pp GM",2.0,4.0,"Q2",25,"new"),
        ("RC-E2E-06","Costco-Logistics last-mile optimization","+22% slot util",1.5,3.0,"Q2–Q3",20,"new"),
        ("RC-E2E-09","Fresh-foods waste reduction","−28% loss",1.2,2.5,"Q3",15,"new"),
        ("RC-E2E-05","Warehouse front-end throughput","+9% throughput",1.0,2.0,"Q3",15,"new"),
        ("RC-E2E-07","Membership / returns-fraud detection","+$15M/yr",0.7,1.4,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"TGT","name_short":"Target","name_long":"Target Corporation",
    "segment":"Retail","sub_path":"Retail","folder":"Target",
    "hq":"Minneapolis, MN · NYSE: TGT","revenue":"$106.6B","employees":"440,000",
    "metric3":"~1,960","metric3_lbl":"Stores","metric4":"~100M",
    "metric4_lbl":"Active Guests","metric5":"$67B","metric5_lbl":"Market Cap",
    "metric6":"28.2%","metric6_lbl":"Gross Margin",
    "primary_cloud":"GCP + Azure","erp":"Custom + SAP migration","brand_color":"#CC0000",
    "priorities":[
        ("Enterprise Acceleration","Multi-year tech & supply-chain modernization"),
        ("Roundel Advertising","$2B+ run-rate retail-media business"),
        ("Owned Brands","Good & Gather · Cat & Jack · ~$30B+"),
        ("Drive-Up / Same-Day","Fulfillment from store · Drive-Up scale"),
    ],
    "contacts":[
        ("Brian Cornell","CEO"),
        ("Jim Lee","CFO"),
        ("Prat Vemana","CIO"),
        ("Cara Sylvester","EVP, CMO & Digital Officer"),
    ],
    "scenarios":[
        ("RC-E2E-04","Roundel + Circle 360 personalization","+18% LTV",2.5,5.0,"Q1–Q2",30,"wedge"),
        ("RC-E2E-03","Owned-brand pricing / margin optimization","+1.6pp GM",2.0,4.0,"Q2",25,"new"),
        ("RC-E2E-06","Drive-Up / Same-Day routing","+22% slot util",1.5,3.0,"Q2–Q3",20,"new"),
        ("RC-E2E-05","Store-team-member copilot","+12% task complete",1.2,2.5,"Q3",15,"new"),
        ("RC-E2E-07","Loss-prevention / SCO shrink detection","+$25M/yr",1.0,2.0,"Q3",10,"new"),
        ("RC-E2E-09","Fresh-foods waste reduction","−24% loss",0.8,1.6,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"HD","name_short":"Home Depot","name_long":"The Home Depot, Inc.",
    "segment":"Retail","sub_path":"Retail","folder":"Home_Depot",
    "hq":"Atlanta, GA · NYSE: HD","revenue":"$159.5B","employees":"475,000",
    "metric3":"~2,340","metric3_lbl":"Stores","metric4":"~1B",
    "metric4_lbl":"Customer Trips","metric5":"$390B","metric5_lbl":"Market Cap",
    "metric6":"33.4%","metric6_lbl":"Gross Margin",
    "primary_cloud":"GCP + Azure","erp":"SAP + custom","brand_color":"#F96302",
    "priorities":[
        ("Pro Customer","Pro-segment growth · SRS Distribution acquisition"),
        ("Interconnected Retail","One Home Depot experience · digital + store"),
        ("Supply Chain","Store-WD, Distribution Centers, Direct Fulfillment Centers"),
        ("Generative AI","Magic Apron · associate copilots · supplier"),
    ],
    "contacts":[
        ("Ted Decker","Chair, President & CEO"),
        ("Richard McPhail","CFO"),
        ("Fahim Siddiqui","EVP & CIO"),
        ("Chip Devine","SVP, Outside Sales (Pro)"),
    ],
    "scenarios":[
        ("RC-E2E-04","Pro-customer (SRS) cross-sell agent","+18% repeat",2.5,5.0,"Q1–Q2",30,"wedge"),
        ("RC-E2E-03","Pro-quote pricing optimization","+1.5pp GM",2.0,4.0,"Q2",25,"new"),
        ("RC-E2E-06","Direct-Fulfillment-Center routing","+22% slot util",1.5,3.0,"Q2–Q3",20,"new"),
        ("RC-E2E-05","Store-associate Magic-Apron copilot","+14% task complete",1.2,2.5,"Q3",15,"new"),
        ("AXLE-Supply-04","Building-products supplier risk","−16% disruption",1.0,2.0,"Q3",10,"new"),
        ("RC-E2E-07","Theft / ORC reduction · scale","+$30M/yr",0.8,1.6,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"AD","name_short":"Ahold Delhaize","name_long":"Ahold Delhaize USA / Group",
    "segment":"Retail","sub_path":"Retail","folder":"Ahold_Delhaize",
    "hq":"Zaandam, NL / Quincy, MA · AMS: AD","revenue":"€89B (~$95B)","employees":"~393,000",
    "metric3":"~7,700","metric3_lbl":"Stores","metric4":"~63M",
    "metric4_lbl":"Customers Weekly","metric5":"€34B","metric5_lbl":"Market Cap",
    "metric6":"27.0%","metric6_lbl":"Gross Margin",
    "primary_cloud":"Azure + GCP","erp":"SAP S/4HANA","brand_color":"#0079BF",
    "priorities":[
        ("Growing Together","2024–2028 strategy · own-brand growth · DTC"),
        ("Omnichannel","Bol.com · Stop & Shop · Hannaford · Food Lion · Giant"),
        ("Personalization","Loyalty + bonus-card data · 80% of sales"),
        ("Sustainability","Healthy & sustainable food · Scope-3 commitments"),
    ],
    "contacts":[
        ("Frans Muller","CEO"),
        ("Jolanda Poots-Bijl","CFO"),
        ("Luc Vandenboer","EVP, Chief Digital Officer (USA)"),
        ("Wojciech Pawluk","Chief Procurement Officer"),
    ],
    "scenarios":[
        ("RC-E2E-04","Bonus-card personalization · multi-banner","+18% LTV",2.5,5.0,"Q1–Q2",30,"wedge"),
        ("RC-E2E-03","Localized assortment · 5+ banner banners","+1.7pp GM",2.0,4.0,"Q2",25,"new"),
        ("RC-E2E-09","Perishable waste · multi-banner","−28% loss",1.5,3.0,"Q2–Q3",20,"new"),
        ("RC-E2E-06","Click-and-collect / home-delivery routing","+22% slot util",1.2,2.5,"Q3",15,"new"),
        ("RC-E2E-05","Front-end OSA / wait-time optimization","−24% wait",1.0,2.0,"Q3",15,"new"),
        ("RC-E2E-07","SCO + returns shrink detection","+$20M/yr",0.7,1.4,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"M","name_short":"Macy's","name_long":"Macy's, Inc.",
    "segment":"Retail","sub_path":"Retail","folder":"Macys",
    "hq":"New York, NY · NYSE: M","revenue":"$23.1B","employees":"85,400",
    "metric3":"~720","metric3_lbl":"Stores (3 banners)","metric4":"~30M",
    "metric4_lbl":"Active Customers","metric5":"$3.7B","metric5_lbl":"Market Cap",
    "metric6":"40.3%","metric6_lbl":"Gross Margin",
    "primary_cloud":"Azure","erp":"Oracle Retail · in transition","brand_color":"#E31837",
    "priorities":[
        ("Bold New Chapter","Close ~150 underperforming Macy's · invest in 350 First-50"),
        ("Bloomingdale's / Bluemercury","Luxury growth · expansion store openings"),
        ("Marketplace","3P marketplace expansion · Mirakl-powered"),
        ("Private Brands","On-the-Move · Beam · Charter Club refresh"),
    ],
    "contacts":[
        ("Tony Spring","President & CEO"),
        ("Adrian Mitchell","CFO & COO"),
        ("Laura Miller","Chief Information Officer"),
        ("Jennifer Kasper","EVP, Brand Marketing"),
    ],
    "scenarios":[
        ("RC-E2E-03","First-50-store assortment & pricing","+1.8pp GM",1.5,3.0,"Q1–Q2",25,"wedge"),
        ("RC-E2E-04","Customer-segment loyalty (3 banners)","+16% LTV",1.2,2.5,"Q2",20,"new"),
        ("RC-E2E-05","Bluemercury clienteling agent","+10pp NPS",1.0,2.0,"Q2–Q3",15,"new"),
        ("RC-E2E-06","Cross-banner fulfillment optimization","+22% slot util",0.8,1.6,"Q3",10,"new"),
        ("RC-E2E-07","Returns-fraud detection · DTC","+$10M/yr",0.7,1.4,"Q3",10,"new"),
        ("RC-E2E-09","Perishable / aging-inventory markdown","+1.4pp GM",0.5,1.0,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"TJX","name_short":"TJX","name_long":"The TJX Companies",
    "segment":"Retail","sub_path":"Retail","folder":"TJX_Companies",
    "hq":"Framingham, MA · NYSE: TJX","revenue":"$56.4B","employees":"360,000",
    "metric3":"~5,000","metric3_lbl":"Stores","metric4":"6",
    "metric4_lbl":"Banners","metric5":"$140B","metric5_lbl":"Market Cap",
    "metric6":"30.6%","metric6_lbl":"Gross Margin",
    "primary_cloud":"Azure","erp":"Custom + SAP","brand_color":"#E11B22",
    "priorities":[
        ("Off-Price Treasure Hunt","Buying-organization scale · 21K+ vendors"),
        ("Marshalls / TJ Maxx / HomeGoods","US banner growth · Sierra · Homesense"),
        ("International Growth","Europe · Australia · TK Maxx"),
        ("Inventory Velocity","Rapid turn · scarcity-driven shopping"),
    ],
    "contacts":[
        ("Ernie Herrman","President & CEO"),
        ("John Klinger","CFO"),
        ("(Vacant)","EVP, COO"),
        ("Carol Meyrowitz","Executive Chairman"),
    ],
    "scenarios":[
        ("RC-E2E-03","Off-price markdown velocity / margin","+1.6pp GM",2.0,4.0,"Q1–Q2",25,"wedge"),
        ("RC-E2E-06","Multi-banner allocation / replenishment","−12% safety stock",1.5,3.0,"Q2",20,"new"),
        ("RC-E2E-04","Loyalty + customer segment (TJX Rewards)","+14% repeat",1.2,2.5,"Q2–Q3",15,"new"),
        ("AXLE-Supply-04","Vendor-network risk · 21K vendors","−14% disruption",1.0,2.0,"Q3",10,"new"),
        ("RC-E2E-05","Store-throughput / queue management","−22% wait",0.7,1.4,"Q3",10,"new"),
        ("RC-E2E-07","Returns-fraud + ORC detection","+$20M/yr",0.5,1.2,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"EBAY","name_short":"eBay","name_long":"eBay Inc.",
    "segment":"Retail","sub_path":"Retail","folder":"eBay",
    "hq":"San Jose, CA · NASDAQ: EBAY","revenue":"$10.3B","employees":"11,200",
    "metric3":"~134M","metric3_lbl":"Active Buyers","metric4":"~1.9B",
    "metric4_lbl":"Live Listings","metric5":"$28B","metric5_lbl":"Market Cap",
    "metric6":"71.7%","metric6_lbl":"Gross Margin",
    "primary_cloud":"GCP","erp":"Custom","brand_color":"#E53238",
    "priorities":[
        ("Focus Categories","P&A · Refurbished · Trading Cards · Sneakers · Watches"),
        ("AI Listing & Discovery","Generative listing creation · GenAI search"),
        ("Advertising","Promoted Listings · advertising business growth"),
        ("Trust & Authentication","Authentication Guarantee · counterfeit prevention"),
    ],
    "contacts":[
        ("Jamie Iannone","CEO"),
        ("Steve Priest","CFO"),
        ("Mazen Rawashdeh","CTO"),
        ("Derek Allgood","SVP & Chief Customer Service Officer"),
    ],
    "scenarios":[
        ("RC-E2E-04","Buyer-discovery / personalization GenAI","+18% conv",2.0,4.0,"Q1–Q2",30,"wedge"),
        ("RC-E2E-07","Counterfeit / authentication agent","+$25M/yr",1.5,3.0,"Q2",25,"new"),
        ("RC-E2E-03","Promoted-Listing / pricing optimization","+1.6pp GM",1.2,2.5,"Q2–Q3",20,"new"),
        ("RC-E2E-04","Listing-quality automation (seller side)","+14% sell-through",1.0,2.0,"Q3",15,"new"),
        ("RC-E2E-06","Cross-border logistics optimization","+22% slot util",0.7,1.4,"Q3",10,"new"),
        ("RC-E2E-08","Customer-service contact deflection","−24% AHT",0.5,1.2,"Q3–Q4",10,"expansion"),
    ],
})

CLIENTS.append({
    "ticker":"DEMOS","name_short":"Demos","name_long":"Demos Restaurants",
    "segment":"Retail","sub_path":"Retail","folder":"Demos",
    "hq":"Lebanon, TN · Privately held","revenue":"~$65M (est.)","employees":"800+",
    "metric3":"7","metric3_lbl":"Restaurants","metric4":"35+",
    "metric4_lbl":"Years in Business","metric5":"Family-owned","metric5_lbl":"Status",
    "metric6":"~3M","metric6_lbl":"Customers/Year",
    "primary_cloud":"Azure (M365)","erp":"Microsoft Dynamics 365 BC","brand_color":"#8B0000",
    "priorities":[
        ("Family Brand","Steakhouse · Italian · Mediterranean · classic concepts"),
        ("Operational Excellence","Restaurant cost control · labor + food cost"),
        ("Digital Ordering","Online + delivery integration"),
        ("Loyalty","Demos Rewards · repeat-customer program"),
    ],
    "contacts":[
        ("Peter Demos","President"),
        ("(Owner Family)","Demos Family Ownership"),
        ("(Director Ops)","Director, Restaurant Operations"),
        ("(Marketing Lead)","Marketing & Loyalty Lead"),
    ],
    "scenarios":[
        ("RC-E2E-04","Demos-Rewards loyalty personalization","+18% repeat",0.4,0.8,"Q1–Q2",25,"wedge"),
        ("RC-E2E-09","Food-cost & waste optimization","−24% loss",0.3,0.7,"Q2",20,"new"),
        ("RC-E2E-08","Labor-scheduling / shift optimization","−18% labor cost",0.3,0.6,"Q2–Q3",15,"new"),
        ("RC-E2E-03","Menu-engineering / margin optimization","+1.5pp GM",0.2,0.5,"Q3",15,"new"),
        ("RC-E2E-05","Front-of-house guest-experience agent","+8pp NPS",0.2,0.4,"Q3",10,"new"),
        ("AXLE-Supply-04","Beef / produce supplier risk","−12% disruption",0.1,0.3,"Q3–Q4",10,"expansion"),
    ],
})


# ---------------------------------------------------------------------------
# HTML template
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
        return f"${lo*1000:.0f}K–${hi*1000:.0f}K"
    return f"${lo:.1f}–{hi:.1f}M"


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
        # Range string
        if lo < 1:
            value_str = f"${int(lo*1000)}K–${int(hi*1000)}K"
        else:
            value_str = f"${lo:.1f}–{hi:.1f}M"
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
         f"Establish APEX substrate on {client['primary_cloud']}: SOR connectors → Bronze landing → Silver canonical "
         f"(MERML / SCML schemas) → LEDGER 14-field audit row store. Wire MCP server, Entra identities, "
         f"Adaptive-Card HITL surface in Teams. BVA-funded discovery + first-scenario assessment."),
        ("Wave 2 · Pilot (you are here)", "W2 · Q2–Q3 FY27",
         f"Stand up the marquee scenario for the highest-value functional area &mdash; "
         f"<strong>{SERVICE_NAMES.get(client['scenarios'][0][0], client['scenarios'][0][0])}</strong>. "
         f"6-agent fleet: Assess &middot; Classify &middot; Quantify &middot; Approve &middot; Act &middot; Evidence-Write. "
         f"Sequential-with-HITL-gate orchestration. KPI: <strong>{client['scenarios'][0][2]}</strong>."),
        ("Wave 3 · Scale & Fuse", "W3 · Q3–Q4 FY27",
         "Expand to adjacent scenarios across the same functional area &middot; cross-banner / multi-region rollout &middot; "
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
    if "AWS" in primary:
        risks.append(("high", "AWS-primary cloud", "APEX Decision/Runtime planes are Microsoft-native; position as workload-specific COEXIST + Foundry agentic on AWS data-lake feeds"))
    elif "GCP" in primary:
        risks.append(("high", "GCP-primary cloud", "APEX Decision/Runtime planes are Microsoft-native; position as agentic workload on existing data foundation"))
    else:
        risks.append(("low", "Azure-aligned", "Primary cloud is Azure &mdash; APEX runs natively on Microsoft platform"))
    risks.append(("medium", "ERP modernization in flight", f"{client['erp']} migration may compress capacity; sequence APEX behind ERP cutover"))
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
        # Build agent fleet
        agents = "Assess · Classify · Quantify · Approve · Act · Evidence-Write".split(" · ")
        agent_pills = "".join(f'<span class="agent-pill">{a}</span>' for a in agents)
        if lo < 1:
            value_str = f"${int(lo*1000)}K–${int(hi*1000)}K"
        else:
            value_str = f"${lo:.1f}M–${hi:.1f}M"
        out.append(f"""
<div class="modal-overlay" id="{modal_id}">
  <div class="modal-box">
    <div class="mh"><div><div class="mh-title">{_esc(title)}</div>
      <div class="mh-sub">{code} &middot; {_esc(svc_name)} &middot; {value_str} &middot; {tag.upper()}</div></div>
      <button class="mclose" onclick="closeModal('{modal_id}')">&#10005;</button></div>
    <div class="mb">
      <h4>Functional Area &amp; Business Moment</h4>
      <p><strong>{_esc(fa)}</strong> &mdash; This scenario fires when the operational signal arrives at the SOR (POS, ERP, IoT, CRM, WMS depending on functional area). APEX agents take it from event &rarr; bounded mutation with full LEDGER audit. Target KPI uplift: <strong>{_esc(kpi)}</strong>.</p>

      <h4>APEX 6-Agent Fleet</h4>
      <div class="agent-row">{agent_pills}</div>
      <p style="margin-top:8px">Sequential orchestration with a Teams Adaptive-Card HITL gate before any material mutation. Every action emits a 14-field audit row to the LEDGER plane &mdash; drillable from KPI &rarr; trace_id &rarr; reasoning trace.</p>

      <h4>KPI Uplift Chain</h4>
      <ul>
        <li><strong>Wave 1 ({client['primary_cloud']} foundation):</strong> SOR &rarr; Bronze &rarr; Silver canonical. KPI baseline established.</li>
        <li><strong>Wave 2 (pilot):</strong> {_esc(kpi)} on the first cohort &middot; sequential agents with HITL gate &middot; Teams notification.</li>
        <li><strong>Wave 3 (scale &amp; fuse):</strong> Cross-banner / multi-region run-rate &middot; A2A fusion with adjacent scenarios &middot; LEDGER-fed retraining.</li>
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
    # Total opportunity
    total_lo = sum(s[3] for s in client["scenarios"])
    total_hi = sum(s[4] for s in client["scenarios"])
    if total_lo < 1:
        total_str = f"${int(total_lo*1000)}K–${int(total_hi*1000)}K"
    else:
        total_str = f"${total_lo:.1f}–{total_hi:.1f}M"

    # Chart data
    fa_map = {}
    for code, _, _, lo, hi, *_ in client["scenarios"]:
        fa = FUNCTIONAL_AREA.get(code, "Other").split(" · ")[-1]
        fa_map.setdefault(fa, [0,0])
        fa_map[fa][0] += lo; fa_map[fa][1] += hi
    fa_labels = list(fa_map.keys())
    fa_lows = [v[0] for v in fa_map.values()]
    fa_ups = [v[1]-v[0] for v in fa_map.values()]

    # Scenario value data for chart 1
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
    <a href="{client['name_short'].replace(' ','')}_APEX_OnePager.html" style="padding:6px 14px;font-size:11px;font-weight:600;text-decoration:none;color:#86BC25;border-bottom:2px solid #86BC25;background:rgba(134,188,37,.1);font-family:'DM Sans',sans-serif;display:inline-block;">APEX Agentic AI Services</a>
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
    print(f"Building APEX Agentic AI OnePagers for {len(CLIENTS)} Consumer clients...\n")
    written = 0
    for client in CLIENTS:
        out_dir = CONSUMER_ROOT / client["sub_path"] / client["folder"] / "01_account" / "one_pager"
        out_dir.mkdir(parents=True, exist_ok=True)
        # File name: <NameShort with no spaces>_APEX_OnePager.html (ASCII-safe)
        import unicodedata
        nfkd = unicodedata.normalize("NFKD", client["name_short"])
        ascii_name = "".join(c for c in nfkd if not unicodedata.combining(c))
        fname = ascii_name.replace(" ", "").replace(".", "").replace("'", "")
        out_path = out_dir / f"{fname}_APEX_OnePager.html"
        try:
            html_text = build_html(client)
            out_path.write_text(html_text, encoding="utf-8")
            print(f"  [{client['segment']}] {client['name_short']:25s} -> {out_path.name}  ({len(html_text):,} chars)")
            written += 1
        except Exception as e:
            print(f"  [{client['segment']}] {client['name_short']:25s} -> ERROR: {e}")
    print(f"\nDone. {written}/{len(CLIENTS)} OnePagers written.")


if __name__ == "__main__":
    main()
