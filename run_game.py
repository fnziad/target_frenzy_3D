#!/usr/bin/env python3
"""
Launcher script for Target Frenzy 3D - Battle Royale Edition
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from target_frenzy_3d import main

if __name__ == "__main__":
    print("=" * 50)
    print("  TARGET FRENZY 3D - BATTLE ROYALE EDITION")
    print("=" * 50)
    print()
    print("  W/S          - Move forward/backward")
    print("  A/D          - Rotate left/right")
    print("  Q/E          - Strafe left/right")
    print("  Shift + Move - Sprint")
    print("  Space        - Shoot")
    print("  1/2/3        - Switch weapon (Pistol/AR/Shotgun)")
    print("  R            - Reload")
    print("  F            - Toggle First/Third Person")
    print("  Arrow Keys   - Zoom (third person)")
    print("  P            - Pause")
    print("  ESC          - Quit game")
    print()
    print("  Survive. Eliminate. Dominate.")
    print("=" * 50)
    print()
    main()
