#!/usr/bin/env python3
"""
Last Stand Arena — Launcher
Author: Fahad Nadim Ziad, 2026
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from last_stand_arena import main

if __name__ == "__main__":
    print()
    print("  ╔══════════════════════════════════════════════════╗")
    print("  ║           LAST STAND ARENA                      ║")
    print("  ║      Battle Royale 3D Shooter  •  Python/OpenGL ║")
    print("  ║          Fahad Nadim Ziad — 2026                ║")
    print("  ╚══════════════════════════════════════════════════╝")
    print()
    print("  MOVEMENT")
    print("    W / S          Move forward / backward")
    print("    A / D          Rotate left / right")
    print("    Q / E          Strafe left / right")
    print("    Shift + Move   Sprint  (uses stamina)")
    print()
    print("  COMBAT")
    print("    Space          Fire weapon")
    print("    1 / 2 / 3      Switch weapon  (Pistol / AR / Shotgun)")
    print("    R              Reload")
    print()
    print("  SYSTEM")
    print("    F              Toggle First / Third Person")
    print("    Arrow Keys     Zoom (third person)")
    print("    P              Pause / Resume")
    print("    ESC            Quit")
    print()
    print("  Survive. Eliminate. Dominate.")
    print()
    main()
