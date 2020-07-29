import glfw
import numpy as np
from OpenGL.GL import *


def render(n):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    if(n==1):
        glBegin(GL_POINTS)
    elif(n==2):
        glBegin(GL_LINES)
    elif(n==3):
        glBegin(GL_LINE_STRIP)
    elif(n==4):
        glBegin(GL_LINE_LOOP)
    elif(n==5):
        glBegin(GL_TRIANGLES)
    elif(n==6):
        glBegin(GL_TRIANGLE_STRIP)
    elif(n==7):
        glBegin(GL_TRIANGLE_FAN)
    elif(n==8):
        glBegin(GL_QUADS)
    elif(n==9):
        glBegin(GL_QUAD_STRIP)
    elif(n==0):
        glBegin(GL_POLYGON)
    else:
        glBegin(GL_LINE_LOOP)
    #    glBegin(GL_LINE_LOOP)
    ar = np.arange(12)
    for i in ar:
        glVertex2f( np.cos(np.radians(i*30.0)), np.sin(np.radians(i*30.0)) )
    glEnd()

mode = 4

def key_callback(window, key, scancode ,action, mods):
    global mode
    if (key==glfw.KEY_1 and action==glfw.PRESS):
        mode = 1
    elif(key==glfw.KEY_2 and action==glfw.PRESS):
        mode = 2
    elif(key==glfw.KEY_3 and action==glfw.PRESS):
        mode = 3
    elif(key==glfw.KEY_4 and action==glfw.PRESS):
        mode = 4
    elif(key==glfw.KEY_5 and action==glfw.PRESS):
        mode = 5
    elif(key==glfw.KEY_6 and action==glfw.PRESS):
        mode = 6
    elif(key==glfw.KEY_7 and action==glfw.PRESS):
        mode = 7
    elif(key==glfw.KEY_8 and action==glfw.PRESS):
        mode = 8
    elif(key==glfw.KEY_9 and action==glfw.PRESS):
        mode = 9
    elif(key==glfw.KEY_0 and action==glfw.PRESS):
        mode = 0


def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(480,480,"2015004693_양상헌", None,None)
    if not window:
        glfw.terminate()
        return
    
    # Make the window's context current
    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)

# Loop until the user closes the window
    while not glfw.window_should_close(window):
        global mode
        # Poll events
        glfw.poll_events()
        
        # Render here, e.g. using pyOpenGL
        render(mode)
        #key = glfw.KEY_4
        #key_callback(window , key , scancode , action, mods)
        
        # Swap front and back buffers
        glfw.swap_buffers(window)
    
    glfw.terminate()

if __name__ == "__main__":
    main()

