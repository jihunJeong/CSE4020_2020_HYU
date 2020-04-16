import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def render():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    # set the current matrix to the identity matrix
    glLoadIdentity()

    # use orthogonal projection (multiply the current matrix by "projection" matrix - we'll see details later)
    glOrtho(-1,1, -1,1, -1,1)

    # draw global frame
    drawFrame()
    # draw untransformed white triangle
    glColor3ub(255, 255, 255)
    drawTriangle()

    glTranslatef(.6, .0, 0)
    glRotatef(30, 0, 0, 1)
    drawFrame()     # frame defined by TR
    glColor3ub(0, 0, 255)
    drawTriangle()

    drawTriangle()

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()	

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([.0,.5]))
    glVertex2fv(np.array([.0,.0]))
    glVertex2fv(np.array([.5,.0]))
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480, 480, '2016025969', None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
