# Danish straits point cloud (prototype, throwaway)

Question: does the point-cloud look work as a 3D overview of all Danish waters, with a click on a vessel flying in to a close-up? Learnings: [wiki/point-cloud-terrain.md](../../wiki/point-cloud-terrain.md).

Data scripts (need numpy, pillow, scipy; run in this order from one folder): `ov.py` (overview tiles, zoom 9), `patches.py` (four strait patches, zoom 13; the Storebælt patch was later widened to ±13 km by hand), `build.py` (coastline cleanup, A* lanes, writes `overview.png`, `patch-*.png` and `meta.json`). Heights are PNG R*256+G in decimetres, offset by 1000 m.
