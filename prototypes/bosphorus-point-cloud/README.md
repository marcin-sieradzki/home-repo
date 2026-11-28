# Bosphorus point cloud (prototype, throwaway)

Question: can we get the stippled point-cloud strait look from Marcin's reference image with real elevation data? Answer and learnings: [wiki/point-cloud-terrain.md](../../wiki/point-cloud-terrain.md).

Run: `python3 -m http.server` in this folder and open `index.html` inside a page skeleton (the claude.ai artifact adds `<!doctype html>` and `<body>`; browsers render it without them too). `fetch_dem.py` downloads the tiles, `prep_dem.py` writes `heights.png` and `meta.json` (needs numpy, pillow, scipy).
