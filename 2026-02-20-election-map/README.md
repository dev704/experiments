# 🗳️ SA Election Results Map — NPE 2024

An interactive choropleth map of South African 2024 National & Provincial Election results by municipality. Built as a reusable component prototype for Coenraad's project.

**Built at 2am on 2026-02-20 🐙**

---

## What it does

- **Interactive choropleth map** of all ~213 SA municipalities, colour-coded by leading party
- **Two ballot views:** National or Provincial
- **Two themes:** Leading Party (with gradient by vote share %) or Voter Turnout heat map
- **Click any municipality** → sidebar shows full results: registered voters, turnout, all party votes + percentages with colour bars
- **Hover tooltip** showing leading party + turnout at a glance
- **Parties covered:** ANC, DA, EFF, MKP (uMkhonto we Sizwe), IFP, VF+, and more
- **Zero API key** — uses Adrian Frith's public election tile server + data API (MIT licensed, CORS-enabled)

## How to run

No build step needed — single HTML file.

### Option A: Python web server (recommended)
```bash
cd experiments/2026-02-20-election-map
python3 -m http.server 8765
# Then open http://localhost:8765 in your browser
```

### Option B: Node.js serve
```bash
npx serve experiments/2026-02-20-election-map -p 8765
```

### Option C: Just open the file
```bash
open experiments/2026-02-20-election-map/index.html
# (Works in most browsers — some may block local fetch requests)
```

### Option D: Docker (expose on network)
```bash
docker run -d -p 8765:80 \
  -v $(pwd)/experiments/2026-02-20-election-map:/usr/share/nginx/html:ro \
  nginx:alpine
```

---

## Tech stack

| Layer | Tech |
|-------|------|
| Map engine | [MapLibre GL JS 4.7](https://maplibre.org) — open-source, no API key |
| Base tiles | CartoDB Dark Matter (free, no key needed) |
| Election tiles | [elections-api.frith.dev](https://elections.adrianfrith.com) — public MVT vector tiles |
| Election data | Adrian Frith's public REST API — MIT licensed |
| UI | Vanilla HTML/CSS/JS (zero dependencies to install) |

---

## Data sources

- **Vector tiles:** `https://elections-api.frith.dev/tiles/muni_npe2024/{z}/{x}/{y}/tile.mvt`
  - Each tile feature has properties: `code`, `name`, `nat_win_party`, `nat_win_perc`, `nat_turnout`, `prov_win_party`, `prov_win_perc`, `prov_turnout`
- **Area detail API:** `https://elections-api.frith.dev/npe2024/{ballot}/muni/{code}`
  - Returns: regpop, valid, spoilt, total, parties[] with votes

Both endpoints are CORS-enabled — can be called from any origin.

---

## How to adapt for your project

### Swap in your own election data
The map is designed to be data-source agnostic. To use your own backend:

1. **Replace the vector tile URL** in `addElectionLayers()`:
   ```js
   tiles: [`https://YOUR-API/tiles/muni_custom/{z}/{x}/{y}/tile.mvt`]
   ```
   Your tiles need properties: `code`, `name`, `nat_win_party`, `nat_win_perc`

2. **Replace the detail API call** in `loadAreaDetail()`:
   ```js
   const res = await fetch(`https://YOUR-API/results/muni/${code}`);
   ```

### Add more elections
Adrian's API also serves:
- `npe2019`, `npe2014` (National elections)
- `lge2021`, `lge2016` (Local government elections)
- Levels: `muni`, `ward`, `vd` (voting district)

### Add ward/VD drill-down
When zoom > 8, switch the source layer to `ward_npe2024` for ward-level detail.

---

## What this proves

✅ MapLibre GL + MVT vector tiles = fast, smooth choropleth with 200+ municipalities  
✅ No backend or build step needed for a working demo  
✅ Party-colour gradients encode both *which* party leads *and* by *how much*  
✅ The IEC/Adrian Frith API is public, reliable, CORS-open — good foundation to build on  

---

## Original source

Based on [afrith/election-map-frontend](https://github.com/afrith/election-map-frontend) (MIT License).  
Hat tip to Adrian Frith for making SA electoral data so accessible.

---

*Built by danger26bot — 2026-02-20 02:00*
