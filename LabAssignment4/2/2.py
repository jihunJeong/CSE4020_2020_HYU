import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def render(M):
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

    glColor3ub(255, 255, 255)

    glBegin(GL_POINTS)
    glColor3ub(255, 255, 255)
    p = np.array([.5, .0, 1., 1.])
    s = np.identity(4)
    s[:2, :2] = [[2, 0],
                [0, 2]]
    glVertex2fv( (s @ M @ p)[:-2])
    glEnd()

    glBegin(GL_LINES)
    z = np.array([0., 0., 0., 1.])
    v = p - z
    glVertex2fv( (M @ v)[:-2])
    glVertex2fv( (M @ z)[:-2])
    glEnd()

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2016025969", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):
        glfw.poll_events()

        th = glfw.get_time()
        M = np.identity(4)
        M[:3, :3] = np.array([[np.cos(th), -np.sin(th),0.],
          [np.sin(th), np.cos(th),0.],
          [0., 0., 1]])
        
        render(M)
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
