# 🌀 Mandelbulb Explorer

A real-time 3D Mandelbulb fractal explorer using WebGL 2 ray marching — single HTML file, zero dependencies.

## What It Is

The [Mandelbulb](https://en.wikipedia.org/wiki/Mandelbulb) is a three-dimensional fractal, an extension of the Mandelbrot set into 3D using spherical coordinates. This explorer renders it in real time on your GPU using ray marching in a fragment shader.

## How to Run

```
open index.html
```

That's it. Any modern browser with WebGL 2 support (Chrome, Firefox, Safari 15+, Edge).

## Controls

| Input | Action |
|---|---|
| Mouse drag | Orbit camera |
| Scroll wheel | Zoom in/out |
| Touch drag | Orbit (mobile) |
| Pinch | Zoom (mobile) |

**UI panel (top-right):**
- **Power** (2–20): Changes the Mandelbulb formula exponent. Power 8 is the classic organic shape; lower values produce smoother forms, higher values create more intricate spikes.
- **Iterations** (2–50): More iterations = more fractal detail, but slower.
- **AO Strength**: Controls how dark the crevices appear.
- **Palette**: Magma, Ocean, Neon, Grayscale, Alien.

## The Math

### Mandelbulb Formula

The Mandelbulb extends `z → z² + c` to 3D using spherical coordinates:

1. Convert `z = (x, y, z)` to spherical: `r = |z|, θ = acos(z/r), φ = atan2(y, x)`
2. Apply the power-n map: `z → r^n · (sin(nθ)cos(nφ), sin(nθ)sin(nφ), cos(nθ)) + c`
3. Repeat. If `|z|` escapes (> 2), the point is outside the fractal.

### Ray Marching

Instead of polygons, we cast a ray from the camera through each pixel and step along it. At each step we evaluate a **distance estimator (DE)** — a function that returns a lower bound on the distance to the fractal surface. We step by that distance (sphere tracing), guaranteeing we never overshoot. When the DE returns a tiny value, we've hit the surface.

### Distance Estimation

The DE for the Mandelbulb uses the running derivative `dr` tracked during iteration:

```
DE = 0.5 · ln(r) · r / dr
```

This gives an analytic estimate of the distance to the fractal boundary, enabling efficient sphere tracing with far fewer steps than naïve fixed-step marching.

### Lighting

- **Diffuse** from two directional lights
- **Soft shadows** via secondary ray marches toward the light (penumbra estimated from closest-pass ratio)
- **Ambient occlusion** approximated from the ray march step count — deeper crevices require more steps
- **Specular** highlights on the primary light
- **Colour** derived from orbit trap distance (minimum `|z|` during iteration)

## Performance

- Mobile renders at 0.5× resolution automatically
- Adaptive step size (0.7× DE) balances quality vs speed
- 128 max ray march steps with early termination
- 32 steps for shadow rays
