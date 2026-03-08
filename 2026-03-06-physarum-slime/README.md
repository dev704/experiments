# Physarum Slime Mold Simulation

## What is Physarum?

**Physarum polycephalum** is a remarkable single-celled organism — a slime mold that can solve complex optimization problems without a brain. In a famous 2010 experiment, researchers placed food sources at locations matching Tokyo's major rail stations. The Physarum network that grew between them closely replicated the actual Tokyo rail system — a network designed by teams of engineers over decades.

This simulation recreates Physarum's behaviour using hundreds of thousands of virtual agents running entirely on the GPU.

## How It Works

The simulation is **agent-based** and **GPU-accelerated** using WebGL 2:

1. **Agents** (stored as pixels in a texture) each have a position and heading angle
2. Each frame, every agent:
   - **Senses** the chemical trail map at three points ahead (left, center, right)
   - **Rotates** toward the strongest trail concentration
   - **Moves** forward in its current direction
   - **Deposits** chemical trail at its new position
3. The **trail map** diffuses (spreads) and decays each frame
4. The emergent result: stunning organic networks, veins, and tendrils

### Multi-Species

Up to 3 species can coexist, each depositing on a different colour channel (R/G/B). Species interact and compete for space, creating beautiful interleaving patterns.

## How to Run

Just open `index.html` in a modern browser (Chrome, Firefox, Edge, Safari). No server needed. Requires WebGL 2 support.

## Controls

| Control | Range | Description |
|---------|-------|-------------|
| Sensor Angle | 10°–90° | Angle between forward and side sensors |
| Sensor Distance | 5–50px | How far ahead agents sense |
| Turn Speed | 0.1–2.0 | How quickly agents rotate |
| Deposit Amount | 0.1–5.0 | Trail chemical deposited per step |
| Decay Rate | 0.90–1.00 | How quickly trails fade (1.0 = never) |
| Diffuse Rate | 0.0–1.0 | How much trails spread each frame |
| Species | 1–3 | Number of competing species |
| Agent Count | 100K/500K/1M | Number of simulated agents |

### Presets
- **Network** — Classic veiny transport network
- **Tendrils** — Wispy, reaching filaments
- **Maze** — Tight labyrinthine patterns
- **Galaxy** — Spiral arm formations

### Interaction
- **Click/touch** to attract agents and deposit extra trail chemical
- **Palette selector** to change colour mapping
- **Fullscreen** button for immersive viewing

## Screenshot

![Physarum simulation showing organic network patterns](screenshot-placeholder.png)

*The simulation produces emergent network structures reminiscent of biological vasculature, fungal mycelium, and urban transport networks.*

## Technical Details

- All computation runs on the GPU via WebGL 2 fragment shaders
- Agent state stored in floating-point textures (RG = position, B = angle, A = species)
- Trail map uses ping-pong framebuffers for double-buffered updates
- Toroidal topology (agents wrap around edges)
- 5 colour palettes: Bio, Neon, Fire, Ocean, Mono
