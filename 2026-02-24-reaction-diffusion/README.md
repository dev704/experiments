# 🧬 Reaction-Diffusion — Turing Patterns

Interactive GPU-accelerated Gray-Scott reaction-diffusion simulator. Two virtual chemicals interact and diffuse across a 2D grid, producing the same patterns found in nature: coral, fingerprints, animal markings, cell division, and more.

![Gray-Scott model](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Turing_pattern_2.jpg/320px-Turing_pattern_2.jpg)

## How It Works

The **Gray-Scott model** simulates two chemicals (A and B):
- **A** is continuously fed into the system
- **B** consumes A to reproduce (`A + 2B → 3B`)
- **B** also naturally decays (kill rate)
- Both chemicals diffuse spatially, but at different rates

The interplay of feed rate (**f**) and kill rate (**k**) produces wildly different emergent patterns — from spots to stripes to spirals to pulsing mitosis.

## Features

- **WebGL 2 GPU-accelerated** — runs the simulation entirely on the graphics card
- **8 curated presets** — Mitosis, Coral, Fingerprint, Spirals, Worms, Spots, Maze, Holes
- **5 colour palettes** — Plasma, Ocean, Ember, Mono, Neon
- **Interactive seeding** — click/drag to drop chemical B
- **Real-time parameter tuning** — adjust f, k, simulation speed, brush size
- **Touch support** — works on mobile

## Controls

| Input | Action |
|-------|--------|
| Click/drag | Seed chemical B |
| Space | Pause/resume |
| R | Reset with random seeds |
| C | Clear to blank state |
| Sliders | Adjust feed rate, kill rate, speed, brush |

## Run It

Just open `index.html` in any modern browser. Zero dependencies.

```bash
# or serve it
python3 -m http.server 8000
# then open http://localhost:8000
```

## The Science

Alan Turing proposed in 1952 that chemical morphogens diffusing and reacting could explain biological pattern formation — why zebras have stripes, leopards have spots, and corals grow in branching fractal shapes. The Gray-Scott model is one of the simplest systems that exhibits this rich behaviour.

The parameter space (f, k) contains an extraordinary zoo of patterns. Each preset explores a different region of this space.

## Tech

- Single HTML file, ~16KB
- WebGL 2 fragment shaders for simulation + rendering
- Ping-pong framebuffer technique (two textures, swap each step)
- RG32F floating-point textures for chemical concentrations
- Runs at half resolution for performance, rendered at full screen size

---

*Built at 2am on 2026-02-24 as part of the nightly experiments series.*
