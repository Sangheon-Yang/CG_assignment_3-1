import glfw
import numpy as np
from OpenGL.GL import *

def render(T):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    # draw triangle
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()


metrix_1 = np.array([[1. ,0. ,0.],
                     [0. ,1. ,0.],
                     [0. ,0. ,1.]])


metrix_Q = np.array([[1. ,0. ,-0.1],
                     [0. ,1. ,0.],
                     [0. ,0. ,1.]])


metrix_E = np.array([[1. ,0. ,0.1],
                     [0. ,1. ,0.],
                     [0. ,0. ,1.]])


metrix_W = np.array([[0.9 ,0. ,0.],
                     [0. ,1. ,0.],
                     [0. ,0. ,1.]])


metrix_S = np.array([[np.cos(np.radians(10)) ,-np.sin(np.radians(10)) ,0.],
                     [np.sin(np.radians(10)) ,np.cos(np.radians(10)) ,0.],
                     [0. ,0. ,1.]])

metrix_A = np.array([[np.cos(np.radians(10)) ,-np.sin(np.radians(10)) ,0.],
                     [np.sin(np.radians(10)) ,np.cos(np.radians(10)) ,0.],
                     [0. ,0. ,1.]])

metrix_D = np.array([[np.cos(np.radians(-10)) ,-np.sin(np.radians(-10)) ,0.],
                     [np.sin(np.radians(-10)) ,np.cos(np.radians(-10)) ,0.],
                     [0. ,0. ,1.]])

metrix_current = np.array([[1. ,0. ,0.],
                           [0. ,1. ,0.],
                           [0. ,0. ,1.]])


def key_callback(window, key, scancode ,action, mods):
   
    global metrix_1
    global metrix_Q
    global metrix_E
    global metrix_W
    global metrix_S
    global metrix_A
    global metrix_D
    global metrix_current
    
    if (key==glfw.KEY_1 and (action==glfw.PRESS or action==glfw.REPEAT)):
        metrix_current = metrix_1
    elif(key==glfw.KEY_Q and (action==glfw.PRESS or action==glfw.REPEAT)):
        metrix_current = metrix_Q @ metrix_current
    elif(key==glfw.KEY_E and (action==glfw.PRESS or action==glfw.REPEAT)):
        metrix_current = metrix_E @ metrix_current
    elif(key==glfw.KEY_W and (action==glfw.PRESS or action==glfw.REPEAT)):
        metrix_current = metrix_W @ metrix_current
    elif(key==glfw.KEY_S and (action==glfw.PRESS or action==glfw.REPEAT)):
        metrix_current = metrix_S @ metrix_current
    elif(key==glfw.KEY_A and (action==glfw.PRESS or action==glfw.REPEAT)):
        metrix_current = metrix_current @ metrix_A
    elif(key==glfw.KEY_D and (action==glfw.PRESS or action==glfw.REPEAT)):
        metrix_current = metrix_current @ metrix_D


def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2015004693-3-1", None,None)
    if not window:
        glfw.terminate()
        return

    global metrix_1
    global metrix_Q
    global metrix_E
    global metrix_W
    global metrix_S
    global metrix_A
    global metrix_D
    global metrix_current

    # Make the window's context current
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()
        
        # Render here, e.g. using pyOpenGL
        render(metrix_current)
        
        # Swap front and back buffers
        glfw.swap_buffers(window)
    
    glfw.terminate()

if __name__ == "__main__":
    main()
