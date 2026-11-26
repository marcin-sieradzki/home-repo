# Vessel schedule and AIS data sources

Research for a possible demo app: multi-carrier schedule search, live vessel positions on a map, and an AI layer that answers routing questions and flags likely delays by comparing schedules with AIS positions. All claims were checked on 2026-11-26 unless dated otherwise. Sources are linked beside each claim; "not stated" means the pages read were silent.

## Summary (2026-11-26)

- Carrier schedule APIs are customer products. Maersk's needs a paid subscription and is marked for Maersk Ocean customers; Hapag-Lloyd's is marked "Customer" and needs approval. None was found that a private person can use without approval.
- Live AIS is easy: aisstream.io is free, self-service (GitHub sign-in), but server-side only and with no SLA.
- Port lists: Upply's seaport list is CC BY 4.0 with coordinates. UN/LOCODE's own licence is unclear for redistribution.
- So a demo that must not wait on anyone's approval can derive "observed" port calls from AIS (vessel enters a port area) instead of reading carrier schedules, and add a carrier schedule API later if an application is approved.

## Carrier schedules

All carriers below say they follow the DCSA Commercial Schedules standard: three endpoints, `GET /v1/point-to-point-routes`, `/v1/port-schedules`, `/v1/vessel-schedules`, current release v1.0.3 ([DCSA reference](https://reference.dcsa.org/content/standards/releases/commercial-schedules/v1)). DCSA says the standard is live with nine carriers and tells consumers to contact each carrier for access; it publishes no list of endpoints ([DCSA explainer](https://dcsa.org/newsroom/commercial-schedules-standard-explainer)). One client could, in principle, read every carrier that grants access.

| Source | Data | Access | Cost | Limits | Public demo? |
|---|---|---|---|---|---|
| Maersk Commercial Schedules [DCSA] | Point-to-point, port and vessel schedules | Developer portal account, then subscription; product page says "Available for Maersk Ocean Customers" ([product](https://developer.maersk.com/api-catalogue/ocean-commercial-schedules/Learn-more)) | Catalogue says "Access to this Product requires a paid subscription" ([catalogue](https://developer.maersk.com/catalogue)) | Not stated; terms allow Maersk to set them | API terms forbid sharing data with third parties without written agreement, and apps that replicate the Maersk experience ([API licence terms](https://terms.maersk.com/api-license-terms)) |
| Hapag-Lloyd Commercial Schedule (DCSA, v3) | Point-to-point route options before booking | Free portal account, create app, request subscription, "Receive Approval"; product tagged "Customer" ([portal](https://api-portal.hlag.com/)) | Not stated | Not stated | Not stated |
| MSC | Point-to-point live; vessel and port schedules in development (article updated 2026-04-27) ([MSC](https://www.msc.com/en/lp/blog/technology/msc-adopts-dcsa-commercial-schedule-api)) | Developer portal developerportal.msc.com, not checked | Not stated | Not stated | Not stated |
| CMA CGM | No schedule product found on the first page of its API catalogue ([portal](https://api-portal.cma-cgm.com/)); not checked further | Sign-up on the portal | Not checked | Not checked | Not checked |
| ONE, Evergreen and others | Not checked | | | | |
| SeaRates Ship Schedules (aggregator) | Multi-carrier schedules; vessel schedules only within 3 months of request ([docs](https://docs.searates.com/reference/schedules/v1/rate-limit)) | Commercial API | Pricing page could not be read | Not stated | Not checked |

Maersk's own portal also lists a public Track & Trace product ("no customer account required", "offered on a subscription basis") ([catalogue](https://developer.maersk.com/catalogue)); price not checked.

## Live and historical AIS

| Source | Data | Access | Cost and limits | Terms |
|---|---|---|---|---|
| [aisstream.io](https://aisstream.io/documentation) | Global AIS over WebSocket (`wss://stream.aisstream.io/v0/stream`): position reports, static ship data and other message types; filter by bounding boxes (required), up to 200 MMSIs, message types. Terrestrial vs satellite coverage not stated | Sign in with GitHub, create an API key; no approval step | Free. 3 subscribed connections per account, 3 open connections per IP, 1 subscription update per second; per-user bandwidth limits on uncompressed connections from September 2026 (use `permessage-deflate`) | "Direct browser connections are not permitted"; key stays server-side. No SLA, no replay. No terms of use found |
| [BarentsWatch Live AIS](https://developer.barentswatch.no/docs/AIS/live-ais-api) | Norwegian waters only; excludes small fishing and leisure craft | barentswatch.no user, API client, OAuth2 client credentials | Not stated | Not checked |
| [Danish Maritime Authority](https://www.dma.dk/safety-at-sea/navigational-information/ais-data) | Historical AIS for Danish waters as zipped daily CSV, free; live feeds are paid yearly subscriptions | Historical: no sign-up named; live: order form | Historical free | No identifying persons by combining data; no correctness guarantee ([policy](https://www.dma.dk/safety-at-sea/navigational-information/ais-data/ais-data-management-policy-)) |
| [Global Fishing Watch](https://globalfishingwatch.org/our-apis/documentation/docs/license-rate-limits) | Vessel identity from 40+ registries; port visit events for all vessel types; encounters, loitering, AIS gaps | Account plus token; GFW may reject a registration and asks you to represent an organisation supporting sustainable ocean use | 50,000 requests a day, 1.5 million a month | CC BY-NC 4.0, non-commercial only; credit "Powered by Global Fishing Watch"; token must not be discoverable in a public web page |

## Ports

- [Upply seaports](https://opendata.upply.com/seaports): UN/LOCODE, name, country, zone, latitude and longitude; CC BY 4.0, credit "Upply (upply.com)". The page also mentions share-alike, which CC BY does not have.
- [UN/LOCODE on DataHub](https://datahub.io/core/un-locode): CSV, monthly rebuild from the UNECE pre-release, coordinates as text in degrees and minutes. Its README says the data's own licence is unclear and UNECE's terms restrict use to personal, non-commercial use.

## Things to design around

- aisstream needs a long-lived server WebSocket. A Vercel serverless function cannot hold one, so a worker elsewhere has to keep the stream and store positions (as noted on 2026-11-26; hosting not chosen).
- Every carrier path needs a manual approval or a customer account. A transit API application for Mylder went unanswered for weeks in October and November 2026, so do not plan a launch on an approval.

## Related

- [repos.md](repos.md)
- [hosting.md](hosting.md)
