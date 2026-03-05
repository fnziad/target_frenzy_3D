"""
Target Frenzy 3D - Battle Royale Edition
A fast-paced 3D arena shooter with battle royale mechanics

Features:
- Large battle arena with obstacles for cover
- Shrinking battle royale zone
- 4 enemy types with unique AI and shooting abilities
- Level/wave progression system
- Power-up system (Health, Speed, Damage, Shield)
- Sprint mechanic with stamina
- Combo/kill streak scoring
- Player name entry and stats tracking
- Minimap, HUD bars, and particle effects

Author: Fahad Nadim Ziad
License: MIT
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18, GLUT_BITMAP_HELVETICA_12
from OpenGL.GLUT import GLUT_BITMAP_TIMES_ROMAN_24, GLUT_BITMAP_9_BY_15

import math
import random
import time

# ============================================================
# WINDOW CONFIGURATION
# ============================================================
WIN_W = 1000
WIN_H = 800
FOV = 70

# ============================================================
# GAME STATES
# ============================================================
STATE_NAME_ENTRY = 0
STATE_GUIDELINES = 1
STATE_PLAYING = 2
STATE_PAUSED = 3
STATE_GAME_OVER = 4

game_state = STATE_NAME_ENTRY
player_name = ""

# ============================================================
# ARENA CONFIGURATION
# ============================================================
GRID = 2000
TILE_SIZE = 200
WALL_HEIGHT = 300

# ============================================================
# CAMERA
# ============================================================
cam_ang = 0
cam_dist = 800
cam_h = 600
cam_min_h = 200
cam_max_h = 1500
cam_min_dist = 300
cam_max_dist = 1500
fp_view = False

# ============================================================
# PLAYER
# ============================================================
p_pos = [0, 0, 0]
p_dir = 0
p_spd = 8
p_sprint_spd = 16
p_rot = 5
p_hp = 100
p_max_hp = 100
p_score = 0
p_mom = [0, 0, 0]
p_fric = 0.85
p_shield = 0
p_shield_max = 50
p_damage_mult = 1.0
p_speed_boost_timer = 0
p_damage_boost_timer = 0
p_shield_timer = 0

# Stamina / Sprint
p_stamina = 100
p_max_stamina = 100
p_stamina_drain = 0.8
p_stamina_regen = 0.3
p_sprinting = False

# Input
keys = {b'w': False, b's': False, b'a': False, b'd': False}
shift_held = False

# ============================================================
# WEAPON
# ============================================================
shots = []
shot_size = 8
shot_spd = 6
gun_pos = [30, 15, 80]
fire_cooldown = 0
fire_rate = 0.15

# ============================================================
# ENEMIES
# ============================================================
enemies = []
enemy_shots = []
enemy_types = {
    'grunt':  {'hp': 30,  'speed': 0.035, 'color': (0.9, 0.2, 0.1),  'size': 30, 'fire_rate': 3.0,  'points': 10,  'damage': 5,  'shot_speed': 3,   'accuracy': 8},
    'tank':   {'hp': 80,  'speed': 0.015, 'color': (0.5, 0.05, 0.05), 'size': 45, 'fire_rate': 2.0,  'points': 25,  'damage': 15, 'shot_speed': 2.5, 'accuracy': 12},
    'scout':  {'hp': 15,  'speed': 0.065, 'color': (1.0, 0.6, 0.1),  'size': 22, 'fire_rate': 1.5,  'points': 15,  'damage': 8,  'shot_speed': 4,   'accuracy': 10},
    'sniper': {'hp': 25,  'speed': 0.01,  'color': (0.2, 0.8, 0.2),  'size': 25, 'fire_rate': 4.0,  'points': 20,  'damage': 20, 'shot_speed': 6,   'accuracy': 2},
}

# ============================================================
# LEVEL / WAVE SYSTEM
# ============================================================
current_level = 1
kills_this_level = 0
kills_to_advance = 10
total_kills = 0
level_up_display = 0

# ============================================================
# BATTLE ROYALE ZONE
# ============================================================
zone_radius = 2000
zone_target_radius = 2000
zone_shrink_rate = 0.8
zone_damage = 2
zone_shrink_interval = 45
zone_next_shrink_time = 45
zone_center = [0, 0]
zone_warning = False

# ============================================================
# POWER-UPS
# ============================================================
powerups = []
powerup_types = {
    'health': {'color': (0.1, 1.0, 0.1),  'label': 'HP+'},
    'speed':  {'color': (0.1, 0.5, 1.0),  'label': 'SPD'},
    'damage': {'color': (1.0, 0.1, 0.1),  'label': 'DMG'},
    'shield': {'color': (0.9, 0.9, 0.1),  'label': 'SHD'},
}
powerup_spawn_timer = 0
powerup_spawn_interval = 10

# ============================================================
# OBSTACLES
# ============================================================
obstacles = []

# ============================================================
# COMBO / STREAK
# ============================================================
combo_count = 0
combo_timer = 0
combo_timeout = 3.0
kill_streak = 0
best_streak = 0
best_combo = 0
combo_multiplier = 1.0

# ============================================================
# STATS
# ============================================================
total_shots_fired = 0
total_shots_hit = 0
time_survived = 0

# ============================================================
# EFFECTS
# ============================================================
t_pulse = 1.0
t_pulse_t = 0
particles = []
notifications = []
damage_flash = 0
game_time = 0
last_time = 0
delta_time = 0


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def begin_2d():
    """Set up 2D overlay rendering"""
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()


def end_2d():
    """Restore 3D rendering state"""
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)


def draw_text_2d(x, y, text, font=GLUT_BITMAP_HELVETICA_18, color=(1, 1, 1)):
    """Draw text in 2D overlay (call between begin_2d/end_2d)"""
    glColor3f(*color)
    glRasterPos2f(x, y)
    for c in text:
        glutBitmapCharacter(font, ord(c))


def draw_rect(x, y, w, h, color):
    """Draw filled rectangle in 2D overlay"""
    if len(color) == 4:
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(*color)
    else:
        glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x, y + h)
    glEnd()
    if len(color) == 4:
        glDisable(GL_BLEND)


def draw_bar(x, y, w, h, current, maximum, bg_color, fill_color, border=True):
    """Draw a status bar with background, fill, and optional border"""
    draw_rect(x, y, w, h, bg_color)
    fill_w = w * (max(current, 0) / maximum) if maximum > 0 else 0
    draw_rect(x, y, fill_w, h, fill_color)
    if border:
        glColor3f(0.8, 0.8, 0.8)
        glBegin(GL_LINE_LOOP)
        glVertex2f(x, y)
        glVertex2f(x + w, y)
        glVertex2f(x + w, y + h)
        glVertex2f(x, y + h)
        glEnd()


def add_notification(text, color=(1, 1, 1), duration=3.0):
    """Add a floating notification message"""
    notifications.append({'text': text, 'timer': duration, 'color': color})


def spawn_particles(pos, color, count=10):
    """Spawn particle effects at a position"""
    for _ in range(count):
        particles.append({
            'pos': [pos[0], pos[1], pos[2] + 30],
            'vel': [random.uniform(-3, 3), random.uniform(-3, 3), random.uniform(1, 5)],
            'color': color,
            'life': 1.0,
            'size': random.uniform(3, 8)
        })


def take_damage(amount):
    """Apply damage to player (absorbed by shield first)"""
    global p_hp, p_shield, damage_flash, game_state
    if p_shield > 0:
        absorbed = min(p_shield, amount)
        p_shield -= absorbed
        amount -= absorbed
    p_hp -= amount
    if amount > 0:
        damage_flash = 1.0
    if p_hp <= 0:
        p_hp = 0
        game_state = STATE_GAME_OVER
        add_notification("YOU DIED!", color=(1, 0, 0), duration=5.0)


def check_obstacle_collision(pos, radius=20):
    """Check if a position collides with any obstacle"""
    for obs in obstacles:
        if obs['type'] == 'crate':
            half = obs['size'] / 2
            if (abs(pos[0] - obs['pos'][0]) < half + radius and
                abs(pos[1] - obs['pos'][1]) < half + radius):
                return True
        elif obs['type'] == 'pillar':
            dx = pos[0] - obs['pos'][0]
            dy = pos[1] - obs['pos'][1]
            if dx * dx + dy * dy < (obs['size'] / 2 + radius) ** 2:
                return True
    return False


# ============================================================
# HUD DRAWING
# ============================================================

def draw_hud():
    """Draw complete heads-up display"""
    begin_2d()

    # Health bar
    draw_text_2d(10, WIN_H - 25, "HP", GLUT_BITMAP_HELVETICA_12, (1, 1, 1))
    hp_color = (0.1, 0.9, 0.1) if p_hp > 50 else (1, 1, 0) if p_hp > 25 else (1, 0.1, 0.1)
    draw_bar(30, WIN_H - 30, 200, 18, p_hp, p_max_hp, (0.2, 0, 0), hp_color)
    draw_text_2d(95, WIN_H - 26, f"{int(p_hp)}/{p_max_hp}", GLUT_BITMAP_HELVETICA_12, (1, 1, 1))

    # Shield bar
    if p_shield > 0 or p_shield_timer > 0:
        draw_text_2d(10, WIN_H - 50, "SH", GLUT_BITMAP_HELVETICA_12, (1, 1, 0.5))
        draw_bar(30, WIN_H - 55, 200, 14, p_shield, p_shield_max, (0.15, 0.15, 0), (0.8, 0.8, 0.1))

    # Stamina bar
    draw_text_2d(10, WIN_H - 72, "ST", GLUT_BITMAP_HELVETICA_12, (0.5, 0.8, 1))
    stam_color = (0.1, 0.5, 1.0) if p_stamina > 30 else (0.8, 0.3, 0.1)
    draw_bar(30, WIN_H - 77, 200, 14, p_stamina, p_max_stamina, (0, 0, 0.15), stam_color)

    # Score and combo (top right)
    score_text = f"Score: {p_score}"
    draw_text_2d(WIN_W - 200, WIN_H - 25, score_text, GLUT_BITMAP_HELVETICA_18, (1, 1, 1))
    if combo_count > 1:
        combo_pulse = 0.7 + 0.3 * math.sin(game_time * 6)
        draw_text_2d(WIN_W - 200, WIN_H - 50, f"x{combo_multiplier:.0f} COMBO! ({combo_count})",
                     GLUT_BITMAP_HELVETICA_18, (1, combo_pulse, 0))

    # Level and kills (top center)
    level_text = f"Level {current_level}"
    draw_text_2d(WIN_W // 2 - 40, WIN_H - 25, level_text, GLUT_BITMAP_HELVETICA_18, (1, 1, 0.5))
    kills_text = f"Kills: {kills_this_level}/{kills_to_advance}"
    draw_text_2d(WIN_W // 2 - 50, WIN_H - 48, kills_text, GLUT_BITMAP_HELVETICA_12, (0.8, 0.8, 0.8))

    # Player name
    draw_text_2d(10, WIN_H - 95, player_name, GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 1.0))

    # Active power-up indicators
    pu_y = WIN_H - 115
    if p_speed_boost_timer > 0:
        draw_text_2d(10, pu_y, f"SPD BOOST {p_speed_boost_timer:.1f}s", GLUT_BITMAP_HELVETICA_12, (0.1, 0.5, 1))
        pu_y -= 18
    if p_damage_boost_timer > 0:
        draw_text_2d(10, pu_y, f"DMG BOOST {p_damage_boost_timer:.1f}s", GLUT_BITMAP_HELVETICA_12, (1, 0.2, 0.2))
        pu_y -= 18
    if p_shield_timer > 0:
        draw_text_2d(10, pu_y, f"SHIELD {p_shield_timer:.1f}s", GLUT_BITMAP_HELVETICA_12, (0.9, 0.9, 0.1))

    # Kill streak
    if kill_streak >= 3:
        streak_color = (1, 0.5, 0) if kill_streak < 5 else (1, 0, 0) if kill_streak < 10 else (1, 0, 1)
        if kill_streak >= 10:
            streak_label = "UNSTOPPABLE!"
        elif kill_streak >= 7:
            streak_label = "DOMINATING!"
        elif kill_streak >= 5:
            streak_label = "RAMPAGE!"
        else:
            streak_label = "KILLING SPREE!"
        draw_text_2d(WIN_W // 2 - 70, WIN_H - 80, f"{streak_label} ({kill_streak})",
                     GLUT_BITMAP_HELVETICA_18, streak_color)

    # Zone warning
    if zone_warning:
        if int(game_time * 4) % 2 == 0:
            draw_text_2d(WIN_W // 2 - 90, WIN_H // 2 + 100, "!! ZONE SHRINKING !!",
                         GLUT_BITMAP_TIMES_ROMAN_24, (1, 0.2, 0.2))

    # View mode
    view_text = "[FP] Right-click to switch" if fp_view else "[3P] Right-click for FP | Arrows: camera"
    draw_text_2d(10, 15, view_text, GLUT_BITMAP_HELVETICA_12, (0.6, 0.6, 0.6))

    # Sprint hint
    if p_sprinting:
        draw_text_2d(10, 35, "SPRINTING", GLUT_BITMAP_HELVETICA_12, (0.3, 0.7, 1))

    # Level up display
    if level_up_display > 0:
        pulse = 0.5 + 0.5 * math.sin(game_time * 4)
        draw_text_2d(WIN_W // 2 - 80, WIN_H // 2 + 40, f"LEVEL {current_level}!",
                     GLUT_BITMAP_TIMES_ROMAN_24, (1, 1, pulse))
        draw_text_2d(WIN_W // 2 - 60, WIN_H // 2 + 10, "+20 HP Restored",
                     GLUT_BITMAP_HELVETICA_18, (0, 1, 0))

    # Notifications (right side)
    ny = WIN_H // 2
    for n in notifications:
        alpha = min(n['timer'], 1.0)
        draw_text_2d(WIN_W - 350, ny, n['text'], GLUT_BITMAP_HELVETICA_18, n['color'])
        ny -= 25

    # Crosshair (first person)
    if fp_view:
        cx, cy = WIN_W // 2, WIN_H // 2
        glColor3f(1, 1, 1)
        glBegin(GL_LINES)
        glVertex2f(cx - 15, cy)
        glVertex2f(cx - 5, cy)
        glVertex2f(cx + 5, cy)
        glVertex2f(cx + 15, cy)
        glVertex2f(cx, cy - 15)
        glVertex2f(cx, cy - 5)
        glVertex2f(cx, cy + 5)
        glVertex2f(cx, cy + 15)
        glEnd()

    # Minimap
    draw_minimap()

    # Damage flash overlay
    if damage_flash > 0:
        draw_rect(0, 0, WIN_W, WIN_H, (1, 0, 0, min(damage_flash * 0.3, 0.4)))

    end_2d()


def draw_minimap():
    """Draw minimap in bottom-right corner"""
    map_size = 160
    map_x = WIN_W - map_size - 15
    map_y = 15
    scale = map_size / (GRID * 2)

    # Background
    draw_rect(map_x, map_y, map_size, map_size, (0, 0, 0, 0.6))

    # Zone circle
    glColor3f(1, 0.3, 0.3)
    cx = map_x + map_size / 2 + zone_center[0] * scale
    cy = map_y + map_size / 2 + zone_center[1] * scale
    r = zone_radius * scale
    glBegin(GL_LINE_LOOP)
    for i in range(36):
        angle = 2 * math.pi * i / 36
        glVertex2f(cx + r * math.cos(angle), cy + r * math.sin(angle))
    glEnd()

    # Target zone
    if zone_target_radius < zone_radius:
        glColor3f(1, 1, 1)
        tr = zone_target_radius * scale
        glBegin(GL_LINE_LOOP)
        for i in range(36):
            angle = 2 * math.pi * i / 36
            glVertex2f(cx + tr * math.cos(angle), cy + tr * math.sin(angle))
        glEnd()

    # Obstacles
    glColor3f(0.5, 0.4, 0.3)
    for obs in obstacles:
        ox = map_x + map_size / 2 + obs['pos'][0] * scale
        oy = map_y + map_size / 2 + obs['pos'][1] * scale
        os = max(obs['size'] * scale * 0.5, 2)
        draw_rect(ox - os / 2, oy - os / 2, os, os, (0.5, 0.4, 0.3))

    # Power-ups
    glPointSize(4)
    for pu in powerups:
        if pu['active']:
            glColor3f(*powerup_types[pu['type']]['color'])
            glBegin(GL_POINTS)
            px = map_x + map_size / 2 + pu['pos'][0] * scale
            py = map_y + map_size / 2 + pu['pos'][1] * scale
            glVertex2f(px, py)
            glEnd()

    # Enemies
    glPointSize(3)
    glColor3f(1, 0.2, 0.2)
    glBegin(GL_POINTS)
    for e in enemies:
        if e['alive']:
            ex = map_x + map_size / 2 + e['pos'][0] * scale
            ey = map_y + map_size / 2 + e['pos'][1] * scale
            glVertex2f(ex, ey)
    glEnd()

    # Player (green dot with direction)
    px = map_x + map_size / 2 + p_pos[0] * scale
    py = map_y + map_size / 2 + p_pos[1] * scale
    glColor3f(0, 1, 0)
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(px, py)
    glEnd()
    dir_len = 12
    dir_ang = math.radians(p_dir - 90)
    glBegin(GL_LINES)
    glVertex2f(px, py)
    glVertex2f(px + dir_len * math.cos(dir_ang), py + dir_len * math.sin(dir_ang))
    glEnd()

    glPointSize(1)

    # Border
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINE_LOOP)
    glVertex2f(map_x, map_y)
    glVertex2f(map_x + map_size, map_y)
    glVertex2f(map_x + map_size, map_y + map_size)
    glVertex2f(map_x, map_y + map_size)
    glEnd()


# ============================================================
# GAME SCREENS
# ============================================================

def draw_name_entry():
    """Draw the name entry screen"""
    begin_2d()
    draw_rect(0, 0, WIN_W, WIN_H, (0.05, 0.05, 0.15))

    draw_text_2d(WIN_W // 2 - 160, WIN_H // 2 + 180, "TARGET FRENZY 3D",
                 GLUT_BITMAP_TIMES_ROMAN_24, (1, 0.8, 0.2))
    draw_text_2d(WIN_W // 2 - 120, WIN_H // 2 + 150, "- BATTLE ROYALE EDITION -",
                 GLUT_BITMAP_HELVETICA_18, (0.8, 0.6, 0.2))

    draw_text_2d(WIN_W // 2 - 100, WIN_H // 2 + 50, "ENTER YOUR NAME:",
                 GLUT_BITMAP_HELVETICA_18, (0.8, 0.8, 0.8))

    # Name box
    box_w = 300
    box_x = WIN_W // 2 - box_w // 2
    box_y = WIN_H // 2 - 5
    draw_rect(box_x, box_y, box_w, 35, (0.15, 0.15, 0.25))
    glColor3f(0.5, 0.5, 0.8)
    glBegin(GL_LINE_LOOP)
    glVertex2f(box_x, box_y)
    glVertex2f(box_x + box_w, box_y)
    glVertex2f(box_x + box_w, box_y + 35)
    glVertex2f(box_x, box_y + 35)
    glEnd()

    # Name text with blinking cursor
    cursor = "_" if int(game_time * 2) % 2 == 0 else " "
    draw_text_2d(box_x + 10, box_y + 10, player_name + cursor,
                 GLUT_BITMAP_HELVETICA_18, (1, 1, 1))

    draw_text_2d(WIN_W // 2 - 100, WIN_H // 2 - 50, "Press ENTER to continue",
                 GLUT_BITMAP_HELVETICA_12, (0.5, 0.5, 0.5))

    end_2d()


def draw_guidelines():
    """Draw the controls/guidelines screen"""
    begin_2d()
    draw_rect(0, 0, WIN_W, WIN_H, (0.05, 0.05, 0.12))

    cx = WIN_W // 2
    y = WIN_H - 60

    draw_text_2d(cx - 120, y, "TARGET FRENZY 3D", GLUT_BITMAP_TIMES_ROMAN_24, (1, 0.8, 0.2))
    y -= 50

    draw_text_2d(cx - 80, y, "=== CONTROLS ===", GLUT_BITMAP_HELVETICA_18, (0.5, 0.8, 1))
    y -= 30
    controls = [
        ("W / A / S / D", "Move / Strafe"),
        ("Shift + Move", "Sprint (uses stamina)"),
        ("Left Click / Space", "Fire weapon"),
        ("Right Click / F", "Toggle first-person view"),
        ("Arrow Keys", "Camera control (third person)"),
        ("P", "Pause game"),
        ("R", "Restart (when dead)"),
    ]
    for key, desc in controls:
        draw_text_2d(cx - 200, y, key, GLUT_BITMAP_HELVETICA_12, (1, 1, 0.5))
        draw_text_2d(cx + 20, y, desc, GLUT_BITMAP_HELVETICA_12, (0.8, 0.8, 0.8))
        y -= 22

    y -= 15
    draw_text_2d(cx - 80, y, "=== GAMEPLAY ===", GLUT_BITMAP_HELVETICA_18, (0.5, 1, 0.5))
    y -= 28
    tips = [
        "- Eliminate enemies to score points and level up",
        "- The ZONE shrinks over time - stay inside or take damage!",
        "- Enemies shoot back - use obstacles for cover!",
        "- Quick kills build COMBOS for score multipliers (up to 5x)",
        "- Kill streaks earn bonus points",
        "- Collect power-ups scattered across the arena",
    ]
    for tip in tips:
        draw_text_2d(cx - 220, y, tip, GLUT_BITMAP_HELVETICA_12, (0.7, 0.7, 0.7))
        y -= 20

    y -= 15
    draw_text_2d(cx - 80, y, "=== POWER-UPS ===", GLUT_BITMAP_HELVETICA_18, (1, 0.5, 1))
    y -= 28
    pups = [
        ((0.1, 1, 0.1), "Health Pack - Restores 30 HP"),
        ((0.1, 0.5, 1), "Speed Boost - 10s faster movement"),
        ((1, 0.1, 0.1), "Damage Boost - 10s double damage"),
        ((0.9, 0.9, 0.1), "Shield - 15s damage absorption"),
    ]
    for color, desc in pups:
        draw_rect(cx - 220, y - 2, 12, 12, color)
        draw_text_2d(cx - 200, y, desc, GLUT_BITMAP_HELVETICA_12, (0.8, 0.8, 0.8))
        y -= 20

    y -= 15
    draw_text_2d(cx - 80, y, "=== ENEMIES ===", GLUT_BITMAP_HELVETICA_18, (1, 0.5, 0.5))
    y -= 28
    enemy_info = [
        ((0.9, 0.2, 0.1), "Grunt - Standard chaser, moderate threat"),
        ((0.5, 0.05, 0.05), "Tank - Slow but tough, heavy damage"),
        ((1, 0.6, 0.1), "Scout - Fast and agile, zigzag movement"),
        ((0.2, 0.8, 0.2), "Sniper - Keeps distance, accurate shots"),
    ]
    for color, desc in enemy_info:
        draw_rect(cx - 220, y - 2, 12, 12, color)
        draw_text_2d(cx - 200, y, desc, GLUT_BITMAP_HELVETICA_12, (0.8, 0.8, 0.8))
        y -= 20

    y -= 20
    pulse = 0.5 + 0.5 * math.sin(game_time * 3)
    draw_text_2d(cx - 110, y, "Press ENTER to start!", GLUT_BITMAP_HELVETICA_18, (pulse, 1, pulse))

    end_2d()


def draw_game_over():
    """Draw game over screen with stats"""
    begin_2d()
    draw_rect(0, 0, WIN_W, WIN_H, (0.05, 0, 0, 0.7))

    cx = WIN_W // 2
    y = WIN_H // 2 + 160

    draw_text_2d(cx - 80, y, "GAME OVER", GLUT_BITMAP_TIMES_ROMAN_24, (1, 0.2, 0.2))
    y -= 50

    draw_text_2d(cx - 100, y, f"Player: {player_name}", GLUT_BITMAP_HELVETICA_18, (0.8, 0.8, 1))
    y -= 35

    stats = [
        (f"Final Score: {p_score}", (1, 1, 0.5)),
        (f"Level Reached: {current_level}", (0.5, 1, 0.5)),
        (f"Total Kills: {total_kills}", (1, 0.5, 0.5)),
        (f"Best Streak: {best_streak}", (1, 0.7, 0.3)),
        (f"Best Combo: x{best_combo}", (1, 0.5, 1)),
        (f"Time Survived: {int(time_survived)}s", (0.5, 0.8, 1)),
    ]

    accuracy = (total_shots_hit / total_shots_fired * 100) if total_shots_fired > 0 else 0
    stats.append((f"Accuracy: {accuracy:.1f}%", (0.8, 0.8, 0.8)))

    for text, color in stats:
        draw_text_2d(cx - 100, y, text, GLUT_BITMAP_HELVETICA_18, color)
        y -= 30

    y -= 20
    pulse = 0.5 + 0.5 * math.sin(game_time * 2)
    draw_text_2d(cx - 100, y, "Press R to restart", GLUT_BITMAP_HELVETICA_18, (pulse, pulse, pulse))

    end_2d()


def draw_pause():
    """Draw pause screen overlay"""
    begin_2d()
    draw_rect(0, 0, WIN_W, WIN_H, (0, 0, 0, 0.5))
    draw_text_2d(WIN_W // 2 - 60, WIN_H // 2 + 20, "PAUSED",
                 GLUT_BITMAP_TIMES_ROMAN_24, (1, 1, 1))
    draw_text_2d(WIN_W // 2 - 80, WIN_H // 2 - 20, "Press P to resume",
                 GLUT_BITMAP_HELVETICA_18, (0.7, 0.7, 0.7))
    end_2d()


# ============================================================
# 3D DRAWING FUNCTIONS
# ============================================================

def draw_arena():
    """Render the large battle arena floor"""
    glBegin(GL_QUADS)
    for i in range(-GRID, GRID, TILE_SIZE):
        for j in range(-GRID, GRID, TILE_SIZE):
            cx = i + TILE_SIZE / 2
            cy = j + TILE_SIZE / 2
            dist = math.sqrt(cx * cx + cy * cy) / GRID

            if (i // TILE_SIZE + j // TILE_SIZE) % 2 == 0:
                r, g, b = 0.35 - dist * 0.08, 0.35 - dist * 0.08, 0.42 - dist * 0.08
            else:
                r, g, b = 0.25 - dist * 0.06, 0.25 - dist * 0.06, 0.32 - dist * 0.06

            glColor3f(max(r, 0.08), max(g, 0.08), max(b, 0.1))
            glNormal3f(0, 0, 1)
            glVertex3f(i, j, 0)
            glVertex3f(i + TILE_SIZE, j, 0)
            glVertex3f(i + TILE_SIZE, j + TILE_SIZE, 0)
            glVertex3f(i, j + TILE_SIZE, 0)
    glEnd()


def draw_walls():
    """Draw arena boundary walls"""
    glBegin(GL_QUADS)
    # North wall
    glColor3f(0.15, 0.2, 0.15)
    glNormal3f(0, -1, 0)
    glVertex3f(-GRID, GRID, 0)
    glVertex3f(GRID, GRID, 0)
    glVertex3f(GRID, GRID, WALL_HEIGHT)
    glVertex3f(-GRID, GRID, WALL_HEIGHT)
    # South wall
    glNormal3f(0, 1, 0)
    glVertex3f(-GRID, -GRID, 0)
    glVertex3f(GRID, -GRID, 0)
    glVertex3f(GRID, -GRID, WALL_HEIGHT)
    glVertex3f(-GRID, -GRID, WALL_HEIGHT)
    # East wall
    glColor3f(0.15, 0.15, 0.2)
    glNormal3f(-1, 0, 0)
    glVertex3f(GRID, -GRID, 0)
    glVertex3f(GRID, GRID, 0)
    glVertex3f(GRID, GRID, WALL_HEIGHT)
    glVertex3f(GRID, -GRID, WALL_HEIGHT)
    # West wall
    glNormal3f(1, 0, 0)
    glVertex3f(-GRID, -GRID, 0)
    glVertex3f(-GRID, GRID, 0)
    glVertex3f(-GRID, GRID, WALL_HEIGHT)
    glVertex3f(-GRID, -GRID, WALL_HEIGHT)
    glEnd()


def draw_obstacles():
    """Draw all obstacles in the arena"""
    for obs in obstacles:
        glPushMatrix()
        if obs['type'] == 'crate':
            glTranslatef(obs['pos'][0], obs['pos'][1], obs['size'] / 2)
            glColor3f(*obs['color'])
            glutSolidCube(obs['size'])
        elif obs['type'] == 'pillar':
            glTranslatef(obs['pos'][0], obs['pos'][1], 0)
            glColor3f(*obs['color'])
            gluCylinder(gluNewQuadric(), obs['size'] / 2, obs['size'] / 2 * 0.8,
                        obs['height'], 12, 1)
            # Cap on top
            glTranslatef(0, 0, obs['height'])
            gluDisk(gluNewQuadric(), 0, obs['size'] / 2 * 0.8, 12, 1)
        glPopMatrix()


def draw_zone():
    """Draw the battle royale zone boundary"""
    glDisable(GL_LIGHTING)
    segments = 72

    # Zone circle on ground
    glLineWidth(3.0)
    pulse = 0.5 + 0.5 * math.sin(game_time * 2)
    glColor3f(1.0, pulse * 0.3, pulse * 0.3)
    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        x = zone_center[0] + zone_radius * math.cos(angle)
        y = zone_center[1] + zone_radius * math.sin(angle)
        glVertex3f(x, y, 2)
    glEnd()

    # Translucent zone wall
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1, 0.1, 0.1, 0.08 + 0.04 * pulse)
    wall_h = 200
    glBegin(GL_QUAD_STRIP)
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        x = zone_center[0] + zone_radius * math.cos(angle)
        y = zone_center[1] + zone_radius * math.sin(angle)
        glVertex3f(x, y, 0)
        glVertex3f(x, y, wall_h)
    glEnd()

    # Target zone (white, if shrinking)
    if zone_target_radius < zone_radius - 5:
        glColor3f(1, 1, 1)
        glLineWidth(1.5)
        glBegin(GL_LINE_LOOP)
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = zone_center[0] + zone_target_radius * math.cos(angle)
            y = zone_center[1] + zone_target_radius * math.sin(angle)
            glVertex3f(x, y, 2)
        glEnd()

    glDisable(GL_BLEND)
    glLineWidth(1.0)
    glEnable(GL_LIGHTING)


def draw_player():
    """Render the player character model"""
    glPushMatrix()
    glTranslatef(*p_pos)
    glRotatef(p_dir, 0, 0, 1)

    if game_state == STATE_GAME_OVER:
        glRotatef(-90, 1, 0, 0)

    # Legs
    glColor3f(0.1, 0.1, 0.5)
    glPushMatrix()
    glTranslatef(-8, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 10, 45, 10, 1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(8, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 10, 45, 10, 1)
    glPopMatrix()

    # Body
    glPushMatrix()
    glTranslatef(0, 0, 70)
    glColor3f(0.2, 0.35, 0.2)
    glutSolidCube(38)
    glPopMatrix()

    # Head
    glPushMatrix()
    glTranslatef(0, 0, 108)
    glColor3f(0.85, 0.7, 0.55)
    gluSphere(gluNewQuadric(), 18, 12, 12)
    # Eyes
    glTranslatef(6, -15, 3)
    glColor3f(0.1, 0.1, 0.1)
    gluSphere(gluNewQuadric(), 3, 6, 6)
    glTranslatef(-12, 0, 0)
    gluSphere(gluNewQuadric(), 3, 6, 6)
    glPopMatrix()

    # Arms
    glColor3f(0.85, 0.7, 0.55)
    glPushMatrix()
    glTranslatef(22, -20, 55)
    glRotatef(-70, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 4, 6, 45, 8, 1)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-22, -20, 55)
    glRotatef(-70, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 4, 6, 45, 8, 1)
    glPopMatrix()

    # Gun
    glPushMatrix()
    glTranslatef(0, -45, 60)
    glRotatef(-80, 1, 0, 0)
    glColor3f(0.3, 0.3, 0.35)
    gluCylinder(gluNewQuadric(), 3, 5, 70, 8, 1)
    # Muzzle
    glTranslatef(0, 0, 70)
    glColor3f(0.6, 0.4, 0.1)
    gluCylinder(gluNewQuadric(), 5, 3, 15, 8, 1)
    glPopMatrix()

    # Shield effect
    if p_shield > 0:
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        shield_pulse = 0.15 + 0.05 * math.sin(game_time * 4)
        glColor4f(0.3, 0.3, 1.0, shield_pulse)
        glTranslatef(0, 0, 55)
        gluSphere(gluNewQuadric(), 55, 16, 16)
        glDisable(GL_BLEND)

    glPopMatrix()


def draw_enemy(enemy):
    """Render an enemy based on its type"""
    if not enemy['alive']:
        return
    et = enemy_types[enemy['type']]
    pos = enemy['pos']

    glPushMatrix()
    glTranslatef(pos[0], pos[1], 0)

    # Scale pulsing
    glScalef(t_pulse * 0.95 + 0.05, t_pulse * 0.95 + 0.05, 1)

    if enemy['type'] == 'tank':
        # Tank: large dark body, armored look
        glColor3f(*et['color'])
        glTranslatef(0, 0, et['size'])
        glutSolidCube(et['size'] * 1.5)
        glTranslatef(0, 0, et['size'] * 0.9)
        glColor3f(et['color'][0] * 0.7, et['color'][1] * 0.7, et['color'][2] * 0.7)
        gluSphere(gluNewQuadric(), et['size'] * 0.6, 12, 12)
    elif enemy['type'] == 'scout':
        # Scout: small, sleek
        glTranslatef(0, 0, et['size'])
        glColor3f(*et['color'])
        gluSphere(gluNewQuadric(), et['size'], 10, 10)
        glTranslatef(0, 0, et['size'] * 1.2)
        glColor3f(0.1, 0.1, 0.1)
        gluSphere(gluNewQuadric(), et['size'] * 0.5, 8, 8)
    elif enemy['type'] == 'sniper':
        # Sniper: tall, thin
        glColor3f(*et['color'])
        gluCylinder(gluNewQuadric(), et['size'] * 0.4, et['size'] * 0.6, et['size'] * 2.5, 8, 1)
        glTranslatef(0, 0, et['size'] * 2.5)
        gluSphere(gluNewQuadric(), et['size'] * 0.6, 10, 10)
        # Sniper scope/gun
        glPushMatrix()
        glTranslatef(0, -et['size'], -et['size'] * 0.3)
        glRotatef(-80, 1, 0, 0)
        glColor3f(0.15, 0.15, 0.15)
        gluCylinder(gluNewQuadric(), 2, 2, et['size'] * 2, 6, 1)
        glPopMatrix()
    else:
        # Grunt: standard sphere body
        glTranslatef(0, 0, et['size'] + 5)
        glColor3f(*et['color'])
        gluSphere(gluNewQuadric(), et['size'], 14, 14)
        glTranslatef(0, 0, et['size'] * 1.3)
        glColor3f(0.05, 0.05, 0.05)
        gluSphere(gluNewQuadric(), et['size'] * 0.45, 10, 10)

    glPopMatrix()

    # Health bar above enemy (only if damaged)
    if enemy['hp'] < enemy['max_hp']:
        draw_enemy_health_bar(enemy)


def draw_enemy_health_bar(enemy):
    """Draw a health bar floating above an enemy"""
    et = enemy_types[enemy['type']]
    pos = enemy['pos']
    bar_z = et['size'] * 3 + 20
    bar_w = 40
    bar_h = 5
    hp_ratio = enemy['hp'] / enemy['max_hp']

    glDisable(GL_LIGHTING)
    # Background
    glColor3f(0.3, 0, 0)
    glBegin(GL_QUADS)
    glVertex3f(pos[0] - bar_w / 2, pos[1], bar_z)
    glVertex3f(pos[0] + bar_w / 2, pos[1], bar_z)
    glVertex3f(pos[0] + bar_w / 2, pos[1], bar_z + bar_h)
    glVertex3f(pos[0] - bar_w / 2, pos[1], bar_z + bar_h)
    glEnd()
    # Fill
    fill_w = bar_w * hp_ratio
    if hp_ratio > 0.5:
        glColor3f(0, 1, 0)
    elif hp_ratio > 0.25:
        glColor3f(1, 1, 0)
    else:
        glColor3f(1, 0, 0)
    glBegin(GL_QUADS)
    glVertex3f(pos[0] - bar_w / 2, pos[1], bar_z)
    glVertex3f(pos[0] - bar_w / 2 + fill_w, pos[1], bar_z)
    glVertex3f(pos[0] - bar_w / 2 + fill_w, pos[1], bar_z + bar_h)
    glVertex3f(pos[0] - bar_w / 2, pos[1], bar_z + bar_h)
    glEnd()
    glEnable(GL_LIGHTING)


def draw_powerup_3d(pu):
    """Draw a rotating, bobbing power-up"""
    if not pu['active']:
        return
    ptype = powerup_types[pu['type']]
    bob = 25 + 12 * math.sin(game_time * 2 + pu['pos'][0] * 0.1)

    glPushMatrix()
    glTranslatef(pu['pos'][0], pu['pos'][1], bob)
    glRotatef(game_time * 90, 0, 0, 1)
    glRotatef(game_time * 45, 1, 0, 0)
    glColor3f(*ptype['color'])
    glutSolidCube(22)
    glPopMatrix()


def draw_player_shot(shot):
    """Draw a player projectile"""
    glPushMatrix()
    glTranslatef(shot[0], shot[1], shot[2])
    glColor3f(1, 0.6, 0)
    glutSolidCube(shot_size)
    glPopMatrix()


def draw_enemy_shot(shot):
    """Draw an enemy projectile"""
    glPushMatrix()
    glTranslatef(*shot['pos'])
    glColor3f(1, 0.1, 0.1)
    gluSphere(gluNewQuadric(), 5, 6, 6)
    glPopMatrix()


def draw_particles_3d():
    """Draw all active particles"""
    if not particles:
        return
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    for p in particles:
        glPushMatrix()
        glTranslatef(*p['pos'])
        glColor4f(*p['color'], max(p['life'], 0))
        glutSolidCube(p['size'])
        glPopMatrix()
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)


def draw_scene():
    """Render the complete 3D scene"""
    draw_arena()
    draw_walls()
    draw_obstacles()
    draw_zone()
    draw_player()

    for e in enemies:
        draw_enemy(e)

    for pu in powerups:
        draw_powerup_3d(pu)

    for s in shots:
        draw_player_shot(s)

    for s in enemy_shots:
        draw_enemy_shot(s)

    draw_particles_3d()


# ============================================================
# GAME LOGIC
# ============================================================

def generate_obstacles():
    """Generate random obstacles across the arena"""
    global obstacles
    obstacles = []
    # Crate clusters
    for _ in range(20):
        cx = random.uniform(-GRID + 400, GRID - 400)
        cy = random.uniform(-GRID + 400, GRID - 400)
        if abs(cx) < 300 and abs(cy) < 300:
            continue
        for _ in range(random.randint(1, 3)):
            ox = cx + random.uniform(-80, 80)
            oy = cy + random.uniform(-80, 80)
            size = random.uniform(40, 70)
            shade = random.uniform(0.4, 0.65)
            obstacles.append({
                'pos': [ox, oy, 0],
                'size': size,
                'color': (shade, shade * 0.7, shade * 0.4),
                'type': 'crate'
            })
    # Pillars
    for _ in range(10):
        px = random.uniform(-GRID + 300, GRID - 300)
        py = random.uniform(-GRID + 300, GRID - 300)
        if abs(px) < 350 and abs(py) < 350:
            continue
        obstacles.append({
            'pos': [px, py, 0],
            'size': random.uniform(30, 50),
            'height': random.uniform(100, 200),
            'color': (0.35, 0.35, 0.45),
            'type': 'pillar'
        })


def spawn_enemies_for_level():
    """Spawn enemies based on current level"""
    count = 5 + current_level * 2
    for _ in range(count):
        roll = random.random()
        if current_level < 3:
            etype = 'grunt'
        elif current_level < 5:
            if roll < 0.55:
                etype = 'grunt'
            elif roll < 0.85:
                etype = 'scout'
            else:
                etype = 'tank'
        elif current_level < 8:
            if roll < 0.35:
                etype = 'grunt'
            elif roll < 0.6:
                etype = 'scout'
            elif roll < 0.85:
                etype = 'tank'
            else:
                etype = 'sniper'
        else:
            if roll < 0.25:
                etype = 'grunt'
            elif roll < 0.5:
                etype = 'scout'
            elif roll < 0.75:
                etype = 'tank'
            else:
                etype = 'sniper'
        spawn_enemy(etype)


def spawn_enemy(etype, pos=None):
    """Spawn a single enemy of given type"""
    et = enemy_types[etype]
    if pos is None:
        attempts = 0
        while attempts < 50:
            x = random.uniform(-zone_radius * 0.85 + zone_center[0],
                               zone_radius * 0.85 + zone_center[0])
            y = random.uniform(-zone_radius * 0.85 + zone_center[1],
                               zone_radius * 0.85 + zone_center[1])
            dx = x - p_pos[0]
            dy = y - p_pos[1]
            if dx * dx + dy * dy > 400 * 400:
                break
            attempts += 1
        pos = [x, y, 0]

    hp_scale = 1.0 + (current_level - 1) * 0.12
    enemies.append({
        'pos': list(pos),
        'hp': int(et['hp'] * hp_scale),
        'max_hp': int(et['hp'] * hp_scale),
        'type': etype,
        'dir': random.uniform(0, 360),
        'fire_cd': random.uniform(1, et['fire_rate']),
        'alive': True,
        'dodge_timer': random.uniform(0, 2),
        'dodge_dir': random.choice([-1, 1]),
    })


def spawn_powerup():
    """Spawn a random power-up in the arena"""
    ptype = random.choice(list(powerup_types.keys()))
    attempts = 0
    while attempts < 30:
        x = random.uniform(-zone_radius * 0.8 + zone_center[0],
                           zone_radius * 0.8 + zone_center[0])
        y = random.uniform(-zone_radius * 0.8 + zone_center[1],
                           zone_radius * 0.8 + zone_center[1])
        if not check_obstacle_collision([x, y], radius=30):
            break
        attempts += 1
    powerups.append({
        'pos': [x, y, 0],
        'type': ptype,
        'active': True,
    })


def fire_weapon():
    """Fire a projectile from the player's weapon"""
    global fire_cooldown, total_shots_fired
    if fire_cooldown > 0:
        return
    fire_cooldown = fire_rate
    total_shots_fired += 1

    if fp_view:
        ang = math.radians(p_dir + 45)
        x = p_pos[0] + (gun_pos[0] + 5) * math.sin(ang) - gun_pos[1] * math.cos(ang)
        y = p_pos[1] - (gun_pos[0] + 5) * math.cos(ang) - gun_pos[1] * math.sin(ang)
        z = p_pos[2] + gun_pos[2]
        spread = 0.6
    else:
        ang = math.radians(p_dir - 90)
        off_x = gun_pos[0] * math.cos(ang) - gun_pos[1] * math.sin(ang)
        off_y = gun_pos[0] * math.sin(ang) + gun_pos[1] * math.cos(ang)
        x = p_pos[0] + off_x
        y = p_pos[1] + off_y
        z = p_pos[2] + gun_pos[2]
        spread = 0.3

    direction = p_dir + random.uniform(-spread, spread)
    shots.append([x, y, z, direction, p_damage_mult])


def enemy_fire(enemy):
    """Make an enemy fire at the player"""
    et = enemy_types[enemy['type']]
    dx = p_pos[0] - enemy['pos'][0]
    dy = p_pos[1] - enemy['pos'][1]
    angle = math.degrees(math.atan2(dy, dx))
    angle += random.uniform(-et['accuracy'], et['accuracy'])

    enemy_shots.append({
        'pos': [enemy['pos'][0], enemy['pos'][1], et['size'] + 10],
        'dir': angle,
        'speed': et['shot_speed'],
        'damage': et['damage'],
        'life': 250,
    })


def update_player():
    """Update player movement, sprint, stamina, and power-up timers"""
    global p_pos, p_dir, p_mom, p_sprinting, p_stamina
    global p_speed_boost_timer, p_damage_boost_timer, p_shield_timer
    global p_damage_mult, p_shield

    if game_state != STATE_PLAYING:
        return

    # Sprint
    current_speed = p_spd
    p_sprinting = shift_held and p_stamina > 0 and (keys[b'w'] or keys[b's'] or keys[b'a'] or keys[b'd'])
    if p_sprinting:
        current_speed = p_sprint_spd
        p_stamina = max(0, p_stamina - p_stamina_drain * delta_time * 60)
    else:
        p_stamina = min(p_max_stamina, p_stamina + p_stamina_regen * delta_time * 60)

    # Speed boost power-up
    if p_speed_boost_timer > 0:
        current_speed *= 1.5
        p_speed_boost_timer -= delta_time

    # Damage boost power-up
    if p_damage_boost_timer > 0:
        p_damage_mult = 2.0
        p_damage_boost_timer -= delta_time
    else:
        p_damage_mult = 1.0

    # Shield timer
    if p_shield_timer > 0:
        p_shield_timer -= delta_time
        if p_shield_timer <= 0:
            p_shield = 0

    # Rotation
    if keys[b'a']:
        p_dir += p_rot
    if keys[b'd']:
        p_dir -= p_rot
    p_dir %= 360

    # Movement
    ang = math.radians(p_dir - 90)
    move_x = move_y = 0
    if keys[b'w']:
        move_x += current_speed * math.cos(ang)
        move_y += current_speed * math.sin(ang)
    if keys[b's']:
        move_x -= current_speed * math.cos(ang)
        move_y -= current_speed * math.sin(ang)

    final_x = p_pos[0] + move_x
    final_y = p_pos[1] + move_y

    # Clamp to arena
    final_x = max(-GRID + 20, min(GRID - 20, final_x))
    final_y = max(-GRID + 20, min(GRID - 20, final_y))

    # Obstacle collision
    if not check_obstacle_collision([final_x, final_y], radius=15):
        apply_smooth_movement(final_x, final_y, p_pos[2])
    else:
        # Try sliding along one axis
        if not check_obstacle_collision([final_x, p_pos[1]], radius=15):
            apply_smooth_movement(final_x, p_pos[1], p_pos[2])
        elif not check_obstacle_collision([p_pos[0], final_y], radius=15):
            apply_smooth_movement(p_pos[0], final_y, p_pos[2])


def apply_smooth_movement(t_x, t_y, t_z):
    """Apply momentum-based smooth movement"""
    global p_pos, p_mom
    p_mom[0] = p_mom[0] * p_fric + (t_x - p_pos[0]) * (1 - p_fric)
    p_mom[1] = p_mom[1] * p_fric + (t_y - p_pos[1]) * (1 - p_fric)
    p_mom[2] = p_mom[2] * p_fric + (t_z - p_pos[2]) * (1 - p_fric)
    p_pos[0] += p_mom[0]
    p_pos[1] += p_mom[1]
    p_pos[2] += p_mom[2]


def update_enemies():
    """Update enemy AI: movement, shooting, zone damage"""
    for e in enemies:
        if not e['alive']:
            continue
        et = enemy_types[e['type']]
        dx = p_pos[0] - e['pos'][0]
        dy = p_pos[1] - e['pos'][1]
        dist = math.sqrt(dx * dx + dy * dy)
        ang = math.atan2(dy, dx)

        spd = et['speed'] * (1.0 + current_level * 0.04) * delta_time * 60

        if e['type'] == 'scout':
            e['dodge_timer'] -= delta_time
            if e['dodge_timer'] <= 0:
                e['dodge_dir'] *= -1
                e['dodge_timer'] = random.uniform(0.5, 1.5)
            perp = ang + math.pi / 2
            new_x = e['pos'][0] + spd * (math.cos(ang) + 0.6 * e['dodge_dir'] * math.cos(perp))
            new_y = e['pos'][1] + spd * (math.sin(ang) + 0.6 * e['dodge_dir'] * math.sin(perp))
        elif e['type'] == 'sniper':
            if dist < 500:
                new_x = e['pos'][0] - spd * math.cos(ang) * 0.5
                new_y = e['pos'][1] - spd * math.sin(ang) * 0.5
            elif dist > 800:
                new_x = e['pos'][0] + spd * math.cos(ang) * 0.3
                new_y = e['pos'][1] + spd * math.sin(ang) * 0.3
            else:
                new_x = e['pos'][0]
                new_y = e['pos'][1]
        else:
            new_x = e['pos'][0] + spd * math.cos(ang)
            new_y = e['pos'][1] + spd * math.sin(ang)

        # Keep in arena
        new_x = max(-GRID + 30, min(GRID - 30, new_x))
        new_y = max(-GRID + 30, min(GRID - 30, new_y))
        e['pos'][0] = new_x
        e['pos'][1] = new_y

        # Zone damage to enemies
        edx = e['pos'][0] - zone_center[0]
        edy = e['pos'][1] - zone_center[1]
        if edx * edx + edy * edy > zone_radius * zone_radius:
            e['hp'] -= zone_damage * delta_time * 3
            if e['hp'] <= 0:
                e['alive'] = False
                spawn_particles(e['pos'], et['color'], 5)
                continue

        # Melee damage on contact
        if dist < 25 + et['size']:
            take_damage(et['damage'] * delta_time * 2)

        # Shooting
        e['fire_cd'] -= delta_time
        if e['fire_cd'] <= 0 and dist < 1200:
            enemy_fire(e)
            e['fire_cd'] = et['fire_rate'] * random.uniform(0.7, 1.3)

    enemies[:] = [e for e in enemies if e['alive']]


def update_projectiles():
    """Update player projectile positions and check for obstacle collisions"""
    to_remove = []
    for s in shots:
        ang = math.radians(s[3] - 90)
        s[0] += shot_spd * math.cos(ang) * delta_time * 60
        s[1] += shot_spd * math.sin(ang) * delta_time * 60

        if (s[0] > GRID or s[0] < -GRID or s[1] > GRID or s[1] < -GRID):
            to_remove.append(s)
        elif check_obstacle_collision([s[0], s[1]], radius=shot_size / 2):
            to_remove.append(s)
            spawn_particles([s[0], s[1], s[2]], (1, 0.5, 0), 3)

    for s in to_remove:
        if s in shots:
            shots.remove(s)


def update_enemy_projectiles():
    """Update enemy projectile positions and check for player hits"""
    to_remove = []
    for s in enemy_shots:
        ang = math.radians(s['dir'])
        s['pos'][0] += s['speed'] * math.cos(ang) * delta_time * 60
        s['pos'][1] += s['speed'] * math.sin(ang) * delta_time * 60
        s['life'] -= 1

        # Hit player?
        dx = s['pos'][0] - p_pos[0]
        dy = s['pos'][1] - p_pos[1]
        if dx * dx + dy * dy < 30 * 30:
            take_damage(s['damage'])
            to_remove.append(s)
            spawn_particles([s['pos'][0], s['pos'][1], s['pos'][2]], (1, 0, 0), 4)
            continue

        # Hit obstacle?
        if check_obstacle_collision(s['pos'], radius=4):
            to_remove.append(s)
            continue

        # Out of bounds or expired?
        if s['life'] <= 0 or abs(s['pos'][0]) > GRID or abs(s['pos'][1]) > GRID:
            to_remove.append(s)

    for s in to_remove:
        if s in enemy_shots:
            enemy_shots.remove(s)


def detect_hits():
    """Detect player projectile hits on enemies"""
    global p_score, total_shots_hit, combo_count, combo_timer, combo_multiplier
    global kill_streak, best_streak, best_combo, kills_this_level, total_kills

    for s in shots[:]:
        for e in enemies:
            if not e['alive']:
                continue
            et = enemy_types[e['type']]
            dx = s[0] - e['pos'][0]
            dy = s[1] - e['pos'][1]
            hit_r = et['size'] + 12
            if dx * dx + dy * dy <= hit_r * hit_r:
                dmg = 10 * s[4]  # base damage * multiplier
                e['hp'] -= dmg
                total_shots_hit += 1

                if s in shots:
                    shots.remove(s)

                if e['hp'] <= 0:
                    e['alive'] = False
                    # Scoring
                    combo_count += 1
                    combo_timer = combo_timeout
                    combo_multiplier = min(combo_count, 5)
                    best_combo = max(best_combo, combo_count)

                    points = int(et['points'] * combo_multiplier)
                    p_score += points
                    kill_streak += 1
                    best_streak = max(best_streak, kill_streak)
                    kills_this_level += 1
                    total_kills += 1

                    # Streak bonuses
                    if kill_streak == 5:
                        p_score += 50
                        add_notification("RAMPAGE! +50 bonus", (1, 0.5, 0), 3)
                    elif kill_streak == 10:
                        p_score += 100
                        add_notification("UNSTOPPABLE! +100 bonus", (1, 0, 1), 3)
                    elif kill_streak == 15:
                        p_score += 200
                        add_notification("GODLIKE! +200 bonus", (1, 0, 0), 3)

                    spawn_particles(e['pos'], et['color'], 12)

                    type_label = e['type'].capitalize()
                    add_notification(f"{type_label} eliminated! +{points} (x{combo_multiplier:.0f})",
                                     et['color'], 2.5)
                else:
                    spawn_particles([s[0], s[1], s[2]], (1, 1, 0), 3)

                break


def update_zone():
    """Update battle royale zone shrinking and damage"""
    global zone_radius, zone_target_radius, zone_next_shrink_time, zone_center, zone_warning

    # Trigger shrink after level 2
    if current_level >= 2 and game_time >= zone_next_shrink_time and zone_target_radius > 350:
        zone_target_radius = max(zone_target_radius - 150, 350)
        zone_next_shrink_time = game_time + zone_shrink_interval
        zone_center[0] += random.uniform(-80, 80)
        zone_center[1] += random.uniform(-80, 80)
        zone_center[0] = max(-500, min(500, zone_center[0]))
        zone_center[1] = max(-500, min(500, zone_center[1]))
        add_notification("ZONE SHRINKING!", (1, 0.3, 0.3), 5)

    # Smooth shrink
    if zone_radius > zone_target_radius:
        zone_radius = max(zone_radius - zone_shrink_rate * delta_time * 60, zone_target_radius)
        zone_warning = True
    else:
        zone_warning = False

    # Damage player outside zone
    dx = p_pos[0] - zone_center[0]
    dy = p_pos[1] - zone_center[1]
    if dx * dx + dy * dy > zone_radius * zone_radius:
        take_damage(zone_damage * delta_time * 8)


def update_powerups():
    """Spawn and handle power-up collection"""
    global powerup_spawn_timer, p_hp, p_speed_boost_timer, p_damage_boost_timer
    global p_shield, p_shield_timer

    # Spawn timer
    powerup_spawn_timer += delta_time
    if powerup_spawn_timer >= powerup_spawn_interval and len(powerups) < 8:
        spawn_powerup()
        powerup_spawn_timer = 0

    # Collection check
    for pu in powerups:
        if not pu['active']:
            continue
        dx = p_pos[0] - pu['pos'][0]
        dy = p_pos[1] - pu['pos'][1]
        if dx * dx + dy * dy < 40 * 40:
            pu['active'] = False
            ptype = pu['type']
            if ptype == 'health':
                healed = min(30, p_max_hp - p_hp)
                p_hp = min(p_hp + 30, p_max_hp)
                add_notification(f"Health +{int(healed)}", (0.1, 1, 0.1), 2)
            elif ptype == 'speed':
                p_speed_boost_timer = 10
                add_notification("Speed Boost! (10s)", (0.1, 0.5, 1), 2)
            elif ptype == 'damage':
                p_damage_boost_timer = 10
                add_notification("Damage Boost! (10s)", (1, 0.2, 0.2), 2)
            elif ptype == 'shield':
                p_shield = p_shield_max
                p_shield_timer = 15
                add_notification("Shield Active! (15s)", (0.9, 0.9, 0.1), 2)
            spawn_particles(pu['pos'], powerup_types[ptype]['color'], 8)

    powerups[:] = [pu for pu in powerups if pu['active']]


def update_combo():
    """Update combo timer and reset if expired"""
    global combo_count, combo_timer, combo_multiplier, kill_streak

    if combo_timer > 0:
        combo_timer -= delta_time
        if combo_timer <= 0:
            combo_count = 0
            combo_multiplier = 1.0
            kill_streak = 0


def update_particles():
    """Update particle positions and lifetimes"""
    for p in particles:
        p['life'] -= delta_time * 2
        p['pos'][0] += p['vel'][0] * delta_time * 60
        p['pos'][1] += p['vel'][1] * delta_time * 60
        p['pos'][2] += p['vel'][2] * delta_time * 60
        p['vel'][2] -= 0.3 * delta_time * 60  # gravity
    particles[:] = [p for p in particles if p['life'] > 0 and p['pos'][2] > -5]


def update_notifications():
    """Update notification timers"""
    for n in notifications:
        n['timer'] -= delta_time
    notifications[:] = [n for n in notifications if n['timer'] > 0]


def update_pulse():
    """Update enemy pulsing animation"""
    global t_pulse_t, t_pulse
    t_pulse_t += delta_time
    t_pulse = 1.0 + 0.15 * math.sin(t_pulse_t * 3)


def check_level_up():
    """Check if player has enough kills to advance to next level"""
    global current_level, kills_this_level, kills_to_advance, level_up_display

    if kills_this_level >= kills_to_advance:
        current_level += 1
        kills_this_level = 0
        kills_to_advance = 10 + current_level * 2
        level_up_display = 3.0

        # Heal on level up
        p_hp_restore = min(20, p_max_hp - p_hp)
        global p_hp
        p_hp = min(p_hp + 20, p_max_hp)

        # Clear remaining enemies and spawn new wave
        enemies.clear()
        enemy_shots.clear()
        spawn_enemies_for_level()

        add_notification(f"LEVEL {current_level}!", (1, 1, 0), 3)
        if p_hp_restore > 0:
            add_notification(f"+{int(p_hp_restore)} HP Restored", (0, 1, 0), 2)


def init_game():
    """Initialize game state for a new game"""
    global game_state, p_pos, p_dir, p_hp, p_score, p_mom, p_shield
    global p_stamina, p_speed_boost_timer, p_damage_boost_timer, p_shield_timer, p_damage_mult
    global current_level, kills_this_level, kills_to_advance, total_kills
    global combo_count, combo_timer, combo_multiplier, kill_streak, best_streak, best_combo
    global total_shots_fired, total_shots_hit, time_survived
    global zone_radius, zone_target_radius, zone_next_shrink_time, zone_center, zone_warning
    global fire_cooldown, damage_flash, level_up_display, powerup_spawn_timer
    global game_time

    game_state = STATE_PLAYING
    p_pos = [0, 0, 0]
    p_dir = 0
    p_mom = [0, 0, 0]
    p_hp = p_max_hp
    p_score = 0
    p_shield = 0
    p_stamina = p_max_stamina
    p_speed_boost_timer = 0
    p_damage_boost_timer = 0
    p_shield_timer = 0
    p_damage_mult = 1.0

    current_level = 1
    kills_this_level = 0
    kills_to_advance = 10
    total_kills = 0

    combo_count = 0
    combo_timer = 0
    combo_multiplier = 1.0
    kill_streak = 0
    best_streak = 0
    best_combo = 0

    total_shots_fired = 0
    total_shots_hit = 0
    time_survived = 0
    game_time = 0

    zone_radius = 2000
    zone_target_radius = 2000
    zone_next_shrink_time = 45
    zone_center = [0, 0]
    zone_warning = False

    fire_cooldown = 0
    damage_flash = 0
    level_up_display = 0
    powerup_spawn_timer = 0

    shots.clear()
    enemy_shots.clear()
    enemies.clear()
    particles.clear()
    notifications.clear()
    powerups.clear()

    for k in keys:
        keys[k] = False

    generate_obstacles()
    spawn_enemies_for_level()


def reset_game():
    """Full game reset"""
    init_game()


# ============================================================
# INPUT HANDLERS
# ============================================================

def keyboardListener(key, x, y):
    """Handle keyboard key press events"""
    global keys, game_state, player_name, shift_held, fp_view, p_rot

    # Update shift state
    mods = glutGetModifiers()
    shift_held = bool(mods & GLUT_ACTIVE_SHIFT)

    # Normalize to lowercase
    key_lower = key.lower()

    # Name entry mode
    if game_state == STATE_NAME_ENTRY:
        if key in (b'\r', b'\n'):
            if len(player_name) > 0:
                game_state = STATE_GUIDELINES
        elif key in (b'\x08', b'\x7f'):
            player_name = player_name[:-1]
        elif len(player_name) < 15:
            try:
                ch = key.decode('ascii')
                if ch.isprintable() and ch != ' ' or (ch == ' ' and len(player_name) > 0):
                    player_name += ch
            except (UnicodeDecodeError, ValueError):
                pass
        return

    # Guidelines mode
    if game_state == STATE_GUIDELINES:
        if key in (b'\r', b'\n'):
            init_game()
        return

    # Game over
    if game_state == STATE_GAME_OVER:
        if key_lower == b'r':
            reset_game()
        return

    # Paused
    if game_state == STATE_PAUSED:
        if key_lower == b'p':
            game_state = STATE_PLAYING
        return

    # Playing
    if game_state == STATE_PLAYING:
        if key_lower in keys:
            keys[key_lower] = True
        if key_lower == b'p':
            game_state = STATE_PAUSED
        elif key_lower == b'f':
            fp_view = not fp_view
            p_rot = 3 if fp_view else 5
        elif key == b' ':
            fire_weapon()


def keyboardUpListener(key, x, y):
    """Handle keyboard key release events"""
    global keys, shift_held
    mods = glutGetModifiers()
    shift_held = bool(mods & GLUT_ACTIVE_SHIFT)
    key_lower = key.lower()
    if key_lower in keys:
        keys[key_lower] = False


def specialKeyListener(key, x, y):
    """Handle special key events (arrow keys for camera)"""
    global cam_ang, cam_dist, cam_h, shift_held
    mods = glutGetModifiers()
    shift_held = bool(mods & GLUT_ACTIVE_SHIFT)

    if key == GLUT_KEY_UP:
        if cam_h > cam_min_h:
            cam_h -= 30
        if cam_dist > cam_min_dist:
            cam_dist -= 30
    elif key == GLUT_KEY_DOWN:
        if cam_h < cam_max_h:
            cam_h += 30
        if cam_dist < cam_max_dist:
            cam_dist += 30
    elif key == GLUT_KEY_LEFT:
        cam_ang -= 5
    elif key == GLUT_KEY_RIGHT:
        cam_ang += 5


def mouseListener(button, state, x, y):
    """Handle mouse button events"""
    global fp_view, p_rot
    if game_state != STATE_PLAYING:
        return
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_weapon()
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        fp_view = not fp_view
        p_rot = 3 if fp_view else 5


# ============================================================
# CAMERA & RENDERING
# ============================================================

def setupCamera():
    """Configure camera perspective and position"""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOV, float(WIN_W) / float(WIN_H), 1, 10000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if fp_view:
        ang_r = math.radians(p_dir)
        eye_x = p_pos[0] + gun_pos[0] / 2 * math.sin(ang_r) - gun_pos[1] * math.cos(ang_r)
        eye_y = p_pos[1] - gun_pos[0] / 2 * math.cos(ang_r) - gun_pos[1] * math.sin(ang_r)
        eye_z = p_pos[2] + gun_pos[2] + 25
        cen_x = eye_x - math.sin(-ang_r) * 100
        cen_y = eye_y - math.cos(-ang_r) * 100
        cen_z = eye_z
        gluLookAt(eye_x, eye_y, eye_z, cen_x, cen_y, cen_z, 0, 0, 1)
    else:
        ang_r = math.radians(cam_ang)
        x = p_pos[0] + cam_dist * math.sin(ang_r)
        y = p_pos[1] + cam_dist * math.cos(ang_r)
        z = p_pos[2] + cam_h
        gluLookAt(x, y, z, p_pos[0], p_pos[1], p_pos[2] + 50, 0, 0, 1)


def update_time():
    """Update delta time and game clock"""
    global last_time, delta_time, game_time, time_survived, fire_cooldown
    global damage_flash, level_up_display

    current = time.time()
    delta_time = min(current - last_time, 0.05)  # Cap at 50ms to prevent huge jumps
    last_time = current

    if game_state == STATE_PLAYING:
        game_time += delta_time
        time_survived = game_time
        if fire_cooldown > 0:
            fire_cooldown -= delta_time
    elif game_state in (STATE_NAME_ENTRY, STATE_GUIDELINES):
        game_time += delta_time  # For animations

    if damage_flash > 0:
        damage_flash -= delta_time * 3
    if level_up_display > 0:
        level_up_display -= delta_time


def idle():
    """Main game loop - updates all game logic"""
    update_time()

    if game_state == STATE_PLAYING:
        update_player()
        update_enemies()
        update_pulse()
        update_projectiles()
        update_enemy_projectiles()
        detect_hits()
        update_zone()
        update_powerups()
        update_combo()
        update_particles()
        update_notifications()
        check_level_up()

        # Respawn enemies if too few alive
        alive_count = sum(1 for e in enemies if e['alive'])
        if alive_count < 3:
            spawn_enemy(random.choice(['grunt', 'scout']))

    glutPostRedisplay()


def showScreen():
    """Render the complete scene"""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, WIN_W, WIN_H)

    if game_state == STATE_NAME_ENTRY:
        draw_name_entry()
    elif game_state == STATE_GUIDELINES:
        draw_guidelines()
    elif game_state in (STATE_PLAYING, STATE_PAUSED, STATE_GAME_OVER):
        setupCamera()
        # Update light position relative to scene
        glLightfv(GL_LIGHT0, GL_POSITION, [200, 200, 2000, 0])
        draw_scene()
        draw_hud()
        if game_state == STATE_PAUSED:
            draw_pause()
        elif game_state == STATE_GAME_OVER:
            draw_game_over()

    glutSwapBuffers()


def init_graphics():
    """Set up OpenGL rendering state"""
    glClearColor(0.04, 0.04, 0.12, 1.0)
    glEnable(GL_DEPTH_TEST)

    # Lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.25, 0.25, 0.3, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.75, 0.75, 0.7, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.3, 0.3, 0.3, 1.0])
    glLightfv(GL_LIGHT0, GL_POSITION, [200, 200, 2000, 0])

    # Fog for atmosphere
    glEnable(GL_FOG)
    fog_color = [0.04, 0.04, 0.12, 1.0]
    glFogfv(GL_FOG_COLOR, fog_color)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_START, 2000)
    glFogf(GL_FOG_END, 6000)

    glShadeModel(GL_SMOOTH)


def main():
    """Initialize OpenGL and start the game"""
    global WIN_W, WIN_H, last_time

    glutInit()
    WIN_W = glutGet(GLUT_SCREEN_WIDTH)
    WIN_H = glutGet(GLUT_SCREEN_HEIGHT)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIN_W, WIN_H)
    glutCreateWindow(b"Target Frenzy 3D - Battle Royale")
    glutFullScreen()

    init_graphics()
    last_time = time.time()

    glutDisplayFunc(showScreen)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboardListener)
    glutKeyboardUpFunc(keyboardUpListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutMainLoop()


if __name__ == "__main__":
    main()
