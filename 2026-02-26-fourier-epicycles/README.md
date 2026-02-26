# Fourier Epicycle Drawing Machine 🌀

A visual demonstration of how **any closed curve can be decomposed into rotating circles** (epicycles) using the Discrete Fourier Transform.

## What It Does

1. **Draw** a freehand shape on the canvas (or pick a preset)
2. The app computes the **DFT** of your path
3. Watch as spinning epicycles **reconstruct your drawing** in real-time

## The Math

Any discrete path of N points can be represented as complex numbers: `z_n = x_n + i·y_n`.

The **Discrete Fourier Transform** decomposes this into N frequency components:

```
X_k = (1/N) Σ z_n · e^(-2πi·k·n/N)
```

Each coefficient X_k has:
- **Amplitude** `|X_k|` → radius of the circle
- **Frequency** `k` → how fast it rotates
- **Phase** `arg(X_k)` → starting angle

Sorting by amplitude (largest first) means the biggest circles capture the overall shape, and smaller ones add detail. Using only the top K coefficients gives a smooth approximation — crank the slider up for more fidelity.

The reconstruction is the inverse: stack all the rotating circles tip-to-tail, and the final tip traces the original path.

## Features

- 🖊️ Freehand drawing with mouse or touch
- ⭐ Preset shapes: star, infinity, treble clef, heart
- 🎛️ Adjustable number of epicycles and animation speed
- 👁️ Toggle original drawing overlay
- 🌙 Dark neon aesthetic
- 📱 Mobile-friendly

## How to Run

```bash
open index.html
# or
python3 -m http.server 8000  # then visit localhost:8000
```

No dependencies. No build step. Just a browser.

## Credits

Inspired by 3Blue1Brown's [Fourier series video](https://www.youtube.com/watch?v=r6sGWTCMz2k) and the timeless beauty of circles drawing anything.

---

*A 2am experiment. 🐙*
