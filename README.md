# 2001 Ford Ranger Tie Rod — 3D Model

Custom tie rod assembly for a 2001 Ford Ranger, modeled in Blender.

![Render](render.png)

## Specifications

| Component | Spec |
|-----------|------|
| Tube | 1.25" OD x 0.120" wall DOM (drawn over mandrel) |
| Tube ID | 1.010" |
| Approximate length | 22" center-to-center |
| Inserts | 1.5" weld-in, turned to ~1.008" OD slip fit, 1/8" flush shoulder |
| Thread | 3/4-16 (RH one end, LH other for adjustment) |
| Tie rod ends | 3/4-16 heim joints |
| Jam nuts | 1-1/8" hex, both ends |

## Design

- **1.25" DOM tube** chosen for clean insert geometry -- the 1.01" bore accepts inserts that transition smoothly to the 3/4" heim shank without a visible step-down
- **Weld-in inserts** with a flush shoulder at the tube face, fillet welded
- **Heim joints** thread into inserts, acting as tie rod ends with spherical bearing for misalignment
- **LH/RH threading** allows toe adjustment by rotating the tube without disconnecting

## Files

- `ford_ranger_tie_rod.blend` — Blender project file (Blender 4.0+)
- `build_tie_rod.py` — Python build script (runs inside Blender)
- `render.png` — Rendered preview

## Build from script

```bash
blender --background --python build_tie_rod.py
```
