# SONAIR - Sim2real Operational beNchmark for AI Robotics 
## Open Multimodal AI Benchmark & Digital‑Shadow Portal — Nottingham ↔ UCL Co‑Creation
### This is a prototype for the future SONAIR platform, not the final version.

## What’s inside

Landing / Hub — `UoN Multimodal AI Platform.html
  A web‑native hub showcasing pipelines, community exchange, and an entry card *“UR Robotic Arm Calibration (UoN × UCL)”  
No build tools needed; runs directly in the browser.

UR Operation Interface — `UR operation interface.html`
  - Load CSV motion logs (`q_0…q_5` / `j1…j6`; degrees or radians auto‑detect)  
  - Load GLB/GLTF UR rig (GLB hierarchy is authoritative)  
  - Kinematics playback with cubic/linear interpolation, Loop & Ping‑pong (default on)  
  - Calib=1st one‑click offset calibration; joint axis/sign/map editors  
  - Live joint curves (Chart.js) & seek bar, time scaling  
  - Mesh→Point Cloud sampling for the rig (export PLY/XYZ)  
  - External PCD/PLY/XYZ loader with decimation and scale/pose controls

## Entry links (once Pages is enabled)

- Platform home
  `https://mingyutang0728.github.io/OMAIB-UoN-UCL/UoN%20Multimodal%20AI%20Platform.html`

- UR console (auto‑load defaults)  
  `https://mingyutang0728.github.io/OMAIB-UoN-UCL/UR%20operation%20interface.html?csv=UR5e_motion_full_clean.csv&glb=ur5e.glb`


## Auto‑load rules (UR console)

The interface keeps your original file‑input readers intact and simulates user selection programmatically:

- If `?glb=` / `?csv=` are provided, the page fetches those files and injects them into the inputs.  
- If no query params are given, it tries repo‑root fallbacks:
  - `ur5e.glb`  
  - `UR5e_motion_full_clean.csv`  
- A cache‑busting token is appended to avoid stale assets on Pages.  
- The Events panel logs the source path and a short SHA‑256 of each fetched asset for reproducibility.


## CSV & rig notes

- CSV header aliases: 
  Time: `pc_ts|time|timestamp|t|ms|usec|nsec|…`  
  Joints: `q_0..q_5` / `j1..j6`.  
- Degrees vs radians are auto‑detected; angle unwrap removes discontinuities.  
- Calib=1st aligns offsets to your first frame. You may edit:  
  - `Axes` (per joint `x/y/z`)  
  - `Signs` (±1)  
  - `Map` (remap column order)  
- J1 axis auto‑picked to maximize TCP motion response.  
- Mesh→Point Cloud samples per‑mesh by surface area; export global PLY/XYZ.

## Background & intent (SONAIR / deployment‑centric benchmark)

This prototype supports a broader UK‑wide vision: a web‑native, API‑key “rooms” portal for deployment‑centric benchmarking (SONAIR). The portal emphasizes:
- Sim↔Real replication with matched I/O schemas and time‑sync;  
- Cross‑site comparability (UoN ↔ UCL and beyond);  
- System‑level evaluation: selective sensor fusion, long‑horizon/streaming inference, uncertainty & abstention, and edge‑efficiency constraints;  
- Reproducibility: dataset/task/evaluator cards, containerized evaluators, browser replays, and SOPs.

---

## Contributing

Issues and PRs are welcome — especially bugfixes, small UI improvements, and new data loaders or evaluators that keep the no‑bundler philosophy.


## License

- Code: MIT  
- Data / motion CSVs: CC BY 4.0  
Please attribute appropriately when reusing.

## Acknowledgements

University of Nottingham and UCL collaborators. 
Community contributors and UK university partners are welcome — PRs / issues encouraged.
