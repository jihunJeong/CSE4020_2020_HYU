import glfw
from OpenGL.GL import *
import numpy as np

gComposedM = np.array([[1, 0, 0],
                      [0, 1, 0],
                      [0.,0.,1.]])
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
    # draw triangle - p'=Mp
    glBegin(GL_TRIANGLES)
    glColor3ub(255, 255, 255)
    glVertex2fv( (T @ np.array([.0,.5,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.0,.0,1.]))[:-1] )
    glVertex2fv( (T @ np.array([.5,.0,1.]))[:-1] )
    glEnd()

def key_callback(window, key, scancode, action, mods):
    global gComposedM

    if chr(key) == 'W'and action == glfw.PRESS:
        newM = np.array([[0.9, 0, 0],
                      [0, 1, 0],
                      [0.,0.,1.]])
        gComposedM = newM @ gComposedM
    elif chr(key) == 'E'and action == glfw.PRESS:
        newM = np.array([[1.1, 0, 0],
                      [0, 1, 0],
                      [0.,0.,1.]])
        gComposedM = newM @ gComposedM
    elif chr(key) == 'S' and action == glfw.PRESS:
        th = np.radians(10)
        newM = np.array([[np.cos(th), -np.sin(th), 0],
                      [np.sin(th), np.cos(th), 0],
                      [0.,0.,1.]])
        gComposedM = newM @ gComposedM
    elif chr(key) == 'D' and action == glfw.PRESS:
        th = np.radians(10)
        newM = np.array([[np.cos(th), np.sin(th), 0],
                      [-np.sin(th), np.cos(th), 0],
                      [0.,0.,1.]])
        gComposedM = newM @ gComposedM
    elif chr(key) == 'X' and action == glfw.PRESS:
        newM = np.array([[1, -0.1, 0],
                      [0, 1, 0],
                      [0.,0.,1.]])
        gComposedM = newM @ gComposedM
    elif chr(key) == 'C' and action == glfw.PRESS:
        newM = np.array([[1, 0.1, 0],
                      [0, 1, 0],
                      [0.,0.,1.]])
        gComposedM = newM @ gComposedM
    elif chr(key) == 'R' and action == glfw.PRESS:
        newM = np.array([[1, 0, 0],
                      [0, -1, 0],
                      [0.,0.,1.]])
        gComposedM = newM @ gComposedM
    
    if chr(key) == '1' and action == glfw.PRESS:
         gComposedM = np.array([[1, 0, 0],
                      [0, 1, 0],
                      [0.,0.,1.]])

def main():
    if not glfw.init():
        return
    window = glfw.create_window(480,480,"2016025969", None,None)
    if not window:
        glfw.terminate()
        return
    glfw.set_key_callback(window, key_callback)
    glfw.make_context_current(window)
     
    render(gComposedM)
    while not glfw.window_should_close(window):
        glfw.poll_events()
         
        render(gComposedM)
        
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
