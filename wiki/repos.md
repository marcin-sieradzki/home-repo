# Repos

All claims below as of 2026-11-24 unless dated otherwise.

| Repo | What it is | Stack | Live |
|---|---|---|---|
| portfolio | Marcin's personal site, English at `/`, Polish at `/pl` | Next.js 16 static export, React 19, Tailwind | www.marcinsieradzki.com |
| perron | Mylder's design system: tokens, icons, components, docs site, MCP server | npm workspaces, Base UI, Storybook | perron.marcinsieradzki.com |
| mylder | Live map of Copenhagen's buses, S-tog, metro and trains | Next.js 16, React 19, Effect, deck.gl | mylder.marcinsieradzki.com |
| fsd-simulator | Self-driving simulator, planned in the Perron and Mylder style (repo created 2026-11-24) | not decided as of 2026-11-24 | not deployed |
| strait-watch | Live 3D view of ship traffic in Danish waters from AIS, on a baked point-cloud coast (planned 2026-11-28) | Next.js 16, React Three Fiber, Perron; Node worker on Fly.io for the aisstream feed | not deployed as of 2026-11-28 |

## How they depend on each other

- Mylder takes every component from Perron (Mylder ADR 0004) through the pinned `@mylder/perron` package. A Perron fix reaches Mylder only after a Perron release and a bump in Mylder.
- A Mylder stand-in for a missing Perron piece carries `perron-stand-in: perron#<n>`; Mylder's weekly Stand-ins workflow opens a ticket when that Perron issue closes.
- The portfolio shows both as case studies, but shares no code with them.

## Agent setup in each repo

- Perron and Mylder each run a "factory": `/factory` builds a spec's tickets to merged PRs inside that repo. Their skills (factory, tdd, retro, to-spec, to-tickets, code review) are adapted to the repo and stay there.
- Glossaries: Perron `docs/glossary.md`, Mylder `GLOSSARY.md`. ADRs: `docs/adr/` in both.
- Portfolio has no skills yet; its AGENTS.md holds only the Next.js block that `next dev` writes.
