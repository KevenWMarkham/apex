# 02 — Vehicle Signal Feeds

## 1. OEM telematics feeds

| Source | Feed | Classification |
|---|---|---|
| Toyota Connected Services | Vehicle health, location-hashed, odometer, charge state, alerts | pii + cpni (embedded SIM identity) |
| Ford SYNC 4 / FordPass | Same shape | pii + cpni |
| GM OnStar / Ultium | Same shape; SuperCruise OTA-update status | pii + cpni |
| Tesla | API: charge state, location-hashed, FSD status, software updates | pii + cpni |
| Honda HondaLink | Telematics | pii + cpni |
| Hyundai Bluelink | Telematics | pii + cpni |
| Stellantis Uconnect | Telematics | pii + cpni |

## 2. Recall + service-bulletin feeds (public)

| Source | Use |
|---|---|
| NHTSA recall API | Recall campaign cross-reference against household fleet |
| OEM-direct recall feed | Toyota, Honda, Ford, GM each publish |
| NHTSA TSB (Technical Service Bulletin) | Service-due triage |

## 3. Service-network signals

| Source | Feed |
|---|---|
| Toyota dealer DMS (Dealer Management System) | Appointment availability, service capacity |
| Ford dealer DMS | Same |
| GM dealer DMS | Same |
| Independent service network (Jiffy Lube, Firestone) | Already in Retail Channel RTL-03 |
| Walmart TLE | Already in Retail Channel RTL-03 |

## 4. Finance + insurance signals

| Source | Feed |
|---|---|
| Toyota Financial Services | Loan / lease metadata, payment history (tokenised), end-of-lease date |
| Toyota Insurance Management Solutions | UBI score, premium status |
| Ford Credit | Same shape |
| GM Financial | Same shape |
| Generic auto-insurance carrier (handoff to Finance Channel future) | State Farm, Progressive, Allstate, Geico, Root |

## 5. Charging-network feeds (EV)

Already in HOM-07 vehicle (Home pack). The Mobility Channel reads:
- ChargePoint, EVgo, Electrify America, Tesla Supercharger
- Home Powerwall + EV charger via HOM-02

## 6. Consent scopes consumed

- `vehicle` — telematics + service history (always required)
- `vehicle.financial` — TFS / lease / loan data (MOB-04 only)
- `vehicle.insurance` — UBI / policy data (MOB-04 only)
- `location.vehicle` — vehicle-side geo (already in Home pack)
