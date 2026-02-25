# Strange Attractors Explorer

**An interactive WebGL 2 visualizer for chaotic dynamical systems.**

![Lorenz Attractor](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Lorenz_attractor.svg/200px-Lorenz_attractor.svg.png)

## What Is This?

Explore 8 famous strange attractors rendered as flowing particle trails in real-time:

- **Lorenz** — the butterfly effect (1963)
- **Rössler** — simplest continuous chaos (1976)
- **Aizawa** — cosmic jellyfish torus
- **Thomas** — cyclically symmetric beauty (1999)
- **Halvorsen** — three-lobed tumbling symmetry
- **Chen-Lee** — rigid body chaos
- **Dadras** — multi-scroll dynamics (2010)
- **Sprott** — minimalist chaos

Each attractor simulates tens of thousands of particles following deterministic equations that produce unpredictable, never-repeating paths. The simulation uses RK4 integration on the GPU via transform feedback in fragment shaders.

## Features

- 🎨 **5 color palettes** — Plasma, Ocean, Fire, Aurora, Neon
- 🖱️ **Interactive** — drag to rotate, scroll to zoom
- ⚡ **GPU-accelerated** — RK4 integration + rendering in WebGL 2 fragment shaders
- 🎛️ **Adjustable** — trail length, simulation speed, particle count (10k–200k)
- 📱 **Touch support** — works on mobile
- 📐 **Additive blending** — particles glow where orbits converge

## How to Run

```bash
# Just open the HTML file
open index.html
# or
python3 -m http.server 8000
# then visit http://localhost:8000
```

Single HTML file, zero dependencies, ~24KB.

## The Math

Each attractor is a system of three ordinary differential equations:

**Lorenz:** dx/dt = σ(y-x), dy/dt = x(ρ-z)-y, dz/dt = xy-βz

These simple equations produce infinitely complex, never-repeating trajectories — deterministic chaos. The particles trace these paths, revealing the hidden geometry of chaos.

## Built

2026-02-25 — 2am experiment by Claude 🐙
