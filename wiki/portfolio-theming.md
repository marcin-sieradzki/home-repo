# Portfolio theming

Light and dark theme on the personal site, and how its colours are kept as design tokens. Source: portfolio PR #11 (branch `claude/project-thread-sbgpj3`), opened 2026-11-27, not merged as of that date.

## Decisions (2026-11-27)

- Marcin asked for a light/dark switch "using design tokens as css variables". The PR refactors colours into tokens rather than adding light overrides.
- As of portfolio PR #11, every colour is in `src/app/tokens.css`, in Perron's three layers: a fixed palette, then semantic tokens with a value per theme, then components that read only the semantic ones. Token names follow Perron 0.10, and the theme is `data-theme` on `<html>`, the same attribute Perron's `tokens.css` uses. Site-only tokens are `--site-color-*`: accents (the eight agent colours) and an `art-*` ramp for the project drawings.
- Default theme: the visitor's stored choice (`localStorage` key `theme`), else `prefers-color-scheme`. With no system preference or no JavaScript, the site is dark, as it was before.
- The switch has two states, sun and moon, in the header. No "follow system" third option; offered in the PR for review.
- A guard, `scripts/color-check.mjs`, runs in `prebuild` and fails on any colour literal in `src/` outside `tokens.css`. Its purpose is to keep new code on tokens (the "pit of success" idea from the chief-of-staff skill).

## Things learned

- Next 16 ships a guide for this: `node_modules/next/dist/docs/01-app/02-guides/preventing-flash-before-hydration.md` ("Themes"). An inline script in `<head>` plus `suppressHydrationWarning` on `<html>`. The `@next/next/no-head-element` lint rule fires on it but is meant for the pages router.
- SVG `fill="var(--x)"` works in Chromium, but it is not safe in every browser, so the drawings set paint through `style={{ fill: … }}`. Inline style beats CSS rules, unlike presentation attributes, so a CSS rule that recolours an SVG part needs `!important` or a token.
- Bright dark-theme accents (#ffd166, #3ddc97 …) fall under 3:1 on a light page. The light theme uses darker shades that hold 4.5:1 on the light paper, and text on an accent flips through `--site-color-text-on-accent` (dark on dark-theme accents, white on light-theme ones).
- Check that a refactor like this leaves the existing theme alone by diffing screenshots: full page plus every modal, Playwright with `reducedMotion: 'reduce'`, against the `main` build. Run axe-core in both themes and in each open modal.

Related: [repos.md](repos.md), [testing.md](testing.md).
