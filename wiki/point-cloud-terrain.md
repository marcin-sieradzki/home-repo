# Point-cloud terrain for the vessel app

On 2026-11-28 Marcin shared a reference image (a "Chokepoint Watch" style strait view: land as stippled white beads, flat matte grey water, ships with white wakes, monochrome with orange accents) and asked what tech gives that look. A prototype of the Bosphorus was built the same day. It belongs to the vessel schedule / AIS app idea; see [vessel-schedule-apis.md](vessel-schedule-apis.md) and [vessel-app-designs.md](vessel-app-designs.md) where those pages exist (PRs #2 and #3).

Prototype source as of 2026-11-28: `prototypes/bosphorus-point-cloud/` in this repo (throwaway, plain Three.js in one HTML file; published privately as a claude.ai artifact).

## What worked (2026-11-28)

- **Elevation data with no key:** AWS Terrain Tiles, Terrarium PNG encoding, `https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png`, height in metres = `R*256 + G + B/256 - 32768`. Zoom 13 is about 14 m per pixel at 41° N. Sea comes back at about 0 m, so `h < 1.2 m` plus "largest connected water body" gives a clean water mask. `fetch_dem.py` and `prep_dem.py` crop 41.02–41.16° N, 28.98–29.14° E, halve it to a 466 × 541 grid (~29 m), and write heights as decimetres in the R and G bytes of a PNG.
- **Shipping lanes from the DEM:** the channel centreline is the per-row maximum of a distance transform over the water mask, smoothed. Lanes are that line offset to starboard on each side. No AIS or chart data needed for a believable demo.
- **The bead look:** `THREE.Points` with a custom shader, not instanced meshes. Each sprite is shaded as a little sphere in the fragment shader (normal from `gl_PointCoord`, a soft highlight, a darker rim), and its base colour comes from terrain lighting baked on the CPU (Lambert from a low raking light, plus a cavity term). Size in world units, divided by view depth.
- **Density is what sells it:** one dot per 29 m cell looked like scattered marbles. About 1.75 dots per cell edge (bilinear between samples, small jitter) plus up to 5 extra dots on steep faces, where the rise across one dot spacing exceeds the dot width, closed the gaps on cliffs. That is about 880k points on desktop; phones (coarse pointer) get 1.25 per edge.
- **Vertical exaggeration ×4.2** matched the reference's drama; ×2.6 looked flat. Ships are drawn 1.7× real length so they read at this scale.
- **Water:** a plain plane with a faint fresnel towards the sky colour, low-amplitude noise, and darkening near steep land from a blurred land-mask texture. No reflections.
- **Wakes:** a CPU particle pool per ship. Particles leave the stern with sideways speed proportional to ship speed (Kelvin arms), plus a dense slow centre trail and a small bow wave; alpha fades with age.
- **Post:** EffectComposer with four directional blur passes whose radius grows with distance from a focus band (tilt-shift), the band following the selected ship on screen; then a grade pass that pulls colour 45% towards grey (so orange survives), a vignette and grain.

## Notes for a real build

- The coordinator suggested React Three Fiber; the prototype used plain Three.js only because it had to be one self-contained HTML page. The same shaders port to R3F as `<points>` with a `shaderMaterial`.
- For live AIS positions, map lon/lat to the same grid as the DEM crop (linear is fine over 15 km).
- Headless Chromium in the cloud container renders WebGL with `--use-angle=swiftshader --enable-unsafe-swiftshader`, but cannot reach the CDN through the proxy; route `cdn.jsdelivr.net/npm/three@…` to a local `npm pack` copy in Playwright.
