# 2001 Ford Ranger Tie Rod — 3D Model

Custom tie rod assembly for a 2001 Ford Ranger, modeled in Blender.

![Render](render.png)

## Specifications

| Component | Spec |
|-----------|------|
| Tube | 1.20" OD x 0.120" wall DOM (drawn over mandrel) |
| Tube ID | 0.960" |
| Approximate length | 22" center-to-center |
| Inserts | 1.5" weld-in, bored 3/4" for heim thread |
| Thread | 3/4-16 (RH one end, LH other for adjustment) |
| Tie rod ends | 3/4-16 heim joints |
| Jam nuts | Hex, both ends |

## Files

- `ford_ranger_tie_rod.blend` — Blender project file (Blender 4.0+)
- `build_tie_rod.py` — Python build script (runs inside Blender)
- `render.png` — Rendered preview

## Build from script

```bash
blender --background --python build_tie_rod.py
```

## Notes

- One insert is left-hand thread, the other right-hand — allows toe adjustment by rotating the tube
- Weld beads modeled at tube-insert junctions
- Heim joint eyes are oriented vertically for bolt-through mounting
