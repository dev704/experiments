# Fluid Simulation — Navier-Stokes on GPU

A real-time 2D fluid simulation running entirely on the GPU via WebGL 2 fragment shaders.

![Neon fluid](https://img.shields.io/badge/WebGL_2-Fluid_Sim-blueviolet)

## How to Run

Just open `index.html` in any modern browser (Chrome, Firefox, Edge, Safari 15+). No server, no dependencies, no build step.

```bash
# Or serve locally:
python3 -m http.server 8000
# Then open http://localhost:8000
```

## The Math

This implements **Jos Stam's "Stable Fluids"** (1999), solving the incompressible Navier-Stokes equations on a 2D grid:

### Navier-Stokes (2D, incompressible)
```
∂u/∂t = -(u·∇)u - ∇p + ν∇²u + f
∇·u = 0
```

Where **u** is velocity, **p** is pressure, **ν** is viscosity, and **f** is external forces.

### Simulation Steps (per frame)

1. **Vorticity Confinement** — Compute curl of velocity field, then apply a confinement force to counteract numerical dissipation of vortices. This keeps the flow looking swirly and organic.

2. **Advection** (Semi-Lagrangian) — For each grid cell, trace backwards along the velocity field by `dt` and sample the value there using bilinear interpolation. Unconditionally stable regardless of timestep.

3. **Divergence** — Compute ∇·u (how much fluid is being "created" or "destroyed" at each point).

4. **Pressure Solve** — Solve the Poisson equation `∇²p = ∇·u` using **Jacobi iteration** (30 iterations per frame). This finds the pressure field needed to make the flow divergence-free.

5. **Gradient Subtraction** — Subtract ∇p from velocity to project it onto the divergence-free field: `u = u - ∇p`.

6. **Dye Advection** — Advect the visible dye/color field using the corrected velocity, with configurable dissipation.

7. **Bloom Post-Processing** — Threshold bright pixels, Gaussian blur at quarter resolution, composite back for a neon glow effect.

### GPU Implementation

- All steps run as **fragment shaders** on the GPU
- **Ping-pong framebuffers** (double-buffered FBOs) for read/write separation
- **HALF_FLOAT textures** for velocity, pressure, and dye fields
- Simulation grid: 512×512, dye grid: 1024×1024
- Mouse/touch input splats Gaussian blobs of velocity and dye

## Controls

| Control | Description |
|---------|-------------|
| **Viscosity** | Velocity dissipation (higher = more damping) |
| **Dye Dissipation** | How quickly dye fades (1.0 = never, 0.9 = fast) |
| **Brush Size** | Radius of the injection splat |
| **Force** | Multiplier for injected velocity |
| **Vorticity** | Strength of vorticity confinement (swirl factor) |
| **Bloom Intensity** | Glow post-processing strength |
| **Display Mode** | Dye (default), Velocity, Pressure, or Vorticity |
| **Pause/Play** | Freeze/resume simulation |
| **Clear** | Reset all fields |

Click/touch and drag on the canvas to inject colorful dye and velocity. Colors cycle through the rainbow automatically.

## References

- Stam, J. (1999). *Stable Fluids*. SIGGRAPH '99.
- Harris, M. (2004). *Fast Fluid Dynamics Simulation on the GPU*. GPU Gems, Ch. 38.
