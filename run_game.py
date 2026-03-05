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
    print("  WASD         - Move")
    print("  Shift + Move - Sprint")
    print("  Space / LMB  - Shoot")
    print("  RMB / F      - Toggle First Person")
    print("  Arrow Keys   - Camera Control")
    print("  P            - Pause")
    print("  R            - Restart (when dead)")
    print()
    print("  Survive. Eliminate. Dominate.")
    print("=" * 50)
    print()
    main()
