import math
import pygame as pg
from OpenGL.GL import *
from OpenGL.GLU import *


def mouseMotion(dx, dy):
    global rot
    dx /= 8
    dy /= 8
    rot[0] += dy
    rot[1] += dx
    if rot[0] > 90:
        rot[0] = 90
    elif rot[0] < -90:
        rot[0] = -90


def updatePosition():
    global px, py, pz, rot
    spd = MSPEED * FPS / 1000

    keys = pg.key.get_pressed()

    rotY = rot[1] / 180 * math.pi
    dx, dz = spd * math.sin(rotY), spd * math.cos(rotY)
    DX, DY, DZ = 0, 0, 0

    if keys[pg.K_w]:
        DX += dx
        DZ -= dz
    if keys[pg.K_s]:
        DX -= dx
        DZ += dz
    if keys[pg.K_a]:
        DX -= dz
        DZ -= dx
    if keys[pg.K_d]:
        DX += dz
        DZ += dx
    if keys[pg.K_LSHIFT]:
        DY -= spd
    if keys[pg.K_SPACE]:
        DY += spd

    px += DX
    py += DY
    pz += DZ

    glRotatef(rot[0], 1, 0, 0)
    glRotatef(rot[1], 0, 1, 0)
    glTranslatef(-px, -py, -pz)


def drawCube(x, y, z):
    glColor3f(0.2, 1.0, 0.2)
    glVertex3f(x + 1.0, y + 1.0, z + 0.0)
    glVertex3f(x + 0.0, y + 1.0, z + 0.0)
    glVertex3f(x + 0.0, y + 1.0, z + 1.0)
    glVertex3f(x + 1.0, y + 1.0, z + 1.0)

    glColor3f(1.0, 0.2, 0.2)
    glVertex3f(x + 1.0, y + 0.0, z + 1.0)
    glVertex3f(x + 0.0, y + 0.0, z + 1.0)
    glVertex3f(x + 0.0, y + 0.0, z + 0.0)
    glVertex3f(x + 1.0, y + 0.0, z + 0.0)

    glColor3f(0.2, 0.2, 1.0)
    glVertex3f(x + 1.0, y + 1.0, z + 1.0)
    glVertex3f(x + 0.0, y + 1.0, z + 1.0)
    glVertex3f(x + 0.0, y + 0.0, z + 1.0)
    glVertex3f(x + 1.0, y + 0.0, z + 1.0)

    glColor3f(1.0, 1.0, 0.2)
    glVertex3f(x + 1.0, y + 0.0, z + 0.0)
    glVertex3f(x + 0.0, y + 0.0, z + 0.0)
    glVertex3f(x + 0.0, y + 1.0, z + 0.0)
    glVertex3f(x + 1.0, y + 1.0, z + 0.0)

    glColor3f(0.2, 1.0, 1.0)
    glVertex3f(x + 0.0, y + 1.0, z + 1.0)
    glVertex3f(x + 0.0, y + 1.0, z + 0.0)
    glVertex3f(x + 0.0, y + 0.0, z + 0.0)
    glVertex3f(x + 0.0, y + 0.0, z + 1.0)

    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(x + 1.0, y + 1.0, z + 0.0)
    glVertex3f(x + 1.0, y + 1.0, z + 1.0)
    glVertex3f(x + 1.0, y + 0.0, z + 1.0)
    glVertex3f(x + 1.0, y + 0.0, z + 0.0)


WIDTH, HEIGHT, FPS, PAUSE, MSPEED = 1280, 720, 1000, False, 0.2
px, py, pz, rot = 0, 0, 0, [0, 0]

pg.init()
pg.display.set_mode((WIDTH, HEIGHT), pg.DOUBLEBUF | pg.OPENGL)
clock = pg.time.Clock()

glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(100, (WIDTH / HEIGHT), 0.1, 1000)
glMatrixMode(GL_MODELVIEW)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit(0)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                PAUSE = not PAUSE
    pg.mouse.set_visible(PAUSE)
    if PAUSE:
        continue
    mx, my = pg.mouse.get_pos()
    mouseMotion(mx - WIDTH // 2, my - HEIGHT // 2)
    pg.mouse.set_pos((WIDTH // 2, HEIGHT // 2))
    glClearColor(0.5, 0.7, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glPushMatrix()
    updatePosition()
    glBegin(GL_QUADS)
    for i in range(20):
        for j in range(20):
            drawCube(i, -2, j)
    glEnd()
    glPopMatrix()

    glFlush()

    pg.display.set_caption(f"FPS: {clock.get_fps()}")
    pg.display.flip()
    clock.tick(FPS)
