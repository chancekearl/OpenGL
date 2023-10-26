import sys
import numpy as np

try:
    from OpenGL.GLUT import *
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GL import glOrtho
    from OpenGL.GLU import gluPerspective
    from OpenGL.GL import glRotated
    from OpenGL.GL import glTranslated
    from OpenGL.GL import glLoadIdentity
    from OpenGL.GL import glMatrixMode
    from OpenGL.GL import GL_MODELVIEW
    from OpenGL.GL import GL_PROJECTION
except:
    print("ERROR: PyOpenGL not installed properly. ")

DISPLAY_WIDTH = 500.0
DISPLAY_HEIGHT = 500.0
TRANSLATE = [0,-3,-10]
ROTATE = [0,0,0]
PERSP = [1]
CAR_DIST = 0
TIRE_ROT = 0

def init(): 
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glShadeModel (GL_FLAT)

 
def drawCar():
	glLineWidth(2.5)
	glColor3f(0.0, 1.0, 0.0)
	glBegin(GL_LINES)
	#Front Side
	glVertex3f(-3, 2, 2)
	glVertex3f(-2, 3, 2)
	glVertex3f(-2, 3, 2)
	glVertex3f(2, 3, 2)
	glVertex3f(2, 3, 2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 1, 2)
	glVertex3f(3, 1, 2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 2, 2)
	#Back Side
	glVertex3f(-3, 2, -2)
	glVertex3f(-2, 3, -2)
	glVertex3f(-2, 3, -2)
	glVertex3f(2, 3, -2)
	glVertex3f(2, 3, -2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 1, -2)
	glVertex3f(3, 1, -2)
	glVertex3f(-3, 1, -2)
	glVertex3f(-3, 1, -2)
	glVertex3f(-3, 2, -2)
	#Connectors
	glVertex3f(-3, 2, 2)
	glVertex3f(-3, 2, -2)
	glVertex3f(-2, 3, 2)
	glVertex3f(-2, 3, -2)
	glVertex3f(2, 3, 2)
	glVertex3f(2, 3, -2)
	glVertex3f(3, 2, 2)
	glVertex3f(3, 2, -2)
	glVertex3f(3, 1, 2)
	glVertex3f(3, 1, -2)
	glVertex3f(-3, 1, 2)
	glVertex3f(-3, 1, -2)
	glEnd()
	
def drawTire():
	glLineWidth(2.5)
	glColor3f(0.0, 0.0, 1.0)
	glBegin(GL_LINES)
	#Front Side
	glVertex3f(-1, .5, .5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(.5, 1, .5)
	glVertex3f(.5, 1, .5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, -.5, .5)
	glVertex3f(1, -.5, .5)
	glVertex3f(.5, -1, .5)
	glVertex3f(.5, -1, .5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, .5, .5)
	#Back Side
	glVertex3f(-1, .5, -.5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-1, -.5, -.5)
	glVertex3f(-1, -.5, -.5)
	glVertex3f(-1, .5, -.5)
	#Connectors
	glVertex3f(-1, .5, .5)
	glVertex3f(-1, .5, -.5)
	glVertex3f(-.5, 1, .5)
	glVertex3f(-.5, 1, -.5)
	glVertex3f(.5, 1, .5)
	glVertex3f(.5, 1, -.5)
	glVertex3f(1, .5, .5)
	glVertex3f(1, .5, -.5)
	glVertex3f(1, -.5, .5)
	glVertex3f(1, -.5, -.5)
	glVertex3f(.5, -1, .5)
	glVertex3f(.5, -1, -.5)
	glVertex3f(-.5, -1, .5)
	glVertex3f(-.5, -1, -.5)
	glVertex3f(-1, -.5, .5)
	glVertex3f(-1, -.5, -.5)
	glEnd()

def drawHouse ():
    glLineWidth(2.5)
    glColor3f(1.0, 0.0, 0.0)
    #Floor
    glBegin(GL_LINES)
    glVertex3f(-5.0, 0.0, -5.0)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 0, -5)
    #Ceiling
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 5, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, 5)
    glVertex3f(-5, 5, -5)
    #Walls
    glVertex3f(-5, 0, -5)
    glVertex3f(-5, 5, -5)
    glVertex3f(5, 0, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(5, 0, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(-5, 0, 5)
    glVertex3f(-5, 5, 5)
    #Door
    glVertex3f(-1, 0, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(-1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 3, 5)
    glVertex3f(1, 0, 5)
    #Roof
    glVertex3f(-5, 5, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(0, 8, -5)
    glVertex3f(5, 5, -5)
    glVertex3f(-5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(5, 5, 5)
    glVertex3f(0, 8, 5)
    glVertex3f(0, 8, -5)
    glEnd()

def display():
    glClear (GL_COLOR_BUFFER_BIT)
    glColor3f (1.0, 1.0, 1.0)
    # viewing transformation 

    #Your Code Here
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if PERSP[0] == 1:
        gluPerspective(60, 1, 1, 500)
    else:
        glOrtho(-8, 8, -8, 8, 0.1, 500.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glRotated(ROTATE[1], 0, -1, 0)   
    glTranslated(TRANSLATE[0], TRANSLATE[1], TRANSLATE[2])
    
    glPushMatrix()

    shift = -15
    for i in range(3):
        glPushMatrix()
        glTranslated(shift,0,-20)
        drawHouse()
        glPopMatrix()
        shift += 15
    shift = -15
    for i in range(3):
        glPushMatrix()
        glRotated(180,0,1,0)
        glTranslated(shift,0,-20)
        drawHouse()
        glPopMatrix()
        shift += 15
    glPushMatrix()
    glRotated(90,0,1,0)
    glTranslated(0,0,-30)
    drawHouse()
    glPopMatrix()

    glPushMatrix()
    glTranslated(-10 + CAR_DIST,0.0025,0)
    drawCar()
    offset = 2.5
    for i in range(2):
        glPushMatrix()
        glTranslated(offset,-0.2,1.5)
        glRotated(0 - TIRE_ROT, 0,0,1)
        drawTire()
        glPopMatrix()
        offset = -2.5
    offset = 2.5
    for i in range(2):
        glPushMatrix()
        glTranslated(offset,-0.2,-1.5)
        glRotated(0 - TIRE_ROT, 0,0,1)
        drawTire()
        glPopMatrix()
        offset = -2.5
    glPopMatrix()
    
    glPopMatrix()
    
    glFlush()


def timer(value):
    global CAR_DIST
    global TIRE_ROT
    CAR_DIST += 0.6
    TIRE_ROT += 18
    glutTimerFunc(100, timer, 0)
    glutPostRedisplay()
    

def keyboard(key, x, y):
    global CAR_DIST
    global TIRE_ROT
    
    if key == chr(27):
        import sys
        sys.exit(0)
  
    if key == b'r':
        TRANSLATE[1] -= 1

    if key ==b'q':
        ROTATE[1] += 1

    if key ==b'e':
        ROTATE[1] -= 1

    if key ==b'a':
        TRANSLATE[2] += np.cos(np.radians(ROTATE[1] + 90))
        TRANSLATE[0] += np.sin(np.radians(ROTATE[1] + 90))

    if key ==b'f':
        TRANSLATE[1] += 1

    if key ==b'd':
        TRANSLATE[2] += np.cos(np.radians(ROTATE[1] - 90))
        TRANSLATE[0] += np.sin(np.radians(ROTATE[1] - 90))

    if key ==b'w':
        TRANSLATE[2] += np.cos(np.radians(ROTATE[1]))
        TRANSLATE[0] += np.sin(np.radians(ROTATE[1]))

    if key ==b's':
        TRANSLATE[2] -= np.cos(np.radians(ROTATE[1]))
        TRANSLATE[0] -= np.sin(np.radians(ROTATE[1]))
        
    if key ==b'h':
        TRANSLATE[0] = 0
        TRANSLATE[1] = -3
        TRANSLATE[2] = -10
        ROTATE[0] = 0
        ROTATE[1] = 0
        ROTATE[2] = 0
        CAR_DIST = 0
        TIRE_ROT = 0

    if key==b'i':
        CAR_DIST = 0
        TIRE_ROT = 0

    if key ==b'o':
        PERSP[0] = 0

    if key ==b'p':
        PERSP[0] = 1


    glutPostRedisplay()


glutInit(sys.argv)
glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize (int(DISPLAY_WIDTH), int(DISPLAY_HEIGHT))
glutInitWindowPosition (100, 100)
glutCreateWindow (b'OpenGL Lab')
init ()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
timer(0)
glutMainLoop()
