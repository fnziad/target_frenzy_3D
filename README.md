# Target Frenzy 3D - Battle Royale Edition

A fast-paced 3D arena shooter with battle royale mechanics, built with Python and OpenGL.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![OpenGL](https://img.shields.io/badge/OpenGL-GLUT-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Features

### Core Gameplay

- **Large Battle Arena** - Massive 4000x4000 unit arena with procedurally generated obstacles for cover
- **Battle Royale Zone** - Shrinking zone that forces action — stay inside or take damage
- **4 Enemy Types** - Each with unique AI, movement patterns, and shooting behavior
- **Enemies Shoot Back** - Dodge enemy fire, use cover, and fight to survive
- **Level/Wave System** - Progressive difficulty with increasing enemy count and variety
- **Combo System** - Chain kills for score multipliers up to 5x
- **Kill Streaks** - Earn bonus points for consecutive kills (Rampage, Unstoppable, Godlike)

### Player Mechanics

- **Sprint System** - Hold Shift to sprint with stamina management
- **Smooth Movement** - Physics-based momentum with friction
- **First/Third Person** - Toggle between camera perspectives
- **Name Entry** - Enter your name at game start, shown in HUD and game over stats

### Power-Up System

| Power-Up     | Color  | Effect                  | Duration   |
| ------------ | ------ | ----------------------- | ---------- |
| Health Pack  | Green  | Restores 30 HP          | Instant    |
| Speed Boost  | Blue   | 1.5x movement speed     | 10 seconds |
| Damage Boost | Red    | 2x weapon damage        | 10 seconds |
| Shield       | Yellow | Absorbs up to 50 damage | 15 seconds |

### Enemy Types

| Type       | Behavior                                  | Threat    |
| ---------- | ----------------------------------------- | --------- |
| **Grunt**  | Standard chaser, moderate accuracy        | Medium    |
| **Tank**   | Slow but heavily armored, high damage     | High      |
| **Scout**  | Fast zigzag movement, agile               | Medium    |
| **Sniper** | Maintains distance, highly accurate shots | Very High |

### Visual Features

- OpenGL lighting and shading
- Atmospheric fog effect
- Particle effects on kills and impacts
- Enemy health bars
- Damage flash overlay
- Pulsing zone boundary with translucent walls
- Rotating, bobbing power-up pickups
- Shield visual effect around player
- Minimap with real-time tracking

### HUD

- Health, Shield, and Stamina bars
- Score with combo multiplier display
- Level and kill progress
- Active power-up timers
- Kill streak notifications
- Crosshair in first-person mode
- Minimap showing enemies, power-ups, zone, and obstacles
- Zone shrinking warnings

## Controls

### Movement

| Key              | Action                  |
| ---------------- | ----------------------- |
| **W**            | Move forward            |
| **S**            | Move backward           |
| **A**            | Turn left               |
| **D**            | Turn right              |
| **Shift + Move** | Sprint (drains stamina) |

### Combat

| Key                    | Action                   |
| ---------------------- | ------------------------ |
| **Space / Left Click** | Fire weapon              |
| **Right Click / F**    | Toggle first-person view |

### Camera (Third Person)

| Key                  | Action                  |
| -------------------- | ----------------------- |
| **Arrow Up**         | Zoom in / lower camera  |
| **Arrow Down**       | Zoom out / raise camera |
| **Arrow Left/Right** | Rotate camera           |

### System

| Key   | Action              |
| ----- | ------------------- |
| **P** | Pause/Resume        |
| **R** | Restart (when dead) |

## Installation

### Prerequisites

- Python 3.7+
- pip

### Setup

```bash
git clone https://github.com/fnziad/target_frenzy_3D.git
cd target_frenzy_3D
pip install -r requirements.txt
```

### Run

```bash
python run_game.py
```

Or directly:

```bash
python src/target_frenzy_3d.py
```

## Game Flow

1. **Name Entry** — Type your player name and press Enter
2. **Guidelines** — Review controls and game info, press Enter to start
3. **Battle** — Survive waves of enemies in a shrinking arena
4. **Level Up** — Kill enough enemies to advance (heals +20 HP per level)
5. **Game Over** — View your stats (score, kills, streak, accuracy, time)
6. **Restart** — Press R to try again

## Scoring

- **Base Points**: Vary by enemy type (10-25 per kill)
- **Combo Multiplier**: Up to 5x for chaining kills within 3 seconds
- **Kill Streak Bonuses**:
  - 5 kills: _Rampage!_ (+50 points)
  - 10 kills: _Unstoppable!_ (+100 points)
  - 15 kills: _Godlike!_ (+200 points)

## Project Structure

```
target-frenzy-3d/
├── src/
│   ├── target_frenzy_3d.py    # Main game (1100+ lines)
│   └── OpenGL/                 # OpenGL Python bindings
├── run_game.py                 # Launcher script
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

## Technical Details

- **Graphics**: OpenGL with GLUT, lighting, fog, blending
- **Language**: Python 3
- **Rendering**: 3D models using OpenGL primitives (spheres, cylinders, cubes, quads)
- **Physics**: Momentum-based movement with friction
- **AI**: 4 distinct enemy behaviors (chase, zigzag, maintain-distance, direct)
- **Collision**: Distance and AABB-based detection
- **Timing**: Frame-rate independent using delta time

## Author

**Fahad Nadim Ziad**

## License

MIT License — see [LICENSE](LICENSE) for details.
