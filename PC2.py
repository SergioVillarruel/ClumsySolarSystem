import sys, pygame
import numpy as np
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from obj_loader import *
import math 

def render():
    pygame.init()
    viewport = (1280,720)
    hx = viewport[0]/2
    hy = viewport[1]/2
    srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

    glLightfv(GL_LIGHT0, GL_POSITION,  (0, 0, 1, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5, 0.5, 0.5, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    #Sombreado suavecito
    glShadeModel(GL_SMOOTH)    

    sol = OBJ("sol/model.obj", swapyz=True)
    sol.generate()

    planeta = OBJ("covid/model.obj", swapyz=True)
    planeta.generate()

    planeta2 = OBJ("chicken/chicken.obj", swapyz=True)
    planeta2.generate()

    satelite = OBJ("egg/egg.obj", swapyz=True)
    satelite.generate()

    clock = pygame.time.Clock()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = viewport
    gluPerspective(90.0, width/float(height), 1., 150.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    rx, ry = (0,0)
    tx, ty = (0,0)
    zpos = 5
    rotate = move = False
    running = 1
    while running:
        clock.tick(30)
        for e in pygame.event.get():
            if e.type == QUIT:
                running = False
           
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                running = False
          
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 4: zpos = max(1, zpos-1)
                elif e.button == 5: zpos += 1
                elif e.button == 1: rotate = True
                elif e.button == 3: move = True
            elif e.type == MOUSEBUTTONUP:
                if e.button == 1: rotate = False
                elif e.button == 3: move = False
            elif e.type == MOUSEMOTION:
                i, j = e.rel
                if rotate:
                    rx += i
                    ry += j
                if move:
                    tx += i
                    ty -= j

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.,0.,0.,0)
        glLoadIdentity()

        # Renderizamos el objeto

        glTranslate(tx/20., ty/20., - zpos)
        glRotate(ry, 1, 0, 0)
        rx += 1
        glRotate(rx, 0, 1, 0)
        glEnable(GL_LIGHT0)
        #SOL
        sol.rotation += 3
        glRotate(-90, 1, 0, 0)
        glRotate(sol.rotation, 0, 0, 1)
        sol.render()
        glRotate(-sol.rotation, 0, 0, 1)
        glRotate(90, 1, 0, 0)
        glDisable(GL_LIGHT0)

        glPushMatrix()
        planeta.rx += 1
        #glRotate(planeta.rx, 0, 1, 0)
        #PLANETA 1
        glTranslate(2, 0., 0.)
        glRotate(sol.rotation, 0, 1, 0)
        glScalef(0.5,0.5,0.5)
        planeta.render()
        glScalef(-0.5,-0.5,-0.5)
        glRotate(-sol.rotation, 0, 1, 0)
        glTranslate(-2., 0., 0.)
        glRotate(-planeta.rx, 0, 1, 0)
        glPopMatrix()

        planeta2.rx += 1.5
        #glRotate(planeta2.rx, 0, 1, 0)

        #glRotate(rx, 0, 1, 0)
        #PLANETA 2
        glTranslate(1, 0., 0.)
        glRotate(-90, 1, 0, 0)
        glRotate(-sol.rotation, 0, 0, 1)
        glScalef(0.2,0.2,0.2)
        planeta2.render()
        glScalef(1,1,1)
        glRotate(90, 1, 0, 0)
        glRotate(sol.rotation, 0, 0, 1)
        glTranslate(-1., 0., 0.)

        glEnable(GL_LIGHT0)
        #SATELITE
        glTranslate(1, 2., 0.)
        glRotate(90, 1, 0, 0)
        glRotate(sol.rotation, 0, 1, 1)
        glScalef(3,3,3)
        satelite.render()
        glScalef(1,1,1)
        glRotate(-90, 1, 0, 0)
        glRotate(-sol.rotation, 0, 1, 1)
        glTranslate(-1., -2., 0.)
        glDisable(GL_LIGHT0)
        #glRotate(-planeta2.rx, 0, 1, 0)
        #glTranslate(-tx/20., -ty/20., + zpos)
        #glRotate(-ry, 1, 0, 0)
        #glRotate(-rx, 0, 1, 0)
       

        pygame.display.flip()
render()