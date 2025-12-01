#!/usr/bin/env python3
"""
Launcher script for Target Frenzy 3D
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the game
from target_frenzy_3d import main

if __name__ == "__main__":
    print("Starting Target Frenzy 3D...")
    print("Controls:")
    print("  WASD - Movement")
    print("  Mouse/Space - Fire")
    print("  Right Click - Toggle First Person View")
    print("  Arrow Keys - Camera Control (Third Person)")
    print("  R - Restart")
    print("\nGood luck!\n")
    main()
