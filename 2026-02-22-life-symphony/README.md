# Life Symphony 🎵🧬

**Conway's Game of Life × Generative Music**

Each living cell sings a note. The X-axis maps to pitch (left = low, right = high), the Y-axis maps to stereo panning. Births shimmer with sine waves, deaths whisper with triangles. The grid plays itself.

## How to Run

```bash
# Just open the HTML file in any browser
open index.html
# or
python3 -m http.server 8080  # then visit localhost:8080
```

Zero dependencies. Single HTML file. Works offline.

## Controls

| Control | Action |
|---------|--------|
| **▶ Play / ⏸ Pause** | Start/stop the simulation (or press Space) |
| **⏭ Step** | Advance one generation |
| **🎲 Random** | Randomize the grid (or press R) |
| **🛩 Glider Gun** | Place a Gosper Glider Gun |
| **🗑 Clear** | Clear the grid (or press C) |
| **Scale** | Choose musical scale (pentatonic, major, minor, chromatic, blues, Japanese) |
| **Speed** | Generations per second |
| **Volume** | Master volume |

Click/drag on the grid to draw cells manually.

## Musical Mapping

- **X position → Pitch**: Cells on the left play low notes, cells on the right play high notes, mapped to the selected musical scale across 3 octaves
- **Y position → Stereo pan**: Top cells pan left, bottom cells pan right
- **Cell births** → bright sine wave pings
- **Cell deaths** → soft triangle wave whispers (limited to 12 per frame for texture, not cacophony)

## Scales

- **Pentatonic**: Safe, always consonant, great default
- **Major/Minor**: Classic Western harmony
- **Blues**: Soulful with the ♭5
- **Japanese** (In scale): Haunting, sparse intervals
- **Chromatic**: Chaotic — all 12 semitones

## What Makes It Interesting

A Gosper Glider Gun creates a repeating rhythmic pattern — like a sequencer that writes itself. Random soups produce dense textures that thin out as the automaton stabilizes. Oscillators (blinkers, pulsars) become drones. Still lifes are silent.

The emergent music is never the same twice.

## Tech

- Canvas 2D for rendering
- Web Audio API for synthesis (oscillators + gain envelopes + stereo panning)
- Toroidal grid (wraps around edges)
- ~200 lines, zero dependencies
