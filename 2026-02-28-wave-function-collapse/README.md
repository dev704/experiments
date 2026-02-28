# Wave Function Collapse — Procedural Pattern Generator

## What is WFC?

Wave Function Collapse is a procedural generation algorithm inspired by quantum mechanics. Every cell in a grid starts in a "superposition" of all possible tiles. The algorithm repeatedly:

1. **Observe** — Find the cell with the lowest entropy (fewest remaining options)
2. **Collapse** — Randomly choose one tile for that cell
3. **Propagate** — Remove incompatible tiles from neighboring cells based on adjacency rules
4. **Repeat** — Until every cell is resolved, or a contradiction is detected

If a contradiction occurs (a cell has zero valid options), the algorithm restarts.

## How to Run

Just open `index.html` in any modern browser. No server, no dependencies.

```bash
open index.html
# or
xdg-open index.html
```

## Controls

| Control | Description |
|---------|-------------|
| **Tileset** | Choose from Circuit Board, Pipes, Terrain, or Abstract Geometric |
| **Grid Size** | Slider from 10×10 to 50×50 |
| **Speed** | Steps per animation frame (1–20) |
| **Play/Pause** | Toggle automatic generation |
| **Step** | Advance one collapse step manually |
| **Generate New** | Restart with a fresh random seed |
| **Entropy Heatmap** | Toggle overlay showing remaining possibilities per cell |
| **Click a cell** | Force-collapse it to a specific tile |

## Algorithm Details

### Tiles & Sockets

Each tile has four edges (N, E, S, W). Each edge has a **socket type** — a label describing what kind of connection it offers. Two tiles can be placed adjacent if their touching edges have matching socket types.

### Rotation

Base tiles are automatically rotated (90°, 180°, 270°) to generate variants, with socket labels rotated accordingly.

### Entropy

Entropy = number of remaining valid tiles for a cell. Lower entropy = more constrained = collapsed first. Ties are broken randomly for variety.

### Contradiction Handling

When propagation leaves a cell with zero options, the contradiction area flashes red and the algorithm restarts.

## Credits & References

- **Original WFC** by Maxim Gumin: [github.com/mxgmn/WaveFunctionCollapse](https://github.com/mxgmn/WaveFunctionCollapse)
- Inspired by quantum superposition concepts
- Built as a single-file vanilla JS/Canvas experiment
