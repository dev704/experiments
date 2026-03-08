# Physarum — Slime Mold Transport Networks

A GPU-accelerated simulation of *Physarum polycephalum* (slime mold) transport network formation, running entirely in the browser using WebGL 2.

## What is this?

Physarum polycephalum is a slime mold that creates remarkably efficient transport networks. This simulation models hundreds of thousands of virtual agents that:

1. **Move** forward in their current direction
2. **Sense** pheromone levels at three points ahead (left, center, right sensors)
3. **Turn** toward the strongest pheromone signal
4. **Deposit** pheromone where they walk
5. **Diffuse & decay** — the pheromone trail spreads and fades over time

The result: stunning emergent organic networks that resemble neural pathways, road networks, river deltas, and cosmic filaments — all from simple local rules.

## How to run

Open `index.html` in any modern browser (Chrome, Firefox, Edge, Safari). No server needed — it's a single self-contained file.

```bash
# Or serve locally
python3 -m http.server 8000
# Then open http://localhost:8000
```

## Architecture

Everything runs on the GPU via WebGL 2 with floating-point textures:

- **Agent state texture** — Each pixel stores one agent's position (x,y), heading angle, and species ID. A 512×512 texture = 262,144 agents.
- **Trail map texture** — Full-resolution pheromone concentration field.
- **Four GPU passes per frame:**
  1. **Agent update** — Fragment shader reads agent states + trail map → computes new heading via 3-sensor comparison → writes new position/heading
  2. **Deposit** — Point primitives rendered into trail FBO with additive blending (vertex texture fetch reads positions from agent texture)
  3. **Diffuse + Decay** — Box blur + multiplicative decay on the trail map
  4. **Render** — Maps trail intensity to a colour palette

## Parameters

| Parameter | Range | Default | Effect |
|-----------|-------|---------|--------|
| **Sensor Angle** | 5° – 90° | 30° | Angle offset for left/right sensors. Higher = wider sensing cone |
| **Sensor Distance** | 1 – 60 px | 12 | How far ahead agents look. Higher = more global patterns |
| **Turn Speed** | 0.05 – 1.5 rad | 0.35 | Max rotation per step. Higher = sharper turns |
| **Move Speed** | 0.2 – 5 px | 1.2 | Pixels moved per step |
| **Deposit** | 0.5 – 20 | 5.0 | Pheromone deposited per step. Higher = brighter trails |
| **Decay** | 0.9 – 0.999 | 0.97 | Trail persistence. Higher = longer-lasting trails |
| **Diffuse** | 0.01 – 0.5 | 0.18 | Blur strength. Higher = smoother, more spread-out trails |

## Spawn Patterns

- **Random** — Uniform random positions and angles across the canvas
- **Center Burst** — All agents start at center with random angles (explosion outward)
- **Ring** — Agents arranged on a circle, pointing inward (gorgeous collapse patterns)
- **Multi-Ring** — Four concentric rings collapsing inward
- **Dual Species** — Two populations with different sensor parameters sharing the trail

## Colour Palettes

1. **Bio** — Black → green → yellow → white (classic slime mold)
2. **Neural** — Dark blue → cyan → white (brain/neural aesthetic)
3. **Magma** — Black → red → orange → yellow → white
4. **Neon** — Dark → purple → electric blue → pink
5. **Monochrome** — Pure white on black
6. **Cosmic** — Deep purple → blue → cyan → white (cosmic web)

## Interaction

- **Click/tap** on the canvas to deposit a burst of pheromone, attracting nearby agents
- **Drag** to continuously deposit pheromone along a path
- Works on mobile with touch

## Tips for beautiful patterns

- **Ring + Neural palette** — Classic collapse into web-like structure
- **Low sensor angle (10-15°) + high decay (0.99)** — Dense, thick trunk networks
- **High sensor angle (60°+) + low decay (0.95)** — Wispy, fractal-like tendrils
- **Center burst + Cosmic** — Expanding universe aesthetic
- **High deposit + low diffuse** — Sharp, high-contrast trails
- **Dual species** — Two interacting networks that compete for space

## Requirements

- WebGL 2 with `EXT_color_buffer_float` extension (virtually all modern browsers)
- No external dependencies — pure WebGL 2, no libraries

## Credits

Inspired by the work of Jeff Jones ("Characteristics of pattern formation and evolution in approximations of Physarum transport networks", 2010) and Sage Jenson's beautiful Physarum visualizations.
