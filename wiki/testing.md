# Testing

All claims below as of 2026-11-24 unless dated otherwise.

- Work in Perron and Mylder is done when `npm run check` passes.
- Full suites and long builds (over about 10 minutes) run on Marcin's computer. Short, targeted test runs can run in the cloud.
- Timing tests (Perron's NumberField steppers, Mylder's tracker updates) miss under load: run the two repos' checks one at a time.
- Perron: build the site with `PERRON_SITE_URL` set, but run `npm run check` without it.
- Mylder: prove a change in the real app with the `verify-mylder` skill. In a cloud container, set `PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium`.
- Portfolio: `prebuild` fails on a missing or unused Polish string, so new copy needs an entry in `src/i18n/pl.ts`. Measure Lighthouse with `npx lighthouse@12` against `npx serve@14` of `out/`.
