# Target Frenzy 3D 🎯

A fast-paced 3D first-person shooter game built with OpenGL and Python. Battle against waves of enemies in an arena-style combat environment!

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![OpenGL](https://img.shields.io/badge/OpenGL-GLUT-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎮 Features

- **Immersive 3D Graphics**: Full 3D rendering using OpenGL with smooth camera controls
- **Dynamic Gameplay**: Face increasingly challenging waves of enemies that adapt to your score
- **Multiple View Modes**: Switch between third-person and first-person perspectives
- **Smooth Movement System**: Physics-based player movement with momentum and friction
- **Score Tracking**: Track your hits, misses, and overall performance
- **Difficulty Scaling**: Enemy speed increases as you progress

## 🕹️ Controls

### Movement
- **W**: Move forward
- **S**: Move backward
- **A**: Turn left / Strafe left (easy mode)
- **D**: Turn right / Strafe right (easy mode)

### Combat
- **Space Bar** / **Left Click**: Fire weapon
- **Right Click**: Toggle first-person view

### Camera (Third-Person Mode)
- **Arrow Up**: Zoom in and lower camera
- **Arrow Down**: Zoom out and raise camera
- **Arrow Left**: Rotate camera left
- **Arrow Right**: Rotate camera right

### Special
- **C**: Toggle cheat mode (for testing)
- **V**: Toggle vision mode (when in first-person + cheat mode)
- **R**: Restart game

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/target-frenzy-3d.git
cd target-frenzy-3d
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python run_game.py
```

Or directly:
```bash
python src/target_frenzy_3d.py
```

## 🎯 Gameplay

- Eliminate enemies (red spheres) by shooting them
- Enemies chase you and deal damage on contact
- Score points for each successful hit
- Avoid missing too many shots (max 10 misses in normal mode)
- Enemy speed increases as your score grows
- Game ends when you run out of health or miss too many shots

## 🏗️ Project Structure

```
target-frenzy-3d/
├── src/
│   ├── target_frenzy_3d.py    # Main game file
│   └── OpenGL/                 # OpenGL Python bindings
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

## 🛠️ Technical Details

- **Graphics**: OpenGL with GLUT for rendering
- **Language**: Python 3
- **Rendering**: 3D models using OpenGL primitives (spheres, cylinders, cubes)
- **Physics**: Custom momentum-based movement system
- **Collision Detection**: Distance-based hit detection

## 📝 Game Mechanics

### Player Stats
- Health: 5 HP
- Movement Speed: 10 units/frame
- Rotation Speed: 5°/frame (normal), 45°/frame (cheat mode)

### Enemies
- Initial Count: 5 enemies per wave
- Base Speed: 0.025 units/frame
- Speed Multiplier: Increases up to 3x based on player score
- Damage: 1 HP per hit
- Hit Radius: 60 units (80 in cheat mode)

### Weapons
- Fire Rate: 0.5 seconds
- Projectile Speed: 4 units/frame
- Projectile Size: 8 units
- Accuracy: Random spread (varies by mode and view)

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Fahad Nadim Ziad**

## 🙏 Acknowledgments

- Built with PyOpenGL
- Inspired by classic arena shooter games
- OpenGL GLUT for window management and input handling

---

**Enjoy the game! 🎮**
