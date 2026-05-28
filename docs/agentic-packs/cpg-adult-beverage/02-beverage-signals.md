# 02 — Adult-Beverage Signals

## 1. Sazerac-side signals

- Allocation drops (BTAC, Pappy, Eagle Rare 17, etc.) — per-retailer SKU + quantity + drop-time webhook
- Standard releases (Buffalo Trace, Blanton's, Sazerac Rye) — inventory + pricing
- Distillery tour availability + tasting-event calendar
- Brand-experience content (heritage, mash bill, distillery-tour content)

## 2. Bench-partner signals

- **Diageo**: Johnnie Walker, Crown Royal, Bulleit, Lagavulin, Talisker, Don Julio
- **Pernod Ricard**: Jameson, Glenlivet, Chivas, Absolut, Beefeater
- **Brown-Forman**: Woodford Reserve, Jack Daniel's, Old Forester, Coopers' Craft
- **Constellation Brands**: Casa Noble, High West, Mi Campo

Each provides allocation + standard-release + tasting-event feeds via the same MCP protocol.

## 3. Retailer-side signals

| Source | Feed |
|---|---|
| Total Wine & More | Inventory by store, allocation-receive notifications |
| BevMo! / Gopuff | Inventory + delivery options where state-legal |
| Binny's (Chicago region) | Inventory + auction events |
| Independent licensed retailers | Onboarded via partner directory (Pearson's, Schneider's, etc.) |
| Costco wine / spirits | Membership-gated allocation flow |
| Walmart liquor stores (state-legal) | Inventory |

## 4. Age + identity signals

- `travel_document.doc_token` (extended from Travel Channel) — Real ID, driver's license, passport tokenised reference
- Age-verification provider integration (Veratad, AgeChecker.net, BlueCheck, etc.)
- Pickup-side age check (retailer scans ID; result reported via MCP webhook)

## 5. State / jurisdiction signals

- State alcohol-control board rules feed (per-state, periodically updated)
- Dry-county / dry-precinct zip-code list
- Tied-house compliance rules (varies per state)
- TTB labelling + shipping rules (federal)

## 6. Cocktail-side signals

- Recipe corpus (Sazerac brand recipe library + external partnership with Diffords / Liquor.com / Punch)
- Bar-stock inventory in household vault (user-curated + receipt-augmented)
- Mixer / garnish demand routed to Walmart / Costco grocery

## 7. Consent scopes

- `purchases.beverage` — BEV order history
- `age_verified` — ID-document reference for age verification (CPNI, tokenised)
- `cellar` — household spirits inventory
- `tasting_events` — event-booking history
