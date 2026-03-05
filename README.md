<p align="center">
  <h1 align="center">Last Stand Arena</h1>
  <p align="center">
    A complete 3D battle royale arena shooter — built from scratch in Python with OpenGL. Survive. Eliminate. Dominate.
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/OpenGL-PyOpenGL-5586A4?style=for-the-badge&logo=opengl&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Lines_of_Code-2600+-f97316?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-8b5cf6?style=for-the-badge"/>
</p>

---

## About the Game

**Last Stand Arena** is a real-time 3D battle royale shooter written entirely in Python using the OpenGL fixed-function pipeline. All geometry, AI, physics, rendering, and UI are hand-coded from scratch — no game engine, no assets, just pure code.

Fight through waves of intelligent enemies across a massive arena while a shrinking zone forces you into relentless action. Switch between three weapons, land headshots, chain combo kills, and survive as long as you can.

> Made by **Fahad Nadim Ziad** — 2026

---

## Features at a Glance

### 🔫 Three-Weapon Arsenal

| Weapon          | Key | Damage | Rate   | Ammo | Style                   |
|-----------------|:---:|--------|--------|------|-------------------------|
| Pistol          | `1` | 12     | Slow   | 50   | Precise single shots    |
| Assault Rifle   | `2` | 10     | Fast   | 120  | Full-auto tracer rounds |
| Shotgun         | `3` | 8 × 6  | Slow   | 24   | 6-pellet spread blast   |

- Each weapon has a **unique first-person 3D model** rendered in-engine
- Manual reload with `R`, auto-reload on empty, ammo refills on kills

### 👾 Four Enemy Types

| Type    | HP | Speed | Behaviour                          |
|---------|----|-------|------------------------------------|
| Grunt   | 30 | 3.5   | Direct chaser, medium accuracy     |
| Tank    | 80 | 1.8   | Slow, heavy armour, high damage    |
| Scout   | 15 | 6.0   | Fast zigzag, hard to track         |
| Sniper  | 25 | 1.2   | Holds distance, highly accurate    |

- All enemies **shoot back** with type-specific accuracy and fire rates
- HP scales with level (+12% per level)

### 💊 Power-Ups (with 3D models)

| Power-Up     | Shape           | Effect                   |
|--------------|-----------------|--------------------------|
| Health Pack  | Green cross     | +30 HP                   |
| Speed Boost  | Blue diamond    | 1.5× speed for 10 s      |
| Damage Boost | Red spiky star  | 2× damage for 10 s       |
| Shield       | Yellow dome     | 50 HP absorb for 15 s    |

### 🎯 Combat Feel

- **Headshots** — Upper-body hits deal 2× damage and trigger a red hit marker
- **Hit markers** — X-shaped crosshair flash on every hit
- **Floating damage numbers** — Damage pops up on screen in real time
- **Muzzle flash overlay** — Visual recoil feedback when firing
- **Particle effects** — Kills and impacts burst with coloured particles

### 🏟️ Battle Royale Zone

- 10 000 × 10 000 unit outdoor arena with procedural crates and pillars
- Zone shrinks every 60 seconds starting from level 2
- Getting caught outside the zone deals continuous damage
- Zone position drifts randomly to keep you moving

### 📊 Scoring

- Combo multiplier up to **5×** for chaining kills within 3 seconds
- Kill-streak milestones: **Rampage (×5)**, **Unstoppable (×10)**, **Godlike (×15)**
- Headshot kills award 1.5× score bonus
- Full stat screen on death: score, level, kills, streak, combo, time, accuracy

---

## Controls

| Action                  | Key(s)               |
|-------------------------|----------------------|
| Move forward / back     | `W` / `S`            |
| Rotate left / right     | `A` / `D`            |
| Strafe left / right     | `Q` / `E`            |
| Sprint                  | `Shift` + move       |
| Fire                    | `Space`              |
| Switch weapon           | `1` / `2` / `3`      |
| Reload                  | `R`                  |
| Toggle FP / 3P camera   | `F`                  |
| Zoom (third person)     | `Arrow Keys`         |
| Pause / Resume          | `P`                  |
| Restart (after death)   | `R`                  |
| Quit                    | `ESC`                |

---

## Installation & Running

> Full step-by-step guide: see **[INSTALL.md](INSTALL.md)**

**Quick start:**

```bash
# 1. Clone the repository
git clone https://github.com/fnziad/last_stand_arena.git
cd last_stand_arena

# 2. Install the dependency
pip install -r requirements.txt

# 3. Play
python run_game.py
```

**Requirements:** Python 3.7 or later, PyOpenGL 3.x

---

## Project Structure

```
last_stand_arena/
├── src/
│   └── last_stand_arena.py   # Complete game engine (~2,600 lines)
├── run_game.py               # Launcher with controls reference
├── requirements.txt          # Single dependency: PyOpenGL
├── INSTALL.md                # Full installation guide
├── README.md                 # This file
├── PROJECT_INFO.txt          # Detailed technical overview
└── LICENSE                   # MIT License
```

---

## Technical Overview

| Area             | Implementation                                          |
|------------------|---------------------------------------------------------|
| Language         | Python 3                                                |
| Graphics API     | OpenGL 2.x fixed-function via PyOpenGL + GLUT           |
| 3D Models        | Primitives: cubes, spheres, octahedra, tori, cylinders  |
| Physics          | Momentum + friction, delta-time scaled, AABB + sphere  |
| AI               | 4 behaviour trees: chase, zigzag, range-hold, direct   |
| Frame rate       | 60 FPS target with sleep-based limiter                  |
| Architecture     | Single-file engine, modular functions, state machine   |

---

## Author

**Fahad Nadim Ziad** — [@fnziad](https://github.com/fnziad)

---

## License

MIT License — see [LICENSE](LICENSE) for full text.
