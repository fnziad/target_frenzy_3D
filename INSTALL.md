# Installation Guide — Last Stand Arena

This guide walks you through installing and running **Last Stand Arena** on macOS, Windows, and Linux.

---

## Requirements

| Requirement | Version  | Notes                                     |
|-------------|----------|-------------------------------------------|
| Python      | 3.7+     | 3.10+ recommended                         |
| pip         | Any      | Comes with Python                         |
| PyOpenGL    | 3.x      | Only external dependency                  |
| OpenGL      | System   | Pre-installed on all desktop OS           |
| GLUT / freeglut | System | See platform notes below              |

---

## Quick Install (All Platforms)

```bash
git clone https://github.com/fnziad/last_stand_arena.git
cd last_stand_arena
pip install -r requirements.txt
python run_game.py
```

---

## Platform-Specific Setup

### macOS

1. **Install Python** (if not already installed):

   ```bash
   # Using Homebrew (recommended)
   brew install python
   ```

   Or download from [python.org](https://www.python.org/downloads/).

2. **Install PyOpenGL:**

   ```bash
   pip3 install PyOpenGL PyOpenGL_accelerate
   ```

3. **Run the game:**

   ```bash
   python3 run_game.py
   ```

   > **Note for Apple Silicon (M1/M2/M3/M4):** GLUT is included in macOS system frameworks.
   > If you see an OpenGL/GLUT error, try:
   > ```bash
   > pip3 install --upgrade PyOpenGL PyOpenGL_accelerate
   > ```

---

### Windows

1. **Install Python** from [python.org](https://www.python.org/downloads/).
   - During install, check **"Add Python to PATH"**.

2. **Install PyOpenGL:**

   ```cmd
   pip install PyOpenGL PyOpenGL_accelerate
   ```

3. **Install freeglut** (required on Windows):
   - Download `freeglut-3.x.x.zip` from [freeglut.sourceforge.net](http://freeglut.sourceforge.net/).
   - Copy `freeglut.dll` to `C:\Windows\System32\` (64-bit) or `C:\Windows\SysWOW64\` (32-bit).

   Alternatively, use the bundled DLL included with PyOpenGL:
   ```cmd
   pip install pyopengl-accelerate
   ```

4. **Run the game:**

   ```cmd
   python run_game.py
   ```

---

### Linux (Ubuntu / Debian)

1. **Install Python and freeglut:**

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip freeglut3 freeglut3-dev
   ```

2. **Install PyOpenGL:**

   ```bash
   pip3 install PyOpenGL PyOpenGL_accelerate
   ```

3. **Run the game:**

   ```bash
   python3 run_game.py
   ```

---

### Linux (Fedora / RHEL)

```bash
sudo dnf install python3 python3-pip freeglut freeglut-devel
pip3 install PyOpenGL PyOpenGL_accelerate
python3 run_game.py
```

---

### Linux (Arch)

```bash
sudo pacman -S python python-pip freeglut
pip install PyOpenGL PyOpenGL_accelerate
python run_game.py
```

---

## Using a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# macOS / Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependency
pip install -r requirements.txt

# Run the game
python run_game.py
```

---

## Verifying Your Installation

Run this quick check before launching the game:

```bash
python3 -c "from OpenGL.GL import *; from OpenGL.GLUT import *; print('OpenGL OK')"
```

If you see `OpenGL OK`, you're good to go.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'OpenGL'` | Run `pip install PyOpenGL` |
| `GLUT not found` / `libglut` error on Linux | Run `sudo apt install freeglut3` |
| `freeglut.dll not found` on Windows | Copy `freeglut.dll` to System32 (see Windows section) |
| Black screen / no window | Update your GPU drivers |
| Game window does not open on macOS | Try running from Terminal directly, not from an IDE |
| Slow performance | Close other GPU-intensive apps; ensure discrete GPU is active |

---

## Running Without the Launcher

You can also run the main file directly:

```bash
python3 src/last_stand_arena.py
```

---

## Game Controls (Quick Reference)

```
  MOVEMENT
    W / S           Move forward / backward
    A / D           Rotate left / right
    Q / E           Strafe left / right
    Shift + Move    Sprint

  COMBAT
    Space           Fire
    1 / 2 / 3       Switch weapon (Pistol / AR / Shotgun)
    R               Reload

  SYSTEM
    F               Toggle First / Third Person
    Arrow Keys      Zoom (third person)
    P               Pause
    ESC             Quit
```

---

*Last Stand Arena — Fahad Nadim Ziad, 2026 — MIT License*
