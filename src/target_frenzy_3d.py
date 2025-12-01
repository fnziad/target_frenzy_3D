"""
Target Frenzy 3D - A fast-paced 3D arena shooter game
Author: Fahad Nadim Ziad
License: MIT
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18

import math
import random

# Window configuration
WIN_W = 1000  # Updated to screen width at runtime
WIN_H = 800   # Updated to screen height at runtime
GRID = 600
FOV = 60

# Camera configuration
cam_pos = (0, 600, 600)
cam_ang = 0
cam_dist = 600
cam_h = 600
cam_min_h = 200
cam_max_h = 1000
cam_min_dist = 200
cam_max_dist = 1000

# Game state flags
done = False
fp_view = False
easy_mode = False
easy_vision = False

# Player configuration
p_pos = [0, 0, 0]
p_dir = 0
p_spd = 10
p_rot = 5
p_easy_rot = 45
p_hp = 5
p_score = 0
p_mom = [0, 0, 0]
p_fric = 0.85

# Movement keys
keys = {b'w': False, b's': False, b'a': False, b'd': False}

# Weapon configuration
gun_rate = 0.5
shots = []
misses = 0
max_miss = 10
shot_size = 8
shot_spd = 4
gun_pos = [30, 15, 80]

# Aiming configuration
easy_aim = 5.0
fp_aim = 3.0

# Enemy configuration
targs = []
t_pulse = 1.0
t_pulse_t = 0
targ_spd = 0.025
targ_num = 5
targ_size = 60
targ_bonus = 20

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    """Renders text on screen at specified coordinates"""
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WIN_W, 0, WIN_H)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for c in text:
        glutBitmapCharacter(font, ord(c))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_shapes():
    """Renders all game objects in the scene"""
    draw_game_floor()
    draw_player_model()
    if not done:
        for t in targs:
            draw_target_model(*t)
        for s in shots:
            draw_projectile(s[0], s[1], s[2])

def draw_game_floor():
    """Renders the checkered floor and arena walls"""
    glBegin(GL_QUADS)
    for i in range(-GRID, GRID + 1, 100):
        for j in range(-GRID, GRID + 1, 100):
            glColor3f(0.9, 0.9, 0.9) if (i + j) % 200 == 0 else glColor3f(0.6, 0.4, 0.8)
            glVertex3f(i, j, 0)
            glVertex3f(i + 100, j, 0)
            glVertex3f(i + 100, j + 100, 0)
            glVertex3f(i, j + 100, 0)
    # Walls
    glColor3f(0.2, 0.8, 0.3)  # Green left
    glVertex3f(-GRID, -GRID, 0)
    glVertex3f(-GRID, GRID + 100, 0)
    glVertex3f(-GRID, GRID + 100, 100)
    glVertex3f(-GRID, -GRID, 100)
    glColor3f(0.2, 0.3, 0.8)  # Blue right
    glVertex3f(GRID + 100, -GRID, 0)
    glVertex3f(GRID + 100, GRID + 100, 0)
    glVertex3f(GRID + 100, GRID + 100, 100)
    glVertex3f(GRID + 100, -GRID, 100)
    glColor3f(0.9, 0.9, 0.9)  # White bottom
    glVertex3f(-GRID, GRID + 100, 0)
    glVertex3f(GRID + 100, GRID + 100, 0)
    glVertex3f(GRID + 100, GRID + 100, 100)
    glVertex3f(-GRID, GRID + 100, 100)
    glColor3f(0.2, 0.8, 0.8)  # Cyan top
    glVertex3f(-GRID, -GRID, 0)
    glVertex3f(GRID + 100, -GRID, 0)
    glVertex3f(GRID + 100, -GRID, 100)
    glVertex3f(-GRID, -GRID, 100)
    glEnd()

def draw_player_model():
    """Renders the player character model"""
    global gun_pos
    glPushMatrix()
    glTranslatef(*p_pos)
    glRotatef(p_dir, 0, 0, 1)
    if done:
        glRotatef(-90, 1, 0, 0)
    # Legs
    glTranslatef(0, 0, 0)
    glColor3f(0.1, 0.1, 0.7)
    gluCylinder(gluNewQuadric(), 6, 12, 45, 10, 10)
    glTranslatef(30, 0, 0)
    glColor3f(0.1, 0.1, 0.7)
    gluCylinder(gluNewQuadric(), 6, 12, 45, 10, 10)
    # Body
    glTranslatef(-15, 0, 70)
    glColor3f(0.3, 0.4, 0.2)
    glutSolidCube(40)
    # Head
    glTranslatef(0, 0, 40)
    glColor3f(0.1, 0.1, 0.1)
    gluSphere(gluNewQuadric(), 20, 12, 12)
    # Arms
    glTranslatef(20, -60, -30)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.95, 0.85, 0.75)
    gluCylinder(gluNewQuadric(), 4, 8, 50, 10, 10)
    glRotatef(90, 1, 0, 0)
    glTranslatef(-40, 0, 0)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.95, 0.85, 0.75)
    gluCylinder(gluNewQuadric(), 4, 8, 50, 10, 10)
    # Gun
    glRotatef(90, 1, 0, 0)
    glTranslatef(20, -40, 0)
    glRotatef(-90, 1, 0, 0)
    glColor3f(0.75, 0.75, 0.75)
    gluCylinder(gluNewQuadric(), 3, 12, 80, 10, 10)
    glPopMatrix()
    gun_pos = [30, 15, 80]

def draw_target_model(x, y, z):
    """Renders an enemy target at specified position"""
    glPushMatrix()
    glTranslatef(x, y, z + 35)
    glScalef(t_pulse, t_pulse, t_pulse)
    glColor3f(0.9, 0.1, 0.1)
    gluSphere(gluNewQuadric(), 35, 16, 16)
    glTranslatef(0, 0, 50)
    glColor3f(0, 0, 0)
    gluSphere(gluNewQuadric(), 15, 12, 12)
    glPopMatrix()

def draw_projectile(x, y, z):
    """Renders a projectile at specified position"""
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    glColor3f(1, 0.5, 0)
    glutSolidCube(shot_size)
    glPopMatrix()

def fire_weapon():
    """Fires a projectile from the player's weapon"""
    global shots, shot_spd
    if fp_view:
        ang = math.radians(p_dir + 45)
        x = p_pos[0] + (gun_pos[0] + 5) * math.sin(ang) - gun_pos[1] * math.cos(ang)
        y = p_pos[1] - (gun_pos[0] + 5) * math.cos(ang) - gun_pos[1] * math.sin(ang)
        z = p_pos[2] + gun_pos[2]
        var = 0.8 if not easy_mode else 0.1
        shot = [x, y, z, p_dir + random.uniform(-var, var)]
    else:
        ang = math.radians(p_dir - 90)
        off_x = gun_pos[0] * math.cos(ang) - gun_pos[1] * math.sin(ang)
        off_y = gun_pos[0] * math.sin(ang) + gun_pos[1] * math.cos(ang)
        x = p_pos[0] + off_x
        y = p_pos[1] + off_y
        z = p_pos[2] + gun_pos[2]
        var = 0.4 if not easy_mode else 0.05
        shot = [x, y, z, p_dir + random.uniform(-var, var)]
    shots.append(shot)

def update_projectiles():
    """Updates projectile positions and checks for boundary collisions"""
    global shots, misses, targs, done
    to_rem = []
    for s in shots:
        ang = math.radians(s[3] - 90)
        s[0] += shot_spd * math.cos(ang)
        s[1] += shot_spd * math.sin(ang)
        if (s[0] > GRID + 100 or s[0] < -GRID or
            s[1] > GRID + 100 or s[1] < -GRID):
            to_rem.append(s)
            if not easy_mode:
                misses += 1
                print(f"Miss! {misses}/{max_miss}")
    for s in to_rem:
        if s in shots:
            shots.remove(s)
    if misses >= max_miss and not easy_mode:
        done = True
        print("Game over! Too many misses.")
        print(f"Score: {p_score}")

def update_targets():
    """Updates enemy positions and checks for player collisions"""
    global targs, p_hp, done, targ_spd
    base_spd = 0.025
    spd_up = 1.0 + (p_score / 50.0)
    targ_spd = min(base_spd * spd_up, base_spd * 3.0)
    for t in targs[:]:
        dx = p_pos[0] - t[0]
        dy = p_pos[1] - t[1]
        dist = math.sqrt(dx*dx + dy*dy)
        if dist < 50:
            if not easy_mode:
                p_hp -= 1
                print(f"Ouch! HP: {p_hp}")
                if p_hp <= 0:
                    done = True
                    print("Game over! Dead.")
                    print(f"Score: {p_score}")
                    targs.clear()
                    shots.clear()
                    break
            if t in targs:
                targs.remove(t)
            spawn_targets(1)
        else:
            ang = math.atan2(dy, dx)
            t[0] += targ_spd * math.cos(ang)
            t[1] += targ_spd * math.sin(ang)

def detect_target_hits():
    """Detects collisions between projectiles and enemies"""
    global shots, targs, p_score
    for s in shots[:]:
        s_x = s[0]
        s_y = s[1]
        for t in targs[:]:
            t_x = t[0]
            t_y = t[1]
            dx = s_x - t_x
            dy = s_y - t_y
            dist = math.sqrt(dx*dx + dy*dy)
            hit_r = targ_size + 10
            if easy_mode:
                hit_r += targ_bonus
            if dist <= hit_r:
                p_score += 1
                print(f"Hit! Score: {p_score}")
                if s in shots:
                    shots.remove(s)
                if t in targs:
                    targs.remove(t)
                spawn_targets(1)
                break

def update_target_pulse():
    """Animates the pulsing effect for enemy targets"""
    global t_pulse_t, t_pulse
    t_pulse_t += 0.01
    t_pulse = 1.0 + 0.4 * math.sin(t_pulse_t)

def get_target_angles():
    """Calculates angles to all enemies relative to player direction"""
    angles = []
    for t in targs:
        dx = p_pos[0] - t[0]
        dy = p_pos[1] - t[1]
        ang = math.degrees(math.atan2(dy, dx)) - 90
        ang = (ang + 360) % 360
        angles.append(ang)
    return angles

def assist_aim_and_fire():
    """Provides auto-aim assistance in easy mode"""
    global p_pos, p_dir
    if not targs:
        return
    angles = get_target_angles()
    p_dir = (p_dir + p_easy_rot / 10) % 360
    for ang in angles:
        diff = abs((p_dir - ang + 540) % 360 - 180)
        if fp_view:
            if diff <= fp_aim:
                fire_weapon()
                break
        else:
            if diff <= easy_aim:
                fire_weapon()
                break

def update_player_movement():
    """Handles player movement based on input keys"""
    global p_pos, p_dir, p_mom
    if done:
        return
    rot_spd = p_easy_rot if easy_mode else p_rot
    if not easy_mode:
        if keys[b'a']:
            p_dir += rot_spd
        if keys[b'd']:
            p_dir -= rot_spd
    p_dir %= 360
    move_x = move_y = 0
    if easy_mode:
        if keys[b'w']:
            move_y += p_spd
        if keys[b's']:
            move_y -= p_spd
        if keys[b'a']:
            move_x -= p_spd
        if keys[b'd']:
            move_x += p_spd
        if not fp_view:
            move_y = -move_y
            move_x = -move_x
        final_x = p_pos[0] + move_x
        final_y = p_pos[1] + move_y
    else:
        ang = p_dir - 90
        ang_r = math.radians(ang)
        if keys[b'w']:
            move_x += p_spd * math.cos(ang_r)
            move_y += p_spd * math.sin(ang_r)
        if keys[b's']:
            move_x -= p_spd * math.cos(ang_r)
            move_y -= p_spd * math.sin(ang_r)
        final_x = p_pos[0] + move_x
        final_y = p_pos[1] + move_y
    if final_x < -GRID:
        final_x = -GRID
    if final_x > GRID:
        final_x = GRID
    if final_y < -GRID:
        final_y = -GRID
    if final_y > GRID:
        final_y = GRID
    apply_smooth_movement(final_x, final_y, p_pos[2])

def apply_smooth_movement(t_x, t_y, t_z):
    """Applies momentum-based smooth movement to player"""
    global p_pos, p_mom, p_fric
    p_mom[0] = p_mom[0] * p_fric + (t_x - p_pos[0]) * (1 - p_fric)
    p_mom[1] = p_mom[1] * p_fric + (t_y - p_pos[1]) * (1 - p_fric)
    p_mom[2] = p_mom[2] * p_fric + (t_z - p_pos[2]) * (1 - p_fric)
    p_pos[0] += p_mom[0]
    p_pos[1] += p_mom[1]
    p_pos[2] += p_mom[2]

def spawn_targets(count=targ_num):
    """Spawns specified number of enemy targets at random positions"""
    global targs
    for _ in range(count):
        x = random.uniform(-GRID + 100, GRID - 100)
        y = random.uniform(-GRID + 100, GRID - 100)
        z = 0
        while abs(x - p_pos[0]) < 200:
            x = random.uniform(-GRID + 100, GRID - 100)
        while abs(y - p_pos[1]) < 200:
            y = random.uniform(-GRID + 100, GRID - 100)
        targs.append([x, y, z])

def reset_game():
    """Resets all game variables to initial state"""
    global done, fp_view, easy_mode, easy_vision, p_pos, p_dir, p_mom
    global p_hp, p_score, misses, keys
    done = False
    fp_view = False
    easy_mode = False
    easy_vision = False
    p_pos = [0, 0, 0]
    p_mom = [0, 0, 0]
    p_dir = 0
    p_hp = 5
    p_score = 0
    for k in keys:
        keys[k] = False
    misses = 0
    shots.clear()
    targs.clear()
    spawn_targets()

def keyboardListener(key, x, y):
    """Handles keyboard key press events"""
    global keys, easy_mode, easy_vision, fp_view, done
    if done and key != b'r':
        return
    if key in keys:
        keys[key] = True
    if key == b'c':
        easy_mode = not easy_mode
        if easy_mode:
            misses = 0
    elif key == b'v':
        if fp_view and easy_mode:
            easy_vision = not easy_vision
    elif key == b'r':
        reset_game()
    elif key == b' ':
        fire_weapon()

def keyboardUpListener(key, x, y):
    """Handles keyboard key release events"""
    global keys
    if key in keys:
        keys[key] = False

def specialKeyListener(key, x, y):
    """Handles special key events (arrow keys for camera control)"""
    global cam_ang, cam_dist, cam_h, cam_min_h, cam_max_h, cam_min_dist, cam_max_dist
    if key == GLUT_KEY_UP:
        if cam_h > cam_min_h:
            cam_h -= 20
        if cam_dist > cam_min_dist:
            cam_dist -= 20
    elif key == GLUT_KEY_DOWN:
        if cam_h < cam_max_h:
            cam_h += 20
        if cam_dist < cam_max_dist:
            cam_dist += 20
    elif key == GLUT_KEY_LEFT:
        cam_ang -= 5
    elif key == GLUT_KEY_RIGHT:
        cam_ang += 5

def mouseListener(button, state, x, y):
    """Handles mouse button click events"""
    global fp_view, p_rot, easy_vision, done
    if done:
        return
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        fire_weapon()
        print("Shot!")
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        fp_view = not fp_view
        easy_vision = False
        p_rot = 2.5 if fp_view else 5

def setupCamera():
    """Configures camera perspective and position"""
    global cam_pos, cam_ang, cam_dist, cam_h
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOV, float(WIN_W) / float(WIN_H), 0.1, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if fp_view:
        ang_r = math.radians(p_dir)
        if easy_mode and not easy_vision:
            eye_x = p_pos[0]
            eye_y = p_pos[1] - 60
            eye_z = p_pos[2] + gun_pos[2] + 30
            cen_x = p_pos[0]
            cen_y = p_pos[1] + 300
            cen_z = p_pos[2] + 10
        else:
            eye_x = p_pos[0] + gun_pos[0]/2 * math.sin(ang_r) - gun_pos[1] * math.cos(ang_r)
            eye_y = p_pos[1] - gun_pos[0]/2 * math.cos(ang_r) - gun_pos[1] * math.sin(ang_r)
            eye_z = p_pos[2] + gun_pos[2] + 20
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

def idle():
    """Main game loop - updates all game logic"""
    if not done:
        update_player_movement()
        update_targets()
        update_target_pulse()
        update_projectiles()
        detect_target_hits()
        if easy_mode:
            assist_aim_and_fire()
    glutPostRedisplay()

def showScreen():
    """Renders the complete scene and HUD"""
    global done, p_hp, p_score, misses
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, WIN_W, WIN_H)
    setupCamera()
    draw_shapes()
    if not done:
        draw_text(10, WIN_H - 50, f"HP: {p_hp}")
        draw_text(10, WIN_H - 80, f"Score: {p_score}")
        draw_text(10, WIN_H - 110, f"Misses: {misses}")
        draw_text(10, WIN_H - 140, "FP View" if fp_view else "Cam: Arrows to move")
        if easy_mode:
            draw_text(10, WIN_H - 170, "Cheat MODE - Can't die")
    else:
        draw_text(10, WIN_H - 50, f"Game Over! Score: {p_score}")
        draw_text(10, WIN_H - 80, "Press R to restart")
    glutSwapBuffers()

def main():
    """Initializes OpenGL and starts the game"""
    glutInit()
    global WIN_W, WIN_H
    WIN_W = glutGet(GLUT_SCREEN_WIDTH)
    WIN_H = glutGet(GLUT_SCREEN_HEIGHT)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WIN_W, WIN_H)
    glutCreateWindow(b"Target Frenzy 3D")
    glutFullScreen()
    glEnable(GL_DEPTH_TEST)
    spawn_targets()
    glutDisplayFunc(showScreen)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboardListener)
    glutKeyboardUpFunc(keyboardUpListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutMainLoop()

if __name__ == "__main__":
    main()