import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *



vertices= (
    ( 1, 1, 1),
    (-1, 1, 1),
    (-1,-1, 1),
    ( 1,-1, 1)
)


edges = (
    (0,1),
    (0,3),
    (2,1),
    (2,3),
)

DEG2RAD = 3.14159/180;

def Cube():
	glBegin(GL_LINES)
	for edge in edges:
		for vertex in edge:
			glVertex3fv(vertices[vertex])
	glEnd()

 
def drawCircle(radius, x, y):
   glBegin(GL_LINE_LOOP);
 
   for i in range(0,360):
      degInRad = i*DEG2RAD;
      glVertex2f(math.cos(degInRad)*radius+x,math.sin(degInRad)*radius+y)
 
   glEnd();

def drawEdge(x1, y1, x2, y2, r):
    glBegin(GL_LINES)
    glVertex2f(x1,y1)
    glVertex2f(x2,y2)
    glEnd()

def main():
	pygame.init()
	display = (800,600)
	pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
	gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
	# glTranslatef(0.0,0.0, -5)
        glTranslatef(0.0,0.0, -1)

	while True:
        	for event in pygame.event.get():
            		if event.type == pygame.QUIT:
                		pygame.quit()
                		quit()
#        	glRotatef(1, 3, 1, 1)
         	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        	# Cube()
                drawCircle(.1,.2,.2)
                drawCircle(.1,-.2,.2)
                drawEdge(.2,.2,-.2,.2, .1)
        	pygame.display.flip()
        	pygame.time.wait(10)


main()
