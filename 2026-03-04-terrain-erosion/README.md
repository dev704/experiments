# ⛰️ Procedural Terrain with Hydraulic Erosion

An interactive 3D terrain generator that combines fractal noise generation with physically-based hydraulic erosion simulation, rendered in real-time with three.js.

![Screenshot placeholder](screenshot.png)

## What It Is

A single-file HTML experiment that procedurally generates realistic terrain and then simulates thousands of virtual raindrops eroding the surface — carving river channels, depositing sediment in valleys, and creating natural-looking drainage patterns.

## How It Works

### Terrain Generation — Fractal Brownian Motion (FBM)

The base terrain is built by layering multiple octaves of 2D simplex noise. Each octave adds finer detail at higher frequency but lower amplitude:

```
height(x,y) = Σ amplitude^i × noise(x × frequency^i, y × frequency^i)
```

- **Octaves** control detail levels (more = finer features)
- **Persistence** controls how much each octave contributes (lower = smoother)
- **Lacunarity** controls frequency scaling between octaves
- **Scale** controls the overall zoom level

The simplex noise is implemented from scratch in JavaScript (no external library).

### Hydraulic Erosion — Raindrop Particle Simulation

Each virtual raindrop:

1. **Spawns** at a random position on the heightmap
2. **Flows downhill** following the terrain gradient (with inertia for natural curves)
3. **Erodes** terrain when moving fast with low sediment load
4. **Deposits** sediment when slowing down or moving uphill
5. **Evaporates** gradually, losing water volume each step

Key parameters:
- **Inertia**: How much a drop resists changing direction (creates meandering)
- **Capacity**: Maximum sediment a drop can carry (proportional to speed × water)
- **Erosion radius**: Smooths erosion across neighboring cells (prevents spiky artifacts)

After thousands of iterations, realistic features emerge: river channels, sediment fans, ridgelines, and drainage basins.

## How to Run

Just open `index.html` in any modern browser. No build step, no server needed.

```bash
# Or serve locally if you prefer
python3 -m http.server 8080
# Then visit http://localhost:8080
```

## Controls

### Terrain Generation
| Control | Description |
|---------|-------------|
| Octaves | Number of noise layers (1-10) |
| Persistence | Amplitude falloff per octave (0.1-0.9) |
| Lacunarity | Frequency multiplier per octave (1.0-4.0) |
| Scale | Overall noise zoom (1.0-12.0) |
| **Generate** | Create new random terrain |

### Erosion
| Control | Description |
|---------|-------------|
| Drop Count | Number of raindrops to simulate (1k-200k) |
| **Erode** | Run full erosion (animated progress) |
| **Step 1k** | Apply 1,000 drops (watch it evolve) |

### Appearance
| Control | Description |
|---------|-------------|
| Colour Scheme | Earth, Desert, Arctic, or Alien |
| Water Level | Height of the translucent water plane |
| Sun Angle/Elevation | Directional light position |
| Wireframe | Toggle wireframe rendering |
| Shadows | Toggle shadow casting |

### Export
| Control | Description |
|---------|-------------|
| **Export Heightmap** | Download as grayscale PNG (256×256) |

## Tech Stack

- **Three.js** (via CDN) — 3D rendering, orbit controls, shadows
- **Simplex noise** — Self-contained JS implementation
- **Zero other dependencies** — Single HTML file, ~27KB

---

*Built as a portfolio piece. Open source, do whatever you want with it.*
