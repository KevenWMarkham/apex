"""Classify every scenario into a functional domain and preview distribution.

Dry-run: does NOT move any folders. Prints the distribution per practice so the
user can confirm (or tune) the taxonomy before we execute the reorganization.
"""

from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path("docs/scenarios")
library = json.load(open(ROOT / "_catalog" / "scenario-library.json", encoding="utf-8"))
chains = json.load(open(ROOT / "_catalog" / "featured-chains.json", encoding="utf-8"))

# --------------------------------------------------------------------------
# Functional domain taxonomy — 12 domains, scored keyword rules.
# Every domain gets a score for each scenario; highest score wins.
# This avoids the "first-match-steals" ordering problem.
# --------------------------------------------------------------------------
DOMAINS = [
    ("clinical-care",
     "Clinical & Care",
     [
        r"\bclinical\b", r"\bpatient\b", r"\btriage\b", r"\bsepsis\b", r"\bicu\b",
        r"\boncolog", r"\bradiolog", r"\bdiagnos", r"\bhedis\b", r"\bcare gap\b",
        r"\breadmit", r"\bclinical trial\b", r"\bcohort\b", r"\bhl7\b", r"\bcdi\b",
        r"\bade\b", r"\badverse (event|drug)", r"\bdenial\b", r"\bprior auth",
        r"\badherence\b", r"\brx\b", r"\bmedicat", r"\bpharmacy benefit",
        r"\butilization mgmt\b", r"\bpopulation health\b", r"\bformulary\b",
        r"\bprovider\b", r"\bpayer\b", r"\bvalue-based\b", r"\bvbc\b",
        r"\bhospice\b", r"\bscreening\b", r"\bpreventive-screening\b",
        r"\bdischarge\b", r"\bcaseload\b", r"\bcare-manager\b", r"\bcredentialing\b",
        r"\bbiomarker\b", r"\bbiospecimen\b", r"\bbiolog", r"\bdrug\b",
        r"\b(bundled|direct)-contract", r"\bbundled-payment\b",
        r"\bicd\b", r"\bcpt\b", r"\bmips\b", r"\bacuity\b",
        r"\bcommunity-resource\b", r"\bbenefit-plan\b", r"\bmember\b",
        r"\blab\b", r"\bemr\b", r"\behr\b", r"\bedvisit\b",
        r"\badverse-event\b", r"\bopioid\b", r"\bpressure-injury\b",
        r"\bdevice-utilization\b", r"\bppe-demand\b",
     ]),

    ("network-infrastructure",
     "Network & Infrastructure",
     [
        r"\bnetwork\b", r"\bfault predict", r"\boutage\b", r"\bcell site",
        r"\b5g\b", r"\bspectrum\b", r"\boss\b", r"\bbss\b", r"\bfiber\b",
        r"\bcapacity plan", r"\bcdn\b", r"\bstreaming quality\b", r"\bqoe\b",
        r"\bbandwidth\b", r"\blatency\b", r"\bpacket\b",
        r"\bgrid\b", r"\bsubstation\b", r"\btransformer\b", r"\bsmart meter\b",
        r"\bscada\b", r"\bdistribution outage\b", r"\btransmission\b",
        r"\bline-loss\b", r"\bline loss\b", r"\bpeaker\b", r"\bdemand response\b",
        r"\bload forecast\b", r"\brenewable\b",
        r"\bpipeline\b", r"\bleak detect", r"\bintegrity\b", r"\brefinery\b",
        r"\bwellhead\b", r"\bdrilling\b", r"\bupstream\b", r"\bdownstream\b",
        r"\bmidstream\b", r"\bflaring\b", r"\bemission", r"\bcell-site\b",
     ]),

    ("engineering-rd",
     "Engineering & R&D",
     [
        r"\bcad\b", r"\bbom\b", r"\bbill-of-material\b", r"\bbill of material",
        r"\bdesign\b", r"\bdfm\b", r"\bdesign-for-manufactur",
        r"\bconfigurator\b", r"\bengineering-change\b", r"\bengineering-spec\b",
        r"\b8d\b", r"\bdigital-twin\b", r"\bcapa\b", r"\bpart-serialization\b",
        r"\bgauge-r&r\b", r"\br&d\b", r"\bprototype\b", r"\blab\b",
        r"\bresearch and development\b", r"\btest-case generat",
        r"\bergonomic\b", r"\barc-flash\b", r"\btolerance\b",
        r"\bspec matching\b", r"\bspec-matching\b", r"\bpart-commonality\b",
        r"\bcomponent-commonality\b", r"\bmanufacturing-yield\b",
        r"\bab-test\b", r"\bfeature-flag\b", r"\bnew-product\b",
        r"\blaunch-readiness\b", r"\bliterature-review\b", r"\bresearch-grant\b",
        r"\bpublication-impact\b", r"\bsite-feasibility\b", r"\bcommissioning\b",
        r"\bdeveloper-relations\b", r"\bidentity-access-review\b",
     ]),

    ("supply-chain",
     "Supply Chain & Inventory",
     [
        r"\bsupply\b", r"\binventory\b", r"\bstockout\b", r"\boos\b",
        r"\bout-of-stock\b", r"\breplenish", r"\bprocure", r"\bsupplier\b",
        r"\bsourcing\b", r"\blogistics\b", r"\bwarehouse\b", r"\bfulfillment\b",
        r"\bshipment\b", r"\bfreight\b", r"\b3pl\b", r"\botif\b",
        r"\bbopis\b", r"\bclick-and-collect\b", r"\blast-mile\b",
        r"\bbackhaul\b", r"\bload\b", r"\bcarrier\b",
        r"\bsku\b", r"\bassortment\b", r"\bplan-o-gram\b", r"\ballocation\b",
        r"\bdistribution center\b", r"\bperishable\b", r"\bcold.chain\b",
        r"\bexpir", r"\bshrink\b", r"\breceiving\b", r"\bcrossdock\b",
        r"\bdispatch\b", r"\bnew-item\b", r"\bnew-market\b",
        r"\bshelving\b", r"\bmanufacturer-demand\b",
        r"\bdemand forecast", r"\bshipping-cost\b", r"\bpack-size\b",
        r"\bgrab-and-go\b", r"\border-picking\b", r"\bline-balancing\b",
        r"\bplant-capacity\b", r"\bkanban\b", r"\bfuel-tank-level\b",
        r"\bon-rent\b", r"\boff-rent\b", r"\basset-rotation\b",
        r"\breservoir-production\b", r"\bore-grade\b",
     ]),

    ("asset-maintenance",
     "Asset, Maintenance & Reliability",
     [
        r"\bpredictive maint", r"\bmaintenance\b", r"\breliability\b",
        r"\buptime\b", r"\bdowntime\b", r"\boee\b", r"\bmtbf\b", r"\bmttr\b",
        r"\bwear\b", r"\bbearing\b", r"\bvibration\b", r"\bspare part\b",
        r"\bfield service\b", r"\bdispatch optim\b",
        r"\brebuild\b", r"\boverhaul\b", r"\bfleet\b", r"\btelemetry\b",
        r"\bsensor drift\b", r"\biot anomaly\b", r"\baog\b",
        r"\baircraft on ground\b", r"\besp\b", r"\bboiler-tube\b",
        r"\bartificial-lift\b", r"\bgas-lift\b", r"\bcompressor\b",
        r"\bheat-exchanger\b", r"\bhydraulic\b", r"\bfrac-completion\b",
        r"\bcatalyst-performance\b", r"\bpump\b", r"\bturbine\b",
        r"\bequipment\b", r"\bindustrial-iot\b", r"\balarm suppression\b",
     ]),

    ("quality-compliance",
     "Quality, Compliance & Regulatory",
     [
        r"\bquality\b", r"\bdefect\b", r"\bscrap\b", r"\brework\b",
        r"\bfirst-pass yield\b", r"\bfpy\b", r"\bspc\b", r"\bstatistical process",
        r"\baudit\b", r"\bcompliance\b", r"\bregulatory\b", r"\bregulator\b",
        r"\bfda\b", r"\bferc\b", r"\benvironment\b", r"\bemissions?\b",
        r"\bjoint commission\b", r"\baccred", r"\bhipaa\b", r"\bgdpr\b",
        r"\bpci\b", r"\bsox\b", r"\besg\b", r"\bsustainab",
        r"\bviolation\b", r"\bfine\b", r"\bsafety\b", r"\bhazard\b",
        r"\bosha\b", r"\bnear-miss\b", r"\bincident report",
        r"\bquality escape\b", r"\broot-cause\b", r"\bwarranty claim\b",
        r"\brecall\b", r"\bfsma\b", r"\biso\b", r"\b6 sigma\b", r"\blean\b",
        r"\bhot-work-permit\b", r"\bcompressed-air-leak\b",
        r"\bcarbon-credit\b", r"\bcoding-accuracy\b", r"\bcharge-capture\b",
     ]),

    ("risk-fraud-security",
     "Risk, Fraud & Security",
     [
        r"\bfraud\b", r"\baml\b", r"\banti-money\b", r"\bkyc\b",
        r"\bknow-your\b", r"\bcredit risk\b", r"\bunderwrit", r"\brisk scoring\b",
        r"\breturns fraud\b", r"\bclaims fraud\b", r"\bad fraud\b",
        r"\bwarranty fraud\b", r"\binvoice fraud\b",
        r"\bcyber", r"\bsecurity\b", r"\bthreat\b", r"\bmalware\b",
        r"\bphishing\b", r"\bdata exfil", r"\bvulnerability\b",
        r"\bfraud ring\b", r"\bidentity theft\b", r"\bsynthetic\b",
        r"\bbot detect", r"\baccount takeover\b", r"\baccount-sharing\b",
        r"\bchargeback\b", r"\bdispute\b", r"\bfraud detect", r"\bsoc alert\b",
        r"\bdata-exfiltration\b", r"\brevenue-protection\b", r"\btheft detect",
     ]),

    ("pricing-revenue",
     "Pricing, Revenue & Margin",
     [
        r"\bpricing\b", r"\bmarkdown\b", r"\bmargin\b", r"\brevenue mgmt\b",
        r"\brevenue management\b", r"\byield mgmt\b", r"\byield management\b",
        r"\belasticity\b", r"\brevpar\b", r"\badr\b", r"\barpu\b", r"\barr\b",
        r"\bnrr\b", r"\bexpansion arr\b",
        r"\bdynamic pric", r"\bpromotional pric", r"\bancillary revenue\b",
        r"\bbilling\b", r"\bgross margin\b", r"\bcontribution margin\b",
        r"\bbundle pric", r"\brate card\b", r"\bupsell\b", r"\bcross-sell\b",
        r"\bsubscription\b", r"\bfare\b", r"\bprofitability\b",
        r"\bconcessionaire revenue\b", r"\bm&a\b", r"\bfinancial-counseling\b",
        r"\boverbooking\b", r"\blength-of-stay\b", r"\blounge-capacity\b",
        r"\bpremium-cabin\b", r"\bpoints-redemption\b", r"\bpackage-holiday\b",
        r"\blocation-demand\b", r"\bplant-.*pl\b", r"\bcost-variance\b",
        r"\bbid-proposal\b", r"\bgovernment.*bid\b", r"\bpaid-search-bid\b",
        r"\bdeal-forecast\b", r"\bhigh-cost-claimant\b",
     ]),

    ("customer-experience",
     "Customer Experience & Loyalty",
     [
        r"\bcustomer\b", r"\bcx\b", r"\bloyalty\b", r"\bchurn\b", r"\bwinback\b",
        r"\bretention\b", r"\bpersonaliz", r"\brecommend", r"\bsegmentation\b",
        r"\bcart abandon", r"\bnps\b", r"\bcsat\b", r"\bsentiment\b",
        r"\bcontact center\b", r"\bchatbot\b", r"\baht\b", r"\bfcr\b",
        r"\bself-service\b", r"\bvoice of customer\b", r"\bvoc\b",
        r"\bcdp\b", r"\bcustomer.360\b", r"\bnext-best-action\b",
        r"\bguest\b", r"\btraveler\b", r"\bpassenger\b",
        r"\bcomplaint\b", r"\brefund\b", r"\bservice recovery\b",
        r"\birops\b", r"\bpnr\b", r"\bfeedback-survey\b",
        r"\bdisruption-communication\b", r"\belite-requalification\b",
        r"\bdischarge-education\b", r"\bbill-shock\b",
        r"\bcart-abandon", r"\bdamage-inspection\b", r"\bin-stay-issue\b",
        r"\breview-response\b", r"\bcrisis-response\b",
        r"\bknowledge-base-search\b", r"\blive-commerce\b",
        r"\bfamily-plan-optimization\b",
     ]),

    ("marketing-growth",
     "Marketing & Growth",
     [
        r"\bmarketing\b", r"\bcampaign\b", r"\battribution\b",
        r"\bchannel mix\b", r"\bmedia mix\b", r"\bmmm\b",
        r"\bacquisition\b", r"\bbrand\b", r"\bsentiment track",
        r"\bsocial signal\b", r"\bcontent recommend", r"\bseo\b", r"\bsem\b",
        r"\bpaid media\b", r"\bprogrammatic\b", r"\bcreative\b",
        r"\baudience\b", r"\blookalike\b", r"\bpropensity\b",
        r"\blead gen", r"\bmql\b", r"\bactivation\b",
        r"\bpromo\b", r"\bcoupon\b",
        r"\bad-copy\b", r"\bemail subject-line\b", r"\bcompetitor-mention\b",
        r"\bcontent-metadata\b", r"\bcontent-cold-start\b",
        r"\bmedia-mix\b", r"\bend-cap\b", r"\bcompetitor-rate-shop\b",
        r"\bsports-highlight\b", r"\bhighlight auto-generation\b",
        r"\bcommunity-content-moderation\b", r"\bcontent-catalog\b",
        r"\bmarket-cannibalization\b", r"\bcategory-role\b",
        r"\bcompetitive-opening\b", r"\bpromotional-lift\b",
        r"\bkey-opinion-leader\b", r"\bkol\b", r"\bprivate-label\b",
        r"\bplant-performance-benchmark\b",
     ]),

    ("operations-workforce",
     "Operations & Workforce",
     [
        r"\boperations\b", r"\bworkflow\b", r"\bthroughput\b", r"\bproductivity\b",
        r"\bcycle time\b", r"\bscheduling\b", r"\bcrew\b", r"\bworkforce\b",
        r"\blabor\b", r"\bstaffing\b", r"\broster\b", r"\bshift\b",
        r"\btraining\b", r"\bonboarding\b", r"\battrition\b", r"\bheadcount\b",
        r"\brouting\b", r"\bprocess\b", r"\bqueue\b", r"\bwait time\b",
        r"\bops center\b", r"\bslo\b", r"\bsla\b", r"\bops intelligence\b",
        r"\bcatering\b", r"\bgate-assignment\b", r"\bground-handling\b",
        r"\bembarkation\b", r"\bbaggage-carousel\b", r"\bin-flight entertain",
        r"\bchangeover-time\b", r"\bcleaning-crew\b", r"\bbookings-pace\b",
        r"\btimetable\b", r"\bquota\b",
        r"\bovertime-cost\b", r"\boperator-skill\b", r"\bplant-commissioning\b",
        r"\bidle-time\b", r"\bhaul-truck\b", r"\bfuel-consumption\b",
        r"\bautonomous-haulage\b", r"\bfield-variable-rate\b",
        r"\bcycle-time-variance\b", r"\bmeasurement-system-drift\b",
        r"\blease-operator route\b",
     ]),

    ("channel-partner-dealer",
     "Channel, Partner & Dealer",
     [
        r"\bdealer\b", r"\bpartner\b", r"\bcodeshare\b", r"\bchannel-conflict\b",
        r"\bdistributor\b", r"\breseller\b", r"\bcommission\b",
        r"\bfranchis", r"\boem\b", r"\bagency\b",
        r"\bchannel-mix\b", r"\bco-op\b", r"\brebate\b",
        r"\bparts-distribution\b", r"\bdealer-prospect",
        r"\bdealer-certif", r"\bdealer-financing\b", r"\bdealer-leads\b",
     ]),
]
DEFAULT_DOMAIN = ("other", "Other / Cross-cutting", [])


def classify(title: str, blurb: str = "") -> tuple[str, str]:
    """Score-based classifier: highest matching-keyword count wins.

    Ties broken by domain order in DOMAINS (clinical-care first).
    If nothing matches, returns the Other / Cross-cutting bucket.
    """
    text = f"{title} {blurb}".lower()
    best_slug = DEFAULT_DOMAIN[0]
    best_name = DEFAULT_DOMAIN[1]
    best_score = 0
    for slug, name, patterns in DOMAINS:
        score = sum(1 for pat in patterns if re.search(pat, text))
        if score > best_score:
            best_score = score
            best_slug = slug
            best_name = name
    return best_slug, best_name


# Classify all scenarios
all_items: list[dict] = []

# Featured scenarios — classify on title + Scenario body
for c in chains:
    slug, name = classify(c["title"], c.get("Scenario", ""))
    all_items.append({
        "practice": c["practice"],
        "kind": "featured",
        "title": c["title"],
        "service": (c.get("Service", "").split()[0] if c.get("Service") else ""),
        "domain_slug": slug,
        "domain_name": name,
    })

# Compact scenarios — classify on title + blurb
for p, rows in library.items():
    for r in rows:
        # Skip if title matches a featured chain title in same practice
        featured_titles = [c["title"].lower() for c in chains if c["practice"] == p]
        t_lower = r["t"].lower().strip()
        if any(ft == t_lower or ft in t_lower or t_lower in ft for ft in featured_titles):
            continue
        slug, name = classify(r["t"], r.get("b", ""))
        all_items.append({
            "practice": p,
            "kind": "compact",
            "title": r["t"],
            "service": r.get("s", ""),
            "domain_slug": slug,
            "domain_name": name,
        })

# ------- Print distribution -------
print(f"Classified {len(all_items)} scenarios across 7 practices.\n")

PRACTICES = ["RC", "HLS", "ER", "AXLE", "TMT", "TH", "ICE"]
domain_order = [d[0] for d in DOMAINS] + [DEFAULT_DOMAIN[0]]
domain_names = {d[0]: d[1] for d in DOMAINS} | {DEFAULT_DOMAIN[0]: DEFAULT_DOMAIN[1]}

# Pivot: domain x practice
matrix = {d: {p: 0 for p in PRACTICES} for d in domain_order}
for it in all_items:
    matrix[it["domain_slug"]][it["practice"]] += 1

print(f"{'Domain':<40} " + " ".join(f"{p:>5}" for p in PRACTICES) + "   TOTAL")
print("-" * 90)
for d in domain_order:
    total = sum(matrix[d].values())
    if total == 0:
        continue
    print(f"{domain_names[d]:<40} " + " ".join(f"{matrix[d][p]:>5}" for p in PRACTICES) + f"  {total:>5}")
print("-" * 90)
print(f"{'TOTAL':<40} " + " ".join(f"{sum(matrix[d][p] for d in domain_order):>5}" for p in PRACTICES))

# Save classification for the reorganizer to pick up
json.dump(all_items, open(ROOT / "_catalog" / "domain-classification.json", "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)
print(f"\nSaved classification to docs/scenarios/_catalog/domain-classification.json")

# Sample per domain per practice
print("\n\n=== SAMPLE scenarios per domain (first 3) ===")
for d in domain_order:
    items = [it for it in all_items if it["domain_slug"] == d]
    if not items:
        continue
    print(f"\n[{domain_names[d]}]  ({len(items)})")
    for it in items[:3]:
        print(f"  · {it['practice']:4} {it['title'][:70]}")
