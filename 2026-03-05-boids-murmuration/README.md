# Murmuration — 3D Boids Simulator

> *A thousand wings, one mind. Watch them breathe together.*

A real-time 3D flocking simulation built with three.js, where thousands of boid agents follow Craig Reynolds' classic rules to produce mesmerizing murmuration patterns — like a flock of starlings wheeling against a burning dusk sky.

## How to Run

Just open `index.html` in any modern browser. No build step, no server, no dependencies to install.

```bash
# Or serve it if you prefer
python3 -m http.server 8000
# Then open http://localhost:8000
```

**Note:** Must be served over HTTP (not `file://`) due to ES module imports. Use any local server.

## Controls

### Camera
- **Orbit:** Click and drag (left button)
- **Zoom:** Scroll wheel
- **Pan:** Right-click drag

### Interaction
- **Click** anywhere in the scene to create a scare point — boids flee from it temporarily, then reform
- **Drag the red predator sphere** to steer it through the flock and watch dramatic splits and reunions

### Control Panel (right side, collapsible)
| Slider | Effect |
|--------|--------|
| Separation | How strongly boids avoid crowding each other |
| Alignment | How much boids match their neighbors' heading |
| Cohesion | How strongly boids steer toward the flock center |
| Speed | Overall simulation speed multiplier |
| Boids | Number of agents (200–4000) — adjustable live |
| Trail length | Ghostly trail behind each boid (0 = off, up to 8) |

### Toggles & Buttons
- **Predator** toggle — enable/disable the hunting hawk
- **Pause/Play** — freeze the simulation
- **Reset** — reinitialize all boids to random positions

### Themes
Four colour schemes, each with matching sky:
1. **Dusk** — Dark silhouettes against an orange-purple gradient sky. The classic starling murmuration look.
2. **Ocean** — Bioluminescent fish in deep water. Glowing blues and greens against abyssal darkness.
3. **Neon** — Rainbow-cycling boids on black. Each boid a different hue, shifting over time.
4. **Mono** — White boids on black. Stark, elegant, minimal.

## Technical Notes

### Algorithm
- **Craig Reynolds' Boids (1986):** Three rules — separation (avoid crowding), alignment (steer toward average heading), cohesion (steer toward average position)
- **4th rule: Predator avoidance** — A hawk agent chases the flock center with wander noise. Boids within its fear radius flee outward, creating dramatic splits
- **Boundary constraint:** Soft spherical boundary — boids get a gentle push back as they approach the edge, no hard walls
- **Scare points:** Click-placed temporary repulsors that decay over 2 seconds

### Performance
- **InstancedMesh:** All boids share one geometry and material, rendered in a single draw call via `THREE.InstancedMesh`
- **Spatial hashing:** O(n) neighbor lookups instead of O(n²) brute force. Grid cells sized to match perception radius
- **Structure of Arrays (SoA):** Boid data stored as flat `Float32Array`s for cache-friendly access
- **Delta time:** Frame-rate independent simulation with capped dt to prevent explosion on tab-switch
- **Target:** 2000+ boids at 60fps on modern hardware

### Rendering
- Boids are elongated cones oriented along their velocity vector
- Optional additive-blended trail particles for a ghostly ribbon effect
- Procedural gradient sky sphere (no texture loading)
- Ambient dust particles for atmospheric depth
- `FogExp2` for distance fade

## What It Looks Like

Imagine standing in a field at dusk in Rome. Above you, thousands of starlings wheel and fold in impossible shapes — liquid geometry, breathing as one. The flock splits around a diving hawk, two dark rivers of wings pouring apart, then rushing back together in a moment of collective grace.

That's what this simulates. Except you can grab the hawk and throw it through the middle yourself. And then switch to neon mode because why not.

---

*Built with three.js. Inspired by nature's most beautiful algorithm.*
