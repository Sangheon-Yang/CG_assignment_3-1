import glfw
from OpenGL.GL import *
import numpy as np
from OpenGL.GLU import *
def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-2,2, -2,2, -1,1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    drawFrame()
    t = glfw.get_time()
    
    # blue base transformation
    glPushMatrix() #push.1
    glTranslatef(np.sin(t), 0, 0)
    
    # blue base drawing
    glPushMatrix() #push.2
    drawFrame()
    glScalef(.2, .2, .2)
    glColor3ub(0, 0, 255)
    drawBox()
    glPopMatrix() #pop.1
    
    # red arm transformation
    glPushMatrix() #push.3
    glRotatef(t*(180/np.pi), 0, 0, 1)
    glTranslatef(.5, 0, .01)
    
    # red arm drawing
    glPushMatrix() #push.4
    drawFrame()
    glScalef(.5, .1, .1)
    glColor3ub(255, 0, 0)
    drawBox()
    glPopMatrix() #pop.2

    # green arm transformation
    glPushMatrix() #push.5
    glTranslatef(.5, 0, .01)
    glRotatef(t*(180/np.pi), 0, 0, 1)
    
    
    # grean arm drawing
    glPushMatrix() #push.6
    drawFrame()
    glScalef(.2,.2,.2)
    glColor3ub(0, 255, 0)
    drawBox()
    glPopMatrix() #pop.3
    glPopMatrix() #pop.4
    glPopMatrix() #pop.5
    glPopMatrix() #pop.6



def drawBox():
    glBegin(GL_QUADS)
    glVertex3fv(np.array([1,1,0.]))
    glVertex3fv(np.array([-1,1,0.]))
    glVertex3fv(np.array([-1,-1,0.]))
    glVertex3fv(np.array([1,-1,0.]))
    glEnd()

def drawFrame():
    # draw coordinate: x in red, y in green, z in blue
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,'2015004693-lab6-1', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
