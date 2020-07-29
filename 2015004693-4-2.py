import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gCamAng = 0.
gCamHeight = 1.

# draw a cube of side 1, centered at the origin.
def drawUnitCube():
    glBegin(GL_QUADS)
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5) 
                             
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5) 
                             
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
                             
    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)
 
    glVertex3f(-0.5, 0.5, 0.5) 
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5) 
    glVertex3f(-0.5,-0.5, 0.5) 
                             
    glVertex3f( 0.5, 0.5,-0.5) 
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()

def drawCubeArray():
    for i in range(5):
        for j in range(5):
            for k in range(5):
                glPushMatrix()
                glTranslatef(i,j,-k-1)
                glScalef(.5,.5,.5)
                drawUnitCube()
                glPopMatrix()

def drawFrame():
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

def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode( GL_FRONT_AND_BACK, GL_LINE )
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)
# Replace this call with two glRotatef() calls and one glTranslatef() call
    #gluLookAt(3,3,3, 0,0,0, 0,1,0)
    glTranslatef(0,0,-3*np.sqrt(3))
    glRotatef(36.264,1,0,0)
    glRotatef(-45,0,1,0)
    '''
    glTranslatef(0,0,-3*np.sqrt(3))
    glRotatef(-45,0,1,0)
    glRotatef(36.264,1,0,0)
    '''
    
    
    drawFrame()
    glColor3ub(255, 255, 255)
    drawCubeArray()

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

def getUnit(v):
    return (1./np.sqrt(np.dot(v,v)))*v

def myLookAt(eyex, eyey, eyez , atx,aty,atz,upx,upy, upz):
    eye = np.array([eyex,eyey,eyez])
    at = np.array([atx,aty,atz])
    up = np.array([upx,upy,upz])
    forward_c = getUnit(eye - at)
    side_c = getUnit(np.cross(up,forward_c))
    up_c = np.cross(forward_c , side_c)
    pos_cx = -np.dot(eye , side_c)
    pos_cy = -np.dot(eye , up_c)
    pos_cz = -np.dot(eye , forward_c)

    Mr = np.array([[ side_c[0], side_c[1] , side_c[2] , pos_cx],
                  [ up_c[0]  , up_c[1] , up_c[2] , pos_cy],
                  [ forward_c[0], forward_c[1] , forward_c[2] , pos_cz],
                  [ 0,  0 , 0, 1.0]])
                  
    glMultMatrixf(Mr.T)

def myOrtho(l , r , b , t , zN , zF):
    Mr = np.array([[2/(r-l) ,0 ,0 ,-(r+l)/(r-l) ],
                   [0 ,2/(t-b) ,0 ,-(t+b)/(t-b)],
                   [0 ,0 , 2/(zN-zF),-(zN+zF)/(zN-zF)],
                   [0 ,0 ,0 , 1]])
    glMultMatrixf(Mr.T)

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,'2015004693-4-2', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
