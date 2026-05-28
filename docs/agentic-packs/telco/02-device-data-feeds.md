# 02 — Device & Data Feeds

> Each device class is a data stream the orchestrator + sub-agents can act on. Categorized by the household function the device serves, with the example vendors that today produce machine-consumable telemetry. Strategic anchor is the router/ONT — the Telco's own equipment is the data-collection chokepoint that no other player owns.

## Kitchen & food inventory

- Smart refrigerators (Samsung Family Hub, LG InstaView) — interior cameras, item recognition, temperature logs
- Smart pantries / shelf-weight sensors (Ovie, Smarter FridgeCam)
- Connected ovens, microwaves, ranges — cook history, recipes
- Smart dishwashers — detergent levels, cycle data
- Coffee machines (Nespresso, Keurig connected) — consumption rates
- Smart scales & sous-vide devices
- Wine fridges / beverage coolers
- Trash / recycling cans with barcode scanning (GeniCan)

## Climate, energy & utilities

- Smart thermostats (Nest, Ecobee, Honeywell / Resideo)
- Smart meters (electric, gas, water) and utility gateways
- Solar inverters & battery systems (Tesla Powerwall, Enphase)
- EV chargers (ChargePoint, Wallbox, Tesla)
- HVAC systems with IoT controllers
- Smart vents & zone controllers
- Water-leak sensors, smart shutoff valves (Flo by Moen, Phyn)
- Sump pumps & water heaters
- Air-quality monitors (Awair, Airthings) — CO₂, VOC, radon, humidity

## Security, access & presence

- Video doorbells (Ring, Nest, Eufy)
- Indoor / outdoor cameras
- Smart locks & garage-door openers
- Motion, door / window, glass-break sensors
- Alarm panels (ADT, SimpliSafe, Vivint)
- Smart lighting (Hue, Lutron, LIFX) — occupancy proxy
- Presence / geofence data from phones

## Health, wellness & wearables

- Smartwatches & fitness bands (Apple Watch, Fitbit, Garmin, Oura, Whoop)
- Continuous glucose monitors, BP cuffs, smart scales (Withings)
- Sleep trackers / smart mattresses (Eight Sleep, Sleep Number)
- Connected CPAPs, inhalers, pill dispensers (Hero, MedMinder)
- Smart toilets / urine analyzers (emerging — Withings U-Scan)
- Baby monitors with vitals (Owlet, Nanit)
- Hearing aids with telemetry

## Entertainment & daily activity

- Smart TVs, streaming sticks, game consoles — usage, schedule, content preferences
- Smart speakers / displays (Echo, Google Nest, HomePod) — voice intents
- Connected audio systems (Sonos)
- E-readers, tablets

## Mobility & vehicles

- Connected cars — tire pressure, fuel / charge, location, maintenance alerts
- E-bikes, e-scooters
- In-vehicle telematics dongles
- Fleet / insurance trackers

## Cleaning, maintenance & outdoor

- Robot vacuums & mops (Roomba, Roborock) — floor maps, run logs
- Smart washers / dryers — cycle counts, detergent
- Smart sprinkler controllers (Rachio) & soil sensors
- Robotic mowers
- Pool / spa controllers
- Air purifiers, dehumidifiers — filter life

## Pets

- Smart pet feeders & water fountains (Petnet, PetSafe)
- Pet cameras, GPS collars (Fi, Whistle)
- Smart litter boxes (Litter-Robot)

## Connectivity & network — the Telco's home turf

> The router / ONT is the natural anchor. The Telco already sits at the data choke point. Everything else above only matters because this layer brings it together.

- Wi-Fi router / mesh nodes — the most valuable feed: device fingerprinting, traffic patterns, presence inference
- ONT / gateway (FIOS-style optical terminal)
- 5G CPE / mobile data
- Smart hubs (SmartThings, Home Assistant, Hubitat, Matter controllers)

## Productivity, finance & personal data — with user consent

- Calendars, email, contacts
- Banking / payment apps — recurring purchases, budget signals
- Subscription services
- Shopping accounts (Amazon, grocery loyalty programs) — purchase history
- Cloud photo / document storage

## Eldercare & accessibility

- Fall-detection devices, medical-alert pendants
- Activity-of-daily-living sensors (motion patterns, bed-exit sensors)
- Smart bed-exit sensors

## Classification of each feed

Every feed is tagged with one of four classifications that propagate through Bronze → Silver → Gold and govern who/what can read it:

| Classification | Examples |
|---|---|
| `INTERNAL` | Thermostat setpoints, appliance status, energy readings |
| `PII` | Location, presence, video, voice, purchase history |
| `PHI` | Wearable vitals, glucose, sleep, fall events, ADL signals |
| `CPNI` | Subscriber identifiers, OAuth tokens, network identity |

Classifications enforce **forbidden-classifications** rules on agents (e.g., the orchestrator never sees PHI directly; only the eldercare sub-agent does). See [`04-medallion-bronze-silver-gold.md`](./04-medallion-bronze-silver-gold.md) for how this is enforced in Silver / Gold and [`05-services-catalog.md`](./05-services-catalog.md) for how each sub-agent declares its allowed classifications.

## The grocery-example signal stack

The headline use case combines:

1. **Fridge camera** + **pantry weight sensors** + **trash barcode scanner** → continuous inventory state
2. **Purchase history** (Kroger / Instacart / Amazon Fresh) → consumption rate calibration
3. **Calendar** ("dinner party Saturday") → demand-side signal
4. **Banking / budget** → spending guardrail
5. **Smart-speaker voice intent** ("we're out of coffee") → manual override channel

Five distinct device classes, three different vendors per class, one orchestrated outcome: a grocery order drafted, approved, and submitted without the customer typing into an app. That's the proof point. The other seven sub-agents are the same shape with different anchor devices.
