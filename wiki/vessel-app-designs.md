# Vessel tracker: design proposals

On 2026-11-26 Marcin asked for three design proposals for a vessel schedule and ship tracker demo app, built on Perron. The data plan behind it (aisstream.io positions, Upply ports, a schedule learned from AIS port calls, an assistant with tool use) is in the API research from the same day. No proposal is chosen yet, and there is no production code.

The proposals are a Design canvas artifact with 12 artboards: https://claude.ai/artifact/PoFnbQBCUWK1LQ6AT8kZFW (private to Marcin). All vessels, positions and times on it are made-up sample data. Coastlines are Natural Earth (via the `world-atlas` npm package), ports are real.

On 2026-11-26 Marcin cut v1 to the live AIS stream only: no history, port calls, learned schedules, owner or operator. Proposal A was revised to that scope (crew-entered destination and ETA, nav-status counts, a draught-based load estimate marked as an estimate, transponder facts). B and C still show the older, larger scope on the canvas, kept for comparison; B's whole premise (the learned schedule) is out of v1.

## The three proposals

| Proposal | Front door | Theme | Best for |
| --- | --- | --- | --- |
| A · Live map | The map, Mylder’s shell: glass top bar, overview sheet left, detail panel right, an Ask bar over the map | Dark, glowing sea and 3D-style ship glyphs (restyled 2026-11-26 at Marcin’s ask; was light) | A demo that feels alive the moment it loads |
| B · Port board | A port's arrivals as a timeline of berth windows: dashed is the usual window, solid is where the vessel is heading now | Dark | Showing the learned schedule and delay logic |
| C · Ask first | A chat; answers come back as vessel and route cards, with the map in a side pane | Light | Showing the assistant and its tool calls |

Each has a main view, a vessel detail, the assistant, and a phone screen.

## Decisions the three share

These hold whichever proposal is picked, because they come from Perron's rules:

- **Perron's five data states carry over to ships.** Live, Ageing, Estimated, Timetable only and No signal, drawn on a hull glyph that points along the course (Perron lets aircraft have their own glyph the same way). The app sets its own thresholds from AIS report intervals: a ship underway reports every few seconds, one at anchor every few minutes. "Timetable only" means a call predicted from the learned schedule with no AIS fix yet; in the live-only v1 scope it does not appear, so A's revised screens use only the other four. A ship with no signal keeps moving on its dead-reckoned course, as Perron's "No signal keeps moving" rule says.
- **"Usually" is the median of the last 6 observed calls.** Every delay compares where a ship is heading now with that median, and the screens say so in words. Nothing calls itself a carrier schedule. (Out of the v1 scope; applies to B, C and any later phase that learns schedules.)
- **Wording follows Perron's content design.** 24-hour clock, `~` before estimated times, `≈` before estimates, "—" for an unknown delay, Perron's delay and state words.
- **The assistant shows its tool calls** (`find_vessel`, `get_track`, `get_port_calls`, `get_port_queue`, `find_services`) and cites where each claim came from, with numbered markers that also appear on the map.
- **Colour.** Ink, glass and neutral surfaces, Perron yellow only for the main action. The vessel type colours (container blue, tanker orange, bulk green, ro-ro red) use Perron palette values directly; a real build needs a `color.vessel.*` token set in Perron first.
- **Working name: Farvand** (Danish for waters, or a fairway), in the same spirit as Mylder. Placeholder until Marcin names it.
- No Maersk branding, layouts or names, at Marcin's request.

## Prototype notes

- Fonts load from Google Fonts in the prototype only. The real app self-hosts them through Perron's `@fontsource` setup.
- The map is one 1600 x 1009 Mercator box (lon −6 to 32, lat 48.5 to 62) with the land as a CSS mask, so every artboard crops it with a CSS transform. Ports and lanes are placed in that box's coordinates.
- Screenshots of every artboard: the project's `vessel-app-designs/` folder.
