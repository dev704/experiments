# 🌌 Procedural Spiral Galaxy Generator

A real-time 3D procedural spiral galaxy you can fly through, built with three.js. Scientifically inspired by density wave theory.

## What It Does

Generates a spiral galaxy with ~200,000 particles using mathematically accurate logarithmic spiral equations. Features multiple star populations (core bulge, disk/arm stars, young blue stars, halo stars), nebula clouds simulating H-II regions, and post-processing bloom for that authentic cosmic glow.

## How to Run

Open `index.html` in any modern browser. No server required — everything loads from CDN.

```bash
# Or serve locally:
cd experiments/2026-03-07-galaxy-generator
python3 -m http.server 8080
# Visit http://localhost:8080
```

## Controls

| Control | Range | What It Does |
|---------|-------|-------------|
| **Arms** | 2–6 | Number of spiral arms |
| **Arm Tightness** | 0.1–0.8 | How tightly wound the spiral is (higher = tighter) |
| **Arm Spread** | 0.1–1.2 | Star dispersion from arm center (higher = fuzzier arms) |
| **Core Size** | 0.05–0.4 | Size of the central bulge relative to galaxy radius |
| **Galaxy Radius** | 20–100 | Overall size of the galaxy |
| **Rotation Speed** | 0–0.1 | How fast the galaxy rotates |
| **Color Theme** | 3 options | Visual style (see below) |
| **Autopilot** | Toggle | Smooth fly-through camera path |
| **Regenerate** | Button | Re-roll the galaxy with current settings |

### Color Themes

- **Realistic** — Natural star colors: warm core, mixed arms with blue star-forming regions
- **Nebula Heavy** — Pink/purple tones with vivid nebula clouds
- **Infrared False-Color** — Yellow/orange/cyan palette mimicking infrared telescope imagery

## Navigation

- **Mouse drag** — Orbit around the galaxy
- **Scroll wheel** — Zoom in/out
- **Touch** — One finger to rotate, two fingers to zoom/pan
- **Autopilot** — Toggle for a hands-free fly-through (disables manual controls)

## Technical Details

- **180,000 stars** + **12,000 nebula particles** + **4,000 background stars**
- `THREE.Points` with custom `ShaderMaterial` for vertex-level size attenuation and per-star color
- Logarithmic spiral positioning: `r = a × e^(b×θ)` with Gaussian perpendicular dispersion
- Core bulge: 3D oblate Gaussian distribution
- Halo stars: spherical distribution with warm/old star colors
- Post-processing bloom via `UnrealBloomPass`
- Additive blending for natural stellar glow
- Mobile-responsive controls panel (collapses on small screens)

## Dependencies

All loaded from CDN (no local dependencies):
- [three.js](https://threejs.org/) v0.170.0
- OrbitControls, EffectComposer, RenderPass, UnrealBloomPass (three.js examples)
