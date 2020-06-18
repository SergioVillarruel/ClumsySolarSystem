import pygame as pg
import numpy as np
from pygame.locals import *
import math 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

from open_off import *

VERTEX_SHADER = """
attribute vec3 position;
uniform float dz;
void main()
{
  gl_Position = vec4(position,10.0);

  // or gl_Position.xyzw = vec4(position, 0.0, 1.0);

  // or gl_Position.xy = position;
  //    gl_Position.zw = vec2(0.0, 1.0);

  //gl_Position.x = position.x;
  //gl_Position.y = position.y;
  //gl_Position.z = 0.0;
  //gl_Position.w = 1;
}
"""

FRAGMENT_SHADER = """
void main()
{
  gl_FragColor = vec4(0.5, 0.0, 0.5, 1.0);

  // or gl_FragColor.rgba = vec4(1.0, 0.0, 0.0, 1.0);

  // or gl_FragColor.rgb = vec3(1.0, 0.0, 0.0);
  //    gl_FragColor.a = 1.0;
}
"""

def draw_model(verts,triangle_faces,quads_faces):
    glBegin(GL_QUADS)
    for face in quads_faces:
        for vertex in face:
            glVertex3fv(verts[vertex])
    glEnd()
    glBegin(GL_TRIANGLES)
    for face in triangle_faces:
        for vertex in face:
            glVertex3fv(verts[vertex])
    glEnd()

def matriz_rotacion(points,axis=0,grade=5):
    radian = grade * math.pi / 180
    coseno = math.cos(radian)
    seno = math.sin(radian)
    R = [[0,0,0],
        [0,0,0],
        [0,0,0]]
    if axis == 0:
        R = [[1,0,0],
        [0,coseno,-1*seno],
        [0,seno,coseno]]
    elif axis == 1:
        R = [[coseno,0,seno],
        [0,1,0],
        [-seno,0,coseno]]
    elif axis == 2:
        R = [[coseno,-1*seno,0],
        [seno,coseno,0],
        [0,0,1]]
    R = np.array(R)
    return np.dot(points,R)

def main():
    pg.init()
    display = (1680, 1050)
    pg.display.set_mode(display, DOUBLEBUF|OPENGL)
    verts, t_faces,q_faces = read_model("sphere.off")
    verts2, t_faces2, q_faces2 = read_model("dragon.off")
    verts3, t_faces3, q_faces3 = read_model("helice.off")
    vertexshader = shaders.compileShader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragmentshader = shaders.compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    shaderProgram = shaders.compileProgram(vertexshader, fragmentshader)
    
    glLinkProgram(shaderProgram)

    #AnGULO RATIO plano más cercano plano más lejano
    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)

    #traslacion
    verts2 += np.array([6,0,0])
    verts3 += np.array([15,0,4.5])

    #Posición x y z 
    glTranslatef(0.0, 0.0, -20)
    #glUseProgram(shaderProgram
    x = 1
    dx = 0.1
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
     

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
       
        if(verts.min(0)[2]<verts2.min(0)[2]):
            glTranslatef(0.0, 0.0, 10)
            glColor3f(0.0,x,1.0)
            draw_model(verts, t_faces,q_faces)
            glTranslatef(0.0, 0.0, -10)
            glColor3f(1.0,0.0,0.0)
            draw_model(verts2, t_faces2,q_faces2)
            glTranslatef(0.0, 0.0, -30)
            draw_model(verts3, t_faces3,q_faces3)
            glTranslatef(0.0, 0.0, 30)
        else:
            glColor3f(1.0,0.0,0.0)
            draw_model(verts2, t_faces2,q_faces2)
            glTranslatef(0.0, 0.0, -30)
            draw_model(verts3, t_faces3,q_faces3)
            glTranslatef(0.0, 0.0, 30)

            glTranslatef(0.0, 0.0, 10)
            glColor3f(0.0,x,1.0)
            draw_model(verts, t_faces,q_faces)
            glTranslatef(0.0, 0.0, -10)
        x += dx
        if x > 1:
            dx *= -1
        elif x < 0:
            dx *= -1
        verts2 = matriz_rotacion(verts2,1,10)
        verts3 = matriz_rotacion(verts3,1,10)
        #verts3 = matriz_rotacion(verts3,0,5)
        

        pg.display.flip()
        pg.time.wait(10)

if __name__ == "__main__":
    main()

