###################################################
# [Practice] First OpenGL Program import glfw
from OpenGL.GL import *
import numpy as np
import glfw

gstring = [GL_POLYGON, GL_POINTS, GL_LINES, GL_LINE_STRIP, GL_LINE_LOOP, GL_TRIANGLES, GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN, GL_QUADS, GL_QUAD_STRIP, GL_POLYGON]

def render(str):
	glClear(GL_COLOR_BUFFER_BIT)
	glLoadIdentity()

	radius = 1.0

	vx = np.linspace(0.0, 360.0, 13)
	vy = np.linspace(0.0, 360.0, 13)
	glBegin(str)
	for i in range(12):
		glVertex2f(np.cos(vx[i]*np.pi/180.), np.sin(vy[i]*np.pi/180))
	glEnd()

def key_callback(window, key, scancode, action, mods):
	render(gstring[key-48])

def main():
    # Initialize the library
    if not glfw.init():
        return
    # Create a windowed mode window and its OpenGL context
	#2.A
    window = glfw.create_window(480,480,"2016025969", None,None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)
    render(gstring[4])
    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Poll events
        glfw.poll_events()
        # Render here, e.g. using pyOpenGL
        
		#render()
        glfw.set_key_callback(window, key_callback)
		# Swap front and back buffers
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

