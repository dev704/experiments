# 🧬 Particle Life

An artificial life simulation where colored particles interact via simple attraction/repulsion rules, producing stunning emergent behaviors — cells, organisms, galaxies, hunting packs, and more.

## How It Works

- **N species** of particles live on a 2D canvas
- Each pair of species has an **interaction force** (-1 = repel, +1 = attract)
- These forces are stored in an **N×N matrix** — the "DNA" of the universe
- All particles repel at very close range (prevents collapse)
- The combination of simple rules creates complex emergent life

## Emergent Behaviors

Different matrices produce radically different "universes":

- **🧫 Cells** — Self-attracting species form blobs with membranes
- **🐍 Snakes** — Chase chains where A→B→C→A creates spiraling organisms  
- **🌀 Galaxies** — Swirling clusters with orbiting satellite species
- **⚔️ Predator-Prey** — Species that hunt and flee each other

## Controls

| Control | Effect |
|---------|--------|
| **Particles** slider | 200–4000 particles |
| **Species** slider | 2–9 different types |
| **Interaction Range** | How far particles sense each other |
| **Friction** | Energy dissipation (lower = more damping) |
| **Force Strength** | Global force multiplier |
| **Matrix cells** | Click to cycle interaction values |
| **🎲 Randomize** | New random interaction matrix |
| **🪞 Symmetry** | Symmetric matrix (A↔B same force) |
| **🎨 Preset** | Cycle through curated presets (cells, chains, snakes, galaxies) |
| **↺ Reset** | Respawn everything |
| **Click & drag** | Attract particles toward cursor |
| **Space** | Pause/resume |

## Run It

```bash
open index.html
# or
python3 -m http.server 8080  # then visit localhost:8080
```

Single HTML file, zero dependencies.

## Inspired By

- [Particle Life by Tom Mohr](https://www.youtube.com/watch?v=p4YirERTVF0)
- [Clusters by Jeffrey Ventrella](http://www.ventrella.com/Clusters/)
- Lenia, Primordial Soup, and other artificial life systems

## Tech

- Canvas 2D rendering with motion trails
- Spatial hashing for O(n·k) neighbor lookups instead of O(n²)
- Speed-based particle glow for visual feedback
- Bell-curve force profile with universal short-range repulsion
