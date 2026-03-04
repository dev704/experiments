# 🪐 Procedural Planet Generator

An interactive 3D procedural planet generator built with Three.js. Each click of "Generate" creates a unique alien world with terrain, oceans, clouds, atmosphere, and day/night lighting.

## How to Run

Just open `index.html` in any modern browser. No server needed — everything loads from CDN.

```bash
# Or serve locally if you prefer
python3 -m http.server 8000
# Then visit http://localhost:8000
```

## Features

- **Fractal terrain** — FBM (Fractal Brownian Motion) noise in GLSL displaces a sphere mesh to create mountains, valleys, and plains. Altitude-based colouring from ocean depths to snow peaks.
- **Transparent ocean** — Fresnel-reflective water sphere with animated vertex-displaced waves.
- **Atmosphere** — Rim-lit glow shell tinted by planet type, brighter on the sun-facing side.
- **Volumetric clouds** — Independent sphere with noise-based alpha, slowly rotating at a different speed than the surface.
- **Day/night cycle** — Directional sun light with a visible terminator. The dark side shows city lights (or volcanic glow on volcanic worlds).
- **Star field** — 3,000-point particle background.
- **5 planet presets** — Earth-like, Desert, Ice, Volcanic, Gas Giant. Each tunes terrain roughness, ocean level, cloud density, colours, and atmosphere.
- **Live sliders** — Rotation speed, cloud density, ocean level, terrain roughness.
- **Orbit controls** — Drag to rotate, scroll to zoom, touch-friendly.
- **Planet stats** — Type, radius, ocean coverage, roughness, and seed displayed in the UI.

## What's Interesting

All terrain generation happens in GLSL vertex/fragment shaders — no CPU-side geometry modification. The planet surface uses 6-octave FBM simplex noise for displacement and altitude-based colour mapping. This means generation is instant (no mesh rebuild) and runs at 60fps.

The night side city lights use a separate noise function thresholded against a land mask, so lights only appear on terrain above sea level — a small detail that sells the effect.

Each "Generate" click randomizes the noise seed plus adds colour jitter to the preset palette, so even within the same planet type you get meaningfully different worlds.

## Tech Stack

- [Three.js](https://threejs.org/) v0.170 (ES modules from CDN)
- Custom GLSL ShaderMaterial for all planet layers
- Simplex noise (Ashima/webgl-noise) implemented in GLSL
- Zero dependencies, single HTML file (~26KB)
