import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

global key_input
key_input = []

def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # draw coordinate system: x in red, y in green, z in blue
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()

    # draw triangle
    glColor3ub(255, 255, 255)
    global key_input
    for i in range(len(key_input)):
        #glLoadIdentity()
        nM = np.identity(4)
        if chr(key_input[i]) == 'Q':
            nM[0][3] = -0.1
        elif chr(key_input[i]) == 'E':
            nM[0][3] = 0.1
        elif chr(key_input[i]) == 'A':
            th = np.radians(10)
            nM[:3,:3] = [[np.cos(th), -np.sin(th), 0],
                        [np.sin(th), np.cos(th), 0],
                        [0, 0, 0]]
        elif chr(key_input[i]) == 'D':
            th = np.radians(10)
            nM[:3,:3] = [[np.cos(th), np.sin(th), 0],
                        [-np.sin(th), np.cos(th), 0],
                        [0, 0, 0]]
        elif chr(key_input[i]) == '1':
            key_input = []
            glLoadIdentity()
            break
        glMultMatrixf(nM.T)
    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([.0,.5]))
    glVertex2fv(np.array([.0,.0]))
    glVertex2fv(np.array([.5,.0]))
    glEnd()


def key_callback(window, key, scancode, action, mods):
    # rotate the camera when 1 or 3 key is pressed or repeated
    if action==glfw.PRESS:
        global key_input
        key_input.insert(0, key)

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480, 480, '2016025969', None,None)
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
