# Black Hole Gravitational Lensing Simulator

A real-time WebGL 2 simulation of gravitational lensing around a Schwarzschild black hole.

## How to Run

Open `index.html` in any modern browser (Chrome, Firefox, Safari, Edge). No server needed.

## Controls

- **Drag** — move the black hole
- **Scroll** — adjust mass (Schwarzschild radius)
- **Controls panel** (top-right) — mass, spin, brightness, accretion disk toggle, colour themes

## Physics

### Gravitational Lensing
Light passing near a massive object is deflected by spacetime curvature. For a Schwarzschild black hole, the weak-field deflection angle is α = 4GM/(c²b), where b is the impact parameter (closest approach distance). Near the photon sphere (r = 1.5 Rs), deflection becomes extreme — light can orbit multiple times.

### Einstein Ring
When a light source is directly behind the black hole relative to the observer, lensing is symmetric in all directions, producing a bright ring — the Einstein ring.

### Photon Sphere
At r = 1.5 Rs, photons can theoretically orbit the black hole. This creates a bright ring in the simulation where light accumulates.

### Accretion Disk
Hot gas spiralling into the black hole forms a thin disk. The temperature follows T ∝ r^(-3/4), hottest near the innermost stable circular orbit (ISCO) at r = 3 Rs. Doppler boosting makes the approaching side brighter and bluer, the receding side dimmer and redder.

### Gravitational Redshift
Light climbing out of the gravitational well loses energy. Near the event horizon, the redshift factor z = 1/√(1 - Rs/r) - 1 causes light to dim and shift toward red.

## Colour Themes

- **Realistic** — natural blackbody colours
- **False-colour scientific** — remapped channels, astrophysics paper style
- **Interstellar warm** — golden tones inspired by the film
- **Cool blue** — cold, ethereal aesthetic

## Technical Details

Everything runs in a single fragment shader. For each pixel, a ray is cast from the camera, deflected based on its impact parameter relative to the black hole, and sampled against a procedural starfield. The accretion disk is modelled as a thin equatorial plane with temperature-dependent emission and relativistic Doppler boosting.
